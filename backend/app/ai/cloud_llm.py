import os
import time
import httpx
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class KeyTracker:
    """
    Tracks state, exhaustion cooldown, auto-recharge, and usage statistics for an API key.
    """
    def __init__(
        self,
        key: str,
        provider: str,
        cooldown_rate_limit: float = 60.0,
        cooldown_quota: float = 300.0
    ):
        self.key = key.strip()
        self.provider = provider.lower()
        self.exhausted_until: float = 0.0
        self.cooldown_rate_limit = cooldown_rate_limit
        self.cooldown_quota = cooldown_quota
        self.failure_count: int = 0
        self.success_count: int = 0
        self.last_used: float = 0.0
        self.last_error: str = ""

    def is_available(self) -> bool:
        """Returns True if the key is ready or its cooldown period has expired (auto-recharged)."""
        if not self.key:
            return False
        return time.time() >= self.exhausted_until

    def mark_exhausted(self, is_quota_or_permission: bool = False, custom_duration: Optional[float] = None, error_msg: str = ""):
        """Places key into temporary cooldown. Recharges automatically when timer expires."""
        now = time.time()
        dur = custom_duration or (self.cooldown_quota if is_quota_or_permission else self.cooldown_rate_limit)
        self.exhausted_until = now + dur
        self.failure_count += 1
        if error_msg:
            self.last_error = error_msg

    def mark_success(self):
        """Marks successful response, clearing error and restoring full availability."""
        self.success_count += 1
        self.last_used = time.time()
        self.exhausted_until = 0.0
        self.last_error = ""

    @property
    def remaining_cooldown(self) -> float:
        now = time.time()
        if now >= self.exhausted_until:
            return 0.0
        return round(self.exhausted_until - now, 1)

    @property
    def status_label(self) -> str:
        if not self.key:
            return "UNCONFIGURED"
        rem = self.remaining_cooldown
        if rem > 0:
            return f"COOLING_DOWN ({rem}s left)"
        if self.success_count > 0:
            return "READY (RECHARGED)"
        return "READY"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "masked": CloudLLMHub._mask_key(self.key),
            "is_available": self.is_available(),
            "status": self.status_label,
            "remaining_cooldown_seconds": self.remaining_cooldown,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "last_error": self.last_error
        }


