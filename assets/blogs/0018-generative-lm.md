@{id = "e641a543-88bf-4623-a02a-d6216540015f"
  title = "Breaking Free from Context Limits: Recursive Language Models Explained"
  date = "2026-01-20T00:00:00Z"
  tags = ['journal club', 'machine learning', 'arxiv', 'language models']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/zhang-kraska-khattab-rlm.svg"
  description = "This entry is a summary of the paper \"Recursive Language Models\" by Zhang, Kraska & Khattab"
  type = "note"
  disabled = "False"
}

<p align="center">
  <img src="https://storage.googleapis.com/gn-portfolio/images/zhang-kraska-khattab-rlm.svg" max-width="700">
</p>


# Breaking Free from Context Limits: Recursive Language Models Explained

**How MIT researchers taught AI to handle million-token prompts by treating them as external data**

*Based on "Recursive Language Models" by Zhang, Kraska & Khattab (MIT CSAIL, 2025)*

---

## The Context Window Problem

Imagine trying to read a book, but you can only look at 2-3 pages at a time. Now imagine trying to answer complex questions about that entire book. This is essentially the challenge modern AI models face with their limited "context windows."

Even the most advanced models like GPT-5 struggle with this fundamental limitation. As shown in groundbreaking research from MIT, when you feed these models longer and longer text, their performance doesn't just plateau—it **degrades dramatically**. The researchers call this phenomenon "context rot."

But what if we could fundamentally rethink how AI handles long documents? That's exactly what Recursive Language Models (RLMs) do.

### The Big Idea

Instead of cramming everything into the AI's limited memory, RLMs treat long prompts as **external data**—like files on a hard drive that can be programmatically examined, chunked, and processed piece by piece through recursive calls.

```txt
┌───────────────────────────────────────────────────────────┐
│  Traditional LLM Approach                                 │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌────────────┐      ┌──────────────────┐                 │
│  │   Entire   │ ───> │  Neural Network  │ ───> Answer     │
│  │   Prompt   │      │  (Limited Memory)│   ❌ Fails at   │
│  │ (Too Big!) │      │    Overloaded    │      scale      │
│  └────────────┘      └──────────────────┘                 │
│                                                           │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  RLM Approach: Prompt as External Environment             │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌────────────┐    ┌──────────────────┐                   │
│  │   Prompt   │    │   Python REPL    │                   │
│  │ Stored as  │───>│   Environment    │                   │
│  │  Variable  │    │                  │                   │
│  └────────────┘    │  • Peek at data  │                   │
│                    │  • Chunk it      │                   │
│  10M+ tokens OK!   │  • Filter it     │                   │
│                    │                  │                   │
│                    │  When needed:    │                   │
│                    │  Make sub-query──┼──────┐            │
│                    │                  │      │            │
│                    │  Get result<───┐ │      │            │
│                    └────────────────┼─┘      │            │
│                           │         │        │            │
│                           │         │        ▼            │
│                           │         │ ┌─────────────┐     │
│                           │         │ │  Sub-LLM    │     │
│                           │         │ │             │     │
│                           │         └─│  Processes  │     │
│                           │           │  One Chunk  │     │
│                           │           └─────────────┘     │
│                           │                               │
│                           └────> Final Answer ✅          │
│                                                           │
└───────────────────────────────────────────────────────────┘

```

### Key Takeaways

- **Context rot is real**: Even frontier models degrade significantly as context grows
- **RLMs scale 100x**: Handle inputs **two orders of magnitude** beyond context windows
- **Better performance**: Outperform base models by double-digit percentages even on shorter prompts
- **Cost-effective**: Comparable or cheaper cost per query vs. naive approaches

---

## How RLMs Work: The Architecture

The brilliance of RLMs lies in their simplicity. Instead of feeding a massive prompt directly into the neural network, RLMs:

1. **Load the prompt as a variable** in a Python REPL environment
2. **Give the LLM tools** to programmatically examine this data
3. **Enable recursive sub-queries** where the LLM can call itself on smaller chunks
4. **Iterate until solved** with full execution feedback

### The REPL-Based Architecture

