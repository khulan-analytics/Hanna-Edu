import base64
import hashlib
import io
import re
from pathlib import Path
from urllib.parse import quote

import streamlit as st

st.set_page_config(
    page_title="Hanna Edu",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
LANGUAGES = ["English", "Монгол", "한국어"]          # position = tuple index in TEXT
CONTACT_EMAIL = "mongolianhannaedu@gmail.com"
WEBSITE = "https://www.hanna-edu.com/"

# Translation format: English / Mongolian / Korean
TEXT = {
    "home": ("Home", "Нүүр", "홈"),
    "education": ("Education", "Боловсрол", "교육"),
    "visa": ("Visa Consulting", "Визний зөвлөгөө", "비자 상담"),
    "travel": ("Travel & Relocation", "Аялал ба суурьшил", "여행 및 이주"),
    "contact": ("Contact Us", "Холбоо барих", "문의하기"),
    "language": ("Language", "Хэл", "언어"),

    "hero_label": ("EDUCATION · VISA · TRAVEL · RELOCATION",
                   "БОЛОВСРОЛ · ВИЗ · АЯЛАЛ · СУУРЬШИЛ",
                   "교육 · 비자 · 여행 · 해외 정착"),
    "hero_title": ("Your trusted partner for studying and living abroad.",
                   "Гадаадад суралцах, амьдрахад таны итгэлтэй түнш.",
                   "해외 유학과 생활을 위한 믿을 수 있는 파트너."),
    "hero_desc": ("We guide students and families through school placement, visa preparation, travel planning and relocation.",
                  "Бид оюутан, гэр бүлүүдэд сургууль сонгох, виз мэдүүлэх, аялал төлөвлөх болон гадаадад суурьшихад тусална.",
                  "학생과 가족의 학교 선택, 비자 준비, 여행 계획 및 해외 정착을 도와드립니다."),
    "start": ("Start Your Inquiry", "Хүсэлт илгээх", "문의 시작하기"),
    "consult": ("Request a Consultation", "Зөвлөгөө авах", "상담 신청"),

    "what_we_do": ("WHAT WE DO", "БИДНИЙ ҮЙЛЧИЛГЭЭ", "서비스 소개"),
    "services_title": ("Services built around your journey",
                       "Таны зорилгод нийцсэн үйлчилгээ",
                       "여정을 함께하는 서비스"),
    "services_desc": ("From your first question to your arrival abroad, we are here to help.",
                      "Анхны асуултаас эхлээд гадаадад очих хүртэл бид танд тусална.",
                      "첫 문의부터 해외 도착까지 필요한 서비스를 제공합니다."),

    "education_service": ("Education Abroad", "Гадаадад суралцах", "해외 유학"),
    "education_desc": ("School and university placement, ESL, undergraduate and graduate programs.",
                       "Сургууль, их сургууль, англи хэлний бэлтгэл, бакалавр болон магистрын хөтөлбөр.",
                       "학교 및 대학교 진학, ESL, 학부 및 대학원 과정 안내."),
    "visa_service": ("Visa Consulting", "Визний зөвлөгөө", "비자 상담"),
    "visa_desc": ("Visitor and student visa guidance, document preparation and application support.",
                  "Зочлох болон оюутны визний зөвлөгөө, бичиг баримт бүрдүүлэлт.",
                  "방문 비자 및 학생 비자 안내와 서류 준비 지원."),
    "travel_service": ("Travel Services", "Аяллын үйлчилгээ", "여행 서비스"),
    "travel_desc": ("Flight and hotel assistance, travel planning and documentation.",
                    "Нислэг, зочид буудал, аяллын төлөвлөлт болон бичиг баримтын туслалцаа.",
                    "항공편, 호텔, 여행 계획 및 서류 준비 지원."),
    "relocation_service": ("Relocation Support", "Гадаадад суурьшихад туслах", "해외 정착 지원"),
    "relocation_desc": ("Pre-departure preparation and information for settling abroad.",
                        "Явахаас өмнөх бэлтгэл болон гадаадад суурьших мэдээлэл.",
                        "출국 전 준비와 해외 정착 정보를 제공합니다."),
    "language_service": ("Language Courses", "Хэлний сургалт", "어학 과정"),
    "language_desc": ("Online English and Korean courses.",
                      "Англи, солонгос хэлний онлайн сургалт.",
                      "온라인 영어 및 한국어 과정."),

    "partners": ("OUR PARTNER SCHOOLS", "ХАМТРАН АЖИЛЛАДАГ СУРГУУЛИУД", "협력 교육기관"),
    "partners_title": ("Our partner institutions", "Манай хамтрагч сургуулиуд", "협력 교육기관 소개"),
    "partners_desc": ("Explore universities, colleges and language schools in the United States and Canada.",
                      "АНУ болон Канадын их сургууль, коллеж, хэлний сургуулиудтай танилцаарай.",
                      "미국과 캐나다의 대학교, 컬리지 및 어학원을 살펴보세요."),

    "destinations": ("DESTINATIONS", "ЧИГЛЭЛҮҮД", "주요 목적지"),
    "destinations_title": ("Where would you like to go?",
                           "Та аль улс руу явахыг хүсэж байна вэ?",
                           "어느 나라로 가고 싶으신가요?"),

    "why": ("WHY HANNA EDU", "ЯАГААД HANNA EDU ВЭ?", "HANNA EDU를 선택하는 이유"),
    "why_title": ("A clear, personal approach",
                  "Танд зориулсан ойлгомжтой зөвлөгөө",
                  "명확하고 세심한 맞춤형 안내"),
    "why1": ("One team, every step", "Нэг баг, бүх үе шатанд", "모든 단계를 함께하는 한 팀"),
    "why1_desc": ("Education, visa, travel and relocation support in one place.",
                  "Боловсрол, виз, аялал болон суурьшлын үйлчилгээг нэг дороос.",
                  "교육, 비자, 여행 및 해외 정착 지원을 한곳에서 제공합니다."),
    "why2": ("Honest guidance", "Шударга зөвлөгөө", "정직한 안내"),
    "why2_desc": ("We explain requirements clearly and never guarantee government decisions.",
                  "Шаардлагыг тодорхой тайлбарлаж, төрийн байгууллагын шийдвэрийг баталгаажуулахгүй.",
                  "요건을 명확하게 설명하며 정부 기관의 결정을 보장하지 않습니다."),
    "why3": ("International support", "Олон улсын дэмжлэг", "국제적인 지원"),
    "why3_desc": ("Support for students and families planning an international journey.",
                  "Олон улсад суралцах, аялах, амьдрахаар төлөвлөж буй хүмүүст тусална.",
                  "해외 유학과 여행을 계획하는 학생과 가족을 지원합니다."),

    "how": ("HOW IT WORKS", "ҮЙЛЧИЛГЭЭНИЙ ҮЕ ШАТ", "진행 절차"),
    "step1": ("Discover", "Зорилгоо тодорхойлох", "목표 확인"),
    "step1_desc": ("Tell us about your goals and destination.",
                   "Зорилго болон очих улсынхаа талаар бидэнд хэлээрэй.",
                   "목표와 목적지를 알려주세요."),
    "step2": ("Plan", "Төлөвлөх", "계획 수립"),
    "step2_desc": ("We outline suitable options and next steps.",
                   "Бид тохирох боломж болон дараагийн алхмуудыг танилцуулна.",
                   "적합한 선택지와 다음 단계를 안내합니다."),
    "step3": ("Prepare", "Бэлтгэх", "준비"),
    "step3_desc": ("Organize documents and prepare applications.",
                   "Бичиг баримтаа бүрдүүлж, өргөдлөө бэлтгэнэ.",
                   "서류를 정리하고 신청서를 준비합니다."),
    "step4": ("Move Forward", "Дараагийн алхам", "새로운 시작"),
    "step4_desc": ("Prepare for travel and settling in.",
                   "Аялал болон шинэ орчинд суурьшихад бэлтгэнэ.",
                   "여행과 현지 정착을 준비합니다."),

    "faq": ("FREQUENTLY ASKED QUESTIONS", "ТҮГЭЭМЭЛ АСУУЛТ", "자주 묻는 질문"),
    "faq_title": ("Common Questions", "Түгээмэл асуултууд", "자주 묻는 질문"),
    "faq_q1": ("Do you guarantee visa approval?",
               "Та виз гарах баталгаа өгдөг үү?",
               "비자 승인을 보장하나요?"),
    "faq_a1": ("No. Visa decisions are made by government authorities. We help you understand requirements and prepare documents.",
               "Үгүй. Визний шийдвэрийг төрийн эрх бүхий байгууллага гаргадаг. Бид шаардлага болон бичиг баримтаа бэлтгэхэд тусална.",
               "아니요. 비자 결정은 정부 기관에서 내립니다. 저희는 요건 이해와 서류 준비를 도와드립니다."),
    "faq_q2": ("Which destinations do you cover?",
               "Та ямар улсуудад зөвлөгөө өгдөг вэ?",
               "어느 국가를 지원하나요?"),
    "faq_a2": ("We provide guidance for the United States, Canada, Australia, South Korea and other destinations.",
               "Бид АНУ, Канад, Австрали, Өмнөд Солонгос болон бусад чиглэлд зөвлөгөө өгдөг.",
               "미국, 캐나다, 호주, 대한민국 및 기타 목적지에 대한 안내를 제공합니다."),
    "faq_q3": ("Can I take language courses online?",
               "Хэлний сургалтад онлайнаар хамрагдаж болох уу?",
               "온라인 어학 과정을 수강할 수 있나요?"),
    "faq_a3": ("Yes. We offer online English and Korean courses.",
               "Тийм. Бид англи, солонгос хэлний онлайн сургалт санал болгодог.",
               "네. 온라인 영어 및 한국어 과정을 제공합니다."),
    "faq_q4": ("How do I get started?",
               "Хэрхэн эхлэх вэ?",
               "어떻게 시작하면 되나요?"),
    "faq_a4": ("Send an inquiry through our Contact Us page and tell us about your plans.",
               "Холбоо барих хэсгээр хүсэлт илгээж, төлөвлөгөөгөө бичээрэй.",
               "문의하기 페이지에서 계획을 알려주세요."),

    "cta_title": ("Ready to plan your next chapter?",
                  "Дараагийн алхмаа төлөвлөхөд бэлэн үү?",
                  "다음 단계를 계획할 준비가 되셨나요?"),
    "cta_desc": ("Tell us about your goals and we will help you understand your next steps.",
                 "Зорилгоо бидэнд хэлээрэй. Бид дараагийн алхмыг тодорхойлоход тусална.",
                 "목표를 알려주시면 다음 단계를 안내해 드리겠습니다."),

    "education_head": ("Build your global future.",
                       "Дэлхийд хүрэх ирээдүйгээ бүтээгээрэй.",
                       "세계로 향하는 미래를 준비하세요."),
    "education_sub": ("Explore our partner schools and get guidance from application to arrival.",
                      "Манай хамтрагч сургуулиудтай танилцаж, өргөдлөөс эхлээд очих хүртэл зөвлөгөө аваарай.",
                      "협력 학교를 살펴보고 지원부터 도착까지 안내를 받아보세요."),
    "school_filter": ("Filter schools", "Сургуулиар шүүх", "학교 필터"),
    "country": ("Country", "Улс", "국가"),
    "school_type": ("School Type", "Сургуулийн төрөл", "학교 유형"),
    "all": ("All", "Бүгд", "전체"),
    "university": ("University", "Их сургууль", "대학교"),
    "college": ("College", "Коллеж", "컬리지"),
    "language_school": ("Language School", "Хэлний сургууль", "어학원"),
    "programs": ("Programs and areas of study", "Хөтөлбөр ба суралцах чиглэлүүд", "프로그램 및 전공 분야"),
    "school_note": ("Program availability, tuition and admission requirements can change. Contact us for current details.",
                    "Хөтөлбөр, сургалтын төлбөр болон элсэлтийн шаардлага өөрчлөгдөж болно. Шинэ мэдээллийг биднээс лавлана уу.",
                    "프로그램, 학비 및 입학 요건은 변경될 수 있습니다. 최신 정보는 문의해 주세요."),
    "view_details": ("View Details", "Дэлгэрэнгүй үзэх", "상세 정보 보기"),
    "visit_school": ("Visit Official Website", "Албан ёсны вэбсайт үзэх", "공식 웹사이트 방문"),
    "back": ("Back to all schools", "Бүх сургууль руу буцах", "전체 학교 목록으로 돌아가기"),

    "visa_head": ("Your visa journey starts here.",
                  "Таны визний аялал эндээс эхэлнэ.",
                  "비자 준비, 여기서 시작하세요."),
    "visa_sub": ("Visa consultation for the USA, Canada, Australia, the UK, Schengen countries, Japan and Korea.",
                 "АНУ, Канад, Австрали, Их Британи, Шенгений орнууд, Япон болон Солонгосын визний зөвлөгөө.",
                 "미국, 캐나다, 호주, 영국, 솅겐 국가, 일본 및 한국 비자 상담을 제공합니다."),
    "choose_country": ("Select your destination", "Очих улсаа сонгоно уу", "목적지를 선택하세요"),
    "visa_type": ("What type of consultation do you need?",
                  "Танд ямар төрлийн зөвлөгөө хэрэгтэй вэ?",
                  "어떤 상담이 필요하신가요?"),
    "visitor_visa": ("Visitor / Tourist Visa", "Зочлох / Жуулчны виз", "방문 / 관광 비자"),
    "student_visa": ("Student Visa", "Оюутны виз", "학생 비자"),
    "documents": ("Document Preparation", "Бичиг баримт бүрдүүлэлт", "서류 준비"),
    "general": ("General Consultation", "Ерөнхий зөвлөгөө", "일반 상담"),
    "not_sure": ("Not Sure Yet", "Одоогоор сайн мэдэхгүй байна", "아직 잘 모르겠습니다"),
    "visa_warning": ("Visa decisions are made by government authorities. Consultation does not guarantee visa approval.",
                     "Визний шийдвэрийг төрийн эрх бүхий байгууллага гаргана. Зөвлөгөө нь виз гарах баталгаа болохгүй.",
                     "비자 결정은 정부 기관에서 내립니다. 상담은 비자 승인을 보장하지 않습니다."),
    "request_visa": ("Request Visa Consultation", "Визний зөвлөгөө авах хүсэлт", "비자 상담 신청"),

    "travel_head": ("Explore. Travel. Relocate.",
                    "Судал. Аял. Суурьш.",
                    "탐험하세요. 여행하세요. 정착하세요."),
    "travel_sub": ("Prepare for international travel and get practical support for moving abroad.",
                   "Олон улсын аялалдаа бэлтгэж, гадаадад нүүхэд хэрэгтэй дэмжлэг аваарай.",
                   "해외여행을 준비하고 해외 이주에 필요한 지원을 받아보세요."),
    "flight": ("Flight Assistance", "Нислэгийн туслалцаа", "항공편 지원"),
    "hotel": ("Hotel Assistance", "Зочид буудлын туслалцаа", "호텔 예약 지원"),
    "travel_prep": ("Travel Preparation", "Аяллын бэлтгэл", "여행 준비"),
    "moving": ("Moving Abroad", "Гадаадад нүүх", "해외 이주"),
    "settlement": ("Settlement Guidance", "Суурьших зөвлөгөө", "현지 정착 안내"),
    "travel_destination": ("Tell us where you are headed", "Хаашаа явах гэж байгаагаа хэлээрэй", "목적지를 알려주세요"),
    "purpose": ("Main Purpose", "Аяллын гол зорилго", "주요 목적"),
    "tourism": ("Tourism", "Аялал жуулчлал", "관광"),
    "family": ("Visiting Family", "Гэр бүлдээ зочлох", "가족 방문"),
    "moving_abroad": ("Moving Abroad", "Гадаадад нүүх", "해외 이주"),
    "request_travel": ("Request Travel Consultation", "Аяллын зөвлөгөө авах хүсэлт", "여행 상담 신청"),

    "contact_head": ("Let's plan your next chapter.",
                     "Дараагийн алхмаа хамтдаа төлөвлөе.",
                     "새로운 시작을 함께 계획해요."),
    "contact_sub": ("Tell us about your goals and the services you are interested in.",
                    "Зорилго болон сонирхож буй үйлчилгээгээ бидэнд бичээрэй.",
                    "목표와 관심 있는 서비스를 알려주세요."),
    "send_inquiry": ("Send an Inquiry", "Хүсэлт илгээх", "문의 보내기"),
    "name": ("Full Name", "Овог нэр", "성명"),
    "email": ("Email Address", "И-мэйл хаяг", "이메일 주소"),
    "phone": ("Phone Number", "Утасны дугаар", "전화번호"),
    "destination": ("Preferred Destination", "Очихыг хүсэж буй улс", "희망 목적지"),
    "interested": ("Services You Are Interested In", "Сонирхож буй үйлчилгээ", "관심 있는 서비스"),
    "message": ("Tell us about your plans", "Төлөвлөгөөнийхөө талаар бичнэ үү", "계획을 알려주세요"),
    "message_hint": ("Tell us about your education, visa or travel plans...",
                     "Боловсрол, виз эсвэл аяллын төлөвлөгөөнийхөө талаар бичнэ үү...",
                     "유학, 비자 또는 여행 계획을 알려주세요..."),
    "submit": ("Prepare My Inquiry", "Хүсэлтээ бэлтгэх", "문의 내용 준비하기"),
    "required_error": ("Please enter your name and email and select at least one service.",
                       "Овог нэр, и-мэйл хаягаа оруулж, дор хаяж нэг үйлчилгээ сонгоно уу.",
                       "성명과 이메일을 입력하고 최소 한 가지 서비스를 선택해 주세요."),
    "email_error": ("Please enter a valid email address.",
                    "Зөв и-мэйл хаяг оруулна уу.",
                    "올바른 이메일 주소를 입력해 주세요."),
    "success": ("Your inquiry is ready. Open your email application to send it.",
                "Таны хүсэлт бэлэн боллоо. И-мэйл програмаа нээн илгээнэ үү.",
                "문의 내용이 준비되었습니다. 이메일 앱을 열어 보내주세요."),
    "open_email": ("Open Email to Send Inquiry", "И-мэйл нээж хүсэлт илгээх", "이메일 앱을 열어 문의 보내기"),
    "services": ("Services", "Үйлчилгээ", "서비스"),
    "contact_label": ("Contact", "Холбоо барих", "연락처"),
    "footer": ("Education, visa consulting, travel and relocation support for students and families.",
               "Оюутан, гэр бүлүүдэд зориулсан боловсрол, виз, аялал болон суурьшлын дэмжлэг.",
               "학생과 가족을 위한 교육, 비자 상담, 여행 및 해외 정착 지원 서비스입니다."),
    "legal": ("© 2026 Hanna Edu. All rights reserved. Visa decisions are made by the relevant authorities; consultation does not guarantee approval.",
              "© 2026 Hanna Edu. Бүх эрх хуулиар хамгаалагдсан. Визний шийдвэрийг эрх бүхий байгууллага гаргана.",
              "© 2026 Hanna Edu. 모든 권리 보유. 비자 결정은 관계 당국에서 내립니다."),
}

# School names remain official. Descriptions and program labels are translated.
SCHOOLS = [
    {
        "name": "University at Buffalo",
        "country": "United States",
        "type": "University",
        "city": "Buffalo, New York",
        "url": "https://www.buffalo.edu/",
        "description": (
            "A public research university in Buffalo, New York, part of the State University of New York (SUNY) system.",
            "Нью-Йорк мужийн Буффало хотод байрлах, Нью-Йорк мужийн их сургуулийн (SUNY) системд багтдаг улсын судалгааны их сургууль.",
            "뉴욕주 버펄로에 위치한 뉴욕주립대학교(SUNY) 소속 공립 연구 중심 대학교입니다.",
        ),
        "programs": ("Undergraduate programs · Graduate programs",
                     "Бакалавр · Магистрын хөтөлбөрүүд",
                     "학부 과정 · 대학원 과정"),
    },
    {
        "name": "University of Hawaii",
        "country": "United States",
        "type": "University",
        "city": "Hawaii",
        "url": "https://www.hawaii.edu/",
        "description": (
            "A public university system in the state of Hawaii, offering a wide range of academic programs.",
            "Хавай мужийн олон төрлийн сургалтын хөтөлбөр санал болгодог улсын их сургуулийн систем.",
            "다양한 학업 프로그램을 제공하는 하와이주의 공립 대학교 시스템입니다.",
        ),
        "programs": ("Undergraduate programs · Graduate programs",
                     "Бакалавр · Магистрын хөтөлбөрүүд",
                     "학부 과정 · 대학원 과정"),
    },
    {
        "name": "Midwestern Career College",
        "country": "United States",
        "type": "College",
        "city": "Chicago, Illinois",
        "url": "https://mccollege.edu/",
        "description": (
            "A private career college in downtown Chicago with career-focused programs.",
            "Чикаго хотын төвд байрлах, ажил мэргэжилд чиглэсэн хөтөлбөртэй хувийн коллеж.",
            "시카고 도심에 위치한 취업 중심 프로그램을 제공하는 사립 직업 교육 컬리지입니다.",
        ),
        "programs": ("Allied Health · Business · Information Technology · ESL",
                     "Эрүүл мэнд · Бизнес · Мэдээллийн технологи · ESL",
                     "보건 관련 분야 · 경영 · 정보기술 · ESL"),
    },
    {
        "name": "Academia Language School",
        "country": "United States",
        "type": "Language School",
        "city": "Honolulu, Hawaii",
        "url": "https://www.academiaschool.edu/",
        "description": (
            "An English language school in Honolulu, Hawaii, founded in 1969.",
            "1969 онд байгуулагдсан, Хавай мужийн Хонолулу хотын англи хэлний сургууль.",
            "1969년에 설립된 하와이주 호놀룰루의 영어 어학원입니다.",
        ),
        "programs": ("English language programs · ESL preparation",
                     "Англи хэлний хөтөлбөр · ESL бэлтгэл",
                     "영어 과정 · ESL 준비 과정"),
    },
    {
        "name": "Mentora College",
        "country": "United States",
        "type": "Language School",
        "city": "Washington, D.C.",
        "url": "https://bau.edu/mentora-esl/mentora-college/",
        "description": (
            "The ESL school of Bay Atlantic University in Washington, D.C.",
            "Вашингтон хотод байрлах Bay Atlantic University-ийн англи хэлний сургууль.",
            "워싱턴 D.C.에 위치한 Bay Atlantic University의 ESL 학교입니다.",
        ),
        "programs": ("English language programs · Test preparation",
                     "Англи хэлний хөтөлбөр · Шалгалтын бэлтгэл",
                     "영어 과정 · 시험 준비 과정"),
    },
    {
        "name": "Durham College",
        "country": "Canada",
        "type": "College",
        "city": "Oshawa, Ontario",
        "url": "https://durhamcollege.ca/",
        "description": (
            "A public college in Ontario, Canada, offering career-focused education.",
            "Канадын Онтарио мужид байрлах, ажил мэргэжилд чиглэсэн улсын коллеж.",
            "캐나다 온타리오주에 위치한 취업 중심 교육을 제공하는 공립 컬리지입니다.",
        ),
        "programs": ("Diploma programs · Certificate programs · Applied degrees",
                     "Диплом · Сертификат · Хэрэглээний бакалаврын хөтөлбөр",
                     "디플로마 과정 · 수료 과정 · 응용 학위 과정"),
    },
    {
        "name": "Canada Christian College",
        "country": "Canada",
        "type": "College",
        "city": "Whitby, Ontario",
        "url": "https://canadachristiancollege.com/",
        "description": (
            "A private Christian college in Whitby, Ontario.",
            "Канадын Онтарио мужийн Уитби хотод байрлах хувийн христийн коллеж.",
            "온타리오주 휘트비에 위치한 사립 기독교 컬리지입니다.",
        ),
        "programs": ("Ministry · Sacred Music · Christian Counselling · Religious Education",
                     "Шашны үйлчлэл · Шашны хөгжим · Христийн зөвлөгөө · Шашны боловсрол",
                     "목회 · 종교 음악 · 기독교 상담 · 종교 교육"),
    },
]

DESTINATIONS = [
    "United States", "Canada", "Australia", "United Kingdom",
    "Europe", "Japan", "South Korea", "Other",
]

DESTINATION_TRANSLATIONS = {
    "United States": ("United States", "АНУ", "미국"),
    "Canada": ("Canada", "Канад", "캐나다"),
    "Australia": ("Australia", "Австрали", "호주"),
    "United Kingdom": ("United Kingdom", "Их Британи", "영국"),
    "Europe": ("Europe", "Европ", "유럽"),
    "Japan": ("Japan", "Япон", "일본"),
    "South Korea": ("South Korea", "Өмнөд Солонгос", "대한민국"),
    "Other": ("Other", "Бусад", "기타"),
}

SERVICE_OPTIONS = ["Education", "Visa Consulting", "Travel", "Relocation", "Language Courses"]

SERVICE_TRANSLATIONS = {
    "Education": ("Education", "Боловсрол", "교육"),
    "Visa Consulting": ("Visa Consulting", "Визний зөвлөгөө", "비자 상담"),
    "Travel": ("Travel", "Аялал", "여행"),
    "Relocation": ("Relocation", "Суурьшил", "해외 정착"),
    "Language Courses": ("Language Courses", "Хэлний сургалт", "어학 과정"),
}

# Internal keys -> translation keys
VISA_DESTINATIONS = ["United States", "Canada", "Australia", "United Kingdom", "Europe", "Japan", "South Korea"]
VISA_TYPES = ["visitor_visa", "student_visa", "documents", "general", "not_sure"]
TRAVEL_PURPOSES = ["tourism", "family", "moving_abroad", "education"]
SCHOOL_TYPE_KEYS = {"University": "university", "College": "college", "Language School": "language_school"}
PAGES = ["home", "education", "visa", "travel", "contact"]

# ---------------------------------------------------------------------------
# Image system
# ---------------------------------------------------------------------------
# Put photos in an "assets" folder next to app.py. File names (jpg/png/webp):
#   hero_home, hero_education, hero_visa, hero_travel, hero_contact
#   country_<slug>   e.g. country_united-states, country_south-korea
#   school_<slug>    e.g. school_university-at-buffalo
#   service_<name>   education, visa, travel, relocation, language
# Anything missing automatically falls back to an elegant gradient tile.
# You can also point a key at a hosted image: IMAGE_URLS["country_canada"] = "https://..."
ASSETS_DIR = Path(__file__).parent / "assets"
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")
IMAGE_URLS = {}

COUNTRY_FLAGS = {
    "United States": "🇺🇸", "Canada": "🇨🇦", "Australia": "🇦🇺",
    "United Kingdom": "🇬🇧", "Europe": "🇪🇺", "Japan": "🇯🇵",
    "South Korea": "🇰🇷", "Other": "🌍",
}
SCHOOL_EMOJI = {"University": "🎓", "College": "🏛️", "Language School": "🗣️"}
GRADIENTS = [
    "linear-gradient(135deg,#1b3a6b,#2f63c8)",
    "linear-gradient(135deg,#1d4378,#0ea5e9)",
    "linear-gradient(135deg,#1f3f73,#6366f1)",
    "linear-gradient(135deg,#1b3a6b,#334155)",
]
FLAG_CODES = {
    "United States": "us", "Canada": "ca", "Australia": "au",
    "United Kingdom": "gb", "Europe": "eu", "Japan": "jp", "South Korea": "kr",
}


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


@st.cache_data(show_spinner=False)
def _file_to_data_uri(path_str, mtime):
    """Downscale (if Pillow is installed) and embed a local image as a data URI."""
    path = Path(path_str)
    data, mime = path.read_bytes(), "image/" + path.suffix.lower().lstrip(".").replace("jpg", "jpeg")
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(data))
        img.thumbnail((1600, 1600))
        buf = io.BytesIO()
        img.convert("RGB").save(buf, "JPEG", quality=82)
        data, mime = buf.getvalue(), "image/jpeg"
    except Exception:
        pass
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


