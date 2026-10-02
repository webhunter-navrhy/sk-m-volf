"""Zostaví index.html + style.css s cache bustingom (?v=hash). Obsah je z m-volf.sk (podklady/)."""
import hashlib, json
from pathlib import Path
D = Path(__file__).parent

# činnosti presne podľa ich stránky Činnosti; popis, fotka (alebo None), typ do formulára
CINNOSTI = [
    ('Kompletné stavby na kľúč', 'Rodinný dom od základov až po odovzdanie, pripravený na bývanie.', 's-kluc', 'Stavba na kľúč'),
    ('Kompletná stavebná činnosť', 'Rodinné domy aj menšie priemyselné objekty, celá stavba v jedných rukách.', 's-stav', 'Stavba na kľúč'),
    ('Uskutočňovanie stavieb a ich zmien', 'Nové stavby aj zmeny tých existujúcich: prístavby, nadstavby, stavebné úpravy.', 's-zmeny', 'Prístavba / zmena stavby'),
    ('Dostavby rozostavaných realizácií', 'Stavba sa zastavila? Prevezmeme ju a dotiahneme do konca.', 's-dostavby', 'Dostavba'),
    ('Rekonštrukcie', 'Od drobných úprav až po rekonštrukciu celého domu.', 's-rek', 'Rekonštrukcia'),
    ('Renovácie', 'Nový vzhľad interiéru aj exteriéru, napríklad kúpeľne.', 's-ren', 'Rekonštrukcia'),
    ('Čiastkové stavebné práce', 'Netreba celú stavbu? Urobíme len tú časť, ktorú potrebujete.', 's-ciast', 'Čiastkové práce'),
    ('Strojové omietky', 'Omietky nanášané strojom.', 's-omietky', 'Omietky / potery'),
    ('Potery', 'Podlahové potery.', 's-potery', 'Omietky / potery'),
    ('Projektové poradenstvo', 'Poradíme už vo fáze projektu.', None, 'Poradenstvo'),
    ('Poradenstvo', 'Pri výbere riešenia aj materiálov.', None, 'Poradenstvo'),
    ('Dovoz materiálu', 'Materiál na stavbu Vám dovezieme.', 's-dovoz', 'Iné'),
]
# stavba v piatich záberoch – fotky f1..f5 z ich stavieb
KROKY = [
    ('Murivo', 'Hrubá stavba rastie rad za radom. Základ, na ktorom stojí všetko ďalšie.'),
    ('Krov', 'Na hotové murivo prichádza krov. Dom dostáva svoj tvar.'),
    ('Strecha', 'Strecha je hore a stavba je pod ochranou pred počasím.'),
    ('Zateplenie a fasáda', 'Lešenie, zateplenie a fasáda. Teraz sa rozhoduje, ako bude dom pôsobiť.'),
    ('Na kľúč', 'Hotovo. Dom je pripravený na bývanie a záhrada môže rásť.'),
]
TYPY = ['Stavba na kľúč', 'Dostavba', 'Rekonštrukcia', 'Prístavba / zmena stavby', 'Čiastkové práce', 'Omietky / potery', 'Poradenstvo', 'Iné']

marquee = ''.join(f'<span>{c[0]}</span><i></i>' for c in CINNOSTI) * 2

cinnosti = '\n'.join(
    f'''      <li class="row rv"{f' data-img="img/{img}.jpg"' if img else ''}>
        <span class="row__n">{i:02d}</span>
        <h3>{n}</h3>
        <p>{p}</p>
        {f'<img class="row__img" src="img/{img}.jpg" alt="" loading="lazy">' if img else ''}
        <a href="#kontakt" data-typ="{t}" class="row__a" aria-label="{n} – dopyt"><span aria-hidden="true">→</span></a>
      </li>''' for i, (n, p, img, t) in enumerate(CINNOSTI, 1))

zabery = ''.join(f'<img src="img/f{i}.jpg" alt="{n} – stavba M-VOLF" data-z="{i}" loading="lazy" width="1200" height="1600">' for i, (n, _) in enumerate(KROKY, 1))
kroky = '\n'.join(
    f'''        <li class="step" data-step="{i}"><img class="step__img" src="img/f{i}.jpg" alt="" loading="lazy"><span class="step__n">{i:02d}</span><h3>{n}</h3><p>{p}</p></li>'''
    for i, (n, p) in enumerate(KROKY, 1))

chip = lambda nm, v: f'<label class="chip"><input type="radio" name="{nm}" value="{v}"><span>{v}</span></label>'
typy = ''.join(chip('typ', t) for t in TYPY)

g = json.load(open(D / 'galeria.json'))
galeria = '\n'.join(
    f'      <figure class="gi rv" data-full="img/g-{x["n"]}.jpg"><img src="img/t-{x["n"]}.jpg" alt="{x["popis"]} – realizácia M-VOLF" loading="lazy" width="{x["wh"][0]}" height="{x["wh"][1]}"><figcaption>{x["popis"]}</figcaption></figure>'
    for x in g)

css = (D / 'fonts/fonts.css').read_text() + '\n' + (D / 'style.src.css').read_text()
(D / 'style.css').write_text(css)
h = lambda b: hashlib.md5(b).hexdigest()[:8]
html = (D / 'src.html').read_text()
for k, v in dict(marquee=marquee, cinnosti=cinnosti, zabery=zabery, kroky=kroky, typy=typy, galeria=galeria).items():
    html = html.replace('{{' + k + '}}', v)
html = html.replace('{{css}}', h(css.encode())).replace('{{js}}', h((D / 'main.js').read_bytes()))
assert '{{' not in html
(D / 'index.html').write_text(html)
(D / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
print('ok', len(g), 'fotiek v galérii')
