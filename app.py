import streamlit as st
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# Configuración de página
st.set_page_config(page_title="Control de Órdenes de Pedido", layout="wide")

st.title("📋 Control de Orden de Pedido (OP)")

# --- DICCIONARIO DE CLIENTES Y VIDA ÚTIL (MESES) ---
CLIENTES_VIDA_UTIL = {
    "INTEGRA": 7,
    "ENA": 12,
    "DELUXE": 12,
    "GARRAPIÑADA": 8
}

# --- ENCABEZADO DE LA OP ---
col1, col2, col3 = st.columns(3)

with col1:
    fecha_op = st.date_input("FECHA DE LA OP", value=date.today())
    num_op = st.text_input("OP N°", value="240")
    cant_total = st.number_input("Cantidad Total a Producir", value=87000, step=1000)

with col2:
    cliente = st.selectbox("CLIENTE", list(CLIENTES_VIDA_UTIL.keys()), index=0)
    producto = st.text_input("PRODUCTO", value="AVELLANA")

vida_util_meses = CLIENTES_VIDA_UTIL[cliente]

with col3:
    st.info(f"**Vida Útil para {cliente}:** {vida_util_meses} meses")

st.markdown("---")

# --- TABLA DE CARGA DE PARCIALES (1 a 10) ---
st.subheader("📦 Registro de Parciales")

# Inicializar estado si no existe
if "filas" not in st.session_state:
    st.session_state.filas = [
        {"Turno": "M", "Fecha": date.today(), "Cantidad": 45000},
        {"Turno": "T", "Fecha": datetime.strptime("14/09/2026", "%d/%m/%Y").date(), "Cantidad": 0},
    ] + [{"Turno": "", "Fecha": None, "Cantidad": 0} for _ in range(8)]

hoy = date.today()
max_vto = hoy + relativedelta(months=13)
tot_producido = 0

# Encabezados de la tabla
c_parc, c_tur, c_fec, c_lot, c_vto, c_cant = st.columns([1.2, 0.8, 1.5, 1.2, 1.5, 1.5])
c_parc.markdown("**Parcial**")
c_tur.markdown("**Turno**")
c_fec.markdown("**Fecha**")
c_lot.markdown("**Lote**")
c_vto.markdown("**VTO**")
c_cant.markdown("**Cant. Producida**")

for i in range(10):
    nombre_parcial = f"Parcial {i+1}"
    
    col_parcial, col_turno, col_fecha, col_lote, col_vto, col_cant = st.columns([1.2, 0.8, 1.5, 1.2, 1.5, 1.5])
    
    with col_parcial:
        st.write(f"{nombre_parcial}")
        
    with col_turno:
        turno = st.selectbox("", ["", "M", "T", "N"], key=f"turno_{i}", index=["", "M", "T", "N"].index(st.session_state.filas[i]["Turno"]) if st.session_state.filas[i]["Turno"] in ["", "M", "T", "N"] else 0, label_visibility="collapsed")
        
    with col_fecha:
        f_val = st.date_input("", value=st.session_state.filas[i]["Fecha"] if st.session_state.filas[i]["Fecha"] else hoy, key=f"fecha_{i}", label_visibility="collapsed")
        
    # Lógica de Lote y Vencimiento
    lote_str = f_val.strftime("%d%m%y") if f_val else ""
    vto_date = f_val + relativedelta(months=vida_util_meses) if f_val else None
    vto_str = vto_date.strftime("%d%m%y") if vto_date else ""
    
    # Validaciones
    es_hoy = (f_val == hoy)
    es_vto_valido = (vto_date and hoy <= vto_date <= max_vto)
    
    with col_lote:
        st.text_input("", value=lote_str, disabled=True, key=f"lote_{i}", label_visibility="collapsed")
        
    with col_vto:
        vto_label = f"{vto_str} 🟢" if es_vto_valido else f"{vto_str} 🔴"
        st.text_input("", value=vto_label, disabled=True, key=f"vto_{i}", label_visibility="collapsed")
        
    with col_cant:
        cant = st.number_input("", min_value=0, value=int(st.session_state.filas[i]["Cantidad"]), step=1000, key=f"cant_{i}", label_visibility="collapsed")
        tot_producido += cant

# --- RESUMEN Y TOTALES ---
st.markdown("---")
col_res1, col_res2 = st.columns(2)

restan = cant_total - tot_producido

with col_res1:
    st.metric(label="Total Producido", value=f"{tot_producido:,}".replace(",", "."))

with col_res2:
    st.metric(
        label="Restan", 
        value=f"{restan:,}".replace(",", "."), 
        delta=-restan, 
        delta_color="inverse" if restan > 0 else "normal"
    )