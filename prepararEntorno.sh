#!/bin/bash

# Salir inmediatamente si un comando falla
set -e

echo "--- Configurando entorno ---"

# Asegura dependencias
sudo apt update && sudo apt install -y python3-venv python3-pip

# Crea el entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
fi

# Instalar dependencias usando el binario directo del venv
echo "Instalando dependencias desde pyproject.toml..."
./.venv/bin/python3 -m pip install --upgrade pip
./.venv/bin/python3 -m pip install .

echo "------------------------------------------------"
echo "¡Listo! Para empezar a trabajar, ejecuta:"
echo "source .venv/bin/activate"
echo "------------------------------------------------"
