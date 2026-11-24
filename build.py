# בונה את דפי האתר מתוך src/: התבנית המשותפת (תפריט, כותרת תחתונה) + התוכן של כל דף.
# הרצה: python build.py   (הדפים נכתבים לתיקייה הזו: index.html, method.html ...)
import json, re, html, os
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = ''  # כשהאתר יעלה לאוויר: הכתובת המלאה, למשל https://example.github.io/  (משמש לקישור הקנוני ולגוגל)

WA_NUM = '19294359064'
WA = f'https://wa.me/{WA_NUM}?text=' + quote('שלום יועז, יש לי שאלה')
USB_MSG = 'שלום יועז, אני רוצה להזמין את הקורס על דיסק און קי עד הבית.\n\nשם:\nטלפון:\nכתובת למשלוח:\nנוסח:'
WA_USB = f'https://wa.me/{WA_NUM}?text=' + quote(USB_MSG)
MAIL_USB = 'mailto:yoazcam770@gmail.com?subject=' + quote('הזמנת הקורס על דיסק און קי') + '&amp;body=' + quote(USB_MSG)

def svg(p, sw=1.8):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

IC = {
    'home': svg('<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>'),
    'book': svg('<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20"/>'),
    'gift': svg('<rect x="3" y="8" width="18" height="5" rx="1"/><path d="M5 13v8h14v-8M12 8v13"/><path d="M12 8C10 4 6.5 4.5 7 7c.3 1.2 2.5 1 5 1zM12 8c2-4 5.5-3.5 5-1-.3 1.2-2.5 1-5 1z"/>'),
    'scroll': svg('<path d="M7 4h11a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H7"/><path d="M7 4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2 2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"/><path d="M12 9h5M12 13h5"/>'),
    'grid': svg('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>'),
    'question': svg('<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.2 2.4c-.4.2-.7.6-.7 1.1v.5M12 16.5h.01"/>'),
    'play': svg('<circle cx="12" cy="12" r="9"/><path d="M10 8.5l5 3.5-5 3.5z"/>', 2),
    'steps': svg('<path d="M4 6h16M4 12h10M4 18h7"/><path d="M16 16l2 2 4-4"/>'),
    'chat': svg('<path d="M4 12a8 8 0 1 1 3.3 6.5L4 20l1.3-3.5A7.9 7.9 0 0 1 4 12z"/>'),
    'shield': svg('<path d="M12 3l7 3v5c0 4.5-3 8.5-7 10-4-1.5-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>'),
    'lock': svg('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>', 2),
    'user': svg('<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/>'),
    'users': svg('<circle cx="9" cy="7" r="3.5"/><circle cx="17" cy="10" r="2.5"/><path d="M2.5 21c0-3.6 2.9-6.5 6.5-6.5s6.5 2.9 6.5 6.5M15 15.2c.6-.2 1.3-.2 2-.2 2.5 0 4.5 2 4.5 4.5"/>'),
    'usb': svg('<rect x="7" y="9" width="10" height="13" rx="2"/><path d="M9 9V3h6v6M11 5.5h.01M13 5.5h.01"/>'),
    'mail': svg('<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3.5 7l8.5 6 8.5-6"/>'),
    'alert': svg('<circle cx="12" cy="12" r="9"/><path d="M12 7.5v5M12 16h.01"/>', 2),
    'check': svg('<circle cx="12" cy="12" r="9"/><path d="M8 12.5l3 3 5-6"/>'),
}

TABS = [  # (מפתח, קובץ, שם הלשונית, אייקון)
    ('index', 'index.html', 'ראשי', 'home'),
    ('method', 'method.html', 'שיטת קמפבל', 'book'),
    ('gift', 'gift.html', 'המדריך החינמי', 'gift'),
    ('haftara', 'haftara.html', 'לימוד הפטרות', 'scroll'),
    ('courses', 'courses.html', 'עוד קורסים', 'grid'),
    ('ask', 'ask.html', 'שאל את יועז', 'question'),
]

REVIEWS = [('1216390940', 'הרב ישראל מלמד'), ('1216390941', 'ראובן קריצבסקי'), ('1216390942', 'ראובן נחודה')]