def image_source(key):
    if key in IMAGE_URLS:
        return IMAGE_URLS[key]
    for ext in IMAGE_EXTS:
        path = ASSETS_DIR / f"{key}{ext}"
        if path.exists():
            return _file_to_data_uri(str(path), path.stat().st_mtime)
    return None


def mark(col, name):
    """Invisible marker so CSS can lay this row of columns out as a 2/3/4-per-row grid on phones."""
    col.markdown(f'<span class="m m-{name}"></span>', unsafe_allow_html=True)


def svg_uri(svg):
    return "data:image/svg+xml;utf8," + quote(svg)


def flag_img(dest, width=28):
    """Real flag image. Local assets/flag_<code>.png wins, else flagcdn.com."""
    code = FLAG_CODES.get(dest)
    if not code:
        return "🌍"
    src = image_source(f"flag_{code}") or f"https://flagcdn.com/w160/{code}.png"
    return f'<img class="flag" src="{src}" width="{width}" alt="{dest}">'


def campus_svg(kind="University", variant=0):
    top, bottom = [("#1b3a6b", "#2f63c8"), ("#1d4378", "#0ea5e9"), ("#1f3f73", "#6366f1")][variant % 3]
    head = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" width="800" height="400">'
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
        f'<stop offset="1" stop-color="{bottom}"/></linearGradient></defs>'
        '<rect width="800" height="400" fill="url(#g)"/>'
        '<circle cx="650" cy="80" r="34" fill="#fde68a" fill-opacity=".9"/>'
        '<g fill="#fff" fill-opacity=".18"><ellipse cx="140" cy="70" rx="70" ry="18"/>'
        '<ellipse cx="200" cy="85" rx="55" ry="14"/><ellipse cx="560" cy="150" rx="60" ry="14"/></g>'
        '<rect y="330" width="800" height="70" fill="#1b3a6b" fill-opacity=".85"/>'
        '<path d="M360 330 L440 330 L520 400 L280 400Z" fill="#cbd5e1" fill-opacity=".5"/>'
    )
    trees = (
        '<g><rect x="78" y="290" width="8" height="45" fill="#3f3f46"/><circle cx="82" cy="280" r="30" fill="#0d9488"/>'
        '<rect x="714" y="290" width="8" height="45" fill="#3f3f46"/><circle cx="718" cy="280" r="30" fill="#0d9488"/></g>'
    )
    if kind == "University":
        body = (
            '<rect x="200" y="190" width="400" height="120" fill="#94a3b8"/>'
            '<polygon points="190,172 400,98 610,172" fill="#e2e8f0"/>'
            '<rect x="190" y="172" width="420" height="18" fill="#cbd5e1"/>'
            + "".join(f'<rect x="{214 + i * 68}" y="190" width="24" height="120" fill="#f8fafc"/>' for i in range(6))
            + '<rect x="370" y="76" width="60" height="22" fill="#e2e8f0"/>'
            '<path d="M370 76 Q400 22 430 76Z" fill="#fbbf24"/>'
            '<rect x="180" y="310" width="440" height="14" fill="#cbd5e1"/><rect x="160" y="324" width="480" height="12" fill="#94a3b8"/>'
        )
    elif kind == "College":
        wins = "".join(
            f'<rect x="{x}" y="{y}" width="18" height="26" fill="#38bdf8"/>'
            for x in (150, 190, 230, 270, 310, 468, 508, 548, 588, 628) for y in (215, 265)
        )
        body = (
            '<rect x="130" y="195" width="540" height="135" fill="#e2e8f0"/>' + wins +
            '<rect x="350" y="95" width="100" height="235" fill="#f8fafc"/>'
            '<polygon points="338,95 400,38 462,95" fill="#1e293b"/>'
            '<circle cx="400" cy="135" r="22" fill="#fff" stroke="#1b3a6b" stroke-width="4"/>'
            '<path d="M400 135 V120 M400 135 L411 141" stroke="#1b3a6b" stroke-width="3" fill="none"/>'
            '<rect x="383" y="262" width="34" height="68" fill="#1e3a8a"/>'
        )
    else:
        body = (
            '<rect x="170" y="180" width="460" height="150" fill="#f8fafc"/>'
            '<rect x="170" y="168" width="460" height="14" fill="#1b3a6b"/>'
            + "".join(f'<rect x="{190 + i * 108}" y="205" width="90" height="85" fill="#7dd3fc"/>' for i in range(4))
            + '<circle cx="400" cy="108" r="40" fill="#38bdf8"/>'
            '<g fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="2"><ellipse cx="400" cy="108" rx="40" ry="14"/>'
            '<ellipse cx="400" cy="108" rx="18" ry="40"/><line x1="360" y1="108" x2="440" y2="108"/></g>'
            '<g font-family="Arial,sans-serif" font-size="17" font-weight="700" fill="#1b3a6b">'
            '<rect x="170" y="60" width="96" height="38" rx="12" fill="#fff"/><text x="190" y="85">Hello</text>'
            '<rect x="540" y="60" width="96" height="38" rx="12" fill="#fff"/><text x="566" y="85">안녕</text></g>'
        )
    return head + body + trees + "</svg>"