```txt
┌──────────────────────────────────────────────────────────────┐
│                    RLM Execution Flow                        │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────┐
              │  1. Initialize REPL       │
              │  context = load_prompt()  │
              │  len(context) = 10M chars │
              └───────────┬───────────────┘
                          │
                          ▼
              ┌───────────────────────────┐
              │  2. Root LLM Examines     │
              │  "I see 10M chars.        │
              │   Let me peek at first    │
              │   1000 lines..."          │
              └───────────┬───────────────┘
                          │
                          ▼
              ┌───────────────────────────┐
              │  3. Execute Python Code   │
              │  chunk = context[:5000]   │
              │  print(chunk)             │
              └───────────┬───────────────┘
                          │
                          ▼
              ┌───────────────────────────┐
              │  4. Recursive Sub-Query   │
              │  answer = llm_query(      │
              │    "Find X in: " + chunk  │
              │  )                        │──┐
              └───────────┬───────────────┘  │
                          │                  │
                     ┌────┘                  │
                     │                       │
                     ▼                       │
          ┌────────────────────┐             │
          │  Sub-LLM Call      │             │
          │  (smaller context) │             │
          │  Processes chunk   │             │
          │  Returns result ───│─────────────┘
          └────────────────────┘
                     │
                     ▼
          ┌────────────────────┐
          │  5. Aggregate      │
          │  Combine results   │
          │  from all chunks   │
          │  Build final       │
          │  answer            │
          └────────┬───────────┘
                   │
                   ▼
          ┌────────────────────┐
          │  6. Return Result  │
          │  FINAL(answer)     │
          └────────────────────┘
```

### Implementation Example

Here's how you might implement a simple RLM-style processor:

```python
from typing import Callable, Any

class SimpleRLM:
    """A simplified RLM that processes long documents recursively."""

    def __init__(self, llm_call: Callable[[str], str], chunk_size: int = 5000):
        """
        Args:
            llm_call: Function that calls an LLM with a prompt
            chunk_size: Max characters to process in one sub-call
        """
        self.llm_call = llm_call
        self.chunk_size = chunk_size

    def process(self, prompt: str, context: str) -> str:
        """
        Process a long context recursively.

        Args:
            prompt: The question to answer
            context: The (potentially huge) document

        Returns:
            The final answer
        """
        # If context is small enough, process directly
        if len(context) < self.chunk_size:
            return self.llm_call(f"{prompt}\n\nContext: {context}")

        # Otherwise, chunk and recursively process
        chunks = self._smart_chunk(context, self.chunk_size)
        sub_answers = []

        for i, chunk in enumerate(chunks):
            # Recursive sub-query on each chunk
            sub_prompt = f"""Extract information relevant to: {prompt}

This is chunk {i+1} of {len(chunks)}. Only extract relevant info."""

            sub_answer = self.llm_call(f"{sub_prompt}\n\n{chunk}")
            sub_answers.append(sub_answer)

        # Aggregate results
        aggregation_prompt = f"""Original question: {prompt}

I've processed {len(chunks)} chunks. Here are the findings:

{chr(10).join(f"Chunk {i+1}: {ans}" for i, ans in enumerate(sub_answers))}

Synthesize these to answer the original question."""

        return self.llm_call(aggregation_prompt)

    def _smart_chunk(self, text: str, max_size: int) -> list[str]:
        """Split text at paragraph boundaries when possible."""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = []
        current_size = 0

        for para in paragraphs:
            para_size = len(para)
            if current_size + para_size > max_size and current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = [para]
                current_size = para_size
            else:
                current_chunk.append(para)
                current_size += para_size

        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))

        return chunks


# Example usage:
def mock_llm(prompt: str) -> str:
    """Placeholder for actual LLM API call."""
    return "Extracted relevant info..."

rlm = SimpleRLM(llm_call=mock_llm, chunk_size=5000)
answer = rlm.process(
    prompt="What are the key findings about protein folding?",
    context=ten_million_character_biology_paper  # Can handle this!
)
```

### Key Takeaways

- **REPL environment** lets the LLM programmatically explore data
- **Recursive sub-calls** break problems into manageable pieces
- **Code execution** provides precise control over chunking and filtering
- **Stateful processing** maintains context across recursive calls through variables

---

## The Results: 100x Scale, Better Performance

The MIT team tested RLMs on four challenging benchmarks with dramatically different complexity profiles:

### Performance Across Scales

