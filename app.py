import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import json
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from streamlit_local_storage import LocalStorage

# Configuración de página
st.set_page_config(page_title="Control Golomaster V1", layout="wide")

# Instancia de almacenamiento local
localS = LocalStorage()

# --- BASE DE DATOS DEL MÓDULO PLANNING ---
RAW_DATA_PLANNING = [
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR BANANA", "BULTO": "SI", "UNIDADES": 192},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR AVELLANA", "BULTO": "SI", "UNIDADES": 192},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR MANI", "BULTO": "SI", "UNIDADES": 192},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR CACAO", "BULTO": "SI", "UNIDADES": 192},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR COCO", "BULTO": "SI", "UNIDADES": 192},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR BANANA AFA", "BULTO": "SI", "UNIDADES": 192},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR CACAO AFA", "BULTO": "SI", "UNIDADES": 192},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR BANANA CT", "BULTO": "SI", "UNIDADES": 128},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR BANANA CM", "BULTO": "SI", "UNIDADES": 64},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR BROWNIE CT", "BULTO": "SI", "UNIDADES": 128},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR BROWNIE CM", "BULTO": "SI", "UNIDADES": 64},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR FRUTILLA CT", "BULTO": "SI", "UNIDADES": 128},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR FRUTILLA CM", "BULTO": "SI", "UNIDADES": 64},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR COCO CT", "BULTO": "SI", "UNIDADES": 128},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR COCO CM", "BULTO": "SI", "UNIDADES": 64},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "DELUX", "PRODUCTO": "BARRA DE CHOCOLATE SABOR BANANA", "BULTO": "SI", "UNIDADES": 192},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "DELUX", "PRODUCTO": "BARRA DE CHOCOLATE SABOR CHOCOLATE", "BULTO": "SI", "UNIDADES": 192},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "DELUX", "PRODUCTO": "BARRA DE CHOCOLATE SABOR COCO", "BULTO": "SI", "UNIDADES": 192},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "DELUX", "PRODUCTO": "BARRA DE CHOCOLATE SABOR FRUTILLA", "BULTO": "SI", "UNIDADES": 192},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "DELUX", "PRODUCTO": "BARRA DE CHOCOLATE SABOR MANI", "BULTO": "SI", "UNIDADES": 192},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "DELUX", "PRODUCTO": "BARRA DE CHOCOLATE SABOR PISTACHO", "BULTO": "SI", "UNIDADES": 192},
    {"CATEGORIA": "GARRAPIÑADA MANI", "CLIENTE": "GOLOMASTER", "PRODUCTO": "GARRAPIÑADA DE MANI X 15", "BULTO": "NO", "UNIDADES": 0},
    {"CATEGORIA": "GARRAPIÑADA MANI", "CLIENTE": "EL 32", "PRODUCTO": "GARRAPIÑADA DE MANI X 5", "BULTO": "NO", "UNIDADES": 0},
    {"CATEGORIA": "GARRAPIÑADA ALMENDRA", "CLIENTE": "GOLOMASTER", "PRODUCTO": "GARRAPIÑADA DE ALMENDRA X 15", "BULTO": "NO", "UNIDADES": 0},
    {"CATEGORIA": "GARRAPIÑADA MANI", "CLIENTE": "GOLOMASTER", "PRODUCTO": "ENVASADO MANI GARRAPIÑADA 50U*80G", "BULTO": "SI", "UNIDADES": 50},
    {"CATEGORIA": "MANI CROCANTE", "CLIENTE": "ARGENFRUT", "PRODUCTO": "GARRAPIÑADA DE MANI X 15", "BULTO": "NO", "UNIDADES": 0},
    {"CATEGORIA": "ALMENDRAS + CH", "CLIENTE": "GOLOMASTER", "PRODUCTO": "ENGORDE - 1", "BULTO": "NO", "UNIDADES": 0},
    {"CATEGORIA": "ALMENDRAS + CH", "CLIENTE": "GOLOMASTER", "PRODUCTO": "CHOCOLATADO -2", "BULTO": "NO", "UNIDADES": 0},
    {"CATEGORIA": "ALMENDRAS + CH", "CLIENTE": "GOLOMASTER", "PRODUCTO": "ALISADO - 3", "BULTO": "NO", "UNIDADES": 0},
    {"CATEGORIA": "ALMENDRAS + CH", "CLIENTE": "GOLOMASTER", "PRODUCTO": "ABRILLANTADO - 4", "BULTO": "NO", "UNIDADES": 0},
    {"CATEGORIA": "ALMENDRAS + CH", "CLIENTE": "GOLOMASTER", "PRODUCTO": "ENVASADO DE ALMENDRA + CH 36U*80GR", "BULTO": "SI", "UNIDADES": 36},
    {"CATEGORIA": "ALMENDRAS + CH", "CLIENTE": "CHOCOMORA", "PRODUCTO": "ENVASADO DE ALMENDRA + CH 40U*80GR", "BULTO": "SI", "UNIDADES": 40}
]

