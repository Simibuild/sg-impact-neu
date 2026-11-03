"""Generiert alle HTML-Seiten der neuen SG-Impact-Webseite.

Aufruf aus dem Projektordner:  python3 _build/build.py
Die Seiten landen eine Ebene darüber (also direkt in sg-impact-neu/).
Kopf, Fuß, SEO-Daten und Referenzen stehen nur hier, damit Änderungen überall gleich wirken.
"""
import json
import os
import re
import html as H

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
ALT_SRC = os.path.abspath(os.path.join(OUT, '..', 'sg-impact'))  # alte Seite, nur für Impressum/Datenschutz

BASE = 'https://www.sg-impact.de'
TODAY = '2026-11-03'
PHONE = '+49 151 59102629'
PHONE_TEL = '+4915159102629'
MAIL = 'info@giesbrecht-s.de'
ADDR = 'Beethovenstr. 4, 57577 Hamm/Sieg'
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
           "%3Crect width='100' height='100' rx='22' fill='%23C94F1A'/%3E%3Ctext x='50' y='66' "
           "font-family='Arial, sans-serif' font-weight='900' font-size='46' fill='white' "
           "text-anchor='middle'%3ESG%3C/text%3E%3C/svg%3E")

ICONS = {
    'monitor': '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 21h8M12 18v3"/>',
    'search': '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    'bolt': '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
    'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    'pin': '<path d="M21 10c0 6-9 12-9 12s-9-6-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    'mail': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
    'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    'chart': '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'file': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/>',
    'bot': '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01M9 17h6"/>',
    'briefcase': '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>',
    'star': '<path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
    'globe': '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/>',
}


def icon(name):
    return ('<div class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + ICONS[name] + '</svg></div>')


def fill(s):
    return (s.replace('{{PHONE}}', PHONE).replace('{{PHONE_TEL}}', PHONE_TEL)
             .replace('{{MAIL}}', MAIL).replace('{{ADDR}}', ADDR))


NAV = [('leistungen.html', 'Leistungen'), ('referenzen.html', 'Referenzen'),
       ('index.html#ueber-mich', 'Über mich'), ('faq.html', 'FAQ')]

ORG = {
    '@context': 'https://schema.org',
    '@type': 'ProfessionalService',
    '@id': BASE + '/#business',
    'name': 'SG-Impact',
    'url': BASE + '/',
    'telephone': PHONE,
    'email': MAIL,
    'founder': {'@type': 'Person', 'name': 'Simeon Giesbrecht'},
    'address': {'@type': 'PostalAddress', 'streetAddress': 'Beethovenstr. 4',
                'postalCode': '57577', 'addressLocality': 'Hamm/Sieg', 'addressCountry': 'DE'},
    'areaServed': {'@type': 'Country', 'name': 'Deutschland'},
    'description': 'Webseiten für Handwerksbetriebe, die mehr Anfragen und mehr Sichtbarkeit bei Google bringen.',
}


# ---------- Referenzen: nur Projekte mit erreichbarer Live-Seite (geprüft am 03.11.2026) ----------

REFS = [
    dict(slug='schoenenbach', name='Schönenbach Steinteppich', url='https://www.schoenenbach-steinteppich.de/',
         tag='Handwerk', region='Westerwald / Hessen',
         desc='Spezialist für Steinteppich-Böden auf Terrassen, Balkonen und in Innenräumen.',
         quote='Vorher kamen trotz Werbung kaum brauchbare Anfragen rein. Seitdem erreichen uns regelmäßig genau die richtigen Kunden.'),
    dict(slug='brandschutz', name='Brandschutz Schräder', url='https://brandschutzschraeder.de/',
         tag='Handwerk', region='Nordrhein-Westfalen',
         desc='Familiengeführt seit über 45 Jahren: Wartung und Installation von Brandschutztechnik sowie Brandschutzhelfer-Ausbildungen.',
         quote='Bereits eine Woche nach dem Launch unserer Webseite kamen die ersten Anfragen rein, komplett ohne bezahlte Werbung.'),
    dict(slug='asmontagebetrieb', name='AS Montagebetrieb', url='https://www.asmontagebetrieb.de/',
         tag='Handwerk', region='Stolzenau',
         desc='Fenster, Haustüren, Rollläden und Terrassendächer: persönlich beraten und sauber montiert.', quote=None),
    dict(slug='cncopti', name='CNC Opti', url='https://www.cncopti.de/',
         tag='Industrie', region='Allgäu / Bayern',
         desc='Zertifizierte Schulungen für Siemens- und Heidenhain-Steuerungen sowie Messmittel.', quote=None),
    dict(slug='planttech', name='Planttech GmbH', url='https://planttech.ch/',
         tag='Industrie', region='Sarnen, Schweiz',
         desc='Fördertechnik, Staubbindung und mechanische Anlageninstandhaltung mit Notfalleinsätzen in der Schweiz, Deutschland und Österreich.', quote=None),
    dict(slug='febrix', name='Febrix-Projekt', url='https://febrix-projekt.de/',
         tag='Industrie', region='Deutschland',
         desc='Ingenieurbüro für CAD-Konstruktion, 3D-Scanning und technische Planung.',
         quote='Die Webseite sieht nicht nur gut aus, sondern bringt mir auch neue Kunden.'),
    dict(slug='kingofcopper', name='King of Copper', url='https://kingofcopper.de/',
         tag='Beratung', region='Deutschland',
         desc='Persönlicher Online-Auftritt für den technischen Verkaufsberater rund um Kupfer-Produkte.', quote=None),
    dict(slug='versichert-wissen', name='Versichert-Wissen', url='https://versichert-wissen.de/',
         tag='Beratung', region='',
         desc='Verständliche Versicherungs- und Finanzberatung in Reise, Mobilität, Gesundheit und Vorsorge.', quote=None),
]
REF_BY = {r['slug']: r for r in REFS}


def ref_link(slug, text=None):
    r = REF_BY[slug]
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (r['url'], text or r['name'])


def ref_card(r, i, show_quote=True):
    media = ('<div class="ref-img"><img src="assets/img/ref/%s.jpg" alt="Startseite von %s" loading="lazy" '
             'width="960" height="600"></div>' % (r['slug'], H.escape(r['name'])))
    q = ''
    if show_quote and r.get('quote'):
        q = '<div class="quote"><p>„%s“</p><small>Kundenstimme</small></div>' % r['quote']
    region = '<p class="region">%s</p>' % r['region'] if r.get('region') else ''
    return ('<article class="card ref reveal"%s>%s<span class="tag">%s</span><h3>%s</h3>%s<p class="desc">%s</p>%s'
            '<a class="more" href="%s" target="_blank" rel="noopener">Webseite ansehen →</a></article>'
            % (delay(i, 0.06), media, r['tag'], r['name'], region, r['desc'], q, r['url']))


# ---------- Seitenbausteine ----------

def layout(p):
    url = BASE + '/' + ('' if p['file'] == 'index.html' else p['file'])
    ld = [ORG] + p.get('ld', [])
    if p.get('crumbs'):
        items = [{'@type': 'ListItem', 'position': 1, 'name': 'Start', 'item': BASE + '/'}]
        for i, (name, f) in enumerate(p['crumbs'], start=2):
            items.append({'@type': 'ListItem', 'position': i, 'name': name, 'item': BASE + '/' + f})
        ld.append({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items})
    ldhtml = ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>'
                     for x in ld)
    title = H.escape(p['title'], quote=True)
    desc = H.escape(p['desc'], quote=True)
    doc = (
        '<!doctype html>\n<html lang="de">\n<head>\n'
        '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>' + title + '</title>\n'
        '<meta name="description" content="' + desc + '">\n'
        '<link rel="canonical" href="' + url + '">\n'
        '<meta name="robots" content="index, follow">\n'
        '<meta name="theme-color" content="#C94F1A">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:locale" content="de_DE">\n'
        '<meta property="og:site_name" content="SG-Impact">\n'
        '<meta property="og:title" content="' + title + '">\n'
        '<meta property="og:description" content="' + desc + '">\n'
        '<meta property="og:url" content="' + url + '">\n'
        '<link rel="icon" href="' + FAVICON + '">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600..800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
        '<link rel="stylesheet" href="assets/style.css">\n'
        + ldhtml + '\n</head>\n<body>\n'
        '<a class="skip" href="#main">Zum Inhalt springen</a>\n'
        + header(p['active']) + '\n<main id="main">\n'
        + fill(p['body']) + '\n</main>\n'
        + fill(footer()) + '\n'
        '<script src="assets/main.js" defer></script>\n</body>\n</html>\n')
    with open(os.path.join(OUT, p['file']), 'w', encoding='utf-8') as fh:
        fh.write(doc)
    return p['file']


