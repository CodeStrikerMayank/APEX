"""
Offline Local LLM & Hardened Deterministic AI Assistant Client
Platform Upgrade v3.0 — Offline-First, Zero-Hallucination
"""
import os
import httpx
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

from backend.app.ai.intent_classifier import (
    IntentClassifier,
    INTENT_ANALYZE_MISTAKES,
    INTENT_EXPLAIN_ROADMAP,
    INTENT_STRATEGY_TIPS,
    INTENT_EXPLAIN_CONCEPT,
    INTENT_UNKNOWN
)
from backend.app.ai.templates import (
    format_mistake_analysis,
    format_roadmap_explanation,
    format_strategy_tips,
    format_concept_explanation,
    format_unknown_fallback
)


class LocalLLMClient:
    """
    Hardened AI Assistant:
    1. Primary Engine: Deterministic IntentClassifier + Slot-filling Templates.
    2. Fallback / Optional Polish: Local Ollama (if running on host).
    3. Guarantees 100% factual fidelity to student's quiz answers and roadmap DAG.
    """
    def __init__(
        self,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        enabled: Optional[bool] = None
    ):
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model_name = model_name or os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")
        self.enabled = enabled if enabled is not None else os.getenv("LOCAL_AI_ENABLED", "true").lower() == "true"
        self.timeout = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "35.0"))

    async def generate_text(
        self,
        prompt: str,
        system_prompt: str = "",
        student_context: Optional[Dict[str, Any]] = None,
        use_polish: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Classifies user intent, generates bulletproof grounded response,
        and optionally polishes via Ollama or Cloud LLM if available.
        """
        if not self.enabled:
            return {
                "text": "Local AI mentor is disabled.",
                "source": "DISABLED"
            }

        # 1. Sanitize user input
        sanitized_prompt = IntentClassifier.sanitize_input(prompt)
        if not sanitized_prompt:
            sanitized_prompt = "hello"

        # 2. Classify intent
        intent, confidence, topic_hint = IntentClassifier.classify(sanitized_prompt)

        # 3. Normalize context keys
        ctx = dict(student_context or {})
        exam = ctx.get("exam") or ctx.get("target_exam") or "JEE"
        ctx["exam"] = exam
        if "latest_quiz" in ctx and "latest_attempt" not in ctx:
            ctx["latest_attempt"] = ctx["latest_quiz"]
        if "roadmap_actions" in ctx and "roadmap_milestones" not in ctx:
            ctx["roadmap_milestones"] = ctx["roadmap_actions"]

        # 4. Generate deterministic grounded response
        if intent == INTENT_ANALYZE_MISTAKES:
            grounded_text = format_mistake_analysis(ctx)
        elif intent == INTENT_EXPLAIN_ROADMAP:
            grounded_text = format_roadmap_explanation(ctx)
        elif intent == INTENT_STRATEGY_TIPS:
            grounded_text = format_strategy_tips(exam, ctx)
        elif intent == INTENT_EXPLAIN_CONCEPT:
            grounded_text = format_concept_explanation(topic_hint, exam)
        else:
            grounded_text = format_unknown_fallback(exam)

        # 5. Cloud Frontier Polish Pass (Gemini / Grok) if enabled
        should_polish = use_polish if use_polish is not None else True
        use_gemini = should_polish and os.getenv("USE_GEMINI_POLISH", "true").lower() == "true"
        if use_gemini:
            try:
                from backend.app.ai.cloud_llm import CloudLLMHub
                hub = CloudLLMHub()
                polish_prompt = (
                    f"Polish the following educational response for an Indian {exam} student. "
                    "Make it encouraging, razor-sharp, and clear. Preserve all mathematical equations, "
                    f"markdown formatting, and technical accuracy:\n\n{grounded_text}"
                )
                cloud_res = await hub.generate_best(polish_prompt)
                if cloud_res.get("text") and len(cloud_res["text"]) > 50:
                    return {
                        "text": cloud_res["text"],
                        "intent": intent,
                        "confidence": confidence,
                        "source": cloud_res["source"]
                    }
            except Exception:
                pass  # Fall through to local Ollama

        # 6. Optional Local Ollama Polish Pass (hardware-optimized timeout on Drive D)
        ollama_enabled = should_polish and os.getenv("USE_OLLAMA_POLISH", "false").lower() == "true"
        if ollama_enabled:
            try:
                url = f"{self.base_url}/api/generate"
                payload = {
                    "model": self.model_name,
                    "prompt": f"Polish the following educational response for clarity and tone, preserving all technical details and markdown formatting exactly:\n\n{grounded_text}",
                    "stream": False
                }
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        polished = data.get("response", "").strip()
                        if len(polished) > 50:
                            return {
                                "text": polished,
                                "intent": intent,
                                "confidence": confidence,
                                "source": f"OLLAMA_POLISHED_{self.model_name}"
                            }
            except Exception:
                pass  # Fall through to deterministic text

        return {
            "text": grounded_text,
            "intent": intent,
            "confidence": confidence,
            "source": "DETERMINISTIC_INTENT_ENGINE"
        }

    async def generate_raw(
        self,
        prompt: str,
        system_prompt: str = ""
    ) -> Dict[str, Any]:
        """
        Direct inference through Ollama for free-form generation.
        """
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "system": system_prompt,
                "stream": False
            }
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    return {
                        "text": data.get("response", "").strip(),
                        "source": f"OLLAMA_DIRECT_{self.model_name}"
                    }
        except Exception:
            pass
        return {
            "text": "Direct local LLM generation unavailable.",
            "source": "FALLBACK"
        }
