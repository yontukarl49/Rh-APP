 RH Pro — Système de Gestion des Ressources Humaines

Application en ligne de commande pour la gestion des ressources humaines d'une entreprise. Développée en Python avec une interface terminal esthétique grâce à la bibliothèque **Rich**.

---

# Fonctionnalités

- **Connexion par identifiant** avec redirection selon le rôle
- **Rapport individuel** : salaire brut, taux horaire réel, statut
- **Rapport d'équipe** : statistiques, membres, salaires
- **Rapport global** : vue complète de l'entreprise
- **Export** en `.txt` ou `.pdf` (via fpdf2)
- **Interface colorée** avec tableaux, panneaux et codes couleur

---

# Rôles disponibles

| Rôle | Accès |
|------|-------|
| `employe` | Son rapport individuel uniquement |
| `manager` | Son rapport + rapport de son équipe |
| `directeur` | Accès complet à tous les rapports |

---

#Structure du projet
analyse des données rh/
├── main.py              # Point d'entrée principal (sans PDF)
├── main_avec_pdf.py     # Version avec export PDF
├── rapport_pdf.py       # Module de génération PDF
├── employes.csv         # Base de données des employés
├── DejaVuSans.ttf       # Police pour les PDF
├── DejaVuSans-Bold.ttf  # Police bold pour les PDF
└── rapports/            # Dossier de sortie des rapports générés

---

# Installation

### Prérequis
- Python 3.10 ou supérieur
- pip

### 1. Cloner le dépôt

```bash
git clone https://github.com/yontukarl49/Rh-APP.git
cd Rh-APP
```

# 2. Installer les dépendances

```bash
pip install rich fpdf2
```

---

# Lancer l'application

```bash
python main_avec_pdf.py
```

L'application demande un **identifiant employé** pour se connecter.

### Identifiants de test

| ID | Nom | Rôle |
|----|-----|------|
| 1 | Alice Martin | Directeur |
| 2 | Jean Dupont | Manager |
| 3 | Sophie Bernard | Employé |

---

## 📄 Format des données

Le fichier `employes.csv` doit respecter ce format :

```csv
id,nom,prenom,role,equipe,heures_travaillees,taux_horaire,prime
1,Martin,Alice,directeur,Direction,160,45.0,500
```

### Règles de calcul

| Calcul | Formule |
|--------|---------|
| Salaire brut | `heures × taux_horaire + prime` |
| Salaire horaire réel | `salaire_brut / heures` |
| Statut | `< 150h` → Temps partiel · `150–155h` → Temps plein · `> 155h` → Heures supp. |

---

# Technologies utilisées

- [Python 3](https://www.python.org/)
- [Rich](https://github.com/Textualize/rich) — interface terminal
- [fpdf2](https://py-pdf.github.io/fpdf2/) — génération de PDF
- CSV — stockage des données

---

## Auteur

**Karl YONTU** 
