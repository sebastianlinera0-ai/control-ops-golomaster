import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Control de Órdenes de Producción", layout="wide")

# ==========================================
# 1. BARRAS DE NAVEGACIÓN Y MÓDULOS
# ==========================================
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.button("📌 Módulo Producción", use_container_width=True, type="primary")
with col_m2:
    st.button("📦 Módulo Stocks", use_container_width=True)
with col_m3:
    st.button("📅 Módulo Planning", use_container_width=True)
with col_m4:
    st.button("📊 Módulo Analítica", use_container_width=True)

st.write("")  # Espaciado

# ==========================================
# 2. 🤖 ASISTENTE DE AYUDA (PARTE SUPERIOR)
# ==========================================
with st.expander("🤖 Asistente de Ayuda Golomaster - ¿Necesitas ayuda con la app?", expanded=False):
    pregunta_asistente = st.selectbox(
        "Selecciona una consulta:",
        [
            "Selecciona una opción...",
            "📝 ¿Cómo ingresar una Orden de Producción (OP)?",
            "📦 ¿Cómo registrar parciales de producción?",
            "📅 ¿Cómo funciona el Cronograma Semanal?",
            "🏷️ ¿Cómo generar una etiqueta de Último Parcial?",
            "🧹 ¿Para qué sirve el botón Limpiar Formulario?"
        ]
    )

    if pregunta_asistente == "📝 ¿Cómo ingresar una Orden de Producción (OP)?":
        st.info("""
        **Pasos para ingresar una OP:**
        1. Ingresa la **Fecha de la OP** y el número de **OP N°**.
        2. Selecciona el **Cliente** y el **Producto** en los menús desplegables.
        3. Indica la **Cantidad Total a Producir**.
        4. Al completar estos datos, la sección de *Registro de Parciales* se habilitará automáticamente.
        """)

    elif pregunta_asistente == "📦 ¿Cómo registrar parciales de producción?":
        st.info("""
        **Pasos para registrar un parcial:**
        1. Asegúrate de haber completado los datos de la OP arriba.
        2. En la tabla de *Registro de Parciales*, selecciona **Turno** y **Responsable**.
        3. Verifica el **Lote** y la fecha de **VTO**.
        4. Ingresa la **Cant. Producida** y, si aplica, las Mermas o Scrap.
        """)

    elif pregunta_asistente == "📅 ¿Cómo funciona el Cronograma Semanal?":
        st.info("""
        **Uso del Cronograma:**
        * Muestra las OPs planificadas y cargadas para la semana en curso.
        * Te permite visualizar rápidamente qué cliente, producto y cantidad están programados por turno y día.
        """)

    elif pregunta_asistente == "🏷️ ¿Cómo generar una etiqueta de Último Parcial?":
        st.info("""
        **Generar Etiqueta:**
        * Haz clic en el botón **'Generar Etiqueta ÚLTIMO Parcial'** una vez completados los datos del último turno o parcial de la producción.
        * Se desplegará la vista previa lista para mandar a imprimir.
        """)

    elif pregunta_asistente == "🧹 ¿Para qué sirve el botón Limpiar Formulario?":
        st.info("""
        **Limpiar Formulario:**
        * Reinicia todos los campos de la OP y de los parciales a sus valores vacíos o por defecto para comenzar a cargar una nueva orden desde cero.
        """)

st.divider()

# ==========================================
# 3. CRONOGRAMA SEMANAL DE PLANIFICACIÓN
# ==========================================
st.subheader("📅 CRONOGRAMA SEMANAL DE PLANIFICACIÓN")

dias = [
    "LUNES 21/09/26", "MARTES 22/09/26", "MIÉRCOLES 23/09/26", 
    "JUEVES 24/09/26", "VIERNES 25/09/26", "SÁBADO 26/09/26"
]

cols_dias = st.columns(len(dias))
for i, dia in enumerate(dias):
    with cols_dias[i]:
        st.markdown(f"<div style='background-color: #ffff00; color: black; font-weight: bold; text-align: center;'>{dia}</div>", unsafe_allow_html=True)
        if dia == "VIERNES 25/09/26":
            st.caption("OP: 189 | Turno: M | Cliente: DELUX | BARRA DE CHOCOLATE")
        else:
            st.caption("empty")

st.divider()

# ==========================================
# 4. FORMULARIO PRINCIPAL - CONTROL DE OP
# ==========================================
st.title("📋 Control de órdenes de producción Golomaster V1")

col_f1, col_f2 = st.columns(2)

with col_f1:
    fecha_op = st.date_input("FECHA DE LA OP")
    op_num = st.text_input("OP N°")
    cant_total = st.number_input("Cantidad Total a Producir", min_value=0, step=1)

with col_f2:
    cliente = st.selectbox("CLIENTE", ["Choose an option", "DELUX", "Cliente B", "Cliente C"])
    producto = st.selectbox("PRODUCTO", ["Choose an option", "BARRA DE CHOCOLATE SABOR CH", "Producto Y"])
    
    if cliente == "Choose an option" or producto == "Choose an option":
        st.info("Seleccione un cliente y producto.")

st.write("")

# Botones de Acción
col_b1, col_b2, col_b3 = st.columns([1, 1, 2])
with col_b1:
    if st.button("🧹 Limpiar Formulario"):
        st.rerun()
with col_b2:
    st.button("🏷️ Generar Etiqueta ÚLTIMO Parcial")

st.divider()

# ==========================================
# 5. REGISTRO DE PARCIALES
# ==========================================
st.subheader("📦 Registro de Parciales")

# Validación para habilitar formulario
if op_num == "" or cliente == "Choose an option" or cant_total <= 0:
    st.warning("⚠️ Para comenzar a cargar parciales, primero debe completar el N° de OP, Cliente, Producto y Cantidad Total (> 0).")
else:
    st.success("✅ Formulario habilitado para la carga de parciales.")

# Fila del Parcial 1
col_p1, col_p2, col_p3, col_p4, col_p5, col_p6, col_p7, col_p8 = st.columns(8)

with col_p1:
    st.write("**Parcial**")
    st.text("Parcial 1")
with col_p2:
    turno = st.selectbox("Turno", ["Choose an option", "Mañana", "Tarde", "Noche"])
with col_p3:
    responsable = st.selectbox("Responsable", ["Choose an option", "Juan Pérez", "María Gómez"])
with col_p4:
    fecha_parcial = st.date_input("Fecha", key="f_parcial")
with col_p5:
    lote = st.text_input("Lote", value="240926")
with col_p6:
    vto = st.text_input("VTO", value="-")
with col_p7:
    mermas = st.number_input("Mermas.C", min_value=0.0, step=0.1)
with col_p8:
    cant_prod = st.number_input("Cant. Producida", min_value=0, step=1)
