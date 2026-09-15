import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# Configuración de página
st.set_page_config(page_title="Control de órdenes de producción Golomaster V1", layout="wide")

st.title("📋 Control de órdenes de producción Golomaster V1")

# --- CONEXIÓN CON GOOGLE SHEETS / APPS SCRIPT ---
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbywDdFRA0GkivkkNk7uDXk6Q3hJkU47-lBZYnd_dz7D16kVF274AVgmXejyt2hF3Na_/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/17He8h4AfTjuMHLSTWOMAAMD960ow_-Gj-AvsI9XC_lc/export?format=csv"

def cargar_historial():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        return df
    except Exception:
        return pd.DataFrame()

def op_existe(num_op):
    df = cargar_historial()
    if not df.empty and "OP_Num" in df.columns:
        return str(num_op).strip() in df["OP_Num"].astype(str).str.strip().values
    return False

def guardar_op_en_sheets(datos_op, filas_parciales):
    registros = []
    
    for f in filas_parciales:
        if f["Cantidad"] > 0 or f["Turno"] != "" or f["Responsable"] != "":
            registro = {**datos_op, **f}
            registros.append(registro)
            
    if not registros:
        registros.append({
            **datos_op, 
            "Parcial": "Sin cargas", 
            "Turno": "", 
            "Responsable": "",
            "Fecha_Parcial": "", 
            "Lote": "", 
            "VTO": "", 
            "Mermas_C": 0.0,
            "Scrap_P": 0.0,
            "Cantidad": 0
        })
        
    try:
        response = requests.post(WEBAPP_URL, json=registros)
        return response.status_code == 200
    except Exception:
        return False

def solicitar_limpieza():
    st.session_state["necesita_limpieza"] = True

# --- DICCIONARIO DE CLIENTES, VIDA ÚTIL Y PRODUCTOS ---
CLIENTES_VIDA_UTIL = {
    "INTEGRA": 7,
    "ENA": 12,
    "DELUXE": 12,
    "GARRAPIÑADA": 8
}

PRODUCTOS_POR_CLIENTE = {
    "INTEGRA": [
        "BARRAS DE CACAO SABOR MANI",
        "BARRAS DE CACAO SABOR AVELLANA",
        "BARRAS DE CACAO SABOR COCO",
        "BARRAS DE CACAO CON CHOCOLATE",
        "BARRAS DE CACAO SABOR BANANA"
    ],
    "ENA": [
        "BARRA SABOR BANANA CM",
        "BARRA SABOR BANANA CT",
        "BARRA SABOR FRUTILLA CM",
        "BARRA SABOR FRUTILLA CT",
        "BARRA SABOR BROWNIE CM",
        "BARRA SABOR BROWNIE CT",
        "BARRA SABOR COCO CT",
        "SABOR COCO CM"
    ],
    "DELUXE": [
        "PRODUCTO DELUXE GENERAL"
    ],
    "GARRAPIÑADA": [
        "GARRAPIÑADA GENERAL"
    ]
}

LISTA_RESPONSABLES = ["", "Carlos", "Victor", "Guille", "Lujan", "Sebastian"]

# --- ENCABEZADO DE LA OP ---
col1, col2, col3 = st.columns(3)

with col1:
    fecha_op = st.date_input("FECHA DE LA OP", value=date.today(), key="fecha_op")
    num_op = st.text_input("OP N°", value="", key="num_op").strip()
    cant_total = st.number_input("Cantidad Total a Producir", value=87000, step=1000, key="cant_total")

with col2:
    cliente = st.selectbox("CLIENTE", list(CLIENTES_VIDA_UTIL.keys()), index=0, key="cliente_select")
    
    # Lista desplegable dinámica de productos según el cliente seleccionado
    lista_productos = PRODUCTOS_POR_CLIENTE.get(cliente, ["OTROS"])
    producto = st.selectbox("PRODUCTO", lista_productos, key="producto_select")

vida_util_meses = CLIENTES_VIDA_UTIL[cliente]

with col3:
    st.info(f"**Vida Útil para {cliente}:** {vida_util_meses} meses")

# Validación de OP existente
op_bloqueada = False
if num_op != "":
    if op_existe(num_op):
        st.error(f"⛔ LA OP N° '{num_op}' YA FUE CERRADA ANTERIORMENTE. NO SE PUEDE REUTILIZAR ESTE NÚMERO.")
        op_bloqueada = True

st.markdown("---")

# --- LÓGICA DE LIMPIEZA ---
if st.session_state.get("necesita_limpieza", False):
    for i in range(10):
        st.session_state[f"turno_{i}"] = ""
        st.session_state[f"resp_{i}"] = ""
        st.session_state[f"fecha_input_{i}"] = fecha_op
        st.session_state[f"lote_{i}"] = ""
        st.session_state[f"mermas_{i}"] = 0.0
        st.session_state[f"scrap_{i}"] = 0.0
        st.session_state[f"cant_{i}"] = 0
    st.session_state["necesita_limpieza"] = False

