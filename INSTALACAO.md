# 🔧 Guia de Instalação - Canine AI

## Compatibilidade de Versões Python

### ✅ Versões Recomendadas
- **Python 3.11.x** (Recomendado)
- **Python 3.12.x** (Recomendado)
- **Python 3.13.x** (Suportado com pacotes atualizados)

### ⚠️ Versões Não Recomendadas
- Python 3.8 e 3.9 (descontinuadas)
- Python 3.10 (pode funcionar, mas não testada)

---

## Instalação Padrão (Python 3.11+)

### 1. Criar Ambiente Virtual

```bash
# Navegue até o diretório do projeto
cd analise_canina_yolo

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 2. Instalar Dependências

```bash
# Atualize pip primeiro
pip install --upgrade pip

# Instale os pacotes
pip install -r requirements.txt
```

### 3. Verificar Instalação

```bash
# Teste se o Streamlit foi instalado corretamente
streamlit --version

# Teste se o YOLO foi instalado
python -c "from ultralytics import YOLO; print('YOLO OK')"
```

### 4. Executar a Aplicação

```bash
streamlit run app.py
```

---

## 🐛 Solução de Problemas

### Problema: Erro ao compilar pandas no Python 3.13

**Sintoma:**
```
error: too few arguments to function '_PyLong_AsByteArray'
```

**Solução:**
O `requirements.txt` já foi atualizado com versões compatíveis. Se ainda ocorrer erro:

1. Limpe o cache do pip:
```bash
pip cache purge
```

2. Atualize o pip e setuptools:
```bash
pip install --upgrade pip setuptools wheel
```

3. Reinstale os pacotes:
```bash
pip install -r requirements.txt --no-cache-dir
```

### Problema: PyTorch muito pesado ou sem GPU

**Para instalar apenas CPU (mais leve):**
```bash
# Primeiro, instale tudo exceto torch e torchvision
pip install streamlit streamlit-option-menu pandas plotly Pillow PyYAML ultralytics opencv-python numpy

# Depois instale PyTorch CPU-only (muito mais leve)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Problema: Erro com NumPy 2.0

**Sintoma:**
```
AttributeError: module 'numpy' has no attribute 'X'
```

**Solução:**
Algumas bibliotecas podem não ser compatíveis com NumPy 2.0. Use NumPy 1.26:
```bash
pip install "numpy<2.0" --force-reinstall
```

Depois atualize o requirements.txt para:
```
numpy>=1.26.0,<2.0
```

### Problema: Ultralytics não encontra o modelo

**Sintoma:**
```
FileNotFoundError: weights/best.pt
```

**Solução:**
Certifique-se de que os pesos do modelo estão na pasta `weights/`:
```bash
ls weights/
# Deve mostrar: best.pt  last.pt
```

### Problema: Streamlit não inicia

**Sintoma:**
```
command not found: streamlit
```

**Solução:**
1. Certifique-se de que o ambiente virtual está ativado:
```bash
which python  # Deve apontar para venv/bin/python
```

2. Reinstale streamlit:
```bash
pip install --force-reinstall streamlit
```

### Problema: Porta 8501 já em uso

**Sintoma:**
```
Port 8501 is in use
```

**Solução:**
Use outra porta:
```bash
streamlit run app.py --server.port 8502
```

---

## 🚀 Instalação com Script Automatizado

### Linux/Mac

O script `run.sh` já faz tudo automaticamente:

```bash
chmod +x run.sh
./run.sh
```

O script irá:
1. Criar ambiente virtual (se não existir)
2. Ativar ambiente virtual
3. Instalar dependências (se necessário)
4. Iniciar a aplicação

### Windows

Crie um arquivo `run.bat`:

```batch
@echo off
echo 🐕 Iniciando Canine AI...

if not exist venv (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate

if not exist venv\.deps_installed (
    echo 📥 Instalando dependências...
    pip install -r requirements.txt
    echo. > venv\.deps_installed
)

echo 🚀 Iniciando aplicação...
streamlit run app.py

pause
```

Depois execute:
```cmd
run.bat
```

---

## 📦 Instalação em Produção

### Com Docker (Recomendado para Produção)

Crie um `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expor porta
EXPOSE 8501

# Comando de inicialização
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Construir e executar:
```bash
docker build -t canine-ai .
docker run -p 8501:8501 canine-ai
```

### Com Docker Compose

Crie um `docker-compose.yml`:

```yaml
version: '3.8'

services:
  canine-ai:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./images:/app/images
      - ./weights:/app/weights
      - ./results:/app/results
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_PORT=8501
```

Executar:
```bash
docker-compose up
```

---

## 🌐 Deploy em Nuvem

### Streamlit Cloud (Grátis)

1. Faça push do código para GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu repositório
4. Configure:
   - Python version: 3.11
   - Main file: `app.py`
5. Deploy!

### Heroku

```bash
# Criar Procfile
echo "web: streamlit run app.py --server.port \$PORT" > Procfile

# Criar runtime.txt
echo "python-3.11.7" > runtime.txt

# Deploy
heroku create canine-ai
git push heroku main
```

### Railway

1. Conecte seu repositório GitHub
2. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
3. Deploy automático!

---

## 🔍 Verificação Pós-Instalação

Execute este script Python para verificar tudo:

```python
# test_installation.py
import sys
print(f"✓ Python {sys.version}")

try:
    import streamlit
    print(f"✓ Streamlit {streamlit.__version__}")
except ImportError:
    print("✗ Streamlit não instalado")

try:
    import pandas
    print(f"✓ Pandas {pandas.__version__}")
except ImportError:
    print("✗ Pandas não instalado")

try:
    import plotly
    print(f"✓ Plotly {plotly.__version__}")
except ImportError:
    print("✗ Plotly não instalado")

try:
    from ultralytics import YOLO
    print("✓ Ultralytics instalado")
except ImportError:
    print("✗ Ultralytics não instalado")

try:
    import torch
    print(f"✓ PyTorch {torch.__version__}")
    print(f"  CUDA disponível: {torch.cuda.is_available()}")
except ImportError:
    print("✗ PyTorch não instalado")

print("\n✅ Verificação completa!")
```

Execute:
```bash
python test_installation.py
```

---

## 📞 Suporte

Se encontrar problemas:

1. **Verifique a versão do Python:**
   ```bash
   python --version
   ```

2. **Verifique os logs de erro completos**

3. **Tente a instalação limpa:**
   ```bash
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt --no-cache-dir
   ```

4. **Abra uma issue no GitHub:**
   - Inclua a versão do Python
   - Inclua o erro completo
   - Inclua seu sistema operacional

---

**🐕 Canine AI** - Sistema Inteligente de Reconhecimento de Raças Caninas

