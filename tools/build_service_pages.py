"""Generate the service landing pages (shared template, content below).

Run from the repo root:  python3 tools/build_service_pages.py
Content sources: Booksy service descriptions written by the salon, the
printed price list (09.2026) and the terms of service.
"""
import html
import json
import re

BASE = "https://slowheadspa.pl"
BOOKSY = "https://booksy.com/pl-pl/280278_slow-head-spa-opole_inni_12930_opole"
TODAY = "2026-10-04"

PROVIDER = {
    "@type": "HealthAndBeautyBusiness",
    "name": "Slow Head Spa",
    "url": BASE + "/",
    "telephone": "+48888773993",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "ul. Piastowska 2/2",
        "postalCode": "45-081",
        "addressLocality": "Opole",
        "addressCountry": "PL",
    },
}


def prices(rows):
    out = ['<div class="pricing__table service__prices">']
    for name, dur, price in rows:
        d = f'\n                                <p class="pricing__duration">{dur}</p>' if dur else ""
        out.append(f'''                        <div class="pricing__item">
                            <div class="pricing__info">
                                <p class="pricing__name">{name}</p>{d}
                            </div>
                            <div class="pricing__price">{price}</div>
                        </div>''')
    out.append("                    </div>")
    return "\n".join(out)


def faq_html(items):
    out = ['<section class="faq faq--article">', '                        <h2>Najczęstsze pytania</h2>']
    for q, a in items:
        out.append(f'''                        <details class="faq__item">
                            <summary>{q}</summary>
                            <p>{a}</p>
                        </details>''')
    out.append("                    </section>")
    return "\n".join(out)


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def card(href, img, tag, title, excerpt):
    return f'''                        <a href="{href}" class="blog-card">
                            <div class="blog-card__image">
                                <img src="{img}" alt="{title}" loading="lazy">
                            </div>
                            <div class="blog-card__content">
                                <span class="blog-card__tag">{tag}</span>
                                <h3 class="blog-card__title">{title}</h3>
                                <p class="blog-card__excerpt">{excerpt}</p>
                            </div>
                        </a>'''


CARDS = {
    "rytualy": ("/rytualy-head-spa", "/images/head-spa-rytual-wide.jpg", "Zabieg", "Rytuały head spa: Era, Jarga, Daro, Zargo, Istra",
                "Co zawiera każdy rytuał, ile trwa i ile kosztuje — porównanie w jednym miejscu."),
    "transbukalny": ("/masaz-transbukalny-opole", "/images/masaz-transbukalny.jpg", "Zabieg", "Masaż transbukalny w Opolu",
                     "Rozluźnienie żwaczy od wewnątrz policzków — ulga przy bruksizmie i napięciu żuchwy."),
    "glowface": ("/glow-face-opole", "/images/masaz-twarzy.jpg", "Zabieg", "Masaż Glow Face — Korugi i Kobido",
                 "Modelowanie owalu i natychmiastowe rozświetlenie skóry w 60-minutowym rytuale."),
    "dwoje": ("/head-spa-dla-dwojga", "/images/headspa5.jpeg", "Zabieg", "Head spa dla dwojga",
              "Wspólny rytuał dla dwóch osób i chwila przy ciepłym napoju — także jako prezent."),
    "czym": ("/blog/czym-jest-head-spa", "/images/headspa5.jpeg", "Przewodnik", "Czym jest Head Spa? Kompletny przewodnik",
             "Na czym polega zabieg head spa, jakie daje efekty i dlaczego warto go wypróbować."),
    "korugi": ("/blog/masaz-korugi-japonski-lifting", "/images/masaz-twarzy-wide.jpg", "Zabiegi", "Masaż Korugi — japoński lifting bez skalpela",
               "Japońska technika modelowania twarzy, która redukuje obrzęki i napięcie."),
    "voucher": ("/blog/voucher-head-spa-prezent", "/images/headspa3.jpeg", "Prezent", "Voucher na Head Spa — prezent, który zostaje w pamięci",
                "Pomysł na prezent w Opolu: relaks zamiast kolejnej rzeczy na półkę."),
}

PAGES = []

