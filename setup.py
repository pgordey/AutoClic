from setuptools import setup

APP = ['main.py']  # замените 'your_script.py' на имя вашего основного скрипта
DATA_FILES = []
OPTIONS = {
    'packages': ['rubicon.objc'],
    'includes': ['pyautogui', 'pyscreeze', 'pygetwindow', 'pyperclip', 'mouseinfo'],
    'excludes': ['tkinter'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app', 'rubicon-objc'],
)