def header(active):
    links = ''
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ''
        links += '<a href="%s"%s>%s</a>' % (href, cur, label)
    return ('<header class="site"><div class="container nav">'
            '<a href="index.html" class="logo"><img src="assets/logo.svg" alt="SG-Impact" width="89" height="56"></a>'
            '<nav class="nav-links" aria-label="Hauptmenü">' + links +
            '<a href="kontakt.html" class="btn btn-primary">Erstgespräch sichern</a></nav>'
            '<button class="burger" aria-label="Menü öffnen" aria-expanded="false"><span></span></button>'
            '</div></header>')


def footer():
    return (
        '<footer class="site"><div class="container">'
        '<div class="footer-grid">'
        '<div><div class="footer-logo"><img src="assets/logo.svg" alt="SG-Impact" width="111" height="70"></div>'
        '<p>Webseiten für Handwerksbetriebe, die mehr Anfragen und mehr Sichtbarkeit bei Google bringen.</p></div>'
        '<div><h4>Seiten</h4><ul>'
        '<li><a href="leistungen.html">Leistungen</a></li>'
        '<li><a href="referenzen.html">Referenzen</a></li>'
        '<li><a href="index.html#ueber-mich">Über mich</a></li>'
        '<li><a href="faq.html">FAQ</a></li>'
        '<li><a href="kontakt.html">Kontakt</a></li>'
        '</ul></div>'
        '<div><h4>Kontakt</h4><ul>'
        '<li><a href="tel:{{PHONE_TEL}}">{{PHONE}}</a></li>'
        '<li><a href="mailto:{{MAIL}}">{{MAIL}}</a></li>'
        '<li>{{ADDR}}</li>'
        '</ul></div>'
        '</div>'
        '<div class="footer-bottom"><span>© 2026 SG-Impact, Simeon Giesbrecht</span>'
        '<span><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></span></div>'
        '</div></footer>')


def section(inner, cls='', sid=None):
    idattr = ' id="%s"' % sid if sid else ''
    return '<section class="%s"%s><div class="container">%s</div></section>' % (cls, idattr, inner)


def sec_head(h2, text=''):
    t = '<p>%s</p>' % text if text else ''
    return '<div class="section-head reveal"><h2>%s</h2>%s</div>' % (h2, t)


def delay(i, step=0.08):
    return ' style="--d:%.2fs"' % (i * step)


def card(i, ic, title, text, href=None):
    inner = icon(ic) + '<h3>%s</h3><p>%s</p>' % (title, text)
    if href:
        return '<a class="card reveal" href="%s"%s>%s<span class="more">Mehr erfahren →</span></a>' % (href, delay(i), inner)
    return '<div class="card reveal"%s>%s</div>' % (delay(i), inner)


def hero_page(h1, lead, crumbs=None, actions=''):
    trail = ''
    if crumbs:
        parts = ['<a href="index.html">Start</a>']
        for name, f in crumbs[:-1]:
            parts.append('<a href="%s">%s</a>' % (f, name))
        parts.append(crumbs[-1][0])
        trail = '<nav class="crumbs" aria-label="Breadcrumb">' + ' / '.join(parts) + '</nav>'
    return ('<section class="page-hero"><div class="container">' + trail +
            '<h1>%s</h1><p class="lead">%s</p>%s</div></section>' % (
                h1, lead, '<div class="hero-actions">%s</div>' % actions if actions else ''))


def cta(h2, text):
    return section(
        '<div class="cta reveal"><div><h2>%s</h2><p>%s</p></div>'
        '<a href="kontakt.html" class="btn btn-white">Kostenloses Erstgespräch sichern</a></div>' % (h2, text),
        'cta-wrap')


def steps(items):
    out = '<div class="steps">'
    for i, (t, txt) in enumerate(items, start=1):
        out += ('<div class="step reveal"%s><div class="num">%d</div><h3>%s</h3><p>%s</p></div>'
                % (delay(i - 1), i, t, txt))
    return out + '</div>'


def checks(items):
    return '<ul class="checks">' + ''.join('<li>%s</li>' % x for x in items) + '</ul>'


def radar(label='Dein Betrieb'):
    pins = [(118, 150, 0.3), (276, 118, 0.5), (304, 252, 0.7), (196, 306, 0.9), (104, 270, 1.1),
            (262, 320, 1.3), (330, 180, 0.6), (72, 196, 0.8)]
    dots = ''.join('<circle class="pin" cx="%d" cy="%d" r="7" style="--d:%ss"/>' % (x, y, d) for x, y, d in pins)
    return ('<svg class="radar" viewBox="0 0 400 400" role="img" aria-label="Grafik: Ein Betrieb ist im Umkreis '
            'seiner Region bei Google gut zu finden">'
            '<defs><radialGradient id="rg" cx="50%" cy="50%" r="50%">'
            '<stop offset="0" stop-color="#C94F1A" stop-opacity=".18"/>'
            '<stop offset="1" stop-color="#C94F1A" stop-opacity="0"/></radialGradient></defs>'
            '<circle cx="200" cy="200" r="195" fill="url(#rg)"/>'
            '<circle class="ring" cx="200" cy="200" r="60"/>'
            '<circle class="ring" cx="200" cy="200" r="120"/>'
            '<circle class="ring" cx="200" cy="200" r="180"/>'
            '<circle class="ping" cx="200" cy="200" r="12"/>'
            '<circle class="ping ping-2" cx="200" cy="200" r="12"/>'
            + dots +
            '<circle cx="200" cy="200" r="13" fill="#C94F1A" stroke="#fff" stroke-width="4"/>'
            '<text x="200" y="246" text-anchor="middle" class="lbl">%s</text></svg>' % label)