# ---------------------------------------------------------------- rytuały
PAGES.append(dict(
    slug="rytualy-head-spa",
    title="Rytuały Head Spa: Era, Jarga, Zargo, Istra | Slow Head Spa Opole",
    description="Porównaj rytuały head spa w Slow Head Spa Opole — od 75-minutowej Ery po 2,5-godzinną Istrę. Co zawiera każdy zabieg, ile trwa i ile kosztuje.",
    h1="Rytuały head spa w Opolu — Era, Jarga, Daro, Zargo i Istra",
    crumb="Rytuały head spa",
    service="Head spa", service_type="Head spa — masaż i pielęgnacja skóry głowy",
    image=("/images/head-spa-rytual-wide.jpg", 1200, 675, "Rytuał head spa z wodnym masażerem w Slow Head Spa Opole"),
    offers=[("Head Spa Era (1 h 15 min)", 200), ("Head Spa Jarga (1 h 30 min)", 300), ("Head Spa Daro (1 h 45 min)", 330),
            ("Head Spa Zargo (2 h)", 400), ("Head Spa Istra (2 h 30 min)", 500)],
    body=f'''<p>W Slow Head Spa w Opolu każdy rytuał <strong>head spa</strong> łączy relaksacyjny masaż skóry głowy, enzymatyczny peeling i indywidualnie dobraną pielęgnację włosów. Rytuały różnią się czasem trwania i liczbą etapów — od 75-minutowej Ery, idealnej na pierwszy raz, po 2,5-godzinną Istrę z masażem twarzy, sauną parową i parafiną na dłonie. Poniżej znajdziesz, co dokładnie zawiera każdy z nich.</p>

                    <p>Jeśli dopiero poznajesz ten zabieg, zacznij od przewodnika <a href="/blog/czym-jest-head-spa">Czym jest head spa?</a></p>

                    <h2>W każdym rytuale</h2>
                    <ul>
                        <li>relaksacyjny masaż skóry głowy dłońmi i specjalistycznymi masażerami,</li>
                        <li>enzymatyczny peeling skóry głowy,</li>
                        <li>mycie szamponem i odżywka dobrana do potrzeb Twoich włosów,</li>
                        <li>suszenie włosów.</li>
                    </ul>

                    <h2>Head Spa Era — 1 h 15 min, 200 zł</h2>
                    <p>Najkrótszy rytuał i dobry wybór na pierwszą wizytę. Skupia się na skórze głowy i pielęgnacji włosów: masaż dłońmi i masażerami, enzymatyczny peeling połączony z masażem, mycie i odżywienie włosów, suszenie.</p>

                    <h2>Head Spa Jarga — 1 h 30 min, 300 zł</h2>
                    <p>Wszystko, co w Erze, plus elementy, które rozluźniają całe ciało:</p>
                    <ul>
                        <li>aromaterapia sprzyjająca głębokiemu relaksowi,</li>
                        <li>masaż szyi i klatki piersiowej,</li>
                        <li>ciepłe ręczniczki z energetyzującą aromaterapią,</li>
                        <li>krótki masaż pleców w pozycji siedzącej,</li>
                        <li>nawilżający balsam do ust.</li>
                    </ul>

                    <h2>Head Spa Zargo — 2 h, 400 zł</h2>
                    <p>Jarga rozszerzona o pielęgnację twarzy i intensywną regenerację włosów:</p>
                    <ul>
                        <li>demakijaż twarzy,</li>
                        <li>liftingujący masaż twarzy i nawilżające płatki pod oczy,</li>
                        <li>sauna parowa z maską dobraną do kondycji włosów,</li>
                        <li>odżywczo-nawilżający balsam do ust.</li>
                    </ul>

                    <h2>Head Spa Istra — 2 h 30 min, 500 zł</h2>
                    <p>Najbardziej kompleksowy rytuał w ofercie — wszystko, co w Zargo, uzupełnione o maseczkę nawilżającą na twarz i zabieg parafinowy na dłonie. Idealny na wyjątkową okazję albo jako prezent.</p>

                    <h2>Head Spa Daro — 1 h 45 min, 330 zł — rytuał dla panów</h2>
                    <p>Rytuał zaprojektowany z myślą o mężczyznach:</p>
                    <ul>
                        <li>aromaterapia i relaksacyjny masaż skóry głowy dłońmi oraz masażerami,</li>
                        <li>masaż szyi, klatki piersiowej i twarzy,</li>
                        <li>maseczka lub nawilżające płatki pod oczy,</li>
                        <li>peeling skóry głowy, mycie włosów i maska w formie pianki — przy zaroście nakładana również na brodę,</li>
                        <li>regenerująca maska na włosy z wykorzystaniem sauny parowej,</li>
                        <li>suszenie włosów.</li>
                    </ul>

                    <blockquote class="article__highlight">
                        <p>Czas trwania może się nieznacznie różnić w zależności od długości i gęstości włosów — wynika to z czasu potrzebnego na ich wysuszenie.</p>
                    </blockquote>

                    <h2>Który rytuał wybrać?</h2>
                    <ul>
                        <li><strong>Pierwszy raz</strong> — Era albo Jarga.</li>
                        <li><strong>Napięcie i stres</strong> — Jarga, z masażem szyi i krótkim masażem pleców.</li>
                        <li><strong>Pełny reset głowy i twarzy</strong> — Zargo.</li>
                        <li><strong>Wyjątkowa okazja lub prezent</strong> — Istra.</li>
                        <li><strong>Dla niego</strong> — Daro.</li>
                        <li><strong>We dwoje</strong> — <a href="/head-spa-dla-dwojga">head spa dla dwojga</a>.</li>
                    </ul>

                    <h2>Cennik rytuałów head spa</h2>
                    {prices([("Head Spa Era", "1h 15min", "200 zł"), ("Head Spa Jarga", "1h 30min", "300 zł"), ("Head Spa Daro", "1h 45min · rytuał dla panów", "330 zł"), ("Head Spa Zargo", "2h", "400 zł"), ("Head Spa Istra", "2h 30min", "500 zł")])}

                    <h2>Przedłuż swój relaks</h2>
                    <p>Do każdego rytuału możesz dobrać dodatek. Ampułka trychologiczna pomaga zapobiegać wypadaniu włosów — więcej o tym piszę w artykule <a href="/blog/head-spa-wypadanie-wlosow">head spa a wypadanie włosów</a>.</p>
                    {prices([("Maseczka Hydrojelly", "20min", "50 zł"), ("Spa dla oczu", "20min", "70 zł"), ("Masaż twarzy", "20min", "70 zł"), ("Masaż głowy", "15min", "40 zł"), ("Parafina na dłonie", "10min", "30 zł"), ("Ampułka trychologiczna", "Zapobiega wypadaniu włosów", "30 zł")])}''',
    faq=[
        ("Który rytuał head spa wybrać na pierwszą wizytę?", "Najczęściej polecam Erę (1 h 15 min) albo Jargę (1 h 30 min). Era skupia się na skórze głowy i włosach, a Jarga dodaje aromaterapię, masaż szyi i krótki masaż pleców."),
        ("Czy przed head spa trzeba umyć włosy?", "Nie. Mycie, pielęgnacja i suszenie włosów są częścią każdego rytuału. Wystarczy, że przyjdziesz kilka minut wcześniej — przed pierwszą wizytą wypełniamy krótką kartę klienta."),
        ("Czy head spa pomaga przy wypadaniu włosów?", "Masaż i peeling poprawiają kondycję skóry głowy, a do rytuału możesz dodać ampułkę trychologiczną, która pomaga zapobiegać wypadaniu włosów."),
    ],
    cta=("Zarezerwuj rytuał head spa", "Wybierz rytuał i termin w Booksy. Gabinet znajdziesz przy ul. Piastowskiej 2/2 w Opolu."),
    related=["dwoje", "czym"],
))

