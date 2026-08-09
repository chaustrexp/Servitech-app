@echo off
echo ==============================================
echo  Limpiando base de datos y sembrando datos
echo ==============================================

REM Intenta activar el entorno virtual
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ADVERTENCIA] No se encontro el entorno virtual venv. Usando entorno global...
)

python manage.py flush --no-input
python seed_full.py

echo ==============================================
echo  Proceso Finalizado. Ya puedes probar el sistema.
echo ==============================================
pause
