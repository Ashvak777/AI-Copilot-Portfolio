#!/usr/bin/env python3
"""Generate professional portfolio PDFs (local build helper; not part of client deliverable logic)."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

NAVY = colors.HexColor("#0B2545")
STEEL = colors.HexColor("#13315C")
ACCENT = colors.HexColor("#1B4F72")
LIGHT = colors.HexColor("#F4F6F8")
MUTED = colors.HexColor("#4A5568")
LINE = colors.HexColor("#CBD5E0")


def styles():
    base = getSampleStyleSheet()
    return {
        "cover": ParagraphStyle(
            "cover",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=14,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=STEEL,
            spaceBefore=10,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#1A202C"),
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=12.5,
            textColor=colors.HexColor("#1A202C"),
            leftIndent=8,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#1A202C"),
        ),
        "cellh": ParagraphStyle(
            "cellh",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=colors.white,
        ),
        "flow": ParagraphStyle(
            "flow",
            parent=base["Normal"],
            fontName="Courier",
            fontSize=8,
            leading=11,
            textColor=STEEL,
            backColor=LIGHT,
            borderPadding=6,
            spaceAfter=8,
        ),
        "label": ParagraphStyle(
            "label",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=10,
            textColor=ACCENT,
            spaceAfter=6,
        ),
    }


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(0.75 * inch, LETTER[1] - 0.55 * inch, LETTER[0] - 0.75 * inch, LETTER[1] - 0.55 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.75 * inch, LETTER[1] - 0.45 * inch, "Enterprise AI & Microsoft Copilot Solution Portfolio")
    canvas.drawRightString(LETTER[0] - 0.75 * inch, LETTER[1] - 0.45 * inch, "Confidentiality-aware · Sanitized")
    canvas.line(0.75 * inch, 0.55 * inch, LETTER[0] - 0.75 * inch, 0.55 * inch)
    canvas.drawCentredString(LETTER[0] / 2, 0.35 * inch, f"Page {doc.page}")
    canvas.restoreState()


def bullets(items, st):
    return ListFlowable(
        [ListItem(Paragraph(i, st["bullet"]), leftIndent=12, bulletColor=ACCENT) for i in items],
        bulletType="bullet",
        start="•",
        leftIndent=15,
        spaceBefore=2,
        spaceAfter=6,
    )


def simple_table(headers, rows, st, col_widths):
    data = [[Paragraph(h, st["cellh"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(c, st["cell"]) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def rule():
    return HRFlowable(width="100%", thickness=1, color=LINE, spaceBefore=4, spaceAfter=10)


def build_executive(path: Path, st):
    doc = SimpleDocTemplate(
        str(path),
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    story = []
    story.append(Paragraph("Enterprise AI & Microsoft Copilot", st["cover"]))
    story.append(Paragraph("Executive Portfolio Summary", st["subtitle"]))
    story.append(rule())
    story.append(Paragraph("Background", st["h1"]))
    story.append(
        Paragraph(
            "Technology professional with 9+ years across Microsoft data, BI, cloud, automation, "
            "and enterprise platforms. Recent delivery focus: Microsoft Copilot Studio, Azure AI / "
            "Azure OpenAI, RAG and grounded assistants, agentic workflows, Microsoft Fabric, Power "
            "Platform, and production ALM with enterprise security and governance—primarily in "
            "banking, insurance, and regulatory environments.",
            st["body"],
        )
    )
    story.append(Paragraph("Copilot Capabilities", st["h1"]))
    story.append(
        bullets(
            [
                "Grounded enterprise knowledge assistants with citations and access control",
                "Process automation agents that create requests, validate inputs, and return status",
                "Agentic orchestration across knowledge, structured data, APIs, MCP, and workflows",
                "Enterprise RAG pipelines with evaluation for groundedness, relevance, and latency",
                "Fabric lakehouse foundations for governed analytics and AI consumption",
                "Security, Purview-aligned governance, and Dev/Test/UAT/Prod ALM",
            ],
            st,
        )
    )
    story.append(Paragraph("Representative Project Types", st["h1"]))
    story.append(
        simple_table(
            ["Project", "Outcome Focus"],
            [
                ["Enterprise Knowledge Copilot", "Verified answers from approved content"],
                ["Process Automation Agent", "Intent → workflow → enterprise action"],
                ["Agentic AI Workflow", "Tool selection with human approval for writes"],
                ["Enterprise RAG", "Measurable retrieval quality and grounding"],
                ["Fabric + Copilot", "Curated Gold data behind BI and AI"],
                ["AI Security & Governance", "Least privilege; no entitlement bypass"],
                ["Copilot ALM", "Repeatable managed-solution promotion"],
            ],
            st,
            [2.4 * inch, 4.4 * inch],
        )
    )
    story.append(Paragraph("Technology Stack", st["h1"]))
    story.append(
        Paragraph(
            "Copilot Studio · Azure OpenAI · RAG / embeddings / vector search · Power Automate · "
            "Power Apps · Dataverse · SharePoint · Microsoft Fabric · Power BI · ADF / Synapse · "
            "Databricks · Python · SQL · REST / MCP · Entra ID · RBAC · Purview · CI/CD",
            st["body"],
        )
    )
    story.append(Paragraph("Security & Governance", st["h1"]))
    story.append(
        Paragraph(
            "Solutions are designed so agents never expose information or operations beyond the "
            "authenticated user’s normal entitlements. Controls include Entra ID authentication, "
            "RBAC/RLS, managed identities, Key Vault, DLP, Purview classification, audit logging, "
            "connector governance, and environment isolation.",
            st["body"],
        )
    )
    story.append(Paragraph("Business Outcomes", st["h1"]))
    story.append(
        bullets(
            [
                "Faster access to governed knowledge with citation-backed answers",
                "Reduced manual handling for routine service and validation work",
                "Example impact: Python file-validation process reduced processing from ~3 days to ~10 minutes",
                "Clearer audit and change-management story for regulated AI releases",
            ],
            st,
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            "Confidentiality: Client-specific implementations, source code, datasets, credentials, "
            "internal URLs, and proprietary architecture details are intentionally excluded. "
            "Architectures are sanitized reference patterns representing the types of enterprise "
            "solutions delivered.",
            st["small"],
        )
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


def project_block(st, title, problem, solution, tech, security, value):
    bits = [
        Paragraph(title, st["h2"]),
        Paragraph(f"<b>Business problem.</b> {problem}", st["body"]),
        Paragraph(f"<b>Solution.</b> {solution}", st["body"]),
        Paragraph(f"<b>Technologies.</b> {tech}", st["body"]),
        Paragraph(f"<b>Security.</b> {security}", st["body"]),
        Paragraph(f"<b>Value.</b> {value}", st["body"]),
    ]
    return KeepTogether(bits)


def build_project_portfolio(path: Path, st):
    doc = SimpleDocTemplate(
        str(path),
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    story = []
    story.append(Paragraph("Copilot Project Portfolio", st["cover"]))
    story.append(Paragraph("Technical case studies · Sanitized reference patterns", st["subtitle"]))
    story.append(rule())
    story.append(
        Paragraph(
            "This document summarizes representative Microsoft Copilot and enterprise AI delivery "
            "patterns. Diagrams and deeper notes live in the companion GitHub repository "
            "<b>AI-Copilot-Portfolio</b>.",
            st["body"],
        )
    )
    story.append(Paragraph("label: Sanitized Reference Architecture — not proprietary client code", st["label"]))

    projects = [
        (
            "01 — Enterprise Knowledge Copilot",
            "Employees struggle to find verified policies and procedures across SharePoint and approved knowledge stores.",
            "Copilot Studio assistant with RAG over enterprise documents; Azure OpenAI grounded generation with citations.",
            "Copilot Studio, Azure OpenAI, embeddings, vector search, SharePoint, Dataverse, Entra ID.",
            "Authorization-aware retrieval, RBAC, managed identity, Purview-aligned classification, audit of retrieval IDs.",
            "Faster, consistent answers tied to sources employees are entitled to open.",
        ),
        (
            "02 — Process Automation Agent",
            "Routine service requests and validations create backlog and inconsistent data entry.",
            "Intent detection in Copilot Studio → Power Automate / REST → Dataverse or backend → structured status.",
            "Copilot Studio, Power Automate, custom connectors, OAuth 2.0, Dataverse, REST APIs.",
            "Least-privilege scopes, error handling without leaking internals, approvals for high-impact writes.",
            "Shorter cycle times; example adjacent automation reduced file validation from ~3 days to ~10 minutes.",
        ),
        (
            "03 — Agentic AI Workflow",
            "Users ask mixed questions requiring knowledge, data, APIs, or workflows—scripted topics do not scale.",
            "Orchestrator selects tools: RAG, structured data, REST/MCP, Power Automate, specialist agents, or refusal.",
            "Azure OpenAI tool calling, Copilot Studio, MCP/API integrations, SharePoint, Dataverse, Databricks.",
            "Narrow tool permissions; human approval for high-risk writes; full tool-invocation logging.",
            "One controlled entry point for knowledge and actions without entitlement expansion.",
        ),
        (
            "04 — Enterprise RAG Architecture",
            "Ungrounded generation is unsuitable for regulated Q&A.",
            "Ingest → preprocess → chunk → embed → vector index → filtered retrieve → prompt assembly → evaluate.",
            "Azure OpenAI embeddings/completions, vector index, metadata filters, evaluation datasets.",
            "ACL-aware retrieval, prompt-injection isolation, sensitivity tiers, release gates on groundedness.",
            "Defensible answers with measurable quality and latency.",
        ),
        (
            "05 — Copilot + Microsoft Fabric",
            "AI over raw tables yields conflicting metrics and unclear ownership.",
            "Fabric Lakehouse Bronze/Silver/Gold → semantic model → Power BI and Copilot/downstream AI.",
            "Fabric, Dataflows/pipelines, ADF/Databricks where applicable, Power BI, SQL/Python, Purview.",
            "Workspace RBAC, RLS on models, AI-approved entities documented separately from raw landing zones.",
            "Shared business definitions across reports and conversational AI.",
        ),
        (
            "06 — AI Security & Governance",
            "Agents can become unintended entitlement bypasses without deliberate controls.",
            "Framework covering Entra ID, RBAC/RLS, managed identity, Key Vault, DLP, Purview, Responsible AI, env isolation.",
            "Entra ID, Power Platform DLP, Purview, Key Vault, audit logging, OAuth.",
            "Principle: never exceed the authenticated user’s normal access for information or operations.",
            "Audit-ready AI delivery aligned to existing IAM programs.",
        ),
        (
            "07 — Copilot ALM / Production Deployment",
            "Portal-only development lacks review, regression, and rollback discipline.",
            "Dev → source control → Test → UAT → Prod using managed solutions, env vars, connection references, CI/CD.",
            "Power Platform ALM, Azure DevOps or GitHub Actions, monitoring and adoption analytics.",
            "Least-privilege deploy identities; secrets outside the repository; approval gates for Prod.",
            "Predictable releases with evidence for regulated change management.",
        ),
    ]

    for idx, p in enumerate(projects):
        story.append(project_block(st, *p))
        if idx in (2, 5):
            story.append(PageBreak())

    story.append(Paragraph("Architecture Pattern (Knowledge Copilot)", st["h1"]))
    story.append(
        Paragraph(
            "Employee → Entra ID → Copilot Studio → orchestration / grounding → RAG retrieval "
            "(embeddings, vector search, ACL/metadata filters) → Azure OpenAI → grounded response "
            "with citations. Knowledge sources typically include SharePoint, approved document "
            "sets, and selected Dataverse content.",
            st["body"],
        )
    )
    story.append(Paragraph("Architecture Pattern (Agentic Action)", st["h1"]))
    story.append(
        Paragraph(
            "User intent → orchestrator → choose among knowledge search, structured data read, "
            "REST/MCP action, Power Automate workflow, specialist agent, or refusal. High-risk "
            "writes pause for human approval. Every tool call is schema-validated and audited.",
            st["body"],
        )
    )
    story.append(PageBreak())
    story.append(Paragraph("Implementation Considerations", st["h1"]))
    story.append(
        bullets(
            [
                "Start with grounded Q&A and measurement before enabling write tools.",
                "Prefer curated Fabric Gold / semantic models for analytical answers.",
                "Separate read and write identities; require human approval for high-risk actions.",
                "Treat retrieved document text as untrusted for instruction override.",
                "Promote with evaluation evidence and managed solutions—not manual portal edits in Prod.",
            ],
            st,
        )
    )
    story.append(Paragraph("Agent Capabilities Summary", st["h1"]))
    story.append(
        simple_table(
            ["Capability", "Pattern"],
            [
                ["Knowledge Q&A", "RAG + citations + refusal"],
                ["Status lookup", "Authorized API / Dataverse read"],
                ["Request intake", "Validated create via flow/API"],
                ["Approvals", "Human-in-the-loop on sensitive writes"],
                ["Delegation", "Specialist agents for narrow domains"],
                ["Analytics answers", "Governed semantic model / Gold data"],
            ],
            st,
            [2.2 * inch, 4.6 * inch],
        )
    )
    story.append(Paragraph("Delivery & ALM Snapshot", st["h1"]))
    story.append(
        Paragraph(
            "Solutions are developed in Dev as unmanaged packages, stored in source control, and "
            "promoted as managed solutions through Test, UAT, and Production. Environment variables "
            "and connection references keep environment-specific values out of hard-coded topics. "
            "CI/CD (Azure DevOps or GitHub Actions) applies approval gates; AI evaluation regression "
            "sets protect groundedness and relevance before production changes.",
            st["body"],
        )
    )
    story.append(Paragraph("Representative Experience Context", st["h1"]))
    story.append(
        Paragraph(
            "<b>Regulatory / insurance-style programs:</b> Copilot Studio, Azure AI/OpenAI, Power "
            "Platform, Dataverse, SharePoint, RAG, embeddings, vector search, prompt engineering, "
            "agentic workflows, connectors, Responsible AI, RBAC, AI evaluation, ALM/CI/CD, Purview, "
            "Entra ID, Fabric Dataflows/Lakehouse, Power Automate.",
            st["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Banking-style programs:</b> Copilot Studio assistants, Azure AI/OpenAI, agentic "
            "workflows, SharePoint, SAP integration layers, Databricks, Dataverse, MCP/API "
            "integrations, RAG pipelines, evaluation, security/governance, ALM/DevOps.",
            st["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Fabric / analytics:</b> Bronze/Silver/Gold Lakehouse, Fabric, ADF, Synapse, "
            "Databricks, Power BI, semantic models, SQL, Python, Power Automate.",
            st["body"],
        )
    )
    story.append(PageBreak())
    story.append(Paragraph("Security Controls Applied Across Projects", st["h1"]))
    story.append(
        simple_table(
            ["Control", "How it shows up in delivery"],
            [
                ["Entra ID", "Every user session authenticated; groups drive AuthZ filters"],
                ["RBAC / RLS", "Tool access and semantic-model rows scoped to role"],
                ["Managed identity", "Azure resources avoid embedded secrets where possible"],
                ["OAuth scopes", "Read vs write API permissions separated"],
                ["Key Vault", "Remaining secrets outside source control and topics"],
                ["DLP / connectors", "Approved connector set in Power Platform"],
                ["Purview", "Classification influences what may enter indexes"],
                ["Audit", "Correlation IDs on retrieval and tool calls"],
                ["Environments", "Dev / Test / UAT / Prod isolation"],
                ["Human approval", "Required before high-risk write tools commit"],
            ],
            st,
            [2.0 * inch, 4.8 * inch],
        )
    )
    story.append(Paragraph("Outcomes Stakeholders Typically Track", st["h1"]))
    story.append(
        bullets(
            [
                "Time-to-answer for policy and procedure questions",
                "Citation coverage rate on knowledge responses",
                "Automation rate for routine service requests",
                "Evaluation scores (groundedness / relevance) on release candidates",
                "Flow failure rate and mean time to recover after a bad deploy",
                "Adoption and containment metrics from Copilot analytics",
            ],
            st,
        )
    )
    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            "Confidentiality: Client-specific implementations, source code, datasets, credentials, "
            "internal URLs, and proprietary architecture details are intentionally excluded.",
            st["small"],
        )
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


def arch_box(st, title, steps):
    return KeepTogether(
        [
            Paragraph(title, st["h2"]),
            Paragraph("Sanitized Reference Architecture", st["label"]),
            Paragraph("<br/>".join(steps), st["flow"]),
        ]
    )


def build_architecture(path: Path, st):
    doc = SimpleDocTemplate(
        str(path),
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    story = []
    story.append(Paragraph("Architecture Overview", st["cover"]))
    story.append(Paragraph("Microsoft Copilot · Azure AI · Fabric · Governance", st["subtitle"]))
    story.append(rule())
    story.append(
        Paragraph(
            "Flow diagrams below are textual renderings of the Mermaid sources in the repository "
            "<font face='Courier'>architecture/</font> folder. They are sanitized reference "
            "architectures for discussion with technical stakeholders.",
            st["body"],
        )
    )

    story.append(
        arch_box(
            st,
            "1. Enterprise Copilot",
            [
                "Employee → Entra ID → Copilot Studio",
                "→ Orchestration / grounding instructions",
                "→ Query embedding → Vector index → ACL / metadata filter → re-rank",
                "→ Azure OpenAI (grounded generation) → Citations → Employee",
                "Knowledge sources: SharePoint · Approved documents · Dataverse",
            ],
        )
    )
    story.append(
        Paragraph(
            "Purpose: identity-aware internal Q&A with hallucination controls and verifiable sources.",
            st["body"],
        )
    )

    story.append(
        arch_box(
            st,
            "2. Enterprise RAG",
            [
                "Documents → Preprocess / classify → Chunk + metadata → Embeddings → Vector index",
                "Query → AuthZ filter → Embed → Semantic/hybrid retrieve → Metadata filter",
                "→ Prompt/context assembly → Azure OpenAI → Grounded answer + citations",
                "→ Evaluate groundedness · relevance · completeness · latency",
            ],
        )
    )
    story.append(
        Paragraph(
            "Purpose: operable retrieval pipeline with release gates suitable for financial-services style corpora.",
            st["body"],
        )
    )

    story.append(
        arch_box(
            st,
            "3. Agentic Workflow",
            [
                "User → Copilot Studio → Orchestrator (tool calling)",
                "Tools: Knowledge (RAG) · Data (Dataverse/Databricks API) · Action (REST/MCP)",
                "· Power Automate · Specialist agent",
                "High-risk write? → Human approval → Execute · else Execute",
                "→ Unified response + audit trail",
            ],
        )
    )
    story.append(
        Paragraph(
            "Purpose: controlled multi-tool automation with narrowly scoped permissions.",
            st["body"],
        )
    )

    story.append(PageBreak())
    story.append(
        arch_box(
            st,
            "4. Fabric + Copilot",
            [
                "Sources → Fabric pipelines / Dataflows → Lakehouse",
                "Bronze → Silver → Gold → Semantic model",
                "→ Power BI  and  Copilot / downstream AI",
                "Governance: Purview · Workspace RBAC · RLS",
            ],
        )
    )
    story.append(
        Paragraph(
            "Purpose: AI consumes curated business data and shared metric definitions—not raw landing tables.",
            st["body"],
        )
    )

    story.append(
        arch_box(
            st,
            "5. Security & Governance",
            [
                "User → Entra ID → Conditional Access → Copilot / AI app",
                "→ Policy (RBAC · tool allow-list · DLP)",
                "→ Read tools (least privilege) / Write tools (separate identity + approval)",
                "→ Enterprise systems · Purview · Audit logging",
                "Environments: Dev · Test · UAT · Prod",
            ],
        )
    )
    story.append(
        Paragraph(
            "<b>Principle:</b> An AI agent should never provide access to information or operations "
            "that the authenticated user would not normally be authorized to access.",
            st["body"],
        )
    )

    story.append(Paragraph("Technical Depth Checklist", st["h1"]))
    story.append(
        simple_table(
            ["Concern", "Typical control"],
            [
                ["Grounding", "Context-only prompts; citation required"],
                ["Retrieval AuthZ", "ACL/group filter before generation"],
                ["Tool calling", "Schema validation; allow-listed tools"],
                ["Secrets", "Key Vault / pipeline secrets; managed identity"],
                ["Data for AI", "Fabric Gold / semantic model preferred"],
                ["Promotion", "Managed solutions + evaluation evidence"],
            ],
            st,
            [2.2 * inch, 4.6 * inch],
        )
    )
    story.append(PageBreak())
    story.append(Paragraph("Component Responsibilities", st["h1"]))
    story.append(
        simple_table(
            ["Component", "Responsibility"],
            [
                ["Copilot Studio", "Channel UX, topics, generative orchestration"],
                ["Azure OpenAI", "Embeddings, grounded completion, tool selection"],
                ["Vector index", "Semantic retrieval with metadata payload"],
                ["Power Automate", "Workflows, approvals, Platform connectors"],
                ["Dataverse", "Operational entities and configuration"],
                ["SharePoint", "Document knowledge corpus"],
                ["Fabric Lakehouse", "Medallion analytics foundation"],
                ["Semantic model", "Measures, relationships, RLS for BI/AI"],
                ["Entra ID", "Authentication, groups, conditional access"],
                ["Purview", "Classification, catalog, lineage signals"],
                ["Key Vault", "Secret/certificate material when required"],
                ["CI/CD", "Solution validation and environment promotion"],
            ],
            st,
            [2.2 * inch, 4.6 * inch],
        )
    )
    story.append(Paragraph("Integration Notes", st["h1"]))
    story.append(
        bullets(
            [
                "Custom connectors expose OpenAPI-defined REST surfaces to Copilot and flows.",
                "MCP-based integrations may standardize tool access alongside connectors.",
                "OAuth 2.0 delegated calls are preferred when the action must run as the user.",
                "Databricks and SAP are reached through governed APIs—not credentials in prompts.",
                "Evaluation datasets gate prompt/index changes the same way tests gate code.",
            ],
            st,
        )
    )
    story.append(Paragraph("Repository Diagram Sources", st["h1"]))
    story.append(
        Paragraph(
            "Maintainable Mermaid diagrams: architecture/enterprise-copilot-architecture.md, "
            "rag-architecture.md, agentic-workflow.md, fabric-ai-architecture.md, "
            "security-governance.md. SVG exports for slides/PDF packaging: assets/diagrams/.",
            st["body"],
        )
    )
    story.append(PageBreak())
    story.append(Paragraph("End-to-End Sequence (Knowledge + Action)", st["h1"]))
    story.append(
        Paragraph(
            "1. Authenticate the user with Entra ID and establish session claims.<br/>"
            "2. Classify intent: knowledge, data lookup, workflow, or mixed.<br/>"
            "3. For knowledge: embed query, retrieve with ACL/metadata filters, assemble context, generate grounded answer with citations.<br/>"
            "4. For actions: validate tool schema, authorize tool and resource, execute via connector/API/MCP or Power Automate.<br/>"
            "5. For high-risk writes: pause for human approval; deny by default on failure.<br/>"
            "6. Log correlation ID, tools used, and outcome; return a user-safe response.<br/>"
            "7. Feed production telemetry and evaluation samples back into the ALM quality gate.",
            st["body"],
        )
    )
    story.append(Paragraph("What Is Intentionally Not Shown", st["h1"]))
    story.append(
        bullets(
            [
                "Client network diagrams, private endpoints, or tenant identifiers",
                "Proprietary prompt libraries and production index schemas",
                "Real document corpora, customer records, or internal SharePoint URLs",
                "Credentials, certificates, connection strings, or pipeline secrets",
            ],
            st,
        )
    )
    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            "Confidentiality: Client-specific implementations, source code, datasets, credentials, "
            "internal URLs, and proprietary architecture details are intentionally excluded.",
            st["small"],
        )
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


def main():
    DOCS.mkdir(parents=True, exist_ok=True)
    st = styles()
    build_executive(DOCS / "Executive-Portfolio.pdf", st)
    build_project_portfolio(DOCS / "Copilot-Project-Portfolio.pdf", st)
    build_architecture(DOCS / "Architecture-Overview.pdf", st)
    for name in (
        "Executive-Portfolio.pdf",
        "Copilot-Project-Portfolio.pdf",
        "Architecture-Overview.pdf",
    ):
        p = DOCS / name
        print(f"Wrote {p} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
