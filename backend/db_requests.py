class _Requests:
    get_all_users = "SELECT userID, username, email, is_google_user FROM users;"

    get_user_hashpass = "SELECT password FROM users WHERE userID = {};"

    get_projects_by_user_id = (
        "SELECT p.projectID, p.name FROM projects p "
        "JOIN users_groups ug ON p.projectID = ug.projectID "
        "WHERE ug.userID = {};"
    )

    get_tasks_by_project_id = (
        "SELECT t.taskID, ti.title, ti.description, ti.status, ti.priority, ti.covered, "
        "ti.assign, ti.dead_line FROM tasks t JOIN tasks_infos ti ON t.task_infoID = "
        "ti.task_infoID WHERE t.projectID = {};"
    )

    get_subtasks_by_task_id = (
        "SELECT st.subtaskID, ti.title, ti.description, ti.status, ti.priority, ti.covered, "
        "ti.assign, ti.dead_line FROM subtasks st "
        "JOIN tasks_infos ti ON st.task_infoID = ti.task_infoID WHERE st.taskID = {};"
    )

    get_user_logs_by_id = (
        "SELECT logID, action, action_time, details FROM users_logs WHERE userID = {};"
    )

    get_users_in_project_by_project_id = (
        "SELECT u.userID, u.username, ug.permission FROM users u "
        "JOIN users_groups ug ON u.userID = ug.userID "
        "WHERE ug.projectID = {};"
    )

    get_tasks_by_user_id = (
        "SELECT t.taskID, ti.title, ti.description, ti.status, ti.priority, ti.covered, "
        "ti.assign, ti.dead_line FROM tasks t "
        "JOIN tasks_infos ti ON t.task_infoID = ti.task_infoID "
        "WHERE t.userID = {};"
    )

    get_users_in_tasks_group_by_group_id = (
        "SELECT u.userID, u.username, utg.task_projectID FROM users u "
        "JOIN users_tasks_groups utg ON u.userID = utg.userID "
        "WHERE utg.task_projectID = {};"
    )

    get_all_status = "SELECT userID, status FROM status;"

    add_user = (
        "INSERT INTO users (username, password, email, is_google_user) VALUES ({}, {}, {}, {});"
    )

    add_status = "INSERT INTO status (userID, status) VALUES ({}, {});"

    add_project = "INSERT INTO projects (name) VALUES ({});"

    add_user_to_group = (
        "INSERT INTO users_groups (projectID, userID, "
        "permission, joined) VALUES ({}, {}, {}, {});"
    )

    add_task_info = (
        "INSERT INTO tasks_infos (status, priority, title, description, "
        "dead_line, covered, assign) VALUES ({}, {}, {}, {}, {}, {}, {});"
    )

    add_task = "INSERT INTO tasks (projectID, task_infoID, userID) VALUES ({}, {}, {});"

    add_subtask = "INSERT INTO subtasks (taskID, task_infoID) VALUES ({}, {});"

    add_user_to_task_group = (
        "INSERT INTO users_tasks_groups (task_projectID, userID) VALUES ({}, {});"
    )

    add_user_log = "INSERT INTO users_logs (userID, action, details) VALUES ({}, {}, {});"


if __name__ == "__main__":
    _Requests.get_user_hashpass.format("test")
