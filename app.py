import streamlit as st

from utils.sop_retriever import SOPRetriever
from utils.genai_agent import BankingL1Agent


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Banking L1 GenAI Agent",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==================================================
# RESPONSIVE CSS
# ==================================================

st.markdown(
    """
    <style>

    /* ------------------------------------------
       GENERAL
    ------------------------------------------ */

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }


    /* ------------------------------------------
       BUTTONS
    ------------------------------------------ */

    .stButton > button {
        width: 100%;
        min-height: 44px;
        border-radius: 10px;
        font-size: 15px;
    }


    /* ------------------------------------------
       INPUT
    ------------------------------------------ */

    .stChatInput textarea {
        font-size: 16px !important;
    }


    /* ------------------------------------------
       MOBILE
    ------------------------------------------ */

    @media only screen and (max-width: 768px) {

        .block-container {
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            padding-top: 0.5rem;
        }


        h1 {
            font-size: 1.6rem !important;
        }


        h2 {
            font-size: 1.3rem !important;
        }


        h3 {
            font-size: 1.1rem !important;
        }


        p {
            font-size: 15px;
        }


        .stButton > button {
            min-height: 48px;
            font-size: 16px;
        }


        /* Chat messages */

        [data-testid="stChatMessage"] {
            padding: 0.5rem 0.2rem;
        }


        /* Expanders */

        [data-testid="stExpander"] {
            border-radius: 10px;
        }


        /* Select boxes */

        [data-testid="stSelectbox"] {
            margin-bottom: 0.5rem;
        }


        /* Chat input */

        [data-testid="stChatInput"] {
            padding-bottom: 0.5rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# LOAD SERVICES
# ==================================================

@st.cache_resource
def load_retriever():

    return SOPRetriever("sops")


@st.cache_resource
def load_agent():

    return BankingL1Agent()


retriever = load_retriever()
agent = load_agent()


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "selected_sop" not in st.session_state:

    st.session_state.selected_sop = None


if "search_results" not in st.session_state:

    st.session_state.search_results = []


# ==================================================
# HEADER
# ==================================================

st.title("🏦 Banking L1 Support")

st.caption(
    "SOP-grounded GenAI support assistant"
)


# ==================================================
# MOBILE / DESKTOP ISSUE SELECTOR
# ==================================================

with st.expander(
    "📂 Select Banking Issue",
    expanded=not bool(
        st.session_state.selected_sop
    )
):

    categories = retriever.get_categories()


    category = st.selectbox(
        "Category",
        ["Select"] + categories
    )


    issue = "Select"


    if category != "Select":

        issues = retriever.get_issues(
            category
        )

        issue = st.selectbox(
            "Issue",
            ["Select"] + issues
        )


    if (
        category != "Select"
        and issue != "Select"
    ):

        if st.button(
            "🔎 Load SOP",
            use_container_width=True
        ):

            results = retriever.get_by_issue(
                category,
                issue
            )


            if results:

                st.session_state.selected_sop = (
                    results[0]
                )

                st.session_state.messages = []

                st.session_state.search_results = []

                st.rerun()

            else:

                st.error(
                    "No approved SOP found."
                )


# ==================================================
# ACTIVE SOP
# ==================================================

if st.session_state.selected_sop:

    sop = st.session_state.selected_sop


    st.success(
        f"📄 {sop['document_id']} — "
        f"{sop['title']}"
    )


    # ----------------------------------------------
    # VIEW SOP
    # ----------------------------------------------

    with st.expander(
        "📖 View SOP Document"
    ):

        st.markdown(
            f"**SOP ID:** {sop['document_id']}"
        )

        st.markdown(
            f"**Category:** {sop['category']}"
        )

        st.markdown(
            f"**Issue:** {sop['issue']}"
        )

        st.markdown(
            f"**Support Level:** "
            f"{sop['support_level']}"
        )

        st.markdown(
            f"**Version:** {sop['version']}"
        )

        st.divider()

        st.markdown(
            sop["content"]
        )


# ==================================================
# CHAT HEADER
# ==================================================

st.subheader("💬 L1 Support Chat")


# ==================================================
# CHAT HISTORY
# ==================================================

if not st.session_state.messages:

    st.info(
        "👋 Select a banking issue and start "
        "your conversation."
    )


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==================================================
# CHAT INPUT
# ==================================================

user_input = st.chat_input(
    "Describe the customer's issue..."
)


if user_input:

    # ----------------------------------------------
    # AUTOMATIC SOP RETRIEVAL
    # ----------------------------------------------

    if not st.session_state.selected_sop:

        results = retriever.search(
            user_input,
            top_k=1
        )


        if results:

            st.session_state.selected_sop = (
                results[0]
            )

        else:

            st.error(
                "No approved SOP was found for this "
                "issue. Please select an issue or "
                "escalate to L2."
            )

            st.stop()


    # ----------------------------------------------
    # USER MESSAGE
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    with st.chat_message("user"):

        st.markdown(user_input)


    # ----------------------------------------------
    # AI RESPONSE
    # ----------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Checking SOP..."
        ):

            try:

                response = agent.chat(
                    messages=
                    st.session_state.messages,

                    sop_document=
                    st.session_state.selected_sop
                )


                st.markdown(response)


            except Exception as e:

                response = (
                    "I encountered an error while "
                    "processing your request."
                )


                st.error(
                    str(e)
                )


    # ----------------------------------------------
    # SAVE RESPONSE
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# ==================================================
# MOBILE SEARCH
# ==================================================

with st.expander(
    "🔎 Search Other SOP"
):

    search_query = st.text_input(
        "Describe the issue"
    )


    if st.button(
        "Search Knowledge Base",
        use_container_width=True
    ):

        if search_query.strip():

            st.session_state.search_results = (
                retriever.search(
                    search_query,
                    top_k=3
                )
            )


    if st.session_state.search_results:

        st.markdown(
            "### Matching SOPs"
        )


        for result in st.session_state.search_results:

            if st.button(
                f"{result['document_id']} — "
                f"{result['title']}",
                key=f"mobile_{result['document_id']}"
            ):

                st.session_state.selected_sop = result

                st.session_state.messages = []

                st.session_state.search_results = []

                st.rerun()


# ==================================================
# CONTROLS
# ==================================================

with st.expander(
    "⚙️ Chat Controls"
):

    if st.button(
        "🧹 Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    if st.button(
        "🔄 Reset Agent",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.selected_sop = None

        st.session_state.search_results = []

        st.rerun()


# ==================================================
# SECURITY
# ==================================================

st.divider()

st.warning(
    "🔐 Never share OTP, PIN, UPI PIN, password, "
    "CVV, or full card details."
)


st.caption(
    "Banking L1 GenAI Agent • SOP-grounded responses"
)