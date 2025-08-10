# 📅 AI Content Calendar Generator

**Plan · Create · Export —** An AI-powered content calendar generator.  
Plan dates based on your topic, target audience, tone, and platforms. Generate titles and descriptions using OpenAI, and export your schedule as CSV or XLSX.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python" />
  <img src="https://img.shields.io/badge/Framework-Streamlit-ff4b4b?logo=streamlit" />
  <img src="https://img.shields.io/badge/AI-OpenAI_API-412991?logo=openai" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>


## ✨ Features

- 🤖 **AI-Powered Generation** — Titles, descriptions, formats, and hashtag suggestions  
- 📆 **Flexible Scheduling** — Daily • Weekly • **X times/week (custom weekdays)**  
- 🎨 **Theme Options** — System (Auto) / Light / Dark  
- 📤 **Exports** — One-click **CSV** and **Excel** downloads  
- 🛠 **Production Ready** — ENV-based logging, unit tests, linting (ruff/black/pylint)


## 🎥 Demo
> Add a GIF or video here to showcase the app in action.  
> Example: `assets/demo.mp4` or a YouTube link.


## 📊 Example Output

### 📊 Example Output

| Date       | Week Index | Platform   | Topic           | Audience           | Tone         | Title                                                      | Description                                                                                                                                           | Format | Hashtags                                                                                      |
|------------|------------|------------|-----------------|--------------------|--------------|------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------------------------------------------------------------|
| 2025-08-11 | 1          | X (Twitter)| Personal Finance| Young Professionals| Professional | Master Your Money Tips for Young Professionals            | Boost your financial savvy with these essential tips tailored for young professionals.                                                               | thread | #PersonalFinance, #YoungPros, #MoneyManagement                                               |
| 2025-08-13 | 1          | X (Twitter)| Personal Finance| Young Professionals| Professional | Boost Your Financial Savvy Today!                          | Unlock financial success with smart strategies tailored for young professionals. Learn how to manage your money effectively.                          | thread | #PersonalFinance, #YoungProfessionals, #FinancialLiteracy                                   |
| 2025-08-15 | 1          | X (Twitter)| Personal Finance| Young Professionals| Professional | Master Your Money Tips for Young Professionals            | Discover essential personal finance strategies tailored for young professionals to boost financial stability and growth.                              | thread | #PersonalFinance, #YoungPros, #MoneyMatters                                                  |
| 2025-08-11 | 1          | TikTok     | Personal Finance| Young Professionals| Professional | Master Your Money in Your 20s!                             | Discover essential tips for young professionals to manage finances effectively. Learn to budget, save, and invest smartly.                            | video  | #PersonalFinance, #YoungProfessionals, #MoneyTips                                            |
| 2025-08-13 | 1          | TikTok     | Personal Finance| Young Professionals| Professional | Master Your Money Personal Finance Tips                    | Learn professional strategies to manage your finances effectively and secure your future. Perfect for young professionals aiming for financial success.| reel   | #PersonalFinance, #YoungProfessionals, #MoneyManagement                                     |
| 2025-08-15 | 1          | TikTok     | Personal Finance| Young Professionals| Professional | Mastering Personal Finance for Young Pros                  | Learn essential tips to manage your finances and secure your future. Perfect for young professionals aiming for financial independence.               | video  | #PersonalFinance, #YoungProfessionals, #FinancialIndependence                               |

## 📂 Project Structure

```
ai-content-calendar-generator/
├─ app.py                         # Main Streamlit app: UI flow, AI calls, export & theme integration
├─ pyproject.toml                 # Ruff/Black configuration (line-length, target-version, etc.)
├─ requirements.txt               # Python dependencies
├─ scripts/
│  ├─ quality.sh                  # Code quality & tests (ruff, black --check, pylint, pytest)
│  └─ run.sh                      # Runs the app (optional .env loading)
├─ src/
│  ├─ core/
│  │  ├─ constants.py             # Constants: FREQUENCIES, WEEK_DAYS, PLATFORMS, TONES, MODELS
│  │  └─ schedule.py              # Date generation (Daily / 3x/week / Weekly / X times/week) & week_index
│  ├─ services/
│  │  ├─ ai.py                    # OpenAI integration layer (generate_post_idea wrapper)
│  │  ├─ export.py                # DataFrame → CSV/XLSX byte stream (for download_button)
│  │  └─ logging.py               # ENV-based logging (LOG_LEVEL, LOG_FILE, etc.) + time_block utils
│  └─ ui/
│     ├─ layout.py                # Sidebar inputs: topic, audience, frequency, platform, tone, AI toggle & model
│     └─ theme.py                 # Light/Dark/System CSS themes, Google Fonts, button/card styles
└─ tests/
   ├─ conftest.py                 # Pytest fixtures (e.g., temporary OPENAI_API_KEY env)
   └─ test_schedule.py            # Unit tests for generate_dates
```


## ⚙️ Installation

```bash
# 1) Virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Dependencies
pip install -r requirements.txt

# 3) Environment variables (optional but recommended)
cp .env.example .env
# Add your OPENAI_API_KEY and DEFAULT_MODEL to .env

# 4) Run the app
streamlit run app.py
# or
bash scripts/run.sh
```


## 🖥 Usage

1. Choose **topic**, **target audience**, **frequency**, **duration**, **platform(s)**, and **tone** from the sidebar.  
2. Toggle **"Generate AI titles & descriptions"** to enable AI mode and select a model.  
3. Click **"Generate Plan"** to create the content calendar.  
4. Download the schedule as **CSV** or **XLSX**.


## 🔑 Environment Variables

From `.env.example`:

```env
OPENAI_API_KEY=your_api_key_here
DEFAULT_MODEL=gpt-4o-mini

# Logging (optional)
LOG_LEVEL=INFO
LOG_TO_CONSOLE=1
LOG_FILE=app.log
LOG_MAX_BYTES=1000000
LOG_BACKUPS=3
LOG_FORMAT=%(asctime)s | %(levelname)s | %(name)s | %(message)s
LOG_DATEFMT=%Y-%m-%d %H:%M:%S
```

- Without `OPENAI_API_KEY`, AI features are disabled.
- Logging configuration is fully adjustable via environment variables.


## 🧪 Quality & Tests

```bash
# One command for all checks:
bash scripts/quality.sh

# Or manually:
ruff check . --fix
black . --line-length 100
pylint $(git ls-files '*.py' | tr '\n' ' ')
pytest -q
```

> `ruff` → fast linter, `black` → formatting, `pylint` → deep analysis, `pytest` → tests.


## 🗺 Roadmap

- Grid calendar view with color-coded entries  
- PDF/Markdown export  
- Multi-language support (EN/TR)  
- Platform-specific prompt packs  
- No-code integrations (Make.com / Zapier)


## 📜 License

MIT © 2025 Celal Akçelik
