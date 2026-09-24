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

# ==============================================================================
# --- BASE DE DATOS MAESTRA ---
# ==============================================================================
RAW_DATA_MAESTRA = [
    # BARRITAS - INTEGRA
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR BANANA", "BULTO": "SI", "UNIDADES": 192, "VIDA_UTIL": 7},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR AVELLANA", "BULTO": "SI", "UNIDADES": 192, "VIDA_UTIL": 7},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR MANI", "BULTO": "SI", "UNIDADES": 192, "VIDA_UTIL": 7},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR CACAO", "BULTO": "SI", "UNIDADES": 192, "VIDA_UTIL": 7},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR COCO", "BULTO": "SI", "UNIDADES": 192, "VIDA_UTIL": 7},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR BANANA AFA", "BULTO": "SI", "UNIDADES": 192, "VIDA_UTIL": 7},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "INTEGRA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR CACAO AFA", "BULTO": "SI", "UNIDADES": 192, "VIDA_UTIL": 7},
    
    # BARRITAS - ENA
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR BANANA CT", "BULTO": "SI", "UNIDADES": 128, "VIDA_UTIL": 12},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE GARRA PIÑADA BANANA CM", "BULTO": "SI", "UNIDADES": 64, "VIDA_UTIL": 12},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR BROWNIE CT", "BULTO": "SI", "UNIDADES": 128, "VIDA_UTIL": 12},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR BROWNIE CM", "BULTO": "SI", "UNIDADES": 64, "VIDA_UTIL": 12},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR FRUTILLA CT", "BULTO": "SI", "UNIDADES": 128, "VIDA_UTIL": 12},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR FRUTILLA CM", "BULTO": "SI", "UNIDADES": 64, "VIDA_UTIL": 12},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR COCO CT", "BULTO": "SI", "UNIDADES": 128, "VIDA_UTIL": 12},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "ENA", "PRODUCTO": "BARRA DE CHOCOLATE SABOR COCO CM", "BULTO": "SI", "UNIDADES": 64, "VIDA_UTIL": 12},
    
    # BARRITAS - DELUX
    {"CATEGORIA": "BARRITAS", "CLIENTE": "DELUX", "PRODUCTO": "BARRA DE CHOCOLATE SABOR BANANA", "BULTO": "SI", "UNIDADES": 192, "VIDA_UTIL": 12},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "DELUX", "PRODUCTO": "BARRA DE CHOCOLATE SABOR CHOCOLATE", "BULTO": "SI", "UNIDADES": 192, "VIDA_UTIL": 12},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "DELUX", "PRODUCTO": "BARRA DE CHOCOLATE SABOR COCO", "BULTO": "SI", "UNIDADES": 192, "VIDA_UTIL": 12},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "DELUX", "PRODUCTO": "BARRA DE CHOCOLATE SABOR FRUTILLA", "BULTO": "SI", "UNIDADES": 192, "VIDA_UTIL": 12},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "DELUX", "PRODUCTO": "BARRA DE CHOCOLATE SABOR MANI", "BULTO": "SI", "UNIDADES": 192, "VIDA_UTIL": 12},
    {"CATEGORIA": "BARRITAS", "CLIENTE": "DELUX", "PRODUCTO": "BARRA DE CHOCOLATE SABOR PISTACHO", "BULTO": "SI", "UNIDADES": 192, "VIDA_UTIL": 12},
    
    # GARRAPIÑADAS & MANI CROCANTE
    {"CATEGORIA": "GARRAPIÑADA MANI", "CLIENTE": "GOLOMASTER", "PRODUCTO": "GARRAPIÑADA DE MANI X 15", "BULTO": "NO", "UNIDADES": 0, "VIDA_UTIL": 8},
    {"CATEGORIA": "GARRAPIÑADA MANI", "CLIENTE": "EL 32", "PRODUCTO": "GARRAPIÑADA DE MANI X 5", "BULTO": "NO", "UNIDADES": 0, "VIDA_UTIL": 8},
    {"CATEGORIA": "GARRAPIÑADA ALMENDRA", "CLIENTE": "GOLOMASTER", "PRODUCTO": "GARRAPIÑADA DE ALMENDRA X 15", "BULTO": "NO", "UNIDADES": 0, "VIDA_UTIL": 8},
    {"CATEGORIA": "GARRAPIÑADA MANI", "CLIENTE": "GOLOMASTER", "PRODUCTO": "ENVASADO MANI GARRAPIÑADA 50U*80G", "BULTO": "SI", "UNIDADES": 50, "VIDA_UTIL": 8},
    {"CATEGORIA": "MANI CROCANTE", "CLIENTE": "ARGENFRUT", "PRODUCTO": "GARRAPIÑADA DE MANI X 15", "BULTO": "NO", "UNIDADES": 0, "VIDA_UTIL": 8},
    
    # ALMENDRAS + CH
    {"CATEGORIA": "ALMENDRAS + CH", "CLIENTE": "GOLOMASTER", "PRODUCTO": "ENGORDE - 1", "BULTO": "NO", "UNIDADES": 0, "VIDA_UTIL": 0},
    {"CATEGORIA": "ALMENDRAS + CH", "CLIENTE": "GOLOMASTER", "PRODUCTO": "CHOCOLATADO -2", "BULTO": "NO", "UNIDADES": 0, "VIDA_UTIL": 0},
    {"CATEGORIA": "ALMENDRAS + CH", "CLIENTE": "GOLOMASTER", "PRODUCTO": "ALISADO - 3", "BULTO": "NO", "UNIDADES": 0, "VIDA_UTIL": 0},
    {"CATEGORIA": "ALMENDRAS + CH", "CLIENTE": "GOLOMASTER", "PRODUCTO": "ABRILLANTADO - 4", "BULTO": "NO", "UNIDADES": 0, "VIDA_UTIL": 0},
    {"CATEGORIA": "ALMENDRAS + CH", "CLIENTE": "GOLOMASTER", "PRODUCTO": "ENVASADO DE ALMENDRA + CH 36U*80GR", "BULTO": "SI", "UNIDADES": 36, "VIDA_UTIL": 8},
    {"CATEGORIA": "ALMENDRAS + CH", "CLIENTE": "CHOCOMORA", "PRODUCTO": "ENVASADO DE ALMENDRA + CH 40U*80GR", "BULTO": "SI", "UNIDADES": 40, "VIDA_UTIL": 8}
]