# ---------------------------------------------------------------- transbukalny
PAGES.append(dict(
    slug="masaz-transbukalny-opole",
    title="Masaż transbukalny Opole — ulga przy bruksizmie | Slow Head Spa",
    description="Masaż transbukalny w Slow Head Spa Opole: praca na mięśniach twarzy z zewnątrz i od wewnątrz policzków. Rozluźnia żwacze, pomaga przy bruksizmie. 45 min, 180 zł.",
    h1="Masaż transbukalny w Opolu — rozluźnienie żuchwy i ulga przy bruksizmie",
    crumb="Masaż transbukalny",
    service="Masaż transbukalny", service_type="Masaż twarzy",
    image=("/images/masaz-transbukalny.jpg", 1200, 900, "Masaż transbukalny w Slow Head Spa Opole"),
    offers=[("Masaż transbukalny (45 min)", 180), ("Masaż Glow Face + masaż transbukalny (1 h 30 min)", 390)],
    body=f'''<p>Zaciskasz zęby we śnie, budzisz się z napiętą żuchwą, a twarz wydaje się ciągle spięta? <strong>Masaż transbukalny</strong> to specjalistyczny masaż wykonywany zarówno na zewnątrz, jak i wewnątrz policzków. Dzięki temu dociera do mięśni, do których zwykły masaż twarzy nie ma dostępu — przede wszystkim do żwaczy, które przy bruksizmie pracują ponad siły.</p>

                    <h2>Na czym polega masaż transbukalny?</h2>
                    <p>Nazwa pochodzi od łacińskiego <em>bucca</em>, czyli policzek. Część masażu wykonuję klasycznie, od zewnątrz twarzy, a część — w jednorazowych rękawiczkach — od wewnątrz jamy ustnej, wzdłuż mięśni policzków i żuchwy. Siłę nacisku dopasowuję na bieżąco, a w każdej chwili możesz dać znać, że wolisz delikatniej. Zabieg trwa 45 minut.</p>

                    <h2>Dla kogo jest masaż transbukalny?</h2>
                    <ul>
                        <li>dla osób z bruksizmem — zaciskających lub zgrzytających zębami, szczególnie w nocy,</li>
                        <li>dla osób, które czują napięcie i ból w okolicy żuchwy, policzków i skroni,</li>
                        <li>dla tych, którzy w stresie odruchowo zaciskają szczęki,</li>
                        <li>dla szukających naturalnego liftingu — rozluźnione mięśnie to gładsze rysy twarzy.</li>
                    </ul>

                    <h2>Efekty masażu transbukalnego</h2>
                    <ul>
                        <li>rozluźnienie mięśni żwaczy i napięć w obrębie twarzy,</li>
                        <li>ulga w bólach wynikających z zaciskania szczęk,</li>
                        <li>wygładzenie rysów i efekt naturalnego liftingu,</li>
                        <li>głębokie odprężenie.</li>
                    </ul>

                    <blockquote class="article__highlight">
                        <p>Masaż transbukalny nie zastępuje leczenia stomatologicznego. Jeśli masz zdiagnozowany bruksizm, najlepsze efekty daje połączenie masażu z opieką stomatologa — na przykład z szyną relaksacyjną.</p>
                    </blockquote>

                    <h2>Przeciwwskazania</h2>
                    <p>Typowe przeciwwskazania to m.in. stany zapalne i rany w jamie ustnej, aktywna opryszczka, okres tuż po zabiegach stomatologicznych lub ekstrakcji zęba oraz świeże zabiegi medycyny estetycznej w obrębie twarzy. Przed pierwszym zabiegiem wypełniasz kartę klienta, a w razie wątpliwości warto skonsultować się z lekarzem lub stomatologiem.</p>

                    <h2>Masaż transbukalny w duecie z Glow Face</h2>
                    <p>Najmocniejszy efekt daje połączenie obu zabiegów: <a href="/glow-face-opole">masaż Glow Face</a> modeluje owal i rozświetla skórę, a masaż transbukalny rozluźnia mięśnie od wewnątrz. Razem trwają 1 h 30 min i kosztują 390 zł — o 40 zł mniej niż osobno.</p>

                    <h2>Cennik</h2>
                    {prices([("Masaż transbukalny", "45min", "180 zł"), ("Glow Face + masaż transbukalny", "1h 30min · oszczędzasz 40 zł", "390 zł")])}''',
    faq=[
        ("Czy masaż transbukalny boli?", "Bywa intensywny, zwłaszcza przy mocno napiętych żwaczach, ale nie powinien sprawiać bólu. Siłę nacisku dopasowuję do Ciebie na bieżąco."),
        ("Czy masaż transbukalny jest higieniczny?", "Tak — część wewnątrz jamy ustnej wykonuję w jednorazowych rękawiczkach."),
        ("Ile trwa i ile kosztuje masaż transbukalny w Opolu?", "Zabieg trwa 45 minut i kosztuje 180 zł. W połączeniu z masażem Glow Face (1 h 30 min) — 390 zł."),
    ],
    cta=("Zarezerwuj masaż transbukalny", "Umów wizytę w Booksy albo zadzwoń: 888 773 993. Gabinet: ul. Piastowska 2/2, Opole."),
    related=["glowface", "korugi"],
))

