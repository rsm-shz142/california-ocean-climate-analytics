import streamlit as st


def kpi_card(icon: str, value: str, label: str):
    st.markdown(
        f"""
        <div style="
            padding: 1.1rem;
            border-radius: 16px;
            background-color: #111827;
            border: 1px solid #263244;
            min-height: 130px;
        ">
            <div style="font-size: 1.8rem;">{icon}</div>
            <div style="font-size: 1.7rem; font-weight: 700; margin-top: 0.3rem;">
                {value}
            </div>
            <div style="font-size: 0.9rem; color: #9CA3AF; margin-top: 0.2rem;">
                {label}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_intro(title: str, text: str):
    st.subheader(title)
    st.markdown(
        f"""
        <div style="color: #CBD5E1; font-size: 1rem; margin-bottom: 1rem;">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )
