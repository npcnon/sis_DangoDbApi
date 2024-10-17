import mysql.connector

# Database connection settings
config = {
    'user': 'u286307273_portal',          # Replace with your MariaDB username
    'password': 'W5Cn6Q>+:l',             # Replace with your MariaDB password
    'host': 'srv1417.hstgr.io',           # Replace with your host (e.g., 'localhost' or IP)
    'database': 'u286307273_portal',      # Replace with your database name
    'port': 3306                          # Optional: use the default MySQL/MariaDB port 3306
}

try:
    # Establish a connection to the MariaDB database
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Disable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

    # List of DROP TABLE commands
    drop_table_commands = [
        "DROP TABLE IF EXISTS `DangoDBApp_tblstudentacademichistory`;",
        "DROP TABLE IF EXISTS `django_cron_cronjoblock`;",
        "DROP TABLE IF EXISTS `django_celery_beat_periodictasks`;",
        "DROP TABLE IF EXISTS `django_admin_log`;",
        "DROP TABLE IF EXISTS `users_user_user_permissions`;",
        "DROP TABLE IF EXISTS `django_celery_beat_clockedschedule`;",
        "DROP TABLE IF EXISTS `django_celery_beat_intervalschedule`;",
        "DROP TABLE IF EXISTS `auth_group_permissions`;",
        "DROP TABLE IF EXISTS `django_cron_cronjoblog`;",
        "DROP TABLE IF EXISTS `DangoDBApp_tblemployee`;",
        "DROP TABLE IF EXISTS `DangoDBApp_tblstudentpersonaldata`;",
        "DROP TABLE IF EXISTS `django_celery_beat_crontabschedule`;",
        "DROP TABLE IF EXISTS `django_celery_beat_solarschedule`;",
        "DROP TABLE IF EXISTS `DangoDBApp_tblstudentaddpersonaldata`;",
        "DROP TABLE IF EXISTS `auth_permission`;",
        "DROP TABLE IF EXISTS `django_celery_results_taskresult`;",
        "DROP TABLE IF EXISTS `DangoDBApp_tblstudentfamilybackground`;",
        "DROP TABLE IF EXISTS `django_content_type`;",
        "DROP TABLE IF EXISTS `users_user_groups`;",
        "DROP TABLE IF EXISTS `DangoDBApp_tblprogram`;",
        "DROP TABLE IF EXISTS `django_celery_results_groupresult`;",
        "DROP TABLE IF EXISTS `django_session`;",
        "DROP TABLE IF EXISTS `DangoDBApp_tbldepartment`;",
        "DROP TABLE IF EXISTS `DangoDBApp_tblclass`;",
        "DROP TABLE IF EXISTS `DangoDBApp_emailverification`;",
        "DROP TABLE IF EXISTS `DangoDBApp_tblcampus`;",
        "DROP TABLE IF EXISTS `DangoDBApp_tblstudentacademicbackground`;",
        "DROP TABLE IF EXISTS `django_migrations`;",
        "DROP TABLE IF EXISTS `users_user`;",
        "DROP TABLE IF EXISTS `DangoDBApp_tblstudentofficialinfo`;",
        "DROP TABLE IF EXISTS `DangoDBApp_tblstudentbasicinfo`;",
        "DROP TABLE IF EXISTS `auth_group`;",
        "DROP TABLE IF EXISTS `DangoDBApp_tblsemester`;",
        "DROP TABLE IF EXISTS `django_celery_results_chordcounter`;",
        "DROP TABLE IF EXISTS `django_celery_beat_periodictask`;",
        "DROP TABLE IF EXISTS `users_profile`;",
        "DROP TABLE IF EXISTS `DangoDBApp_tblbugreport`;"
    ]

    # Execute each DROP TABLE command
    for command in drop_table_commands:
        cursor.execute(command)
        print(f"Executed: {command}")

    # Re-enable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    # Commit changes
    connection.commit()
    print("Tables dropped successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Ensure cursor and connection are defined before closing
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'connection' in locals() and connection:
        connection.close()
