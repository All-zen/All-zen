"""Gera o banner "vault vivo" e o fluxo da busca do README do perfil.

Cada partícula da constelação é uma nota indexada (699 em 04/11/2026), agrupada pela seção do vault.
As três perguntas e os escores vêm de buscas reais no vault-vector; os caminhos aparecem resumidos.
Uso: python3 gen_vivo.py <pasta-de-saida>
"""
import math, random, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from azt import text, width

OUT = pathlib.Path(sys.argv[1])
VOID, WHITE, ASH, SILVER = '#000000', '#ffffff', '#9a9a9a', '#bdbdbd'
IRIS, SAFFRON, VERDANT = '#8052ff', '#ffb829', '#15846e'
LILAC, MAGENTA, BLUE, TEAL = '#a98bff', '#ff5fd2', '#4d7cff', '#2fbf9f'
TR_D, TR_L = -0.04, 0.025


def n(v):
    s = f'{v:.1f}'.rstrip('0').rstrip('.')
    return '0' if s == '-0' else s


def tri(cx, cy, r, rot):
    p = [(cx + r * math.cos(rot + k * 2 * math.pi / 3), cy + r * math.sin(rot + k * 2 * math.pi / 3)) for k in range(3)]
    return f'M{n(p[0][0])} {n(p[0][1])}L{n(p[1][0])} {n(p[1][1])}L{n(p[2][0])} {n(p[2][1])}Z'


def tri_path(items, color, filled=False, sw=1.1, extra=''):
    d = ''.join(tri(*it) for it in items)
    if filled:
        return f'<path d="{d}" fill="{color}"{extra}/>'
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"{extra}/>'


def label(s, x, y, fill=SAFFRON, size=13, anchor='start'):
    return text(s, 600, size, x, y, fill, TR_L, anchor=anchor, upper=True)[0]


def svg(w, h, title, style, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<title>{title}</title><style>{style}</style>'
            f'<rect width="{w}" height="{h}" rx="24" fill="{VOID}"/>{body}</svg>')


# ------------------------------------------------------------------ banner
SECTIONS = [  # (notas, centro, espalhamento, cores) — as 8 seções reais do vault, numa massa só
    (338, (990, 300), (92, 78), [IRIS, LILAC, IRIS, BLUE, MAGENTA]),
    (148, (858, 212), (56, 46), [BLUE, TEAL, LILAC, BLUE]),
    (93, (1108, 196), (44, 38), [SAFFRON, SAFFRON, LILAC, MAGENTA]),
    (62, (1112, 392), (40, 32), [MAGENTA, LILAC, SAFFRON]),
    (45, (872, 396), (36, 28), [LILAC, TEAL]),
    (6, (985, 150), (14, 10), [LILAC]),
    (4, (790, 300), (8, 8), [TEAL]),
    (3, (1186, 300), (6, 6), [ASH]),
]
SCENES = [
    dict(kind='search', cap='Busca híbrida', q='reranker juiz local faixa média', sec=0, at=(1000, 270),
         tag='reranker', title='Reranker: o juiz local da faixa média', fill=WHITE,
         meta='semântico #1 (0,653) + literal #1 · os dois lados concordam',
         extra='com o juiz, 5 de 8 perguntas legítimas sobem para confiança alta'),
    dict(kind='weak', cap='Sinalização de incerteza', q='qual a receita de pão de queijo', sec=0, at=(1030, 330),
         tag='confiança baixa', title='Confiança baixa · similaridade 0,483', fill=SAFFRON,
         meta='“receita” existe no vault, mas como fórmula industrial',
         extra='trate como “o vault não responde isso”'),
    dict(kind='write', cap='Escrita com histórico', q='vault_append · registrar a decisão de hoje', sec=0, at=(948, 236),
         tag='nota atualizada', title='Sete ferramentas de escrita pelo MCP', fill=WHITE,
         meta='editar · acrescentar · criar · mover · apagar · listar · reindexar',
         extra='a versão anterior vai para _historico/ antes de gravar'),
    dict(kind='describe', cap='Descrição automática do vault', q='vault_list_sections', sec=None, at=None,
         tag='', title='8 seções · 699 notas · 6.080 trechos', fill=WHITE,
         meta='o servidor lê o próprio índice e descreve a estrutura',
         extra='o modelo navega um vault que nunca viu, sem instrução escrita'),
]
SLOT = 6
CYCLE = SLOT * len(SCENES)


