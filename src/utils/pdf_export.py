from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape


def generate_pdf(df, output_file):

    pdf = SimpleDocTemplate(
        output_file,
        pagesize=landscape(A4)
    )

    # Keep only important columns
    export_df = df[
        [
            "ID",
            "Complaint",
            "Category",
            "Department",
            "Evidence Status",
            "Status",
            "Created At"
        ]
    ]

    data = [list(export_df.columns)]

    for row in export_df.values.tolist():
        data.append(row)

    table = Table(
        data,
        colWidths=[
            35,     # ID
            200,    # Complaint
            70,     # Category
            140,    # Department
            120,    # Evidence Status
            70,     # Status
            90      # Created At
        ]
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("FONTSIZE", (0, 0), (-1, -1), 9),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
    )

    pdf.build([table])