bash cython_windows.sh
pyinstaller --clean --noconfirm --debug --log-level=WARN --name="connectfour_windows" --icon="resources/images/icon.ico" --add-data="resources;resources" --add-data=".;." --add-data="screens;screens" run.py
