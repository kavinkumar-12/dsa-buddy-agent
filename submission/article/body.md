# DSA Buddy: a personal DSA tutor that classifies before it teaches

By DSA Buddy team

Every college student learning Data Structures and Algorithms hits the same wall: they do not know what they do not know, and the tools meant to help them do not ask. A search engine gives a wall of text. A chatbot answers the wrong question. DSA Buddy is a personal DSA tutor that uses Strands Decider 2B to classify each student request before a single word is generated, so the right teaching tool runs and the student gets the explanation they actually asked for. In testing, the decider hit 100% accuracy on request classification and ran 30x faster than the LLM asked the same questions.

## The project

DSA Buddy is for college students learning DSA, especially beginners who need a patient tutor rather than a reference manual. A student opens the chat and types in plain language: "Hi, I am a beginner. Teach me binary search from scratch." The agent introduces the concept with a real-world analogy (guessing a pizza size from a sorted list), walks through the algorithm step by step with a concrete example, shows the Python code with line-by-line comments, and then offers practice problems with progressive hints.

The features cover the full learning loop: concept explanations with analogies, code walkthroughs in Python, C, C++, or Java, side-by-side language comparisons, practice problems with hints before solutions, and guided debugging that explains why code is broken instead of just handing over the fix. Students can set their skill level (beginner, intermediate, advanced) and change it anytime. They can ask for explanations in Tamil, and the agent switches languages while keeping code and technical terms in English.

Here is a real conversation from the demo run:

- Student: "Hi! I'm a beginner. Teach me binary search from scratch."
- DSA Buddy explains the concept with a pizza-ordering analogy, traces through an example with the array [2, 4, 6, 8, 10], shows the Python code, and invites the student to try a mini-problem. The decider classified this as concept_explain with 0.92 confidence in 4.5 seconds.

- Student: "Explain recursion in Tamil please."
- DSA Buddy responds entirely in Tamil script, covering the base case, recursive case, and trust-the-recursion principle, while keeping the English technical terms alongside. The decider detected needs_tamil = true with the request_type concept_explain.

- Student: "What's the weather today?"
- DSA Buddy blocks it: "I'm DSA Buddy, a DSA tutor. Please ask me about Data Structures and Algorithms!" The decider classified this as off_topic with 0.84 confidence and denied it in 4.3 seconds, before the LLM was ever called.

## How I built it

The agent is a Strands Agent with five tools (explain_concept, show_code, get_practice_problems, compare_implementations, debug_code) backed by structured mock data for 12 DSA topics, from arrays through dynamic programming. The generative layer runs on Amazon Bedrock (Amazon Nova Pro by default) in the deployed version, and the conversation and tool use go through the Strands Agents SDK. The agent deploys on Amazon Bedrock AgentCore Runtime.

Strands Decider 2B sits in front of the agent as an InterventionHandler. Before each invocation, it classifies the student's message and either lets the agent proceed, asks the student to clarify, or denies off-topic requests. The agent tracks session state (skill level and preferred language) and adapts its system prompt accordingly.

I built DSA Buddy with Kiro, the AI-powered development environment, using a spec-driven workflow. The kit from the AWS User Group Madurai provided the Strands Decider client, the five decision patterns, and the demo UI. I changed only the agent code and kept the kit's library and contracts intact.

## The decision I handed to Strands Decider 2B

The core question DSA Buddy faces on every message is: what kind of help does this student need? A concept explanation, a code walkthrough, a debugging session, practice problems, a language comparison, or something off-topic entirely? Getting this wrong wastes the student's time. If a student asks for code and gets a theory lecture, or asks for practice and gets a debug walkthrough, the tutor has failed.

This decision needs a fast, calibrated model rather than another LLM call. An LLM can classify requests, but it takes 100+ seconds on the hosted API and sometimes returns the wrong type. Strands Decider 2B reads the student's message and three typed questions in one forward pass and returns calibrated probabilities. The agent branches on those probabilities in ordinary Python code.

```python
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
```

