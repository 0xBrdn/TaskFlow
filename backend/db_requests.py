class _Requests:
    # Lecture simple (pas besoin de paramètres)
    get_all_users = """
        SELECT userID, username, email, is_google_user
        FROM users;
    """

    # Requêtes paramétrées avec %s
    get_email_hashpass = """
        SELECT password
        FROM users
        WHERE email = %s;
    """

    get_user_hashpass = """
        SELECT password
        FROM users
        WHERE userID = %s;
    """

    get_project_id_by_project_name = """
        SELECT projectID
        FROM projects
        WHERE projects.name = %s;
    """

    get_projects_by_user_id = """
        SELECT p.projectID, p.name, ug.joined
        FROM projects p
        JOIN users_groups ug ON p.projectID = ug.projectID
        WHERE ug.userID = %s;
    """

    get_project_in_users_groups = """
        SELECT ug.projectID, p.name, ug.permission, ug.joined
        FROM users_groups ug
        JOIN projects p ON p.projectID = ug.projectID
        WHERE userID = %s;
    """

    get_tasks_by_project_id = """
        SELECT t.taskID, ti.title, ti.description, ti.status,
               ti.priority, ti.covered, ti.assign, ti.dead_line
        FROM tasks t
        JOIN tasks_infos ti ON t.task_infoID = ti.task_infoID
        WHERE t.projectID = %s;
    """

    get_subtasks_by_task_id = """
        SELECT st.subtaskID, ti.title, ti.description, ti.status,
               ti.priority, ti.covered, ti.assign, ti.dead_line
        FROM subtasks st
        JOIN tasks_infos ti ON st.task_infoID = ti.task_infoID
        WHERE st.taskID = %s;
    """

    get_user_logs_by_id = """
        SELECT logID, action, action_time, details
        FROM users_logs
        WHERE userID = %s;
    """

    get_users_in_project_by_project_id = """
        SELECT u.userID, u.username, ug.permission
        FROM users u
        JOIN users_groups ug ON u.userID = ug.userID
        WHERE ug.projectID = %s;
    """

    get_tasks_by_user_id = """
        SELECT t.taskID, ti.title, ti.description, ti.status,
               ti.priority, ti.covered, ti.assign, ti.dead_line
        FROM tasks t
        JOIN tasks_infos ti ON t.task_infoID = ti.task_infoID
        WHERE t.userID = %s;
    """

    get_users_in_tasks_group_by_group_id = """
        SELECT u.userID, u.username, utg.task_projectID
        FROM users u
        JOIN users_tasks_groups utg ON u.userID = utg.userID
        WHERE utg.task_projectID = %s;
    """

    get_userID_by_username = """
        SELECT userID
        FROM users
        WHERE username = %s;
    """

    get_all_status = """
        SELECT userID, status
        FROM status;
    """

    get_all_projects = """
        SELECT projectID, name
        FROM projects;
    """

    get_all_tasks = """
        SELECT t.taskID, ti.title, ti.description, ti.status,
               ti.priority, ti.covered, ti.assign, ti.dead_line
        FROM tasks t
        JOIN tasks_infos ti ON t.task_infoID = ti.task_infoID;
    """

    get_user_email = """
        SELECT email
        FROM users
        WHERE userID = %s;
    """

    get_emails_by_task_projectID = """
        SELECT u.email
        FROM users_tasks_groups utg
        JOIN users u ON utg.userID = u.userID
        WHERE utg.task_projectID = %s;
    """

    get_users_groups_by_project_name = """
        SELECT ug.*
        FROM users_groups ug
        JOIN projects p ON ug.projectID = p.projectID
        WHERE p.name = %s;
    """

    get_tasks_by_title = """
        SELECT t.taskID, t.projectID, ti.description, ti.status,
               ti.priority, ti.covered, ti.assign, ti.dead_line
        FROM tasks t
        JOIN tasks_infos ti ON t.task_infoID = ti.task_infoID
        WHERE ti.title = %s;
    """

    get_email = """
        SELECT email
        FROM users
        WHERE email = %s;
    """

    get_user = """
        SELECT username
        FROM users
        WHERE username = %s;
    """

    get_userID_by_email = """
        SELECT userID
        FROM users
        WHERE email = %s;
    """

    # Insertion paramétrée
    add_user = """
        INSERT INTO users (username, password, email, is_google_user)
        VALUES (%s, %s, %s, %s);
    """

    add_status = """
        INSERT INTO status (userID, status)
        VALUES (%s, %s);
    """

    add_project = """
        INSERT INTO projects (name)
        VALUES (%s);
    """

    add_user_to_group = """
        INSERT INTO users_groups (projectID, userID, permission, joined)
        VALUES (%s, %s, %s, %s);
    """

    add_task_info = """
        INSERT INTO tasks_infos (status, priority, title, description,
                                 dead_line, covered, assign)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    set_invites_status = """
        UPDATE users_groups
        SET joined = %s
        WHERE projectID = %s
          AND userID = %s;
    """

    add_task = """
        INSERT INTO tasks (projectID, task_infoID, userID)
        VALUES (%s, %s, %s);
    """

    add_subtask = """
        INSERT INTO subtasks (taskID, task_infoID)
        VALUES (%s, %s);
    """

    add_user_to_task_group = """
        INSERT INTO users_tasks_groups (task_projectID, userID)
        VALUES (%s, %s);
    """

    add_user_log = """
        INSERT INTO users_logs (userID, action, details)
        VALUES (%s, %s, %s);
    """

    add_task_group = """
        INSERT INTO tasks_groups ()
        VALUES ();
    """

    # Suppression paramétrée
    delete_user = """
        DELETE FROM users
        WHERE userID = %s;
    """

    delete_task = """
        DELETE FROM tasks
        WHERE taskID = %s;
    """

    delete_subtask = """
        DELETE FROM subtasks
        WHERE subtaskID = %s;
    """

    update_task_infos = "UPDATE tasks_infos SET {columns} WHERE task_infoID = %s"

    get_user_permission = (
        "SELECT permission FROM users_groups WHERE projectID = '{}'" "AND userID = '{}';"
    )

    delete_project = "DELETE FROM projects WHERE projectID = '{}';"

    get_task_info_by_task_id = (
        "SELECT ti.title, ti.description, ti.status, ti.priority, ti.covered,"
        "ti.assign, ti.dead_line "
        "FROM tasks t "
        "JOIN tasks_infos ti ON t.task_infoID = ti.task_infoID "
        "WHERE t.taskID = %s;"
    )

    delete_users_groups = "DELETE FROM users_groups WHERE projectID = '{}';"

    delete_tasks_groups = (
        "DELETE tg FROM tasks_groups tg INNER JOIN tasks t ON t.assign = tg.task_projectID WHERE "
        "t.projectID = '{}';"
    )

    delete_tasks_infos = (
        "DELETE ti FROM tasks_infos ti INNER JOIN tasks t ON t.task_infoID = ti.task_infoID WHERE t.projectID = '{}';"
    )

    delete_tasks = (
        "DELETE FROM tasks where projectID = '{}';"
    )
    
    check_projects = "SELECT COUNT(*) AS project_count FROM projects WHERE name = '{}';"

    delete_users_from_users_tasks_groups = (
        "DELETE FROM users_tasks_groups "
        "WHERE task_projectID = %s;"
    )

    update_task_status = """
        UPDATE tasks_infos
        SET status = %s
        WHERE task_infoID = %s;
    """

    update_task_status_to_zero = """
        UPDATE tasks_infos
        SET status = %s
        WHERE task_infoID = %s;
    """

if __name__ == "__main__":
    # Exemple fictif :
    # print(_Requests.get_user_hashpass % "test_user")
    pass