def agency_hero_svg():
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 420" width="520" height="420">'
        '<defs><radialGradient id="gl" cx="40%" cy="35%"><stop offset="0" stop-color="#60a5fa"/>'
        '<stop offset="1" stop-color="#1e3a8a"/></radialGradient></defs>'
        '<circle cx="260" cy="215" r="150" fill="url(#gl)"/>'
        '<g fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="1.5"><ellipse cx="260" cy="215" rx="150" ry="55"/>'
        '<ellipse cx="260" cy="215" rx="75" ry="150"/><line x1="110" y1="215" x2="410" y2="215"/>'
        '<line x1="260" y1="65" x2="260" y2="365"/></g>'
        '<g fill="#93c5fd" fill-opacity=".55"><path d="M170 150 q30-30 70-15 q20 20-5 40 q-30 10-45 30 q-25-20-20-55z"/>'
        '<path d="M290 130 q40-20 80 10 q10 30-20 40 q-30-5-45 15 q-25-25-15-65z"/>'
        '<path d="M300 250 q30-10 55 15 q-5 40-40 50 q-25-25-15-65z"/>'
        '<path d="M190 255 q20-5 30 20 q-5 30-25 35 q-15-25-5-55z"/></g>'
        '<path d="M70 330 C140 130 340 40 470 110" fill="none" stroke="#fbbf24" stroke-width="3" '
        'stroke-dasharray="3 9" stroke-linecap="round"/>'
        '<g transform="translate(468 108) rotate(28)"><polygon points="30,0 -10,-8 -22,-30 -30,-30 -22,-6 -40,-4 -44,-12 '
        '-50,-12 -46,0 -50,12 -44,12 -40,4 -22,6 -30,30 -22,30 -10,8" fill="#fff"/></g>'
        '<g transform="translate(40 70)"><rect width="90" height="70" rx="14" fill="#fff"/>'
        '<polygon points="45,16 75,30 45,44 15,30" fill="#1b3a6b"/><path d="M28 38 v12 q17 10 34 0 v-12 l-17 8z" fill="#2f63c8"/>'
        '<line x1="75" y1="30" x2="75" y2="48" stroke="#fbbf24" stroke-width="3"/></g>'
        '<g transform="translate(395 265)"><rect width="80" height="100" rx="10" fill="#fbbf24"/>'
        '<circle cx="40" cy="40" r="18" fill="none" stroke="#1b3a6b" stroke-width="3"/>'
        '<ellipse cx="40" cy="40" rx="8" ry="18" fill="none" stroke="#1b3a6b" stroke-width="2"/>'
        '<rect x="18" y="72" width="44" height="6" rx="3" fill="#1b3a6b"/><rect x="26" y="84" width="28" height="5" rx="2.5" fill="#1b3a6b"/></g>'
        '<g transform="translate(55 285)"><path d="M25 0 C8 0 0 13 0 25 C0 45 25 70 25 70 C25 70 50 45 50 25 C50 13 42 0 25 0z" fill="#ef4444"/>'
        '<circle cx="25" cy="25" r="10" fill="#fff"/></g></svg>'
    )