# ---------------------------------------------------------------- glow face
PAGES.append(dict(
    slug="glow-face-opole",
    title="Masaż Glow Face Opole — Korugi i Kobido | Slow Head Spa",
    description="Glow Face w Slow Head Spa Opole łączy głębokie techniki Korugi z dynamicznym Kobido. Modeluje owal, wygładza rysy i rozświetla skórę. 60 min, 250 zł.",
    h1="Masaż Glow Face w Opolu — Korugi i Kobido w jednym rytuale",
    crumb="Masaż Glow Face",
    service="Masaż Glow Face", service_type="Masaż twarzy",
    image=("/images/masaz-twarzy.jpg", 1200, 900, "Masaż twarzy Glow Face w Slow Head Spa Opole"),
    offers=[("Masaż Glow Face (1 h)", 250), ("Masaż Glow Face + masaż transbukalny (1 h 30 min)", 390),
            ("Masaż Korugi (1 h 30 min)", 230), ("Pakiet Korugi — 4 zabiegi", 800)],
    body=f'''<p><strong>Glow Face</strong> to masaż twarzy, który łączy precyzyjne, głębokie techniki Korugi z dynamicznymi ruchami Kobido. Modeluje owal, wygładza rysy, poprawia napięcie skóry i przywraca jej naturalny blask. Efekt? Natychmiastowe odświeżenie, rozświetlenie i widoczne odmłodzenie twarzy — bez igieł i bez okresu rekonwalescencji.</p>

                    <h2>Korugi i Kobido — dwie techniki, jeden zabieg</h2>
                    <p><strong>Korugi</strong> to intensywny masaż liftingujący, który łączy głęboki ucisk, pracę na kościach twarzy i drenaż limfatyczny. Odpowiada za modelowanie owalu i redukcję opuchlizny.</p>
                    <p><strong>Kobido</strong> działa na głębokie warstwy skóry i mięśni. Szybkie, precyzyjne ruchy poprawiają krążenie, dotleniają tkanki i stymulują produkcję kolagenu, dzięki czemu skóra staje się jędrniejsza i bardziej elastyczna.</p>
                    <p>W Glow Face łączę obie techniki w jednym, 60-minutowym rytuale.</p>

                    <h2>Efekty masażu Glow Face</h2>
                    <ul>
                        <li>wymodelowany owal i wygładzone rysy,</li>
                        <li>lepsze napięcie i elastyczność skóry,</li>
                        <li>rozświetlona, wypoczęta cera,</li>
                        <li>mniej napięć w okolicy twarzy, szyi i karku,</li>
                        <li>głębokie odprężenie.</li>
                    </ul>

                    <h2>Dla kogo jest Glow Face?</h2>
                    <ul>
                        <li>jeśli chcesz szybko odświeżyć twarz przed ważnym wydarzeniem,</li>
                        <li>jeśli zauważasz utratę jędrności i pierwsze zmarszczki,</li>
                        <li>jeśli szukasz naturalnej alternatywy dla zabiegów medycyny estetycznej,</li>
                        <li>jeśli nosisz napięcie w mięśniach twarzy.</li>
                    </ul>

                    <h2>Glow Face czy Korugi?</h2>
                    <p><a href="/blog/masaz-korugi-japonski-lifting">Masaż Korugi</a> (1 h 30 min, 230 zł) to dłuższa, intensywna praca liftingująca — najlepiej sprawdza się w serii, dlatego w ofercie jest też pakiet 4 zabiegów za 800 zł. Glow Face (1 h, 250 zł) łączy Korugi z Kobido i daje efekt rozświetlenia od razu. Jeśli zaciskasz szczęki, wybierz Glow Face w duecie z <a href="/masaz-transbukalny-opole">masażem transbukalnym</a>.</p>

                    <h2>Cennik masaży twarzy</h2>
                    {prices([("Masaż Glow Face", "1h", "250 zł"), ("Glow Face + masaż transbukalny", "1h 30min · oszczędzasz 40 zł", "390 zł"), ("Masaż Korugi", "1h 30min", "230 zł"), ("Pakiet Korugi — 4 zabiegi", "4 × 1h 30min · oszczędzasz 120 zł", "800 zł")])}''',
    faq=[
        ("Czym Glow Face różni się od masażu Korugi?", "Korugi to głęboka praca na kościach i mięśniach twarzy połączona z drenażem limfatycznym. Glow Face łączy techniki Korugi z dynamicznym Kobido, trwa krócej (60 minut) i daje natychmiastowy efekt rozświetlenia."),
        ("Kiedy widać efekty masażu Glow Face?", "Odświeżenie i rozświetlenie skóry widać od razu po zabiegu."),
        ("Ile kosztuje masaż Glow Face w Opolu?", "250 zł za 60 minut. W połączeniu z masażem transbukalnym — 390 zł za 1 h 30 min."),
    ],
    cta=("Zarezerwuj masaż Glow Face", "Wybierz termin w Booksy — gabinet znajdziesz przy ul. Piastowskiej 2/2 w Opolu."),
    related=["transbukalny", "korugi"],
))

