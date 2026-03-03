from crewai.tools import BaseTool
from typing import Type, ClassVar
from pydantic import BaseModel, Field
import requests
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class PractoTool(BaseTool):
    name: str = "Practo_Health_Consultation"
    description: str = (
        "A medical consultation tool that can book appointments with doctors, "
        "search for specialists, and provide healthcare services. Use this when "
        "there are severe health concerns that require professional medical attention."
    )
    
    def _run(self) -> str:
        patient_info = {
            "patientName": "John Doe",
            "age": 50
        }
        response = requests.post("https://practotool.onrender.com/appointment", json=patient_info)
        return f"Practo consultation booked. A doctor will contact you shortly."


class EmailTool(BaseTool):
    name: str = "Email_Notification"
    description: str = "Send a confirmation email to the patient using SendGrid."

    def _run(self) -> str:
        from_email = os.environ["SENDGRID_FROM_EMAIL"]
        to_email = os.environ["SENDGRID_TO_DEFAULT"]

        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject="Your medical consultation has been booked",
            plain_text_content="This is a confirmation that your consultation has been scheduled.",
        )

        client = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
        response = client.send(message)
        return f"SendGrid email status: {response.status_code}"


class AskUserTool(BaseTool):
    # Instance-level counters so each tool instance has its own prompt budget
    prompt_count: int = 0
    max_prompts: int = 2  # 1 for main concern + 1 clarifying
    name: str = "AskUser"
    description: str = (
        "Interactively ask the human user a clarifying question via the console and return their answer. "
        "Use this to gather more details about symptoms, duration, medications, or any other missing context. "
        "This tool will ask a limited number of questions to avoid loops."
    )

    def _run(self, prompt: str | None = None, **kwargs) -> str:
        default_question = prompt or "Please describe your main health concern (symptoms and duration)."
        # Allow up to max_prompts prompts for this tool instance
        if self.prompt_count >= self.max_prompts:
            return "No further user input available. Proceeding with current information."

        try:
            answer = input(f"[Inquiry] {default_question}\n> ")
        except EOFError:
            # Non-interactive environment fallback
            answer = ""

        # Count this prompt to enforce the maximum prompts per instance
        self.prompt_count += 1
        return answer
