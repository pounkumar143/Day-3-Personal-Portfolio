import streamlit as st
from Utils.pdf_generator import export_portfolio_pdf
from PIL import Image
import tempfile

st.set_page_config(page_title="Professional Portfolio Builder", layout="wide")

if "portfolio" not in st.session_state:
    st.session_state.portfolio = {
        "name": "",
        "photo_file": None,
        "photo_path": "",
        "title": "",
        "summary": "",
        "email": "",
        "linkedin": "",
        "phone": "",
        "work_exp": [],
        "education": [],
        "certifications": [],
        "skills_tech": "",
        "skills_soft": "",
        "projects": [],
        "testimonials": [],
        "blog_links": [],
        "contact_message": ""
    }

section = st.sidebar.radio(
    "Navigation", ["Create Portfolio", "Preview Portfolio", "Download Your Portfolio"]
)

if section == "Create Portfolio":
    st.title("📝 Create Portfolio")
    with st.expander("👤 Profile/Contact", expanded=True):
        cols = st.columns([1.1, 2])
        with cols[0]:
            photo_file = st.file_uploader("Upload Profile Photo", type=["jpg", "jpeg", "png"])
            if photo_file:
                img = Image.open(photo_file)
                tempdir = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                img.convert('RGB').save(tempdir.name)
                st.session_state.portfolio["photo_file"] = photo_file
                st.session_state.portfolio["photo_path"] = tempdir.name
                st.image(img, width=130, caption="Preview")
        with cols[1]:
            st.session_state.portfolio["name"] = st.text_input("Full Name", value=st.session_state.portfolio["name"])
            st.session_state.portfolio["title"] = st.text_input("Professional Title", value=st.session_state.portfolio["title"])
            st.session_state.portfolio["summary"] = st.text_area(
                "Professional Summary", value=st.session_state.portfolio["summary"], height=70)
            st.session_state.portfolio["email"] = st.text_input("Email", value=st.session_state.portfolio["email"])
            st.session_state.portfolio["linkedin"] = st.text_input("LinkedIn", value=st.session_state.portfolio["linkedin"])
            st.session_state.portfolio["phone"] = st.text_input("Phone", value=st.session_state.portfolio["phone"])
    with st.expander("💼 Work Experience"):
        exp_org = st.text_input("Company/Organization", key="exp_org")
        exp_role = st.text_input("Role/Position", key="exp_role")
        exp_time = st.text_input("Duration", key="exp_time")
        exp_loc = st.text_input("Location", key="exp_loc")
        exp_desc = st.text_area("Achievements/Responsibilities", key="exp_desc", height=70)  # CHANGED height here!
        add_exp = st.button("Add Experience")
        if add_exp and exp_role:
            st.session_state.portfolio["work_exp"].append({
                "org": exp_org, "role": exp_role, "duration": exp_time,
                "location": exp_loc, "desc": exp_desc
            })
        for n, job in enumerate(st.session_state.portfolio["work_exp"]):
            st.markdown(f'- **{job["role"]}**, {job["org"]} ({job["location"]} | {job["duration"]}): {job["desc"]}')
            if st.button(f"🗑 Delete Experience {n+1}", key=f"del_exp_{n}"):
                st.session_state.portfolio["work_exp"].pop(n)
    with st.expander("🎓 Education"):
        edu_school = st.text_input("Institution", key="edu_school")
        edu_degree = st.text_input("Degree", key="edu_degree")
        edu_year = st.text_input("Year of Graduation", key="edu_year")
        add_edu = st.button("Add Education")
        if add_edu and edu_school:
            st.session_state.portfolio["education"].append({
                "school": edu_school, "degree": edu_degree, "year": edu_year
            })
        for n, edu in enumerate(st.session_state.portfolio["education"]):
            st.markdown(f'- **{edu["degree"]}**, {edu["school"]} ({edu["year"]})')
            if st.button(f"🗑 Delete Education {n+1}", key=f"del_edu_{n}"):
                st.session_state.portfolio["education"].pop(n)
    with st.expander("🎖 Certifications"):
        cert_text = st.text_input("Certification", key="cert_text")
        add_cert = st.button("Add Certification")
        if add_cert and cert_text:
            st.session_state.portfolio["certifications"].append(cert_text)
        for n, cert in enumerate(st.session_state.portfolio["certifications"]):
            st.markdown(f'- {cert}')
            if st.button(f"🗑 Delete Cert {n+1}", key=f"del_cert_{n}"):
                st.session_state.portfolio["certifications"].pop(n)
    with st.expander("🧰 Skills Overview"):
        st.session_state.portfolio["skills_tech"] = st.text_input(
            "Technical Skills (comma-separated)", value=st.session_state.portfolio["skills_tech"])
        st.session_state.portfolio["skills_soft"] = st.text_input(
            "Soft Skills (comma-separated)", value=st.session_state.portfolio["skills_soft"])
    with st.expander("💡 Projects & Case Studies"):
        pj_name = st.text_input("Project Name", key="pj_name")
        pj_desc = st.text_area("Short Description", key="pj_desc", height=70)  # CHANGED height here!
        pj_tech = st.text_input("Technologies Used", key="pj_tech")
        pj_role = st.text_input("Your Role", key="pj_role")
        pj_link = st.text_input("Link (optional)", key="pj_link")
        pj_outcome = st.text_input("Outcome/Impact", key="pj_outcome")
        add_pj = st.button("Add Project")
        if add_pj and pj_name:
            st.session_state.portfolio["projects"].append({
                "name": pj_name, "desc": pj_desc, "tech": pj_tech,
                "role": pj_role, "link": pj_link, "outcome": pj_outcome
            })
        for n, pj in enumerate(st.session_state.portfolio["projects"]):
            st.markdown(f'**{pj["name"]}** ({pj["tech"]}) – {pj["role"]}: {pj["desc"]}\nOutcome: {pj["outcome"]}')
            if pj["link"]:
                st.markdown(f"[Link]({pj['link']})")
            if st.button(f"🗑 Delete Project {n+1}", key=f"del_pj_{n}"):
                st.session_state.portfolio["projects"].pop(n)
    with st.expander("🗣 Testimonials"):
        test_name = st.text_input("Referee Name/Company", key="test_name")
        test_text = st.text_area("Testimonial Text", key="test_text", height=70)  # CHANGED height here!
        add_test = st.button("Add Testimonial")
        if add_test and test_name and test_text:
            st.session_state.portfolio["testimonials"].append({
                "name": test_name, "text": test_text
            })
        for n, t in enumerate(st.session_state.portfolio["testimonials"]):
            st.markdown(f'*"{t["text"]}" – {t["name"]}*')
            if st.button(f"🗑 Delete Testimonial {n+1}", key=f"del_test_{n}"):
                st.session_state.portfolio["testimonials"].pop(n)
    with st.expander("📚 Blog/Articles"):
        blog_link = st.text_input("Blog/Article/Tutorial Link", key="blog_link")
        add_blog = st.button("Add Blog/Article")
        if add_blog and blog_link:
            st.session_state.portfolio["blog_links"].append(blog_link)
        for n, link in enumerate(st.session_state.portfolio["blog_links"]):
            st.markdown(f'- [Blog/Article]({link})')
            if st.button(f"🗑 Delete Blog {n+1}", key=f"del_blog_{n}"):
                st.session_state.portfolio["blog_links"].pop(n)
    with st.expander("✉️ Contact/Inquiry"):
        st.session_state.portfolio["contact_message"] = st.text_area(
            "Contact Note (for inquiry form)", value=st.session_state.portfolio["contact_message"], height=70)  # CHANGED height here!

