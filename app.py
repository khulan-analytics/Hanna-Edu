import streamlit as st
from urllib.parse import quote

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Hanna Edu | Education, Visa, Travel & Relocation",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# SETTINGS
# =========================================================

# Optional: paste a direct image link (https://...) to use a photo behind the
# hero section. Leave as None for the built-in gradient design (no external
# images needed, so nothing can break).
HERO_PHOTO = None

CONTACT_EMAIL = "mongolianhannaedu@gmail.com"
WEBSITE = "https://www.hanna-edu.com/"

DESTINATIONS = ["United States", "Canada", "Australia", "South Korea", "Europe", "Other"]
CONTACT_SERVICES = ["Education", "Visa Consulting", "Travel", "Relocation", "Language Courses"]
PAGES = ["Home", "Education", "Visa Consulting", "Travel & Relocation", "Contact Us"]


def flatten(markup: str) -> str:
    """Strip indentation/blank lines so Markdown never renders HTML as a code block."""
    return " ".join(line.strip() for line in markup.splitlines() if line.strip())


def html(markup: str):
    st.markdown(flatten(markup), unsafe_allow_html=True)


# =========================================================
# STYLES
# =========================================================

html(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
  --navy: #0F1D33;
  --navy-2: #1B2F4E;
  --gold: #C9A24D;
  --gold-soft: #E9D7A8;
  --cream: #F6F4EE;
  --ink: #1F2937;
  --muted: #64748B;
  --line: #E5E1D6;
}

/* hide default Streamlit chrome and sidebar */
#MainMenu, footer, header[data-testid="stHeader"] { display: none !important; visibility: hidden; }
section[data-testid="stSidebar"], div[data-testid="collapsedControl"],
div[data-testid="stSidebarCollapsedControl"] { display: none !important; }

.stApp { background: var(--cream); font-family: 'DM Sans', sans-serif; color: var(--ink); }
.block-container { max-width: 1180px; padding-top: 1rem; padding-bottom: 0; }

h1, h2, h3, h4 { font-family: 'Playfair Display', serif !important; color: var(--navy) !important; letter-spacing: -0.01em; }

/* ---------- top navigation ---------- */
.brand { font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 700; color: var(--navy); line-height: 1; }
.brand span { color: var(--gold); }
.brand-sub { font-size: 10px; letter-spacing: 3px; color: var(--muted); margin-top: 4px; font-weight: 600; }

/* Menu buttons: inactive = white pill with navy text, active = navy pill with gold text.
   Two selector sets so it works on any Streamlit version or theme. */
