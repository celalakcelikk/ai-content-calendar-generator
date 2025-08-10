"""Layout helpers for the Streamlit sidebar and inputs.

This module centralizes the sidebar controls and returns a single dictionary of
inputs used by the application. Docstrings follow the NumPy style for clarity.
"""

from __future__ import annotations

import os

import streamlit as st
from src.core.constants import FREQUENCIES, MODELS, PLATFORMS, TONES, WEEK_DAYS


def sidebar_inputs() -> dict:
    """Render the sidebar and collect user inputs.

    Returns
    -------
    dict
        Dictionary containing keys: ``theme_mode``, ``topic``, ``audience``,
        ``frequency``, ``duration``, ``custom_days``, ``platform``, ``tone``,
        ``use_ai``, ``model_name``, and ``generate``.

    Notes
    -----
    - ``use_ai`` reflects the state of the toggle "Generate AI titles & descriptions".
    - ``model_name`` is only provided when the toggle is enabled; otherwise it is ``None``.
    - If you want a default model when disabled, set it in the app layer using ``os.getenv``.
    """
    with st.sidebar:
        st.header("📅 Plan Settings")

        # Theme and general inputs
        theme_mode = st.selectbox("Theme", ["System (Auto)", "Light", "Dark"], index=0)
        topic = st.text_input("Topic", placeholder="e.g., Personal Finance")
        audience = st.text_input("Audience", placeholder="e.g., Young Professionals")

        # Planning controls
        frequency = st.selectbox("Content Frequency", FREQUENCIES, index=0)
        duration = st.slider("Duration (Weeks)", 1, 8, 2)

        custom_days: list[str] = []
        if frequency == "X times/week":
            custom_days = st.multiselect(
                "Days (custom)", WEEK_DAYS, default=["Monday", "Wednesday", "Friday"]
            )

        platform = st.multiselect("Platforms", PLATFORMS)
        tone = st.selectbox("Tone of Voice", TONES, index=0)

        # AI toggle and conditional model picker
        use_ai = st.toggle("Generate AI titles & descriptions", value=False)
        model_name = (
            st.selectbox("OpenAI Model", MODELS, index=0) if use_ai else os.getenv("DEFAULT_MODEL")
        )

        st.markdown("---")
        generate = st.button("🚀 Generate Plan")

        return {
            "theme_mode": theme_mode,
            "topic": topic,
            "audience": audience,
            "frequency": frequency,
            "duration": duration,
            "custom_days": custom_days,
            "platform": platform,
            "tone": tone,
            "use_ai": use_ai,
            "model_name": model_name,
            "generate": generate,
        }