if section == "Preview Portfolio":
    p = st.session_state.portfolio
    st.title("🌟 Portfolio Preview")
    c1, c2 = st.columns([1, 2])
    with c1:
        if p['photo_path']:
            img = Image.open(p['photo_path'])
            st.image(img, width=150)
        else:
            st.image("https://placehold.co/180x180", width=150)
    with c2:
        st.header(p['name'])
        st.markdown(f"**{p['title']}**")
        st.markdown(f"{p['summary']}")
        st.write(f"**Email:** {p['email']}   \n**LinkedIn:** {p['linkedin']}   \n**Phone:** {p['phone']}")
    st.divider()
    if p['work_exp']:
        st.subheader("💼 Work Experience")
        for job in p['work_exp']:
            st.markdown(f"**{job['role']}**, {job['org']} ({job['location']} | {job['duration']})\n> {job['desc']}")
    if p['education']:
        st.subheader("🎓 Education")
        for edu in p['education']:
            st.markdown(f"- **{edu['degree']}**, {edu['school']} ({edu['year']})")
    if p['certifications']:
        st.subheader("🎖 Certifications")
        st.markdown("\n".join([f"- {c}" for c in p['certifications']]))
    if p['skills_tech'] or p['skills_soft']:
        st.subheader("🧰 Skills")
        if p['skills_tech']:
            st.markdown(f"**Technical:** {p['skills_tech']}")
        if p['skills_soft']:
            st.markdown(f"**Soft skills:** {p['skills_soft']}")
    if p['projects']:
        st.subheader("💡 Projects & Case Studies")
        for pj in p['projects']:
            st.markdown(f"**{pj['name']}** ({pj['tech']})\n— {pj['role']}\n{pj['desc']}\nOutcome: {pj['outcome']}")
            if pj["link"]:
                st.markdown(f"[Link]({pj['link']})")
    if p['testimonials']:
        st.subheader("🗣 Testimonials")
        for t in p['testimonials']:
            st.markdown(f'"{t["text"]}" – {t["name"]}')
    if p['blog_links']:
        st.subheader("📚 Blog & Articles")
        for l in p['blog_links']:
            st.markdown(f'- [Link]({l})')
    if p['contact_message']:
        st.subheader("✉️ Contact")
        st.info(p['contact_message'])

if section == "Download Your Portfolio":
    p = st.session_state.portfolio
    st.title("⬇️ Download Your Portfolio")
    if p["name"]:
        pdf_bytes = export_portfolio_pdf(p)
        st.download_button(
            "Download Portfolio PDF",
            pdf_bytes,
            file_name=f"{p['name'].replace(' ','_')}_portfolio.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Please fill your details first in Create Portfolio.")
