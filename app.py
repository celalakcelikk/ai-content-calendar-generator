"""
AI Content Calendar Planner app (Streamlit).

This module wires the Streamlit UI, applies theming, orchestrates AI calls,
and renders/downloads the generated content plan. Helper functions are kept
in-module for clarity.

Notes
-----
- The app persists the latest generated DataFrame in ``st.session_state.df`` so
  that download clicks (which trigger a rerun) do not clear the plan.
- AI responses are requested in JSON but the parser is resilient to code-fence
formatting and stray text.

Examples
--------
Run the application locally::

    streamlit run app.py
"""

import json
from pathlib import Path
import sys
from typing import Any

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.core.constants import WEEK_DAYS
from src.core.schedule import generate_dates, week_index
from src.services.ai import generate_post_idea
from src.services.export import to_csv_bytes, to_excel_bytes
from src.services.logging import configure_logging, get_logger
from src.ui.layout import sidebar_inputs


# then non-import module code
sys.path.append(str(Path(__file__).resolve().parent / "src"))
load_dotenv()
configure_logging()
logger = get_logger(__name__)

configure_logging()
logger = get_logger(__name__)

st.set_page_config(page_title="AI Content Calendar Planner", layout="wide")
st.title("📅 AI Content Calendar Planner")
st.markdown("Plan and generate **high-quality content ideas** using AI.")

# Sidebar & theme
inputs = sidebar_inputs()

# --- Helpers ---------------------------------------------------------------


def _parse_ai_json(text: str) -> dict[str, Any] | None:
    """
    Parse a model response into JSON.

    Attempts to parse ``text`` as a JSON object while being lenient with common
    LLM response patterns (e.g., fenced code blocks such as `````json ... ````` or
    extra prose surrounding the JSON). If a valid JSON object cannot be recovered,
    ``None`` is returned.

    Parameters
    ----------
    text : str
        Raw response returned by the model.

    Returns
    -------
    Optional[Dict[str, Any]]
        Parsed JSON object if successful; otherwise ``None``.

    Examples
    --------
    >>> _parse_ai_json('{"title": "T", "description": "D", "hashtags": []}')
    {'title': 'T', 'description': 'D', 'hashtags': []}
    """
    logger.debug(f"Parsing AI JSON response, raw text length: {len(text) if text else 0}")
    if not text:
        logger.warning("Empty text received for JSON parsing.")
        return None
    cleaned = str(text).strip()
    # Strip code fences like ```json ... ```
    if cleaned.startswith("```") and cleaned.endswith("```"):
        cleaned = cleaned.strip("`\n ")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].lstrip()
    # First, try direct JSON
    try:
        result = json.loads(cleaned)
        logger.debug("Successfully parsed JSON from AI response.")
        return result
    except Exception:
        pass
    # Fallback: try to find outermost {...}
    try:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            result = json.loads(cleaned[start : end + 1])
            logger.debug("Successfully parsed JSON from AI response using fallback.")
            return result
    except Exception:
        logger.warning("Failed to parse AI response as JSON.")
        return None
    logger.warning("Failed to parse AI response as JSON.")
    return None