def agency_office_svg():
    skyline = "".join(
        f'<rect x="{x}" y="{200 - h}" width="{w}" height="{h}" fill="#1e3a8a" fill-opacity=".55"/>'
        for x, w, h in [(60, 50, 90), (120, 40, 130), (170, 60, 70), (240, 45, 110), (300, 55, 150),
                        (370, 40, 80), (420, 60, 120), (490, 45, 95)]
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 440" width="640" height="440">'
        '<rect width="640" height="440" rx="22" fill="#eaf1fb"/>'
        '<rect x="40" y="40" width="560" height="190" rx="10" fill="#bfdbfe"/>'
        '<circle cx="540" cy="80" r="22" fill="#fde68a"/>' + skyline +
        '<rect x="40" y="40" width="560" height="190" rx="10" fill="none" stroke="#fff" stroke-width="6"/>'
        '<line x1="320" y1="40" x2="320" y2="230" stroke="#fff" stroke-width="5"/>'
        '<path d="M150 330 v-62 q0-34 40-34 q40 0 40 34 v62z" fill="#2f63c8"/><circle cx="190" cy="212" r="27" fill="#f1c9a5"/>'
        '<path d="M163 208 q4-30 30-28 q26 0 28 26 q-20-14-58 2z" fill="#1f2937"/>'
        '<path d="M410 330 v-62 q0-34 40-34 q40 0 40 34 v62z" fill="#0f766e"/><circle cx="450" cy="212" r="27" fill="#e0ac84"/>'
        '<path d="M421 212 q0-36 30-34 q30 2 28 34 q-12-18-30-16 q-18 0-28 16z" fill="#111827"/>'
        '<rect x="30" y="326" width="580" height="22" rx="6" fill="#1b3a6b"/><rect x="70" y="348" width="14" height="70" fill="#1e293b"/>'
        '<rect x="556" y="348" width="14" height="70" fill="#1e293b"/>'
        '<rect x="285" y="292" width="70" height="36" rx="4" fill="#334155"/><rect x="291" y="297" width="58" height="26" fill="#38bdf8"/>'
        '<rect x="110" y="312" width="52" height="14" fill="#fff"/><rect x="490" y="312" width="52" height="14" fill="#fff"/>'
        '<rect x="565" y="290" width="26" height="36" rx="4" fill="#b45309"/><ellipse cx="578" cy="278" rx="26" ry="14" fill="#16a34a"/>'
        '<ellipse cx="560" cy="290" rx="16" ry="10" fill="#22c55e"/></svg>'
    )


