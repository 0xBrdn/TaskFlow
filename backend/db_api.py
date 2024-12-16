import datetime
import logging
from typing import Optional, Union

from mysql.connector.cursor import MySQLCursor

from backend.db_helper import cm_cursor, ResultType, cm_conn
from backend.db_requests import _Requests

_log = logging.getLogger(__name__)


class DB_API:
    """Classe permettant d'executer les commandes vers la DB SQL"""

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
        renvoie None ou dans certains cas, un objet de type Exception.

        :param project_name: Nom du projet
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> project_id = DB_API.get_project_id_by_project_name()
        >>> if project_id and not isinstance(project_id, Exception):
        >>>     print(project_id)

        """
        cursor.execute(_Requests.get_project_id_by_project_name.format(project_name))
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
        cursor.execute(_Requests.get_user_hashpass.format(user_id))
        result = cursor.fetchone()
        return result

    @staticmethod
    @cm_cursor()
    def get_projects_by_user_id(user_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer tous les projets d'un utilisateur en fonction de son userID.

        Cette fonction renvoie une liste de tuples comprenant les
        projets sous la forme (projectID, name).
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
        cursor.execute(_Requests.get_projects_by_user_id.format(user_id))
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
        cursor.execute(_Requests.get_tasks_by_project_id.format(project_id))
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
        cursor.execute(_Requests.get_subtasks_by_task_id.format(task_id))
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
        cursor.execute(_Requests.get_user_logs_by_id.format(log_id))
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
        cursor.execute(_Requests.get_users_in_project_by_project_id.format(project_id))
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
        cursor.execute(_Requests.get_tasks_by_user_id.format(user_id))
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
        cursor.execute(_Requests.get_users_in_tasks_group_by_group_id.format(group_id))
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
    def add_user(
        username: str,
        password: Optional[str],
        email: str,
        is_google_user: bool,
        *,
        cursor: MySQLCursor,
    ) -> Union[Exception, Optional[int]]:
        """
        Permet d'ajouter un nouvel utilisateur à la DB.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param username: Nom d'utilisateur
        :param password: Mot de passe (hashé)
        :param email: Adresse email de l'utilisateur
        :param is_google_user: Si l'utilisateur se connecte avec google
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> user_id = DB_API.add_user("new_user", "hashed_password", "user@Exemple.com")
        >>> if user_id and not isinstance(user_id, Exception):
        >>>     print(user_id)
        """
        cursor.execute(_Requests.add_user.format(username, password, email, is_google_user))
        return cursor.lastrowid

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
        cursor.execute(_Requests.add_status.format(user_id, status))
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
        cursor.execute(_Requests.add_project.format(name))
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
        cursor.execute(_Requests.add_user_to_group.format(project_id, user_id, permission, joined))
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
            _Requests.add_task_info.format(
                status, priority, title, description, dead_line, covered, assign
            )
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
        cursor.execute(_Requests.add_task.format(project_id, task_info_id, user_id))
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
        cursor.execute(_Requests.add_subtask.format(task_id, task_info_id))
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
        cursor.execute(_Requests.add_user_to_task_group.format(task_project_id, user_id))
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
        cursor.execute(_Requests.add_user_log.format(user_id, action, details))
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
        cursor.execute(_Requests.get_userID_by_username.format(username))
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
        cursor.execute(_Requests.get_user_email.format(user_id))
        result = cursor.fetchone()
        return result

    @staticmethod
    @cm_cursor()
    def get_emails_by_task_project_id(
        task_project_id: int, *, cursor: MySQLCursor
    ) -> Union[Exception, Optional[list]]:
        """
        Permet d'ajouter un task_group dans la db.

        Cette fonction renvoie l'id du task_group ou None, une exception de façon rare.
        En cas d'échec, elle renverra une exc et en cas de succes,
        elle renverra l'id du task_group.

        :param task_project_id: L'id du task_project
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> emails = DB_API.get_emails_by_task_project_id(2)
        >>> if emails and not isinstance(emails, Exception):
        >>>     print(f"emails = {emails}")
        """
        cursor.execute(_Requests.get_emails_by_task_projectID.format(task_project_id))
        result = cursor.fetchall()
        return [row[0] for row in result]

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
        Permet de delete un utilisateur de la db et toutes ses dépendances.

        Cette fonction renvoie None ou None, une exception de façon rare. En cas d'échec,
        elle renverra une None et en cas de succes, elle renverra None.
        Elle renverra une Exception que dans certains cas.

        :param user_id: ID de l'utilisateur
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> err = DB_API.delete_user(1)
        >>> if and not isinstance(err, Exception):
        >>>     print("delete avec succes")
        """
        return cursor.execute(_Requests.delete_user.format(user_id))

    @staticmethod
    @cm_conn()
    @cm_cursor()
    def update_task_infos(
        taskinfos_id: int, update_fields: list, values: list, *, cursor: MySQLCursor
    ) -> Optional[Exception]:
        """
        Permet d'update un ou plusieurs objets d'une task_infos.

        Cette fonction renvoie None ou None, une exception de façon rare. En cas d'échec,
        elle renverra une exc et en cas de succes, elle renverra None.

        :param taskinfos_id: ID de la task info
        :param update_fields: Tous les objets a modifier
        :param values: Les valeurs des objets a modifier
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> err = DB_API.update_task_infos(4, ['status', 'title'], [3, 'nouveau title'])
        >>> if and not isinstance(err, Exception):
        >>>     print("delete avec succes")
        """
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
        return cursor.execute(_Requests.delete_task.format(task_id))

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


if __name__ == "__main__":
    # print(DB_API.add_project('tebgfbgrsbs'))
    # t = (DB_API.add_user(username="vlad", password="trql",
    # email="email@vlad.com", is_google_user=False))
    t = DB_API.get_all_tasks()
    print(type(t), t)
    pass
