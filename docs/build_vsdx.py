"""Generate docs/coach-rose-job-flow.vsdx — Coach Rose job system flow (intake job offer -> outcome).

Hand-built VSDX (Open Packaging XML), no third-party libraries. Run: python3 docs/build_vsdx.py
"""
import os
import zipfile
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coach-rose-job-flow.vsdx")
PW, PH = 17.0, 11.0  # tabloid landscape, inches

# ---- lanes -----------------------------------------------------------------
LANES = [
    ("1 · INTAKE", 2.25, "#E8F0FB", "#2F5C9E"),
    ("2 · PREP & BUILD", 6.4, "#E6F4F1", "#1F7A6A"),
    ("3 · PRACTICE WITH ROSE", 10.6, "#FDEEF4", "#B0416B"),
    ("4 · INTERVIEW & OUTCOME", 14.75, "#EAF5E6", "#3C7A2E"),
]
LANE_W, LANE_TOP, LANE_BOT = 4.0, 10.45, 0.35

PROC, TERM, DEC, DATA = "proc", "term", "dec", "data"
STY = {  # fill, line, text
    "intake": ("#FFFFFF", "#2F5C9E", "#1D2B40"),
    "prep": ("#FFFFFF", "#1F7A6A", "#1D2B40"),
    "rose": ("#FFFFFF", "#B0416B", "#3D1F2B"),
    "roseH": ("#B0416B", "#B0416B", "#FFFFFF"),
    "out": ("#FFFFFF", "#3C7A2E", "#1D2B40"),
    "start": ("#2F5C9E", "#2F5C9E", "#FFFFFF"),
    "end": ("#3C7A2E", "#3C7A2E", "#FFFFFF"),
    "stop": ("#8A8F98", "#8A8F98", "#FFFFFF"),
    "dec": ("#FFF6DD", "#C08A00", "#3A2C00"),
}

X1, X2, X3, X4 = (l[1] for l in LANES)
W, H = 3.2, 0.72
# id: (kind, style, x, y, w, h, text)
N = {
    "a1": (TERM, "start", X1, 9.55, W, 0.6, "Job offer / posting received"),
    "a2": (PROC, "intake", X1, 8.45, W, H, "Capture job details\ntitle · team · level · location · comp · full JD"),
    "a3": (PROC, "intake", X1, 7.3, W, H, "Score fit vs. master résumé\n(must-haves, gaps, keywords)"),
    "a4": (DEC, "dec", X1, 6.0, 2.4, 1.1, "Strong fit?"),
    "a5": (TERM, "stop", X1, 4.6, 2.6, 0.6, "Pass / archive & log reason"),

    "b1": (PROC, "prep", X2, 9.55, W, H, "Tailor résumé to JD\n(ATS keywords, quantified wins)"),
    "b2": (PROC, "prep", X2, 8.4, W, H, "Map JD → Leadership Principles\n& role competencies"),
    "b3": (PROC, "prep", X2, 7.25, W, H, "Build question bank\nLP · Role/Technical · Warm-up"),
    "b4": (PROC, "prep", X2, 6.1, W, 0.85, "Per question: model answer, STAR\nskeleton, talking points, follow-up\nprobes, LP keywords (from résumé)"),
    "b5": (PROC, "prep", X2, 4.85, W, H, "Publish Mock Interview Studio\n(GitHub Pages URL + QR to phone)"),

    "c1": (PROC, "rose", X3, 9.55, W, H, "Pick question\n(filter by type / 🎲 random)"),
    "c2": (PROC, "rose", X3, 8.5, W, H, "Glance at STAR skeleton &\ntalking points (model answer once)"),
    "c3": (PROC, "rose", X3, 7.45, W, H, "● Record spoken answer\n(target 2:00–4:00)"),
    "c4": (DEC, "dec", X3, 6.25, 2.6, 1.1, "Live speech-to-\ntext available?"),
    "c5": (PROC, "rose", X3 + 1.3, 5.05, 1.6, 0.7, "Paste / edit\ntranscript"),
    "c6": (PROC, "roseH", X3, 3.95, W, 0.95, "🌹 Rose scores 0–5\nSTAR · Ownership (I vs we) · Data ·\nQuantified result · Maps to LP"),
    "c7": (PROC, "rose", X3, 2.7, W, 0.95, "Verdict: overall /5 + Strong Hire /\nHire / Lean No / No Hire, strengths,\nfixes, pacing, fillers, follow-up probe"),
    "c8": (PROC, "rose", X3, 1.5, W, H, "Self-score + notes → 💾 Save take\n(localStorage on device)"),

    "d1": (DEC, "dec", X4, 9.4, 2.9, 1.2, "Hire bar met on\nall questions?\n(Rose avg ≥ 3.4)"),
    "d2": (PROC, "out", X4, 8.0, W, H, "Export debrief to PDF\n+ JSON backup"),
    "d3": (PROC, "out", X4, 6.9, W, H, "Live interview\n(answer follow-up probes)"),
    "d4": (DEC, "dec", X4, 5.65, 2.4, 1.1, "Offer\nextended?"),
    "d5": (PROC, "out", X4, 4.35, W, H, "Evaluate & negotiate offer\n(comp, level, start date)"),
    "d6": (TERM, "end", X4, 3.25, 2.6, 0.6, "Accept offer ✔"),
    "d7": (PROC, "out", X4, 1.85, W, H, "Debrief: log probes asked &\nweak answers → next intake"),
}


