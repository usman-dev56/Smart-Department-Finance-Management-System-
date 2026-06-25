# build.py
import os
import shutil
import subprocess

def clean_build():
    folders = ['build', 'dist']
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✅ Removed {folder}")
    
    for f in os.listdir('.'):
        if f.endswith('.spec'):
            os.remove(f)
            print(f"✅ Removed {f}")

def build_exe():
    print("=" * 50)
    print("Building SDFMS Executable")
    print("=" * 50)
    
    clean_build()
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=SDFMS',
        # '--icon=src/assets/images/logo.png',  # ← REMOVED/COMMENTED
        '--add-data=src;src',
        '--add-data=data;data',
        '--add-data=src/database/schema.sql;src/database',  # ← ADDED schema.sql
        '--hidden-import=customtkinter',
        '--hidden-import=PIL',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=reportlab',
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=matplotlib',
        '--hidden-import=qrcode',
        '--hidden-import=sqlite3',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.messagebox',
        'main.py'
    ]
    
    print("\n📦 Running PyInstaller...")
    print("⏳ This may take 3-5 minutes. Please wait...\n")
    
    try:
        subprocess.run(cmd, check=True)
        print("\n" + "=" * 50)
        print("✅ BUILD SUCCESSFUL!")
        print("📁 Executable: dist\\SDFMS.exe")
        print("=" * 50)
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 50)
        print("❌ BUILD FAILED!")
        print(f"Error: {e}")
        print("=" * 50)

if __name__ == "__main__":
    build_exe()