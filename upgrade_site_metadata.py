#!/usr/bin/env python3
import os, json, glob, datetime, re
from urllib.parse import urljoin

SITE_URL = "https://wealthyrobots.com/"
ROOT = "wealthyrobots_website"

# GA4
GA_MEASUREMENT_ID = "G-WN2DRKBWRF"
GA_SNIPPET = (
    "<!-- Google tag (gtag.js) -->\n"
    f"<script async src=\"https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}\"></script>\n"
    "<script>\n"
    "  window.dataLayer = window.dataLayer || [];\n"
    "  function gtag(){dataLayer.push(arguments);}\n"
    "  gtag('js', new Date());\n"
    f"  gtag('config', '{GA_MEASUREMENT_ID}');\n"
    "</script>\n"
)

ORG_JSONLD = {
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "WealthyRobot Empire",
  "url": SITE_URL,
  "logo": urljoin(SITE_URL, "assets/img/logo.png"),
  "sameAs": ["https://twitter.com/WealthyRobot"]
}

RSS_LINK_TAG = '<link rel="alternate" type="application/rss+xml" title="WealthyRobot Empire" href="/feed.xml">'
SITEMAP_LINK_TAG = '<link rel="sitemap" type="application/xml" title="Sitemap" href="/sitemap.xml">'

RSS_HEADER = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<rss version=\"2.0\">\n<channel>\n<title>WealthyRobot Empire</title>\n<link>{site}</link>\n<description>AI automation strategies that actually make money</description>\n<lastBuildDate>{now}</lastBuildDate>\n"""
RSS_ITEM = """\n<item>\n<title>{title}</title>\n<link>{link}</link>\n<guid>{link}</guid>\n<pubDate>{now}</pubDate>\n</item>\n"""
RSS_FOOTER = """\n</channel>\n</rss>\n"""

