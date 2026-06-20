"""
SEO and GEO (Generative Engine Optimization) helpers.

Everything that makes the site discoverable by search engines AND by AI answer
engines (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews) lives here:

  * per-page <meta>, canonical, Open Graph and Twitter Card data  -> build_meta()
  * Schema.org structured data as JSON-LD                          -> *_jsonld()
  * machine-readable site maps for crawlers and LLMs               -> robots_txt(),
    sitemap_xml(), llms_txt()

Why JSON-LD and llms.txt matter for GEO: answer engines extract entities and
facts from structured data and from clean, linkable summaries far more reliably
than from prose. Declaring an Organization, a Person, Services, Courses, and an
FAQ in machine-readable form makes the brand quotable and citable.

The production domain comes from the SITE_BASE_URL environment variable. When it
is not set (local development) we fall back to the incoming request's base URL,
so canonical, Open Graph, and sitemap links always point at a working host.
Set SITE_BASE_URL to the real domain in production, e.g.

    SITE_BASE_URL=https://www.pasekaseleke.com
"""
from __future__ import annotations

import os

from app.data import content as C

# Absolute path (served from /static) to the social share image.
OG_IMAGE_PATH = "/static/brand/og-image.png"
LOGO_PATH = "/static/brand/favicon-512.png"
DEFAULT_LOCALE = "en_US"
BRAND_SUFFIX = "Paseka Seleke Consultancy"

# Subjects the brand should be associated with in knowledge graphs / AI answers.
KNOWS_ABOUT = [
    "Instructional design",
    "eLearning development",
    "Learning management systems",
    "Moodle administration",
    "Virtual training and webinars",
    "AI in education",
    "Digital academy development",
    "Learner engagement",
    "Multilingual learning",
]


# --------------------------------------------------------------------------- #
#  URL helpers
# --------------------------------------------------------------------------- #
def base_url(request) -> str:
    """Canonical origin with no trailing slash."""
    env = os.getenv("SITE_BASE_URL")
    if env:
        return env.rstrip("/")
    return str(request.base_url).rstrip("/")


def abs_url(request, path: str = "/") -> str:
    """Make an absolute URL from a site-relative path (or pass through http[s])."""
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return base_url(request) + "/" + path.lstrip("/")


def _full_title(page_title: str) -> str:
    # Avoid "Paseka ... | Paseka ..." duplication when the brand is already present.
    if "Paseka" in page_title:
        return page_title
    return f"{page_title} | {BRAND_SUFFIX}"


# --------------------------------------------------------------------------- #
#  Per-page meta (title / description / canonical / OG / Twitter)
# --------------------------------------------------------------------------- #
def build_meta(
    request,
    *,
    title: str,
    description: str,
    path: str = "/",
    image: str = OG_IMAGE_PATH,
    type_: str = "website",
    robots: str = "index, follow",
    keywords: list[str] | None = None,
    published=None,
    modified=None,
) -> dict:
    def _iso(value):
        return value.isoformat() if hasattr(value, "isoformat") else value

    return {
        "title": _full_title(title),
        "description": description,
        "canonical": abs_url(request, path),
        "image": abs_url(request, image),
        "type": type_,
        "robots": robots,
        "keywords": ", ".join(keywords) if keywords else None,
        "author": "Paseka Seleke",
        "site_name": BRAND_SUFFIX,
        "locale": DEFAULT_LOCALE,
        "published": _iso(published),
        "modified": _iso(modified),
    }


# --------------------------------------------------------------------------- #
#  Structured data (JSON-LD). Stable @id values let the nodes reference each
#  other, which search engines and AI models use to build a single entity graph.
# --------------------------------------------------------------------------- #
def _org_id(request) -> str:
    return base_url(request) + "/#organization"


def _person_id(request) -> str:
    return base_url(request) + "/#person"


