@{id = "e24bdadd-bd73-43a9-8358-f6cf6e75cf15"
  title = "Training-Free GRPO: Doing RL on the Prompt, Not the Weights"
  date = "2026-05-01T00:00:00Z"
  tags = ['journal club', 'machine learning', 'arxiv', 'language models', 'reinforcement learning', 'agents']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/training-free-grpo-thumb.svg"
  description = "Tencent's Youtu-Agent team adapts GRPO to a frozen LLM by replacing the gradient with a natural-language experience buffer, beating fine-tuned 32B models for around eighteen dollars."
  type = "note"
  disabled = "false"
}

<p align="center">
  <img src="https://storage.googleapis.com/gn-portfolio/images/training-free-grpo-thumb.svg" max-width="700">
</p>


# Training-Free GRPO: Doing RL on the Prompt, Not the Weights

*Analysis of Youtu-Agent Team (2025), arXiv:2510.08191 — preprint*
*Generated on April 29, 2026*

---

## Table of Contents

- [Abstract](#abstract)
- [Introduction](#introduction)
- [Method: Training-Free GRPO](#method-training-free-grpo)
- [Mathematical Reasoning Results](#mathematical-reasoning-results)
- [Web Searching Results](#web-searching-results)
- [Context Space vs Parameter Space](#context-space-vs-parameter-space)
- [Related Work in One Page](#related-work-in-one-page)
- [Conclusion](#conclusion)
- [Key Takeaways (Summary)](#key-takeaways-summary)

---

## Abstract

### Overview

If you have used a large language model agent to do something specialized — say, multi-step web research or contest math with a code interpreter — you have probably felt the gap between a frontier model's *general* capability and its *domain-specific* habits. The model knows how to reason; it just does not know which moves work in your domain, which tools to skip, which sources to trust. The textbook fix is reinforcement learning: collect ground-truth examples, run a few thousand training rollouts, and update the model's weights so high-reward behaviors become more likely. The recipe most teams reach for, made famous by DeepSeek's R1, is **Group Relative Policy Optimization (GRPO)** — a relative of PPO that drops the value-network critic and instead estimates per-output advantage by comparing each sample to the group mean of a small batch of rollouts. It works, and it is now the default tool for "agentic RL".

The Youtu-Agent team at Tencent argue that the *vast majority of GRPO's value is mechanical* — the multi-epoch rollout structure, the group-relative comparison, the iterative refinement — and that the gradient update at the end is one specific way to capture what was learned, not the only way. Their proposal: keep GRPO's structure, but replace the gradient with a natural-language *experience buffer* that gets read into the prompt. They call it **Training-Free GRPO**. The frozen base model takes the role of the policy; an evolving block of plain-text "lessons" takes the role of the learned weights.

The headline numbers are unflattering to the parameter-update orthodoxy. With **about $18** in API spend, **100 training samples**, and **zero gradient updates**, a frozen DeepSeek-V3.1-Terminus reaches **82.7% on AIME24** and **73.3% on AIME25** (Mean@32), beating the best 32B model fine-tuned via vanilla agentic RL — methods like ReTool [arXiv:2504.11536] and AFM [arXiv:2508.13167] that the paper estimates at ~$10K each. Web search gets the same treatment: WebWalkerQA pass@1 climbs from 63.2% to 67.8% with a different 100-sample buffer.

The fine print matters. The method depends on a *strong* base model — running the same recipe on QwQ-32B for web search actually *hurts* performance (-2.0 pass@1). It also depends on the buffer being learned with proper group-relative comparison: an ablation that just dumps directly-generated tips into the prompt gives essentially no gain (79.8% vs 80.0% baseline). The optimization machinery is doing real work; this is not a glorified prompt template.

What's at stake practically: if this generalizes, the cost calculus of building a vertical agent flips. Instead of paying $10K to fine-tune a model you have to host on a fixed-cost GPU cluster, you pay $20 to learn a small block of natural-language lessons (a few dozen entries, on the order of a few KB) that you append to API calls. For low-traffic specialized agents — most enterprise agents, in practice — that is a different business.

### Concept Diagram

<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="abs-diag-title">
  <title id="abs-diag-title">Training-Free GRPO replaces gradient updates with a natural-language experience buffer</title>
  <defs>
    <marker id="abs-arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Two routes from a query to a better next answer</text>
  <!-- Vanilla GRPO row -->
  <text x="40" y="68" font-size="12" font-weight="700" fill="#991b1b">Vanilla GRPO</text>
  <rect x="40" y="78" width="120" height="50" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="100" y="100" text-anchor="middle" font-weight="600" fill="#1e40af">Query q</text>
  <text x="100" y="118" text-anchor="middle" font-size="11" fill="#64748b">+ policy π_θ</text>
  <line x1="160" y1="103" x2="200" y2="103" stroke="#64748b" stroke-width="1.5" marker-end="url(#abs-arrow)"/>
  <rect x="200" y="78" width="120" height="50" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="260" y="100" text-anchor="middle" font-weight="600" fill="#334155">G rollouts</text>
  <text x="260" y="118" text-anchor="middle" font-size="11" fill="#64748b">scored by R</text>
  <line x1="320" y1="103" x2="360" y2="103" stroke="#64748b" stroke-width="1.5" marker-end="url(#abs-arrow)"/>
  <rect x="360" y="78" width="140" height="50" rx="8" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="430" y="100" text-anchor="middle" font-weight="600" fill="#854d0e">Numerical Â_i</text>
  <text x="430" y="118" text-anchor="middle" font-size="11" fill="#854d0e">(r − μ)/σ</text>
  <line x1="500" y1="103" x2="540" y2="103" stroke="#64748b" stroke-width="1.5" marker-end="url(#abs-arrow)"/>
  <rect x="540" y="78" width="140" height="50" rx="8" fill="#fef2f2" stroke="#ef4444" stroke-width="2"/>
  <text x="610" y="100" text-anchor="middle" font-weight="700" fill="#991b1b">Update θ</text>
  <text x="610" y="118" text-anchor="middle" font-size="11" fill="#991b1b">~$10K, GPUs</text>
  <!-- Training-Free GRPO row -->
  <text x="40" y="208" font-size="12" font-weight="700" fill="#166534">Training-Free GRPO</text>
  <rect x="40" y="218" width="120" height="50" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="100" y="240" text-anchor="middle" font-weight="600" fill="#1e40af">Query q</text>
  <text x="100" y="258" text-anchor="middle" font-size="11" fill="#64748b">+ frozen π_θ + E</text>
  <line x1="160" y1="243" x2="200" y2="243" stroke="#64748b" stroke-width="1.5" marker-end="url(#abs-arrow)"/>
  <rect x="200" y="218" width="120" height="50" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="260" y="240" text-anchor="middle" font-weight="600" fill="#334155">G rollouts</text>
  <text x="260" y="258" text-anchor="middle" font-size="11" fill="#64748b">scored by R</text>
  <line x1="320" y1="243" x2="360" y2="243" stroke="#64748b" stroke-width="1.5" marker-end="url(#abs-arrow)"/>
  <rect x="360" y="218" width="140" height="50" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5"/>
  <text x="430" y="240" text-anchor="middle" font-weight="600" fill="#6b21a8">Semantic A_text</text>
  <text x="430" y="258" text-anchor="middle" font-size="11" fill="#6b21a8">LLM introspects</text>
  <line x1="500" y1="243" x2="540" y2="243" stroke="#64748b" stroke-width="1.5" marker-end="url(#abs-arrow)"/>
  <rect x="540" y="218" width="140" height="50" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="610" y="240" text-anchor="middle" font-weight="700" fill="#166534">Update E</text>
  <text x="610" y="258" text-anchor="middle" font-size="11" fill="#166534">~$18, API calls</text>
  <text x="360" y="320" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Same multi-epoch loop. The output of "training" is text the next prompt reads, not weights.</text>
</svg>

### Key Takeaways

- **The gradient was one option, not the only option.** GRPO's structure (group rollouts, relative comparison, multi-epoch refinement) does most of the work; the parameter update is one specific way to commit the lesson.
- **The "advantage" can be a paragraph.** Replacing the scalar Â_i with a natural-language explanation of what worked vs what failed — a *semantic advantage* — keeps the optimization signal interpretable and lets the LLM itself do the credit assignment.
- **Frozen-model RL flips the cost calculus.** $18 + 100 samples beats $10K + thousands of samples when you can use a strong frontier API model as the backbone.
- **It only works when the base is strong.** On weaker bases (QwQ-32B in web search), the same recipe regresses — the method amplifies an already-capable agent rather than teaching one from scratch.

---

## Introduction

### Overview

A short historical arc helps here. Until about 2017, "reinforcement learning for language models" mostly meant REINFORCE-style policy gradients with a learned baseline — high variance, painful to stabilize. **PPO** (Proximal Policy Optimization, Schulman et al. 2017) tamed that variance by clipping the per-step ratio between the new and old policy and adding a value-network critic to estimate per-token advantages. PPO is what powered the original RLHF wave at OpenAI and Anthropic, and it remains the default for instruction tuning.

PPO has a wart, though: the critic. Training a separate value network roughly doubles your active parameter count and adds its own optimization headaches. **GRPO** (Group Relative Policy Optimization), introduced by DeepSeek's mathematical-reasoning work in 2024 and now widely used in DeepSeek's reasoning-model lineage, throws the critic out. Its trick is to sample G outputs for the same prompt, score them all with the reward model, and define each output's advantage *relative to its group's mean and standard deviation*. No critic, no separate value model, just a small batch of rollouts and a normalized score. It is a remarkably clean idea, and it scales.

When the LLM-agents community adopted GRPO, they kept the gradient-update assumption intact. **"Agentic RL"** — as opposed to ordinary fine-tuning — usually means: build a tool-using ReAct loop, generate multi-step trajectories, score the trajectories, then GRPO-update the policy. The result is a domain-specialized model: ReTool for math with code interpreter, AFM for web research, and so on. Each one is good at its domain and worse than the base elsewhere. Each one costs roughly $10K to train and requires a dedicated GPU cluster to serve.

Now consider the cost calculus the paper opens with. Fine-tuning anything bigger than ~32B parameters is essentially out of reach for most teams (compute budget, but also data scarcity — annotated agentic trajectories are scarce). So you fine-tune a smaller model, get a domain-specific gain, but lose to the *general-purpose* frontier model on everything else. Worse, you pay continuous serving costs even when traffic is low. This is the *cost-performance dilemma* the authors put at the center of the paper: API access to a strong frozen model is cheap and elastic, but you can't fine-tune it; smaller models you can fine-tune are inherently weaker.

The paper's pivot is conceptual. The authors note that GRPO's parameter update is just one mechanism for steering the output distribution toward higher-reward behaviors. **In-context learning** — the GPT-3 finding that LLMs adapt their outputs based on prompt content — provides a second mechanism. If we can manufacture a chunk of text that, when prepended to the prompt, has the same effect on the output distribution as a weight update would have, we have built a non-parametric optimizer. They call this chunk the **experiential knowledge buffer** and treat it as the analog of θ. The optimization loop then becomes: roll out, compare, distill what worked into the buffer, repeat.

The "why now" is mundane but real. Two recent shifts make this feasible: (1) frontier API models like DeepSeek-V3.1 became cheap enough per token to run real multi-epoch rollouts via API; (2) those same models became coherent enough at long-context reasoning to play *both* roles in this loop — they are the policy generating rollouts *and* the judge introspecting on them and updating the buffer. Earlier, weaker models couldn't credibly self-introspect; now they can.

### Concept Diagram

<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="intro-diag-title">
  <title id="intro-diag-title">Lineage of policy-gradient methods leading to Training-Free GRPO</title>
  <defs>
    <marker id="intro-arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Lineage: REINFORCE → PPO → GRPO → Training-Free GRPO</text>
  <!-- REINFORCE -->
  <rect x="30" y="80" width="140" height="80" rx="10" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="100" y="108" text-anchor="middle" font-weight="700" fill="#334155">REINFORCE</text>
  <text x="100" y="128" text-anchor="middle" font-size="11" fill="#475569">policy gradient</text>
  <text x="100" y="144" text-anchor="middle" font-size="11" fill="#64748b">high variance</text>
  <line x1="170" y1="120" x2="200" y2="120" stroke="#64748b" stroke-width="1.5" marker-end="url(#intro-arrow)"/>
  <!-- PPO -->
  <rect x="200" y="80" width="140" height="80" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="270" y="108" text-anchor="middle" font-weight="700" fill="#1e40af">PPO</text>
  <text x="270" y="128" text-anchor="middle" font-size="11" fill="#475569">+ critic, + clip</text>
  <text x="270" y="144" text-anchor="middle" font-size="11" fill="#64748b">2017</text>
  <line x1="340" y1="120" x2="370" y2="120" stroke="#64748b" stroke-width="1.5" marker-end="url(#intro-arrow)"/>
  <!-- GRPO -->
  <rect x="370" y="80" width="140" height="80" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="440" y="108" text-anchor="middle" font-weight="700" fill="#1e40af">GRPO</text>
  <text x="440" y="128" text-anchor="middle" font-size="11" fill="#475569">drop critic,</text>
  <text x="440" y="144" text-anchor="middle" font-size="11" fill="#475569">group-relative Â</text>
  <line x1="510" y1="120" x2="540" y2="120" stroke="#64748b" stroke-width="1.5" marker-end="url(#intro-arrow)"/>
  <!-- Training-Free GRPO -->
  <rect x="540" y="80" width="150" height="80" rx="10" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="615" y="108" text-anchor="middle" font-weight="700" fill="#166534">Training-Free</text>
  <text x="615" y="124" text-anchor="middle" font-weight="700" fill="#166534">GRPO</text>
  <text x="615" y="144" text-anchor="middle" font-size="11" fill="#166534">drop gradient</text>
  <!-- Annotations -->
  <text x="100" y="190" text-anchor="middle" font-size="11" fill="#64748b">value baseline</text>
  <text x="270" y="190" text-anchor="middle" font-size="11" fill="#64748b">value network</text>
  <text x="440" y="190" text-anchor="middle" font-size="11" fill="#64748b">no value net</text>
  <text x="615" y="190" text-anchor="middle" font-size="11" fill="#166534" font-weight="600">no parameters</text>
  <!-- What gets updated row -->
  <rect x="30" y="220" width="660" height="50" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5"/>
  <text x="40" y="242" font-size="11" font-weight="600" fill="#6b21a8">Updated by training:</text>
  <text x="100" y="262" text-anchor="middle" font-size="11" fill="#475569">θ (gradient)</text>
  <text x="270" y="262" text-anchor="middle" font-size="11" fill="#475569">θ (gradient)</text>
  <text x="440" y="262" text-anchor="middle" font-size="11" fill="#475569">θ (gradient)</text>
  <text x="615" y="262" text-anchor="middle" font-size="11" fill="#6b21a8" font-weight="700">E (text buffer)</text>
  <text x="360" y="310" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Each step keeps the previous structure and replaces one component. Training-Free GRPO replaces θ.</text>
</svg>

### Key Takeaways

- **GRPO's value is structural.** The group-relative comparison and multi-epoch loop are the parts that move the needle; the gradient was just the implementation.
- **The cost-performance dilemma is real.** Fine-tuning is restricted to small models you can afford to train; the strongest models you can only call via API. Training-Free GRPO targets exactly that gap.
- **Two enabling shifts make this work now.** Cheap frontier API tokens, plus models coherent enough to introspect on their own rollouts.
- **In-context learning is the optimization channel.** A well-crafted prompt prefix can shift the output distribution the same way a weight update can — if you craft it from the right signal.

---

## Method: Training-Free GRPO

### Overview

Before the algorithm, a 1-sentence orientation: a *rollout* is a complete trajectory the agent produces for a given query — every reasoning step, every tool call, every final answer — and a *group* is the set of G rollouts the algorithm samples for the same query, so it can rank them against each other.

Vanilla GRPO produces, for each query q, a group of G outputs {o_1, …, o_G}. Each output gets a scalar reward r_i from a verifier (in math, a check whether the boxed answer is correct; in web search, a graded comparison to a ground-truth answer). The group-relative advantage is Â_i = (r_i − mean(r)) / std(r). The training loss is a PPO-clipped objective over these advantages, with a KL-divergence penalty pulling the policy back toward a fixed reference model. Gradient ascent on θ.

Training-Free GRPO keeps the rollouts and the rewards, but replaces *every step downstream of "I have G rewards"*. The policy is the frozen base model conditioned on an experiential knowledge buffer E — π_θ(o_i | q, E) — where E is plain text, initialized to the empty string. After scoring, the algorithm checks whether the group has both clear winners (correct answers) and clear losers (incorrect answers). If not, the group is skipped (analogous to the std(r) = 0 case in vanilla GRPO, where Â_i = 0). If yes, the LLM itself is asked to (1) summarize each rollout step-by-step, (2) compare them given the ground-truth answer, and (3) extract a *natural-language experience* — a concise piece of advice for what worked or what to avoid. This natural-language object is the **semantic advantage** A_text, the analog of Â_i.

The "optimization step" is then a buffer update. Given the existing E and the new A_text from this batch, the LLM is prompted to emit one of four operations: **Add** a new lesson, **Delete** a lesson that this batch contradicts, **Modify** an existing lesson with new nuance, or **Keep** E unchanged. The buffer typically grows to a few dozen entries — Appendix A of the paper shows a math buffer of 37 lessons (e.g. *"When solving geometry problems with intersections, validate solutions lie within bounded regions"*) and a web-search buffer with similar style.

Two design notes worth pulling out. First, the frozen base model serves the function of the KL constraint in vanilla GRPO: because π_θ never changes, the policy cannot drift arbitrarily far from a coherent base — the buffer can only steer, not corrupt. Second, the same LLM (DeepSeek-V3.1-Terminus in the main experiments) plays three roles: policy that generates rollouts, judge that produces semantic advantages, and optimizer that emits buffer operations. There is no separate critic, no separate reward model, no separate optimizer. It is the same model called with different prompts.

### Concept Diagram

<svg viewBox="0 0 720 460" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="method-diag-title">
  <title id="method-diag-title">One epoch of Training-Free GRPO: rollouts, semantic advantage, buffer update</title>
  <defs>
    <marker id="method-arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">One optimization step</text>
  <!-- Inputs -->
  <rect x="30" y="60" width="170" height="50" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="115" y="82" text-anchor="middle" font-weight="600" fill="#1e40af">Query q + ground truth</text>
  <text x="115" y="100" text-anchor="middle" font-size="11" fill="#64748b">from minimal training set</text>
  <rect x="30" y="130" width="170" height="50" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="115" y="152" text-anchor="middle" font-weight="600" fill="#334155">Frozen π_θ + buffer E</text>
  <text x="115" y="170" text-anchor="middle" font-size="11" fill="#64748b">(E starts empty)</text>
  <line x1="200" y1="120" x2="240" y2="160" stroke="#64748b" stroke-width="1.5" marker-end="url(#method-arrow)"/>
  <line x1="200" y1="155" x2="240" y2="170" stroke="#64748b" stroke-width="1.5" marker-end="url(#method-arrow)"/>
  <!-- G rollouts -->
  <rect x="240" y="120" width="180" height="80" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="330" y="146" text-anchor="middle" font-weight="600" fill="#334155">Sample G rollouts</text>
  <text x="330" y="166" text-anchor="middle" font-size="11" fill="#64748b">o_1, o_2, …, o_G</text>
  <text x="330" y="184" text-anchor="middle" font-size="11" fill="#64748b">score each: r_1, …, r_G</text>
  <line x1="420" y1="160" x2="460" y2="160" stroke="#64748b" stroke-width="1.5" marker-end="url(#method-arrow)"/>
  <!-- Semantic advantage -->
  <rect x="460" y="120" width="220" height="80" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="2"/>
  <text x="570" y="146" text-anchor="middle" font-weight="700" fill="#6b21a8">Semantic advantage A_text</text>
  <text x="570" y="166" text-anchor="middle" font-size="11" fill="#6b21a8">"the winners did X;</text>
  <text x="570" y="182" text-anchor="middle" font-size="11" fill="#6b21a8">losers got stuck on Y"</text>
  <!-- Skip note -->
  <rect x="240" y="220" width="180" height="36" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="330" y="244" text-anchor="middle" font-size="11" fill="#991b1b" font-style="italic">skip group if all win or all fail</text>
  <!-- Buffer update -->
  <line x1="570" y1="200" x2="570" y2="290" stroke="#64748b" stroke-width="1.5" marker-end="url(#method-arrow)"/>
  <rect x="430" y="290" width="280" height="100" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="570" y="316" text-anchor="middle" font-weight="700" fill="#166534">Update buffer E</text>
  <text x="450" y="340" font-size="11" fill="#166534">• Add — new lesson</text>
  <text x="450" y="356" font-size="11" fill="#166534">• Delete — drop a stale lesson</text>
  <text x="450" y="372" font-size="11" fill="#166534">• Modify — refine wording</text>
  <text x="450" y="388" font-size="11" fill="#166534">• Keep — no change</text>
  <!-- Loop arrow back -->
  <path d="M 430 340 Q 280 340 200 240 Q 100 230 100 180" stroke="#22c55e" stroke-width="2" fill="none" stroke-dasharray="6,4" marker-end="url(#method-arrow)"/>
  <text x="160" y="280" font-size="11" fill="#166534" font-style="italic">next batch reads</text>
  <text x="160" y="296" font-size="11" fill="#166534" font-style="italic">updated E</text>
  <text x="360" y="430" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Same LLM plays three roles: policy (rollouts), judge (A_text), and optimizer (buffer ops).</text>
</svg>

### Try It Yourself

Group size G is the parameter that gives Training-Free GRPO its name. The whole point of "group relative" is that comparing rollouts against each other generates a useful contrast — a judgment of why one path worked and another did not. With G = 1 there is nothing to compare to (and the paper's ablation confirms this collapses the gain). The interesting question is how large G needs to be before the contrast saturates. Click through to feel it:

<style>
  .ptb-step-grpo { border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px 20px; margin: 16px 0; background: #f8fafc; }
  .ptb-step-grpo .ptb-label-grpo { display: block; font-size: 13px; color: #475569; margin-bottom: 8px; font-weight: 600; }
  .ptb-step-grpo .ptb-buttons-grpo { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
  .ptb-step-grpo input[type="radio"] { display: none; }
  .ptb-step-grpo .ptb-btn-grpo {
    padding: 6px 14px; border: 1px solid #cbd5e1; border-radius: 6px;
    cursor: pointer; font-size: 13px; font-weight: 600; color: #475569;
    background: #ffffff; user-select: none;
  }
  .ptb-step-grpo .ptb-btn-grpo:hover { border-color: #3b82f6; color: #1e40af; }
  .ptb-step-grpo .ptb-state-grpo { display: none; }

  .ptb-step-grpo input#g-1:checked ~ .ptb-buttons-grpo label[for="g-1"],
  .ptb-step-grpo input#g-2:checked ~ .ptb-buttons-grpo label[for="g-2"],
  .ptb-step-grpo input#g-5:checked ~ .ptb-buttons-grpo label[for="g-5"],
  .ptb-step-grpo input#g-8:checked ~ .ptb-buttons-grpo label[for="g-8"] {
    background: #eff6ff; border-color: #3b82f6; color: #1e40af;
  }
  .ptb-step-grpo input#g-1:checked ~ #g-s1,
  .ptb-step-grpo input#g-2:checked ~ #g-s2,
  .ptb-step-grpo input#g-5:checked ~ #g-s5,
  .ptb-step-grpo input#g-8:checked ~ #g-s8 { display: block; }
</style>

<div class="ptb-step-grpo">
  <span class="ptb-label-grpo">Group size G — how many rollouts per query before extracting a lesson:</span>

  <input type="radio" name="grpo-g" id="g-1">
  <input type="radio" name="grpo-g" id="g-2">
  <input type="radio" name="grpo-g" id="g-5" checked>
  <input type="radio" name="grpo-g" id="g-8">

  <div class="ptb-buttons-grpo">
    <label for="g-1" class="ptb-btn-grpo">G = 1</label>
    <label for="g-2" class="ptb-btn-grpo">G = 2</label>
    <label for="g-5" class="ptb-btn-grpo">G = 5 (paper)</label>
    <label for="g-8" class="ptb-btn-grpo">G = 8</label>
  </div>

  <div class="ptb-state-grpo" id="g-s1">
    <svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="g-s1-title">
      <title id="g-s1-title">G=1: one rollout, no contrast available</title>
      <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#991b1b">G = 1 — no group, no contrast</text>
      <rect x="220" y="50" width="160" height="50" rx="8" fill="#f1f5f9" stroke="#94a3b8"/>
      <text x="300" y="74" text-anchor="middle" font-weight="600" fill="#334155">Rollout 1</text>
      <text x="300" y="92" text-anchor="middle" font-size="11" fill="#64748b">no peer to compare</text>
      <rect x="160" y="130" width="280" height="50" rx="8" fill="#fef2f2" stroke="#ef4444"/>
      <text x="300" y="154" text-anchor="middle" font-weight="700" fill="#991b1b">No semantic advantage</text>
      <text x="300" y="172" text-anchor="middle" font-size="11" fill="#991b1b">Ablation: gains collapse vs G = 5</text>
      <text x="300" y="206" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Self-reflection on a single trajectory loses the relative signal.</text>
    </svg>
  </div>

  <div class="ptb-state-grpo" id="g-s2">
    <svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="g-s2-title">
      <title id="g-s2-title">G=2: minimal contrast, often degenerate</title>
      <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#854d0e">G = 2 — minimal but fragile</text>
      <rect x="100" y="50" width="160" height="50" rx="8" fill="#f0fdf4" stroke="#22c55e"/>
      <text x="180" y="74" text-anchor="middle" font-weight="600" fill="#166534">Rollout 1 (correct)</text>
      <rect x="340" y="50" width="160" height="50" rx="8" fill="#fef2f2" stroke="#ef4444"/>
      <text x="420" y="74" text-anchor="middle" font-weight="600" fill="#991b1b">Rollout 2 (wrong)</text>
      <rect x="160" y="130" width="280" height="50" rx="8" fill="#fefce8" stroke="#eab308"/>
      <text x="300" y="154" text-anchor="middle" font-weight="700" fill="#854d0e">Thin signal</text>
      <text x="300" y="172" text-anchor="middle" font-size="11" fill="#854d0e">often both right or both wrong → skip</text>
      <text x="300" y="206" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Many groups have std(r) = 0 and yield no lesson.</text>
    </svg>
  </div>

  <div class="ptb-state-grpo" id="g-s5">
    <svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="g-s5-title">
      <title id="g-s5-title">G=5: enough contrast for a stable lesson</title>
      <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#166534">G = 5 — paper's setting (math)</text>
      <rect x="40"  y="50" width="100" height="40" rx="6" fill="#f0fdf4" stroke="#22c55e"/>
      <text x="90"  y="75" text-anchor="middle" font-size="11" fill="#166534">correct</text>
      <rect x="160" y="50" width="100" height="40" rx="6" fill="#f0fdf4" stroke="#22c55e"/>
      <text x="210" y="75" text-anchor="middle" font-size="11" fill="#166534">correct</text>
      <rect x="280" y="50" width="100" height="40" rx="6" fill="#fef2f2" stroke="#ef4444"/>
      <text x="330" y="75" text-anchor="middle" font-size="11" fill="#991b1b">wrong</text>
      <rect x="400" y="50" width="100" height="40" rx="6" fill="#fef2f2" stroke="#ef4444"/>
      <text x="450" y="75" text-anchor="middle" font-size="11" fill="#991b1b">wrong</text>
      <rect x="520" y="50" width="60"  height="40" rx="6" fill="#fef2f2" stroke="#ef4444"/>
      <text x="550" y="75" text-anchor="middle" font-size="11" fill="#991b1b">wrong</text>
      <rect x="100" y="130" width="400" height="50" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
      <text x="300" y="154" text-anchor="middle" font-weight="700" fill="#166534">Rich contrast</text>
      <text x="300" y="172" text-anchor="middle" font-size="11" fill="#166534">winners and losers in most groups → most groups produce a lesson</text>
      <text x="300" y="206" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Paper used G = 5 for math, G = 3 for web search.</text>
    </svg>
  </div>

  <div class="ptb-state-grpo" id="g-s8">
    <svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="g-s8-title">
      <title id="g-s8-title">G=8: more contrast, but cost grows linearly</title>
      <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1e40af">G = 8 — diminishing returns, higher cost</text>
      <g>
        <rect x="20"  y="50" width="60" height="40" rx="6" fill="#f0fdf4" stroke="#22c55e"/>
        <rect x="90"  y="50" width="60" height="40" rx="6" fill="#f0fdf4" stroke="#22c55e"/>
        <rect x="160" y="50" width="60" height="40" rx="6" fill="#f0fdf4" stroke="#22c55e"/>
        <rect x="230" y="50" width="60" height="40" rx="6" fill="#fef2f2" stroke="#ef4444"/>
        <rect x="300" y="50" width="60" height="40" rx="6" fill="#fef2f2" stroke="#ef4444"/>
        <rect x="370" y="50" width="60" height="40" rx="6" fill="#fef2f2" stroke="#ef4444"/>
        <rect x="440" y="50" width="60" height="40" rx="6" fill="#fef2f2" stroke="#ef4444"/>
        <rect x="510" y="50" width="60" height="40" rx="6" fill="#fef2f2" stroke="#ef4444"/>
      </g>
      <rect x="80" y="130" width="440" height="50" rx="8" fill="#eff6ff" stroke="#3b82f6"/>
      <text x="300" y="154" text-anchor="middle" font-weight="700" fill="#1e40af">Saturating contrast</text>
      <text x="300" y="172" text-anchor="middle" font-size="11" fill="#1e40af">marginal extra signal · linear extra API cost</text>
      <text x="300" y="206" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Paper does not directly ablate G beyond 5; budget caps the natural choice.</text>
    </svg>
  </div>
</div>

### Implementation

A minimal sketch of the inner loop. This is a faithful translation of the paper's pseudocode in §2 — same structure, abbreviated for readability. It does not run as-is (it expects a stub `LLM` interface and a reward function), but the shapes and step structure are correct.

```python
from dataclasses import dataclass, field

@dataclass
class TrainingFreeGRPO:
    """One epoch of Training-Free GRPO over a small training set.

    Faithful sketch of Algorithm in Youtu-Agent (2025), §2. The same
    LLM is reused as policy (rollouts), judge (semantic advantage),
    and optimizer (buffer ops). No gradient is computed anywhere.

    The buffer E starts empty and grows into a few-dozen-line block
    of natural-language lessons that the next epoch's rollouts read.
    """
    llm: "LLM"                              # frontier API client
    reward_fn: callable                     # scores one trajectory
    group_size: int = 5                     # paper used G=5 (math), G=3 (web)
    experience: list[str] = field(default_factory=list)

    def step(self, query: str, ground_truth: str) -> None:
        # 1. Roll out G trajectories conditioned on the current buffer.
        prompt = f"{self._render_buffer()}\n\nQuestion: {query}"
        rollouts = [self.llm.complete(prompt) for _ in range(self.group_size)]

        # 2. Score each rollout. In math, this is exact-match on the boxed
        #    answer; in web search, the agent's answer is graded vs gt.
        rewards = [self.reward_fn(r, ground_truth) for r in rollouts]

        # 3. Skip groups with no contrast — same as Â_i = 0 when std(r) = 0.
        if min(rewards) == max(rewards):
            return

        # 4. Semantic advantage: have the LLM compare winners and losers,
        #    extract one lesson in plain text. This is A_text in the paper.
        a_text = self.llm.judge(
            query=query,
            rollouts=rollouts,
            rewards=rewards,
            ground_truth=ground_truth,
            existing_buffer=self._render_buffer(),
        )

        # 5. Buffer update: ask the LLM to emit Add / Delete / Modify / Keep
        #    operations on the current buffer given the new advantage.
        ops = self.llm.optimize_buffer(
            buffer=self.experience,
            new_advantage=a_text,
        )
        self._apply(ops)

    def _render_buffer(self) -> str:
        if not self.experience:
            return ""
        lines = "\n".join(f"[{i+1}] {e}" for i, e in enumerate(self.experience))
        return f"Useful experiences from prior problems:\n{lines}"

    def _apply(self, ops: list[dict]) -> None:
        # ops example: [{"type": "add", "text": "Verify rectangle..."}, ...]
        for op in ops:
            match op["type"]:
                case "add":    self.experience.append(op["text"])
                case "delete": self.experience.pop(op["index"])
                case "modify": self.experience[op["index"]] = op["text"]
                case "keep":   pass
```

### Key Takeaways

- **The structure is GRPO; only the update rule changes.** Group rollouts, group-relative comparison, multi-epoch refinement — all preserved. Gradient ascent on θ becomes natural-language ops on E.
- **Skipping the no-contrast groups is critical.** When all G rollouts get the same reward there is no signal — the algorithm declines to fabricate a lesson, mirroring vanilla GRPO's std(r) = 0 case.
- **The base model serves as the KL anchor.** Because π_θ never moves, the buffer can only steer its prompts within the model's coherent behavior space; unlike weight-tuning, this method cannot "break" the model.
- **One LLM, three hats.** Same model is policy, judge, and optimizer. The savings come from not having to host a separate reward model or critic.

---

## Mathematical Reasoning Results

### Overview

A quick orientation for the unfamiliar reader: AIME (American Invitational Mathematics Examination) is a 15-question competition for high school students; the AIME24 and AIME25 sets used here are the official problem batches from those years. They are short-answer integer problems requiring multi-step proof-style reasoning. **Mean@32** is the average accuracy across 32 independent runs of the same problem — useful because LLMs at non-zero temperature give different answers across runs, and a single-shot Pass@1 is noisy.

The setup: train on **DAPO-100**, a random sample of 100 problems from the DAPO-Math-17K dataset. 3 epochs, single batch per epoch (so 3 optimization steps total), G = 5, temperature 0.7 during training, 0.3 at evaluation. The base model is **DeepSeek-V3.1-Terminus** (671B total parameters, MoE; called via API), evaluated in two configurations — *Direct* (prompt-only, no tools) and *ReAct* (with a Python code interpreter as a tool).

The headline numbers (Mean@32):

| Configuration | AIME24 | AIME25 |
| --- | --- | --- |
| Direct | 68.6% | 52.9% |
| Direct + Training-Free GRPO | 72.6% (+4.0) | 54.0% (+1.1) |
| ReAct | 80.0% | 67.9% |
| ReAct + Training-Free GRPO | **82.7% (+2.7)** | **73.3% (+5.4)** |

Three things to register. First, the gains transfer to a different base — DeepSeek-V3.2-Exp also improves (+2.1, +1.4 on the same benchmarks). Second, the gains transfer to *smaller* bases too, suggesting the method isn't purely a frontier-model phenomenon: Qwen3-32B Non-Thinking gets +4.4 / +5.9, Qwen2.5-72B-Instruct gets +1.4 / +1.8. Third, and this is the loudest finding, the absolute number 82.7% on AIME24 *beats* fully fine-tuned 32B models like ReTool (67.0%) and AFM (66.7%) that cost ~$10K to train — and it does so with $18 of API spend.

The ablations make the case that the optimization machinery is what matters, not just having a longer prompt. The most pointed one: prepending experiences *directly generated* by DeepSeek-V3.1-Terminus (the paper asks the model to produce a list of useful experiences, matched in quantity to what Training-Free GRPO learned) gives **79.8%** — basically identical to the 80.0% baseline. The same model, the same kind of content, but produced without the rollout-then-distill loop, gives no gain. It is the iterative comparison against ground truth that earns the +2.7. A second ablation removes ground truth entirely (the LLM has to compare rollouts against each other only, leveraging implicit majority voting / self-consistency) and recovers most but not all of the gain — 80.7% / 68.9%, still meaningfully above baseline. A third sets G = 1, eliminating the group, and gains collapse — confirming the relative comparison is load-bearing, not just the buffer mechanism.

A subtler observation from Figure 4 of the paper: across the 3 learning steps, the **average number of tool calls per problem decreases** even though accuracy rises. The buffer doesn't just teach the agent which moves are correct — it teaches it which tool calls are wasted. That dual effect (more correct, more efficient) is consistent with what an experienced practitioner internalizes after solving many problems.

### Concept Diagram

<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="math-diag-title">
  <title id="math-diag-title">AIME accuracy and learning cost: Training-Free GRPO vs fine-tuned 32B models</title>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">AIME24 Mean@32 vs learning cost</text>
  <text x="360" y="42" text-anchor="middle" font-size="11" fill="#64748b">Higher and further left is better</text>
  <!-- Header -->
  <text x="240" y="72" text-anchor="end" font-size="11" fill="#64748b" font-weight="600">Method</text>
  <text x="680" y="72" text-anchor="end" font-size="11" fill="#64748b" font-weight="600">AIME24 (%)</text>
  <!-- Bar 1: TF-GRPO winner -->
  <text x="240" y="102" text-anchor="end" fill="#334155" font-size="12">TF-GRPO + DeepSeek-V3.1-T (671B, frozen)</text>
  <rect x="250" y="90" width="386" height="22" rx="4" fill="#22c55e" opacity="0.8"/>
  <text x="644" y="106" font-size="11" fill="#166534" font-weight="700">82.7 · ~$18 ✓</text>
  <!-- Bar 2: ReAct baseline same model -->
  <text x="240" y="134" text-anchor="end" fill="#334155" font-size="12">ReAct + DeepSeek-V3.1-T (no learning)</text>
  <rect x="250" y="122" width="373" height="22" rx="4" fill="#3b82f6" opacity="0.6"/>
  <text x="630" y="138" font-size="11" fill="#1e40af">80.0 · $0</text>
  <!-- Bar 3: ReTool 32B -->
  <text x="240" y="166" text-anchor="end" fill="#334155" font-size="12">ReTool — fine-tuned Qwen2.5-32B</text>
  <rect x="250" y="154" width="313" height="22" rx="4" fill="#94a3b8" opacity="0.55"/>
  <text x="570" y="170" font-size="11" fill="#64748b">67.0 · ~$10K</text>
  <!-- Bar 4: AFM 32B -->
  <text x="240" y="198" text-anchor="end" fill="#334155" font-size="12">AFM — fine-tuned Qwen2.5-32B</text>
  <rect x="250" y="186" width="311" height="22" rx="4" fill="#94a3b8" opacity="0.55"/>
  <text x="570" y="202" font-size="11" fill="#64748b">66.7 · ~$10K</text>
  <!-- Bar 5: SimpleTIR 32B -->
  <text x="240" y="230" text-anchor="end" fill="#334155" font-size="12">SimpleTIR — fine-tuned Qwen2.5-32B</text>
  <rect x="250" y="218" width="280" height="22" rx="4" fill="#94a3b8" opacity="0.4"/>
  <text x="540" y="234" font-size="11" fill="#64748b">59.9 · ~$20K</text>
  <!-- Bar 6: ZeroTIR -->
  <text x="240" y="262" text-anchor="end" fill="#334155" font-size="12">ZeroTIR — fine-tuned Qwen2.5-32B</text>
  <rect x="250" y="250" width="265" height="22" rx="4" fill="#ef4444" opacity="0.4"/>
  <text x="525" y="266" font-size="11" fill="#dc2626">56.7 · ~$20K</text>
  <!-- Caption -->
  <rect x="60" y="290" width="600" height="46" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
  <text x="360" y="312" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">A frozen 671B model + a $18 prompt buffer beats every fine-tuned 32B model in this slate.</text>
  <text x="360" y="328" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Source: Tables 1 and 3 of the paper.</text>
</svg>

### Key Takeaways

- **+2.7 on AIME24, +5.4 on AIME25 with ReAct** — 100 training examples, 3 epochs, no gradient updates, ~$18 in API spend.
- **The frozen 671B beats fine-tuned 32Bs.** The headline 82.7% on AIME24 is higher than ReTool, AFM, SimpleTIR, ZeroTIR — every fine-tuned 32B in the paper's slate.
- **Direct experience-prompting is not enough.** Pasting in directly-generated tips (matched in quantity) gives 79.8% — essentially the baseline. The optimization loop is what creates the +2.7.
- **The agent learns to call fewer tools.** Average tool calls per problem decrease over the 3 training steps even as accuracy rises — the buffer teaches efficiency too.
- **G = 1 collapses the gain.** Removing the group breaks the method, confirming that *relative* comparison among rollouts is the load-bearing component.

---

## Web Searching Results

### Overview

Before the numbers: **WebWalkerQA** [arXiv:2501.07572] is a benchmark that gives an agent a real web environment plus a natural-language question whose answer requires navigating, clicking, reading, and synthesizing across multiple pages. The reward is whether the final answer matches ground truth. Pass@1 is single-trajectory accuracy; pass@3 is success-among-three-attempts. **AFM-100** is 100 queries randomly sampled from the AFM (Chain-of-Agents) web-RL training corpus.

Same recipe, different domain. 3 epochs, group size G = 3 (smaller than math because web rollouts are more expensive), DeepSeek-V3.1-Terminus, ReAct loop with web tools.

| Configuration | pass@1 | pass@3 |
| --- | --- | --- |
| ReAct (baseline) | 63.2% (full set) / 66.7% (51-instance subset) | 74.5% (subset) |
| + Directly generated experiences | — / 64.7% | 76.5% |
| + TF-GRPO (no ground truth) | — / 66.7% | 78.4% |
| + TF-GRPO (full) | **67.8% (full) / 68.6% (subset)** | **78.4% (subset)** |

The +4.6 pass@1 on the full WebWalkerQA set (63.2% → 67.8%) confirms the method generalizes beyond math. The same shape of ablation holds: directly-generated experiences fail (64.7%, slightly *below* baseline), confirming that the optimization is not just "longer prompt = better". And the no-ground-truth variant matches baseline pass@1 but lifts pass@3 to 78.4%, suggesting that even without explicit verification, the LLM-on-LLM relative comparison improves the *consistency* of the agent across attempts.

The buffer the method learns for web search reads like the inside of a research analyst's head. Examples from the paper's Appendix A.2: *"Prioritize systematic extraction from authoritative comprehensive documents over fragmented information for coherent topic coverage"* (Source prioritization), *"Continuously refine search terms based on emerging patterns while periodically re-evaluating previously encountered information"* (Iterative refinement), *"Focus on extracting formal titles and collection names from official metadata and headers rather than inferring relationships from content descriptions"* (Document identification). These are tactical, transferable, and not the kind of thing you would write down a priori — they emerge from comparing successful and failed rollouts on actual queries.

The discordant note: **applying TF-GRPO to QwQ-32B drops pass@1 from 27.5% to 25.5%** — the ablated 32B model regresses below its own ReAct baseline. The authors attribute this to the underlying capability ceiling: the buffer adds advice the model still cannot follow because its reasoning and tool-use foundations are too weak. Pass@3 on QwQ-32B does improve (43.1% → 45.1%), so the method is not pure noise on the smaller model — but the pass@1 regression is a real failure mode and worth taking seriously when planning to apply this to a smaller-base agent.

### Concept Diagram

<svg viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="web-diag-title">
  <title id="web-diag-title">WebWalkerQA pass@1 by configuration on the 51-instance subset</title>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">WebWalkerQA — what the buffer adds vs the prompt alone</text>
  <text x="360" y="42" text-anchor="middle" font-size="11" fill="#64748b">Stratified 51-instance subset, 2 epochs, DeepSeek-V3.1-Terminus, pass@1 (%)</text>
  <!-- Header -->
  <text x="320" y="74" text-anchor="end" font-size="11" fill="#64748b" font-weight="600">Configuration</text>
  <text x="660" y="74" text-anchor="end" font-size="11" fill="#64748b" font-weight="600">pass@1</text>
  <!-- TF-GRPO full -->
  <text x="320" y="104" text-anchor="end" fill="#334155" font-size="12">TF-GRPO (full, with ground truth)</text>
  <rect x="330" y="92" width="290" height="22" rx="4" fill="#22c55e" opacity="0.8"/>
  <text x="630" y="108" font-size="11" fill="#166534" font-weight="700">68.6 ✓</text>
  <!-- TF-GRPO no GT -->
  <text x="320" y="136" text-anchor="end" fill="#334155" font-size="12">TF-GRPO (without ground truth)</text>
  <rect x="330" y="124" width="282" height="22" rx="4" fill="#3b82f6" opacity="0.65"/>
  <text x="622" y="140" font-size="11" fill="#1e40af">66.7</text>
  <!-- ReAct baseline -->
  <text x="320" y="168" text-anchor="end" fill="#334155" font-size="12">ReAct (no buffer)</text>
  <rect x="330" y="156" width="282" height="22" rx="4" fill="#94a3b8" opacity="0.55"/>
  <text x="622" y="172" font-size="11" fill="#64748b">66.7</text>
  <!-- Direct experiences -->
  <text x="320" y="200" text-anchor="end" fill="#334155" font-size="12">Directly-generated experiences</text>
  <rect x="330" y="188" width="274" height="22" rx="4" fill="#ef4444" opacity="0.5"/>
  <text x="614" y="204" font-size="11" fill="#dc2626">64.7 ✗</text>
  <!-- QwQ regression -->
  <text x="320" y="232" text-anchor="end" fill="#334155" font-size="12">TF-GRPO on QwQ-32B (weaker base)</text>
  <rect x="330" y="220" width="108" height="22" rx="4" fill="#ef4444" opacity="0.6"/>
  <text x="448" y="236" font-size="11" fill="#dc2626" font-weight="600">25.5 (regresses)</text>
  <!-- Caption -->
  <rect x="60" y="262" width="600" height="46" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
  <text x="360" y="284" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Direct prompt-injection of tips slightly hurts. The optimization-derived buffer wins by ~2 points.</text>
  <text x="360" y="300" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">On a weaker base (QwQ-32B) the same recipe regresses below baseline.</text>
</svg>

### Key Takeaways

- **+4.6 pass@1 on WebWalkerQA** (63.2% → 67.8%) on the full benchmark — same recipe as math, different buffer.
- **Directly-injected tips slightly hurt.** 64.7% vs 66.7% baseline on the subset confirms the optimization-distilled buffer is qualitatively different from a hand-written tips list.
- **The buffer captures real research craft.** "Prioritize primary sources", "extract exact official quotes", "iterate from broad to targeted queries" — tactical knowledge that emerges from comparing trajectories.
- **No-ground-truth variant lifts pass@3.** Even without verification, the relative comparison between rollouts pushes consistency up (74.5% → 78.4% pass@3).
- **Weaker base = regression risk.** QwQ-32B drops 27.5% → 25.5% pass@1; the method amplifies a capable agent and hurts an incapable one.

---

## Context Space vs Parameter Space

### Overview

The most damaging comparison in the paper is the cross-domain transfer table. Take ReTool, fine-tuned via PPO on math; it scores 67.0% on AIME24 (good, in-domain) and **18.3% on WebWalker** (worse than the un-tuned ReAct baseline of 31.9% on the same model). Take MiroThinker, fine-tuned for web research; it scores 53.6% on WebWalker but only 43.5% on AIME24. Each fine-tuned specialist trades cross-domain capability for in-domain gains.

Training-Free GRPO does not have this trade-off because the model never changes — only the buffer does. The authors maintain *two* buffers, one for math, one for web search, and plug whichever is appropriate into the prompt. The frozen DeepSeek-V3.1-Terminus then scores 82.7% on AIME24 *and* 67.8% on WebWalker — best in both columns simultaneously. A weight-tuned model is one specialist; a frozen-base + buffer system is N specialists for the cost of N text files.

The compute cost story is even more lopsided. ReTool's reported training cost is roughly **20K GPU-hours × $0.50 = ~$10K**, plus a dedicated 32B model deployment. Training-Free GRPO with DeepSeek-V3.1-Terminus takes **6 hours** to run 3 steps on 100 samples, consuming **38M input tokens + 6.6M output tokens ≈ $18** at DeepSeek's pricing (most input qualifies for cache-hit pricing because the prompt prefix is reused across rollouts). That is a three-orders-of-magnitude reduction in training cost.

Inference cost is the one place fine-tuning has an edge — but only conditionally. ReTool-32B running on a 4×GPU vLLM server at $0.50/GPU-hour processes ~400 problems/hour, costing about **$0.005 per problem** *if you can keep the GPUs saturated*. Training-Free GRPO via API is **~$0.02 per problem** (60K input + 8K output tokens at cache-hit pricing). Per-call, the API is 4× more expensive. But the API has zero fixed serving cost: you pay $0 when there is no traffic. Most enterprise agentic deployments have spiky, low-volume traffic — the kind where a dedicated GPU sits idle most of the day. The break-even is roughly: if you would have utilized a 4-GPU cluster less than ~25% of the time, the API model is cheaper *in total*.

### Concept Diagram

<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="cmp-diag-title">
  <title id="cmp-diag-title">Cross-domain capability of fine-tuned specialists vs Training-Free GRPO</title>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Cross-domain transfer (Pass@1, %)</text>
  <text x="360" y="42" text-anchor="middle" font-size="11" fill="#64748b">Each method's score in its trained domain (in-domain) vs the other domain (off-domain)</text>
  <!-- Header -->
  <text x="220" y="76" text-anchor="end" font-size="11" fill="#64748b" font-weight="600">Method (trained on)</text>
  <text x="380" y="76" text-anchor="middle" font-size="11" fill="#64748b" font-weight="600">AIME24</text>
  <text x="540" y="76" text-anchor="middle" font-size="11" fill="#64748b" font-weight="600">WebWalker</text>
  <!-- ReTool (Math) -->
  <text x="220" y="106" text-anchor="end" fill="#334155" font-size="12">ReTool — Math specialist</text>
  <rect x="320" y="94" width="120" height="22" rx="4" fill="#22c55e" opacity="0.7"/>
  <text x="385" y="110" text-anchor="middle" font-size="11" fill="#166534" font-weight="700">67.0</text>
  <rect x="480" y="94" width="33"  height="22" rx="4" fill="#ef4444" opacity="0.55"/>
  <text x="545" y="110" text-anchor="middle" font-size="11" fill="#dc2626" font-weight="600">18.3 ✗</text>
  <!-- MiroThinker (Web) -->
  <text x="220" y="138" text-anchor="end" fill="#334155" font-size="12">MiroThinker — Web specialist</text>
  <rect x="320" y="126" width="78"  height="22" rx="4" fill="#eab308" opacity="0.55"/>
  <text x="385" y="142" text-anchor="middle" font-size="11" fill="#854d0e">43.5 ◐</text>
  <rect x="480" y="126" width="96"  height="22" rx="4" fill="#22c55e" opacity="0.65"/>
  <text x="545" y="142" text-anchor="middle" font-size="11" fill="#166534" font-weight="700">53.6</text>
  <!-- ReAct base 32B for context -->
  <text x="220" y="170" text-anchor="end" fill="#334155" font-size="12">ReAct (Qwen2.5-32B, no train)</text>
  <rect x="320" y="158" width="53"  height="22" rx="4" fill="#94a3b8" opacity="0.5"/>
  <text x="385" y="174" text-anchor="middle" font-size="11" fill="#64748b">29.6</text>
  <rect x="480" y="158" width="57"  height="22" rx="4" fill="#94a3b8" opacity="0.5"/>
  <text x="545" y="174" text-anchor="middle" font-size="11" fill="#64748b">31.9</text>
  <!-- TF-GRPO -->
  <text x="220" y="202" text-anchor="end" fill="#334155" font-size="12">TF-GRPO + DeepSeek-V3.1-T (Math + Web)</text>
  <rect x="320" y="190" width="149" height="22" rx="4" fill="#22c55e" opacity="0.85"/>
  <text x="385" y="206" text-anchor="middle" font-size="11" fill="#166534" font-weight="700">82.7 ✓</text>
  <rect x="480" y="190" width="121" height="22" rx="4" fill="#22c55e" opacity="0.85"/>
  <text x="545" y="206" text-anchor="middle" font-size="11" fill="#166534" font-weight="700">67.8 ✓</text>
  <!-- Caption -->
  <rect x="60" y="240" width="600" height="100" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
  <text x="360" y="262" text-anchor="middle" font-size="12" fill="#1e293b" font-weight="600">Domain specialization is a trade — context-space optimization avoids it.</text>
  <text x="80" y="284" font-size="11" fill="#475569">• ReTool (math) collapses to 18.3% on web — worse than the un-tuned base (31.9%).</text>
  <text x="80" y="302" font-size="11" fill="#475569">• MiroThinker (web) loses ~10 points on AIME relative to a math-trained 32B.</text>
  <text x="80" y="320" font-size="11" fill="#475569">• TF-GRPO is best in both columns by swapping the buffer, not the model.</text>
</svg>

### Key Takeaways

- **Specialization is a trade in parameter space.** Fine-tuned math models lose at web (ReTool: 67.0 → 18.3); fine-tuned web models lose at math.
- **Specialization is free in context space.** Two buffers, one frozen model — best-in-class on both AIME and WebWalker simultaneously.
- **Three orders of magnitude cheaper to train.** ~$18 vs ~$10K. 6 hours and 100 samples vs 20K GPU-hours and thousands of samples.
- **Inference economics flip on traffic shape.** Per-call API cost is ~4× higher; total cost is *lower* for any deployment with under-25% utilization.
- **No specialist deployments.** A dedicated GPU cluster per fine-tuned model becomes one shared API endpoint plus a folder of buffer files.

---

## Related Work in One Page

### Overview

The paper's place in the landscape is worth pinning down. Three lines converge here.

**Line 1 — agentic RL.** Started with ReAct (interleave reasoning and acting), formalized by GRPO and its derivatives (DAPO, GSPO, GiGPO), instantiated for tool use by ReTool, AFM, Tongyi DeepResearch, and similar systems. All of these update model weights.

**Line 2 — training-free / in-context methods.** GPT-3 demonstrated few-shot in-context learning. **Self-Refine** has a model critique its own output and revise within a single trajectory. **Reflexion** layers a verbal critic on top of an agent loop. **TextGrad** generalizes this to "back-propagation through text", treating LLM calls as differentiable nodes whose gradients are natural-language critiques. **In-context RL** (Song et al. 2025; Monea et al. 2024) explicitly feeds reward signals into the prompt across attempts. The common thread: optimization happens *within* a single query's lifetime.

**Line 3 — shared-experience agents.** **Agent KB** maintains a hierarchical knowledge base across tasks but uses a complex retrieve-refine pipeline and collects training trajectories off-policy.

Training-Free GRPO sits at the intersection. From Line 1 it inherits the multi-epoch on-policy structure and the explicit group-relative comparison. From Line 2 it inherits the "no gradients" stance. From Line 3 it inherits the shared, persistent buffer. What is new is the combination: an on-policy multi-epoch RL loop whose update is buffer-edit operations on a single shared text artifact. Self-Refine and Reflexion give per-query corrections; TextGrad gives per-call gradients; Agent KB gives a static knowledge base. None of them have all three pieces — multi-epoch, group-relative, single shared buffer — at once.

### Concept Diagram

<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="rel-diag-title">
  <title id="rel-diag-title">Three lines of related work converging at Training-Free GRPO</title>
  <defs>
    <marker id="rel-arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Where Training-Free GRPO sits in the landscape</text>
  <!-- Line 1: agentic RL -->
  <rect x="40" y="60" width="180" height="80" rx="10" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="130" y="84" text-anchor="middle" font-weight="700" fill="#991b1b">Agentic RL</text>
  <text x="130" y="104" text-anchor="middle" font-size="11" fill="#475569">GRPO, ReTool, AFM</text>
  <text x="130" y="120" text-anchor="middle" font-size="11" fill="#64748b">multi-epoch · groups</text>
  <text x="130" y="134" text-anchor="middle" font-size="11" fill="#991b1b" font-style="italic">updates θ</text>
  <!-- Line 2: training-free -->
  <rect x="270" y="60" width="180" height="80" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="360" y="84" text-anchor="middle" font-weight="700" fill="#1e40af">Training-Free</text>
  <text x="360" y="104" text-anchor="middle" font-size="11" fill="#475569">Self-Refine, Reflexion</text>
  <text x="360" y="120" text-anchor="middle" font-size="11" fill="#475569">ICRL, TextGrad</text>
  <text x="360" y="134" text-anchor="middle" font-size="11" fill="#1e40af" font-style="italic">within-query refinement</text>
  <!-- Line 3: shared-buffer -->
  <rect x="500" y="60" width="180" height="80" rx="10" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="590" y="84" text-anchor="middle" font-weight="700" fill="#854d0e">Shared Experience</text>
  <text x="590" y="104" text-anchor="middle" font-size="11" fill="#475569">Agent KB</text>
  <text x="590" y="120" text-anchor="middle" font-size="11" fill="#64748b">cross-task buffer</text>
  <text x="590" y="134" text-anchor="middle" font-size="11" fill="#854d0e" font-style="italic">off-policy collection</text>
  <!-- Convergence -->
  <line x1="130" y1="140" x2="320" y2="220" stroke="#64748b" stroke-width="1.5" marker-end="url(#rel-arrow)"/>
  <line x1="360" y1="140" x2="360" y2="220" stroke="#64748b" stroke-width="1.5" marker-end="url(#rel-arrow)"/>
  <line x1="590" y1="140" x2="400" y2="220" stroke="#64748b" stroke-width="1.5" marker-end="url(#rel-arrow)"/>
  <rect x="220" y="230" width="280" height="80" rx="12" fill="#f0fdf4" stroke="#22c55e" stroke-width="2.5"/>
  <text x="360" y="258" text-anchor="middle" font-weight="700" fill="#166534" font-size="14">Training-Free GRPO</text>
  <text x="360" y="278" text-anchor="middle" font-size="11" fill="#166534">on-policy + multi-epoch + group-relative</text>
  <text x="360" y="294" text-anchor="middle" font-size="11" fill="#166534">+ no gradients + single shared buffer</text>
  <text x="360" y="350" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Inherits structure from Line 1, the no-gradient stance from Line 2, and the shared buffer from Line 3.</text>
</svg>

### Key Takeaways

- **Most "training-free" methods optimize within one query.** Self-Refine, Reflexion, and TextGrad refine a single trajectory or a small chain; they do not learn across separate examples.
- **Most "agentic RL" methods update weights.** GRPO and its descendants assume gradient ascent is the way the lesson is committed.
- **Agent KB is the closest sibling but not the same shape.** It has a shared buffer, but its collection is off-policy and its retrieval pipeline is more complex; Training-Free GRPO is on-policy and uses the buffer directly in the prompt.
- **The new piece is the combination.** Three separate ideas — group-relative comparison, on-policy multi-epoch loops, shared text buffer — combined into a single training-free RL paradigm.

---

## Conclusion

### Overview

The point of the paper, in one sentence: **the optimization that matters in modern agentic RL can be done in context space rather than parameter space, with most of the benefit and a small fraction of the cost**. The authors do not claim parameter updates are obsolete — they explicitly note their method depends on a strong base model and would not replace fine-tuning when the base is too weak to introspect on its own behavior. What they do show is that for the very real case of "I have access to a strong frontier API model and I need it to behave better in my domain", the GRPO recipe ports cleanly to a no-gradient setting. The fine-tune-or-prompt question, often answered with "fine-tune for serious work, prompt for prototypes", now has a third option that competes on serious work.

If the technique generalizes — and the cross-domain transfer experiment is encouraging here — the operational implication is significant. Building a domain-specialized agent becomes a matter of curating ~100 ground-truth examples, paying $20 of API spend, and shipping a text file alongside the rest of your prompt template. Specialists multiply with low marginal cost. Updates to the base model carry the buffer forward without retraining. The agentic-RL pipeline, as it currently exists, is mostly compute and infrastructure overhead designed to enable parameter updates that, this paper argues, may not have been the most efficient way to encode the lesson.

A fair criticism: the paper's evaluation is narrow. AIME math and WebWalkerQA are real benchmarks, but they are also benchmarks where verification is cleanly available (correct answer or not). For domains without easy verification — open-ended writing, scientific hypothesis generation — the no-ground-truth ablation suggests the method still works partially, but the gap between "with GT" and "without GT" widens. The technique is also not the unconditional win a casual reading might suggest: on QwQ-32B the same recipe hurts. There is a regime where this works; the paper has mapped a useful slice of it.

### Key Takeaways (Summary)

- **Training-Free GRPO ports the GRPO recipe to a frozen-model setting** by replacing gradient updates with edit operations on a natural-language experience buffer that gets prepended to subsequent prompts.
- **The "advantage" becomes a paragraph.** Instead of Â_i = (r_i − μ) / σ, the model produces a natural-language explanation of why winners beat losers (the *semantic advantage*), and that paragraph is what updates the buffer.
- **Headline result: 82.7% on AIME24 + 73.3% on AIME25 + 67.8% on WebWalkerQA** with a single frozen DeepSeek-V3.1-Terminus and two domain-specific buffers — beating fine-tuned 32B specialists in both math and web search.
- **Cost: ~$18 and 100 samples vs ~$10K and thousands of samples** for standard agentic RL — three orders of magnitude cheaper, and no fixed serving infrastructure required.
- **Cross-domain wins are essentially free** because the model never changes — swap the buffer to swap the specialty. Fine-tuned specialists collapse off-domain (ReTool: 67% on AIME → 18% on web).
- **It depends on a strong base.** On QwQ-32B the same recipe regresses (-2.0 pass@1) — the buffer amplifies a capable agent, not an incapable one.
- **Directly-injected tips do not work** (79.8% vs 80.0% baseline). The optimization loop, not the buffer-mechanism alone, is what produces the gain.
- **Tools get used more efficiently too** — average tool calls per problem decreases over training even as accuracy rises.

---

*Code: [TencentCloudADP/youtu-agent — training_free_GRPO branch](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO). Paper: [arXiv:2510.08191](https://arxiv.org/abs/2510.08191).*
