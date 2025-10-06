# 🚀 Guia de Deploy no Streamlit Cloud

Este guia explica como fazer o deploy do DogBreed Vision no Streamlit Cloud.

## 📋 Pré-requisitos

1. **Conta no GitHub**: Repositório público ou privado
2. **Conta no Streamlit Cloud**: Gratuita em [share.streamlit.io](https://share.streamlit.io)
3. **Git LFS configurado**: Para o arquivo de modelo `weights/best.pt`

## 🔧 Preparação do Repositório

### 1. Configurar Git LFS (Large File Storage)

O modelo YOLO (`weights/best.pt`) é um arquivo grande e precisa do Git LFS:

```bash
# Instalar Git LFS (se ainda não tiver)
# Ubuntu/Debian:
sudo apt-get install git-lfs

# macOS:
brew install git-lfs

# Windows: baixar de https://git-lfs.github.com/

# Inicializar Git LFS no repositório
git lfs install

# Rastrear arquivos .pt com Git LFS
git lfs track "*.pt"

# Adicionar .gitattributes
git add .gitattributes

# Commit
git commit -m "Configure Git LFS for model weights"
```

### 2. Verificar Estrutura de Arquivos

Certifique-se de que todos esses arquivos estão no repositório:

```
analise_canina_yolo/
├── app.py                    # ✅ Aplicação principal
├── requirements.txt          # ✅ Dependências
├── packages.txt             # ✅ Dependências do sistema
├── config.yaml              # ✅ Configurações do modelo
├── .streamlit/
│   └── config.toml          # ✅ Configuração do Streamlit
├── weights/
│   └── best.pt              # ✅ Modelo YOLO (via Git LFS)
├── images/                  # ✅ Imagens de teste
│   ├── image1.png
│   ├── image2.png
│   └── ...
├── results/                 # ✅ Resultados do treinamento
│   ├── results.csv
│   ├── confusion_matrix_normalized.png
│   ├── BoxPR_curve.png
│   └── ...
└── args/
    └── args.yaml            # ✅ Argumentos de treinamento
```

### 3. Adicionar Arquivos ao Git

```bash
# Adicionar todos os arquivos necessários
git add .
git add -f .streamlit/config.toml  # Forçar adição do config
git add -f weights/best.pt         # Será rastreado pelo Git LFS

# Commit
git commit -m "Prepare for Streamlit Cloud deployment"

# Push para GitHub
git push origin main
```

## 🌐 Deploy no Streamlit Cloud

### Passo 1: Acessar Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em **"New app"**

### Passo 2: Configurar o App

Preencha as informações:

- **Repository**: `sidnei-almeida/analise_canina_yolo`
- **Branch**: `main`
- **Main file path**: `app.py`
- **App URL**: Escolha um nome (ex: `dogbreed-vision`)

### Passo 3: Configurações Avançadas (opcional)

Clique em **"Advanced settings"** se precisar:

- **Python version**: 3.11
- **Secrets**: Não necessário para este projeto

### Passo 4: Deploy

1. Clique em **"Deploy!"**
2. Aguarde o build (pode levar 5-10 minutos na primeira vez)
3. O app estará disponível em: `https://dogbreed-vision.streamlit.app`

## 🔍 Verificação de Deploy

Após o deploy, verifique:

- ✅ Modelo carregado corretamente
- ✅ Imagens de teste disponíveis
- ✅ Gráficos de análise funcionando
- ✅ Upload de imagens funcionando
- ✅ Detecção funcionando

## ⚠️ Troubleshooting

### Erro: "Module not found"
**Solução**: Verifique se todos os pacotes estão em `requirements.txt`

### Erro: "Model file not found"
**Solução**: 
1. Confirme que Git LFS está configurado
2. Verifique se `weights/best.pt` foi commitado
3. Execute: `git lfs ls-files` para listar arquivos LFS

### Erro: "Out of memory"
**Solução**: 
- Streamlit Cloud tem limite de ~1GB RAM
- Use `device='cpu'` no config.yaml
- Desabilite `use_half_precision` se necessário

### Erro: "OpenCV error"
**Solução**: Verifique se `packages.txt` contém:
```
libgl1-mesa-glx
libglib2.0-0
```

### Build muito lento
**Solução**: 
- Normal na primeira vez (instalação de PyTorch)
- Builds subsequentes são em cache (~2-3 min)

## 📊 Monitoramento

No Streamlit Cloud Dashboard você pode:

- 📈 Ver logs em tempo real
- 🔄 Fazer redeploy manual
- ⚙️ Ajustar configurações
- 📊 Ver métricas de uso
- 🗑️ Deletar o app

## 🔄 Atualizações

Para atualizar o app após mudanças:

```bash
# Fazer alterações no código
git add .
git commit -m "Update: descrição das mudanças"
git push origin main
```

O Streamlit Cloud detecta automaticamente e faz redeploy!

## 🔗 Links Úteis

- **Documentação Streamlit Cloud**: https://docs.streamlit.io/streamlit-community-cloud
- **Git LFS Docs**: https://git-lfs.github.com/
- **Streamlit Community**: https://discuss.streamlit.io/

## 📝 Notas Importantes

1. **Git LFS é essencial** para o arquivo `weights/best.pt`
2. **CPU-only PyTorch** já está configurado em `requirements.txt`
3. **OpenCV headless** está configurado para evitar erros de display
4. **Todas as referências de arquivos** usam caminhos relativos seguros
5. **Tratamento de erros** implementado para arquivos ausentes

## ✅ Checklist Final

Antes do deploy, confirme:

- [ ] Git LFS configurado e `*.pt` rastreado
- [ ] Todos os arquivos commitados
- [ ] `requirements.txt` atualizado
- [ ] `packages.txt` presente
- [ ] `.streamlit/config.toml` commitado
- [ ] Modelo `weights/best.pt` no repositório
- [ ] Push para GitHub realizado
- [ ] Branch `main` atualizada

## 🎉 Pronto!

Seu app estará disponível em:
`https://[seu-app-url].streamlit.app`

Compartilhe o link no seu portfólio! 🚀

