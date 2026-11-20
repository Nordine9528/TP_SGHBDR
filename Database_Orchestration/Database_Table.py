def create_pays(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pays (
            No_Pays   INTEGER PRIMARY KEY,
            Nom_Pays  TEXT NOT NULL,
            Climat    TEXT,
            Continent TEXT NOT NULL
        )
    """)


def create_adresse(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Adresse (
            No_Rue          INTEGER PRIMARY KEY,
            Texte_Rue       TEXT,
            Numero_Batiment TEXT,
            Ville           TEXT NOT NULL,
            Pays            TEXT NOT NULL
        )
    """)


def create_type_produit(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Type_Produit (
            No_Type   INTEGER PRIMARY KEY,
            Nom_Type  TEXT NOT NULL,
            Categorie TEXT
        )
    """)


def create_mois(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Mois (
            No_Mois     INTEGER PRIMARY KEY,
            Annee       INTEGER NOT NULL,
            Numero_Mois INTEGER NOT NULL CHECK (Numero_Mois BETWEEN 1 AND 12),
            UNIQUE (Annee, Numero_Mois)
        )
    """)



'''
Table Niveau 2 qui dépendes des tables définis au dessus de ce commentaire
'''

def create_fabricants(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Fabricants (
            No_Fabricants INTEGER PRIMARY KEY,
            No_Pays       INTEGER NOT NULL,
            Nom_Fabricant TEXT NOT NULL,
            Telephone     TEXT,
            Email         TEXT,
            FOREIGN KEY (No_Pays) REFERENCES Pays (No_Pays)
        )
    """)


def create_negociant(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Negociant (
            No_Negociant INTEGER PRIMARY KEY,
            No_Rue       INTEGER NOT NULL,
            No_Pays      INTEGER NOT NULL,
            Nom          TEXT NOT NULL,
            Prenom       TEXT NOT NULL,
            Pct_CA       REAL CHECK (Pct_CA BETWEEN 0 AND 100),
            FOREIGN KEY (No_Rue)  REFERENCES Adresse (No_Rue),
            FOREIGN KEY (No_Pays) REFERENCES Pays (No_Pays)
        )
    """)


def create_produits(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Produits (
            No_Produits   INTEGER PRIMARY KEY,
            No_Type       INTEGER NOT NULL,
            Nom_Produit   TEXT NOT NULL,
            Prix_Unitaire REAL NOT NULL CHECK (Prix_Unitaire > 0),
            Couleur       TEXT,
            FOREIGN KEY (No_Type) REFERENCES Type_Produit (No_Type)
        )
    """)


'''
Table Niveau 3 qui dépendes des tables définis au dessus de ce commentaire
'''

def create_salarie(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Salarie (
            No_Negociant     INTEGER PRIMARY KEY,
            Date_Prise_Poste TEXT NOT NULL,
            Salaire_Minimum  REAL CHECK (Salaire_Minimum >= 0),
            FOREIGN KEY (No_Negociant) REFERENCES Negociant (No_Negociant)
                ON DELETE CASCADE
        )
    """)


def create_contractuel(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Contractuel (
            No_Negociant       INTEGER PRIMARY KEY,
            Date_Debut_Contrat TEXT NOT NULL,
            Date_Fin_Contrat   TEXT,
            CHECK (Date_Fin_Contrat IS NULL
                   OR Date_Fin_Contrat >= Date_Debut_Contrat),
            FOREIGN KEY (No_Negociant) REFERENCES Negociant (No_Negociant)
                ON DELETE CASCADE
        )
    """)


def create_commande(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Commande (
            No_Commande           INTEGER PRIMARY KEY,
            No_Negociant          INTEGER NOT NULL,
            No_Fabricants         INTEGER NOT NULL,
            Date_Initialisation   TEXT NOT NULL,
            Date_Limite_Livraison TEXT,
            CHECK (Date_Limite_Livraison IS NULL
                   OR Date_Limite_Livraison >= Date_Initialisation),
            FOREIGN KEY (No_Negociant)  REFERENCES Negociant (No_Negociant),
            FOREIGN KEY (No_Fabricants) REFERENCES Fabricants (No_Fabricants)
        )
    """)


def create_cree(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cree (
            No_Fabricants INTEGER NOT NULL,
            No_Produits   INTEGER NOT NULL,
            PRIMARY KEY (No_Fabricants, No_Produits),
            FOREIGN KEY (No_Fabricants) REFERENCES Fabricants (No_Fabricants),
            FOREIGN KEY (No_Produits)   REFERENCES Produits (No_Produits)
        )
    """)


def create_vendus(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vendus (
            No_Produits   INTEGER NOT NULL,
            No_Mois       INTEGER NOT NULL,
            Nombre_Vendus INTEGER NOT NULL CHECK (Nombre_Vendus >= 0),
            PRIMARY KEY (No_Produits, No_Mois),
            FOREIGN KEY (No_Produits) REFERENCES Produits (No_Produits),
            FOREIGN KEY (No_Mois)     REFERENCES Mois (No_Mois)
        )
    """)


'''
Table Niveau 4 qui dépendes des tables définis au dessus de ce commentaire
'''

def create_historique_salarial(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Historique_Salarial (
            No_HistoSalaire  INTEGER PRIMARY KEY,
            No_Negociant     INTEGER NOT NULL,
            Date_Application TEXT NOT NULL,
            Salaire_Minimum  REAL NOT NULL CHECK (Salaire_Minimum >= 0),
            FOREIGN KEY (No_Negociant) REFERENCES Salarie (No_Negociant)
                ON DELETE CASCADE
        )
    """)


def create_concerne(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Concerne (
            No_Commande INTEGER NOT NULL,
            No_Produits INTEGER NOT NULL,
            Quantite    INTEGER NOT NULL CHECK (Quantite > 0),
            PRIMARY KEY (No_Commande, No_Produits),
            FOREIGN KEY (No_Commande) REFERENCES Commande (No_Commande)
                ON DELETE CASCADE,
            FOREIGN KEY (No_Produits) REFERENCES Produits (No_Produits)
        )
    """)




def create_vue_ca(cursor):
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS Vue_CA AS
        SELECT p.No_Pays,
               p.Nom_Pays,
               m.Annee,
               m.Numero_Mois,
               SUM(v.Nombre_Vendus * pr.Prix_Unitaire) AS CA
        FROM Vendus v
        JOIN Produits   pr ON pr.No_Produits  = v.No_Produits
        JOIN Cree       c  ON c.No_Produits   = pr.No_Produits
        JOIN Fabricants f  ON f.No_Fabricants = c.No_Fabricants
        JOIN Pays       p  ON p.No_Pays       = f.No_Pays
        JOIN Mois       m  ON m.No_Mois       = v.No_Mois
        GROUP BY p.No_Pays, m.Annee, m.Numero_Mois
    """)