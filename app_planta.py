import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Scanner Metal Química", layout="wide")

st.title("🛠️ Scanner Bruto - O Molde Perfeito")
st.write("Limpando a sujeira pra você decalcar no Corel com o chassi alinhado.")

uploaded_file = st.file_uploader("Sobe a foto ou print da planta aqui (JPG, PNG)", type=["jpg", "jpeg", "png"])

st.sidebar.header("🎛️ 1. Alinhamento de Direção")
angulo = st.sidebar.slider("Girar a Planta (Graus)", -45.0, 45.0, 0.0, step=0.5)

if uploaded_file is not None:
    image_original = Image.open(uploaded_file).convert("RGB")
    
    if angulo != 0:
        image_original = image_original.rotate(-angulo, expand=True, fillcolor=(255, 255, 255))
        
    img_array = np.array(image_original)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    st.sidebar.header("🔥 2. O Ferro de Passar")
    forca_ferro = st.sidebar.slider("Força do Fundo Branco", 1, 151, 51, step=2)
    
    # LINHA 34 - OLHA O PARÊNTESE FECHANDO NO FINAL, CARALHO!
    fundo_borrado = cv2.GaussianBlur(gray, (forca_ferro, forca_ferro), 0)
    imagem_passada = cv2.divide(gray, fundo_borrado, scale=255)

    st.sidebar.header("🖋️ 3. Tinta da Caneta")
    contraste = st.sidebar.slider("Escurecer Linhas", 0, 100, 50)
    
    _, imagem_final = cv2.threshold(imagem_passada, 255 - contraste, 255, cv2.THRESH_TRUNC)
    imagem_final = cv2.normalize(imagem_final, None, 0, 255, cv2.NORM_MINMAX)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Planta Original")
        st.image(image_original, use_container_width=True)

    with col2:
        st.subheader("Planta Pronta")
        st.image(imagem_final, use_container_width=True)
        
    img_pil_final = Image.fromarray(imagem_final)
    buf = io.BytesIO()
    img_pil_final.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.sidebar.header("📥 4. Exportar")
    st.sidebar.download_button(
        label="Baixar Molde (PNG)",
        data=byte_im,
        file_name="planta_metalquimica.png",
        mime="image/png"
    )
