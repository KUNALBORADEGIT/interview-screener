import pdfplumber
import docx
import json
import re
from engine.services.llm_client import LLMClient


class ResumeParser:
    def __init__(self):
        self.llm = LLMClient()

    def extract_text(self, file_path: str) -> str:
        ext = file_path.split(".")[-1].lower()
        if ext == "pdf":
            return self._extract_pdf(file_path)
        elif ext == "docx":
            return self._extract_docx(file_path)
        else:
            return ""

    def _extract_pdf(self, file_path: str) -> str:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
        return text

    def _extract_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

    def _normalize_phone(self, phone: str, default_country="+91") -> str:
        """Normalize phone number to E.164 format."""
        if not phone:
            return ""
        phone = re.sub(r"[^\d+]", "", phone)  # remove spaces, -, ()
        if phone.startswith("+") and re.match(r"^\+[1-9]\d{1,14}$", phone):
            return phone
        elif re.match(r"^\d{10}$", phone):  # assume local number
            return default_country + phone
        return phone  # fallback

    async def parse(self, file_path: str) -> dict:
        resume_text = self.extract_text(file_path)

        prompt = f"""
        You are a resume parser. Extract the following fields strictly in **valid JSON** only:

        {{
          "name": "string",
          "email": "string",
          "phone": "string"
        }}

        Resume Text:
        {resume_text}
        """

        response = await self.llm.ask(prompt)

        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Invalid LLM response", "raw": response}

        # Normalize phone
        if "phone" in parsed:
            parsed["phone"] = self._normalize_phone(parsed.get("phone", ""))

        return parsed
