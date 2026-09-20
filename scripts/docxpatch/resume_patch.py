#!/usr/bin/env python3
"""Regenerate the resume .docx from docs/resume.md, preserving the original docx formatting."""
import os, re, shutil, zipfile

SRC   = "/Users/user/projects/124c41/docs/Resume_wong_teck_meng_v2024 (1).docx"
BAK   = "/tmp/resume_original_backup.docx"
WORK  = "/tmp/docxpatch/work"

if not os.path.exists(BAK):
    raise SystemExit("backup missing")
shutil.copy(BAK, SRC)          # always start from the pristine original

if os.path.exists(WORK): shutil.rmtree(WORK)
os.makedirs(WORK)
with zipfile.ZipFile(SRC) as z:
    names = z.namelist()
    z.extractall(WORK)

doc_path  = os.path.join(WORK, "word/document.xml")
rels_path = os.path.join(WORK, "word/_rels/document.xml.rels")
doc  = open(doc_path,  encoding="utf-8").read()
rels = open(rels_path, encoding="utf-8").read()

# ---------------------------------------------------------------- formatting templates
F = 'w:ascii="Calibri" w:hAnsi="Calibri"'
RPR_PLAIN  = f'<w:rPr><w:rFonts {F} /><w:sz w:val="21" /><w:szCs w:val="21" /><w:rtl w:val="0" /><w:lang w:val="en-US" /></w:rPr>'
RPR_BOLD   = f'<w:rPr><w:rFonts {F} /><w:b w:val="1" /><w:bCs w:val="1" /><w:sz w:val="21" /><w:szCs w:val="21" /><w:rtl w:val="0" /><w:lang w:val="en-US" /></w:rPr>'
RPR_S23    = f'<w:rPr><w:rFonts {F} /><w:sz w:val="23" /><w:szCs w:val="23" /><w:rtl w:val="0" /><w:lang w:val="en-US" /></w:rPr>'
RPR_S23_HINT = f'<w:rPr><w:rFonts {F} w:hint="default" /><w:sz w:val="23" /><w:szCs w:val="23" /><w:rtl w:val="0" /><w:lang w:val="en-US" /></w:rPr>'
RPR_COMPANY = f'<w:rPr><w:rFonts {F} /><w:b w:val="1" /><w:bCs w:val="1" /><w:sz w:val="23" /><w:szCs w:val="23" /><w:rtl w:val="0" /><w:lang w:val="en-US" /></w:rPr>'
RPR_H2     = f'<w:rPr><w:rFonts {F} /><w:b w:val="1" /><w:bCs w:val="1" /><w:sz w:val="22" /><w:szCs w:val="22" /><w:rtl w:val="0" /><w:lang w:val="en-US" /></w:rPr>'
RPR_LINK   = '<w:rPr><w:rStyle w:val="Hyperlink.0" /></w:rPr>'

PPR_BODY    = '<w:pPr><w:pStyle w:val="Body A" /></w:pPr>'
PPR_COMPANY = '<w:pPr><w:pStyle w:val="Body A" /><w:spacing w:line="242" w:lineRule="auto" /></w:pPr>'
PPR_ROLE    = '<w:pPr><w:pStyle w:val="Body A" /><w:spacing w:before="80" /></w:pPr>'
PPR_BULLET  = ('<w:pPr><w:pStyle w:val="List Paragraph" /><w:numPr><w:ilvl w:val="0" /><w:numId w:val="2" /></w:numPr>'
               '<w:bidi w:val="0" /><w:ind w:right="0" /><w:jc w:val="left" /></w:pPr>')
PPR_EMPTY   = ('<w:pPr><w:pStyle w:val="List Paragraph" /><w:spacing w:before="0" w:after="0" '
               'w:line="240" w:lineRule="auto" /></w:pPr>')

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def t(text):   return f'<w:t xml:space="preserve">{esc(text)}</w:t>'
def run(text, rpr=RPR_PLAIN): return f'<w:r>{rpr}{t(text)}</w:r>'
def b(text):   return run(text, RPR_BOLD)
def tabrun():  return f'<w:r>{RPR_PLAIN}<w:tab /></w:r>'

def link(url, text):
    return (f'<w:hyperlink r:id="{add_rel(url)}"><w:r>{RPR_LINK}'
            f'{t(text)}</w:r></w:hyperlink>')

def bullet(label, body):
    return f'<w:p>{PPR_BULLET}{b(label)}{run(body)}</w:p>'

def bullet_rich(label, *chunks):
    return f'<w:p>{PPR_BULLET}{b(label)}{"".join(chunks)}</w:p>'

