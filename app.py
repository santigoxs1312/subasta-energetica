import random
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
    </style>
""",
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
        "df_despacho_completo": {},
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
    "Carbón": "⛏️️",
    "Gas": "🔥",
    "Diésel": "⛽",
}

COLOR_TIPO = {
    "FNCER": {
        "bg": "#ECFDF5",
        "border": "#059669",
        "text": "#064E3B",
        "badge": "Renovable No Convencional",
        "color_plot": "#10B981",
    },
    "Convencional": {
        "bg": "#EFF6FF",
        "border": "#2563EB",
        "text": "#1E3A8A",
        "badge": "Renovable Convencional",
        "color_plot": "#3B82F6",
    },
    "Térmica": {
        "bg": "#FEF2F2",
        "border": "#DC2626",
        "text": "#7F1D1D",
        "badge": "No Renovable / Térmica",
        "color_plot": "#EF4444",
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
    estado_global["df_despacho_completo"] = {}
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
    "Modo de Acceso:",
    ["Portal Jugador", "Panel Administrador", "Portal del Docente"],
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
                    "id": p["id"],
                    "nombre": p["nombre"],
                    "fuente": p["fuente"],
                    "tipo": p["tipo"],
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
                    estado_global["df_despacho_completo"][ronda_proc] = df

                    st.markdown(
                        "### 💰 Precio Marginal de Bolsa:"
                        f" **${precio_marginal:,.2f} COP/kWh**"
                    )
                    st.success("✅ ¡Despacho económico calculado con éxito! Puedes consultar los gráficos en el Portal del Docente.")

# ---------------------------------------------------------
# PORTAL DEL DOCENTE (VISUALIZACIÓN INTERACTIVA)
# ---------------------------------------------------------
elif rol == "Portal del Docente":
    st.subheader("👨‍🏫 Dashboard y Visualizaciones en Tiempo Real")
    
    ronda_doc = st.selectbox(
        "Seleccionar Escenario / Ronda para Visualización:",
        options=[1, 2],
        format_func=lambda x: INFO_RONDAS[x]["nombre"],
        index=estado_global["ronda_actual"] - 1,
    )
    
    info_r = INFO_RONDAS[ronda_doc]
    demanda_r = info_r["demanda"]
    precio_m = estado_global["precios_marginales"].get(ronda_doc, None)
    df_desp = estado_global["df_despacho_completo"].get(ronda_doc, None)
    
    if df_desp is None or df_desp.empty:
        st.info("ℹ️ El despacho económico para esta ronda aún no ha sido ejecutado desde el Panel Administrador.")
    else:
        mw_total_desp = df_desp["despachado_mw"].sum()
        
        # 1. Métricas Clave
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Escenario Activo", f"Ronda {ronda_doc}")
        m2.metric("Demanda Total System", f"{demanda_r:,} MW")
        m3.metric("Precio Marginal Bolsa", f"${precio_m:,.2f} COP/kWh")
        m4.metric("Energía Despachada", f"{mw_total_desp:,.0f} MW")
        
        st.divider()
        
        # 2. Curva de Merit Order (Oferta y Demanda)
        st.markdown("### 📈 Curva de Oferta (Orden de Mérito) vs. Demanda")
        
        fig = go.Figure()
        
        # Construcción de pasos para el gráfico de orden de mérito
        x_vals = [0]
        y_vals = [df_desp.iloc[0]["precio_oferta"]]
        hover_texts = ["Inicio"]
        
        for idx, row in df_desp.iterrows():
            prev_x = row["mw_previos"]
            curr_x = row["mw_acumulados"]
            p = row["precio_oferta"]
            
            # Crear trazo escalonado por tipo de fuente
            color = COLOR_TIPO.get(row["tipo"], {}).get("color_plot", "#64748B")
            
            fig.add_trace(go.Scatter(
                x=[prev_x, curr_x, curr_x],
                y=[p, p, p],
                mode='lines',
                line=dict(color=color, width=3),
                name=f"{row['nombre']} ({row['grupo']})",
                hovertemplate=(
                    f"<b>{row['nombre']}</b> ({row['grupo']})<br>" +
                    f"Fuente: {row['fuente']}<br>" +
                    f"Oferta: ${p:,.2f} COP/kWh<br>" +
                    f"Cap. Ofertada: {row['cap_disp']:.0f} MW<br>" +
                    f"MW Acumulados: {curr_x:.0f} MW<extra></extra>"
                )
            ))
            
        # Línea de Demanda
        fig.add_vline(
            x=demanda_r, 
            line_width=3, 
            line_dash="dash", 
            line_color="#DC2626",
            annotation_text=f"Demanda Target: {demanda_r} MW",
            annotation_position="top right"
        )
        
        # Línea de Precio Marginal
        fig.add_hline(
            y=precio_m, 
            line_width=2, 
            line_dash="dot", 
            line_color="#2563EB",
            annotation_text=f"Precio Bolsa: ${precio_m:,.2f}",
            annotation_position="bottom left"
        )

        fig.update_layout(
            title=f"Curva de Mérito Económico — {info_r['nombre']}",
            xaxis_title="Capacidad Acumulada (MW)",
            yaxis_title="Precio de Oferta (COP/kWh)",
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(color="#0F172A", size=12),
            showlegend=False,
            height=500,
            margin=dict(l=40, r=40, t=60, b=40),
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9')

        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # 3. Rendimiento y Resultados por Equipo
        st.markdown("### 🏆 Ranking de Resultados Financieros por Equipo")
        
        df_res_ronda = estado_global["resultados"].get(ronda_doc, pd.DataFrame())
        if not df_res_ronda.empty:
            df_res_sorted = df_res_ronda.sort_values(by="Utilidad_Neta", ascending=False)
            
            fig_bar = go.Figure(go.Bar(
                x=df_res_sorted["grupo"],
                y=df_res_sorted["Utilidad_Neta"],
                marker_color="#0284C7",
                text=[f"${val:,.0f}" for val in df_res_sorted["Utilidad_Neta"]],
                textposition='auto',
            ))
            
            fig_bar.update_layout(
                title="Utilidad Neta Obtenida (COP)",
                xaxis_title="Equipo",
                yaxis_title="COP",
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font=dict(color="#0F172A"),
                height=380,
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # 4. Tabla Detallada del Despacho
        st.markdown("### 📋 Desglose Detallado del Despacho de Generación")
        
        df_tabla = df_desp[[
            "grupo", "nombre", "fuente", "tipo", "cap_disp", "costo", 
            "precio_oferta", "despachado_mw", "ingreso", "utilidad"
        ]].copy()
        
        df_tabla.columns = [
            "Equipo", "Planta", "Fuente", "Tipo", "Cap. Disp (MW)", 
            "Costo (COP)", "Oferta (COP)", "MW Despachados", "Ingresos (COP)", "Utilidad (COP)"
        ]
        
        st.dataframe(
            df_tabla.style.format({
                "Cap. Disp (MW)": "{:,.0f}",
                "Costo (COP)": "${:,.2f}",
                "Oferta (COP)": "${:,.2f}",
                "MW Despachados": "{:,.0f}",
                "Ingresos (COP)": "${:,.2f}",
                "Utilidad (COP)": "${:,.2f}",
            }),
            use_container_width=True,
        )
