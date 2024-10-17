from mysql.connector.cursor import MySQLCursor

from db_helper import cm_cursor, _T, cm_conn
from db_requests import _Requests


class DB_API:
    @cm_cursor()
    def get_all_users(self, *, cursor: MySQLCursor) -> _T:
        cursor.execute(_Requests.get_all_users)
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_user_hashpass(self, user_id: str, *, cursor: MySQLCursor) -> _T:
        cursor.execute(_Requests.get_user_hashpass.format(user_id))
        result = cursor.fetchone()
        return result

    @cm_cursor()
    def get_projects_by_user_id(self, user_id: str, *, cursor: MySQLCursor) -> _T:
        cursor.execute(_Requests.get_projects_by_user_id.format(user_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_tasks_by_project_id(self, project_id: str, *, cursor: MySQLCursor) -> _T:
        cursor.execute(_Requests.get_tasks_by_project_id.format(project_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_subtasks_by_task_id(self, task_id: str, *, cursor: MySQLCursor) -> _T:
        cursor.execute(_Requests.get_subtasks_by_task_id.format(task_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_user_logs_by_id(self, log_id: str, *, cursor: MySQLCursor) -> _T:
        cursor.execute(_Requests.get_user_logs_by_id.format(log_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_users_in_project_by_project_id(self, project_id: str, *, cursor: MySQLCursor) -> _T:
        cursor.execute(_Requests.get_users_in_project_by_project_id.format(project_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_tasks_by_user_id(self, user_id: str, *, cursor: MySQLCursor) -> _T:
        cursor.execute(_Requests.get_tasks_by_user_id.format(user_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_users_in_tasks_group_by_group_id(self, group_id: str, *, cursor: MySQLCursor) -> _T:
        cursor.execute(_Requests.get_users_in_tasks_group_by_group_id.format(group_id))
        result = cursor.fetchall()
        return result

    @cm_cursor()
    def get_all_status(self, *, cursor: MySQLCursor) -> _T:
        cursor.execute(_Requests.get_all_status)
        result = cursor.fetchall()
        return result

    @cm_conn()
    @cm_cursor()
    def add_user(self, username: str, password: str, email: str, *, cursor: MySQLCursor):
        cursor.execute(_Requests.add_user.format(username, password, email))

    @cm_conn()
    @cm_cursor()
    def add_status(self, user_id: str, status: str, *, cursor: MySQLCursor):
        cursor.execute(_Requests.add_status.format(user_id, status))

    @cm_conn()
    @cm_cursor()
    def add_project(self, name: str, *, cursor: MySQLCursor):
        cursor.execute(_Requests.add_project.format(name))

    @cm_conn()
    @cm_cursor()
    def add_user_to_group(
        self, project_id: str, user_id: str, permission: str, joined: str, *, cursor: MySQLCursor
    ):
        cursor.execute(_Requests.add_user_to_group.format(project_id, user_id, permission, joined))

    @cm_conn()
    @cm_cursor()
    def add_task_info(
        self,
        status: str,
        priority: str,
        title: str,
        description: str,
        dead_line: str,
        covered: str,
        assign: str,
        *,
        cursor: MySQLCursor,
    ):
        cursor.execute(
            _Requests.add_task_info.format(
                status, priority, title, description, dead_line, covered, assign
            )
        )

    @cm_conn()
    @cm_cursor()
    def add_task(self, project_id: str, task_info_id: str, user_id: str, *, cursor: MySQLCursor):
        cursor.execute(_Requests.add_task.format(project_id, task_info_id, user_id))

    @cm_conn()
    @cm_cursor()
    def add_subtask(self, task_id: str, task_info_id: str, *, cursor: MySQLCursor):
        cursor.execute(_Requests.add_subtask.format(task_id, task_info_id))

    @cm_conn()
    @cm_cursor()
    def add_user_to_task_group(self, task_project_id: str, user_id: str, *, cursor: MySQLCursor):
        cursor.execute(_Requests.add_user_to_task_group.format(task_project_id, user_id))

    @cm_conn()
    @cm_cursor()
    def add_user_log(self, user_id: str, action: str, details: str, *, cursor: MySQLCursor):
        cursor.execute(_Requests.add_user_log.format(user_id, action, details))


if __name__ == "__main__":
    DB_API().get_user_hashpass()
