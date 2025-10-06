import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_image_select import image_select
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import yaml
from pathlib import Path
import os
from ultralytics import YOLO
import numpy as np
import time

# Configuração da página
st.set_page_config(
    page_title="DogBreed Vision - Sistema de Reconhecimento de Raças",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para design dark premium
st.markdown("""
    <style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Variáveis de cor - Tema Dark Premium */
    :root {
        --bg-primary: #0f1419;
        --bg-secondary: #1a1f2e;
        --bg-tertiary: #252d3d;
        --accent-primary: #00d9ff;
        --accent-secondary: #7c3aed;
        --accent-gradient: linear-gradient(135deg, #00d9ff 0%, #7c3aed 100%);
        --text-primary: #ffffff;
        --text-secondary: #a0aec0;
        --border-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Fundo principal dark */
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    /* Ajuste de padding global */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Sidebar escura elegante */
    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }
    
    /* Título principal com gradiente */
    .gradient-title {
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Poppins', sans-serif;
        font-size: 2.2em;
        font-weight: 700;
        text-align: center;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    /* Subtítulo */
    .subtitle {
        text-align: center;
        color: var(--text-secondary);
        font-size: 0.95em;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Cards de métricas dark */
    .metric-card {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.25rem 1rem;
        text-align: center;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--accent-gradient);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: var(--accent-primary);
        box-shadow: 0 8px 24px rgba(0, 217, 255, 0.15);
    }
    
    .metric-value {
        font-size: 2.2em;
        font-weight: 700;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.3rem 0;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.8em;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Info boxes dark */
    .info-box {
        background: var(--bg-tertiary);
        border-left: 3px solid var(--accent-primary);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: var(--text-primary);
    }
    
    .info-box h3, .info-box h4 {
        color: var(--accent-primary);
        margin-top: 0;
    }
    
    /* Divisores sutis */
    hr {
        border: none;
        height: 1px;
        background: var(--border-color);
        margin: 2rem 0;
    }
    
    /* Botões com gradiente */
    .stButton>button {
        background: var(--accent-gradient);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 217, 255, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 217, 255, 0.5);
    }
    
    /* Tabs customizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: var(--bg-secondary);
        padding: 0.4rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 6px;
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 0.9em;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent-gradient);
        color: white;
        font-weight: 600;
    }
    
    /* Dataframes dark */
    .dataframe {
        background-color: var(--bg-tertiary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    /* Expander dark */
    .streamlit-expanderHeader {
        background-color: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
    }
    
    /* Upload area dark */
    [data-testid="stFileUploader"] {
        background-color: var(--bg-tertiary);
        border: 2px dashed var(--accent-primary);
        border-radius: 12px;
        padding: 2rem;
    }
    
    /* Metrics nativas do Streamlit */
    [data-testid="stMetricValue"] {
        font-size: 2em;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Imagens com borda sutil */
    img {
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }
    
    /* Headers de seção */
    h3 {
        color: var(--text-primary);
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.3em;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid transparent;
        border-image: var(--accent-gradient);
        border-image-slice: 1;
        border-width: 0 0 2px 0;
    }
    
    /* Headers de subseção */
    h4 {
        color: var(--text-primary);
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        font-size: 1.05em;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }
    
    /* Inputs e selects */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select {
        background-color: var(--bg-tertiary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    /* Scrollbar dark */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--bg-tertiary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-primary);
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: var(--accent-gradient);
    }
    
    /* Spinners */
    .stSpinner > div {
        border-top-color: var(--accent-primary);
    }
    
    /* Image Select - Imagens compactas */
    div[data-testid="column"] img {
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    div[data-testid="column"] img:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0, 217, 255, 0.3);
    }
    
    /* Ajustar tamanho das imagens no image_select */
    .stImage {
        max-height: 180px;
        object-fit: cover;
    }
    </style>
""", unsafe_allow_html=True)

# Funções auxiliares
@st.cache_data
def load_config():
    """Carrega as configurações do arquivo config.yaml"""
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        st.error(f"Erro ao carregar configurações: {e}")
        # Retornar configurações padrão
        return {
            'detection': {
                'confidence_threshold': 0.25,
                'iou_threshold': 0.45,
                'max_detections': 10,
                'image_size': 640
            },
            'visualization': {
                'line_thickness': 2,
                'show_labels': True,
                'show_confidence': True,
                'confidence_format': 'percentage'
            },
            'performance': {
                'use_half_precision': False,
                'device': 'cpu'
            }
        }

@st.cache_data
def load_training_data():
    """Carrega os dados de treinamento do CSV"""
    try:
        df = pd.read_csv('results/results.csv')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados de treinamento: {e}")
        return None

@st.cache_data
def load_args():
    """Carrega os argumentos de treinamento do YAML"""
    try:
        with open('args/args.yaml', 'r') as f:
            args = yaml.safe_load(f)
        return args
    except Exception as e:
        st.error(f"Erro ao carregar configurações: {e}")
        return None

@st.cache_resource
def load_model():
    """Carrega o modelo YOLO"""
    try:
        config = load_config()
        device = config['performance'].get('device', 'cpu')
        model = YOLO('weights/best.pt')
        model.to(device)
        return model
    except Exception as e:
        st.error(f"Erro ao carregar modelo: {e}")
        return None

def get_test_images():
    """Obtém lista de imagens de teste"""
    images_dir = Path('images')
    if images_dir.exists():
        images = list(images_dir.glob('*.png')) + list(images_dir.glob('*.jpg')) + list(images_dir.glob('*.jpeg'))
        return [str(img) for img in images]
    return []

# Header principal
def show_header():
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0 0.5rem 0;'>
            <h1 class="gradient-title">DogBreed Vision</h1>
            <p class="subtitle">Sistema Profissional de Reconhecimento de Raças Caninas com YOLOv8</p>
        </div>
        <div style='margin: 1.5rem 0; height: 1px; background: var(--border-color);'></div>
    """, unsafe_allow_html=True)

# Sidebar com menu
with st.sidebar:
    # Logo/Header compacto
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0 1.5rem 0;'>
            <h2 style='margin: 0; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.4em; font-weight: 700; letter-spacing: -0.3px;'>
                DogBreed Vision
            </h2>
            <p style='margin: 0.25rem 0 0 0; font-size: 0.7em; color: var(--text-secondary); letter-spacing: 0.5px;'>
                YOLOV8 BREED RECOGNITION SYSTEM
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Menu de navegação (sem emojis duplicados)
    selected = option_menu(
        menu_title=None,
        options=["Início", "Análise", "Testar", "Sobre"],
        icons=["house-fill", "graph-up-arrow", "stars", "info-circle-fill"],
        menu_icon=None,
        default_index=0,
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"color": "#00d9ff", "font-size": "18px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "0 0 4px 0",
                "padding": "10px 14px",
                "border-radius": "8px",
                "color": "#a0aec0",
                "font-weight": "500",
                "--hover-color": "rgba(0, 217, 255, 0.1)",
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, rgba(0, 217, 255, 0.15) 0%, rgba(124, 58, 237, 0.15) 100%)",
                "color": "#00d9ff",
                "border-left": "3px solid #00d9ff",
                "font-weight": "600",
            },
        }
    )
    
    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # Status compacto com ícones
    st.markdown("""
        <div style='background: var(--bg-tertiary); border-radius: 8px; padding: 0.75rem; margin-bottom: 1rem; border: 1px solid var(--border-color);'>
            <div style='font-size: 0.85em; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-primary);'>
                Status do Sistema
            </div>
            <div style='font-size: 0.8em; line-height: 1.8; color: var(--text-secondary);'>
                <div>• Modelo carregado</div>
                <div>• 120 raças ativas</div>
                <div>• CPU otimizado</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Configurações ativas compactas
    config = load_config()
    st.markdown(f"""
        <div style='background: var(--bg-tertiary); border-radius: 8px; padding: 0.75rem; border: 1px solid var(--border-color);'>
            <div style='font-size: 0.85em; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-primary);'>
                Configurações
            </div>
            <div style='font-size: 0.75em; line-height: 1.6; color: var(--text-secondary);'>
                <div style='display: flex; justify-content: space-between;'>
                    <span>Confiança</span>
                    <span style='color: #00d9ff; font-weight: 600;'>{config['detection']['confidence_threshold']:.0%}</span>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <span>IoU</span>
                    <span style='color: #00d9ff; font-weight: 600;'>{config['detection']['iou_threshold']:.2f}</span>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <span>Tamanho</span>
                    <span style='color: #00d9ff; font-weight: 600;'>{config['detection']['image_size']}px</span>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <span>Device</span>
                    <span style='color: #00d9ff; font-weight: 600;'>{config['performance']['device']}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
    
    # Botão de recarregar config
    if st.button("⟳ Recarregar Config", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Página: Início
if selected == "Início":
    show_header()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Épocas Treinadas</div>
                <div class="metric-value">164</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-label">mAP50-95</div>
                <div class="metric-value">84.3%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Precisão</div>
                <div class="metric-value">80.6%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Raças</div>
                <div class="metric-value">120</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Sobre o Projeto")
        st.markdown("""
        <div class="info-box">
        <p style='font-size: 1.1em; line-height: 1.8;'>
        O <b>Canine AI</b> é um sistema de visão computacional de última geração que utiliza 
        a arquitetura YOLOv8 para reconhecimento preciso de raças caninas. Treinado com o 
        renomado dataset Stanford Dogs, nosso modelo é capaz de identificar <b>120 raças diferentes</b> 
        com alta precisão e velocidade.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔬 Tecnologias Utilizadas")
        tech_cols = st.columns(3)
        with tech_cols[0]:
            st.markdown("**🤖 YOLOv8n**\n\nModelo nano otimizado")
        with tech_cols[1]:
            st.markdown("**📚 Stanford Dogs**\n\nDataset premium")
        with tech_cols[2]:
            st.markdown("**⚡ PyTorch**\n\nFramework robusto")
    
    with col2:
        st.markdown("### 📸 Exemplos de Detecção")
        try:
            val_img = Image.open('results/val_batch0_pred.jpg')
            st.image(val_img, caption="Predições de Validação", use_container_width=True)
        except:
            st.info("Imagens de exemplo serão exibidas aqui")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📊 Amostras de Treinamento")
    
    train_cols = st.columns(3)
    for i, col in enumerate(train_cols):
        with col:
            try:
                img = Image.open(f'results/train_batch{i}.jpg')
                st.image(img, caption=f"Batch de Treinamento {i}", use_container_width=True)
            except:
                pass

# Página: Análise de Resultados
elif selected == "Análise":
    show_header()
    
    df = load_training_data()
    
    if df is not None:
        st.markdown("### 📈 Evolução do Treinamento")
        
        # Métricas finais
        final_metrics = df.iloc[-1]
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">mAP50-95 Final</div>
                    <div class="metric-value">{final_metrics['metrics/mAP50-95(B)']:.1%}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Precisão Final</div>
                    <div class="metric-value">{final_metrics['metrics/precision(B)']:.1%}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Recall Final</div>
                    <div class="metric-value">{final_metrics['metrics/recall(B)']:.1%}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">mAP50 Final</div>
                    <div class="metric-value">{final_metrics['metrics/mAP50(B)']:.1%}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráficos interativos
        tab1, tab2, tab3, tab4 = st.tabs(["Métricas Principais", "Losses", "Precisão vs Recall", "mAP Evolution"])
        
        with tab1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['epoch'], y=df['metrics/precision(B)'], 
                name='Precisão', 
                line=dict(color='#00d9ff', width=3),
                mode='lines'
            ))
            fig.add_trace(go.Scatter(
                x=df['epoch'], y=df['metrics/recall(B)'], 
                name='Recall', 
                line=dict(color='#7c3aed', width=3),
                mode='lines'
            ))
            fig.add_trace(go.Scatter(
                x=df['epoch'], y=df['metrics/mAP50(B)'], 
                name='mAP50', 
                line=dict(color='#06b6d4', width=3),
                mode='lines'
            ))
            fig.add_trace(go.Scatter(
                x=df['epoch'], y=df['metrics/mAP50-95(B)'], 
                name='mAP50-95', 
                line=dict(color='#8b5cf6', width=3),
                mode='lines'
            ))
            
            fig.update_layout(
                title="Evolução das Métricas de Performance",
                xaxis_title="Época",
                yaxis_title="Valor da Métrica",
                hovermode='x unified',
                template='plotly_dark',
                height=500,
                paper_bgcolor='#1a1f2e',
                plot_bgcolor='#252d3d',
                font=dict(family="Poppins", size=12, color='#ffffff'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['epoch'], y=df['train/box_loss'], 
                name='Box Loss (Train)', 
                line=dict(color='#00d9ff', width=2.5),
                mode='lines'
            ))
            fig.add_trace(go.Scatter(
                x=df['epoch'], y=df['train/cls_loss'], 
                name='Class Loss (Train)', 
                line=dict(color='#7c3aed', width=2.5),
                mode='lines'
            ))
            fig.add_trace(go.Scatter(
                x=df['epoch'], y=df['val/box_loss'], 
                name='Box Loss (Val)', 
                line=dict(color='#06b6d4', width=2.5, dash='dash'),
                mode='lines'
            ))
            fig.add_trace(go.Scatter(
                x=df['epoch'], y=df['val/cls_loss'], 
                name='Class Loss (Val)', 
                line=dict(color='#8b5cf6', width=2.5, dash='dash'),
                mode='lines'
            ))
            
            fig.update_layout(
                title="Evolução das Perdas (Losses)",
                xaxis_title="Época",
                yaxis_title="Loss",
                hovermode='x unified',
                template='plotly_dark',
                height=500,
                paper_bgcolor='#1a1f2e',
                plot_bgcolor='#252d3d',
                font=dict(family="Poppins", size=12, color='#ffffff'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            fig = px.scatter(
                df, 
                x='metrics/recall(B)', 
                y='metrics/precision(B)', 
                color='epoch', 
                size='metrics/mAP50-95(B)',
                hover_data=['epoch', 'metrics/mAP50(B)'],
                color_continuous_scale=[[0, '#7c3aed'], [0.5, '#06b6d4'], [1, '#00d9ff']],
                title='Precisão vs Recall ao Longo do Treinamento'
            )
            
            fig.update_layout(
                template='plotly_dark',
                height=500,
                paper_bgcolor='#1a1f2e',
                plot_bgcolor='#252d3d',
                font=dict(family="Poppins", size=12, color='#ffffff'),
                xaxis_title="Recall",
                yaxis_title="Precisão"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['epoch'], 
                y=df['metrics/mAP50-95(B)'],
                fill='tozeroy',
                name='mAP50-95',
                line=dict(color='#00d9ff', width=3),
                fillcolor='rgba(0, 217, 255, 0.2)',
                mode='lines'
            ))
            
            fig.update_layout(
                title="Evolução do mAP50-95",
                xaxis_title="Época",
                yaxis_title="mAP50-95",
                template='plotly_dark',
                height=500,
                paper_bgcolor='#1a1f2e',
                plot_bgcolor='#252d3d',
                font=dict(family="Poppins", size=12, color='#ffffff')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Matrizes de confusão e curvas
        st.markdown("### 🎯 Análises Visuais Detalhadas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                st.markdown("#### Matriz de Confusão Normalizada")
                img = Image.open('results/confusion_matrix_normalized.png')
                st.image(img, use_container_width=True)
            except:
                st.info("Matriz de confusão não disponível")
        
        with col2:
            try:
                st.markdown("#### Curva Precision-Recall")
                img = Image.open('results/BoxPR_curve.png')
                st.image(img, use_container_width=True)
            except:
                st.info("Curva PR não disponível")
        
        col3, col4 = st.columns(2)
        
        with col3:
            try:
                st.markdown("#### Curva de Precisão")
                img = Image.open('results/BoxP_curve.png')
                st.image(img, use_container_width=True)
            except:
                pass
        
        with col4:
            try:
                st.markdown("#### Curva de Recall")
                img = Image.open('results/BoxR_curve.png')
                st.image(img, use_container_width=True)
            except:
                pass

# Página: Testar Modelo
elif selected == "Testar":
    show_header()
    
    st.markdown("### Teste o Modelo em Tempo Real")
    
    model = load_model()
    
    if model:
        tab1, tab2 = st.tabs(["Imagens de Teste", "Upload de Imagem"])
        
        with tab1:
            test_images = get_test_images()
            
            if test_images:
                st.markdown("#### Selecione uma Imagem para Análise")
                
                # Inicializar estado da sessão
                if 'selected_image_path' not in st.session_state:
                    st.session_state.selected_image_path = None
                if 'analyzing' not in st.session_state:
                    st.session_state.analyzing = False
                
                # Usar image_select para mostrar todas as imagens
                selected_image = image_select(
                    label="",
                    images=test_images,
                    captions=[f"Imagem {i+1}" for i in range(len(test_images))],
                    use_container_width=True,
                    return_value="original"
                )
                
                # Botão de análise
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Analisar Imagem Selecionada", key="analyze_btn", use_container_width=True, type="primary"):
                        st.session_state.selected_image_path = selected_image
                        st.session_state.analyzing = True
                
                # Análise com animação
                if st.session_state.analyzing and st.session_state.selected_image_path:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    
                    # Animação de loading
                    with st.spinner("Analisando imagem com YOLOv8..."):
                        # Carregar configurações
                        config = load_config()
                        conf_threshold = config['detection']['confidence_threshold']
                        iou_threshold = config['detection']['iou_threshold']
                        img_size = config['detection']['image_size']
                        max_det = config['detection']['max_detections']
                        half = config['performance']['use_half_precision']
                        
                        # Medir tempo de inferência
                        start_time = time.time()
                        
                        results = model.predict(
                            st.session_state.selected_image_path, 
                            conf=conf_threshold,
                            iou=iou_threshold,
                            imgsz=img_size,
                            max_det=max_det,
                            half=half,
                            verbose=False
                        )
                        
                        inference_time = time.time() - start_time
                        
                        # Pequeno delay para animação
                        time.sleep(0.3)
                    
                    # Mostrar resultados com design premium
                    if len(results[0].boxes) > 0:
                        # Obter informações da detecção
                        box = results[0].boxes[0]
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        breed_name = model.names[cls]
                        
                        # Grid compacto com todos os elementos em uma linha
                        metric_cols = st.columns([2, 1, 1, 1])
                        
                        with metric_cols[0]:
                            st.markdown(f"""
                                <div style='background: var(--bg-tertiary); border: 1px solid var(--border-color); 
                                     border-radius: 10px; padding: 0.9rem; text-align: center;
                                     box-shadow: 0 2px 8px rgba(0, 217, 255, 0.1); height: 100%;
                                     display: flex; flex-direction: column; justify-content: center;'>
                                    <div style='font-size: 0.6em; text-transform: uppercase; letter-spacing: 1px; 
                                         color: var(--text-secondary); margin-bottom: 0.3rem; font-weight: 500;'>
                                        Raça Identificada
                                    </div>
                                    <div style='font-size: 1.5em; font-weight: 700; 
                                         background: var(--accent-gradient); 
                                         -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                                         letter-spacing: -0.5px;'>
                                        {breed_name}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with metric_cols[1]:
                            st.markdown(f"""
                                <div style='background: var(--bg-tertiary); border: 1px solid var(--border-color); 
                                     border-radius: 10px; padding: 0.9rem; text-align: center;
                                     box-shadow: 0 2px 8px rgba(0, 217, 255, 0.08); height: 100%;
                                     display: flex; flex-direction: column; justify-content: center;'>
                                    <div style='font-size: 1.4em; font-weight: 700; 
                                         background: linear-gradient(135deg, #00d9ff, #06b6d4); 
                                         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                                         margin-bottom: 0.25rem;'>
                                        {conf:.1%}
                                    </div>
                                    <div style='font-size: 0.65em; color: var(--text-secondary); 
                                         text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500;'>
                                        Confiança
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with metric_cols[2]:
                            st.markdown(f"""
                                <div style='background: var(--bg-tertiary); border: 1px solid var(--border-color); 
                                     border-radius: 10px; padding: 0.9rem; text-align: center;
                                     box-shadow: 0 2px 8px rgba(124, 58, 237, 0.08); height: 100%;
                                     display: flex; flex-direction: column; justify-content: center;'>
                                    <div style='font-size: 1.4em; font-weight: 700; 
                                         background: linear-gradient(135deg, #7c3aed, #8b5cf6); 
                                         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                                         margin-bottom: 0.25rem;'>
                                        {inference_time:.2f}s
                                    </div>
                                    <div style='font-size: 0.65em; color: var(--text-secondary); 
                                         text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500;'>
                                        Tempo
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with metric_cols[3]:
                            st.markdown(f"""
                                <div style='background: var(--bg-tertiary); border: 1px solid var(--border-color); 
                                     border-radius: 10px; padding: 0.9rem; text-align: center;
                                     box-shadow: 0 2px 8px rgba(0, 217, 255, 0.08); height: 100%;
                                     display: flex; flex-direction: column; justify-content: center;'>
                                    <div style='font-size: 1.4em; font-weight: 700; color: var(--accent-primary);
                                         margin-bottom: 0.25rem;'>
                                        YOLOv8n
                                    </div>
                                    <div style='font-size: 0.65em; color: var(--text-secondary); 
                                         text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500;'>
                                        Modelo
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
                        
                        # Comparação visual lado a lado
                        col_img1, col_img2 = st.columns(2, gap="small")
                        
                        with col_img1:
                            st.markdown("#### Imagem Original")
                            original_img = Image.open(st.session_state.selected_image_path)
                            st.image(original_img, use_container_width=True)
                        
                        with col_img2:
                            st.markdown("#### Detecção")
                            # Plotar com configurações otimizadas
                            result_img = results[0].plot(
                                line_width=3,
                                labels=True,
                                conf=True,
                                boxes=True
                            )
                            st.image(result_img, use_container_width=True)
                        
                        # Espaçamento para não sobrepor o footer
                        st.markdown("<div style='margin-bottom: 3rem;'></div>", unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Nenhum cão detectado na imagem. Tente outra imagem.")
            else:
                st.info("📁 Adicione imagens PNG na pasta 'images' para testá-las aqui!")
                st.markdown("""
                <div class="info-box">
                    <p>Aguardando o upload de 8 imagens PNG na pasta <code>images/</code></p>
                    <p>As imagens aparecerão automaticamente aqui quando adicionadas.</p>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("#### Faça upload de uma imagem")
            uploaded_file = st.file_uploader("Escolha uma imagem", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("#### Imagem Enviada")
                    st.image(image, use_container_width=True)
                
                with col2:
                    st.markdown("#### Detecção")
                    with st.spinner("Processando..."):
                        # Salvar temporariamente
                        temp_path = "temp_upload.jpg"
                        image.save(temp_path)
                        
                        # Carregar configurações
                        config = load_config()
                        conf_threshold = config['detection']['confidence_threshold']
                        iou_threshold = config['detection']['iou_threshold']
                        img_size = config['detection']['image_size']
                        max_det = config['detection']['max_detections']
                        half = config['performance']['use_half_precision']
                        
                        # Medir tempo de inferência
                        start_time = time.time()
                        
                        results = model.predict(
                            temp_path,
                            conf=conf_threshold,
                            iou=iou_threshold,
                            imgsz=img_size,
                            max_det=max_det,
                            half=half
                        )
                        
                        inference_time = time.time() - start_time
                        
                        # Visualizar resultado
                        result_img = results[0].plot(
                            line_width=config['visualization']['line_thickness'],
                            labels=config['visualization']['show_labels'],
                            conf=config['visualization']['show_confidence']
                        )
                        st.image(result_img, use_container_width=True)
                        
                        # Mostrar tempo de inferência
                        if config.get('debug', {}).get('show_inference_time', True):
                            st.caption(f"⏱️ Tempo de inferência: {inference_time:.3f}s")
                        
                        # Limpar arquivo temporário
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                
                # Mostrar detecções
                if len(results[0].boxes) > 0:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown("#### Detecções Encontradas")
                    
                    det_cols = st.columns(min(3, len(results[0].boxes)))
                    
                    for idx, box in enumerate(results[0].boxes):
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        class_name = model.names[cls]
                        
                        with det_cols[idx % 3]:
                            st.markdown(f"""
                                <div class="metric-card">
                                    <div class="metric-label">🐕 {class_name}</div>
                                    <div class="metric-value">{conf:.1%}</div>
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Nenhum cão detectado na imagem")
    else:
        st.error("❌ Não foi possível carregar o modelo. Verifique se o arquivo 'weights/best.pt' existe.")

# Página: Sobre o Modelo
else:  # "Sobre"
    show_header()
    
    args = load_args()
    
    if args:
        st.markdown("### 🔬 Especificações Técnicas do Modelo")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <h4>🏗️ Arquitetura</h4>
                <ul style='line-height: 2;'>
                    <li><b>Modelo Base:</b> YOLOv8n (Nano)</li>
                    <li><b>Framework:</b> Ultralytics</li>
                    <li><b>Tamanho de Entrada:</b> 640x640 pixels</li>
                    <li><b>Classes:</b> 120 raças de cães</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
                <h4>📊 Dataset</h4>
                <ul style='line-height: 2;'>
                    <li><b>Fonte:</b> Stanford Dogs Dataset</li>
                    <li><b>Raças:</b> 120 diferentes</li>
                    <li><b>Qualidade:</b> Alta resolução</li>
                    <li><b>Diversidade:</b> Múltiplas poses e ambientes</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="info-box">
                <h4>⚙️ Hiperparâmetros de Treinamento</h4>
                <ul style='line-height: 2;'>
                    <li><b>Épocas:</b> {args.get('epochs', 'N/A')}</li>
                    <li><b>Paciência (Early Stop):</b> {args.get('patience', 'N/A')}</li>
                    <li><b>Learning Rate Inicial:</b> {args.get('lr0', 'N/A')}</li>
                    <li><b>Momentum:</b> {args.get('momentum', 'N/A')}</li>
                    <li><b>Weight Decay:</b> {args.get('weight_decay', 'N/A')}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="info-box">
                <h4>🎨 Augmentações de Dados</h4>
                <ul style='line-height: 2;'>
                    <li><b>HSV-H:</b> {args.get('hsv_h', 'N/A')}</li>
                    <li><b>Flip LR:</b> {args.get('fliplr', 'N/A')}</li>
                    <li><b>Mosaic:</b> {args.get('mosaic', 'N/A')}</li>
                    <li><b>Scale:</b> {args.get('scale', 'N/A')}</li>
                    <li><b>Translate:</b> {args.get('translate', 'N/A')}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("### 📈 Performance e Métricas")
        
        df = load_training_data()
        if df is not None:
            final_epoch = df.iloc[-1]
            
            # Usar métricas nativas do Streamlit
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="📊 Precisão",
                    value=f"{final_epoch['metrics/precision(B)']:.1%}",
                    help="Proporção de predições positivas corretas"
                )
                st.metric(
                    label="📊 Recall",
                    value=f"{final_epoch['metrics/recall(B)']:.1%}",
                    help="Proporção de positivos reais encontrados"
                )
            
            with col2:
                st.metric(
                    label="🎯 mAP50",
                    value=f"{final_epoch['metrics/mAP50(B)']:.1%}",
                    help="Precisão média em IoU 0.5"
                )
                st.metric(
                    label="🎯 mAP50-95",
                    value=f"{final_epoch['metrics/mAP50-95(B)']:.1%}",
                    help="Precisão média em IoU 0.5-0.95"
                )
            
            with col3:
                st.metric(
                    label="📉 Box Loss",
                    value=f"{final_epoch['val/box_loss']:.4f}",
                    help="Erro de localização da caixa"
                )
                st.metric(
                    label="📉 Class Loss",
                    value=f"{final_epoch['val/cls_loss']:.4f}",
                    help="Erro de classificação"
                )
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("### 🎯 Aplicações e Uso")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="info-box" style="text-align: center;">
                <h3>🏥</h3>
                <h4>Veterinária</h4>
                <p>Identificação rápida de raças em clínicas veterinárias</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box" style="text-align: center;">
                <h3>🏠</h3>
                <h4>Adoção</h4>
                <p>Catalogação automática em abrigos de animais</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="info-box" style="text-align: center;">
                <h3>📱</h3>
                <h4>Apps Mobile</h4>
                <p>Integração em aplicativos de pet care</p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--border-color);'>
        <div style='text-align: center; color: var(--text-secondary); font-family: Poppins;'>
            <p style='font-size: 0.9em; margin: 0.5rem 0;'>
                <span style='background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 600;'>
                DogBreed Vision
                </span>
                <span style='opacity: 0.6;'> · Powered by YOLOv8 & Streamlit</span>
            </p>
            <p style='font-size: 0.8em; opacity: 0.5; margin: 0.5rem 0;'>
                120 breeds · mAP 84.3% · Deep Learning Portfolio Project
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

