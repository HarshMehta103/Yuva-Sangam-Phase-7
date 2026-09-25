"""Assemble the Yuva Sangam Phase 7 single-file site.

Inputs (in src/assets):
  india_sat.jpg      NASA Blue Marble crop (public domain)
  cloud0-3.webp      procedural cloud sprites
  cloudbank.webp     dense cloud bank for the whiteout
  map.json           projected India / Sikkim / Rajasthan paths + pin positions
Output: index.html
"""
import base64, json, math, random

import os
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, 'assets') + os.sep
T = os.path.join(HERE, 'ys7_template.html')
OUT = os.path.join(HERE, '..', 'index.html')

def b64(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()

m = json.load(open(A + 'map.json'))
gx, gy = m['gangtok']; jx, jy = m['iitj']

# Great-circle distance Gangtok -> IIT Jodhpur, rounded to 10 km for display honesty
def hav(lon1, lat1, lon2, lat2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    x = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(x))
KM = round(hav(88.6138, 27.3314, 73.1135, 26.4710) / 10) * 10

# Route arc: quadratic curve lifted north of the straight line (reads as a journey)
mx, my = (gx + jx)/2, (gy + jy)/2
dist = math.hypot(gx - jx, gy - jy)
cx, cy = mx, my - dist*0.34
ARC = f'M{gx:.1f},{gy:.1f} Q{cx:.1f},{cy:.1f} {jx:.1f},{jy:.1f}'

# ---------------------------------------------------------------------------
# SIKKIM panel (viewBox 400x900): Kanchenjunga's five summits, forested ridges,
# a hilltop monastery with golden tiered roof, lungta prayer flags.
# ---------------------------------------------------------------------------
random.seed(4)
LUNGTA = ['#2E6FB5', '#FFFFFF', '#C23B2E', '#3C8C4A', '#F2C230']  # traditional order

def flag_string(x0, y0, x1, y1, sag, n, size=14):
    """Prayer-flag string as a quadratic curve with n flags hanging from it."""
    qx, qy = (x0 + x1)/2, (y0 + y1)/2 + sag
    out = [f'<path d="M{x0},{y0} Q{qx},{qy} {x1},{y1}" stroke="#6B5B4B" stroke-width="1.2" fill="none"/>']
    for i in range(n):
        t = (i + 0.5)/n
        x = (1-t)**2*x0 + 2*(1-t)*t*qx + t**2*x1
        y = (1-t)**2*y0 + 2*(1-t)*t*qy + t**2*y1
        c = LUNGTA[i % 5]
        tilt = random.uniform(-7, 7)
        out.append(f'<rect x="{x-size/2:.1f}" y="{y:.1f}" width="{size}" height="{size*1.15:.1f}" fill="{c}" '
                   f'stroke="rgba(0,0,0,.08)" transform="rotate({tilt:.1f} {x:.1f} {y:.1f})"/>')
    return ''.join(out)

def forest(y_base, color, count, hmin, hmax, x0=-20, x1=420):
    """Row of simple conifers along a ridge."""
    s = []
    for i in range(count):
        x = x0 + (x1 - x0)*i/count + random.uniform(-6, 6)
        h = random.uniform(hmin, hmax)
        s.append(f'<path d="M{x:.1f},{y_base:.1f} l{h*0.28:.1f},{-h:.1f} l{h*0.28:.1f},{h:.1f} Z" fill="{color}"/>')
    return ''.join(s)

SIKKIM_SVG = f'''<svg viewBox="0 0 400 900" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<defs>
  <linearGradient id="skS" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#AFC9E2"/><stop offset=".55" stop-color="#E6EEF5"/><stop offset="1" stop-color="#F4F7FA"/></linearGradient>
  <linearGradient id="h1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8DB39C"/><stop offset="1" stop-color="#6F9C82"/></linearGradient>
  <linearGradient id="h2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5E9277"/><stop offset="1" stop-color="#3F7A5C"/></linearGradient>
  <linearGradient id="h3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2F6A4D"/><stop offset="1" stop-color="#1F4E38"/></linearGradient>
  <linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3CE63"/><stop offset="1" stop-color="#C9962C"/></linearGradient>
</defs>
<rect width="400" height="900" fill="url(#skS)"/>
<!-- Kanchenjunga massif: five summits; lit faces white, shaded faces blue-grey -->
<path d="M-20,410 L40,330 L70,350 L120,262 L150,300 L182,228 L205,262 L232,236 L262,286 L292,250 L330,318 L368,300 L420,380 L420,430 L-20,430 Z" fill="#C9D6E4"/>
<path d="M120,262 L150,300 L140,330 L110,300 Z M182,228 L205,262 L196,300 L176,270 Z M232,236 L262,286 L250,312 L226,270 Z M292,250 L330,318 L316,334 L290,290 Z" fill="#FFFFFF"/>
<path d="M182,228 L160,300 L130,340 L176,318 L200,330 L232,236 L214,300 Z" fill="#F7FAFD" opacity=".9"/>
<path d="M40,330 L70,350 L58,372 Z M368,300 L420,380 L390,372 Z" fill="#FFFFFF" opacity=".85"/>
<path d="M-20,420 L60,378 L130,398 L200,372 L270,396 L340,370 L420,396 L420,440 L-20,440 Z" fill="#A9BBCF" opacity=".7"/>
<!-- mist -->
<ellipse cx="120" cy="438" rx="170" ry="22" fill="#fff" opacity=".75"/>
<ellipse cx="320" cy="452" rx="150" ry="18" fill="#fff" opacity=".65"/>
<!-- ridges -->
<path d="M-20,520 C60,470 120,500 190,462 C260,430 320,470 420,450 L420,900 L-20,900 Z" fill="url(#h1)"/>
{forest(515, '#6E9A80', 26, 16, 30)}
<ellipse cx="220" cy="540" rx="220" ry="16" fill="#fff" opacity=".45"/>
<path d="M-20,640 C70,590 150,610 230,580 C300,556 360,590 420,572 L420,900 L-20,900 Z" fill="url(#h2)"/>
<!-- monastery on the ridge: white walls, maroon band, golden tiered roof -->
<g transform="translate(222,528)">
  <rect x="-58" y="20" width="116" height="52" fill="#FBFBF7"/>
  <rect x="-58" y="20" width="116" height="9" fill="#8B2D2D"/>
  <rect x="-40" y="-8" width="80" height="30" fill="#FBFBF7"/>
  <rect x="-40" y="-8" width="80" height="7" fill="#8B2D2D"/>
  <path d="M-72,22 L72,22 L54,8 L-54,8 Z" fill="url(#gold)"/>
  <path d="M-52,-6 L52,-6 L36,-22 L-36,-22 Z" fill="url(#gold)"/>
  <rect x="-8" y="-40" width="16" height="18" fill="#FBFBF7"/>
  <path d="M-16,-38 L16,-38 L0,-52 Z" fill="url(#gold)"/>
  <rect x="-1.5" y="-66" width="3" height="16" fill="#C9962C"/><circle cx="0" cy="-68" r="4" fill="#E9B949"/>
  <g fill="#6B3A2A">{''.join(f'<rect x="{-48+i*16}" y="38" width="8" height="12" rx="1"/>' for i in range(7))}</g>
  <rect x="-9" y="48" width="18" height="24" fill="#7A2626"/>
  <g fill="#6B3A2A">{''.join(f'<rect x="{-30+i*14}" y="6" width="6" height="9"/>' for i in range(5))}</g>
</g>
{forest(640, '#4E8468', 22, 22, 40)}
<!-- tall white darchor poles -->
<g>
  <rect x="58" y="560" width="3" height="160" fill="#F4F1EA"/><rect x="61" y="566" width="10" height="120" fill="#FFFFFF" opacity=".95"/>
  <rect x="84" y="590" width="3" height="140" fill="#F4F1EA"/><rect x="87" y="596" width="9" height="104" fill="#FFFFFF" opacity=".9"/>
</g>
<!-- lungta strings sweeping across -->
{flag_string(-10, 600, 300, 660, 60, 18)}
{flag_string(40, 690, 420, 640, 70, 20)}
<path d="M-20,760 C90,720 190,748 270,716 C330,694 380,712 420,704 L420,900 L-20,900 Z" fill="url(#h3)"/>
{forest(760, '#1E4B36', 20, 30, 56)}
<rect x="0" y="760" width="400" height="140" fill="url(#h3)"/>
</svg>'''

# ---------------------------------------------------------------------------
# RAJASTHAN panel (viewBox 400x900): Mehrangarh on its rock above the Blue
# City, sun over the Thar, dunes with ripples and a camel.
# ---------------------------------------------------------------------------
random.seed(9)
def blue_city(y0, rows, x0=-10, x1=410):
    s = []
    blues = ['#4E7DB6', '#6A96C8', '#3D6A9F', '#7FA6D2', '#5A88BF']
    for r in range(rows):
        y = y0 + r*26
        x = x0 + random.uniform(-10, 0)
        while x < x1:
            w = random.uniform(22, 42); h = random.uniform(24, 44)
            c = random.choice(blues)
            s.append(f'<rect x="{x:.1f}" y="{y-h:.1f}" width="{w:.1f}" height="{h+30:.1f}" fill="{c}"/>')
            # windows
            for k in range(int(w//14)):
                s.append(f'<rect x="{x+5+k*13:.1f}" y="{y-h+8:.1f}" width="5" height="7" fill="#26446B" opacity=".7"/>')
            x += w + random.uniform(-2, 3)
    return ''.join(s)

def crenel(x0, x1, y, step=9, h=6, color='#B8674A'):
    return ''.join(f'<rect x="{x:.1f}" y="{y-h}" width="{step*0.55:.1f}" height="{h}" fill="{color}"/>'
                   for x in [x0 + i*step for i in range(int((x1-x0)//step)+1)])

RAJ_SVG = f'''<svg viewBox="0 0 400 900" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<defs>
  <linearGradient id="skR" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6D9A6"/><stop offset=".6" stop-color="#FBEBD0"/><stop offset="1" stop-color="#FDF5E8"/></linearGradient>
  <linearGradient id="rock" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A9623F"/><stop offset="1" stop-color="#7E432C"/></linearGradient>
  <linearGradient id="fort" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C47352"/><stop offset="1" stop-color="#A55A3C"/></linearGradient>
  <linearGradient id="d1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EDC074"/><stop offset="1" stop-color="#DDA049"/></linearGradient>
  <linearGradient id="d2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2A443"/><stop offset="1" stop-color="#C98A2B"/></linearGradient>
</defs>
<rect width="400" height="900" fill="url(#skR)"/>
<circle cx="300" cy="150" r="54" fill="#F4B63F" opacity=".9"/>
<circle cx="300" cy="150" r="90" fill="#F4B63F" opacity=".18"/>
<!-- the rock -->
<path d="M-20,560 L10,470 L60,430 L110,420 L170,398 L250,404 L310,430 L360,470 L420,500 L420,640 L-20,640 Z" fill="url(#rock)"/>
<path d="M60,430 L90,470 L80,520 M170,398 L190,450 L176,500 M300,428 L286,480 L300,530" stroke="#6E3A25" stroke-width="2" fill="none" opacity=".5"/>
<!-- Mehrangarh: long curtain wall, round bastions, palace block with jharokhas -->
<g>
  <path d="M30,432 L40,356 L372,350 L380,440 Z" fill="url(#fort)"/>
  {crenel(40, 372, 356)}
  <g fill="#B8674A">
    <rect x="30" y="330" width="44" height="110" rx="20"/><rect x="118" y="318" width="40" height="120" rx="18"/>
    <rect x="236" y="322" width="40" height="118" rx="18"/><rect x="330" y="330" width="46" height="112" rx="20"/>
  </g>
  {crenel(30, 74, 334)}{crenel(118, 158, 322)}{crenel(236, 276, 326)}{crenel(330, 376, 334)}
  <rect x="160" y="250" width="120" height="106" fill="#C47352"/>
  <rect x="176" y="214" width="88" height="40" fill="#CC7C5A"/>
  {crenel(176, 264, 214, 8, 5, '#CC7C5A')}
  <g fill="#8E4A34">
    {''.join(f'<path d="M{170+i*20},{300} v-18 a6,6 0 0 1 12,0 v18 Z"/>' for i in range(5))}
    {''.join(f'<path d="M{184+i*18},{242} v-14 a5,5 0 0 1 10,0 v14 Z"/>' for i in range(4))}
    {''.join(f'<rect x="{50+i*34}" y="392" width="8" height="12" rx="3"/>' for i in range(10))}
  </g>
  <path d="M160,318 h120 v8 h-120 Z" fill="#9C5238"/>
  <rect x="216" y="186" width="2" height="30" fill="#6E3A25"/>
  <path d="M218,188 l22,6 l-22,6 Z" fill="#E0912E"/>
</g>
<!-- Blue City -->
{blue_city(640, 5)}
<rect x="-10" y="740" width="420" height="40" fill="#3D6A9F" opacity=".35"/>
<!-- Thar dunes -->
<path d="M-20,760 C80,720 160,752 240,730 C310,712 370,736 420,724 L420,900 L-20,900 Z" fill="url(#d1)"/>
<path d="M-20,812 C60,782 150,808 230,790 C300,774 360,798 420,786 L420,900 L-20,900 Z" fill="url(#d2)"/>
<g stroke="#C98A2B" stroke-width="1.2" fill="none" opacity=".55">
  <path d="M10,780 q40,-10 80,0"/><path d="M130,770 q50,-12 100,0"/><path d="M270,752 q40,-8 80,0"/>
</g>
<!-- camel -->
<g transform="translate(96,742) scale(1.05)" fill="#5A3A22">
  <path d="M0,40 C4,20 18,8 30,12 C38,0 50,0 56,14 C62,6 70,10 72,18 L86,4 C90,0 96,2 96,8 L92,16 C90,22 84,24 80,26 L76,40 C74,46 70,46 68,40 L66,32 L22,34 L20,48 C18,54 14,54 12,48 L10,40 Z"/>
  <rect x="14" y="40" width="4" height="30" rx="2"/><rect x="24" y="40" width="4" height="30" rx="2"/>
  <rect x="58" y="36" width="4" height="34" rx="2"/><rect x="68" y="36" width="4" height="34" rx="2"/>
  <path d="M86,6 l6,-4" stroke="#5A3A22" stroke-width="2"/>
</g>
</svg>'''

# ---------------------------------------------------------------------------
# Label positions in map user space (font sizes are in user units via CSS)
# ---------------------------------------------------------------------------
GLX, GLY = gx, gy - 58
JLX, JLY = jx, jy + 56


# ---------------------------------------------------------------------------
# Toran (bandhanwar): a festive door-hanging of mango leaves and marigolds,
# drawn as one seamless pattern tile so it can span any width.
# ---------------------------------------------------------------------------
def toran(pid, h=58):
    return f"""<svg class="toran-svg" width="100%" height="{h}" aria-hidden="true" focusable="false">
<defs><pattern id="{pid}" width="72" height="{h}" patternUnits="userSpaceOnUse">
  <path d="M0,3 Q36,20 72,3" fill="none" stroke="#8B5A2B" stroke-width="1.6"/>
  <path d="M36,11 C29,22 30,34 36,45 C42,34 43,22 36,11 Z" fill="#4E8A5A"/>
  <path d="M36,13 L36,42" stroke="#2F6647" stroke-width=".9"/>
  <g><circle cx="0" cy="9" r="5.2" fill="#F2A51F"/><circle cx="0" cy="18.5" r="5.2" fill="#E8871B"/><circle cx="0" cy="28" r="5.2" fill="#F2A51F"/><circle cx="0" cy="35.5" r="2.4" fill="#B8452F"/></g>
  <g><circle cx="72" cy="9" r="5.2" fill="#F2A51F"/><circle cx="72" cy="18.5" r="5.2" fill="#E8871B"/><circle cx="72" cy="28" r="5.2" fill="#F2A51F"/><circle cx="72" cy="35.5" r="2.4" fill="#B8452F"/></g>
</pattern></defs>
<line x1="0" y1="2.5" x2="100%" y2="2.5" stroke="#8B5A2B" stroke-width="2"/>
<rect x="0" y="0" width="100%" height="{h}" fill="url(#{pid})"/>
</svg>"""

# Rajasthan map (base layers built by tools/rajmap.py)
RAJMAP = open(A + 'raj_map.svg').read()
RAJPLACES = open(A + 'raj_places.json').read()

sat_url = b64(A + 'india_sat.jpg', 'image/jpeg')
clouds = [b64(A + f'cloud{i}.webp', 'image/webp') for i in range(4)]
bank = b64(A + 'cloudbank.webp', 'image/webp')

html = open(T, encoding="utf-8").read()

import json as _json
def _extra():
    pa = _json.load(open(A + 'pdf_assets.json'))
    cm = _json.load(open(A + 'campus.json'))
    return {'__LOGO_MOE__': pa['logos']['moe'], '__LOGO_IITJ__': pa['logos']['iitj'], '__LOGO_YUVA__': pa['logos']['yuva'],
            '__LOGO_EBSB__': pa['logos']['ebsb'], '__GALLERY__': _json.dumps(pa['gallery']),
            '__CAMPUS_SVG__': cm['svg'], '__CAMPUS_PINS__': _json.dumps(cm['pins']), '__CAMPUS_VB__': ' '.join(str(v) for v in cm['vb']),
            '__CAMPUS_W__': str(cm['w']), '__CAMPUS_H__': str(cm['h'])}
rep = {
  '__SATURL__': sat_url, '__SAT__': sat_url,
  '__C0__': clouds[0], '__C1__': clouds[1], '__C2__': clouds[2], '__C3__': clouds[3], '__BANK__': bank,
  '__INDIA__': m['india'], '__SIK__': m['sik'], '__RAJ__': m['raj'], '__ARC__': ARC,
  '__MW__': str(m['w']), '__MH__': str(m['h']), '__MW2__': str(m['w'] + 40), '__MH2__': str(round(m['h'] + 40)),
  '__GX__': f'{gx:.1f}', '__GY__': f'{gy:.1f}', '__JX__': f'{jx:.1f}', '__JY__': f'{jy:.1f}',
  '__GLX__': f'{GLX:.1f}', '__GLY__': f'{GLY:.1f}', '__JLX__': f'{JLX:.1f}', '__JLY__': f'{JLY:.1f}',
  '__KM__': str(KM), '__TORAN1__': toran('toranP1'), '__TORAN2__': toran('toranP2', 50), '__RAJMAP__': RAJMAP, '__RAJPLACES__': RAJPLACES, '__SIKKIM_SVG__': SIKKIM_SVG, '__RAJ_SVG__': RAJ_SVG, '__PHOTOS__': open(A + 'photos.json').read(), **_extra(),
}
# labels: centre them over / under their pins
html = html.replace('id="lblG" x="__GLX__" y="__GLY__" text-anchor="end"', 'id="lblG" x="__GLX__" y="__GLY__" text-anchor="middle"')
html = html.replace('id="lblJ" x="__JLX__" y="__JLY__"', 'id="lblJ" x="__JLX__" y="__JLY__" text-anchor="middle"')
for k, v in rep.items():
    html = html.replace(k, v)

assert '__' not in ''.join(t for t in html.split('"') if t.startswith('__') and t.endswith('__')), 'unreplaced token'
leftover = [k for k in rep if k in html]
assert not leftover, leftover

open(OUT, 'w', encoding='utf-8').write(html)
print('written', OUT, round(len(html)/1024), 'KB', 'KM =', KM)
