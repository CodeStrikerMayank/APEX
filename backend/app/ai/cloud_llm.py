import os
import time
import httpx
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class CloudLLMHub:
    """
    Multi-Provider Cloud LLM Gateway for APEX:
    - Gemini Flash API (Primary high-speed reasoning, explanations & vision)
    - Grok xAI API (Socratic deep counter-arguments & edge cases)
    - Custom Providers (OpenRouter, OpenAI Compatible, Local Ollama custom endpoint)
    - Dynamic Runtime BYOK (Bring Your Own Key) & Hot-Swapping via Ctrl+O+P
    - Fast circuit breaker for key exhaustion (401, 403, 429) to avoid latency on low-end hardware
    """
    _gemini_exhausted_until: float = 0.0
    _grok_exhausted_until: float = 0.0
    _custom_exhausted_until: float = 0.0

    # Runtime key overrides (can be updated without restarting server)
    _runtime_gemini_key: Optional[str] = None
    _runtime_grok_key: Optional[str] = None
    _runtime_custom_provider: Optional[str] = None
    _runtime_custom_api_key: Optional[str] = None
    _runtime_custom_base_url: Optional[str] = None
    _runtime_custom_model: Optional[str] = None

    def __init__(self):
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        self.gemini_timeout = float(os.getenv("GEMINI_TIMEOUT_SECONDS", "3.5"))

        self.grok_model = os.getenv("GROK_MODEL", "grok-2-latest")
        self.grok_timeout = float(os.getenv("GROK_TIMEOUT_SECONDS", "3.5"))

        self.custom_timeout = 4.0

    @property
    def gemini_key(self) -> Optional[str]:
        if CloudLLMHub._runtime_gemini_key is not None:
            return CloudLLMHub._runtime_gemini_key
        return os.getenv("GEMINI_API_KEY")

    @property
    def grok_key(self) -> Optional[str]:
        if CloudLLMHub._runtime_grok_key is not None:
            return CloudLLMHub._runtime_grok_key
        return os.getenv("GROK_API_KEY")

    @property
    def custom_provider(self) -> str:
        return CloudLLMHub._runtime_custom_provider or os.getenv("CUSTOM_AI_PROVIDER", "None")

    @property
    def custom_api_key(self) -> Optional[str]:
        return CloudLLMHub._runtime_custom_api_key or os.getenv("CUSTOM_API_KEY")

    @property
    def custom_base_url(self) -> Optional[str]:
        return CloudLLMHub._runtime_custom_base_url or os.getenv("CUSTOM_AI_BASE_URL")

    @property
    def custom_model(self) -> Optional[str]:
        return CloudLLMHub._runtime_custom_model or os.getenv("CUSTOM_AI_MODEL", "deepseek/deepseek-r1")

    def is_gemini_available(self) -> bool:
        return bool(self.gemini_key) and time.time() > CloudLLMHub._gemini_exhausted_until

    def is_grok_available(self) -> bool:
        return bool(self.grok_key) and time.time() > CloudLLMHub._grok_exhausted_until

    def is_custom_available(self) -> bool:
        return bool(self.custom_api_key) and bool(self.custom_base_url) and time.time() > CloudLLMHub._custom_exhausted_until

    def mark_gemini_exhausted(self, duration_seconds: float = 600.0):
        CloudLLMHub._gemini_exhausted_until = time.time() + duration_seconds

    def mark_grok_exhausted(self, duration_seconds: float = 600.0):
        CloudLLMHub._grok_exhausted_until = time.time() + duration_seconds

    def mark_custom_exhausted(self, duration_seconds: float = 600.0):
        CloudLLMHub._custom_exhausted_until = time.time() + duration_seconds

    @classmethod
    def update_keys(
        cls,
        gemini_key: Optional[str] = None,
        grok_key: Optional[str] = None,
        custom_provider: Optional[str] = None,
        custom_api_key: Optional[str] = None,
        custom_base_url: Optional[str] = None,
        custom_model: Optional[str] = None,
        persist_to_env: bool = False
    ) -> Dict[str, Any]:
        """
        Dynamically updates active keys, resets circuit breakers, and optionally updates .env file.
        """
        changes = []
        if gemini_key is not None:
            clean_gemini = gemini_key.strip()
            cls._runtime_gemini_key = clean_gemini if clean_gemini else None
            cls._gemini_exhausted_until = 0.0
            changes.append("Gemini Key")

        if grok_key is not None:
            clean_grok = grok_key.strip()
            cls._runtime_grok_key = clean_grok if clean_grok else None
            cls._grok_exhausted_until = 0.0
            changes.append("Grok Key")

        if custom_provider is not None:
            cls._runtime_custom_provider = custom_provider.strip() or None
        if custom_api_key is not None:
            cls._runtime_custom_api_key = custom_api_key.strip() or None
            cls._custom_exhausted_until = 0.0
            changes.append("Custom Provider Key")
        if custom_base_url is not None:
            cls._runtime_custom_base_url = custom_base_url.strip() or None
        if custom_model is not None:
            cls._runtime_custom_model = custom_model.strip() or None

        if persist_to_env:
            cls._persist_keys_to_env()

        return {
            "success": True,
            "updated_fields": changes,
            "gemini_active": bool(cls._runtime_gemini_key or os.getenv("GEMINI_API_KEY")),
            "grok_active": bool(cls._runtime_grok_key or os.getenv("GROK_API_KEY")),
            "custom_active": bool(cls._runtime_custom_api_key and cls._runtime_custom_base_url)
        }

    @classmethod
    def reset_to_defaults(cls):
        """Clears all runtime overrides back to server environment variables."""
        cls._runtime_gemini_key = None
        cls._runtime_grok_key = None
        cls._runtime_custom_provider = None
        cls._runtime_custom_api_key = None
        cls._runtime_custom_base_url = None
        cls._runtime_custom_model = None
        cls._gemini_exhausted_until = 0.0
        cls._grok_exhausted_until = 0.0
        cls._custom_exhausted_until = 0.0

    @classmethod
    def _mask_key(cls, key: Optional[str]) -> str:
        if not key:
            return ""
        k = key.strip()
        if len(k) <= 8:
            return "••••••••"
        return f"{k[:4]}••••••••{k[-4:]}"

    @classmethod
    def get_masked_config(cls) -> Dict[str, Any]:
        """Returns safe masked configuration for UI display."""
        active_gemini = cls._runtime_gemini_key or os.getenv("GEMINI_API_KEY", "")
        active_grok = cls._runtime_grok_key or os.getenv("GROK_API_KEY", "")
        active_custom_key = cls._runtime_custom_api_key or os.getenv("CUSTOM_API_KEY", "")

        return {
            "gemini": {
                "has_key": bool(active_gemini),
                "masked": cls._mask_key(active_gemini),
                "is_custom": cls._runtime_gemini_key is not None,
                "is_exhausted": time.time() <= cls._gemini_exhausted_until
            },
            "grok": {
                "has_key": bool(active_grok),
                "masked": cls._mask_key(active_grok),
                "is_custom": cls._runtime_grok_key is not None,
                "is_exhausted": time.time() <= cls._grok_exhausted_until
            },
            "custom": {
                "provider": cls._runtime_custom_provider or os.getenv("CUSTOM_AI_PROVIDER", "OpenRouter"),
                "has_key": bool(active_custom_key),
                "masked": cls._mask_key(active_custom_key),
                "base_url": cls._runtime_custom_base_url or os.getenv("CUSTOM_AI_BASE_URL", "https://openrouter.ai/api/v1"),
                "model": cls._runtime_custom_model or os.getenv("CUSTOM_AI_MODEL", "deepseek/deepseek-r1"),
                "is_active": bool(active_custom_key) and bool(cls._runtime_custom_base_url or os.getenv("CUSTOM_AI_BASE_URL"))
            }
        }

    @classmethod
    async def test_key(cls, provider: str, key: str, base_url: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
        """Performs a live lightweight validation request."""
        clean_key = key.strip()
        if not clean_key:
            return {"valid": False, "message": "Key cannot be empty"}

        if provider.lower() == "gemini":
            test_model = model or "gemini-2.0-flash"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{test_model}:generateContent?key={clean_key}"
            payload = {"contents": [{"role": "user", "parts": [{"text": "Ping"}]}]}
            try:
                async with httpx.AsyncClient(timeout=4.0) as client:
                    resp = await client.post(url, json=payload, headers={"Content-Type": "application/json"})
                    if resp.status_code == 200:
                        return {"valid": True, "status_code": 200, "message": "Gemini API Key Verified Successfully!"}
                    else:
                        err_text = resp.text[:120]
                        return {"valid": False, "status_code": resp.status_code, "message": f"Gemini Rejected Key (HTTP {resp.status_code}): {err_text}"}
            except Exception as e:
                return {"valid": False, "status_code": 500, "message": f"Connection error: {str(e)}"}

        elif provider.lower() == "grok":
            url = "https://api.x.ai/v1/chat/completions"
            payload = {
                "model": model or "grok-2-latest",
                "messages": [{"role": "user", "content": "Ping"}],
                "max_tokens": 2
            }
            try:
                async with httpx.AsyncClient(timeout=4.0) as client:
                    resp = await client.post(
                        url, json=payload,
                        headers={"Authorization": f"Bearer {clean_key}", "Content-Type": "application/json"}
                    )
                    if resp.status_code == 200:
                        return {"valid": True, "status_code": 200, "message": "Grok xAI Key Verified Successfully!"}
                    else:
                        err_text = resp.text[:120]
                        return {"valid": False, "status_code": resp.status_code, "message": f"Grok Rejected Key (HTTP {resp.status_code}): {err_text}"}
            except Exception as e:
                return {"valid": False, "status_code": 500, "message": f"Connection error: {str(e)}"}

        else:  # Custom / OpenRouter / OpenAI
            target_url = (base_url or "https://openrouter.ai/api/v1").rstrip("/") + "/chat/completions"
            payload = {
                "model": model or "deepseek/deepseek-r1",
                "messages": [{"role": "user", "content": "Ping"}],
                "max_tokens": 2
            }
            try:
                async with httpx.AsyncClient(timeout=4.0) as client:
                    resp = await client.post(
                        target_url, json=payload,
                        headers={"Authorization": f"Bearer {clean_key}", "Content-Type": "application/json"}
                    )
                    if resp.status_code in (200, 201):
                        return {"valid": True, "status_code": resp.status_code, "message": f"{provider} Key Verified Successfully!"}
                    else:
                        err_text = resp.text[:120]
                        return {"valid": False, "status_code": resp.status_code, "message": f"Rejected (HTTP {resp.status_code}): {err_text}"}
            except Exception as e:
                return {"valid": False, "status_code": 500, "message": f"Connection error: {str(e)}"}

    @classmethod
    def _persist_keys_to_env(cls):
        """Helper to safely write runtime overrides to .env."""
        env_path = os.path.join(os.getcwd(), ".env")
        lines = []
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

        keys_to_write = {}
        if cls._runtime_gemini_key:
            keys_to_write["GEMINI_API_KEY"] = cls._runtime_gemini_key
        if cls._runtime_grok_key:
            keys_to_write["GROK_API_KEY"] = cls._runtime_grok_key
        if cls._runtime_custom_provider:
            keys_to_write["CUSTOM_AI_PROVIDER"] = cls._runtime_custom_provider
        if cls._runtime_custom_api_key:
            keys_to_write["CUSTOM_API_KEY"] = cls._runtime_custom_api_key
        if cls._runtime_custom_base_url:
            keys_to_write["CUSTOM_AI_BASE_URL"] = cls._runtime_custom_base_url
        if cls._runtime_custom_model:
            keys_to_write["CUSTOM_AI_MODEL"] = cls._runtime_custom_model

        if not keys_to_write:
            return

        new_lines = []
        written_keys = set()
        for line in lines:
            trimmed = line.strip()
            if trimmed and not trimmed.startswith("#") and "=" in trimmed:
                k = trimmed.split("=", 1)[0].strip()
                if k in keys_to_write:
                    new_lines.append(f"{k}={keys_to_write[k]}\n")
                    written_keys.add(k)
                    continue
            new_lines.append(line)

        for k, v in keys_to_write.items():
            if k not in written_keys:
                new_lines.append(f"{k}={v}\n")

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    async def generate_gemini(self, prompt: str, system_instruction: str = "") -> Optional[str]:
        """Calls Google Gemini REST API with multiple model fallback and fast exhaustion circuit breaker."""
        if not self.is_gemini_available():
            return None

        models = [self.gemini_model]
        for fallback in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-3.6-flash"]:
            if fallback not in models:
                models.append(fallback)

        contents = []
        if system_instruction:
            contents.append({"role": "user", "parts": [{"text": f"[System Instruction: {system_instruction}]"}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})
        payload = {"contents": contents}
        headers = {"Content-Type": "application/json"}

        for model in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.gemini_key}"
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
                    elif resp.status_code in (401, 403, 429):
                        self.mark_gemini_exhausted()
                        break
            except Exception:
                continue

        return None

    async def generate_grok(self, prompt: str, system_instruction: str = "") -> Optional[str]:
        """Calls xAI Grok API with fast exhaustion circuit breaker."""
        if not self.is_grok_available():
            return None

        url = "https://api.x.ai/v1/chat/completions"
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        models = [self.grok_model]
        if "grok-2" not in self.grok_model:
            models.append("grok-2-latest")

        for model in models:
            payload = {
                "model": model,
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
                    elif resp.status_code in (401, 403, 429):
                        self.mark_grok_exhausted()
                        return None
            except Exception:
                continue

        return None

    async def generate_custom(self, prompt: str, system_instruction: str = "") -> Optional[str]:
        """Calls user-added custom provider (OpenRouter / OpenAI / Anthropic compatible)."""
        if not self.is_custom_available():
            return None

        target_url = self.custom_base_url.rstrip("/") + "/chat/completions"
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.custom_model,
            "messages": messages,
            "stream": False
        }
        headers = {
            "Authorization": f"Bearer {self.custom_api_key}",
            "Content-Type": "application/json"
        }
        try:
            async with httpx.AsyncClient(timeout=self.custom_timeout) as client:
                resp = await client.post(target_url, json=payload, headers=headers)
                if resp.status_code in (200, 201):
                    data = resp.json()
                    return data["choices"][0]["message"]["content"].strip()
                elif resp.status_code in (401, 403, 429):
                    self.mark_custom_exhausted()
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
        Attempts generation using primary cloud provider with instant failover to alternate/custom.
        """
        if preferred_provider == "gemini":
            ans = await self.generate_gemini(prompt, system_instruction)
            if ans:
                return {"text": ans, "source": f"CLOUD_{self.gemini_model.upper()}", "tier": "CLOUD_PRIMARY"}
            ans_grok = await self.generate_grok(prompt, system_instruction)
            if ans_grok:
                return {"text": ans_grok, "source": f"CLOUD_{self.grok_model.upper()}", "tier": "CLOUD_PRIMARY"}
        else:
            ans_grok = await self.generate_grok(prompt, system_instruction)
            if ans_grok:
                return {"text": ans_grok, "source": f"CLOUD_{self.grok_model.upper()}", "tier": "CLOUD_PRIMARY"}
            ans = await self.generate_gemini(prompt, system_instruction)
            if ans:
                return {"text": ans, "source": f"CLOUD_{self.gemini_model.upper()}", "tier": "CLOUD_PRIMARY"}

        # Try user-configured custom provider if active
        if self.is_custom_available():
            ans_custom = await self.generate_custom(prompt, system_instruction)
            if ans_custom:
                return {"text": ans_custom, "source": f"CUSTOM_{self.custom_provider.upper()}", "tier": "CLOUD_CUSTOM"}

        return {"text": "", "source": "NONE", "tier": "EXHAUSTED"}
