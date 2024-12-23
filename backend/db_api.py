import datetime
import logging
from typing import Optional, Union

# --- Argon2
from argon2 import PasswordHasher
from argon2 import exceptions as argon2_exceptions

# --- Votre décorateur et requêtes
from mysql.connector.cursor import MySQLCursor
from backend.db_helper import cm_cursor, ResultType, cm_conn
from backend.db_requests import _Requests

_log = logging.getLogger(__name__)

# Instanciation globale du PasswordHasher
ph = PasswordHasher()


class DB_API:
    """
    Classe permettant d'exécuter les commandes vers la DB SQL.
    """

    @staticmethod
    @cm_cursor()
    def check_user_credentials(email: str, plain_password: str, *, cursor: MySQLCursor) -> bool:
        """
        Vérifie si l'utilisateur 'email' existe et si le mot de passe 'plain_password'
        correspond (Argon2). Retourne True si OK, sinon False.
        """
        # Récupère le hash stocké dans la table `users` (champ "password")
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if not row:
            return False  # Email inconnu

        hashed_password = row[0]
        if not hashed_password:
            return False  # Pas de mot de passe stocké => compte Google ?

        try:
            # Vérifier via Argon2
            ph.verify(hashed_password, plain_password)
            # Si les paramètres Argon2 ont changé, on peut re-hasher
            if ph.check_needs_rehash(hashed_password):
                new_hash = ph.hash(plain_password)
                cursor.execute(
                    "UPDATE users SET password = %s WHERE email = %s", (new_hash, email)
                )
            return True
        except argon2_exceptions.VerifyMismatchError:
            return False
        except Exception:
            return False

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def add_user(
        username: str, password: str, email: str, is_google_user: bool, *, cursor: MySQLCursor
    ) -> Union[Exception, Optional[int]]:
        """
        Ajoute un nouvel utilisateur dans la DB.
        - Si is_google_user == False, hache le password (Argon2).
        - Sinon, on stocke un placeholder (ex: "").
        Retourne l'ID (userID) inséré, ou un objet Exception en cas d'erreur.
        """
        if not is_google_user:
            try:
                # Hachage Argon2 du mot de passe
                password = ph.hash(password)
            except Exception as e:
                return e
        else:
            # Compte Google => mot de passe vide ou placeholder
            password = ""

        # Insertion en DB
        try:
            # Ici, _Requests.add_user doit être une requête du type:
            # "INSERT INTO users (username, password, email, is_google_user) VALUES (%s, %s, %s, %s);" # noqa
            cursor.execute(_Requests.add_user, (username, password, email, is_google_user))
            return cursor.lastrowid
        except Exception as e:
            return e

    @staticmethod
    @cm_cursor()
    def get_email_hashpass(email: str, *, cursor: MySQLCursor) -> Union[tuple, Exception, None]:
        """
        Retourne (hashed_password,) pour un utilisateur donné par son email,
        ou None si non trouvé, ou Exception si erreur DB.
        (Fonction legacy, vous pouvez la garder si du code l'utilise.)
        """
        try:
            cursor.execute(_Requests.get_email_hashpass, (email,))
            row = cursor.fetchone()
            if row:
                return (row[0],)  # pour rester compatible
            else:
                return None
        except Exception as e:
            return e

    @staticmethod
    @cm_cursor()
    def get_all_users(*, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer tous les utilisateurs de la DB.

        Cette fonction renvoie une liste de tuples comprenant les
        users sous la forme (userID, username, email, is_google_user).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie None ou dans certains cas, un objet de type Exception.

        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> users = DB_API.get_all_users()
        >>> if users and not isinstance(users, Exception):
        >>>     print(users)

        """
        cursor.execute(_Requests.get_all_users)
        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_cursor()
    def get_project_id_by_project_name(project_name: str, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer le project id en fonction du project name de la DB.

        Cette fonction renvoie un tuple comprenant le project id
        sous la forme (project_id,).
        Cette fonction peut ne pas fonctionner, dans ce cas elle

        :param project_name: Nom du projet
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> project_id = DB_API.get_project_id_by_project_name()
        >>> if project_id and not isinstance(project_id, Exception):
        >>>     print(project_id)

        """
        cursor.execute(_Requests.get_project_id_by_project_name, (project_name,))

        result = cursor.fetchone()
        return result

    @staticmethod
    @cm_cursor()
    def get_email_hashpass(email: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer le mdp hash d'un user en fonction de l'email dans la DB.

        Cette fonction renvoie un tuple comprenant uniquement le
        mot de passe hash de la personne.
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie un objet de type Exception.

        :param email: Email de l'utilisateur
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> hash_pass = DB_API.get_email_hashpass(1)
        >>> if not isinstance(hash_pass, Exception):
        >>>     print(hash_pass)
        """
        cursor.execute(_Requests.get_email_hashpass, (email,))
        result = cursor.fetchone()
        return result

    @staticmethod
    @cm_cursor()
    def get_user_hashpass(user_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer le mdp hash d'un user dans la DB.

        Cette fonction renvoie un tuple comprenant uniquement le
        mot de passe hash de la personne.
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie None.

        :param user_id: ID de l'utilisateur
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> hash_pass = DB_API.get_user_hashpass(1)
        >>> if hash_pass and not isinstance(:
        >>>     print(hash_pass)
        """
        cursor.execute(_Requests.get_user_hashpass, (user_id,))
        result = cursor.fetchone()
        return result

    @staticmethod
    @cm_cursor()
    def get_projects_by_user_id(user_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer tous les projets d'un utilisateur en fonction de son userID.

        Cette fonction renvoie une liste de tuples comprenant les
        projets sous la forme (projectID, name, joined).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie None ou dans certains cas, un objet de type Exception.

        :param user_id: ID de l'utilisateur
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> projects = DB_API.get_projects_by_user_id(1)
        >>> if projects and not isinstance(projects, Exception):
        >>>     print(projects)
        """
        cursor.execute(_Requests.get_projects_by_user_id, (user_id,))

        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_cursor()
    def get_tasks_by_project_id(project_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer toutes les taches d'un projet en fonction de son projectID.

        Cette fonction renvoie une liste de tuples comprenant les
        taches sous la forme (taskID, title, description, status,
        priority, covered, assign, dead_line).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie None ou dans certains cas, un objet de type Exception.

        :param project_id: projectID
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> tasks = DB_API.get_tasks_by_project_id(1)
        >>> if tasks and not isinstance(tasks, Exception):
        >>>     print(tasks)
        """
        cursor.execute(_Requests.get_tasks_by_project_id, (project_id,))

        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_cursor()
    def get_subtasks_by_task_id(task_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer toutes les sous taches d'un projet en fonction de son taskID.

        Cette fonction renvoie une liste de tuples comprenant les
        sous taches sous la forme (subtaskID, title, description, status,
        priority, covered, assign, dead_line).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie None ou dans certains cas, un objet de type Exception.

        :param task_id: taskID
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> subtasks = DB_API.get_subtasks_by_task_id(1)
        >>> if subtasks and not isinstance(subtasks, Exception):
        >>>     print(subtasks)
        """
        cursor.execute(_Requests.get_subtasks_by_task_id, (task_id,))

        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_cursor()
    def get_user_logs_by_id(log_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer toutes les logs d'un user grace a son userID.

        Cette fonction renvoie une liste de tuples comprenant les
        logs sous la forme (logID, action, action_time, details).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie None ou dans certains cas, un objet de type Exception.

        :param log_id: logID
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> logs = DB_API.get_user_logs_by_id(1)
        >>> if logs and not isinstance(logs, Exception):
        >>>     print(logs)
        """
        cursor.execute(_Requests.get_user_logs_by_id, (log_id,))

        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_cursor()
    def get_users_in_project_by_project_id(project_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer toutes users dans un projet en fonction du projectID.

        Cette fonction renvoie une liste de tuples comprenant les
        projets de l'user sous la forme (userID, username, permission).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie None ou dans certains cas, un objet de type Exception.

        :param project_id: projectID
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> users_in_project = DB_API.get_users_in_project_by_project_id(1)
        >>> if users_in_project and not isinstance(users_in_project, Exception):
        >>>     print(users_in_project)
        """
        cursor.execute(_Requests.get_users_in_project_by_project_id, (project_id,))
        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_cursor()
    def get_tasks_by_user_id(user_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer toutes les taches d'un utilisateur en fonction de son userID.

        Cette fonction renvoie une liste de tuples comprenant les taches
        sous la forme (taskID, title, description, status, priority, covered, assign, dead_line).
        Cette fonction peut ne pas fonctionner, dans ce cas
        elle renvoie un objet de type Exception.

        :param user_id: ID de l'utilisateur
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> user_tasks = DB_API.get_tasks_by_user_id(1)
        >>> if user_tasks and not isinstance(user_tasks, Exception):
        >>>     print(user_tasks)
        """
        cursor.execute(_Requests.get_tasks_by_user_id, (user_id,))
        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_cursor()
    def get_users_in_tasks_group_by_group_id(group_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer tous les utilisateurs dans un groupe
        de tâches en fonction de son groupID.

        Cette fonction renvoie une liste de tuples comprenant les
        utilisateurs sous la forme (userID, username, task_projectID).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie None ou dans certains cas, un objet de type Exception.

        :param group_id: groupID
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> users_in_group = DB_API.get_users_in_tasks_group_by_group_id(1)
        >>> if users_in_group and not isinstance(users_in_group, Exception):
        >>>     print(users_in_group)
        """
        cursor.execute(_Requests.get_users_in_tasks_group_by_group_id, (group_id,))
        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_cursor()
    def get_all_status(*, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer les statuts de tous les users dans la DB.

        Cette fonction renvoie une liste de tuples comprenant les
        statuts sous la forme (userID, status), note : statut = (0 = deco; 1 = connect; 2 = idle).
        Cette fonction peut ne pas fonctionner, dans ce cas elle renvoie un objet
        de type Exception.
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> status = DB_API.get_all_status()
        >>> if status and not isinstance(status, Exception):
        >>>     print(status)
        """
        cursor.execute(_Requests.get_all_status)
        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def add_status(
        user_id: int, status: int, *, cursor: MySQLCursor
    ) -> Union[Exception, Optional[int]]:
        """
        Permet d'ajouter un statut à un utilisateur.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param user_id: ID de l'utilisateur
        :param status: Statut à ajouter (0 = deco; 1 = connect; 2 = idle)
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> status_id = DB_API.add_status(1, 0)
        >>> if status_id and not isinstance(status_id, Exception):
        >>>     print(status_id)
        """
        cursor.execute(_Requests.add_status, (user_id, status))
        return cursor.lastrowid

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def add_project(name: str, *, cursor: MySQLCursor) -> Union[Exception, Optional[int]]:
        """
        Permet d'ajouter un nouveau projet à la DB.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param name: Nom du projet
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> project_id = DB_API.add_project("project_test")
        >>> if project_id and not isinstance(project_id, Exception):
        >>>     print(project_id)
        """
        cursor.execute(_Requests.add_project, (name,))
        return cursor.lastrowid

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def add_user_to_group(
        project_id: int, user_id: int, permission: int, joined: bool, *, cursor: MySQLCursor
    ) -> Union[Exception, Optional[int]]:
        """
        Permet d'ajouter un utilisateur à un groupe de projet.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param project_id: ID du projet
        :param user_id: ID de l'utilisateur
        :param permission: Permission de l'utilisateur dans le projet
        (0 = read, 1 = write, 2 = admin)
        :param joined: Date d'ajout à la groupe
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> user_group_id = DB_API.add_user_to_group(1, 1, 1, True)
        >>> if user_group_id and not isinstance(user_group_id, Exception):
        >>>     print(user_group_id)
        """
        cursor.execute(_Requests.add_user_to_group, (project_id, user_id, permission, joined))
        return cursor.lastrowid

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def add_task_info(
        status: int,
        priority: int,
        title: str,
        description: str,
        dead_line: datetime.datetime,
        covered: bool,
        assign: int,
        *,
        cursor: MySQLCursor,
    ) -> Union[Exception, Optional[int]]:
        """
        Permet d'ajouter des informations sur une tâche.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param status: Statut de la tâche
        :param priority: Priorité de la tâche (0 = basse; 1 = moyenne; 2= haute)
        :param title: Titre de la tâche
        :param description: Description de la tâche
        :param dead_line: Date limite de la tâche (datetime.datetime,
         le field dans la db est TIMESTAMP)
        :param covered: Informations sur la couverture de la tâche (bool)
        :param assign: task_projectID (lie la tache a un ou plusieurs
         user a travers la table tasks_groups)
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> taskinfo_id = DB_API.add_task_info(1, 2, "titre tache",
        "ceci est une description de la tache", datetime.datetime.now(), False, 1)
        >>> if taskinfo_id and not isinstance(taskinfo_id, Exception):
        >>>     print(taskinfo_id)
        """
        cursor.execute(
            _Requests.add_task_info,
            (status, priority, title, description, dead_line, covered, assign),
        )

        return cursor.lastrowid

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def add_task(
        project_id: int, task_info_id: int, user_id: int, *, cursor: MySQLCursor
    ) -> Union[Exception, Optional[int]]:
        """
        Permet d'ajouter une tâche à un projet.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param project_id: ID du projet
        :param task_info_id: ID des informations de la tâche
        :param user_id: ID de l'utilisateur assigné
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> task_id = DB_API.add_task(1, 1, 1)
        >>> if task_id and not isinstance(task_id, Exception):
        >>>     print(task_id)
        """
        cursor.execute(_Requests.add_task, (project_id, task_info_id, user_id))

        return cursor.lastrowid

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def add_subtask(
        task_id: int, task_info_id: int, *, cursor: MySQLCursor
    ) -> Union[Exception, Optional[int]]:
        """
        Permet d'ajouter une sous-tâche à une tâche.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param task_id: ID de la tâche parente
        :param task_info_id: ID des informations de la sous-tâche
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> subtask_id = DB_API.add_subtask(1, 1)
        >>> if subtask_id and not isinstance(subtask_id, Exception):
        >>>     print(subtask_id)
        """
        cursor.execute(_Requests.add_subtask, (task_id, task_info_id))

        return cursor.lastrowid

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def add_user_to_task_group(
        task_project_id: int, user_id: int, *, cursor: MySQLCursor
    ) -> Union[Exception, Optional[int]]:
        """
        Permet d'ajouter un utilisateur à un groupe de tâches.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param task_project_id: ID du projet de la tâche
        :param user_id: ID de l'utilisateur à ajouter
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> users_tasks_groups_id = DB_API.add_user_to_task_group(1, 1)
        >>> if users_tasks_groups_id and not isinstance(users_tasks_groups_id, Exception):
        >>>     print(users_tasks_groups_id)
        """
        cursor.execute(_Requests.add_user_to_task_group, (task_project_id, user_id))

        return cursor.lastrowid

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def add_user_log(
        user_id: int, action: str, details: str, *, cursor: MySQLCursor
    ) -> Union[Exception, Optional[int]]:
        """
        Permet d'ajouter une log d'action pour un utilisateur.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param user_id: ID de l'utilisateur
        :param action: Action réalisée par l'utilisateur
        :param details: Détails de l'action
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> user_log_id = DB_API.add_user_log(1, "affect", "user to task")
        >>> if user_log_id and not isinstance(user_log_id, Exception):
        >>>     print(user_log_id)
        """
        cursor.execute(_Requests.add_user_log, (user_id, action, details))

        return cursor.lastrowid

    @staticmethod
    @cm_cursor()
    def get_user_id_by_username(username: str, *, cursor: MySQLCursor) -> Optional[int]:
        """
        Permet de recup les projets dans la db.

        Cette fonction renvoie l'user id.
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie None ou dans certains cas, un objet de type Exception.

        :param username: Username de l'utilisateur
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> user_id = DB_API.get_user_id_by_username("toto")
        >>> if user_id and not isinstance(user_id, Exception):
        >>>     print(f"user_id = {user_id}")
        """
        cursor.execute(_Requests.get_userID_by_username, (username,))

        result = cursor.fetchone()
        return result[0]

    @staticmethod
    @cm_cursor()
    def get_all_projects(*, cursor: MySQLCursor) -> ResultType:
        """
        Permet de recup les projets dans la db.

        Cette fonction renvoie une liste de tuples comprenant les
        taches sous la forme (projectID, name).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie None ou dans certains cas, un objet de type Exception.

        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> all_projects = DB_API.get_all_projects()
        >>> if all_projects and not isinstance(all_projects, Exception):
        >>>     print(f"all_projects = {all_projects}")
        """
        cursor.execute(_Requests.get_all_projects)
        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_cursor()
    def get_all_tasks(*, cursor: MySQLCursor) -> ResultType:
        """
        Permet de recup toutes les tasks dans la db.

        Cette fonction renvoie une liste de tuples comprenant les
        taches sous la forme (taskID, title, description, status,
        priority, covered, assign, dead_line).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie None ou dans certains cas, un objet de type Exception.

        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> all_tasks = DB_API.get_all_tasks()
        >>> if all_tasks and not isinstance(all_tasks, Exception):
        >>>     print(f"all_tasks = {all_tasks}")
        """
        cursor.execute(_Requests.get_all_tasks)
        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_cursor()
    def get_user_email(user_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de recup l'email de l'userid dans la db.

        Cette fonction renvoie un tuple ou None, une exception de façon rare.
        En cas d'échec, elle renverra une exc et en cas de succes,
        elle renverra le mail de l'user dans un tuple.

        :param user_id: L'id de l'user
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> email = DB_API.get_user_email(2)
        >>> if email and not isinstance(email, Exception):
        >>>     print(f"email = {email}")
        """
        cursor.execute(_Requests.get_user_email, (user_id,))

        result = cursor.fetchone()
        return result

    @staticmethod
    @cm_cursor()
    def get_emails_by_task_projectID(task_project_id: int, *, cursor: MySQLCursor) -> list:
        """
        Retrieves the emails of users associated with a specific task project.

        Args:
            task_project_id (int): The ID of the task project.
            cursor (MySQLCursor): Cursor for the database connection
            (managed automatically by the cm_cursor decorator).

        Returns:
            list: A list of emails associated with the task project.
        """
        cursor.execute(_Requests.get_emails_by_task_projectID, (task_project_id,))

        result = cursor.fetchall()
        return [row[0] for row in result]

    @staticmethod
    @cm_cursor()
    def get_users_groups_by_project_name(name: str, *, cursor: MySQLCursor) -> ResultType:
        """
        Récupère les groupes d'utilisateurs associés à un nom de projet spécifique.

        Args:
            name (str): Le nom du projet.
            cursor (MySQLCursor): Curseur pour la connexion à la base de données
            (géré automatiquement par le décorateur cm_cursor).

        Returns:
            ResultType: Une liste de groupes d'utilisateurs associés au projet.
        """
        cursor.execute(_Requests.get_users_groups_by_project_name, (name,))

        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_cursor()
    def get_tasks_by_title(title: str, *, cursor: MySQLCursor) -> ResultType:
        """
        Récupère les tâches en fonction de leur titre.

        Cette fonction exécute une requête SQL pour obtenir les tâches
        correspondant au titre fourni. Elle renvoie le résultat de la requête
        sous forme de liste de tuples ou une exception en cas d'erreur.

        Args:
            title (str): Le titre des tâches à rechercher.
            cursor (MySQLCursor): Curseur pour la connexion à la base de données
            (géré automatiquement par le décorateur cm_cursor).

        Returns:
            ResultType: Une liste de tuples représentant les tâches ou une exception.
        """
        cursor.execute(_Requests.get_tasks_by_title, (title,))
        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_cursor()
    def get_email(email: str, *, cursor: MySQLCursor) -> ResultType:
        """
        Récupère l'email d'un utilisateur.

        Cette fonction exécute une requête SQL pour obtenir l'email
        correspondant à l'email fourni. Elle renvoie le résultat de la requête
        sous forme de tuple ou une exception en cas d'erreur.

        Args:
            email (str): L'email de l'utilisateur.
            cursor (MySQLCursor): Curseur pour la connexion à la base de données
            (géré automatiquement par le décorateur cm_cursor).

        Returns:
            ResultType: Un tuple représentant l'email ou une exception.
        """
        cursor.execute(_Requests.get_email, (email,))

        result = cursor.fetchone()
        return result

    @staticmethod
    @cm_cursor()
    def get_user(username: str, *, cursor: MySQLCursor) -> ResultType:
        """
        Récupère les informations d'un utilisateur en fonction de son nom d'utilisateur.

        Cette fonction exécute une requête SQL pour obtenir les informations de l'utilisateur
        correspondant au nom d'utilisateur fourni. Elle renvoie le résultat de la requête
        sous forme de tuple ou une exception en cas d'erreur.

        Args:
            username (str): Le nom d'utilisateur.
            cursor (MySQLCursor): Curseur pour la connexion à la base de données
            (géré automatiquement par le décorateur cm_cursor).

        Returns:
            ResultType: Un tuple représentant les informations de l'utilisateur ou une exception.
        """
        cursor.execute(_Requests.get_user, (username,))

        result = cursor.fetchone()
        return result

    @staticmethod
    @cm_cursor()
    def get_userID_by_email(email: str, *, cursor: MySQLCursor) -> ResultType:
        """
        Récupère l'ID d'un utilisateur en fonction de son email.

        Cette fonction exécute une requête SQL pour obtenir l'ID de l'utilisateur
        correspondant à l'email fourni. Elle renvoie le résultat de la requête
        sous forme de tuple ou une exception en cas d'erreur.

        Args:
            email (str): L'email de l'utilisateur.
            cursor (MySQLCursor): Curseur pour la connexion à la base de données
            (géré automatiquement par le décorateur cm_cursor).

        Returns:
            ResultType: L'ID de l'utilisateur sous forme de tuple ou une exception.
        """
        cursor.execute(_Requests.get_userID_by_email, (email,))

        result = cursor.fetchone()
        return result

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def add_task_group(*, cursor: MySQLCursor) -> Union[Exception, Optional[int]]:
        """
        Permet d'ajouter un task_group dans la db.

        Cette fonction renvoie l'id du task_group ou None, une exception de façon rare.
        En cas d'échec, elle renverra une exc et en cas de succes,
        elle renverra l'id du task_group.

        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> err = DB_API.add_task_group()
        >>> if err and not isinstance(err, Exception):
        >>>     print(f"taskgroup_id = {err}")
        """
        cursor.execute(_Requests.add_task_group)
        return cursor.lastrowid

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def delete_user(user_id, *, cursor: MySQLCursor) -> Optional[Exception]:
        """
        Supprime un utilisateur de la base de données.

        :param user_id: ID de l'utilisateur à supprimer.
        :param cursor: Curseur pour exécuter la requête SQL.
        :return: None si la suppression réussit, ou une Exception si elle échoue.
        """
        return cursor.execute(_Requests.delete_user, (user_id,))

    @staticmethod
    @cm_cursor()
    def get_project_in_users_groups_userid(user_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer tous les projets où l'user est invités (accepté ou non).

        Cette fonction renvoie une liste de tuples comprenant les
        projets sous la forme (projectID, name, permission, joined).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie None ou dans certains cas, un objet de type Exception.

        :param user_id: L'userID
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> projects = DB_API.get_project_in_users_groups_userid(10)
        >>> if projects and not isinstance(projects, Exception):
        >>>     print(projects)

        """
        cursor.execute(_Requests.get_project_in_users_groups, (user_id,))

        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def update_task_infos(
        taskinfos_id: int, update_fields: list, values: list, *, cursor: MySQLCursor
    ) -> Optional[Exception]:
        return cursor.execute(
            _Requests.update_task_infos.format(", ".join(update_fields), taskinfos_id), values
        )

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def delete_task(task_id, *, cursor: MySQLCursor) -> Optional[Exception]:
        """
        Permet de delete une task de la db et toutes ses dépendances.

        Cette fonction renvoie None ou None, une exception de façon rare. En cas d'échec,
        elle renverra une exc et en cas de succes, elle renverra None.

        :param task_id: ID de la tache
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> err = DB_API.delete_task(1)
        >>> if and not isinstance(err, Exception):
        >>>     print("delete avec succes")
        """
        return cursor.execute(_Requests.delete_task, (task_id,))

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def set_invites_status(
        project_id: int, user_id: int, joined: int, *, cursor: MySQLCursor
    ) -> Optional[Exception]:
        """
        Permet d'accepter ou refuser une invitation vers un projet.
        Cette fonction renvoie None ou une exception. En cas d'échec,
        elle renverra une exc et en cas de succes, elle renverra None.
        :param project_id: Le project_ID
        :param user_id: ID de l'utilisateur
        :param joined: Accepter ou pas l'invit
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        Exemple:
        >>> err = DB_API.set_invites_status(1, 1, False)
        >>> if not isinstance(err, Exception):
        >>>     print("delete avec succes")
        """
        return cursor.execute(_Requests.set_invites_status, (joined, project_id, user_id))

    @staticmethod
    @cm_cursor()
    def get_totp_secret(email: str, *, cursor: MySQLCursor) -> Optional[str]:
        """
        Retourne la clé TOTP stockée pour cet email, ou None si pas trouvée.
        """
        cursor.execute("SELECT totp_secret FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if row:
            return row[0]  # la clé
        return None

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def delete_subtask(subtask_id, *, cursor: MySQLCursor) -> Optional[Exception]:
        """
        Permet de delete une subtask de la db et toutes ses dépendances.

        Cette fonction renvoie None ou None, une exception de façon rare. En cas d'échec,
        elle renverra une exc et en cas de succes, elle renverra None.

        :param subtask_id: ID de la tache
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> err = DB_API.delete_subtask(1)
        >>> if and not isinstance(err, Exception):
        >>>     print("delete avec succes")
        """
        return cursor.execute(_Requests.delete_task.format(subtask_id))

    @staticmethod
    @cm_cursor()
    def get_user_permission(project_id: int, user_id: int, *, cursor: MySQLCursor) -> ResultType:
        cursor.execute(_Requests.get_user_permission.format(project_id, user_id))
        result = cursor.fetchone()
        return result

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def set_totp_secret(email: str, secret: str, *, cursor: MySQLCursor) -> bool:
        """
        Stocke la clé TOTP 'secret' dans la table 'users' pour l'email donné.
        Suppose qu'une colonne 'totp_secret' existe dans la table 'users'.
        """
        cursor.execute("UPDATE users SET totp_secret = %s WHERE email = %s", (secret, email))
        return True

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def delete_project(project_id: int, *, cursor: MySQLCursor) -> Optional[Exception]:
        return cursor.execute(_Requests.delete_project.format(project_id))

    @staticmethod
    @cm_cursor()
    def get_task_info_by_task_id(taskID: str, *, cursor: MySQLCursor) -> ResultType:
        query = _Requests.get_task_info_by_task_id
        cursor.execute(query, (taskID,))
        result = cursor.fetchall()
        return result

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def delete_user_group(project_id: int, *, cursor: MySQLCursor) -> Optional[Exception]:
        return cursor.execute(_Requests.delete_users_groups.format(project_id))

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def delete_tasks_groups(project_id: int, *, cursor: MySQLCursor) -> Optional[Exception]:
        return cursor.execute(_Requests.delete_tasks_groups.format(project_id))

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def delete_tasks_infos(project_id: int, *, cursor: MySQLCursor) -> Optional[Exception]:
        return cursor.execute(_Requests.delete_tasks_infos.format(project_id))

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def delete_tasks(project_id: int, *, cursor: MySQLCursor) -> Optional[Exception]:
        return cursor.execute(_Requests.delete_tasks.format(project_id))
        
    @staticmethod
    @cm_conn()
    @cm_cursor()
    def check_projects(project_name: str, *, cursor: MySQLCursor) -> bool:
        """
        Vérifie si un projet existe dans la base de données par son nom.

        :param project_name: Nom du projet à vérifier.
        :param cursor: Curseur de la base de données.
        :return: True si le projet existe, False sinon.
        """
        cursor.execute(_Requests.check_projects.format(project_name))
        result = cursor.fetchone()

        return result[0] > 0 if result else False

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def delete_users_from_users_tasks_groups(task_group_id: int, *, cursor: MySQLCursor) -> Optional[Exception]:
        """
        Supprime tous les utilisateurs d'un groupe de tâches spécifique

        Args:
            task_group_id (int): L'ID du groupe de tâches
            cursor (MySQLCursor): Curseur de base de données (injecté par le décorateur)

        Returns:
            Optional[Exception]: None si succès, Exception si erreur
        """
        return cursor.execute(_Requests.delete_users_from_users_tasks_groups.format(task_group_id))

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def update_task_status(task_info_id: int, status: int, *, cursor: MySQLCursor) -> bool:
        """
        Met à jour le statut de la tâche dans la table tasks_infos.
        """
        try:
            query = "UPDATE tasks_infos SET status = %s WHERE task_infoID = %s"
            cursor.execute(query, (status, task_info_id))
            print(f"Mise à jour du statut : task_infoID={task_info_id}, status={status}")
            return cursor.rowcount > 0  # Retourne True si une ligne a été affectée
        except Exception as e:
            print(f"Erreur lors de la mise à jour du statut de la tâche : {e}")
            return False

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def get_task_info_id_by_task_id(task_id: int, *, cursor: MySQLCursor) -> Optional[int]:
        """
        Récupère task_infoID associé à une tâche (taskID).
        """
        try:
            query = "SELECT task_infoID FROM tasks WHERE taskID = %s"
            cursor.execute(query, (task_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Erreur lors de la récupération de task_infoID : {e}")
            return None

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def update_task_status_to_zero(task_info_id: int, status: int = 0, *, cursor: MySQLCursor) -> bool:
        """
        Met à jour le statut de la tâche dans la table tasks_infos en mettant le statut à 0 (non terminé).
        """
        try:
            query = "UPDATE tasks_infos SET status = %s WHERE task_infoID = %s"
            cursor.execute(query, (status, task_info_id))
            print(f"Mise à jour du statut : task_infoID={task_info_id}, status={status}")
            return cursor.rowcount > 0  # Retourne True si une ligne a été affectée
        except Exception as e:
            print(f"Erreur lors de la mise à jour du statut de la tâche : {e}")
            return False


if __name__ == "__main__":
    # print(DB_API.add_project('tebgfbgrsbs'))
    # t = (DB_API.add_user(username="vlad", password="trql",
    # email="email@vlad.com", is_google_user=False))
    t = DB_API.get_all_tasks()
    print(type(t), t)
    pass

# TODO: ajouter les tests pour get_project_in_users_groups_userid, set_invites_status
