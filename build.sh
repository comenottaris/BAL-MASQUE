#!/bin/bash

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

clear

echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo "  🎭 BAL MASQUÉ - BUILD"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

# Vérification Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 n'est pas installé !${NC}"
    echo "   Installez-le :"
    echo "   - Ubuntu/Debian : sudo apt install python3 python3-pip python3-tk"
    echo "   - Mac : brew install python3 python-tk"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python3 détecté : $(python3 --version)"
echo ""

# Installation des dépendances
echo "[1/4] Installation des dépendances..."
python3 -m pip install --upgrade pip --quiet
pip3 install pyinstaller pillow opencv-python numpy --quiet

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de l'installation${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Dépendances installées"
echo ""

# Nettoyage des anciens builds
echo "[2/4] Nettoyage..."
rm -rf dist build release *.spec 2>/dev/null

echo -e "${GREEN}✓${NC} Nettoyage effectué"
echo ""

# Build avec PyInstaller
echo "[3/4] Compilation de l'application..."
echo "   Cela peut prendre quelques minutes..."
echo ""

python3 -m PyInstaller \
    --name="BalMasque" \
    --onefile \
    --windowed \
    --add-data "logo.png:." \
    --hidden-import=cv2 \
    --hidden-import=PIL \
    --hidden-import=PIL.Image \
    --hidden-import=PIL.ImageTk \
    --hidden-import=PIL.ImageFilter \
    --hidden-import=PIL.ImageDraw \
    --hidden-import=numpy \
    --noconfirm \
    --clean \
    bal_masque.py

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Erreur lors de la compilation${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓${NC} Compilation réussie"
echo ""

# Création du package final
echo "[4/4] Création du package final..."

mkdir -p release/BalMasque

cp dist/BalMasque release/BalMasque/BalMasque
chmod +x release/BalMasque/BalMasque

if [ -f "logo.png" ]; then
    cp logo.png release/BalMasque/logo.png
fi

# Création du README
cat > release/BalMasque/README.md << 'EOF'
# 🎭 Bal Masqué

## Utilisation

1. Lancez `./BalMasque`
2. Acceptez le disclaimer
3. Chargez une image
4. Choisissez le mode :
   - **Auto** : détection automatique des visages
   - **Manuel** : dessinez les zones à flouter
5. Ajustez l'effet et l'intensité
6. Sauvegardez

## Raccourcis

- `Ctrl+O` : Ouvrir une image
- `Ctrl+S` : Sauvegarder
- `Ctrl+Z` : Annuler (mode manuel)
- `Ctrl+D` : Détecter les visages
- `Échap` : Quitter

## Ressources

- La Quadrature du Net : https://www.laquadrature.net
- Technopolice : https://technopolice.fr

---
Logiciel libre sous licence GPL-3.0
EOF

# Nettoyage des fichiers temporaires
rm -rf build dist *.spec 2>/dev/null

echo -e "${GREEN}✓${NC} Package créé"
echo ""

# Calcul de la taille
SIZE=$(du -sh release/BalMasque/BalMasque | cut -f1)

echo "════════════════════════════════════════════════════════════════════════"
echo "  ✅ BUILD TERMINÉ !"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "  📁 Dossier : release/BalMasque/"
echo "  📦 Taille  : $SIZE"
echo ""
echo "  Contenu :"
echo "    - BalMasque       (application)"
echo "    - logo.png        (logo)"
echo "    - README.md       (documentation)"
echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo ""

# Option ZIP
read -p "Créer un fichier ZIP pour la distribution ? (o/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    echo ""
    echo "Création du ZIP..."
    cd release
    zip -r BalMasque_v1.0.zip BalMasque/
    cd ..
    echo ""
    echo -e "${GREEN}✓${NC} ZIP créé : release/BalMasque_v1.0.zip"
    echo ""
fi

echo "Terminé ! 🎭"
