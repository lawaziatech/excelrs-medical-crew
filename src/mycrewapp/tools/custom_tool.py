from crewai.tools import BaseTool
from typing import Type, ClassVar
from pydantic import BaseModel, Field


class PractoTool(BaseTool):
    name: str = "Practo_Health_Consultation"
    description: str = (
        "A medical consultation tool that can book appointments with doctors, "
        "search for specialists, and provide healthcare services. Use this when "
        "there are severe health concerns that require professional medical attention."
    )
    
    def _run(self) -> str:
        default_note = "Severe case detected. Booking a medical consultation based on inquiry summary."
        # API URL and key would be configured here
        # make http call to Practo API
        return f"Practo consultation booked. A doctor will contact you shortly."


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
