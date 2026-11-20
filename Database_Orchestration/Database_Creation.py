import sqlite3
import Database_Orchestration.Database_Table as db_tbl

def db_create_table_1er_Niveau(cursor):
    db_tbl.create_pays(cursor)
    db_tbl.create_adresse(cursor)
    db_tbl.create_type_produit(cursor)
    db_tbl.create_mois(cursor)

def db_create_table_2eme_Niveau(cursor):
    db_tbl.create_fabricants(cursor)
    db_tbl.create_negociant(cursor)
    db_tbl.create_produits(cursor)

def db_create_table_3eme_Niveau(cursor):
    db_tbl.create_salarie(cursor)
    db_tbl.create_contractuel(cursor)
    db_tbl.create_commande(cursor)
    db_tbl.create_cree(cursor)
    db_tbl.create_vendus(cursor)

def db_create_table_4eme_Niveau(cursor):
    db_tbl.create_historique_salarial(cursor)
    db_tbl.create_concerne(cursor)
    db_tbl.create_vue_ca(cursor)
