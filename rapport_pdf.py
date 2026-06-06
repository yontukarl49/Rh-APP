import os
from datetime import datetime

try:
    from fpdf import FPDF
    FPDF_DISPONIBLE = True
except ImportError:
    FPDF_DISPONIBLE = False


DOSSIER_RAPPORTS = "rapports"


def creer_dossier_rapports():
    """Cree le dossier de rapports s'il n'existe pas."""
    if not os.path.exists(DOSSIER_RAPPORTS):
        os.makedirs(DOSSIER_RAPPORTS)


class RapportPDF(FPDF):
    

    def header(self):
        
        self.set_font("DejaVu", size=14)
        self.set_text_color(30, 30, 120)
        self.cell(0, 10, "Systeme RH - Rapport", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(30, 30, 120)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        
        self.set_y(-15)
        self.set_font("DejaVu", size=8)
        self.set_text_color(128, 128, 128)
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(0, 10, f"Genere le {date_str} - Page {self.page_no()}", align="C")


def sauvegarder_rapport_pdf(contenu: str, nom_fichier: str):
    
    if not FPDF_DISPONIBLE:
        print("[AVERTISSEMENT] fpdf2 n'est pas installe.")
        print("Executez : pip install fpdf2 --break-system-packages")
        return

    creer_dossier_rapports()
    chemin = os.path.join(DOSSIER_RAPPORTS, f"{nom_fichier}.pdf")

    pdf = RapportPDF()
    pdf.set_margins(15, 20, 15)

    pdf.add_font("DejaVu", fname="DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", style="B", fname="DejaVuSans-Bold.ttf", uni=True)

    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.set_font("DejaVu", size=10)
    pdf.set_text_color(20, 20, 20)

    for ligne in contenu.splitlines():
        if ligne.startswith("="):
            pdf.set_font("DejaVu", style="B", size=10)
            pdf.set_text_color(30, 30, 120)
        elif ligne.strip().startswith("--"):
            pdf.set_font("DejaVu", style="B", size=9)
            pdf.set_text_color(60, 60, 60)
        else:
            pdf.set_font("DejaVu", size=10)
            pdf.set_text_color(20, 20, 20)

        pdf.multi_cell(0, 6, ligne, new_x="LMARGIN", new_y="NEXT")

    pdf.output(chemin)
    print(f"[OK] Rapport PDF sauvegarde : {chemin}")