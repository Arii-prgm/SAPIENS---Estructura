@echo off
title Sapiens - Sistema de Organización Académica
echo ====================================================================
echo   Iniciando Sapiens - Sistema de Organización Académica
echo ====================================================================
echo.

:: Verificar si python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no está instalado o no se encuentra en la variable de entorno PATH.
    echo.
    echo Por favor, instala Python desde la Microsoft Store o desde https://www.python.org/
    echo Asegúrate de marcar la casilla "Add Python to PATH" durante la instalación.
    echo.
    pause
    exit /b 1
)

:: Ejecutar el script de arranque principal
python run.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Hubo un problema al iniciar la aplicación.
    echo Revisa el mensaje de error de arriba para más detalles.
    echo.
    pause
)
