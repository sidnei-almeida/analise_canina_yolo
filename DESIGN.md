# 🎨 Design System - Canine AI

## Paleta de Cores Dark Premium

### Cores Principais
```css
--bg-primary: #0f1419      /* Fundo principal escuro */
--bg-secondary: #1a1f2e    /* Sidebar e cards */
--bg-tertiary: #252d3d     /* Cards e elementos elevados */
```

### Cores de Destaque
```css
--accent-primary: #00d9ff   /* Cyan brilhante */
--accent-secondary: #7c3aed /* Purple profundo */
--accent-gradient: linear-gradient(135deg, #00d9ff 0%, #7c3aed 100%)
```

### Cores de Texto
```css
--text-primary: #ffffff     /* Texto principal */
--text-secondary: #a0aec0   /* Texto secundário */
--border-color: rgba(255, 255, 255, 0.1) /* Bordas sutis */
```

---

## Tipografia

### Fonte Principal
- **Família:** Poppins (Google Fonts)
- **Pesos:** 300 (Light), 400 (Regular), 500 (Medium), 600 (SemiBold), 700 (Bold)

### Hierarquia
- **H1 (Título Principal):** 3em, Bold, Gradiente Cyan-Purple
- **H3 (Seções):** 1.5em, SemiBold, Underline Gradiente
- **Subtítulo:** 1.1em, Light, Color Secondary
- **Body:** 1em, Regular, Color Primary

---

## Componentes

### Cards de Métricas
```css
Background: var(--bg-tertiary)
Border: 1px solid var(--border-color)
Border-top: 3px solid gradient
Border-radius: 12px
Padding: 1.5rem
Hover: Elevação + Borda Cyan
```

**Características:**
- Borda superior com gradiente
- Efeito hover com elevação
- Shadow cyan ao passar o mouse
- Números com gradiente

### Info Boxes
```css
Background: var(--bg-tertiary)
Border-left: 3px solid cyan
Border-radius: 8px
Padding: 1.5rem
```

**Uso:**
- Informações importantes
- Descrições de funcionalidades
- Notas e avisos

### Botões
```css
Background: gradient(cyan → purple)
Color: white
Border-radius: 8px
Padding: 0.6rem 1.5rem
Shadow: rgba(0, 217, 255, 0.3)
```

**Estados:**
- Normal: Gradiente suave
- Hover: Elevação + Shadow intenso

### Tabs
```css
Background (lista): var(--bg-secondary)
Tab ativa: gradient
Tab inativa: transparente
Border-radius: 6px
```

---

## Gráficos Plotly

### Configuração Dark
```python
template='plotly_dark'
paper_bgcolor='#1a1f2e'
plot_bgcolor='#252d3d'
font=dict(family="Poppins", size=12, color='#ffffff')
```

### Cores de Linhas
- **Linha 1:** `#00d9ff` (Cyan)
- **Linha 2:** `#7c3aed` (Purple)
- **Linha 3:** `#06b6d4` (Cyan claro)
- **Linha 4:** `#8b5cf6` (Purple claro)

### Gradientes
```python
color_continuous_scale=[
    [0, '#7c3aed'],    # Purple
    [0.5, '#06b6d4'],  # Cyan médio
    [1, '#00d9ff']     # Cyan brilhante
]
```

---

## Elementos Interativos

### Upload Area
```css
Background: var(--bg-tertiary)
Border: 2px dashed cyan
Border-radius: 12px
Padding: 2rem
```

### Expanders
```css
Background: var(--bg-tertiary)
Border: 1px solid border-color
Border-radius: 8px
```

### Inputs e Selects
```css
Background: var(--bg-tertiary)
Color: var(--text-primary)
Border: 1px solid border-color
Border-radius: 8px
```

### Progress Bars
```css
Background: gradient(cyan → purple)
```

### Spinners
```css
Border-top-color: cyan
```

---

## Scrollbar Customizada

```css
Width: 8px
Track: var(--bg-secondary)
Thumb: var(--bg-tertiary)
Thumb Hover: var(--accent-primary)
Border-radius: 4px
```

---

## Espaçamento

### Padrões
- **Extra Small:** 0.5rem (8px)
- **Small:** 1rem (16px)
- **Medium:** 1.5rem (24px)
- **Large:** 2rem (32px)
- **Extra Large:** 3rem (48px)

### Aplicações
- **Padding Cards:** 1.5rem
- **Margin Sections:** 2rem top
- **Gap Columns:** 1rem
- **Border Radius:** 8px - 12px

