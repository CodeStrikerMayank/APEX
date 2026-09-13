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
        if CloudLLMHub._runtime_custom_provider:
            return CloudLLMHub._runtime_custom_provider
        env_prov = os.getenv("CUSTOM_AI_PROVIDER")
        if env_prov and env_prov.lower() != "none":
            return env_prov
        if os.getenv("EXPLABS_API_KEY"):
            return "ExperientialLabs"
        return "None"

    @property
    def custom_api_key(self) -> Optional[str]:
        return CloudLLMHub._runtime_custom_api_key or os.getenv("CUSTOM_API_KEY") or os.getenv("EXPLABS_API_KEY")

    @property
    def custom_base_url(self) -> Optional[str]:
        if CloudLLMHub._runtime_custom_base_url:
            return CloudLLMHub._runtime_custom_base_url
        env_url = os.getenv("CUSTOM_AI_BASE_URL")
        if env_url:
            return env_url
        if os.getenv("EXPLABS_API_KEY"):
            return "https://api.experientiallabs.ai/v1"
        return None

    @property
    def custom_model(self) -> Optional[str]:
        if CloudLLMHub._runtime_custom_model:
            return CloudLLMHub._runtime_custom_model
        env_model = os.getenv("CUSTOM_AI_MODEL")
        if env_model:
            return env_model
        if os.getenv("EXPLABS_API_KEY") or (os.getenv("CUSTOM_AI_PROVIDER") and "experiential" in os.getenv("CUSTOM_AI_PROVIDER", "").lower()):
            return "gpt-5.6-luna"
        return "deepseek/deepseek-r1"

    def is_gemini_available(self) -> bool:
        return bool(self.gemini_key) and time.time() > CloudLLMHub._gemini_exhausted_until

    def is_grok_available(self) -> bool:
        return bool(self.grok_key) and time.time() > CloudLLMHub._grok_exhausted_until

    def is_custom_available(self) -> bool:
        return bool(self.custom_api_key) and bool(self.custom_base_url) and time.time() > CloudLLMHub._custom_exhausted_until

    def mark_gemini_exhausted(self, duration_seconds: float = 15.0):
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
        active_custom_key = cls._runtime_custom_api_key or os.getenv("CUSTOM_API_KEY", "") or os.getenv("EXPLABS_API_KEY", "")

        default_provider = cls._runtime_custom_provider or os.getenv("CUSTOM_AI_PROVIDER") or ("ExperientialLabs" if (os.getenv("EXPLABS_API_KEY") or os.getenv("CUSTOM_API_KEY")) else "OpenRouter")
        default_base_url = cls._runtime_custom_base_url or os.getenv("CUSTOM_AI_BASE_URL") or ("https://api.experientiallabs.ai/v1" if (os.getenv("EXPLABS_API_KEY") or os.getenv("CUSTOM_API_KEY")) else "https://openrouter.ai/api/v1")
        default_model = cls._runtime_custom_model or os.getenv("CUSTOM_AI_MODEL") or ("gemini-3.7-flash" if (os.getenv("EXPLABS_API_KEY") or os.getenv("CUSTOM_API_KEY")) else "deepseek/deepseek-r1")

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
                "provider": default_provider,
                "has_key": bool(active_custom_key),
                "masked": cls._mask_key(active_custom_key),
                "base_url": default_base_url,
                "model": default_model,
                "is_active": bool(active_custom_key) and bool(default_base_url)
            }
        }

    @classmethod
    async def test_key(cls, provider: str, key: str, base_url: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
        """Performs a live lightweight validation request."""
        clean_key = key.strip()
        if not clean_key:
            return {"valid": False, "message": "Key cannot be empty"}

        p_lower = provider.lower()
        if p_lower == "gemini":
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

        elif p_lower == "grok":
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

        elif p_lower in ("explabs", "experientiallabs"):
            target_url = (base_url or "https://api.experientiallabs.ai/v1").rstrip("/") + "/chat/completions"
            models_to_test = [model] if model else ["gpt-5.6-luna", "gemini-3.7-flash"]
            last_err = ""
            for m in models_to_test:
                payload = {
                    "model": m,
                    "messages": [{"role": "user", "content": "Ping"}],
                    "max_tokens": 5
                }
                try:
                    async with httpx.AsyncClient(timeout=5.0) as client:
                        resp = await client.post(
                            target_url, json=payload,
                            headers={"Authorization": f"Bearer {clean_key}", "Content-Type": "application/json"}
                        )
                        if resp.status_code in (200, 201):
                            data = resp.json()
                            usage = data.get("usage", {})
                            u_str = f"Tokens: {usage.get('total_tokens', 'N/A')} (prompt: {usage.get('prompt_tokens', 0)}, comp: {usage.get('completion_tokens', 0)})"
                            return {
                                "valid": True,
                                "status_code": resp.status_code,
                                "model": m,
                                "usage": usage,
                                "message": f"ExperientialLabs ({m}) Verified Successfully! {u_str}"
                            }
                        else:
                            last_err = f"HTTP {resp.status_code}: {resp.text[:100]}"
                except Exception as e:
                    last_err = str(e)
            return {"valid": False, "status_code": 500, "message": f"ExperientialLabs Rejected: {last_err}"}

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
            if "experientiallabs" in (cls._runtime_custom_base_url or "").lower() or (cls._runtime_custom_provider or "").lower() == "experientiallabs":
                keys_to_write["EXPLABS_API_KEY"] = cls._runtime_custom_api_key
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

        # Prioritize verified working endpoints for Gemini v1beta
        preferred_model = self.gemini_model if self.gemini_model not in ("gemini-2.5-flash", "gemini-3.6-flash") else "gemini-flash-latest"
        models = [preferred_model]
        for fallback in ["gemini-flash-latest", "gemini-flash-lite-latest", "gemma-4-26b-a4b-it", "gemini-3.6-flash", "gemini-2.5-flash"]:
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
                        # Detect Gemini "model output error" — returned as HTTP 200 with error key
                        if "error" in data:
                            err_msg = data["error"].get("message", "")
                            if "model output" in err_msg.lower() or "output text" in err_msg.lower():
                                continue  # Skip to next model — safety/content filter triggered
                            continue
                        candidates = data.get("candidates", [])
                        if not candidates:
                            continue  # Empty candidates — blocked output, try next model
                        candidate = candidates[0]
                        # Check finishReason — SAFETY/OTHER = blocked, skip
                        finish_reason = candidate.get("finishReason", "STOP")
                        if finish_reason in ("SAFETY", "OTHER", "RECITATION", "BLOCKLIST"):
                            continue
                        if "content" in candidate:
                            parts = candidate["content"].get("parts", [])
                            if parts and "text" in parts[0]:
                                text = parts[0]["text"].strip()
                                if text:
                                    return text
                    elif resp.status_code == 429:
                        continue  # Try next model before marking entire provider exhausted
                    elif resp.status_code in (401, 403):
                        self.mark_gemini_exhausted(duration_seconds=300.0)
                        return None
            except Exception:
                continue

        self.mark_gemini_exhausted(duration_seconds=15.0)
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

    async def generate_custom(self, prompt: str, system_instruction: str = "") -> Optional[Dict[str, Any]]:
        """Calls user-added custom provider (ExperientialLabs / OpenRouter / OpenAI compatible)."""
        if not self.is_custom_available():
            return None

        target_url = self.custom_base_url.rstrip("/") + "/chat/completions"
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        # Multi-model candidate list for Experiential gateway: gpt-5.6-luna primary, gemini-3.7-flash fallback
        models = [self.custom_model]
        is_explabs = "experiential" in self.custom_provider.lower() or "experiential" in (self.custom_base_url or "").lower()
        if is_explabs:
            if "gpt-5.6-luna" not in models:
                models.insert(0, "gpt-5.6-luna")
            if "gemini-3.7-flash" not in models:
                models.append("gemini-3.7-flash")

        headers = {
            "Authorization": f"Bearer {self.custom_api_key}",
            "Content-Type": "application/json"
        }

        for model in models:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False
            }
            try:
                async with httpx.AsyncClient(timeout=self.custom_timeout) as client:
                    resp = await client.post(target_url, json=payload, headers=headers)
                    if resp.status_code in (200, 201):
                        data = resp.json()
                        # Detect gateway-relayed "model output error" from Gemini models
                        if "error" in data and not data.get("choices"):
                            err_msg = str(data["error"])
                            if "model output" in err_msg.lower() or "output text" in err_msg.lower():
                                continue  # Try next gateway model
                            continue
                        choices = data.get("choices", [])
                        if not choices:
                            continue
                        content = (choices[0].get("message") or {}).get("content", "") or ""
                        content = content.strip()
                        if not content:
                            continue  # Empty response, try next model
                        usage = data.get("usage", {})
                        return {"text": content, "model": model, "usage": usage}
                    elif resp.status_code in (401, 403):
                        self.mark_custom_exhausted()
                        return None
                    elif resp.status_code == 429:
                        continue  # Try next fallback model (e.g. gemini-3.7-flash)
            except Exception:
                continue

        self.mark_custom_exhausted(duration_seconds=20.0)
        return None

    async def generate_best(
        self,
        prompt: str,
        system_instruction: str = "",
        preferred_provider: str = "experiential"
    ) -> Dict[str, Any]:
        """
        Attempts generation using primary ExperientialLabs cloud provider (gpt-5.6-luna -> gemini-3.7-flash)
        with multi-tier instant failover to Gemini direct, Grok xAI, and offline tiers.
        """
        effective_preference = os.getenv("PREFERRED_AI_PROVIDER", preferred_provider).lower()
        
        # TIER 1 & TIER 2: ExperientialLabs Gateway (gpt-5.6-luna, then gemini-3.7-flash)
        if effective_preference in ("experiential", "explabs", "experientiallabs", "custom") or self.is_custom_available():
            if self.is_custom_available():
                ans_custom = await self.generate_custom(prompt, system_instruction)
                if ans_custom and ans_custom.get("text"):
                    return {
                        "text": ans_custom["text"],
                        "source": f"EXPERIENTIAL_{ans_custom.get('model', self.custom_model).upper()}",
                        "tier": "CLOUD_PRIMARY",
                        "model": ans_custom.get("model", self.custom_model),
                        "usage": ans_custom.get("usage", {})
                    }
        
        # TIER 3: Google Gemini Direct Frontier
        ans_gemini = await self.generate_gemini(prompt, system_instruction)
        if ans_gemini:
            return {"text": ans_gemini, "source": f"CLOUD_{self.gemini_model.upper()}", "tier": "CLOUD_FALLBACK"}

        # TIER 4: xAI Grok Frontier
        ans_grok = await self.generate_grok(prompt, system_instruction)
        if ans_grok:
            return {"text": ans_grok, "source": f"CLOUD_{self.grok_model.upper()}", "tier": "CLOUD_FALLBACK"}

        # Secondary check if custom wasn't primary but is available
        if self.is_custom_available():
            ans_custom = await self.generate_custom(prompt, system_instruction)
            if ans_custom and ans_custom.get("text"):
                return {
                    "text": ans_custom["text"],
                    "source": f"EXPERIENTIAL_{ans_custom.get('model', self.custom_model).upper()}",
                    "tier": "CLOUD_FALLBACK",
                    "model": ans_custom.get("model", self.custom_model),
                    "usage": ans_custom.get("usage", {})
                }

        return {"text": "", "source": "NONE", "tier": "EXHAUSTED"}