def _generate_rows(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Generate calendar rows from user inputs.

    Builds a list of row dictionaries representing scheduled content items.
    When ``use_ai`` is enabled, each row is enriched using the model output which
    is parsed via :func:`_parse_ai_json` with a robust fallback to heuristic parsing.

    Parameters
    ----------
    inputs : Dict[str, Any]
        Dictionary produced by the sidebar form. Expected keys include
        ``topic``, ``audience``, ``frequency``, ``duration``, ``custom_days``,
        ``platform``, ``tone``, ``use_ai``, and ``model_name``.

    Returns
    -------
    List[Dict[str, Any]]
        Rows containing columns: ``Date``, ``Week Index``, ``Platform``, ``Topic``,
        ``Audience``, ``Tone``, ``Title``, ``Description``, ``Format``, ``Hashtags``.

    Notes
    -----
    - The function updates a progress bar to indicate generation progress.
    - Dates are computed via :func:`src.core.schedule.generate_dates`.
    """
    logger.info(
        "Inputs summary: topic=%r, audience=%r, frequency=%r, duration=%s, platforms=%s, "
        "tone=%r, use_ai=%s",
        inputs.get("topic"),
        inputs.get("audience"),
        inputs.get("frequency"),
        inputs.get("duration"),
        inputs.get("platform"),
        inputs.get("tone"),
        inputs.get("use_ai"),
    )
    # dates
    custom_idx = (
        [WEEK_DAYS.index(d) for d in inputs["custom_days"]]
        if inputs["frequency"] == "X times/week"
        else []
    )
    schedule_dates = generate_dates(
        frequency=inputs["frequency"],
        duration_weeks=inputs["duration"],
        custom_weekdays=custom_idx,
    )

    rows: list[dict[str, Any]] = []
    total = max(len(schedule_dates) * max(len(inputs["platform"]), 1), 1)
    done = 0
    progress = st.progress(0, text="Preparing…")

    for platform in inputs["platform"]:
        logger.debug(f"Processing platform: {platform}")
        for i, d in enumerate(schedule_dates, start=1):
            logger.debug(
                "Generating for date %s (index %s) on platform %s",
                d.strftime("%Y-%m-%d"),
                i,
                platform,
            )
            title = f"{inputs['topic']} — Idea #{i}"
            desc = (
                f"Post about {inputs['topic']} for {inputs['audience']} in {inputs['tone']} tone."
            )
            fmt = ""
            hashtags: list[str] = []

            logger.debug(
                "Calling generate_post_idea topic=%r audience=%r tone=%r platform=%r model=%r",
                inputs["topic"],
                inputs["audience"],
                inputs["tone"],
                platform,
                inputs.get("model_name"),
            )
            idea = generate_post_idea(
                inputs["topic"],
                inputs["audience"],
                inputs["tone"],
                platform,
                inputs.get("model_name"),
            )
            logger.debug("Received AI generated idea.")
            if idea:
                parsed = _parse_ai_json(str(idea))

                if isinstance(parsed, dict):
                    title = str(parsed.get("title") or title)[:120]
                    desc = str(parsed.get("description") or desc)[:600]
                    fmt = str(parsed.get("format") or "")[:40]
                    raw_tags = parsed.get("hashtags")
                    if isinstance(raw_tags, list):
                        hashtags = [str(x).strip() for x in raw_tags if str(x).strip()][:12]
                    elif isinstance(raw_tags, str):
                        hashtags = [t.strip() for t in raw_tags.split(",") if t.strip()][:12]
                else:
                    parts = [p.strip() for p in str(idea).split("\n") if p.strip()]
                    if parts:
                        title = parts[0][:120]
                        if len(parts) > 1:
                            desc = " ".join(parts[1:])[:600]

            rows.append(
                {
                    "Date": d.strftime("%Y-%m-%d"),
                    "Week Index": week_index(i, inputs["frequency"]),
                    "Platform": platform,
                    "Topic": inputs["topic"],
                    "Audience": inputs["audience"],
                    "Tone": inputs["tone"],
                    "Title": (
                        title.replace("**", "")
                        .replace("Title", "")
                        .replace(":", "")
                        .replace('"', "")
                    ),
                    "Description": (
                        desc.replace("**", "")
                        .replace("Short", "")
                        .replace("Description", "")
                        .replace(":", "")
                        .replace('"', "")
                    ),
                    "Format": fmt,
                    "Hashtags": ", ".join(hashtags) if hashtags else "",
                }
            )
            done += 1
            progress.progress(int(done / total * 100), text=f"Generating… {done}/{total}")

    logger.info(f"Generated {len(rows)} rows for content calendar.")
    return rows


if "df" not in st.session_state:
    st.session_state.df = None

if inputs["generate"]:
    logger.info("Content calendar generation triggered by user.")
    if not inputs["topic"] or not inputs["audience"] or not inputs["platform"]:
        logger.warning("Missing required fields for generation: topic, audience, or platform.")
        st.warning("⚠️ Please fill in all required fields.")
    else:
        st.success("✅ Here's your AI-generated content calendar:")

        rows = _generate_rows(inputs)
        df = pd.DataFrame(rows)
        logger.info(f"DataFrame created with shape: {df.shape}")
        st.session_state.df = df
        st.success("Plan generated. You can review and download it below.")

df = st.session_state.df
if df is not None:
    st.markdown("### 📊 Plan Overview")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="📥 Download CSV",
        data=to_csv_bytes(df),
        file_name="content_calendar.csv",
        mime="text/csv",
        key="dl_csv",
    )

    st.download_button(
        label="📘 Download XLSX",
        data=to_excel_bytes(df),
        file_name="content_calendar.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="dl_xlsx",
    )

    st.markdown("---")
    st.info("📩 Contact: celalakcelikk@gmail.com · www.linkedin.com/in/celalakcelik")
