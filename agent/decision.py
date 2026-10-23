"""REUSABLE DECISION PATTERN: DSA request classifier  (#policy)

What it does
    Before the DSA Buddy agent runs, Strands Decider 2B classifies each student message into
    the appropriate teaching mode:
    - what kind of request is it (concept, code, debug, practice, compare, off-topic)?
    - does the student want a Tamil explanation?
    - what skill level is implied by the message?
    This drives the agent's tool selection and teaching approach without reading the LLM's output.

Typed questions and options
    request_type (choice): concept_explain | code_walkthrough | debug_help | practice_problems
                            | language_compare | off_topic — one-line definitions for each.
    needs_tamil (noul): true if the student asks for Tamil, false for English.
    skill_level (choice): beginner | intermediate | advanced | unspecified.

Wiring (PolicyCheck InterventionHandler)
    `DSABuddyPolicy` is a Strands `InterventionHandler` that runs `before_invocation`
    (classifying the student's request before the LLM acts):

        policy = DSABuddyPolicy(Decider())
        agent = Agent(..., interventions=[policy])

    If the request is off_topic with high confidence it returns Deny.
    If the request type is unclear it returns Guide (asking the student to clarify).
    Otherwise it logs the classification and returns Proceed.

How to reuse it
    Copy this file. Replace QUESTIONS with your own taxonomy and update the thresholds in
    DSABuddyPolicy.before_invocation. The pattern works for any domain that needs fast,
    cheap request routing before a generative model responds.
"""

from __future__ import annotations

from typing import Any

from strands.interventions import Deny, Guide, InterventionHandler, Proceed

from decider_kit import Decider

PATTERN_TAG = "#policy"

QUESTIONS = {
    "request_type": Decider.choice(
        "What kind of DSA learning request is the student making?",
        {
            "concept_explain": "student wants to understand a DSA concept, definition, or theory",
            "code_walkthrough": "student wants to see or understand code for an algorithm",
            "debug_help": "student has broken code and wants help fixing it",
            "practice_problems": "student wants practice questions, exercises, or challenges",
            "language_compare": "student wants to compare the same algorithm across programming languages",
            "off_topic": "question is unrelated to data structures, algorithms, or programming",
        },
    ),
    "needs_tamil": Decider.noul(
        "Is the student asking for the explanation in the Tamil language?",
        {
            "true": "student is asking for explanation in Tamil language",
            "false": "explanation should be in English",
        },
    ),
    "skill_level": Decider.choice(
        "What skill level does the student's message imply?",
        {
            "beginner": "student mentions being new, a beginner, or wants simple explanation",
            "intermediate": "student has some knowledge and wants deeper understanding",
            "advanced": "student wants complexity analysis, optimization, or advanced discussion",
            "unspecified": "no skill level mentioned, use session default",
        },
    ),
}


class DSABuddyPolicy(InterventionHandler):
    """Before-invocation policy that classifies each student request with Strands Decider 2B."""

    name = "dsa-buddy-policy"

    def __init__(self, decider: Decider):
        self.decider = decider
        self.log: list[dict[str, Any]] = []
        self.last_guidance: dict[str, Any] = {}
        self._last_guided_msg: str | None = None  # Guide convergence guard

    def _extract_message(self, event: Any) -> str:
        """Pull the latest user message text from a Strands before_invocation event."""
        messages = getattr(event, "messages", None) or []
        # Walk backwards to find the most recent user turn.
        for msg in reversed(messages):
            if isinstance(msg, dict) and msg.get("role") == "user":
                content = msg.get("content", "")
                if isinstance(content, str):
                    return content
                if isinstance(content, list):
                    # Strands content blocks: [{"text": "..."}, ...]
                    parts = []
                    for block in content:
                        if isinstance(block, dict) and "text" in block:
                            parts.append(block["text"])
                    return " ".join(parts)
        return ""

    def before_invocation(self, event: Any, **kwargs: Any) -> Any:
        """Classify the student's message before the agent runs."""
        student_msg = self._extract_message(event)

        if not student_msg:
            return Proceed()

        # Guide convergence: if we already guided on this exact message, just proceed.
        if student_msg == self._last_guided_msg:
            self._last_guided_msg = None
            return Proceed()

        state = student_msg
        a = self.decider.ask(state, QUESTIONS)

        request_type = a["request_type"].label or "off_topic"
        request_conf = a["request_type"].confidence or 0.0
        needs_tamil = a["needs_tamil"].yes
        skill_level = a["skill_level"].label or "unspecified"
        decider_ms = round(self.decider.last_latency_ms or 0)

        rec: dict[str, Any] = {
            "pattern": PATTERN_TAG,
            "request_type": request_type,
            "needs_tamil": needs_tamil,
            "skill_level": skill_level,
            "decider_ms": decider_ms,
        }

        if request_type == "off_topic" and request_conf > 0.75:
            rec["verdict"] = "deny"
            self.log.append(rec)
            return Deny(
                reason="I'm DSA Buddy, a DSA tutor. Please ask me about Data Structures and Algorithms!"
            )

        if request_conf < 0.6:
            rec["verdict"] = "guide"
            self._last_guided_msg = student_msg
            self.log.append(rec)
            return Guide(
                feedback=(
                    "Please clarify your question — are you asking for an explanation, "
                    "code example, practice problems, or debugging help?"
                )
            )

        rec["verdict"] = "proceed"
        self.last_guidance = {
            "request_type": request_type,
            "needs_tamil": needs_tamil,
            "skill_level": skill_level,
        }
        self.log.append(rec)
        return Proceed()
