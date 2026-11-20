import sqlite3
import Database_Orchestration.Database_Creation as db_crt
import Database_Orchestration.Database_insertion as db_insert


def creation_tables(cursor):
    try:
        db_crt.db_create_table_1er_Niveau(cursor)
        print("Tables de 1er niveau initialise")
    except Exception as e:
        print(f"Erreur dans la création des tables de 1er niveau :  {e}")

    try:
        db_crt.db_create_table_2eme_Niveau(cursor)
        print("Tables de 2eme niveau initialise")
    except Exception as e:
        print(f"Erreur dans la création des tables de 2eme niveau :  {e}")

    try:
        db_crt.db_create_table_3eme_Niveau(cursor)
        print("Tables de 3eme niveau initialise")
    except Exception as e:
        print(f"Erreur dans la création des tables de 3eme niveau :  {e}")

    try:
        db_crt.db_create_table_4eme_Niveau(cursor)
        print("Tables de 4eme niveau initialise")
    except Exception as e:
        print(f"Erreur dans la création des tables de 4eme niveau :  {e}")

database_name = 'NaniAzi.db'
connection = sqlite3.connect(database_name)
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

creation_tables(cursor)
db_insert.charger_donnees(cursor)