def side(nid, s):
    k, _, x, y, w, h, _ = N[nid]
    return {"t": (x, y + h / 2), "b": (x, y - h / 2), "l": (x - w / 2, y), "r": (x + w / 2, y)}[s]


# edges: (from, fromSide, to, toSide, via points, label)
GAP = 0.18  # lane gutter x offset
E = [
    ("a1", "b", "a2", "t", [], ""),
    ("a2", "b", "a3", "t", [], ""),
    ("a3", "b", "a4", "t", [], ""),
    ("a4", "b", "a5", "t", [], "No"),
    ("a4", "r", "b1", "l", [(X1 + 1.85, 6.0), (X1 + 1.85, 9.55)], "Yes"),
    ("b1", "b", "b2", "t", [], ""),
    ("b2", "b", "b3", "t", [], ""),
    ("b3", "b", "b4", "t", [], ""),
    ("b4", "b", "b5", "t", [], ""),
    ("b5", "r", "c1", "l", [(X2 + 2.0, 4.85), (X2 + 2.0, 9.55)], ""),
    ("c1", "b", "c2", "t", [], ""),
    ("c2", "b", "c3", "t", [], ""),
    ("c3", "b", "c4", "t", [], ""),
    ("c4", "b", "c6", "t", [], "Yes – live transcript"),
    ("c4", "r", "c5", "t", [(X3 + 1.3, 6.25)], "No"),
    ("c5", "b", "c6", "t", [(X3 + 1.3, 4.58), (X3, 4.58)], ""),
    ("c6", "b", "c7", "t", [], ""),
    ("c7", "b", "c8", "t", [], ""),
    ("c8", "r", "d1", "l", [(X3 + 1.95, 1.5), (X3 + 1.95, 9.4)], ""),
    ("d1", "l", "c1", "r", [(X3 + 1.95 + 0.0, 9.4)], ""),  # placeholder replaced below
    ("d1", "b", "d2", "t", [], "Yes"),
    ("d2", "b", "d3", "t", [], ""),
    ("d3", "b", "d4", "t", [], ""),
    ("d4", "b", "d5", "t", [], "Yes"),
    ("d5", "b", "d6", "t", [], ""),
    ("d4", "r", "d7", "r", [(X4 + 1.85, 5.65), (X4 + 1.85, 1.85)], "No"),
    ("d7", "b", "a1", "l", [(X4, 0.62), (0.45, 0.62), (0.45, 9.55)], "Next job"),
]
# "No — practise again" loop: d1 top -> over to c1 top
E[19] = ("d1", "t", "c1", "t", [(X4, 10.56), (X3, 10.56)], "No – re-record weakest")

