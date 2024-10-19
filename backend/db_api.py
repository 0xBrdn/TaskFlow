import datetime
import logging
from typing import Optional

from mysql.connector.cursor import MySQLCursor

from db_helper import cm_cursor, ResultType, cm_conn
from db_requests import _Requests

_log = logging.getLogger(__name__)


class DB_API:
    """Classe permettant d'executer les commandes vers la DB SQL"""

    @cm_cursor()
    def get_all_users(self, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer tous les utilisateurs de la DB.

        Cette fonction renvoie une liste de tuples comprenant les
        users sous la forme (userID, username, email, is_google_user).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie un objet de type Exception.

        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> db_api = DB_API()
        >>> users = db_api.get_all_users()
        >>> print(users)

        """
        cursor.execute(_Requests.get_all_users)
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_user_hashpass(self, user_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer le mdp hash d'un user dans la DB.

        Cette fonction renvoie un tuple comprenant uniquement le
        mot de passe hash de la personne.
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie un objet de type Exception.

        :param user_id: ID de l'utilisateur
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> db_api = DB_API()
        >>> hash_pass = db_api.get_user_hashpass(1)
        >>> print(hash_pass)
        """
        cursor.execute(_Requests.get_user_hashpass.format(user_id))
        result = cursor.fetchone()
        return result

    @cm_cursor()
    def get_projects_by_user_id(self, user_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer tous les projets d'un utilisateur en fonction de son userID.

        Cette fonction renvoie une liste de tuples comprenant les
        projets sous la forme (projectID, name).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie un objet de type Exception.

        :param user_id: ID de l'utilisateur
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> db_api = DB_API()
        >>> projects = db_api.get_projects_by_user_id(1)
        >>> print(projects)
        """
        cursor.execute(_Requests.get_projects_by_user_id.format(user_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_tasks_by_project_id(self, project_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer toutes les taches d'un projet en fonction de son projectID.

        Cette fonction renvoie une liste de tuples comprenant les
        taches sous la forme (taskID, title, description, status,
        priority, covered, assign, dead_line).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie un objet de type Exception.

        :param project_id: projectID
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> db_api = DB_API()
        >>> tasks = db_api.get_tasks_by_project_id(1)
        >>> print(tasks)
        """
        cursor.execute(_Requests.get_tasks_by_project_id.format(project_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_subtasks_by_task_id(self, task_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer toutes les sous taches d'un projet en fonction de son taskID.

        Cette fonction renvoie une liste de tuples comprenant les
        sous taches sous la forme (subtaskID, title, description, status,
        priority, covered, assign, dead_line).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie un objet de type Exception.

        :param task_id: taskID
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> db_api = DB_API()
        >>> subtasks = db_api.get_subtasks_by_task_id(1)
        >>> print(subtasks)
        """
        cursor.execute(_Requests.get_subtasks_by_task_id.format(task_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_user_logs_by_id(self, log_id: int, *, cursor: MySQLCursor) -> ResultType:
        """
        Permet de récuperer toutes les logs d'un user grace a son userID.

        Cette fonction renvoie une liste de tuples comprenant les
        logs sous la forme (logID, action, action_time, details).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie un objet de type Exception.

        :param log_id: logID
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> db_api = DB_API()
        >>> logs = db_api.get_user_logs_by_id(1)
        >>> print(logs)
        """
        cursor.execute(_Requests.get_user_logs_by_id.format(log_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_users_in_project_by_project_id(
        self, project_id: int, *, cursor: MySQLCursor
    ) -> ResultType:
        """
        Permet de récuperer toutes users dans un projet en fonction du projectID.

        Cette fonction renvoie une liste de tuples comprenant les
        projets de l'user sous la forme (userID, username, permission).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie un objet de type Exception.

        :param project_id: projectID
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> db_api = DB_API()
        >>> users_in_project = db_api.get_users_in_project_by_project_id(1)
        >>> print(users_in_project)
        """
        cursor.execute(_Requests.get_users_in_project_by_project_id.format(project_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_tasks_by_user_id(self, user_id: int, *, cursor: MySQLCursor) -> ResultType:
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
        >>> db_api = DB_API()
        >>> user_tasks = db_api.get_tasks_by_user_id(1)
        >>> print(user_tasks)
        """
        cursor.execute(_Requests.get_tasks_by_user_id.format(user_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_users_in_tasks_group_by_group_id(
        self, group_id: int, *, cursor: MySQLCursor
    ) -> ResultType:
        """
        Permet de récuperer tous les utilisateurs dans un groupe
        de tâches en fonction de son groupID.

        Cette fonction renvoie une liste de tuples comprenant les
        utilisateurs sous la forme (userID, username, task_projectID).
        Cette fonction peut ne pas fonctionner, dans ce cas elle
        renvoie un objet de type Exception.

        :param group_id: groupID
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())
        :return: resultat de la commande ou exception

        Exemple:
        >>> db_api = DB_API()
        >>> users_in_group = db_api.get_users_in_tasks_group_by_group_id(1)
        >>> print(users_in_group)
        """
        cursor.execute(_Requests.get_users_in_tasks_group_by_group_id.format(group_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_all_status(self, *, cursor: MySQLCursor) -> ResultType:
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
        >>> db_api = DB_API()
        >>> status = db_api.get_all_status()
        >>> print(status)
        """
        cursor.execute(_Requests.get_all_status)
        result = cursor.fetchall()
        return result

    @cm_conn()
    @cm_cursor()
    def add_user(
        self,
        username: str,
        password: Optional[str],
        email: str,
        is_google_user: bool,
        *,
        cursor: MySQLCursor,
    ):
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
        >>> db_api = DB_API()
        >>> success = db_api.add_user("new_user", "hashed_password", "user@Exemple.com")
        >>> assert success is True
        """

        return cursor.execute(_Requests.add_user.format(username, password, email, is_google_user))

    @cm_conn()
    @cm_cursor()
    def add_status(self, user_id: int, status: int, *, cursor: MySQLCursor):
        """
        Permet d'ajouter un statut à un utilisateur.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param user_id: ID de l'utilisateur
        :param status: Statut à ajouter (0 = deco; 1 = connect; 2 = idle)
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> db_api = DB_API()
        >>> success = db_api.add_status(1, 0)
        >>> assert success is True
        """

        return cursor.execute(_Requests.add_status.format(user_id, status))

    @cm_conn()
    @cm_cursor()
    def add_project(self, name: str, *, cursor: MySQLCursor):
        """
        Permet d'ajouter un nouveau projet à la DB.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param name: Nom du projet
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> db_api = DB_API()
        >>> success = db_api.add_project("project_test")
        >>> assert success is True
        """
        return cursor.execute(_Requests.add_project.format(name))

    @cm_conn()
    @cm_cursor()
    def add_user_to_group(
        self, project_id: int, user_id: int, permission: int, joined: bool, *, cursor: MySQLCursor
    ):
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
        >>> db_api = DB_API()
        >>> success = db_api.add_user_to_group(1, 1, 1, True)
        >>> assert success is True
        """
        return cursor.execute(
            _Requests.add_user_to_group.format(project_id, user_id, permission, joined)
        )

    @cm_conn()
    @cm_cursor()
    def add_task_info(
        self,
        status: int,
        priority: int,
        title: str,
        description: str,
        dead_line: datetime.datetime,
        covered: bool,
        assign: int,
        *,
        cursor: MySQLCursor,
    ):
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
        >>> db_api = DB_API()
        >>> success = db_api.add_task_info(1, 2, "titre tache",
        "ceci est une description de la tache", datetime.datetime.now(), False, 1)
        >>> assert success is True
        """
        return cursor.execute(
            _Requests.add_task_info.format(
                status, priority, title, description, dead_line, covered, assign
            )
        )

    @cm_conn()
    @cm_cursor()
    def add_task(self, project_id: int, task_info_id: int, user_id: int, *, cursor: MySQLCursor):
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
        >>> db_api = DB_API()
        >>> success = db_api.add_task(1, 1, 1)
        >>> assert success is True
        """
        return cursor.execute(_Requests.add_task.format(project_id, task_info_id, user_id))

    @cm_conn()
    @cm_cursor()
    def add_subtask(self, task_id: int, task_info_id: int, *, cursor: MySQLCursor):
        """
        Permet d'ajouter une sous-tâche à une tâche.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param task_id: ID de la tâche parente
        :param task_info_id: ID des informations de la sous-tâche
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> db_api = DB_API()
        >>> success = db_api.add_subtask(1, 1)
        >>> assert success is True
        """
        return cursor.execute(_Requests.add_subtask.format(task_id, task_info_id))

    @cm_conn()
    @cm_cursor()
    def add_user_to_task_group(self, task_project_id: int, user_id: int, *, cursor: MySQLCursor):
        """
        Permet d'ajouter un utilisateur à un groupe de tâches.

        Cette fonction renvoie un boolean. En cas d'échec,
        elle renverra False et en cas de succes, elle renverra True.

        :param task_project_id: ID du projet de la tâche
        :param user_id: ID de l'utilisateur à ajouter
        :param cursor: Curseur d'une connexion vers une DB
        (optionnel, géré automatiquement par le décorateur cm_cursor())

        Exemple:
        >>> db_api = DB_API()
        >>> success = db_api.add_user_to_task_group(1, 1)
        >>> assert success is True
        """
        return cursor.execute(_Requests.add_user_to_task_group.format(task_project_id, user_id))

    @cm_conn()
    @cm_cursor()
    def add_user_log(self, user_id: int, action: str, details: str, *, cursor: MySQLCursor):
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
        >>> db_api = DB_API()
        >>> success = db_api.add_user_log(1, "affect", "user to task")
        >>> assert success is True
        """
        return cursor.execute(_Requests.add_user_log.format(user_id, action, details))


if __name__ == "__main__":
    api = DB_API()