def company(name, location, period):
    """Reproduce the original heading layout: bold name | – location | <tab> | bold period."""
    return ('<w:p>' + PPR_COMPANY + run(name, RPR_COMPANY) + run(" – ", RPR_S23_HINT)
            + run(location, RPR_S23) + tabrun() + run(period, RPR_BOLD) + '</w:p>')

def role(title, dates=None):
    inner = b(title) + (run(dates) if dates else '')
    return f'<w:p>{PPR_ROLE}{inner}</w:p>'

def h2(text):
    return f'<w:p>{PPR_BODY}{run(text, RPR_H2)}</w:p>'

def empty():
    return f'<w:p>{PPR_BODY}<w:r><w:rPr><w:sz w:val="21" /><w:szCs w:val="21" /></w:rPr></w:r></w:p>'

def empty_bullet():
    return f'<w:p>{PPR_EMPTY}<w:r><w:rPr><w:sz w:val="21" /><w:szCs w:val="21" /></w:rPr></w:r></w:p>'

def add_rel(url):
    global rels
    used = [int(x) for x in re.findall(r'Id="rId(\d+)"', rels)]
    new = f"rId{max(used, default=0) + 1}"
    rels = rels.replace("</Relationships>",
        f'<Relationship Id="{new}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
        f'relationships/hyperlink" Target="{esc(url)}" TargetMode="External" /></Relationships>')
    return new

def para_text(seg):
    return ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', seg))

def para_spans():
    return [(m.start(), m.end(), m.group(0)) for m in re.finditer(r'<w:p>(?:(?!</w:p>).)*?</w:p>', doc, re.S)]

def find(fragment, nth=0):
    hits = [s for s in para_spans() if fragment in para_text(s[2])]
    if len(hits) <= nth:
        raise SystemExit(f"NOT FOUND ({nth}): {fragment!r}  (hits={len(hits)})")
    return hits[nth]

def replace(fragment, new_xml, nth=0):
    global doc
    s, e, _ = find(fragment, nth)
    doc = doc[:s] + new_xml + doc[e:]

def insert_after(fragment, new_xml, nth=0):
    global doc
    s, e, _ = find(fragment, nth)
    doc = doc[:e] + new_xml + doc[e:]

def delete(fragment, nth=0):
    global doc
    s, e, _ = find(fragment, nth)
    doc = doc[:s] + doc[e:]

# ================================================================== EDITS
# 1. Executive summary -----------------------------------------------------
replace("20 years of",
        '<w:p>' + PPR_BODY + run("20+ years of ") + b("software engineering")
        + run(" experience. Adept at reverse engineering code with a strong drive for continuous learning "
              "and technical innovation.") + '</w:p>')

# 2. NEW: ST Engineering (insert before uParcel) ---------------------------
stengg = (company("ST Engineering", "Singapore", "2025 - present")
          + role("AI Principal Engineer")
          + bullet("Platform Development", ": Lead the design and development of scalable AI systems, ensuring high performance and reliability.")
          + bullet("MLOps", ": Implement and optimize MLOps practices to streamline the machine learning lifecycle, from development to deployment and monitoring.")
          + bullet("Standardization", ": Establish and enforce best practices for AI systems development, testing, and deployment.")
          + bullet("Collaboration", ": Collaborate with cross-functional teams to integrate AI systems into Maintenance, Repair and Overhaul (MRO) workflows.")
          + bullet("Innovation", ": Stay abreast of the latest advancements in AI, applying this knowledge to improve platform capabilities and processes.")
          + bullet("Mentorship", ": Provide technical guidance and mentorship to junior engineers and team members.")
          + bullet("Client Engagement", ": Develop technical proposals and architecture presentations for the MRO operations team.")
          + bullet("AI Champions", ": Champion AI adoption across Lines of Business.")
          + empty())
replace("uParcel", stengg + company("uParcel", "Singapore", "2023 - 2024"))

# 3. uParcel updates -------------------------------------------------------
replace("DEC 2023", role("AI Engineer", " (DEC 2023 – DEC 2024)"))
replace("Malaysian market", bullet("Market Launch",
        ": Successfully launched optimised last-mile delivery solutions in the Singapore/Malaysian market, "
        "expanding UParcel's presence and capabilities."))
replace("CD/CI Pipeline Management", bullet_rich("CI/CD Pipeline Management",
        run(": Managed the project pipeline for UParcel's Continuous Integration/Continuous Deployment (CI/CD) using the "),
        b("AWS"), run(" tech stack "), b("CDK"),
        run(", ensuring seamless and efficient development operations while maintaining a high degree of "
            "reliability and scalability.")))