def organization_jsonld(request) -> dict:
    url = base_url(request)
    return {
        "@context": "https://schema.org",
        "@type": ["Organization", "ProfessionalService"],
        "@id": _org_id(request),
        "name": C.SITE["name"],
        "alternateName": BRAND_SUFFIX,
        "url": url + "/",
        "logo": {"@type": "ImageObject", "url": abs_url(request, LOGO_PATH)},
        "image": abs_url(request, OG_IMAGE_PATH),
        "description": C.SITE["description"],
        "email": C.SITE["email"],
        "telephone": C.SITE["phone"],
        "founder": {"@id": _person_id(request)},
        "address": {
            "@type": "PostalAddress",
            "addressLocality": C.SITE["city"],
            "addressCountry": C.SITE["country_code"],
        },
        "areaServed": ["Africa", "Worldwide"],
        "knowsLanguage": ["English", "French", "Portuguese"],
        "knowsAbout": KNOWS_ABOUT,
        "sameAs": [C.SITE["linkedin"]],
    }


def person_jsonld(request) -> dict:
    url = base_url(request)
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": _person_id(request),
        "name": "Paseka Seleke",
        "url": url + "/about",
        "jobTitle": "eLearning and Digital Learning Specialist",
        "description": C.CV["summary"],
        "image": abs_url(request, OG_IMAGE_PATH),
        "email": C.SITE["email"],
        "telephone": C.SITE["phone"],
        "worksFor": {"@id": _org_id(request)},
        "address": {
            "@type": "PostalAddress",
            "addressLocality": C.SITE["city"],
            "addressCountry": C.SITE["country_code"],
        },
        "knowsLanguage": ["English", "French", "Portuguese"],
        "knowsAbout": C.CV["skills"],
        "sameAs": [C.SITE["linkedin"]],
    }


def website_jsonld(request) -> dict:
    url = base_url(request)
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": url + "/#website",
        "name": C.SITE["name"],
        "url": url + "/",
        "inLanguage": "en",
        "publisher": {"@id": _org_id(request)},
    }


def breadcrumb_jsonld(request, items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": abs_url(request, path),
            }
            for i, (name, path) in enumerate(items)
        ],
    }


def faq_jsonld(request, faqs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
            for question, answer in faqs
        ],
    }


def service_jsonld(request, data: dict, slug: str) -> dict:
    items = [item for group in data.get("groups", []) for item in group.get("items", [])]
    offers = {
        "@type": "OfferCatalog",
        "name": data["title"],
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": item}}
            for item in items
        ],
    }
    node = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": data["title"],
        "serviceType": data["nav_label"],
        "description": data["intro"],
        "url": abs_url(request, f"/services/{slug}"),
        "provider": {"@id": _org_id(request)},
        "areaServed": ["Africa", "Worldwide"],
        "availableLanguage": ["English", "French", "Portuguese"],
    }
    if items:
        node["hasOfferCatalog"] = offers
    return node


def course_jsonld(request, course) -> dict:
    teaches = [line.strip() for line in (course.outcomes or "").split("\n") if line.strip()]
    return {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": course.title,
        "description": course.summary,
        "url": abs_url(request, f"/samples/{course.slug}"),
        "inLanguage": "en",
        "isAccessibleForFree": True,
        "provider": {"@id": _org_id(request)},
        "educationalCredentialAwarded": "Sample course (portfolio demonstration)",
        "audience": {"@type": "EducationalAudience", "educationalRole": course.audience},
        "teaches": teaches,
        "hasCourseInstance": {
            "@type": "CourseInstance",
            "courseMode": "online",
            "courseWorkload": course.duration,
        },
    }


def blogposting_jsonld(request, post) -> dict:
    published = post.published.isoformat()
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "description": post.excerpt,
        "articleSection": post.category,
        "datePublished": published,
        "dateModified": published,
        "url": abs_url(request, f"/blog/{post.slug}"),
        "mainEntityOfPage": abs_url(request, f"/blog/{post.slug}"),
        "image": abs_url(request, post.image_path or OG_IMAGE_PATH),
        "inLanguage": "en",
        "author": {"@id": _person_id(request)},
        "publisher": {"@id": _org_id(request)},
    }


# --------------------------------------------------------------------------- #
#  Page-level builders: (meta, jsonld) ready to drop into the template context.
# --------------------------------------------------------------------------- #
def _site_graph(request) -> list[dict]:
    """The base entity graph included on most pages."""
    return [organization_jsonld(request), person_jsonld(request), website_jsonld(request)]


