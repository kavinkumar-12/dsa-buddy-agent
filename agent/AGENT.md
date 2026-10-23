# DSA Buddy

- **Pitch:** DSA Buddy — a personal DSA tutor for college students that teaches algorithms step by step, explains code line by line, gives practice problems with progressive hints, and supports English and Tamil explanations.
- **Who it is for:** College students learning Data Structures and Algorithms, especially beginners.
- **Features:**
  - explain DSA concepts in simple language with real-world analogies (English or Tamil);
  - walk through algorithms step by step with visualized state changes;
  - show code line by line in Python, C, C++, or Java;
  - compare implementations of the same algorithm across languages;
  - give practice problems with progressive hints and full solutions on request;
  - debug the student's code with guided explanations, not just the fix;
  - skill level (beginner/intermediate/advanced) set at start, changeable anytime;
  - deployed on Amazon Bedrock AgentCore Runtime.
- **The decision handed to Strands Decider 2B:** classify each student request into one of: concept_explain, code_walkthrough, debug_help, practice_problems, language_compare, off_topic — so the agent selects the right teaching approach before responding. (`#policy`)
- **Why a decision model:** request classification must be fast, cheap, and consistent; wrong classification wastes the student's time with the wrong teaching style.
- **Amazon Bedrock:** the conversation and tool use (Amazon Nova Pro by default).
