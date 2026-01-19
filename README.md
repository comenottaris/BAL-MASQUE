# Bal Masqué

**Logiciel libre de floutage de visages**

![Version](https://img.shields.io/badge/version-1.0-ff2d55)
![Licence](https://img.shields.io/badge/licence-GPL--3.0-00e5a0)
![Python](https://img.shields.io/badge/python-3.8+-5cb8ff)

---

## Description

**Bal Masqué** est un outil de protection de la vie privée permettant de flouter automatiquement ou manuellement les visages sur vos photos.

### Fonctionnalités

- **Détection automatique** des visages (OpenCV Haar Cascades)
- **Mode manuel** pour sélectionner des zones personnalisées
- **3 effets** : Pixelisation, Flou gaussien, Masque noir
- **Intensité réglable** (15-99)
- **Export** PNG/JPEG haute qualité
- **Disclaimer juridique** sur le respect de la vie privée

---

## Installation

### Option 1 : Télécharger l'exécutable (recommandé)

**Aucune installation requise !**

1. Allez dans **[Releases](../../releases)**
2. Téléchargez `BalMasque_v1.0.zip` (Windows/Linux/Mac selon votre OS)
3. Décompressez
4. Double-cliquez sur `BalMasque.exe` (Windows) ou `./BalMasque` (Linux/Mac)

### Option 2 : Depuis le code source

```bash
# Cloner le repo
git clone https://github.com/VOTRE_USERNAME/bal-masque.git
cd bal-masque

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python bal_masque.py
```

### Option 3 : Builder vous-même

```bash
# Windows
build.bat

# Linux/Mac
chmod +x build.sh
./build.sh
```

L'exécutable sera dans `release/BalMasque/`

---

## Utilisation

### Interface
## 📸 Captures d'écran

![Interface d'accueil](screenshots/Accueil.png)
![Interface de retouche](screenshots/retouches.png)

### Étapes

1. Ouvrir une image → Bouton "Ouvrir image"
2. Choisir le mode :
   - **Auto-détection** : détecte automatiquement les visages
   - **Manuel** : cliquez-glissez pour dessiner des zones
3. Paramétrer :
   - Effet (Pixels/Flou/Noir)
   - Intensité (15 = léger, 99 = intense)
4. Masquer → Bouton "Masquer"
5. Enregistrer → Bouton "Enregistrer"

### Mode manuel

- **Dessiner** : Clic gauche + glisser
- **Annuler dernière zone** : Bouton "Annuler"
- **Tout effacer** : Bouton "Effacer zones"

---

## Aspects juridiques

### Droit à l'image

En France (et dans de nombreux pays) :

- ✅ Toute personne a un droit sur son image
- ✅ La publication d'une photo nécessite le consentement des personnes reconnaissables
- ✅ Les personnes peuvent demander le retrait ou le floutage de leur image

**Exceptions** (selon contexte) :

- Événements publics avec foule (manifestations, concerts...)
- Personnalités publiques dans l'exercice de leurs fonctions
- Images accessoires (personne non reconnaissable/non centrale)

### Ressources

- CNIL - Droit à l'image
- La Quadrature du Net - Défense des libertés numériques
- Technopolice - Lutte contre la surveillance
- Guide BOUM - Pratiques numériques émancipatrices

### Bon usage

Ce logiciel est conçu pour :

- ✅ Protéger la vie privée des personnes photographiées
- ✅ Respecter le droit à l'image
- ✅ Permettre la diffusion de photos d'événements collectifs

Il **ne doit PAS** être utilisé pour :

- ❌ Cacher des informations relevant de l'intérêt public
- ❌ Entraver le travail journalistique légitime
- ❌ Dissimuler des actes répréhensibles

---

## Technologies

- Python 3.8+
- OpenCV - Détection de visages
- Pillow - Manipulation d'images
- Tkinter - Interface graphique
- NumPy - Traitement matriciel

---

## Arborescence du projet

```
bal-masque/
├── bal_masque.py          # Code principal
├── logo.png               # Logo de l'application
├── requirements.txt       # Dépendances Python
├── build.bat              # Script de build Windows
├── build.sh               # Script de build Linux/Mac
├── README.md              # Ce fichier
└── LICENSE                # Licence GPL-3.0
```

---

## Contribuer

Les contributions sont bienvenues !

1. Fork le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez (`git commit -m 'Ajout fonctionnalité X'`)
4. Push (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

### Idées de contributions

- Support vidéo (floutage frame par frame)
- Détection de plaques d'immatriculation
- Mode batch (traiter plusieurs images)
- Reconnaissance faciale pour exclure certaines personnes
- Export en GIF animé
- Interface en ligne de commande (CLI)

---

## Licence

**GPL-3.0** - Logiciel libre et open source

Vous êtes libre de :

- ✅ Utiliser ce logiciel à toute fin
- ✅ Étudier et modifier le code
- ✅ Redistribuer des copies
- ✅ Redistribuer des versions modifiées

**Conditions** :

- Le code source doit rester disponible
- Les modifications doivent être documentées
- La même licence doit être appliquée aux dérivés

Voir **LICENSE** pour plus de détails.

---

## Crédits

### Développement

- Inspiration : [BlurryFaces](https://github.com/asmaamirkhan/BlurryFaces) par @asmaamirkhan

### Typographie du logo

- Fonte Ouvrières - typotheque.genderfluid.space


## Contact & Support

- Issues : Signaler un bug
- Discussions : Forum
- Email : siratton@pm.me

---

## Remerciements

Merci aux organisations qui défendent nos libertés numériques :

- La Quadrature du Net
- Technopolice
- BOUM
- Exodus Privacy
- Framasoft
- ...
---

Protégez la vie privée. Respectez le droit à l'image. Utilisez des logiciels libres.