# ---------------------------------------------------------------- dla dwojga
PAGES.append(dict(
    slug="head-spa-dla-dwojga",
    title="Head Spa dla dwojga w Opolu — prezent dla pary | Slow Head Spa",
    description="Rytuał head spa dla dwóch osób w Slow Head Spa Opole — Jarga, Zargo lub Istra, a po zabiegu wspólna chwila przy ciepłym napoju. Od 650 zł za dwie osoby.",
    h1="Head spa dla dwojga w Opolu — wspólny rytuał relaksu",
    crumb="Head spa dla dwojga",
    service="Head spa dla dwojga", service_type="Head spa dla dwóch osób",
    image=("/images/headspa5.jpeg", 2340, 1560, "Head spa dla dwojga w Slow Head Spa Opole"),
    offers=[("Head Spa Jarga dla dwojga (1 h 45 min, 2 osoby)", 650), ("Head Spa Zargo dla dwojga (2 h 15 min, 2 osoby)", 850),
            ("Head Spa Istra dla dwojga (2 h 45 min, 2 osoby)", 1050)],
    body=f'''<p>Chwila relaksu, którą możecie przeżyć razem. <strong>Head spa dla dwojga</strong> to rytuał dla dwóch osób — idealny na prezent, wspólne świętowanie, wieczór panieński, urodziny albo po prostu czas tylko dla Was. A po zabiegu relaks się nie kończy: czeka na Was wspólna chwila przy wcześniej wybranym ciepłym napoju — moment na rozmowę i spokojne domknięcie rytuału.</p>

                    <h2>Trzy rytuały do wyboru</h2>

                    <h3>Jarga dla dwojga — 1 h 45 min, 650 zł</h3>
                    <ul>
                        <li>aromaterapia sprzyjająca głębokiemu relaksowi,</li>
                        <li>relaksacyjny masaż skóry głowy dłońmi i specjalistycznymi masażerami,</li>
                        <li>enzymatyczny peeling skóry głowy,</li>
                        <li>masaż szyi i klatki piersiowej,</li>
                        <li>mycie szamponem i indywidualnie dobrana odżywka,</li>
                        <li>ciepłe ręczniczki z aromaterapią i krótki masaż pleców w pozycji siedzącej,</li>
                        <li>suszenie włosów i nawilżający balsam do ust.</li>
                    </ul>

                    <h3>Zargo dla dwojga — 2 h 15 min, 850 zł</h3>
                    <p>Wszystko z Jargi oraz demakijaż i liftingujący masaż twarzy, nawilżające płatki pod oczy, sauna parowa z maską dopasowaną do kondycji włosów i odżywczo-nawilżający balsam do ust.</p>

                    <h3>Istra dla dwojga — 2 h 45 min, 1050 zł</h3>
                    <p>Wszystko z Zargo oraz maska Hydrojelly na twarz i parafina na zimno na dłonie — najbardziej kompleksowa wersja wspólnego relaksu.</p>

                    <p>Ceny dotyczą dwóch osób. Ze względu na długość i gęstość włosów czas zabiegu może się nieco różnić. Szczegóły pojedynczych rytuałów znajdziesz na stronie <a href="/rytualy-head-spa">rytuały head spa</a>.</p>

                    <h2>Na jaką okazję?</h2>
                    <ul>
                        <li>rocznica, walentynki albo randka inna niż wszystkie,</li>
                        <li>urodziny i imieniny,</li>
                        <li>wieczór panieński,</li>
                        <li>prezent dla mamy i córki albo dla przyjaciółek,</li>
                        <li>po prostu — czas tylko dla Was.</li>
                    </ul>

                    <h2>Cennik head spa dla dwojga</h2>
                    {prices([("Head Spa Jarga dla dwojga", "1h 45min · cena za 2 osoby", "650 zł"), ("Head Spa Zargo dla dwojga", "2h 15min · cena za 2 osoby", "850 zł"), ("Head Spa Istra dla dwojga", "2h 45min · cena za 2 osoby", "1050 zł")])}

                    <h2>Head spa dla dwojga na prezent</h2>
                    <p>Sprzedaż voucherów przez stronę ruszy wkrótce — szczegóły znajdziesz w <a href="/#voucher">sekcji voucherów</a>, a o starcie damy znać na <a href="https://www.instagram.com/headspa_opole" target="_blank" rel="noopener noreferrer">Instagramie</a>.</p>''',
    faq=[
        ("Ile kosztuje head spa dla dwojga w Opolu?", "Od 650 zł za dwie osoby (Jarga, 1 h 45 min). Zargo dla dwojga kosztuje 850 zł, a Istra dla dwojga — 1050 zł."),
        ("Co jest po zabiegu?", "Po rytuale czeka na Was wspólny czas przy wcześniej wybranym ciepłym napoju — moment na rozmowę i spokojne domknięcie wizyty."),
        ("Jak zarezerwować head spa dla dwojga?", "Najwygodniej przez Booksy albo telefonicznie: 888 773 993."),
    ],
    cta=("Zarezerwujcie wspólny rytuał", "Wybierzcie termin w Booksy albo zadzwońcie: 888 773 993. Gabinet: ul. Piastowska 2/2, Opole."),
    related=["rytualy", "voucher"],
))


