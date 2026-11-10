"""
Generate obe_test_template.docx with Jinja2 tags for Component 1.
Correct docxtpl table row tag syntax: {%tr for x in list %} ... {%tr endfor %}
"""
import zipfile, shutil, os, tempfile
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ORIG   = "/app/templates/obe_test_template.docx.bak"
OUT    = "/app/templates/obe_test_template.docx"

doc = Document()

# ─── Page margins ────────────────────────────────────────────
section = doc.sections[0]
section.top_margin    = Cm(2.54)
section.bottom_margin = Cm(2.54)
section.left_margin   = Cm(3.0)
section.right_margin  = Cm(2.54)

FONT_NAME = "TH SarabunPSK"

def set_font(run, size=16, bold=False):
    run.font.name = FONT_NAME
    run.font.size = Pt(size)
    run.font.bold = bold
    r = run._r
    rPr = r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), FONT_NAME)
    rFonts.set(qn('w:hAnsi'), FONT_NAME)
    rFonts.set(qn('w:cs'),    FONT_NAME)
    rFonts.set(qn('w:eastAsia'), FONT_NAME)
    existing = rPr.find(qn('w:rFonts'))
    if existing is not None:
        rPr.remove(existing)
    rPr.insert(0, rFonts)

def para(text, bold=False, size=16, align=WD_ALIGN_PARAGRAPH.LEFT, sb=0, sa=4):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(sb)
    p.paragraph_format.space_after  = Pt(sa)
    r = p.add_run(text)
    set_font(r, size=size, bold=bold)
    return p

