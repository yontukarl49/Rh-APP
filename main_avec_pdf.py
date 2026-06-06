import csv
import os
from datetime import datetime

try:
    from rapport_pdf import sauvegarder_rapport_pdf, FPDF_DISPONIBLE
except ImportError:
    FPDF_DISPONIBLE = False
    def sauvegarder_rapport_pdf(contenu, nom_fichier):
        print("[INFO] Module PDF non disponible.")


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
    """salaire_brut = heures_travaillees × taux_horaire + prime"""
    return employe["heures_travaillees"] * employe["taux_horaire"] + employe["prime"]


def calculer_salaire_horaire_reel(employe: dict) -> float:
    """salaire_horaire_reel = salaire_brut / heures_travaillees"""
    salaire_brut = calculer_salaire_brut(employe)
    if employe["heures_travaillees"] == 0:
        return 0.0
    return salaire_brut / employe["heures_travaillees"]


def determiner_statut(heures: float) -> str:
    """Détermine le statut selon les heures travaillées."""
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
    """Retourne un horodatage pour les noms de fichiers."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def sauvegarder_txt(contenu: str, nom_fichier: str):
    """Sauvegarde le rapport au format .txt."""
    creer_dossier_rapports()
    chemin = os.path.join(DOSSIER_RAPPORTS, f"{nom_fichier}.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"[OK] Rapport TXT sauvegardé : {chemin}")


def afficher_et_sauvegarder(contenu: str, nom_fichier: str, format_pdf: bool = False):
    
    print("\n" + contenu)
    if format_pdf and FPDF_DISPONIBLE:
        sauvegarder_rapport_pdf(contenu, nom_fichier)
    else:
        sauvegarder_txt(contenu, nom_fichier)


def generer_rapport_individuel(employe: dict) -> str:
    """Génère le contenu texte du rapport individuel."""
    salaire_brut = calculer_salaire_brut(employe)
    salaire_horaire_reel = calculer_salaire_horaire_reel(employe)
    statut = determiner_statut(employe["heures_travaillees"])

    lignes = [
        "=" * 50,
        "       RAPPORT INDIVIDUEL",
        "=" * 50,
        "",
        "── IDENTITE ──────────────────────────────────",
        f"  Nom           : {employe['nom']}",
        f"  Prenom        : {employe['prenom']}",
        f"  Equipe        : {employe['equipe']}",
        f"  Identifiant   : {employe['id']}",
        f"  Role          : {employe['role'].capitalize()}",
        "",
        "── DONNEES DU MOIS ───────────────────────────",
        f"  Heures travaillees : {employe['heures_travaillees']:.2f} h",
        f"  Taux horaire       : {employe['taux_horaire']:.2f} EUR/h",
        f"  Prime              : {employe['prime']:.2f} EUR",
        "",
        "── CALCULS ───────────────────────────────────",
        f"  Salaire brut         : {salaire_brut:.2f} EUR",
        f"  Salaire horaire reel : {salaire_horaire_reel:.2f} EUR/h",
        "",
        "── STATUT ────────────────────────────────────",
        f"  {statut}",
        "",
        "=" * 50,
    ]
    return "\n".join(lignes)



def generer_rapport_equipe(employes: list, nom_equipe: str) -> str:
    """Génère le rapport d'une équipe spécifique."""
    membres = [e for e in employes if e["equipe"] == nom_equipe]
    if not membres:
        return f"[INFO] Aucun employé dans l'équipe '{nom_equipe}'."

    salaires = [calculer_salaire_brut(e) for e in membres]
    heures_totales = sum(e["heures_travaillees"] for e in membres)
    salaire_moyen = sum(salaires) / len(salaires)
    prime_moyenne = sum(e["prime"] for e in membres) / len(membres)
    salaire_min = min(salaires)
    salaire_max = max(salaires)

    lignes = [
        "=" * 50,
        f"       RAPPORT EQUIPE : {nom_equipe.upper()}",
        "=" * 50,
        "",
        f"  Nombre d'employes          : {len(membres)}",
        f"  Total heures travaillees   : {heures_totales:.2f} h",
        f"  Salaire brut moyen         : {salaire_moyen:.2f} EUR",
        f"  Prime moyenne              : {prime_moyenne:.2f} EUR",
        f"  Salaire minimum            : {salaire_min:.2f} EUR",
        f"  Salaire maximum            : {salaire_max:.2f} EUR",
        "",
        "── MEMBRES ───────────────────────────────────",
    ]
    for m in membres:
        sb = calculer_salaire_brut(m)
        statut = determiner_statut(m["heures_travaillees"])
        lignes.append(
            f"  [{m['id']:>3}] {m['prenom']} {m['nom']:<15} "
            f"| {sb:>8.2f} EUR | {statut}"
        )
    lignes += ["", "=" * 50]
    return "\n".join(lignes)

