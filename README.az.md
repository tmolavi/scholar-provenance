# ScholarProvenance

<p align="center">
  <strong>Real texniki sübutları və təcrübələri izlənilə bilən elmi məqalələrə çevirin.</strong><br>
  <em>Tədqiqatçılar, mühəndislər və texniki komandalar üçün açıq mənbəli, sübuta əsaslanan süni intellekt agent bacarığı.</em>
</p>

<p align="center">
  <a href="README.md"><strong>English</strong></a> •
  <a href="README.fa.md"><strong>فارسی</strong></a> •
  <a href="README.tr.md"><strong>Türkçe</strong></a> •
  <a href="README.az.md"><strong>Azərbaycan dili</strong></a> •
  <a href="README.ar.md"><strong>العربية</strong></a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/lisenziya-MIT-blue.svg" alt="Lisenziya: MIT"></a>
  <a href="https://github.com/tmolavi/scholar-provenance/releases"><img src="https://img.shields.io/badge/burax%C4%B1l%C4%B1%C5%9F-v0.1.0-emerald.svg" alt="Buraxılış: v0.1.0"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
  <a href="SHOWCASE.md"><img src="https://img.shields.io/badge/icma-vitrini-purple.svg" alt="İcma vitrini"></a>
</p>

---

## ScholarProvenance Nədir?

Mühəndislər, müstəqil tədqiqatçılar və texniki komandalar adətən dəyərli ilkin sübutlara sahibdirlər:
- Bençmark nəticələri və xam təcrübə qeydləri (CSV, JSON, sistem loqları)
- Açıq mənbəli proqram təminatı repozitoriyaları və memarlıq layihələri
- Məlumat dəstləri, texniki sənədlər və tədqiqat qeydləri

Lakin bu materialları elmi cəhətdən əsaslandırılmış akademik məqaləyə çevirmək; dəqiq tədqiqat suallarının formalaşdırılmasını, sistemli ədəbiyyat axtarışını, ziddiyyətli sübutların təhlilini və mənbələrin yoxlanılmasını tələb edir.

**ScholarProvenance**, uydurma istinad (hallüsinasiya) yaratmadan bu prosesi avtomatlaşdıran daşına bilən süni intellekt agent bacarığıdır:

> **Sənədlərinizi, təcrübələrinizi, məlumat dəstlərinizi və mənbələrinizi təqdim edin.**  
> Agent əlaqəli ədəbiyyatı araşdırır, sübutları təsdiqləyir, elmi boşluğu müəyyənləşdirir, istinadların mənşəyini qurur və çapa hazır akademik məqalələr hazırlayır.  
> **Bu alət saxta tədqiqat uydurmur; sübutlarla əsaslandırıla bilən elmi işləri sənədləşdirir.**

---

## Əsas Prinsip: Yazıdan Əvvəl Sübut

Yazı prosesi hər zaman tədqiqatdan sonra gəlir. ScholarProvenance təsdiqlənmiş Sübut Kitabı (Evidence Ledger) qurulmadan əlyazmanın yazılmasına icazə vermir.

```
[İSTİFADƏÇİ TƏRƏFİNDƏN TƏQDİM EDİLƏN MATERİALLAR]
       ↓
Mərhələ 01: Təhlil və 16 Standart Sübut Kateqoriyasına Ayırma
       ↓
Mərhələ 02: Tədqiqat Suallarının və Çərçivənin Təyini
       ↓
Mərhələ 03: Açıq Elmi Ədəbiyyat Axtarışı (OpenAlex, Crossref, arXiv)
       ↓
Mərhələ 04: Sıfır-Uydurma Mənbə Yoxlama Qapısı
       ↓
Mərhələ 05: Sübut Matrisinin Qovuşdurulması (evidence-matrix.json & .md)
       ↓
Mərhələ 06: Ziddiyyətli Sübutların və Mənfi Nəticələrin Axtarışı
       ↓
Mərhələ 07: Tədqiqat Boşluğu Təhlili və Yeniliyin Yoxlanılması
       ↓
Mərhələ 08: Metodologiyanın Əsaslandırılması və Statistik İntizam
       ↓
Mərhələ 09: İddia-Sübut Auditi və Şişirdilmiş İddiaların Çıxarılması
       ↓
Mərhələ 10: Çoxdilli Tərtibat (HTML, PDF, DOCX, LaTeX)
       ↓
Mərhələ 11: Tənqidi Rəyçi Simulyasiyası (Rəyçi 1 və Rəyçi 2)
       ↓
Mərhələ 12: Məxfilik Yoxlanışı və 12 Keyfiyyət Qapısının Təsdiqi
```

---

## Quraşdırma

```bash
pip install git+https://github.com/tmolavi/scholar-provenance.git
```

---

## Tək Sorğu Təcrübəsi

```markdown
"Bu repozitoriyanı və sənədləri əsas sübut kimi istifadə et.
Adım [ADINIZ].
Məqaləni Azərbaycan dilində hazırla.
Əlaqəli müasir elmi ədəbiyyatı araşdır, hər bir istinadı yoxla,
lazım gələrsə sübutlarımı şübhə altına al və ədəbiyyat siyahısı,
diaqramlar, qrafiklər, PDF və DOCX faylları ilə birlikdə yekun məqaləni tərtib et."
```

---

## Layihənin Müəllifi

Layihə **Taghi Molavi** tərəfindən yaradılmış və idarə olunur. Süni İntellekt Axtarışı (AI Search), Generativ Mühərrik Optimizasiyası (GEO), AI Görünürlüyü və tətbiqi süni intellekt sistemləri üzrə müstəqil tədqiqatçı və sistem arxitektorudur.

- Şəxsi Vebsayt: [molavi.pro](https://molavi.pro)
- GitHub Profili: [@tmolavi](https://github.com/tmolavi)
- Əlaqə: `info@molavi.pro`

> **Öyrən. Öyrət. Qalıcı bir şey yarat.**

---

## Lisenziya

Bu layihə **MIT Lisenziyası** altında yayımlanır. Ətraflı məlumat üçün [LICENSE](LICENSE) faylına baxın.
