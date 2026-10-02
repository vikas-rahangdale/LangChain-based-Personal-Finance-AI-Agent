import streamlit as st
from dotenv import load_dotenv
from agent import create_personal_agent

load_dotenv()

st.set_page_config(
    page_title="Personal Finance Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
        .stApp { background: #f5f7fb; }
        [data-testid="stHeader"] { background: rgba(245,247,251,0.9); }
        .block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem; }
        .hero {
            padding: 2rem 2.2rem; border-radius: 20px; color: white;
            background: linear-gradient(120deg, #102a43 0%, #176b67 100%);
            box-shadow: 0 12px 30px rgba(16,42,67,.15); margin-bottom: 1.4rem;
        }
        .hero-kicker { color: #a8e6d6; font-size: .78rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
        .hero h1 { color: white; font-size: 2.15rem; margin: .35rem 0 .4rem; }
        .hero p { color: #e0f2ef; margin: 0; font-size: 1.02rem; }
        .section-label { color: #183b56; font-weight: 700; font-size: 1.05rem; margin: .7rem 0 .35rem; }
        .hint { color: #66788a; font-size: .9rem; margin: 0 0 1rem; }
        div[data-testid="stForm"] {
            background: white; border: 1px solid #e4eaf0; padding: 1.1rem 1.25rem;
            border-radius: 16px; box-shadow: 0 5px 18px rgba(16,42,67,.05);
        }
        .stButton > button, div[data-testid="stFormSubmitButton"] button {
            border-radius: 10px; border: 0; font-weight: 600; min-height: 2.7rem;
            background: #176b67; color: white;
        }
        .stButton > button:hover, div[data-testid="stFormSubmitButton"] button:hover {
            background: #125653; color: white; border: 0;
        }
        [data-testid="stSidebar"] { background: #fff; border-right: 1px solid #e7edf2; }
        .response-title { color: #183b56; font-weight: 700; font-size: 1.2rem; margin: 1.5rem 0 .7rem; }
        .disclaimer { color: #6b7785; font-size: .8rem; line-height: 1.5; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 💼 Finance Desk")
    st.caption("Your personal planning workspace")
    st.divider()
    st.markdown("### What I can help with")
    st.markdown("- Loan EMI and repayment estimates\n- SIP and investment projections\n- Monthly budgets and savings goals\n- Everyday financial calculations")
    st.divider()
    st.markdown("### A quick note")
    st.markdown(
        '<p class="disclaimer">Responses are for educational purposes and are not a substitute for personalized advice from a qualified financial professional. Verify assumptions before making financial decisions.</p>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="hero"><div class="hero-kicker">Personal finance, made clearer</div>'
    '<h1>Your financial planning assistant</h1>'
    '<p>Explore scenarios, understand your numbers, and plan your next step with confidence.</p></div>',
    unsafe_allow_html=True,
)

agent = create_personal_agent()

def display_structured_response(result):
    st.markdown('<div class="response-title">Your analysis</div>', unsafe_allow_html=True)
    structured_output = result.get("structured_response")

    if structured_output is not None:
        if isinstance(structured_output, (dict, list)):
            st.json(structured_output)
        else:
            st.write(structured_output)
        return

    messages = result.get("messages", [])
    assistant_message = next(
        (message for message in reversed(messages)
         if getattr(message, "type", None) == "ai"),
        None,
    )
    st.write(assistant_message.content if assistant_message is not None else result)


def ask_agent(prompt):
    with st.spinner("Reviewing your numbers..."):
        try:
            result = agent.invoke({"messages": [("user", prompt)]})
            display_structured_response(result)
        except Exception as error:
            st.error("The assistant couldn't complete that request. Please try again.")
            st.caption(str(error))


st.markdown('<div class="section-label">What would you like to plan?</div>', unsafe_allow_html=True)
st.markdown('<p class="hint">Share the amount, time period, and rate where relevant for a more useful estimate.</p>', unsafe_allow_html=True)
with st.form("finance_question", clear_on_submit=False):
    query = st.text_input(
        "Your question",
        placeholder="e.g. What would the EMI be on a ₹10 lakh loan at 8% for 20 years?",
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button("Get a financial estimate  →", use_container_width=True)

if submitted:
    if query.strip():
        ask_agent(query.strip())
    else:
        st.info("Enter a question to get started.")

st.markdown('<div class="section-label" style="margin-top:1.8rem">Explore an example</div>', unsafe_allow_html=True)
st.markdown('<p class="hint">Choose a scenario to see how the assistant can help.</p>', unsafe_allow_html=True)
examples = [
    ("🏠  Loan EMI", "Calculate EMI for ₹10 lakh loan at 8% interest for 20 years"),
    ("📈  SIP growth", "If I invest ₹7000 monthly for 15 years at 10% return"),
    ("🧾  Monthly budget", "Create a budget plan for income ₹90,000"),
    ("％  Quick calculation", "What is 20% of ₹85,000"),
]
columns = st.columns(4)
for column, (label, prompt) in zip(columns, examples):
    with column:
        if st.button(label, use_container_width=True):
            ask_agent(prompt)