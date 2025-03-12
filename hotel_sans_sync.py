import threading
import time
import random

# Chambres 101 à 105
chambres = {i: True for i in range(101, 106)}  # 5 chambres
reservations = {}  # Dictionnaire des réservations

# Afficher l’état des chambres
def afficher_etat():
    print("\nÉtat des chambres :")
    for chambre, dispo in chambres.items():
        statut = "Disponible" if dispo else "Occupée"
        print(f"  Chambre {chambre} : {statut}")
    print("-" * 40)

# Fonction exécutée par chaque client
def reserver_chambre(client_id):
    while True:
        chambre_choisie = random.choice(list(chambres.keys()))  # Choix aléatoire du chambre
        if chambres[chambre_choisie]:  # Aucune synchronisation ici
            print(f"[✅] Client {client_id} tente de réserver la chambre {chambre_choisie}...")
            time.sleep(random.uniform(0.1, 0.5))  # Simule un délai avant la mise à jour
            chambres[chambre_choisie] = False  # Risque de collision ici
            reservations[client_id] = chambre_choisie
            afficher_etat()
            sejour = random.randint(5, 10)
            threading.Thread(target=depart_client, args=(client_id, sejour)).start()
        else:
            print(f"[❌] Chambre {chambre_choisie} déjà occupée pour le client {client_id}.")
        time.sleep(random.randint(5, 10))

# Fonction de départ du client
def depart_client(client_id, delay):
    time.sleep(delay)
    if client_id in reservations:
        chambre = reservations[client_id]
        chambres[chambre] = True
        del reservations[client_id]
        print(f"[🔄] Client {client_id} quitte la chambre {chambre} après {delay}s.")
        afficher_etat()

# Création des clients
clients = [{"id": i} for i in range(1, 10)]

# Démarrage des threads clients
for client in clients:
    t = threading.Thread(target=reserver_chambre, args=(client["id"],))
    t.daemon = True
    t.start()

# Garder le programme actif
while True:
    time.sleep(1)
