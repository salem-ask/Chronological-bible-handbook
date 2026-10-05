"""Build "Archaeology and the Bible" (HTML, then PDF via build-pdf.js).

    python3 bonuses/archaeology/build_archaeology.py

The illustrations are simple line drawings in the Bookline style. They are
not photographs and are not to scale.
"""
import html
import os

from discoveries import DISCOVERIES

HERE = os.path.dirname(os.path.abspath(__file__))
G = "#C9A24E"   # gold
S = 'fill="none" stroke="%s" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"' % G


def lines(x1, x2, y0, n, gap=9, jag=0):
    out = []
    for i in range(n):
        y = y0 + i * gap
        out.append('<path %s stroke-width="1.3" d="M%d %d H%d"/>' % (S, x1 + (i * 7 % 11 if jag else 0), y, x2 - (i * 5 % 13 if jag else 0)))
    return "".join(out)


ART = {
    "stele": '<path %s d="M45 205 V70 Q100 18 155 70 V205 Z"/>' % S + lines(60, 140, 82, 13),
    "stele2": '<path %s d="M50 205 V78 Q100 30 150 78 V205 Z"/>' % S
              + '<path %s stroke-width="1.2" d="M62 120 L85 135 L80 160 L105 175 M118 98 L130 128 L150 136"/>' % S
              + lines(62, 138, 92, 12),
    "fragments": '<path %s d="M40 60 L95 52 L104 110 L70 128 L44 112 Z"/>' % S
                 + '<path %s d="M112 70 L160 78 L150 140 L118 132 Z"/>' % S
                 + '<path %s d="M60 140 L112 146 L104 196 L58 186 Z"/>' % S
                 + lines(50, 92, 70, 5, 10, 1) + lines(120, 150, 90, 4, 10, 1) + lines(66, 104, 156, 3, 10, 1),
    "obelisk": '<path %s d="M70 205 V58 L82 38 H118 L130 58 V205 Z"/>' % S
               + "".join('<rect x="76" y="%d" width="48" height="22" %s stroke-width="1.3"/>' % (y, S) for y in (66, 98, 130, 162))
               + '<path %s stroke-width="1.2" d="M86 92 q6 -10 14 0 M104 92 h12"/>' % S,
    "tunnel": '<path %s d="M30 60 C70 40, 60 120, 110 110 S150 170, 175 190"/>' % S
              + '<path %s d="M30 80 C64 62, 50 140, 108 130 S140 188, 160 200"/>' % S
              + '<circle cx="30" cy="70" r="7" %s/>' % S + '<rect x="120" y="40" width="54" height="34" rx="2" %s/>' % S
              + lines(127, 167, 50, 3, 8),
    "prism": '<path %s d="M70 30 H130 L148 48 V190 L130 208 H70 L52 190 V48 Z"/>' % S
             + '<path %s stroke-width="1.3" d="M70 30 V208 M130 30 V208"/>' % S + lines(76, 124, 50, 16, 9),
    "amulet": '<rect x="40" y="70" width="34" height="90" rx="17" %s/>' % S
              + '<path %s stroke-width="1.3" d="M40 88 H74 M40 142 H74"/>' % S
              + '<path %s d="M100 60 H172 V178 H100 Z"/>' % S + lines(108, 164, 76, 11, 9, 1),
    "tablet": '<rect x="55" y="40" width="90" height="150" rx="14" %s/>' % S
              + "".join('<path %s stroke-width="1.3" d="M%d %d l6 0 l-3 6 z"/>' % (S, x, y)
                        for y in range(58, 178, 14) for x in range(68, 132, 12)),
    "ostracon": '<path %s d="M42 70 Q60 40 110 46 Q160 50 162 92 Q168 150 120 176 Q70 192 48 150 Q30 110 42 70 Z"/>' % S
                + lines(58, 146, 78, 9, 10, 1),
    "cylinder": '<ellipse cx="100" cy="60" rx="38" ry="12" %s/>' % S
                + '<path %s d="M62 60 Q56 125 62 190 M138 60 Q144 125 138 190"/>' % S
                + '<path %s d="M62 190 Q100 204 138 190"/>' % S + lines(66, 134, 84, 11, 9),
    "block": '<path %s d="M35 70 H165 V170 H35 Z"/>' % S
             + '<path %s stroke-width="1.3" d="M35 70 L50 58 H175 L165 70 M175 58 V158 L165 170"/>' % S
             + lines(55, 145, 96, 3, 22) + '<path %s stroke-width="1.2" d="M40 150 L60 170 M140 70 L150 92"/>' % S,
    "gallio": '<path %s d="M30 60 L80 56 L84 104 L36 110 Z"/>' % S
              + '<path %s d="M92 50 L150 56 L146 98 L96 96 Z"/>' % S
              + '<path %s d="M40 124 L96 118 L100 176 L44 184 Z"/>' % S
              + '<path %s d="M110 112 L168 118 L162 170 L114 166 Z"/>' % S
              + lines(42, 76, 70, 4, 9, 1) + lines(102, 140, 66, 3, 9, 1) + lines(52, 92, 134, 5, 9, 1) + lines(122, 158, 128, 4, 9, 1),
}


