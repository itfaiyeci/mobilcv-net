# -*- coding: utf-8 -*-
"""EN meslek sayfalarini genisletir (Search Console'da gosterim alan: nurse, architect, lawyer, teacher).
Dogruluk kurali: istatistik/yuzde/uydurma kaynak yok; ornek cumleler "Example" olarak isaretli.
Ayrica "for a Architect" -> "for an Architect" dilbilgisi duzeltmesi (tum EN sablon sayfalari).
Idempotent. Kullanim: python3 en_meslek_genislet.py (mobilcv-net kokunde)"""
import json, re
from pathlib import Path

def ul(items): return "<ul>\n" + "".join(f"    <li>{x}</li>\n" for x in items) + "</ul>\n"
def ol(items): return "<ol>\n" + "".join(f"    <li>{x}</li>\n" for x in items) + "</ol>\n"
def ex(items): return ul([f"Example: “{x}”" for x in items])

PAGES = {
"architect-cv-template.html": {
 "html":
 "<h2>What to Include in an Architect CV</h2>\n<p>A clear order helps a practice find what it needs quickly:</p>\n" + ol([
  "Contact details and a working portfolio link",
  "A short professional summary (two or three lines)",
  "Professional registration or licence status, if you have one",
  "Work experience, with the projects you worked on and your role in each",
  "Education, including your diploma or thesis project",
  "Software skills",
  "Competitions, awards and exhibitions",
  "Languages"]) +
 "<h2>Example Professional Summaries</h2>\n" + ex([
  "Architectural assistant with experience in residential and mixed-use projects from concept design to construction drawings. Confident in Revit and AutoCAD, and comfortable coordinating with structural and MEP consultants.",
  "Recent architecture graduate with a diploma project on adaptive reuse of industrial buildings. Experienced in SketchUp, Rhino and physical model making through two practice internships."]) +
 "<h2>Skills to List</h2>\n<p><strong>Technical:</strong> concept and design development, technical drawings and construction documents, BIM coordination, knowledge of local building regulations, site visits and supervision, 3D visualisation.</p>\n<p><strong>Working with people:</strong> presenting to clients, coordinating with engineers and contractors, teamwork on competition entries.</p>\n" +
 "<h2>Registration and the Title “Architect”</h2>\n<p>In some countries “architect” is a protected title. In the UK, for example, only people registered with the Architects Registration Board (ARB) may practise or do business under that title; in the United States, licensing is handled by each state. If you are not registered yet, describe your role accurately, for example “architectural assistant”, and state where you are in the registration process.</p>\n" +
 "<h2>Common Mistakes</h2>\n" + ul([
  "A missing or broken portfolio link. Check it before every application.",
  "Listing software without saying what you used it for.",
  "Putting large images inside the CV. Keep visuals in the portfolio so the CV stays readable by application systems and small enough to email.",
  "Calling yourself an architect where the title is protected and you are not registered."]),
 "faq": [
  ("Should I put images in my architect CV?", "Usually keep the CV text-based and put drawings and renders in your portfolio. A text-based CV is easier for application systems to read and keeps the file small."),
  ("How long should an architect CV be?", "One to two pages is a common length. If the employer gives a limit, follow it."),
  ("What should a graduate architect put on a CV?", "Your diploma project, internships or placements, competition entries, software skills and any model-making or site experience."),
  ("Should I add a photo to my CV?", "It depends on the country. In the UK and the US a photo is usually left out; in some other countries it is common. See our <a href=\"cv-rules-by-country.html\">CV rules by country</a>.")]},

"nurse-cv-template.html": {
 "html":
 "<h2>What to Include in a Nursing CV</h2>\n" + ol([
  "Contact details",
  "Professional registration (for example your NMC PIN in the UK, or your state RN licence in the US)",
  "A short professional summary with your clinical area",
  "Clinical experience: ward or unit, type of patients, your main responsibilities",
  "Education and clinical placements",
  "Certifications such as Basic Life Support (BLS) or Advanced Life Support (ALS), with expiry dates",
  "Clinical skills and the electronic health record systems you have used",
  "Languages"]) +
 "<h2>Registration Comes First</h2>\n<p>Employers check registration before anything else. In the UK, nurses must be registered with the Nursing and Midwifery Council (NMC). In the United States, registered nurses need a licence from the state where they work, which requires passing the NCLEX-RN exam. Put your registration near the top of the CV; if it is in progress, say so and give the expected date.</p>\n" +
 "<h2>Example Professional Summaries</h2>\n" + ex([
  "Registered nurse with experience on a busy surgical ward, including post-operative care, wound management and patient education. Calm under pressure and confident working in a multidisciplinary team.",
  "Newly qualified nurse with clinical placements in emergency care, paediatrics and community nursing. BLS certified and keen to develop in acute care."]) +
 "<h2>Example Experience Bullet Points</h2>\n" + ex([
  "Provided post-operative care including pain assessment, wound care and early mobilisation.",
  "Administered and documented medication in line with ward policy and the electronic prescribing system.",
  "Supported newly qualified nurses and students during their placements.",
  "Communicated care plans to patients and families and coordinated discharges with the community team."]) +
 "<h2>Common Mistakes</h2>\n" + ul([
  "Leaving out your registration number or licence status.",
  "Writing only generic duties (“caring for patients”) instead of your clinical area and skills.",
  "Including any information that could identify a patient. Never do this, even as an example.",
  "Unexplained gaps. A short line such as “Career break – family care” is enough."]),
 "faq": [
  ("Should I include my NMC PIN or licence number on my CV?", "Many employers ask for it, so it is common to include it in a registration section near the top. If you prefer, you can provide it at application stage instead."),
  ("How do I write a CV as a newly qualified nurse?", "Lead with your registration status and clinical placements. For each placement, give the setting and the skills you practised."),
  ("How long should a nursing CV be?", "Two pages is a common length. Follow any limit the employer gives."),
  ("Should I list certifications like BLS?", "Yes. Give the certification name and its expiry date, because many employers require it to be current.")]},

"lawyer-cv-template.html": {
 "html":
 "<h2>What to Include in a Lawyer CV</h2>\n" + ol([
  "Contact details",
  "Qualification and admission (for example solicitor or barrister in England and Wales, or the state bar you are admitted to in the US)",
  "A short professional summary with your practice areas",
  "Legal experience: firm or organisation, practice area, the type of matters you worked on and your role",
  "Education, including law school and professional training",
  "Legal research tools and languages",
  "Publications, moots or pro bono work, if relevant"]) +
 "<h2>State Your Admission Clearly</h2>\n<p>Legal employers first check whether you can practise. In England and Wales, say whether you are a solicitor (regulated by the Solicitors Regulation Authority) or a barrister (called to the Bar). In the United States, list each state bar you are admitted to. Trainees and students can give an expected admission date.</p>\n" +
 "<h2>Example Experience Bullet Points</h2>\n" + ex([
  "Drafted and negotiated commercial contracts for clients in the technology sector.",
  "Conducted legal research and prepared memos on employment law questions for partners.",
  "Prepared court bundles and witness statements in civil litigation matters.",
  "Supported due diligence on company acquisitions, reviewing corporate and employment documents."]) +
 "<h2>Confidentiality on Your CV</h2>\n<p>Describe the type of matter, the sector and your role rather than naming clients. Only name a client or case if it is already public and your employer allows it.</p>\n" +
 "<h2>Common Mistakes</h2>\n" + ul([
  "Typos and inconsistent formatting. Legal employers read CVs as a sample of your attention to detail.",
  "Vague lines such as “handled cases” with no practice area or role.",
  "Revealing confidential client information.",
  "Leaving your admission status unclear."]),
 "faq": [
  ("Should I name clients on my legal CV?", "Usually not. Describe the sector and type of work instead, unless the matter is public and your employer has agreed."),
  ("How long should a lawyer CV be?", "Two pages is a common length for qualified lawyers; one page is often enough for students and trainees. Follow any limit the employer sets."),
  ("What should a law student put on a CV?", "Your degree and grades, legal work experience or vacation schemes, moots, pro bono work, and skills such as research and drafting."),
  ("Should I list legal research tools?", "Yes, briefly. Name the databases you have used, for example Westlaw or LexisNexis.")]},

"teacher-cv-template.html": {
 "html":
 "<h2>What to Include in a Teacher CV</h2>\n" + ol([
  "Contact details",
  "Teaching qualification (for example Qualified Teacher Status in England, or a state teaching licence in the US)",
  "A short professional summary with your subject and the age range you teach",
  "Teaching experience: school, subjects, year groups or grades, and responsibilities",
  "Education and teacher training, including teaching practice",
  "Extra responsibilities such as clubs, pastoral roles or exam coordination",
  "Classroom technology and languages"]) +
 "<h2>Example Professional Summaries</h2>\n" + ex([
  "Secondary mathematics teacher experienced in teaching mixed-ability classes and preparing students for national exams. Uses regular assessment to adapt lessons to each group.",
  "Primary teacher with a focus on early reading and inclusive teaching. Experienced in supporting pupils with special educational needs alongside teaching assistants."]) +
 "<h2>Example Experience Bullet Points</h2>\n" + ex([
  "Planned and taught lessons for students aged 11 to 16, following the national curriculum.",
  "Adapted materials for students with special educational needs in cooperation with the support team.",
  "Ran an after-school coding club and organised a school science fair.",
  "Communicated progress to parents through reports and parent meetings."]) +
 "<h2>Skills to List</h2>\n<p>Lesson planning, classroom management, differentiation, assessment and feedback, safeguarding awareness, working with parents, and the digital tools you use, such as Google Classroom or Microsoft Teams.</p>\n" +
 "<h2>Common Mistakes</h2>\n" + ul([
  "Not stating your subject and age range clearly at the top.",
  "Listing duties without the year groups or grades you taught.",
  "Leaving out your teaching qualification or its status.",
  "Writing a long teaching philosophy in the CV. Keep it to one or two lines; the cover letter is the place to expand."]),
 "faq": [
  ("How should a newly qualified teacher write a CV?", "Start with your qualification, then your teaching practice placements: school type, subjects, age groups and what you taught."),
  ("How long should a teacher CV be?", "Two pages is a common length. Follow the school's application instructions; some schools use their own application form instead of a CV."),
  ("Should I include a teaching philosophy?", "A short line in your profile is enough. Explain your approach in the cover letter."),
  ("What skills should a teacher CV include?", "Lesson planning, classroom management, differentiation, assessment, communication with parents and the classroom technology you use.")]},
}

