import csv
import os
from datetime import datetime

FICHIER_CSV = "employes.csv"
DOSSIER_RAPPORTS = "rapports"

SEUIL_TEMPS_PARTIEL = 150      
SEUIL_TEMPS_PLEIN_MAX = 155    


def lire_employes(chemin_csv: str) -> list:
    
    employes = []
    try:
        with open(chemin_csv, newline="", encoding="utf-8") as fichier:
            lecteur = csv.DictReader(fichier)
            for ligne in lecteur:
                employe = {
                    "id": int(ligne["id"]),
                    "nom": ligne["nom"].strip(),
                    "prenom": ligne["prenom"].strip(),
                    "role": ligne["role"].strip(),
                    "equipe": ligne["equipe"].strip(),
                    "heures_travaillees": float(ligne["heures_travaillees"]),
                    "taux_horaire": float(ligne["taux_horaire"]),
                    "prime": float(ligne["prime"]),
                }
                employes.append(employe)
    except FileNotFoundError:
        print(f"[ERREUR] Le fichier '{chemin_csv}' est introuvable.")
    except KeyError as e:
        print(f"[ERREUR] Colonne manquante dans le CSV : {e}")
    return employes

def calculer_salaire_brut(employe: dict) -> float:
    
    return employe["heures_travaillees"] * employe["taux_horaire"] + employe["prime"]


def calculer_salaire_horaire_reel(employe: dict) -> float:
    
    salaire_brut = calculer_salaire_brut(employe)
    if employe["heures_travaillees"] == 0:
        return 0.0
    return salaire_brut / employe["heures_travaillees"]


def determiner_statut(heures: float) -> str:
    """
    Détermine le statut d'un employé selon ses heures travaillées.

    < 150h        → Temps partiel
    150h à 155h   → Temps plein
    > 155h        → Heures supplémentaires

    :param heures: Nombre d'heures travaillées dans le mois.
    :return: Chaîne décrivant le statut.
    """
    if heures < SEUIL_TEMPS_PARTIEL:
        return "Temps partiel"
    elif heures <= SEUIL_TEMPS_PLEIN_MAX:
        return "Temps plein"
    else:
        return "Heures supplémentaires"


def connexion(employes: list) -> dict | None:
    
    print("\n╔══════════════════════════════════════╗")
    print("║   Système RH – Connexion             ║")
    print("╚══════════════════════════════════════╝")

    saisie = input("Entrez votre identifiant employé : ").strip()

    try:
        id_saisi = int(saisie)
    except ValueError:
        print("[ERREUR] L'identifiant doit être un nombre entier.")
        return None

    for employe in employes:
        if employe["id"] == id_saisi:
            print(f"\nBienvenue, {employe['prenom']} {employe['nom']} "
                  f"({employe['role'].capitalize()}) !")
            return employe

    print("[ERREUR] Identifiant introuvable.")
    return None


def creer_dossier_rapports():
    """Crée le dossier de rapports s'il n'existe pas encore."""
    if not os.path.exists(DOSSIER_RAPPORTS):
        os.makedirs(DOSSIER_RAPPORTS)