# --- BOTONES DE ACCIÓN LADO A LADO ---
col_btn1, col_btn2, _ = st.columns([1.5, 2.0, 3.0])

with col_btn1:
    st.button("🧹 Limpiar Solo Parciales", on_click=solicitar_limpieza, type="secondary")

with col_btn2:
    mostrar_etiqueta = st.button("🏷️ Generar Etiqueta ÚLTIMO Parcial", type="secondary")

def actualizar_fecha_fila(indice, fecha_base_op):
    f_ingresada = st.session_state[f"fecha_input_{indice}"]
    if f_ingresada < fecha_base_op:
        st.session_state[f"error_fecha_{indice}"] = True
        st.session_state[f"fecha_input_{indice}"] = fecha_base_op
    else:
        st.session_state[f"error_fecha_{indice}"] = False

# --- TABLA DE CARGA DE PARCIALES ---
st.subheader("📦 Registro de Parciales")

hoy = date.today()
max_vto = hoy + relativedelta(months=13)
tot_producido = 0
parciales_cargados = []

c_parc, c_tur, c_resp, c_fec, c_lot, c_vto, c_merm, c_scrap, c_cant = st.columns([1.0, 0.7, 1.2, 1.2, 1.0, 1.1, 0.9, 0.9, 1.2])

c_parc.markdown("**Parcial**")
c_tur.markdown("**Turno**")
c_resp.markdown("**Responsable**")
c_fec.markdown("**Fecha**")
c_lot.markdown("**Lote**")
c_vto.markdown("**VTO**")
c_merm.markdown("**Mermas.C**")
c_scrap.markdown("**Scrap.P**")
c_cant.markdown("**Cant. Producida**")

for i in range(10):
    nombre_parcial = f"Parcial {i+1}"
    col_p, col_t, col_r, col_f, col_l, col_v, col_m, col_s, col_c = st.columns([1.0, 0.7, 1.2, 1.2, 1.0, 1.1, 0.9, 0.9, 1.2])
    
    with col_p:
        st.write(f"{nombre_parcial}")
        
    with col_t:
        turno = st.selectbox("", ["", "M", "T", "N"], key=f"turno_{i}", disabled=op_bloqueada, label_visibility="collapsed")
        
    with col_r:
        responsable = st.selectbox("", LISTA_RESPONSABLES, key=f"resp_{i}", disabled=op_bloqueada, label_visibility="collapsed")
        
    with col_f:
        if f"fecha_input_{i}" not in st.session_state:
            st.session_state[f"fecha_input_{i}"] = fecha_op

        f_val = st.date_input(
            "", 
            key=f"fecha_input_{i}", 
            disabled=op_bloqueada, 
            label_visibility="collapsed",
            on_change=actualizar_fecha_fila,
            args=(i, fecha_op)
        )
        
        if st.session_state.get(f"error_fecha_{i}", False):
            st.error(f"🚨 **ERROR DE FECHA EN {nombre_parcial}**")

    lote_auto = f_val.strftime("%d%m%y")
    vto_date = f_val + relativedelta(months=vida_util_meses)
    vto_str = vto_date.strftime("%d%m%y")
    es_vto_valido = (hoy <= vto_date <= max_vto)
    
    with col_l:
        if cliente == "ENA":
            lote_final = st.text_input("", key=f"lote_{i}", disabled=op_bloqueada, label_visibility="collapsed")
        else:
            lote_final = lote_auto
            st.text_input("", value=lote_auto, key=f"lote_dis_{i}_{lote_auto}", disabled=True, label_visibility="collapsed")
        
    with col_v:
        vto_label = f"{vto_str} 🟢" if es_vto_valido else f"{vto_str} 🔴"
        st.text_input("", value=vto_label, key=f"vto_dis_{i}_{vto_str}", disabled=True, label_visibility="collapsed")
        
    with col_m:
        mermas_c = st.number_input("", min_value=0.0, step=0.1, format="%.1f", key=f"mermas_{i}", disabled=op_bloqueada, label_visibility="collapsed")

    with col_s:
        scrap_p = st.number_input("", min_value=0.0, step=0.1, format="%.1f", key=f"scrap_{i}", disabled=op_bloqueada, label_visibility="collapsed")

    with col_c:
        cant = st.number_input("", min_value=0, step=1000, key=f"cant_{i}", disabled=op_bloqueada, label_visibility="collapsed")
        tot_producido += cant

    parciales_cargados.append({
        "Parcial": nombre_parcial,
        "Turno": turno,
        "Responsable": responsable,
        "Fecha_Parcial": f_val.strftime("%d/%m/%Y"),
        "Lote": lote_final,
        "VTO": vto_str,
        "Mermas_C": mermas_c,
        "Scrap_P": scrap_p,
        "Cantidad": cant
    })

