import sqlite3
import Database_Orchestration.Database_Creation as db_crt
import Database_Orchestration.Database_insertion as db_insert
import Database_transactions as db_trsct


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

choix = input("Voulez vous enregistrer une commande dans la Base de donnee ? [y/n]: ")
choix = choix.lower()
if choix == "y" or choix == "yes":
    No_nego, No_fab, Date_cmd, Date_limite_livraison, liste_produits = db_trsct.ihm_bdd_description_commande(cursor)

    db_trsct.passer_commande(cursor, No_nego, No_fab,Date_cmd,Date_limite_livraison,liste_produits)
