@echo off
echo Creando entorno virtual...
python -m venv venv

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Instalando libreria omninative-ui y dependencias...
pip install -e .

echo.
echo Entorno virtual creado, activado y dependencias instaladas con exito.
echo Para mantener el entorno activo, ejecuta este script desde una linea de comandos o ejecuta: venv\Scripts\activate
pause

