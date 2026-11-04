"""Texto em caminhos SVG com kerning do GPOS (Inter), sem depender de fonte no navegador."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT_DIR = '/usr/share/fonts/opentype/inter/'
FILES = {
    200: 'Inter-ExtraLight.otf',
    300: 'Inter-Light.otf',
    400: 'Inter-Regular.otf',
    500: 'Inter-Medium.otf',
    600: 'Inter-SemiBold.otf',
    'display': 'InterDisplay-Regular.otf',
}


def _num(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return '0' if s == '-0' else s


class Font:
    def __init__(self, key):
        self.tt = TTFont(FONT_DIR + FILES[key])
        self.gs = self.tt.getGlyphSet()
        self.cmap = self.tt.getBestCmap()
        self.upm = self.tt['head'].unitsPerEm
        self.hmtx = self.tt['hmtx']
        self._subtables = self._kern_subtables()
        self._cache = {}

    def _kern_subtables(self):
        gpos = self.tt['GPOS'].table
        idx = sorted({i for fr in gpos.FeatureList.FeatureRecord if fr.FeatureTag == 'kern'
                      for i in fr.Feature.LookupListIndex})
        out = []
        for li in idx:
            lk = gpos.LookupList.Lookup[li]
            subs = []
            for st in lk.SubTable:
                if lk.LookupType == 9:
                    if st.ExtensionLookupType != 2:
                        continue
                    st = st.ExtSubTable
                elif lk.LookupType != 2:
                    continue
                subs.append(st)
            if subs:
                out.append(subs)
        return out

    def kern(self, a, b):
        key = (a, b)
        if key in self._cache:
            return self._cache[key]
        total = 0
        for subs in self._subtables:
            for st in subs:
                cov = st.Coverage.glyphs
                if a not in cov:
                    continue
                if st.Format == 1:
                    ps = st.PairSet[cov.index(a)]
                    hit = next((r for r in ps.PairValueRecord if r.SecondGlyph == b), None)
                    if hit is None:
                        continue
                    v = hit.Value1
                    total += getattr(v, 'XAdvance', 0) or 0 if v else 0
                    break
                else:
                    c1 = st.ClassDef1.classDefs.get(a, 0)
                    c2 = st.ClassDef2.classDefs.get(b, 0)
                    v = st.Class1Record[c1].Class2Record[c2].Value1
                    total += (getattr(v, 'XAdvance', 0) or 0) if v else 0
                    break
        self._cache[key] = total
        return total

    def layout(self, text, size, tracking=0.0):
        s = size / self.upm
        names = [self.cmap[ord(c)] for c in text]
        xs, x = [], 0.0
        for i, g in enumerate(names):
            xs.append(x)
            adv = self.hmtx[g][0]
            if i + 1 < len(names):
                adv += self.kern(g, names[i + 1])
            x += adv * s + (tracking if i + 1 < len(names) else 0)
        return names, xs, x

    def width(self, text, size, tracking=0.0):
        return self.layout(text, size, tracking)[2]

    def path(self, text, size, x, y, tracking=0.0, anchor='start'):
        names, xs, w = self.layout(text, size, tracking)
        if anchor == 'end':
            x -= w
        elif anchor == 'middle':
            x -= w / 2
        s = size / self.upm
        pen = SVGPathPen(self.gs, ntos=_num)
        for g, gx in zip(names, xs):
            self.gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x + gx, y)))
        return pen.getCommands(), w


_fonts = {}


def font(key):
    if key not in _fonts:
        _fonts[key] = Font(key)
    return _fonts[key]


def text(s, key, size, x, y, fill, tracking_em=0.0, anchor='start', opacity=None, cls=None, upper=False):
    if upper:
        s = s.upper()
    d, w = font(key).path(s, size, x, y, tracking_em * size, anchor)
    attrs = f' fill="{fill}"'
    if opacity is not None:
        attrs += f' opacity="{opacity}"'
    if cls:
        attrs += f' class="{cls}"'
    return f'<path d="{d}"{attrs}/>', w


def width(s, key, size, tracking_em=0.0, upper=False):
    if upper:
        s = s.upper()
    return font(key).width(s, size, tracking_em * size)
