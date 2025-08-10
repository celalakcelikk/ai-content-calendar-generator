"""
Theme management for Streamlit app.

This module provides utilities to manage and apply custom themes to a Streamlit application.
It defines CSS variables for both light and dark modes, and injects the appropriate CSS into
the Streamlit app based on the selected theme mode. It also supports system theme auto-detection.

Functions
---------
apply_theme(mode: str = "System (Auto)") -> None
    Applies the selected theme to the Streamlit app by injecting CSS.
"""

from __future__ import annotations

import streamlit as st


def apply_theme(mode: str = "System (Auto)") -> None:
    """
    Apply a custom theme to the Streamlit app.

    Parameters
    ----------
    mode : str, optional
        The theme mode to apply. Can be "Light", "Dark", or "System (Auto)" (default).
        - "Light": Forces light theme.
        - "Dark": Forces dark theme.
        - "System (Auto)": Uses user's system preference for light/dark mode.

    Usage
    -----
    Call this function at the beginning of your Streamlit script to apply the desired theme:

        import theme
        theme.apply_theme("Dark")

    The function injects CSS variables and styles into the app to control colors, backgrounds,
    and component appearance according to the selected theme.
    """
    light_vars = """
        :root {
            --bg: #ffffff;
            --text: #111827;
            --muted-text: #6b7280;
            --accent: #3B82F6;
            --accent-hover: #2563EB;
            --sidebar-bg: #F7F7F9;
            --card-bg: #ffffff;
            --card-border: #E5E7EB;
            --card-accent: #93C5FD;
        }
    """
    dark_vars = """
        :root {
            --bg: #0f172a;
            --text: #e5e7eb;
            --muted-text: #9ca3af;
            --accent: #60A5FA;
            --accent-hover: #3B82F6;
            --sidebar-bg: #0b1220;
            --card-bg: #111827;
            --card-border: #1f2937;
            --card-accent: #2563EB;
        }
    """
    base_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            color: var(--text);
            background-color: var(--bg);
        }
        [data-testid="stSidebar"] {
            background-color: var(--sidebar-bg);
            color: var(--text);
        }
        [data-testid="stSidebar"] * { color: var(--text) !important; }
        div.stButton > button {
            background-color: var(--accent);
            color: #fff;
            border-radius: 10px;
            padding: 0.55em 1.1em;
            font-weight: 500;
            border: 1px solid transparent;
            transition: background-color .15s ease, box-shadow .15s ease;
            box-shadow: 0 1px 2px rgba(0,0,0,.06);
        }
        div.stButton > button:hover {
            background-color: var(--accent-hover);
            box-shadow: 0 2px 6px rgba(37, 99, 235, .25);
        }
        .content-card {
            background-color: var(--card-bg);
            padding: 14px 16px;
            margin-bottom: 12px;
            border-radius: 12px;
            border: 1px solid var(--card-border);
            box-shadow: 0 1px 2px rgba(0,0,0,.04);
            position: relative;
        }
        .content-card::before {
            content: '';
            position: absolute;
            left: 0; top: 0; bottom: 0;
            width: 4px;
            background: var(--card-accent);
            border-top-left-radius: 12px;
            border-bottom-left-radius: 12px;
        }
    """

    if mode == "Light":
        theme_css = f"<style>{light_vars}\n{base_css}</style>"
    elif mode == "Dark":
        theme_css = f"<style>{dark_vars}\n{base_css}</style>"
    else:
        system_css = f"""
            <style>
            {light_vars}
            {base_css}
            @media (prefers-color-scheme: dark) {{
                {dark_vars}
            }}
            </style>
        """
        theme_css = system_css

    st.markdown(theme_css, unsafe_allow_html=True)