# שאלות נפוצות – אותן שאלות ותשובות כמו באתר ברב מסר
FAQ = [
    ('איך לומדים קריאה בתורה בשיטת קמפבל?', 'בתהליך מסודר, שלב אחרי שלב: לימוד הטעמים, לימוד הניקוד, כללים בסיסיים בקריאה, קריאה מתוך החומש, הכנה מתוך תיקון קוראים, וההיגיון שמאחורי הטעמים. כל שלב בנוי על הקודם. בסוף אתה לא רק חוזר אחרי מישהו, אלא מבין מה אתה עושה.'),
    ('איך לומדים טעמי המקרא בלי לשנן?', 'במקום לשנן כל מנגינה בנפרד, לומדים לזהות כל טעם, להבדיל בין טעמים שנראים או נשמעים דומים, ולהבין את ההיגיון שמאחוריהם: איזה טעם מגיע מתי, ומה התפקיד שלו. מנגינה שצריך לשנן הופכת לתבנית שאפשר להבין.'),
    ('מה זה שיטת קמפבל?', 'שיטה ללימוד קריאת התורה שפיתח יועז קמפבל, קורא בתורה ומורה לקריאה. היא מפרקת את קריאת התורה לגורמים פשוטים וברורים, ומלמדת חוקים שחוזרים בכל נוסח ובכל פרשה. ככה אפשר לגשת לכל פרשה, ולא רק לזו שהכנת.'),
    ('מה זה "בטעם המקרא"?', 'בטעם המקרא הוא המקום שבו יועז קמפבל מלמד קריאת התורה בשיטת קמפבל: קורס מלא, מדריך חינמי, ומענה לשאלות בדרך.'),
    ('מי זה יועז קמפבל?', 'יועז קמפבל קורא בתורה כבר יותר מ־15 שנה, ומלמד קריאה בתורה יותר מ־10 שנים: מנערי בר מצווה ועד שלוחים ורבנים בקהילות בארץ ובחו"ל. מתוך העבודה הזו נולדה שיטת קמפבל.'),
    ('אני כבר יודע קצת לקרוא. זה מתאים לי?', 'כן. דווקא מי שכבר קורא, אבל מרגיש שהוא עדיין תלוי בהקלטות או במישהו שיסמן ויתקן אותו, מקבל כאן סדר ובהירות.'),
    ('זה מתאים גם למי שמתחיל מאפס?', 'כן. השיטה בנויה בהדרגה, מהבסיס ועד ההכנה מתוך תיקון קוראים.'),
    ('אחרי השיטה לא צריך להכין קריאה?', 'בוודאי שצריך. אבל ההכנה משתנה לגמרי: במקום להתחיל כל פעם מאפס, ניגשים לקריאה עם הבנה של הטעמים, התבניות וההיגיון.'),
    ('אפשר ללמוד קריאה בתורה בנוסח מרוקאי, ירושלמי, אשכנזי או חב"ד?', 'כן. כל אחד מקבל קורס מותאם לנוסח שלו: אשכנזי, חב"ד, מרוקאי או ירושלמי.'),
    ('צריך תיקון קוראים?', 'מומלץ מאוד, כי חלק מהשיטה מלמד איך להכין קריאה מתוך תיקון קוראים בצורה נכונה.'),
    ('זה מתאים ללימוד קריאה בתורה לבר מצווה?', 'כן. זה מתאים מאוד לנער בר מצווה שרוצה לדעת לקרוא כמו שצריך, ולא רק להגיע מוכן לקריאה של הבר מצווה.'),
    ('זה מתאים למבוגרים?', 'כן. השיטה מתאימה למבוגרים, לאברכים, לשלוחים, לרבנים ולכל מי שרוצה לקרוא בתורה בצורה מסודרת ובטוחה יותר.'),
    ('כמה זמן תהיה לי גישה?', 'הגישה לקורס היא למשך שנה מיום הרכישה.'),
    ('אפשר לשאול שאלות אם אני נתקע?', 'בוודאי. שולחים שאלה במייל או בוואטסאפ, ומקבלים מענה. אתה לא לבד בתהליך.'),
    ('מה ההבדל בין נוסח אשכנזי לנוסח חב"ד?', 'נוסח אשכנזי הוא כפי המקובל בקהילות אשכנז, בהגייה עברית רגילה. נוסח חב"ד הוא כפי המקובל בקהילות אנ"ש, בהגייה אשכנזית ("לשון הקודש").'),
]

