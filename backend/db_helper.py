from functools import partial
from typing import Callable, Optional, List, TypeVar

import mysql.connector
from mysql.connector import errorcode
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.types import RowType

from config import DB_HOST, DB_USER, DB_DATABASE, DB_PASSWORD

_T = TypeVar("_T", List[RowType], Optional[RowType], str, Exception)


def cm_cursor() -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> _T:
            global conn
            if not isinstance(conn, MySQLConnectionAbstract):
                _conn = _create_conn()
                assert _conn
                assert _conn.is_connected(), "La db est injoinable"
                conn = _conn

            cursor = kwargs.get("cursor", None)
            if cursor:
                kwargs.pop("cursor")
            else:
                cursor = conn.cursor()

            try:
                res = func(cursor=cursor, *args, **kwargs)
            except Exception as e:
                res = e
            cursor.close()
            return res

        return wrapper

    return decorator


def create_conn(
        host: str, user: str, password: str, database: str
) -> Optional[MySQLConnectionAbstract]:
    global conn
    try:
        connexion = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print(
                "Erreur d'authentification : Vérifiez votre nom d'utilisateur et votre mot de passe."
            )
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print(
                "Base de données non existante : Vérifiez le nom de la base de données."
            )
        else:
            print(f"Erreur MySQL non gérée : {err}")
        connexion = None
    conn = connexion
    return connexion


_create_conn = partial(
    create_conn, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE
)
conn: Optional[MySQLConnectionAbstract] = _create_conn()


def cm_conn() -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> bool:
            global conn
            if not isinstance(conn, MySQLConnectionAbstract):
                _conn: Optional[MySQLConnectionAbstract] = _create_conn()
                if _conn is None or not _conn.is_connected():
                    return False
                conn = _conn

            res = func(*args, **kwargs)
            if isinstance(res, Exception):
                conn.rollback()
                return False
            else:
                conn.commit()
                return True

        return wrapper

    return decorator
