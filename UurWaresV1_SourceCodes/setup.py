from cx_Freeze import setup, Executable

build_options = {
    "packages": ["mysql.connector", "requests", "os", "json", "subprocess", "PyQt6", "shutil", "zipfile"],
    "excludes": [],
    "include_files": [
        "UurWaresLogo.png",  # Include the logo
        "UurWaresLogo.ico",      # Include the application icon
    ],
}

executables = [
    Executable(
        script="updater.py",
        base="Win32GUI",
        target_name="uurwaresv1.exe",
        icon="UurWaresLogo.ico"  # Set the application icon
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