When the decider is confident (above 0.6), the agent proceeds with the classified teaching mode. When the request is off-topic with high confidence (above 0.75), the agent denies it and redirects the student back to DSA. When confidence is low, the agent asks the student to clarify their question instead of guessing. A convergence guard prevents infinite Guide loops: if the agent guides on the same message twice, it proceeds.

< FIGURE 1 of 5: upload submission/article/img/architecture.png here >
Alt text: Architecture: the user, the agent with its tools and decision, Amazon Bedrock and Strands Decider 2B

## Measured

I benchmarked the decider against the LLM (qwen3.5-4b on the AWS User Group Madurai cloud) on 10 labelled cases with 20 total decisions (request_type and needs_tamil per case).

| | Strands Decider 2B | qwen3.5-4b |
|---|---|---|
| Accuracy | 100.0% | 90.0% |
| Latency p50 per decision | 3742 ms | 113947 ms |
| Latency p95 | 6331 ms | 174798 ms |
| Cost per 1,000 decisions | $0.0350 | $0.0000 |
| Answered alone at confidence >= 0.7 | 90% | 100% |
| Accuracy when confident | 100.0% | 90.0% |

At the median the decider was 30.4x faster than the LLM. The decider ran on the AWS User Group Madurai hosted API (strands-decider-2b-hobson-v19). The LLM baseline ran on the same hosted cloud. Both used the same 10 cases from the tune split.

The decider answered 90% of decisions alone at the 0.7 confidence threshold. Two decisions were below threshold and would have been sent to a human or a clarification prompt. The LLM was confident on every decision but got 10% wrong, including one request_type misclassification where it answered code_walkthrough instead of language_compare. The decider got all 20 right.

The weak spot is latency when the decider runs on the hosted API: 3.7 seconds per decision at the median, which adds to the LLM's response time. On a GPU or Apple silicon the same model runs in 0.1 to 0.3 seconds. The cost ($0.035 per 1,000 decisions) is low enough that it does not factor into decisions about whether to run the check.

< FIGURE 2 of 5: upload submission/article/img/bench-accuracy.png here >
Alt text: Accuracy of Strands Decider 2B and the Bedrock LLM on the labelled cases

< FIGURE 3 of 5: upload submission/article/img/bench-latency.png here >
Alt text: Median latency per decision for both

< FIGURE 4 of 5: upload submission/article/img/bench-cost.png here >
Alt text: Cost per 1,000 decisions for both

< FIGURE 5 of 5: upload submission/article/img/bench-confidence.png here >
Alt text: Accuracy against the share of decisions answered without a human, as the confidence threshold moves

## The reusable decision pattern

The pattern lives in agent/decision.py. It defines PATTERN_TAG = "#policy", the QUESTIONS dict with three typed questions, and DSABuddyPolicy, a Strands InterventionHandler that runs before_invocation.

To reuse it in your own agent, copy the file and replace the QUESTIONS with your own taxonomy. The wiring is three lines: create a DSABuddyPolicy with a Decider instance, pass it as an intervention to your Strands Agent, and the handler classifies every message before the LLM runs. Update the thresholds (0.75 for deny, 0.6 for guide) and the option descriptions to match your domain. The pattern works for any agent that needs fast, cheap request routing before a generative model responds.

## What I learned and what is next

The biggest lesson was that the decision model's accuracy depends almost entirely on the option descriptions, not the state text. When I wrote vague descriptions ("a code question"), the decider confused code walkthroughs with debugging. When I wrote specific descriptions ("student wants to see or understand code for an algorithm" versus "student has broken code and wants help fixing it"), accuracy went to 100%.

The Tamil language detection was a pleasant surprise. The noul question with clear true/false descriptions correctly identified Tamil requests without any script detection or keyword matching in the agent code. The decider reads the message and returns a calibrated probability, and the agent branches on it.

What is next: adding more DSA topics, supporting more natural languages, and using the decider for a second decision (skill-level detection is already classified but not yet wired into tool selection). I also want to add a visual step-by-step algorithm tracer that renders state changes in the demo UI.

---

Code: (repo link to be added after publish) . Video: (video link to be added after upload) . Tags: #strands-decider-2b #policy

Built with the AWS User Group Madurai Strands Decider hackathon kit
