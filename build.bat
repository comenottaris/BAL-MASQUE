@echo off
chcp 65001 >nul
mode con cols=80 lines=30
title 🎭 Build Bal Masqué

echo.
echo ═══════════════════════════════════════════════════════════════════════
echo   🎭 BAL MASQUÉ - BUILD
echo ═══════════════════════════════════════════════════════════════════════
echo.

REM Vérification Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé !
    echo    Téléchargez-le : https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python détecté
echo.

REM Installation des dépendances
echo [1/4] Installation des dépendances...
python -m pip install --upgrade pip --quiet
pip install pyinstaller pillow opencv-python numpy --quiet

if errorlevel 1 (
    echo ❌ Erreur lors de l'installation
    pause
    exit /b 1
)

echo ✓ Dépendances installées
echo.

REM Création du dossier build
if exist "dist" rd /s /q dist
if exist "build" rd /s /q build

REM Build avec PyInstaller
echo [2/4] Compilation de l'application...
echo.

python -m PyInstaller ^
    --name="BalMasque" ^
    --onefile ^
    --windowed ^
    --icon=NONE ^
    --add-data "logo.png;." ^
    --hidden-import=cv2 ^
    --hidden-import=PIL ^
    --hidden-import=numpy ^
    --collect-data cv2 ^
    --noconfirm ^
    bal_masque.py

if errorlevel 1 (
    echo.
    echo ❌ Erreur lors de la compilation
    pause
    exit /b 1
)

echo.
echo ✓ Compilation réussie
echo.

REM Nettoyage
echo [3/4] Nettoyage...
rd /s /q build
del /q BalMasque.spec

REM Copie du logo
if exist "logo.png" (
    copy /y logo.png dist\logo.png >nul
)

echo ✓ Fichiers nettoyés
echo.

REM Création du package final
echo [4/4] Création du package final...

if not exist "release" mkdir release
if exist "release\BalMasque" rd /s /q "release\BalMasque"
mkdir "release\BalMasque"

move dist\BalMasque.exe release\BalMasque\ >nul
copy logo.png release\BalMasque\ >nul

REM Création du README
(
echo # 🎭 Bal Masqué
echo.
echo ## Lancement
echo.
echo Double-cliquez sur `BalMasque.exe`
echo.
echo ## Utilisation
echo.
echo 1. **Ouvrir une image** : Cliquez sur "Ouvrir image"
echo 2. **Choisir le mode** :
echo    - Auto-détection : détection automatique des visages
echo    - Manuel : dessinez les zones à masquer
echo 3. **Sélectionner l'effet** : Pixels / Flou / Noir
echo 4. **Ajuster l'intensité** : Curseur 15-99
echo 5. **Masquer** : Cliquez sur "✦ Masquer"
echo 6. **Enregistrer** : Sauvegardez le résultat
echo.
echo ## Mode manuel
echo.
echo - Cliquez et glissez pour dessiner une zone
echo - "Annuler" : supprime la dernière zone
echo - "Effacer" : supprime toutes les zones
echo.
echo ## Ressources
echo.
echo - La Quadrature du Net : https://www.laquadrature.net
echo - Technopolice : https://technopolice.fr
echo - Guide BOUM : https://guide.boum.org
echo.
echo ---
echo.
echo Fonte Ouvrières — typotheque.genderfluid.space
) > release\BalMasque\README.md

echo ✓ Package créé
echo.

echo ═══════════════════════════════════════════════════════════════════════
echo   ✓ BUILD TERMINÉ !
echo ═══════════════════════════════════════════════════════════════════════
echo.
echo   📁 Dossier : release\BalMasque\
echo   📦 Taille  : 
dir /s release\BalMasque\BalMasque.exe | find "BalMasque.exe"
echo.
echo   Contenu :
echo     - BalMasque.exe  (application)
echo     - logo.png       (logo)
echo     - README.md      (documentation)
echo.

REM Option pour créer un ZIP
echo Voulez-vous créer un fichier ZIP ? (O/N)
choice /c ON /n
if errorlevel 2 goto :skip_zip
if errorlevel 1 goto :create_zip

:create_zip
echo.
echo Création du ZIP...
powershell -command "Compress-Archive -Path 'release\BalMasque' -DestinationPath 'release\BalMasque_v1.0.zip' -Force"
echo ✓ ZIP créé : release\BalMasque_v1.0.zip
echo.

:skip_zip
echo.
pause
