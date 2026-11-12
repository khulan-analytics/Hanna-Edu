import streamlit as st
from urllib.parse import quote


def flatten(html: str) -> str:
    """Strip indentation/blank lines so Markdown never treats HTML as a code block."""
    return " ".join(line.strip() for line in html.splitlines() if line.strip())

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Hanna Edu | Global Consultancy",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CONSTANTS
# =========================================================

HERO_IMAGE = "https://static.wixstatic.com/media/d7ab6f_a08c7048efa0443bac8b5a85931f6e8e~mv2.png"
SECOND_IMAGE = "https://static.wixstatic.com/media/d7ab6f_f3e2a5c60104491ba57c3c89e23f9b2d~mv2.png"
CONTACT_IMAGE = "https://static.wixstatic.com/media/d7ab6f_37d9c1f1c2b94aeaa0c51e7a847f7b03~mv2.png"

DESTINATIONS = ["United States", "Canada", "Australia", "South Korea", "Europe", "Other"]
CONTACT_SERVICES = ["Education", "Visa Consulting", "Travel", "Relocation", "Language Courses"]
PAGES = ["Home", "Education", "Visa Consulting", "Travel & Relocation", "Contact Us"]

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(flatten("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

.stApp { background-color: #F7F5F0; font-family: 'DM Sans', sans-serif; }
.block-container { max-width: 1250px; padding-top: 2rem; padding-bottom: 3rem; }

h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #142238 !important; }

.section-label { color: #B18B42; font-size: 12px; font-weight: 700; letter-spacing: 2px; }
.brand-name { font-family: 'Playfair Display', serif; color: #142238; font-size: 29px; font-weight: 700; }

.service-card {
    background: white; padding: 27px; border-radius: 14px; border: 1px solid #E8E4DA;
    min-height: 205px; box-shadow: 0 4px 15px rgba(20,34,56,0.04); margin-bottom: 15px;
}
.service-card h3 { font-size: 22px; margin-bottom: 10px; }
.service-card p { color: #718096; font-size: 14px; line-height: 1.8; }
.service-icon { font-size: 32px; margin-bottom: 12px; }

.country-card {
    background: #142238; color: white; padding: 22px 10px; text-align: center;
    border-radius: 12px; border-bottom: 3px solid #D6B46A; min-height: 135px;
}
.country-card h3 { color: white !important; font-size: 18px; }
.country-card p { color: #DCE2EA; font-size: 12px; }

.info-box { background: #EEEAE0; padding: 25px; border-radius: 12px; border-left: 4px solid #D6B46A; }
.info-box p { color: #526174; line-height: 1.8; }

/* Sidebar: dark background, light text only for labels/text/headings
   (so input widgets stay readable) */
div[data-testid="stSidebar"] { background-color: #142238; }
div[data-testid="stSidebar"] label,
div[data-testid="stSidebar"] label p,
div[data-testid="stSidebar"] .stMarkdown p,
div[data-testid="stSidebar"] .stMarkdown li,
div[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: #FFFFFF !important; }
div[data-testid="stSidebar"] h1,
div[data-testid="stSidebar"] h2,
div[data-testid="stSidebar"] h3 { color: #E4C77F !important; }

.stButton > button,
[data-testid="stLinkButton"] a,
[data-testid="stFormSubmitButton"] button {
    background-color: #142238; color: white !important;
    border: 1px solid #D6B46A; border-radius: 8px; font-weight: 600;
}
.stButton > button p,
[data-testid="stLinkButton"] a p,
[data-testid="stFormSubmitButton"] button p { color: inherit !important; }
.stButton > button:hover,
[data-testid="stLinkButton"] a:hover,
[data-testid="stFormSubmitButton"] button:hover {
    background-color: #D6B46A; color: #142238 !important;
}

div[data-testid="stImage"] img { border-radius: 12px; }
hr { border-color: #E6E0D5; }
</style>
"""), unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================


def show_image(url):
    """Full-width image that works on old and new Streamlit versions."""
    try:
        st.image(url, width="stretch")
    except TypeError:
        st.image(url, use_container_width=True)


def card_html(icon, title, description):
    return flatten(f"""
    <div class="service-card">
        <div class="service-icon">{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
    </div>
    """)


def render_cards(items, n_cols):
    cols = st.columns(n_cols)
    for i, (icon, title, description) in enumerate(items):
        with cols[i % n_cols]:
            st.markdown(card_html(icon, title, description), unsafe_allow_html=True)


def go_to_contact(destination, services, message):
    """Button callback: prefill the contact form and switch page.
    Runs before the next rerun, so changing the radio's key is allowed."""
    st.session_state["prefill_destination"] = destination
    st.session_state["prefill_services"] = services
    st.session_state["prefill_message"] = message
    st.session_state["page"] = "Contact Us"


def normalize_destination(dest):
    if dest == "Schengen / Europe":
        return "Europe"
    return dest if dest in DESTINATIONS else "Other"


# =========================================================
# SERVICE INFORMATION
# =========================================================

services = {
    "Education": {
        "icon": "🎓",
        "title": "Education Abroad",
        "description": "Explore international education opportunities, school placement and academic pathways.",
        "items": [
            "School and university placement",
            "ESL programs",
            "Undergraduate programs",
            "Graduate programs",
            "Education consultation",
            "Application guidance",
        ],
    },
    "Visa": {
        "icon": "🛂",
        "title": "Visa Consulting",
        "description": "Get guidance with visa applications, documentation and application preparation.",
        "items": [
            "Visitor visa consultation",
            "Student visa guidance",
            "Visa documentation",
            "Visa category change guidance",
            "Application preparation",
        ],
    },
    "Travel": {
        "icon": "✈️",
        "title": "Travel Services",
        "description": "Prepare for international travel with practical travel-related assistance.",
        "items": [
            "Flight booking assistance",
            "Hotel booking assistance",
            "Travel planning",
            "Travel documentation",
            "Destination information",
        ],
    },
    "Relocation": {
        "icon": "🌍",
        "title": "Relocation Support",
        "description": "Prepare for moving abroad and understand practical settlement considerations.",
        "items": [
            "Pre-departure guidance",
            "Moving abroad preparation",
            "Settlement information",
            "International lifestyle orientation",
            "Long-term planning",
        ],
    },
    "Language": {
        "icon": "📚",
        "title": "Language Courses",
        "description": "Explore English and Korean online learning opportunities.",
        "items": [
            "English online courses",
            "Korean online courses",
            "Language learning resources",
            "Study preparation",
        ],
    },
}

# =========================================================
# SIDEBAR
# =========================================================

st.session_state.setdefault("page", "Home")

with st.sidebar:
    st.markdown(flatten("""
        <h2 style="color:#E4C77F;">HANNA EDU</h2>
        <p style="font-size:11px;letter-spacing:2px;color:white;">GLOBAL CONSULTANCY</p>
        """), unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio("MAIN MENU", PAGES, key="page")

    st.markdown("---")
    st.markdown("### Explore Services")

    selected_services = st.multiselect(
        "Select one or more interests",
        list(services.keys()),
        default=["Education", "Visa"],
    )

    st.markdown("---")
    st.markdown("### Destinations")
    st.markdown(
        """
🇺🇸 United States

🇨🇦 Canada

🇦🇺 Australia

🇰🇷 South Korea

🌍 Europe
"""
    )
    st.markdown("---")
    st.caption("Your journey starts here.")

# =========================================================
# HEADER
# =========================================================

header1, header2 = st.columns([3, 1])

with header1:
    st.markdown(flatten("""
        <div class="brand-name">HANNA <span style="color:#D6B46A;">EDU.</span></div>
        <p style="color:#718096;font-size:13px;">Education · Visa · Travel · Relocation</p>
        """), unsafe_allow_html=True)

with header2:
    st.markdown(flatten("""
        <p style="text-align:right;color:#B18B42;font-size:12px;font-weight:700;">
            MONGOLIA | INTERNATIONAL SERVICES
        </p>
        """), unsafe_allow_html=True)

st.divider()


def show_service_card(service_name):
    data = services[service_name]
    st.markdown(card_html(data["icon"], data["title"], data["description"]), unsafe_allow_html=True)
    with st.expander(f"Explore {data['title']}"):
        for item in data["items"]:
            st.markdown(f"✓ {item}")


# =========================================================
# HOME PAGE
# =========================================================

if page == "Home":
    show_image(HERO_IMAGE)
    st.markdown("")

    st.markdown('<div class="section-label">OUR SERVICES</div>', unsafe_allow_html=True)
    st.title("Explore Your Opportunities")
    st.write("Discover international education, visa consulting, travel and relocation services.")

    if selected_services:
        cols = st.columns(2)
        for i, service in enumerate(selected_services):
            with cols[i % 2]:
                show_service_card(service)
    else:
        st.info("Select your interests from the sidebar to explore our services.")

    st.markdown("---")
    st.markdown('<div class="section-label">GLOBAL DESTINATIONS</div>', unsafe_allow_html=True)
    st.title("Where Would You Like to Go?")

    country_data = [
        ("🇺🇸", "USA", "Education & Visa"),
        ("🇨🇦", "Canada", "Education & Visa"),
        ("🇦🇺", "Australia", "Study & Travel"),
        ("🇰🇷", "South Korea", "Study & Language"),
        ("🌍", "Europe", "Travel & Education"),
    ]

    for col, (flag, name, desc) in zip(st.columns(5), country_data):
        with col:
            st.markdown(flatten(f"""
                <div class="country-card">
                    <div style="font-size:30px;">{flag}</div>
                    <h3>{name}</h3>
                    <p>{desc}</p>
                </div>
                """), unsafe_allow_html=True)

    st.markdown("---")
    show_image(SECOND_IMAGE)
    st.markdown("---")

    st.markdown('<div class="section-label">HOW WE HELP</div>', unsafe_allow_html=True)
    st.title("From Planning to Your Next Chapter")

    steps = st.columns(3)
    step_data = [
        ("01. Discover", "Tell us about your international education, visa or travel goals."),
        ("02. Prepare", "Explore available options and prepare the relevant documents."),
        ("03. Move Forward", "Get ready for your international journey and next opportunities."),
    ]
    for col, (title, text) in zip(steps, step_data):
        with col:
            st.markdown(f"### {title}")
            st.write(text)

    st.markdown("---")
    st.markdown(flatten("""
        <div class="info-box">
            <h3>One Destination. New Possibilities.</h3>
            <p>
                Whether you are planning to study abroad, apply for a visa,
                travel internationally, or prepare for a new life overseas,
                Hanna Edu helps you understand your next steps.
            </p>
        </div>
        """), unsafe_allow_html=True)

# =========================================================
# EDUCATION PAGE
# =========================================================

elif page == "Education":
    st.markdown('<div class="section-label">01 — EDUCATION</div>', unsafe_allow_html=True)
    st.title("Build Your Global Future.")
    st.write("Explore international education opportunities and academic pathways.")
    show_image(SECOND_IMAGE)

    st.markdown("### Our Education Services")
    render_cards(
        [
            ("🎓", "University Placement", "Explore international universities and academic programs."),
            ("📚", "ESL Programs", "Explore English language learning opportunities."),
            ("🏫", "Undergraduate Programs", "Plan your international undergraduate education."),
            ("🌍", "Graduate Programs", "Explore postgraduate and master's degree opportunities."),
            ("🗣️", "Language Courses", "Explore online English and Korean courses."),
            ("📝", "Application Guidance", "Understand application requirements and preparation."),
        ],
        2,
    )

    st.markdown("---")
    st.markdown("### Start Your Education Journey")

    destination = st.selectbox("Preferred study destination", DESTINATIONS)
    education_level = st.selectbox(
        "Education level",
        ["English Language Program", "Undergraduate", "Graduate / Master's", "Other"],
    )

    st.button(
        "Continue to Contact Us",
        on_click=go_to_contact,
        args=(
            destination,
            ["Education"],
            f"I am interested in {education_level} in {destination}.",
        ),
    )

# =========================================================
# VISA CONSULTING PAGE
# =========================================================

elif page == "Visa Consulting":
    st.markdown('<div class="section-label">02 — VISA CONSULTING</div>', unsafe_allow_html=True)
    st.title("Your Visa Journey Starts Here.")
    st.write(
        "Get guidance on visa documentation, application preparation "
        "and understanding destination-specific requirements."
    )

    st.markdown("### Select Your Destination")

    destination = st.selectbox(
        "Which country are you interested in?",
        ["United States", "Canada", "Australia", "South Korea", "Schengen / Europe", "Other"],
    )
    visa_type = st.selectbox(
        "What type of consultation do you need?",
        [
            "Visitor / Tourist Visa",
            "Student Visa",
            "Document Preparation",
            "Visa Category Change",
            "General Consultation",
            "Not Sure Yet",
        ],
    )

    visa_options = {
        "United States": ["Visitor visa guidance", "Student visa guidance", "Document preparation", "Application guidance"],
        "Canada": ["Visitor visa guidance", "Study permit guidance", "Document preparation", "Application guidance"],
        "Australia": ["Visitor visa guidance", "Student visa guidance", "Document preparation", "Application guidance"],
        "South Korea": ["Visa information", "Study-related guidance", "Document preparation"],
        "Schengen / Europe": ["Tourist visa information", "Travel documentation", "Application preparation"],
        "Other": ["General visa consultation", "Document preparation"],
    }

    st.markdown("### Consultation Areas")
    for item in visa_options[destination]:
        st.markdown(f"✓ {item}")

    st.markdown("---")
    st.markdown(flatten(f"""
        <div class="info-box">
            <h3>{destination} Consultation</h3>
            <p>Selected consultation: {visa_type}</p>
            <p>
                Understand the relevant application requirements and
                documentation before taking your next step.
            </p>
        </div>
        """), unsafe_allow_html=True)

    st.caption(
        "Visa decisions are made by the relevant government authorities. "
        "Consultation does not guarantee visa approval."
    )

    st.button(
        "Request Visa Consultation",
        on_click=go_to_contact,
        args=(
            normalize_destination(destination),
            ["Visa Consulting"],
            f"I am interested in {visa_type} for {destination}.",
        ),
    )

# =========================================================
# TRAVEL & RELOCATION PAGE
# =========================================================

elif page == "Travel & Relocation":
    st.markdown('<div class="section-label">03 — TRAVEL & RELOCATION</div>', unsafe_allow_html=True)
    st.title("Explore. Travel. Relocate.")
    st.write("Prepare for international travel and explore practical support for moving abroad.")
    show_image(CONTACT_IMAGE)

    render_cards(
        [
            ("✈️", "Flight Assistance", "Get assistance with international flight planning."),
            ("🏨", "Hotel Assistance", "Explore accommodation booking support."),
            ("🧳", "Travel Preparation", "Prepare your travel documents and itinerary."),
            ("🌍", "Moving Abroad", "Understand practical considerations before relocating."),
            ("🏡", "Settlement Guidance", "Explore information about adapting to a new country."),
            ("🗺️", "Destination Guidance", "Learn about international destinations and travel."),
        ],
        3,
    )

    st.markdown("---")
    st.markdown("### Plan Your Journey")

    travel_destination = st.selectbox("Select your destination", DESTINATIONS)
    travel_purpose = st.radio(
        "What is your main purpose?",
        ["Tourism", "Education", "Moving Abroad", "Visiting Family", "Other"],
        horizontal=True,
    )

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
        args=(
            travel_destination,
            purpose_services[travel_purpose],
            f"I am interested in {travel_purpose} in {travel_destination}.",
        ),
    )

# =========================================================
# CONTACT PAGE
# =========================================================

elif page == "Contact Us":
    st.markdown('<div class="section-label">04 — CONTACT</div>', unsafe_allow_html=True)
    st.title("Let's Plan Your Next Chapter.")
    st.write("Tell us about your goals and the services you are interested in.")
    show_image(CONTACT_IMAGE)

    st.markdown("### Send an Inquiry")

    prefill_dest = st.session_state.get("prefill_destination", DESTINATIONS[0])
    dest_index = DESTINATIONS.index(prefill_dest) if prefill_dest in DESTINATIONS else 0
    prefill_services = [
        s for s in st.session_state.get("prefill_services", []) if s in CONTACT_SERVICES
    ]

    with st.form("contact_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        destination = st.selectbox("Preferred Destination", DESTINATIONS, index=dest_index)
        inquiry_services = st.multiselect(
            "Services You Are Interested In",
            CONTACT_SERVICES,
            default=prefill_services,
        )
        message = st.text_area(
            "Tell Us About Your Plans",
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
            mailto = f"mailto:mongolianhannaedu@gmail.com?subject={subject}&body={body}"

            st.success("Your inquiry is ready. Open your email application to send it.")
            st.link_button("Open Email to Send Inquiry", mailto, use_container_width=True)

    st.markdown("---")
    st.markdown("### Contact Information")

    contact_cols = st.columns(3)
    with contact_cols[0]:
        st.markdown("#### 🇲🇳 Mongolia")
        st.write("99178308")
    with contact_cols[1]:
        st.markdown("#### 🇺🇸 USA")
        st.write("+1 (773) 209-9479")
    with contact_cols[2]:
        st.markdown("#### 🇨🇦 Canada")
        st.write("(780) 394-4377")

    st.markdown("**Email:** mongolianhannaedu@gmail.com")
    st.markdown("[Visit Official Hanna Edu Website](https://www.hanna-edu.com/)")

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

if page != "Contact Us":
    show_image(CONTACT_IMAGE)

st.markdown(flatten("""
    <p style="text-align:center;color:#718096;font-size:12px;padding:15px;">
        © 2026 Hanna Edu. All Rights Reserved.
    </p>
    """), unsafe_allow_html=True)
