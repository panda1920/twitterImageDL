@ECHO OFF

SET PROJECT_DIR=%~dp0..

pipenv run pyi-makespec -p %PROJECT_DIR%\src --name twitter_image_dl --specpath=%PROJECT_DIR%\build\spec dl.py
pipenv run pyi-makespec -p %PROJECT_DIR%\src -w --name gui --specpath=%PROJECT_DIR%\build\spec gui.py
python %PROJECT_DIR%\build\spec-creator.py
pipenv run pyinstaller --workpath=%PROJECT_DIR%\build\temp -y --clean %PROJECT_DIR%\build\spec\build.spec
