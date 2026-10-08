"""Mandatory Research Intake and Interactive Onboarding Engine for ScholarProvenance.

Manages progressive interview stages, author profiles, context extraction from workspaces,
evidence source catalogs, research brief synthesis, and gate approvals.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any, Dict, List, Optional, Tuple
import yaml


USER_PROFILE_DIR = Path.home() / ".scholar-provenance"
GLOBAL_PROFILE_FILE = USER_PROFILE_DIR / "author-profile.json"


# Multilingual Prompt Templates for the Intake Interview
INTAKE_LOCALIZED_MESSAGES = {
    "en": {
        "welcome": "Welcome to ScholarProvenance. Before drafting or researching, I need to understand your research context, empirical evidence, and publication goals through a short onboarding interview.",
        "stage_a_intro": "### Stage A — Author Identity",
        "stage_a_author_name": "What is the primary author's full name (native script and English if different)?",
        "stage_a_affiliation": "What is your academic/professional affiliation or institution? (Enter 'Independent' if unaffiliated):",
        "stage_a_email": "What is your contact/corresponding email address? (Optional, press Enter to skip):",
        "stage_a_orcid": "Do you have an ORCID iD, website, or Google Scholar profile? (Optional, press Enter to skip):",
        "stage_a_coauthors": "Are there coauthors and specific contribution divisions? (Optional, press Enter to skip):",
        "stage_b_intro": "### Stage B — Research Definition",
        "stage_b_topic": "What is the primary topic and target title of this research?",
        "stage_b_problem": "What specific problem, research question, or gap does this paper address?",
        "stage_b_contribution": "What is the core novel contribution of this work?",
        "stage_b_type": "What is the research type? (1: Empirical Study, 2: Architecture/System, 3: Literature Review, 4: Case Study, 5: Technical Report):",
        "stage_c_intro": "### Stage C — Evidence & Research Materials",
        "stage_c_sources": "What primary evidence, datasets, repositories, test logs, or documentation should this paper be grounded on? (Provide paths, URLs, or file lists):",
        "stage_c_is_mandatory": "Are these provided sources mandatory primary evidence (strict provenance required)? [Y/n]:",
        "stage_d_intro": "### Stage D — External Research Permission",
        "stage_d_permission": "Should I independently research and retrieve recent scholarly sources to complement your materials?\n[1] Yes - Broaden with credible external academic literature\n[2] Yes - But stay strictly within my specific research scope (Recommended)\n[3] No - Ground exclusively on the materials I provided",
        "stage_e_intro": "### Stage E — Publication Goals",
        "stage_e_venue": "Where do you intend to publish? (e.g. arXiv, IEEE, ACM, NeurIPS, specific journal, or 'recommend'):",
        "stage_e_doi": "Do you require a persistent citable DOI (e.g. via Zenodo / publisher)? [Y/n]:",
        "stage_f_intro": "### Stage F — Manuscript Preferences",
        "stage_f_lang": "What is the target publication language? [en / fa / tr / az / ar]:",
        "stage_f_style": "What citation and document style do you prefer? (e.g. IEEE, ACM, APA, Nature):",
        "stage_g_intro": "### Stage G — Research Integrity & Confidentiality",
        "stage_g_completed": "Are all experiments completed and benchmark measurements finalized? [Y/n]:",
        "stage_g_proprietary": "Are there any confidentiality restrictions, proprietary secrets, or unpublished IP in the provided materials? [y/N]:",
        "stage_g_ai": "Has AI assistance been used in previous stages of this research? (Will be disclosed ethically per COPE standards) [Y/n]:",
        "brief_confirm": "Please review the generated Research Brief below. Do you approve this brief to begin research and drafting? [Y/n]:",
    },
    "fa": {
        "welcome": "به سامانه ScholarProvenance خوش آمدید. پیش از آغاز پژوهش یا نگارش، چند پرسش کوتاه مطرح می‌شود تا مقاله دقیقاً بر پایه شواهد و اهداف علمی شما تنظیم گردد.",
        "stage_a_intro": "### بخش الف — هویت و اطلاعات نویسنده",
        "stage_a_author_name": "نام و نام خانوادگی نویسنده اصلی (به فارسی و نگارش انگلیسی) چیست؟",
        "stage_a_affiliation": "وابستگی دانشگاهی یا حرفه‌ای شما چیست؟ (در صورت عدم وابستگی سازمانی، عبارت «پژوهشگر مستقل» را وارد کنید):",
        "stage_a_email": "نشانی ایمیل مکاتبه‌کننده (اختیاری، برای عبور Enter بزنید):",
        "stage_a_orcid": "شناسه ORCID، تارنما یا پیوند پژوهشی (اختیاری، برای عبور Enter بزنید):",
        "stage_a_coauthors": "آیا نویسندگان همکار دیگری وجود دارند؟ (اختیاری، برای عبور Enter بزنید):",
        "stage_b_intro": "### بخش ب — تعریف و هدف پژوهش",
        "stage_b_topic": "موضوع اصلی و عنوان پیشنهادی مقاله چیست؟",
        "stage_b_problem": "مقاله به چه پرسش، مسئله یا خلاء پژوهشی مشخصی پاسخ می‌دهد؟",
        "stage_b_contribution": "نوآوری و مشارکت اصلی این پژوهش در چیست؟",
        "stage_b_type": "نوع پژوهش کدام است؟ (۱: مطالعه تجربی/بنچ‌مارک، ۲: معماری سیستم، ۳: مرور ادبیات، ۴: مطالعه موردی، ۵: گزارش فنی):",
        "stage_c_intro": "### بخش ج — شواهد و داده‌های مبنا",
        "stage_c_sources": "چه داده‌ها، لاگ‌های آزمایش، مخازن کد، اسناد یا فایل‌هایی باید مبنای این مقاله باشند؟ (مسیر فایل‌ها یا نشانی وب را بنویسید):",
        "stage_c_is_mandatory": "آیا این منابع ارائه شده، شواهد اصلی و الزامی هستند (ردیابی قطعی)؟ [Y/n]:",
        "stage_d_intro": "### بخش د — مجوز جستجوی ادبیات بیرونی",
        "stage_d_permission": "آیا مقالات و منابع دانشگاهی معتبر جدید از پایگاه‌های علمی استخراج و به مراجع افزوده شوند؟\n[۱] بله - با جستجوی گسترده در ادبیات علمی معتبر\n[۲] بله - اما منحصراً در چارچوب موضوع مشخص پژوهش (پیشنهادی)\n[۳] خیر - فقط بر اساس مدارک و کدهایی که تحویل دادم نوشته شود",
        "stage_e_intro": "### بخش هـ — اهداف انتشار",
        "stage_e_venue": "قصد انتشار مقاله در چه مرجعی را دارید؟ (مانند arXiv، ژورنال IEEE/ACM، کنفرانس، یا «پیشنهاد دهید»):",
        "stage_e_doi": "آیا به ثبت شناسه دیجیتال رسمی DOI نیاز دارید؟ [Y/n]:",
        "stage_f_intro": "### بخش و — قالب و شیوه نگارش",
        "stage_f_lang": "زبان نگارش نهایی مقاله چیست؟ [fa / en / tr / az / ar]:",
        "stage_f_style": "قالب استناد ترجیحی شما چیست؟ (مانند IEEE، ACM، APA):",
        "stage_g_intro": "### بخش ز — اخلاق پژوهش و محرمانگی",
        "stage_g_completed": "آیا آزمایش‌ها و اندازه‌گیری‌های عددی به پایان رسیده‌اند؟ [Y/n]:",
        "stage_g_proprietary": "آیا داده‌های محرمانه، اسرار تجاری یا داده‌های حساس فاش‌نشده در مدارک وجود دارد؟ [y/N]:",
        "stage_g_ai": "آیا از هوش مصنوعی در مراحل اجرای پژوهش یا آزمون‌ها استفاده شده است؟ (طبق اصول COPE در مقاله افشا می‌شود) [Y/n]:",
        "brief_confirm": "لطفاً چکیده سند راهبردی پژوهش (Research Brief) را در زیر مرور فرمایید. آیا این چارچوب را برای آغاز پژوهش و تدوین مقاله تأیید می‌فرمایید؟ [Y/n]:",
    },
    "tr": {
        "welcome": "ScholarProvenance'a hoş geldiniz. Makale yazımına başlamadan önce, araştırmanızın bağlamını, ampirik verilerini ve hedeflerini anlamak için kısa bir ön mülakat gerçekleştireceğiz.",
        "stage_a_intro": "### Aşama A — Yazar Kimliği",
        "stage_a_author_name": "Birincil yazarın tam adı nedir?",
        "stage_a_affiliation": "Akademik veya kurumsal bağlantınız nedir? (Bağımsız araştırmacı için 'Bağımsız' yazınız):",
        "stage_a_email": "İletişim e-posta adresi (İsteğe bağlı):",
        "stage_a_orcid": "ORCID iD veya web sitesi (İsteğe bağlı):",
        "stage_b_intro": "### Aşama B — Araştırma Tanımı",
        "stage_b_topic": "Araştırma konusu ve makale başlığı nedir?",
        "stage_b_problem": "Bu çalışma hangi araştırma sorusuna veya soruna odaklanmaktadır?",
        "stage_b_contribution": "Çalışmanın temel özgün katkısı nedir?",
        "stage_c_intro": "### Aşama C — Kanıt ve Veri Kaynakları",
        "stage_c_sources": "Makaleye temel oluşturacak veri setleri, kod depoları veya belgeler nelerdir?",
        "stage_d_permission": "Dış akademik kaynakları bağımsız olarak araştırmamıza izin veriyor musunuz? [1: Kapsamlı, 2: Sadece araştırma kapsamında (Önerilen), 3: Yalnızca sağlanan kaynaklar]:",
        "stage_e_venue": "Hedef yayın mecrası nedir? (arXiv, IEEE, dergi veya 'öneri'):",
        "stage_g_completed": "Deneyler ve ölçümler tamamlandı mı? [Y/n]:",
        "brief_confirm": "Lütfen Araştırma Özeti'ni (Research Brief) inceleyiniz. Araştırmaya ve taslağa başlamayı onaylıyor musunuz? [Y/n]:",
    },
    "az": {
        "welcome": "ScholarProvenance sisteminə xoş gəlmisiniz. Elmi məqalənin tərtibatından əvvəl tədqiqat kontekstini və ilkin dəlilləri müəyyən etmək üçün qısa sorğu aparılacaqdır.",
        "stage_a_intro": "### Mərhələ A — Müəllif Məlumatları",
        "stage_a_author_name": "Əsas müəllifin tam adı:",
        "stage_a_affiliation": "Akademik mənsubiyyət və ya müstəqil tədqiqatçı statusu:",
        "stage_b_intro": "### Mərhələ B — Tədqiqatın Məqsədi",
        "stage_b_topic": "Tədqiqat mövzusu və təklif olunan başlıq:",
        "stage_b_problem": "Məqalənin həll etdiyi elmi problem və ya tədqiqat sualı:",
        "stage_c_sources": "Əsas götürüləcək mənbələr, verilənlər bazası və ya kod depoları:",
        "stage_d_permission": "Xarici elmi mənbələrin araşdırılmasına icazə verirsinizmi? [1: Geniş, 2: Mövzu çərçivəsində, 3: Yalnız təqdim olunan]:",
        "stage_e_venue": "Nəşr hədəfi:",
        "brief_confirm": "Tədqiqat planını təsdiq edirsinizmi? [Y/n]:",
    },
    "ar": {
        "welcome": "مرحبًا بك في ScholarProvenance. قبل البدء في كتابة البحث، سنقوم بإجراء مقابلة تأهيلية قصيرة لفهم سياق البحث والأدلة التجريبية وأهداف النشر بدقة.",
        "stage_a_intro": "### المرحلة أ — هوية الباحث",
        "stage_a_author_name": "الاسم الكامل للمؤلف الرئيسي (بالعربية والإنجليزية):",
        "stage_a_affiliation": "الانتماء الأكاديمي أو المؤسسي (أو باحث مستقل):",
        "stage_a_email": "البريد الإلكتروني للتواصل (اختياري):",
        "stage_a_orcid": "معرف ORCID أو الموقع الشخصي (اختياري):",
        "stage_b_intro": "### المرحلة ب — تعريف البحث",
        "stage_b_topic": "موضوع البحث والعنوان المقترح:",
        "stage_b_problem": "ما هو السؤال البحثي أو المشكلة المحددة التي يعالجها البحث؟",
        "stage_b_contribution": "ما هي الإضافة العلمية أو الابتكار الأساسي في هذا العمل؟",
        "stage_c_intro": "### المرحلة ج — مصادر الأدلة والبيانات",
        "stage_c_sources": "ما هي مجموعات البيانات أو مستودعات البرمجيات أو سجلات التجارب التي يستند إليها هذا البحث؟",
        "stage_d_permission": "هل تأذن بالبحث المستقل في قواعد البيانات العلمية؟ [1: توسع كامل، 2: في حدود نطاق البحث فقط (مستحسن)، 3: الاعتماد فقط على ما تم تقديمه]:",
        "stage_e_venue": "أين تنوي نشر البحث؟ (مثل arXiv، مجلة IEEE/ACM، أو طلب ترشيح):",
        "stage_g_completed": "هل تم الانتهاء من جميع التجارب والقياسات المعيارية؟ [Y/n]:",
        "brief_confirm": "يرجى مراجعة ملخص خطة البحث (Research Brief). هل توافق على البدء في كتابة وتوثيق البحث؟ [Y/n]:",
    },
}


@dataclass
class AuthorProfile:
    name: str
    english_name: Optional[str] = None
    affiliation: str = "Independent Researcher"
    email: Optional[str] = ""
    orcid: Optional[str] = ""
    website: Optional[str] = ""
    bio: Optional[str] = ""
    corresponding: bool = True
    coauthors: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AuthorProfile:
        return cls(
            name=data.get("name", "Independent Researcher"),
            english_name=data.get("english_name"),
            affiliation=data.get("affiliation", "Independent Researcher"),
            email=data.get("email", ""),
            orcid=data.get("orcid", ""),
            website=data.get("website", ""),
            bio=data.get("bio", ""),
            corresponding=data.get("corresponding", True),
            coauthors=data.get("coauthors", []),
        )


@dataclass
class EvidenceSource:
    url_or_path: str
    source_type: str = "code_repository"  # dataset, benchmark_log, paper, doc, repo
    is_primary_evidence: bool = True
    description: str = ""
    verified: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PublicationPreferences:
    target_venue: str = "arXiv"
    publication_mode: str = "preprint"  # preprint, peer_reviewed, technical_report
    doi_required: bool = True
    budget_usd: Optional[float] = None
    target_length_pages: Optional[int] = None
    citation_style: str = "ieee"
    output_formats: List[str] = field(default_factory=lambda: ["pdf", "html", "docx", "latex", "markdown"])
    language: str = "en"
    ai_assistance_disclosure: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ResearchIntegrity:
    experiments_completed: bool = True
    datasets_available: bool = True
    benchmarks_reproducible: bool = True
    confidentiality_restrictions: bool = False
    proprietary_ip_cleared: bool = True
    ai_assistance_used: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ResearchBrief:
    approved: bool
    approval_date: Optional[str]
    approved_by: Optional[str]
    author_profile: AuthorProfile
    topic: str
    title: str
    research_question: str
    original_contribution: str
    research_type: str
    target_audience: str
    language: str
    english_abstract_required: bool
    sources: List[EvidenceSource]
    external_research_permission: str  # "expand", "scope_only", "none"
    publication_preferences: PublicationPreferences
    integrity: ResearchIntegrity
    evidence_gaps: List[str] = field(default_factory=list)
    scientific_limitations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ResearchBrief:
        author_data = data.get("author_profile") or data.get("author") or {}
        author = AuthorProfile.from_dict(author_data)

        sources_data = data.get("sources", [])
        sources = [EvidenceSource(**s) if isinstance(s, dict) else EvidenceSource(url_or_path=str(s)) for s in sources_data]

        pub_data = data.get("publication_preferences") or {}
        pub = PublicationPreferences(**pub_data) if isinstance(pub_data, dict) else PublicationPreferences()

        integ_data = data.get("integrity") or {}
        integ = ResearchIntegrity(**integ_data) if isinstance(integ_data, dict) else ResearchIntegrity()

        return cls(
            approved=data.get("approved", False),
            approval_date=data.get("approval_date"),
            approved_by=data.get("approved_by"),
            author_profile=author,
            topic=data.get("topic", "Empirical Evaluation"),
            title=data.get("title", "Empirical Study of Intelligent Systems"),
            research_question=data.get("research_question", "How do system properties affect performance and reliability?"),
            original_contribution=data.get("original_contribution", "Empirical benchmark and provenance audit"),
            research_type=data.get("research_type", "empirical"),
            target_audience=data.get("target_audience", "Computer Science Researchers and Engineers"),
            language=data.get("language", "en"),
            english_abstract_required=data.get("english_abstract_required", True),
            sources=sources,
            external_research_permission=data.get("external_research_permission", "scope_only"),
            publication_preferences=pub,
            integrity=integ,
            evidence_gaps=data.get("evidence_gaps", []),
            scientific_limitations=data.get("scientific_limitations", []),
        )


def detect_language(text_or_locale: str) -> str:
    """Detect appropriate language code (en, fa, tr, az, ar) from input."""
    if not text_or_locale:
        return "en"
    lower = text_or_locale.lower()
    # Check Persian / Arabic characters
    if any("\u0600" <= ch <= "\u06FF" for ch in text_or_locale):
        # Persian-specific letters: گ چ پ ژ
        if any(ch in text_or_locale for ch in ["گ", "چ", "پ", "ژ", "ی"]):
            return "fa"
        return "ar"
    if "fa" in lower or "farsi" in lower or "persian" in lower:
        return "fa"
    if "tr" in lower or "turkish" in lower or "türkçe" in lower:
        return "tr"
    if "az" in lower or "azerbaijani" in lower or "azərbaycan" in lower:
        return "az"
    if "ar" in lower or "arabic" in lower or "عربي" in lower:
        return "ar"
    return "en"


def load_author_profile(custom_path: Optional[str | Path] = None) -> Optional[AuthorProfile]:
    """Load reusable author profile from project or global user config."""
    paths_to_check = []
    if custom_path:
        paths_to_check.append(Path(custom_path))
    paths_to_check.extend([
        Path("author-profile.json"),
        Path(".scholar-provenance/author-profile.json"),
        GLOBAL_PROFILE_FILE,
    ])

    for p in paths_to_check:
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                return AuthorProfile.from_dict(data)
            except Exception:
                continue
    return None


def save_author_profile(profile: AuthorProfile, custom_path: Optional[str | Path] = None, save_globally: bool = True) -> Path:
    """Save author profile locally or to user config directory."""
    if custom_path:
        target = Path(custom_path).resolve()
    else:
        target = Path("author-profile.json").resolve()

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(profile.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

    if save_globally:
        try:
            USER_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
            GLOBAL_PROFILE_FILE.write_text(json.dumps(profile.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    return target


def extract_context_from_workspace(workspace_dir: str | Path) -> Dict[str, Any]:
    """Inspect workspace files and extract existing research evidence and metadata.
    
    Distinguishes:
    - EXTRACTED: Found in code/repo
    - MISSING: Needs to be prompted
    """
    root = Path(workspace_dir).resolve()
    extracted: Dict[str, Any] = {
        "author_name": None,
        "author_email": None,
        "project_title": None,
        "description": None,
        "sources": [],
        "research_type": "empirical",
        "has_datasets": False,
        "has_tests": False,
        "existing_manifest": False,
    }

    # 1. Check existing manifest
    for m_name in ["research-project.yml", "research-project.yaml"]:
        m_file = root / m_name
        if m_file.exists():
            extracted["existing_manifest"] = True
            try:
                data = yaml.safe_load(m_file.read_text(encoding="utf-8")) or {}
                proj = data.get("project", {})
                extracted["project_title"] = proj.get("title")
                authors = proj.get("authors", [])
                if authors and isinstance(authors[0], dict):
                    extracted["author_name"] = authors[0].get("name")
                    extracted["author_email"] = authors[0].get("email")
                extracted["research_type"] = proj.get("research_type", "empirical")
            except Exception:
                pass

    # 2. Check git configuration and remotes
    try:
        git_name = subprocess.check_output(["git", "-C", str(root), "config", "user.name"], text=True, stderr=subprocess.DEVNULL).strip()
        git_email = subprocess.check_output(["git", "-C", str(root), "config", "user.email"], text=True, stderr=subprocess.DEVNULL).strip()
        if git_name and not extracted["author_name"]:
            extracted["author_name"] = git_name
        if git_email and not extracted["author_email"]:
            extracted["author_email"] = git_email
    except Exception:
        pass

    # 3. Check README.md
    readme_path = root / "README.md"
    if readme_path.exists():
        r_text = readme_path.read_text(encoding="utf-8")
        h1 = re.search(r"^#\s+(.+)$", r_text, re.MULTILINE)
        if h1 and not extracted["project_title"]:
            extracted["project_title"] = h1.group(1).strip()
        extracted["sources"].append(EvidenceSource(
            url_or_path="README.md",
            source_type="documentation",
            is_primary_evidence=False,
            description="Project documentation overview",
        ))

    # 4. Check benchmark data, CSVs, JSON datasets
    for p in root.glob("**/*"):
        if p.is_file():
            if p.suffix in [".csv", ".tsv"]:
                extracted["has_datasets"] = True
                extracted["sources"].append(EvidenceSource(
                    url_or_path=str(p.relative_to(root)),
                    source_type="dataset",
                    is_primary_evidence=True,
                    description="Raw empirical dataset",
                ))
            elif "test" in p.name.lower() and p.suffix in [".py", ".rs", ".go", ".ts", ".js"]:
                extracted["has_tests"] = True

    return extracted


def synthesize_research_brief(
    author: AuthorProfile,
    topic: str,
    title: str,
    research_question: str,
    original_contribution: str,
    research_type: str,
    sources: List[EvidenceSource],
    permission: str = "scope_only",
    target_venue: str = "arXiv",
    language: str = "en",
    preferences: Optional[PublicationPreferences] = None,
    integrity: Optional[ResearchIntegrity] = None,
) -> ResearchBrief:
    """Construct a comprehensive, unconfirmed Research Brief."""
    pub_prefs = preferences or PublicationPreferences(target_venue=target_venue, language=language)
    integ = integrity or ResearchIntegrity()

    # Identify evidence gaps
    evidence_gaps = []
    has_primary = any(s.is_primary_evidence for s in sources)
    if not has_primary:
        evidence_gaps.append("No primary experimental dataset or verified benchmark logs provided. Risk of overclaim.")

    scientific_limitations = [
        f"Evaluation scope is constrained to the verified test environments within target: {title}.",
        "External generalization claims must be supported by external literature.",
    ]

    return ResearchBrief(
        approved=False,
        approval_date=None,
        approved_by=None,
        author_profile=author,
        topic=topic,
        title=title,
        research_question=research_question,
        original_contribution=original_contribution,
        research_type=research_type,
        target_audience="Computer Science and Systems Researchers",
        language=language,
        english_abstract_required=True,
        sources=sources,
        external_research_permission=permission,
        publication_preferences=pub_prefs,
        integrity=integ,
        evidence_gaps=evidence_gaps,
        scientific_limitations=scientific_limitations,
    )


def save_research_brief(brief: ResearchBrief, output_dir: str | Path) -> Tuple[Path, Path]:
    """Save Research Brief as YAML and Markdown."""
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    yaml_file = out / "research-brief.yaml"
    md_file = out / "research-brief.md"

    # YAML
    brief_dict = brief.to_dict()
    yaml_file.write_text(yaml.dump(brief_dict, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # Markdown
    approval_status = "✅ APPROVED" if brief.approved else "⚠️ PENDING AUTHOR APPROVAL (Drafting Blocked)"
    authors_str = brief.author_profile.name
    if brief.author_profile.affiliation:
        authors_str += f" ({brief.author_profile.affiliation})"

    md_lines = [
        f"# Research Brief: {brief.title}",
        "",
        f"**Status:** `{approval_status}`",
        f"**Approval Date:** {brief.approval_date or 'Pending'}",
        f"**Primary Author:** {authors_str}",
        f"**Language:** {brief.language.upper()} · **Type:** {brief.research_type.capitalize()} · **Target:** {brief.publication_preferences.target_venue}",
        "",
        "## 1. Research Question & Scope",
        f"**Core Problem / Question:** {brief.research_question}",
        "",
        f"**Original Contribution:** {brief.original_contribution}",
        "",
        "## 2. Evidence Base & Primary Sources",
        "",
        "| Source | Type | Role | Verified |",
        "| :--- | :---: | :---: | :---: |",
    ]

    for s in brief.sources:
        role = "Primary Evidence" if s.is_primary_evidence else "Background Material"
        md_lines.append(f"| `{s.url_or_path}` | {s.source_type} | {role} | {'✅' if s.verified else '⏳'} |")

    md_lines.extend([
        "",
        "## 3. Independent Literature Permission",
        f"**Permission Level:** `{brief.external_research_permission.upper()}`",
        "- `SCOPE_ONLY`: Independently retrieve and verify recent peer-reviewed literature strictly within the stated research scope.",
        "",
        "## 4. Evidence Gaps & Threats to Validity",
    ])

    if brief.evidence_gaps:
        for eg in brief.evidence_gaps:
            md_lines.append(f"- ⚠️ **Gap:** {eg}")
    else:
        md_lines.append("- Primary empirical materials fully supplied.")

    for lim in brief.scientific_limitations:
        md_lines.append(f"- 🔬 **Limitation:** {lim}")

    md_lines.extend([
        "",
        "## 5. Research Integrity & AI Assistance Disclosure",
        f"- Experiments Completed: {'Yes' if brief.integrity.experiments_completed else 'No'}",
        f"- Datasets Available: {'Yes' if brief.integrity.datasets_available else 'No'}",
        f"- Benchmarks Reproducible: {'Yes' if brief.integrity.benchmarks_reproducible else 'No'}",
        f"- Confidentiality Restrictions: {'Yes (Sensitive)' if brief.integrity.confidentiality_restrictions else 'None (Open)'}",
        f"- AI Disclosure: {'Mandatory COPE statement enabled' if brief.publication_preferences.ai_assistance_disclosure else 'Disabled'}",
        "",
        "---",
        "*(This document must be approved by the author before manuscript generation is permitted)*",
    ])

    md_file.write_text("\n".join(md_lines), encoding="utf-8")
    return (yaml_file, md_file)


def approve_research_brief(workspace_dir: str | Path, approved_by: Optional[str] = None) -> bool:
    """Mark research-brief.yaml as approved."""
    root = Path(workspace_dir).resolve()
    candidates = [
        root / "research-brief.yaml",
        root / "research-brief.yml",
        root / "research" / "research-brief.yaml",
    ]

    for c in candidates:
        if c.exists():
            try:
                data = yaml.safe_load(c.read_text(encoding="utf-8")) or {}
                data["approved"] = True
                data["approval_date"] = datetime.now(timezone.utc).isoformat()
                data["approved_by"] = approved_by or data.get("author_profile", {}).get("name") or "Primary Author"
                c.write_text(yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

                # Also update markdown if exists
                md_f = c.with_suffix(".md")
                if md_f.exists():
                    txt = md_f.read_text(encoding="utf-8")
                    txt = txt.replace("⚠️ PENDING AUTHOR APPROVAL (Drafting Blocked)", "✅ APPROVED")
                    txt = txt.replace("**Approval Date:** Pending", f"**Approval Date:** {data['approval_date']}")
                    md_f.write_text(txt, encoding="utf-8")
                return True
            except Exception:
                return False
    return False


def check_intake_approval(workspace_dir: str | Path) -> Tuple[bool, Optional[str]]:
    """Check whether a verified, approved Research Brief exists in workspace.
    
    Returns:
        (is_approved, explanation_message)
    """
    root = Path(workspace_dir).resolve()
    candidates = [
        root / "research-brief.yaml",
        root / "research-brief.yml",
        root / "research" / "research-brief.yaml",
    ]

    for c in candidates:
        if c.exists():
            try:
                data = yaml.safe_load(c.read_text(encoding="utf-8")) or {}
                if data.get("approved") is True:
                    return (True, f"Approved Research Brief found at {c.name} (Approved by {data.get('approved_by')}).")
                else:
                    return (False, f"Research Brief found at {c.name} but status is UNAPPROVED. Author confirmation required.")
            except Exception as e:
                return (False, f"Error parsing {c.name}: {e}")

    return (False, "No research-brief.yaml found. Mandatory onboarding interview must be completed first.")


def delete_author_profile(custom_path: Optional[str | Path] = None) -> bool:
    """Delete stored author profile."""
    target = Path(custom_path).resolve() if custom_path else GLOBAL_PROFILE_FILE
    if target.exists():
        try:
            target.unlink()
            return True
        except Exception:
            return False
    return False


def run_interactive_intake(
    workspace_dir: str | Path,
    lang: str = "en",
    non_interactive: bool = False,
    auto_approve: bool = False,
    custom_inputs: Optional[Dict[str, Any]] = None,
) -> Tuple[ResearchBrief, Path, Path]:
    """Execute the mandatory intake workflow for a workspace."""
    root = Path(workspace_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    lang_code = detect_language(lang)
    msg = INTAKE_LOCALIZED_MESSAGES.get(lang_code, INTAKE_LOCALIZED_MESSAGES["en"])
    custom = custom_inputs or {}

    extracted = extract_context_from_workspace(root)
    saved_author = load_author_profile()

    # Stage A: Author Identity
    if custom.get("author"):
        if isinstance(custom["author"], dict):
            author = AuthorProfile.from_dict(custom["author"])
        else:
            author = AuthorProfile(name=str(custom["author"]))
    elif non_interactive:
        if saved_author:
            author = saved_author
        elif extracted.get("author_name"):
            author = AuthorProfile(
                name=extracted["author_name"],
                email=extracted.get("author_email") or "",
                affiliation="Independent Researcher",
            )
        else:
            author = AuthorProfile(name="Independent Researcher")
    else:
        print(f"\n{msg['welcome']}\n")
        print(msg["stage_a_intro"])

        # Check for saved profile
        reuse_saved = False
        if saved_author:
            ans = input(f"Found saved author profile for '{saved_author.name}' ({saved_author.affiliation}). Reuse? [Y/n]: ").strip().lower()
            if ans in ["", "y", "yes"]:
                author = saved_author
                reuse_saved = True

        if not reuse_saved:
            def_name = extracted.get("author_name") or ""
            prompt_name = f"{msg['stage_a_author_name']} [{def_name}]: " if def_name else f"{msg['stage_a_author_name']}: "
            in_name = input(prompt_name).strip() or def_name or "Independent Researcher"

            in_aff = input(f"{msg['stage_a_affiliation']} [Independent]: ").strip() or "Independent Researcher"
            in_email = input(f"{msg['stage_a_email']} ").strip() or extracted.get("author_email") or ""
            in_orcid = input(f"{msg['stage_a_orcid']} ").strip() or ""

            author = AuthorProfile(
                name=in_name,
                affiliation=in_aff,
                email=in_email,
                orcid=in_orcid,
            )
            # Ask to remember profile
            save_ans = input("Remember this author profile for future papers? [Y/n]: ").strip().lower()
            if save_ans in ["", "y", "yes"]:
                save_author_profile(author)

    # Stage B: Research Definition
    def_title = custom.get("title") or extracted.get("project_title") or "Empirical Study of Intelligent Systems"
    if non_interactive or custom.get("title"):
        title = def_title
        topic = custom.get("topic") or "AI Systems & Empirical Software Engineering"
        problem = custom.get("problem") or "Verifying system behaviors with auditable provenance ledgers."
        contribution = custom.get("contribution") or "Empirical benchmark and reproducibility analysis."
        res_type = custom.get("type") or extracted.get("research_type") or "empirical"
    else:
        print(f"\n{msg['stage_b_intro']}")
        title = input(f"{msg['stage_b_topic']} [{def_title}]: ").strip() or def_title
        problem = input(f"{msg['stage_b_problem']}: ").strip() or "Rigorous empirical evaluation and provenance tracking."
        contribution = input(f"{msg['stage_b_contribution']}: ").strip() or "Architecture, benchmark, and provenance ledger."
        type_choice = input(f"{msg['stage_b_type']} [1]: ").strip()
        type_map = {"1": "empirical", "2": "architecture", "3": "literature_review", "4": "case_study", "5": "technical_report"}
        res_type = type_map.get(type_choice, "empirical")
        topic = title

    # Stage C: Evidence & Materials
    sources: List[EvidenceSource] = list(extracted.get("sources", []))
    if custom.get("sources"):
        raw_sources = custom["sources"]
        if isinstance(raw_sources, str):
            raw_sources = [s.strip() for s in raw_sources.split(",") if s.strip()]
        for s in raw_sources:
            sources.append(EvidenceSource(url_or_path=s, is_primary_evidence=True))
    elif not non_interactive:
        print(f"\n{msg['stage_c_intro']}")
        if sources:
            print(f"Auto-detected {len(sources)} source file(s) in repository (e.g., {[s.url_or_path for s in sources[:3]]}).")
        add_sources = input(f"{msg['stage_c_sources']} ").strip()
        if add_sources:
            for s in add_sources.split(","):
                s_c = s.strip()
                if s_c:
                    sources.append(EvidenceSource(url_or_path=s_c, is_primary_evidence=True))

    if not sources:
        # Fallback to current directory as source
        sources.append(EvidenceSource(url_or_path=".", source_type="code_repository", is_primary_evidence=True))

    # Stage D: External Research Permission
    if custom.get("permission"):
        permission = custom["permission"]
    elif non_interactive:
        permission = "scope_only"
    else:
        print(f"\n{msg['stage_d_intro']}")
        print(msg["stage_d_permission"])
        p_ans = input("Choice [2]: ").strip()
        perm_map = {"1": "expand", "2": "scope_only", "3": "none"}
        permission = perm_map.get(p_ans, "scope_only")

    # Stage E: Publication Goals
    venue = custom.get("venue") or "arXiv"
    if not non_interactive and not custom.get("venue"):
        print(f"\n{msg['stage_e_intro']}")
        in_venue = input(f"{msg['stage_e_venue']} [arXiv]: ").strip()
        if in_venue:
            venue = in_venue

    # Stage F & G: Synthesize and approve
    brief = synthesize_research_brief(
        author=author,
        topic=topic,
        title=title,
        research_question=problem,
        original_contribution=contribution,
        research_type=res_type,
        sources=sources,
        permission=permission,
        target_venue=venue,
        language=lang_code,
    )

    if auto_approve or custom.get("approved", False):
        brief.approved = True
        brief.approval_date = datetime.now(timezone.utc).isoformat()
        brief.approved_by = author.name
    elif not non_interactive:
        yaml_path, md_path = save_research_brief(brief, root)
        print("\n" + "=" * 70)
        print("📄 Generated Research Brief Preview:")
        print("=" * 70)
        print(f"Title:         {brief.title}")
        print(f"Author:        {brief.author_profile.name} ({brief.author_profile.affiliation})")
        print(f"Problem:       {brief.research_question}")
        print(f"Contribution:  {brief.original_contribution}")
        print(f"Sources:       {len(brief.sources)} items identified")
        print(f"Permission:    {brief.external_research_permission.upper()}")
        print("=" * 70 + "\n")

        conf = input(f"{msg['brief_confirm']} ").strip().lower()
        if conf in ["", "y", "yes"]:
            brief.approved = True
            brief.approval_date = datetime.now(timezone.utc).isoformat()
            brief.approved_by = author.name
            print("✅ Research Brief APPROVED. You may now proceed with research and manuscript generation.\n")
        else:
            print("⚠️ Research Brief remains UNAPPROVED. Manuscript generation will be blocked by quality gates.\n")

    yaml_path, md_path = save_research_brief(brief, root)
    return (brief, yaml_path, md_path)

