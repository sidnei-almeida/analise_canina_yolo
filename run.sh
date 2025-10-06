#!/bin/bash

# Script para executar a aplicação Canine AI

echo "🐕 Iniciando Canine AI..."
echo ""

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências se necessário
if [ ! -f "venv/.deps_installed" ]; then
    echo "📥 Instalando dependências..."
    pip install -r requirements.txt
    touch venv/.deps_installed
fi

# Executar aplicação
echo "🚀 Iniciando aplicação Streamlit..."
echo ""
streamlit run app.py

# Desativar ambiente virtual ao sair
deactivate

