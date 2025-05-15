"""
Build script for packaging the application with cx_Freeze.
- Specifies required packages and files to include.
- Configures the executable for Windows, including the application icon.
"""

from cx_Freeze import setup, Executable

build_options = {
    "packages": [
        "os", "sys", "json", "requests", "subprocess", "PyQt6", "psycopg2", "logging"
    ],
    "excludes": [],
    "include_files": [
        "UurWaresLogo.png",
        "UurWaresLogo.ico",
        "venv\Lib\site-packages\psycopg2_binary.libs\libcrypto-3-x64-e57e1a41cc5d7f9b741c935f04fe4f2f.dll",
        "venv\Lib\site-packages\psycopg2_binary.libs\libpq-29b01d8382d5824098bc0b4861813b70.dll",
        "venv\Lib\site-packages\psycopg2_binary.libs\libssl-3-x64-6b7807fd98efdd91c677351cd0a9f2d8.dll",
    ],
}

executables = [
    Executable(
        script="loginpage.py",
        base="Win32GUI",
        target_name="uurwaresv1.exe",
        icon="UurWaresLogo.ico"
    )
]

setup(
    name="UurWares",
    version="1.0",
    description="UurWares Client",
    author="Ugurkan Yilmaz",
    options={"build_exe": build_options},
    executables=executables
)
