import os
import subprocess
import tempfile
from sqlalchemy.orm import Session, selectinload
from docxtpl import DocxTemplate
from models import Program

TEMPLATE_PATH = "templates/obe_test_template.docx"

def generate_component1_docx(program_id: int, db: Session) -> str:
    # 1. Fetch Program and Component 1 relations
    program = (
        db.query(Program)
        .options(
            selectinload(Program.majors),
            selectinload(Program.careers_list),
            selectinload(Program.approvals),
            selectinload(Program.instructors),
        )
        .filter(Program.id == program_id)
        .first()
    )
    if not program:
        return None

    # 2. Build context dictionary
    context = {
        "program_code": program.program_code or "",
        "name_th": program.name_th or "",
        "name_en": program.name_en or "",
        "degree_name_th": program.degree_name_th or "",
        "degree_abbr_th": program.degree_abbr_th or "",
        "degree_name_en": program.degree_name_en or "",
        "degree_abbr_en": program.degree_abbr_en or "",
        "university_name": program.university_name or "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ",
        "campus": program.campus or "วิทยาลัยเทคโนโลยีอุตสาหกรรม",
        "location": program.location or "วิทยาลัยเทคโนโลยีอุตสาหกรรม มจพ.",
        "program_format": program.program_format,
        "program_category": program.program_category,
        "language": program.language,
        "admission_req": program.admission_req,
        "cooperation": program.cooperation,
        "degree_granting": program.degree_granting,
        "open_year": program.open_year or "2568",
        "readiness": program.readiness,
        "majors": [m.major_name for m in program.majors],
        "careers": [c.career_name for c in program.careers_list],
        "approvals": [
            {"committee": a.committee, "approval_date": str(a.approval_date or "")}
            for a in program.approvals
        ],
        "instructors": [
            {
                "name": i.name,
                "position": i.position,
                "degree": i.degree,
            }
            for i in program.instructors
        ],
    }

    # 3. Render DOCX
    doc = DocxTemplate(TEMPLATE_PATH)
    doc.render(context)

    # 4. Save to temporary docx
    tmp_dir = tempfile.mkdtemp()
    docx_path = os.path.join(tmp_dir, f"OBE2_Component1_{program_id}.docx")
    doc.save(docx_path)
    return docx_path


def convert_docx_to_pdf(docx_path: str) -> str:
    """Uses LibreOffice in headless mode to convert .docx to .pdf"""
    out_dir = os.path.dirname(docx_path)
    cmd = [
        "soffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", out_dir,
        docx_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
    return pdf_path