---

## Efeitos e Transições

### Hover em Cards
```css
transition: all 0.3s ease
transform: translateY(-5px)
border-color: var(--accent-primary)
box-shadow: 0 10px 30px rgba(0, 217, 255, 0.2)
```

### Hover em Botões
```css
transition: all 0.3s ease
transform: translateY(-2px)
box-shadow: 0 6px 25px rgba(0, 217, 255, 0.5)
```

### Gradientes de Texto
```css
background: var(--accent-gradient)
-webkit-background-clip: text
-webkit-text-fill-color: transparent
```

---

## Sidebar

### Estilo
```css
Background: var(--bg-secondary)
Border-right: 1px solid border-color
Text: var(--text-primary)
```

### Menu de Navegação
- **Background:** Transparente
- **Item Ativo:** Gradiente cyan-purple
- **Item Inativo:** Texto secondary
- **Hover:** Background rgba(255,255,255,0.2)

---

## Responsividade

### Colunas
- **4 colunas:** Métricas principais
- **3 colunas:** Informações técnicas
- **2 colunas:** Comparações
- **1 coluna:** Gráficos e análises

### Breakpoints (Streamlit)
- Mobile: 1 coluna
- Tablet: 2 colunas
- Desktop: 3-4 colunas

---

## Boas Práticas

### CSS
1. ✅ Usar variáveis CSS (`:root`)
2. ✅ Evitar `!important` (exceto quando necessário)
3. ✅ Manter especificidade baixa
4. ✅ Agrupar seletores relacionados
5. ✅ Comentar seções complexas

### Streamlit
1. ✅ Usar componentes nativos quando possível
2. ✅ Evitar HTML excessivo
3. ✅ Aproveitar `st.metric`, `st.columns`, `st.tabs`
4. ✅ Cache para performance (`@st.cache_data`)
5. ✅ Templates dark do Plotly

### Performance
1. ✅ Transições suaves (0.3s)
2. ✅ Sombras sutis
3. ✅ Evitar animações complexas
4. ✅ Otimizar imagens
5. ✅ Lazy loading quando possível

---

## Componentes Personalizados

### Metric Card (HTML)
```python
st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
""", unsafe_allow_html=True)
```

### Info Box (HTML)
```python
st.markdown(f"""
    <div class="info-box">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
""", unsafe_allow_html=True)
```

### Native Metrics (Streamlit)
```python
st.metric(
    label="Label",
    value="Value",
    delta="Change",
    help="Description"
)
```

---

## Checklist de Design

Antes de fazer deploy:

- [ ] ✅ Todas as cores seguem a paleta definida
- [ ] ✅ Fonte Poppins carregada corretamente
- [ ] ✅ Gráficos usando template dark
- [ ] ✅ Bordas e espaçamentos consistentes
- [ ] ✅ Efeitos hover funcionando
- [ ] ✅ Scrollbar customizada
- [ ] ✅ Progress bars com gradiente
- [ ] ✅ Inputs e selects com tema dark
- [ ] ✅ Imagens com bordas arredondadas
- [ ] ✅ Footer bem formatado
- [ ] ✅ Sidebar com menu estilizado

---

## Exemplos de Uso

### Criar um Card de Métrica
```python
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Precisão</div>
            <div class="metric-value">80.6%</div>
        </div>
    """, unsafe_allow_html=True)
```

### Criar um Info Box
```python
st.markdown("""
    <div class="info-box">
        <h4>🔬 Tecnologia</h4>
        <p>YOLOv8n com 120 classes de raças caninas</p>
    </div>
""", unsafe_allow_html=True)
```

### Gráfico Plotly Dark
```python
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=data['x'],
    y=data['y'],
    line=dict(color='#00d9ff', width=3),
    mode='lines'
))

fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='#1a1f2e',
    plot_bgcolor='#252d3d',
    font=dict(family="Poppins", size=12, color='#ffffff')
)

st.plotly_chart(fig, use_container_width=True)
```

---

## Referências

- **Fonte:** [Google Fonts - Poppins](https://fonts.google.com/specimen/Poppins)
- **Cores:** Inspirado em temas dark modernos (GitHub Dark, Discord, VS Code)
- **Componentes:** Streamlit Docs + Custom CSS
- **Gráficos:** Plotly Dark Template

---

**🐕 Canine AI** - Design System Dark Premium

