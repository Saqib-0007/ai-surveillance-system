from pathlib import Path
import csv
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)


class ReportGenerator:

    def __init__(self, report_dir="reports"):

        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(exist_ok=True)

    def export_csv(
        self,
        events,
        filename="events.csv",
    ):

        csv_path = self.report_dir / filename

        with open(csv_path, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "Timestamp",
                    "Event",
                    "Label",
                    "Object ID",
                    "Details",
                ]
            )

            for event in events:

                writer.writerow(
                    [
                        event.get("timestamp", ""),
                        event.get("type", ""),
                        event.get("label", ""),
                        event.get("object_id", ""),
                        event.get("details", {}),
                    ]
                )

        return csv_path

    def export_pdf(
        self,
        events,
        analytics,
        filename="sentinel_vision_report.pdf",
    ):

        pdf_path = self.report_dir / filename

        doc = SimpleDocTemplate(str(pdf_path))

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b><font size=18>Sentinel Vision</font></b>",
                styles["Title"],
            )
        )

        story.append(
            Paragraph(
                "AI Surveillance Analytics Report",
                styles["Heading2"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                styles["Normal"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Analytics Summary</b>",
                styles["Heading2"],
            )
        )

        summary_table = Table(
            [
                ["Metric", "Value"],
                ["People", analytics["people"]],
                ["Vehicles", analytics["vehicles"]],
                ["Occupancy", analytics["occupancy"]],
                ["Queue Size", analytics["queue_size"]],
                [
                    "Average Wait",
                    f"{analytics['average_wait']:.1f} sec",
                ],
            ]
        )

        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ]
            )
        )

        story.append(summary_table)

        story.append(Spacer(1, 25))

        story.append(
            Paragraph(
                "<b>Recent Events</b>",
                styles["Heading2"],
            )
        )

        table_data = [
            [
                "Time",
                "Event",
                "Label",
                "ID",
            ]
        ]

        for event in events[-20:]:

            table_data.append(
                [
                    event.get("timestamp", ""),
                    event.get("type", ""),
                    event.get("label", ""),
                    str(event.get("object_id", "")),
                ]
            )

        events_table = Table(table_data)

        events_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ]
            )
        )

        story.append(events_table)

        doc.build(story)

        return pdf_path