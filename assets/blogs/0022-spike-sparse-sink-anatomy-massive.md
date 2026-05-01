@{id = "c093aed3-559a-4e9e-ac23-a4a81faa2315"
  title = "The Spike, the Sparse and the Sink: Anatomy of Massive Activations and Attention Sinks"
  date = "2026-04-29T00:00:00Z"
  tags = ['journal club', 'machine learning', 'arxiv', 'language models', 'interpretability', 'quantization']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/spike-sparse-sink-anatomy-massive-thumb.svg"
  description = "Sun, Canziani, LeCun, and Zhu dissect why pre-norm LLMs grow giant outlier activations and attention sinks together, then show the two phenomena are decoupled architectural artifacts you can suppress independently."
  type = "note"
  disabled = "false"
}

<p align="center">
  <img src="https://storage.googleapis.com/gn-portfolio/images/spike-sparse-sink-anatomy-massive-thumb.svg" max-width="700">
</p>


# The Spike, the Sparse and the Sink: Anatomy of Massive Activations and Attention Sinks

*Analysis of Sun, Canziani, LeCun, Zhu (2026), New York University — arXiv preprint*
*Generated on April 29, 2026*

---

## Table of Contents

- [Abstract](#abstract)
- [Introduction](#introduction)
- [Preliminaries (Pre-Norm Transformer)](#preliminaries-pre-norm-transformer)
- [The Emergence of Massive Activations](#the-emergence-of-massive-activations)
- [The Emergence of Attention Sinks](#the-emergence-of-attention-sinks)
- [Anatomy by Ablation](#anatomy-by-ablation)
  - [Feed-Forward Block Design](#feed-forward-block-design)
  - [Normalization Configuration](#normalization-configuration)
  - [Attention Head Settings](#attention-head-settings)
  - [Gated Attention](#gated-attention)
  - [Training Context Length](#training-context-length)
- [Discussion](#discussion)
- [Key Takeaways (Summary)](#key-takeaways-summary)

---

## Abstract

### Overview

Two strange things keep showing up in large language models, and nobody has been able to explain why they travel together. The first is **massive activations**: a handful of tokens (almost always the very first token in a sequence, sometimes a period or a newline) carry hidden-state values *thousands* of times larger than the rest of the network. The second is **attention sinks**: those same tokens absorb a huge slice of attention probability across many heads, regardless of what the prompt is about. Sun, Canziani, LeCun and Zhu set out to ask whether these are two faces of the same mechanism, or two phenomena that just happen to land on the same tokens.

If you have only worked at the application layer of LLMs, both terms can sound exotic, so a quick orientation. A modern decoder-only Transformer (think Llama or Qwen) is a stack of layers; each layer reads the running hidden state, applies a normalization step (RMSNorm — just rescale each row to unit RMS), and then either does multi-head attention or a SwiGLU feed-forward block. The output is added back to the running state via a residual connection. "Pre-norm" means the normalization happens *before* the block, not after; this design has become essentially universal because it trains more stably than the original "post-norm" Transformer. The catch — and this paper's central thesis — is that pre-norm has a side effect: the residual stream can accumulate unbounded values, and the model learns to use that.

The headline finding is that the co-occurrence is *not* a fundamental property of Transformers. It is an artifact of the pre-norm design plus the training recipe. Massive activations and attention sinks serve **related but distinct** functions: spikes act *globally* (a few channels carry a near-constant signal across all intermediate layers, behaving like implicit bias parameters baked into the residual stream), while sinks act *locally* (specific heads route excess attention into the spike token to bias themselves toward short-range dependencies). Crucially, the authors show you can suppress either phenomenon without harming the model. Swap RMSNorm for a sandwich-norm or QKNorm and the spikes vanish but the sinks remain. Add per-head conditional gating and the sinks vanish but the spikes remain (sort of — they fall too in some configurations).

That decoupling matters because both phenomena have caused real engineering pain. Quantization — squeezing model weights and activations into 8-bit or 4-bit integers to make inference fast — gets brittle when a few channels carry values in the thousands. KV-cache eviction strategies need special handling for sink tokens or model quality collapses. If we can choose to keep one and drop the other, the cost-quality frontier widens.

### Concept Diagram

<svg viewBox="0 0 720 420" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="abs-diag-title">
  <title id="abs-diag-title">Massive activations and attention sinks: same tokens, different functions</title>
  <defs>
    <marker id="abs-arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">
    Two phenomena, one token
  </text>
  <!-- Center token -->
  <rect x="290" y="170" width="140" height="60" rx="10" fill="#fef3c7" stroke="#92400e" stroke-width="2"/>
  <text x="360" y="195" text-anchor="middle" font-weight="700" fill="#92400e">first token</text>
  <text x="360" y="215" text-anchor="middle" font-size="11" fill="#92400e">(or a delimiter)</text>
  <!-- Spike (global) on left -->
  <rect x="30" y="80" width="220" height="70" rx="10" fill="#fef2f2" stroke="#ef4444" stroke-width="2"/>
  <text x="140" y="106" text-anchor="middle" font-weight="700" fill="#991b1b">Massive activation</text>
  <text x="140" y="126" text-anchor="middle" font-size="11" fill="#991b1b">few channels, magnitudes 1000+</text>
  <text x="140" y="142" text-anchor="middle" font-size="11" fill="#991b1b" font-style="italic">role: global, implicit parameter</text>
  <line x1="220" y1="150" x2="290" y2="190" stroke="#ef4444" stroke-width="1.5" marker-end="url(#abs-arr)"/>
  <!-- Sink (local) on right -->
  <rect x="470" y="80" width="220" height="70" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
  <text x="580" y="106" text-anchor="middle" font-weight="700" fill="#1e40af">Attention sink</text>
  <text x="580" y="126" text-anchor="middle" font-size="11" fill="#1e40af">most attention mass routed here</text>
  <text x="580" y="142" text-anchor="middle" font-size="11" fill="#1e40af" font-style="italic">role: local, per-head router</text>
  <line x1="500" y1="150" x2="430" y2="190" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#abs-arr)"/>
  <!-- Bridge: normalization -->
  <rect x="200" y="270" width="320" height="60" rx="10" fill="#faf5ff" stroke="#a855f7" stroke-width="2"/>
  <text x="360" y="296" text-anchor="middle" font-weight="700" fill="#6b21a8">Pre-norm RMSNorm bridges them</text>
  <text x="360" y="315" text-anchor="middle" font-size="11" fill="#6b21a8">collapses spike tokens to a sparse near-constant vector</text>
  <line x1="360" y1="230" x2="360" y2="270" stroke="#a855f7" stroke-width="1.5" marker-end="url(#abs-arr)"/>
  <text x="360" y="365" text-anchor="middle" font-size="12" fill="#475569" font-style="italic">
    Swap the normalizer and the two phenomena decouple.
  </text>
  <text x="360" y="385" text-anchor="middle" font-size="11" fill="#64748b">
    They look like one thing because they share a token, but they are two.
  </text>
</svg>

### Key Takeaways

- **Two phenomena, one token, one bridge**: massive activations and attention sinks frequently land on the same first / delimiter tokens, but the bridge between them is normalization, not a single underlying mechanism.
- **Different jobs**: spikes operate as global, near-constant implicit parameters in the residual stream; sinks operate as local, per-head attention routers.
- **Suppressible independently**: swap RMSNorm for sandwich-norm or QKNorm and spikes vanish; add conditional gating and sinks vanish. Either is possible without measurable language-modeling cost.

---

## Introduction

### Overview

To see why this paper is more than an interpretability curiosity, it helps to walk through how the field arrived here. When the original Transformer was published in 2017, attention was a clean idea: every token computes a softmax over the keys of every other token, and the resulting weights say "attend here this much". Five or six years and many trillions of parameters later, we know the *behavior* of attention in trained LLMs is not always so clean. Two specific oddities have been documented and re-documented: certain hidden activations are gigantic compared to typical values, and certain tokens (especially the first one in a sequence) absorb most of the attention mass even when they are semantically irrelevant.

The first hints of "outlier dimensions" came from BERT-era work in 2021 (Kovaleva et al.) and from Dettmers et al.'s 2022 quantization paper, which found that 8-bit quantization of GPT-3 only worked if you handled a few outlier channels in higher precision. The second oddity — attention sinks — was named and characterized by Xiao et al. in 2024, who showed that streaming inference works well only when you keep the first few tokens around as "sinks". Sun et al. (2024) brought the two together by showing the outlier tokens *are* the sink tokens, but framed the link as observational. This paper is the mechanistic follow-up: it asks *why* they share tokens, and *what each phenomenon is for*.

The "why now?" is largely about practical pressure. Modern LLM serving lives or dies by quantization (FP16 weights and activations are too expensive at scale, so the field has driven hard into INT8, INT4, and now FP4 / NVFP4). Massive activations sabotage low-precision arithmetic because their magnitudes do not fit into the dynamic range of small integer types (BondarenkoĀ etĀ al., 2021; Wei et al., 2022). At the same time, the success of long-context inference techniques like StreamingLLM (Xiao et al., 2024b) and adaptive KV-cache eviction (Ge et al., 2024) hinges on protecting sink tokens. So if you are an LLM systems engineer in 2026, you have been simultaneously trying to *suppress* spikes (for quantization) and *preserve* sinks (for long-context fidelity). It would be very useful to know whether you have to trade off, or whether the two can be controlled independently. This paper says you can.

The paper makes three central claims, which structure the rest of the post:

1. **Normalization is the bridge.** Standard pre-norm RMSNorm allows residual values to grow unbounded across layers and then collapses spike tokens into a sparse, nearly-constant vector. That collapse is what *enables* sinks — without it, you cannot reliably separate sink keys from non-sink keys. Swap the normalizer and the bridge breaks.
2. **Sinks are driven by attention dimensionality and training context length.** Larger per-head dimension gives the geometry room to separate sink keys from non-sink keys; mixed short / long context training makes sinks *useful* as a way to dump attention.
3. **Independent suppression is possible without quality cost.** Architectural choices that eliminate spikes do not necessarily destroy sinks, and vice versa. The two are not functionally fused.

A note on terminology used throughout: a **spike token** is a token where massive activations appear; a **spike channel** is one of the few hidden-state dimensions where the magnitudes get huge. A **sink token** is a token that absorbs disproportionate attention; a **sink head** is an attention head that routes most of its mass into the sink token. Empirically these largely overlap in pre-norm LLMs — that is the puzzle.

### Concept Diagram

<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="intro-diag-title">
  <title id="intro-diag-title">A short history of outliers and sinks in Transformer LLMs</title>
  <defs>
    <marker id="int-arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">
    Where this paper sits
  </text>
  <!-- Timeline axis -->
  <line x1="60" y1="320" x2="660" y2="320" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="60" y="345" text-anchor="middle" font-size="11" fill="#64748b">2017</text>
  <text x="200" y="345" text-anchor="middle" font-size="11" fill="#64748b">2021–22</text>
  <text x="370" y="345" text-anchor="middle" font-size="11" fill="#64748b">2024</text>
  <text x="540" y="345" text-anchor="middle" font-size="11" fill="#64748b">2024–25</text>
  <text x="660" y="345" text-anchor="middle" font-size="11" fill="#64748b">2026</text>
  <!-- Marker dots -->
  <circle cx="60" cy="320" r="5" fill="#94a3b8"/>
  <circle cx="200" cy="320" r="5" fill="#3b82f6"/>
  <circle cx="370" cy="320" r="5" fill="#ef4444"/>
  <circle cx="540" cy="320" r="5" fill="#a855f7"/>
  <circle cx="660" cy="320" r="6" fill="#22c55e"/>
  <!-- Boxes above markers -->
  <rect x="20" y="60" width="120" height="80" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="80" y="82" text-anchor="middle" font-weight="600" fill="#334155" font-size="12">Transformer</text>
  <text x="80" y="100" text-anchor="middle" font-size="11" fill="#64748b">Vaswani et al.</text>
  <text x="80" y="118" text-anchor="middle" font-size="11" fill="#64748b">post-norm origin</text>
  <rect x="150" y="60" width="120" height="80" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="210" y="82" text-anchor="middle" font-weight="600" fill="#1e40af" font-size="12">Outliers</text>
  <text x="210" y="100" text-anchor="middle" font-size="11" fill="#1e40af">Kovaleva, Dettmers</text>
  <text x="210" y="118" text-anchor="middle" font-size="11" fill="#64748b">quantization breaks</text>
  <rect x="305" y="60" width="130" height="80" rx="8" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="370" y="82" text-anchor="middle" font-weight="600" fill="#991b1b" font-size="12">Sinks named</text>
  <text x="370" y="100" text-anchor="middle" font-size="11" fill="#991b1b">Xiao et al.</text>
  <text x="370" y="118" text-anchor="middle" font-size="11" fill="#64748b">streaming LLMs</text>
  <rect x="475" y="60" width="130" height="80" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5"/>
  <text x="540" y="82" text-anchor="middle" font-weight="600" fill="#6b21a8" font-size="12">Co-occurrence</text>
  <text x="540" y="100" text-anchor="middle" font-size="11" fill="#6b21a8">Sun et al. 2024</text>
  <text x="540" y="118" text-anchor="middle" font-size="11" fill="#64748b">same tokens (descriptive)</text>
  <rect x="600" y="160" width="100" height="100" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="650" y="184" text-anchor="middle" font-weight="700" fill="#166534" font-size="12">This paper</text>
  <text x="650" y="204" text-anchor="middle" font-size="11" fill="#166534">mechanism +</text>
  <text x="650" y="220" text-anchor="middle" font-size="11" fill="#166534">causal ablation</text>
  <text x="650" y="240" text-anchor="middle" font-size="11" fill="#166534" font-style="italic">decouples them</text>
  <!-- Connectors -->
  <line x1="80" y1="140" x2="80" y2="315" stroke="#94a3b8" stroke-dasharray="3,3"/>
  <line x1="210" y1="140" x2="210" y2="315" stroke="#3b82f6" stroke-dasharray="3,3"/>
  <line x1="370" y1="140" x2="370" y2="315" stroke="#ef4444" stroke-dasharray="3,3"/>
  <line x1="540" y1="140" x2="540" y2="315" stroke="#a855f7" stroke-dasharray="3,3"/>
  <line x1="650" y1="260" x2="650" y2="315" stroke="#22c55e" stroke-dasharray="3,3"/>
</svg>

### Key Takeaways

- **The puzzle is mechanistic, not observational**: previous work established that spikes and sinks share tokens. This paper explains *why* they share tokens and *what each phenomenon does*.
- **Practical stakes are quantization and long-context inference**: spikes break low-precision arithmetic; sinks support short-range routing. Engineers want to control them separately.
- **Three claims drive the paper**: normalization is the bridge, sinks live in head-dimension and context-length, and either can be suppressed alone.

---

## Preliminaries (Pre-Norm Transformer)

### Overview

Before diving into the mechanism, lock in the architecture the paper is studying. A modern Llama / Qwen-style decoder-only Transformer is a stack of `2L` blocks — alternating attention and feed-forward — with a single hidden-state matrix `H` flowing through. Each block applies the **pre-norm + residual** rule:

```
H_{i+1} = H_i + F_i(RMSNorm(H_i))
```

A few terms to defuse, since not everyone has stared at this equation for years.

- **RMSNorm**: a simpler cousin of LayerNorm. It divides each row of `H` by its L2 norm and rescales to `sqrt(d_model)`. Where LayerNorm subtracts the mean and divides by the std, RMSNorm just divides by the RMS. It is faster and works just as well in practice (Zhang & Sennrich, 2019), which is why every modern LLM uses it.
- **Pre-norm vs post-norm**: in pre-norm (every modern LLM), the normalization happens *before* the attention or FFN block, and the residual connection adds the un-normalized input. In post-norm (the original Transformer), normalization happens *after* the block. Pre-norm is much more stable to train at depth, but it has the side effect that the residual stream can accumulate unbounded values across layers — nothing normalizes the running sum until you hit the final norm before the prediction head. That accumulation is where massive activations live.
- **Multi-head attention**: each layer has `N_head` heads, each of dimension `d_head`. For each head, `Q = H̃ W_Q`, `K = H̃ W_K`, `V = H̃ W_V` (where `H̃` is the RMSNormed input), and the head output is `softmax(Q K^T / sqrt(d_head)) V`. The per-head outputs are concatenated and projected by `W_O`.
- **SwiGLU FFN**: the modern feed-forward block is `F_ffn(h) = W_down (SiLU(W_gate h) ⊙ (W_up h))`, where `⊙` is element-wise product. The gating structure (multiplying two parallel projections) is what makes SwiGLU more expressive than a standard MLP — and, as we will see, what lets it act as a *quadratic* amplifier when SiLU happens to be near identity.

The paper focuses on Llama 2 7B / 13B, Llama 3 8B, and Qwen 2.5 / 3 (7B/8B/14B) for the analysis, plus a from-scratch 7B Llama-style model trained for 100B tokens for the ablations.

### Concept Diagram

<svg viewBox="0 0 600 460" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="prelim-diag-title">
  <title id="prelim-diag-title">Pre-norm Transformer block: normalization happens before, residual adds the un-normalized input</title>
  <defs>
    <marker id="prearr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
  </defs>
  <text x="300" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">
    A single pre-norm block
  </text>
  <!-- Input H_i -->
  <rect x="220" y="50" width="160" height="40" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="300" y="76" text-anchor="middle" font-weight="600" fill="#92400e">H_i (un-normalized)</text>
  <line x1="300" y1="90" x2="300" y2="115" stroke="#64748b" stroke-width="1.5"/>
  <!-- Branch: residual passes through -->
  <line x1="300" y1="115" x2="500" y2="115" stroke="#64748b" stroke-width="1.5"/>
  <line x1="500" y1="115" x2="500" y2="370" stroke="#64748b" stroke-width="1.5"/>
  <text x="510" y="240" font-size="11" fill="#64748b" font-style="italic">residual</text>
  <text x="510" y="256" font-size="11" fill="#64748b" font-style="italic">(carries spikes)</text>
  <!-- Norm -->
  <rect x="220" y="120" width="160" height="40" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5"/>
  <text x="300" y="146" text-anchor="middle" font-weight="600" fill="#6b21a8">RMSNorm</text>
  <line x1="300" y1="160" x2="300" y2="195" stroke="#64748b" stroke-width="1.5" marker-end="url(#prearr)"/>
  <!-- Block -->
  <rect x="180" y="200" width="240" height="120" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="300" y="226" text-anchor="middle" font-weight="700" fill="#1e40af">F_i: Attention OR SwiGLU FFN</text>
  <text x="300" y="252" text-anchor="middle" font-size="11" fill="#64748b">attention: softmax(QK&#8868;/√d_head)V</text>
  <text x="300" y="270" text-anchor="middle" font-size="11" fill="#64748b">FFN: W_down(SiLU(W_gate h)&#8857;(W_up h))</text>
  <text x="300" y="298" text-anchor="middle" font-size="11" fill="#64748b" font-style="italic">2L of these in total</text>
  <line x1="300" y1="320" x2="300" y2="350" stroke="#64748b" stroke-width="1.5"/>
  <!-- Sum -->
  <circle cx="300" cy="370" r="14" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="300" y="375" text-anchor="middle" font-weight="700" fill="#166534" font-size="14">+</text>
  <line x1="300" y1="384" x2="300" y2="410" stroke="#64748b" stroke-width="1.5" marker-end="url(#prearr)"/>
  <!-- Output -->
  <rect x="220" y="410" width="160" height="40" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="300" y="436" text-anchor="middle" font-weight="600" fill="#166534">H_{i+1}</text>
  <text x="500" y="386" text-anchor="end" font-size="11" fill="#64748b">H_i comes here un-normalized</text>
</svg>

### Key Takeaways

- **The residual stream is un-normalized between blocks**: nothing rescales the running sum until the final layer. That is what lets a few channels grow huge.
- **Pre-norm is universal but not free**: the price of training stability is the quiet accumulation that makes massive activations possible.
- **SwiGLU is a multiplication of two projections**: the gate `(W_gate h) ⊙ (W_up h)` is the structural reason an FFN can act as a *quadratic* amplifier, not just a linear one.

---

## The Emergence of Massive Activations

### Overview

Here is the load-bearing observation. If you instrument a trained Llama 2 7B and watch the magnitudes of the hidden state across its 64 layers, almost every channel is small — a few units, maybe a few tens. But two or three specific channels, on a small set of specific tokens (overwhelmingly the very first token), reach magnitudes in the **thousands** for a long stretch of intermediate layers. The trajectory is consistent: a sharp jump up around block 4, a plateau through the middle, a sharp drop back to normal at block 62 (out of 64). The authors call this the "rise – plateau – fall" lifecycle, and they identify three classes of blocks that produce it: **step-up blocks** that inject the spike, intermediate blocks that propagate it via residual addition, and **step-down blocks** at the end that cancel it by injecting equal-and-opposite values.

The mechanism behind step-up is the most surprising part. The SwiGLU feed-forward block, which usually looks like a humdrum nonlinearity, behaves as a **directional quadratic amplifier** for these tokens. Here is the chain of approximations the paper lays out: when SiLU happens to operate in its near-identity regime (the specific spike tokens land in a part of input space where `SiLU(x) ≈ x`), the SwiGLU FFN simplifies from `W_down (SiLU(W_gate h) ⊙ (W_up h))` to roughly `W_down ((W_gate h) ⊙ (W_up h))`. That elementwise product of two linear projections is *quadratic in `h`*. Each output coordinate `k` then has the form `h^T S_k h` for some matrix `S_k`. For most output coordinates, `S_k` is unremarkable. But for a few "spike channels", `S_k` is dominated by a single eigenvalue `λ*` orders of magnitude larger than the rest of the spectrum. When the input `h` aligns with the leading eigenvector `s*`, the FFN multiplies it by `λ*` — that is the moment a hidden value goes from order-10 to order-1000.

Why does the alignment with `s*` happen for the first token specifically? Because the first token is in a structurally privileged position. With causal masking, the first token can only attend to itself, so the attention block at position 0 collapses to a fixed linear map `W_VO`. That map is *the same for every prompt*. The model has therefore learned a `W_VO` that consistently steers position-0 representations toward `s*`. Delimiter tokens (periods, newlines) follow a related but slightly different path: their embeddings are highly aligned with the RMSNorm scale parameters, so RMSNorm gives them an outsized magnitude post-norm, which makes them self-attend disproportionately, which lands them in a near-first-token regime, which triggers the same quadratic amplifier. The pattern holds remarkably broadly: across Llama 2 / 3 and Qwen 2.5 / 3, **over 98% of all vocabulary items become spike tokens when placed at position 0** (Table 2 in the paper). The exceptions are rare characters from low-resource scripts whose embeddings stayed close to initialization.

Five concrete properties characterize massive activations, and they all fall out of this mechanism: (i) they appear only in intermediate layers (because of the step-up / step-down injection pattern), (ii) only in a small number of channels (the few `S_k` matrices with high-gain quadratic forms), (iii) the affected channels spike *together* (they share the same trigger direction `s*`), (iv) inter-channel ratios stay nearly fixed (governed by the leading eigenvalues of the shared `S_k`s), and (v) only a small number of tokens spike (the few that align with `s*`).

### Concept Diagram

<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="spike-diag-title">
  <title id="spike-diag-title">Rise-plateau-fall lifecycle of a spike channel across Transformer blocks</title>
  <defs>
    <marker id="sp-arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">
    Rise – plateau – fall: a spike channel across 64 blocks
  </text>
  <!-- Axes -->
  <line x1="80" y1="280" x2="660" y2="280" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="80" y1="60" x2="80" y2="280" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="80" y="300" text-anchor="middle" font-size="11" fill="#64748b">block 1</text>
  <text x="160" y="300" text-anchor="middle" font-size="11" fill="#64748b">4</text>
  <text x="370" y="300" text-anchor="middle" font-size="11" fill="#64748b">32</text>
  <text x="600" y="300" text-anchor="middle" font-size="11" fill="#64748b">62</text>
  <text x="660" y="300" text-anchor="middle" font-size="11" fill="#64748b">64</text>
  <text x="370" y="320" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">block index</text>
  <text x="55" y="170" text-anchor="end" font-size="11" fill="#475569" font-style="italic" transform="rotate(-90 55 170)">|hidden|</text>
  <!-- Typical channel: flat low -->
  <path d="M 80 270 L 660 270" stroke="#94a3b8" stroke-width="2" stroke-dasharray="5,4"/>
  <text x="660" y="265" text-anchor="end" font-size="10" fill="#94a3b8">typical channel ~ 10</text>
  <!-- Spike channel trajectory -->
  <path d="M 80 270 L 140 268 L 160 100 L 200 80 L 600 80 L 620 270 L 660 270"
        stroke="#dc2626" stroke-width="3" fill="none"/>
  <circle cx="160" cy="100" r="5" fill="#dc2626"/>
  <circle cx="600" cy="270" r="5" fill="#dc2626"/>
  <!-- Annotations -->
  <rect x="120" y="120" width="120" height="50" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1"/>
  <text x="180" y="140" text-anchor="middle" font-size="12" font-weight="700" fill="#991b1b">step-up block</text>
  <text x="180" y="158" text-anchor="middle" font-size="11" fill="#991b1b">SwiGLU amplifier</text>
  <line x1="180" y1="120" x2="170" y2="100" stroke="#ef4444" stroke-width="1"/>
  <rect x="310" y="100" width="160" height="50" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="1"/>
  <text x="390" y="120" text-anchor="middle" font-size="12" font-weight="700" fill="#92400e">plateau (residual carry)</text>
  <text x="390" y="138" text-anchor="middle" font-size="11" fill="#92400e">later blocks contribute &lt;&lt; spike</text>
  <rect x="540" y="180" width="120" height="50" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1"/>
  <text x="600" y="200" text-anchor="middle" font-size="12" font-weight="700" fill="#991b1b">step-down block</text>
  <text x="600" y="218" text-anchor="middle" font-size="11" fill="#991b1b">opposite-sign cancel</text>
  <line x1="600" y1="230" x2="610" y2="265" stroke="#ef4444" stroke-width="1"/>
  <text x="370" y="345" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">
    Llama 2 7B: spike at block 4, cancel at block 62, of 64 total
  </text>
</svg>

### Try It Yourself

The model spends most of its life in the plateau. The exact step-up and step-down indices vary across families, but the shape stays the same. Click through the model presets to see the architecture summary and where the spike rises and falls.

<style>
  .ptb-step-mds { border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px 20px; margin: 16px 0; }
  .ptb-step-mds .ptb-label { display: block; font-size: 13px; color: #475569; margin-bottom: 8px; font-weight: 600; }
  .ptb-step-mds .ptb-buttons { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
  .ptb-step-mds input[type="radio"] { display: none; }
  .ptb-step-mds .ptb-btn { padding: 6px 14px; border: 1px solid #cbd5e1; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600; color: #475569; background: #f8fafc; user-select: none; }
  .ptb-step-mds .ptb-btn:hover { border-color: #3b82f6; color: #1e40af; }
  .ptb-step-mds .ptb-state { display: none; }
  .ptb-step-mds input#mds-l27:checked ~ .ptb-buttons label[for="mds-l27"],
  .ptb-step-mds input#mds-l213:checked ~ .ptb-buttons label[for="mds-l213"],
  .ptb-step-mds input#mds-q3:checked ~ .ptb-buttons label[for="mds-q3"],
  .ptb-step-mds input#mds-q3l:checked ~ .ptb-buttons label[for="mds-q3l"] {
    background: #eff6ff; border-color: #3b82f6; color: #1e40af;
  }
  .ptb-step-mds input#mds-l27:checked ~ #mds-s-l27,
  .ptb-step-mds input#mds-l213:checked ~ #mds-s-l213,
  .ptb-step-mds input#mds-q3:checked ~ #mds-s-q3,
  .ptb-step-mds input#mds-q3l:checked ~ #mds-s-q3l { display: block; }
</style>

<div class="ptb-step-mds">
  <span class="ptb-label">Pick a model — see where the spike turns on and off:</span>

  <input type="radio" name="mds" id="mds-l27" checked>
  <input type="radio" name="mds" id="mds-l213">
  <input type="radio" name="mds" id="mds-q3">
  <input type="radio" name="mds" id="mds-q3l">

  <div class="ptb-buttons">
    <label for="mds-l27" class="ptb-btn">Llama 2 7B</label>
    <label for="mds-l213" class="ptb-btn">Llama 2 13B</label>
    <label for="mds-q3" class="ptb-btn">Qwen3 8B</label>
    <label for="mds-q3l" class="ptb-btn">Qwen3 14B</label>
  </div>

  <div class="ptb-state" id="mds-s-l27">
    <svg viewBox="0 0 640 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="mds-l27-t">
      <title id="mds-l27-t">Llama 2 7B: 64 blocks, step-up at 4, step-down at 62</title>
      <line x1="40" y1="160" x2="600" y2="160" stroke="#94a3b8"/>
      <text x="40" y="180" font-size="11" fill="#64748b">block 1</text>
      <text x="600" y="180" font-size="11" fill="#64748b" text-anchor="end">block 64</text>
      <path d="M 40 155 L 75 153 L 90 50 L 120 40 L 555 40 L 575 155 L 600 155" stroke="#dc2626" stroke-width="3" fill="none"/>
      <circle cx="90" cy="50" r="5" fill="#dc2626"/>
      <circle cx="575" cy="155" r="5" fill="#dc2626"/>
      <text x="90" y="32" text-anchor="middle" font-size="11" fill="#dc2626" font-weight="600">block 4</text>
      <text x="575" y="32" text-anchor="middle" font-size="11" fill="#dc2626" font-weight="600">block 62</text>
      <text x="320" y="35" text-anchor="middle" font-size="12" fill="#92400e" font-weight="700">peak ~ 3000</text>
    </svg>
  </div>

  <div class="ptb-state" id="mds-s-l213">
    <svg viewBox="0 0 640 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="mds-l213-t">
      <title id="mds-l213-t">Llama 2 13B: 80 blocks, step-up at 8, step-down at 78-79</title>
      <line x1="40" y1="160" x2="600" y2="160" stroke="#94a3b8"/>
      <text x="40" y="180" font-size="11" fill="#64748b">block 1</text>
      <text x="600" y="180" font-size="11" fill="#64748b" text-anchor="end">block 80</text>
      <path d="M 40 155 L 105 153 L 120 50 L 150 40 L 540 40 L 560 155 L 600 155" stroke="#dc2626" stroke-width="3" fill="none"/>
      <circle cx="120" cy="50" r="5" fill="#dc2626"/>
      <circle cx="560" cy="155" r="5" fill="#dc2626"/>
      <text x="120" y="32" text-anchor="middle" font-size="11" fill="#dc2626" font-weight="600">block 8</text>
      <text x="560" y="32" text-anchor="middle" font-size="11" fill="#dc2626" font-weight="600">blocks 78–79</text>
      <text x="320" y="35" text-anchor="middle" font-size="12" fill="#92400e" font-weight="700">step-down spread over two blocks</text>
    </svg>
  </div>

  <div class="ptb-state" id="mds-s-q3">
    <svg viewBox="0 0 640 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="mds-q3-t">
      <title id="mds-q3-t">Qwen3 8B: 72 blocks, step-up at 14, step-down at 70 / 72</title>
      <line x1="40" y1="160" x2="600" y2="160" stroke="#94a3b8"/>
      <text x="40" y="180" font-size="11" fill="#64748b">block 1</text>
      <text x="600" y="180" font-size="11" fill="#64748b" text-anchor="end">block 72</text>
      <path d="M 40 155 L 140 153 L 160 50 L 200 40 L 530 40 L 555 155 L 600 155" stroke="#dc2626" stroke-width="3" fill="none"/>
      <circle cx="160" cy="50" r="5" fill="#dc2626"/>
      <circle cx="555" cy="155" r="5" fill="#dc2626"/>
      <text x="160" y="32" text-anchor="middle" font-size="11" fill="#dc2626" font-weight="600">block 14</text>
      <text x="555" y="32" text-anchor="middle" font-size="11" fill="#dc2626" font-weight="600">blocks 70, 72</text>
      <text x="320" y="35" text-anchor="middle" font-size="12" fill="#92400e" font-weight="700">peak ~ 8000 (higher than Llama)</text>
    </svg>
  </div>

  <div class="ptb-state" id="mds-s-q3l">
    <svg viewBox="0 0 640 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="mds-q3l-t">
      <title id="mds-q3l-t">Qwen3 14B: 80 blocks, step-up at 14, step-down at 79</title>
      <line x1="40" y1="160" x2="600" y2="160" stroke="#94a3b8"/>
      <text x="40" y="180" font-size="11" fill="#64748b">block 1</text>
      <text x="600" y="180" font-size="11" fill="#64748b" text-anchor="end">block 80</text>
      <path d="M 40 155 L 130 153 L 150 50 L 195 40 L 555 40 L 575 155 L 600 155" stroke="#dc2626" stroke-width="3" fill="none"/>
      <circle cx="150" cy="50" r="5" fill="#dc2626"/>
      <circle cx="575" cy="155" r="5" fill="#dc2626"/>
      <text x="150" y="32" text-anchor="middle" font-size="11" fill="#dc2626" font-weight="600">block 14</text>
      <text x="575" y="32" text-anchor="middle" font-size="11" fill="#dc2626" font-weight="600">block 79</text>
      <text x="320" y="35" text-anchor="middle" font-size="12" fill="#92400e" font-weight="700">single step-down at the end</text>
    </svg>
  </div>
</div>

### Implementation

A minimal sketch of the directional quadratic amplifier — the part of SwiGLU that becomes a quadratic form when SiLU is in its near-identity regime.

```python
import torch
import torch.nn as nn

class DirectionalQuadraticAmplifier(nn.Module):
    """SwiGLU FFN, simplified to the regime that produces massive activations.

    When SiLU(x) is approximately x for the spike token's input, the SwiGLU
    block reduces to W_down ((W_gate h) elementwise* (W_up h)). Each output
    coordinate k is then h^T S_k h, and a few output channels have an S_k
    that is rank-one dominated by a leading eigenvector s*. When h aligns
    with s*, those channels are amplified by the leading eigenvalue lambda*.
    """

    def __init__(self, d_model: int, d_ffn: int):
        super().__init__()
        self.W_gate = nn.Linear(d_model, d_ffn, bias=False)
        self.W_up   = nn.Linear(d_model, d_ffn, bias=False)
        self.W_down = nn.Linear(d_ffn, d_model, bias=False)

    def forward(self, h: torch.Tensor) -> torch.Tensor:
        # h shape: (batch, seq, d_model). Each output channel k will end up
        # behaving like a quadratic form h^T S_k h.
        gate = self.W_gate(h)
        up   = self.W_up(h)

        # SwiGLU normally applies SiLU here; for spike tokens it is
        # near-identity, so the multiplicative gate is the dominant nonlinearity.
        # The element-wise product is what makes the whole block quadratic in h.
        product = gate * up

        # W_down picks linear combinations; spike channels are rows whose
        # corresponding S_k matrix has a single dominant eigenvalue.
        return self.W_down(product)
```

### Key Takeaways

- **Step-up + step-down is structural**: spikes are injected by one or two early blocks and cancelled by a symmetric block at the end. They live in the residual stream, not the activations of any one block.
- **SwiGLU is a quadratic amplifier when SiLU is near-identity**: the gating structure makes the FFN behave like `h^T S_k h`, and a handful of `S_k` matrices have rank-one structure that explodes a single direction.
- **First tokens are structurally privileged**: with causal masking the first token sees only itself, so the attention block applies a fixed linear map that the model can train to point at the spike direction. Delimiters reach the same regime through a related route.
- **The 5 properties of massive activations are corollaries of one mechanism**: layer confinement, channel scarcity, joint activation, fixed ratios, and token scarcity all fall out of the rank-one-dominated quadratic forms.

---

## The Emergence of Attention Sinks

### Overview

So we have a few tokens carrying values in the thousands across most of the network. Why does *that* turn into an attention sink? The answer hinges on what RMSNorm does to those tokens. Three properties matter, and they all follow from the spike structure described above.

First, RMSNorm **bounds the magnitudes**. A spike token entering a block has L2 norm dominated by the few spike channels. After RMSNorm, every coordinate is bounded by `sqrt(d_model)`. So the spike disappears from the *normalized* input, even though it is still huge in the residual stream.

Second, RMSNorm **sparsifies** the spike token. Because the L2 norm is dominated by a few channels, division-by-norm crushes the non-spike channels relative to the spike channels. The post-norm vector is approximately a sparse multi-hot indicator over the spike channel set — the rest is noise.

Third, and most importantly, RMSNorm makes the spike token **near-constant across prompts**. Spike channels maintain (almost) fixed inter-channel ratios across different spike tokens, so when you normalize, you get nearly the same vector regardless of which specific spike token you started from. The paper visualizes this with cosine similarity: pre-step-up, spike-token representations vary widely; post-step-up, they collapse to cosine similarity ≈ 1.0.

Now feed those near-constant vectors into the key projection `W_K`. Spike-token keys collapse to the span of just one or two rows of `W_K` (the rows corresponding to the spike channels). That is a *radical* dimensionality reduction relative to `d_head` — sink keys live in 1-2 dimensions, not 64 or 128. Non-spike-token keys, in contrast, span a much higher-dimensional manifold.

Whether a head becomes a sink head is then a matter of geometry. Each head has a query subspace and a key subspace. If the query subspace happens to align more closely with the (1-2 dim, near-constant) sink-key subspace than with the non-sink-key subspace, the dot products `q^T k_sink` are systematically larger than `q^T k_non-sink`, and the softmax dumps mass on the sink. If the alignment is the other way, the head attends semantically. The model has many heads, and the geometry of their query subspaces relative to `W_K` determines who becomes a sink head.

This is the key mechanistic insight: sinks emerge because (i) sparsification from normalization confines sink keys to a low-dimensional subspace, and (ii) near-constancy keeps that subspace stable across prompts, which gives the learned `W_K` something predictable to *route around*. The result is that `W_K` partitions the key space cleanly into "sink" and "non-sink" regions, and each query head picks a side.

### Concept Diagram

<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="sink-diag-title">
  <title id="sink-diag-title">RMSNorm collapses spike tokens to a near-constant sparse vector, which gives sink keys a stable 1-2 dim subspace</title>
  <defs>
    <marker id="sk-arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">
    From spike token to sink key, in three steps
  </text>
  <!-- Stage 1: Spike vector (variable across prompts) -->
  <rect x="30" y="60" width="180" height="220" rx="10" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="120" y="84" text-anchor="middle" font-weight="700" fill="#92400e">Pre-norm spike token</text>
  <!-- 5 stylized "channels" with spikes -->
  <rect x="50" y="100" width="20" height="120" fill="#dc2626"/>
  <rect x="80" y="190" width="20" height="30" fill="#94a3b8"/>
  <rect x="110" y="195" width="20" height="25" fill="#94a3b8"/>
  <rect x="140" y="110" width="20" height="110" fill="#dc2626" opacity="0.85"/>
  <rect x="170" y="200" width="20" height="20" fill="#94a3b8"/>
  <text x="120" y="248" text-anchor="middle" font-size="11" fill="#92400e">few channels &gt;&gt; rest</text>
  <text x="120" y="264" text-anchor="middle" font-size="11" fill="#92400e">|h| &gt; 1000</text>
  <line x1="210" y1="170" x2="245" y2="170" stroke="#a855f7" stroke-width="1.5" marker-end="url(#sk-arr)"/>
  <!-- Stage 2: post-RMSNorm: sparse + near-constant -->
  <rect x="250" y="60" width="180" height="220" rx="10" fill="#faf5ff" stroke="#a855f7" stroke-width="2"/>
  <text x="340" y="84" text-anchor="middle" font-weight="700" fill="#6b21a8">Post-RMSNorm</text>
  <text x="340" y="100" text-anchor="middle" font-size="11" fill="#6b21a8">bounded by √d_model</text>
  <!-- Sparse with two dominant channels (same ratio) -->
  <rect x="270" y="120" width="20" height="100" fill="#a855f7"/>
  <rect x="300" y="210" width="20" height="6" fill="#94a3b8"/>
  <rect x="330" y="210" width="20" height="6" fill="#94a3b8"/>
  <rect x="360" y="130" width="20" height="90" fill="#a855f7" opacity="0.85"/>
  <rect x="390" y="210" width="20" height="6" fill="#94a3b8"/>
  <text x="340" y="248" text-anchor="middle" font-size="11" fill="#6b21a8">sparse multi-hot</text>
  <text x="340" y="264" text-anchor="middle" font-size="11" fill="#6b21a8" font-style="italic">same vector for all spike tokens</text>
  <line x1="430" y1="170" x2="465" y2="170" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#sk-arr)"/>
  <!-- Stage 3: sink key in 1-2 dim subspace of W_K -->
  <rect x="470" y="60" width="220" height="220" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
  <text x="580" y="84" text-anchor="middle" font-weight="700" fill="#1e40af">Sink key k^(s)</text>
  <text x="580" y="100" text-anchor="middle" font-size="11" fill="#1e40af">= W_K^T · (post-norm)</text>
  <!-- Schematic: a small star vs a wide cloud -->
  <circle cx="540" cy="180" r="4" fill="#1e40af"/>
  <circle cx="544" cy="178" r="4" fill="#1e40af"/>
  <circle cx="538" cy="184" r="4" fill="#1e40af"/>
  <ellipse cx="630" cy="180" rx="40" ry="28" fill="none" stroke="#94a3b8" stroke-dasharray="3,3"/>
  <text x="540" y="220" text-anchor="middle" font-size="11" fill="#1e40af" font-weight="600">sink keys</text>
  <text x="540" y="234" text-anchor="middle" font-size="10" fill="#1e40af">1-2 dim, stable</text>
  <text x="630" y="220" text-anchor="middle" font-size="11" fill="#64748b" font-weight="600">non-sink keys</text>
  <text x="630" y="234" text-anchor="middle" font-size="10" fill="#64748b">spread, varied</text>
  <text x="580" y="264" text-anchor="middle" font-size="11" fill="#1e40af" font-style="italic">W_K cleanly separates them</text>
  <text x="360" y="320" text-anchor="middle" font-size="12" fill="#475569">
    Sink heads' query subspace aligns with the small sink-key subspace; non-sink heads' query subspace aligns with the cloud.
  </text>
  <text x="360" y="340" text-anchor="middle" font-size="11" fill="#64748b" font-style="italic">
    The geometry, not the semantics, decides who sinks.
  </text>
</svg>

### Key Takeaways

- **RMSNorm produces three magic properties for spike tokens**: bounded magnitudes, sparsity, and near-constancy across prompts. All three matter for sink formation.
- **Sink keys live in a 1-2 dim subspace**: a dramatic dimensional collapse from the full `d_head` (typically 64 or 128). That is what the learned `W_K` exploits.
- **Sink-vs-non-sink heads are a matter of geometry**: which side of `W_K`'s partition the head's query subspace falls on, not anything semantic.

---

## Anatomy by Ablation

The previous two sections build a *mechanism*. The next sections turn that mechanism into a *causal* claim by intervening — one architectural component at a time — and watching what happens to the spike magnitude, the sink ratio (the fraction of attention mass routed to the sink token), and language-modeling perplexity. The setup: a Llama-style 7B model trained from scratch on the DCLM dataset for 100B tokens, which is enough to reproduce both phenomena. Each ablation modifies a specific architectural choice while keeping the rest fixed.

The picture that emerges across the ablations is the headline of the paper: **the two phenomena respond differently to the same interventions**. That is the empirical fingerprint of two mechanisms, not one.

---

### Feed-Forward Block Design

#### Overview

If SwiGLU is the "directional quadratic amplifier" responsible for spikes, what happens when you take it away? The authors compare four feed-forward designs at fixed capacity: SwiGLU (baseline), GeLU (the older standard), a single linear layer, and an attention-only design (no FFN, just more attention layers).

A quick orientation on what those mean for a non-specialist. SwiGLU and GeLU are both "gated MLP" variants — they apply a nonlinearity (SiLU or GeLU) and, in SwiGLU's case, a multiplicative gate. A single linear layer is just `W h`, the simplest possible block. Attention-only replaces every FFN with another attention layer; the model becomes "all attention all the time".

The result: **massive activations and attention sinks emerge in all four configurations**. The block design is *not* a prerequisite. But the *magnitude* of the spikes varies wildly. SwiGLU and GeLU yield spike magnitudes around 3000-4000. Linear and attention-only yield spike magnitudes around 600-700 — the spikes still exist, but they are much smaller because they have to be built up *gradually* across many layers instead of in a single block. The gating (SwiGLU) and saturating-nonlinearity (GeLU) designs concentrate amplification within one block; the others spread it.

That is a useful refinement of the earlier story. SwiGLU is not *necessary* for spikes — any pre-norm architecture will accumulate them — but it is the most *efficient* amplifier, which is why the spike magnitudes are largest there. The implication for quantization is direct: if your model uses SwiGLU, expect bigger spikes and budget more dynamic range for them.

#### Concept Diagram

<svg viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="ffn-diag-title">
  <title id="ffn-diag-title">Feed-forward block design vs spike magnitude and sink ratio</title>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">
    FFN design changes spike size, not sink emergence
  </text>
  <text x="360" y="42" text-anchor="middle" font-size="11" fill="#64748b">All configurations produce sinks. SwiGLU/GeLU are the best amplifiers.</text>
  <text x="220" y="74" text-anchor="end" font-size="11" fill="#64748b" font-weight="600">FFN design</text>
  <text x="660" y="74" text-anchor="end" font-size="11" fill="#64748b" font-weight="600">Spike magnitude</text>
  <!-- SwiGLU (baseline) -->
  <text x="220" y="104" text-anchor="end" fill="#334155" font-size="12">SwiGLU (baseline)</text>
  <rect x="230" y="92" width="380" height="20" rx="4" fill="#dc2626" opacity="0.85"/>
  <text x="618" y="107" font-size="11" fill="#991b1b" font-weight="700">3818  · sink 46%</text>
  <!-- GeLU -->
  <text x="220" y="134" text-anchor="end" fill="#334155" font-size="12">GeLU</text>
  <rect x="230" y="122" width="335" height="20" rx="4" fill="#ef4444" opacity="0.7"/>
  <text x="573" y="137" font-size="11" fill="#991b1b" font-weight="700">3369  · sink 69%</text>
  <!-- Linear -->
  <text x="220" y="164" text-anchor="end" fill="#334155" font-size="12">Single linear</text>
  <rect x="230" y="152" width="68" height="20" rx="4" fill="#94a3b8" opacity="0.55"/>
  <text x="306" y="167" font-size="11" fill="#475569" font-weight="700">688  · sink 59%</text>
  <!-- Attention-only -->
  <text x="220" y="194" text-anchor="end" fill="#334155" font-size="12">Attention-only</text>
  <rect x="230" y="182" width="63" height="20" rx="4" fill="#94a3b8" opacity="0.55"/>
  <text x="301" y="197" font-size="11" fill="#475569" font-weight="700">637  · sink 74%</text>
  <line x1="230" y1="84" x2="230" y2="208" stroke="#cbd5e1" stroke-dasharray="3,3"/>
  <rect x="60" y="246" width="600" height="50" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>
  <text x="360" y="266" text-anchor="middle" font-size="12" fill="#475569">
    Lesson: SwiGLU/GeLU concentrate amplification in one block (big spikes);
  </text>
  <text x="360" y="284" text-anchor="middle" font-size="12" fill="#475569" font-style="italic">
    linear/attention-only spread it across many (small spikes). Sinks always show up.
  </text>
</svg>

#### Key Takeaways

- **FFN design is a knob, not a switch**: every architecture produces spikes and sinks, but SwiGLU and GeLU produce far larger spikes (~3000-4000) than linear or attention-only (~600-700).
- **Concentration vs accumulation**: gated nonlinearities concentrate the amplification into a single block; flatter designs accumulate the same effect over many blocks.
- **Quantization implication**: SwiGLU models will always have the biggest dynamic range pressure. If you can swap to a less concentrated design, you buy precision headroom.

---

### Normalization Configuration

#### Overview

Now the most consequential ablation. If normalization is the bridge between spikes and sinks, swapping it should disconnect them. The authors test three alternatives.

- **Sandwich normalization** (Ding et al., 2021): an extra RMSNorm at the *output* of each block, after the residual addition. This bounds the residual-stream magnitudes between blocks, which should prevent the unbounded accumulation that makes spikes possible.
- **Sandwich-QK normalization**: a related variant where input normalization is applied only to queries and keys. This decouples the path that produces sinks (Q/K projections) from the rest of the residual stream.
- **DynamicTanh** (Zhu et al., 2025): replace RMSNorm with an *element-wise* `tanh`-like saturating function. This caps each coordinate independently, which means it cannot produce the sparse multi-hot vector that arises from L2 normalization of a peaky distribution.

The headline result, summarized in the comparison below: each alternative successfully reduces spike magnitude relative to the baseline, but **the sink ratio mostly survives**. Sandwich norm: spike falls from 3818 to 520 while sinks stay at 44.7%. Sandwich-QK: spikes almost gone (92), sinks 42.0%. DynamicTanh: spikes vanish (153) and sinks *increase* to 61.0% — the model finds an alternative pathway to designate the first token as a stable reference, without needing huge magnitudes.

That is a striking decoupling. The standard story — "spikes cause sinks" — is too strong. What is true is: pre-norm RMSNorm + unbounded residual + SwiGLU is *one* path to sinks, but it is not the only path. When you take the magnitudes away, the model finds another way.

#### Concept Diagram

<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="norm-diag-title">
  <title id="norm-diag-title">Normalization variants vs spike magnitude and sink ratio</title>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">
    Normalization is the lever to decouple spikes from sinks
  </text>
  <text x="360" y="42" text-anchor="middle" font-size="11" fill="#64748b">
    Same model, four normalization variants. Spike falls; sinks mostly survive.
  </text>
  <text x="220" y="76" text-anchor="end" font-size="11" font-weight="600" fill="#64748b">Variant</text>
  <text x="465" y="76" text-anchor="middle" font-size="11" font-weight="600" fill="#64748b">Spike magnitude</text>
  <text x="650" y="76" text-anchor="end" font-size="11" font-weight="600" fill="#64748b">Sink ratio</text>
  <!-- Pre-norm (baseline) -->
  <text x="220" y="104" text-anchor="end" fill="#334155" font-size="12">Pre-norm RMSNorm (baseline)</text>
  <rect x="230" y="92" width="380" height="20" rx="4" fill="#dc2626" opacity="0.85"/>
  <text x="618" y="107" font-size="11" fill="#991b1b" font-weight="700">3818</text>
  <text x="650" y="107" text-anchor="end" font-size="11" fill="#1e40af" font-weight="700">46.0%</text>
  <!-- Sandwich -->
  <text x="220" y="144" text-anchor="end" fill="#334155" font-size="12">Sandwich norm</text>
  <rect x="230" y="132" width="55" height="20" rx="4" fill="#22c55e" opacity="0.75"/>
  <text x="293" y="147" font-size="11" fill="#166534" font-weight="700">520</text>
  <text x="650" y="147" text-anchor="end" font-size="11" fill="#1e40af" font-weight="700">44.7%</text>
  <!-- Sandwich-QK -->
  <text x="220" y="184" text-anchor="end" fill="#334155" font-size="12">Sandwich-QK norm</text>
  <rect x="230" y="172" width="12" height="20" rx="4" fill="#22c55e" opacity="0.85"/>
  <text x="250" y="187" font-size="11" fill="#166534" font-weight="700">92</text>
  <text x="650" y="187" text-anchor="end" font-size="11" fill="#1e40af" font-weight="700">42.0%</text>
  <!-- DynamicTanh -->
  <text x="220" y="224" text-anchor="end" fill="#334155" font-size="12">DynamicTanh</text>
  <rect x="230" y="212" width="18" height="20" rx="4" fill="#22c55e" opacity="0.85"/>
  <text x="256" y="227" font-size="11" fill="#166534" font-weight="700">153</text>
  <text x="650" y="227" text-anchor="end" font-size="11" fill="#a855f7" font-weight="700">61.0%</text>
  <line x1="230" y1="84" x2="230" y2="244" stroke="#cbd5e1" stroke-dasharray="3,3"/>
  <rect x="60" y="280" width="600" height="80" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>
  <text x="360" y="302" text-anchor="middle" font-size="12" fill="#475569">
    Sandwich norm and QKNorm bound the residual; spikes collapse, sinks are barely touched.
  </text>
  <text x="360" y="320" text-anchor="middle" font-size="12" fill="#475569">
    DynamicTanh is even more emphatic: spikes go away and the sink ratio *rises* —
  </text>
  <text x="360" y="338" text-anchor="middle" font-size="12" fill="#475569" font-style="italic">
    the model finds a different way to designate the first token as a sink.
  </text>
</svg>

#### Key Takeaways

- **Pre-norm + unbounded residual is one path to sinks, not the only one**: Sandwich, QKNorm, and DynamicTanh all kill spike magnitudes while preserving (or even increasing) sinks.
- **DynamicTanh is the cleanest decoupling**: element-wise saturation is mathematically incapable of producing the sparse multi-hot post-norm vector, yet sinks not only survive but strengthen.
- **The implication for low-precision serving**: you can keep sinks (good for streaming inference) and drop spikes (good for INT4 / FP4 quantization) by changing the normalizer at training time. This is the most actionable result in the paper.

---

### Attention Head Settings

#### Overview

If the geometric story is right — sinks emerge when the per-head subspace is large enough to cleanly separate sink keys from non-sink keys — then the attention head dimension `d_head` should be a major lever. The authors run a clean sweep.

A quick orientation. In multi-head attention, the total attention capacity is split into `N_head` heads of dimension `d_head`. The per-head Q/K/V projections are `d_model -> d_head` matrices. Larger `d_head` gives each head more "room" geometrically. Modern Llama-style models use `d_head = 128` and `N_head = 32` for a 4096-dim model.

The ablation: hold `N_head = 32` fixed, vary `d_head` from 8 to 128. Result: a monotonic rise in sink ratio (4.1% at `d_head=8` to 46.0% at `d_head=128`) and spike magnitude (291 to 3818). Tiny heads cannot form sinks at all, because the sink-key subspace and non-sink-key subspace cannot be cleanly separated in low dimensions.

A second sweep is more illuminating: hold the *total* attention capacity `d_head x N_head = 4096` fixed, and re-allocate it. With `8/512` (tiny heads, lots of them) the sink ratio is 11%; with `128/32` (Llama-style) it is 46%; with `256/16` (giant heads, fewer of them) it is 52%. **Concentrating capacity into fewer, larger heads strengthens sink behavior**, even at fixed total capacity.

This is a strong piece of evidence for the geometric mechanism. Sink formation is fundamentally about whether the head has enough dimensions to *partition*, not about how much total capacity the model has.

#### Concept Diagram

<svg viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="head-diag-title">
  <title id="head-diag-title">Sink ratio rises with d_head, even at fixed total capacity</title>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">
    Sinks need head-dimension room to form
  </text>
  <text x="360" y="42" text-anchor="middle" font-size="11" fill="#64748b">
    Total attention capacity (d_head x N_head) held at 4096 across all rows
  </text>
  <!-- Axes -->
  <line x1="100" y1="260" x2="660" y2="260" stroke="#94a3b8"/>
  <line x1="100" y1="80" x2="100" y2="260" stroke="#94a3b8"/>
  <text x="100" y="280" text-anchor="middle" font-size="11" fill="#64748b">d=8</text>
  <text x="200" y="280" text-anchor="middle" font-size="11" fill="#64748b">d=16</text>
  <text x="320" y="280" text-anchor="middle" font-size="11" fill="#64748b">d=32</text>
  <text x="440" y="280" text-anchor="middle" font-size="11" fill="#64748b">d=64</text>
  <text x="560" y="280" text-anchor="middle" font-size="11" fill="#64748b">d=128</text>
  <text x="660" y="280" text-anchor="middle" font-size="11" fill="#64748b">d=256</text>
  <text x="380" y="305" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">d_head (with N_head adjusted to keep capacity fixed)</text>
  <text x="78" y="170" text-anchor="end" font-size="11" fill="#475569">sink ratio</text>
  <!-- Y-axis ticks -->
  <text x="92" y="265" text-anchor="end" font-size="10" fill="#64748b">0%</text>
  <text x="92" y="220" text-anchor="end" font-size="10" fill="#64748b">25%</text>
  <text x="92" y="170" text-anchor="end" font-size="10" fill="#64748b">50%</text>
  <!-- Curve -->
  <path d="M 100 240 L 200 196 L 320 178 L 440 175 L 560 158 L 660 145" stroke="#3b82f6" stroke-width="3" fill="none"/>
  <circle cx="100" cy="240" r="5" fill="#3b82f6"/>
  <circle cx="200" cy="196" r="5" fill="#3b82f6"/>
  <circle cx="320" cy="178" r="5" fill="#3b82f6"/>
  <circle cx="440" cy="175" r="5" fill="#3b82f6"/>
  <circle cx="560" cy="158" r="5" fill="#3b82f6"/>
  <circle cx="660" cy="145" r="5" fill="#3b82f6"/>
  <!-- Annotations -->
  <text x="100" y="234" text-anchor="middle" font-size="10" fill="#1e40af" font-weight="600">11%</text>
  <text x="320" y="172" text-anchor="middle" font-size="10" fill="#1e40af" font-weight="600">41%</text>
  <text x="560" y="152" text-anchor="middle" font-size="10" fill="#1e40af" font-weight="600">46%</text>
  <text x="660" y="139" text-anchor="middle" font-size="10" fill="#1e40af" font-weight="600">52%</text>
  <text x="180" y="100" font-size="11" fill="#475569" font-style="italic">tiny heads cannot</text>
  <text x="180" y="116" font-size="11" fill="#475569" font-style="italic">separate sink keys</text>
  <text x="540" y="100" font-size="11" fill="#475569" font-style="italic">fewer-larger heads</text>
  <text x="540" y="116" font-size="11" fill="#475569" font-style="italic">give cleaner partition</text>
</svg>

### Try It Yourself

How much does the per-head dimension change sink behavior at a fixed total capacity? Pick a configuration to see the layout and the resulting sink ratio.

<style>
  .ptb-step-hd { border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px 20px; margin: 16px 0; }
  .ptb-step-hd .ptb-label { display: block; font-size: 13px; color: #475569; margin-bottom: 8px; font-weight: 600; }
  .ptb-step-hd .ptb-buttons { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
  .ptb-step-hd input[type="radio"] { display: none; }
  .ptb-step-hd .ptb-btn { padding: 6px 14px; border: 1px solid #cbd5e1; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600; color: #475569; background: #f8fafc; user-select: none; }
  .ptb-step-hd .ptb-btn:hover { border-color: #3b82f6; color: #1e40af; }
  .ptb-step-hd .ptb-state { display: none; }
  .ptb-step-hd input#hd-8:checked ~ .ptb-buttons label[for="hd-8"],
  .ptb-step-hd input#hd-32:checked ~ .ptb-buttons label[for="hd-32"],
  .ptb-step-hd input#hd-128:checked ~ .ptb-buttons label[for="hd-128"],
  .ptb-step-hd input#hd-256:checked ~ .ptb-buttons label[for="hd-256"] {
    background: #eff6ff; border-color: #3b82f6; color: #1e40af;
  }
  .ptb-step-hd input#hd-8:checked ~ #hd-s-8,
  .ptb-step-hd input#hd-32:checked ~ #hd-s-32,
  .ptb-step-hd input#hd-128:checked ~ #hd-s-128,
  .ptb-step-hd input#hd-256:checked ~ #hd-s-256 { display: block; }
</style>

<div class="ptb-step-hd">
  <span class="ptb-label">Pick a (d_head / N_head) split — total capacity = 4096:</span>

  <input type="radio" name="hd" id="hd-8">
  <input type="radio" name="hd" id="hd-32">
  <input type="radio" name="hd" id="hd-128" checked>
  <input type="radio" name="hd" id="hd-256">

  <div class="ptb-buttons">
    <label for="hd-8" class="ptb-btn">8 / 512</label>
    <label for="hd-32" class="ptb-btn">32 / 128</label>
    <label for="hd-128" class="ptb-btn">128 / 32 (Llama)</label>
    <label for="hd-256" class="ptb-btn">256 / 16</label>
  </div>

  <div class="ptb-state" id="hd-s-8">
    <svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="hd-s-8-t">
      <title id="hd-s-8-t">d_head = 8, N_head = 512: tiny heads, sink ratio 11%</title>
      <text x="300" y="30" text-anchor="middle" font-weight="700" fill="#1e293b" font-size="14">d_head = 8, N_head = 512</text>
      <!-- A long row of tiny heads -->
      <g fill="#bfdbfe" stroke="#3b82f6">
        <rect x="50"  y="80" width="20" height="40"/>
        <rect x="74"  y="80" width="20" height="40"/>
        <rect x="98"  y="80" width="20" height="40"/>
        <rect x="122" y="80" width="20" height="40"/>
        <rect x="146" y="80" width="20" height="40"/>
        <rect x="170" y="80" width="20" height="40"/>
        <rect x="194" y="80" width="20" height="40"/>
        <rect x="218" y="80" width="20" height="40"/>
      </g>
      <text x="380" y="105" font-size="12" fill="#64748b">… (504 more tiny heads)</text>
      <text x="300" y="170" text-anchor="middle" font-size="13" fill="#475569" font-style="italic">
        too few dimensions per head to separate sink/non-sink keys
      </text>
      <text x="300" y="195" text-anchor="middle" font-size="14" fill="#1e40af" font-weight="700">sink ratio: 11.0%</text>
    </svg>
  </div>

  <div class="ptb-state" id="hd-s-32">
    <svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="hd-s-32-t">
      <title id="hd-s-32-t">d_head = 32, N_head = 128: small heads, sink ratio 41%</title>
      <text x="300" y="30" text-anchor="middle" font-weight="700" fill="#1e293b" font-size="14">d_head = 32, N_head = 128</text>
      <g fill="#bfdbfe" stroke="#3b82f6">
        <rect x="60" y="70" width="40" height="60"/>
        <rect x="104" y="70" width="40" height="60"/>
        <rect x="148" y="70" width="40" height="60"/>
        <rect x="192" y="70" width="40" height="60"/>
        <rect x="236" y="70" width="40" height="60"/>
      </g>
      <text x="380" y="105" font-size="12" fill="#64748b">… (123 more)</text>
      <text x="300" y="170" text-anchor="middle" font-size="13" fill="#475569" font-style="italic">
        partial separation; sink behavior emerges in some heads
      </text>
      <text x="300" y="195" text-anchor="middle" font-size="14" fill="#1e40af" font-weight="700">sink ratio: 41.1%</text>
    </svg>
  </div>

  <div class="ptb-state" id="hd-s-128">
    <svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="hd-s-128-t">
      <title id="hd-s-128-t">d_head = 128, N_head = 32: Llama config, sink ratio 46%</title>
      <text x="300" y="30" text-anchor="middle" font-weight="700" fill="#1e293b" font-size="14">d_head = 128, N_head = 32 (Llama-style)</text>
      <g fill="#bfdbfe" stroke="#3b82f6">
        <rect x="80" y="60" width="80" height="80"/>
        <rect x="170" y="60" width="80" height="80"/>
        <rect x="260" y="60" width="80" height="80"/>
        <rect x="350" y="60" width="80" height="80"/>
      </g>
      <text x="500" y="105" font-size="12" fill="#64748b">… (28 more)</text>
      <text x="300" y="170" text-anchor="middle" font-size="13" fill="#475569" font-style="italic">
        clean partition between sink and non-sink keys
      </text>
      <text x="300" y="195" text-anchor="middle" font-size="14" fill="#1e40af" font-weight="700">sink ratio: 46.0%</text>
    </svg>
  </div>

  <div class="ptb-state" id="hd-s-256">
    <svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="hd-s-256-t">
      <title id="hd-s-256-t">d_head = 256, N_head = 16: giant heads, sink ratio 52%</title>
      <text x="300" y="30" text-anchor="middle" font-weight="700" fill="#1e293b" font-size="14">d_head = 256, N_head = 16</text>
      <g fill="#bfdbfe" stroke="#3b82f6">
        <rect x="80" y="50" width="160" height="100"/>
        <rect x="250" y="50" width="160" height="100"/>
      </g>
      <text x="450" y="105" font-size="12" fill="#64748b">… (14 more)</text>
      <text x="300" y="170" text-anchor="middle" font-size="13" fill="#475569" font-style="italic">
        ample geometry to separate keys; sinks strengthen further
      </text>
      <text x="300" y="195" text-anchor="middle" font-size="14" fill="#a855f7" font-weight="700">sink ratio: 52.1%</text>
    </svg>
  </div>
</div>

#### Key Takeaways

- **`d_head` is the dominant architectural lever for sinks**: monotonic rise from 4.1% at `d_head=8` to 46% at `d_head=128`.
- **Concentration beats distribution at fixed capacity**: moving from many-tiny to few-large heads strengthens sinks even when total capacity is held constant.
- **The geometric mechanism is the right model**: sinks need *room* in the per-head subspace to separate sink-keys from non-sink-keys. Total capacity is not the binding constraint; per-head capacity is.

---

### Gated Attention

#### Overview

A second-order question: if sinks are useful for routing, what happens when we give the model an *explicit* routing mechanism instead? The answer is striking. Following Qiu et al. (2025), the authors test gated attention variants — the head output gets multiplied by a learned gate.

The taxonomy that matters is whether the gate is **conditional** (a function of the current hidden representation, so it changes prompt-by-prompt) or **unconditional / static** (fixed at the per-head, per-channel, or per-position level). Within conditional, you can have per-channel gates (one gate per output channel), per-head gates, or single-token gates.

Result: **conditional gating eliminates sinks**. Per-channel conditional gate yields a 4.5% sink ratio (down from 46%) with spike magnitude 202. Per-head: 6.4% sink, spike 186. Single-token: 31% — partial. Static gates (positional or token-embedding based) preserve sink behavior almost fully (~31-44%).

The interpretation: attention sinks are a **learned input-conditioned gating mechanism**. When the model lacks a built-in dynamic gate, it improvises one by routing excess attention into the spike token, effectively zeroing out unwanted heads. When you give it a real gate, the improvisation becomes redundant and disappears.

This connects sinks to a larger architectural conversation. Multiple recent designs — gated linear units, gated state-space models, mixture-of-experts routers — build dynamic input-conditioned routing as an explicit primitive. The sink phenomenon is a hint that vanilla self-attention has been silently doing a version of this, with the first token playing the role of a "this head is off" signal.

#### Concept Diagram

<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="gate-diag-title">
  <title id="gate-diag-title">Gating type vs sink ratio: conditional gating eliminates sinks; static gating does not</title>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">
    Sinks act as an implicit, input-conditioned gate
  </text>
  <text x="360" y="42" text-anchor="middle" font-size="11" fill="#64748b">
    Replace the implicit gate with an explicit one and sinks vanish — only when the gate is conditional.
  </text>
  <!-- Conditional gating panel -->
  <rect x="40" y="70" width="320" height="260" rx="10" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="200" y="94" text-anchor="middle" font-weight="700" fill="#166534">Conditional gating (gate = f(h))</text>
  <text x="60" y="124" font-size="12" fill="#334155">per-channel gate</text>
  <rect x="180" y="114" width="14" height="14" rx="3" fill="#22c55e"/>
  <text x="220" y="125" font-size="12" fill="#166534" font-weight="700">sink 4.5%</text>
  <text x="60" y="154" font-size="12" fill="#334155">per-head gate</text>
  <rect x="180" y="144" width="20" height="14" rx="3" fill="#22c55e"/>
  <text x="220" y="155" font-size="12" fill="#166534" font-weight="700">sink 6.4%</text>
  <text x="60" y="184" font-size="12" fill="#334155">single-token gate</text>
  <rect x="180" y="174" width="100" height="14" rx="3" fill="#94a3b8" opacity="0.7"/>
  <text x="290" y="185" font-size="12" fill="#475569" font-weight="700">sink 31.2%</text>
  <text x="200" y="240" text-anchor="middle" font-size="11" fill="#166534" font-style="italic">
    finer-grained conditional gates kill sinks
  </text>
  <text x="200" y="258" text-anchor="middle" font-size="11" fill="#166534">
    (per-channel and per-head gates do best)
  </text>
  <text x="200" y="294" text-anchor="middle" font-size="11" fill="#475569">
    perplexity barely changes vs baseline 10.1
  </text>
  <!-- Unconditional / static gating panel -->
  <rect x="380" y="70" width="320" height="260" rx="10" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="540" y="94" text-anchor="middle" font-weight="700" fill="#92400e">Unconditional / static gating</text>
  <text x="400" y="124" font-size="12" fill="#334155">unconditional channel</text>
  <rect x="540" y="114" width="135" height="14" rx="3" fill="#f59e0b" opacity="0.8"/>
  <text x="685" y="125" text-anchor="end" font-size="12" fill="#92400e" font-weight="700">42.2%</text>
  <text x="400" y="154" font-size="12" fill="#334155">unconditional head</text>
  <rect x="540" y="144" width="132" height="14" rx="3" fill="#f59e0b" opacity="0.8"/>
  <text x="685" y="155" text-anchor="end" font-size="12" fill="#92400e" font-weight="700">41.3%</text>
  <text x="400" y="184" font-size="12" fill="#334155">positional</text>
  <rect x="540" y="174" width="131" height="14" rx="3" fill="#f59e0b" opacity="0.8"/>
  <text x="685" y="185" text-anchor="end" font-size="12" fill="#92400e" font-weight="700">41.1%</text>
  <text x="400" y="214" font-size="12" fill="#334155">token-embedding</text>
  <rect x="540" y="204" width="100" height="14" rx="3" fill="#f59e0b" opacity="0.8"/>
  <text x="685" y="215" text-anchor="end" font-size="12" fill="#92400e" font-weight="700">31.1%</text>
  <text x="540" y="270" text-anchor="middle" font-size="11" fill="#92400e" font-style="italic">
    gates that do not depend on the current state
  </text>
  <text x="540" y="288" text-anchor="middle" font-size="11" fill="#92400e">
    cannot replace the role of sinks
  </text>
  <text x="540" y="312" text-anchor="middle" font-size="11" fill="#475569">
    sinks survive at near-baseline levels
  </text>
</svg>

#### Key Takeaways

- **Sinks are implicit gates**: when an explicit input-conditioned gate is added, sink behavior disappears with no perplexity cost.
- **Conditional vs static is the dividing line**: unconditional or static-signal gates do not replace sinks. The model needs a *dynamic* gating signal to free up the first token.
- **A unifying view of recent architectures**: gated attention, gated SSMs, and similar explicit-gating designs are doing what attention sinks have been silently doing. Once explicit, the implicit version is vestigial.

---

### Training Context Length

#### Overview

The last ablation tests the hypothesis that sinks are not just architectural — they are *useful* for short-range prediction. Xiao et al. (2024a) noted that sink heads tend to attend to nearby tokens of the query; the authors of this paper test that systematically by varying the *training* context-length distribution. Concretely, they change the range of sequence positions over which the loss is computed during training. Configurations are reported as `min/max` — e.g. `1/4096` means losses are computed at positions 1 to 4096.

Result: when training includes short sequences (`1/256`, `1/1024`, `1/4096`), the sink ratio is stable at ~42-46%. When short contexts are *removed* and only long-range positions are optimized (`1024/4096`, `2048/4096`, `2048/6144`), the sink ratio collapses dramatically — 13%, 1.2%, 5.8% respectively. Spike magnitudes go *up* in some of these long-only configs (38000+ at `1024/4096`), but the sinks have already disengaged.

The interpretation: sinks exist to support short-range prediction. In a mixed-length training regime, the first token serves as a cheap, universal "ignore the far context" reference for short-context examples. When the model never has to do short-context prediction, it never learns to use that reference, and sinks do not form. This is a counterintuitive but empirically robust result — a phenomenon we usually frame as architectural turns out to be partly *training-data-distribution-driven*.

#### Concept Diagram

<svg viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="ctx-diag-title">
  <title id="ctx-diag-title">Sinks collapse when training distribution excludes short contexts</title>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">
    Sinks are a byproduct of short-context training
  </text>
  <text x="360" y="42" text-anchor="middle" font-size="11" fill="#64748b">
    Train on positions in (min/max). Remove short positions, sinks collapse.
  </text>
  <text x="220" y="74" text-anchor="end" font-size="11" font-weight="600" fill="#64748b">Train positions</text>
  <text x="660" y="74" text-anchor="end" font-size="11" font-weight="600" fill="#64748b">Sink ratio</text>
  <!-- 1/256 -->
  <text x="220" y="104" text-anchor="end" fill="#334155" font-size="12">1 / 256 (short only)</text>
  <rect x="230" y="92" width="335" height="20" rx="4" fill="#3b82f6" opacity="0.7"/>
  <text x="660" y="107" text-anchor="end" font-size="11" fill="#1e40af" font-weight="700">42.1%</text>
  <!-- 1/4096 baseline -->
  <text x="220" y="134" text-anchor="end" fill="#334155" font-size="12">1 / 4096 (mixed, baseline)</text>
  <rect x="230" y="122" width="370" height="20" rx="4" fill="#3b82f6" opacity="0.85"/>
  <text x="660" y="137" text-anchor="end" font-size="11" fill="#1e40af" font-weight="700">46.0%</text>
  <!-- 1024/4096 -->
  <text x="220" y="164" text-anchor="end" fill="#334155" font-size="12">1024 / 4096 (no short)</text>
  <rect x="230" y="152" width="105" height="20" rx="4" fill="#ef4444" opacity="0.6"/>
  <text x="660" y="167" text-anchor="end" font-size="11" fill="#dc2626" font-weight="700">13.0%</text>
  <!-- 1024/5120 -->
  <text x="220" y="194" text-anchor="end" fill="#334155" font-size="12">1024 / 5120 (no short)</text>
  <rect x="230" y="182" width="65" height="20" rx="4" fill="#ef4444" opacity="0.6"/>
  <text x="660" y="197" text-anchor="end" font-size="11" fill="#dc2626" font-weight="700">8.0%</text>
  <!-- 2048/4096 -->
  <text x="220" y="224" text-anchor="end" fill="#334155" font-size="12">2048 / 4096 (long only)</text>
  <rect x="230" y="212" width="10" height="20" rx="4" fill="#ef4444" opacity="0.85"/>
  <text x="660" y="227" text-anchor="end" font-size="11" fill="#dc2626" font-weight="700">1.2%</text>
  <line x1="230" y1="84" x2="230" y2="244" stroke="#cbd5e1" stroke-dasharray="3,3"/>
  <rect x="60" y="262" width="600" height="40" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>
  <text x="360" y="285" text-anchor="middle" font-size="12" fill="#475569" font-style="italic">
    Short-context training is what makes the first-token sink useful. Remove it, and the model never learns to dump.
  </text>
</svg>

#### Key Takeaways

- **Sinks are partly a data-distribution phenomenon**: training only on long-context positions collapses sinks to ~1-13%.
- **The first token is a cheap universal "ignore far context" reference**: in mixed-length training, it lets the model ignore distant tokens for short-range prediction.
- **Architectural and data-side mitigations are both available**: if you want to avoid sinks, you can change the architecture (gated attention, alternative norm) *or* change the training context distribution.

---

## Discussion

### Overview

Pulled together, the picture is coherent. Pre-norm Transformers, as currently trained, have a quirky internal logic. The first token, which can only attend to itself, sits in a structurally privileged position; the model learns to push its representation in a direction `s*` that the SwiGLU FFN can amplify quadratically; that amplification dumps massive values into a few specific channels, which persist through the residual stream as approximately constant signals (implicit parameters, not data); RMSNorm then transforms those large values into a sparse, near-constant input vector; the learned key projection `W_K` notices that the first-token keys cluster in a tiny subspace, and partitions the key space accordingly; some heads orient their queries toward the sink subspace and become sink heads, which is useful because dumping attention into the first token is a cheap way to bias toward short-range prediction in mixed-length training.

So the spike-and-sink couple is not one phenomenon; it is two phenomena tied together by an architectural choice (pre-norm + RMSNorm) and a training distribution choice (mixed-length context). Each can be undone:

- **Suppress spikes, keep sinks**: sandwich norm, QKNorm, DynamicTanh.
- **Suppress sinks, keep spikes**: per-channel or per-head conditional gating; long-only training distribution.
- **Suppress both**: combining the above.
- **In every case, language-modeling perplexity is preserved**.

That last point is the load-bearing engineering claim. If the spike-and-sink coupling were doing something *necessary*, suppressing it would damage the model. It does not. Their overlap in standard pretrained LLMs is best understood as a byproduct of the default normalization-and-training recipe, not a reflection of any underlying functional necessity.

For practitioners, the main implications:

- **Quantization gets easier with the right normalizer.** A model trained with sandwich norm or QKNorm has 6-40x smaller spike magnitudes, which directly translates to lower precision-loss in INT4 / FP4 quantization without specialized outlier handling.
- **KV-cache strategies that rely on sinks need not break under spike suppression.** Sinks survive most spike-killing interventions, including DynamicTanh (where they actually strengthen).
- **Long-context-only training is a different regime.** If you fine-tune a base model exclusively on very long sequences, expect attention sinks to fade — which may or may not be what you want depending on your inference pipeline.

The bigger picture: this paper continues a useful trend of treating "weird LLM behaviors" as *architectural artifacts to be designed around*, rather than mysterious emergent properties. Spikes and sinks are not magic; they are the predictable output of pre-norm + RMSNorm + SwiGLU + mixed-length training, and we now have a menu of replacements for each ingredient.

### Concept Diagram

<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="disc-diag-title">
  <title id="disc-diag-title">Levers for suppressing spikes and sinks independently</title>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">
    A 2x2 of architectural levers
  </text>
  <text x="360" y="42" text-anchor="middle" font-size="11" fill="#64748b">
    Each axis: which phenomenon does the intervention suppress?
  </text>
  <!-- Quadrants -->
  <line x1="80" y1="80" x2="80" y2="320" stroke="#94a3b8"/>
  <line x1="640" y1="80" x2="640" y2="320" stroke="#94a3b8"/>
  <line x1="80" y1="200" x2="640" y2="200" stroke="#94a3b8"/>
  <line x1="80" y1="80" x2="640" y2="80" stroke="#94a3b8"/>
  <line x1="80" y1="320" x2="640" y2="320" stroke="#94a3b8"/>
  <line x1="360" y1="80" x2="360" y2="320" stroke="#94a3b8"/>
  <!-- Axis labels -->
  <text x="360" y="74" text-anchor="middle" font-size="12" font-weight="600" fill="#475569">Affects spikes?</text>
  <text x="60" y="200" text-anchor="end" font-size="12" font-weight="600" fill="#475569" transform="rotate(-90 60 200)">Affects sinks?</text>
  <text x="220" y="98" text-anchor="middle" font-size="11" fill="#64748b">no</text>
  <text x="500" y="98" text-anchor="middle" font-size="11" fill="#64748b">yes</text>
  <text x="74" y="140" text-anchor="end" font-size="11" fill="#64748b">yes</text>
  <text x="74" y="260" text-anchor="end" font-size="11" fill="#64748b">no</text>
  <!-- Quadrant 1: top-left, kills sinks but not spikes -->
  <text x="220" y="130" text-anchor="middle" font-weight="700" fill="#1e40af" font-size="12">Conditional gating</text>
  <text x="220" y="148" text-anchor="middle" font-size="11" fill="#1e40af">per-channel / per-head</text>
  <text x="220" y="166" text-anchor="middle" font-size="11" fill="#1e40af">long-only training</text>
  <text x="220" y="184" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">sinks ↓, spikes ~ same</text>
  <!-- Quadrant 2: top-right, kills both -->
  <text x="500" y="130" text-anchor="middle" font-weight="700" fill="#a855f7" font-size="12">Combined</text>
  <text x="500" y="148" text-anchor="middle" font-size="11" fill="#6b21a8">DynamicTanh + gated attn</text>
  <text x="500" y="166" text-anchor="middle" font-size="11" fill="#6b21a8">QKNorm + gated attn</text>
  <text x="500" y="184" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">both phenomena suppressed</text>
  <!-- Quadrant 3: bottom-left, baseline (no intervention) -->
  <text x="220" y="240" text-anchor="middle" font-weight="700" fill="#94a3b8" font-size="12">Baseline (do nothing)</text>
  <text x="220" y="258" text-anchor="middle" font-size="11" fill="#64748b">pre-norm + SwiGLU</text>
  <text x="220" y="276" text-anchor="middle" font-size="11" fill="#64748b">mixed-length training</text>
  <text x="220" y="294" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">spikes + sinks (the puzzle)</text>
  <!-- Quadrant 4: bottom-right, kills spikes but not sinks -->
  <text x="500" y="240" text-anchor="middle" font-weight="700" fill="#16a34a" font-size="12">Sandwich / QKNorm / DyT</text>
  <text x="500" y="258" text-anchor="middle" font-size="11" fill="#166534">linear / attention-only FFN</text>
  <text x="500" y="276" text-anchor="middle" font-size="11" fill="#166534">(quantization-friendly)</text>
  <text x="500" y="294" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">spikes ↓, sinks ~ same</text>
</svg>

### Key Takeaways

- **Two phenomena, two levers**: normalization controls spikes; gated attention and short-context training control sinks. They are not knobs on the same machine.
- **No language-modeling cost**: every intervention examined preserves perplexity. The spike-and-sink coupling is not load-bearing for next-token prediction.
- **Engineering frontier widens**: low-precision serving (which wants no spikes) and streaming inference (which wants sinks) are no longer in tension once you pick the right combination of normalizer and gating.

---

## Key Takeaways (Summary)

- **Massive activations and attention sinks share tokens but not mechanisms**: they co-occur because pre-norm + RMSNorm bridges them, not because one causes the other.
- **Spikes are a directional quadratic amplifier story**: SwiGLU's gated structure makes the FFN behave like `h^T S_k h`; a few rank-one-dominated `S_k` blow up a single direction `s*`, which the first token consistently aligns with.
- **Sinks are a geometric story**: RMSNorm collapses spike tokens to a sparse near-constant vector, so sink keys live in a 1-2 dim subspace. `W_K` partitions, heads pick a side based on query alignment.
- **The engineering payoff is real**: swap the normalizer to suppress spikes (good for INT4/FP4 quantization) while keeping sinks (good for streaming inference / KV-cache).
- **Sinks are also a training-distribution phenomenon**: in long-only training, they collapse to ~1-13%. Mixed-length training is what makes the first-token sink *useful* in the first place.
- **The bigger picture**: these are designable artifacts, not emergent magic. The recipe `pre-norm + RMSNorm + SwiGLU + mixed-length training` is one path; the menu of alternatives is now mapped.