YN = ['מונח זרקא מונח סגול', 'מונח זרקא סגול', 'זרקא מונח סגול', 'זרקא סגול', 'מונח מונח רביעי', 'מונח רביעי', 'רביעי',
      'קדמא מהפך פשטא מונח זקף-קטן', 'מהפך פשטא מונח זקף-קטן', 'פשטא מונח זקף-קטן', 'מהפך פשטא זקף-קטן', 'מרכא פשטא זקף-קטן',
      'פשטא זקף-קטן', 'מונח זקף-קטן', 'זקף-קטן', 'זקף-גדול', 'מרכא טיפחא מונח אתנחתא', 'טיפחא מונח אתנחתא', 'מרכא טיפחא אתנחתא',
      'טיפחא אתנחתא', 'אתנחתא', 'פזר', 'מונח פזר', 'תלישא-קטנה', 'מונח תלישא-קטנה', 'תלישא-גדולה', 'מונח תלישא-גדולה',
      'קדמא ואזלא', 'אזלא-גרש', 'גרשיים', 'מונח גרשיים', 'דרגא תביר', 'מרכא תביר', 'תביר', 'יתיב', 'מרכא טיפחא מרכא סוף-פסוק',
      'מרכא טיפחא סוף-פסוק', 'טיפחא מרכא סוף-פסוק', 'טיפחא סוף-פסוק', 'סוף-פסוק', 'מרכא טיפחא סוף-פסוק סיום עלייה',
      'טיפחא מרכא סוף-פסוק סיום עלייה']
YN_AUDIO = 'https://raw.githubusercontent.com/ilanmat0/landing-page-assets/main/yoaz-campbell/audio/chabad-yamim-noraim/chabad-yn-{:02d}.mp3'

e = html.escape


def faq_html(items):
    out = ['        <div class="faq">']
    for q, a in items:
        out.append(f'          <details class="rv"><summary>{e(q, False)}</summary><p>{e(a, False)}</p></details>')
    out.append('        </div>')
    return '\n'.join(out)


def reviews_html():
    out = ['        <div class="reviews">']
    for vid, name in REVIEWS:
        out.append(f'''          <figure class="review rv">
            <div class="review__v"><iframe src="https://player.vimeo.com/video/{vid}?title=0&amp;byline=0&amp;portrait=0" title="המלצה של {e(name)}" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen></iframe></div>
            <figcaption><i aria-hidden="true">{name.replace('הרב ', '')[0]}</i><b>{e(name, False)}</b></figcaption>
          </figure>''')
    out.append('        </div>')
    return '\n'.join(out)


def templates_html():
    rows = []
    for i, name in enumerate(YN, 1):
        rows.append(f'''          <li class="tpl rv" data-name="{e(name)}"><button class="tpl__play" type="button" data-src="{YN_AUDIO.format(i)}" aria-label="השמעת התבנית {e(name)}">{svg('<path d="M8 5.5v13l11-6.5z" fill="currentColor"/>', 1.6)}</button><span class="tpl__n">{i}</span><div style="flex:1"><span class="tpl__name">{e(name, False)}</span><div class="tpl__bar"><i></i></div></div></li>''')
    return '\n'.join(rows)


