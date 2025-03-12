import threading  # Module pour la gestion des threads (exécution parallèle)
import time       # Module pour les délais (pause/sommeil)
import random     # Module pour faire des choix aléatoires (chambres, durée, etc.)

# Création d'un verrou pour protéger l'accès aux ressources partagées
lock = threading.Lock()

# Condition de synchronisation basée sur ce verrou, elle permet à un thread d'attendre jusqu'à ce qu'une autre action le réveille
condition = threading.Condition(lock)

# Dictionnaire représentant les chambres (chambre_numéro : True si disponible, False si occupée)
chambres = {i: True for i in range(101, 106)}  # 5 chambres : 101 à 105

# Dictionnaire des réservations en cours : (client_id : numéro de chambre réservée)
reservations = {}

# Fonction pour afficher l'état de toutes les chambres (occupée ou disponible)
def afficher_etat():
    print("\nÉtat des chambres :")
    for chambre, dispo in chambres.items():
        statut = "Disponible" if dispo else "Occupée"
        print(f"  Chambre {chambre} : {statut}")
    print("-" * 40)

# Fonction exécutée par chaque thread client, elle tente de réserver une chambre aléatoire, attend si elle est occupée, puis recommence plus tard
def reserver_chambre(client_id):
    while True:  # Boucle infinie pour permettre à un client de réserver plusieurs fois
        # Le client choisit une chambre au hasard
        chambre_choisie = random.choice(list(chambres.keys()))

        # Synchronisation pour vérifier ou réserver la chambre de manière sûre
        with condition:
            # Si la chambre est occupée, le client attend qu'elle se libère
            while not chambres[chambre_choisie]:
                print(f"[⏳] Client {client_id} attend que la chambre {chambre_choisie} se libère...")
                condition.wait()  # Le thread s'endort jusqu'à être réveillé

            # ✅ Si la chambre est libre, le client la réserve
            chambres[chambre_choisie] = False
            reservations[client_id] = chambre_choisie
            print(f"[✅] Client {client_id} a réservé la chambre {chambre_choisie}.")
            afficher_etat()

            # Planification du départ du client (il partira après un délai aléatoire)
            sejour = random.randint(5, 10)  # Durée du séjour entre 5 et 10 secondes
            threading.Thread(target=depart_client, args=(client_id, sejour)).start()

        # Le client attend un moment (entre 10 et 20 secondes) avant de tenter une nouvelle réservation
        time.sleep(random.randint(10, 20))

# Fonction appelée automatiquement quand un client quitte sa chambre
def depart_client(client_id, delay):
    time.sleep(delay)  # Attendre la durée du séjour avant le départ
    with condition:  # Synchronisation pour libérer la chambre en toute sécurité
        if client_id in reservations:
            chambre = reservations[client_id]  # Obtenir la chambre occupée
            chambres[chambre] = True           # Libérer la chambre
            del reservations[client_id]        # Supprimer la réservation du client
            print(f"[🔄] Client {client_id} quitte la chambre {chambre} après {delay}s.")
            afficher_etat()
            condition.notify_all()  # Réveiller tous les clients qui attendent une chambre

# Création d'une liste de clients (identifiants de 1 à 9)
clients = [{"id": i} for i in range(1, 10)]

# Lancement d'un thread pour chaque client
for client in clients:
    t = threading.Thread(target=reserver_chambre, args=(client["id"],))
    t.daemon = True  # Thread "daemon" : il s'arrête automatiquement si le programme principal se termine
    t.start()

# Boucle infinie pour que le programme principal reste actif (sinon tous les threads s’arrêtent immédiatement)
while True:
    time.sleep(1)  # Pause pour ne pas saturer le processeur
