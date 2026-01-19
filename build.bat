@echo off
chcp 65001 >nul
mode con cols=80 lines=35
title 🎭 Build Bal Masqué

echo.
echo ════════════════════════════════════════════════════════════════════════
echo   🎭 BAL MASQUÉ - BUILD
echo ════════════════════════════════════════════════════════════════════════
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

REM Nettoyage des anciens builds
echo [2/4] Nettoyage...
if exist "dist" rd /s /q dist
if exist "build" rd /s /q build
if exist "release" rd /s /q release
if exist "*.spec" del /q *.spec

echo ✓ Nettoyage effectué
echo.

REM Build avec PyInstaller
echo [3/4] Compilation de l'application...
echo    Cela peut prendre quelques minutes...
echo.

python -m PyInstaller ^
    --name="BalMasque" ^
    --onefile ^
    --windowed ^
    --add-data "logo.png;." ^
    --hidden-import=cv2 ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ImageTk ^
    --hidden-import=PIL.ImageFilter ^
    --hidden-import=PIL.ImageDraw ^
    --hidden-import=numpy ^
    --noconfirm ^
    --clean ^
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

REM Création du package final
echo [4/4] Création du package final...

mkdir release
mkdir release\BalMasque

copy /y dist\BalMasque.exe release\BalMasque\BalMasque.exe >nul

if exist "logo.png" (
    copy /y logo.png release\BalMasque\logo.png >nul
)

REM Création du README
(
echo # 🎭 Bal Masqué
echo.
echo ## Utilisation
echo.
echo 1. Double-cliquez sur `BalMasque.exe`
echo 2. Acceptez le disclaimer
echo 3. Chargez une image
echo 4. Choisissez le mode :
echo    - **Auto** : détection automatique des visages
echo    - **Manuel** : dessinez les zones à flouter
echo 5. Ajustez l'effet et l'intensité
echo 6. Sauvegardez
echo.
echo ## Raccourcis
echo.
echo - `Ctrl+O` : Ouvrir une image
echo - `Ctrl+S` : Sauvegarder
echo - `Ctrl+Z` : Annuler ^(mode manuel^)
echo - `Ctrl+D` : Détecter les visages
echo - `Échap` : Quitter
echo.
echo ## Ressources
echo.
echo - La Quadrature du Net : https://www.laquadrature.net
echo - Technopolice : https://technopolice.fr
echo.
echo ---
echo Logiciel libre sous licence GPL-3.0
) > release\BalMasque\README.md

REM Nettoyage des fichiers temporaires
rd /s /q build
rd /s /q dist
del /q *.spec 2>nul

echo ✓ Package créé
echo.

echo ════════════════════════════════════════════════════════════════════════
echo   ✅ BUILD TERMINÉ !
echo ════════════════════════════════════════════════════════════════════════
echo.
echo   📁 Dossier : release\BalMasque\
echo.
echo   Contenu :
echo     - BalMasque.exe    ^(application^)
echo     - logo.png         ^(logo^)
echo     - README.md        ^(documentation^)
echo.
echo   👉 Pour distribuer : compressez le dossier release\BalMasque en ZIP
echo.
echo ════════════════════════════════════════════════════════════════════════
echo.

pause
