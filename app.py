
import streamlit as st
from urllib.parse import quote
from datetime import date

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Hanna Edu | Global Education & Travel",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# BRAND COLORS & CUSTOM CSS
# =========================================================

NAVY = "#142238"
GOLD = "#D6B46A"
CREAM = "#F7F5F0"
DARK = "#202B3C"
MUTED = "#718096"

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

.stApp {
    background-color: #F7F5F0;
    color: #202B3C;
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #142238 !important;
}

.hero {
    background: linear-gradient(
        115deg,
        rgba(12, 27, 48, 0.97),
        rgba(28, 53, 77, 0.87)
    );
    padding: 65px 55px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
    border: 1px solid rgba(214,180,106,0.4);
}

.hero h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 49px !important;
    color: white !important;
    line-height: 1.2;
}

.hero p {
    color: #E2E7ED;
    font-size: 17px;
    line-height: 1.8;
    max-width: 700px;
}

.gold-text {
    color: #E4C77F;
}

.eyebrow {
    color: #D6B46A;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
}

.service-card {
    background: white;
    padding: 27px;
    border-radius: 14px;
    border: 1px solid #E8E4DA;
    min-height: 215px;
    box-shadow: 0 4px 15px rgba(20,34,56,0.04);
}

.service-card h3 {
    font-size: 22px;
    margin-bottom: 10px;
}

.service-card p {
    color: #718096;
    font-size: 14px;
    line-height: 1.7;
}

.service-icon {
    font-size: 31px;
    margin-bottom: 13px;
}

.country-card {
    background: #142238;
    color: white;
    border-radius: 12px;
    padding: 22px;
    text-align: center;
    border-bottom: 3px solid #D6B46A;
}

.country-card h3 {
    color: white !important;
    font-size: 19px;
}

.country-card p {
    color: #DCE2EA;
    font-size: 12px;
}

.section-label {
    color: #B18B42;
    font-size: 12px;
    letter-spacing: 2px;
    font-weight: 700;
}

.info-box {
    background: #EEEAE0;
    padding: 23px;
    border-radius: 12px;
    border-left: 4px solid #D6B46A;
}

.footer {
    background: #142238;
    padding: 35px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-top: 40px;
}

.footer p {
    color: #DCE2EA;
}

.stButton > button {
    background-color: #142238;
    color: white;
    border-radius: 8px;
    border: 1px solid #D6B46A;
    padding: 10px 22px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #D6B46A;
    color: #142238;
    border-color: #D6B46A;
}

div[data-testid="stSidebar"] {
    background-color: #142238;
}

div[data-testid="stSidebar"] * {
    color: white;
}

div[data-testid="stSidebar"] label {
    color: white !important;
}