df_maestro = pd.DataFrame(RAW_DATA_MAESTRA)

# --- CONEXIÓN A GOOGLE SHEETS ---
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbywDdFRA0GkivkkNk7uDXk6Q3hJkU47-lBZYnd_dz7D16kVF274AVgmXejyt2hF3Na_/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/17He8h4AfTjuMHLSTWOMAAMD960ow_-Gj-AvsI9XC_lc/export?format=csv"
SHEET_PLANNING_CSV_URL = "https://docs.google.com/spreadsheets/d/17He8h4AfTjuMHLSTWOMAAMD960ow_-Gj-AvsI9XC_lc/gviz/tq?tqx=out:csv&sheet=BD%20PLANNING"

def obtener_ahora_arg():
    return datetime.utcnow() - timedelta(hours=3)

def cargar_historial():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        return df
    except Exception:
        return pd.DataFrame()

def cargar_historial_planning():
    try:
        df = pd.read_csv(SHEET_PLANNING_CSV_URL)
        return df
    except Exception:
        return pd.DataFrame()

# ==============================================================================
# --- FUNCIONES DE GUARDADO RESTRUCTURADAS ---
# ==============================================================================
def guardar_op_en_sheets(datos_op, filas_parciales):
    """Envía la información formateada para la pestaña BD PRODU (A -> Q)"""
    registros = []
    parciales_validos = [f for f in filas_parciales if f.get("Cantidad", 0) > 0 or f.get("Turno", "") != "" or f.get("Responsable", "") != ""]

    if not parciales_validos:
        registro_unico = {
            "OP_Num": datos_op.get("OP_Num", ""),
            "Fecha_OP": str(datos_op.get("Fecha_OP", "")),
            "Cliente": datos_op.get("Cliente", ""),
            "Producto": datos_op.get("Producto", ""),
            "Cant_Total_OP": datos_op.get("Cant_Total_OP", 0),
            "Parcial": "Sin cargas",
            "Turno": "",
            "Responsable": "",
            "Fecha_Parcial": "",
            "Lote": "",
            "VTO": "",
            "Mermas_C": 0.0,
            "Scrap_P": 0.0,
            "Cantidad": 0,
            "Total_Producido": datos_op.get("Total_Producido", 0),
            "Saldo_Restante": datos_op.get("Saldo_Restante", 0),
            "Fecha_Cierre": str(datos_op.get("Fecha_Cierre", ""))
        }
        registros.append(registro_unico)
    else:
        for f in parciales_validos:
            registro = {
                "OP_Num": datos_op.get("OP_Num", ""),
                "Fecha_OP": str(datos_op.get("Fecha_OP", "")),
                "Cliente": datos_op.get("Cliente", ""),
                "Producto": datos_op.get("Producto", ""),
                "Cant_Total_OP": datos_op.get("Cant_Total_OP", 0),
                "Parcial": f.get("Parcial", ""),
                "Turno": f.get("Turno", ""),
                "Responsable": f.get("Responsable", ""),
                "Fecha_Parcial": str(f.get("Fecha_Parcial", "")),
                "Lote": f.get("Lote", ""),
                "VTO": str(f.get("VTO", "")),
                "Mermas_C": f.get("Mermas_C", 0.0),
                "Scrap_P": f.get("Scrap_P", 0.0),
                "Cantidad": f.get("Cantidad", 0),
                "Total_Producido": datos_op.get("Total_Producido", 0),
                "Saldo_Restante": datos_op.get("Saldo_Restante", 0),
                "Fecha_Cierre": str(datos_op.get("Fecha_Cierre", ""))
            }
            registros.append(registro)

    payload = {
        "hoja": "BD PRODU",
        "registros": registros
    }

    try:
        response = requests.post(WEBAPP_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"}, allow_redirects=True)
        return response.status_code in [200, 302] and "Error" not in response.text
    except Exception:
        return False

def guardar_planning_en_sheets(datos_planning):
    """Envía la información formateada para la pestaña BD PLANNING (A -> H)"""
    registro = {
        "Fecha_Plan": str(datos_planning.get("Fecha_Plan", "")),
        "OP_Num": datos_planning.get("OP_Num", ""),
        "Turno": datos_planning.get("Turno", ""),
        "Categoria": datos_planning.get("Categoria", ""),
        "Cliente": datos_planning.get("Cliente", ""),
        "Producto": datos_planning.get("Producto", ""),
        "Detalle_Cantidad": datos_planning.get("Detalle_Cantidad", 0),
        "Fecha_Carga": str(datos_planning.get("Fecha_Carga", ""))
    }

    payload = {
        "hoja": "BD PLANNING",
        "registros": [registro]
    }

    try:
        response = requests.post(WEBAPP_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"}, allow_redirects=True)
        return response.status_code in [200, 302] and "Error" not in response.text
    except Exception:
        return False

# --- FUNCIONES DE AUXILIO E INTERFAZ ---
def obtener_todas_las_ops_existentes():
    ops = set()
    df_prod = cargar_historial()
    if not df_prod.empty and "OP_Num" in df_prod.columns:
        for val in df_prod["OP_Num"].dropna().unique():
            ops.add(str(val).strip())
            
    df_plan = cargar_historial_planning()
    if not df_plan.empty and "OP_Num" in df_plan.columns:
        for val in df_plan["OP_Num"].dropna().unique():
            ops.add(str(val).strip())
            
    if "lista_planes" in st.session_state:
        for p in st.session_state["lista_planes"]:
            ops.add(str(p.get("OP_Num", "")).strip())
            
    return ops

def obtener_siguiente_op_sugerida():
    ops_existentes = obtener_todas_las_ops_existentes()
    numeros = []
    for op in ops_existentes:
        if op.isdigit():
            numeros.append(int(op))
            
    return str(max(numeros) + 1) if numeros else "100"

def estilar_celda_masas(val):
    if "Masas" in str(val):
        return 'color: #ffff00; font-weight: bold; background-color: #262626;'
    return ''

def renderizar_cronograma_semanal():
    dias_nombre = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO"]
    hoy = obtener_ahora_arg().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fechas_semana = [inicio_semana + timedelta(days=i) for i in range(6)]
    
    df_p = cargar_historial_planning()
    planes_consolidadosa = []
    
    if not df_p.empty:
        for _, r in df_p.iterrows():
            planes_consolidadosa.append({
                "Fecha_Plan": str(r.get("Fecha_Plan", "")).strip(),
                "OP": str(r.get("OP_Num", "")).strip(),
                "TURNO": str(r.get("Turno", "")).strip(),
                "CLIENTE": str(r.get("Cliente", "")).strip(),
                "PRODUCTO": str(r.get("Producto", "")).strip(),
                "CANTIDAD": str(r.get("Detalle_Cantidad", "")).strip()
            })
            
    if "lista_planes" in st.session_state:
        for p in st.session_state["lista_planes"]:
            planes_consolidadosa.append({
                "Fecha_Plan": str(p.get("Fecha_Plan", "")).strip(),
                "OP": str(p.get("OP_Num", "")).strip(),
                "TURNO": str(p.get("Turno", "")).strip(),
                "CLIENTE": str(p.get("Cliente", "")).strip(),
                "PRODUCTO": str(p.get("Producto", "")).strip(),
                "CANTIDAD": str(p.get("Detalle_Cantidad", "")).strip()
            })

    st.markdown("##### 📅 CRONOGRAMA SEMANAL DE PLANIFICACIÓN")
    cols = st.columns(6)
    
    for idx, f_date in enumerate(fechas_semana):
        f_str = f_date.strftime("%d/%m/%Y")
        nom_dia = f"{dias_nombre[idx]} {f_date.strftime('%d/%m/%y')}"
        
        with cols[idx]:
            st.markdown(
                f"""
                <div style="background-color: #ffff00; color: #000000; font-weight: bold; text-align: center; padding: 6px; border: 1px solid #000; font-size: 13px; margin-bottom: 5px;">
                    {nom_dia}
                </div>
                """, 
                unsafe_allow_html=True
            )
            items_dia = [it for it in planes_consolidadosa if it["Fecha_Plan"] == f_str or it["Fecha_Plan"] == f_date.strftime("%d/%m/%Y")]
            
            if items_dia:
                df_dia = pd.DataFrame(items_dia)[["OP", "TURNO", "CLIENTE", "PRODUCTO", "CANTIDAD"]]
                df_styled = df_dia.style.map(estilar_celda_masas, subset=['CANTIDAD'])
                st.dataframe(df_styled, use_container_width=True, hide_index=True)
            else:
                df_vacio = pd.DataFrame(columns=["OP", "TURNO", "CLIENTE", "PRODUCTO", "CANTIDAD"])
                st.dataframe(df_vacio, use_container_width=True, hide_index=True)

# --- NAVEGACIÓN Y SOLAPAS ---
if "modulo_activo" not in st.session_state:
    st.session_state["modulo_activo"] = "Producción"

if "planning_autenticado" not in st.session_state:
    st.session_state["planning_autenticado"] = False

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

col_nav1, col_nav2, col_nav3, col_nav4, _ = st.columns([1.2, 1.1, 1.1, 1.2, 4.8])

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

with col_nav4:
    btn_analitica_type = "primary" if st.session_state["modulo_activo"] == "Analítica" else "secondary"
    if st.button("📊 Módulo Analítica", type=btn_analitica_type, use_container_width=True):
        st.session_state["modulo_activo"] = "Analítica"
        st.rerun()

st.markdown("---")

# ==========================================
# 1. MÓDULO PRODUCCIÓN
# ==========================================
if st.session_state["modulo_activo"] == "Producción":
    renderizar_cronograma_semanal()
    st.markdown("---")

    st.title("📋 Control de órdenes de producción Golomaster V1")

    fecha_actual_hoy = obtener_ahora_arg().date()

    def op_existe(num_op):
        df = cargar_historial()
        if not df.empty and "OP_Num" in df.columns:
            return str(num_op).strip() in df["OP_Num"].astype(str).str.strip().values
        return False

    def solicitar_limpieza():
        st.session_state["necesita_limpieza"] = True
        try:
            localS.deleteItem("borrador_golomaster")
        except Exception:
            pass

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
        st.session_state["cliente_select_prod"] = ""
        st.session_state["producto_select_prod"] = ""
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

    lista_clientes_prod = [""] + sorted(df_maestro["CLIENTE"].unique().tolist())
    cli_guardado_prod = st.session_state.get("cliente_select_prod", "")
    idx_cli_prod = lista_clientes_prod.index(cli_guardado_prod) if cli_guardado_prod in lista_clientes_prod else 0

    with col2:
        cliente = st.selectbox("CLIENTE", lista_clientes_prod, index=idx_cli_prod, key="cliente_select_prod")
        
        if cliente != "":
            prods_filtrados = df_maestro[df_maestro["CLIENTE"] == cliente]["PRODUCTO"].unique().tolist()
            lista_productos_prod = [""] + sorted(prods_filtrados)
        else:
            lista_productos_prod = [""]

        prod_guardado_prod = st.session_state.get("producto_select_prod", "")
        idx_prod_p = lista_productos_prod.index(prod_guardado_prod) if prod_guardado_prod in lista_productos_prod else 0
        producto = st.selectbox("PRODUCTO", lista_productos_prod, index=idx_prod_p, key="producto_select_prod")

    vida_util_meses = 0
    if cliente != "" and producto != "":
        match_item = df_maestro[(df_maestro["CLIENTE"] == cliente) & (df_maestro["PRODUCTO"] == producto)]
        if not match_item.empty:
            vida_util_meses = int(match_item.iloc[0]["VIDA_UTIL"])

    with col3:
        if cliente != "" and producto != "":
            if vida_util_meses > 0:
                st.info(f"**Vida Útil para {producto}:** {vida_util_meses} meses")
            else:
                st.warning(f"**Vida Útil para {producto}:** No aplica VTO (-)")
        elif cliente != "":
            st.info("Seleccione un producto para obtener su vida útil.")
        else:
            st.info("Seleccione un cliente y producto.")

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
        
        if vida_util_meses > 0:
            vto_date = f_val + relativedelta(months=vida_util_meses)
            vto_str = vto_date.strftime("%d%m%y")
            es_vto_valido = (hoy <= vto_date <= max_vto)
            vto_label = f"{vto_str} 🟢" if es_vto_valido else f"{vto_str} 🔴"
        else:
            vto_str = "-"
            vto_label = "-"

        with col_l:
            if cliente == "ENA":
                lote_final = st.text_input("", key=f"lote_{i}", disabled=filas_deshabilitadas, label_visibility="collapsed")
            else:
                lote_final = lote_auto
                st.text_input("", value=lote_auto, key=f"lote_dis_{i}_{lote_auto}", disabled=True, label_visibility="collapsed")
            
        with col_v:
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
        "cliente_select_prod": cliente,
        "producto_select_prod": producto
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
                st.success(f"✅ ¡OP N° {num_op} registrada en la pestaña 'BD PRODU' correctamente!")
                st.rerun()
            else:
                st.error("❌ Ocurrió un error al guardar en Google Sheets. Verifique la conexión.")

    st.markdown("---")
    st.subheader("📚 Historial de OPs Cerradas (Google Sheets - BD PRODU)")
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
# 3. MÓDULO PLANNING
# ==========================================
elif st.session_state["modulo_activo"] == "Planning":
    st.title("📅 Módulo Planning - Planificación de Producción")

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

        todas_las_ops = obtener_todas_las_ops_existentes()
        op_planning_duplicada = False
        
        if op_plan != "" and op_plan in todas_las_ops:
            st.error(f"⛔ LA OP N° '{op_plan}' YA FUE REGISTRADA O PLANIFICADA PREVIAMENTE. NO SE PUEDE REPETIR EL NÚMERO DE OP.")
            op_planning_duplicada = True

        st.markdown("---")
        st.markdown("### 🔍 Selección de Producto a Planificar")

        categorias_disponibles = [""] + sorted(df_maestro["CATEGORIA"].unique().tolist())
        cat_sel = st.selectbox("1. CATEGORÍA", categorias_disponibles, key="plan_cat_select")

        if cat_sel != "":
            df_cat = df_maestro[df_maestro["CATEGORIA"] == cat_sel]
            clientes_disponibles = [""] + sorted(df_cat["CLIENTE"].unique().tolist())
        else:
            clientes_disponibles = [""]

        cli_sel = st.selectbox("2. CLIENTE", clientes_disponibles, key="plan_cli_select")

        if cat_sel != "" and cli_sel != "":
            df_prod = df_maestro[(df_maestro["CATEGORIA"] == cat_sel) & (df_maestro["CLIENTE"] == cli_sel)]
            productos_disponibles = [""] + sorted(df_prod["PRODUCTO"].unique().tolist())
        else:
            productos_disponibles = [""]

        prod_sel = st.selectbox("3. PRODUCTO", productos_disponibles, key="plan_prod_select")

        st.markdown("---")

        if cat_sel != "" and cli_sel != "" and prod_sel != "":
            fila_item = df_maestro[
                (df_maestro["CATEGORIA"] == cat_sel) & 
                (df_maestro["CLIENTE"] == cli_sel) & 
                (df_maestro["PRODUCTO"] == prod_sel)
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
                    
                    if cli_sel == "INTEGRA":
                        kg_totales = cant_unidades_ingresadas * 0.035
                        masas_calculadas = kg_totales / 150.0
                        
                        col_m1, col_m2 = st.columns(2)
                        with col_m1:
                            st.metric(label="EQUIVALENTE EN CAJAS", value=f"{cajas_calculadas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                        with col_m2:
                            st.metric(label="EQUIVALENTE EN MASAS (150 KG)", value=f"{masas_calculadas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                            
                        total_resumen = f"{cajas_calculadas:,.2f} Cajas ({cant_unidades_ingresadas:,} U) | {masas_calculadas:,.2f} Masas ({kg_totales:,.2f} KG)"
                    else:
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
            if st.button("➕ Guardar y Enviar Plan a Google Sheets (BD PLANNING)", type="primary", disabled=op_planning_duplicada):
                if op_plan == "":
                    st.warning("⚠️ Debe especificar un N° de OP.")
                else:
                    payload_planning = {
                        "Fecha_Plan": fecha_plan.strftime("%d/%m/%Y"),
                        "OP_Num": op_plan,
                        "Turno": turno_plan,
                        "Categoria": cat_sel,
                        "Cliente": cli_sel,
                        "Producto": prod_sel,
                        "Detalle_Cantidad": total_resumen,
                        "Fecha_Carga": obtener_ahora_arg().strftime("%d/%m/%Y %H:%M")
                    }
                    
                    exito = guardar_planning_en_sheets(payload_planning)
                    if exito:
                        nuevo_plan = {
                            "Fecha_Plan": fecha_plan.strftime("%d/%m/%Y"),
                            "OP_Num": op_plan,
                            "Turno": turno_plan,
                            "Categoria": cat_sel,
                            "Cliente": cli_sel,
                            "Producto": prod_sel,
                            "Detalle_Cantidad": total_resumen
                        }
                        st.session_state["lista_planes"].append(nuevo_plan)
                        st.success(f"✅ ¡Plan para la OP N° {op_plan} guardado en la solapa 'BD PLANNING' correctamente!")
                        st.rerun()
                    else:
                        st.error("❌ Ocurrió un error al guardar en la base de datos de Google Sheets.")

        else:
            st.info("👈 Seleccione Categoría, Cliente y Producto para habilitar la carga de cantidades.")

        st.markdown("---")
        st.subheader("📚 Base de Datos de Planificaciones (Google Sheets - BD PLANNING)")
        
        df_planning_historial = cargar_historial_planning()
        
        if not df_planning_historial.empty:
            st.dataframe(df_planning_historial, use_container_width=True)
        else:
            st.info("No hay órdenes de planificación registradas aún en la pestaña BD PLANNING de Google Sheets.")

# ==========================================
# 4. MÓDULO ANALÍTICA
# ==========================================
elif st.session_state["modulo_activo"] == "Analítica":
    st.title("📊 Dashboard y Analítica de Producción")
    st.caption("Alimentado dinámicamente desde la base de datos `BD PRODUCCION`")

    df_analytics = cargar_historial()

    if df_analytics.empty:
        st.warning("⚠️ No se encontraron datos en `BD PRODU` para analizar en este momento.")
    else:
        col_fecha_nom = "Fecha_OP" if "Fecha_OP" in df_analytics.columns else ("Fecha_Parcial" if "Fecha_Parcial" in df_analytics.columns else None)
        
        if col_fecha_nom:
            df_analytics["Fecha_DT"] = pd.to_datetime(df_analytics[col_fecha_nom], format="%d/%m/%Y", errors="coerce")
        else:
            df_analytics["Fecha_DT"] = pd.NaT

        df_valid_dates = df_analytics.dropna(subset=["Fecha_DT"])

        for num_col in ["Cantidad", "Total_Producido", "Cant_Total_OP", "Mermas_C", "Scrap_P"]:
            if num_col in df_analytics.columns:
                df_analytics[num_col] = pd.to_numeric(df_analytics[num_col].astype(str).str.replace(",", "."), errors="coerce").fillna(0)
            else:
                df_analytics[num_col] = 0

        st.markdown("### 🎛️ Panel de Control y Filtros")

        col_f1, col_f2, col_f3 = st.columns([2.0, 1.5, 1.5])

        with col_f1:
            if not df_valid_dates.empty:
                min_f = df_valid_dates["Fecha_DT"].min().date()
                max_f = df_valid_dates["Fecha_DT"].max().date()
                if min_f == max_f:
                    min_f = min_f - timedelta(days=7)
            else:
                min_f = date.today() - timedelta(days=30)
                max_f = date.today()

            rango_fechas = st.slider(
                "📅 Rango de Fechas de Producción",
                min_value=min_f,
                max_value=max_f,
                value=(min_f, max_f),
                format="DD/MM/YYYY",
                key="slider_fechas_analitica"
            )

        with col_f2:
            clientes_options = ["TODOS"] + sorted(df_analytics["Cliente"].dropna().unique().tolist()) if "Cliente" in df_analytics.columns else ["TODOS"]
            cliente_filtro = st.multiselect("🏢 Filtrar por Cliente", options=clientes_options, default=["TODOS"], key="filter_cliente_analitica")

        with col_f3:
            prods_options = ["TODOS"] + sorted(df_analytics["Producto"].dropna().unique().tolist()) if "Producto" in df_analytics.columns else ["TODOS"]
            producto_filtro = st.multiselect("🍫 Filtrar por Producto", options=prods_options, default=["TODOS"], key="filter_producto_analitica")

        df_filtered = df_analytics.copy()

        if "Fecha_DT" in df_filtered.columns:
            f_inicio = pd.to_datetime(rango_fechas[0])
            f_fin = pd.to_datetime(rango_fechas[1])
            df_filtered = df_filtered[(df_filtered["Fecha_DT"] >= f_inicio) & (df_filtered["Fecha_DT"] <= f_fin)]

        if "TODOS" not in cliente_filtro and len(cliente_filtro) > 0:
            df_filtered = df_filtered[df_filtered["Cliente"].isin(cliente_filtro)]

        if "TODOS" not in producto_filtro and len(producto_filtro) > 0:
            df_filtered = df_filtered[df_filtered["Producto"].isin(producto_filtro)]

        st.markdown("---")

        col_k1, col_k2, col_k3, col_k4 = st.columns(4)

        if "Cantidad" in df_filtered.columns and df_filtered["Cantidad"].sum() > 0:
            total_unid = df_filtered["Cantidad"].sum()
        else:
            total_unid = df_filtered["Total_Producido"].sum() if "Total_Producido" in df_filtered.columns else 0

        tot_mermas = df_filtered["Mermas_C"].sum() if "Mermas_C" in df_filtered.columns else 0
        tot_scrap = df_filtered["Scrap_P"].sum() if "Scrap_P" in df_filtered.columns else 0
        total_ops = df_filtered["OP_Num"].nunique() if "OP_Num" in df_filtered.columns else 0

        with col_k1:
            st.metric("📦 Unidades Producidas", f"{int(total_unid):,}".replace(",", "."))
        with col_k2:
            st.metric("📋 Órdenes de Producción (OPs)", f"{total_ops}")
        with col_k3:
            st.metric("📉 Mermas Totales (KG)", f"{tot_mermas:.2f} kg")
        with col_k4:
            st.metric("🗑️ Scrap Total (KG)", f"{tot_scrap:.2f} kg")

        st.markdown("---")

        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown("#### 📈 Evolución Diaria de Producción")
            if not df_filtered.empty and "Fecha_DT" in df_filtered.columns:
                df_trend = df_filtered.groupby(df_filtered["Fecha_DT"].dt.strftime("%d/%m/%Y"))["Cantidad"].sum().reset_index()
                st.line_chart(df_trend.set_index("Fecha_DT"))
            else:
                st.info("Sin datos suficientes para graficar la tendencia.")

        with col_g2:
            st.markdown("#### 🏢 Participación de Producción por Cliente")
            if not df_filtered.empty and "Cliente" in df_filtered.columns:
                df_cli_chart = df_filtered.groupby("Cliente")["Cantidad"].sum().reset_index()
                st.bar_chart(df_cli_chart.set_index("Cliente"))
            else:
                st.info("Sin datos de clientes para mostrar.")

        st.markdown("---")
        col_g3, col_g4 = st.columns(2)

        with col_g3:
            st.markdown("#### 🏆 Top Productos Fabricados")
            if not df_filtered.empty and "Producto" in df_filtered.columns:
                df_prod_chart = df_filtered.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False).head(5)
                st.bar_chart(df_prod_chart)
            else:
                st.info("Sin datos de productos.")

        with col_g4:
            st.markdown("#### ⏱️ Producción por Turno")
            if not df_filtered.empty and "Turno" in df_filtered.columns:
                df_turno_chart = df_filtered.groupby("Turno")["Cantidad"].sum()
                st.bar_chart(df_turno_chart)
            else:
                st.info("Sin datos por turno.")

        st.markdown("---")

        st.markdown("### 🔍 Detalle de Registros Filtrados")
        st.dataframe(df_filtered, use_container_width=True)

        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Datos Filtrados en CSV",
            data=csv_data,
            file_name=f"reporte_produccion_{date.today().strftime('%d_%m_%Y')}.csv",
            mime="text/csv"
        )
