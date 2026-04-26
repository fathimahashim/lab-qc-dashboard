from fpdf import FPDF
import pandas as pd

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Laboratory QC Report - Wine Quality Analysis', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(df, analysis, charts, deviations, date_range, output_path):
    pdf = PDFReport()
    pdf.add_page()
    
    # Summary stats table
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Process Summary', 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 10)
    for param, stats in analysis.items():
        pdf.cell(30, 8, param, 1)
        pdf.cell(20, 8, f'{stats["mean"]:.2f}', 1, 0, 'C')
        pdf.cell(20, 8, f'{stats["std"]:.2f}', 1, 0, 'C')
        pdf.cell(20, 8, f'{stats["Cp"]:.2f}', 1, 0, 'C')
        pdf.cell(20, 8, f'{stats["Cpk"]:.2f}', 1, 1, 'C')
    
    # Deviations
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Deviation Log', 0, 1)
    if not deviations.empty:
        for _, row in deviations.iterrows():
            pdf.cell(0, 8, f'{row["Parameter"]}: {row["Issue"]}', 0, 1)
    else:
        pdf.cell(0, 8, 'No significant deviations detected', 0, 1)
    
    pdf.output(output_path)
    print(f"✅ PDF saved: {output_path}")