# --- MOSTRAR RECUADRO DE ETIQUETA E IMPRESIÓN ---
if mostrar_etiqueta:
    ultimos_validos = [p for p in parciales_cargados if p["Turno"] != ""]
    
    if ultimos_validos:
        ultimo_p = ultimos_validos[-1]
        
        st.markdown("---")
        st.subheader("🖨️ Recuadro de Rotulado / Etiqueta de Impresión")
        
        # CSS de impresión: oculta el resto de la aplicación y solo imprime el div #seccion-impresion
        st.markdown(
            """
            <style>
            @media print {
                body * {
                    visibility: hidden !important;
                }
                #seccion-impresion, #seccion-impresion * {
                    visibility: visible !important;
                }
                #seccion-impresion {
                    position: absolute !important;
                    left: 0 !important;
                    top: 0 !important;
                    width: 100% !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }
                .btn-imprimir {
                    display: none !important;
                }
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div id="seccion-impresion">
                <button class="btn-imprimir" onclick="window.print()" style="
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 5px;
                    cursor: pointer;
                    margin-bottom: 15px;
                    display: block;
                ">
                    🖨️ IMPRIMIR ETIQUETA
                </button>
                <div style="
                    border: 3px solid #1f77b4;
                    border-radius: 10px;
                    padding: 20px;
                    background-color: #ffffff;
                    color: #111111;
                    width: 100%;
                    max-width: 480px;
                    font-family: Arial, sans-serif;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                ">
                    <h3 style="margin-top:0; color:#1f77b4; text-align:center; border-bottom: 2px solid #1f77b4; padding-bottom: 5px;">
                        ETIQUETA DE PRODUCCIÓN ({ultimo_p['Parcial']})
                    </h3>
                    <p style="font-size: 16px; margin: 8px 0;"><b>CLIENTE:</b> {cliente}</p>
                    <p style="font-size: 16px; margin: 8px 0;"><b>PRODUCTO:</b> {producto}</p>
                    <p style="font-size: 20px; margin: 12px 0; color: #d9534f;"><b>LOTE:</b> {ultimo_p['Lote'] if ultimo_p['Lote'] else 'SIN LOTE'}</p>
                    <p style="font-size: 20px; margin: 12px 0; color: #28a745;"><b>VTO:</b> {ultimo_p['VTO']}</p>
                    <hr style="border: 0.5px solid #ccc;">
                    <p style="font-size: 12px; color: #555; text-align: right; margin-bottom:0;">
                        Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')} | Turno: {ultimo_p['Turno']}
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ No hay ningún parcial cargado con la celda 'Turno' completa para generar la etiqueta.")

# --- RESUMEN Y TOTALES ---
st.markdown("---")
col_res1, col_res2, col_cerrar = st.columns([1.5, 1.5, 1.5])
restan = cant_total - tot_producido

with col_res1:
    st.metric(label="Total Producido", value=f"{tot_producido:,}".replace(",", "."))

with col_res2:
    st.metric(label="Restan", value=f"{restan:,}".replace(",", "."), delta=-restan, delta_color="inverse" if restan > 0 else "normal")

with col_cerrar:
    st.write("")
    st.write("")
    if st.button("🔒 Cerrar y Guardar OP", type="primary", disabled=op_bloqueada):
        if num_op == "":
            st.warning("⚠️ Ingresa un N° de OP válido antes de cerrar.")
        else:
            datos_encabezado = {
                "OP_Num": num_op,
                "Fecha_OP": fecha_op.strftime("%d/%m/%Y"),
                "Cliente": cliente,
                "Producto": producto,
                "Cant_Total_OP": cant_total,
                "Total_Producido": tot_producido,
                "Saldo_Restante": restan,
                "Fecha_Cierre": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            exito = guardar_op_en_sheets(datos_encabezado, parciales_cargados)
            if exito:
                st.session_state["necesita_limpieza"] = True
                st.success(f"✅ ¡OP N° {num_op} registrada en Google Sheets correctamente!")
                st.rerun()
            else:
                st.error("❌ Ocurrió un error al guardar en Google Sheets. Verifique la conexión.")

# --- HISTORIAL DESDE GOOGLE SHEETS ---
st.markdown("---")
st.subheader("📚 Historial de OPs Cerradas (Google Sheets)")
df_historial = cargar_historial()

if not df_historial.empty:
    st.dataframe(df_historial, use_container_width=True)
else:
    st.info("No hay órdenes de producción cerradas aún en la nube.")
