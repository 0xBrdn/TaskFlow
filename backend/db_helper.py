from functools import partial
from typing import Callable, Optional, List, Union, TypeAlias

import mysql.connector
from mysql.connector import errorcode
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.types import RowType

from config import DB_HOST, DB_USER, DB_DATABASE, DB_PASSWORD

ResultType: TypeAlias = Union[List[RowType], Optional[RowType], str, Exception]


def cm_cursor() -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> ResultType:
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
) -> Optional[Union[MySQLConnectionAbstract, PooledMySQLConnection]]:
    global conn
    try:
        connexion = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(
                "Accès refusé. Vérifiez votre nom d'utilisateur ou votre mot de passe.")  # Ne doit pas apparaitre sauf si mal config coté server
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de données spécifiée n'existe pas.")
        elif err.errno == errorcode.CR_CONN_HOST_ERROR:
            print("Impossible de se connecter au serveur mysql (mauvaise ip ?).")
        elif err.errno == errorcode.CR_CONNECTION_ERROR:
            print("Erreur de connexion à la base de données.")
        elif err.errno == errorcode.CR_SERVER_LOST:
            print("La connexion au serveur MySQL a été perdue.")
        else:
            print(f"Erreur MySQL: {err}")
        connexion = None
    conn = connexion
    return connexion


_create_conn = partial(
    create_conn, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE
)
conn: Optional[Union[MySQLConnectionAbstract, PooledMySQLConnection]] = _create_conn()


def cm_conn() -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> bool:
            global conn
            if not isinstance(conn, MySQLConnectionAbstract):
                _conn: Optional[Union[MySQLConnectionAbstract, PooledMySQLConnection]] = _create_conn()
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
