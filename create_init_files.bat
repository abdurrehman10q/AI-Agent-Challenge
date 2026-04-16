@echo off
echo Creating __init__.py files...

REM Create agent subfolders __init__.py
type nul > agents\feature_engineering\__init__.py
type nul > agents\detection\__init__.py
type nul > agents\risk_scoring\__init__.py
type nul > agents\decision\__init__.py
type nul > agents\coordinator\__init__.py
type nul > agents\learning\__init__.py

REM Create api subfolders __init__.py
type nul > api\routes\__init__.py
type nul > api\schemas\__init__.py

REM Create core __init__.py
type nul > core\__init__.py

REM Create models subfolders __init__.py
type nul > models\ml\__init__.py
type nul > models\saved\.gitkeep

REM Create orchestration __init__.py
type nul > orchestration\__init__.py

REM Create dashboard subfolders __init__.py
type nul > dashboard\pages\__init__.py
type nul > dashboard\components\__init__.py

REM Create tests subfolders __init__.py
type nul > tests\agents\__init__.py
type nul > tests\api\__init__.py
type nul > tests\models\__init__.py

REM Create data subfolders
type nul > data\raw\.gitkeep
type nul > data\processed\.gitkeep
type nul > data\demo\.gitkeep

echo All __init__.py files created successfully!
pause