NAV = f'''    <nav class="nav nav--scrolled" id="nav">
        <div class="nav__container">
            <a href="/" class="nav__logo">Slow Head Spa</a>
            <button class="nav__toggle" id="navToggle" aria-label="Menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <ul class="nav__menu" id="navMenu">
                <li><a href="/#o-mnie" class="nav__link">O mnie</a></li>
                <li><a href="/#uslugi" class="nav__link">Usługi</a></li>
                <li><a href="/#cennik" class="nav__link">Cennik</a></li>
                <li><a href="/#voucher" class="nav__link">Voucher</a></li>
                <li><a href="/#kontakt" class="nav__link">Kontakt</a></li>
                <li><a href="/blog/" class="nav__link">Blog</a></li>
                <li><a href="{BOOKSY}" target="_blank" rel="noopener noreferrer" class="nav__link nav__link--cta">Zarezerwuj</a></li>
            </ul>
        </div>
    </nav>'''

FOOTER = '''    <footer class="footer">
        <div class="container">
            <div class="footer__content">
                <div class="footer__brand">
                    <span class="footer__logo">Slow Head Spa</span>
                    <p>Przestrzeń relaksu i profesjonalnej pielęgnacji w sercu Opola.</p>
                </div>
                <div class="footer__links">
                    <a href="/#o-mnie">O mnie</a>
                    <a href="/#uslugi">Usługi</a>
                    <a href="/#cennik">Cennik</a>
                    <a href="/#voucher">Voucher</a>
                    <a href="/#kontakt">Kontakt</a>
                    <a href="/blog/">Blog</a>
                </div>
            </div>
            <div class="footer__bottom">
                <p>&copy; 2025–2026 Slow Head Spa Opole. Wszystkie prawa zastrzeżone.</p>
                <div class="footer__legal-links">
                    <a href="/polityka-prywatnosci">Polityka prywatności</a>
                    <a href="/regulamin">Regulamin</a>
                </div>
            </div>
            <div class="footer__credit">
                <p>Forged by <a href="https://cyberdemigods.com" target="_blank" rel="noopener noreferrer"><span style="font-family:var(--font-heading);font-size:0.875rem;letter-spacing:0.05em;text-transform:none">CyberDemigods</span></a></p>
            </div>
        </div>
    </footer>'''


