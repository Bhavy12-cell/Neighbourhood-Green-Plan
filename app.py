import re
import streamlit as st
from google import genai

# ---------- Settings ----------
API_KEY = "AQ.Ab8RN6JcH70E2cEr-L60PWQCtjiXW0AVNuNYvO8hmJ7Vnaux9A"  # paste your Google AI Studio key between the quotes
MODEL = "models/gemma-4-26b-a4b-it"

st.set_page_config(page_title="Neighbourhood Green Plan", page_icon="🌳", layout="centered")

# ---------- Styling ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&family=Hind:wght@400;500;600&display=swap');

:root {
  --leaf: #1f5e3b;
  --moss: #3f8a56;
  --mint: #e4f1e6;
  --chalk: #fbfdfb;
  --marigold: #f2a900;
  --soil: #4a3426;
}

html, body, [class*="css"], .stApp { font-family: 'Hind', sans-serif; }
.stApp { background: var(--chalk); color: #1c2a20; }
.block-container { padding-top: 1.5rem; max-width: 780px; }

.hero {
  background: linear-gradient(135deg, var(--leaf) 0%, var(--moss) 100%);
  border-radius: 22px;
  padding: 2rem 1.8rem;
  color: #fff;
  margin-bottom: 1.4rem;
  border-bottom: 6px solid var(--marigold);
}
.hero h1 {
  font-family: 'Baloo 2', sans-serif;
  font-weight: 800;
  font-size: 2.4rem;
  margin: 0 0 .3rem 0;
  color: #fff;
  line-height: 1.1;
}
.hero p { margin: 0; font-size: 1.05rem; opacity: .95; }

.chips { margin-top: .9rem; }
.chip {
  display: inline-block;
  background: rgba(255,255,255,.18);
  border: 1px solid rgba(255,255,255,.35);
  padding: .15rem .7rem;
  border-radius: 999px;
  font-size: .85rem;
  margin-right: .4rem;
}

.stButton > button {
  background: var(--marigold);
  color: var(--soil);
  font-family: 'Baloo 2', sans-serif;
  font-weight: 600;
  font-size: 1.15rem;
  border: none;
  border-radius: 14px;
  padding: .6rem 1.4rem;
  width: 100%;
}
.stButton > button:hover { background: #ffbc1f; color: var(--soil); }
.stButton > button:focus-visible { outline: 3px solid var(--leaf); }

.stDownloadButton > button {
  border-radius: 12px;
  border: 2px solid var(--leaf);
  color: var(--leaf);
  font-weight: 600;
}

.stTabs [data-baseweb="tab-list"] { gap: .3rem; flex-wrap: wrap; }
.stTabs [data-baseweb="tab"] {
  background: var(--mint);
  border-radius: 10px 10px 0 0;
  padding: .4rem .9rem;
  font-weight: 500;
}
.stTabs [aria-selected="true"] { background: var(--leaf); color: #fff; }

.footer { text-align: center; color: #6b7d70; font-size: .85rem; margin-top: 2rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Hero ----------
st.markdown(
    """
<div class="hero">
  <h1>🌳 Neighbourhood Green Plan</h1>
  <p>A complete cleanup and tree-planting plan for your neighbourhood, in one click.</p>
  <div class="chips">
    <span class="chip">Open-weight Gemma</span>
    <span class="chip">Native trees</span>
    <span class="chip">WhatsApp invite</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- Form ----------
with st.container(border=True):
    area = st.text_input("📍 Your area / neighbourhood", "My street, Uttar Pradesh")
    c1, c2 = st.columns(2)
    with c1:
        people = st.slider("👥 How many volunteers?", 2, 50, 8)
    with c2:
        date = st.date_input("📅 When?")
    space = st.radio(
        "🌱 Type of space",
        ["Street side", "Park", "Outside a school", "Empty plot"],
        horizontal=True,
    )

go = st.button("🌿 Create plan")

# ---------- Generate ----------
SECTIONS = [
    ("TREES", "🌳 Trees"),
    ("PLAN", "📋 Plan"),
    ("ROLES", "👥 Roles"),
    ("SUPPLIES", "🧰 Supplies"),
    ("WHATSAPP", "💬 WhatsApp"),
]


def build_prompt():
    return f"""You are a neighbourhood cleanup and tree-planting organizer.
Area: {area} (India). Date: {date}. Volunteers: {people}. Space: {space}.
Answer in simple, friendly English. Split your answer into exactly these 5 sections.
Start each section with its marker on its own line (add nothing else on that line):
[[TREES]] 4-5 native trees/plants suited to this season and area (like neem, jamun, amla, tulsi) and why
[[PLAN]] a step-by-step cleanup + planting plan, with timings
[[ROLES]] how to divide the work among {people} volunteers
[[SUPPLIES]] a checklist of supplies
[[WHATSAPP]] a short, friendly invite message for the neighbourhood WhatsApp group
Keep it short and practical."""


def parse(text):
    parts = {}
    pattern = r"\[\[(TREES|PLAN|ROLES|SUPPLIES|WHATSAPP)\]\]"
    pieces = re.split(pattern, text)
    for i in range(1, len(pieces) - 1, 2):
        parts[pieces[i]] = pieces[i + 1].strip()
    return parts


if go:
    if not API_KEY.strip():
        st.warning("Paste your API key in the API_KEY line at the top of app.py.")
    else:
        try:
            client = genai.Client(api_key=API_KEY)
            with st.spinner("Creating your plan..."):
                out = client.models.generate_content(model=MODEL, contents=build_prompt())
            st.session_state["result"] = out.text
        except Exception as e:
            st.error(f"Something went wrong: {e}")

if "result" in st.session_state:
    text = st.session_state["result"]
    parts = parse(text)

    st.success("Your plan is ready! 🎉")

    if len(parts) >= 3:
        tabs = st.tabs([label for _, label in SECTIONS])
        for tab, (key, _) in zip(tabs, SECTIONS):
            with tab:
                body = parts.get(key, "This section is missing. Try creating the plan again.")
                if key == "WHATSAPP":
                    st.caption("Copy this and send it to your group 👇")
                    st.code(body, language=None)
                else:
                    st.markdown(body)
        full = "\n\n".join(f"## {label}\n{parts.get(k, '')}" for k, label in SECTIONS)
    else:
        st.markdown(text)
        full = text

    st.download_button("⬇️ Download the full plan", full, file_name="Neighbourhood_Green_Plan.md")

st.markdown(
    '<div class="footer">Built with open-weight Gemma · Hacktoberfest 2026 Touch Grass</div>',
    unsafe_allow_html=True,
)