def pct(t):
    return f'{t / CYCLE * 100:.2f}%'


def banner():
    rng = random.Random(699)
    W, H = 1280, 560
    pts = []
    for si, (cnt, (cx, cy), (sx, sy), cols) in enumerate(SECTIONS):
        k = 0
        while k < cnt:
            x, y = rng.gauss(cx, sx), rng.gauss(cy, sy)
            if not (650 < x < W - 26 and 26 < y < H - 30):
                continue
            pts.append((x, y, rng.uniform(2.0, 3.8), rng.uniform(0, 2 * math.pi), rng.choice(cols), si)); k += 1
    assert len(pts) == 699

    body = [tri_path([(69, 66, 6.5, -math.pi / 2)], IRIS, filled=True),
            label('AZ Sistemas · Bento Gonçalves, RS', 84, 71, ASH, 13),
            text('Allan Zeni', 'display', 112, 56, 188, WHITE, TR_D)[0],
            label('Infraestrutura de TI · Python · IA aplicada', 64, 234, SAFFRON, 13)]
    for i, line in enumerate(['Criei o vault-vector para a IA trabalhar com a minha',
                              'memória: 699 notas, indexadas no meu computador e',
                              'consultadas ou atualizadas pelo MCP.']):
        body.append(text(line, 300, 18, 64, 270 + i * 26, SILVER)[0])
    body.append(label('Buscas reais no meu vault · 04/11/2026 · cada triângulo é uma nota', 64, 530, ASH, 10))

    mesh = []
    for i, a in enumerate(pts):
        near2 = sorted(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2, j) for j, b in enumerate(pts) if j != i)[:2]
        for d2, j in near2:
            if j > i and d2 < 30 ** 2:
                mesh.append(f'M{n(a[0])} {n(a[1])}L{n(pts[j][0])} {n(pts[j][1])}')
    body.append(f'<path d="{"".join(mesh)}" stroke="{LILAC}" stroke-width=".6" opacity=".16"/>')
    groups = {}
    for (x, y, r, rot, c, si) in pts:
        groups.setdefault((rng.randrange(4), c), []).append((x, y, r, rot))
    body.append('<g opacity=".88">' + ''.join(tri_path(v, c, sw=1, extra=f' class="tw t{g}"')
                                             for (g, c), v in sorted(groups.items())) + '</g>')

    S = SLOT
    style = [
        '.tw{animation:tw 6s ease-in-out infinite}.t1{animation-delay:-1.5s}.t2{animation-delay:-3s}.t3{animation-delay:-4.5s}',
        '@keyframes tw{0%,100%{opacity:1}50%{opacity:.35}}',
        f'.slot{{opacity:0;animation:slot {CYCLE}s infinite}}',
        f'@keyframes slot{{0%{{opacity:0}}{pct(.15)}{{opacity:1}}{pct(S - .35)}{{opacity:1}}{pct(S - .05)}{{opacity:0}}100%{{opacity:0}}}}',
        f'.ty{{animation:ty {CYCLE}s infinite}}@keyframes ty{{0%{{width:0}}{pct(1.2)}{{width:var(--w)}}100%{{width:var(--w)}}}}',
        f'.pulse{{opacity:0;animation:pulse {CYCLE}s infinite}}',
        f'@keyframes pulse{{0%,{pct(1.19)}{{opacity:0;offset-distance:0%}}{pct(1.2)}{{opacity:1;offset-distance:0%}}'
        f'{pct(2.4)}{{opacity:1;offset-distance:100%}}{pct(2.45)},100%{{opacity:0;offset-distance:100%}}}}',
        f'.rip{{opacity:0;transform-box:fill-box;transform-origin:center;animation:rip {CYCLE}s infinite}}',
        f'@keyframes rip{{0%,{pct(2.19)}{{opacity:0;transform:scale(.08)}}{pct(2.2)}{{opacity:.9;transform:scale(.08)}}'
        f'{pct(3.3)}{{opacity:0;transform:scale(1)}}100%{{opacity:0;transform:scale(1)}}}}',
        f'.lit{{opacity:0;animation:lit {CYCLE}s infinite}}@keyframes lit{{0%,{pct(2.6)}{{opacity:0}}{pct(2.9)},100%{{opacity:1}}}}',
        f'.ln{{animation:ln {CYCLE}s infinite}}@keyframes ln{{0%,{pct(2.6)}{{stroke-dashoffset:var(--l)}}{pct(3.4)},100%{{stroke-dashoffset:0}}}}',
        f'.hit{{opacity:0;animation:hit {CYCLE}s infinite}}@keyframes hit{{0%,{pct(3.0)}{{opacity:0}}{pct(3.2)},100%{{opacity:1}}}}',
        f'.res{{opacity:0;animation:res {CYCLE}s infinite}}@keyframes res{{0%,{pct(3.2)}{{opacity:0}}{pct(3.5)},100%{{opacity:1}}}}',
        f'.ghost{{opacity:0;animation:ghost {CYCLE}s infinite}}@keyframes ghost{{0%,{pct(2.4)}{{opacity:0;offset-distance:0%}}'
        f'{pct(2.5)}{{opacity:.9;offset-distance:0%}}{pct(3.8)}{{opacity:.9;offset-distance:100%}}{pct(4.2)},100%{{opacity:.5;offset-distance:100%}}}}',
    ]
    reduced = ['@media (prefers-reduced-motion:reduce){*{animation:none!important}',
               '.q0.slot,.q0 .lit,.q0 .hit,.q0 .res{opacity:1}.q0 .ty{width:var(--w)}.q0 .ln{stroke-dashoffset:0}}']

    for qi, sc in enumerate(SCENES):
        dl = qi * S
        delay = f'animation-delay:{dl}s'
        g = [f'<g class="slot q{qi}" style="{delay}">', label(sc['cap'], 64, 368, SAFFRON, 12)]
        mono = sc['kind'] in ('write', 'describe')
        qkey = 400 if mono else 300
        qw = width(sc['q'], qkey, 22)
        g.append(f'<clipPath id="c{qi}"><rect x="84" y="380" height="36" width="0" class="ty" style="--w:{qw + 4:.1f}px;{delay}"/></clipPath>')
        g.append(tri_path([(70, 401, 5.5, 0)], IRIS, filled=True))
        g.append(f'<g clip-path="url(#c{qi})">{text(sc["q"], qkey, 22, 86, 408, LILAC if mono else WHITE)[0]}</g>')
        sx, sy = 86 + qw + 22, 400

        if sc['kind'] in ('search', 'weak', 'write'):
            strong = sc['kind'] != 'weak'
            same = [p for p in pts if p[5] == sc['sec']]
            ax, ay = sc['at']
            hx, hy = min(same, key=lambda p: (p[0] - ax) ** 2 + (p[1] - ay) ** 2)[:2]
            if sc['kind'] == 'search':
                ring = [p for p in same if 30 < math.hypot(p[0] - hx, p[1] - hy) < 125]
                ring.sort(key=lambda p: math.atan2(p[1] - hy, p[0] - hx))
                near = ring[::max(1, len(ring) // 11)][:11]
            elif sc['kind'] == 'weak':
                near = sorted(same, key=lambda p: -((p[0] - hx) ** 2 + (p[1] - hy) ** 2))[::60][:5]
            else:  # escrita: os wikilinks da nota para três vizinhas
                others = [p for p in pts if 45 < math.hypot(p[0] - hx, p[1] - hy) < 140]
                near = [others[i] for i in rng.sample(range(len(others)), 3)]
            mx, my = (sx + hx) / 2, min(sy, hy) - 90
            g.append(f'<path d="{tri(0, 0, 5, 0)}" fill="{IRIS}" class="pulse" '
                     f'style="offset-path:path(\'M{n(sx)} {n(sy)}Q{n(mx)} {n(my)} {n(hx)} {n(hy)}\');offset-rotate:0deg;{delay}"/>')
            rr = 120 if sc['kind'] == 'search' else (190 if sc['kind'] == 'weak' else 60)
            g.append(f'<circle cx="{n(hx)}" cy="{n(hy)}" r="{rr}" fill="none" stroke="{SAFFRON if sc["kind"] == "weak" else IRIS}" '
                     f'stroke-width="1.2" class="rip" style="{delay}"/>')
            col = SAFFRON if sc['kind'] == 'weak' else IRIS
            for k_, (x, y, r, rot, c, si) in enumerate(near):
                L = math.hypot(x - hx, y - hy)
                g.append(f'<path d="M{n(hx)} {n(hy)}L{n(x)} {n(y)}" stroke="{col}" stroke-width="1.3" '
                         f'opacity="{.85 if strong else .45}" stroke-dasharray="{L:.1f}" class="ln" style="--l:{L:.1f};{delay}"/>')
                g.append(tri_path([(x, y, r + 1.6, rot)], WHITE if strong else SAFFRON, filled=strong,
                                  extra=f' class="lit" style="animation-delay:{dl + k_ * 0.09:.2f}s"'))
            hit = (tri_path([(hx, hy, 10, -math.pi / 2)], SAFFRON, filled=strong, sw=1.6)
                   + tri_path([(hx, hy, 17, -math.pi / 2)], SAFFRON, sw=1)
                   + label(sc['tag'], hx + 22, hy - 18, SAFFRON, 11))
            g.append(f'<g class="hit" style="{delay}">{hit}</g>')
            if sc['kind'] == 'write':  # a versão anterior viaja até _historico/
                tx, ty_ = 1196, 500
                g.append(f'<g class="hit" style="{delay}">{label("_historico/", tx, ty_ + 4, ASH, 11, anchor="end")}</g>')
                g.append(f'<path d="{tri(0, 0, 8, -math.pi / 2)}" fill="none" stroke="{ASH}" stroke-width="1.2" class="ghost" '
                         f'style="offset-path:path(\'M{n(hx)} {n(hy)}Q{n(hx + 140)} {n(hy + 40)} {tx - 96} {ty_}\');offset-rotate:0deg;{delay}"/>')
        else:  # descrição: cada seção ganha contorno e contagem
            for k_, (cnt, (cx, cy), (sxx, syy), cols) in enumerate(SECTIONS[:5]):
                d_ = dl + 1.4 + k_ * 0.35
                g.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{sxx * 1.55:.0f}" ry="{syy * 1.55:.0f}" fill="none" stroke="{LILAC}" '
                         f'stroke-width="1" stroke-dasharray="3 5" opacity=".7" class="lit" style="animation-delay:{d_ - 1.2:.2f}s"/>')
                g.append(f'<g class="lit" style="animation-delay:{d_ - 1.2:.2f}s">'
                         f'{text(str(cnt), "display", 26, cx, (cy + 9) if k_ == 0 else (cy - syy * 1.55 - 8), WHITE, TR_D, anchor="middle")[0]}</g>')
        res = [text(sc['title'], 400, 18, 64, 452, sc['fill'])[0],
               text(sc['meta'], 300, 13, 64, 476, ASH)[0],
               text(sc['extra'], 300, 15, 64, 500, SILVER)[0]]
        g.append(f'<g class="res" style="{delay}">{"".join(res)}</g></g>')
        body.append(''.join(g))
        for t_ in (sc['title'], sc['extra']):
            assert width(t_, 400, 18) < 580, t_
        assert qw < 560, sc['q']

    title = ('Allan Zeni, AZ Sistemas. Infraestrutura de TI, Python e IA aplicada. Constelação com as 699 notas do meu vault '
             'e o vault-vector em ação: busca híbrida (semântico #1 e literal #1 para o reranker), sinalização de incerteza '
             '(uma pergunta de culinária volta com confiança baixa), escrita com histórico pelo MCP e descrição automática '
             'das 8 seções, 699 notas e 6.080 trechos.')
    return svg(W, H, title, ''.join(style + reduced), ''.join(body))


# ------------------------------------------------------------------ fluxo da busca
def fluxo():
    rng = random.Random(6080)
    W, H = 1280, 400
    body = [label('Como o vault-vector responde', 64, 72, SAFFRON, 13),
            text('Duas buscas, uma resposta com o grau de certeza.', 'display', 40, 62, 124, WHITE, TR_D)[0]]
    # estágios
    st = [  # (x, y, nome, detalhe)
        (64, 262, 'pergunta', 'texto livre'),
        (300, 212, 'semântico', 'bge-m3 no Ollama'),
        (300, 312, 'literal', 'SQLite FTS5'),
        (560, 262, 'fusão', 'Reciprocal Rank Fusion'),
        (790, 262, 'confiança', 'alta · média · baixa'),
        (1036, 262, 'juiz local', 'relê a faixa média'),
    ]
    for (x, y, name, det) in st:
        body.append(text(name, 300, 24, x, y, WHITE)[0])
        body.append(text(det, 300, 13, x, y + 22, ASH)[0])
    # trilhas de partículas entre os estágios (pontos fixos + pulsos que correm)
    lanes = [
        ('M180 254C230 254 240 204 290 204', 1.0),
        ('M180 254C230 254 240 304 290 304', 1.0),
        ('M450 204C500 204 510 254 550 254', 1.0),
        ('M430 304C490 304 510 254 550 254', 1.0),
        ('M712 254L780 254', .5),
        ('M934 254L1026 254', .5),
    ]
    trail = []
    def bezier_pts(d, k):
        nums = [float(v) for v in d.replace('M', ' ').replace('C', ' ').replace('L', ' ').split()]
        if 'C' in d:
            (x0, y0, x1, y1, x2, y2, x3, y3) = nums
            out = []
            for i in range(k + 1):
                t = i / k; u = 1 - t
                out.append((u**3*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t**3*x3, u**3*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t**3*y3))
            return out
        (x0, y0, x3, y3) = nums
        return [(x0 + (x3 - x0) * i / k, y0 + (y3 - y0) * i / k) for i in range(k + 1)]
    for d, _ in lanes:
        for (x, y) in bezier_pts(d, 14):
            trail.append((x, y, 1.7, rng.uniform(0, 6.3)))
    body.append(f'<g opacity=".45">{tri_path(trail, ASH, sw=.9)}</g>')
    cols = [IRIS, LILAC, BLUE, SAFFRON]
    for li, (d, _) in enumerate(lanes):
        for k in range(3):
            c = cols[(li + k) % len(cols)]
            body.append(f'<path d="{tri(0, 0, 4.2, 0)}" fill="{c}" class="run" '
                        f'style="offset-path:path(\'{d}\');animation-delay:{-(k * 0.8 + li * 0.25):.2f}s"/>')
    # saída
    body.append(text('trecho + aviso', 300, 24, 1036, 334, WHITE)[0])
    body.append(text('a incerteza vai junto', 300, 13, 1036, 356, ASH)[0])
    f = [(1044, 302, 4.5, math.pi / 2)]
    body.append(tri_path(f, SAFFRON, filled=True))
    body.append(label('699 notas · 6.080 trechos · índice local de 71 MB · nada vai para a nuvem', 64, 370, ASH, 11))
    style = ('.run{animation:run 2.4s linear infinite}@keyframes run{0%{offset-distance:0%;opacity:0}15%{opacity:1}'
             '85%{opacity:1}100%{offset-distance:100%;opacity:0}}'
             '@media (prefers-reduced-motion:reduce){.run{animation:none;opacity:0}}')
    return svg(W, H, 'Como o vault-vector responde: a pergunta vai para a busca semântica (bge-m3 no Ollama) e para a literal '
               '(SQLite FTS5); os dois rankings são fundidos por Reciprocal Rank Fusion, o resultado ganha uma faixa de '
               'confiança e um juiz local relê os casos da faixa média. 699 notas, 6.080 trechos, índice local de 71 MB.',
               style, ''.join(body))


OUT.mkdir(parents=True, exist_ok=True)
for name, fn in [('vault-vivo', banner), ('como-busca', fluxo)]:
    s = fn(); (OUT / f'{name}.svg').write_text(s)
    print(f'{name}.svg {len(s) // 1024} KB')