def ld(obj):
    body = json.dumps(obj, ensure_ascii=False, indent=4)
    return "    <script type=\"application/ld+json\">\n" + "\n".join("    " + line for line in body.splitlines()) + "\n    </script>"


def render(p):
    url = f"{BASE}/{p['slug']}"
    img, iw, ih, alt = p["image"]
    service = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": p["service"],
        "serviceType": p["service_type"],
        "description": p["description"],
        "url": url,
        "image": BASE + img,
        "areaServed": {"@type": "City", "name": "Opole"},
        "provider": PROVIDER,
        "offers": [{"@type": "Offer", "name": n, "price": str(v), "priceCurrency": "PLN"} for n, v in p["offers"]],
    }
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Strona główna", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Zabiegi", "item": BASE + "/#uslugi"},
            {"@type": "ListItem", "position": 3, "name": p["crumb"]},
        ],
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in p["faq"]],
    }
    related = "\n\n".join(card(*CARDS[k]) for k in p["related"])
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{p['description']}">
    <title>{p['title']}</title>

    <meta property="og:type" content="website">
    <meta property="og:title" content="{p['h1']}">
    <meta property="og:description" content="{p['description']}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{BASE}{img}">
    <meta property="og:locale" content="pl_PL">
    <meta name="theme-color" content="#3D3433">

    <link rel="canonical" href="{url}">
    <link rel="icon" href="/favicon.ico" sizes="48x48">
    <link rel="icon" href="/favicon-96x96.png" type="image/png" sizes="96x96">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="manifest" href="/site.webmanifest">

    <link rel="stylesheet" href="/css/fonts.css">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="stylesheet" href="/css/blog.css">