df_planning_db = pd.DataFrame(RAW_DATA_PLANNING)

# --- CONEXIÓN A GOOGLE SHEETS / HISTORIAL ---
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbywDdFRA0GkivkkNk7uDXk6Q3hJkU47-lBZYnd_dz7D16kVF274AVgmXejyt2hF3Na_/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/17He8h4AfTjuMHLSTWOMAAMD960ow_-Gj-AvsI9XC_lc/export?format=csv"

def obtener_ahora_arg():
    return datetime.utcnow() - timedelta(hours=3)

def cargar_historial():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        return df
    except Exception:
        return pd.DataFrame()

def obtener_siguiente_op_sugerida():
    df = cargar_historial()
    ops_existentes = []
    
    if not df.empty and "OP_Num" in df.columns:
        for val in df["OP_Num"].dropna().unique():
            val_str = str(val).strip()
            if val_str.isdigit():
                ops_existentes.append(int(val_str))
                
    # Consultar también planes locales acumulados
    if "lista_planes" in st.session_state:
        for p in st.session_state["lista_planes"]:
            if str(p.get("OP_Num", "")).isdigit():
                ops_existentes.append(int(p["OP_Num"]))
                
    if ops_existentes:
        return str(max(ops_existentes) + 1)
    else:
        return "100"

# --- NAVEGACIÓN Y PESTAÑAS (SOLAPAS) ---
if "modulo_activo" not in st.session_state:
    st.session_state["modulo_activo"] = "Producción"

if "planning_autenticado" not in st.session_state:
    st.session_state["planning_autenticado"] = False

