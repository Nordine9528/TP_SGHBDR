import csv

DOSSIER = "/Users/nordinetsouli/PycharmProjects/WelcomeScreen/TP_SGHBDR_NTSO_YMOU/data"


def lire_csv(nom_fichier):
    try:
        with open(f"{DOSSIER}/{nom_fichier}", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except  Exception as e:
        print(e)


# Niveau 1
def insert_pays(cursor):
    for l in lire_csv("negociants.csv") + lire_csv("catalogue.csv"):
        cursor.execute(
            "INSERT OR IGNORE INTO Pays (No_Pays, Nom_Pays, Climat, Continent) VALUES (?, ?, ?, ?)",
            (l["No_Pays"], l["Nom_Pays"], l["Climat"], l["Continent"]))


def insert_adresse(cursor):
    for l in lire_csv("negociants.csv"):
        cursor.execute(
            "INSERT OR IGNORE INTO Adresse (No_Rue, Texte_Rue, Numero_Batiment, Ville, Pays) VALUES (?, ?, ?, ?, ?)",
            (l["No_Rue"], l["Texte_Rue"], l["Numero_Batiment"], l["Ville"], l["Pays_Adresse"]))


def insert_type_produit(cursor):
    for l in lire_csv("catalogue.csv"):
        cursor.execute(
            "INSERT OR IGNORE INTO Type_Produit (No_Type, Nom_Type, Categorie) VALUES (?, ?, ?)",
            (l["No_Type"], l["Nom_Type"], l["Categorie"]))


def insert_mois(cursor):
    for l in lire_csv("ventes.csv"):
        cursor.execute(
            "INSERT OR IGNORE INTO Mois (No_Mois, Annee, Numero_Mois) VALUES (?, ?, ?)",
            (l["No_Mois"], l["Annee"], l["Numero_Mois"]))


# Niveau 2
def insert_fabricants(cursor):
    for l in lire_csv("catalogue.csv"):
        cursor.execute(
            "INSERT OR IGNORE INTO Fabricants (No_Fabricants, No_Pays, Nom_Fabricant, Telephone, Email) VALUES (?, ?, ?, ?, ?)",
            (l["No_Fabricants"], l["No_Pays"], l["Nom_Fabricant"], l["Telephone"], l["Email"]))


def insert_negociant(cursor):
    for l in lire_csv("negociants.csv"):
        cursor.execute(
            "INSERT OR IGNORE INTO Negociant (No_Negociant, No_Rue, No_Pays, Nom, Prenom, Pct_CA) VALUES (?, ?, ?, ?, ?, ?)",
            (l["No_Negociant"], l["No_Rue"], l["No_Pays"], l["Nom"], l["Prenom"], l["Pct_CA"]))


def insert_produits(cursor):
    for l in lire_csv("catalogue.csv"):
        cursor.execute(
            "INSERT OR IGNORE INTO Produits (No_Produits, No_Type, Nom_Produit, Prix_Unitaire, Couleur) VALUES (?, ?, ?, ?, ?)",
            (l["No_Produits"], l["No_Type"], l["Nom_Produit"], l["Prix_Unitaire"], l["Couleur"]))


# Niveau 3

def insert_salarie(cursor):
    for l in lire_csv("negociants.csv"):
        if l["Statut"] == "Salarie":
            cursor.execute(
                "INSERT OR IGNORE INTO Salarie (No_Negociant, Date_Prise_Poste, Salaire_Minimum) VALUES (?, ?, ?)",
                (l["No_Negociant"], l["Date_Prise_Poste"], l["Salaire_Minimum"]))


def insert_contractuel(cursor):
    for l in lire_csv("negociants.csv"):
        if l["Statut"] == "Contractuel":
            cursor.execute(
                "INSERT OR IGNORE INTO Contractuel (No_Negociant, Date_Debut_Contrat, Date_Fin_Contrat) VALUES (?, ?, ?)",
                (l["No_Negociant"], l["Date_Debut_Contrat"], l["Date_Fin_Contrat"]))


def insert_commande(cursor):
    for l in lire_csv("commandes.csv"):
        cursor.execute(
            "INSERT OR IGNORE INTO Commande (No_Commande, No_Negociant, No_Fabricants, Date_Initialisation, Date_Limite_Livraison) VALUES (?, ?, ?, ?, ?)",
            (l["No_Commande"], l["No_Negociant"], l["No_Fabricants"], l["Date_Initialisation"], l["Date_Limite_Livraison"]))


def insert_cree(cursor):
    for l in lire_csv("catalogue.csv"):
        cursor.execute(
            "INSERT OR IGNORE INTO Cree (No_Fabricants, No_Produits) VALUES (?, ?)",
            (l["No_Fabricants"], l["No_Produits"]))


def insert_vendus(cursor):
    for l in lire_csv("ventes.csv"):
        cursor.execute(
            "INSERT OR IGNORE INTO Vendus (No_Produits, No_Mois, Nombre_Vendus) VALUES (?, ?, ?)",
            (l["No_Produits"], l["No_Mois"], l["Nombre_Vendus"]))


# Niveau 4
def insert_historique_salarial(cursor):
    for l in lire_csv("negociants.csv"):
        if l["Statut"] == "Salarie":
            cursor.execute(
                "INSERT OR IGNORE INTO Historique_Salarial (No_HistoSalaire, No_Negociant, Date_Application, Salaire_Minimum) VALUES (?, ?, ?, ?)",
                (l["No_HistoSalaire"], l["No_Negociant"], l["Date_Application"], l["Salaire_Histo"]))


def insert_concerne(cursor):
    for l in lire_csv("commandes.csv"):
        cursor.execute(
            "INSERT OR IGNORE INTO Concerne (No_Commande, No_Produits, Quantite) VALUES (?, ?, ?)",
            (l["No_Commande"], l["No_Produits"], l["Quantite"]))



def charger_donnees(cursor):
    cursor.execute("BEGIN TRANSACTION")
    try:
        # Niveau 1
        insert_pays(cursor)
        insert_adresse(cursor)
        insert_type_produit(cursor)
        insert_mois(cursor)
        # Niveau 2
        insert_fabricants(cursor)
        insert_negociant(cursor)
        insert_produits(cursor)
        # Niveau 3
        insert_salarie(cursor)
        insert_contractuel(cursor)
        insert_commande(cursor)
        insert_cree(cursor)
        insert_vendus(cursor)
        # Niveau 4
        insert_historique_salarial(cursor)
        insert_concerne(cursor)
        cursor.execute("COMMIT")
    except Exception:
        cursor.execute("ROLLBACK")
        raise