def generer_rapport_global(employes: list) -> str:
    """Génère le rapport global de l'entreprise."""
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
        "── STATISTIQUES GENERALES ────────────────────",
        f"  Nombre total d'employes     : {len(employes)}",
        f"  Total heures travaillees    : {heures_totales:.2f} h",
        f"  Salaire moyen               : {salaire_moyen:.2f} EUR",
        f"  Salaire minimum             : {salaire_min:.2f} EUR",
        f"  Salaire maximum             : {salaire_max:.2f} EUR",
        f"  Total primes versees        : {total_primes:.2f} EUR",
        "",
        "── EMPLOYES REMARQUABLES ─────────────────────",
        f"  Salaire le plus eleve  : {employe_max['prenom']} {employe_max['nom']} "
        f"({salaire_max:.2f} EUR)",
        f"  Salaire le plus faible : {employe_min['prenom']} {employe_min['nom']} "
        f"({salaire_min:.2f} EUR)",
        "",
        "── REPARTITION PAR STATUT ────────────────────",
        f"  Temps partiel           : {repartition['Temps partiel']} employe(s)",
        f"  Temps plein             : {repartition['Temps plein']} employe(s)",
        f"  Heures supplementaires  : {repartition['Heures supplémentaires']} employe(s)",
        "",
        "=" * 50,
    ]
    return "\n".join(lignes)


def choisir_format() -> bool:
    
    if not FPDF_DISPONIBLE:
        return False
    print("\nFormat de sortie :")
    print("  1. TXT  (défaut)")
    print("  2. PDF  (bonus)")
    choix = input("Votre choix : ").strip()
    return choix == "2"


def menu_employe(utilisateur: dict, employes: list):
    """Menu d'un employé – rapport personnel uniquement."""
    print("\n── Menu Employe ──")
    print("1. Voir mon rapport individuel")
    print("0. Se deconnecter")

    choix = input("\nVotre choix : ").strip()
    if choix == "1":
        pdf = choisir_format()
        contenu = generer_rapport_individuel(utilisateur)
        nom = f"rapport_individuel_{utilisateur['id']}_{horodatage()}"
        afficher_et_sauvegarder(contenu, nom, format_pdf=pdf)
    elif choix == "0":
        print("Deconnexion.")
    else:
        print("[INFO] Choix invalide.")


def menu_manager(utilisateur: dict, employes: list):
    """Menu d'un manager – équipe propre uniquement."""
    equipe = utilisateur["equipe"]
    membres_equipe = [e for e in employes if e["equipe"] == equipe]

    while True:
        print("\n── Menu Manager ──")
        print("1. Voir mon rapport individuel")
        print("2. Voir le rapport d'un membre de mon equipe")
        print("3. Voir le rapport de mon equipe")
        print("0. Se deconnecter")

        choix = input("\nVotre choix : ").strip()

        if choix == "0":
            print("Deconnexion.")
            break

        elif choix == "1":
            pdf = choisir_format()
            contenu = generer_rapport_individuel(utilisateur)
            nom = f"rapport_individuel_{utilisateur['id']}_{horodatage()}"
            afficher_et_sauvegarder(contenu, nom, format_pdf=pdf)

        elif choix == "2":
            print(f"\nMembres de l'equipe {equipe} :")
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
                pdf = choisir_format()
                contenu = generer_rapport_individuel(cible)
                nom = f"rapport_individuel_{cible['id']}_{horodatage()}"
                afficher_et_sauvegarder(contenu, nom, format_pdf=pdf)
            else:
                print("[ACCES REFUSE] Cet employe n'appartient pas a votre equipe.")

        elif choix == "3":
            pdf = choisir_format()
            contenu = generer_rapport_equipe(employes, equipe)
            nom = f"rapport_equipe_{equipe.lower()}_{horodatage()}"
            afficher_et_sauvegarder(contenu, nom, format_pdf=pdf)

        else:
            print("[INFO] Choix invalide.")


