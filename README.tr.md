# ScholarProvenance

<p align="center">
  <strong>Teknik kanıtları ve deneyleri izlenebilir akademik makalelere dönüştürün.</strong><br>
  <em>Araştırmacılar, mühendisler ve teknik ekipler için açık kaynaklı, kanıt odaklı yapay zeka ajan becerisi.</em>
</p>

<p align="center">
  <a href="README.md"><strong>English</strong></a> •
  <a href="README.fa.md"><strong>فارسی</strong></a> •
  <a href="README.tr.md"><strong>Türkçe</strong></a> •
  <a href="README.az.md"><strong>Azərbaycan dili</strong></a> •
  <a href="README.ar.md"><strong>العربية</strong></a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/lisans-MIT-blue.svg" alt="Lisans: MIT"></a>
  <a href="https://github.com/tmolavi/scholar-provenance/releases"><img src="https://img.shields.io/badge/s%C3%BCr%C3%BCm-v0.1.0-emerald.svg" alt="Sürüm: v0.1.0"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
  <a href="SHOWCASE.md"><img src="https://img.shields.io/badge/topluluk-vitrini-purple.svg" alt="Vitrini"></a>
</p>

---

## ScholarProvenance Nedir?

Mühendisler, bağımsız araştırmacılar ve teknik ekipler genellikle ellerinde değerli birincil kanıtlara sahiptir:
- Kıyaslama (benchmark) sonuçları ve ham deney çıktıları (CSV, JSON, sistem günlükleri)
- Açık kaynaklı yazılım depoları ve sistem mimarisi tasarımları
- Veri kümeleri, teknik dokümantasyonlar ve araştırma notları

Ancak bu materyalleri bilimsel olarak savunulabilir bir akademik makaleye dönüştürmek; yanlışlanabilir araştırma soruları formüle etmeyi, literatür taramasını, çelişkili kanıtların incelenmesini ve kaynak doğrulamasını gerektirir.

**ScholarProvenance**, uydurma kaynak (halüsinasyon) üretmeksizin bu süreci otomatikleştiren taşınabilir bir yapay zeka ajan becerisidir:

> **Dokümantasyonunuzu, deneylerinizi, veri kümelerinizi, depolarınızı ve kaynaklarınızı getirin.**  
> Ajan, ilgili literatürü araştırır, kanıtları doğrular, araştırma boşluğunu tespit eder, kaynak izlenebilirliğini kurar ve yayına hazır akademik makaleler üretir.  
> **Bu araç sahte araştırma üretmez; kanıtlarla desteklenebilecek bilimsel çalışmaları belgeler.**

---

## Temel İlke: Yazımdan Önce Kanıt

Yazım süreci daima araştırmanın ardılıdır. ScholarProvenance, doğrulanmış bir Kanıt Defteri (Evidence Ledger) oluşturulmadan metin yazımına başlanmasını kesin olarak engeller.

```
[KULLANICI KANITLARI VE BELGELERİ]
       ↓
Aşama 01: İnceleme ve 16 Standart Kanıt Sınıfına Ayırma
       ↓
Aşama 02: Araştırma Sorularının ve Kapsamın Belirlenmesi
       ↓
Aşama 03: Açık Akademik Literatür Araması (OpenAlex, Crossref, arXiv)
       ↓
Aşama 04: Sıfır-Uydurma Kaynak Doğrulama Kapısı
       ↓
Aşama 05: Kanıt Matrisi Sentezi (evidence-matrix.json & .md)
       ↓
Aşama 06: Çelişkili Kanıt ve Olumsuz Bulguların Taranması
       ↓
Aşama 07: Araştırma Boşluğu Analizi ve Özgünlük Teyidi
       ↓
Aşama 08: Metodoloji Gerekçelendirmesi ve İstatistiksel Disiplin
       ↓
Aşama 09: İddia-Kanıt Denetimi ve Aşırı İddiaların Ayıklanması
       ↓
Aşama 10: Çok Dilli Dizgi (HTML, PDF, DOCX, LaTeX)
       ↓
Aşama 11: Karşıt Hakem Değerlendirmesi (Hakem 1 ve Hakem 2 Simülasyonu)
       ↓
Aşama 12: Güvenlik Taraması ve 12 Kalite Kapısı Onayı
```

---

## Öne Çıkan Özellikler