def home_seo(request):
    meta = build_meta(
        request,
        title="Paseka Seleke | eLearning, LMS and AI-Powered Learning Consultancy",
        description=C.SITE["description"],
        path="/",
        keywords=[
            "eLearning consultant",
            "instructional design",
            "Moodle administration",
            "LMS consultant",
            "virtual training",
            "AI in learning",
            "digital academy",
            "Kigali Rwanda",
        ],
    )
    jsonld = _site_graph(request) + [faq_jsonld(request, C.FAQS)]
    return meta, jsonld


def about_seo(request):
    meta = build_meta(
        request,
        title="About Paseka Seleke",
        description=(
            "Meet Paseka Seleke, an eLearning specialist in Moodle administration, "
            "instructional design, webinar facilitation, and AI-enabled learning "
            "across Africa."
        ),
        path="/about",
        type_="profile",
    )
    jsonld = _site_graph(request) + [
        breadcrumb_jsonld(request, [("Home", "/"), ("About", "/about")]),
    ]
    return meta, jsonld


def service_seo(request, data: dict, slug: str):
    meta = build_meta(
        request,
        title=data["title"],
        description=data["intro"],
        path=f"/services/{slug}",
        keywords=[data["nav_label"], "eLearning", "learning consultancy", C.SITE["city"]],
    )
    jsonld = [
        organization_jsonld(request),
        service_jsonld(request, data, slug),
        breadcrumb_jsonld(
            request,
            [("Home", "/"), ("Services", f"/services/{slug}"), (data["nav_label"], f"/services/{slug}")],
        ),
    ]
    return meta, jsonld


def samples_seo(request):
    meta = build_meta(
        request,
        title="Sample Courses",
        description=(
            "Step into interactive sample courses with knowledge checks scored on the "
            "server. See how Paseka Seleke designs engaging, outcomes-first learning."
        ),
        path="/samples",
    )
    jsonld = _site_graph(request) + [
        breadcrumb_jsonld(request, [("Home", "/"), ("Sample Courses", "/samples")]),
    ]
    return meta, jsonld


def sample_detail_seo(request, course):
    meta = build_meta(
        request,
        title=course.title,
        description=course.summary,
        path=f"/samples/{course.slug}",
        type_="article",
    )
    jsonld = [
        organization_jsonld(request),
        course_jsonld(request, course),
        breadcrumb_jsonld(
            request,
            [("Home", "/"), ("Sample Courses", "/samples"), (course.title, f"/samples/{course.slug}")],
        ),
    ]
    return meta, jsonld


def blog_seo(request):
    meta = build_meta(
        request,
        title="Paseka's Thoughts",
        description=(
            "Articles on instructional design, LMS strategy, learner engagement, and "
            "practical AI for digital learning teams, by Paseka Seleke."
        ),
        path="/blog",
    )
    jsonld = _site_graph(request) + [
        breadcrumb_jsonld(request, [("Home", "/"), ("Articles", "/blog")]),
    ]
    return meta, jsonld


def blog_post_seo(request, post):
    meta = build_meta(
        request,
        title=post.title,
        description=post.excerpt,
        path=f"/blog/{post.slug}",
        image=post.image_path or OG_IMAGE_PATH,
        type_="article",
        published=post.published,
        modified=post.published,
    )
    jsonld = [
        organization_jsonld(request),
        blogposting_jsonld(request, post),
        breadcrumb_jsonld(
            request,
            [("Home", "/"), ("Articles", "/blog"), (post.title, f"/blog/{post.slug}")],
        ),
    ]
    return meta, jsonld


def contact_seo(request):
    meta = build_meta(
        request,
        title="Contact",
        description=(
            "Book a consultation with Paseka Seleke for instructional design, LMS setup, "
            "virtual training, and AI-powered learning. Based in Kigali, Rwanda."
        ),
        path="/contact",
    )
    jsonld = _site_graph(request) + [
        breadcrumb_jsonld(request, [("Home", "/"), ("Contact", "/contact")]),
    ]
    return meta, jsonld


# --------------------------------------------------------------------------- #
#  Crawler and LLM site maps
# --------------------------------------------------------------------------- #
# AI answer-engine crawlers we explicitly welcome (GEO). Being listed (and
# allowed) is what lets these systems read and cite the site.
AI_CRAWLERS = [
    "GPTBot",          # OpenAI training/index
    "OAI-SearchBot",   # ChatGPT search
    "ChatGPT-User",    # ChatGPT browsing on a user's behalf
    "ClaudeBot",       # Anthropic
    "Claude-Web",
    "anthropic-ai",
    "PerplexityBot",   # Perplexity
    "Perplexity-User",
    "Google-Extended",  # Gemini / AI Overviews opt-in
    "Applebot-Extended",
    "Amazonbot",
    "Bytespider",
    "CCBot",           # Common Crawl (feeds many models)
    "cohere-ai",
    "Meta-ExternalAgent",
]


