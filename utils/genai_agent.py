import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# LOAD ENVIRONMENT
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# --------------------------------------------------
# BANKING L1 AGENT
# --------------------------------------------------

class BankingL1Agent:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:

            raise ValueError(
                f"GEMINI_API_KEY not found.\n"
                f"Expected .env file at: {ENV_FILE}"
            )

        self.client = genai.Client(
            api_key=api_key
        )

        # Use the Gemini model available to your API account.
        self.model = "gemini-3.1-flash-lite"


    # --------------------------------------------------
    # SYSTEM INSTRUCTIONS
    # --------------------------------------------------

    def get_system_instruction(self):

        return """
You are a Banking L1 Support Agent.

You assist customers and L1 support agents with
banking-related problems.

==================================================
STRICT SOP RULES
==================================================

1. You MUST use the provided approved SOP as the
   primary and authoritative source.

2. Do NOT invent troubleshooting steps.

3. Do NOT provide banking procedures that are not
   contained in the approved SOP.

4. Follow the SOP's troubleshooting sequence.

5. If the user asks a question unrelated to the
   provided SOP, explain that the current SOP does
   not cover the request.

6. If there is insufficient information in the SOP,
   recommend L2 escalation.

==================================================
SECURITY RULES
==================================================

NEVER request or ask the customer to provide:

- OTP
- Password
- PIN
- UPI PIN
- CVV
- Full card number
- Banking credentials

If the customer voluntarily provides sensitive
information, do not repeat it back.

Tell the customer not to share sensitive
authentication information.

==================================================
ESCALATION
==================================================

If the SOP says the issue requires escalation,
clearly tell the user:

"This issue requires escalation to L2 support."

Do not attempt to bypass an escalation requirement.

==================================================
RESPONSE STYLE
==================================================

Be concise, professional and helpful.

For troubleshooting requests, use:

Issue Identified:
...

Steps to Resolve:

1. ...
2. ...
3. ...

Escalation:
Yes/No

Reason:
...

Security Reminder:
...

For normal conversational questions, respond
naturally while staying within the SOP context.
"""


    # --------------------------------------------------
    # BUILD SOP CONTEXT
    # --------------------------------------------------

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
END OF APPROVED SOP
==================================================
"""


    # --------------------------------------------------
    # CHAT
    # --------------------------------------------------

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


        # ----------------------------------------------
        # Build conversation
        # ----------------------------------------------

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


        # ----------------------------------------------
        # Final prompt
        # ----------------------------------------------

        prompt = f"""
{system_instruction}

==================================================
CONVERSATION HISTORY
==================================================

{conversation_text}

==================================================
INSTRUCTION
==================================================

Respond to the user's latest message.

Remember:

- Use only the approved SOP.
- Do not invent procedures.
- Protect sensitive information.
- Follow escalation rules.
"""


        # ----------------------------------------------
        # Gemini
        # ----------------------------------------------

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )


        return response.text