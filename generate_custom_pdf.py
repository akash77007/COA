"""
Custom PDF Generator for Akash Sharma
Computer Organization & Architecture (ENCA302)
Generates an executive, modern, visually distinct academic report.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable, Preformatted
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and render total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        width, height = A4
        margin = 36

        if self._pageNumber > 1:
            self.saveState()
            
            # --- Header ---
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1E3A8A")) # Deep Royal Blue
            self.drawString(margin, height - 25, "Akash Sharma | Roll: 2401201108")

            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B")) # Slate
            self.drawRightString(width - margin, height - 25, "ENCA302: Cache Memory Mapping Simulation")

            # Running header line
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(margin, height - 29, width - margin, height - 29)
            
            # Accent tick on header
            self.setStrokeColor(colors.HexColor("#0284C7")) # Cyan / Sky
            self.setLineWidth(1.5)
            self.line(margin, height - 29, margin + 60, height - 29)

            # --- Footer ---
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(margin, 35, width - margin, 35)

            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(margin, 23, "K.R. Mangalam University — School of Engineering and Technology")
            self.drawRightString(width - margin, 23, f"Page {self._pageNumber} of {page_count}")

            self.restoreState()
        else:
            # First page clean footer
            self.saveState()
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(margin, 35, width - margin, 35)

            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(margin, 23, "K.R. Mangalam University — Department of Computer Science & Engineering")
            self.drawRightString(width - margin, 23, "Academic Session 2025–2026")
            self.restoreState()


def build_pdf(filename="Akash_Sharma_2401201108_COA_Assignment2.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    # --- Color Palette ---
    C_PRIMARY = colors.HexColor("#0F2C59")    # Deep Navy
    C_SECONDARY = colors.HexColor("#1E3A8A")  # Royal Blue
    C_ACCENT = colors.HexColor("#0284C7")     # Sky Blue
    C_TEXT = colors.HexColor("#1E293B")       # Dark Charcoal Slate
    C_MUTED = colors.HexColor("#475569")      # Muted Slate
    C_CARD_BG = colors.HexColor("#F8FAFC")    # Very light slate
    C_BORDER = colors.HexColor("#E2E8F0")     # Light border

    # --- Typography Styles ---
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=25,
        textColor=C_PRIMARY,
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=C_MUTED,
        alignment=1
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=C_PRIMARY,
        spaceBefore=8,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=C_SECONDARY,
        spaceBefore=6,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=C_TEXT,
        spaceAfter=3
    )

    caption_style = ParagraphStyle(
        "Caption_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=10,
        textColor=C_MUTED,
        alignment=1,
        spaceAfter=4
    )

    pre_style = ParagraphStyle(
        "PreStyle",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=6.5,
        leading=8.2,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F8FAFC"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.75,
        borderPadding=6,
        spaceAfter=6
    )

    table_header_style = ParagraphStyle(
        "TH_Style",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        "TD_Style",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=C_TEXT,
        alignment=1
    )

    table_cell_left = ParagraphStyle(
        "TD_Style_Left",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=C_TEXT,
        alignment=0
    )

    hit_style = ParagraphStyle(
        "Hit_Style",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#15803D"),
        alignment=1
    )

    miss_style = ParagraphStyle(
        "Miss_Style",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#B91C1C"),
        alignment=1
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 10))
    if os.path.exists("docs/krmu_logo.png"):
        logo = Image("docs/krmu_logo.png", width=95, height=95)
        logo.hAlign = 'CENTER'
        story.append(logo)
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("K.R. MANGALAM UNIVERSITY", ParagraphStyle(
        "UnivTitle", fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=C_PRIMARY, alignment=1
    )))
    story.append(Paragraph("School of Engineering and Technology", ParagraphStyle(
        "SchoolTitle", fontName="Helvetica", fontSize=12, leading=16, textColor=C_MUTED, alignment=1
    )))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", ParagraphStyle(
        "DeptTitle", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=C_ACCENT, alignment=1
    )))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="80%", thickness=1.5, color=C_SECONDARY, spaceBefore=4, spaceAfter=12))

    # Title Card
    title_card_data = [
        [Paragraph("ACADEMIC LAB EXPERIMENT & SIMULATION REPORT", ParagraphStyle(
            "Badge", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=C_ACCENT, alignment=1
        ))],
        [Spacer(1, 4)],
        [Paragraph("Cache Memory Mapping & Architecture Simulator", title_style)],
        [Spacer(1, 4)],
        [Paragraph("Empirical Investigation of Direct-Mapped, 2-Way Set-Associative, and Fully Associative Placement Policies under Benchmark & Stress Access Patterns", subtitle_style)]
    ]
    title_card = Table(title_card_data, colWidths=[510])
    title_card.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(title_card)

    story.append(Spacer(1, 18))

    # Metadata Cards (2 Columns: Student on Left, Course on Right)
    left_meta = [
        [Paragraph("<b>STUDENT DETAILS</b>", ParagraphStyle("HMeta", fontName="Helvetica-Bold", fontSize=8.5, textColor=C_SECONDARY))],
        [Paragraph("<b>Name:</b> Akash Sharma", body_style)],
        [Paragraph("<b>Roll Number:</b> 2401201108", body_style)],
        [Paragraph("<b>Program:</b> BCA (AI & Data Science)", body_style)],
        [Paragraph("<b>Section:</b> Section B", body_style)],
        [Paragraph("<b>Semester:</b> Academic Year 2025–2026", body_style)],
    ]
    right_meta = [
        [Paragraph("<b>COURSE & EVALUATION</b>", ParagraphStyle("HMeta", fontName="Helvetica-Bold", fontSize=8.5, textColor=C_SECONDARY))],
        [Paragraph("<b>Course Title:</b> Computer Organization & Architecture", body_style)],
        [Paragraph("<b>Course Code:</b> ENCA302", body_style)],
        [Paragraph("<b>Course Coordinator:</b> Ms. Alina Banerjee", body_style)],
        [Paragraph("<b>Institution:</b> K.R. Mangalam University", body_style)],
        [Paragraph("<b>Status:</b> Completed & Verified", body_style)],
    ]

    meta_table_data = [
        [
            Table(left_meta, colWidths=[240]),
            Table(right_meta, colWidths=[240])
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[255, 255])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (0,0), 1, C_BORDER),
        ('BOX', (1,0), (1,0), 1, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 18))

    # GitHub Repository Card
    repo_data = [
        [Paragraph("<b>Verified GitHub Source Code & Experimental Artifacts:</b>", ParagraphStyle("RepoH", fontName="Helvetica-Bold", fontSize=8.5, textColor=C_PRIMARY, alignment=1))],
        [Paragraph('<link href="https://github.com/akash77007/COA"><u><font color="#0284C7"><b>https://github.com/akash77007/COA</b></font></u></link>', ParagraphStyle("RepoLink", fontName="Helvetica-Bold", fontSize=9.5, textColor=C_ACCENT, alignment=1))]
    ]
    repo_table = Table(repo_data, colWidths=[510])
    repo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0F9FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BAE6FD")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(repo_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: PROBLEM STATEMENT & CACHE ARCHITECTURAL MODELS
    # =========================================================================
    story.append(Paragraph("1. Problem Statement & Experimental Objectives", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceBefore=2, spaceAfter=6))

    q_box = [
        [Paragraph("<b>Assignment Specification (Question 2: Cache Mapping Simulation):</b><br/>"
                   "Develop a simulation comparing memory block placement using <b>Direct-Mapped</b>, "
                   "<b>Set-Associative</b>, and <b>Fully Associative</b> cache architectures. "
                   "Given a small cache of <b>4 cache lines</b> (L0, L1, L2, L3) and memory block request sequence "
                   "<b>[0, 4, 8, 0, 4, 12]</b>, display for each request the selected cache location, hit/miss status, "
                   "and total performance metrics. Provide an empirical and theoretical explanation of which mapping "
                   "delivers superior placement flexibility.", body_style)]
    ]
    t_qbox = Table(q_box, colWidths=[510])
    t_qbox.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_qbox)
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. Architectural Organization of the Three Mapping Paradigms", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "All three configurations manage exactly four physical cache lines (L0, L1, L2, L3), but they differ "
        "in how these lines are clustered into sets. When an access arrives, the block address <i>B</i> is decoded into "
        "a <b>Set Index</b> and a <b>Tag</b>:", body_style
    ))

    # Architecture Overview Table
    arch_table_data = [
        [Paragraph("Mapping Architecture", table_header_style),
         Paragraph("Organization", table_header_style),
         Paragraph("Set Index Formula", table_header_style),
         Paragraph("Placement Freedom", table_header_style),
         Paragraph("Hardware Complexity", table_header_style)],
        [Paragraph("<b>Direct-Mapped</b>", table_cell_left),
         Paragraph("4 Sets × 1 Way", table_cell_style),
         Paragraph("Set = B mod 4", table_cell_style),
         Paragraph("Rigid: Exactly 1 target line", table_cell_left),
         Paragraph("Minimal (1 Comparator)", table_cell_left)],
        [Paragraph("<b>2-Way Set-Associative</b>", table_cell_left),
         Paragraph("2 Sets × 2 Ways", table_cell_style),
         Paragraph("Set = B mod 2", table_cell_style),
         Paragraph("Moderate: 2 lines per set (LRU)", table_cell_left),
         Paragraph("Medium (2 Comparators)", table_cell_left)],
        [Paragraph("<b>Fully Associative</b>", table_cell_left),
         Paragraph("1 Set × 4 Ways", table_cell_style),
         Paragraph("Set = 0 (No index)", table_cell_style),
         Paragraph("Universal: Any of 4 lines (LRU)", table_cell_left),
         Paragraph("High (4 Comparators)", table_cell_left)],
    ]
    t_arch = Table(arch_table_data, colWidths=[110, 85, 95, 120, 100])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SECONDARY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
        ('BACKGROUND', (0,2), (-1,2), C_CARD_BG),
        ('BACKGROUND', (0,3), (-1,3), colors.white),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 8))

    if os.path.exists("docs/screenshots/architecture.png"):
        img_arch = Image("docs/screenshots/architecture.png", width=490, height=220)
        img_arch.hAlign = 'CENTER'
        story.append(img_arch)
        story.append(Paragraph("<b>Figure 1:</b> Architectural request pipeline and line partitioning across Direct-Mapped, 2-Way, and Fully Associative caches.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ADDRESS SPLIT & WORKED EXAMPLE (CYCLE 3 BLOCK 8)
    # =========================================================================
    story.append(Paragraph("3. Address Decoding and Set Contention Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "Each requested block number <i>B</i> is partitioned based on the number of sets in the cache. "
        "Because all four requested blocks (0, 4, 8, 12) are integer multiples of 4, they create an aggressive "
        "indexing collision pattern:", body_style
    ))

    # Bit decomposition table
    bits_data = [
        [Paragraph("Block", table_header_style),
         Paragraph("Binary", table_header_style),
         Paragraph("Direct Tag", table_header_style),
         Paragraph("Direct Set (mod 4)", table_header_style),
         Paragraph("2-Way Tag", table_header_style),
         Paragraph("2-Way Set (mod 2)", table_header_style),
         Paragraph("Fully Assoc Tag", table_header_style)],
        [Paragraph("0", table_cell_style), Paragraph("0000", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0 (L0)", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0 (Set 0)", table_cell_style), Paragraph("0", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("0100", table_cell_style), Paragraph("1", table_cell_style), Paragraph("0 (L0)", table_cell_style), Paragraph("2", table_cell_style), Paragraph("0 (Set 0)", table_cell_style), Paragraph("4", table_cell_style)],
        [Paragraph("8", table_cell_style), Paragraph("1000", table_cell_style), Paragraph("2", table_cell_style), Paragraph("0 (L0)", table_cell_style), Paragraph("4", table_cell_style), Paragraph("0 (Set 0)", table_cell_style), Paragraph("8", table_cell_style)],
        [Paragraph("12", table_cell_style), Paragraph("1100", table_cell_style), Paragraph("3", table_cell_style), Paragraph("0 (L0)", table_cell_style), Paragraph("6", table_cell_style), Paragraph("0 (Set 0)", table_cell_style), Paragraph("12", table_cell_style)],
    ]
    t_bits = Table(bits_data, colWidths=[55, 65, 75, 85, 70, 85, 75])
    t_bits.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
        ('BACKGROUND', (0,2), (-1,2), C_CARD_BG),
        ('BACKGROUND', (0,3), (-1,3), colors.white),
        ('BACKGROUND', (0,4), (-1,4), C_CARD_BG),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_bits)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. Step-by-Step Cycle Analysis (Worked Example: Arrival of Block 8 at Cycle 3)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "To rigorously trace how placement constraints dictate data retention, consider <b>Cycle 3</b> when <b>Block 8</b> arrives. "
        "Prior to Cycle 3, Block 0 (Cycle 1) and Block 4 (Cycle 2) were already requested:", body_style
    ))

    # Worked example breakdown card
    wk_data = [
        [Paragraph("<b>Direct-Mapped (Cycle 3):</b> Target line = 8 mod 4 = <b>0</b>. Line L0 currently holds Block 4. Result: <b>CONFLICT MISS</b>. Block 4 is evicted immediately, leaving L0 holding [8], while lines L1, L2, L3 remain completely empty.", body_style)],
        [Paragraph("<b>2-Way Set-Associative (Cycle 3):</b> Target set = 8 mod 2 = <b>0</b>. Set 0 currently contains Block 0 (L0) and Block 4 (L1). Result: <b>CONFLICT MISS</b>. Because both lines in Set 0 are full, LRU evicts the oldest entry (<b>Block 0</b>). Block 8 replaces it in L0, yielding Set 0 = [L0: 8, L1: 4].", body_style)],
        [Paragraph("<b>Fully Associative (Cycle 3):</b> Target = Any cache line. Block 8 is looked up in parallel across all lines and not found. Result: <b>COMPULSORY MISS</b>. However, line <b>L2 is vacant</b>! Block 8 is loaded directly into L2 with <b>zero evictions</b>: [L0: 0, L1: 4, L2: 8, L3: -].", body_style)],
    ]
    t_wk = Table(wk_data, colWidths=[510])
    t_wk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#FEF2F2")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FFFBEB")),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_wk)
    story.append(Spacer(1, 6))

    if os.path.exists("docs/screenshots/shot_check1.png"):
        img_check1 = Image("docs/screenshots/shot_check1.png", width=490, height=215)
        img_check1.hAlign = 'CENTER'
        story.append(img_check1)
        story.append(Paragraph("<b>Figure 2:</b> Terminal execution capture highlighting Cycle 3 Block 8 arrival and eviction comparisons.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: SIMULATION EXECUTION TRACES (DIRECT & 2-WAY)
    # =========================================================================
    story.append(Paragraph("5. Empirical Simulation Execution Traces", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("5.1 Direct-Mapped Cache Trace (Sets = 4, Ways/Set = 1)", h2_style))
    story.append(Paragraph("Every requested block maps strictly to line <code>Block mod 4 = 0</code> (Line L0), inducing severe thrashing:", body_style))

    dm_rows = [
        [Paragraph("Step", table_header_style), Paragraph("Block", table_header_style), Paragraph("Tag", table_header_style),
         Paragraph("Set", table_header_style), Paragraph("Line", table_header_style), Paragraph("Result", table_header_style),
         Paragraph("Evicted", table_header_style), Paragraph("Cache Contents [L0, L1, L2, L3]", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L0", table_cell_style), Paragraph("MISS", miss_style), Paragraph("—", table_cell_style), Paragraph("[0, -, -, -]", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("4", table_cell_style), Paragraph("1", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L0", table_cell_style), Paragraph("MISS", miss_style), Paragraph("0", table_cell_style), Paragraph("[4, -, -, -]", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("8", table_cell_style), Paragraph("2", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L0", table_cell_style), Paragraph("MISS", miss_style), Paragraph("4", table_cell_style), Paragraph("[8, -, -, -]", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L0", table_cell_style), Paragraph("MISS", miss_style), Paragraph("8", table_cell_style), Paragraph("[0, -, -, -]", table_cell_style)],
        [Paragraph("5", table_cell_style), Paragraph("4", table_cell_style), Paragraph("1", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L0", table_cell_style), Paragraph("MISS", miss_style), Paragraph("0", table_cell_style), Paragraph("[4, -, -, -]", table_cell_style)],
        [Paragraph("6", table_cell_style), Paragraph("12", table_cell_style), Paragraph("3", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L0", table_cell_style), Paragraph("MISS", miss_style), Paragraph("4", table_cell_style), Paragraph("[12, -, -, -]", table_cell_style)],
    ]
    t_dm = Table(dm_rows, colWidths=[40, 45, 40, 40, 45, 60, 55, 185])
    t_dm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
    ]))
    story.append(t_dm)
    story.append(Paragraph("<b>Direct-Mapped Result:</b> Hits = 0, Misses = 6, Hit Rate = <b>0.00%</b> (100% Conflict Thrashing on L0).", caption_style))

    if os.path.exists("docs/screenshots/shot_direct.png"):
        img_dm = Image("docs/screenshots/shot_direct.png", width=490, height=130)
        img_dm.hAlign = 'CENTER'
        story.append(img_dm)
        story.append(Spacer(1, 4))

    story.append(Paragraph("5.2 2-Way Set-Associative Cache Trace (Sets = 2, Ways/Set = 2, LRU)", h2_style))
    story.append(Paragraph("All even block numbers map into Set 0. The 2-way capacity of Set 0 cannot retain the 3-block active working set {0, 4, 8}:", body_style))

    sa_rows = [
        [Paragraph("Step", table_header_style), Paragraph("Block", table_header_style), Paragraph("Tag", table_header_style),
         Paragraph("Set", table_header_style), Paragraph("Line", table_header_style), Paragraph("Result", table_header_style),
         Paragraph("Evicted", table_header_style), Paragraph("Cache Contents [L0, L1, L2, L3]", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L0", table_cell_style), Paragraph("MISS", miss_style), Paragraph("—", table_cell_style), Paragraph("[0, -, -, -]", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("4", table_cell_style), Paragraph("2", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L1", table_cell_style), Paragraph("MISS", miss_style), Paragraph("—", table_cell_style), Paragraph("[0, 4, -, -]", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("8", table_cell_style), Paragraph("4", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L0", table_cell_style), Paragraph("MISS", miss_style), Paragraph("0", table_cell_style), Paragraph("[8, 4, -, -]", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L1", table_cell_style), Paragraph("MISS", miss_style), Paragraph("4", table_cell_style), Paragraph("[8, 0, -, -]", table_cell_style)],
        [Paragraph("5", table_cell_style), Paragraph("4", table_cell_style), Paragraph("2", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L0", table_cell_style), Paragraph("MISS", miss_style), Paragraph("8", table_cell_style), Paragraph("[4, 0, -, -]", table_cell_style)],
        [Paragraph("6", table_cell_style), Paragraph("12", table_cell_style), Paragraph("6", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L1", table_cell_style), Paragraph("MISS", miss_style), Paragraph("0", table_cell_style), Paragraph("[4, 12, -, -]", table_cell_style)],
    ]
    t_sa = Table(sa_rows, colWidths=[40, 45, 40, 40, 45, 60, 55, 185])
    t_sa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
    ]))
    story.append(t_sa)
    story.append(Paragraph("<b>2-Way Set-Associative Result:</b> Hits = 0, Misses = 6, Hit Rate = <b>0.00%</b> (LRU prematurely evicts blocks before reuse).", caption_style))

    if os.path.exists("docs/screenshots/shot_setassoc.png"):
        img_sa = Image("docs/screenshots/shot_setassoc.png", width=490, height=130)
        img_sa.hAlign = 'CENTER'
        story.append(img_sa)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: FULLY ASSOCIATIVE TRACE & PERFORMANCE MATRIX
    # =========================================================================
    story.append(Paragraph("5.3 Fully Associative Cache Trace (Sets = 1, Ways/Set = 4, Global LRU)", h2_style))
    story.append(Paragraph("Universal line selection enables all distinct blocks to reside concurrently without collision:", body_style))

    fa_rows = [
        [Paragraph("Step", table_header_style), Paragraph("Block", table_header_style), Paragraph("Tag", table_header_style),
         Paragraph("Set", table_header_style), Paragraph("Line", table_header_style), Paragraph("Result", table_header_style),
         Paragraph("Evicted", table_header_style), Paragraph("Cache Contents [L0, L1, L2, L3]", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L0", table_cell_style), Paragraph("MISS", miss_style), Paragraph("—", table_cell_style), Paragraph("[0, -, -, -]", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("4", table_cell_style), Paragraph("4", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L1", table_cell_style), Paragraph("MISS", miss_style), Paragraph("—", table_cell_style), Paragraph("[0, 4, -, -]", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("8", table_cell_style), Paragraph("8", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L2", table_cell_style), Paragraph("MISS", miss_style), Paragraph("—", table_cell_style), Paragraph("[0, 4, 8, -]", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L0", table_cell_style), Paragraph("HIT", hit_style), Paragraph("—", table_cell_style), Paragraph("[0, 4, 8, -]", table_cell_style)],
        [Paragraph("5", table_cell_style), Paragraph("4", table_cell_style), Paragraph("4", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L1", table_cell_style), Paragraph("HIT", hit_style), Paragraph("—", table_cell_style), Paragraph("[0, 4, 8, -]", table_cell_style)],
        [Paragraph("6", table_cell_style), Paragraph("12", table_cell_style), Paragraph("12", table_cell_style), Paragraph("0", table_cell_style), Paragraph("L3", table_cell_style), Paragraph("MISS", miss_style), Paragraph("—", table_cell_style), Paragraph("[0, 4, 8, 12]", table_cell_style)],
    ]
    t_fa = Table(fa_rows, colWidths=[40, 45, 40, 40, 45, 60, 55, 185])
    t_fa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
    ]))
    story.append(t_fa)
    story.append(Paragraph("<b>Fully Associative Result:</b> Hits = 2, Misses = 4, Hit Rate = <b>33.33%</b> (Successfully captures temporal reuse on blocks 0 and 4).", caption_style))

    if os.path.exists("docs/screenshots/shot_full.png"):
        img_fa = Image("docs/screenshots/shot_full.png", width=490, height=125)
        img_fa.hAlign = 'CENTER'
        story.append(img_fa)
        story.append(Spacer(1, 4))

    story.append(Paragraph("6. Quantitative Evaluation & AMAT Performance Modeling", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceBefore=2, spaceAfter=6))

    # Summary performance table
    perf_rows = [
        [Paragraph("Architecture", table_header_style), Paragraph("Hits", table_header_style), Paragraph("Misses", table_header_style),
         Paragraph("Hit Rate", table_header_style), Paragraph("Miss Rate", table_header_style), Paragraph("Occupancy", table_header_style), Paragraph("Space Utilisation", table_header_style)],
        [Paragraph("<b>Direct-Mapped</b>", table_cell_left), Paragraph("0", table_cell_style), Paragraph("6", table_cell_style), Paragraph("0.00%", table_cell_style), Paragraph("100.00%", table_cell_style), Paragraph("1 / 4 lines", table_cell_style), Paragraph("25.0%", table_cell_style)],
        [Paragraph("<b>2-Way Set-Associative</b>", table_cell_left), Paragraph("0", table_cell_style), Paragraph("6", table_cell_style), Paragraph("0.00%", table_cell_style), Paragraph("100.00%", table_cell_style), Paragraph("2 / 4 lines", table_cell_style), Paragraph("50.0%", table_cell_style)],
        [Paragraph("<b>Fully Associative</b>", table_cell_left), Paragraph("<b>2</b>", hit_style), Paragraph("<b>4</b>", table_cell_style), Paragraph("<b>33.33%</b>", hit_style), Paragraph("66.67%", table_cell_style), Paragraph("<b>4 / 4 lines</b>", table_cell_style), Paragraph("<b>100.0%</b>", hit_style)],
    ]
    t_perf = Table(perf_rows, colWidths=[120, 50, 55, 65, 65, 80, 75])
    t_perf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
        ('BACKGROUND', (0,2), (-1,2), C_CARD_BG),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#F0FDF4")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_perf)
    story.append(Spacer(1, 6))

    # AMAT Box with clean typography
    amat_data = [
        [Paragraph("<b>Average Memory Access Time (AMAT) Analysis:</b><br/>"
                   "Assuming a realistic L1 Hit Time <i>t<sub>hit</sub></i> = 1 cycle and Main Memory Miss Penalty <i>t<sub>miss</sub></i> = 50 cycles:<br/>"
                   "• <b>Direct-Mapped:</b> AMAT = 1 + (1.0000 × 50) = <b>51.00 cycles</b><br/>"
                   "• <b>2-Way Set-Associative:</b> AMAT = 1 + (1.0000 × 50) = <b>51.00 cycles</b><br/>"
                   "• <b>Fully Associative:</b> AMAT = 1 + (0.6667 × 50) = <b>34.33 cycles</b><br/>"
                   "<b>Architectural Impact:</b> Fully Associative reduces average memory latency by <b>32.7%</b> (1.49× effective speedup) purely through placement flexibility.", body_style)]
    ]
    t_amat = Table(amat_data, colWidths=[510])
    t_amat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_amat)

    if os.path.exists("docs/screenshots/shot_summary.png"):
        img_sum = Image("docs/screenshots/shot_summary.png", width=490, height=155)
        img_sum.hAlign = 'CENTER'
        story.append(Spacer(1, 4))
        story.append(img_sum)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: EXTENDED EXPERIMENTS (TEST 1, 2, 3)
    # =========================================================================
    story.append(Paragraph("7. Extended Experimental Validation & Stress Testing", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "To verify that the simulator generalizes beyond the question's specific access sequence, three additional "
        "independent test scenarios were executed via <code>python cache_simulator.py --all</code>:", body_style
    ))

    ext_rows = [
        [Paragraph("Experiment", table_header_style), Paragraph("Sequence", table_header_style),
         Paragraph("Direct-Mapped", table_header_style), Paragraph("2-Way Assoc", table_header_style),
         Paragraph("Fully Assoc", table_header_style), Paragraph("Architectural Insight", table_header_style)],
        [Paragraph("<b>Test 1: Disjoint Blocks</b>", table_cell_left),
         Paragraph("0, 1, 0, 1, 0, 1", table_cell_style),
         Paragraph("4H / 2M (66.7%)", table_cell_style),
         Paragraph("4H / 2M (66.7%)", table_cell_style),
         Paragraph("4H / 2M (66.7%)", table_cell_style),
         Paragraph("When working set has no index conflicts (0 mod 4 = 0, 1 mod 4 = 1), DM performs identically to FA with simpler hardware.", table_cell_left)],
        [Paragraph("<b>Test 2: Set Contention</b>", table_cell_left),
         Paragraph("2, 6, 10, 14, 2, 6", table_cell_style),
         Paragraph("0H / 6M (0.0%)", table_cell_style),
         Paragraph("0H / 6M (0.0%)", table_cell_style),
         Paragraph("2H / 4M (33.3%)", table_cell_style),
         Paragraph("Stride-4 accesses all target Set 0 (Line L2 in DM). Demonstrates that stride matching set count cripples fixed-index caches.", table_cell_left)],
        [Paragraph("<b>Test 3: Capacity Flushing</b>", table_cell_left),
         Paragraph("0, 1, 2, 3, 4, 5, 0, 1", table_cell_style),
         Paragraph("0H / 8M (0.0%)", table_cell_style),
         Paragraph("0H / 8M (0.0%)", table_cell_style),
         Paragraph("0H / 8M (0.0%)", table_cell_style),
         Paragraph("6 distinct blocks exceed the 4-line capacity limit. LRU evicts older blocks across all three, demonstrating the capacity boundary.", table_cell_left)],
    ]
    t_ext = Table(ext_rows, colWidths=[105, 80, 75, 75, 75, 100])
    t_ext.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
        ('BACKGROUND', (0,2), (-1,2), C_CARD_BG),
        ('BACKGROUND', (0,3), (-1,3), colors.white),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ext)
    story.append(Spacer(1, 8))

    story.append(Paragraph("8. Space Utilisation and Eviction Behavior Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceBefore=2, spaceAfter=6))

    obs_card_data = [
        [Paragraph("<b>1. Spatial Waste in Fixed-Index Caches:</b> In the benchmark sequence, Direct-Mapped uses only 25% of its available storage (Line L0), leaving L1–L3 idle. 2-Way Set-Associative uses only 50% (Set 0). Fully Associative achieves 100% space utilisation by placing each unique block into an available line.", body_style)],
        [Paragraph("<b>2. Temporal Locality Retention:</b> A cache hit requires retaining previously requested data until it is reused. Because the benchmark re-accesses blocks 0 and 4, any mapping that evicts them before Cycle 4 and 5 misses completely. Fully Associative successfully retains both.", body_style)],
        [Paragraph("<b>3. The Law of Associativity:</b> Associativity eliminates conflict misses caused by unfavorable strides. However, it cannot prevent compulsory misses (first-touch) nor capacity misses (when the unique footprint exceeds cache size C).", body_style)]
    ]
    t_obs = Table(obs_card_data, colWidths=[510])
    t_obs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_obs)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: OBJECT-ORIENTED SIMULATION ENGINE (CODE LISTING)
    # =========================================================================
    story.append(Paragraph("9. Full Python Simulation Engine Implementation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceBefore=2, spaceAfter=6))
    story.append(Paragraph("Architectural simulation engine (<code>cache_simulator.py</code>) implementing physical <code>CacheLine</code>, <code>CacheSet</code>, and <code>CacheMemory</code> hardware abstractions with LRU replacement logic:", body_style))

    # Read source code from cache_simulator.py
    code_text = ""
    if os.path.exists("cache_simulator.py"):
        with open("cache_simulator.py", "r", encoding="utf-8") as f:
            code_text = f.read()

    p_engine_end = code_text.find("def display_trace")
    code_part1 = code_text[:p_engine_end].strip()
    code_part2 = code_text[p_engine_end:].strip()

    story.append(Paragraph("<b>Part A: Hardware Architecture Models (CacheLine, CacheSet, CacheMemory)</b>", h2_style))
    story.append(Preformatted(code_part1, pre_style))

    story.append(PageBreak())

    story.append(Paragraph("<b>Part B: Simulation Pipeline & Benchmark Execution Suite</b>", h2_style))
    story.append(Preformatted(code_part2, pre_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 10 & 11: CONCLUSIONS, TRADE-OFFS & REPRODUCIBILITY
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("10. Architectural Conclusions & Hardware Engineering Trade-Offs", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceBefore=2, spaceAfter=6))

    conc_box_data = [
        [Paragraph("<b>Summary of Findings & Design Trade-Offs:</b><br/>"
                   "1. <b>Superior Flexibility:</b> For the benchmark access sequence <code>[0, 4, 8, 0, 4, 12]</code>, <b>Fully Associative Cache</b> provides unequivocally superior placement flexibility, achieving a <b>33.33% hit rate</b> compared to <b>0.00%</b> for both Direct-Mapped and 2-Way Set-Associative designs.<br/>"
                   "2. <b>Hardware vs Performance Trade-Off:</b> While Fully Associative eliminates conflict misses, it requires <b>N parallel comparators</b> and intricate global LRU tracking circuits. As cache capacity scales to megabytes, fully associative lookup becomes prohibitively expensive in terms of silicon area, power dissipation, and critical path cycle delay.<br/>"
                   "3. <b>Industry Design Consensus:</b> Modern microprocessor architectures (e.g., Intel Core, AMD Zen, ARM Cortex) utilize <b>Set-Associative Caches</b> (typically 8-way to 16-way associative) for L1 and L2 caches as an optimal engineering balance between hardware simplicity and conflict miss mitigation.", body_style)]
    ]
    t_conc = Table(conc_box_data, colWidths=[510])
    t_conc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_conc)
    story.append(Spacer(1, 6))

    story.append(Paragraph("11. Reproducibility & Execution Verification Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceBefore=2, spaceAfter=6))

    # Repro Card
    repro_data = [
        [Paragraph("<b>Command-Line Execution Instructions:</b>", ParagraphStyle("RPH", fontName="Helvetica-Bold", fontSize=8, textColor=C_PRIMARY))],
        [Paragraph("<code># 1. Execute primary question benchmark [0, 4, 8, 0, 4, 12]:<br/>"
                   "python cache_simulator.py<br/><br/>"
                   "# 2. Execute full empirical test suite (Benchmark + Tests 1, 2, 3):<br/>"
                   "python cache_simulator.py --all<br/><br/>"
                   "# 3. Execute custom sequence parameter:<br/>"
                   "python cache_simulator.py \"2, 6, 10, 14, 2, 6\"</code>", ParagraphStyle("RPC", fontName="Courier", fontSize=7, leading=9.5, textColor=C_TEXT))],
        [Spacer(1, 2)],
        [Paragraph("<b>GitHub Repository URL:</b> "
                   '<link href="https://github.com/akash77007/COA"><u><font color="#0284C7"><b>https://github.com/akash77007/COA</b></font></u></link>', body_style)]
    ]
    t_repro = Table(repro_data, colWidths=[510])
    t_repro.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_repro)
    story.append(Spacer(1, 6))

    if os.path.exists("docs/screenshots/shot_build.png"):
        img_build = Image("docs/screenshots/shot_build.png", width=490, height=125)
        img_build.hAlign = 'CENTER'
        story.append(img_build)
        story.append(Paragraph("<b>Figure 3:</b> Clean simulator startup, initialization check, and execution log capture.", caption_style))

    # Build PDF with custom NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {filename}")


if __name__ == "__main__":
    build_pdf("Akash_Sharma_2401201108_COA_Assignment2.pdf")
    import shutil
    shutil.copyfile("Akash_Sharma_2401201108_COA_Assignment2.pdf", "reports/Akash_Sharma_2401201108_COA_Assignment2.pdf")
    print("Copied to reports/Akash_Sharma_2401201108_COA_Assignment2.pdf")