def ensure_head_links(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    changed = False
    if RSS_LINK_TAG not in html and '</head>' in html:
        html = html.replace('</head>', RSS_LINK_TAG + '\n' + '</head>')
        changed = True
    if SITEMAP_LINK_TAG not in html and '</head>' in html:
        html = html.replace('</head>', SITEMAP_LINK_TAG + '\n' + '</head>')
        changed = True
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

def ensure_ga_tag(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    if GA_MEASUREMENT_ID in html:
        return
    if '<head>' in html:
        html = html.replace('<head>', '<head>\n' + GA_SNIPPET)
    elif '</head>' in html:
        html = html.replace('</head>', GA_SNIPPET + '</head>')
    else:
        return
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

FOOTER_LINKS = '''<div class="footer-links">
  <a href="/feed.xml">RSS</a> · 
  <a href="/sitemap.xml">Sitemap</a>
</div>'''

def ensure_footer_links(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    if 'href="/feed.xml"' in html and 'href="/sitemap.xml"' in html:
        return
    if '<div class="footer-bottom">' in html:
        html = html.replace('<div class="footer-bottom">', FOOTER_LINKS + '\n<div class="footer-bottom">')
    elif '</footer>' in html:
        html = html.replace('</footer>', FOOTER_LINKS + '\n</footer>')
    else:
        return
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


def inject_jsonld_to_html(path, breadcrumb=None, article=None):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    scripts = []
    scripts.append(f'<script type="application/ld+json">{json.dumps(ORG_JSONLD)}</script>')
    if breadcrumb:
        scripts.append(f'<script type="application/ld+json">{json.dumps(breadcrumb)}</script>')
    if article:
        scripts.append(f'<script type="application/ld+json">{json.dumps(article)}</script>')
    if '</head>' in html:
        html = html.replace('</head>', '\n'.join(scripts) + '\n</head>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)


def generate_breadcrumb(path_parts):
    item_list = []
    agg = SITE_URL.rstrip('/')
    for i, part in enumerate(path_parts, start=1):
        agg = agg + '/' + part
        item_list.append({"@type": "ListItem", "position": i, "name": part.capitalize(), "item": agg + ('/' if i < len(path_parts) else '')})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": item_list}


def tokenize(title: str):
    words = re.findall(r"[a-zA-Z0-9]+", title.lower())
    stop = {"the","a","an","for","and","or","of","to","in","with","on","ai","2025","20250806"}
    return [w for w in words if w not in stop and len(w) > 2]


def build_related(articles_info, current_key, k=3):
    base_tokens = set(articles_info[current_key]["tokens"])
    scores = []
    for key, info in articles_info.items():
        if key == current_key:
            continue
        overlap = len(base_tokens.intersection(info["tokens"]))
        if overlap > 0:
            scores.append((overlap, key))
    scores.sort(reverse=True)
    top = [key for _, key in scores[:k]]
    return top


def insert_related_block(html: str, related_links):
    if 'class="related-articles"' in html:
        return html
    block_items = '\n'.join([f'<li><a href="{href}">{title}</a></li>' for title, href in related_links])
    block = f'''\n<section class="related-block">\n  <h3>Related Articles</h3>\n  <ul class="related-articles">\n    {block_items}\n  </ul>\n</section>\n'''
    if '<footer class="article-footer">' in html:
        return html.replace('<footer class="article-footer">', block + '<footer class="article-footer">')
    if '</article>' in html:
        return html.replace('</article>', block + '</article>')
    if '</body>' in html:
        return html.replace('</body>', block + '</body>')
    return html


def ensure_robots_sitemaps(section_list):
    robots_path = os.path.join(ROOT, 'robots.txt')
    if not os.path.exists(robots_path):
        # create a minimal robots with sitemaps
        lines = ["User-agent: *", "Allow: /", ""]
    else:
        with open(robots_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
    # remove existing sitemap lines
    lines = [l for l in lines if not l.lower().startswith('sitemap:')]
    # add main sitemap and section sitemaps
    sitemap_lines = [f"Sitemap: {urljoin(SITE_URL, 'sitemap.xml')}\n"]
    for sec in section_list:
        sitemap_lines.append(f"Sitemap: {urljoin(SITE_URL, f'sitemap_{sec}.xml')}\n")
    # ensure newline separation
    content = "\n".join(lines).strip() + "\n" + "".join(sitemap_lines)
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(content)


def upgrade_all():
    now_http = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    # Home
    for path in [os.path.join(ROOT, 'index.html')]:
        if os.path.exists(path):
            inject_jsonld_to_html(path)
            ensure_head_links(path)
            ensure_footer_links(path)
            ensure_ga_tag(path)

    # Section indexes
    sections = ['articles','strategies','tools','resources','about','contact','privacy','terms']
    for section in sections:
        idx = os.path.join(ROOT, section, 'index.html')
        if os.path.exists(idx):
            bc = generate_breadcrumb([section])
            inject_jsonld_to_html(idx, breadcrumb=bc)
            ensure_head_links(idx)
            ensure_footer_links(idx)
            ensure_ga_tag(idx)

    # Articles JSON-LD + RSS + Related + head/footer + GA
    rss_items = []
    articles = sorted(glob.glob(os.path.join(ROOT,'articles','article_*.html')))
    info = {}
    for a in articles:
        name = os.path.basename(a)
        title = name.replace('article_','').replace('_',' ').replace('.html','').title()
        link = urljoin(SITE_URL, f'articles/{name}')
        info[name] = {"title": title, "link": link, "path": a, "tokens": tokenize(title)}
    for name, meta in info.items():
        a = meta["path"]
        title = meta["title"]
        link = meta["link"]
        bc = generate_breadcrumb(['articles', name.replace('.html','')])
        article_ld = {"@context":"https://schema.org","@type":"Article","headline": title,"url": link,"author": {"@type":"Organization","name":"WealthyRobot Empire"},"publisher": {"@type":"Organization","name":"WealthyRobot Empire"}}
        inject_jsonld_to_html(a, breadcrumb=bc, article=article_ld)
        ensure_head_links(a)
        ensure_footer_links(a)
        ensure_ga_tag(a)
        related_keys = build_related(info, name, k=3)
        related_links = [(info[k]["title"], f'/articles/{k}') for k in related_keys]
        with open(a,'r',encoding='utf-8') as f:
            html = f.read()
        new_html = insert_related_block(html, related_links)
        if new_html != html:
            with open(a,'w',encoding='utf-8') as f:
                f.write(new_html)
        rss_items.append(RSS_ITEM.format(title=title, link=link, now=now_http))

    # Write RSS
    rss_path = os.path.join(ROOT, 'feed.xml')
    with open(rss_path,'w',encoding='utf-8') as f:
        f.write(RSS_HEADER.format(site=SITE_URL, now=now_http) + '\n'.join(rss_items) + RSS_FOOTER)

    # Section sitemaps
    def write_sitemap(section):
        paths = []
        if section=='articles':
            for a in articles:
                name = os.path.basename(a)
                paths.append(urljoin(SITE_URL, f'articles/{name}'))
        else:
            idx = urljoin(SITE_URL, f'{section}/')
            paths.append(idx)
        xml = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for p in paths:
            xml.append(f'<url><loc>{p}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>')
        xml.append('</urlset>')
        with open(os.path.join(ROOT, f'sitemap_{section}.xml'),'w',encoding='utf-8') as f:
            f.write('\n'.join(xml))
    for sec in sections:
        write_sitemap(sec)

    # Ensure robots.txt lists all sitemaps
    ensure_robots_sitemaps(sections)

if __name__ == '__main__':
    upgrade_all()
    print('✅ Metadata + GA + related links + head/footer links updated, RSS and sitemaps generated, robots.txt sitemap lines managed')