```txt
┌────────────────────────────────────────────────────────────┐
│  Performance vs Context Length (GPT-5 vs RLM)              │
└────────────────────────────────────────────────────────────┘

Score (%)
     │                  S-NIAH (RLM ~95-100%)
100% ├ ●━━●━━●━━●━━●━━●━━●━━●━━●━━●━━●━━●━━●━━●━━●━━
     │
 90% ├ ○···○
     │      ╲           S-NIAH (GPT-5 ~80-90%)
 80% │       ○···○···○···○···○···○···○···○···○···○··
     │
 70% │
     │                  OOLONG-Pairs (RLM ~58%)
 60% ├ ■━━■━━■━━■━━■━━■━━■━━■━━■━━■━━■━━■━━■━━■━━■━━
     │                  OOLONG (RLM ~56.5%)
 50% │ ▲━━▲━━▲━━▲━━▲━━▲━━▲━━▲━━▲━━▲━━▲━━▲━━▲━━▲━━▲━━
     │     △            OOLONG (GPT-5 ~44%)
 40% │        △···△···△···△···△···△···△···△···△
     │
 30% │
     │
 20% │
     │
 10% │
     │                  OOLONG-Pairs (GPT-5 ~0.04%)
  0% ├ □···□···□···□···□···□···□···□···□···□···□···□
     │
     └─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────
          8K   16K  33K  66K  131K 262K 524K  1M
                    Context Length (tokens)


LEGEND:
━━━  Solid lines = RLM
···  Dotted lines = Base GPT-5

● / ○  S-NIAH (Simple task)
▲ / △  OOLONG (Medium complexity)
■ / □  OOLONG-Pairs (Highest complexity)

Key Insight: RLM performance stays strong as complexity increases
             while base models catastrophically degrade
```

### Benchmark Results

| Task | Complexity | RLM(GPT-5) | Base GPT-5 | Improvement |
|------|-----------|------------|------------|-------------|
| **CodeQA** | Code understanding | 62% | 24%* | **+158%** |
| **BrowseComp+** | Multi-doc research | 91% | 0%* | **Enables task** |
| **OOLONG** | Dense aggregation | 56.5% | 44% | **+28%** |
| **OOLONG-Pairs** | Quadratic pairs | 58% | 0.04% | **+145,000%** |

*Base model exceeded context limit

### Cost Efficiency

