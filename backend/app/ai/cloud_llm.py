import os
import httpx
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class CloudLLMHub:
    """
    Multi-Provider Cloud LLM Gateway for APEX:
    - Gemini 3.6 Flash (Primary high-speed reasoning, explanations & vision)
    - Grok xAI (Socratic deep counter-arguments & edge cases)
    - Automatic resilient failover
    """
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        self.gemini_timeout = float(os.getenv("GEMINI_TIMEOUT_SECONDS", "10.0"))

        self.grok_key = os.getenv("GROK_API_KEY")
        self.grok_model = os.getenv("GROK_MODEL", "grok-beta")
        self.grok_timeout = 10.0

    async def generate_gemini(self, prompt: str, system_instruction: str = "") -> Optional[str]:
        """Calls Google Gemini REST API."""
        if not self.gemini_key:
            return None
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent?key={self.gemini_key}"
        
        contents = []
        if system_instruction:
            contents.append({"role": "user", "parts": [{"text": f"[System Context: {system_instruction}]"}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})
        
        payload = {"contents": contents}
        headers = {"Content-Type": "application/json"}
        
        try:
            async with httpx.AsyncClient(timeout=self.gemini_timeout) as client:
                resp = await client.post(url, json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts and "text" in parts[0]:
                            return parts[0]["text"].strip()
        except Exception:
            pass
        return None

    async def generate_grok(self, prompt: str, system_instruction: str = "") -> Optional[str]:
        """Calls xAI Grok API."""
        if not self.grok_key:
            return None
        url = "https://api.x.ai/v1/chat/completions"
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.grok_model,
            "messages": messages,
            "stream": False
        }
        headers = {
            "Authorization": f"Bearer {self.grok_key}",
            "Content-Type": "application/json"
        }
        try:
            async with httpx.AsyncClient(timeout=self.grok_timeout) as client:
                resp = await client.post(url, json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"].strip()
        except Exception:
            pass
        return None

    async def generate_best(
        self,
        prompt: str,
        system_instruction: str = "",
        preferred_provider: str = "gemini"
    ) -> Dict[str, Any]:
        """
        Attempts generation using preferred provider, failing over gracefully.
        """
        if preferred_provider == "gemini":
            ans = await self.generate_gemini(prompt, system_instruction)
            if ans:
                return {"text": ans, "source": f"CLOUD_{self.gemini_model.upper()}"}
            # Fallback to grok
            ans_grok = await self.generate_grok(prompt, system_instruction)
            if ans_grok:
                return {"text": ans_grok, "source": f"CLOUD_{self.grok_model.upper()}"}
        else:
            ans = await self.generate_grok(prompt, system_instruction)
            if ans:
                return {"text": ans, "source": f"CLOUD_{self.grok_model.upper()}"}
            ans_gem = await self.generate_gemini(prompt, system_instruction)
            if ans_gem:
                return {"text": ans_gem, "source": f"CLOUD_{self.gemini_model.upper()}"}

        return {"text": "", "source": "NONE"}