# Estilo para solapas pequeñas arriba a la izquierda
st.markdown(
    """
    <style>
    div[data-testid="column"] button[kind="secondary"], 
    div[data-testid="column"] button[kind="primary"] {
        padding: 4px 12px !important;
        font-size: 13px !important;
        height: auto !important;
        min-height: 0px !important;
        border-radius: 6px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col_nav1, col_nav2, col_nav3, _ = st.columns([1.2, 1.1, 1.1, 6.0])

with col_nav1:
    btn_prod_type = "primary" if st.session_state["modulo_activo"] == "Producción" else "secondary"
    if st.button("🏷️ Módulo Producción", type=btn_prod_type, use_container_width=True):
        st.session_state["modulo_activo"] = "Producción"
        st.rerun()

with col_nav2:
    btn_stock_type = "primary" if st.session_state["modulo_activo"] == "Stocks" else "secondary"
    if st.button("📦 Módulo Stocks", type=btn_stock_type, use_container_width=True):
        st.session_state["modulo_activo"] = "Stocks"
        st.rerun()

with col_nav3:
    btn_plan_type = "primary" if st.session_state["modulo_activo"] == "Planning" else "secondary"
    if st.button("📅 Módulo Planning", type=btn_plan_type, use_container_width=True):
        st.session_state["modulo_activo"] = "Planning"
        st.rerun()

st.markdown("---")

# ==========================================
# 1. MÓDULO PRODUCCIÓN
# ==========================================
if st.session_state["modulo_activo"] == "Producción":
    st.title("📋 Control de órdenes de producción Golomaster V1")

    fecha_actual_hoy = obtener_ahora_arg().date()

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
                "Mermas_C": 0.000,
                "Scrap_P": 0.000,
                "Cantidad": 0
            })
            
        try:
            response = requests.post(WEBAPP_URL, json=registros)
            return response.status_code == 200
        except Exception:
            return False

    def solicitar_limpieza():
        st.session_state["necesita_limpieza"] = True
        try:
            localS.deleteItem("borrador_golomaster")
        except Exception:
            pass

    CLIENTES_VIDA_UTIL = {
        "": 0,
        "INTEGRA": 7,
        "ENA": 12,
        "DELUXE": 12,
        "GARRAPIÑADA": 8
    }

    PRODUCTOS_POR_CLIENTE = {
        "": [""],
        "INTEGRA": [
            "",
            "BARRAS DE CACAO SABOR MANI",
            "BARRAS DE CACAO SABOR AVELLANA",
            "BARRAS DE CACAO SABOR COCO",
            "BARRAS DE CACAO CON CHOCOLATE",
            "BARRAS DE CACAO SABOR BANANA"
        ],
        "ENA": [
            "",
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
            "",
            "PRODUCTO DELUXE GENERAL"
        ],
        "GARRAPIÑADA": [
            "",
            "GARRAPIÑADA GENERAL"
        ]
    }

    LISTA_RESPONSABLES = ["", "Carlos", "Victor", "Guille", "Lujan", "Sebastian"]

    if "borrador_cargado" not in st.session_state:
        borrador = localS.getItem("borrador_golomaster")
        if borrador:
            try:
                datos_recuperados = json.loads(borrador) if isinstance(borrador, str) else borrador
                for k, v in datos_recuperados.items():
                    if k == "fecha_op":
                        continue
                    elif "fecha" in k and isinstance(v, str):
                        try:
                            st.session_state[k] = datetime.strptime(v, "%Y-%m-%d").date()
                        except Exception:
                            st.session_state[k] = v
                    else:
                        st.session_state[k] = v
                st.toast("🛡️ **Borrador de seguridad recuperado.**", icon="💾")
            except Exception:
                pass
        st.session_state["borrador_cargado"] = True

    if st.session_state.get("necesita_limpieza", False):
        st.session_state["num_op"] = ""
        st.session_state["cliente_select"] = ""
        st.session_state["producto_select"] = ""
        st.session_state["cant_total"] = 0
        st.session_state["fecha_op"] = fecha_actual_hoy
        
        for i in range(10):
            st.session_state[f"turno_{i}"] = ""
            st.session_state[f"resp_{i}"] = ""
            st.session_state[f"fecha_input_{i}"] = fecha_actual_hoy
            st.session_state[f"lote_{i}"] = ""
            st.session_state[f"mermas_{i}"] = 0.000
            st.session_state[f"scrap_{i}"] = 0.000
            st.session_state[f"cant_{i}"] = 0
        st.session_state["necesita_limpieza"] = False

    col1, col2, col3 = st.columns(3)

    with col1:
        fecha_op = st.date_input("FECHA DE LA OP", value=fecha_actual_hoy, key="fecha_op")
        num_op = st.text_input("OP N°", value=st.session_state.get("num_op", ""), key="num_op").strip()
        cant_total = st.number_input("Cantidad Total a Producir", value=st.session_state.get("cant_total", 0), step=1000, key="cant_total")

    lista_clientes = list(CLIENTES_VIDA_UTIL.keys())
    cliente_guardado = st.session_state.get("cliente_select", "")
    idx_cliente = lista_clientes.index(cliente_guardado) if cliente_guardado in lista_clientes else 0

    with col2:
        cliente = st.selectbox("CLIENTE", lista_clientes, index=idx_cliente, key="cliente_select")
        lista_productos = PRODUCTOS_POR_CLIENTE.get(cliente, [""])
        
        prod_guardado = st.session_state.get("producto_select", "")
        idx_prod = lista_productos.index(prod_guardado) if prod_guardado in lista_productos else 0
        producto = st.selectbox("PRODUCTO", lista_productos, index=idx_prod, key="producto_select")

    vida_util_meses = CLIENTES_VIDA_UTIL.get(cliente, 0)

    with col3:
        if cliente != "":
            st.info(f"**Vida Útil para {cliente}:** {vida_util_meses} meses")
        else:
            st.info("Seleccione un cliente para ver su vida útil.")

    op_bloqueada = False
    if num_op != "":
        if op_existe(num_op):
            st.error(f"⛔ LA OP N° '{num_op}' YA FUE CERRADA ANTERIORMENTE. NO SE PUEDE REUTILIZAR ESTE NÚMERO.")
            op_bloqueada = True

    encabezado_completo = (num_op != "") and (cliente != "") and (producto != "") and (cant_total > 0)

    st.markdown("---")

    col_btn1, col_btn2, _ = st.columns([1.5, 2.0, 3.0])

    with col_btn1:
        st.button("🧹 Limpiar Formulario", on_click=solicitar_limpieza, type="secondary")

    with col_btn2:
        mostrar_etiqueta = st.button("🏷️ Generar Etiqueta ÚLTIMO Parcial", type="secondary", disabled=not encabezado_completo or op_bloqueada)

    def actualizar_fecha_fila(indice, fecha_base_op):
        f_ingresada = st.session_state[f"fecha_input_{indice}"]
        if f_ingresada < fecha_base_op:
            st.session_state[f"error_fecha_{indice}"] = True
            st.session_state[f"fecha_input_{indice}"] = fecha_base_op
        else:
            st.session_state[f"error_fecha_{indice}"] = False

    st.subheader("📦 Registro de Parciales")

    if not encabezado_completo:
        st.warning("⚠️ Para comenzar a cargar parciales, primero debe completar el N° de OP, Cliente, Producto y Cantidad Total (> 0).")

    filas_deshabilitadas = (not encabezado_completo) or op_bloqueada

    hoy = fecha_actual_hoy
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
            turno = st.selectbox("", ["", "M", "T", "N"], key=f"turno_{i}", disabled=filas_deshabilitadas, label_visibility="collapsed")
            
        with col_r:
            responsable = st.selectbox("", LISTA_RESPONSABLES, key=f"resp_{i}", disabled=filas_deshabilitadas, label_visibility="collapsed")
            
        with col_f:
            if f"fecha_input_{i}" not in st.session_state:
                st.session_state[f"fecha_input_{i}"] = fecha_op

            f_val = st.date_input(
                "", 
                key=f"fecha_input_{i}", 
                disabled=filas_deshabilitadas, 
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
                lote_final = st.text_input("", key=f"lote_{i}", disabled=filas_deshabilitadas, label_visibility="collapsed")
            else:
                lote_final = lote_auto
                st.text_input("", value=lote_auto, key=f"lote_dis_{i}_{lote_auto}", disabled=True, label_visibility="collapsed")
            
        with col_v:
            vto_label = f"{vto_str} 🟢" if es_vto_valido else f"{vto_str} 🔴"
            st.text_input("", value=vto_label, key=f"vto_dis_{i}_{vto_str}", disabled=True, label_visibility="collapsed")
            
        with col_m:
            mermas_c = st.number_input("", min_value=0.0, step=0.001, format="%.3f", key=f"mermas_{i}", disabled=filas_deshabilitadas, label_visibility="collapsed")

        with col_s:
            scrap_p = st.number_input("", min_value=0.0, step=0.001, format="%.3f", key=f"scrap_{i}", disabled=filas_deshabilitadas, label_visibility="collapsed")

        with col_c:
            cant = st.number_input("", min_value=0, step=1000, key=f"cant_{i}", disabled=filas_deshabilitadas, label_visibility="collapsed")
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

    datos_borrador = {
        "num_op": num_op,
        "cant_total": cant_total,
        "cliente_select": cliente,
        "producto_select": producto
    }

    for i in range(10):
        datos_borrador[f"turno_{i}"] = st.session_state.get(f"turno_{i}", "")
        datos_borrador[f"resp_{i}"] = st.session_state.get(f"resp_{i}", "")
        datos_borrador[f"lote_{i}"] = st.session_state.get(f"lote_{i}", "")
        datos_borrador[f"mermas_{i}"] = st.session_state.get(f"mermas_{i}", 0.000)
        datos_borrador[f"scrap_{i}"] = st.session_state.get(f"scrap_{i}", 0.000)
        datos_borrador[f"cant_{i}"] = st.session_state.get(f"cant_{i}", 0)
        
        f_input = st.session_state.get(f"fecha_input_{i}", fecha_op)
        datos_borrador[f"fecha_input_{i}"] = f_input.isoformat() if isinstance(f_input, date) else str(f_input)

    try:
        localS.setItem("borrador_golomaster", json.dumps(datos_borrador))
    except Exception:
        pass

    if mostrar_etiqueta:
        ultimos_validos = [p for p in parciales_cargados if p["Turno"] != ""]
        
        if ultimos_validos:
            ultimo_p = ultimos_validos[-1]
            
            hora_arg = obtener_ahora_arg().strftime('%d/%m/%Y %H:%M')
            texto_op = f"OP: {num_op}" if num_op else "OP: N/A"

            html_impresion = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 10px;
                        background-color: #ffffff;
                    }}
                    .etiqueta {{
                        border: 3px solid #1f77b4;
                        border-radius: 10px;
                        padding: 20px;
                        width: 420px;
                        background-color: #ffffff;
                        color: #111111;
                        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
                    }}
                    .titulo {{
                        margin-top: 0;
                        color: #1f77b4;
                        text-align: center;
                        border-bottom: 2px solid #1f77b4;
                        padding-bottom: 5px;
                        font-size: 18px;
                    }}
                    p {{
                        margin: 8px 0;
                    }}
                    .lote {{
                        font-size: 20px;
                        color: #d9534f;
                    }}
                    .vto {{
                        font-size: 20px;
                        color: #28a745;
                    }}
                    .pie-container {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-top: 15px;
                        font-size: 11px;
                        color: #555555;
                    }}
                    .op-num {{
                        font-size: 12px;
                        font-weight: bold;
                        color: #333333;
                    }}
                    .btn-reimprimir {{
                        background-color: #28a745;
                        color: white;
                        border: none;
                        padding: 8px 15px;
                        font-size: 14px;
                        font-weight: bold;
                        border-radius: 5px;
                        cursor: pointer;
                        margin-bottom: 10px;
                    }}
                    @media print {{
                        .btn-reimprimir {{
                            display: none !important;
                        }}
                    }}
                </style>
            </head>
            <body>
                <button class="btn-reimprimir" onclick="window.print()">🖨️ Re-abrir Impresión</button>
                <div class="etiqueta">
                    <h3 class="titulo">ETIQUETA DE PRODUCCIÓN ({ultimo_p['Parcial']})</h3>
                    <p><b>CLIENTE:</b> {cliente}</p>
                    <p><b>PRODUCTO:</b> {producto}</p>
                    <p class="lote"><b>LOTE:</b> {ultimo_p['Lote'] if ultimo_p['Lote'] else 'SIN LOTE'}</p>
                    <p class="vto"><b>VTO:</b> {ultimo_p['VTO']}</p>
                    <hr style="border: 0.5px solid #ccc;">
                    <div class="pie-container">
                        <span class="op-num">{texto_op}</span>
                        <span>Generado: {hora_arg} | Turno: {ultimo_p['Turno']}</span>
                    </div>
                </div>
                <script>
                    window.onload = function() {{
                        window.print();
                    }};
                </script>
            </body>
            </html>
            """
            components.html(html_impresion, height=350)
        else:
            st.warning("⚠️ No hay ningún parcial cargado con la celda 'Turno' completa para generar la etiqueta.")

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
        if st.button("🔒 Cerrar y Guardar OP", type="primary", disabled=not encabezado_completo or op_bloqueada):
            fecha_cierre_arg = obtener_ahora_arg().strftime("%d/%m/%Y %H:%M")
            datos_encabezado = {
                "OP_Num": num_op,
                "Fecha_OP": fecha_op.strftime("%d/%m/%Y"),
                "Cliente": cliente,
                "Producto": producto,
                "Cant_Total_OP": cant_total,
                "Total_Producido": tot_producido,
                "Saldo_Restante": restan,
                "Fecha_Cierre": fecha_cierre_arg
            }
            exito = guardar_op_en_sheets(datos_encabezado, parciales_cargados)
            if exito:
                solicitar_limpieza()
                st.success(f"✅ ¡OP N° {num_op} registrada en Google Sheets correctamente!")
                st.rerun()
            else:
                st.error("❌ Ocurrió un error al guardar en Google Sheets. Verifique la conexión.")

    st.markdown("---")
    st.subheader("📚 Historial de OPs Cerradas (Google Sheets)")
    df_historial = cargar_historial()

    if not df_historial.empty:
        st.dataframe(df_historial, use_container_width=True)
    else:
        st.info("No hay órdenes de producción cerradas aún en la nube.")

# ==========================================
# 2. MÓDULO STOCKS
# ==========================================
elif st.session_state["modulo_activo"] == "Stocks":
    st.title("📦 Módulo Stocks")
    st.info("🛠️ Módulo en desarrollo. Esta sección se encuentra lista para integrar la gestión de inventario, ubicaciones y materias primas.")

# ==========================================
# 3. MÓDULO PLANNING (CON CONTRASEÑA)
# ==========================================
elif st.session_state["modulo_activo"] == "Planning":
    st.title("📅 Módulo Planning - Planificación de Producción")

    # Control de Autenticación por Contraseña
    if not st.session_state["planning_autenticado"]:
        st.subheader("🔒 Acceso Restringido")
        col_pass1, col_pass2 = st.columns([2.0, 3.0])
        with col_pass1:
            clave_ingresada = st.text_input("Ingrese la contraseña de acceso:", type="password", key="pwd_planning")
            if st.button("🔑 Ingresar al Módulo Planning", type="primary"):
                if clave_ingresada == "golomaster":
                    st.session_state["planning_autenticado"] = True
                    st.success("🔓 Acceso concedido.")
                    st.rerun()
                else:
                    st.error("❌ Contraseña incorrecta. Intente nuevamente.")
    else:
        # Pestaña autenticada
        if "lista_planes" not in st.session_state:
            st.session_state["lista_planes"] = []

        fecha_plan_default = obtener_ahora_arg().date() + timedelta(days=1)
        sug_op = obtener_siguiente_op_sugerida()

        st.subheader("📋 Configuración del Plan de Producción")
        
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            fecha_plan = st.date_input("Fecha a Planificar", value=fecha_plan_default, key="fecha_plan")
            op_plan = st.text_input("OP N° (Sugerida automática)", value=sug_op, key="op_plan").strip()

        with col_c2:
            turno_plan = st.selectbox("Turno de Trabajo", ["M", "T", "N"], key="turno_plan")

        st.markdown("---")
        st.markdown("### 🔍 Selección de Producto a Planificar")

        # 1. Categoría
        categorias_disponibles = [""] + sorted(df_planning_db["CATEGORIA"].unique().tolist())
        cat_sel = st.selectbox("1. CATEGORÍA", categorias_disponibles, key="plan_cat_select")

        # 2. Cliente (Filtra según Categoría seleccionada)
        if cat_sel != "":
            df_cat = df_planning_db[df_planning_db["CATEGORIA"] == cat_sel]
            clientes_disponibles = [""] + sorted(df_cat["CLIENTE"].unique().tolist())
        else:
            clientes_disponibles = [""]

        cli_sel = st.selectbox("2. CLIENTE", clientes_disponibles, key="plan_cli_select")

        # 3. Producto (Filtra según Categoría y Cliente)
        if cat_sel != "" and cli_sel != "":
            df_prod = df_planning_db[(df_planning_db["CATEGORIA"] == cat_sel) & (df_planning_db["CLIENTE"] == cli_sel)]
            productos_disponibles = [""] + sorted(df_prod["PRODUCTO"].unique().tolist())
        else:
            productos_disponibles = [""]

        prod_sel = st.selectbox("3. PRODUCTO", productos_disponibles, key="plan_prod_select")

        st.markdown("---")

        # Detalle y Cuarta Celda (Cantidad en Unidades / Conversión)
        if cat_sel != "" and cli_sel != "" and prod_sel != "":
            fila_item = df_planning_db[
                (df_planning_db["CATEGORIA"] == cat_sel) & 
                (df_planning_db["CLIENTE"] == cli_sel) & 
                (df_planning_db["PRODUCTO"] == prod_sel)
            ].iloc[0]

            es_bulto = fila_item["BULTO"] == "SI"
            unidades_por_bulto = int(fila_item["UNIDADES"]) if es_bulto else 0

            col_p1, col_p2, col_p3 = st.columns([1.5, 1.5, 2.0])

            with col_p1:
                st.write(f"**Categoría:** {cat_sel}")
                st.write(f"**Cliente:** {cli_sel}")
                st.write(f"**Producto:** {prod_sel}")

            with col_p2:
                st.write(f"**Aplica Bulto:** {fila_item['BULTO']}")
                if es_bulto:
                    st.write(f"**Unidades por Bulto / Caja:** {unidades_por_bulto}")
                else:
                    st.write("**Unidad de Medida:** KG")

            with col_p3:
                if es_bulto:
                    cant_unidades_ingresadas = st.number_input(
                        "4. CANTIDAD DE BARRAS / UNIDADES A PRODUCIR", 
                        min_value=0, 
                        step=100, 
                        value=0, 
                        key="cant_unid_plan"
                    )
                    cajas_calculadas = (cant_unidades_ingresadas / unidades_por_bulto) if unidades_por_bulto > 0 else 0.0
                    st.metric(label="EQUIVALENTE EN CAJAS / BULTOS", value=f"{cajas_calculadas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                    total_resumen = f"{cajas_calculadas:,.2f} Cajas ({cant_unidades_ingresadas:,} U)"
                else:
                    cant_kg_ingresados = st.number_input(
                        "4. CANTIDAD A PRODUCIR EN KILOGRAMOS (KG)", 
                        min_value=0.000, 
                        step=0.100, 
                        format="%.3f", 
                        value=0.000, 
                        key="cant_kg_plan"
                    )
                    st.metric(label="TOTAL KILOGRAMOS (KG)", value=f"{cant_kg_ingresados:.3f} KG")
                    total_resumen = f"{cant_kg_ingresados:.3f} KG"

            st.markdown("---")
            if st.button("➕ Agregar a Plan de Producción", type="primary"):
                if op_plan == "":
                    st.warning("⚠️ Debe especificar un N° de OP.")
                else:
                    nuevo_plan = {
                        "Fecha_Plan": fecha_plan.strftime("%d/%m/%Y"),
                        "OP_Num": op_plan,
                        "Turno": turno_plan,
                        "Cliente": cli_sel,
                        "Producto": prod_sel,
                        "Detalle_Cantidad": total_resumen
                    }
                    st.session_state["lista_planes"].append(nuevo_plan)
                    st.success(f"✅ ¡Plan para la OP N° {op_plan} agregado exitosamente!")
                    st.rerun()

        else:
            st.info("👈 Seleccione Categoría, Cliente y Producto para habilitar la carga de cantidades.")

        # Tabla de Cronograma Acumulado
        st.markdown("---")
        st.subheader("📊 Cronograma de Planificaciones Cargadas")
        
        if st.session_state["lista_planes"]:
            df_planes_vista = pd.DataFrame(st.session_state["lista_planes"])
            st.dataframe(df_planes_vista, use_container_width=True)
            
            if st.button("🧹 Limpiar Tabla de Planificación"):
                st.session_state["lista_planes"] = []
                st.rerun()
        else:
            st.info("No hay ítems planificados en el cronograma actual.")