```txt
┌─────────────────────────────────────────────────────────────────────────────┐
│  Cost vs Performance Comparison (Mean ± Std Dev)                            │
│  All costs in USD per query                                                 │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
CODEQA (23K-4.2M tokens) - Code repository understanding
═══════════════════════════════════════════════════════════════════════════════
Method              Cost/Query          Performance      Cost-Efficiency
───────────────────────────────────────────────────────────────────────────────
Base GPT-5          $0.13 ± $0.07          24% *        ★☆☆☆☆ Can't fit all
CodeAct + BM25      $0.06 ± $0.08          22% *        ★☆☆☆☆ Cheapest but fails
Summary Agent       $1.31 ± $1.46          58%          ★★★☆☆ Expensive
RLM(GPT-5)          $0.11 ± $0.10          62%          ★★★★★ Best value
───────────────────────────────────────────────────────────────────────────────
                    (* = hit context limits on many tasks)

═══════════════════════════════════════════════════════════════════════════════
BROWSECOMP+ (6-11M tokens) - Multi-document research
═══════════════════════════════════════════════════════════════════════════════
Method              Cost/Query          Performance      Cost-Efficiency
───────────────────────────────────────────────────────────────────────────────
Base GPT-5          N/A (fails)            0% *         ☆☆☆☆☆ Cannot run
CodeAct + BM25      $0.71 ± $1.20          51%          ★★☆☆☆ Works but poor
Summary Agent       $0.57 ± $0.10          70%          ★★★☆☆ Good but lossy
RLM(GPT-5)          $0.99 ± $1.22          91%          ★★★★★ Highest quality
───────────────────────────────────────────────────────────────────────────────
                    (* = exceeds 272K token context window)

═══════════════════════════════════════════════════════════════════════════════
OOLONG (131K tokens) - Dense semantic aggregation
═══════════════════════════════════════════════════════════════════════════════
Method              Cost/Query          Performance      Cost-Efficiency
───────────────────────────────────────────────────────────────────────────────
Base GPT-5          $0.14 ± $0.02          44%          ★★☆☆☆ Baseline
Summary Agent       $0.13 ± $0.01          46%          ★★☆☆☆ Slightly better
CodeAct + BM25      $0.61 ± $1.06          38%          ★☆☆☆☆ More cost, worse
RLM(GPT-5)          $0.43 ± $0.85          56.5%        ★★★★☆ 3x cost, +28% perf
───────────────────────────────────────────────────────────────────────────────

═══════════════════════════════════════════════════════════════════════════════
OOLONG-PAIRS (32K tokens) - Quadratic pairwise reasoning
═══════════════════════════════════════════════════════════════════════════════
Method              Cost/Query          Performance      Cost-Efficiency
───────────────────────────────────────────────────────────────────────────────
Base GPT-5          $0.16 ± $0.10          0.04%        ☆☆☆☆☆ Complete failure
Summary Agent       $0.13 ± $0.09          0.01%        ☆☆☆☆☆ Complete failure
CodeAct + BM25      $0.75 ± $0.43          24.67%       ★★☆☆☆ Partial success
RLM(GPT-5)          $0.33 ± $0.20          58.00%       ★★★★★ Only viable method
───────────────────────────────────────────────────────────────────────────────


KEY INSIGHTS:
═════════════════════════════════════════════════════════════════════════════

1. SHORT CONTEXTS (32K-131K): RLM costs 2-3x more than base model
   Trade-off: Pay 2-3x for significantly better quality (+28% to +58% absolute)

2. LONG CONTEXTS (4M+ tokens): RLM cheaper or comparable to alternatives
   - CodeQA: RLM $0.11 vs Summary $1.31 (88% savings!)
   - BrowseComp+: RLM $0.99 vs Summary $0.57 (but +30% performance)

3. HIGH VARIANCE: Note the large ± values for RLM
   - Median costs are good (Figure 3 in paper)
   - But 95th percentile can be 10x higher due to long trajectories

4. IMPOSSIBLE TASKS: RLM enables tasks that others simply cannot do
   - BrowseComp+ with 10M tokens: Base model cannot even attempt
   - OOLONG-Pairs: Base model ~0%, RLM ~58%
```

### Key Takeaways

- **10M+ token scale**: RLMs successfully process inputs 100x beyond context windows
- **Dramatic improvements**: 2x better on long tasks, enables impossible tasks
- **Cost-effective**: Median cost is **cheaper** than base model while performing far better
- **Scales with complexity**: Performance degrades gracefully unlike base models

---

## Emergent Intelligence: What RLMs Learn to Do

Perhaps the most fascinating finding: **RLMs spontaneously develop sophisticated problem-solving strategies** without explicit training. The researchers observed several emergent behaviors:

### 1. Smart Filtering Using Code & Priors

RLMs learn to filter massive datasets without reading everything:

```python
# Example: RLM searching 10M chars for festival information

# Step 1: Use regex + domain knowledge to filter
import re

festival_keywords = ["festival", "La Union", "celebration", "event"]
results = {}

# Only examine chunks containing keywords
for i, chunk in enumerate(context.split('\n')):
    if any(keyword.lower() in chunk.lower() for keyword in festival_keywords):
        results[i] = chunk
        print(f"Found relevant line {i}: {chunk[:100]}...")

# Step 2: Only send filtered content to sub-LLM
relevant_context = '\n'.join(results.values())
answer = llm_query(f"About the festival: {relevant_context}")
```

**Why this matters**: The LLM avoided reading 99.9% of irrelevant content, saving massive cost.

### 2. Recursive Chunking for Dense Tasks

For semantically complex tasks, RLMs chunk intelligently:

```txt
┌────────────────────────────────────────────────────┐
│  Task: Classify 1000 questions semantically        │
└────────────────────────────────────────────────────┘

Instead of:
  ❌ Read all 1000 → Process in one giant prompt

RLM does:
  ✅ Chunk into 100 groups of 10
     ↓
  For each chunk:
     llm_query("Classify these 10 questions...")
     Store results in buffer
     ↓
  Aggregate all buffers → Final answer

  ┌──────┐  ┌──────┐  ┌──────┐     ┌──────┐
  │Chunk1│  │Chunk2│  │Chunk3│ ... │Chunk │
  │ 10Qs │  │ 10Qs │  │ 10Qs │     │100 Qs│
  └──┬───┘  └──┬───┘  └──┬───┘     └──┬───┘
     │         │         │            │
     ▼         ▼         ▼            ▼
   [LLM]    [LLM]    [LLM]     ... [LLM] ← 100 parallel
     │         │         │            │    sub-calls
     ▼         ▼         ▼            ▼
    Res1     Res2      Res3    ...   Res100
     └─────────┴─────────┴──── ... ───┘
                    │
                    ▼
             Aggregate Results
                    │
                    ▼
              Final Answer
```

