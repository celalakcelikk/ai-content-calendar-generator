"""
AI service functions for generating content ideas via OpenAI API.
"""

import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def openai_generate_post_idea(topic, audience, tone, platform, model_name):
    """
    Generate a social media post idea using the OpenAI API.

    Parameters
    ----------
    topic : str
        The main topic or subject of the post.
    audience : str
        The target audience for the content.
    tone : str
        The desired tone of the content (e.g., formal, casual).
    platform : str
        The social media platform for which the content is intended.
    model_name : str
        The OpenAI model name to use for generation.

    Returns
    -------
    str
        A JSON string containing the post idea with keys:
        'title', 'description', 'format', and 'hashtags'.

    Example
    -------
    {
      "title": "Boost Your Productivity with These Simple Tips",
      "description": "Discover easy ways to enhance your daily workflow and get more done.",
      "format": "text",
      "hashtags": ["#productivity", "#tips", "#workflow"]
    }
    """
    prompt = f"""
You are an AI content strategist.

Return the output ONLY as a valid JSON object with this exact structure:
{{
  "title": "Short, catchy title (max 80 chars)",
  "description": "1–2 sentences. Max 280 chars.",
  "format": "one of: text | image | reel | carousel | video | thread",
  "hashtags": ["#tag1", "#tag2", "#tag3"]
}}

Rules:
- Output MUST be valid JSON. No backticks, no markdown, no extra text.
- Keep language consistent with the user’s inputs.
- Respect length limits.
- Do not include any keys other than: title, description, format, hashtags.

Inputs:
- Topic: "{topic}"
- Audience: "{audience}"
- Tone: "{tone}"
- Platform: "{platform}"
    """
    response = openai.ChatCompletion.create(
        model=model_name, messages=[{"role": "user", "content": prompt}], temperature=0.7
    )
    return response.choices[0].message.content.strip()


def generate_post_idea(
    topic: str, audience: str, tone: str, platform: str, model_name: str | None = None
) -> str | None:
    """
    Generate a post idea by calling the OpenAI API wrapper function.

    Parameters
    ----------
    topic : str
        The main topic or subject of the post.
    audience : str
        The target audience for the content.
    tone : str
        The desired tone of the content.
    platform : str
        The social media platform for which the content is intended.
    model_name : Optional[str], optional
        The OpenAI model name to use for generation, by default None.

    Returns
    -------
    Optional[str]
        The JSON string of the post idea if successful; otherwise, None.

    Notes
    -----
    Returns None if the generation function is not available or if an exception occurs.
    """
    if not openai_generate_post_idea:
        return None
    try:
        return openai_generate_post_idea(topic, audience, tone, platform, model_name)
    except Exception:
        return None