def robots_txt(request) -> str:
    sitemap = abs_url(request, "/sitemap.xml")
    llms = abs_url(request, "/llms.txt")
    lines = [
        "# robots.txt — search engines and AI answer engines are welcome.",
        "User-agent: *",
        "Allow: /",
        "",
    ]
    for bot in AI_CRAWLERS:
        lines += [f"User-agent: {bot}", "Allow: /", ""]
    lines += [f"Sitemap: {sitemap}", f"# LLM guide: {llms}", ""]
    return "\n".join(lines)


def sitemap_xml(request, courses, posts) -> str:
    def url_entry(path, *, lastmod=None, changefreq="monthly", priority="0.6") -> str:
        loc = abs_url(request, path)
        parts = [f"    <loc>{loc}</loc>"]
        if lastmod:
            parts.append(f"    <lastmod>{lastmod}</lastmod>")
        parts.append(f"    <changefreq>{changefreq}</changefreq>")
        parts.append(f"    <priority>{priority}</priority>")
        body = "\n".join(parts)
        return f"  <url>\n{body}\n  </url>"

    entries = [
        url_entry("/", changefreq="weekly", priority="1.0"),
        url_entry("/about", priority="0.8"),
        url_entry("/samples", changefreq="weekly", priority="0.8"),
        url_entry("/blog", changefreq="weekly", priority="0.8"),
        url_entry("/contact", priority="0.7"),
    ]
    for slug in C.SERVICE_PAGES:
        entries.append(url_entry(f"/services/{slug}", priority="0.9"))
    for course in courses:
        entries.append(url_entry(f"/samples/{course.slug}", priority="0.7"))
    for post in posts:
        entries.append(
            url_entry(f"/blog/{post.slug}", lastmod=post.published.isoformat(), priority="0.6")
        )

    body = "\n".join(entries)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )


def llms_txt(request, courses, posts) -> str:
    """A curated, markdown map of the site for LLMs (see llmstxt.org).

    Gives answer engines a clean, linkable overview so they can summarise and
    cite the site accurately instead of guessing from rendered HTML.
    """
    def link(label, path, note):
        return f"- [{label}]({abs_url(request, path)}): {note}"

    lines = [
        "# Paseka Seleke - Consultancy Services",
        "",
        f"> {C.SITE['description']}",
        "",
        "Paseka Seleke is an eLearning and digital learning specialist based in "
        f"{C.SITE['city']}, {C.SITE['country']}, working in English, French, and "
        "Portuguese with organisations across Africa and worldwide.",
        "",
        "## Services",
    ]
    for slug, data in C.SERVICE_PAGES.items():
        lines.append(link(data["title"], f"/services/{slug}", data["intro"]))

    lines += ["", "## Key pages"]
    lines += [
        link("About Paseka Seleke", "/about", "Background, experience, skills, and tools."),
        link("Sample courses", "/samples", "Interactive demo courses with server-scored knowledge checks."),
        link("Articles (Paseka's Thoughts)", "/blog", "Articles on instructional design, LMS strategy, and AI in learning."),
        link("Contact", "/contact", "Request a consultation or proposal."),
    ]

    if courses:
        lines += ["", "## Sample courses"]
        for course in courses:
            lines.append(link(course.title, f"/samples/{course.slug}", course.summary))

    if posts:
        lines += ["", "## Articles"]
        for post in posts:
            lines.append(link(post.title, f"/blog/{post.slug}", post.excerpt))

    lines += ["", "## Frequently asked questions"]
    for question, answer in C.FAQS:
        lines += [f"### {question}", answer, ""]

    lines += [
        "## Contact",
        f"- Email: {C.SITE['email']}",
        f"- Phone: {C.SITE['phone']}",
        f"- Location: {C.SITE['city']}, {C.SITE['country']}",
        f"- LinkedIn: {C.SITE['linkedin']}",
        "",
    ]
    return "\n".join(lines)