[class*="st-key-nav_"] button,
div[data-testid="stHorizontalBlock"]:has(.brand) button {
  background: #FFFFFF !important; color: #0F1D33 !important; border: 1px solid #D9D3C3 !important;
  border-radius: 999px !important; font-weight: 600; padding: 0.45rem 0.6rem; box-shadow: none !important;
}
[class*="st-key-nav_"] button *,
div[data-testid="stHorizontalBlock"]:has(.brand) button * { color: #0F1D33 !important; font-size: 14px; }
[class*="st-key-nav_"] button:hover,
div[data-testid="stHorizontalBlock"]:has(.brand) button:hover {
  background: #F3EBD6 !important; border-color: #C9A24D !important;
}
[class*="st-key-nav_"] button[kind="primary"],
[class*="st-key-nav_"] button[data-testid="stBaseButton-primary"],
div[data-testid="stHorizontalBlock"]:has(.brand) button[kind="primary"],
div[data-testid="stHorizontalBlock"]:has(.brand) button[data-testid="stBaseButton-primary"] {
  background: #0F1D33 !important; border-color: #0F1D33 !important;
}
[class*="st-key-nav_"] button[kind="primary"] *,
[class*="st-key-nav_"] button[data-testid="stBaseButton-primary"] *,
div[data-testid="stHorizontalBlock"]:has(.brand) button[kind="primary"] *,
div[data-testid="stHorizontalBlock"]:has(.brand) button[data-testid="stBaseButton-primary"] * {
  color: #E9D7A8 !important;
}
.stApp { color-scheme: light; }

/* ---------- hero ---------- */
.hero {
  position: relative; overflow: hidden; border-radius: 22px; padding: 76px 56px;
  background:
    radial-gradient(circle at 85% 20%, rgba(201,162,77,0.32), transparent 45%),
    radial-gradient(circle at 10% 90%, rgba(255,255,255,0.07), transparent 40%),
    linear-gradient(135deg, var(--navy) 0%, var(--navy-2) 100%);
  color: white; margin-top: 8px;
}
.hero.photo::before { content:""; position:absolute; inset:0; background-size:cover; background-position:center; opacity:.35; }
.hero::after {
  content:""; position:absolute; right:-80px; top:-80px; width:380px; height:380px; border-radius:50%;
  border: 1px solid rgba(233,215,168,0.25); box-shadow: 0 0 0 40px rgba(233,215,168,0.05), 0 0 0 90px rgba(233,215,168,0.03);
}
.hero > * { position: relative; z-index: 1; }
.eyebrow { color: var(--gold); font-size: 12px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; }
.hero h1 { color: white !important; font-size: 52px; line-height: 1.1; margin: 14px 0 18px; max-width: 700px; }
.hero p { color: #D5DCE8; font-size: 17px; line-height: 1.75; max-width: 600px; }

/* ---------- page header ---------- */
.page-head {
  border-radius: 20px; padding: 48px 48px; margin: 8px 0 28px; color: white;
  background: radial-gradient(circle at 90% 10%, rgba(201,162,77,0.3), transparent 45%),
              linear-gradient(135deg, var(--navy), var(--navy-2));
}
.page-head h1 { color: white !important; font-size: 40px; margin: 10px 0 10px; }
.page-head p { color: #D5DCE8; font-size: 16px; line-height: 1.7; max-width: 640px; margin: 0; }

/* ---------- trust strip ---------- */
.trust { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; background: white; border: 1px solid var(--line);
  border-radius: 16px; margin: 28px 0 8px; box-shadow: 0 8px 28px rgba(15,29,51,0.06); }
.trust div { padding: 22px 20px; text-align: center; border-right: 1px solid var(--line); }
.trust div:last-child { border-right: none; }
.trust b { display: block; color: var(--navy); font-size: 15px; }
.trust small { color: var(--muted); font-size: 12.5px; }

/* ---------- sections ---------- */
.section { margin: 56px 0 22px; }
.section h2 { font-size: 34px; margin: 8px 0 8px; }
.section p.lead { color: var(--muted); max-width: 640px; line-height: 1.7; margin: 0; }
.section .eyebrow { color: #A9822F; }

.card {
  background: white; border: 1px solid var(--line); border-radius: 16px; padding: 28px; margin-bottom: 16px; min-height: 210px;
  box-shadow: 0 2px 10px rgba(15,29,51,0.03); transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
}
.card:hover { transform: translateY(-4px); box-shadow: 0 16px 34px rgba(15,29,51,0.10); border-color: var(--gold); }
.icon-badge { width: 52px; height: 52px; border-radius: 14px; background: #F3EBD6; display:flex; align-items:center;
  justify-content:center; font-size: 26px; margin-bottom: 16px; }
.card h3 { font-size: 21px; margin: 0 0 8px; }
.card p { color: var(--muted); font-size: 14.5px; line-height: 1.75; margin: 0; }

.dest {
  border-radius: 16px; padding: 28px 22px; min-height: 190px; color: white; margin-bottom: 16px;
  background: linear-gradient(160deg, var(--navy-2), var(--navy)); border-bottom: 3px solid var(--gold);
  transition: transform .2s ease;
}
.dest:hover { transform: translateY(-4px); }
.dest .flag { font-size: 34px; }
.dest h3 { color: white !important; font-size: 20px; margin: 12px 0 6px; }
.dest p { color: #CBD5E1; font-size: 13px; line-height: 1.6; margin: 0; }

.why { display: flex; gap: 16px; align-items: flex-start; padding: 6px 0 18px; }
.why .num { flex: 0 0 44px; height: 44px; border-radius: 50%; background: var(--navy); color: var(--gold);
  display:flex; align-items:center; justify-content:center; font-weight:700; font-family:'Playfair Display',serif; }
.why h4 { margin: 0 0 4px; font-size: 18px; }
.why p { margin: 0; color: var(--muted); font-size: 14.5px; line-height: 1.7; }

.step { background: white; border: 1px solid var(--line); border-radius: 16px; padding: 26px; min-height: 190px; position: relative; }
.step .n { font-family: 'Playfair Display', serif; font-size: 40px; color: var(--gold); font-weight: 700; line-height: 1; }
.step h3 { font-size: 19px; margin: 10px 0 6px; }
.step p { color: var(--muted); font-size: 14px; line-height: 1.7; margin: 0; }

.cta {
  border-radius: 20px; padding: 52px 48px; margin: 56px 0 0; text-align: center; color: white;
  background: radial-gradient(circle at 15% 20%, rgba(201,162,77,0.3), transparent 45%), linear-gradient(135deg, var(--navy), var(--navy-2));
}
.cta h2 { color: white !important; font-size: 34px; margin: 0 0 10px; }
.cta p { color: #D5DCE8; max-width: 560px; margin: 0 auto; line-height: 1.7; }

.note { background: #FBF6E8; border-left: 4px solid var(--gold); border-radius: 10px; padding: 18px 22px; color: #5B4B1F; font-size: 14px; line-height: 1.7; }
.checklist li { margin-bottom: 8px; color: var(--ink); }

/* ---------- contact ---------- */
.contact-card { background:white; border:1px solid var(--line); border-radius:16px; padding:22px; text-align:center; }
.contact-card .flag { font-size: 28px; }
.contact-card b { display:block; color: var(--navy); margin-top: 6px; }
.contact-card span { color: var(--muted); font-size: 15px; }

/* ---------- footer ---------- */
.footer { background: var(--navy); color: #CBD5E1; border-radius: 20px 20px 0 0; padding: 44px 44px 24px; margin-top: 56px; }
.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1.4fr; gap: 32px; }
.footer .brand { color: white; }
.footer h4 { color: var(--gold) !important; font-family: 'DM Sans', sans-serif !important; font-size: 12px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px; }
.footer p, .footer li { font-size: 13.5px; line-height: 1.8; color: #CBD5E1; }
.footer ul { list-style: none; padding: 0; margin: 0; }
.footer a { color: var(--gold-soft); text-decoration: none; }
.footer .legal { border-top: 1px solid rgba(255,255,255,0.12); margin-top: 28px; padding-top: 18px; font-size: 12px; color: #94A3B8; }

/* ---------- buttons, inputs ---------- */
.stButton > button:not([class*="nav"]), [data-testid="stFormSubmitButton"] button, [data-testid="stLinkButton"] a {
  background: var(--navy); color: white !important; border: 1px solid var(--gold); border-radius: 10px;
  font-weight: 600; padding: 0.55rem 1.3rem;
}
.stButton > button p, [data-testid="stFormSubmitButton"] button p, [data-testid="stLinkButton"] a p { color: inherit !important; }
.stButton > button:not([class*="nav"]):hover, [data-testid="stFormSubmitButton"] button:hover, [data-testid="stLinkButton"] a:hover {
  background: var(--gold); color: var(--navy) !important; border-color: var(--gold);
}
.st-key-hero_primary button { background: var(--gold) !important; color: var(--navy) !important; }
.st-key-hero_primary button:hover { background: var(--navy) !important; color: white !important; }

div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, textarea { border-radius: 10px !important; }
div[data-testid="stForm"] { background: white; border: 1px solid var(--line); border-radius: 16px; padding: 28px; }
details { background: white; border-radius: 12px !important; border: 1px solid var(--line) !important; }

@media (max-width: 768px) {
  .hero { padding: 44px 26px; } .hero h1 { font-size: 34px; }
  .trust { grid-template-columns: repeat(2, 1fr); } .footer-grid { grid-template-columns: 1fr; }
  .page-head { padding: 32px 26px; } .page-head h1 { font-size: 30px; }
}
</style>
"""
)

# =========================================================
# STATE + NAVIGATION HELPERS
# =========================================================

st.session_state.setdefault("page", "Home")


def navigate(page_name):
    st.session_state["page"] = page_name


def go_to_contact(destination, services, message):
    """Button callback: prefill the contact form and switch to it."""
    st.session_state["prefill_destination"] = destination
    st.session_state["prefill_services"] = services
    st.session_state["prefill_message"] = message
    st.session_state["page"] = "Contact Us"


def normalize_destination(dest):
    if dest == "Schengen / Europe":
        return "Europe"
    return dest if dest in DESTINATIONS else "Other"


def section(label, title, lead=""):
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    html(f'<div class="section"><div class="eyebrow">{label}</div><h2>{title}</h2>{lead_html}</div>')


def page_head(label, title, subtitle):
    html(
        f"""<div class="page-head"><div class="eyebrow">{label}</div>
        <h1>{title}</h1><p>{subtitle}</p></div>"""
    )


def cards(items, n_cols):
    cols = st.columns(n_cols, gap="medium")
    for i, (icon, title, text) in enumerate(items):
        with cols[i % n_cols]:
            html(
                f"""<div class="card"><div class="icon-badge">{icon}</div>
                <h3>{title}</h3><p>{text}</p></div>"""
            )


def cta_band(title, text):
    html(f'<div class="cta"><h2>{title}</h2><p>{text}</p></div>')
    st.write("")
    _, mid, _ = st.columns([1, 1, 1])
    with mid:
        st.button(
            "Request a Consultation",
            key=f"cta_{st.session_state['page']}",
            use_container_width=True,
            on_click=go_to_contact,
            args=("United States", [], ""),
        )


# =========================================================
# TOP NAVIGATION
# =========================================================

nav_cols = st.columns([2.2, 1, 1.15, 1.5, 1.2, 1.1], gap="small", vertical_alignment="center")

with nav_cols[0]:
    html('<div class="brand">HANNA <span>EDU</span></div><div class="brand-sub">GLOBAL CONSULTANCY</div>')

for col, name in zip(nav_cols[1:], PAGES):
    with col:
        st.button(
            name,
            key=f"nav_{name}",
            type="primary" if st.session_state["page"] == name else "secondary",
            on_click=navigate,
            args=(name,),
            use_container_width=True,
        )

page = st.session_state["page"]

# =========================================================
# HOME
# =========================================================

if page == "Home":
    photo_css = (
        f"<style>.hero.photo::before{{background-image:url('{HERO_PHOTO}');}}</style>" if HERO_PHOTO else ""
    )
    html(
        f"""{photo_css}
        <div class="hero {'photo' if HERO_PHOTO else ''}">
          <div class="eyebrow">Education · Visa · Travel · Relocation</div>
          <h1>Your trusted partner for studying and living abroad.</h1>
          <p>Hanna Edu guides students and families through school placement, visa preparation,
          travel planning and relocation, with clear, practical advice at every step.</p>
        </div>"""
    )

    b1, b2, _ = st.columns([1.1, 1.1, 3])
    with b1:
        st.button(
            "Start Your Inquiry",
            key="hero_primary",
            use_container_width=True,
            on_click=go_to_contact,
            args=("United States", [], ""),
        )
    with b2:
        st.button("Visa Consulting", key="hero_secondary", use_container_width=True, on_click=navigate, args=("Visa Consulting",))

    html(
        """<div class="trust">
        <div><b>Education</b><small>Schools, universities &amp; ESL</small></div>
        <div><b>Visa Guidance</b><small>Documents &amp; preparation</small></div>
        <div><b>Travel &amp; Relocation</b><small>Plan and settle in</small></div>
        <div><b>Language Courses</b><small>English &amp; Korean online</small></div>
        </div>"""
    )

    section("WHAT WE DO", "Services built around your journey",
            "From your first question to your arrival abroad, everything in one place.")
    cards(
        [
            ("🎓", "Education Abroad", "School and university placement, ESL, undergraduate and graduate programs, with application guidance."),
            ("🛂", "Visa Consulting", "Visitor and student visa guidance, document preparation and category change support."),
            ("✈️", "Travel Services", "Flight and hotel booking assistance, travel planning and documentation."),
            ("🌍", "Relocation Support", "Pre-departure preparation, settlement information and long-term planning."),
            ("📚", "Language Courses", "Online English and Korean courses and study preparation resources."),
            ("📝", "Application Guidance", "Understand requirements, organize documents and prepare with confidence."),
        ],
        3,
    )

    section("DESTINATIONS", "Where would you like to go?",
            "We support applicants across popular study and travel destinations.")
    dests = [
        ("🇺🇸", "United States", "Universities, colleges and ESL pathways."),
        ("🇨🇦", "Canada", "Colleges, universities and study permit guidance."),
        ("🇦🇺", "Australia", "Study programs, student visa and travel preparation."),
        ("🇰🇷", "South Korea", "Korean language study and university pathways."),
        ("🌍", "Europe", "Travel documentation and Schengen visa information."),
    ]
    for col, (flag, name, text) in zip(st.columns(5, gap="small"), dests):
        with col:
            html(f'<div class="dest"><div class="flag">{flag}</div><h3>{name}</h3><p>{text}</p></div>')

    section("WHY HANNA EDU", "A clear, personal approach")
    w1, w2 = st.columns(2, gap="large")
    why = [
        ("1", "One team, every step", "Education, visa, travel and relocation support under one roof, so nothing falls through the cracks."),
        ("2", "Honest guidance", "We explain requirements and options clearly. We never promise outcomes that only authorities can decide."),
        ("3", "International reach", "Local support in Mongolia, with contact numbers in the USA and Canada."),
        ("4", "Prepared, not rushed", "We help you organize documents and plan timelines before you apply."),
    ]
    for i, (n, t, d) in enumerate(why):
        with (w1 if i % 2 == 0 else w2):
            html(f'<div class="why"><div class="num">{n}</div><div><h4>{t}</h4><p>{d}</p></div></div>')

    section("HOW IT WORKS", "From first question to your next chapter")
    for col, (n, t, d) in zip(
        st.columns(4, gap="medium"),
        [
            ("01", "Discover", "Tell us about your goals, destination and timeline."),
            ("02", "Plan", "We outline suitable options, requirements and next steps."),
            ("03", "Prepare", "Organize documents and complete applications with guidance."),
            ("04", "Move forward", "Get ready for travel, arrival and settling in."),
        ],
    ):
        with col:
            html(f'<div class="step"><div class="n">{n}</div><h3>{t}</h3><p>{d}</p></div>')

    section("FAQ", "Common questions")
    with st.expander("Do you guarantee visa approval?"):
        st.write("No. Visa decisions are made by the relevant government authorities. We help you understand requirements and prepare your application and documents.")
    with st.expander("Which destinations do you cover?"):
        st.write("The United States, Canada, Australia, South Korea and Europe. Contact us if you are considering another destination.")
    with st.expander("Can I take language courses online?"):
        st.write("Yes. We offer online English and Korean courses and study preparation resources.")
    with st.expander("How do I get started?"):
        st.write("Send us an inquiry through the Contact Us page and tell us about your plans. We will follow up with next steps.")

    cta_band("Ready to plan your next chapter?", "Tell us about your goals and we will help you understand your next steps.")

# =========================================================
# EDUCATION
# =========================================================

elif page == "Education":
    page_head("EDUCATION", "Build your global future.",
              "Explore international education opportunities and academic pathways with guidance from application to arrival.")

    cards(
        [
            ("🎓", "University Placement", "Explore international universities and academic programs that fit your goals."),
            ("📚", "ESL Programs", "English language programs to prepare for further study abroad."),
            ("🏫", "Undergraduate Programs", "Plan your international undergraduate education."),
            ("🧑‍🎓", "Graduate Programs", "Explore postgraduate and master's degree opportunities."),
            ("🗣️", "Language Courses", "Online English and Korean courses."),
            ("📝", "Application Guidance", "Understand requirements and prepare strong applications."),
        ],
        3,
    )

    section("GET STARTED", "Tell us what you are looking for")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        destination = st.selectbox("Preferred study destination", DESTINATIONS)
    with c2:
        level = st.selectbox("Education level", ["English Language Program", "Undergraduate", "Graduate / Master's", "Other"])
    st.button(
        "Continue to Contact Us",
        on_click=go_to_contact,
        args=(destination, ["Education"], f"I am interested in {level} in {destination}."),
    )

# =========================================================
# VISA CONSULTING
# =========================================================

elif page == "Visa Consulting":
    page_head("VISA CONSULTING", "Your visa journey starts here.",
              "Get guidance on documentation, application preparation and destination-specific requirements.")

    visa_options = {
        "United States": ["Visitor visa guidance", "Student visa guidance", "Document preparation", "Application guidance"],
        "Canada": ["Visitor visa guidance", "Study permit guidance", "Document preparation", "Application guidance"],
        "Australia": ["Visitor visa guidance", "Student visa guidance", "Document preparation", "Application guidance"],
        "South Korea": ["Visa information", "Study-related guidance", "Document preparation"],
        "Schengen / Europe": ["Tourist visa information", "Travel documentation", "Application preparation"],
        "Other": ["General visa consultation", "Document preparation"],
    }

    c1, c2 = st.columns(2, gap="large")
    with c1:
        destination = st.selectbox("Which country are you interested in?", list(visa_options.keys()))
    with c2:
        visa_type = st.selectbox(
            "What type of consultation do you need?",
            ["Visitor / Tourist Visa", "Student Visa", "Document Preparation", "Visa Category Change", "General Consultation", "Not Sure Yet"],
        )

    items = "".join(f"<li>✓ {i}</li>" for i in visa_options[destination])
    html(
        f"""<div class="card" style="min-height:0">
        <div class="eyebrow" style="color:#A9822F">{destination}</div>
        <h3 style="margin-top:8px">Consultation areas</h3>
        <ul class="checklist" style="list-style:none;padding:0;margin:12px 0 0">{items}</ul>
        <p style="margin-top:14px">Selected consultation: <b>{visa_type}</b></p></div>"""
    )

    html(
        """<div class="note"><b>Please note:</b> visa decisions are made by the relevant government
        authorities. Consultation does not guarantee visa approval.</div>"""
    )
    st.write("")
    st.button(
        "Request Visa Consultation",
        on_click=go_to_contact,
        args=(normalize_destination(destination), ["Visa Consulting"], f"I am interested in {visa_type} for {destination}."),
    )

# =========================================================
# TRAVEL & RELOCATION
# =========================================================

elif page == "Travel & Relocation":
    page_head("TRAVEL & RELOCATION", "Explore. Travel. Relocate.",
              "Prepare for international travel and get practical support for moving abroad.")

    cards(
        [
            ("✈️", "Flight Assistance", "Support with international flight planning and booking."),
            ("🏨", "Hotel Assistance", "Accommodation booking support for your trip."),
            ("🧳", "Travel Preparation", "Organize travel documents and your itinerary."),
            ("📦", "Moving Abroad", "Understand practical considerations before relocating."),
            ("🏡", "Settlement Guidance", "Information on adapting to life in a new country."),
            ("🗺️", "Destination Guidance", "Learn about destinations before you go."),
        ],
        3,
    )

    section("PLAN YOUR JOURNEY", "Tell us where you are headed")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        travel_destination = st.selectbox("Select your destination", DESTINATIONS)
    with c2:
        purpose = st.selectbox("Main purpose", ["Tourism", "Education", "Moving Abroad", "Visiting Family", "Other"])

    purpose_services = {
        "Tourism": ["Travel"],
        "Education": ["Education", "Travel"],
        "Moving Abroad": ["Relocation", "Travel"],
        "Visiting Family": ["Travel"],
        "Other": ["Travel"],
    }
    st.button(
        "Request Travel Consultation",
        on_click=go_to_contact,
        args=(travel_destination, purpose_services[purpose], f"I am interested in {purpose} in {travel_destination}."),
    )

# =========================================================
# CONTACT
# =========================================================

elif page == "Contact Us":
    page_head("CONTACT", "Let's plan your next chapter.",
              "Tell us about your goals and the services you are interested in. We will get back to you with next steps.")

    prefill_dest = st.session_state.get("prefill_destination", DESTINATIONS[0])
    dest_index = DESTINATIONS.index(prefill_dest) if prefill_dest in DESTINATIONS else 0
    prefill_services = [s for s in st.session_state.get("prefill_services", []) if s in CONTACT_SERVICES]

    left, right = st.columns([1.6, 1], gap="large")

    with left:
        with st.form("contact_form"):
            st.markdown("### Send an inquiry")
            name = st.text_input("Full name")
            email = st.text_input("Email address")
            phone = st.text_input("Phone number")
            destination = st.selectbox("Preferred destination", DESTINATIONS, index=dest_index)
            inquiry_services = st.multiselect("Services you are interested in", CONTACT_SERVICES, default=prefill_services)
            message = st.text_area(
                "Tell us about your plans",
                value=st.session_state.get("prefill_message", ""),
                placeholder="Tell us about your education, visa or travel plans...",
            )
            submitted = st.form_submit_button("Prepare My Inquiry", use_container_width=True)

        if submitted:
            if not name.strip() or not email.strip() or not inquiry_services:
                st.error("Please complete your name, email and select at least one service.")
            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("Please enter a valid email address.")
            else:
                subject = quote(f"Hanna Edu Inquiry - {name}")
                body = quote(
                    "\n".join(
                        [
                            f"Name: {name}",
                            f"Email: {email}",
                            f"Phone: {phone}",
                            f"Destination: {destination}",
                            f"Services: {', '.join(inquiry_services)}",
                            "",
                            f"Message: {message}",
                        ]
                    )
                )
                st.success("Your inquiry is ready. Open your email application to send it.")
                st.link_button(
                    "Open Email to Send Inquiry",
                    f"mailto:{CONTACT_EMAIL}?subject={subject}&body={body}",
                    use_container_width=True,
                )

    with right:
        for flag, country, number in [
            ("🇲🇳", "Mongolia", "99178308"),
            ("🇺🇸", "USA", "+1 (773) 209-9479"),
            ("🇨🇦", "Canada", "(780) 394-4377"),
        ]:
            html(f'<div class="contact-card"><div class="flag">{flag}</div><b>{country}</b><span>{number}</span></div>')
            st.write("")
        html(
            f"""<div class="contact-card"><div class="flag">✉️</div><b>Email</b>
            <span>{CONTACT_EMAIL}</span></div>"""
        )
        st.write("")
        st.markdown(f"[Visit the official Hanna Edu website]({WEBSITE})")

# =========================================================
# FOOTER
# =========================================================

html(
    f"""<div class="footer">
    <div class="footer-grid">
      <div>
        <div class="brand">HANNA <span>EDU</span></div>
        <p style="margin-top:12px;max-width:360px">Education, visa consulting, travel and relocation
        support for students and families planning their international journey.</p>
      </div>
      <div>
        <h4>Services</h4>
        <ul><li>Education Abroad</li><li>Visa Consulting</li><li>Travel Services</li>
        <li>Relocation Support</li><li>Language Courses</li></ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul><li>🇲🇳 Mongolia: 99178308</li><li>🇺🇸 USA: +1 (773) 209-9479</li>
        <li>🇨🇦 Canada: (780) 394-4377</li><li><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></li></ul>
      </div>
    </div>
    <div class="legal">© 2026 Hanna Edu. All rights reserved. Visa decisions are made by the relevant
    government authorities; consultation does not guarantee approval.</div>
    </div>"""
)