# ---- XML helpers -------------------------------------------------------------
def cell(n, v, u=None):
    return f'<Cell N="{n}" V="{v}"' + (f' U="{u}"' if u else "") + "/>"


def rgb(c):
    return c


def char_para(color, size_pt=9.0, bold=False):
    return (
        '<Section N="Character"><Row IX="0">'
        + cell("Font", "Calibri") + cell("Color", color) + cell("Size", round(size_pt / 72, 4), "PT")
        + cell("Style", 1 if bold else 0)
        + '</Row></Section>'
        '<Section N="Paragraph"><Row IX="0">' + cell("HorzAlign", 1) + '</Row></Section>'
    )


def text_xml(t):
    return "<Text>" + escape(t).replace("\n", "&#10;") + "</Text>" if t else ""


def geom_rect(w, h):
    return (
        '<Section N="Geometry" IX="0">' + cell("NoFill", 0) + cell("NoLine", 0) +
        f'<Row T="MoveTo" IX="1">{cell("X", 0)}{cell("Y", 0)}</Row>'
        f'<Row T="LineTo" IX="2">{cell("X", w)}{cell("Y", 0)}</Row>'
        f'<Row T="LineTo" IX="3">{cell("X", w)}{cell("Y", h)}</Row>'
        f'<Row T="LineTo" IX="4">{cell("X", 0)}{cell("Y", h)}</Row>'
        f'<Row T="LineTo" IX="5">{cell("X", 0)}{cell("Y", 0)}</Row></Section>'
    )


def geom_diamond(w, h):
    return (
        '<Section N="Geometry" IX="0">' + cell("NoFill", 0) + cell("NoLine", 0) +
        f'<Row T="MoveTo" IX="1">{cell("X", w/2)}{cell("Y", 0)}</Row>'
        f'<Row T="LineTo" IX="2">{cell("X", w)}{cell("Y", h/2)}</Row>'
        f'<Row T="LineTo" IX="3">{cell("X", w/2)}{cell("Y", h)}</Row>'
        f'<Row T="LineTo" IX="4">{cell("X", 0)}{cell("Y", h/2)}</Row>'
        f'<Row T="LineTo" IX="5">{cell("X", w/2)}{cell("Y", 0)}</Row></Section>'
    )


def conn_points(w, h):
    pts = [(w / 2, h), (w / 2, 0), (0, h / 2), (w, h / 2)]
    rows = "".join(f'<Row T="Connection" IX="{i}">{cell("X", x)}{cell("Y", y)}</Row>' for i, (x, y) in enumerate(pts))
    return f'<Section N="Connection">{rows}</Section>'


shapes, connects = [], []
sid = 0


def nid():
    global sid
    sid += 1
    return sid


def box(x, y, w, h, fill, line, tcol, text, kind=PROC, lw=1.25, size=9.0, bold=False, rounding=0.06, name=None, valign=1):
    i = nid()
    r = {TERM: h / 2, DEC: 0, PROC: rounding, DATA: 0}[kind]
    g = geom_diamond(w, h) if kind == DEC else geom_rect(w, h)
    shapes.append(
        f'<Shape ID="{i}" NameU="{name or "Shape"+str(i)}" Type="Shape" LineStyle="0" FillStyle="0" TextStyle="0">'
        + cell("PinX", x) + cell("PinY", y) + cell("Width", w) + cell("Height", h)
        + cell("LocPinX", w / 2) + cell("LocPinY", h / 2) + cell("Angle", 0)
        + cell("FillForegnd", fill) + cell("FillPattern", 1)
        + cell("LineColor", line) + cell("LineWeight", round(lw / 72, 5), "PT") + cell("LinePattern", 1)
        + cell("Rounding", r) + cell("VerticalAlign", valign)
        + cell("LeftMargin", 0.06) + cell("RightMargin", 0.06) + cell("TopMargin", 0.04) + cell("BottomMargin", 0.04)
        + char_para(tcol, size, bold) + conn_points(w, h) + g + text_xml(text) + "</Shape>"
    )
    return i


