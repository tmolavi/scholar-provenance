"""Language-aware typography, script detection, and font resolution for ScholarProvenance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


RTL_LANGUAGES = {"fa", "ar", "ur", "he", "ps", "ku"}


@dataclass
class FontConfig:
    primary_font: str
    fallback_chain: List[str]
    google_font_url: Optional[str]
    sample_text: str
    script: str


FONT_PROFILES: Dict[str, FontConfig] = {
    "fa": FontConfig(
        primary_font="Vazirmatn",
        fallback_chain=["Sahel", "Shabnam", "Tahoma", "Noto Sans Arabic", "sans-serif"],
        google_font_url="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700;800&family=Fira+Code:wght@400;500&display=swap",
        sample_text="پیشرفت پژوهش بر پایه شواهد تجربی و اعتبارسنجی دقیق منابع",
        script="Arabic/Perso-Arabic",
    ),
    "ar": FontConfig(
        primary_font="Noto Sans Arabic",
        fallback_chain=["Amiri", "Geeza Pro", "Arial", "sans-serif"],
        google_font_url="https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;600;700&family=Fira+Code:wght@400;500&display=swap",
        sample_text="توثيق الأدلة العلمية والأبحاث الأكاديمية القابلة لإعادة الإنتاج",
        script="Arabic",
    ),
    "tr": FontConfig(
        primary_font="Inter",
        fallback_chain=["Helvetica Neue", "Arial", "sans-serif"],
        google_font_url="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap",
        sample_text="Gelişmiş kanıt temelli akademik araştırma ve doğrulanabilir yöntemler",
        script="Latin",
    ),
    "az": FontConfig(
        primary_font="Inter",
        fallback_chain=["Helvetica Neue", "Arial", "sans-serif"],
        google_font_url="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap",
        sample_text="Sübutlara əsaslanan elmi tədqiqat və dərcə hazır əlyazmalar",
        script="Latin",
    ),
    "en": FontConfig(
        primary_font="Inter",
        fallback_chain=["Crimson Pro", "Helvetica Neue", "Arial", "sans-serif"],
        google_font_url="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Fira+Code:wght@400;500&display=swap",
        sample_text="Evidence-driven academic inquiry, empirical rigor, and reproducible research",
        script="Latin",
    ),
}

DEFAULT_FONT_CONFIG = FONT_PROFILES["en"]


def detect_writing_direction(lang_code: str, override: Optional[str] = None) -> str:
    """Determine text direction (ltr or rtl)."""
    if override and override.lower() in ["ltr", "rtl"]:
        return override.lower()
    base_lang = lang_code.split("-")[0].lower() if lang_code else "en"
    return "rtl" if base_lang in RTL_LANGUAGES else "ltr"


def get_font_config(lang_code: str) -> FontConfig:
    """Resolve font profile and fallback hierarchy for a target language."""
    base_lang = lang_code.split("-")[0].lower() if lang_code else "en"
    return FONT_PROFILES.get(base_lang, DEFAULT_FONT_CONFIG)


def generate_css_font_family(config: FontConfig) -> str:
    """Generate CSS font-family string with full fallback chain."""
    fonts = [f'"{config.primary_font}"'] + [
        f'"{f}"' if " " in f else f for f in config.fallback_chain
    ]
    return ", ".join(fonts)


def generate_publication_css(
    lang_code: str = "en",
    direction_override: Optional[str] = None,
    for_print: bool = True,
) -> str:
    """Generate complete publication CSS stylesheet adhering to academic design system."""
    direction = detect_writing_direction(lang_code, direction_override)
    font_cfg = get_font_config(lang_code)
    font_family = generate_css_font_family(font_cfg)
    is_rtl = (direction == "rtl")

    text_align = "right" if is_rtl else "left"
    reverse_align = "left" if is_rtl else "right"

    import_font = f"@import url('{font_cfg.google_font_url}');" if font_cfg.google_font_url else ""

    css = f"""/* ScholarProvenance Academic Publication Design System */
{import_font}

@page {{
  size: A4;
  margin: 25mm 20mm 25mm 20mm;
  @top-right {{
    font-family: {font_family};
    font-size: 8pt;
    color: #64748b;
    content: "{'ScholarProvenance Preprint' if not is_rtl else 'پیش‌نویس پژوهشی ScholarProvenance'}";
  }}
  @bottom-center {{
    font-family: {font_family};
    font-size: 9pt;
    color: #475569;
    content: counter(page);
  }}
}}

@page :first {{
  @top-right {{ content: ""; }}
  @bottom-center {{ content: ""; }}
}}

:root {{
  --font-main: {font_family};
  --font-code: "Fira Code", monospace;
  --color-primary: #0f172a;
  --color-secondary: #334155;
  --color-muted: #64748b;
  --color-border: #cbd5e1;
  --color-bg-subtle: #f8fafc;
  --color-accent: #1e3a8a;
}}

