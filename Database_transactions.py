def ca_par_mois(cursor):
    """
    CA de chaque mois, tous pays confondus :
    somme de (Nombre_Vendus x Prix_Unitaire).
    Renvoie une liste de tuples (Annee, Numero_Mois, CA).
    """
    cursor.execute("""
        SELECT m.Annee,
               m.Numero_Mois,
               SUM(v.Nombre_Vendus * pr.Prix_Unitaire) AS CA
        FROM Vendus v
        JOIN Produits pr ON pr.No_Produits = v.No_Produits
        JOIN Mois m      ON m.No_Mois      = v.No_Mois
        GROUP BY m.Annee, m.Numero_Mois
        ORDER BY m.Annee, m.Numero_Mois
    """)
    return cursor.fetchall()


def ca_par_pays_mois(cursor):
    """
    CA par pays (du fabricant) et par mois.
    Renvoie une liste de tuples (Nom_Pays, Annee, Numero_Mois, CA).
    """
    cursor.execute("""
        SELECT p.Nom_Pays,
               m.Annee,
               m.Numero_Mois,
               SUM(v.Nombre_Vendus * pr.Prix_Unitaire) AS CA
        FROM Vendus v
        JOIN Produits   pr ON pr.No_Produits  = v.No_Produits
        JOIN Mois       m  ON m.No_Mois       = v.No_Mois
        JOIN Cree       c  ON c.No_Produits   = pr.No_Produits
        JOIN Fabricants f  ON f.No_Fabricants = c.No_Fabricants
        JOIN Pays       p  ON p.No_Pays       = f.No_Pays
        GROUP BY p.No_Pays, m.Annee, m.Numero_Mois
        ORDER BY p.Nom_Pays, m.Annee, m.Numero_Mois
    """)
    return cursor.fetchall()


def produits_du_fabricant(cursor, no_fabricants):
    """
    Produits créés par un fabricant.
    Renvoie une liste de tuples (No_Produits, Nom_Produit, Prix_Unitaire, Couleur).
    """
    cursor.execute("""
        SELECT pr.No_Produits, pr.Nom_Produit, pr.Prix_Unitaire, pr.Couleur
        FROM Cree c
        JOIN Produits pr ON pr.No_Produits = c.No_Produits
        WHERE c.No_Fabricants = ?
        ORDER BY pr.No_Produits
    """, (no_fabricants,))
    return cursor.fetchall()

def passer_commande(cursor, no_negociant, no_fabricants, date_commande, date_limite_livraison, lignes):
    """
    Un négociant enregistre une commande adressée à un fabricant.
    lignes = [(No_Produits, Quantite), ...] : le détail des produits à fabriquer et la quantité à livrer pour chacun.
    Renvoie le numéro de la commande créée.
    """
    if not lignes:
        raise ValueError("Une commande doit contenir au moins une ligne")

    cursor.execute("BEGIN TRANSACTION")
    try:
        # Le négociant doit exister
        cursor.execute(
            "SELECT 1 FROM Negociant WHERE No_Negociant = ?", (no_negociant,))
        if cursor.fetchone() is None:
            raise ValueError(f"Le négociant {no_negociant} n'existe pas")

        # Chaque produit doit être créé par le fabricant choisi
        for no_produits, quantite in lignes:
            cursor.execute(
                "SELECT 1 FROM Cree WHERE No_Fabricants = ? AND No_Produits = ?",
                (no_fabricants, no_produits))
            if cursor.fetchone() is None:
                raise ValueError(
                    f"Le fabricant {no_fabricants} ne crée pas le produit {no_produits}")

        # La commande : négociant, fabricant, date de commande, date limite de livraison
        cursor.execute(
            "INSERT INTO Commande (No_Negociant, No_Fabricants,Date_Initialisation, Date_Limite_Livraison) VALUES (?, ?, ?, ?)",
            (no_negociant, no_fabricants, date_commande, date_limite_livraison))
        no_commande = cursor.lastrowid

        # Le détail : une ligne par produit avec la quantité à livrer
        for no_produits, quantite in lignes:
            cursor.execute(
                "INSERT INTO Concerne (No_Commande, No_Produits, Quantite) VALUES (?, ?, ?)",
                (no_commande, no_produits, quantite))

        cursor.execute("COMMIT")
    except Exception:
        cursor.execute("ROLLBACK")
        raise

    return no_commande

def ihm_bdd_description_commande(cursor):
    liste = []
    Numero_Nego = int(input("Entrer votre Numero de negociant: "))
    Numero_Fabricant = int(input("Entrer le numero de fabricant: "))

    produits = produits_du_fabricant(cursor, Numero_Fabricant)
    if not produits:
        print("Ce fabricant n'existe pas ou ne crée aucun produit")
    else:
        print("Produits de ce fabricant :")
        for no, nom, prix, couleur in produits:
            print(f"  {no} - {nom} ({couleur}) : {prix:.2f} EUR")

    while True:
        no_produit = input("Numéro de produit (vide pour terminer le choix): ")
        if no_produit == "":
            break
        quantite = int(input("Quantité à livrer: "))
        liste.append((int(no_produit), quantite))


    Date_Commande = input("Entrer la date de la commande au format YYYY-MM-DD: ")
    Date_limite_livraison = input("Entrer la date limite de livraison au format YYYY-MM-DD: ")

    return Numero_Nego, Numero_Fabricant, Date_Commande, Date_limite_livraison, liste