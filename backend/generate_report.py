from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 8, 'Smart Feedback & Suggestion Portal', 0, 1, 'C')
        self.set_font('helvetica', 'B', 11)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, 'Final Project Completion & Progress Report', 0, 1, 'C')
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 8, f'Page {self.page_no()}', 0, 0, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=12)

# Content sections
content = [
    ("PROJECT STATUS", "Implementation updated; run the setup and test instructions in README.md before deployment.", True),
    ("", "", False),
    ("1. Architecture & Backend (Phases 1 - 4)", 
     "- Standard modular folder structure and PostgreSQL database schema with integrity constraints.\n"
     "- FastAPI REST backend with Pydantic v2 schemas, signed JWT authentication, and student/admin role guards.\n"
     "- Interactive Swagger UI documentation (/api/docs) and CORS support for local and deployed clients.", False),
    ("2. Natural Language Processing Pipeline (Phases 5 - 9)",
     "- Preprocessing: Tokenization, stopword cleaning with negation preservation, and WordNet lemmatization.\n"
     "- Sentiment Analysis: VADER when installed, with a lightweight offline fallback.\n"
     "- Classification & Urgency: Rule-based category mapping across academic, facilities, services, library, and placement categories.\n"
     "- Integrated into POST /api/feedback with automated unit & integration test suites.", False),
    ("3. React Frontend & Visual Analytics (Phases 10 - 13)",
     "- Modern React 18 + Vite + Tailwind CSS Single Page Application (SPA).\n"
     "- Student Portal: Dashboard metrics, feedback submission with live NLP analysis modal, and history.\n"
     "- Admin Dashboard: Interactive Recharts (Sentiment Pie, Category Bar, Department Stacked Bar, Trend Line), trending keyword cloud, actionable suggestions, and searchable feedback table.", False),
    ("4. Quality Assurance, Build & Viva Guide (Phases 14 - 16)",
     "- NLP unit tests are included in tests/ml/; API integration tests are included in tests/backend/.\n"
     "- Build locally with npm run build after installing frontend dependencies.\n"
     "- Full documentation: system_design.md, data_dictionary.md, api_specification.md, and viva_preparation_guide.md.", False),
    ("", "", False),
    ("CREDENTIALS & HOW TO RUN", "", True),
    ("FastAPI Backend", "cd backend && uvicorn main:app --reload (Port 8000)", False),
    ("React Frontend", "cd frontend && npm run dev (Port 5173)", False),
    ("Admin Account", "Created on first startup from ADMIN_EMAIL and ADMIN_PASSWORD in backend/.env.", False),
    ("Student Account", "Register a student account from the portal; public registration cannot create administrators.", False),
]

for title, text, is_header in content:
    if is_header:
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 7, title, 0, 1, 'L')
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
        pdf.ln(2)
    else:
        if title:
            pdf.set_font('helvetica', 'B', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 5, title, 0, 1, 'L')
        if text:
            pdf.set_font('helvetica', '', 9.5)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 4.5, text)
            pdf.ln(2.5)

output_path = os.path.join(os.path.dirname(__file__), "..", "Progress_Report.pdf")
pdf.output(output_path)
print(f"Final PDF successfully generated at: {output_path}")