body {{
  direction: {direction};
  text-align: {text_align};
  font-family: var(--font-main);
  font-size: 10.5pt;
  line-height: 1.65;
  color: var(--color-primary);
  background-color: #ffffff;
  margin: 0;
  padding: 0;
  -webkit-font-smoothing: antialiased;
}}

/* Cover & Title Section */
.paper-cover {{
  page-break-after: always;
  padding-top: 50mm;
  text-align: center;
}}

.paper-title {{
  font-size: 24pt;
  font-weight: 800;
  line-height: 1.25;
  color: var(--color-primary);
  margin-bottom: 8mm;
}}

.paper-subtitle {{
  font-size: 14pt;
  font-weight: 400;
  color: var(--color-muted);
  margin-bottom: 12mm;
}}

.paper-authors {{
  font-size: 11pt;
  font-weight: 600;
  color: var(--color-secondary);
  margin-bottom: 4mm;
}}

.author-affiliation {{
  font-size: 9.5pt;
  color: var(--color-muted);
  margin-bottom: 12mm;
}}

.paper-meta-badge {{
  display: inline-block;
  padding: 4px 12px;
  background-color: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 8.5pt;
  color: var(--color-muted);
  margin-top: 15mm;
}}

/* Abstract Block */
.abstract-block {{
  margin: 15mm auto 10mm auto;
  max-width: 90%;
  padding: 10mm 12mm;
  background-color: var(--color-bg-subtle);
  border-left: {'none' if is_rtl else '3px solid var(--color-accent)'};
  border-right: {'3px solid var(--color-accent)' if is_rtl else 'none'};
  border-radius: 2px;
}}

.abstract-title {{
  font-size: 11pt;
  font-weight: 700;
  text-align: center;
  margin-bottom: 4mm;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}

.abstract-text {{
  font-size: 9.5pt;
  line-height: 1.55;
  text-align: justify;
}}

.keywords-line {{
  margin-top: 4mm;
  font-size: 8.5pt;
  color: var(--color-muted);
}}

/* Headings */
h1, h2, h3, h4 {{
  color: var(--color-primary);
  font-weight: 700;
  page-break-after: avoid;
}}

h1 {{
  font-size: 16pt;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 2mm;
  margin-top: 10mm;
  margin-bottom: 4mm;
}}

h2 {{
  font-size: 13pt;
  margin-top: 7mm;
  margin-bottom: 3mm;
}}

h3 {{
  font-size: 11pt;
  margin-top: 5mm;
  margin-bottom: 2mm;
}}

p {{
  margin: 0 0 3.5mm 0;
  text-align: justify;
}}

/* Mixed RTL / LTR inline items */
.latin-inline, .code-inline, .doi-inline, .url-inline {{
  direction: ltr;
  unicode-bidi: embed;
  display: inline-block;
}}

code {{
  font-family: var(--font-code);
  font-size: 9pt;
  background-color: #f1f5f9;
  padding: 1px 4px;
  border-radius: 3px;
  direction: ltr;
  unicode-bidi: embed;
}}

pre {{
  font-family: var(--font-code);
  font-size: 8.5pt;
  background-color: #0f172a;
  color: #f8fafc;
  padding: 10px 14px;
  border-radius: 4px;
  overflow-x: auto;
  direction: ltr;
  text-align: left;
}}

pre code {{
  background-color: transparent !important;
  color: #f8fafc !important;
  padding: 0 !important;
  border-radius: 0;
}}

/* Tables */
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 6mm 0;
  font-size: 9pt;
  page-break-inside: avoid;
}}

th, td {{
  padding: 6px 10px;
  border-bottom: 1px solid var(--color-border);
  text-align: {text_align};
}}

th {{
  background-color: var(--color-bg-subtle);
  font-weight: 700;
  border-top: 1.5px solid var(--color-primary);
  border-bottom: 1.5px solid var(--color-primary);
}}

caption {{
  caption-side: top;
  font-size: 9pt;
  font-weight: 600;
  margin-bottom: 2mm;
  text-align: {text_align};
}}

/* Figures */
figure {{
  margin: 7mm 0;
  text-align: center;
  page-break-inside: avoid;
}}

figure img, figure svg {{
  max-width: 95%;
  height: auto;
  display: block;
  margin: 0 auto;
}}

figcaption {{
  font-size: 8.5pt;
  color: var(--color-muted);
  margin-top: 3mm;
}}

/* References */
.references-list {{
  list-style-type: none;
  padding-{ 'right' if is_rtl else 'left' }: 0;
  font-size: 9pt;
  line-height: 1.45;
}}

.references-list li {{
  margin-bottom: 3.5mm;
  padding-{ 'right' if is_rtl else 'left' }: 6mm;
  text-indent: -6mm;
}}
"""
    return css
