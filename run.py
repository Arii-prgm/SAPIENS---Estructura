#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import shutil

def log(message):
    print(f"[LOG] {message}")

def error_exit(message):
    print(f"\n[ERROR] {message}", file=sys.stderr)
    sys.exit(1)

def get_venv_paths():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(base_dir, ".venv")
    
    if platform.system() == "Windows":
        python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        python_exe = os.path.join(venv_dir, "bin", "python")
        pip_exe = os.path.join(venv_dir, "bin", "pip")
        
    return venv_dir, python_exe, pip_exe

def ensure_venv(venv_dir, python_exe):
    if not os.path.exists(python_exe):
        log("No se encontró el entorno virtual (.venv). Creando uno nuevo...")
        try:
            # Create venv
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
            log("Entorno virtual creado exitosamente.")
        except subprocess.CalledProcessError as e:
            error_exit(f"Error al crear el entorno virtual: {e}")
    else:
        log("Entorno virtual (.venv) detectado.")

def configure_system_site_packages(venv_dir):
    # Enable include-system-site-packages = true in pyvenv.cfg
    # This is essential on Linux so the venv can access system GUI bindings like PyGObject (gi)
    cfg_path = os.path.join(venv_dir, "pyvenv.cfg")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            modified = False
            for i, line in enumerate(lines):
                if line.strip().startswith("include-system-site-packages"):
                    parts = line.split("=")
                    if len(parts) == 2 and parts[1].strip().lower() != "true":
                        lines[i] = "include-system-site-packages = true\n"
                        modified = True
                        break
            else:
                # If the setting was not found, append it
                lines.append("include-system-site-packages = true\n")
                modified = True
                
            if modified:
                with open(cfg_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)
                log("Configuración 'include-system-site-packages = true' habilitada en pyvenv.cfg.")
        except Exception as e:
            log(f"Advertencia: No se pudo modificar pyvenv.cfg: {e}")

def install_dependencies(pip_exe, python_exe):
    log("Instalando/Actualizando dependencias desde requirements.txt...")
    req_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    
    if os.path.exists(req_file):
        try:
            subprocess.run([pip_exe, "install", "-r", req_file], check=True)
            log("Dependencias principales instaladas con éxito.")
        except subprocess.CalledProcessError as e:
            error_exit(f"Error al instalar las dependencias básicas: {e}")
    else:
        # Fallback to installing pywebview directly if requirements.txt is missing
        try:
            subprocess.run([pip_exe, "install", "pywebview"], check=True)
            log("pywebview instalado directamente con éxito.")
        except subprocess.CalledProcessError as e:
            error_exit(f"Error al instalar pywebview: {e}")

    # Platform specific checks
    if platform.system() == "Linux":
        # Check if GUI library is available inside the venv
        try:
            subprocess.run([python_exe, "-c", "import gi"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            log("GUI de Linux (PyGObject/gi) detectada y disponible.")
        except subprocess.CalledProcessError:
            # gi not available, check for PyQt5 or PyQt6
            try:
                subprocess.run([python_exe, "-c", "import PyQt6"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                log("GUI de Linux (PyQt6) detectada y disponible.")
            except subprocess.CalledProcessError:
                try:
                    subprocess.run([python_exe, "-c", "import PyQt5"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    log("GUI de Linux (PyQt5) detectada y disponible.")
                except subprocess.CalledProcessError:
                    log("No se detectó PyGObject (gi) ni PyQt en el entorno virtual.")
                    log("Intentando instalar PyQt6 y PyQt6-WebEngine como solución alternativa en el entorno virtual...")
                    try:
                        subprocess.run([pip_exe, "install", "PyQt6", "PyQt6-WebEngine"], check=True)
                        log("PyQt6 instalado exitosamente como fallback de GUI.")
                    except subprocess.CalledProcessError:
                        print("\n" + "="*80)
                        print("ADVERTENCIA IMPORTANTE PARA LINUX:")
                        print("pywebview necesita una biblioteca de interfaz gráfica (GUI) compatible con WebKit.")
                        print("Por favor, instala los paquetes del sistema correspondientes:")
                        print("\nEn Debian/Ubuntu/Mint:")
                        print("  sudo apt update")
                        print("  sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0")
                        print("\nEn Arch Linux / Manjaro:")
                        print("  sudo pacman -S python-gobject webkit2gtk")
                        print("\nEn Fedora/RHEL:")
                        print("  sudo dnf install python3-gobject webkit2gtk4.0")
                        print("="*80 + "\n")

def run_app(python_exe):
    main_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
    if not os.path.exists(main_py):
        error_exit(f"No se encontró el archivo principal '{main_py}'")
        
    log("Iniciando la aplicación...")
    try:
        # Run main.py using the virtual environment's python interpreter
        # Pass any command line arguments along
        cmd = [python_exe, main_py] + sys.argv[1:]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        error_exit(f"La aplicación terminó con código de error: {e.returncode}")
    except KeyboardInterrupt:
        log("Aplicación detenida por el usuario.")

def main():
    venv_dir, python_exe, pip_exe = get_venv_paths()
    
    ensure_venv(venv_dir, python_exe)
    configure_system_site_packages(venv_dir)
    install_dependencies(pip_exe, python_exe)
    run_app(python_exe)

if __name__ == "__main__":
    main()