def get_experiential_client():
    """
    Builds an OpenAI client configured for the ExperientialLabs gateway.
    1. Points the client at https://api.experientiallabs.ai/v1 as the base URL.
    2. Authenticates with the Experiential API key from EXPLABS_API_KEY environment variable.
       If it isn't set, stops and tells the user to create one under Settings -> API Keys and export it.
    """
    key = os.getenv("EXPLABS_API_KEY")
    if not key or not key.strip():
        raise ValueError(
            "EXPLABS_API_KEY is not set! Please create one under Settings -> API Keys and export it (e.g. in your .env or run export EXPLABS_API_KEY=...)."
        )
    from openai import OpenAI
    return OpenAI(base_url="https://api.experientiallabs.ai/v1", api_key=key.strip())


def build_unified_system_prompt(
    student_context: Dict[str, Any],
    exam: str = "JEE",
    mode: str = "pedagogical",
    is_solve: bool = False,
    troubleshoot_str: str = "",
    history_str: str = ""
) -> str:
    """
    Constructs the single-statement multi-tier system prompt:
    - Tier 1: Persona, Tone & Readability (Kid-friendly, empathetic, structured emojis/badges, zero robotic filler).
    - Tier 2: Domain Protocol Rules (JEE / NEET / UPSC / GENERAL_STEM from DomainProtocolEngine).
    - Tier 3: Psychometric Grounding (IRT Ability theta tier, BKT mastery, FSRS decay, prerequisite root causes).
    - Tier 4: Step-by-Step Problem Solving & Didactic Scaffolding (5-step derivation for mathematical solve queries).
    """
    from backend.app.ai.domain_protocols import DomainProtocolEngine
    from backend.app.ai.omni_context import OmniContextHarvester

    proto = DomainProtocolEngine.get_protocol(exam)
    proto_instructions = proto.get_system_instructions(is_solve=is_solve)

    theta_val = float(student_context.get("latent_ability_theta", 0.0) or 0.0)
    if theta_val < -0.5:
        theta_tier_instruction = (
            "STUDENT COGNITIVE TIER: Foundational Baseline (θ < -0.5).\n"
            "- Use warm, validating encouragement and simplify prerequisites.\n"
            "- Break down mathematical derivations into granular algebraic steps with plain English transitions."
        )
    elif theta_val > 0.7:
        theta_tier_instruction = (
            "STUDENT COGNITIVE TIER: Advanced Mastery (θ > 0.7).\n"
            "- Maintain high competitive rigor; avoid over-explaining trivial steps.\n"
            "- Emphasize dimensional analysis shortcuts, symmetry arguments, and Olympiad/Advanced challenge variations."
        )
    else:
        theta_tier_instruction = (
            "STUDENT COGNITIVE TIER: Intermediate Core (-0.5 <= θ <= 0.7).\n"
            "- Balance conceptual clarity with competitive speed, exam pacing, and negative marking prevention."
        )

    mode_map = {
        "socratic": (
            "PEDAGOGICAL MODE: Socratic Prober. Do NOT reveal complete formulas or final numerical answers immediately. "
            "Pose 1-2 targeted discriminatory questions to guide the student to discover the principle."
        ),
        "scaffolding": (
            "PEDAGOGICAL MODE: Stepped Scaffolding. Provide graduated assistance across 3 structured micro-steps. "
            "Set up Step 1, hint at Step 2, and prompt the student to solve Step 3."
        ),
        "diagnostic": (
            "PEDAGOGICAL MODE: Cognitive Diagnostician. Pinpoint mental model flaws and discriminate between conceptual and calculation gaps."
        ),
        "challenge": (
            "PEDAGOGICAL MODE: Olympiad & Extreme Limits. Stress-test boundary conditions and synthesize multi-concept relations."
        ),
        "forensics": (
            "PEDAGOGICAL MODE: Mistake Forensics. Contrast student misconceptions against correct keys and explain distractor traps."
        ),
        "pedagogical": (
            "PEDAGOGICAL MODE: Canonical Pedagogical Mentor. Provide clear, academically rigorous derivations with LaTeX formulas."
        )
    }
    mode_text = mode_map.get(mode, mode_map["pedagogical"])

    grounding_str = OmniContextHarvester.format_grounding_block(student_context, mode=mode)

    parts = [
        f"You are the APEX AI Cognitive Study Mentor for {exam} ({proto.display_title}).",
        "",
        "=== TIER 1: TONE, STYLE & ACCESSIBILITY ===",
        "- Tone: Warm, deeply encouraging, empathetic, and intellectually rigorous.",
        "- Visual Structure: Use short paragraphs, clear section headers (###), bullet points, and visual emojis (💡, 📐, ⚡, ⚠️, 🎯).",
        "- Kid-Friendly Clarity: Explain hard concepts intuitively (Feynman method) using everyday physical analogies before formal mathematics.",
        "- Formatting Invariant: All equations, formulas, variables, and math MUST be rendered in LaTeX ($...$ inline, $$...$$ block).",
        "",
        "=== TIER 2: DOMAIN PROTOCOL INVARIANTS ===",
        proto_instructions,
        "",
        "=== TIER 3: COGNITIVE & PSYCHOMETRIC GROUNDING ===",
        theta_tier_instruction,
        mode_text,
        f"Live Telemetry Grounding:\n{grounding_str}",
    ]

    if is_solve:
        parts.extend([
            "",
            "=== TIER 4: STEP-BY-STEP PROBLEM SOLVER ===",
            proto.get_solve_structure()
        ])

    if troubleshoot_str:
        parts.extend(["", "=== TECHNICAL TROUBLESHOOTING CONTEXT ===", troubleshoot_str])

    if history_str:
        parts.extend(["", "=== ROLLING MULTI-TURN HISTORY ===", history_str])

    return "\n".join(parts)