def art(key):
    return ('<svg viewBox="0 0 200 230" role="img" aria-label="Line illustration (not to scale)">'
            '<rect x="4" y="4" width="192" height="222" rx="6" fill="#4A1519"/>'
            '<rect x="10" y="10" width="180" height="210" rx="3" fill="none" stroke="%s" stroke-width=".8"/>%s</svg>'
            % (G, ART[key]))


e = html.escape
items = []
glance = []
for i, d in enumerate(DISCOVERIES, 1):
    ref, text = d["verse"]
    glance.append('<li><b>%02d</b><span class="g-name">%s</span><span class="g-date">%s</span></li>'
                  % (i, e(d["name"]), e(d.get("short_date", d["date"]))))
    items.append("""
<article class="disc page">
  <header class="d-head">
    <div class="num">%02d</div>
    <div><p class="kicker">%s</p><h2>%s</h2></div>
  </header>
  <div class="d-grid">
    <aside>
      <figure class="art">%s<figcaption>Illustration, not to scale</figcaption></figure>
      <dl class="facts">
        <dt>The object</dt><dd>%s</dd>
        <dt>Discovered</dt><dd>%s</dd>
        <dt>Where it is today</dt><dd>%s</dd>
      </dl>
    </aside>
    <div class="d-body">
      <h3>What was discovered</h3><p>%s</p>
      <h3><span class="tag">1</span> What the evidence directly shows</h3><p>%s</p>
      <h3><span class="tag">2</span> The historical context</h3><p>%s</p>
      <h3><span class="tag">3</span> How it relates to the biblical account</h3><p>%s</p>
      <p class="refs"><strong>Bible references:</strong> %s</p>
      <blockquote><p>%s</p><cite>%s (KJV)</cite></blockquote>
    </div>
  </div>
  <div class="hb-box"><h3>In the Chronological Bible Handbook</h3><p>%s</p></div>
  <div class="q-box"><h3>For reflection</h3><p>%s</p></div>
</article>""" % (i, e(d["date"]), e(d["name"]), art(d["art"]), e(d["object"]), e(d["found"]), e(d["kept"]),
                 e(d["what"]), d["evidence"], e(d["context"]), e(d["bible"]), e(d["refs"]),
                 e(text), e(ref), e(d["handbook"]), e(d["question"])))

template = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
out = template.replace("{{GLANCE}}", "\n".join(glance)).replace("{{ITEMS}}", "\n".join(items))
open(os.path.join(HERE, "archaeology.html"), "w", encoding="utf-8").write(out)
print("wrote archaeology.html with", len(DISCOVERIES), "discoveries")