### 3. Answer Verification Through Sub-Calls

RLMs validate their reasoning:

```python
# Pattern observed in successful RLM runs:

# Step 1: Generate candidate answer
candidate = process_all_chunks(context)

# Step 2: Verify using a fresh sub-call (avoids context rot!)
verification_prompt = f"""
Given this answer: {candidate}

And this evidence: {relevant_excerpts}

Is the answer correct? If not, what should it be?
"""
verified = llm_query(verification_prompt)

# Step 3: Only return if verification passes
if "correct" in verified.lower():
    return candidate
else:
    return extract_corrected_answer(verified)
```

### 4. Variable-Based Assembly for Long Outputs

For tasks requiring long outputs (>10K tokens), RLMs use variables:

```txt
Task: Generate pairs of matching items from 1000 entries
      (Output could be 50K+ tokens!)

RLM Strategy:
  results = []  # Store in Python variable, not token space

  for chunk in chunks:
      pairs = llm_query(f"Find matching pairs in {chunk}")
      results.extend(pairs)  # Accumulate programmatically

  # Output can be arbitrarily long!
  return FINAL_VAR(results)  # Return the variable itself

This bypasses the model's output token limit entirely!
```

### Key Takeaways

- **Zero-shot problem solving**: RLMs develop strategies without task-specific training
- **Model priors + code**: Combining LLM knowledge with programmatic control
- **Self-verification**: Using sub-calls to validate reasoning and avoid errors
- **Unbounded outputs**: Variables enable outputs beyond token limits

---

## When to Use RLMs

### Perfect Use Cases

✅ **Multi-document research**: Synthesizing info from 100+ papers
✅ **Code repository analysis**: Understanding large codebases
✅ **Dense aggregation**: Tasks requiring processing most/all of the input
✅ **Long-horizon reasoning**: Multi-step problems needing deep context

### When to Stick with Base Models

❌ **Short prompts** (<10K tokens): Base models perform slightly better
❌ **Simple retrieval**: Single needle-in-haystack problems
❌ **Speed-critical**: RLMs trade latency for capability
❌ **Fixed budgets**: High variance in cost due to trajectory length

### Cost-Benefit Trade-off

```
┌────────────────────────────────────────────────────────────────┐
│  Performance vs Context Length: When Does RLM Win?             │
└────────────────────────────────────────────────────────────────┘

Performance
    ▲
100%│
    │ ●━━━━━━━━━━━●━━━━━━━━━●━━━━━━━━━●  RLM (stable)
 80%│ ○╲
    │   ○╲
 60%│     ○╲━━━━━━━━━━━━━━━━━━━━━━━━━━━  Base Model (degrades)
    │       ○╲
 40%│         ○╲
    │           ○╲
 20%│             ○╲
    │               ○
  0%│                X  (Base model fails - exceeds 272K limit)
    └────┬──────┬──────┬──────┬──────┬──────┬──────────►
        10K   50K   100K  272K  500K   1M    10M+  Context Size
                           ▲
                           │
                  GPT-5 context limit


DECISION FRAMEWORK (much simpler):

┌──────────────────┬─────────────────┬──────────────────────────┐
│ Scenario         │ Use This        │ Reasoning                │
├──────────────────┼─────────────────┼──────────────────────────┤
│ Short & Simple   │ BASE MODEL      │ RLM overhead not needed  │
│ (<10K tokens,    │                 │ Faster, simpler          │
│ easy task)       │                 │                          │
├──────────────────┼─────────────────┼──────────────────────────┤
│ Short & Complex  │ RLM             │ Dense processing needed  │
│ (<100K tokens,   │                 │ Example: OOLONG-Pairs    │
│ info-dense)      │                 │ 32K tokens, 58% vs 0%    │
├──────────────────┼─────────────────┼──────────────────────────┤
│ Long but Simple  │ BASE MODEL OK   │ If it fits in context    │
│ (100-272K,       │ (RLM better)    │ RLM ~10-20% better       │
│ sparse task)     │                 │                          │
├──────────────────┼─────────────────┼──────────────────────────┤
│ Long & Complex   │ RLM STRONGLY    │ Base model degrades      │
│ (100-272K,       │ RECOMMENDED     │ RLM maintains quality    │
│ dense task)      │                 │                          │
├──────────────────┼─────────────────┼──────────────────────────┤
│ Beyond Limit     │ RLM ONLY        │ Base model cannot run    │
│ (>272K tokens)   │ OPTION          │ No alternative           │
└──────────────────┴─────────────────┴──────────────────────────┘


KEY INSIGHT: Two factors matter:

1. CONTEXT LENGTH
   ├─ Within limit (< 272K): You have a choice
   └─ Beyond limit (> 272K): RLM is the only option

2. TASK COMPLEXITY (if within limit)
   ├─ Simple (find one thing): Base model is fine
   └─ Dense (process everything): RLM wins by a lot
```