def school_art(school):
    variant = int(hashlib.md5(school["name"].encode()).hexdigest(), 16) % 3
    return svg_uri(campus_svg(school["type"], variant))


def photo(key, height=180, emoji="🌍", label="", art=None, flag=None):
    """Uniformly cropped tile: real photo > illustration (art) > navy gradient with flag/emoji."""
    src = image_source(key) or art
    if src:
        style, inner = f"background-image:url('{src}');", ""
    else:
        idx = int(hashlib.md5(key.encode()).hexdigest(), 16) % len(GRADIENTS)
        big = flag_img(flag, 84).replace('class="flag"', 'class="flag big"') if flag in FLAG_CODES else f'<span class="ph-emoji">{emoji}</span>'
        style, inner = f"background:{GRADIENTS[idx]};", big
    cap = f'<div class="photo-cap">{label}</div>' if label else ""
    return f'<div class="photo" style="height:{height}px;{style}">{inner}{cap}</div>'


def country_photo(dest, height=180):
    return photo(
        f"country_{slugify(dest)}", height, COUNTRY_FLAGS.get(dest, "🌍"),
        f"{flag_img(dest, 26)} {destination_name(dest)}", flag=dest,
    )


def hero_bg(key):
    src = image_source(key) if key else None
    if not src:
        return ""
    return ("background-image:linear-gradient(135deg,rgba(27,58,107,.92),rgba(37,84,147,.75)),"
            f"url('{src}');")