# ---------- Startseite ----------

def page_index():
    hero = (
        '<section class="hero"><div class="container hero-grid">'
        '<div class="hero-copy">'
        '<h1>Mehr Anfragen. <span class="hl">Mehr Sicht bei Google.</span></h1>'
        '<p class="lead">SG-Impact baut Webseiten für Handwerksbetriebe, die in deiner Region gefunden werden. '
        'Seiten, die Besucher überzeugen und sie zum Anruf oder zur Anfrage bringen.</p>'
        '<div class="hero-actions"><a href="kontakt.html" class="btn btn-primary">Kostenloses Erstgespräch</a>'
        '<a href="referenzen.html" class="btn btn-ghost">Projekte ansehen</a></div>'
        '<ul class="trust"><li>Fester Preis und klarer Plan</li><li>Regional bei Google sichtbar</li>'
        '<li>Ein fester Ansprechpartner</li></ul>'
        '</div>'
        '<div class="hero-visual">'
        '<div class="gs" role="img" aria-label="Animation: Eine Suche nach Dachdecker in der Nähe. Dein Betrieb rückt auf Platz 1 und bekommt eine neue Anfrage">'
        '<div class="gs-search"><svg class="gs-lupe" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>'
        '<span class="gs-q">Dachdecker in der Nähe</span></div>'
        '<div class="gs-map" aria-hidden="true"><svg viewBox="0 0 400 128" preserveAspectRatio="xMidYMid slice">'
        '<rect width="400" height="128" fill="#F3EEE8"/>'
        '<rect x="140" y="62" width="52" height="30" rx="5" fill="#E8E0D6"/>'
        '<rect x="300" y="12" width="64" height="26" rx="5" fill="#E8E0D6"/>'
        '<rect x="20" y="14" width="56" height="30" rx="5" fill="#E8E0D6"/>'
        '<path d="M0 46 C120 60 240 24 400 52" stroke="#fff" stroke-width="10" fill="none"/>'
        '<path d="M70 0 L120 128" stroke="#fff" stroke-width="8" fill="none"/>'
        '<path d="M258 0 L212 128" stroke="#fff" stroke-width="7" fill="none"/>'
        '<path d="M0 102 L400 92" stroke="#fff" stroke-width="6" fill="none"/>'
        '<circle class="gs-pin" cx="48" cy="92" r="5"/><circle class="gs-pin" cx="318" cy="98" r="5"/>'
        '<circle class="gs-pin" cx="326" cy="54" r="5"/><circle class="gs-pin" cx="92" cy="26" r="5"/>'
        '<g class="gs-me"><circle class="gs-ring" cx="200" cy="66" r="14"/>'
        '<circle cx="200" cy="66" r="9" fill="#C94F1A" stroke="#fff" stroke-width="3"/></g>'
        '</svg></div>'
        '<ol class="gs-list" aria-hidden="true">'
        '<li class="gs-item s"><i class="gs-bar w1"></i><i class="gs-bar w2"></i></li>'
        '<li class="gs-item me"><div class="gs-name">Dein Betrieb <span class="gs-badge">Beispiel</span></div>'
        '<div class="gs-row"><span class="gs-stars">★★★★★</span>'
        '<span class="gs-btns"><span>Webseite</span><span>Route</span></span></div></li>'
        '<li class="gs-item"><i class="gs-bar w1"></i><i class="gs-bar w2"></i></li>'
        '</ol>'
        '<div class="gs-note" aria-hidden="true"><span class="gs-ico">✓</span>'
        '<div><b>Neue Anfrage</b><small>über deine Webseite</small></div></div>'
        '</div><p class="gs-caption">Vereinfachte Darstellung</p>'
        '</div></section>')

    trust = ('<div class="trust-strip"><div class="container">'
             '<p>Vertrauen von Unternehmen aus Handwerk, Industrie und Beratung</p>'
             '<div class="chips">' + ''.join(
                 '<a class="chip" href="%s" target="_blank" rel="noopener">%s</a>' % (REF_BY[s]['url'], REF_BY[s]['name'])
                 for s in ['schoenenbach', 'brandschutz', 'asmontagebetrieb',
                           'cncopti', 'planttech', 'febrix', 'kingofcopper', 'versichert-wissen']) +
             '</div></div></div>')

    problems = [
        ('Schön, aber wirkungslos', 'Die Seite sieht gut aus, aber niemand findet sie über Google und niemand füllt das Kontaktformular aus.'),
        ('Kein regionaler Auftritt', 'Kunden in deiner Umgebung kennen den Betrieb nicht, obwohl die Konkurrenz online präsenter ist.'),
        ('Alles läuft manuell', 'Jede Anfrage und jedes Angebot wird von Hand erstellt. Diese Zeit fehlt im Tagesgeschäft.'),
    ]
    prob = ''.join('<div class="card reveal"%s><div class="cross" aria-hidden="true">✕</div><h3>%s</h3><p>%s</p></div>'
                   % (delay(i), t, x) for i, (t, x) in enumerate(problems))

    radar_sec = section(
        '<div class="two"><div class="reveal">'
        '<h2>In deiner Region gefunden werden, wenn Kunden suchen</h2>'
        '<p class="lead-s">Bei Anfragen wie „Dachdecker in der Nähe“ entscheidet Google, wer ganz oben steht. '
        'Ich baue deine Seite so, dass sie für deinen Ort und deine Leistungen sichtbar wird.</p>'
        + checks(['Leistungsseiten mit Ort und den Begriffen, nach denen Kunden suchen',
                  'Google Unternehmensprofil, das zu deiner Webseite passt',
                  'Schnelle Technik, die auf dem Handy genauso gut funktioniert']) +
        '</div><div class="radar-wrap reveal" style="--d:.15s">' + radar() + '</div></div>', 'radar-sec')

    services = [
        ('monitor', 'Webseite für Handwerker', 'Individuelles Design, mobil optimiert und auf Anfragen ausgerichtet.', 'webseite-handwerker.html'),
        ('bot', 'Angebots-Bot', 'Anfragen werden auf der Webseite vorqualifiziert und Angebote vorbereitet.', 'automatisierung-angebots-bot.html'),
        ('search', 'Regionale Sichtbarkeit', 'Technik und Inhalte, damit du bei Google in deiner Umgebung gefunden wirst.', 'regionale-sichtbarkeit-seo.html'),
        ('users', 'Mitarbeitergewinnung', 'Eine Karriereseite, die zeigt, warum sich eine Bewerbung bei dir lohnt.', 'karriereseite-mitarbeitergewinnung.html'),
    ]
    svc = ''.join(card(i, ic, t, x, h) for i, (ic, t, x, h) in enumerate(services))

    showcase = (
        '<section class="showcase" aria-label="Vom Klick bis zur Anfrage"><div class="showcase-wrap">'
        '<div class="showcase-sticky"><div class="container sc-grid"><div>'
        '<h2>Vom Klick bis zur Anfrage</h2>'
        '<p>Eine gute Webseite arbeitet in vier Schritten für dich. Scrolle weiter und sieh, wie.</p>'
        '<div class="sc-steps">'
        '<div class="sc-step active"><h3>Gefunden werden</h3><p>Deine Seite erscheint bei Google, wenn Kunden in deiner Region nach deiner Leistung suchen.</p></div>'
        '<div class="sc-step"><h3>Vertrauen gewinnen</h3><p>Klares Design, echte Leistungen und ein Ansprechpartner, der sofort sichtbar ist.</p></div>'
        '<div class="sc-step"><h3>Anfragen abfangen</h3><p>Formular und Angebots-Bot beantworten den Erstkontakt, auch wenn du auf der Baustelle stehst.</p></div>'
        '<div class="sc-step"><h3>Bewerbungen gewinnen</h3><p>Eine Karriereseite zeigt Fachkräften, warum sie sich bei dir bewerben sollten.</p></div>'
        '</div></div>'
        '<div><div class="sc-panel">'
        '<div class="slide active"><div class="big">01</div><h3>Gefunden werden</h3><p>Sichtbar bei Google, dort wo deine Kunden suchen.</p></div>'
        '<div class="slide"><div class="big">02</div><h3>Vertrauen gewinnen</h3><p>Ein Auftritt, der Sorgfalt zeigt, auf dem Handy wie am PC.</p></div>'
        '<div class="slide"><div class="big">03</div><h3>Anfragen abfangen</h3><p>Der Erstkontakt läuft strukturiert, auch außerhalb der Bürozeiten.</p></div>'
        '<div class="slide"><div class="big">04</div><h3>Bewerbungen gewinnen</h3><p>Passende Bewerber finden die Stellen und melden sich.</p></div>'
        '</div><div class="sc-progress"><span></span></div></div>'
        '</div></div></div></section>')

    refs = ''.join(ref_card(r, i) for i, r in enumerate(REFS[:3]))

    body = (
        hero + trust +
        section(sec_head('Kommt dir das bekannt vor?',
                         'Die meisten Webseiten kosten Geld, bringen aber keine Anfragen. Drei Muster sehe ich immer wieder.') +
                '<div class="grid-3">' + prob + '</div>', '') +
        radar_sec +
        section(sec_head('Was ich für dich baue', 'Kein Baukasten von der Stange. Jede Lösung richtet sich auf dein Ziel aus.') +
                '<div class="grid-4">' + svc + '</div>', 'tint') +
        showcase +
        section(sec_head('So läuft die Zusammenarbeit', 'Ein klarer Weg vom ersten Gespräch bis zur fertigen Webseite.') +
                steps([
                    ('Erstgespräch', 'Du schilderst dein Ziel: mehr Anfragen, mehr Bewerbungen oder mehr Sichtbarkeit. Das ist kostenlos.'),
                    ('Potenzialanalyse', 'Ich schaue mir deine Situation und deine Region an und sage dir ehrlich, was sich lohnt.'),
                    ('Plan mit festem Preis', 'Konzept, Umfang und Preis kommen schriftlich, bevor etwas startet.'),
                    ('Umsetzung und Start', 'Design, Texte und Anfrage-Wege entstehen. Nach dem Launch betreue ich dich weiter.'),
                ]), '') +
        section(sec_head('Projekte aus der Praxis', 'Webseiten, die live sind und für Unternehmen arbeiten.') +
                '<div class="grid-3">' + refs + '</div>' +
                '<p class="more-link reveal"><a class="btn btn-ghost" href="referenzen.html">Alle Projekte ansehen</a></p>', '') +
        about_section() +
        cta('Mehr Anfragen und mehr Sicht bei Google?',
            'Im kostenlosen Erstgespräch schauen wir auf deine Situation und klären, was in deiner Region möglich ist.')
    )
    ld = [{'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'SG-Impact', 'url': BASE + '/', 'inLanguage': 'de'}]
    return dict(file='index.html', active='',
                title='Webseiten für Handwerker: mehr Anfragen | SG-Impact',
                desc='Webseiten für Handwerksbetriebe, die mehr Anfragen und mehr Sichtbarkeit bei Google bringen. Kostenloses Erstgespräch.',
                body=body, ld=ld)


def page_leistungen():
    items = [
        ('monitor', 'Webseite für Handwerksbetriebe', 'Individuelles Design, mobil optimiert, mit Leistungsseiten, Referenzen und klarem Weg zur Anfrage.', 'webseite-handwerker.html'),
        ('bot', 'Automatisierung und Angebots-Bot', 'Erstkontakt und Angebotsvorbereitung laufen über die Webseite. Preise pflegst du selbst in einer Tabelle.', 'automatisierung-angebots-bot.html'),
        ('search', 'Regionale Sichtbarkeit und SEO', 'Technik, Inhalte und Google Unternehmensprofil, damit du in deiner Region mehr gefunden wirst.', 'regionale-sichtbarkeit-seo.html'),
        ('users', 'Karriereseite und Mitarbeitergewinnung', 'Eine Karriereseite, die zeigt, wer du als Arbeitgeber bist, und Bewerbungen, die passen.', 'karriereseite-mitarbeitergewinnung.html'),
    ]
    cards = ''.join(card(i, ic, t, x, h) for i, (ic, t, x, h) in enumerate(items))
    body = (
        hero_page('Leistungen für mehr Anfragen und mehr Sicht bei Google',
                  'Vier Bausteine, die einzeln oder zusammen funktionieren. Welcher passt, klären wir im kostenlosen Erstgespräch.',
                  [('Leistungen', 'leistungen.html')]) +
        section('<div class="grid-2">' + cards + '</div>', '') +
        section(sec_head('Laufende Betreuung', '') +
                '<div class="two reveal"><div><p>Eine Webseite ist nach dem Launch nicht fertig. Ich begleite dich bei Pflege, Updates und Weiterentwicklung, '
                'damit deine Investition weiter Ergebnisse bringt.</p>'
                '<p>Du hast immer einen festen Ansprechpartner statt einer anonymen Hotline.</p></div>'
                '<div class="card">' + icon('clock') + '<h3>Ein fester Ansprechpartner</h3>'
                '<p>Du erreichst mich direkt. Keine Warteschleife, keine wechselnden Zuständigkeiten.</p></div></div>', 'tint') +
        cta('Welcher Baustein bringt dich weiter?', 'Schreib mir kurz, was du erreichen willst. Ich melde mich persönlich zurück.')
    )
    return dict(file='leistungen.html', active='leistungen.html',
                title='Leistungen: Webseiten, Anfragen, Google-Sichtbarkeit | SG-Impact',
                desc='Leistungen von SG-Impact: Webseiten für Handwerksbetriebe, Angebots-Bot, regionale Sichtbarkeit bei Google und Karriereseiten.',
                body=body, crumbs=[('Leistungen', 'leistungen.html')])


def page_webseite():
    body = (
        hero_page('Webseite für Handwerksbetriebe, die Anfragen bringt',
                  'Eine moderne, mobile Webseite mit klarer Struktur und festem Preis. Sie soll dafür sorgen, dass Kunden und Bewerber dich anrufen oder anfragen.',
                  [('Leistungen', 'leistungen.html'), ('Webseite für Handwerksbetriebe', 'webseite-handwerker.html')],
                  '<a href="kontakt.html" class="btn btn-primary">Kostenloses Erstgespräch</a>') +
        section(
            '<div class="two"><div class="reveal">' + sec_head('Was in deiner Webseite steckt', '') +
            checks([
                'Individuelles Design statt Baukasten-Vorlage, passend zu deiner Marke',
                'Mobil genauso gut wie am PC, mit schneller Ladezeit',
                'Leistungsseiten, die deine Arbeit konkret zeigen',
                'Telefonnummer und Anfrageformular auf jeder Seite',
                'Vertrauen durch Referenzen, Bewertungen und sichtbaren Ansprechpartner',
                'Impressum und Datenschutzerklärung eingerichtet',
            ]) + '</div>'
            '<div class="browser reveal" style="--d:.1s"><div class="browser-bar"><i></i><i></i><i></i><span>Beispiel aus der Praxis</span></div>'
            '<img src="assets/img/ref/schoenenbach.jpg" alt="Startseite von Schönenbach Steinteppich als Beispiel" width="960" height="600" loading="lazy"></div></div>'
        ) +
        section(sec_head('Für wen das passt', 'Am häufigsten arbeite ich mit Handwerks- und Bauunternehmen. Auch andere Branchen sind willkommen, wenn Anfragen dein Ziel sind.') +
                '<div class="grid-4">' +
                card(0, 'briefcase', 'Handwerk und Bau', 'Etwa Dachdecker, Maler, Elektriker oder Fensterbauer, die in ihrer Region Kunden gewinnen wollen.') +
                card(1, 'chart', 'Industrie und B2B', 'Maschinenbau, Technik und Zulieferer, die online als Partner wahrgenommen werden wollen.') +
                card(2, 'pin', 'Dienstleistung und Gewerbe', 'Betriebe, die Beratung oder Service anbieten und Anfragen über die Webseite steuern wollen.') +
                card(3, 'star', 'Kreativ und Medien', 'Selbstständige und kleine Teams mit eigener Handschrift und klarem Angebot.') +
                '</div>', 'tint') +
        section(sec_head('So läuft das Projekt ab') +
                steps([
                    ('Potenzialanalyse', 'Kostenlos. Wir klären dein Ziel und was in deiner Situation realistisch ist.'),
                    ('Konzept und festen Preis', 'Struktur, Texte und Umfang, schriftlich und mit festem Preis.'),
                    ('Design und Umsetzung', 'Ich baue die Seite, du gibst Feedback an zwei festen Terminen.'),
                    ('Launch und Betreuung', 'Die Seite geht live, und ich bleibe für Pflege und Weiterentwicklung da.'),
                ]), '') +
        cta('Lass uns deine Webseite konkret machen', 'Im kostenlosen Erstgespräch hörst du, was für dich sinnvoll ist, bevor du dich entscheidest.')
    )
    ld = [{'@context': 'https://schema.org', '@type': 'Service', 'name': 'Webseite für Handwerksbetriebe',
           'serviceType': 'Webdesign', 'provider': {'@id': BASE + '/#business'}, 'areaServed': 'DE',
           'description': 'Individuelle, mobile Webseiten für Handwerks- und Gewerbebetriebe mit mehr Anfragen.'}]
    return dict(file='webseite-handwerker.html', active='leistungen.html',
                title='Webseite für Handwerksbetriebe mit mehr Anfragen | SG-Impact',
                desc='Webseiten für Handwerksbetriebe: individuelles Design, mobil optimiert, fester Preis und ein fester Ansprechpartner. Kostenloses Erstgespräch.',
                body=body, ld=ld,
                crumbs=[('Leistungen', 'leistungen.html'), ('Webseite für Handwerksbetriebe', 'webseite-handwerker.html')])


def page_bot():
    body = (
        hero_page('Automatisierung und Angebots-Bot direkt auf deiner Webseite',
                  'Interessenten geben auf deiner Seite ein paar Angaben ein. Daraus entsteht eine vorbereitete Anfrage oder ein Angebotsentwurf, ohne dass du alles von Hand abtippen musst.',
                  [('Leistungen', 'leistungen.html'), ('Automatisierung und Angebots-Bot', 'automatisierung-angebots-bot.html')],
                  '<a href="kontakt.html" class="btn btn-primary">Automatisierung besprechen</a>') +
        section(sec_head('So funktioniert der Ablauf', 'Die Logik passt sich deinem Betrieb an. Hier ein typischer Ablauf.') +
                steps([
                    ('Angaben abfragen', 'Der Besucher wählt Leistung, Umfang oder Maße und einen Wunschtermin.'),
                    ('Berechnen', 'Die Angaben werden nach deinen Preisen und Regeln verarbeitet.'),
                    ('Angebot vorbereiten', 'Ein Angebot als PDF oder ein Rückruf-Vorschlag entsteht automatisch.'),
                    ('Anfrage zustellen', 'Die Anfrage landet bei dir per E-Mail, in einer Tabelle oder im Kundensystem.'),
                ]), 'tint') +
        section(sec_head('Was du davon hast') +
                '<div class="grid-3">' +
                card(0, 'clock', 'Weniger Handarbeit', 'Anfragen und Angebotsentwürfe entstehen, während du auf der Baustelle bist.') +
                card(1, 'bolt', 'Schnellerer Erstkontakt', 'Der Interessent bekommt eine Rückmeldung, bevor er zur Konkurrenz geht.') +
                card(2, 'file', 'Bessere Anfragen', 'Wer schon Angaben macht, hat ernsthaftes Interesse. Das spart Rückfragen.') +
                '</div>', '') +
        section('<div class="two reveal"><div>' + sec_head('Deine Preise bleiben in deiner Hand', '') +
                '<p>Die Preise hinterlegst du in einer Tabelle, die du selbst änderst. Du musst dafür nichts neu programmieren lassen, wenn sich etwas am Markt oder bei deinem Material ändert.</p>'
                '<p>Der Umfang richtet sich nach deinem Gewerk und den Abläufen in deinem Betrieb. Das klären wir im Erstgespräch.</p></div>'
                '<div class="card">' + icon('bot') + '<h3>Was du zum Start brauchst</h3>'
                '<p>Deine Leistungen, deine Preislogik oder Richtwerte und die Angabe, wohin Anfragen fließen sollen, zum Beispiel E-Mail oder Tabelle.</p></div></div>', 'tint') +
        cta('Welche Abläufe kannst du abgeben?', 'Im Erstgespräch schauen wir, welcher Schritt in deinem Betrieb die meiste Zeit frisst.')
    )
    ld = [{'@context': 'https://schema.org', '@type': 'Service', 'name': 'Automatisierung und Angebots-Bot',
           'serviceType': 'Webentwicklung und Automatisierung', 'provider': {'@id': BASE + '/#business'},
           'areaServed': 'DE', 'description': 'Angebots-Bot und Anfrage-Automatisierung direkt auf der Webseite.'}]
    return dict(file='automatisierung-angebots-bot.html', active='leistungen.html',
                title='Angebots-Bot und Automatisierung für Handwerker | SG-Impact',
                desc='Angebots-Bot und Anfrage-Automatisierung auf der Webseite: Angaben werden erfasst, Angebote vorbereitet und Anfragen direkt zugestellt.',
                body=body, ld=ld,
                crumbs=[('Leistungen', 'leistungen.html'), ('Automatisierung und Angebots-Bot', 'automatisierung-angebots-bot.html')])


def page_sichtbarkeit():
    checklist = ['Google Unternehmensprofil ist vollständig und mit Fotos gepflegt',
                 'Jede Leistung hat eine eigene Seite mit Ort und konkreten Suchbegriffen',
                 'Telefonnummer und Anfrageformular sind auf dem Handy direkt erreichbar',
                 'Die Seite lädt zügig, auch mit schwacher Verbindung',
                 'Bewertungen und Referenzen sind sichtbar und aktuell',
                 'Impressum, Datenschutz und Firmendaten sind vollständig']
    chk = ''.join('<label class="check"><input type="checkbox" class="check-input"><span>%s</span></label>' % c
                  for c in checklist)
    body = (
        hero_page('Mehr Sicht bei Google: in deiner Region gefunden werden',
                  'Eine Webseite nützt wenig, wenn sie in Google niemand findet. Ich baue Technik und Inhalte so auf, dass deine Region und deine Leistungen zusammenpassen.',
                  [('Leistungen', 'leistungen.html'), ('Regionale Sichtbarkeit und SEO', 'regionale-sichtbarkeit-seo.html')],
                  '<a href="kontakt.html" class="btn btn-primary">Sichtbarkeit prüfen lassen</a>') +
        section('<div class="two"><div class="reveal"><h2>Dein Betrieb im Umkreis</h2>'
                '<p class="lead-s">Google zeigt Betriebe, die zur Suche und zum Ort passen. Diese Grafik zeigt die Idee: je besser Seite und Profil zusammenpassen, desto häufiger wirst du gefunden.</p>'
                '</div><div class="radar-wrap reveal" style="--d:.1s">' + radar() + '</div></div>', '') +
        section(sec_head('Was ich dafür tue') +
                '<div class="grid-2">' +
                card(0, 'search', 'Leistungsseiten mit Ort', 'Jede Leistung bekommt eine eigene Seite mit Region und den Begriffen, nach denen Kunden tatsächlich suchen.') +
                card(1, 'pin', 'Google Unternehmensprofil', 'Einrichtung und Verknüpfung mit deiner Webseite, damit du auf der Karte und in der lokalen Suche erscheinst.') +
                card(2, 'monitor', 'Technik und Geschwindigkeit', 'Saubere Struktur, mobile Optimierung und schnelle Ladezeit, denn Google bewertet das mit.') +
                card(3, 'shield', 'Vertrauenssignale', 'Referenzen, Bewertungen, Fotos und eine klare Firmenangabe. Sie überzeugen Suchende und Google.') +
                '</div>', 'tint') +
        section('<div class="two"><div class="reveal">' + sec_head('Wie gut steht deine Seite da?', 'Hake ab, was bei dir schon stimmt. Die Auswertung zeigt dir, wo der größte Hebel liegt.') +
                '</div><div class="calc reveal" data-check><div class="check-list">' + chk + '</div>'
                '<p class="note" id="r-check" aria-live="polite">Hake an, was zutrifft.</p></div></div>', '') +
        section('<div class="reveal" style="max-width:820px"><h2>Ehrlich zu Erwartungen</h2>'
                '<p>Kein seriöser Anbieter kann dir Platz 1 bei Google garantieren. Es hängt von Konkurrenz, Region und Suchbegriffen ab. '
                'Ich sage dir im Erstgespräch offen, was realistisch ist und was du dafür selbst leisten musst.</p></div>', 'tint') +
        cta('Wo steht deine Region im Vergleich?', 'Schreib mir deine Branche und deinen Ort. Ich schaue mir an, wie du bei Google heute gefunden wirst.')
    )
    ld = [{'@context': 'https://schema.org', '@type': 'Service', 'name': 'Regionale Sichtbarkeit und SEO',
           'serviceType': 'Suchmaschinenoptimierung', 'provider': {'@id': BASE + '/#business'},
           'areaServed': 'DE', 'description': 'Lokale Suchmaschinenoptimierung für Handwerks- und Gewerbebetriebe.'}]
    return dict(file='regionale-sichtbarkeit-seo.html', active='leistungen.html',
                title='Mehr Sicht bei Google für Handwerker | SG-Impact',
                desc='Lokale SEO für Handwerksbetriebe: Leistungsseiten mit Region, Google Unternehmensprofil, schnelle Technik und Vertrauenssignale.',
                body=body, ld=ld,
                crumbs=[('Leistungen', 'leistungen.html'), ('Regionale Sichtbarkeit und SEO', 'regionale-sichtbarkeit-seo.html')])


def page_karriere():
    body = (
        hero_page('Karriereseite und Mitarbeitergewinnung für Handwerksbetriebe',
                  'Fachkräfte schauen sich einen Arbeitgeber online an, bevor sie sich melden. Eine Karriereseite zeigt, wer du bist und warum sich eine Bewerbung lohnt.',
                  [('Leistungen', 'leistungen.html'), ('Karriereseite und Mitarbeitergewinnung', 'karriereseite-mitarbeitergewinnung.html')],
                  '<a href="kontakt.html" class="btn btn-primary">Karriereseite besprechen</a>') +
        section(sec_head('Was eine gute Karriereseite leistet', 'Bewerbungen, die zu deinem Betrieb passen, statt Anfragen von irgendwem.') +
                '<div class="grid-3">' +
                card(0, 'users', 'Team zeigen', 'Echte Fotos, Aufgaben und Ansprechpartner. Bewerber wollen wissen, mit wem sie arbeiten.') +
                card(1, 'briefcase', 'Stellen klar beschreiben', 'Was der Job ist, was du bietest und welche Voraussetzungen wirklich gebraucht werden.') +
                card(2, 'file', 'Kurz bewerben', 'Ein Bewerbungsformular mit den Angaben, die du wirklich brauchst. Das senkt die Hürde.') +
                '</div>', 'tint') +
        section('<div class="two"><div class="reveal">' + sec_head('Mehr Reichweite für Stellen', '') +
                checks(['Stellenseiten, die bei Google in deiner Region gefunden werden',
                        'Eine Kampagne für offene Stellen, wenn du sie gezielt besetzen willst',
                        'Klare Antwortzeiten, damit Bewerber nicht ins Leere laufen']) + '</div>'
                '<div class="card reveal" style="--d:.1s">' + icon('users') + '<h3>Kunden- und Mitarbeitergewinnung zusammen</h3>'
                '<p>Oft lohnt sich beides über dieselbe Webseite. Ein seriöser Auftritt überzeugt Kunden und Bewerber gleichermaßen.</p></div></div>', '') +
        cta('Wie gewinnst du die Leute, die du suchst?', 'Im Erstgespräch schauen wir, welche Stellen du besetzen willst und wie deine Seite das unterstützt.')
    )
    ld = [{'@context': 'https://schema.org', '@type': 'Service', 'name': 'Karriereseite und Mitarbeitergewinnung',
           'serviceType': 'Employer Branding', 'provider': {'@id': BASE + '/#business'}, 'areaServed': 'DE',
           'description': 'Karriereseiten und Bewerberformulare für Handwerks- und Gewerbebetriebe.'}]
    return dict(file='karriereseite-mitarbeitergewinnung.html', active='leistungen.html',
                title='Karriereseite und Mitarbeitergewinnung | SG-Impact',
                desc='Karriereseiten für Handwerksbetriebe: Teamfotos, klare Stellenbeschreibungen und einfache Bewerbungsformulare. Mehr passende Bewerbungen.',
                body=body, ld=ld,
                crumbs=[('Leistungen', 'leistungen.html'), ('Karriereseite und Mitarbeitergewinnung', 'karriereseite-mitarbeitergewinnung.html')])


def page_referenzen():
    stimmen = ''.join(ref_card(r, i) for i, r in enumerate(REFS))
    fälle = [
        ('Betrieb mit Online-Werbung ohne passende Anfragen',
         'Der Betrieb gab regelmäßig Geld für Werbung aus, bekam aber kaum passende Anfragen.',
         'Die Webseite wurde auf qualifizierte Kundenanfragen ausgerichtet, mit klarer Leistungsdarstellung und Kontaktweg.',
         'Deutlich bessere Anfragen, weniger verlorene Zeit und mehr Aufträge über den Online-Kontakt.'),
        ('Betrieb, der online kaum gefunden wurde',
         'Der Betrieb war bei Google kaum sichtbar, es kamen keine Anfragen über die Webseite.',
         'Neuer Auftritt mit klarer Nutzerführung und Fokus auf die Kontaktaufnahme.',
         'Erste Anfragen schon nach einer Woche, komplett ohne bezahlte Werbung.'),
        ('Neugründung ohne Webseite',
         'Der frisch gegründete Betrieb hatte noch keinen Auftritt und wirkte für erste Kunden nicht seriös.',
         'Eine moderne Webseite, die Vertrauen aufbaut und das Angebot klar zeigt.',
         'Professioneller Auftritt ab dem ersten Tag und ein starker erster Eindruck.'),
    ]
    fall_html = ''.join(
        '<div class="card reveal"%s><h3>%s</h3><p><strong>Ausgangslage:</strong> %s</p>'
        '<p><strong>Lösung:</strong> %s</p><p><strong>Ergebnis:</strong> %s</p></div>' % (delay(i), t, a, l, e)
        for i, (t, a, l, e) in enumerate(fälle))
    body = (
        hero_page('Projekte, die für Unternehmen Anfragen bringen',
                  'Handwerk, Gesundheit und Industrie. Jede Webseite ist auf das Ziel des Unternehmens abgestimmt.',
                  [('Referenzen', 'referenzen.html')]) +
        section(sec_head('Live-Webseiten', 'Ein Klick führt direkt zur Seite. Die Bilder zeigen den Startbereich der jeweiligen Webseite.') +
                '<div class="grid-3 ref-grid">' + stimmen + '</div>', '') +
        section(sec_head('Ausgangslage und Ergebnis', 'Drei typische Fälle, anonymisiert.') +
                '<div class="grid-3">' + fall_html + '</div>', 'tint') +
        cta('Dein Projekt könnte das nächste sein', 'Schreib mir in einem Satz, was du erreichen willst. Ich sage dir, ob und wie ich helfen kann.')
    )
    return dict(file='referenzen.html', active='referenzen.html',
                title='Referenzen und Kundenstimmen | SG-Impact',
                desc='Referenzen von SG-Impact: Live-Webseiten für Handwerk, Gesundheit und Industrie, mit Kundenstimmen und Ergebnissen aus der Praxis.',
                body=body, crumbs=[('Referenzen', 'referenzen.html')])


def about_section():
    """Über-mich-Abschnitt auf der Startseite (Landingpage, keine Unterseite)."""
    return section(
        '<div class="two"><div class="reveal"><img class="about-photo" src="assets/img/simeon.jpg" '
        'alt="Porträt von Simeon Giesbrecht" width="720" height="752" loading="lazy"></div>'
        '<div class="reveal" style="--d:.1s"><h2>Simeon Giesbrecht: dein Partner für Handwerker-Webseiten</h2>'
        '<p>Ich bin kein Fan davon, dass Unternehmen viel Geld in eine Webseite stecken, nur damit sie gut aussieht. '
        'Eine Webseite soll Anfragen und Bewerbungen bringen. Alles andere ist Nebensache.</p>'
        '<p>Deshalb denke ich bei jedem Projekt zuerst an dein Ziel und erst danach an das Design. Und ich nehme dir mit Automatisierungen '
        'Arbeit ab, zum Beispiel beim Erstkontakt und bei Angeboten.</p>'
        + checks(['Individuelle Lösungen statt Baukasten-Vorlagen',
                  'Fokus auf Ergebnisse: Anfragen, Bewerbungen, Sichtbarkeit',
                  'Automatisierung, die dir echte Arbeit abnimmt',
                  'Ein fester Ansprechpartner, keine anonyme Agentur']) + '</div></div>', 'tint', sid='ueber-mich')


FAQ = [
    ('Was kostet eine Webseite bei SG-Impact?',
     'Du bekommst vor Projektstart einen festen Preis und einen klaren Kostenplan, ohne Überraschungen. Der Umfang richtet sich nach deinem Ziel, von einer schlanken Unternehmensseite bis zur Webseite mit Angebots-Bot. Im kostenlosen Erstgespräch erhältst du ein konkretes Angebot.'),
    ('Was ist die Potenzialanalyse?',
     'Ein kostenloses Gespräch, in dem wir dein Ziel klären: mehr Anfragen, mehr Bewerbungen oder mehr Sichtbarkeit. Du erfährst, was realistisch ist und welche Lösung dafür passt. Die Analyse ist kostenlos und unverbindlich.'),
    ('Wie lange dauert die Umsetzung?',
     'Je nach Umfang meist wenige Wochen von Konzept bis Livegang. Den genauen Zeitrahmen legen wir im Erstgespräch gemeinsam fest.'),
    ('Bringt eine neue Webseite wirklich mehr Anfragen?',
     'Sie ist die Grundlage dafür. Anfragen kommen, wenn die Seite in Google gefunden wird und Besucher schnell sehen, dass du der Richtige bist. Ob und wie stark das steigt, hängt von Region, Konkurrenz und Angebot ab. Das besprechen wir offen im Erstgespräch.'),
    ('Kümmerst du dich auch um die Sichtbarkeit bei Google?',
     'Ja. Jede Webseite wird technisch und inhaltlich so aufgebaut, dass sie in deiner Region bei Google gefunden wird. Das ist fester Bestandteil der Arbeit und kein Zusatzpaket.'),
    ('Was bedeutet Automatisierung auf der Webseite?',
     'Zum Beispiel ein Bot, der Anfragen direkt aufnimmt, oder ein Rechner, der aus den Angaben eines Besuchers einen Angebotsentwurf vorbereitet. Damit hast du weniger manuelle Arbeit.'),
    ('Betreust du die Webseite auch nach dem Launch?',
     'Ja, gerne. Eine Webseite ist für mich ein laufendes Investment und keine einmalige Sache. Ich begleite dich bei Pflege und Weiterentwicklung.'),
    ('Für welche Branchen arbeitest du?',
     'Am häufigsten für Handwerks- und Bauunternehmen. Ich arbeite aber auch mit Industrie, B2B, Dienstleistern und kreativen Betrieben, wenn Anfragen oder Bewerbungen dein Ziel sind.'),
    ('Arbeitest du nur in der Region Hamm/Sieg?',
     'Ich bin in Hamm/Sieg zu Hause und arbeite deutschlandweit. Die Zusammenarbeit läuft meist digital.'),
]


def page_faq():
    items = ''.join('<details class="reveal"%s><summary>%s</summary><p>%s</p></details>' % (
        delay(i, 0.04) if i < 6 else '', q, a) for i, (q, a) in enumerate(FAQ))
    body = (
        hero_page('Häufige Fragen zu Webseiten, Kosten und Anfragen',
                  'Die wichtigsten Antworten vorab. Offene Fragen klären wir gerne im kostenlosen Erstgespräch.',
                  [('FAQ', 'faq.html')]) +
        section('<div class="faq">' + items + '</div>', '') +
        cta('Deine Frage ist nicht dabei?', 'Schreib mir oder ruf kurz an. Ich antworte in der Regel innerhalb von 24 Stunden.')
    )
    ld = [{'@context': 'https://schema.org', '@type': 'FAQPage',
           'mainEntity': [{'@type': 'Question', 'name': q,
                           'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}]
    return dict(file='faq.html', active='faq.html', title='Häufige Fragen zu Kosten und Anfragen | SG-Impact',
                desc='Antworten auf häufige Fragen zu Webseiten für Handwerksbetriebe: Kosten, Potenzialanalyse, Umsetzung, Google-Sichtbarkeit und Betreuung.',
                body=body, ld=ld, crumbs=[('FAQ', 'faq.html')])


def page_kontakt():
    contact = (
        '<div class="contact-list">'
        '<div>' + icon('phone') + '<p><strong>Telefon</strong><a href="tel:{{PHONE_TEL}}">{{PHONE}}</a></p></div>'
        '<div>' + icon('mail') + '<p><strong>E-Mail</strong><a href="mailto:{{MAIL}}">{{MAIL}}</a></p></div>'
        '<div>' + icon('pin') + '<p><strong>Standort</strong>{{ADDR}}<br>Deutschlandweit tätig</p></div>'
        '<div>' + icon('clock') + '<p><strong>Antwortzeit</strong>In der Regel innerhalb von 24 Stunden</p></div>'
        '</div>')
    form = (
        '<form class="form reveal" data-mail="{{MAIL}}" novalidate>'
        '<div class="form-row"><div><label for="name">Name *</label><input id="name" name="name" required autocomplete="name" placeholder="Dein Name"></div>'
        '<div><label for="email">E-Mail *</label><input id="email" name="email" type="email" required autocomplete="email" placeholder="du@firma.de"></div></div>'
        '<div class="form-row"><div><label for="phone">Telefon</label><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="Optional"></div>'
        '<div><label for="betrieb">Betrieb</label><input id="betrieb" name="betrieb" autocomplete="organization" placeholder="Firmenname"></div></div>'
        '<label for="ziel">Dein Ziel</label><select id="ziel" name="ziel">'
        '<option value="">Bitte wählen</option><option>Mehr Anfragen über eine neue Webseite</option><option>Mehr Sicht bei Google</option>'
        '<option>Mitarbeitergewinnung</option><option>Automatisierung und Angebots-Bot</option><option>Sonstiges</option></select>'
        '<label for="message">Nachricht *</label>'
        '<textarea id="message" name="message" required placeholder="Erzähl kurz von deinem Betrieb und deinem Ziel."></textarea>'
        '<label class="check"><input type="checkbox" name="datenschutz" required><span>Ich habe die <a href="datenschutz.html">Datenschutzerklärung</a> gelesen.</span></label>'
        '<button type="submit" class="btn btn-primary btn-block">Nachricht senden</button>'
        '<p class="form-note">Mit dem Absenden öffnet sich dein E-Mail-Programm mit vorausgefüllter Nachricht an {{MAIL}}.</p>'
        '</form>')
    body = (
        hero_page('Kostenloses Erstgespräch vereinbaren',
                  'Erzähl mir in ein paar Sätzen, was du erreichen willst. Ich melde mich persönlich zurück.',
                  [('Kontakt', 'kontakt.html')]) +
        section('<div class="two" style="align-items:start">' + contact + form + '</div>', '')
    )
    return dict(file='kontakt.html', active='kontakt.html', title='Kontakt und Erstgespräch | SG-Impact',
                desc='Kontakt zu SG-Impact: kostenloses Erstgespräch für deine Webseite. Telefon, E-Mail oder Anfrage über das Formular.',
                body=body, crumbs=[('Kontakt', 'kontakt.html')])


def legal_body(path):
    """Übernimmt den Textteil der alten Seite (ohne Kopf und Fuß), damit der Wortlaut gleich bleibt."""
    with open(path, encoding='utf-8') as fh:
        s = fh.read()
    m = re.search(r'<main[^>]*>(.*?)</main>', s, re.S)
    if m:
        inner = m.group(1)
    else:
        a = s.find('</header>')
        b = s.find('<footer')
        inner = s[a + len('</header>'):b] if a != -1 and b != -1 else s
    inner = re.sub(r'<script.*?</script>|<style.*?</style>', '', inner, flags=re.S)
    inner = re.sub(r'<a [^>]*>\s*←[^<]*</a>', '', inner)
    inner = re.sub(r'<header.*?</header>|<nav.*?</nav>', '', inner, flags=re.S)
    inner = re.sub(r'<div class="sticky-bar.*?</div>\s*</div>', '', inner, flags=re.S)
    inner = inner.replace('info@jsdigitalwerk.de', MAIL)
    return inner


def page_legal(file, title, desc, src):
    inner = legal_body(os.path.join(ALT_SRC, src))
    body = (hero_page(title, '', [(title, file)]) +
            '<section class="legal-wrap"><div class="container legal">' + inner + '</div></section>')
    return dict(file=file, active='', title=title + ' | SG-Impact', desc=desc, body=body,
                crumbs=[(title, file)])


PAGES = [
    page_index(),
    page_leistungen(),
    page_webseite(),
    page_bot(),
    page_sichtbarkeit(),
    page_karriere(),
    page_referenzen(),
    page_faq(),
    page_kontakt(),
    page_legal('impressum.html', 'Impressum', 'Impressum von SG-Impact, Simeon Giesbrecht, Hamm/Sieg.', 'impressum.html'),
    page_legal('datenschutz.html', 'Datenschutzerklärung', 'Datenschutzerklärung der Webseite von SG-Impact.', 'datenschutz.html'),
]


def write_sitemap():
    urls = []
    for p in PAGES:
        loc = BASE + '/' + ('' if p['file'] == 'index.html' else p['file'])
        prio = '1.0' if p['file'] == 'index.html' else ('0.9' if p['file'] in ('leistungen.html', 'referenzen.html', 'kontakt.html') else '0.7')
        urls.append('  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>' % (loc, TODAY, prio))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + '\n'.join(urls) + '\n</urlset>\n')
    with open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
        fh.write(xml)
    with open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8') as fh:
        fh.write('User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % BASE)


if __name__ == '__main__':
    for p in PAGES:
        print('geschrieben:', layout(p))
    write_sitemap()
    print('sitemap.xml und robots.txt geschrieben')
