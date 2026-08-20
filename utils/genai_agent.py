import os

import streamlit as st
from google import genai


class BankingL1Agent:

    def __init__(self):

        # ==========================================
        # GET GEMINI API KEY
        # ==========================================

        api_key = None

        # Streamlit Cloud
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            pass

        # Local .env / environment variable
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")

        # ==========================================
        # VALIDATE
        # ==========================================

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Please add GEMINI_API_KEY to "
                "Streamlit Cloud Secrets."
            )

        # ==========================================
        # GEMINI CLIENT
        # ==========================================

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-3.1-flash-lite"


    # ==============================================
    # SYSTEM INSTRUCTION
    # ==============================================

    def get_system_instruction(self):

        return """
You are a Banking L1 Support Agent.

You assist L1 support teams with banking-related
customer issues.

IMPORTANT RULES:

1. Use the approved SOP provided to you.
2. Do not invent troubleshooting steps.
3. Do not provide procedures that are not in the SOP.
4. Follow the SOP troubleshooting sequence.
5. If the SOP does not cover the issue, recommend
   L2 escalation.
6. Never request OTP, PIN, UPI PIN, CVV, password,
   or full card number.
7. Never repeat sensitive information provided by
   the user.

For troubleshooting responses use:

Issue Identified:
...

Steps to Resolve:

1. ...
2. ...
3. ...

Escalation:
Yes / No

Reason:
...

Security Reminder:
...

Be concise and professional.
"""


    # ==============================================
    # SOP CONTEXT
    # ==============================================

    def build_sop_context(self, sop_document):

        return f"""
==================================================
APPROVED BANKING SOP
==================================================

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

--------------------------------------------------
SOP CONTENT
--------------------------------------------------

{sop_document["content"]}

==================================================
END SOP
==================================================
"""


    # ==============================================
    # CHAT
    # ==============================================

    def chat(
        self,
        messages,
        sop_document
    ):

        sop_context = self.build_sop_context(
            sop_document
        )

        system_instruction = (
            self.get_system_instruction()
            + "\n\n"
            + sop_context
        )

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

        prompt = f"""
{system_instruction}

==================================================
CONVERSATION
==================================================

{conversation_text}

==================================================
TASK
==================================================

Respond to the latest user message.

Use ONLY the approved SOP.

Do not invent procedures.
Do not ask for sensitive banking credentials.
Follow the SOP escalation process.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text