def horodatage() -> str:
    """Retourne un horodatage formaté pour les noms de fichiers."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")




def generer_rapport_individuel(employe: dict) -> str:

    salaire_brut = calculer_salaire_brut(employe)
    salaire_horaire_reel = calculer_salaire_horaire_reel(employe)
    statut = determiner_statut(employe["heures_travaillees"])

    lignes = [
        "=" * 50,
        "       RAPPORT INDIVIDUEL",
        "=" * 50,
        "",
        "── IDENTITÉ ──────────────────────────────────",
        f"  Nom           : {employe['nom']}",
        f"  Prénom        : {employe['prenom']}",
        f"  Équipe        : {employe['equipe']}",
        f"  Identifiant   : {employe['id']}",
        f"  Rôle          : {employe['role'].capitalize()}",
        "",
        "── DONNÉES DU MOIS ───────────────────────────",
        f"  Heures travaillées : {employe['heures_travaillees']:.2f} h",
        f"  Taux horaire       : {employe['taux_horaire']:.2f} €/h",
        f"  Prime              : {employe['prime']:.2f} €",
        "",
        "── CALCULS ───────────────────────────────────",
        f"  Salaire brut        : {salaire_brut:.2f} €",
        f"  Salaire horaire réel: {salaire_horaire_reel:.2f} €/h",
        "",
        "── STATUT ────────────────────────────────────",
        f"  {statut}",
        "",
        "=" * 50,
    ]
    return "\n".join(lignes)


def sauvegarder_rapport(contenu: str, nom_fichier: str):
    
    creer_dossier_rapports()
    chemin = os.path.join(DOSSIER_RAPPORTS, f"{nom_fichier}.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"[OK] Rapport sauvegardé : {chemin}")


def afficher_et_sauvegarder(contenu: str, nom_fichier: str):
    """Affiche le rapport dans la console et le sauvegarde."""
    print("\n" + contenu)
    sauvegarder_rapport(contenu, nom_fichier)




def generer_rapport_equipe(employes: list, nom_equipe: str) -> str:
    
    membres = [e for e in employes if e["equipe"] == nom_equipe]

    if not membres:
        return f"[INFO] Aucun employé trouvé dans l'équipe '{nom_equipe}'."

    salaires = [calculer_salaire_brut(e) for e in membres]
    heures_totales = sum(e["heures_travaillees"] for e in membres)
    salaire_moyen = sum(salaires) / len(salaires)
    prime_moyenne = sum(e["prime"] for e in membres) / len(membres)
    salaire_min = min(salaires)
    salaire_max = max(salaires)

    lignes = [
        "=" * 50,
        f"       RAPPORT ÉQUIPE : {nom_equipe.upper()}",
        "=" * 50,
        "",
        f"  Nombre d'employés          : {len(membres)}",
        f"  Total heures travaillées   : {heures_totales:.2f} h",
        f"  Salaire brut moyen         : {salaire_moyen:.2f} €",
        f"  Prime moyenne              : {prime_moyenne:.2f} €",
        f"  Salaire minimum            : {salaire_min:.2f} €",
        f"  Salaire maximum            : {salaire_max:.2f} €",
        "",
        "── MEMBRES ───────────────────────────────────",
    ]

    for m in membres:
        sb = calculer_salaire_brut(m)
        statut = determiner_statut(m["heures_travaillees"])
        lignes.append(
            f"  [{m['id']:>3}] {m['prenom']} {m['nom']:<15} "
            f"| {sb:>8.2f} € | {statut}"
        )

    lignes += ["", "=" * 50]
    return "\n".join(lignes)



def generer_rapport_global(employes: list) -> str:
    
    salaires = {e["id"]: calculer_salaire_brut(e) for e in employes}
    heures_totales = sum(e["heures_travaillees"] for e in employes)
    salaire_moyen = sum(salaires.values()) / len(salaires)
    salaire_min = min(salaires.values())
    salaire_max = max(salaires.values())
    total_primes = sum(e["prime"] for e in employes)

    
    id_max = max(salaires, key=salaires.get)
    id_min = min(salaires, key=salaires.get)
    employe_max = next(e for e in employes if e["id"] == id_max)
    employe_min = next(e for e in employes if e["id"] == id_min)
    repartition = {"Temps partiel": 0, "Temps plein": 0, "Heures supplémentaires": 0}
    for e in employes:
        statut = determiner_statut(e["heures_travaillees"])
        repartition[statut] += 1

    lignes = [
        "=" * 50,
        "       RAPPORT GLOBAL ENTREPRISE",
        "=" * 50,
        "",
        "── STATISTIQUES GÉNÉRALES ────────────────────",
        f"  Nombre total d'employés     : {len(employes)}",
        f"  Total heures travaillées    : {heures_totales:.2f} h",
        f"  Salaire moyen               : {salaire_moyen:.2f} €",
        f"  Salaire minimum             : {salaire_min:.2f} €",
        f"  Salaire maximum             : {salaire_max:.2f} €",
        f"  Total primes versées        : {total_primes:.2f} €",
        "",
        "── EMPLOYÉS REMARQUABLES ─────────────────────",
        f"  Salaire le plus élevé  : {employe_max['prenom']} {employe_max['nom']} "
        f"({salaire_max:.2f} €)",
        f"  Salaire le plus faible : {employe_min['prenom']} {employe_min['nom']} "
        f"({salaire_min:.2f} €)",
        "",
        "── RÉPARTITION PAR STATUT ────────────────────",
        f"  Temps partiel           : {repartition['Temps partiel']} employé(s)",
        f"  Temps plein             : {repartition['Temps plein']} employé(s)",
        f"  Heures supplémentaires  : {repartition['Heures supplémentaires']} employé(s)",
        "",
        "=" * 50,
    ]
    return "\n".join(lignes)


def menu_employe(utilisateur: dict, employes: list):
    print("\n── Menu Employé ──")
    print("1. Voir mon rapport individuel")
    print("0. Se déconnecter")

    choix = input("\nVotre choix : ").strip()

    if choix == "1":
        contenu = generer_rapport_individuel(utilisateur)
        nom_fichier = f"rapport_individuel_{utilisateur['id']}_{horodatage()}"
        afficher_et_sauvegarder(contenu, nom_fichier)
    elif choix == "0":
        print("Déconnexion.")
    else:
        print("[INFO] Choix invalide.")


def menu_manager(utilisateur: dict, employes: list):
    equipe = utilisateur["equipe"]
    membres_equipe = [e for e in employes if e["equipe"] == equipe]

    while True:
        print("\n── Menu Manager ──")
        print("1. Voir mon rapport individuel")
        print("2. Voir le rapport d'un membre de mon équipe")
        print("3. Voir le rapport de mon équipe")
        print("0. Se déconnecter")

        choix = input("\nVotre choix : ").strip()

        if choix == "0":
            print("Déconnexion.")
            break

        elif choix == "1":
            contenu = generer_rapport_individuel(utilisateur)
            nom_fichier = f"rapport_individuel_{utilisateur['id']}_{horodatage()}"
            afficher_et_sauvegarder(contenu, nom_fichier)

        elif choix == "2":
            print(f"\nMembres de l'équipe {equipe} :")
            for m in membres_equipe:
                print(f"  [{m['id']}] {m['prenom']} {m['nom']}")
            saisie = input("Identifiant du membre : ").strip()
            try:
                id_choisi = int(saisie)
            except ValueError:
                print("[ERREUR] Identifiant invalide.")
                continue

            cible = next((e for e in membres_equipe if e["id"] == id_choisi), None)
            if cible:
                contenu = generer_rapport_individuel(cible)
                nom_fichier = f"rapport_individuel_{cible['id']}_{horodatage()}"
                afficher_et_sauvegarder(contenu, nom_fichier)
            else:
                print("[ACCÈS REFUSÉ] Cet employé n'appartient pas à votre équipe.")

        elif choix == "3":
            contenu = generer_rapport_equipe(employes, equipe)
            nom_fichier = f"rapport_equipe_{equipe.lower()}_{horodatage()}"
            afficher_et_sauvegarder(contenu, nom_fichier)

        else:
            print("[INFO] Choix invalide.")


def menu_directeur(utilisateur: dict, employes: list):

    equipes = sorted(set(e["equipe"] for e in employes))

    while True:
        print("\n── Menu Directeur ──")
        print("1. Voir mon rapport individuel")
        print("2. Voir le rapport individuel d'un employé")
        print("3. Voir le rapport d'une équipe")
        print("4. Voir le rapport global")
        print("0. Se déconnecter")

        choix = input("\nVotre choix : ").strip()

        if choix == "0":
            print("Déconnexion.")
            break

        elif choix == "1":
            contenu = generer_rapport_individuel(utilisateur)
            nom_fichier = f"rapport_individuel_{utilisateur['id']}_{horodatage()}"
            afficher_et_sauvegarder(contenu, nom_fichier)

        elif choix == "2":
            print("\nListe des employés :")
            for e in employes:
                print(f"  [{e['id']:>3}] {e['prenom']} {e['nom']:<15} "
                      f"| {e['equipe']:<15} | {e['role']}")
            saisie = input("Identifiant de l'employé : ").strip()
            try:
                id_choisi = int(saisie)
            except ValueError:
                print("[ERREUR] Identifiant invalide.")
                continue

            cible = next((e for e in employes if e["id"] == id_choisi), None)
            if cible:
                contenu = generer_rapport_individuel(cible)
                nom_fichier = f"rapport_individuel_{cible['id']}_{horodatage()}"
                afficher_et_sauvegarder(contenu, nom_fichier)
            else:
                print("[ERREUR] Employé introuvable.")

        elif choix == "3":
            print("\nÉquipes disponibles :")
            for i, eq in enumerate(equipes, 1):
                print(f"  {i}. {eq}")
            saisie = input("Numéro de l'équipe : ").strip()
            try:
                idx = int(saisie) - 1
                if 0 <= idx < len(equipes):
                    equipe_choisie = equipes[idx]
                    contenu = generer_rapport_equipe(employes, equipe_choisie)
                    nom_fichier = f"rapport_equipe_{equipe_choisie.lower()}_{horodatage()}"
                    afficher_et_sauvegarder(contenu, nom_fichier)
                else:
                    print("[ERREUR] Numéro hors plage.")
            except ValueError:
                print("[ERREUR] Saisie invalide.")

        elif choix == "4":
            contenu = generer_rapport_global(employes)
            nom_fichier = f"rapport_global_{horodatage()}"
            afficher_et_sauvegarder(contenu, nom_fichier)

        else:
            print("[INFO] Choix invalide.")


def main():
    employes = lire_employes(FICHIER_CSV)
    if not employes:
        print("[ERREUR] Impossible de charger les données. Arrêt du programme.")
        return

    print(f"[INFO] {len(employes)} employé(s) chargé(s).")

    # Connexion
    utilisateur = connexion(employes)
    if utilisateur is None:
        return

    # Redirection selon le rôle
    role = utilisateur["role"]

    if role == "employe":
        menu_employe(utilisateur, employes)
    elif role == "manager":
        menu_manager(utilisateur, employes)
    elif role == "directeur":
        menu_directeur(utilisateur, employes)
    else:
        print(f"[ERREUR] Rôle inconnu : '{role}'.")


if __name__ == "__main__":
    main()
