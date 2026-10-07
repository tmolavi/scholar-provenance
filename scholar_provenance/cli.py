"""Command Line Interface for ScholarProvenance."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import List, Optional
import yaml

from scholar_provenance import __version__
from scholar_provenance.schemas import validate_file
from scholar_provenance.ledger import EvidenceLedger
from scholar_provenance.search import unified_literature_search
from scholar_provenance.audit import audit_manuscript, generate_audit_report
from scholar_provenance.privacy import scan_directory, generate_privacy_report
from scholar_provenance.reviewer import generate_reviewer_1, generate_reviewer_2, generate_red_team_report
from scholar_provenance.gates import evaluate_project_gates, generate_confidence_report
from scholar_provenance.reproducibility import generate_reproducibility_package
from scholar_provenance.visuals import generate_bar_chart_svg, generate_architecture_diagram_svg, VisualAsset, VisualManifestManager
from scholar_provenance.generator import render_full_html_document, render_pdf_from_html, render_docx_manuscript
from scholar_provenance.publisher import get_publication_recommendations, publish_release


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize a research project directory."""
    target = Path(args.path or ".").resolve()
    target.mkdir(parents=True, exist_ok=True)

    manifest_file = target / "research-project.yml"
    if manifest_file.exists() and not args.force:
        print(f"Error: {manifest_file} already exists. Use --force to overwrite.", file=sys.stderr)
        return 1

    authors = []
    if args.author:
        authors.append({
            "name": args.author,
            "affiliation": args.affiliation or "Independent Researcher",
            "email": args.email or "",
            "orcid": args.orcid or "",
            "corresponding": True,
        })

    input_repos = []
    input_files = []
    if args.sources:
        for s in args.sources.split(","):
            s_clean = s.strip()
            if s_clean.startswith("http") or "github.com" in s_clean:
                input_repos.append({"url_or_path": s_clean, "branch": "main", "description": "Primary user source"})
            elif s_clean:
                input_files.append(s_clean)

    manifest_content = {
        "project": {
            "title": args.title or "Empirical Study of Intelligent Systems",
            "authors": authors,
            "ai_assistance_disclosure": {
                "disclose": True,
                "declaration_text": "The authors used an AI agent running ScholarProvenance to assist in literature discovery, evidence ledger formatting, and citation verification. All claims, experimental data, and final manuscript sections were validated and approved by the human authors.",
            },
            "paper_language": args.lang or "en",
            "working_language": "en",
            "source_languages": ["en"],
            "citation_style": "ieee",
            "target_venue": args.venue or "arXiv",
            "research_type": args.type or "architecture",
            "publication_mode": "preprint",
        },
        "inputs": {
            "repositories": input_repos,
            "websites": [],
            "files": input_files,
            "datasets": [],
            "notes": [],
        },
        "research": {
            "external_search": True,
            "contradictory_evidence_search": True,
            "novelty_check": True,
            "citation_verification": "strict",
            "freshness_check": True,
            "freshness_window_years": 3,
        },
        "outputs": {
            "markdown": True,
            "latex": True,
            "bibtex": True,
            "evidence_ledger": True,
            "reproducibility_package": True,
        },
    }

    manifest_file.write_text(yaml.dump(manifest_content, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # Scaffolding directories
    for sub in [
        "research",
        "paper/assets",
        "validation",
        "reviews",
        "reproducibility/data",
        "reproducibility/scripts",
        "reproducibility/configs",
    ]:
        (target / sub).mkdir(parents=True, exist_ok=True)

    print(f"✅ Initialized ScholarProvenance project at {target}")
    print(f"   Manifest created: {manifest_file}")
    if not authors:
        print("   ⚠️ Note: Author information is unset. Please provide explicit human author names in research-project.yml.")
    return 0


def cmd_validate_manifest(args: argparse.Namespace) -> int:
    """Validate research-project.yml manifest."""
    manifest_path = Path(args.manifest).resolve()
    ok, errors = validate_file(manifest_path, "research-project.schema.json")
    if ok:
        print(f"✅ Manifest '{manifest_path.name}' is valid.")
        return 0
    else:
        print(f"❌ Manifest validation failed with {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"   - {err}", file=sys.stderr)
        return 1


def cmd_search(args: argparse.Namespace) -> int:
    """Search open scholarly indices."""
    print(f"🔍 Searching open scholarly literature for: '{args.query}'...")
    results = unified_literature_search(args.query, limit_per_source=args.limit, min_year=args.year)
    if not results:
        print("No literature records found or network unavailable.")
        return 0

    print(f"\nFound {len(results)} relevant scholarly record(s):\n")
    for idx, w in enumerate(results, start=1):
        author_str = ", ".join(w.authors[:3]) + (" et al." if len(w.authors) > 3 else "")
        year_str = f"({w.publication_year})" if w.publication_year else ""
        print(f"[{idx}] {w.title} {year_str}")
        print(f"    Authors: {author_str or 'Unknown'}")
        if w.venue:
            print(f"    Venue: {w.venue}")
        if w.doi:
            print(f"    DOI: {w.doi}")
        elif w.url:
            print(f"    URL: {w.url}")
        print(f"    Index: {w.source_index}")
        print()
    return 0


def cmd_ledger(args: argparse.Namespace) -> int:
    """Validate and format evidence ledger."""
    p = Path(args.file).resolve()
    if not p.exists():
        print(f"Error: Ledger file '{p}' not found.", file=sys.stderr)
        return 1

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        ledger = EvidenceLedger.from_dict(data)
    except Exception as e:
        print(f"Failed to load ledger: {e}", file=sys.stderr)
        return 1

    ok, errors = ledger.validate()
    if not ok:
        print("❌ Ledger validation failed against evidence.schema.json:", file=sys.stderr)
        for err in errors:
            print(f"   - {err}", file=sys.stderr)
        return 1

    print(f"✅ Evidence ledger valid: {len(ledger.claims)} claims, {len(ledger.sources)} sources.")

    if args.markdown:
        out_md = Path(args.markdown).resolve()
        ledger.save_markdown_matrix(out_md)
        print(f"   Generated Markdown evidence matrix: {out_md}")

    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    """Audit manuscript claims and citations."""
    manu_path = Path(args.manuscript).resolve()
    bib_path = Path(args.bib).resolve() if args.bib else None
    matrix_path = Path(args.matrix).resolve() if args.matrix else None

    try:
        passed, findings, stats = audit_manuscript(manu_path, bib_path, matrix_path)
    except Exception as e:
        print(f"Audit failed: {e}", file=sys.stderr)
        return 1

    report_md = generate_audit_report(findings, stats, manu_path.stem)

    if args.output:
        out_p = Path(args.output).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(report_md, encoding="utf-8")
        print(f"Audit report written to: {out_p}")

    if passed:
        print("✅ Citation and claim audit PASSED.")
        return 0
    else:
        print(f"⚠️ Audit detected {len(findings)} potential issue(s).", file=sys.stderr)
        for f in findings[:5]:
            print(f"   [Line {f.line_number}] {f.category}: {f.flagged_text} ({f.explanation})", file=sys.stderr)
        return 1 if any(f.category == "UNVERIFIED_OR_FABRICATED_CITATION" for f in findings) else 0


def cmd_scan_sensitive(args: argparse.Namespace) -> int:
    """Scan directory for sensitive information."""
    target_dir = Path(args.path or ".").resolve()
    passed, findings, stats = scan_directory(target_dir)

    report_md = generate_privacy_report(findings, stats)

    if args.output:
        out_p = Path(args.output).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(report_md, encoding="utf-8")
        print(f"Privacy report written to: {out_p}")

    if passed:
        print(f"✅ Privacy scan clean: {stats['files_scanned']} files scanned, 0 secrets found.")
        return 0
    else:
        print(f"❌ Privacy scan FAILED: {len(findings)} sensitive secret(s) found!", file=sys.stderr)
        for f in findings:
            print(f"   [{f.pattern_name}] {f.file_path}:{f.line_number} -> {f.redacted_preview}", file=sys.stderr)
        return 1


def cmd_review(args: argparse.Namespace) -> int:
    """Generate adversarial reviewer and red-team reports."""
    target_dir = Path(args.path or ".").resolve()
    matrix_path = target_dir / "research" / "evidence-matrix.json"
    if not matrix_path.exists():
        print("Error: research/evidence-matrix.json required for review generation.", file=sys.stderr)
        return 1

    data = json.loads(matrix_path.read_text(encoding="utf-8"))
    title = data.get("project_title", "Research Paper")
    claims = data.get("claims", [])
    sources = data.get("sources", [])

    rev1_text = generate_reviewer_1(title, "architecture", claims)
    rev2_text = generate_reviewer_2(title, "architecture", sources, [])
    redteam_text = generate_red_team_report(title, data)

    rev_dir = target_dir / "reviews"
    val_dir = target_dir / "validation"
    rev_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)

    (rev_dir / "reviewer-1.md").write_text(rev1_text, encoding="utf-8")
    (rev_dir / "reviewer-2.md").write_text(rev2_text, encoding="utf-8")
    (val_dir / "red-team.md").write_text(redteam_text, encoding="utf-8")

    print("✅ Generated adversarial reviews:")
    print(f"   - {rev_dir / 'reviewer-1.md'}")
    print(f"   - {rev_dir / 'reviewer-2.md'}")
    print(f"   - {val_dir / 'red-team.md'}")
    return 0


def cmd_check_gates(args: argparse.Namespace) -> int:
    """Check 12 quality gates and produce confidence report."""
    target_dir = Path(args.path or ".").resolve()
    all_passed, results, readiness = evaluate_project_gates(target_dir)

    report_md = generate_confidence_report(target_dir.name, results, readiness)
    val_dir = target_dir / "validation"
    val_dir.mkdir(parents=True, exist_ok=True)
    out_file = val_dir / "research-confidence.md"
    out_file.write_text(report_md, encoding="utf-8")

    print(f"Research Confidence Report written to: {out_file}")
    print(f"Readiness Status: [{readiness}]")
    passed_count = sum(1 for r in results if r.passed)
    print(f"Quality Gates: {passed_count} / {len(results)} passed.")

    for r in results:
        sym = "✅" if r.passed else "❌"
        print(f"  {sym} {r.gate_id}: {r.title} ({r.status_label})")

    return 0 if readiness in ["READY", "READY_WITH_LIMITATIONS"] else 1


def cmd_package(args: argparse.Namespace) -> int:
    """Package reproducibility artifacts and checksums."""
    target_dir = Path(args.path or ".").resolve()
    success, summary_md, checksums = generate_reproducibility_package(target_dir)
    print(f"✅ Reproducibility package generated ({len(checksums)} artifacts checksummed).")
    return 0 if success else 1


def cmd_build(args: argparse.Namespace) -> int:
    """Build multi-format publication documents (HTML, PDF, DOCX, LaTeX)."""
    manu_p = Path(args.manuscript).resolve()
    if not manu_p.exists():
        print(f"Error: Manuscript '{manu_p}' not found.", file=sys.stderr)
        return 1

    manifest_p = Path(args.manifest).resolve() if args.manifest else manu_p.parent.parent / "research-project.yml"
    if not manifest_p.exists():
        manifest_p = manu_p.parent.parent / "research-project.yaml"

    manifest_data = {}
    if manifest_p.exists():
        try:
            manifest_data = yaml.safe_load(manifest_p.read_text(encoding="utf-8")) or {}
        except Exception as e:
            print(f"Warning: Failed to parse manifest {manifest_p}: {e}", file=sys.stderr)

    md_content = manu_p.read_text(encoding="utf-8")
    paper_dir = manu_p.parent

    # 1. HTML
    html_content = render_full_html_document(md_content, manifest_data)
    out_html = paper_dir / f"{manu_p.stem}.html"
    out_html.write_text(html_content, encoding="utf-8")
    print(f"✅ Built HTML: {out_html}")

    # 2. PDF (via WeasyPrint)
    if not args.no_pdf:
        out_pdf = paper_dir / f"{manu_p.stem}.pdf"
        ok_pdf = render_pdf_from_html(html_content, out_pdf, base_url=paper_dir)
        if ok_pdf:
            print(f"✅ Built PDF: {out_pdf}")
        else:
            print(f"❌ Failed to build PDF", file=sys.stderr)

    # 3. DOCX (via python-docx)
    if not args.no_docx:
        out_docx = paper_dir / f"{manu_p.stem}.docx"
        ok_docx = render_docx_manuscript(md_content, manifest_data, out_docx)
        if ok_docx:
            print(f"✅ Built DOCX: {out_docx}")

    return 0


def cmd_chart(args: argparse.Namespace) -> int:
    """Generate pure SVG academic chart or architecture diagram."""
    out_p = Path(args.output).resolve()
    out_p.parent.mkdir(parents=True, exist_ok=True)

    if args.type == "architecture":
        svg = generate_architecture_diagram_svg(title=args.title or "System Architecture", is_rtl=args.rtl)
    elif args.type == "bar":
        categories = [c.strip() for c in args.categories.split(",")] if args.categories else ["Baseline", "Proposed"]
        # Default sample or parsed
        series = {"Latency (ms)": [245.0, 48.5]}
        if args.series:
            try:
                series = json.loads(args.series)
            except Exception:
                pass
        svg = generate_bar_chart_svg(
            categories=categories,
            series=series,
            title=args.title or "Empirical Benchmark Comparison",
            x_label=args.xlabel or "Configuration",
            y_label=args.ylabel or "Latency (ms)",
            is_rtl=args.rtl,
        )
    else:
        print(f"Unknown chart type: {args.type}", file=sys.stderr)
        return 1

    out_p.write_text(svg, encoding="utf-8")
    print(f"✅ Generated SVG visual: {out_p}")
    return 0


def cmd_showcase(args: argparse.Namespace) -> int:
    """Prepare a voluntary submission for the ScholarProvenance community showcase."""
    print("=" * 70)
    print("ScholarProvenance Community Showcase Submission Preparer")
    print("=" * 70)
    print("This voluntary, privacy-respecting submission creates a submission file")
    print("that you can submit via GitHub Issues or Pull Requests.")
    print("No data is transmitted automatically or secretly.\n")

    title = input("Paper Title: ").strip() if not args.yes else "My Open Research Paper"
    paper_url = input("Public Paper / Preprint URL (or GitHub repo): ").strip() if not args.yes else "https://github.com/example/paper"
    authors = input("Author Names: ").strip() if not args.yes else "Independent Researcher"
    field_name = input("Research Field (e.g. AI Systems, Economics, GEO): ").strip() if not args.yes else "Computer Science"
    lang = input("Paper Language [en/fa/tr/az/ar]: ").strip() if not args.yes else "en"

    submission = {
        "title": title,
        "paper_url": paper_url,
        "authors": authors,
        "field": field_name,
        "language": lang or "en",
        "date_submitted": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "provenance_verified": True,
    }

    out_file = Path("showcase-submission.json").resolve()
    out_file.write_text(json.dumps(submission, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n✅ Created showcase submission manifest: {out_file}")
    print("\nNext steps to publish your entry:")
    print("1. Visit: https://github.com/tmolavi/scholar-provenance/issues/new?template=showcase.md")
    print("2. Paste the contents of showcase-submission.json into the issue.")
    print("3. Once approved, your project will be featured in SHOWCASE.md!")
    return 0


def cmd_publish(args: argparse.Namespace) -> int:
    """Execute autonomous publication, distribution bundling, or venue recommendation."""
    target_dir = Path(args.path or ".").resolve()

    if args.recommend:
        rec = get_publication_recommendations(target_dir)
        print("=" * 70)
        print("🎯 ScholarProvenance: Autonomous Publication & Venue Advisory")
        print("=" * 70)
        print(f"Title:         {rec['title']}")
        print(f"Authors:       {', '.join(rec['authors'])}")
        print(f"Research Type: {rec['research_type'].capitalize()}\n")

        print("📦 Recommended Open Science Preprints & Registries:")
        for a in rec["recommended_archives"]:
            print(f"  • {a['name']} ({a['category']}) - {a['suitability']}")

        print("\n🏛️ Recommended Peer-Review Venues:")
        for v in rec["recommended_venues"]:
            print(f"  • {v['venue']} [{v['type']}] ({v['cycle']})")

        print("\n🚀 Next Autonomous Actions:")
        for act in rec["next_autonomous_actions"]:
            print(f"  • {act}")
        return 0

    print(f"🚀 Executing publication pipeline for '{target_dir.name}' (Target: {args.target})...")
    res = publish_release(
        project_dir=target_dir,
        target=args.target,
        tag=args.tag,
        dry_run=args.dry_run,
    )

    print("\n✅ Publication Assets Generated:")
    print(f"   • Release Notes: {res['release_notes_file']}")
    print(f"   • Zenodo Metadata: {res['zenodo_file']}")
    for art in res.get("artifacts_created", []):
        print(f"   • Bundle: {art}")

    gh_res = res.get("github_release", {})
    if gh_res:
        action = gh_res.get("action")
        if action == "created":
            print(f"\n🎉 GitHub Release successfully published live: {gh_res.get('url')}")
        elif action == "dry_run_simulated":
            print(f"\n🔍 [Dry-Run] GitHub Release simulated for tag '{gh_res.get('tag')}'.")
            print(f"   Assets to attach: {', '.join(gh_res.get('assets', []))}")
        elif action == "failed":
            print(f"\n⚠️ GitHub Release creation returned error: {gh_res.get('error')}", file=sys.stderr)
            print(f"   {gh_res.get('fallback')}")
        elif action == "skipped_no_gh_cli":
            print(f"\n💡 {gh_res.get('fallback')}")

    print("\nNext step: Submit arXiv bundle (`paper/arxiv_submission.tar.gz`) or import `paper/overleaf_bundle.zip` into Overleaf.")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="scholar-provenance",
        description="ScholarProvenance: Rigorous Academic Research & Paper Pipeline CLI",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # init
    p_init = subparsers.add_parser("init", help="Initialize a research project workspace")
    p_init.add_argument("path", nargs="?", default=".", help="Directory to initialize")
    p_init.add_argument("--title", help="Project title")
    p_init.add_argument("--author", help="Primary human author name")
    p_init.add_argument("--affiliation", help="Author institutional affiliation or independent")
    p_init.add_argument("--email", help="Author email")
    p_init.add_argument("--orcid", help="Author ORCID identifier")
    p_init.add_argument("--sources", help="Comma-separated URLs or paths to user evidence materials")
    p_init.add_argument("--lang", default="en", help="Paper language code (e.g. en, fa, tr, az, ar)")
    p_init.add_argument("--type", default="architecture", help="Research type (architecture, empirical, etc.)")
    p_init.add_argument("--venue", help="Target venue name")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing manifest")

    # validate-manifest
    p_val = subparsers.add_parser("validate-manifest", help="Validate research-project.yml")
    p_val.add_argument("manifest", help="Path to manifest file")

    # search
    p_search = subparsers.add_parser("search", help="Query open scholarly literature")
    p_search.add_argument("query", help="Keywords or research query")
    p_search.add_argument("--limit", type=int, default=3, help="Max results per index")
    p_search.add_argument("--year", type=int, help="Minimum publication year")

    # ledger
    p_ledger = subparsers.add_parser("ledger", help="Validate or export evidence ledger")
    p_ledger.add_argument("file", help="Path to evidence-matrix.json")
    p_ledger.add_argument("--markdown", help="Path to write Markdown evidence matrix")

    # audit
    p_audit = subparsers.add_parser("audit", help="Audit manuscript claims and citations")
    p_audit.add_argument("manuscript", help="Path to manuscript.md")
    p_audit.add_argument("--bib", help="Path to references.bib")
    p_audit.add_argument("--matrix", help="Path to evidence-matrix.json")
    p_audit.add_argument("--output", help="Path to output markdown report")

    # scan-sensitive
    p_scan = subparsers.add_parser("scan-sensitive", help="Scan for secrets, tokens, and PII")
    p_scan.add_argument("path", nargs="?", default=".", help="Directory to scan")
    p_scan.add_argument("--output", help="Path to output privacy report")

    # review
    p_rev = subparsers.add_parser("review", help="Generate adversarial reviews and red-team report")
    p_rev.add_argument("path", nargs="?", default=".", help="Project workspace root")

    # check-gates
    p_gates = subparsers.add_parser("check-gates", help="Evaluate 12 quality gates")
    p_gates.add_argument("path", nargs="?", default=".", help="Project workspace root")

    # package
    p_pkg = subparsers.add_parser("package", help="Generate reproducibility package & checksums")
    p_pkg.add_argument("path", nargs="?", default=".", help="Project workspace root")

    # build
    p_bld = subparsers.add_parser("build", help="Build multi-format publications (HTML, PDF, DOCX)")
    p_bld.add_argument("manuscript", help="Path to manuscript.md")
    p_bld.add_argument("--manifest", help="Path to research-project.yml")
    p_bld.add_argument("--no-pdf", action="store_true", help="Skip PDF generation")
    p_bld.add_argument("--no-docx", action="store_true", help="Skip DOCX generation")

    # chart
    p_crt = subparsers.add_parser("chart", help="Generate standalone SVG academic charts")
    p_crt.add_argument("--type", choices=["bar", "architecture"], default="bar", help="Chart type")
    p_crt.add_argument("--output", default="paper/assets/figure-1.svg", help="Output SVG path")
    p_crt.add_argument("--title", help="Chart title")
    p_crt.add_argument("--categories", help="Comma-separated category names")
    p_crt.add_argument("--series", help="JSON dictionary of series names to values")
    p_crt.add_argument("--xlabel", help="X-axis label")
    p_crt.add_argument("--ylabel", help="Y-axis label")
    p_crt.add_argument("--rtl", action="store_true", help="Render for RTL language")

    # showcase
    p_shw = subparsers.add_parser("showcase", help="Prepare voluntary showcase submission")
    p_shw.add_argument("--yes", action="store_true", help="Non-interactive default submission")

    # publish
    p_pub = subparsers.add_parser("publish", help="Autonomous release connector, bundler, and venue advisory")
    p_pub.add_argument("path", nargs="?", default=".", help="Project workspace root")
    p_pub.add_argument(
        "--target",
        choices=["all", "github", "arxiv", "overleaf", "metadata"],
        default="all",
        help="Target distribution system (default: all)",
    )
    p_pub.add_argument("--tag", help="Explicit release tag (e.g. v0.1.0 or paper-v1)")
    p_pub.add_argument("--dry-run", action="store_true", help="Simulate release generation without pushing to remotes")
    p_pub.add_argument("--recommend", action="store_true", help="Display proactive venue & archive recommendations")

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0

    commands = {
        "init": cmd_init,
        "validate-manifest": cmd_validate_manifest,
        "search": cmd_search,
        "ledger": cmd_ledger,
        "audit": cmd_audit,
        "scan-sensitive": cmd_scan_sensitive,
        "review": cmd_review,
        "check-gates": cmd_check_gates,
        "package": cmd_package,
        "build": cmd_build,
        "chart": cmd_chart,
        "showcase": cmd_showcase,
        "publish": cmd_publish,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
