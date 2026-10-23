"""DSA Buddy: a personal DSA tutor backed by Amazon Bedrock, with Strands Decider 2B classifying
each student request before the LLM responds.

    from agent.agent import HackathonAgent
    out = HackathonAgent().chat("Explain binary search to me, I'm a beginner.")
    out["reply"], out["decisions"]
"""

from __future__ import annotations

import time
from typing import Any

from strands import Agent

from decider_kit import Decider
from decider_kit.llm import agent_model, default_model_id, strip_thinking

from .decision import DSABuddyPolicy
from .tools import TOOLS

NAME = "DSA Buddy"

SYSTEM_PROMPT = """You are DSA Buddy, a patient and encouraging personal DSA tutor for college students.
Your goal is to help students understand Data Structures and Algorithms deeply, not just memorize them.
Always teach the concept first, then show code, then give practice.
Adapt your explanations to the student's skill level.
Be warm, clear, and step-by-step.

When a student gives their skill level or preferred language, remember it for the rest of the session.
Use the tools available to you: explain_concept, show_code, get_practice_problems, compare_implementations, debug_code."""


def _build_system_prompt(skill_level: str, preferred_language: str) -> str:
    """Build a session-specific system prompt with skill level and language preference."""
    lang_note = " Explain in Tamil when asked." if preferred_language == "tamil" else ""
    level_note = (
        " Use very simple language, small examples, and break every step down." if skill_level == "beginner"
        else " Go into deeper analysis and more complex examples." if skill_level == "intermediate"
        else " Include time/space complexity analysis and discuss optimizations." if skill_level == "advanced"
        else ""
    )
    return SYSTEM_PROMPT + level_note + lang_note


def _detect_skill_level(message: str) -> str | None:
    """Simple keyword scan to detect an explicit skill level in a message."""
    msg = message.lower()
    if any(w in msg for w in ("beginner", "new to", "just started", "first time", "basic", "simple")):
        return "beginner"
    if any(w in msg for w in ("intermediate", "some experience", "already know")):
        return "intermediate"
    if any(w in msg for w in ("advanced", "expert", "complex", "optimize", "complexity")):
        return "advanced"
    return None


def _detect_language(message: str) -> str | None:
    """Simple keyword scan for language preference."""
    msg = message.lower()
    if any(w in msg for w in ("tamil", "tamil la", "tamil le", "tamilil", "tamil explain")):
        return "tamil"
    # Also detect Tamil script words by checking for non-ASCII in the message alongside context
    if any(ord(c) > 0x0B7F and ord(c) <= 0x0BFF for c in message):
        return "tamil"
    if "english" in msg:
        return "english"
    return None


class HackathonAgent:
    """One Strands agent per session, with DSABuddyPolicy wired in as a before_invocation handler."""

    def __init__(self, decider: Decider | None = None, model_id: str | None = None, eager: bool | None = None):
        self.decider = decider or Decider()
        self.model_id = model_id or default_model_id()
        self.eager = eager  # accepted per kit interface; not used by DSA Buddy
        # session_id -> (Agent, DSABuddyPolicy)
        self.sessions: dict[str, tuple[Agent, DSABuddyPolicy]] = {}
        # session_id -> {"skill_level": str, "preferred_language": str}
        self.session_state: dict[str, dict[str, str]] = {}

    def _get_or_create_session(self, session_id: str) -> tuple[Agent, DSABuddyPolicy]:
        if session_id not in self.sessions:
            state = self.session_state.setdefault(session_id, {
                "skill_level": "beginner",
                "preferred_language": "english",
            })
            policy = DSABuddyPolicy(self.decider)
            agent = Agent(
                model=agent_model(self.model_id),
                system_prompt=_build_system_prompt(state["skill_level"], state["preferred_language"]),
                tools=TOOLS,
                interventions=[policy],
                callback_handler=None,
            )
            self.sessions[session_id] = (agent, policy)
        return self.sessions[session_id]

    def _update_session_state(self, session_id: str, message: str) -> bool:
        """Update skill_level / preferred_language from the message. Returns True if changed."""
        state = self.session_state.setdefault(session_id, {
            "skill_level": "beginner",
            "preferred_language": "english",
        })
        changed = False
        new_level = _detect_skill_level(message)
        if new_level and new_level != state["skill_level"]:
            state["skill_level"] = new_level
            changed = True
        new_lang = _detect_language(message)
        if new_lang and new_lang != state["preferred_language"]:
            state["preferred_language"] = new_lang
            changed = True
        return changed

    def chat(self, message: str, session_id: str = "default") -> dict[str, Any]:
        """Send a student message and return reply + decisions.

        Returns dict with keys: reply, decisions, model_id, latency_ms.
        """
        # Update session state first; recreate agent if level/language changed.
        state_changed = self._update_session_state(session_id, message)
        if state_changed and session_id in self.sessions:
            # Recreate the agent with updated system prompt; preserve the policy log.
            del self.sessions[session_id]

        agent, policy = self._get_or_create_session(session_id)
        before = len(policy.log)

        t0 = time.perf_counter()
        result = agent(message)
        latency_ms = (time.perf_counter() - t0) * 1000

        reply = strip_thinking(str(result))

        # Collect decisions logged since this call started.
        raw_decisions = policy.log[before:]
        decisions = [
            {
                "request_type": d.get("request_type", ""),
                "needs_tamil": d.get("needs_tamil", False),
                "skill_level": d.get("skill_level", ""),
                "verdict": d.get("verdict", ""),
                "decider_ms": d.get("decider_ms", 0),
            }
            for d in raw_decisions
        ]

        return {
            "reply": reply,
            "decisions": decisions,
            "model_id": self.model_id,
            "latency_ms": round(latency_ms),
        }


if __name__ == "__main__":
    import json

    agent = HackathonAgent()
    demo_messages = [
        ("default", "Hi! I'm a beginner. Can you explain binary search to me?"),
        ("default", "Show me the Python code for binary search."),
        ("tamil", "Explain recursion in Tamil please."),
    ]
    for session_id, msg in demo_messages:
        print(f"\n--- [{session_id}] {msg[:60]} ---")
        out = agent.chat(msg, session_id=session_id)
        print(f"Reply (first 300 chars): {out['reply'][:300]}")
        print(f"Decisions: {json.dumps(out['decisions'], indent=2)}")
        print(f"Model: {out['model_id']}  Latency: {out['latency_ms']} ms")
