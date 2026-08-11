#!/bin/bash
echo "=============================================="
echo " Limpiando base de datos y sembrando datos"
echo "=============================================="

# Intenta activar el entorno virtual
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "[ADVERTENCIA] No se encontro el entorno virtual venv. Usando entorno global..."
fi

python manage.py flush --no-input
python seed_full.py

echo "=============================================="
echo " Proceso Finalizado. Ya puedes probar el sistema."
echo "=============================================="