1. **Sıfır Uydurma Alıntı:** Tüm kaynaklar gerçek akademik veritabanlarından teyit edilir. Yapay zeka hafızasından uydurma DOI veya yazar türetilemez.
2. **Kullanıcı Kaynakları Yönü Belirler:** Kullanıcının sunduğu kanıtlar çalışmanın odağını oluşturur; harici literatür araştırması konuyu değiştiremez.
3. **Çok Formatlı Çıktı:** Tek bir kaynak metinden semantik HTML5, WeasyPrint tabanlı PDF, düzenlenebilir DOCX ve LaTeX/BibTeX üretilir.
4. **Saf Vektör SVG Grafikleri:** Harici kütüphane gerektirmeyen akademik çubuk grafikler ve mimari diyagramları.

---

## Kurulum

```bash
pip install git+https://github.com/tmolavi/scholar-provenance.git
```

Geliştirme için:

```bash
git clone https://github.com/tmolavi/scholar-provenance.git
cd scholar-provenance
pip install -e ".[dev]"
```

---

## Başlarken — Zorunlu Ön Araştırma Mülakatı (Research Intake)

Herhangi bir metin taslağı oluşturulmadan önce, ScholarProvenance ampirik kanıtları ve yayın hedeflerini belirlemek üzere **Zorunlu Araştırma Mülakatı** yürütür:

### Örnek Araştırma Özeti (`research-brief.yaml`)

```yaml
approved: true
approval_date: "2026-10-08T10:00:00Z"
approved_by: "Taghi Molavi"

author_profile:
  name: "Taghi Molavi"
  affiliation: "Independent Researcher"
  email: "info@molavi.pro"

topic: "Kurumsal Yapay Zeka Sistemleri ve ERP Entegrasyonu"
title: "Deterministic Metric Calculations for Executive AI Agents"
research_question: "ERP verileri halüsinasyon olmadan yerel LLM'lere nasıl bağlanır?"
original_contribution: "Çift katmanlı kanıt defteri ile sıfır uydurma kaynakça mimarisi"
research_type: "empirical"
sources:
  - url_or_path: "inputs/benchmark_results.csv"
    source_type: "dataset"
    is_primary_evidence: true
external_research_permission: "scope_only"
publication_preferences:
  target_venue: "arXiv"
  citation_style: "ieee"
```

---

## Tek Komut Deneyimi

Ajan ortamınızda tek bir istemle araştırmayı başlatabilirsiniz:

```markdown
"Bu depoyu, bu belgeleri ve bu bağlantıları temel kanıt olarak kullan.
Adım [ADINIZ].
Makaleyi Türkçe olarak hazırla.
İlgili güncel akademik literatürü araştır, her alıntıyı doğrula,
gerekirse kanıtlarımı sorgula ve kaynakçası, şekilleri, grafikleri,
PDF ve DOCX çıktılarıyla nihai makaleyi üret."
```

---

## Bu Proje Neden Var?

Bu çalışma; yapay zeka sistemleri, teknik deneyler ve kıyaslamalar içeren gerçek mühendislik çalışmalarını akademik standartlarda belgelemenin zorluklarından doğmuştur. Dünyadaki tüm bağımsız araştırmacıların ve mühendislerin çalışmalarını bilimsel titizlikle yayınlayabilmesi için açık kaynak olarak paylaşılmıştır.

> **Öğren. Öğret. Kalıcı bir şey üret.**

---

## Geliştirici ve Sürdürücü

**Taghi Molavi** tarafından tasarlanmış ve geliştirilmektedir. Yapay Zeka Arama (AI Search), Üretici Motor Optimizasyonu (GEO), Yapay Zeka Görünürlüğü ve uygulamalı yapay zeka sistemleri üzerine çalışan bağımsız araştırmacı ve yapay zeka sistemleri mimarıdır.

- Kişisel Web Sitesi: [molavi.pro](https://molavi.pro)
- GitHub Profili: [@tmolavi](https://github.com/tmolavi)
- İletişim: `info@molavi.pro`

### Yazılım Geliştiriciliği ve Makale Yazarlığı Ayrımı
Taghi Molavi bu açık kaynak aracın ve araştırma metodolojisinin geliştiricisidir; diğer kullanıcıların bu araçla ürettiği makalelerin yazarı değildir. Makale yazarlığı daima kullanıcı yapılandırmasından gelir.

---

## Atıf (Citation)

```bibtex
@software{molavi2026scholarprovenance,
  author       = {Molavi, Taghi},
  title        = {{ScholarProvenance: Academic Evidence, Literature Verification \& Paper Generation Skill}},
  year         = {2026},
  publisher    = {GitHub},
  version      = {0.2.0},
  url          = {https://github.com/tmolavi/scholar-provenance}
}
```

---

## Lisans

Bu proje **MIT Lisansı** ile lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.
