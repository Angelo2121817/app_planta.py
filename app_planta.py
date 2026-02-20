import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Limpador de Plantas - Metal Química", layout="wide")

st.title("🛠️ Limpador de Plantas Bruto - V1")
st.write("Joga a foto imunda do cliente aqui pra gente derreter a sujeira no ácido antes de mandar pro Corel.")

uploaded_file = st.file_uploader("Sobe a planta cagada aqui (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Converter a imagem do Streamlit para o formato que o OpenCV entende (matriz)
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    # Se a imagem tiver canal alfa (PNG transparente), arranca fora
    if img_array.shape[-1] == 4:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)

    # 1º Banho: Transformar em Tons de Cinza (Arranca o amarelado do papel velho)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    # O Painel de Controle do Mecânico
    st.sidebar.header("🎛️ Regulagem do Ácido")
    st.sidebar.write("Ajuste a limpeza até a sujeira sumir e a linha ficar forte:")
    
    # Controles do Filtro Adaptativo (O melhor pra foto com sombra)
    block_size = st.sidebar.slider("Tamanho da Área (Ímpar)", 3, 99, 15, step=2)
    C = st.sidebar.slider("Nível de Corrosão (Contraste)", 0, 30, 5)

    # 2º Banho: O Threshold Adaptativo (A mágica que deixa Preto e Branco)
    # Ele analisa pedaço por pedaço da foto, por isso não fode tudo se tiver sombra de um lado só
    limpa = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Planta Original")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("Planta no Osso (Limpa)")
        # cmap='gray' pro Streamlit não cagar a cor de volta
        st.image(limpa, cmap="gray", use_container_width=True)
        
    st.success("Aí, caralho! O pior já saiu. Brinca nos controles ali do lado até ficar bom.")
