import streamlit as st
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from PIL import Image
import cloudinary
import cloudinary.uploader
import os

# Configuración de Cloudinary
cloudinary.config(
    cloud_name="dpr44kuqn",       # Reemplaza con tu nombre de nube en Cloudinary
    api_key="933457466638462",             # Reemplaza con tu API key
    api_secret="8NcyXgjjlhUU4-zY0TDaw0HUQ_s"        # Reemplaza con tu API secret
)

# Configuración de la base de datos SQLite
engine = create_engine('sqlite:///comentarios.db')
Base = declarative_base()

class Comentario(Base):
    __tablename__ = 'comentarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    rol = Column(String, nullable=True)
    comentario = Column(Text, nullable=False)
    foto_url = Column(String, nullable=True)
    hora = Column(String, nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Título de la app con estilo
st.title("🍕 Mis compromisos con la cultura de calidad e inocuidad - 2024")

# Sidebar para seleccionar entre "Cargar comentario" y "Ver comentarios"
opcion = st.sidebar.selectbox("Selecciona una sección", ["Cargar compromiso", "Ver compromisos"], index=1)

# Función para subir la foto a Cloudinary
def subir_foto_a_cloudinary(file, nombre):
    if file:
        # Guardar archivo temporalmente y subir a Cloudinary
        img = Image.open(file)
        img_path = f"temp_{nombre}.png"
        img.save(img_path)
        
        upload_result = cloudinary.uploader.upload(img_path, folder="comentarios_clase")
        foto_url = upload_result.get('secure_url')
        
        # Eliminar archivo temporal
        os.remove(img_path)
        
        return foto_url
    return None

# Sección de carga de comentarios
if opcion == "Cargar compromiso":
    with st.form(key="formulario_comentario"):
        st.header("📣 Cargar un nuevo compromiso")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            foto = st.file_uploader("Sube tu foto", type=['jpg', 'png'])
        with col2:
            nombre = st.text_input("Nombre")
            rol = st.text_input("Rol (e.g., Estudiante, Profesor)")
            comentario = st.text_area("Escribe tu compromiso", height=150)
            
        enviar = st.form_submit_button(label="Enviar ✨")

    if enviar and nombre and comentario:
        foto_url = subir_foto_a_cloudinary(foto, nombre)
        nuevo_comentario = Comentario(
            nombre=nombre,
            rol=rol,
            comentario=comentario,
            foto_url=foto_url,
            hora=datetime.now().strftime('%I:%M %p')
        )
        session.add(nuevo_comentario)
        session.commit()
        st.success("¡Comentario agregado con éxito! 🎉")

# Sección de visualización de comentarios
elif opcion == "Ver compromisos":
    st.header("📝 Compromisos")

    comentarios = session.query(Comentario).all()
    
    # Mostrar los comentarios en una cuadrícula de 2 columnas
    for row in range(0, len(comentarios), 3):
        cols = st.columns(3)
        for i, comentario_data in enumerate(comentarios[row:row+3]):
            with cols[i]:
                if comentario_data.foto_url:
                    st.image(comentario_data.foto_url, width=100)
                st.markdown(f"**{comentario_data.nombre}** ({comentario_data.rol}) - _{comentario_data.hora}_", unsafe_allow_html=True)
                st.write(f"_{comentario_data.comentario}_")
                st.markdown("---")

# Agregar un fondo atractivo o modificar el tema
st.markdown("""
    <style>
    .css-1d391kg {background-color: #f8f8f8;}  # Color de fondo para la app
    .css-1v3fvcr {font-size: 18px; color: #333;} # Estilo de los textos en el formulario
    </style>
""", unsafe_allow_html=True)
