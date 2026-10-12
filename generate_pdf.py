import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class BorderCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, num_pages):
        self.saveState()
        # Outer border
        self.setStrokeColor(colors.HexColor('#1A202C'))
        self.setLineWidth(1)
        self.rect(30, 30, 535, 782)
        
        # Inner fine border
        self.setStrokeColor(colors.HexColor('#718096'))
        self.setLineWidth(0.5)
        self.rect(33, 33, 529, 776)
        
        # Header / Footer on pages after cover & title
        if self._pageNumber > 2:
            self.setFont('Helvetica', 8.5)
            self.setFillColor(colors.HexColor('#4A5568'))
            page_text = f"Page {self._pageNumber}"
            self.drawRightString(540, 42, page_text)
            self.drawString(45, 42, "NetGuard AI - Mini Project Report")
            self.setStrokeColor(colors.HexColor('#CBD5E0'))
            self.setLineWidth(0.5)
            self.line(45, 53, 550, 53)
            
        self.restoreState()

def build_pdf(filename="NetGuard_AI_Mini_Project_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold',
        fontSize=18, leading=22, alignment=1, textColor=colors.HexColor('#0F172A'), spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle', parent=styles['Normal'], fontName='Helvetica-Bold',
        fontSize=12, leading=16, alignment=1, textColor=colors.HexColor('#1E293B'), spaceAfter=6
    )
    h1_style = ParagraphStyle(
        'ChapterHeader', parent=styles['Heading1'], fontName='Helvetica-Bold',
        fontSize=14, leading=18, alignment=1, textColor=colors.HexColor('#0F172A'), spaceBefore=10, spaceAfter=12
    )
    h2_style = ParagraphStyle(
        'SectionHeader', parent=styles['Heading2'], fontName='Helvetica-Bold',
        fontSize=11, leading=15, textColor=colors.HexColor('#1E293B'), spaceBefore=8, spaceAfter=4
    )
    h3_style = ParagraphStyle(
        'SubSectionHeader', parent=styles['Heading3'], fontName='Helvetica-Bold',
        fontSize=9.5, leading=13, textColor=colors.HexColor('#334155'), spaceBefore=5, spaceAfter=2
    )
    body_style = ParagraphStyle(
        'BodyDark', parent=styles['Normal'], fontName='Helvetica',
        fontSize=9, leading=13, textColor=colors.HexColor('#1E293B'), alignment=4, spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        'BulletText', parent=styles['Normal'], fontName='Helvetica',
        fontSize=8.5, leading=12, textColor=colors.HexColor('#1E293B'), leftIndent=15, spaceAfter=2.5
    )
    code_style = ParagraphStyle(
        'SqlCode', parent=styles['Normal'], fontName='Courier',
        fontSize=7.5, leading=10, textColor=colors.HexColor('#0F172A'), spaceAfter=3
    )
    center_text = ParagraphStyle(
        'CenterBody', parent=styles['Normal'], fontName='Helvetica',
        fontSize=9.5, leading=13.5, alignment=1, textColor=colors.HexColor('#1E293B'), spaceAfter=4
    )

    elements = []
    logo_path = 'backend/app/static/logo.png'

    # =========================================================================
    # PAGE 1: EXPERIMENT 11 / AIM
    # =========================================================================
    elements.append(Spacer(1, 20))
    elements.append(Paragraph('EXPERIMENT 11', title_style))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph('<b>AIM: MINI PROJECT</b>', h2_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph('Submit the Project Report which will consist of documentation related to different phases of Software Development Life Cycle:', body_style))
    elements.append(Spacer(1, 4))
    for b in [
        'Title of the Project, Abstract, Introduction',
        'Software Requirement Specification',
        'Conceptual Design using ER features, Relational Model in appropriate Normalize form',
        'Graphical User Interface, Source Code',
        'Testing document',
        'Conclusion'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph('<b>Develop application considering:</b>', h2_style))
    elements.append(Paragraph('• <b>Front End:</b> React / JavaScript / Tailwind CSS / Recharts', bullet_style))
    elements.append(Paragraph('• <b>Backend :</b> Python (FastAPI) / SQLite / Scikit-learn / Groq LLM', bullet_style))
    elements.append(Spacer(1, 35))
    if os.path.exists(logo_path):
        elements.append(Image(logo_path, width=70, height=70))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph('<b>NetGuard AI Cyber Defense Architecture</b>', center_text))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 2: TITLE PAGE
    # =========================================================================
    elements.append(Spacer(1, 25))
    elements.append(Paragraph('A Mini Project Report', subtitle_style))
    elements.append(Paragraph('<i>on</i>', center_text))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph('<b>NetGuard AI: Network Traffic Anomaly Detection System</b>', title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph('<i>by</i>', center_text))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph('<b>Candidate (SE-Computer)</b>', subtitle_style))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph('Under the guidance of', center_text))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph('<b>Prof. Harsha Jain</b>', subtitle_style))
    elements.append(Spacer(1, 25))
    if os.path.exists(logo_path):
        elements.append(Image(logo_path, width=65, height=65))
        elements.append(Spacer(1, 12))
    elements.append(Paragraph('<b>Department of Computer Engineering</b>', subtitle_style))
    elements.append(Paragraph("K J's Educational Institute", center_text))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph('<b>K J College of Engineering &amp; Management Research, Pune</b>', subtitle_style))
    elements.append(Paragraph('<b>SAVITRIBAI PHULE PUNE UNIVERSITY</b>', subtitle_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph('<b>2025-2026</b>', subtitle_style))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 3: CERTIFICATE
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>K J's Educational Institute</b>", center_text))
    elements.append(Paragraph('<b>K J College of Engineering &amp; Management Research</b>', subtitle_style))
    elements.append(Paragraph('(Accredited by NAAC)', center_text))
    elements.append(Paragraph("<font size='7.5'>Affiliated to Savitribai Phule Pune University (SPPU), Approved by Govt. of Maharashtra, Recognized by AICTE.</font>", center_text))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph('<b>CERTIFICATE</b>', h1_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('This is to certify that,', body_style))
    elements.append(Paragraph('<b>Candidate (SE-Computer)</b>', subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        'of class <b>S.E Computer</b> has successfully completed the mini project work on '
        '<b>“NetGuard AI: Network Traffic Anomaly Detection System”</b> at <b>K J College of Engineering &amp; Management Research, Pune</b> '
        'in the partial fulfilment of the Graduate Degree course in S.E at the Department of Computer Engineering '
        'in the academic Year <b>2025-2026 Semester - IV</b> as prescribed by the Savitribai Phule Pune University.',
        body_style
    ))
    elements.append(Spacer(1, 140))
    cert_table = Table([
        [Paragraph('<b>Prof. Harsha Jain</b><br/>Project Guide', body_style),
         Paragraph('<b>Dr. Nikita Kulkarni</b><br/>Head of Department', body_style)]
    ], colWidths=[240, 240])
    cert_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
    ]))
    elements.append(cert_table)
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 4: ACKNOWLEDGEMENTS
    # =========================================================================
    elements.append(Spacer(1, 15))
    elements.append(Paragraph('<b>Acknowledgements</b>', h1_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        'With a deep sense of gratitude, we would like to thank all the people who have guided and supported us '
        'throughout the development of our project <b>“NetGuard AI: Network Traffic Anomaly Detection System”</b>. '
        'Their valuable suggestions and encouragement helped us to complete this work successfully.', body_style
    ))
    elements.append(Paragraph(
        'It is our proud privilege to express our sincere thanks to <b>Dr. Suhas S. Khot</b>, Principal of K J College of '
        'Engineering &amp; Management Research, Pune, for providing us the opportunity and necessary facilities to carry out this project. '
        'We are highly thankful to <b>Dr. Nikita Kulkarni</b>, Head of the Computer Engineering Department, for her constant '
        'encouragement and continuous guidance during the project work.', body_style
    ))
    elements.append(Paragraph(
        'We express our special gratitude to our project guide, <b>Prof. Harsha Jain</b>, for providing us with expert advice, '
        'motivation, and support at every stage of project development. Her knowledge and experience helped us understand the '
        'practical implementation of Machine Learning and Database Management System concepts in real-world applications.', body_style
    ))
    elements.append(Paragraph(
        'We would also like to thank all the faculty members, friends, and classmates for their support and cooperation, '
        'which helped us overcome various challenges faced during the completion of this project. Finally, we thank everyone who directly '
        'or indirectly contributed to the successful completion of NetGuard AI.', body_style
    ))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 5: CONTENTS
    # =========================================================================
    elements.append(Spacer(1, 15))
    elements.append(Paragraph('<b>Contents</b>', h1_style))
    elements.append(Spacer(1, 12))
    toc_data = [
        ['Sr.No.', 'Topic', 'Page No.'],
        ['', 'Acknowledgement', 'i'],
        ['', 'Content', 'ii'],
        ['', 'Abstract', 'iii'],
        ['Chapter 1', 'Introduction', '1'],
        ['Chapter 2', 'Literature Review', '3'],
        ['Chapter 3', 'Software and Hardware Requirement Specification', '6'],
        ['', '3.1 Hardware Requirement', ''],
        ['', '3.2 Software Requirement', ''],
        ['Chapter 4', 'Entity Relationship Diagram', '8'],
        ['Chapter 5', 'Tables/Collection', '9'],
        ['Chapter 6', 'Result', '11'],
        ['Chapter 7', 'Conclusion', '16'],
        ['', 'References', '18']
    ]
    toc_table = Table(
        [[Paragraph(f'<b>{c}</b>' if i==0 else c, body_style) for c in row] for i, row in enumerate(toc_data)],
        colWidths=[70, 360, 60]
    )
    toc_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(toc_table)
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 6: ABSTRACT
    # =========================================================================
    elements.append(Spacer(1, 15))
    elements.append(Paragraph('<b>Abstract</b>', h1_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        'The <b>NetGuard AI: Network Traffic Anomaly Detection System</b> is a relational database-driven, machine learning-powered '
        'application designed to detect malicious intrusions and anomalous traffic vectors efficiently. The system is developed using '
        'FastAPI (Python) and structured relational database techniques (SQLite via SQLAlchemy 2.0) and follows normalization principles '
        'to eliminate redundancy and maintain high data consistency.', body_style
    ))
    elements.append(Paragraph(
        'It supports multiple modules such as raw dataset upload and validation, supervised Random Forest classification (88.0% Test Accuracy, '
        '0.98 ROC-AUC, 0.91% False Positive Rate), unsupervised Isolation Forest anomaly detection, automated security alert triage, and '
        'a Groq-powered AI Cybersecurity Assistant grounded in SQLite telemetry.', body_style
    ))
    elements.append(Paragraph(
        'It eliminates the drawbacks of traditional manual log inspection and static firewalls such as high false positives, lack of '
        'contextual explainability, and time consumption. The system ensures data integrity, security, and fast retrieval through '
        'well-designed relational tables and RESTful endpoints.', body_style
    ))
    elements.append(Paragraph(
        'This project highlights the practical implementation of DBMS concepts like ER modeling, relational schema design, '
        'and query processing in a real-world cybersecurity application.', body_style
    ))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 7: CHAPTER 1 INTRODUCTION
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>Chapter 1: Introduction</b>', h1_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph('<b>1.1 Introduction:</b>', h2_style))
    elements.append(Paragraph(
        'In traditional networks, traffic inspection and threat management are done manually or using rigid static rules, '
        'which is time-consuming and error-prone. Managing high-volume flow records, identifying subtle DDoS attacks, and responding '
        'to port scans becomes difficult as data increases.', body_style
    ))
    elements.append(Paragraph(
        'This system uses Database Management System (DBMS) concepts to maintain records such as destination ports, flow duration, '
        'packet counts, anomaly scores, classification verdicts, and security incident alerts. It provides a centralized platform '
        'where all network flow information is stored in a structured format, reducing redundancy and ensuring consistency.', body_style
    ))
    elements.append(Paragraph('The NetGuard AI System is developed to:', body_style))
    for b in [
        'Store and manage large amounts of network flow capture data',
        'Provide quick access to anomaly predictions and telemetry',
        'Reduce manual effort and error in incident triage',
        'Improve overall efficiency of Security Operations Centers (SOCs)'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph('<b>1.2 Problem Statement:</b>', h2_style))
    elements.append(Paragraph(
        'Managing network traffic anomalies manually or using separate disconnected tools leads to inefficiency, data redundancy, and errors. '
        'Enterprises need to handle large amounts of flow information such as Destination Ports, Flow Durations, Forward and Backward packet counts, '
        'and attack signatures. Traditional methods make it difficult to store, update, and retrieve this data accurately in real time.', body_style
    ))
    elements.append(Paragraph(
        'The NetGuard AI System is designed to overcome these problems by using a centralized database and ML pipeline. It helps in '
        'organizing and managing all traffic data efficiently. The system allows proper storage of uploaded datasets, flow predictions, '
        'severity alerts, and chat transcripts.', body_style
    ))
    elements.append(Paragraph(
        'The main objective is to reduce manual work, avoid duplication of data, and ensure data consistency and security. The system '
        'also provides easy access to authorized analysts, enabling smooth triage of security incidents.', body_style
    ))
    elements.append(Paragraph('<b>1.3 Framework of the Proposed Work in Project:</b>', h2_style))
    elements.append(Paragraph('<b>1. Needs Assessment and Requirement Gathering:</b>', h3_style))
    for b in [
        'Identify the needs of SOC analysts, administrators, and security teams.',
        'Study the problems faced in manual packet inspection and static rule firewalls.',
        'Collect benchmark network flow dataset records (CIC-IDS2017).'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 8: CHAPTER 1 CONTINUED (FRAMEWORK)
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>2. System Design and Architecture:</b>', h3_style))
    for b in [
        'Design database structure for storing datasets, detection runs, predictions, and alerts.',
        'Plan user interface for easy access and management of network threat information.',
        'Define relationships between entities such as datasets, runs, predictions, and alerts.'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(Paragraph('<b>3. Development and Coding:</b>', h3_style))
    for b in [
        'Develop the system using suitable programming languages (Python, JavaScript) and DBMS tools (SQLite, SQLAlchemy).',
        'Implement core features such as dataset upload, Random Forest inference, and alert triage.',
        'Apply validation techniques to ensure accurate flow feature schema entry.'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(Paragraph('<b>4. Testing and Quality Assurance:</b>', h3_style))
    for b in [
        'Test the system for accuracy, reliability, and performance using automated Pytest suites.',
        'Ensure proper functioning of modules like traffic analytics, anomaly detection, and AI assistant.'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(Paragraph('<b>5. User Training and Documentation:</b>', h3_style))
    for b in [
        'Prepare user manuals for security analysts and administrators.',
        'Provide instructions for using system features and querying the AI assistant efficiently.'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(Paragraph('<b>6. Launch and Deployment:</b>', h3_style))
    for b in [
        'Deploy the system for use by security analysts and students on cloud platforms (Render).',
        'Collect feedback for improvements.'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(Paragraph('<b>7. Scalability and Enhancement:</b>', h3_style))
    for b in [
        'Improve system performance to handle large amounts of network traffic.',
        'Add advanced features such as live PCAP packet sniffing and automated firewall rule generation.',
        'Upgrade the system based on user feedback and future security requirements.'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 9: CHAPTER 2 LITERATURE REVIEW
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>Chapter 2: Literature Review</b>', h1_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph('<b>2.1 Introduction:</b>', h2_style))
    elements.append(Paragraph(
        'NetGuard AI is a database-driven, machine learning application designed to manage and detect network anomalies in an efficient manner. '
        'With the increasing number of network connections, encrypted protocols, and automated attacks, it becomes difficult to handle all operations '
        'manually. Therefore, a computerized system is required to store, process, and retrieve threat information quickly and accurately.', body_style
    ))
    elements.append(Paragraph(
        'This system uses Database Management System (DBMS) concepts to maintain records such as uploaded dataset files, detection runs, '
        'predictions, alerts, model metrics, and chat sessions. It provides a centralized platform where all information is stored in a structured '
        'format, reducing redundancy and ensuring data consistency.', body_style
    ))
    elements.append(Paragraph(
        'The NetGuard AI system helps different users such as SOC analysts, administrators, and incident handlers to access relevant information '
        'easily. It reduces alert fatigue, saves time, and increases overall efficiency in cybersecurity operations.', body_style
    ))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph('<b>2.2 Existing Methodologies:</b>', h2_style))
    for title, desc in [
        ('1. Manual Analysis Method:', 'Traditionally, security teams analyze packet capture files manually using Wireshark, which is time-consuming and prone to errors. This method lacks proper organization and makes it difficult to detect subtle distributed attacks in real time.'),
        ('2. Database Management Systems (DBMS):', 'DBMS technology has been widely used to store, organize, and manage large amounts of structured data. It helps in efficient data retrieval, updating records, and maintaining data consistency across incidents.'),
        ('3. User-Centered Design Approach:', 'Modern security systems follow user-centered design principles to ensure easy navigation and understanding. Interfaces are designed to be simple and user-friendly for SOC analysts with dark themes and visual charts.'),
        ('4. Web-Based Application Systems:', 'Modern systems are developed as web applications, allowing users to access information anytime and anywhere. These systems improve accessibility and provide centralized data storage.')
    ]:
        elements.append(Paragraph(f'<b>{title}</b>', h3_style))
        elements.append(Paragraph(f'• {desc}', body_style))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 10: CHAPTER 2 CONTINUED (PROPOSED METHODOLOGY)
    # =========================================================================
    elements.append(Spacer(1, 10))
    for title, desc in [
        ('5. Data Analysis Techniques:', 'Machine Learning and data analysis methods are used to identify patterns and trends in network flows. Feature extraction and tree ensembles help in determining anomalous packet sizes and flow duration signatures.'),
        ('6. Secure Data Storage Methods:', 'Security techniques are used to protect network and forensic data from unauthorized access. Authentication, parameterized queries, and environment variable isolation help maintain data integrity and reliability.')
    ]:
        elements.append(Paragraph(f'<b>{title}</b>', h3_style))
        elements.append(Paragraph(f'• {desc}', body_style))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>2.3 Proposed Methodology:</b>', h2_style))
    elements.append(Paragraph('<b>1. Requirement Analysis:</b>', h3_style))
    for b in [
        'Identify the needs of SOC analysts, security engineers, and administrators.',
        'Analyze problems in existing manual tools such as data redundancy, alert fatigue, and errors.',
        'Gather requirements for modules like dataset upload, ML detection, alert triage, and AI advisory.'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))

    elements.append(Paragraph('<b>2. System Design and Database Structure:</b>', h3_style))
    for b in [
        'Design database tables such as: uploaded_datasets, detection_runs, traffic_predictions, security_alerts, model_evaluations, chat_sessions, chat_messages.',
        'Define relationships using ER diagrams (e.g., dataset-run, run-prediction, prediction-alert).',
        'Apply normalization (3NF) to ensure efficient data storage and avoid redundancy.'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))

    elements.append(Paragraph('<b>3. Development and Implementation:</b>', h3_style))
    elements.append(Paragraph('Develop the system using modern web technologies (React, Tailwind CSS, JavaScript) and DBMS (SQLite via FastAPI). Implement modules such as:', body_style))
    for b in [
        '1. Dataset upload, schema validation, and 20-row live preview',
        '2. Random Forest and Isolation Forest inference engine',
        '3. Interactive Recharts analytics and threat radar video feed',
        '4. Security alert triage and analyst note management',
        '5. Groq LLM Assistant grounded in SQLite telemetry'
    ]:
        elements.append(Paragraph(f'&nbsp;&nbsp;&nbsp;&nbsp;{b}', bullet_style))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 11: CHAPTER 2 CONTINUED (TESTING & DEPLOYMENT)
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>4. Testing and Validation:</b>', h3_style))
    for b in [
        'Conduct unit testing and system testing for all API routes and ML predictors.',
        'Validate data inputs to maintain accuracy and consistency across Excel and CSV files.',
        'Ensure proper functioning of operations like data insertion, updating, and retrieval.'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))

    elements.append(Paragraph('<b>5. User Guidance and Documentation:</b>', h3_style))
    elements.append(Paragraph('Prepare user manuals and system documentation explaining features and usage. Provide guidelines for:', body_style))
    for b in [
        'Uploading and analyzing network captures (.xlsx/.csv)',
        'Managing security alerts and updating investigation status',
        'Querying the Groq AI Cybersecurity Assistant for containment guidance',
        'Exporting prediction CSV reports'
    ]:
        elements.append(Paragraph(f'&nbsp;&nbsp;&nbsp;&nbsp;• {b}', bullet_style))

    elements.append(Paragraph('<b>6. Deployment and Data Entry:</b>', h3_style))
    for b in [
        'Deploy the full-stack unified system for online access using Render cloud.',
        'Load and benchmark the CIC-IDS2017 dataset into the relational database.'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 12: CHAPTER 3 SRS
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>Chapter 3 : Software Requirement Specification</b>', h1_style))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph('<b>3.1 Hardware Requirements:</b>', h2_style))
    for b in [
        'Computer/Laptop with Intel i3 or higher (i5/i7 recommended)',
        'Minimum 4 GB RAM (8 GB recommended for ML inference)',
        '256 GB storage / SSD',
        'Keyboard, mouse, display'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph('<b>3.2 Software Requirements:</b>', h2_style))
    for b in [
        'Operating System: Windows 10/11 or Linux',
        'Frontend: React 18, Vite, Tailwind CSS, JavaScript',
        'Backend: Python 3.12, FastAPI, Uvicorn',
        'Database: SQLite 3 via SQLAlchemy 2.0 ORM',
        'Machine Learning: Scikit-learn, Pandas, NumPy, Joblib',
        'AI LLM Core: Groq Python SDK (openai/gpt-oss-120b)',
        'Editor: VS Code / Notepad++',
        'Browser: Google Chrome / Edge'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        'The above software helps in developing a user-friendly web application and managing data efficiently using DBMS and ML concepts.',
        body_style
    ))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 13: CHAPTER 4 ER DIAGRAM
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>Chapter 4 : Entity Relationship Diagram</b>', h1_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        'The Entity-Relationship model defines the conceptual data structure of NetGuard AI. '
        'It illustrates the entities, attributes, primary keys, foreign keys, and relationships governing datasets, '
        'detection runs, predictions, alerts, evaluations, and AI chat sessions.', body_style
    ))
    elements.append(Spacer(1, 10))

    er_table_data = [
        ['Entity', 'Primary Key', 'Foreign Key', 'Attributes', 'Cardinality'],
        ['UploadedDataset', 'id (UUID)', '-', 'filename, file_size, row_count, columns_json', '1 : N with DetectionRun'],
        ['DetectionRun', 'id (UUID)', 'dataset_id', 'model_name, total_records, normal_count, anomaly_pct', '1 : N with TrafficPrediction'],
        ['TrafficPrediction', 'id (Integer)', 'run_id', 'destination_port, flow_duration, packets, label, severity', '1 : 1 with SecurityAlert'],
        ['SecurityAlert', 'id (UUID)', 'run_id, prediction_id', 'alert_title, attack_category, severity, status, notes', 'Child of DetectionRun'],
        ['ModelEvaluation', 'id (Integer)', '-', 'model_name, accuracy, precision, recall, f1, roc_auc', 'Independent Metrics Log'],
        ['ChatSession', 'id (UUID)', '-', 'title, active_run_id, created_at, updated_at', '1 : N with ChatMessage'],
        ['ChatMessage', 'id (Integer)', 'session_id', 'role (user/assistant), content, context_run_id', 'Child of ChatSession']
    ]
    er_table = Table(
        [[Paragraph(f'<b>{c}</b>' if i==0 else c, body_style) for c in row] for i, row in enumerate(er_table_data)],
        colWidths=[85, 65, 65, 155, 95]
    )
    er_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(er_table)
    elements.append(Spacer(1, 15))
    elements.append(Paragraph('<b>Relational Constraints and Multiplicities:</b>', h2_style))
    for b in [
        '<b>UploadedDataset to DetectionRun (1 to Many):</b> A single dataset can be evaluated repeatedly across Random Forest and Isolation Forest.',
        '<b>DetectionRun to TrafficPrediction (1 to Many):</b> A detection run generates individual prediction records for each network flow in the dataset.',
        '<b>TrafficPrediction to SecurityAlert (1 to 1 optional):</b> Every anomalous prediction is automatically transformed into an actionable incident alert.',
        '<b>ChatSession to ChatMessage (1 to Many):</b> A session maintains full multi-turn conversational advisory history with Groq.'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 14: CHAPTER 5 TABLES/COLLECTION PART 1
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>Chapter 5 : Tables/Collections</b>', h1_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>5.1 Database Creation</b>', h2_style))
    elements.append(Paragraph('<b>CREATE DATABASE Statement</b>', h3_style))
    elements.append(Paragraph('The CREATE DATABASE statement / SQLite engine initialization is used to create a new database.', body_style))
    elements.append(Paragraph('<b>Syntax:</b>', h3_style))
    elements.append(Paragraph('<code>CREATE DATABASE netguard_db;</code>', code_style))
    elements.append(Paragraph('<b>Database:</b> Database netguard.db (SQLite via SQLAlchemy)', body_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>5.2 Tables</b>', h2_style))

    for tbl, ddl in [
        ('Table: uploaded_datasets',
"""CREATE TABLE uploaded_datasets (
 dept_id INT(10) PRIMARY KEY, -- id VARCHAR(36)
 filename VARCHAR(255) NOT NULL,
 file_size INT(10) NOT NULL,
 row_count INT(10) NOT NULL,
 column_count INT(10) NOT NULL,
 columns_json TEXT NOT NULL,
 preview_json TEXT NOT NULL,
 created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);"""),
        ('Table: detection_runs',
"""CREATE TABLE detection_runs (
 run_id VARCHAR(36) PRIMARY KEY,
 dataset_id VARCHAR(36) REFERENCES uploaded_datasets(id),
 dataset_name VARCHAR(255) NOT NULL,
 model_name VARCHAR(100) NOT NULL,
 total_records INT(10) NOT NULL,
 normal_count INT(10) NOT NULL,
 anomaly_count INT(10) NOT NULL,
 anomaly_percentage FLOAT NOT NULL,
 duration_ms FLOAT DEFAULT 0.0,
 status VARCHAR(50) DEFAULT 'completed',
 created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);"""),
        ('Table: traffic_predictions',
"""CREATE TABLE traffic_predictions (
 prediction_id INT(10) PRIMARY KEY AUTOINCREMENT,
 run_id VARCHAR(36) REFERENCES detection_runs(id),
 record_index INT(10) NOT NULL,
 destination_port INT(10) NOT NULL,
 flow_duration FLOAT NOT NULL,
 total_fwd_packets INT(10) NOT NULL,
 total_backward_packets INT(10) NOT NULL,
 total_fwd_len FLOAT NOT NULL,
 total_bwd_len FLOAT NOT NULL,
 true_label VARCHAR(100),
 predicted_label VARCHAR(100) NOT NULL,
 is_anomaly BOOLEAN NOT NULL,
 anomaly_score FLOAT NOT NULL,
 confidence FLOAT NOT NULL,
 severity VARCHAR(50) DEFAULT 'low'
);""")
    ]:
        elements.append(Paragraph(f'<b>{tbl}</b>', h3_style))
        elements.append(Paragraph(f'<font face="Courier" size="7">{ddl.replace(chr(10), "<br/>&nbsp;&nbsp;")}</font>', code_style))
        elements.append(Spacer(1, 4))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 15: CHAPTER 5 TABLES/COLLECTION PART 2
    # =========================================================================
    elements.append(Spacer(1, 10))
    for tbl, ddl in [
        ('Table: security_alerts',
"""CREATE TABLE security_alerts (
 alert_id VARCHAR(36) PRIMARY KEY,
 run_id VARCHAR(36) REFERENCES detection_runs(id),
 prediction_id INT(10) REFERENCES traffic_predictions(id),
 record_index INT(10) NOT NULL,
 alert_title VARCHAR(255) NOT NULL,
 attack_category VARCHAR(100) NOT NULL,
 severity VARCHAR(50) NOT NULL, -- critical, high, medium, low
 destination_port INT(10) NOT NULL,
 evidence_summary TEXT NOT NULL,
 investigation_status VARCHAR(50) DEFAULT 'New', -- New, Investigating, Resolved
 notes TEXT,
 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);"""),
        ('Table: model_evaluations',
"""CREATE TABLE model_evaluations (
 eval_id INT(10) PRIMARY KEY AUTOINCREMENT,
 model_name VARCHAR(100) NOT NULL,
 model_type VARCHAR(50) NOT NULL, -- Supervised, Unsupervised
 accuracy FLOAT NOT NULL,
 precision_score FLOAT NOT NULL,
 recall_score FLOAT NOT NULL,
 f1_score FLOAT NOT NULL,
 roc_auc FLOAT,
 fpr FLOAT,
 confusion_matrix_json TEXT NOT NULL,
 trained_at DATETIME DEFAULT CURRENT_TIMESTAMP
);"""),
        ('Table: chat_sessions',
"""CREATE TABLE chat_sessions (
 session_id VARCHAR(36) PRIMARY KEY,
 title VARCHAR(255) DEFAULT 'SOC Security Assessment',
 active_run_id VARCHAR(36),
 created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
 updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);"""),
        ('Table: chat_messages',
"""CREATE TABLE chat_messages (
 message_id INT(10) PRIMARY KEY AUTOINCREMENT,
 session_id VARCHAR(36) REFERENCES chat_sessions(id),
 role VARCHAR(50) NOT NULL, -- user, assistant
 content TEXT NOT NULL,
 context_run_id VARCHAR(36),
 created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);""")
    ]:
        elements.append(Paragraph(f'<b>{tbl}</b>', h3_style))
        elements.append(Paragraph(f'<font face="Courier" size="7">{ddl.replace(chr(10), "<br/>&nbsp;&nbsp;")}</font>', code_style))
        elements.append(Spacer(1, 4))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 16: CHAPTER 6 RESULTS (OVERVIEW & HOME PAGE)
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>Chapter 6 : Results</b>', h1_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>Fig 6.1 : Home Page (Command Overview &amp; Live Threat Radar)</b>', subtitle_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        '<b>Fig. Home Page includes:</b> The UI layout includes a top navigation header with system title, active dataset switcher, '
        'system health indicators, and a responsive collapsible sidebar menu for 9 different operational modules.', body_style
    ))
    elements.append(Paragraph(
        'It provides a comprehensive dashboard with summary KPI cards: Total Scanned Records (1,000), Normal Traffic (55.1%), '
        'Anomalies Flagged (44.9%), and Active Security Alerts.', body_style
    ))
    elements.append(Paragraph(
        'It features an embedded <b>Live Cyber Threat Radar Video Feed</b> with real-time HUD telemetry simulation, radar sweep overlay, '
        'and audio/video controls. Beside the radar, an interactive Recharts donut chart displays the Traffic Verdict Ratio, and a '
        'Top Targeted Destination Ports card details ingress attack concentrations on Port 21 (FTP), Port 22 (SSH), and Port 8080 (DDoS).', body_style
    ))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph('<b>Fig 6.2 : Dataset Upload &amp; Live 20-Row Preview Page</b>', subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        'The Dataset Upload Page is used to enter and store new network flow captures into the system database. '
        'It provides a drag-and-drop zone and file browser supporting .xlsx, .xls, and .csv files.', body_style
    ))
    elements.append(Paragraph(
        'The page automatically validates incoming columns against 10 canonical flow features (Destination Port, Flow Duration, Packet counts, '
        'Packet lengths). It renders an interactive 20-row live preview table before inference, features a model selector (Random Forest vs '
        'Isolation Forest), and provides a 1-click button to analyze the benchmark CIC-IDS2017 dataset.', body_style
    ))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 17: CHAPTER 6 RESULTS (ANALYTICS & ANOMALY DETECTION)
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>Fig 6.3 : Traffic Flow &amp; Threat Vector Analytics Page</b>', subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        'The Analytics module visualizes multi-dimensional threat vectors using interactive Recharts components:', body_style
    ))
    for b in [
        '<b>Destination Port Breakdown:</b> Grouped bar chart comparing normal vs anomalous packet volumes across ports 21, 22, 53, 80, 8080.',
        '<b>Flow Duration Latency Histogram:</b> Binned distribution from sub-millisecond flows (<1ms) to multi-second persistent streams (>10s).',
        '<b>Anomaly Confidence Spectrum:</b> Probability bins from 0.0 to 1.0 reflecting classifier certainty.',
        '<b>Attack Classification Breakdown:</b> Color-coded pie chart detailing percentage shares for DoS Hulk, DDoS, PortScan, and Patator.'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))

    elements.append(Spacer(1, 15))
    elements.append(Paragraph('<b>Fig 6.4 : Anomaly Detection &amp; Forensic Record Inspection Page</b>', subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        'The Anomaly Detection page presents a paginated, searchable, and filterable table of individual flow predictions calculated by the model. '
        'Analysts can filter by verdict (All/Normal/Anomalous), severity (Critical/High/Medium/Low), or attack signature.', body_style
    ))
    elements.append(Paragraph(
        'Clicking any record opens the <b>Forensic Record Modal</b>, exposing all 10 network flow parameters with numerical units '
        '(Destination Port, Flow Duration in us, Packet lengths). It includes a 1-click button: <i>\"Ask AI Assistant to Analyze This Record\"</i> '
        'which instantly transfers the flow parameters to the Groq chatbot for root-cause diagnosis. An Export CSV button streams predictions directly.', body_style
    ))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 18: CHAPTER 6 RESULTS (SECURITY ALERTS & AI ASSISTANT)
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>Fig 6.5 : Security Alerts Incident Triage Board</b>', subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        'The Security Alerts page organizes incidents generated from anomalous flows into three lifecycle tabs: <b>New</b>, <b>Investigating</b>, and <b>Resolved</b>.', body_style
    ))
    elements.append(Paragraph(
        'Severity is automatically assigned using transparent rules: Critical for volumetric DDoS and sensitive ports, High for SSH/FTP brute force, '
        'and Medium for port scans. Analysts can update the investigation status with a single dropdown click and attach persistent notes '
        '(e.g., \"Firewall rule 402 applied to block Port 8080 ingress\") saved directly to SQLite.', body_style
    ))

    elements.append(Spacer(1, 15))
    elements.append(Paragraph('<b>Fig 6.6 : Groq-Powered AI Cybersecurity Assistant Page</b>', subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        'The AI Cybersecurity Assistant provides conversational reasoning powered by Groq cloud LPU inference (openai/gpt-oss-120b). '
        'Unlike generic chatbots that hallucinate, NetGuard AI retrieves verified metrics from SQLite (exact flow counts, anomaly rates, targeted ports) '
        'and injects them into system prompts.', body_style
    ))
    elements.append(Paragraph(
        'The interface features message bubbles, user/assistant avatars, suggested query chips (\"Why did the model flag port 21 / 22?\", '
        '\"Explain precision and recall metrics\"), session history persistence, and defensive containment recommendations.', body_style
    ))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 19: CHAPTER 6 RESULTS (MODEL PERFORMANCE BENCHMARKS)
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>Fig 6.7 : Machine Learning Performance &amp; Benchmarks Page</b>', subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        'The Model Performance page displays verified statistical benchmarks evaluated on a held-out 20% test partition of the CIC-IDS2017 dataset:', body_style
    ))
    for b in [
        '<b>Test Accuracy:</b> 88.0% across all multi-class signatures',
        '<b>Weighted Precision:</b> 87.1% (High positive predictive value)',
        '<b>Weighted Recall:</b> 88.0% (Comprehensive detection coverage)',
        '<b>F1-Score:</b> 87.1% (Harmonic mean of precision and recall)',
        '<b>ROC-AUC Score:</b> 0.980 (Exceptional class separability)',
        '<b>False Positive Rate (FPR):</b> 0.91% (Prevents alert fatigue)'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        'The page includes an interactive <b>Confusion Matrix Heatmap</b> displaying actual versus predicted counts, a per-signature classification '
        'report table, a Gini Feature Importance ranking chart, and a 1-click Retrain Models button.', body_style
    ))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 20: CHAPTER 6 RESULTS (ABOUT US & SYSTEM SETTINGS)
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>Fig 6.8 : Settings &amp; System Diagnostics Page</b>', subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        'The Settings page provides detailed information about NetGuard AI and its operational status. It helps users understand '
        'the system, backend diagnostics, and security configurations.', body_style
    ))
    elements.append(Paragraph(
        'This page explains how the system helps reduce manual work, improves accuracy, and provides quick access to threat telemetry. '
        'It highlights key features of the system such as database storage, model caching, retrieval, updating, and report generation.', body_style
    ))
    elements.append(Paragraph('It includes:', body_style))
    for b in [
        '<b>Project Objective:</b> To detect and manage network traffic anomalies efficiently using DBMS and ML',
        '<b>System Description:</b> Handles dataset captures, runs, predictions, alerts, and chat transcripts',
        '<b>Key Features:</b> Data storage, vectorized inference, live threat radar, Recharts analytics, Groq AI assistant',
        '<b>Advantages:</b> Reduces manual work, improves accuracy, saves time, eliminates hallucinations',
        '<b>Technology Used:</b> React 18, Vite, Tailwind CSS (Frontend), Python FastAPI, SQLite, Scikit-learn, Groq (Backend)',
        '<b>Security Architecture:</b> Zero client-side API key exposure, parameterized queries, local SQLite data sovereignty',
        '<b>Project Details:</b> Information about developers, project guide (Prof. Harsha Jain), and institution'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 21: CHAPTER 7 CONCLUSION
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>Chapter 7:Conclusion</b>', h1_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph('<b>7.1 Advantages</b>', h2_style))
    for b in [
        'Reduces manual paperwork and packet inspection effort',
        'Fast and easy access to flow prediction data (sub-50ms inference)',
        'Improves accuracy and reduces errors (88% Accuracy, 0.98 ROC-AUC)',
        'Centralized data management with SQLite relational schema',
        'Saves time in searching and updating security incident records',
        'User-friendly dark-navy SOC interface with live video telemetry'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))

    elements.append(Spacer(1, 8))
    elements.append(Paragraph('<b>7.2 Disadvantages</b>', h2_style))
    for b in [
        'Initial setup takes time and effort',
        'Requires basic technical knowledge of network flow features',
        'Dependent on system and database availability',
        'Risk of data loss if database is not properly backed up'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))

    elements.append(Spacer(1, 8))
    elements.append(Paragraph('<b>7.3 Applications</b>', h2_style))
    for b in [
        'Used in universities, colleges, and academic networks',
        'Helps SOC administrators manage security records',
        'Useful for incident response teams to triage DDoS and brute force',
        'Helps students and researchers study machine learning intrusion detection',
        'Can be used in data centers and enterprise network monitoring'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))

    elements.append(Spacer(1, 8))
    elements.append(Paragraph('<b>7.4 Future Scope</b>', h2_style))
    for b in [
        'Development of mobile application for on-the-go alerts',
        'Integration with cloud databases (PostgreSQL/MongoDB)',
        'Addition of live PCAP packet sniffing via Scapy',
        'Online portal with multi-tenant role-based login system',
        'Automated firewall rule generation (iptables, AWS Security Groups)'
    ]:
        elements.append(Paragraph(f'• {b}', bullet_style))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph('<b>7.5 Conclusion</b>', h2_style))
    elements.append(Paragraph(
        'The <b>NetGuard AI: Network Traffic Anomaly Detection System</b> is an efficient and reliable solution for managing and securing '
        'academic and enterprise network data using DBMS and Machine Learning. It simplifies the process of storing, organizing, and retrieving '
        'information related to network captures, threat signatures, predictions, and alerts.', body_style
    ))
    elements.append(Paragraph(
        'The system reduces manual effort, improves accuracy, and saves time. Overall, it enhances the performance of educational and '
        'corporate institutions and provides a structured way to handle large amounts of network data effectively.', body_style
    ))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 22: REFERENCES
    # =========================================================================
    elements.append(Spacer(1, 15))
    elements.append(Paragraph('<b>References</b>', h1_style))
    elements.append(Spacer(1, 12))
    for ref in [
        '1. Silberschatz, A., Korth, H. F., &amp; Sudarshan, S., Database System Concepts, McGraw-Hill Education, 7th Edition.',
        '2. Elmasri, R., &amp; Navathe, S. B., Fundamentals of Database Systems, Pearson Education, 7th Edition.',
        '3. Coronel, C., &amp; Morris, S., Database Systems: Design, Implementation, and Management, Cengage Learning.',
        '4. Sharafaldin, I., Lashkari, A. H., &amp; Ghorbani, A. A., \"Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization (CIC-IDS2017)\", Proceedings of ICISSP.',
        '5. Pedregosa, F., et al., \"Scikit-learn: Machine Learning in Python\", Journal of Machine Learning Research (JMLR).',
        '6. Breiman, L., \"Random Forests\", Machine Learning Journal.',
        '7. Tiangolo, S., \"FastAPI: Modern, High-Performance Web Framework for Python\", Available at: https://fastapi.tiangolo.com/',
        '8. Groq Inc., \"Groq LPU Inference Documentation and Python SDK\", Available at: https://console.groq.com/docs',
        '9. W3Schools, \"SQL Tutorial and Database Concepts\", Available at: https://www.w3schools.com/sql/',
        '10. GeeksforGeeks, \"DBMS and SQL Tutorials\", Available at: https://www.geeksforgeeks.org/dbms/',
        '11. Mozilla Developer Network (MDN), \"HTML5 and CSS Documentation\", Available at: https://developer.mozilla.org/',
        '12. TutorialsPoint, \"Database Management System Tutorial\", Available at: https://www.tutorialspoint.com/dbms/',
        '13. Personal implementation and testing using SQLite, FastAPI, Scikit-learn, React, and Groq LLM interface.'
    ]:
        elements.append(Paragraph(ref, body_style))
        elements.append(Spacer(1, 3))

    doc.build(elements, canvasmaker=BorderCanvas)
    print(f'Successfully built {filename}')

if __name__ == '__main__':
    build_pdf()
