// בטעם המקרא – התנהגות האתר: תפריט, טפסי רב מסר, חלון תשלום, שאל את יועז, נגן התבניות, נגישות ועוגיות.
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const lock = on => document.body.classList.toggle('no-scroll', on);

  // ---------- הופעה עדינה בגלילה ----------
  const items = $$('.rv');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    }), { rootMargin: '0px 0px -6% 0px', threshold: 0.08 });
    items.forEach(el => io.observe(el));
  } else items.forEach(el => el.classList.add('in'));

  // ---------- תפריט ----------
  const hdr = $('.hdr');
  const onScroll = () => hdr && hdr.classList.toggle('scrolled', window.scrollY > 30);
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  const drawer = $('#drawer'), burger = $('[data-drawer-open]');
  const setDrawer = on => {
    if (!drawer) return;
    drawer.classList.toggle('open', on); drawer.setAttribute('aria-hidden', String(!on));
    burger?.setAttribute('aria-expanded', String(on)); lock(on);
    if (on) $('.drawer__close', drawer)?.focus();
  };
  burger?.addEventListener('click', () => setDrawer(true));
  $$('[data-drawer-close]').forEach(b => b.addEventListener('click', () => setDrawer(false)));

  // ---------- טפסי רב מסר: מקטינים טופס רחב כדי שייכנס למסך ----------
  const fit = () => $$('.rm-slot').forEach(slot => {
    const form = slot.querySelector('div[class^="RDUI"]');
    if (!form) return;
    form.style.transform = ''; slot.style.height = '';
    const room = slot.clientWidth, w = form.offsetWidth;
    if (w > room + 1 && room > 0) {
      const k = room / w;
      form.style.transformOrigin = 'top center';
      form.style.transform = `scale(${k})`;
      slot.style.height = Math.ceil(form.offsetHeight * k) + 'px';
    }
  });
  window.addEventListener('load', fit); window.addEventListener('resize', fit);
  let n = 0; const t = setInterval(() => { fit(); if (++n > 24) clearInterval(t); }, 500);

  // מחכים שטופס של רב מסר ייטען, ואז מפעילים עליו פעולה
  const whenForm = (scope, fn) => {
    const go = () => { const f = scope.querySelector('form'); if (f && !f.dataset.hooked) { f.dataset.hooked = '1'; fn(f); } return !!f; };
    if (!go()) { const iv = setInterval(() => { if (go()) clearInterval(iv); }, 400); setTimeout(() => clearInterval(iv), 30000); }
  };
  // iframe ריק נטען פעם אחת כשהדף עולה. כל טעינה אחרי זה = רב מסר שלח את הטופס והעביר לדף הבא
  const realLoad = fr => { try { return fr.contentWindow.location.href !== 'about:blank'; } catch { return true; } };

  // ---------- מסמכים ----------
  const LEGAL = {
    terms: ['תקנון שימוש', `
      <p><strong>1. כללי</strong> — השימוש באתר ובתכניו ("בטעם המקרא — שיטת קמפבל") כפוף לתנאים המפורטים להלן. הגלישה באתר מהווה הסכמה לתנאים אלו.</p>
      <p><strong>2. זכויות יוצרים</strong> — כל התכנים, השיעורים, ההקלטות והחומרים המוצגים באתר מוגנים בזכויות יוצרים ושייכים ליועז קמפבל. אין להעתיק, להפיץ, לשתף, להציג בפומבי או לעשות שימוש מסחרי כלשהו ללא אישור מפורש בכתב.</p>
      <p><strong>3. שימוש אישי</strong> — הרישום לקורס מקנה רישיון אישי, לא־מסחרי, לא־ניתן להעברה, לצפייה והאזנה לתכנים. אין לשתף את פרטי הגישה עם צד שלישי.</p>
      <p><strong>4. תשלום והחזר</strong> — קורס שיטת קמפבל כולל אחריות להחזר כספי מלא: מי שיבקש זאת תוך 14 יום ממועד הרכישה, במייל או בוואטסאפ, יקבל את מלוא הסכום בחזרה. בנוסף חלות הוראות חוק הגנת הצרכן.</p>
      <p><strong>5. הגבלת אחריות</strong> — האתר והתכנים ניתנים כמות שהם (As Is). יועז קמפבל לא יישא באחריות לכל נזק עקיף או תוצאתי שייגרם משימוש באתר.</p>
      <p><strong>6. שינויים</strong> — אנו שומרים את הזכות לעדכן את התקנון מעת לעת. השימוש באתר לאחר העדכון מהווה הסכמה לתנאים המעודכנים.</p>
      <p><strong>7. דין ושיפוט</strong> — על השימוש באתר יחולו דיני מדינת ישראל. סמכות שיפוט בלעדית נתונה לבתי המשפט המוסמכים בישראל.</p>`],
    privacy: ['מדיניות פרטיות', `
      <p><strong>איזה מידע אנחנו אוספים?</strong> פרטים שאתם מספקים בטפסים (שם, טלפון, דוא"ל, נוסח מועדף), ונתוני שימוש בסיסיים (כתובת IP, סוג דפדפן, דפים שנצפו).</p>
      <p><strong>למה?</strong> כדי לאפשר רישום לקורסים, ליצור איתכם קשר, לשלוח תכנים ועדכונים, ולשפר את האתר.</p>
      <p><strong>טפסים</strong> — הטפסים באתר מופעלים על ידי מערכת הדיוור "רב מסר". שאלה שנשלחת בטופס "שאל את יועז" מועברת אליו גם במייל באמצעות שירות שליחת טפסים (FormSubmit).</p>
      <p><strong>שיתוף עם צד שלישי</strong> — לא נמכור או נמסור את פרטיכם לגורמים מסחריים. ייתכן שיתוף עם ספקי שירות (אחסון, ניתוח, דיוור, תשלום) הפועלים מטעמנו ומחויבים לסודיות.</p>
      <p><strong>זכויותיכם</strong> — לפי חוק הגנת הפרטיות, באפשרותכם לבקש לעיין במידע, לתקן אותו או למחוק אותו. פנו אלינו במייל ונטפל בבקשה תוך זמן סביר.</p>
      <p><strong>אבטחה</strong> — אנחנו נוקטים אמצעים סבירים לאבטחת המידע, אך אין אבטחה מוחלטת.</p>`],
    cookies: ['מדיניות עוגיות (Cookies)', `
      <p>אתר זה משתמש בקבצי "עוגיות" (Cookies) — קבצי מידע קטנים שנשמרים בדפדפן.</p>
      <h3>סוגי העוגיות באתר</h3>
      <ul><li><strong>חיוניות</strong> — נדרשות לתפקוד תקין של האתר (זכירת בחירת עוגיות, נגישות).</li>
      <li><strong>ביצועים וניתוח</strong> — מסייעות להבין איך משתמשים באתר ולשפר אותו.</li>
      <li><strong>שיווק</strong> — מאפשרות התאמת מודעות וקמפיינים.</li></ul>
      <p>בלחיצה על "אישור" בבאנר העוגיות אתם מאשרים את כל הסוגים. בלחיצה על "רק חיוניות" יישמרו רק עוגיות הכרחיות.</p>`],
    accessibility: ['הצהרת נגישות', `
      <p>האתר נבנה במחויבות להנגשה לפי תקן ישראלי 5568 ברמה AA, הכולל בין היתר:</p>
      <ul><li>תמיכה בניווט מקלדת</li><li>טקסטים בניגודיות תקנית</li><li>תיוג סמנטי וכותרות מסודרות</li><li>טקסט חלופי לתמונות</li><li>תמיכה בכיווניות RTL מלאה</li>
      <li>תפריט נגישות (בפינת המסך) להגדלת טקסט, ניגודיות גבוהה ועצירת אנימציות</li></ul>
      <p>נתקלת בבעיית נגישות? נשמח לדעת ולתקן: <a href="mailto:yoazcam770@gmail.com">yoazcam770@gmail.com</a>.</p>
      <p><strong>רכז נגישות:</strong> יועז קמפבל</p>`]
  };
  const legal = $('#legal'), pay = $('#pay');
  const open = m => { m.hidden = false; lock(true); $('.modal__x', m)?.focus(); };
  const close = m => { if (m && !m.hidden) { m.hidden = true; lock(false); } };
  document.addEventListener('click', e => {
    const a = e.target.closest('[data-modal]');
    if (a) { e.preventDefault(); const d = LEGAL[a.dataset.modal]; if (!d) return; $('#legal-body').innerHTML = '<h2>' + d[0] + '</h2>' + d[1]; open(legal); }
  });
  $$('.modal').forEach(m => {
    m.addEventListener('click', e => { if (e.target === m || e.target.closest('[data-close]')) close(m); });
  });

  // ---------- תשלום: טופס הרכישה נשלח לתוך חלון, ודף התשלום מוצג שם ----------
  const frame = $('#payframe');
  $$('[data-pay-form]').forEach(slot => whenForm(slot, f => f.setAttribute('target', 'payframe')));
  frame?.addEventListener('load', () => { if (realLoad(frame)) { open(pay); $('.modal__panel', pay).scrollTop = 0; } });

  // ---------- שאל את יועז ----------
  const askBox = $('#ask-form');
  if (askBox) {
    const sink = document.createElement('iframe');
    sink.name = sink.id = 'askframe'; sink.hidden = true; sink.title = 'שליחת השאלה';
    document.body.append(sink);
    let sent = null;
    whenForm($('#ask-rm'), f => {
      f.setAttribute('target', 'askframe');
      // מסתירים את "מי שואל" ואת "נוסח" (יועז ביקש בלי השאלות האלה)
      // השדות נטענים קצת אחרי הטופס, ולכן מנסים שוב כמה שניות
      const tidy = () => {
        ['fields[121079_List:129978]', 'fields[121080_List:129978]'].forEach(nm => {
          const inp = f.querySelector('[name="' + nm + '"]'); if (!inp) return;
          const box = inp.closest('.multyfield') || inp.closest('.inner_multyfields > *') || inp;
          box.style.setProperty('display', 'none', 'important');
        });
        const q = f.querySelector('textarea'); if (q) q.placeholder = 'השאלה שלך';
        fit();
      };
      tidy(); let k = 0; const ti = setInterval(() => { tidy(); if (++k > 20) clearInterval(ti); }, 400);
      const grab = () => {
        const v = nm => (f.querySelector('[name="' + nm + '"]') || {}).value || '';
        sent = { name: v('fields[13_Fixed]'), email: v('fields[1_Fixed]'), phone: v('fields[2_Fixed]'), question: v('fields[121078_List:129978]') };
      };
      f.addEventListener('click', e => { if (e.target.closest('[type=submit], .submitButton')) grab(); }, true);
      f.addEventListener('submit', grab, true);
    });
    sink.addEventListener('load', () => {
      if (!realLoad(sink)) return;
      $('#ask-live').hidden = true;
      $('.ask-done', askBox).hidden = false;
      // גיבוי: השאלה נשלחת ליועז גם ישירות למייל, עם כל הטקסט
      if (sent && sent.question) {
        fetch('https://formsubmit.co/ajax/yoazcam770@gmail.com', {
          method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ _subject: 'שאלה חדשה מהאתר – ' + sent.name, _template: 'table', _captcha: 'false', _replyto: sent.email,
            'שם': sent.name, 'מייל': sent.email, 'טלפון': sent.phone, 'השאלה': sent.question })
        }).catch(() => { });
      }
    });
  }

  // ---------- נגן תבניות הטעמים ----------
  const list = $('.tpl-list');
  if (list) {
    const audio = new Audio(); audio.preload = 'none';
    let cur = null;
    const PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>';
    const PAUSE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z" fill="currentColor"/></svg>';
    const reset = () => { if (!cur) return; cur.classList.remove('playing'); $('.tpl__play', cur).innerHTML = PLAY; $('.tpl__bar i', cur).style.width = '0'; };
    list.addEventListener('click', e => {
      const b = e.target.closest('.tpl__play'); if (!b) return;
      const row = b.closest('.tpl');
      if (cur === row && !audio.paused) { audio.pause(); return; }
      if (cur !== row) { reset(); cur = row; audio.src = b.dataset.src; }
      audio.play().catch(() => { });
    });
    audio.addEventListener('play', () => { cur.classList.add('playing'); $('.tpl__play', cur).innerHTML = PAUSE; });
    audio.addEventListener('pause', () => { if (cur) $('.tpl__play', cur).innerHTML = PLAY; });
    audio.addEventListener('ended', reset);
    audio.addEventListener('timeupdate', () => { if (cur && audio.duration) $('.tpl__bar i', cur).style.width = (audio.currentTime / audio.duration * 100) + '%'; });
    const search = $('.tpl-search'), count = $('.tpl-count');
    search?.addEventListener('input', () => {
      const q = search.value.trim().replace(/-/g, ' ');
      let shown = 0;
      $$('.tpl', list).forEach(r => { const ok = !q || r.dataset.name.replace(/-/g, ' ').includes(q); r.hidden = !ok; if (ok) { shown++; r.classList.add('in'); } });
      count.textContent = shown + ' תבניות';
    });
  }

  // ---------- כפתור יצירת קשר ----------
  const fab = $('#fab'), fabBtn = $('#fab-btn'), fabMenu = $('#fab-menu');
  const setFab = on => { fabMenu.hidden = !on; fab.classList.toggle('open', on); fabBtn.setAttribute('aria-expanded', String(on)); };
  fabBtn?.addEventListener('click', e => { e.stopPropagation(); setFab(fabMenu.hidden); });
  document.addEventListener('click', e => { if (fab && !fabMenu.hidden && !fab.contains(e.target)) setFab(false); });

  // ---------- עוגיות ----------
  const ck = $('#cookies');
  try { if (ck && !localStorage.getItem('cookieConsent')) setTimeout(() => { ck.hidden = false; }, 1400); } catch { }
  $$('[data-cookies]').forEach(b => b.addEventListener('click', () => { try { localStorage.setItem('cookieConsent', b.dataset.cookies); } catch { } ck.hidden = true; }));

  // ---------- נגישות ----------
  const ab = $('#a11y-btn'), ap = $('#a11y-panel'), root = document.documentElement;
  let step = 0;
  const panel = on => { ap.hidden = !on; ab.setAttribute('aria-expanded', String(on)); };
  ab?.addEventListener('click', e => { e.stopPropagation(); panel(ap.hidden); });
  document.addEventListener('click', e => { if (ap && !ap.hidden && !ap.contains(e.target) && e.target !== ab) panel(false); });
  $$('[data-a11y]').forEach(b => b.addEventListener('click', () => {
    const a = b.dataset.a11y;
    if (a === 'bigger') step = Math.min(3, step + 1);
    else if (a === 'smaller') step = Math.max(-2, step - 1);
    else if (a === 'reset') {
      step = 0; root.classList.remove('a11y-contrast', 'a11y-gray', 'a11y-links', 'a11y-motion');
      $$('.a11y-toggle').forEach(x => { x.setAttribute('aria-pressed', 'false'); x.textContent = 'הפעלה'; });
    } else {
      const on = root.classList.toggle('a11y-' + a);
      b.setAttribute('aria-pressed', String(on)); b.textContent = on ? 'כיבוי' : 'הפעלה';
    }
    document.body.style.zoom = step === 0 ? '' : (100 + step * 12) + '%';
  }));

  // Escape סוגר הכל
  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    setDrawer(false); close(legal); close(pay); if (fab) setFab(false); if (ap) panel(false);
  });
})();
