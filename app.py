import random
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL Y ESTILO
# ---------------------------------------------------------
st.set_page_config(
    page_title="Subasta Energética - ICESI", page_icon="⚡", layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    .main-header {
        font-size:2.2rem;
        color:#38BDF8;
        text-align:center;
        font-weight:bold;
        margin-bottom:5px;
    }
    .sub-header {
        font-size:1.05rem;
        color:#9CA3AF;
        text-align:center;
        margin-bottom:20px;
    }
    .round-badge {
        background-color: #1E293B;
        border: 1px solid #38BDF8;
        color: #38BDF8;
        padding: 12px 18px;
        border-radius: 12px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .winner-card {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
        border: 2px solid #F59E0B;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
    }
    .locked-card {
        background-color: #371B1E;
        border: 1px solid #EF4444;
        color: #FCA5A5;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .result-card {
        background-color: #0F172A;
        border: 1px solid #10B981;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# ESTADO GLOBAL DE LA APLICACIÓN (MEMORIA DE SERVIDOR)
# ---------------------------------------------------------
@st.cache_resource
def obtener_estado_global():
  return {
      "asignacion": {},
      "ronda_actual": 1,
      "ofertas": {},  # Dict con llaves (ronda, planta_id)
      "bloqueados": {},  # Dict con llaves (ronda, grupo)
      "resultados": {},  # DataFrames resúmenes por ronda
      "precios_marginales": {},  # Guarda el precio marginal por ronda
  }


estado_global = obtener_estado_global()

# ---------------------------------------------------------
# BASE DE DATOS Y CONFIGURACIÓN DE PLANTAS
# ---------------------------------------------------------
PLANTAS_SISTEMA = [
    # FNCER / Renovables No Convencionales (5)
    {
        "id": "G1",
        "nombre": "Sol Radiante 1",
        "fuente": "Solar",
        "tipo": "FNCER",
        "cap_nom": 80,
        "costo": 40000,
    },
    {
        "id": "G2",
        "nombre": "Sol Radiante 2",
        "fuente": "Solar",
        "tipo": "FNCER",
        "cap_nom": 80,
        "costo": 40000,
    },
    {
        "id": "G3",
        "nombre": "HeliOS 3",
        "fuente": "Solar",
        "tipo": "FNCER",
        "cap_nom": 100,
        "costo": 50000,
    },
    {
        "id": "G4",
        "nombre": "Vientos del Norte 1",
        "fuente": "Eólica",
        "tipo": "FNCER",
        "cap_nom": 120,
        "costo": 60000,
    },
    {
        "id": "G5",
        "nombre": "Vientos del Norte 2",
        "fuente": "Eólica",
        "tipo": "FNCER",
        "cap_nom": 120,
        "costo": 60000,
    },
    # Renovables Convencionales (5)
    {
        "id": "G6",
        "nombre": "Río Vivo 1",
        "fuente": "Hidro Filo",
        "tipo": "Convencional",
        "cap_nom": 100,
        "costo": 80000,
    },
    {
        "id": "G7",
        "nombre": "Río Vivo 2",
        "fuente": "Hidro Filo",
        "tipo": "Convencional",
        "cap_nom": 100,
        "costo": 80000,
    },
    {
        "id": "G8",
        "nombre": "Embalse Central 1",
        "fuente": "Hidro Embalse",
        "tipo": "Convencional",
        "cap_nom": 150,
        "costo": 120000,
    },
    {
        "id": "G9",
        "nombre": "Embalse Central 2",
        "fuente": "Hidro Embalse",
        "tipo": "Convencional",
        "cap_nom": 150,
        "costo": 140000,
    },
    {
        "id": "G10",
        "nombre": "Embalse El Salto",
        "fuente": "Hidro Embalse",
        "tipo": "Convencional",
        "cap_nom": 200,
        "costo": 160000,
    },
    # Térmicas / No Renovables (5)
    {
        "id": "G11",
        "nombre": "Térmica Carbón A",
        "fuente": "Carbón",
        "tipo": "Térmica",
        "cap_nom": 150,
        "costo": 280000,
    },
    {
        "id": "G12",
        "nombre": "Térmica Carbón B",
        "fuente": "Carbón",
        "tipo": "Térmica",
        "cap_nom": 150,
        "costo": 300000,
    },
    {
        "id": "G13",
        "nombre": "TermoGas 1",
        "fuente": "Gas",
        "tipo": "Térmica",
        "cap_nom": 200,
        "costo": 380000,
    },
    {
        "id": "G14",
        "nombre": "TermoGas 2",
        "fuente": "Gas",
        "tipo": "Térmica",
        "cap_nom": 200,
        "costo": 420000,
    },
    {
        "id": "G15",
        "nombre": "TermoDiésel Pico",
        "fuente": "Diésel",
        "tipo": "Térmica",
        "cap_nom": 150,
        "costo": 600000,
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
        "bg": "#064e3b",
        "border": "#10B981",
        "badge": "Renovable No Convencional",
    },
    "Convencional": {
        "bg": "#1e3a8a",
        "border": "#3B82F6",
        "badge": "Renovable Convencional",
    },
    "Térmica": {
        "bg": "#7f1d1d",
        "border": "#EF4444",
        "badge": "No Renovable / Térmica",
    },
}

INFO_RONDAS = {
    1: {
        "nombre": "Ronda 1: Hidrología Alta / Soleado",
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
    '<div class="main-header">⚡ Subasta Energética - ICESI INNTERACTIVA</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Mercado de Energía Mayorista | Determinación del'
    " Precio Marginal de Bolsa</div>",
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
            📢 <b>ESCENARIO ACTIVO: {info_ronda['nombre'].upper()}</b><br>
            <span style="font-size:0.9em; font-weight:normal; color:#D1D5DB;">{info_ronda['descripcion']}</span>
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
              <b>🔒 Ofertas Registradas:</b> Las ofertas del <b>{grupo_sel}</b> para la <b>{info_ronda['nombre']}</b> ya fueron enviadas al servidor. Por favor espera a que el docente ejecute el despacho económico.
          </div>
          """,
          unsafe_allow_html=True,
      )

      st.markdown("### 📋 Resumen de Ofertas Enviadas para esta Ronda:")
      for (r, p_id), off in estado_global["ofertas"].items():
        if r == ronda_act and off["grupo"] == grupo_sel:
          icono = ICONOS_FUENTE.get(off["fuente"], "⚡")
          kwh_equivalent = off["precio_oferta"] / 1000.0
          # RENDERIZADO EN MARKDOWN PURO PARA EVITAR ERRORES DE SINTAXIS/ETIQUETAS
          st.markdown(
              f"• **{icono} {off['nombre']}** ({off['fuente']}):"
              f" **${off['precio_oferta']:,.0f} COP/MWh**"
              f" (*${kwh_equivalent:,.1f} COP/kWh*) — Cap. Disp:"
              f" **{off['cap_disp']:.0f} MW**"
          )

      # MOSTRAR RESULTADOS SI EL DOCENTE YA EJECUTÓ EL DESPACHO
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
                  <h3 style="color:#10B981; margin:0;">📊 Resultados de tu Equipo — {info_ronda['nombre']}</h3>
                  <p style="margin:5px 0;"><b>Precio Marginal de Bolsa:</b> ${precio_m:,.2f} COP/MWh (${precio_m/1000:,.1f} COP/kWh)</p>
                  <hr style="border-color:#374151;">
                  <p>⚡ <b>Energía Despachada:</b> {mw_desp:,.0f} MW</p>
                  <p>💵 <b>Ingresos Totales:</b> ${ingresos:,.2f} COP</p>
                  <p>📈 <b>Utilidad Neta Obtenida:</b> <span style="font-size:1.2em; color:#F59E0B; font-weight:bold;">${utilidad:,.2f} COP</span></p>
              </div>
              """,
              unsafe_allow_html=True,
          )

    else:
      plantas_equipo = estado_global["asignacion"].get(grupo_sel, [])
      st.info(
          "📍 Ingresa la tarifa por MWh para tus 3 generadoras. (Ejemplo:"
          " $400,000 COP/MWh equivale a $400 COP/kWh)."
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
        costo_kwh = p["costo"] / 1000.0

        st.markdown(
            f"""
            <div style="background-color: {estilo['bg']}; border-left: 6px solid {estilo['border']}; padding: 12px; border-radius: 8px; margin-bottom: 12px;">
                <h4 style="margin:0; color: #FFFFFF;">{icono} {p['nombre']} — <span style="font-size: 0.85em; opacity: 0.9;">{estilo['badge']}</span></h4>
                <p style="margin:4px 0 0 0; color: #E5E7EB; font-size:0.95em;">
                    Fuente: <b>{p['fuente']}</b> | Capacidad Disp.: <b>{cap_disp:.0f} MW</b> | Costo Base: <b>${p['costo']:,.0f} COP/MWh</b> (${costo_kwh:,.1f} COP/kWh)
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        precio = st.number_input(
            f"Precio de Oferta para {p['nombre']} (COP/MWh)",
            min_value=0.0,
            max_value=2000000.0,
            value=float(p["costo"]),
            step=5000.0,
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
    st.warning("⚠️ Debes ingresar la clave para acceder al panel de control.")
  else:
    st.success("🔓 Sesión de Administrador Activa.")

    # CONTROLES SUPERIORES
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

          df["ingreso"] = df["despachado_mw"] * precio_marginal
          df["costo_total"] = df["despachado_mw"] * df["costo"]
          df["utilidad"] = df["ingreso"] - df["costo_total"]

          # Resumen agrupado por equipos
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

          precio_kwh = precio_marginal / 1000.0
          st.markdown(
              "### 💰 Precio Marginal de Bolsa:"
              f" **${precio_marginal:,.2f} COP/MWh** (${precio_kwh:,.1f}"
              " COP/kWh)"
          )

          # CURVA DE MÉRITO (PLOTLY)
          fig = go.Figure()

          for idx, row in df.iterrows():
            if row["despachado_mw"] == row["cap_disp"]:
              color = "#10B981"  # Verde
              estado_desc = "Totalmente Despachada"
            elif row["despachado_mw"] > 0:
              color = "#F59E0B"  # Naranja
              estado_desc = (
                  f"Parcialmente Despachada ({row['despachado_mw']:.0f} MW)"
              )
            else:
              color = "#EF4444"  # Rojo
              estado_desc = "No Despachada"

            icono = ICONOS_FUENTE.get(row["fuente"], "⚡")
            fig.add_trace(
                go.Scatter(
                    x=[
                        row["mw_previos"],
                        row["mw_acumulados"],
                        row["mw_acumulados"],
                        row["mw_previos"],
                    ],
                    y=[0, 0, row["precio_oferta"], row["precio_oferta"]],
                    fill="toself",
                    fillcolor=color,
                    opacity=0.65,
                    line=dict(color=color, width=2),
                    name=f"{row['nombre']}",
                    text=(
                        f"{icono} {row['nombre']} ({row['grupo']})<br>Estado:"
                        f" {estado_desc}<br>Oferta: ${row['precio_oferta']:,.0f}"
                        f" COP/MWh<br>Despachado: {row['despachado_mw']:.0f} /"
                        f" {row['cap_disp']:.0f} MW"
                    ),
                    hoverinfo="text",
                )
            )

          fig.add_vline(
              x=demanda,
              line_dash="dash",
              line_color="#38BDF8",
              annotation_text=f"Demanda {demanda} MW",
          )
          fig.add_hline(
              y=precio_marginal,
              line_dash="dot",
              line_color="#F59E0B",
              annotation_text=f"Precio Bolsa ${precio_marginal:,.0f}",
          )

          fig.update_layout(
              title=f"Curva de Mérito — {info_proc['nombre']}",
              xaxis_title="Potencia Acumulada (MW)",
              yaxis_title="Precio Ofertado (COP/MWh)",
              paper_bgcolor="#000000",
              plot_bgcolor="#111827",
              font=dict(color="#FFFFFF"),
              showlegend=False,
              height=480,
          )
          st.plotly_chart(fig, use_container_width=True)

          st.subheader("🏆 Resultados Financieros de la Ronda Actual")
          st.dataframe(
              resumen.sort_values(
                  by="Utilidad_Neta", ascending=False
              ).style.format({
                  "MW_Despachados": "{:,.0f} MW",
                  "Ingresos": "${:,.2f}",
                  "Utilidad_Neta": "${:,.2f}",
              }),
              hide_index=True,
              use_container_width=True,
          )

          # BOTÓN PARA DESCARGAR EXCEL / CSV DE LA RONDA
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
              <h1 style="color: #F59E0B; margin:0;">🥇 ¡GRAN CAMPEÓN DEL MERCADO! 🥇</h1>
              <h2 style="color: #FFFFFF; margin: 10px 0;">{ganador['grupo']}</h2>
              <h3 style="color: #10B981; margin:0;">Utilidad Acumulada: ${ganador['Utilidad_Acumulada']:,.2f} COP</h3>
          </div>
          """,
          unsafe_allow_html=True,
      )

      st.dataframe(
          df_total[[
              "grupo",
              "MW_Totales",
              "Ingresos_Totales",
              "Utilidad_Acumulada",
          ]].style.format({
              "MW_Totales": "{:,.0f} MW",
              "Ingresos_Totales": "${:,.2f}",
              "Utilidad_Acumulada": "${:,.2f}",
          }),
          hide_index=True,
          use_container_width=True,
      )

      # DESCARGAR TABLA FINAL EN EXCEL/CSV
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