def jsonld(page):
    base = SITE_URL or ''
    blocks = []
    if page.get('jsonld'):
        g = {"@context": "https://schema.org", "@graph": [
            {"@type": "Organization", "name": "בטעם המקרא – שיטת קמפבל לקריאה בתורה", "alternateName": ["בטעם המקרא", "שיטת קמפבל"],
             **({"url": base} if base else {}), "sameAs": ["https://www.youtube.com/channel/UCgJLPqAMMy7oCZhyFuSgOgw"]},
            {"@type": "Person", "name": "יועז קמפבל", "jobTitle": "קורא בתורה ומורה לקריאת התורה",
             "knowsAbout": ["קריאת התורה", "טעמי המקרא", "לימוד קריאה בתורה"], "sameAs": ["https://www.youtube.com/channel/UCgJLPqAMMy7oCZhyFuSgOgw"]},
            {"@type": "Course", "name": "לימוד קריאת התורה בשיטת קמפבל", "inLanguage": "he",
             "description": "קורס לימוד קריאת התורה: טעמי המקרא, ניקוד, כללי קריאה בתורה והכנה מתוך תיקון קוראים, בנוסח אשכנזי, חב\"ד, מרוקאי וירושלמי.",
             "provider": {"@type": "Organization", "name": "בטעם המקרא"}},
        ]}
        blocks.append(g)
    if page.get('faqld'):
        blocks.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
    out = [f'  <script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in blocks]
    return '\n'.join(out)


# כל טקסט "עלה" (בלי תגיות בתוכו) מקבל סימון לאזור הניהול, כך שאפשר לשנות אותו בלי קוד
LEAF = re.compile(r'<(h1|h2|h3|p|li|b|span|summary|small|blockquote)((?:\s+(?!data-edit)[\w:-]+(?:="[^"]*")?)*)\s*>([^<>]{2,})</\1>')
SKIP_CLASSES = ('step__n', 'card__num', 'tpl__n', 'tpl__name', 'kicker', 'path__go', 'path__tag', 'ccard__go', 'giftcard__badge', 'price__tag', 'guarantee__seal')


def tag_leaves(body, key):
    n = [0]

    def rep(m):
        tag, attrs, text = m.groups()
        if any(c in attrs for c in SKIP_CLASSES) or not text.strip() or text.strip() in ('←', '?', '”', '×'):
            return m.group(0)
        n[0] += 1
        label = re.sub(r'\s+', ' ', html.unescape(text.strip()))[:40]
        typ = ' data-type="long"' if len(text) > 70 else ''
        return f'<{tag}{attrs} data-edit="{key}.t{n[0]}" data-label="{e(label)}"{typ}>{text}</{tag}>'
    return LEAF.sub(rep, body)


def build():
    layout = open(os.path.join(ROOT, 'src', 'layout.html'), encoding='utf-8').read()
    pages_dir = os.path.join(ROOT, 'src', 'pages')
    for fn in sorted(os.listdir(pages_dir)):
        raw = open(os.path.join(pages_dir, fn), encoding='utf-8').read()
        m = re.match(r'\s*<!--(\{.*?\})-->', raw, re.S)
        meta = json.loads(m.group(1))
        body = raw[m.end():]
        key = fn[:-5]
        body = (body.replace('{{reviews}}', reviews_html()).replace('{{faq}}', faq_html(FAQ))
                .replace('{{faq_short}}', faq_html([FAQ[i] for i in (5, 6, 8, 9, 13)]))
                .replace('{{templates}}', templates_html()))
        body = tag_leaves(body, key)
        body = re.sub(r'\{\{ic:(\w+)\}\}', lambda mm: IC[mm.group(1)], body)
        tabs = '\n'.join(f'        <a href="{f}"{" aria-current=\"page\"" if meta["tab"] == k else ""}{" class=\"tabs__gift\"" if k == "gift" else ""}>{n}</a>' for k, f, n, _ in TABS)
        drawer = '\n'.join(f'        <a href="{f}"{" aria-current=\"page\"" if meta["tab"] == k else ""}>{IC[i]}{n}</a>' for k, f, n, i in TABS)
        head = jsonld(meta)
        if SITE_URL:
            url = SITE_URL + ('' if key == 'index' else fn)
            head += f'\n  <link rel="canonical" href="{url}">\n  <meta property="og:url" content="{url}">'
        out = (layout.replace('{{body}}', body).replace('{{tabs}}', tabs).replace('{{drawer}}', drawer)
               .replace('{{title}}', e(meta['title'])).replace('{{desc}}', e(meta['desc']))
               .replace('{{ogimg}}', meta.get('ogimg', 'synagogue.jpg')).replace('{{key}}', key).replace('{{head}}', head))
        out = out.replace('{{wa_usb}}', WA_USB).replace('{{mail_usb}}', MAIL_USB).replace('{{wa}}', WA.replace('&', '&amp;'))
        left = re.findall(r'\{\{[^}]+\}\}', out)
        assert not left, (fn, left)
        open(os.path.join(ROOT, fn), 'w', encoding='utf-8', newline='\n').write(out)
        print('נבנה:', fn)


if __name__ == '__main__':
    build()
