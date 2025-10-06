#!/usr/bin/env python3
"""
Script de verificação pré-deploy para Streamlit Cloud
Verifica se todos os arquivos necessários estão presentes e configurados corretamente
"""

import sys
from pathlib import Path
import yaml

def check_file_exists(file_path, description):
    """Verifica se um arquivo existe"""
    path = Path(file_path)
    if path.exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description} não encontrado: {file_path}")
        return False

def check_directory_exists(dir_path, description):
    """Verifica se um diretório existe"""
    path = Path(dir_path)
    if path.exists() and path.is_dir():
        files = list(path.iterdir())
        print(f"✅ {description}: {dir_path} ({len(files)} arquivos)")
        return True
    else:
        print(f"❌ {description} não encontrado: {dir_path}")
        return False

def check_requirements():
    """Verifica requirements.txt"""
    required_packages = [
        'streamlit',
        'ultralytics',
        'torch',
        'torchvision',
        'opencv-python-headless',
        'pillow',
        'pandas',
        'plotly',
        'pyyaml',
        'streamlit-option-menu',
        'streamlit-image-select'
    ]
    
    req_file = Path('requirements.txt')
    if not req_file.exists():
        print("❌ requirements.txt não encontrado")
        return False
    
    with open(req_file) as f:
        content = f.read().lower()
    
    missing = []
    for pkg in required_packages:
        if pkg.lower() not in content:
            missing.append(pkg)
    
    if missing:
        print(f"❌ Pacotes faltando em requirements.txt: {', '.join(missing)}")
        return False
    else:
        print(f"✅ requirements.txt com todos os pacotes necessários")
        return True

def check_git_lfs():
    """Verifica se Git LFS está configurado"""
    gitattributes = Path('.gitattributes')
    if gitattributes.exists():
        with open(gitattributes) as f:
            content = f.read()
        if '*.pt' in content and 'lfs' in content:
            print("✅ Git LFS configurado para arquivos .pt")
            return True
        else:
            print("❌ Git LFS não configurado corretamente em .gitattributes")
            return False
    else:
        print("⚠️  .gitattributes não encontrado (Git LFS pode não estar configurado)")
        return False

def check_config_yaml():
    """Verifica config.yaml"""
    config_file = Path('config.yaml')
    if not config_file.exists():
        print("⚠️  config.yaml não encontrado (usará defaults)")
        return True
    
    try:
        with open(config_file) as f:
            config = yaml.safe_load(f)
        
        # Verificar se device está configurado para CPU
        device = config.get('performance', {}).get('device', 'cpu')
        if device == 'cpu':
            print("✅ config.yaml configurado para CPU (correto para Streamlit Cloud)")
        else:
            print(f"⚠️  config.yaml com device='{device}' (recomendado: 'cpu' para Streamlit Cloud)")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao ler config.yaml: {e}")
        return False

def main():
    print("🔍 Verificação de Deploy para Streamlit Cloud\n")
    print("="*60)
    
    all_ok = True
    
    # Arquivos essenciais
    print("\n📁 Arquivos Essenciais:")
    all_ok &= check_file_exists('app.py', 'App principal')
    all_ok &= check_file_exists('requirements.txt', 'Dependências Python')
    all_ok &= check_file_exists('packages.txt', 'Dependências do sistema')
    all_ok &= check_file_exists('.streamlit/config.toml', 'Config Streamlit')
    
    # Modelo
    print("\n🤖 Modelo:")
    all_ok &= check_file_exists('weights/best.pt', 'Modelo YOLO')
    
    # Dados e resultados
    print("\n📊 Dados e Resultados:")
    check_directory_exists('images', 'Imagens de teste')
    check_directory_exists('results', 'Resultados de treinamento')
    check_file_exists('results/results.csv', 'CSV de resultados')
    check_file_exists('args/args.yaml', 'Args de treinamento')
    
    # Configurações
    print("\n⚙️  Configurações:")
    all_ok &= check_requirements()
    check_git_lfs()
    check_config_yaml()
    
    # Resumo
    print("\n" + "="*60)
    if all_ok:
        print("✅ Tudo pronto para deploy no Streamlit Cloud!")
        print("\nPróximos passos:")
        print("1. git add .")
        print("2. git commit -m 'Prepare for deployment'")
        print("3. git push origin main")
        print("4. Deploy em https://share.streamlit.io")
        return 0
    else:
        print("❌ Existem problemas que precisam ser corrigidos")
        print("\nVerifique os itens marcados com ❌ acima")
        return 1

if __name__ == "__main__":
    sys.exit(main())

