# 🚀 Guia de Deploy - Canine AI

Este guia explica como fazer deploy da aplicação Canine AI no Streamlit Cloud e outras plataformas.

## 📋 Pré-requisitos

- ✅ Repositório no GitHub
- ✅ Arquivos do modelo em `weights/best.pt`
- ✅ Configuração otimizada para CPU

---

## ☁️ Deploy no Streamlit Cloud (Recomendado)

### Vantagens
- ✅ **100% Gratuito**
- ✅ Deploy automático do GitHub
- ✅ HTTPS incluído
- ✅ Fácil de configurar
- ✅ Atualizações automáticas

### Passo a Passo

#### 1. Preparar o Repositório

Certifique-se de que estes arquivos estão no repositório:

```
analise_canina_yolo/
├── app.py                    # ✅ Aplicação principal
├── config.yaml              # ✅ Configurações
├── requirements.txt         # ✅ Dependências Python (CPU-only)
├── packages.txt            # ✅ Dependências do sistema
├── .streamlit/
│   └── config.toml         # ✅ Tema e configurações
├── weights/
│   └── best.pt            # ✅ Modelo treinado
├── results/                # ✅ Resultados e gráficos
└── images/                 # ✅ Imagens de teste (opcional)
```

#### 2. Fazer Push para o GitHub

```bash
# Adicionar todos os arquivos
git add .

# Commit
git commit -m "Deploy: Canine AI para Streamlit Cloud"

# Push
git push origin main
```

⚠️ **IMPORTANTE:** O arquivo `weights/best.pt` pode ser grande. Se exceder 100MB:

```bash
# Usar Git LFS para arquivos grandes
git lfs install
git lfs track "*.pt"
git add .gitattributes
git add weights/best.pt
git commit -m "Add model weights with LFS"
git push
```

#### 3. Configurar no Streamlit Cloud

