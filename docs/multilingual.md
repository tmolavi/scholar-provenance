# Multilingual Academic Writing & Typesetting Guide

ScholarProvenance is architected to produce publication-ready academic manuscripts in any natural language the agent model can generate.

## Three Language Tiers

```yaml
project:
  source_languages: ["en", "fa"]    # Languages of raw evidence inputs
  working_language: "en"            # Language for intermediate agent ledger
  paper_language: "fa"              # Final manuscript publication language
  writing_direction: "rtl"          # "rtl" or "ltr" (auto-detected if omitted)
```

## First-Class Right-to-Left (RTL) Support
For Persian (`fa`), Arabic (`ar`), and Urdu (`ur`), the layout engine automatically:
- Sets body and block direction to `rtl`.
- Selects dedicated typography (e.g., **Vazirmatn** for Persian, **Noto Sans Arabic** for Arabic).
- Employs bidirectional Unicode embedding (`unicode-bidi: embed`) for inline Latin technical terms, English acronyms, DOIs, and URLs.
- Aligns table headers, captions, and list markers to the right.
- Numbers pages and running headers appropriately.

## Terminology Localization
Do not perform mechanical word-for-word translation. Use established academic conventions:
- Persian: Use formal academic prose (فارسی معیار دانشگاهی) and standard Iranian Academy (فرهنگستان زبان و ادب فارسی) equivalents where standard in computer science.
- Turkish: Use standard Istanbul Turkish academic prose (akademik Türkçe).
- Azerbaijani: Use standard literary Azerbaijani (Azərbaycan ədəbi dili).
- Arabic: Use Modern Standard Academic Arabic (العربية الفصحى الأكاديمية).