---

## The Future of RLMs

The MIT research opens exciting directions:

### 1. Training RLM-Native Models

Current models weren't trained for this workflow. Imagine models explicitly trained to:
- Make efficient chunking decisions
- Minimize redundant sub-calls
- Predict when recursion is needed

### 2. Deeper Recursion Trees

The study used only 1 level of recursion (root → sub-LLM). What about:
```
Root LLM
  ├─ Sub-LLM 1
  │    ├─ Sub-sub-LLM 1.1
  │    └─ Sub-sub-LLM 1.2
  ├─ Sub-LLM 2
  │    └─ Sub-sub-LLM 2.1
  └─ Sub-LLM 3
```

### 3. Asynchronous Processing

Current implementation is sequential. Parallel sub-calls could:
- Reduce latency by 10x+
- Better utilize compute resources
- Enable real-time applications

### 4. Domain-Specific RLMs

Specialized strategies for:
- **Legal**: Case law analysis across thousands of precedents
- **Medical**: Literature review over entire research corpus
- **Code**: Repository-wide refactoring and bug detection

---

## Key Takeaways: The RLM Revolution

1. **Context limits are not fundamental**: RLMs show we can process arbitrarily long inputs through clever inference strategies

2. **Treating prompts as data unlocks new capabilities**: Moving from "all-in-memory" to "programmatic access" is a paradigm shift

3. **Inference-time compute is powerful**: Like test-time compute for reasoning, RLMs show we can scale capability through smarter inference

4. **Emergence without training**: Even unoptimized models develop sophisticated strategies—imagine what trained RLMs could do!

5. **Cost-effective scaling**: Better performance at lower cost proves this isn't just theoretical

---

## Try It Yourself

Want to experiment with RLM-style processing? Here's a starter template:

```python
import anthropic

client = anthropic.Anthropic(api_key="your-key")

def rlm_process(question: str, long_document: str) -> str:
    """Simple RLM-style processing."""

    # 1. Set up the REPL environment context
    system_prompt = f"""You have access to a document with {len(long_document)} characters.
The document is stored in a variable called 'context'.

You can:
- Write Python code to examine parts of it
- Chunk it strategically
- Make sub-queries on specific sections
- Build up your answer incrementally

Think step-by-step and use code to explore the document before answering."""

    # 2. Let the model iterate with code execution
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"""Question: {question}

The document is available as the 'context' variable.
Use code to explore it and build your answer."""
        }]
    )

    return response.content

# Example:
answer = rlm_process(
    "What are the main findings?",
    your_10mb_document
)
```

---

## Further Reading

- 📄 [Original Paper](https://arxiv.org/abs/2512.24601) - Full technical details
- 🔬 [Benchmark Suite](https://github.com/mit-oasys/rlm) - OOLONG, BrowseComp+, etc.
- 💻 [Example Trajectories](https://rlm.csail.mit.edu/examples) - See RLMs in action

---

*This breakdown was created to make cutting-edge AI research accessible. For the complete technical treatment with ablations, prompts, and additional experiments, see the [original paper](https://arxiv.org/abs/2512.24601).*

**Questions or thoughts?** This research has huge implications for how we build AI systems that handle real-world information complexity. What applications would you build with 10M+ token capabilities?