{ld(service)}

{ld(crumbs)}

{ld(faq)}
</head>
<body>
{NAV}

    <main>
        <article class="article">
            <div class="article__container">

                <nav class="article__breadcrumb" aria-label="Breadcrumb">
                    <a href="/">Strona główna</a> / <a href="/#uslugi">Zabiegi</a> / {p['crumb']}
                </nav>

                <header class="article__header">
                    <span class="article__tag">Zabieg</span>
                    <h1 class="article__title">{p['h1']}</h1>
                    <p class="article__meta">Slow Head Spa · ul. Piastowska 2/2, Opole</p>
                </header>

                <div class="article__hero-image">
                    <img src="{img}" alt="{alt}" width="{iw}" height="{ih}">
                </div>

                <div class="article__content">

                    {p['body']}

                    {faq_html(p['faq'])}

                    <div class="article__cta">
                        <h3>{p['cta'][0]}</h3>
                        <p>{p['cta'][1]}</p>
                        <a href="{BOOKSY}" target="_blank" rel="noopener noreferrer" class="btn">Zarezerwuj wizytę</a>
                    </div>

                </div>

                <aside class="article__related">
                    <h2>Zobacz również</h2>
                    <div class="article__related-grid">

{related}

                    </div>
                </aside>

            </div>
        </article>
    </main>

{FOOTER}

    <script src="/js/main.js"></script>
</body>
</html>
'''


if __name__ == "__main__":
    for page in PAGES:
        with open(f"{page['slug']}.html", "w", encoding="utf-8") as f:
            f.write(render(page))
        print("wrote", page["slug"] + ".html")