# lanes (background)
for title, cx, bg, accent in LANES:
    box(cx, (LANE_TOP + LANE_BOT) / 2, LANE_W, LANE_TOP - LANE_BOT, bg, bg, accent, "", rounding=0.08, lw=0.5)

# title
box(PW / 2, 10.8, 14, 0.36, "#FFFFFF", "#FFFFFF", "#3D1F2B",
    "Coach Rose Job System — end-to-end flow from job-offer intake to outcome", lw=0, size=16, bold=True)
# lane headers
for title, cx, bg, accent in LANES:
    box(cx, LANE_TOP - 0.2, LANE_W - 0.3, 0.32, bg, bg, accent, title, lw=0, size=10.5, bold=True)

IDS = {}
for k, (kind, st, x, y, w, h, t) in N.items():
    f, l, tc = STY[st]
    IDS[k] = box(x, y - (0.15 if k[0] in "abcd" and False else 0), w, h, f, l, tc, t, kind=kind,
                 lw=1.75 if kind == DEC else 1.25, bold=st in ("start", "end", "stop", "roseH", "dec"), name=k)

SIDE_IX = {"t": 0, "b": 1, "l": 2, "r": 3}


def connector(a, sa, b, sb, via, label):
    i = nid()
    p = [side(a, sa)] + list(via) + [side(b, sb)]
    bx, by = p[0]
    ex, ey = p[-1]
    w, h = ex - bx, ey - by
    rows = f'<Row T="MoveTo" IX="1">{cell("X", 0)}{cell("Y", 0)}</Row>'
    for j, (px, py) in enumerate(p[1:], start=2):
        rows += f'<Row T="LineTo" IX="{j}">{cell("X", round(px-bx, 4))}{cell("Y", round(py-by, 4))}</Row>'
    # label at midpoint of first segment
    (x0, y0), (x1, y1) = p[0], p[1]
    lx, ly = (x0 + x1) / 2 - bx, (y0 + y1) / 2 - by
    if label and len(p) > 2 and ((abs(x1 - x0) < 0.3 and abs(y1 - y0) < 0.3) or label.startswith("No –")):
        (x0, y0), (x1, y1) = p[1], p[2]
        lx, ly = (x0 + x1) / 2 - bx, (y0 + y1) / 2 - by
    tw = max(0.4, 0.075 * len(label) + 0.15)
    txt = ""
    if label:
        txt = (cell("TxtPinX", round(lx, 4)) + cell("TxtPinY", round(ly, 4)) + cell("TxtWidth", tw) + cell("TxtHeight", 0.2)
               + cell("TxtLocPinX", tw / 2) + cell("TxtLocPinY", 0.1) + cell("TxtAngle", 0))
    shapes.append(
        f'<Shape ID="{i}" NameU="Dynamic connector.{i}" Type="Shape" LineStyle="0" FillStyle="0" TextStyle="0">'
        + cell("PinX", (bx + ex) / 2) + cell("PinY", (by + ey) / 2) + cell("Width", round(w, 4)) + cell("Height", round(h, 4))
        + cell("LocPinX", round(w / 2, 4)) + cell("LocPinY", round(h / 2, 4)) + cell("Angle", 0)
        + cell("BeginX", bx) + cell("BeginY", by) + cell("EndX", ex) + cell("EndY", ey)
        + cell("ObjType", 2) + cell("ShapeRouteStyle", 16) + cell("ConLineRouteExt", 1)
        + cell("LineColor", "#4A4F57") + cell("LineWeight", round(1.1 / 72, 5), "PT") + cell("LinePattern", 1)
        + cell("EndArrow", 13) + cell("EndArrowSize", 2) + cell("Rounding", 0.06)
        + cell("FillForegnd", "#FFFFFF") + cell("FillPattern", 1 if label else 0) + cell("TextBkgnd", "#FFFFFF" if label else 0)
        + txt + char_para("#333333", 8.5, True)
        + f'<Section N="Geometry" IX="0">{cell("NoFill", 1)}{cell("NoLine", 0)}{rows}</Section>'
        + text_xml(label) + "</Shape>"
    )
    connects.append(f'<Connect FromSheet="{i}" FromCell="BeginX" FromPart="9" ToSheet="{IDS[a]}" ToCell="Connections.X{SIDE_IX[sa]+1}" ToPart="{100+SIDE_IX[sa]}"/>')
    connects.append(f'<Connect FromSheet="{i}" FromCell="EndX" FromPart="12" ToSheet="{IDS[b]}" ToCell="Connections.X{SIDE_IX[sb]+1}" ToPart="{100+SIDE_IX[sb]}"/>')