def labeled(label, tag, size=16, indent=1.0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Cm(indent)
    r1 = p.add_run(label)
    set_font(r1, size=size)
    r2 = p.add_run(tag)
    set_font(r2, size=size)
    return p

# ════════════ COVER PAGE ════════════════════════════════════
# Restore logo from backup
logo_data = None
try:
    with zipfile.ZipFile(ORIG) as z:
        if "word/media/image1.jpeg" in z.namelist():
            logo_data = z.read("word/media/image1.jpeg")
except Exception:
    pass

if logo_data:
    with tempfile.NamedTemporaryFile(suffix=".jpeg", delete=False) as tmp:
        tmp.write(logo_data)
        logo_tmp = tmp.name
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(logo_tmp, width=Cm(5))
    os.unlink(logo_tmp)
    print("Logo inserted from backup.")
else:
    para("[โลโก้มหาวิทยาลัย]", align=WD_ALIGN_PARAGRAPH.CENTER)
    print("Logo not found — placeholder used.")

para("{{ name_th }}", bold=True, size=18, align=WD_ALIGN_PARAGRAPH.CENTER, sb=12)
para("({{ name_en }})", size=16, align=WD_ALIGN_PARAGRAPH.CENTER)
para("({{ curriculum_year }})", size=16, align=WD_ALIGN_PARAGRAPH.CENTER, sa=20)
para("{{ department }}", size=16, align=WD_ALIGN_PARAGRAPH.CENTER, sa=2)
para("{{ campus }}",    size=16, align=WD_ALIGN_PARAGRAPH.CENTER, sa=2)
para("{{ university_name }}", size=16, align=WD_ALIGN_PARAGRAPH.CENTER, sa=2)

doc.add_page_break()

# ════════════ OBE 2 header ══════════════════════════════════
para("OBE 2", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.RIGHT, sa=2)

# ════════════ COMPONENT 1 ═══════════════════════════════════
para("องค์ประกอบที่ 1  ชื่อปริญญา ประกาศนียบัตรบัณฑิต ประกาศนียบัตรบัณฑิตชั้นสูง และสาขาวิชา",
     bold=True, size=16, sb=4, sa=8)

# 1. Program code / name
para("1.  รหัสและชื่อหลักสูตร", bold=True, sb=4, sa=4)
labeled("รหัสหลักสูตร : ", "{{ program_code }}")
labeled("ภาษาไทย       : ", "{{ name_th }}")
labeled("ภาษาอังกฤษ    : ", "{{ name_en }}")

# 2. Degree name
para("2.  ชื่อปริญญาและสาขาวิชา", bold=True, sb=8, sa=4)
labeled("ชื่อเต็ม (ภาษาไทย)    : ", "{{ degree_name_th }}")
labeled("ชื่อย่อ  (ภาษาไทย)    : ", "{{ degree_abbr_th }}")
labeled("ชื่อเต็ม (ภาษาอังกฤษ) : ", "{{ degree_name_en }}")
labeled("ชื่อย่อ  (ภาษาอังกฤษ) : ", "{{ degree_abbr_en }}")

# 3. Major
para("3.  วิชาเอก", bold=True, sb=8, sa=4)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Cm(1.0)
p.paragraph_format.space_after = Pt(2)
r = p.add_run("{% if majors %}{{ majors | join(', ') }}{% else %}ไม่มี{% endif %}")
set_font(r)

# 4. Program format
para("4.  รูปแบบของหลักสูตร", bold=True, sb=8, sa=4)
labeled("4.1 รูปแบบ                                    : ", "{{ program_format or 'หลักสูตรระดับปริญญาตรี 4 ปี' }}")
labeled("4.2 ประเภทของหลักสูตร                         : ", "{{ program_category or 'หลักสูตรปริญญาตรีทางวิชาการ' }}")
labeled("4.3 ภาษาที่ใช้                                : ", "{{ language or 'ภาษาไทยและภาษาอังกฤษ' }}")
labeled("4.4 การรับเข้าศึกษา                           : ", "{{ admission_req or 'รับนักศึกษาไทยและนักศึกษาต่างประเทศที่ใช้ภาษาไทยได้' }}")
labeled("4.5 ความร่วมมือกับสถาบันอื่น                 : ", "{{ cooperation or 'ไม่มี' }}")
labeled("4.6 การให้ปริญญาแก่ผู้สำเร็จการศึกษา         : ", "{{ degree_granting or 'ให้ปริญญาเพียงสาขาวิชาเดียว' }}")

# 5. Approval status
para(
    "5.  สถานภาพของหลักสูตรและการพิจารณาอนุมัติ/เห็นชอบหลักสูตร",
    bold=True, sb=8, sa=4
)

p = doc.add_paragraph()
p.paragraph_format.left_indent = Cm(1.0)
r = p.add_run("- เปิดสอนภาคการศึกษาที่ 1 ปีการศึกษา {{ open_year }} เป็นต้นไป")
set_font(r)

# Opening loop tag: its own paragraph
p = doc.add_paragraph()
p.add_run("{%p for app in approvals %}")

# Loop content
p = doc.add_paragraph()
p.paragraph_format.left_indent = Cm(1.0)
r = p.add_run(
    "- ได้พิจารณาโดย {{ app.committee }} "
    "เมื่อวันที่ {{ app.approval_date }}"
)
set_font(r)

# Closing loop tag: its own paragraph
p = doc.add_paragraph()
p.add_run("{%p endfor %}")

# 6. Readiness
para("6.  ความพร้อมในการเผยแพร่หลักสูตรตามกรอบมาตรฐานคุณวุฒิ", bold=True, sb=8, sa=4)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Cm(1.0)
p.paragraph_format.space_after = Pt(2)
r = p.add_run("{{ readiness or 'มีความพร้อมเผยแพร่ตามเกณฑ์มาตรฐาน' }}")
set_font(r)

# 7. Careers
para(
    "7.  อาชีพที่สามารถประกอบได้หลังสำเร็จการศึกษา",
    bold=True, sb=8, sa=4
)

# Opening loop tag
p = doc.add_paragraph()
p.add_run("{%p for career in careers %}")

# Career content
p = doc.add_paragraph()
p.paragraph_format.left_indent = Cm(1.0)
r = p.add_run("- {{ career }}")
set_font(r)

# Closing loop tag
p = doc.add_paragraph()
p.add_run("{%p endfor %}")

# Empty list condition
p = doc.add_paragraph()
p.add_run("{%p if not careers %}")

p = doc.add_paragraph()
p.paragraph_format.left_indent = Cm(1.0)
r = p.add_run("ไม่ระบุ")
set_font(r)

p = doc.add_paragraph()
p.add_run("{%p endif %}")

# 8. Instructors table
para("8.  อาจารย์ผู้รับผิดชอบหลักสูตร", bold=True, sb=8, sa=6)

tbl = doc.add_table(rows=2, cols=4)
tbl.style = "Table Grid"
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

# Header row
hdrs = ["ลำดับ", "ชื่อ - นามสกุล", "ตำแหน่งทางวิชาการ", "คุณวุฒิการศึกษา (สาขาวิชา)"]
for i, cell in enumerate(tbl.rows[0].cells):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(hdrs[i])
    set_font(r, size=14, bold=True)

# Data row — {%tr for %} and {%tr endfor %} in first/last cell of the row
# This is the CORRECT docxtpl syntax (no space between {% and tr)
row_tags = [
    "{%tr for inst in instructors %}{{ loop.index }}",
    "{{ inst.name }}",
    "{{ inst.position }}",
    "{{ inst.degree }}{%tr endfor %}",
]
for i, cell in enumerate(tbl.rows[1].cells):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 0 else WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(row_tags[i])
    set_font(r, size=14)

doc.add_paragraph()

# 9. Location
para("9.  สถานที่จัดการเรียนการสอน", bold=True, sb=8, sa=4)
labeled("", "{{ location or campus }}")

doc.save(OUT)
print(f"Template saved to: {OUT}")
print(f"File size: {os.path.getsize(OUT)} bytes")

# Quick verify — render with dummy context
from docxtpl import DocxTemplate
dummy = DocxTemplate(OUT)
test_ctx = {
    "name_th": "ทดสอบ", "name_en": "Test", "curriculum_year": "พ.ศ. 2568",
    "department": "ภาควิชาทดสอบ", "campus": "วิทยาเขตทดสอบ",
    "university_name": "มหาวิทยาลัยทดสอบ",
    "program_code": "12345", "degree_name_th": "วศ.บ.", "degree_abbr_th": "วศ.บ.",
    "degree_name_en": "B.Eng.", "degree_abbr_en": "B.Eng.",
    "program_format": None, "program_category": None, "language": None,
    "admission_req": None, "cooperation": None, "degree_granting": None,
    "open_year": "2568", "readiness": None,
    "majors": [], "careers": ["วิศวกร", "นักพัฒนา"],
    "approvals": [{"committee": "คณะกรรมการ", "approval_date": "2567-12-27"}],
    "approval_details": "",
    "instructors": [{"name": "อ.ทดสอบ", "position": "ผู้ช่วยศาสตราจารย์", "degree": "วศ.ด."}],
    "location": "วิทยาลัยทดสอบ",
}
dummy.render(test_ctx)
dummy.save("/tmp/obe_rendered_test.docx")
print("Test render: OK -> /tmp/obe_rendered_test.docx")
