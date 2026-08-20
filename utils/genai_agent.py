import os

import streamlit as st

from google import genai


# ============================================================
# BANKING L1 GENAI AGENT
# ============================================================

class BankingL1Agent:

    def __init__(self):

        # ====================================================
        # GET GEMINI API KEY
        # ====================================================

        api_key = None


        # ----------------------------------------------------
        # STREAMLIT CLOUD
        # ----------------------------------------------------

        try:

            api_key = st.secrets.get(
                "GEMINI_API_KEY"
            )

        except Exception:

            api_key = None


        # ----------------------------------------------------
        # LOCAL ENVIRONMENT
        # ----------------------------------------------------

        if not api_key:

            api_key = os.getenv(
                "GEMINI_API_KEY"
            )


        # ====================================================
        # VALIDATE API KEY
        # ====================================================

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY not found.\n\n"
                "For Streamlit Cloud:\n"
                "Go to App Settings → Secrets and add:\n\n"
                'GEMINI_API_KEY = "YOUR_API_KEY"'
            )


        # ====================================================
        # GEMINI CLIENT
        # ====================================================

        self.client = genai.Client(
            api_key=api_key
        )


        # ====================================================
        # MODEL
        # ====================================================

        self.model = "gemini-3.1-flash-lite"


    # ========================================================
    # SYSTEM INSTRUCTIONS
    # ========================================================

    def get_system_instruction(self):

        return """

You are a Banking L1 Support Agent.

You assist L1 banking support staff with
customer banking issues.

============================================================
PRIMARY RULE
============================================================

You MUST use the approved SOP provided to you.

The SOP is the authoritative source.

Do NOT invent troubleshooting procedures.

Do NOT create banking procedures that are not
present in the SOP.

============================================================
SOP BEHAVIOR
============================================================

Follow the troubleshooting sequence defined in
the SOP.

If the SOP provides steps:

1. Follow Step 1.
2. Follow Step 2.
3. Follow Step 3.

Do not skip mandatory steps.

If the SOP says to escalate, escalate.

Do not attempt to bypass an escalation requirement.

============================================================
SECURITY
============================================================

NEVER ask the customer for:

- OTP
- Password
- PIN
- UPI PIN
- CVV
- Full card number
- Banking credentials

If a user provides sensitive information:

- Do not repeat it.
- Do not store it in your response.
- Tell the user not to share sensitive credentials.

============================================================
L2 ESCALATION
============================================================

If the SOP requires escalation, clearly state:

"This issue requires escalation to L2 support."

Do not attempt to solve an issue that the SOP
requires L2 to handle.

============================================================
RESPONSE FORMAT
============================================================

For troubleshooting requests:

Issue Identified:
<issue>

Steps to Resolve:

1. <step>
2. <step>
3. <step>

Escalation:
Yes / No

Reason:
<reason>

Security Reminder:
<security reminder>

============================================================
CONVERSATIONAL BEHAVIOR
============================================================

The user may ask follow-up questions.

Remember the conversation history.

Use the selected SOP throughout the conversation.

If the user asks something outside the SOP:

Explain that the current approved SOP does not
cover that request and recommend L2 support if
appropriate.

Be concise, professional and helpful.

"""


    # ========================================================
    # BUILD SOP CONTEXT
    # ========================================================

    def build_sop_context(
        self,
        sop_document
    ):

        return f"""

============================================================
APPROVED BANKING SOP
============================================================

SOP ID:
{sop_document["document_id"]}

Title:
{sop_document["title"]}

Category:
{sop_document["category"]}

Issue:
{sop_document["issue"]}

Support Level:
{sop_document["support_level"]}

Version:
{sop_document["version"]}

------------------------------------------------------------
SOP CONTENT
------------------------------------------------------------

{sop_document["content"]}

============================================================
END OF APPROVED SOP
============================================================

"""


    # ========================================================
    # CHAT
    # ========================================================

    def chat(
        self,
        messages,
        sop_document
    ):

        # ----------------------------------------------------
        # SOP
        # ----------------------------------------------------

        sop_context = self.build_sop_context(
            sop_document
        )


        # ----------------------------------------------------
        # SYSTEM INSTRUCTION
        # ----------------------------------------------------

        system_instruction = (
            self.get_system_instruction()
            + "\n"
            + sop_context
        )


        # ----------------------------------------------------
        # CONVERSATION
        # ----------------------------------------------------

        conversation = []


        for message in messages:

            role = message["role"]

            content = message["content"]


            if role == "user":

                conversation.append(
                    f"USER:\n{content}"
                )


            elif role == "assistant":

                conversation.append(
                    f"ASSISTANT:\n{content}"
                )


        conversation_text = "\n\n".join(
            conversation
        )


        # ----------------------------------------------------
        # FINAL PROMPT
        # ----------------------------------------------------

        prompt = f"""

{system_instruction}

============================================================
CONVERSATION HISTORY
============================================================

{conversation_text}

============================================================
CURRENT TASK
============================================================

Respond to the user's latest message.

Remember:

- Use ONLY the approved SOP.
- Do not invent procedures.
- Protect sensitive banking information.
- Follow SOP escalation rules.
- Never request OTP, PIN, password, CVV,
  UPI PIN or full card number.

"""


        # ====================================================
        # CALL GEMINI
        # ====================================================

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )


        # ====================================================
        # RETURN RESPONSE
        # ====================================================

        return response.text