1. Acesse: [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em **"New app"**
4. Configure:
   - **Repository:** `sidnei-almeida/analise_canina_yolo`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **Python version:** `3.11` (ou 3.12)
5. Clique em **"Deploy!"**

#### 4. Aguardar Deploy

O Streamlit Cloud irá:
1. ⏳ Clonar o repositório
2. ⏳ Instalar dependências do sistema (`packages.txt`)
3. ⏳ Instalar dependências Python (`requirements.txt`) - PyTorch CPU
4. ⏳ Iniciar a aplicação
5. ✅ Aplicação online!

**Tempo estimado:** 5-10 minutos

#### 5. Acessar a Aplicação

Sua URL será algo como:
```
https://canine-ai-sidnei-almeida.streamlit.app
```

---

## 🔧 Otimizações para Streamlit Cloud

### Limites de Recursos
- **RAM:** ~1GB
- **CPU:** 1 core compartilhado
- **Storage:** Temporário (efêmero)
- **Timeout:** Apps dormem após inatividade

### Configurações Otimizadas

O `requirements.txt` já está otimizado com:
- ✅ PyTorch **CPU-only** (muito mais leve)
- ✅ OpenCV **headless** (sem GUI)
- ✅ Versões compatíveis com Python 3.13

O `config.yaml` está configurado com:
- ✅ `device: "cpu"` (sem GPU)
- ✅ `use_half_precision: false`
- ✅ `image_size: 640` (equilibrado)

### Cache Inteligente

O app já usa cache para:
- ✅ Modelo YOLO (carregado uma vez)
- ✅ Dados de treinamento
- ✅ Configurações

```python
@st.cache_resource
def load_model():
    # Modelo carregado apenas uma vez
    ...
```

---

## 🐙 GitHub LFS para Modelos Grandes

Se o arquivo `weights/best.pt` for maior que 100MB:

### Instalação do Git LFS

```bash
# Ubuntu/Debian
sudo apt-get install git-lfs

# Mac
brew install git-lfs

# Windows
# Baixe de: https://git-lfs.github.com/
```

### Configuração

```bash
# Inicializar LFS no repositório
git lfs install

# Rastrear arquivos .pt
git lfs track "*.pt"

# Adicionar .gitattributes
git add .gitattributes

# Adicionar o modelo
git add weights/best.pt

# Commit e push
git commit -m "Add model with LFS"
git push
```

### Verificar

```bash
# Ver arquivos rastreados pelo LFS
git lfs ls-files
```

---

## 🌐 Deploy em Outras Plataformas

### Hugging Face Spaces

1. Crie uma conta em [huggingface.co](https://huggingface.co)
2. Crie um novo Space:
   - **SDK:** Streamlit
   - **Hardware:** CPU (gratuito)
3. Clone o Space e adicione seus arquivos
4. Push para o repositório do Space

```bash
git clone https://huggingface.co/spaces/seu-usuario/canine-ai
cd canine-ai
# Copie todos os arquivos do projeto
git add .
git commit -m "Initial deploy"
git push
```

### Railway

1. Conecte seu GitHub em [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Selecione o repositório
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Deploy automático!

### Render

1. Crie conta em [render.com](https://render.com)
2. New → Web Service
3. Conecte repositório GitHub
4. Configure:
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Deploy!

---

## 🔒 Variáveis de Ambiente e Secrets

### Streamlit Cloud

Se precisar de API keys ou secrets:

1. No dashboard do Streamlit Cloud
2. Clique em **"Advanced settings"**
3. Adicione em **"Secrets"**:

```toml
# .streamlit/secrets.toml (não commitar!)
api_key = "sua-chave-aqui"
```

No código:
```python
import streamlit as st
api_key = st.secrets["api_key"]
```

---

## 📊 Monitoramento

### Streamlit Cloud

- **Logs:** Acesse via dashboard
- **Métricas:** RAM, CPU no painel
- **Analytics:** Visualizações na dashboard

### Health Check

Adicione ao final do `app.py`:

```python
# Health check endpoint
if st.query_params.get("health") == "check":
    st.write("OK")
    st.stop()
```

Acesse: `https://seu-app.streamlit.app/?health=check`

---

## 🐛 Troubleshooting

### Erro: "App is sleeping"
**Causa:** Inatividade
**Solução:** Apps gratuitos dormem. Use plano pago ou reacorde visitando

### Erro: "Out of memory"
**Causa:** RAM insuficiente (1GB)
**Solução:** 
- Reduza `image_size` no `config.yaml` para 416
- Use cache agressivamente
- Considere upgrade para plano pago

### Erro: "Model not found"
**Causa:** Arquivo `best.pt` não foi commitado
**Solução:**
```bash
# Se for grande, use Git LFS
git lfs track "*.pt"
git add weights/best.pt
git commit -m "Add model"
git push
```

### Erro: "Package installation failed"
**Causa:** Incompatibilidade de versões
**Solução:**
1. Verifique Python version: use 3.11 ou 3.12
2. Limpe cache: Rebuild no dashboard
3. Verifique `requirements.txt`

### App muito lento
**Soluções:**
1. Ajuste `image_size` para 416 ou 320
2. Reduza `max_detections`
3. Desabilite features pesadas
4. Use mais cache

---

## 📈 Melhorias de Performance

### 1. Lazy Loading
Carregue componentes apenas quando necessário:

```python
if selected == "🔮 Testar Modelo":
    model = load_model()  # Só carrega quando necessário
```

### 2. Compression
Comprima imagens antes de processar:

```python
if image.size[0] > 1920:
    image.thumbnail((1920, 1920))
```

### 3. Async Processing
Para múltiplas predições:

```python
import asyncio
# Processar em lote
```

---

## 🎉 Checklist Final

Antes do deploy:

- [ ] ✅ `requirements.txt` usa PyTorch CPU-only
- [ ] ✅ `config.yaml` com `device: "cpu"`
- [ ] ✅ `packages.txt` criado
- [ ] ✅ Modelo `best.pt` commitado (ou com LFS)
- [ ] ✅ Pasta `results/` com gráficos
- [ ] ✅ `.streamlit/config.toml` configurado
- [ ] ✅ Teste local antes: `streamlit run app.py`
- [ ] ✅ Git push para `main` branch
- [ ] ✅ Deploy no Streamlit Cloud
- [ ] ✅ Teste online
- [ ] ✅ Compartilhe a URL! 🎊

---

## 🔗 Links Úteis

- [Streamlit Cloud](https://share.streamlit.io)
- [Streamlit Docs](https://docs.streamlit.io)
- [Git LFS](https://git-lfs.github.com/)
- [Hugging Face Spaces](https://huggingface.co/spaces)
- [Railway](https://railway.app)
- [Render](https://render.com)

---

**🐕 Canine AI** - Pronto para Deploy na Nuvem!