replace("Route Optimisation", bullet_rich("Route Optimisation",
        run(": Improved delivery efficiency by optimizing routes using large-scale "), b("data analysis"),
        run(" and heuristic algorithm parameter fine-tuning, resulting in a "),
        run(" "), b("20% increase"), run(" "), run("in driver acceptance rates for listed jobs.")))

# 4. AI Singapore ----------------------------------------------------------
replace("Content Generation", bullet_rich("Content Generation",
        run(": Scoped requirements for event planning for a government agency using "),
        link("https://python.langchain.com/", "LangChain"), run(" and "), b("prompt engineering"), run(".")))
replace("Mentorship: Mentored batches", bullet("Mentorship", ": Mentored Batches 12 and 13 on Computer Vision."))
replace("AI Apprentice (OCT", role("AI Apprentice", " (OCT 2022 – MAR 2023)"))
# "Cloud Architecture" bullet already exists in the original document - no insert needed

# 5. Career transition + Team Fight Tactics --------------------------------
replace("Career transition", company("Career Transition & Independent Projects", "Singapore", "2021 - 2022"))
replace("Self-Hosting: Successfully", bullet_rich("Self-Hosting",
        run(": Successfully self-hosted applications and API services on a personal domain ("),
        link("https://furyhawk.lol/", "https://furyhawk.lol/"), run(") using "), b("Docker Swarm"),
        run(" on 3 Raspberry Pi devices, demonstrating expertise in "), b("containerisation"), run(" and orchestration.")))
replace("Cloud-Native Migration", bullet_rich("Cloud-Native Migration",
        run(": Transitioned hosted applications and API services to "), b("Kubernetes"), run(" using "),
        b("Talos"), run(" and "), b("Proxmox"),
        run(", showcasing the ability to adapt to new technologies and architectures.")))
# the two stray TFT bullets become a titled sub-section
s, e, _ = find("Dockerisation: Containerized")
s2, e2, _ = find("Frontend Development: Implemented")
tft = (empty() + h2("Team Fight Tactics Strategy Application")
       + f'<w:p>{PPR_BODY}{link("https://github.com/furyhawk/tftchamp", "github.com/furyhawk/tftchamp")}</w:p>'
       + bullet("Dockerization", ": Containerized the application to showcase the current patch's gamer meta using feature importances, utilizing Docker to ensure scalability and reliability.")
       + bullet_rich("Frontend Development",
           run(": Implemented the frontend using "), link("https://react.dev/", "React"), run(" and "),
           link("https://zustand.docs.pmnd.rs/", "Zustand"),
           run(", demonstrating proficiency in building responsive and efficient user interfaces.")))
doc = doc[:s] + tft + doc[e2:]

# 6. NCS 2020-2021, BHP ----------------------------------------------------
replace("SAP Edge Development", bullet("SAP Edge Development",
        ": Implemented SAP Edge applications using Agile methodology, demonstrating the ability to work "
        "iteratively and deliver results in a fast-paced environment."))
replace("Maintenance Dashboard", bullet("Maintenance Dashboard",
        ": Developed a Maintenance Dashboard for the Singapore Air Force F-16/Apache Squadron on Edge devices, "
        "improving turnaround reliability and showcasing expertise in building tailored solutions for complex industries."))
replace("Global Rollout", bullet("Global Rollout",
        ": Successfully implemented the Resource Scheduler application globally, enabling mass scheduling of work "
        "to personnel while considering work restrictions and capacity availability."))
replace("Process Improvement", bullet("Process Improvement",
        ": Achieved significant reductions in Time-on-Task and User Error Rate, and improved safety compliance, "
        "demonstrating the ability to develop solutions that drive business value and enhance operational efficiency."))

# 7. Education / ADDITIONAL ------------------------------------------------
replace("Professional association memberships",
        '<w:p>' + PPR_BULLET + run("Professional association memberships: ")
        + link("https://www.aip.org.sg/certificate-verification/2F363E7-2F36256-7B47D/",
               "AI Professionals Association (AIP) - Certificate Verification") + '</w:p>')
insert_after("Language fluency",
        '<w:p>' + PPR_BULLET + run("Open Source Contributions") + run(": ")
        + link("https://github.com/furyhawk", "Active contributor to Open Source Projects") + '</w:p>')

# ================================================================== write
open(doc_path,  "w", encoding="utf-8").write(doc)
open(rels_path, "w", encoding="utf-8").write(rels)

out = "/tmp/docxpatch/out.docx"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for n in names:
        z.write(os.path.join(WORK, n), n)
shutil.copy(out, SRC)
print("OK ->", SRC, os.path.getsize(SRC), "bytes")
