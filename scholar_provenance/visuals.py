"""Visual assets generation, pure SVG charting, architecture diagramming, and manifest tracking for ScholarProvenance."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class VisualAsset:
    asset_id: str
    type: str  # "architecture_diagram", "bar_chart", "line_chart", "pipeline_flow"
    title: str
    file_path: str
    source: str
    source_data: Optional[str] = None
    generated_by: str = "ScholarProvenance Pure-SVG Engine"
    license: str = "CC-BY-4.0"
    citation: Optional[str] = None
    creation_date: str = ""
    language: str = "en"
    alt_text: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def generate_bar_chart_svg(
    categories: List[str],
    series: Dict[str, List[float]],
    title: str,
    x_label: str = "Configurations",
    y_label: str = "Latency (ms)",
    width: int = 700,
    height: int = 380,
    is_rtl: bool = False,
) -> str:
    """Generate a high-resolution, peer-review-quality academic bar chart in pure SVG."""
    margin_top = 50
    margin_bottom = 60
    margin_left = 70
    margin_right = 140

    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom

    # Find maximum value for Y-axis scaling
    all_vals = [v for vals in series.values() for v in vals]
    max_val = max(all_vals) if all_vals else 1.0
    y_ceiling = max_val * 1.15

    palette = ["#1e3a8a", "#0284c7", "#0d9488", "#d97706", "#dc2626"]
    num_cats = len(categories)
    num_series = len(series)

    group_w = plot_w / max(num_cats, 1)
    bar_w = (group_w * 0.7) / max(num_series, 1)

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}" style="background:#ffffff; font-family: Inter, Vazirmatn, sans-serif;">',
        f'<text x="{width / 2}" y="28" font-size="14" font-weight="700" fill="#0f172a" text-anchor="middle">{title}</text>',
    ]

    # Gridlines and Y-axis ticks
    num_ticks = 5
    for i in range(num_ticks + 1):
        tick_val = (y_ceiling / num_ticks) * i
        y_pos = margin_top + plot_h - (tick_val / y_ceiling) * plot_h
        svg_parts.append(
            f'<line x1="{margin_left}" y1="{y_pos:.1f}" x2="{margin_left + plot_w}" y2="{y_pos:.1f}" stroke="#e2e8f0" stroke-width="1" />'
        )
        svg_parts.append(
            f'<text x="{margin_left - 10}" y="{y_pos + 4:.1f}" font-size="10" fill="#64748b" text-anchor="end">{tick_val:.1f}</text>'
        )

    # Y-axis label
    svg_parts.append(
        f'<text x="20" y="{margin_top + plot_h / 2}" font-size="11" fill="#475569" font-weight="600" text-anchor="middle" transform="rotate(-90 20 {margin_top + plot_h / 2})">{y_label}</text>'
    )

    # Draw Bars
    series_names = list(series.keys())
    for cat_idx, cat in enumerate(categories):
        center_x = margin_left + (cat_idx * group_w) + (group_w / 2)
        start_x = center_x - ((num_series * bar_w) / 2)

        for s_idx, (s_name, s_vals) in enumerate(series.items()):
            val = s_vals[cat_idx] if cat_idx < len(s_vals) else 0.0
            bar_h = (val / y_ceiling) * plot_h
            bx = start_x + (s_idx * bar_w)
            by = margin_top + plot_h - bar_h
            color = palette[s_idx % len(palette)]

            svg_parts.append(
                f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w - 2:.1f}" height="{bar_h:.1f}" fill="{color}" rx="2" />'
            )
            # Value on top of bar
            svg_parts.append(
                f'<text x="{bx + (bar_w - 2)/2:.1f}" y="{by - 4:.1f}" font-size="8.5" fill="#334155" text-anchor="middle">{val:.1f}</text>'
            )

        # X-axis label
        svg_parts.append(
            f'<text x="{center_x:.1f}" y="{margin_top + plot_h + 20}" font-size="10" fill="#334155" font-weight="500" text-anchor="middle">{cat}</text>'
        )

    # X-axis title
    svg_parts.append(
        f'<text x="{margin_left + plot_w / 2}" y="{height - 10}" font-size="11" fill="#475569" font-weight="600" text-anchor="middle">{x_label}</text>'
    )

    # Legend
    legend_x = margin_left + plot_w + 15
    for s_idx, s_name in enumerate(series_names):
        ly = margin_top + 20 + (s_idx * 22)
        color = palette[s_idx % len(palette)]
        svg_parts.append(
            f'<rect x="{legend_x}" y="{ly}" width="12" height="12" fill="{color}" rx="2" />'
        )
        svg_parts.append(
            f'<text x="{legend_x + 18}" y="{ly + 10}" font-size="10" fill="#1e293b">{s_name}</text>'
        )

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def generate_architecture_diagram_svg(
    title: str = "System Architecture & Evidence Pipeline",
    width: int = 720,
    height: int = 340,
    is_rtl: bool = False,
) -> str:
    """Generate a clean, publication-ready systems architecture diagram in pure SVG."""
    align = "right" if is_rtl else "left"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}" style="background:#ffffff; font-family: Inter, Vazirmatn, sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#475569" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="{width / 2}" y="28" font-size="13" font-weight="700" fill="#0f172a" text-anchor="middle">{title}</text>

  <!-- Layer 1: Ingestion Sources -->
  <rect x="30" y="55" width="190" height="230" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)" />
  <text x="125" y="80" font-size="11" font-weight="700" fill="#1e3a8a" text-anchor="middle">1. Empirical Ingestion</text>
  <rect x="45" y="95" width="160" height="35" rx="4" fill="#ffffff" stroke="#94a3b8" />
  <text x="125" y="117" font-size="9.5" fill="#0f172a" text-anchor="middle">Code Repositories &amp; AST</text>
  <rect x="45" y="140" width="160" height="35" rx="4" fill="#ffffff" stroke="#94a3b8" />
  <text x="125" y="162" font-size="9.5" fill="#0f172a" text-anchor="middle">Raw Benchmark Logs (CSV)</text>
  <rect x="45" y="185" width="160" height="35" rx="4" fill="#ffffff" stroke="#94a3b8" />
  <text x="125" y="207" font-size="9.5" fill="#0f172a" text-anchor="middle">Docs, Architecture &amp; Notes</text>
  <rect x="45" y="230" width="160" height="35" rx="4" fill="#ffffff" stroke="#94a3b8" />
  <text x="125" y="252" font-size="9.5" fill="#0f172a" text-anchor="middle">User Field Assertions</text>

  <!-- Arrow 1 to 2 -->
  <line x1="220" y1="170" x2="260" y2="170" stroke="#475569" stroke-width="1.8" marker-end="url(#arrow)" />

  <!-- Layer 2: Verification & Provenance Engine -->
  <rect x="265" y="55" width="200" height="230" rx="6" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.5" filter="url(#shadow)" />
  <text x="365" y="80" font-size="11" font-weight="700" fill="#0369a1" text-anchor="middle">2. Evidence &amp; Verification</text>
  <rect x="280" y="95" width="170" height="35" rx="4" fill="#ffffff" stroke="#38bdf8" />
  <text x="365" y="117" font-size="9.5" fill="#0f172a" text-anchor="middle">Evidence Ledger (Taxonomy)</text>
  <rect x="280" y="140" width="170" height="35" rx="4" fill="#ffffff" stroke="#38bdf8" />
  <text x="365" y="162" font-size="9.5" fill="#0f172a" text-anchor="middle">Scholarly Search (OpenAlex/arXiv)</text>
  <rect x="280" y="185" width="170" height="35" rx="4" fill="#ffffff" stroke="#38bdf8" />
  <text x="365" y="207" font-size="9.5" fill="#0f172a" text-anchor="middle">Zero-Fabrication Citation Audit</text>
  <rect x="280" y="230" width="170" height="35" rx="4" fill="#ffffff" stroke="#38bdf8" />
  <text x="365" y="252" font-size="9.5" fill="#0f172a" text-anchor="middle">Contradictory Evidence Mining</text>

  <!-- Arrow 2 to 3 -->
  <line x1="465" y1="170" x2="505" y2="170" stroke="#475569" stroke-width="1.8" marker-end="url(#arrow)" />

  <!-- Layer 3: Academic Artifacts -->
  <rect x="510" y="55" width="180" height="230" rx="6" fill="#fefce8" stroke="#fef08a" stroke-width="1.5" filter="url(#shadow)" />
  <text x="600" y="80" font-size="11" font-weight="700" fill="#854d0e" text-anchor="middle">3. Publication Artifacts</text>
  <rect x="525" y="95" width="150" height="35" rx="4" fill="#ffffff" stroke="#facc15" />
  <text x="600" y="117" font-size="9.5" fill="#0f172a" text-anchor="middle">Verified Manuscript (PDF)</text>
  <rect x="525" y="140" width="150" height="35" rx="4" fill="#ffffff" stroke="#facc15" />
  <text x="600" y="162" font-size="9.5" fill="#0f172a" text-anchor="middle">Editable DOCX &amp; HTML</text>
  <rect x="525" y="185" width="150" height="35" rx="4" fill="#ffffff" stroke="#facc15" />
  <text x="600" y="207" font-size="9.5" fill="#0f172a" text-anchor="middle">BibTeX &amp; Evidence Matrix</text>
  <rect x="525" y="230" width="150" height="35" rx="4" fill="#ffffff" stroke="#facc15" />
  <text x="600" y="252" font-size="9.5" fill="#0f172a" text-anchor="middle">Reproducibility Package</text>

  <!-- Bottom status note -->
  <text x="{width / 2}" y="315" font-size="9" fill="#64748b" text-anchor="middle">Traceable Data Flow: Raw Inputs &rarr; Verifiable Evidence Matrix &rarr; 12 Gate Checks &rarr; Archival Outputs</text>
</svg>"""
    return svg


class VisualManifestManager:
    """Manages visual assets manifest file (paper/assets/manifest.json)."""

    def __init__(self, manifest_path: Path):
        self.manifest_path = manifest_path
        self.assets: List[VisualAsset] = []
        self._load()

    def _load(self):
        if self.manifest_path.exists():
            try:
                data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
                self.assets = [VisualAsset(**item) for item in data.get("assets", [])]
            except Exception:
                self.assets = []

    def add_asset(self, asset: VisualAsset):
        if not asset.creation_date:
            asset.creation_date = datetime.now(timezone.utc).isoformat()
        # Deduplicate by asset_id
        self.assets = [a for a in self.assets if a.asset_id != asset.asset_id]
        self.assets.append(asset)
        self.save()

    def save(self):
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "1.0.0",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "assets": [a.to_dict() for a in self.assets],
        }
        self.manifest_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