# ---------------------------------------------------------------------------
# Session state + translation helpers
# ---------------------------------------------------------------------------
st.session_state.setdefault("language", "English")
st.session_state.setdefault("page", "home")
st.session_state.setdefault("selected_school", None)
st.session_state.setdefault("c_dest", "United States")
st.session_state.setdefault("c_services", [])
st.session_state.setdefault("c_message", "")
st.session_state.setdefault("mailto", None)


def lang_index():
    lang = st.session_state.get("language", "English")
    return LANGUAGES.index(lang) if lang in LANGUAGES else 0


def pick(options, fallback=""):
    """Pick the current-language entry from an (en, mn, ko) tuple."""
    return options[lang_index()] if options else fallback


def t(key):
    return pick(TEXT.get(key, (key, key, key)))


def destination_name(value):
    return pick(DESTINATION_TRANSLATIONS.get(value, (value, value, value)))


def service_name(value):
    return pick(SERVICE_TRANSLATIONS.get(value, (value, value, value)))


def go(page, **prefill):
    """Button callback: switch page and optionally prefill the contact form."""
    st.session_state["page"] = page
    st.session_state["selected_school"] = None
    if "dest" in prefill:
        st.session_state["c_dest"] = prefill["dest"]
    if "services" in prefill:
        st.session_state["c_services"] = prefill["services"]
    if "message" in prefill:
        st.session_state["c_message"] = prefill["message"]
    st.session_state["mailto"] = None


def select_school(name):
    st.session_state["selected_school"] = name


# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"], .stApp {font-family:'Inter',sans-serif;}
    .stApp {font-size:1.05rem;}
    #MainMenu, footer, header[data-testid="stHeader"] {visibility:hidden; height:0;}
    .block-container {padding-top: 1.5rem; max-width: 1400px; width: 94%; padding-left: 2rem; padding-right: 2rem;}
    .label {color:#2f63c8; font-weight:700; letter-spacing:.08em; font-size:.8rem; margin-bottom:.25rem;}
    .hero {background:linear-gradient(135deg,#1b3a6b 0%,#255493 100%); color:#fff;
           padding:4.5rem 3.5rem; border-radius:22px; margin-bottom:1.5rem;}
    .hero h1 {color:#fff; font-size:3.2rem; line-height:1.2; margin:.4rem 0 1rem 0;}
    .hero p {font-size:1.25rem; opacity:.95; max-width:760px;}
    .hero .label {color:#93c5fd;}
    .hero {background-size:cover; background-position:center; box-shadow:0 10px 30px rgba(27,58,107,.30);}
    .muted {color:#6b7280;}
    .brand {font-size:2.4rem; font-weight:800; letter-spacing:.07em; color:#1b3a6b; white-space:nowrap;
            display:flex; align-items:center; gap:.8rem; line-height:1;}
    .brand-mark {background:linear-gradient(135deg,#1b3a6b,#2f63c8); color:#fff; border-radius:12px; width:50px; height:50px;
                 display:inline-flex; align-items:center; justify-content:center; font-size:1.7rem; letter-spacing:0;}
    .hero-flex {display:flex; align-items:center; justify-content:space-between; gap:2rem;}
    .hero-art {width:440px; max-width:40%; flex-shrink:0;}
    .flag {border-radius:3px; box-shadow:0 1px 4px rgba(0,0,0,.35); vertical-align:middle; margin-right:.35rem;}
    .flag.big {width:84px; border-radius:6px; margin:0; box-shadow:0 4px 14px rgba(0,0,0,.4);}
    .flagcard {text-align:center; padding:.8rem .2rem; border:1px solid #e5e7eb; border-radius:14px; background:#fff;
               font-weight:600; font-size:.82rem; margin-bottom:.4rem; min-height:104px;}
    .flagcard.sel {border:2px solid #1b3a6b; background:#eff6ff;}
    .flagcard .flag {margin:0 0 .4rem 0;}
    [data-testid="stBaseButton-primary"], [data-testid="stBaseLinkButton-primary"] {
        background:#1b3a6b !important; border-color:#1b3a6b !important; color:#fff !important;}
    [data-testid="stBaseButton-primary"]:hover {background:#2f63c8 !important; border-color:#2f63c8 !important;}
    .element-container:has(.m), [data-testid="stElementContainer"]:has(.m) {display:none;}
    @media (max-width:768px) {
        .block-container {padding:1rem .9rem 2rem !important; width:100% !important; max-width:100% !important;}
        .stApp {font-size:1rem;}
        .brand {font-size:1.5rem; gap:.6rem;}
        .brand-mark {width:38px; height:38px; font-size:1.25rem; border-radius:10px;}
        .hero {padding:1.8rem 1.2rem; border-radius:16px;}
        .hero h1 {font-size:1.75rem;}
        .hero p {font-size:1rem;}
        .hero-flex {flex-direction:column; align-items:flex-start; gap:1rem;}
        .hero-art {width:70%; max-width:260px; align-self:center;}
        .photo {max-height:190px;}
        .photo-cap {font-size:.9rem;}
        .ph-emoji {font-size:2rem;}
        .flag.big {width:56px;}
        .flagcard {min-height:84px; font-size:.68rem; padding:.5rem .1rem;}
        .flagcard .flag {width:36px;}
        h2 {font-size:1.5rem !important;} h3 {font-size:1.2rem !important;}
        [data-testid="stHorizontalBlock"]:has(.m-grid2), [data-testid="stHorizontalBlock"]:has(.m-grid3),
        [data-testid="stHorizontalBlock"]:has(.m-grid4) {flex-wrap:wrap !important; gap:.5rem !important;}
        [data-testid="stHorizontalBlock"]:has(.m-grid2) > [data-testid="stColumn"],
        [data-testid="stHorizontalBlock"]:has(.m-grid2) > div[data-testid="column"] {
            flex:1 1 calc(50% - .5rem) !important; min-width:calc(50% - .5rem) !important; width:calc(50% - .5rem) !important;}
        [data-testid="stHorizontalBlock"]:has(.m-grid3) > [data-testid="stColumn"],
        [data-testid="stHorizontalBlock"]:has(.m-grid3) > div[data-testid="column"] {
            flex:1 1 calc(33.333% - .5rem) !important; min-width:calc(33.333% - .5rem) !important; width:calc(33.333% - .5rem) !important;}
        [data-testid="stHorizontalBlock"]:has(.m-grid4) > [data-testid="stColumn"],
        [data-testid="stHorizontalBlock"]:has(.m-grid4) > div[data-testid="column"] {
            flex:1 1 calc(25% - .5rem) !important; min-width:calc(25% - .5rem) !important; width:calc(25% - .5rem) !important;}
        [data-testid="stHorizontalBlock"]:has(.m-grid3) button {font-size:.75rem; padding:.25rem .1rem; min-height:2.3rem;}
    }
    .office-img {width:100%; border-radius:18px; box-shadow:0 8px 24px rgba(27,58,107,.18);}
    .photo {position:relative; width:100%; border-radius:14px; background-size:cover; background-position:center;
            display:flex; align-items:center; justify-content:center; overflow:hidden; margin-bottom:.6rem;
            box-shadow:0 2px 8px rgba(0,0,0,.08); transition:transform .25s ease, box-shadow .25s ease;}
    .photo:hover {transform:translateY(-2px); box-shadow:0 8px 20px rgba(0,0,0,.15);}
    .ph-emoji {font-size:3rem; filter:drop-shadow(0 2px 4px rgba(0,0,0,.25));}
    .photo-cap {position:absolute; left:0; right:0; bottom:0; padding:.6rem .8rem; color:#fff; font-weight:700;
                background:linear-gradient(to top,rgba(0,0,0,.65),rgba(0,0,0,0));}
    div[data-testid="stVerticalBlockBorderWrapper"] {border-radius:16px;}
    .stButton>button, .stLinkButton>a {border-radius:10px; font-weight:600;}
    .chip {display:inline-block; padding:.35rem .9rem; margin:.2rem .3rem .2rem 0;
           background:#ccfbf1; color:#115e59; border-radius:999px; font-weight:600;}
    </style>
    """,
    unsafe_allow_html=True,
)


def section_header(label_key, title_key, desc_key=None):
    st.markdown(f'<div class="label">{t(label_key)}</div>', unsafe_allow_html=True)
    st.subheader(t(title_key))
    if desc_key:
        st.markdown(f'<p class="muted">{t(desc_key)}</p>', unsafe_allow_html=True)


def hero(head_key, sub_key, label_key=None, bg_key=None):
    label = f'<div class="label">{t(label_key)}</div>' if label_key else ""
    st.markdown(
        f'<div class="hero" style="{hero_bg(bg_key)}">{label}<h1>{t(head_key)}</h1><p>{t(sub_key)}</p></div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Header / navigation
# ---------------------------------------------------------------------------
def render_header():
    left, right = st.columns([4, 1.3])
    left.markdown('<div class="brand"><span class="brand-mark">H</span>HANNA EDU</div>', unsafe_allow_html=True)
    right.selectbox(t("language"), LANGUAGES, key="language", label_visibility="collapsed")
    cols = st.columns(len(PAGES))
    mark(cols[0], "grid3")
    for col, page in zip(cols, PAGES):
        col.button(
            t(page), key=f"nav_{page}", on_click=go, args=(page,), use_container_width=True,
            type="primary" if st.session_state["page"] == page else "secondary",
        )
    st.divider()


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_home():
    hero_art = image_source("agency_hero") or svg_uri(agency_hero_svg())
    st.markdown(
        f"""<div class="hero" style="{hero_bg('hero_home')}"><div class="hero-flex"><div>
        <div class="label">{t('hero_label')}</div>
        <h1>{t('hero_title')}</h1>
        <p>{t('hero_desc')}</p></div>
        <img class="hero-art" src="{hero_art}" alt="Hanna Edu"></div></div>""",
        unsafe_allow_html=True,
    )
    c1, c2, _ = st.columns([1, 1, 3])
    c1.button(t("start"), key="home_start", on_click=go, args=("contact",), type="primary")
    c2.button(t("consult"), key="home_consult", on_click=go, args=("contact",))

    st.write("")
    section_header("what_we_do", "services_title", "services_desc")
    services = [
        ("🎓", "education_service", "education_desc", "education"),
        ("🛂", "visa_service", "visa_desc", "visa"),
        ("✈️", "travel_service", "travel_desc", "travel"),
        ("🏠", "relocation_service", "relocation_desc", "travel"),
        ("🗣️", "language_service", "language_desc", "contact"),
    ]
    cols = st.columns(len(services))
    mark(cols[0], "grid2")
    for col, (icon, title, desc, target) in zip(cols, services):
        with col.container(border=True):
            st.markdown(photo(f"service_{title.split('_')[0]}", 120, icon), unsafe_allow_html=True)
            st.markdown(f"**{t(title)}**")
            st.caption(t(desc))
            st.button(t("view_details"), key=f"svc_{title}", on_click=go, args=(target,))

    st.write("")
    section_header("partners", "partners_title", "partners_desc")
    st.button(t("education"), key="home_partners", on_click=go, args=("education",))

    st.write("")
    section_header("destinations", "destinations_title")
    tiles = st.columns(4)
    mark(tiles[0], "grid2")
    for i, d in enumerate(DESTINATIONS[:-1]):
        with tiles[i % 4]:
            st.markdown(country_photo(d, 160), unsafe_allow_html=True)

    st.write("")
    section_header("why", "why_title")
    img_col, text_col = st.columns([1.1, 1])
    office = image_source("agency_office") or svg_uri(agency_office_svg())
    img_col.markdown(f'<img class="office-img" src="{office}" alt="Hanna Edu team">', unsafe_allow_html=True)
    for n in (1, 2, 3):
        with text_col.container(border=True):
            st.markdown(f"**{t(f'why{n}')}**")
            st.caption(t(f"why{n}_desc"))

    st.write("")
    st.markdown(f'<div class="label">{t("how")}</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    mark(cols[0], "grid2")
    for col, n in zip(cols, (1, 2, 3, 4)):
        with col.container(border=True):
            st.markdown(f"**{n}. {t(f'step{n}')}**")
            st.caption(t(f"step{n}_desc"))

    st.write("")
    section_header("faq", "faq_title")
    for n in (1, 2, 3, 4):
        with st.expander(t(f"faq_q{n}")):
            st.write(t(f"faq_a{n}"))

    st.write("")
    with st.container(border=True):
        st.subheader(t("cta_title"))
        st.write(t("cta_desc"))
        st.button(t("start"), key="home_cta", on_click=go, args=("contact",), type="primary")


def school_type_label(value):
    return t(SCHOOL_TYPE_KEYS.get(value, "all"))


def page_education():
    selected = st.session_state.get("selected_school")
    school = next((s for s in SCHOOLS if s["name"] == selected), None)

    if school:
        st.button(f"← {t('back')}", key="school_back", on_click=select_school, args=(None,))
        st.markdown(
            photo(f"school_{slugify(school['name'])}", 320, SCHOOL_EMOJI.get(school["type"], "🎓"), school["name"], art=school_art(school)),
            unsafe_allow_html=True,
        )
        st.markdown(f"## {school['name']}")
        st.caption(f"{school['city']} · {destination_name(school['country'])} · {school_type_label(school['type'])}")
        st.write(pick(school["description"]))
        st.markdown(f"**{t('programs')}**")
        st.write(pick(school["programs"]))
        st.info(t("school_note"))
        c1, c2, _ = st.columns([1.3, 1.3, 3])
        c1.link_button(t("visit_school"), school["url"])
        c2.button(
            t("consult"), key="school_consult", on_click=go, args=("contact",),
            kwargs={
                "dest": school["country"],
                "services": ["Education"],
                "message": school["name"],
            },
            type="primary",
        )
        return

    hero("education_head", "education_sub", bg_key="hero_education")
    st.markdown(f"**{t('school_filter')}**")
    f1, f2, _ = st.columns([1, 1, 2])
    countries = ["All"] + sorted({s["country"] for s in SCHOOLS})
    types = ["All"] + list(SCHOOL_TYPE_KEYS)
    country = f1.selectbox(
        t("country"), countries,
        format_func=lambda v: t("all") if v == "All" else destination_name(v),
    )
    stype = f2.selectbox(
        t("school_type"), types,
        format_func=lambda v: t("all") if v == "All" else school_type_label(v),
    )

    filtered = [
        s for s in SCHOOLS
        if (country == "All" or s["country"] == country)
        and (stype == "All" or s["type"] == stype)
    ]

    for i in range(0, len(filtered), 2):
        cols = st.columns(2)
        for col, s in zip(cols, filtered[i:i + 2]):
            with col.container(border=True):
                st.markdown(
                    photo(f"school_{slugify(s['name'])}", 190, SCHOOL_EMOJI.get(s["type"], "🎓"), art=school_art(s)),
                    unsafe_allow_html=True,
                )
                st.markdown(f"### {s['name']}")
                st.caption(f"{s['city']} · {destination_name(s['country'])} · {school_type_label(s['type'])}")
                st.write(pick(s["description"]))
                st.caption(f"**{t('programs')}:** {pick(s['programs'])}")
                st.button(t("view_details"), key=f"school_{s['name']}", on_click=select_school, args=(s["name"],))
    st.caption(t("school_note"))


def set_visa_dest(dest):
    st.session_state["visa_dest_sel"] = dest


def page_visa():
    hero("visa_head", "visa_sub", bg_key="hero_visa")
    st.subheader(t("choose_country"))
    st.session_state.setdefault("visa_dest_sel", "United States")
    dest = st.session_state["visa_dest_sel"]
    cols = st.columns(len(VISA_DESTINATIONS))
    mark(cols[0], "grid4")
    for col, d in zip(cols, VISA_DESTINATIONS):
        selected = d == dest
        with col:
            st.markdown(
                f'<div class="flagcard{" sel" if selected else ""}">{flag_img(d, 56)}<div>{destination_name(d)}</div></div>',
                unsafe_allow_html=True,
            )
            st.button("✓" if selected else "○", key=f"visa_pick_{slugify(d)}", on_click=set_visa_dest,
                      args=(d,), use_container_width=True, type="primary" if selected else "secondary")
    st.markdown(country_photo(dest, 240), unsafe_allow_html=True)
    st.subheader(t("visa_type"))
    vtype = st.radio(
        t("visa_type"), VISA_TYPES, format_func=t,
        label_visibility="collapsed", key="visa_type_choice",
    )
    st.warning(t("visa_warning"))
    # Message is stored in English so the inquiry email is readable by the team.
    st.button(
        t("request_visa"), key="visa_request", on_click=go, args=("contact",),
        kwargs={
            "dest": dest,
            "services": ["Visa Consulting"],
            "message": f"Visa consultation: {TEXT[vtype][0]}",
        },
        type="primary",
    )


def page_travel():
    hero("travel_head", "travel_sub", bg_key="hero_travel")
    items = [("✈️", "flight"), ("🏨", "hotel"), ("🧳", "travel_prep"), ("📦", "moving"), ("🏠", "settlement")]
    cols = st.columns(len(items))
    mark(cols[0], "grid2")
    for col, (icon, key) in zip(cols, items):
        with col.container(border=True):
            st.markdown(photo(f"travel_{key}", 110, icon), unsafe_allow_html=True)
            st.markdown(f"**{t(key)}**")

    st.write("")
    st.subheader(t("travel_destination"))
    c1, c2 = st.columns(2)
    dest = c1.selectbox(t("destination"), DESTINATIONS, format_func=destination_name, key="travel_dest")
    purpose = c2.selectbox(
        t("purpose"), TRAVEL_PURPOSES,
        format_func=lambda k: t(k) if k in TEXT else service_name("Education"),
        key="travel_purpose",
    )
    st.markdown(country_photo(dest, 240), unsafe_allow_html=True)
    services = ["Relocation"] if purpose == "moving_abroad" else ["Education"] if purpose == "education" else ["Travel"]
    purpose_en = TEXT[purpose][0] if purpose in TEXT else "Education"
    st.button(
        t("request_travel"), key="travel_request", on_click=go, args=("contact",),
        kwargs={"dest": dest, "services": services, "message": f"Purpose: {purpose_en}"},
        type="primary",
    )


def build_mailto(name, email, phone, dest, services, message):
    subject = f"Hanna Edu Inquiry - {name}"
    body = "\n".join([
        f"Name: {name}",
        f"Email: {email}",
        f"Phone: {phone or '-'}",
        f"Preferred destination: {dest}",
        f"Services: {', '.join(services)}",
        "",
        "Message:",
        message or "-",
    ])
    return f"mailto:{CONTACT_EMAIL}?subject={quote(subject, safe='')}&body={quote(body, safe='')}"


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def page_contact():
    hero("contact_head", "contact_sub", bg_key="hero_contact")
    st.subheader(t("send_inquiry"))

    with st.form("contact_form"):
        c1, c2 = st.columns(2)
        name = c1.text_input(t("name"))
        email = c2.text_input(t("email"))
        c3, c4 = st.columns(2)
        phone = c3.text_input(t("phone"))
        dest = c4.selectbox(t("destination"), DESTINATIONS, format_func=destination_name, key="c_dest")
        services = st.multiselect(t("interested"), SERVICE_OPTIONS, format_func=service_name, key="c_services")
        message = st.text_area(t("message"), placeholder=t("message_hint"), height=150, key="c_message")
        submitted = st.form_submit_button(t("submit"), type="primary")

    if submitted:
        if not name.strip() or not email.strip() or not services:
            st.session_state["mailto"] = None
            st.error(t("required_error"))
        elif not EMAIL_RE.match(email.strip()):
            st.session_state["mailto"] = None
            st.error(t("email_error"))
        else:
            st.session_state["mailto"] = build_mailto(
                name.strip(), email.strip(), phone.strip(), dest, services, message.strip()
            )

    if st.session_state.get("mailto"):
        st.success(t("success"))
        st.link_button(t("open_email"), st.session_state["mailto"], type="primary")

    st.write("")
    st.caption(f"{t('contact_label')}: {CONTACT_EMAIL} · {WEBSITE}")


def render_footer():
    st.divider()
    c1, c2, c3 = st.columns([2, 1, 1.5])
    c1.markdown("**HANNA EDU**")
    c1.caption(t("footer"))
    c2.markdown(f"**{t('services')}**")
    for s in SERVICE_OPTIONS:
        c2.caption(service_name(s))
    c3.markdown(f"**{t('contact_label')}**")
    c3.caption(CONTACT_EMAIL)
    c3.caption(WEBSITE)
    st.caption(t("legal"))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
render_header()

{
    "home": page_home,
    "education": page_education,
    "visa": page_visa,
    "travel": page_travel,
    "contact": page_contact,
}.get(st.session_state["page"], page_home)()

render_footer()