for e in E:
    connector(*e)

# legend / footnote
box(PW / 2, 0.15, 16, 0.25, "#FFFFFF", "#FFFFFF", "#6B6F76",
    "Lanes 1–2 & 4 = candidate workflow (résumé tailoring / interview).  Lane 3 = the Rose app (index.html): runs 100% in-browser; audio, transcripts & scores stay on the device.  Hire bar: ≥4.2 Strong Hire · ≥3.4 Hire · ≥2.6 Lean No · else No Hire.",
    lw=0, size=7.5)

# ---- package ------------------------------------------------------------------
NS = 'xmlns="http://schemas.microsoft.com/office/visio/2012/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xml:space="preserve"'
page_xml = (f'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n<PageContents {NS}><Shapes>'
            + "".join(shapes) + "</Shapes><Connects>" + "".join(connects) + "</Connects></PageContents>")

pages_xml = (f'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n<Pages {NS}>'
             f'<Page ID="0" NameU="Coach Rose Flow" Name="Coach Rose Flow" ViewScale="-1" ViewCenterX="{PW/2}" ViewCenterY="{PH/2}">'
             f'<PageSheet LineStyle="0" FillStyle="0" TextStyle="0">{cell("PageWidth", PW)}{cell("PageHeight", PH)}'
             f'{cell("PageScale", 1, "IN_F")}{cell("DrawingScale", 1, "IN_F")}{cell("DrawingSizeType", 0)}{cell("PrintPageOrientation", 2)}'
             f'{cell("RouteStyle", 16)}{cell("LineJumpStyle", 0)}</PageSheet><Rel r:id="rId1"/></Page></Pages>')

