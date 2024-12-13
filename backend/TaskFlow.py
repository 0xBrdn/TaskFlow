from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from db_api import DB_API

accounts = [
    {"email": "taskflowreminder1@gmail.com", "password": "bgnt irxw fblu vemb"},
    {"email": "taskflowreminder2@gmail.com", "password": "lkya wtsu opzy pnse"},
    {"email": "taskflowreminder3@gmail.com", "password": "jjnw nuhq eopy azfw"},
]
current_account_index = 0


def send_email(subject, body, to):
    global current_account_index
    account = accounts[current_account_index]

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(account["email"], account["password"])

            msg = MIMEMultipart()
            msg["From"] = account["email"]
            msg["To"] = to
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain", "utf-8"))

            server.sendmail(account["email"], to, msg.as_string())
            print(f'Email envoyé à {to} avec succès depuis {account["email"]}.')
            current_account_index = (current_account_index + 1) % len(accounts)

    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")


def invite_user_to_project(username, project_name):
    project = DB_API.get_project_id_by_project_name(project_name)
    userID = DB_API.get_userID_by_username(username)
    email = DB_API.get_user_email(userID)
    permission = 1
    joined = 1
    email = email[0]
    if not project:
        print(f"Projet '{project_name}' introuvable.")
        return
    if not userID:
        print(f"Utilisateur '{username}' introuvable.")
        return
    subject = f'Invitation à rejoindre le projet "{project_name}"'
    body = (
        f'Bonjour,\n\nVous avez été invité à rejoindre le projet "{project_name}"'
        f".\n\n\nCordialement,\nL'équipe de gestion de projet."
    )

    send_email(subject, body, email)
    DB_API.add_user_to_group(project, userID, permission, joined)


def check_tasks():
    now = datetime.now()
    print(f'Vérification des tâches à {now.strftime("%d/%m/%Y %H:%M")}...')

    tasks = DB_API.get_all_tasks()
    colonnes = [
        "taskID",
        "title",
        "description",
        "status",
        "priority",
        "covered",
        "assign",
        "due_date",
    ]
    for task_tuple in tasks:
        task = dict(zip(colonnes, task_tuple))
        due_date = task["due_date"]
        time_remaining = (due_date - now).total_seconds()
        user_emails = DB_API.get_emails_by_task_projectID(task["assign"])
        if time_remaining < 0:
            for user_email in user_emails:
                subject = f'Tâche en retard : {task["title"]}'
                body = f"""Bonjour,

        La tâche "{task['title']}" est en retard. Veuillez la terminer dans les meilleurs délais.

        Cordialement,
        L'équipe de gestion de projet."""
                send_email(subject, body, user_email)
                print(f"Email envoyé à {user_email} concernant une tâche en retard.")

        elif 0 < time_remaining < 86400:  # Moins de 24 heures
            for user_email in user_emails:
                subject = f'Rappel : La date limite approche pour "{task["title"]}"'
                body = f"""Bonjour,

        N'oubliez pas que la tâche "{task['title']}"
        doit être terminée avant le {due_date.strftime('%d/%m/%Y %H:%M')}.

        Cordialement,
        L'équipe de gestion de projet."""
                send_email(subject, body, user_email)
                print(f"Rappel envoyé à {user_email}.")


def main():
    while True:
        print("\nMenu principal :")
        print("1. Créer un utilisateur")
        print("2. Créer un projet")
        print("3. Inviter un utilisateur à un projet")
        print("4. Ajouter une tâche")
        print("5. Lister les projets")
        print("6. Lister les tâches d'un projet")
        print("7. Vérifier les tâches (envoyer des rappels)")
        print("8. Quitter")
        choice = input("Choisissez une option : ")

        if choice == "1":
            username = input("Nom d'utilisateur : ")
            email = input("Adresse e-mail : ")
            password = input("Mot de passe : ")
            gmail = "@gmail"
            if gmail in email:
                is_google_user = True
            else:
                is_google_user = False
            DB_API.add_user(username, password, email, is_google_user)
            print(f"Utilisateur {username} créé avec succès.")

        elif choice == "2":
            name = input("Nom du projet : ")
            DB_API.add_project(name)
            print(f"Projet '{name}' créé avec succès.")

        elif choice == "3":
            username = input("Nom de l'utilisateur : ")
            project_name = input("Nom du projet : ")
            invite_user_to_project(username, project_name)

        elif choice == "4":
            project_name = input("Nom du projet : ")
            task_title = input("Titre de la tâche : ")
            priority = input("Priorité (Haute, Moyenne, Basse) : ")
            if priority == "Haute":
                priority = 3
            elif priority == "Moyenne":
                priority = 2
            elif priority == "Basse":
                priority = 1
            else:
                print("erreur")
            description = input("Description : ")
            due_date_str = input("Date d'échéance (YYYY-MM-DD HH:MM) : ")
            username = input("Utilisateur assigné : ")
            userID = DB_API.get_userID_by_username(username)
            task_projectID = DB_API.add_task_group()
            DB_API.add_user_to_task_group(task_projectID, userID)
            covered = 0
            status = 0
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
            project = DB_API.get_project_id_by_project_name(project_name)

            if project:
                task_infoID = DB_API.add_task_info(
                    status, priority, task_title, description, due_date, covered, task_projectID
                )
                DB_API.add_task(project, task_infoID, userID)
                print(f"Tâche '{task_title}' ajoutée au projet '{project_name}'.")
            else:
                print(f"Projet '{project_name}' introuvable.")

        elif choice == "5":
            projects = DB_API.get_all_projects()
            for idx, project in enumerate(projects, start=1):
                print(f"{idx}. {project[1]}")

        elif choice == "6":
            project_name = input("Nom du projet : ")
            project = DB_API.get_project_id_by_project_name(project_name)
            if project:
                tasks = DB_API.get_tasks_by_project_id(project[0])
                print(tasks)
                for idx, task in enumerate(tasks, start=1):
                    print(f"{idx}. {task[1]} - {task[2]} - {task[3]}")
            else:
                print(f"Projet '{project_name}' introuvable.")

        elif choice == "7":
            check_tasks()

        elif choice == "8":
            print("Au revoir !")
            break

        else:
            print("Option invalide. Veuillez réessayer.")


def delete_user(username: str, user_id: Optional[int] = None) -> bool:
    """
    Permet de delete un utilisateur de la db et toutes ses dépendances.

    Cette fonction renvoie un boolean. En cas d'échec,
    elle renverra False et en cas de succes, elle renverra True.

    :param username: Username de l'utilisateur
    :param user_id: ID de l'utilisateur (optionnel)

    Exemple:
    >>> err = delete_user("toto")
    >>> if err:
    >>>     print("supprimé avec succes")
    >>> err = delete_user(user_id=4)
    >>> if err:
    >>>     print("supprimé avec succes")
    """
    if not user_id:
        user_id = DB_API.get_userID_by_username(username)
        if isinstance(user_id, Exception):
            return False
    err = DB_API.delete_user(user_id)
    if isinstance(err, Exception):
        return False
    return True


if __name__ == "__main__":
    main()
