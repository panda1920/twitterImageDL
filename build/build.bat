@ECHO OFF
pipenv run pyi-makespec -p ./src --name twitter_image_dl --specpath=./build/spec dl.py
pipenv run pyi-makespec -p ./src -w --name gui --specpath=./build/spec gui.py
python build/spec-creator.py
pipenv run pyinstaller --workpath=./build/temp -y --clean ./build/spec/build.spec
