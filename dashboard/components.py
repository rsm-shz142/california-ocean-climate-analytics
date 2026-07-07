from pathlib import Path
import base64
import streamlit as st


ASSETS_DIR = Path(__file__).resolve().parent / "assets"


def sidebar_brand():
    logo_path = ASSETS_DIR / "logo.svg"
    st.sidebar.image(str(logo_path), use_container_width=True)

    st.sidebar.markdown(
        """
        <div style="font-size: 0.78rem; color: #94A3B8; margin-top: -0.4rem; margin-bottom: 1rem;">
            Powered by NOAA Data
        </div>
        <hr>
        """,
        unsafe_allow_html=True,
    )


def hero_section():
    hero_path = ASSETS_DIR / "hero.png"

    with open(hero_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <div style="
            padding: 2rem;
            border-radius: 24px;
            background:
                linear-gradient(90deg, rgba(8,15,28,0.98) 0%, rgba(8,15,28,0.82) 48%, rgba(8,15,28,0.25) 100%),
                url('data:image/png;base64,{encoded}');
            background-size: cover;
            background-position: center;
            border: 1px solid #263244;
            margin-bottom: 1.5rem;
        ">
            <h1 style="font-size: 3rem; line-height: 1.05; margin-bottom: 0.5rem;">
                🌊 California Ocean<br>Climate Analytics <span style="color:#60A5FA;">Platform</span>
            </h1>
            <h3 style="color:#E5E7EB; margin-bottom: 1rem;">
                NOAA Ocean Intelligence Dashboard
            </h3>
            <p style="max-width: 680px; color:#CBD5E1; font-size: 1rem; line-height: 1.6;">
                An end-to-end business analytics project using official NOAA ocean observations
                to monitor California coast sea surface temperature, detect marine heatwave events,
                analyze ENSO climate variability, and forecast short-term regional SST.
            </p>
            <div style="display:flex; gap:1rem; margin-top:1.5rem; flex-wrap:wrap;">
                <div style="background:#0F172A; padding:0.8rem 1rem; border-radius:14px; border:1px solid #263244;">
                    <b>NOAA OISST v2.1</b><br><span style="color:#94A3B8;">Sea Surface Temperature</span>
                </div>
                <div style="background:#0F172A; padding:0.8rem 1rem; border-radius:14px; border:1px solid #263244;">
                    <b>NOAA ONI</b><br><span style="color:#94A3B8;">Oceanic Niño Index</span>
                </div>
                <div style="background:#0F172A; padding:0.8rem 1rem; border-radius:14px; border:1px solid #263244;">
                    <b>1982–2024</b><br><span style="color:#94A3B8;">43 Years of Data</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(icon: str, title: str, text: str, accent: str = "#60A5FA"):
    st.markdown(
        f"""
        <div style="
            padding: 1.25rem;
            border-radius: 18px;
            background: linear-gradient(135deg, #111827, #0F172A);
            border: 1px solid #263244;
            min-height: 175px;
        ">
            <div style="font-size: 2rem;">{icon}</div>
            <div style="font-size: 1.15rem; font-weight: 800; margin-top: 0.5rem; color:{accent};">
                {title}
            </div>
            <div style="font-size: 0.92rem; color: #CBD5E1; margin-top: 0.55rem; line-height: 1.45;">
                {text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def snapshot_card(label: str, value: str, subtext: str = ""):
    st.markdown(
        f"""
        <div style="
            padding: 1rem;
            border-left: 1px solid #263244;
            min-height: 95px;
        ">
            <div style="font-size: 0.8rem; color:#94A3B8;">{label}</div>
            <div style="font-size: 1.6rem; font-weight: 800; margin-top: 0.25rem;">{value}</div>
            <div style="font-size: 0.78rem; color:#64748B; margin-top: 0.2rem;">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_intro(title: str, text: str):
    st.subheader(title)
    if text:
        st.markdown(
            f"""
            <div style="color: #CBD5E1; font-size: 1rem; margin-bottom: 1rem;">
                {text}
            </div>
            """,
            unsafe_allow_html=True,
        )