def menu_directeur(utilisateur: dict, employes: list):
    """Menu du directeur – accès complet."""
    equipes = sorted(set(e["equipe"] for e in employes))

    while True:
        print("\n── Menu Directeur ──")
        print("1. Voir mon rapport individuel")
        print("2. Voir le rapport individuel d'un employe")
        print("3. Voir le rapport d'une equipe")
        print("4. Voir le rapport global")
        print("0. Se deconnecter")

        choix = input("\nVotre choix : ").strip()

        if choix == "0":
            print("Deconnexion.")
            break

        elif choix == "1":
            pdf = choisir_format()
            contenu = generer_rapport_individuel(utilisateur)
            nom = f"rapport_individuel_{utilisateur['id']}_{horodatage()}"
            afficher_et_sauvegarder(contenu, nom, format_pdf=pdf)

        elif choix == "2":
            print("\nListe des employes :")
            for e in employes:
                print(f"  [{e['id']:>3}] {e['prenom']} {e['nom']:<15} "
                      f"| {e['equipe']:<15} | {e['role']}")
            saisie = input("Identifiant : ").strip()
            try:
                id_choisi = int(saisie)
            except ValueError:
                print("[ERREUR] Identifiant invalide.")
                continue

            cible = next((e for e in employes if e["id"] == id_choisi), None)
            if cible:
                pdf = choisir_format()
                contenu = generer_rapport_individuel(cible)
                nom = f"rapport_individuel_{cible['id']}_{horodatage()}"
                afficher_et_sauvegarder(contenu, nom, format_pdf=pdf)
            else:
                print("[ERREUR] Employe introuvable.")

        elif choix == "3":
            print("\nEquipes disponibles :")
            for i, eq in enumerate(equipes, 1):
                print(f"  {i}. {eq}")
            saisie = input("Numero de l'equipe : ").strip()
            try:
                idx = int(saisie) - 1
                if 0 <= idx < len(equipes):
                    equipe_choisie = equipes[idx]
                    pdf = choisir_format()
                    contenu = generer_rapport_equipe(employes, equipe_choisie)
                    nom = f"rapport_equipe_{equipe_choisie.lower()}_{horodatage()}"
                    afficher_et_sauvegarder(contenu, nom, format_pdf=pdf)
                else:
                    print("[ERREUR] Numero hors plage.")
            except ValueError:
                print("[ERREUR] Saisie invalide.")

        elif choix == "4":
            pdf = choisir_format()
            contenu = generer_rapport_global(employes)
            nom = f"rapport_global_{horodatage()}"
            afficher_et_sauvegarder(contenu, nom, format_pdf=pdf)

        else:
            print("[INFO] Choix invalide.")


def main():
    """Charge les données, authentifie et redirige selon le rôle."""
    employes = lire_employes(FICHIER_CSV)
    if not employes:
        print("[ERREUR] Impossible de charger les données. Arrêt.")
        return

    print(f"[INFO] {len(employes)} employe(s) charge(s).")

    if FPDF_DISPONIBLE:
        print("[INFO] Export PDF disponible (fpdf2 installe).")
    else:
        print("[INFO] Export PDF non disponible (pip install fpdf2 pour l'activer).")

    utilisateur = connexion(employes)
    if utilisateur is None:
        return

    role = utilisateur["role"]
    if role == "employe":
        menu_employe(utilisateur, employes)
    elif role == "manager":
        menu_manager(utilisateur, employes)
    elif role == "directeur":
        menu_directeur(utilisateur, employes)
    else:
        print(f"[ERREUR] Role inconnu : '{role}'.")


if __name__ == "__main__":
    main()
