import random
from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL Y ESTILO (TEMA CLARO DEDICADO)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Ingeniería en Energía Inteligente", page_icon="⚡", layout="wide"
)

st.markdown(
    """
    <style>
    /* 1. FONDO GENERAL Y TEXTO PRINCIPAL */
    .stApp {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    
    /* 2. OCULTAR O BLANQUEAR BARRA SUPERIOR */
    header[data-testid="stHeader"] {
        background-color: #FFFFFF !important;
    }
    div[data-testid="stDecoration"] {
        background-color: #FFFFFF !important;
        background-image: none !important;
    }
    
    /* 3. BARRA LATERAL (SIDEBAR) EN BLANCO Y GRIS CLARO */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #0F172A !important;
    }

    /* 4. REGLAS DE CONTRASTE PARA TÍTULOS Y TEXTOS */
    h1, h2, h3, h4, h5, h6 {
        color: #1E3A8A !important;
        font-weight: 700 !important;
    }
    p, label, span, div, li {
        color: #0F172A !important;
    }

    /* 5. DISEÑO DE CAJAS DE ENTRADA Y CONTROLES (FINAS Y ELEGANTES) */
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="base-input"] {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #CBD5E1 !important;
        box-shadow: none !important;
    }
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
    }
    input, select, textarea {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        background-color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
    }
    
    /* Number Input y botones +/- ajustados */
    div[data-testid="stNumberInput"] input {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        background-color: #FFFFFF !important;
    }
    div[data-testid="stNumberInput"] button {
        background-color: #F1F5F9 !important;
        color: #334155 !important;
        border: 1px solid #CBD5E1 !important;
    }
    div[data-testid="stNumberInput"] button:hover {
        background-color: #E2E8F0 !important;
    }
    div[data-testid="stNumberInput"] button * {
        color: #0F172A !important;
    }
    
    /* Selectbox y menús desplegables */
    div[data-baseweb="popover"], div[role="listbox"], li[role="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }

    /* 6. BOTONES PRINCIPALES */
    .stButton > button {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
    }
    .stButton > button * {
        color: #FFFFFF !important;
    }

    /* 7. TARJETAS PERSONALIZADAS DE ALTO CONTRASTE */
    .main-header {
        font-size: 2.3rem;
        color: #1E3A8A !important;
        text-align: center;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #334155 !important;
        text-align: center;
        margin-bottom: 20px;
        font-weight: 600;
    }
    .round-badge {
        background-color: #F8FAFC;
        border: 2px solid #0284C7;
        padding: 16px 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .winner-card {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border: 2px solid #D97706;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
    }
    .locked-card {
        background-color: #FEF2F2;
        border: 2px solid #EF4444;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .result-card {
        background-color: #F0FDF4;
        border: 2px solid #16A34A;
        padding: 18px;
        border-radius: 10px;
        margin-top: 15px;
    }
    
    /* 8. METRICAS Y ELEMENTOS DE REGISTRO */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #0F172A !important;
    }

    /* 9. CONTRASTE ADICIONAL: TABLAS DE RESULTADOS (HTML, fondo blanco) */
    .tabla-wrap {
        overflow-x: auto;
        background-color: #FFFFFF !important;
        border: 1px solid #94A3B8;
        border-radius: 10px;
        margin-bottom: 18px;
    }
    table.tabla-mercado {
        width: 100%;
        border-collapse: collapse;
        background-color: #FFFFFF !important;
        font-size: 0.98rem;
    }
    table.tabla-mercado th {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-align: left;
        padding: 10px 14px !important;
        border: none !important;
        border-bottom: 2px solid #0F172A !important;
    }
    table.tabla-mercado td {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        font-weight: 600;
        padding: 9px 14px !important;
        border: none !important;
        border-bottom: 1px solid #CBD5E1 !important;
    }
    table.tabla-mercado tbody tr:nth-child(even) td {
        background-color: #F1F5F9 !important;
    }
    table.tabla-mercado th.num, table.tabla-mercado td.num {
        text-align: right;
    }

    /* 9b. BOTONES DE DESCARGA (no son .stButton, quedaban oscuro sobre oscuro) */
    [data-testid="stDownloadButton"] button {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
    }
    [data-testid="stDownloadButton"] button:hover {
        background-color: #2563EB !important;
    }
    [data-testid="stDownloadButton"] button * {
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stButton > button * {
        color: #FFFFFF !important;
    }

    /* 9c. TEXTOS SECUNDARIOS, ALERTAS, ICONOS Y PLACEHOLDERS */
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] * {
        color: #334155 !important;
        opacity: 1 !important;
    }
    [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] * {
        color: #0F172A !important;
    }
    div[data-testid="stAlert"] *,
    div[data-testid="stAlertContainer"] * {
        color: #0F172A !important;
    }
    div[data-baseweb="select"] svg,
    div[data-baseweb="input"] svg {
        fill: #334155 !important;
        color: #334155 !important;
    }
    input::placeholder, textarea::placeholder {
        color: #64748B !important;
        -webkit-text-fill-color: #64748B !important;
        opacity: 1 !important;
    }
    hr {
        border-color: #CBD5E1 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def mostrar_tabla(df, formatos=None):
    """Dibuja una tabla HTML con fondo blanco y texto oscuro (alto contraste)."""
    formatos = formatos or {}
    encabezado = "".join(
        f'<th class="{"num" if c in formatos else ""}">{escape(str(c))}</th>'
        for c in df.columns
    )
    filas = ""
    for _, fila in df.iterrows():
        celdas = ""
        for c in df.columns:
            valor = fila[c]
            texto = formatos[c].format(valor) if c in formatos else str(valor)
            # &#36; evita que Streamlit interprete el signo $ como fórmula LaTeX
            texto = escape(texto).replace("$", "&#36;")
            clase = "num" if c in formatos else ""
            celdas += f'<td class="{clase}">{texto}</td>'
        filas += f"<tr>{celdas}</tr>"
    st.markdown(
        '<div class="tabla-wrap"><table class="tabla-mercado">'
        f"<thead><tr>{encabezado}</tr></thead><tbody>{filas}</tbody>"
        "</table></div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# ESTADO GLOBAL DE LA APLICACIÓN
# ---------------------------------------------------------
@st.cache_resource
def obtener_estado_global():
    return {
        "asignacion": {},
        "ronda_actual": 1,
        "ofertas": {},
        "bloqueados": {},
        "resultados": {},
        "precios_marginales": {},
    }


estado_global = obtener_estado_global()

# ---------------------------------------------------------
# BASE DE DATOS DE PLANTAS DE GENERACIÓN
# ---------------------------------------------------------
PLANTAS_SISTEMA = [
    # FNCER (5)
    {
        "id": "G1",
        "nombre": "Sol Radiante 1",
        "fuente": "Solar",
        "tipo": "FNCER",
        "cap_nom": 80,
        "costo": 40.0,
    },
    {
        "id": "G2",
        "nombre": "Sol Radiante 2",
        "fuente": "Solar",
        "tipo": "FNCER",
        "cap_nom": 80,
        "costo": 40.0,
    },
    {
        "id": "G3",
        "nombre": "HeliOS 3",
        "fuente": "Solar",
        "tipo": "FNCER",
        "cap_nom": 100,
        "costo": 50.0,
    },
    {
        "id": "G4",
        "nombre": "Vientos del Norte 1",
        "fuente": "Eólica",
        "tipo": "FNCER",
        "cap_nom": 120,
        "costo": 60.0,
    },
    {
        "id": "G5",
        "nombre": "Vientos del Norte 2",
        "fuente": "Eólica",
        "tipo": "FNCER",
        "cap_nom": 120,
        "costo": 60.0,
    },
    # Convencionales (5)
    {
        "id": "G6",
        "nombre": "Río Vivo 1",
        "fuente": "Hidro Filo",
        "tipo": "Convencional",
        "cap_nom": 100,
        "costo": 80.0,
    },
    {
        "id": "G7",
        "nombre": "Río Vivo 2",
        "fuente": "Hidro Filo",
        "tipo": "Convencional",
        "cap_nom": 100,
        "costo": 80.0,
    },
    {
        "id": "G8",
        "nombre": "Embalse Central 1",
        "fuente": "Hidro Embalse",
        "tipo": "Convencional",
        "cap_nom": 150,
        "costo": 120.0,
    },
    {
        "id": "G9",
        "nombre": "Embalse Central 2",
        "fuente": "Hidro Embalse",
        "tipo": "Convencional",
        "cap_nom": 150,
        "costo": 140.0,
    },
    {
        "id": "G10",
        "nombre": "Embalse El Salto",
        "fuente": "Hidro Embalse",
        "tipo": "Convencional",
        "cap_nom": 200,
        "costo": 160.0,
    },
    # Térmicas (5)
    {
        "id": "G11",
        "nombre": "Térmica Carbón A",
        "fuente": "Carbón",
        "tipo": "Térmica",
        "cap_nom": 150,
        "costo": 280.0,
    },
    {
        "id": "G12",
        "nombre": "Térmica Carbón B",
        "fuente": "Carbón",
        "tipo": "Térmica",
        "cap_nom": 150,
        "costo": 300.0,
    },
    {
        "id": "G13",
        "nombre": "TermoGas 1",
        "fuente": "Gas",
        "tipo": "Térmica",
        "cap_nom": 200,
        "costo": 380.0,
    },
    {
        "id": "G14",
        "nombre": "TermoGas 2",
        "fuente": "Gas",
        "tipo": "Térmica",
        "cap_nom": 200,
        "costo": 420.0,
    },
    {
        "id": "G15",
        "nombre": "TermoDiésel Pico",
        "fuente": "Diésel",
        "tipo": "Térmica",
        "cap_nom": 150,
        "costo": 600.0,
    },
]

ICONOS_FUENTE = {
    "Solar": "☀️",
    "Eólica": "🌬️",
    "Hidro Filo": "💧",
    "Hidro Embalse": "🌊",
    "Carbón": "⛏️",
    "Gas": "🔥",
    "Diésel": "⛽",
}

COLOR_TIPO = {
    "FNCER": {
        "bg": "#ECFDF5",
        "border": "#059669",
        "text": "#064E3B",
        "badge": "Renovable No Convencional",
    },
    "Convencional": {
        "bg": "#EFF6FF",
        "border": "#2563EB",
        "text": "#1E3A8A",
        "badge": "Renovable Convencional",
    },
    "Térmica": {
        "bg": "#FEF2F2",
        "border": "#DC2626",
        "text": "#7F1D1D",
        "badge": "No Renovable / Térmica",
    },
}

INFO_RONDAS = {
    1: {
        "nombre": "Ronda 1: Hidrología Alta",
        "demanda": 1000,
        "descripcion": (
            "Condiciones climáticas óptimas. 100% de disponibilidad solar,"
            " eólica e hídrica. Demanda fija del sistema: 1,000 MW."
        ),
    },
    2: {
        "nombre": "Ronda 2: El Niño / Noche",
        "demanda": 1100,
        "descripcion": (
            "Periodo de sequía severa y noche. Solar: 0%, Eólica: 40%, Hidro"
            " Filo: 25%, Embalses: 50%. Demanda fija del sistema: 1,100 MW."
        ),
    },
}


def realizar_sorteo():
    fncer = [p for p in PLANTAS_SISTEMA if p["tipo"] == "FNCER"]
    conv = [p for p in PLANTAS_SISTEMA if p["tipo"] == "Convencional"]
    term = [p for p in PLANTAS_SISTEMA if p["tipo"] == "Térmica"]

    random.shuffle(fncer)
    random.shuffle(conv)
    random.shuffle(term)

    asignacion = {}
    grupos = ["Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4", "Grupo 5"]

    for i, g in enumerate(grupos):
        asignacion[g] = [fncer[i], conv[i], term[i]]

    estado_global["asignacion"] = asignacion
    estado_global["ofertas"] = {}
    estado_global["bloqueados"] = {}
    estado_global["resultados"] = {}
    estado_global["precios_marginales"] = {}
    estado_global["ronda_actual"] = 1


if not estado_global["asignacion"]:
    realizar_sorteo()

# ---------------------------------------------------------
# ENCABEZADO DE LA APLICACIÓN
# ---------------------------------------------------------
st.markdown(
    '<div class="main-header">⚡ Ingeniería en Energía Inteligente</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Mercado de Energía Mayorista</div>',
    unsafe_allow_html=True,
)

st.sidebar.title("Navegación")
rol = st.sidebar.radio(
    "Modo de Acceso:", ["Portal Jugador", "Panel Administrador"]
)

# ---------------------------------------------------------
# PORTAL JUGADOR
# ---------------------------------------------------------
if rol == "Portal Jugador":

    if st.sidebar.button("🔄 Actualizar Estado del Mercado"):
        st.rerun()

    if "mi_grupo" not in st.session_state:
        st.subheader("👥 Selección Inicial de Equipo")
        st.info(
            "👋 Bienvenida/o. Selecciona el grupo asignado para tu mesa de"
            " trabajo."
        )

        grupo_elegido = st.selectbox(
            "Selecciona tu Equipo:",
            ["Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4", "Grupo 5"],
        )
        if st.button("✅ Confirmar e Ingresar como " + grupo_elegido):
            st.session_state["mi_grupo"] = grupo_elegido
            st.rerun()
    else:
        grupo_sel = st.session_state["mi_grupo"]

        ronda_act = estado_global["ronda_actual"]
        info_ronda = INFO_RONDAS[ronda_act]

        c_head1, c_head2 = st.columns([3, 1])
        with c_head1:
            st.subheader(f"👥 Portal de Ofertas — {grupo_sel}")
        with c_head2:
            st.caption(f"🔒 Equipo activo: **{grupo_sel}**")

        st.markdown(
            f"""
            <div class="round-badge">
                <span style="color:#0284C7; font-weight:800; font-size:1.1em;">📢 ESCENARIO ACTIVO: {info_ronda['nombre'].upper()}</span><br>
                <span style="font-size:0.95em; color:#334155;">{info_ronda['descripcion']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        esta_bloqueado = estado_global["bloqueados"].get(
            (ronda_act, grupo_sel), False
        )

        if esta_bloqueado:
            st.markdown(
                f"""
                <div class="locked-card">
                    <b style="color:#991B1B;">🔒 Ofertas Registradas:</b> <span style="color:#7F1D1D;">Las ofertas del <b>{grupo_sel}</b> para la <b>{info_ronda['nombre']}</b> ya fueron enviadas al servidor. Por favor espera a que el docente ejecute el despacho económico.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("### 📋 Resumen de Ofertas Enviadas para esta Ronda:")
            for (r, p_id), off in estado_global["ofertas"].items():
                if r == ronda_act and off["grupo"] == grupo_sel:
                    icono = ICONOS_FUENTE.get(off["fuente"], "⚡")
                    st.markdown(
                        f"• **{icono} {off['nombre']}** ({off['fuente']}):"
                        f" **${off['precio_oferta']:,.2f} COP/kWh** — Cap. Disp:"
                        f" **{off['cap_disp']:.0f} MW**"
                    )

            if ronda_act in estado_global["resultados"]:
                df_res = estado_global["resultados"][ronda_act]
                res_mi_grupo = df_res[df_res["grupo"] == grupo_sel]
                precio_m = estado_global["precios_marginales"].get(ronda_act, 0.0)

                if not res_mi_grupo.empty:
                    mw_desp = res_mi_grupo.iloc[0]["MW_Despachados"]
                    ingresos = res_mi_grupo.iloc[0]["Ingresos"]
                    utilidad = res_mi_grupo.iloc[0]["Utilidad_Neta"]

                    st.markdown(
                        f"""
                        <div class="result-card">
                            <h3 style="color:#065F46; margin:0;">📊 Resultados de tu Equipo — {info_ronda['nombre']}</h3>
                            <p style="margin:8px 0; font-size:1.1em; color:#0F172A;"><b>Precio Marginal de Bolsa:</b> <span style="color:#2563EB; font-weight:bold;">${precio_m:,.2f} COP/kWh</span></p>
                            <hr style="border-color:#CBD5E1;">
                            <p style="color:#0F172A;">⚡ <b>Energía Despachada:</b> {mw_desp:,.0f} MW</p>
                            <p style="color:#0F172A;">💵 <b>Ingresos Totales:</b> ${ingresos:,.2f} COP</p>
                            <p style="color:#0F172A;">📈 <b>Utilidad Neta Obtenida:</b> <span style="font-size:1.2em; color:#D97706; font-weight:bold;">${utilidad:,.2f} COP</span></p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        else:
            plantas_equipo = estado_global["asignacion"].get(grupo_sel, [])
            st.info(
                "📍 Ingresa el precio de oferta en COP/kWh para tus 3 generadoras."
            )

            ofertas_temp = {}

            for p in plantas_equipo:
                if ronda_act == 1:
                    disp_pct = 1.0
                else:
                    disp_map = {
                        "Solar": 0.0,
                        "Eólica": 0.4,
                        "Hidro Filo": 0.25,
                        "Hidro Embalse": 0.5,
                        "Carbón": 1.0,
                        "Gas": 1.0,
                        "Diésel": 1.0,
                    }
                    disp_pct = disp_map.get(p["fuente"], 1.0)

                cap_disp = p["cap_nom"] * disp_pct
                icono = ICONOS_FUENTE.get(p["fuente"], "⚡")
                estilo = COLOR_TIPO[p["tipo"]]

                st.markdown(
                    f"""
                    <div style="background-color: {estilo['bg']}; border-left: 6px solid {estilo['border']}; padding: 14px; border-radius: 8px; margin-bottom: 12px;">
                        <h4 style="margin:0; color: {estilo['text']};">{icono} {p['nombre']} — <span style="font-size: 0.85em;">{estilo['badge']}</span></h4>
                        <p style="margin:4px 0 0 0; color: #1E293B; font-size:0.95em;">
                            Fuente: <b>{p['fuente']}</b> | Capacidad Disp.: <b>{cap_disp:.0f} MW</b> | Costo Base: <b>${p['costo']:,.2f} COP/kWh</b>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                precio = st.number_input(
                    f"Precio de Oferta para {p['nombre']} (COP/kWh)",
                    min_value=0.0,
                    max_value=2000.0,
                    value=float(p["costo"]),
                    step=5.0,
                    key=f"inp_{grupo_sel}_r{ronda_act}_{p['id']}",
                )

                ofertas_temp[(ronda_act, p["id"])] = {
                    "nombre": p["nombre"],
                    "fuente": p["fuente"],
                    "grupo": grupo_sel,
                    "cap_disp": cap_disp,
                    "costo": p["costo"],
                    "precio_oferta": precio,
                }
                st.write("")

            st.divider()

            if st.button(
                f"📤 Registrar y Bloquear Ofertas del {grupo_sel} (Ronda"
                f" {ronda_act})"
            ):
                estado_global["ofertas"].update(ofertas_temp)
                estado_global["bloqueados"][(ronda_act, grupo_sel)] = True
                st.success(f"✅ ¡Ofertas del {grupo_sel} enviadas exitosamente!")
                st.rerun()

# ---------------------------------------------------------
# PANEL ADMINISTRADOR
# ---------------------------------------------------------
elif rol == "Panel Administrador":
    st.subheader("🔒 Control Central del Mercado")

    password = st.text_input(
        "Ingresa la contraseña de administrador:", type="password"
    )

    if password != "subasta2026":
        if password != "":
            st.error("❌ Contraseña incorrecta.")
        st.warning("⚠ Debes ingresar la clave para acceder al panel de control.")
    else:
        st.success("🔓 Sesión de Administrador Activa.")

        c_top1, c_top2 = st.columns(2)
        with c_top1:
            if st.button("🔄 Refrescar Ofertas Recibidas"):
                st.rerun()
        with c_top2:
            if st.button("🚨 REINICIAR PARTIDA COMPLETA (RESET TOTAL)"):
                realizar_sorteo()
                st.success(
                    "🚨 ¡Se ha reiniciado completamente la partida! Plantas"
                    " re-sorteadas y ofertas limpiadas."
                )
                st.rerun()

        st.divider()
        st.markdown("### 🎛️ Control de Ronda Activa para los Estudiantes")
        ronda_sel = st.radio(
            "Selecciona qué Ronda habilitar en la pantalla de los estudiantes:",
            options=[1, 2],
            format_func=lambda x: INFO_RONDAS[x]["nombre"],
            index=estado_global["ronda_actual"] - 1,
            horizontal=True,
        )

        if ronda_sel != estado_global["ronda_actual"]:
            estado_global["ronda_actual"] = ronda_sel
            st.success(
                "¡Ronda de estudiantes actualizada a:"
                f" **{INFO_RONDAS[ronda_sel]['nombre']}**!"
            )
            st.rerun()

        st.divider()

        ronda_proc = estado_global["ronda_actual"]
        info_proc = INFO_RONDAS[ronda_proc]
        demanda = info_proc["demanda"]

        st.markdown(
            f"### 📊 Estado de Recepción y Despacho — **{info_proc['nombre']}**"
        )

        grupos = ["Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4", "Grupo 5"]
        cols_status = st.columns(5)
        grupos_listos = 0

        for idx, g in enumerate(grupos):
            listo = estado_global["bloqueados"].get((ronda_proc, g), False)
            if listo:
                grupos_listos += 1
                cols_status[idx].markdown(f"**{g}**\n\n✅ Listo")
            else:
                cols_status[idx].markdown(f"**{g}**\n\n⏳ Esperando")

        st.write("")
        ofertas_ronda = {
            k[1]: v
            for k, v in estado_global["ofertas"].items()
            if k[0] == ronda_proc
        }

        st.metric(
            label="Progreso Total de Ofertas",
            value=f"{grupos_listos} / 5 Equipos Listos",
            delta=f"{len(ofertas_ronda)} / 15 Plantas Recibidas",
        )

        if st.button(f"🚀 Ejecutar Despacho Económico - Ronda {ronda_proc}"):
            if len(ofertas_ronda) == 0:
                st.warning("No hay ofertas registradas aún para esta ronda.")
            else:
                df = pd.DataFrame.from_dict(ofertas_ronda, orient="index")
                df = df[df["cap_disp"] > 0].copy()

                if df.empty:
                    st.error("No hay capacidad disponible ofertada en esta ronda.")
                else:
                    df = df.sort_values(by="precio_oferta").reset_index(drop=True)

                    df["mw_acumulados"] = df["cap_disp"].cumsum()
                    df["mw_previos"] = df["mw_acumulados"] - df["cap_disp"]

                    df["despachado_mw"] = 0.0
                    precio_marginal = 0.0

                    capacidad_total = df["cap_disp"].sum()
                    if capacidad_total < demanda:
                        st.warning(
                            f"⚠️ ATENCIÓN: La oferta disponible total ({capacidad_total:.0f}"
                            f" MW) no cubre la demanda ({demanda} MW). Se despachará el"
                            " 100% de la oferta recibida."
                        )

                    for idx, row in df.iterrows():
                        if row["mw_previos"] < demanda:
                            mw_necesarios = demanda - row["mw_previos"]
                            mw_efectivos = min(row["cap_disp"], mw_necesarios)
                            df.at[idx, "despachado_mw"] = mw_efectivos
                            precio_marginal = row["precio_oferta"]
                        else:
                            df.at[idx, "despachado_mw"] = 0.0

                    df["ingreso"] = df["despachado_mw"] * 1000.0 * precio_marginal
                    df["costo_total"] = df["despachado_mw"] * 1000.0 * df["costo"]
                    df["utilidad"] = df["ingreso"] - df["costo_total"]

                    resumen = (
                        df.groupby("grupo")
                        .agg(
                            MW_Despachados=("despachado_mw", "sum"),
                            Ingresos=("ingreso", "sum"),
                            Utilidad_Neta=("utilidad", "sum"),
                        )
                        .reset_index()
                    )

                    for g in grupos:
                        if g not in resumen["grupo"].values:
                            resumen = pd.concat(
                                [
                                    resumen,
                                    pd.DataFrame([{
                                        "grupo": g,
                                        "MW_Despachados": 0.0,
                                        "Ingresos": 0.0,
                                        "Utilidad_Neta": 0.0,
                                    }]),
                                ],
                                ignore_index=True,
                            )

                    estado_global["resultados"][ronda_proc] = resumen
                    estado_global["precios_marginales"][ronda_proc] = precio_marginal

                    st.markdown(
                        "### 💰 Precio Marginal de Bolsa:"
                        f" **${precio_marginal:,.2f} COP/kWh**"
                    )

                    # ---------------------------------------------------------
                    # GRAFICACIÓN OPTIMIZADA DE LA CURVA DE MÉRITO
                    # ---------------------------------------------------------
                    fig = go.Figure()

                    for idx, row in df.iterrows():
                        if row["despachado_mw"] == row["cap_disp"]:
                            color_fill = "rgba(16, 185, 129, 0.4)"
                            color_line = "#059669"
                            estado_desc = "Totalmente Despachada"
                        elif row["despachado_mw"] > 0:
                            color_fill = "rgba(245, 158, 11, 0.4)"
                            color_line = "#D97706"
                            estado_desc = (
                                f"Parcialmente Despachada ({row['despachado_mw']:.0f} MW)"
                            )
                        else:
                            color_fill = "rgba(239, 68, 68, 0.3)"
                            color_line = "#DC2626"
                            estado_desc = "No Despachada"

                        icono = ICONOS_FUENTE.get(row["fuente"], "⚡")

                        fig.add_trace(
                            go.Scatter(
                                x=[
                                    row["mw_previos"],
                                    row["mw_acumulados"],
                                    row["mw_acumulados"],
                                    row["mw_previos"],
                                    row["mw_previos"],
                                ],
                                y=[
                                    0,
                                    0,
                                    row["precio_oferta"],
                                    row["precio_oferta"],
                                    0,
                                ],
                                fill="toself",
                                fillcolor=color_fill,
                                line=dict(color=color_line, width=2),
                                name=f"{icono} {row['nombre']} ({row['grupo']})",
                                text=(
                                    f"<b>{icono} {row['nombre']}</b><br>"
                                    f"Equipo: <b>{row['grupo']}</b><br>"
                                    f"Estado: <b>{estado_desc}</b><br>"
                                    f"Oferta: <b>${row['precio_oferta']:,.2f} COP/kWh</b><br>"
                                    f"Despachado: <b>{row['despachado_mw']:.0f} / {row['cap_disp']:.0f} MW</b>"
                                ),
                                hoverinfo="text",
                                showlegend=True,
                            )
                        )

                    # Línea de Demanda
                    fig.add_vline(
                        x=demanda,
                        line_dash="dash",
                        line_color="#0369A1",
                        line_width=2.5,
                        annotation_text=f"<b>Demanda: {demanda} MW</b>",
                        annotation_position="top left",
                        annotation_font=dict(size=12, color="#075985", family="Arial Black"),
                        annotation_bgcolor="rgba(255,255,255,0.95)",
                        annotation_bordercolor="#075985",
                        annotation_borderwidth=1,
                        annotation_borderpad=3,
                    )

                    # Línea de Precio Marginal
                    fig.add_hline(
                        y=precio_marginal,
                        line_dash="dot",
                        line_color="#B45309",
                        line_width=2.5,
                        annotation_text=f"<b>Precio Bolsa: ${precio_marginal:,.2f} COP/kWh</b>",
                        annotation_position="bottom right",
                        annotation_font=dict(size=12, color="#78350F", family="Arial Black"),
                        annotation_bgcolor="rgba(255,255,255,0.95)",
                        annotation_bordercolor="#78350F",
                        annotation_borderwidth=1,
                        annotation_borderpad=3,
                    )

                    fig.update_layout(
                        template="plotly_white",
                        title=dict(
                            text=f"<b>Curva de Mérito — {info_proc['nombre']}</b>",
                            font=dict(size=18, color="#1E3A8A"),
                        ),
                        xaxis=dict(
                            title=dict(
                                text="<b>Potencia Acumulada (MW)</b>",
                                font=dict(color="#0F172A", size=13),
                            ),
                            tickfont=dict(color="#0F172A", size=12),
                            color="#0F172A",
                            gridcolor="#CBD5E1",
                            zerolinecolor="#64748B",
                            linecolor="#64748B",
                        ),
                        yaxis=dict(
                            title=dict(
                                text="<b>Precio Ofertado (COP/kWh)</b>",
                                font=dict(color="#0F172A", size=13),
                            ),
                            tickfont=dict(color="#0F172A", size=12),
                            color="#0F172A",
                            gridcolor="#CBD5E1",
                            zerolinecolor="#64748B",
                            linecolor="#64748B",
                        ),
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#F8FAFC",
                        font=dict(color="#0F172A", size=12),
                        legend=dict(
                            bgcolor="rgba(255,255,255,0.95)",
                            bordercolor="#64748B",
                            borderwidth=1,
                            font=dict(color="#0F172A", size=11),
                        ),
                        hoverlabel=dict(
                            bgcolor="#FFFFFF",
                            bordercolor="#334155",
                            font=dict(color="#0F172A", size=12),
                        ),
                        modebar=dict(
                            bgcolor="rgba(255,255,255,0.9)",
                            color="#334155",
                            activecolor="#1E3A8A",
                        ),
                        height=540,
                        margin=dict(l=50, r=50, t=60, b=50),
                    )

                    # theme=None: evita que Streamlit sobrescriba los colores
                    # de la gráfica con su tema (que puede ser oscuro).
                    st.plotly_chart(fig, use_container_width=True, theme=None)

                    st.subheader("🏆 Resultados Financieros de la Ronda Actual")
                    mostrar_tabla(
                        resumen.sort_values(by="Utilidad_Neta", ascending=False),
                        {
                            "MW_Despachados": "{:,.0f} MW",
                            "Ingresos": "${:,.2f}",
                            "Utilidad_Neta": "${:,.2f}",
                        },
                    )

                    csv_data = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label=(
                            f"📥 Descargar Detalle de Despacho Ronda {ronda_proc} (Excel"
                            " / CSV)"
                        ),
                        data=csv_data,
                        file_name=f"despacho_subasta_ronda_{ronda_proc}.csv",
                        mime="text/csv",
                    )

    # ---------------------------------------------------------
    # TABLA DE POSICIONES FINAL / GRAN GANADOR
    # ---------------------------------------------------------
    st.divider()
    st.markdown("## 🏆 Tabla de Posiciones Final (Acumulado Rondas 1 y 2)")

    if 1 in estado_global["resultados"] and 2 in estado_global["resultados"]:
        df_r1 = estado_global["resultados"][1]
        df_r2 = estado_global["resultados"][2]

        df_total = pd.merge(
            df_r1, df_r2, on="grupo", suffixes=("_R1", "_R2"), how="outer"
        ).fillna(0)
        df_total["MW_Totales"] = (
            df_total["MW_Despachados_R1"] + df_total["MW_Despachados_R2"]
        )
        df_total["Ingresos_Totales"] = (
            df_total["Ingresos_R1"] + df_total["Ingresos_R2"]
        )
        df_total["Utilidad_Acumulada"] = (
            df_total["Utilidad_Neta_R1"] + df_total["Utilidad_Neta_R2"]
        )

        df_total = df_total.sort_values(
            by="Utilidad_Acumulada", ascending=False
        ).reset_index(drop=True)

        ganador = df_total.iloc[0]

        st.balloons()
        st.markdown(
            f"""
            <div class="winner-card">
                <h1 style="color: #78350F; margin:0;">🥇 ¡GRAN CAMPEÓN DEL MERCADO! 🥇</h1>
                <h2 style="color: #1E3A8A; margin: 10px 0;">{ganador['grupo']}</h2>
                <h3 style="color: #047857; margin:0;">Utilidad Acumulada: ${ganador['Utilidad_Acumulada']:,.2f} COP</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        mostrar_tabla(
            df_total[[
                "grupo",
                "MW_Totales",
                "Ingresos_Totales",
                "Utilidad_Acumulada",
            ]],
            {
                "MW_Totales": "{:,.0f} MW",
                "Ingresos_Totales": "${:,.2f}",
                "Utilidad_Acumulada": "${:,.2f}",
            },
        )

        csv_final = df_total.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Descargar Resultados Acumulados Finales (Excel / CSV)",
            data=csv_final,
            file_name="resultados_finales_subasta.csv",
            mime="text/csv",
        )
    else:
        st.info(
            "💡 Para calcular y mostrar la pantalla del Ganador Global, debes"
            " haber ejecutado el despacho económico tanto de la Ronda 1 como de"
            " la Ronda 2."
        )