total = 0
for fname, d in PAGES.items():
    p = Path("en") / fname; s = p.read_text(encoding="utf-8")
    if "data-en-genislet" in s:
        continue
    block = "<div data-en-genislet>\n" + d["html"] + "<h2>Frequently Asked Questions</h2>\n" + "".join(
        f"<h3>{q}</h3>\n<p>{a}</p>\n" for q, a in d["faq"]) + "</div>\n\n"
    assert s.count("<h2>Conclusion</h2>") == 1, fname
    s = s.replace("<h2>Conclusion</h2>", block + "<h2>Conclusion</h2>")
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in d["faq"]]}
    s = s.replace("</head>", '    <script type="application/ld+json">' + json.dumps(faq, ensure_ascii=False) + "</script>\n</head>", 1)
    p.write_text(s, encoding="utf-8"); total += 1

# Dilbilgisi: "for a Architect position" -> "for an Architect position"
fix = 0
for p in sorted(Path("en").glob("*-cv-template.html")):
    s = p.read_text(encoding="utf-8")
    t = re.sub(r"\bfor a ([AEIOU])", r"for an \1", s)
    if t != s:
        p.write_text(t, encoding="utf-8"); fix += 1
print("genisletilen:", total, "| dilbilgisi duzeltilen:", fix)