class CloudLLMHub:
    """
    Multi-Provider & Multi-Key Cloud LLM Gateway with Auto-Failover & Auto-Recharge:
    - Rank 1: Google Gemini Frontier Pool (gemini-3.6-flash, gemini-3.7-flash, gemini-flash-latest)
    - Rank 2: xAI Grok Frontier Pool (grok-2-latest)
    - Rank 3: Hugging Face Serverless Qwen Suite Pool (72B -> 32B -> 7B)
    - Rank 6: Local Ollama on Host (qwen2.5:0.5b / localhost:11434)
    - Rank 7: Deterministic Pedagogical Scaffold & FineWeb Knowledge Vault
    - Dynamic Auto-Recharge Circuit: When a key exhausts, it cools down for a set interval (e.g. 60s).
      The moment its cooldown expires, the engine immediately re-promotes it back to Rank 1 priority!
    """
    _key_trackers: Dict[str, KeyTracker] = {}
    _hf_72b_delayed_until: float = 0.0

    # Runtime key overrides (comma-separated or single)
    _runtime_gemini_keys: Optional[str] = None
    _runtime_grok_keys: Optional[str] = None
    _runtime_hf_tokens: Optional[str] = None
    _runtime_hf_model: Optional[str] = None

    _runtime_custom_provider: Optional[str] = None
    _runtime_custom_api_key: Optional[str] = None
    _runtime_custom_base_url: Optional[str] = None
    _runtime_custom_model: Optional[str] = None
    _custom_exhausted_until: float = 0.0

    def __init__(self):
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        self.gemini_timeout = float(os.getenv("GEMINI_TIMEOUT_SECONDS", "4.5"))

        self.grok_model = os.getenv("GROK_MODEL", "grok-2-latest")
        self.grok_timeout = float(os.getenv("GROK_TIMEOUT_SECONDS", "4.0"))

        self.custom_timeout = 4.0

    @classmethod
    def _get_or_create_tracker(cls, key: str, provider: str) -> KeyTracker:
        clean_key = key.strip()
        map_key = f"{provider.lower()}:{clean_key}"
        if map_key not in cls._key_trackers:
            rate_limit_cd = float(os.getenv("AI_COOLDOWN_RATE_LIMIT", "60.0"))
            quota_cd = float(os.getenv("AI_COOLDOWN_QUOTA", "300.0"))
            cls._key_trackers[map_key] = KeyTracker(
                key=clean_key,
                provider=provider,
                cooldown_rate_limit=rate_limit_cd,
                cooldown_quota=quota_cd
            )
        return cls._key_trackers[map_key]

    @classmethod
    def _parse_keys_list(cls, raw: Optional[str]) -> list[str]:
        if not raw:
            return []
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        return parts

    def get_gemini_keys(self) -> list[KeyTracker]:
        raw = CloudLLMHub._runtime_gemini_keys or os.getenv("GEMINI_API_KEYS") or os.getenv("GEMINI_API_KEY", "")
        keys = CloudLLMHub._parse_keys_list(raw)
        return [CloudLLMHub._get_or_create_tracker(k, "gemini") for k in keys]

    def get_grok_keys(self) -> list[KeyTracker]:
        raw = CloudLLMHub._runtime_grok_keys or os.getenv("GROK_API_KEYS") or os.getenv("GROK_API_KEY", "")
        keys = CloudLLMHub._parse_keys_list(raw)
        return [CloudLLMHub._get_or_create_tracker(k, "grok") for k in keys]

    def get_hf_tokens(self) -> list[KeyTracker]:
        raw = CloudLLMHub._runtime_hf_tokens or os.getenv("HF_TOKENS") or os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_API_KEY", "")
        keys = CloudLLMHub._parse_keys_list(raw)
        return [CloudLLMHub._get_or_create_tracker(k, "huggingface") for k in keys]

    @property
    def gemini_key(self) -> Optional[str]:
        keys = self.get_gemini_keys()
        return keys[0].key if keys else None

    @property
    def grok_key(self) -> Optional[str]:
        keys = self.get_grok_keys()
        return keys[0].key if keys else None

    @property
    def custom_provider(self) -> str:
        if CloudLLMHub._runtime_custom_provider:
            return CloudLLMHub._runtime_custom_provider
        env_prov = os.getenv("CUSTOM_AI_PROVIDER")
        if env_prov and env_prov.lower() != "none":
            return env_prov
        return "None"

    @property
    def custom_api_key(self) -> Optional[str]:
        return CloudLLMHub._runtime_custom_api_key or os.getenv("CUSTOM_API_KEY")

    @property
    def custom_base_url(self) -> Optional[str]:
        if CloudLLMHub._runtime_custom_base_url:
            return CloudLLMHub._runtime_custom_base_url
        return os.getenv("CUSTOM_AI_BASE_URL")

    @property
    def custom_model(self) -> Optional[str]:
        if CloudLLMHub._runtime_custom_model:
            return CloudLLMHub._runtime_custom_model
        return os.getenv("CUSTOM_AI_MODEL", "deepseek/deepseek-r1")

    @property
    def hf_token(self) -> Optional[str]:
        tokens = self.get_hf_tokens()
        return tokens[0].key if tokens else None

    @property
    def hf_base_url(self) -> str:
        return os.getenv("HF_ROUTER_BASE_URL", "https://router.huggingface.co/v1").rstrip("/")

    @property
    def hf_72b_model(self) -> str:
        return os.getenv("HF_QWEN_72B_MODEL", "Qwen/Qwen2.5-72B-Instruct")

    @property
    def hf_32b_model(self) -> str:
        return os.getenv("HF_QWEN_32B_MODEL", "Qwen/Qwen2.5-Coder-32B-Instruct")

    @property
    def hf_7b_model(self) -> str:
        return os.getenv("HF_QWEN_7B_MODEL", "Qwen/Qwen2.5-Coder-7B-Instruct")

    @property
    def hf_model(self) -> str:
        if CloudLLMHub._runtime_hf_model:
            return CloudLLMHub._runtime_hf_model
        return self.hf_72b_model

    def is_gemini_available(self) -> bool:
        return any(k.is_available() for k in self.get_gemini_keys())

    def is_grok_available(self) -> bool:
        return any(k.is_available() for k in self.get_grok_keys())

    def is_custom_available(self) -> bool:
        return bool(self.custom_api_key) and bool(self.custom_base_url) and time.time() > CloudLLMHub._custom_exhausted_until

    def is_hf_available(self) -> bool:
        return any(k.is_available() for k in self.get_hf_tokens())

    def mark_custom_exhausted(self, duration_seconds: float = 600.0):
        CloudLLMHub._custom_exhausted_until = time.time() + duration_seconds

    @classmethod
    def update_keys(
        cls,
        hf_token: Optional[str] = None,
        hf_model: Optional[str] = None,
        gemini_key: Optional[str] = None,
        grok_key: Optional[str] = None,
        custom_provider: Optional[str] = None,
        custom_api_key: Optional[str] = None,
        custom_base_url: Optional[str] = None,
        custom_model: Optional[str] = None,
        persist_to_env: bool = False
    ) -> Dict[str, Any]:
        """
        Dynamically updates active key pools, resets circuit breakers, and optionally updates .env file.
        Accepts single keys or comma-separated key pools.
        """
        changes = []
        if hf_token is not None:
            clean_hf = hf_token.strip()
            cls._runtime_hf_tokens = clean_hf if clean_hf else None
            for k in cls._parse_keys_list(clean_hf):
                cls._get_or_create_tracker(k, "huggingface").mark_success()
            changes.append("Hugging Face Tokens Pool")

        if hf_model is not None:
            cls._runtime_hf_model = hf_model.strip() or None

        if gemini_key is not None:
            clean_gemini = gemini_key.strip()
            cls._runtime_gemini_keys = clean_gemini if clean_gemini else None
            for k in cls._parse_keys_list(clean_gemini):
                cls._get_or_create_tracker(k, "gemini").mark_success()
            changes.append("Gemini Keys Pool")

        if grok_key is not None:
            clean_grok = grok_key.strip()
            cls._runtime_grok_keys = clean_grok if clean_grok else None
            for k in cls._parse_keys_list(clean_grok):
                cls._get_or_create_tracker(k, "grok").mark_success()
            changes.append("Grok Keys Pool")

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

        hub = cls()
        return {
            "success": True,
            "updated_fields": changes,
            "gemini_active": hub.is_gemini_available(),
            "gemini_keys_count": len(hub.get_gemini_keys()),
            "grok_active": hub.is_grok_available(),
            "grok_keys_count": len(hub.get_grok_keys()),
            "huggingface_active": hub.is_hf_available(),
            "huggingface_tokens_count": len(hub.get_hf_tokens()),
            "custom_active": bool(cls._runtime_custom_api_key and cls._runtime_custom_base_url)
        }

    @classmethod
    def reset_to_defaults(cls):
        """Clears all runtime overrides back to server environment variables."""
        cls._runtime_hf_tokens = None
        cls._runtime_hf_model = None
        cls._runtime_gemini_keys = None
        cls._runtime_grok_keys = None
        cls._runtime_custom_provider = None
        cls._runtime_custom_api_key = None
        cls._runtime_custom_base_url = None
        cls._runtime_custom_model = None
        cls._custom_exhausted_until = 0.0
        cls._key_trackers.clear()

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
        """Returns safe masked configuration and per-key cooldown timers for UI display."""
        hub = cls()
        gemini_keys = hub.get_gemini_keys()
        grok_keys = hub.get_grok_keys()
        hf_tokens = hub.get_hf_tokens()

        active_custom_key = cls._runtime_custom_api_key or os.getenv("CUSTOM_API_KEY", "")
        default_provider = cls._runtime_custom_provider or os.getenv("CUSTOM_AI_PROVIDER") or "OpenRouter"
        default_base_url = cls._runtime_custom_base_url or os.getenv("CUSTOM_AI_BASE_URL") or "https://openrouter.ai/api/v1"
        default_model = cls._runtime_custom_model or os.getenv("CUSTOM_AI_MODEL") or "deepseek/deepseek-r1"

        return {
            "gemini": {
                "has_key": len(gemini_keys) > 0,
                "model": hub.gemini_model,
                "is_active": hub.is_gemini_available(),
                "keys_count": len(gemini_keys),
                "keys": [k.to_dict() for k in gemini_keys],
                "masked": gemini_keys[0].to_dict()["masked"] if gemini_keys else "Not Configured"
            },
            "grok": {
                "has_key": len(grok_keys) > 0,
                "model": hub.grok_model,
                "is_active": hub.is_grok_available(),
                "keys_count": len(grok_keys),
                "keys": [k.to_dict() for k in grok_keys],
                "masked": grok_keys[0].to_dict()["masked"] if grok_keys else "Not Configured"
            },
            "huggingface": {
                "has_key": len(hf_tokens) > 0,
                "model": hub.hf_model,
                "is_active": hub.is_hf_available(),
                "tokens_count": len(hf_tokens),
                "keys": [k.to_dict() for k in hf_tokens],
                "masked": hf_tokens[0].to_dict()["masked"] if hf_tokens else "Not Configured"
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
        """Performs a live lightweight validation request for any individual key."""
        clean_key = key.strip()
        if not clean_key:
            return {"valid": False, "message": "Key cannot be empty"}

        p_lower = provider.lower()
        if p_lower in ("hf", "huggingface"):
            test_model = model or "Qwen/Qwen2.5-Coder-7B-Instruct"
            url = (base_url or "https://router.huggingface.co/v1").rstrip("/") + "/chat/completions"
            payload = {
                "model": test_model,
                "messages": [{"role": "user", "content": "Ping"}],
                "max_tokens": 2
            }
            try:
                async with httpx.AsyncClient(timeout=8.0) as client:
                    resp = await client.post(
                        url, json=payload,
                        headers={"Authorization": f"Bearer {clean_key}", "Content-Type": "application/json"}
                    )
                    if resp.status_code in (200, 201):
                        return {"valid": True, "status_code": 200, "message": f"Hugging Face ({test_model}) Verified Successfully!"}
                    else:
                        err_text = resp.text[:120]
                        return {"valid": False, "status_code": resp.status_code, "message": f"Hugging Face Rejected Key (HTTP {resp.status_code}): {err_text}"}
            except Exception as e:
                return {"valid": False, "status_code": 500, "message": f"Connection error: {str(e)}"}

        elif p_lower == "gemini":
            test_model = model or "gemini-3.6-flash"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{test_model}:generateContent?key={clean_key}"
            payload = {"contents": [{"role": "user", "parts": [{"text": "Ping"}]}]}
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
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
                async with httpx.AsyncClient(timeout=5.0) as client:
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
                async with httpx.AsyncClient(timeout=5.0) as client:
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
        if cls._runtime_hf_tokens:
            keys_to_write["HF_TOKENS"] = cls._runtime_hf_tokens
            first_tok = cls._parse_keys_list(cls._runtime_hf_tokens)[0]
            keys_to_write["HF_TOKEN"] = first_tok
            keys_to_write["HUGGINGFACE_API_KEY"] = first_tok
        if cls._runtime_gemini_keys:
            keys_to_write["GEMINI_API_KEYS"] = cls._runtime_gemini_keys
            first_gem = cls._parse_keys_list(cls._runtime_gemini_keys)[0]
            keys_to_write["GEMINI_API_KEY"] = first_gem
        if cls._runtime_grok_keys:
            keys_to_write["GROK_API_KEYS"] = cls._runtime_grok_keys
            first_grok = cls._parse_keys_list(cls._runtime_grok_keys)[0]
            keys_to_write["GROK_API_KEY"] = first_grok
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

    async def generate_gemini(self, prompt: str, system_instruction: str = "") -> Optional[Dict[str, Any]]:
        """
        Calls Google Gemini REST API with multi-key pool failover and automatic cooldown recharge.
        Iterates over pooled keys in strict priority. If a key hits 429/403, it enters cooldown
        and the engine immediately fails over to the next key.
        """
        keys = self.get_gemini_keys()
        if not keys:
            return None

        preferred_model = self.gemini_model if self.gemini_model not in ("gemini-2.0-flash", "gemini-2.5-flash") else "gemini-3.6-flash"
        models = [preferred_model]
        for fallback in ["gemini-3.6-flash", "gemini-3.7-flash", "gemini-flash-latest", "gemini-flash-lite-latest"]:
            if fallback not in models:
                models.append(fallback)

        contents = []
        if system_instruction:
            contents.append({"role": "user", "parts": [{"text": f"[System Instruction: {system_instruction}]"}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})
        payload = {"contents": contents}
        headers = {"Content-Type": "application/json"}

        for tracker in keys:
            if not tracker.is_available():
                continue  # In active cooldown, fail over to next key in pool

            for model in models:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={tracker.key}"
                try:
                    async with httpx.AsyncClient(timeout=self.gemini_timeout) as client:
                        resp = await client.post(url, json=payload, headers=headers)
                        if resp.status_code == 200:
                            data = resp.json()
                            if "error" in data:
                                err_msg = data["error"].get("message", "")
                                if "model output" in err_msg.lower():
                                    continue
                                continue
                            candidates = data.get("candidates", [])
                            if not candidates:
                                continue
                            candidate = candidates[0]
                            finish_reason = candidate.get("finishReason", "STOP")
                            if finish_reason in ("SAFETY", "OTHER", "RECITATION", "BLOCKLIST"):
                                continue
                            parts = candidate.get("content", {}).get("parts", [])
                            if parts and "text" in parts[0]:
                                text = parts[0]["text"].strip()
                                if text:
                                    tracker.mark_success()
                                    return {
                                        "text": text,
                                        "model": model,
                                        "source": f"CLOUD_{model.upper()}",
                                        "key_masked": tracker.to_dict()["masked"]
                                    }
                        elif resp.status_code == 429:
                            tracker.mark_exhausted(is_quota_or_permission=False, error_msg="HTTP 429 Rate Limit Exceeded")
                            break  # Switch to next key in pool!
                        elif resp.status_code in (401, 403):
                            tracker.mark_exhausted(is_quota_or_permission=True, error_msg=f"HTTP {resp.status_code} Quota/Permission Blocked")
                            break  # Switch to next key in pool!
                except Exception:
                    continue

        return None

    async def generate_grok(self, prompt: str, system_instruction: str = "") -> Optional[Dict[str, Any]]:
        """Calls xAI Grok API with multi-key pool failover and cooldown recharge."""
        keys = self.get_grok_keys()
        if not keys:
            return None

        url = "https://api.x.ai/v1/chat/completions"
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        models = [self.grok_model]
        if "grok-2" not in self.grok_model:
            models.append("grok-2-latest")

        for tracker in keys:
            if not tracker.is_available():
                continue

            for model in models:
                payload = {
                    "model": model,
                    "messages": messages,
                    "stream": False
                }
                headers = {
                    "Authorization": f"Bearer {tracker.key}",
                    "Content-Type": "application/json"
                }
                try:
                    async with httpx.AsyncClient(timeout=self.grok_timeout) as client:
                        resp = await client.post(url, json=payload, headers=headers)
                        if resp.status_code == 200:
                            data = resp.json()
                            content = data["choices"][0]["message"]["content"].strip()
                            if content:
                                tracker.mark_success()
                                return {
                                    "text": content,
                                    "model": model,
                                    "source": f"CLOUD_{model.upper()}",
                                    "key_masked": tracker.to_dict()["masked"]
                                }
                        elif resp.status_code in (401, 403, 429):
                            is_quota = resp.status_code in (401, 403)
                            tracker.mark_exhausted(is_quota_or_permission=is_quota, error_msg=f"HTTP {resp.status_code}")
                            break
                except Exception:
                    continue

        return None

    async def generate_custom(self, prompt: str, system_instruction: str = "") -> Optional[Dict[str, Any]]:
        """Calls user-configured custom provider (OpenRouter / OpenAI compatible)."""
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
                    content = (data.get("choices", [{}])[0].get("message") or {}).get("content", "").strip()
                    if content:
                        return {
                            "text": content,
                            "model": data.get("model") or self.custom_model,
                            "usage": data.get("usage", {}),
                            "source": f"CUSTOM_{self.custom_provider.upper()}"
                        }
                elif resp.status_code in (401, 403, 429):
                    self.mark_custom_exhausted()
                    return None
        except Exception:
            self.mark_custom_exhausted()
            return None

        return None

    async def generate_huggingface(self, prompt: str, system_instruction: str = "") -> Optional[Dict[str, Any]]:
        """
        Calls Hugging Face router with multi-token pool failover and descending power models (72B -> 32B -> 7B).
        """
        tokens = self.get_hf_tokens()
        if not tokens:
            return None

        url = f"{self.hf_base_url}/chat/completions"
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        # Descending power capacity order
        if time.time() < CloudLLMHub._hf_72b_delayed_until:
            models_to_try = [self.hf_32b_model, self.hf_7b_model, self.hf_72b_model]
        else:
            models_to_try = [self.hf_72b_model, self.hf_32b_model, self.hf_7b_model]

        for tracker in tokens:
            if not tracker.is_available():
                continue

            headers = {
                "Authorization": f"Bearer {tracker.key}",
                "Content-Type": "application/json"
            }

            token_failed = False
            for model in models_to_try:
                payload = {
                    "model": model,
                    "messages": messages,
                    "max_tokens": 800,
                    "temperature": 0.3
                }
                timeout_sec = 10.0 if "72" in model else 8.0
                try:
                    async with httpx.AsyncClient(timeout=timeout_sec) as client:
                        resp = await client.post(url, json=payload, headers=headers)
                        if resp.status_code in (200, 201):
                            data = resp.json()
                            choices = data.get("choices", [])
                            if choices:
                                content = (choices[0].get("message") or {}).get("content", "").strip()
                                if content:
                                    tracker.mark_success()
                                    usage = data.get("usage", {})
                                    return {
                                        "text": content,
                                        "model": data.get("model") or model,
                                        "usage": usage,
                                        "source": f"HF_{model.split('/')[-1].upper().replace('-', '_')}",
                                        "key_masked": tracker.to_dict()["masked"]
                                    }
                        elif resp.status_code in (401, 403):
                            tracker.mark_exhausted(is_quota_or_permission=True, error_msg=f"HTTP {resp.status_code} Auth/Quota")
                            token_failed = True
                            break
                        elif resp.status_code in (429, 503):
                            if "72" in model:
                                CloudLLMHub._hf_72b_delayed_until = time.time() + 60.0
                            continue
                except Exception:
                    if "72" in model:
                        CloudLLMHub._hf_72b_delayed_until = time.time() + 60.0
                    continue

            if not token_failed:
                tracker.mark_exhausted(is_quota_or_permission=False, error_msg="Temporary Model Busy")

        return None

    async def generate_best(
        self,
        prompt: str,
        system_instruction: str = "",
        preferred_provider: str = "gemini"
    ) -> Dict[str, Any]:
        """
        Power-Ranked Generation with Dynamic Failover & Auto-Recharge Recovery:
        1. Google Gemini Frontier Pool (Key 1 -> Key 2)
        2. xAI Grok Frontier Pool (Key 1)
        3. Hugging Face Serverless Qwen Suite (Token 1 -> Token 2, 72B -> 32B -> 7B)
        * DYNAMIC RECHARGE RECOVERY: If Hugging Face exhausts, checks if Rank 1 (Gemini) or Rank 2 (Grok)
          finished its cooldown in the meantime. If recharged, returns directly to Rank 1!
        6. Custom BYOK Provider (OpenRouter / OpenAI compatible)
        Falls back to Local Ollama and Deterministic Pedagogical Scaffold if all exhausted.
        """
        # ── RANK 1: Google Gemini Frontier Pool ──
        if self.is_gemini_available():
            ans_gemini = await self.generate_gemini(prompt, system_instruction)
            if ans_gemini and ans_gemini.get("text"):
                return {
                    "text": ans_gemini["text"],
                    "source": ans_gemini.get("source", f"CLOUD_{self.gemini_model.upper()}"),
                    "tier": "RANK_1_GEMINI_FRONTIER",
                    "model": ans_gemini.get("model", self.gemini_model),
                    "key_masked": ans_gemini.get("key_masked", ""),
                    "usage": {}
                }

        # ── RANK 2: xAI Grok Frontier Reasoning ──
        if self.is_grok_available():
            ans_grok = await self.generate_grok(prompt, system_instruction)
            if ans_grok and ans_grok.get("text"):
                return {
                    "text": ans_grok["text"],
                    "source": ans_grok.get("source", f"CLOUD_{self.grok_model.upper()}"),
                    "tier": "RANK_2_GROK_REASONING",
                    "model": ans_grok.get("model", self.grok_model),
                    "key_masked": ans_grok.get("key_masked", ""),
                    "usage": {}
                }

        # ── RANK 3, 4, 5: Hugging Face Serverless Qwen Suite Pool ──
        if self.is_hf_available():
            ans_hf = await self.generate_huggingface(prompt, system_instruction)
            if ans_hf and ans_hf.get("text"):
                model_used = ans_hf.get("model", self.hf_72b_model)
                if "72" in model_used:
                    tier_label = "RANK_3_HF_QWEN_72B"
                elif "32" in model_used:
                    tier_label = "RANK_4_HF_QWEN_32B"
                else:
                    tier_label = "RANK_5_HF_QWEN_7B"

                return {
                    "text": ans_hf["text"],
                    "source": ans_hf.get("source", "HF_QWEN2.5"),
                    "tier": tier_label,
                    "model": model_used,
                    "key_masked": ans_hf.get("key_masked", ""),
                    "usage": ans_hf.get("usage", {})
                }

        # ── DYNAMIC RECHARGE RECOVERY (User's Specific Requirement) ──
        # If Rank 3 (Hugging Face) exhausted, do NOT blindly drop to offline fallback if
        # Rank 1 (Gemini) or Rank 2 (Grok) has completed its cooldown and recharged!
        if self.is_gemini_available():
            ans_gemini = await self.generate_gemini(prompt, system_instruction)
            if ans_gemini and ans_gemini.get("text"):
                return {
                    "text": ans_gemini["text"],
                    "source": ans_gemini.get("source", f"CLOUD_{self.gemini_model.upper()}"),
                    "tier": "RANK_1_GEMINI_FRONTIER (RECHARGED)",
                    "model": ans_gemini.get("model", self.gemini_model),
                    "key_masked": ans_gemini.get("key_masked", ""),
                    "usage": {}
                }

        if self.is_grok_available():
            ans_grok = await self.generate_grok(prompt, system_instruction)
            if ans_grok and ans_grok.get("text"):
                return {
                    "text": ans_grok["text"],
                    "source": ans_grok.get("source", f"CLOUD_{self.grok_model.upper()}"),
                    "tier": "RANK_2_GROK_REASONING (RECHARGED)",
                    "model": ans_grok.get("model", self.grok_model),
                    "key_masked": ans_grok.get("key_masked", ""),
                    "usage": {}
                }

        # ── RANK 6 (Custom): User-configured Custom Provider ──
        if self.is_custom_available():
            ans_custom = await self.generate_custom(prompt, system_instruction)
            if ans_custom and ans_custom.get("text"):
                return {
                    "text": ans_custom["text"],
                    "source": f"CUSTOM_{ans_custom.get('model', self.custom_model).upper()}",
                    "tier": "RANK_CUSTOM_PROVIDER",
                    "model": ans_custom.get("model", self.custom_model),
                    "key_masked": "",
                    "usage": ans_custom.get("usage", {})
                }

        return {"text": "", "source": "NONE", "tier": "EXHAUSTED"}


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
        "- ZERO INTERNAL CODES: NEVER mention or output internal database IDs or question codes (such as 'pHQ-1234', 'q_1', 'cnc_...'). Always identify questions by their Topic, Chapter, or Concept Name.",
        "- HUMANIZED MISTAKE CORRECTION: When reviewing test performance or explaining errors, explicitly state:",
        "  1) Which Topic and Chapter the problem originated from.",
        "  2) The specific concept tested and the problem context.",
        "  3) The cognitive misconception or trap (why the student's selected choice was tempting).",
        "  4) The clear step-by-step correct solution and LaTeX formula used.",
        "  5) Warmly invite the student to take a targeted recovery retest drill to solidify understanding.",
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