hr {
    border-color: #E6E0D5;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# BRAND IMAGES FROM HANNA EDU WEBSITE
# =========================================================

HERO_IMAGE = (
    "https://static.wixstatic.com/media/"
    "d7ab6f_a08c7048efa0443bac8b5a85931f6e8e~mv2.png"
)

SECOND_IMAGE = (
    "https://static.wixstatic.com/media/"
    "d7ab6f_f3e2a5c60104491ba57c3c89e23f9b2d~mv2.png"
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown(
        "<h2 style='color:#E4C77F;'>HANNA EDU</h2>",
        unsafe_allow_html=True
    )

    st.caption("GLOBAL EDUCATION & CONSULTING")

    st.markdown("---")

    page = st.radio(
        "MAIN MENU",
        [
            "Home",
            "Education",
            "Visa Consulting",
            "Travel & Relocation",
            "Contact Us"
        ]
    )

    st.markdown("---")

    st.markdown("### Explore our services")

    selected_services = st.multiselect(
        "Choose your interests",
        [
            "Education",
            "Visa Consulting",
            "Travel",
            "Relocation",
            "Language Courses"
        ],
        default=[
            "Education",
            "Visa Consulting"
        ]
    )

    st.markdown("---")

    st.markdown("**Our destinations**")
    st.caption("🇺🇸 USA")
    st.caption("🇨🇦 Canada")
    st.caption("🇦🇺 Australia")
    st.caption("🇰🇷 South Korea")
    st.caption("🇪🇺 Europe")

    st.markdown("---")
    st.caption("Your journey starts with Hanna Edu.")


# =========================================================
# HEADER / BRANDING
# =========================================================

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(
        f"""
        <h2 style='margin-bottom:0;'>
            HANNA <span style='color:{GOLD};'>EDU.</span>
        </h2>
        <p style='color:{MUTED}; margin-top:0;'>
            Global Education · Visa · Travel · Relocation
        </p>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        "<p style='text-align:right;color:#B18B42;"
        "font-weight:600;'>MONGOLIA · GLOBAL SERVICES</p>",
        unsafe_allow_html=True
    )

st.divider()


# =========================================================
# REUSABLE SERVICE DATA
# =========================================================

services = {
    "Education": {
        "icon": "🎓",
        "title": "Education Abroad",
        "description": (
            "Explore international education opportunities, "
            "university applications, school placement, "
            "and academic pathways."
        ),
        "items": [
            "University and college placement",
            "ESL and language programs",
            "Undergraduate programs",
            "Graduate programs",
            "Application guidance",
            "Education pathway consultation"
        ]
    },

    "Visa Consulting": {
        "icon": "🛂",
        "title": "Visa Consulting",
        "description": (
            "Get guidance on visa documentation, "
            "application preparation, and understanding "
            "the requirements of your destination."
        ),
        "items": [
            "Visitor visa consultation",
            "Student visa guidance",
            "Document preparation",
            "Visa category change guidance",
            "Application review",
            "Country-specific visa information"
        ]
    },

    "Travel": {
        "icon": "✈️",
        "title": "Travel Services",
        "description": (
            "Plan your international journey with "
            "travel-related support and practical guidance."
        ),
        "items": [
            "Flight booking assistance",
            "Hotel booking assistance",
            "Travel planning",
            "Destination guidance",
            "Travel document preparation"
        ]
    },

    "Relocation": {
        "icon": "🌍",
        "title": "Relocation Support",
        "description": (
            "Prepare for your transition to a new country "
            "with practical information and settlement guidance."
        ),
        "items": [
            "Pre-departure guidance",
            "Moving abroad preparation",
            "Education and lifestyle orientation",
            "Practical settlement information",
            "Long-term planning"
        ]
    },

    "Language Courses": {
        "icon": "📚",
        "title": "Language Learning",
        "description": (
            "Build language skills through online "
            "English and Korean learning opportunities."
        ),
        "items": [
            "English language courses",
            "Korean language courses",
            "Learning resources",
            "Study preparation"
        ]
    }
}


# =========================================================
# HOME PAGE
# =========================================================

if page == "Home":

    # Hero image from original website
    try:
        st.image(HERO_IMAGE, use_container_width=True)
    except Exception:
        pass

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">YOUR FUTURE. YOUR WORLD.</div>

        <h1>
            Think Beyond Borders.<br>
            <span class="gold-text">We Help You Get There.</span>
        </h1>

        <p>
            From international education and visa consulting
            to travel planning and relocation support,
            Hanna Edu helps you navigate your next chapter abroad.
        </p>

        <p style="color:#E4C77F;font-size:14px;">
            EDUCATION &nbsp; | &nbsp; VISA &nbsp; |
            &nbsp; TRAVEL &nbsp; | &nbsp; RELOCATION
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Explore What We Do")

    st.caption(
        "Select one or multiple services from the menu "
        "to explore the areas that interest you."
    )

    if selected_services:

        cols = st.columns(2)

        for i, service in enumerate(selected_services):

            data = services[service]

            with cols[i % 2]:

                st.markdown(
                    f"""
                    <div class="service-card">
                        <div class="service-icon">{data['icon']}</div>
                        <h3>{data['title']}</h3>
                        <p>{data['description']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                with st.expander(f"Explore {service}"):

                    for item in data["items"]:
                        st.markdown(f"✓ {item}")

    else:
        st.info("Choose a service from the sidebar to get started.")

    st.markdown("---")

    st.markdown("### Your Destination. Our Expertise.")

    country_cols = st.columns(5)

    countries = [
        ("🇺🇸", "USA", "Education & Visa"),
        ("🇨🇦", "Canada", "Education & Visa"),
        ("🇦🇺", "Australia", "Study & Travel"),
        ("🇰🇷", "South Korea", "Study & Language"),
        ("🇪🇺", "Europe", "Travel & Education")
    ]

    for col, country in zip(country_cols, countries):

        with col:
            st.markdown(
                f"""
                <div class="country-card">
                    <div style="font-size:30px;">{country[0]}</div>
                    <h3>{country[1]}</h3>
                    <p>{country[2]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    st.markdown("### How We Can Help")

    steps = st.columns(3)

    with steps[0]:
        st.markdown("#### 01. Discover")
        st.write(
            "Tell us your goals, preferred destination, "
            "and the services you need."
        )

    with steps[1]:
        st.markdown("#### 02. Prepare")
        st.write(
            "Explore your options and receive guidance "
            "on the relevant application process."
        )

    with steps[2]:
        st.markdown("#### 03. Move Forward")
        st.write(
            "Prepare for your international journey "
            "with practical support."
        )

    st.markdown("---")

    st.markdown(
        """
        <div class="info-box">
            <h3>Every journey begins with a plan.</h3>
            <p>
                Whether you want to study overseas, explore
                visa options, travel internationally, or
                prepare for a new life abroad, Hanna Edu
                is here to help you understand your next steps.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# EDUCATION PAGE
# =========================================================

elif page == "Education":

    st.markdown(
        '<div class="section-label">01 — EDUCATION</div>',
        unsafe_allow_html=True
    )

    st.title("Your Education. Your Global Future.")

    st.write(
        "Discover international academic opportunities "
        "and explore education pathways around the world."
    )

    try:
        st.image(SECOND_IMAGE, use_container_width=True)
    except Exception:
        pass

    st.markdown("### Education Services")

    education_programs = [
        ("🎓", "ESL Programs",
         "Improve your English language skills abroad."),
        ("🏫", "Undergraduate",
         "Explore international bachelor's degree programs."),
        ("📚", "Graduate Programs",
         "Plan your master's or postgraduate education."),
        ("🌏", "School Placement",
         "Explore suitable international educational institutions.")
    ]

    cols = st.columns(2)

    for i, (icon, title, description) in enumerate(education_programs):

        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="service-card">
                    <div class="service-icon">{icon}</div>
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    st.markdown("### Education Partners")

    st.write(
        "Hanna Edu's website lists international educational "
        "institutions including:"
    )

    st.markdown("""
    - Mentora College — USA
    - University of Hawaiʻi — USA
    - Midwestern Career College — USA
    - Durham College — Canada
    - Academia Language School — USA
    - Canada Christian College — Canada
    """)

    st.caption(
        "Program availability, partnerships, and admission "
        "requirements should be confirmed before applying."
    )


# =========================================================
# VISA CONSULTING PAGE
# =========================================================

elif page == "Visa Consulting":

    st.markdown(
        '<div class="section-label">02 — VISA CONSULTING</div>',
        unsafe_allow_html=True
    )

    st.title("Your Visa Journey Starts Here.")

    st.write(
        "Understand your visa options and prepare "
        "your application documents with professional guidance."
    )

    st.markdown("### Select Your Destination")

    destination = st.selectbox(
        "Which country are you interested in?",
        [
            "United States",
            "Canada",
            "Australia",
            "South Korea",
            "Schengen / Europe",
            "Other"
        ]
    )

    visa_type = st.selectbox(
        "What type of visa or consultation do you need?",
        [
            "Visitor / Tourist Visa",
            "Student Visa",
            "Document Preparation",
            "Visa Category Change",
            "General Consultation",
            "Not Sure Yet"
        ]
    )

    visa_services = {
        "United States": [
            "Visitor visa guidance",
            "Student visa guidance",
            "Application documentation",
            "Interview preparation"
        ],
        "Canada": [
            "Visitor visa guidance",
            "Study permit guidance",
            "Document preparation",
            "Application review"
        ],
        "Australia": [
            "Visitor visa guidance",
            "Student visa guidance",
            "Visa category change guidance",
            "Application documentation"
        ],
        "South Korea": [
            "Visitor visa guidance",
            "Study-related visa guidance",
            "Document preparation"
        ],
        "Schengen / Europe": [
            "Tourist visa guidance",
            "Travel documentation",
            "Application preparation"
        ],
        "Other": [
            "General visa consultation",
            "Document preparation"
        ]
    }

    st.markdown("### Available Consultation Areas")

    for item in visa_services[destination]:
        st.markdown(f"✓ {item}")

    st.markdown("---")

    st.markdown(
        f"""
        <div class="info-box">
            <h3>{destination} Consultation</h3>
            <p>
                Selected service: {visa_type}<br>
                Our consultation can help you understand
                relevant requirements and documentation.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Visa decisions are made by the relevant government "
        "authorities. Consultation does not guarantee approval."
    )


# =========================================================
# TRAVEL & RELOCATION PAGE
# =========================================================

elif page == "Travel & Relocation":

    st.markdown(
        '<div class="section-label">03 — TRAVEL & RELOCATION</div>',
        unsafe_allow_html=True
    )

    st.title("Go Further. Feel Prepared.")

    st.write(
        "Planning an international trip or preparing "
        "to relocate? Explore practical travel services "
        "and moving-abroad support."
    )

    travel_options = [
        ("✈️", "Flight Assistance",
         "Get assistance with international flight planning."),
        ("🏨", "Hotel Assistance",
         "Explore accommodation booking support."),
        ("🧳", "Travel Preparation",
         "Prepare your travel documents and itinerary."),
        ("🌍", "Moving Abroad",
         "Understand practical steps before relocating."),
        ("🏡", "Settlement Guidance",
         "Explore information about adapting to a new country."),
        ("🗺️", "Destination Guidance",
         "Learn about destinations and international travel.")
    ]

    cols = st.columns(3)

    for i, (icon, title, description) in enumerate(travel_options):

        with cols[i % 3]:

            st.markdown(
                f"""
                <div class="service-card">
                    <div class="service-icon">{icon}</div>
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    st.markdown("### Where Are You Planning to Go?")

    travel_destination = st.selectbox(
        "Select your destination",
        [
            "United States",
            "Canada",
            "Australia",
            "South Korea",
            "Europe",
            "Other"
        ],
        key="travel_destination"
    )

    travel_goal = st.radio(
        "What is your main purpose?",
        [
            "Tourism",
            "Education",
            "Moving Abroad",
            "Visiting Family",
            "Other"
        ],
        horizontal=True
    )

    st.info(
        f"Destination: {travel_destination} | "
        f"Purpose: {travel_goal}"
    )


# =========================================================
# CONTACT PAGE
# =========================================================

elif page == "Contact Us":

    st.markdown(
        '<div class="section-label">04 — CONTACT</div>',
        unsafe_allow_html=True
    )

    st.title("Let's Plan Your Next Chapter.")

    st.write(
        "Tell us about your goals and the services "
        "you are interested in."
    )

    with st.form("contact_form"):

        name = st.text_input("Full Name")

        email = st.text_input("Email Address")

        phone = st.text_input("Phone Number")

        country = st.selectbox(
            "Preferred Destination",
            [
                "United States",
                "Canada",
                "Australia",
                "South Korea",
                "Europe",
                "Other"
            ]
        )

        inquiry_services = st.multiselect(
            "Services You Are Interested In",
            [
                "Education",
                "Visa Consulting",
                "Travel",
                "Relocation",
                "Language Courses"
            ]
        )

        message = st.text_area(
            "Tell Us About Your Plans",
            placeholder=(
                "I am interested in studying abroad..."
            )
        )

        submitted = st.form_submit_button(
            "Submit Inquiry",
            use_container_width=True
        )

        if submitted:

            if not name or not email or not inquiry_services:
                st.error(
                    "Please enter your name, email, "
                    "and at least one service."
                )

            else:

                subject = quote(
                    f"Hanna Edu Inquiry - {name}"
                )

                body = quote(
                    f"""
Name: {name}
Email: {email}
Phone: {phone}
Destination: {country}
Services: {', '.join(inquiry_services)}
Message: {message}
                    """
                )

                mailto = (
                    f"mailto:mongolianhannaedu@gmail.com"
                    f"?subject={subject}&body={body}"
                )

                st.success(
                    "Your inquiry is ready. "
                    "Open your email application to send it."
                )

                st.link_button(
                    "Open Email to Send Inquiry",
                    mailto,
                    use_container_width=True
                )

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

    st.markdown(
        "📧 mongolianhannaedu@gmail.com"
    )

    st.markdown(
        "🌐 [Official Hanna Edu Website](https://www.hanna-edu.com/)"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown("""
<div class="footer">

    <h2 style="color:#E4C77F;">
        HANNA EDU
    </h2>

    <p>
        GLOBAL EDUCATION · VISA · TRAVEL · RELOCATION
    </p>

    <p>
        Helping You Navigate Your Future Beyond Borders.
    </p>

    <p style="font-size:12px;">
        © 2026 Hanna Edu. All Rights Reserved.
    </p>

</div>
""", unsafe_allow_html=True)