document_xml = f'''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<VisioDocument {NS}><DocumentSettings TopPage="0" DefaultTextStyle="0" DefaultLineStyle="0" DefaultFillStyle="0" DefaultGuideStyle="0"><GlueSettings>9</GlueSettings><SnapSettings>65847</SnapSettings><SnapExtensions>34</SnapExtensions><DynamicGridEnabled>0</DynamicGridEnabled><ProtectStyles>0</ProtectStyles><ProtectShapes>0</ProtectShapes><ProtectMasters>0</ProtectMasters><ProtectBkgnds>0</ProtectBkgnds></DocumentSettings>
<Colors><ColorEntry IX="0" RGB="#000000"/><ColorEntry IX="1" RGB="#FFFFFF"/></Colors>
<FaceNames><FaceName NameU="Calibri" UnicodeRanges="-536859905 -1073732485 9 0" CharSets="536871423 0" Panose="2 15 5 2 2 2 4 3 2 4" Flags="325"/></FaceNames>
<StyleSheets><StyleSheet ID="0" NameU="No Style" Name="No Style">{cell("EnableLineProps",1)}{cell("EnableFillProps",1)}{cell("EnableTextProps",1)}{cell("HideForApply",0)}{cell("LineWeight",0.01041666666666667)}{cell("LineColor","#000000")}{cell("LinePattern",1)}{cell("Rounding",0)}{cell("EndArrowSize",2)}{cell("BeginArrow",0)}{cell("EndArrow",0)}{cell("LineCap",0)}{cell("BeginArrowSize",2)}{cell("LineColorTrans",0)}{cell("CompoundType",0)}{cell("FillForegnd","#FFFFFF")}{cell("FillBkgnd","#000000")}{cell("FillPattern",1)}{cell("ShdwForegnd","#000000")}{cell("ShdwPattern",0)}{cell("FillForegndTrans",0)}{cell("FillBkgndTrans",0)}{cell("ShdwForegndTrans",0)}{cell("LeftMargin",0)}{cell("RightMargin",0)}{cell("TopMargin",0)}{cell("BottomMargin",0)}{cell("VerticalAlign",1)}{cell("TextBkgnd",0)}{cell("DefaultTabStop",0.5)}{cell("TextDirection",0)}{cell("TextBkgndTrans",0)}
<Section N="Character"><Row IX="0">{cell("Font","Calibri")}{cell("Color","#000000")}{cell("Style",0)}{cell("Case",0)}{cell("Pos",0)}{cell("FontScale",1)}{cell("Size",0.1666666666666667)}{cell("DblUnderline",0)}{cell("Overline",0)}{cell("Strikethru",0)}{cell("Letterspace",0)}{cell("ColorTrans",0)}</Row></Section>
<Section N="Paragraph"><Row IX="0">{cell("IndFirst",0)}{cell("IndLeft",0)}{cell("IndRight",0)}{cell("SpLine",-1.2)}{cell("SpBefore",0)}{cell("SpAfter",0)}{cell("HorzAlign",1)}{cell("Bullet",0)}</Row></Section>
</StyleSheet></StyleSheets>
<DocumentSheet NameU="TheDoc" LineStyle="0" FillStyle="0" TextStyle="0">{cell("OutputFormat",0)}{cell("LockPreview",0)}{cell("AddMarkup",0)}{cell("ViewMarkup",0)}{cell("DocLockReplace",0)}{cell("NoCoauth",0)}{cell("DocLockDuplicatePage",0)}{cell("PreviewQuality",0)}{cell("PreviewScope",0)}{cell("DocLangID",1033)}</DocumentSheet>
</VisioDocument>'''

content_types = '''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/visio/document.xml" ContentType="application/vnd.ms-visio.drawing.main+xml"/>
<Override PartName="/visio/pages/pages.xml" ContentType="application/vnd.ms-visio.pages+xml"/>
<Override PartName="/visio/pages/page1.xml" ContentType="application/vnd.ms-visio.page+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''

root_rels = '''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/document" Target="visio/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''

doc_rels = '''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/pages" Target="pages/pages.xml"/>
</Relationships>'''

pages_rels = '''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/page" Target="page1.xml"/>
</Relationships>'''

core = '''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>Coach Rose Job System Flow</dc:title><dc:creator>Coach Rose</dc:creator>
<dcterms:created xsi:type="dcterms:W3CDTF">2026-11-13T00:00:00Z</dcterms:created></cp:coreProperties>'''

app = '''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Visio</Application><Template></Template></Properties>'''

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", root_rels)
    z.writestr("docProps/core.xml", core)
    z.writestr("docProps/app.xml", app)
    z.writestr("visio/document.xml", document_xml)
    z.writestr("visio/_rels/document.xml.rels", doc_rels)
    z.writestr("visio/pages/pages.xml", pages_xml)
    z.writestr("visio/pages/_rels/pages.xml.rels", pages_rels)
    z.writestr("visio/pages/page1.xml", page_xml)
print("wrote", OUT, len(shapes), "shapes")
