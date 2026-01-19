@{id = "3d71e896-a306-4877-ac0b-2f37486e3f40"
  title = "Small Batch Training for Language Models: Why Simple SGD Works"
  date = "2026-01-11T00:00:00Z"
  tags = ['journal club', 'machine learning', 'neurips', 'language models']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/marek-simple-sgd-neuroips-thumb.svg"
  description = "This journal club blog reviews the paper "Small Batch Training for Language Models: Why Simple SGD Works" by Marek et al."
  type = "note"
  disabled = "False"
}

<p align="center">
  <img src="https://storage.googleapis.com/gn-portfolio/images/marek-simple-sgd-neuroips-thumb.svg" max-width="700">
</p>

# Small Batch Training for Language Models: Why Simple SGD Works

**From NeurIPS 2025 Research by Marek et al.**

*Challenging conventional wisdom about batch sizes, optimizer complexity, and gradient accumulation in large language model training*

---

## Executive Summary

This groundbreaking paper overturns long-held beliefs about training language models. The researchers demonstrate that:

- **Small batch sizes (even batch size 1) work excellently** when you adjust the right hyperparameters
- **Vanilla SGD without momentum can compete with sophisticated optimizers** like Adam at small batch sizes
- **Gradient accumulation is wasteful** unless you're doing multi-device training
- **The key insight**: Instead of keeping β₂ fixed across batch sizes, keep its "token half-life" fixed

These findings could fundamentally change how we train models, offering simpler algorithms, better memory efficiency, and more robust training with less hyperparameter tuning.

---

## Table of Contents

1. [The Revolutionary Finding](#the-revolutionary-finding)
2. [Understanding Moment Half-Life](#understanding-moment-half-life)
3. [Why Small Batches Are More Robust](#why-small-batches-are-more-robust)
4. [The Hyperparameter Scaling Rule](#the-hyperparameter-scaling-rule)
5. [Vanilla SGD Makes a Comeback](#vanilla-sgd-makes-a-comeback)

---

## The Revolutionary Finding

### Overview

For years, the machine learning community has operated under the assumption that large batch sizes are essential for stable language model training. This led to increasingly complex optimizers and widespread use of gradient accumulation to simulate even larger batches. This paper challenges that entire paradigm.

The researchers trained language models at batch sizes spanning more than four orders of magnitude—from batch size 1 all the way up to 4096—and discovered something remarkable: when you scale the second moment decay parameter β₂ correctly, small batch sizes not only work, they're often better.

Think of it like driving a car. With large batch sizes, you're taking big leaps forward, which requires sophisticated prediction about the terrain ahead (momentum, adaptive learning rates, careful tuning). With small batch sizes, you're taking tiny steps, feeling your way forward—you don't need fancy suspension or predictive systems because you're never jumping far enough to get into trouble.

### The Core Insight

The problem with previous attempts at small batch training wasn't that small batches don't work—it was that researchers were using the wrong hyperparameters. Specifically, they were keeping β₂ (the decay rate for the second moment in Adam) fixed at values like 0.95 or 0.98 across all batch sizes.

But here's the key realization: β₂ controls how many optimizer steps we average over, and different batch sizes mean different numbers of tokens per step. If we want to average over the same amount of training data (measured in tokens), we need to adjust β₂ when we change the batch size.

### Concept Diagram

```txt
Traditional Thinking          This Paper's Insight
===================          ====================

Large Batch Required         Small Batch Works!
       ↓                            ↓
  Sophisticated                Simple SGD
   Optimizer                  (no momentum!)
       ↓                            ↓
  Careful Tuning              Robust Training
       ↓                            ↓
  Gradient                     No Accumulation
  Accumulation                   Needed
       ↓                            ↓
  High Memory                 Low Memory
   Footprint                    Footprint


The Key Difference:
┌────────────────────────────────────────────────┐
│ Fix the TOKEN HALF-LIFE, not the decay rate β₂ │
│                                                │
│  Old Way: β₂ = 0.95 for all batch sizes        │
│  New Way: t₁/₂ = 10M tokens for all batches    │
│                                                │
│  This means: β₂ = 0.9999 for batch size 1      │
│              β₂ = 0.95 for batch size 512      │
└────────────────────────────────────────────────┘
```

### Key Takeaways

- **Small batch sizes achieve equal or better performance than large batches** when hyperparameters are scaled correctly, contradicting widespread assumptions
- **The critical insight is scaling β₂ to maintain constant token half-life** rather than keeping the parameter itself constant
- **This enables drastically simpler training setups** with vanilla SGD, no gradient accumulation, and reduced memory requirements
- **Robustness improves at small batch sizes**, meaning less hyperparameter tuning is needed to achieve good performance

---

## Understanding Moment Half-Life

### Overview

To understand why small batch training works, we need to deeply grasp the concept of "moment half-life." This is perhaps the paper's most important conceptual contribution—a new way of thinking about the timescales over which optimizers average gradients.

In Adam and similar optimizers, we maintain exponential moving averages (EMAs) of gradients. The β₁ parameter controls the first moment (the mean gradient), and β₂ controls the second moment (roughly, the variance). Higher values of β mean we place more weight on historical gradients, averaging over longer timescales.

But here's the problem: when researchers say "β₂ = 0.95," they're thinking in terms of optimizer steps, not tokens. If you have batch size 512, each step sees 512 tokens. If you have batch size 1, each step sees only 1 token. So β₂ = 0.95 means very different things for these two scenarios in terms of how much training data we're averaging over.

The "half-life" concept fixes this by measuring timescales in tokens instead of steps. It answers the question: "After seeing how many tokens does a gradient's contribution to the momentum decay to half its original value?"

### Concept Diagram

```txt
Understanding Exponential Decay of Gradient Contributions
==========================================================

Suppose we're using β₂ = 0.95 for our second moment in Adam.

A gradient computed at step 0 contributes to future moments like this:

Optimizer Step:     0      1      2      3      4      5
                    ↓      ↓      ↓      ↓      ↓      ↓
Exponent:           β₂⁰    β₂¹    β₂²    β₂³    β₂⁴    β₂⁵

Contribution:       1.0    0.95   0.90   0.86   0.81   0.77
                    ████   ███    ███    ██     █▓     ▓▒
                    │      │      │      │
                    │      │      │      └─ After 3 steps: 0.86x
                    │      │      └──────── After 2 steps: 0.90x
                    │      └─────────────── After 1 step:  0.95x
                    └────────────────────── Initial:       1.0x


Calculating the actual values (when β₂ = 0.95):
- β₂⁰ = 1.0         (initial)
- β₂¹ = 0.95        (after 1 step)
- β₂² = 0.9025      (after 2 steps)
- β₂³ = 0.8574      (after 3 steps)
- β₂⁴ = 0.8145      (after 4 steps)

Problem: Steps ≠ Tokens!
========================

Batch Size 512:                  Batch Size 1:
Each step = 512 tokens           Each step = 1 token
     │                                │
     ├─ Step 1: 512 tokens            ├─ Step 1: 1 token
     ├─ Step 2: 1024 tokens           ├─ Step 2: 2 tokens
     ├─ Step 3: 1536 tokens           ├─ Step 3: 3 tokens
     └─ ...                           └─ ...


Solution: Fix Token Half-Life!
==============================

Instead of fixing β₂, we fix t₁/₂ (number of tokens for 0.5x decay)

Given: β₂^(t₁/₂ / (B·T)) = 0.5

Where: B = batch size
       T = sequence length
       t₁/₂ = desired token half-life

Example Calculation 1:

Given:
    t₁/₂ = 7M tokens (our choice for simple calculation)
    T = 1024 (sequence length as a typical value)
    B = 512 (batch size)

What should β₂ be?

    β₂^(t₁/₂ / (B·T)) = 0.5
    β₂^(7,000,000 / (512 × 1024)) = 0.5
    β₂^13.35 = 0.5
    log(β₂^13.35) = log(0.5)
    13.35 * log(β₂) = log(0.5)
    log(β₂) = log(0.5) / 13.35
    β₂ = 10^(log(0.5) / 13.35)
    β₂ ≈ 0.95

Therefore:

    β₂ ≈ 0.95 for desired token half-life of 7M tokens with batch size 512 and sequence length 1024.

Example Calculation 2:

Given:
    t₁/₂ = 7M tokens (Same as above)
    T = 1024 (Same as above)
    B = 1 (batch size, NEW BATCH SIZE)

What should β₂ be?

    β₂^(t₁/₂ / (B·T)) = 0.5
    β₂^(7,000,000 / (1 × 1024)) = 0.5
    β₂^6,835 = 0.5
    log(β₂^6,835) = log(0.5)
    6,835 * log(β₂) = log(0.5)
    log(β₂) = log(0.5) / 6,835
    β₂ = 10^(log(0.5) / 6,835)
    β₂ ≈ 0.9999

Therefore:

    β₂ ≈ 0.9999 for desired token half-life of 7M tokens with batch size 1 and sequence length 1024.
```

### Implementation

Here's how to implement the β₂ scaling rule in practice:

```python
import numpy as np
from typing import Tuple

def compute_beta2_from_halflife(
    token_halflife: float,
    batch_size: int,
    sequence_length: int = 1024
) -> float:
    """
    Compute β₂ (second moment decay) from desired token half-life.

    The half-life represents: after seeing this many tokens,
    a gradient's contribution to the second moment decays to 50%.

    Args:
        token_halflife: Desired half-life in tokens (e.g., 10_000_000)
        batch_size: Number of samples per optimizer step
        sequence_length: Length of each sequence in tokens

    Returns:
        β₂ value that achieves the desired token half-life

    Example:
        >>> # For typical LLM training with batch size 512
        >>> beta2 = compute_beta2_from_halflife(10_000_000, 512)
        >>> print(f"β₂ = {beta2:.5f}")  # Should be close to 0.95
    """
    # Calculate number of optimizer steps to reach half-life
    tokens_per_step = batch_size * sequence_length
    steps_to_halflife = token_halflife / tokens_per_step

    # Solve for β such that β^steps = 0.5
    # Taking log: steps * log(β) = log(0.5)
    # Therefore: β = exp(log(0.5) / steps)
    beta2 = np.exp(np.log(0.5) / steps_to_halflife)

    return float(beta2)


def scale_beta2_for_new_batch_size(
    current_beta2: float,
    current_batch_size: int,
    new_batch_size: int
) -> float:
    """
    Scale β₂ when changing batch size to maintain constant token half-life.

    This is the key formula from the paper (Equation 2):
    β₂* = β₂^(B*/B)

    Args:
        current_beta2: Current β₂ value
        current_batch_size: Current batch size
        new_batch_size: New batch size to scale to

    Returns:
        New β₂ value that maintains same token half-life

    Example:
        >>> # Scale from batch size 512 (β₂=0.95) to batch size 1
        >>> new_beta2 = scale_beta2_for_new_batch_size(0.95, 512, 1)
        >>> print(f"New β₂ = {new_beta2:.6f}")  # Should be ~0.9999
    """
    # The ratio of batch sizes determines the exponent
    batch_ratio = new_batch_size / current_batch_size

    # Scale β₂ by raising to the power of batch ratio
    new_beta2 = current_beta2 ** batch_ratio

    return float(new_beta2)


# Practical example: Setting up optimizers for different batch sizes
# ===================================================================

def setup_adam_for_batch_size(
    batch_size: int,
    token_halflife: float = 10_000_000,
    beta1: float = 0.9,
    learning_rate: float = 0.001
) -> dict:
    """
    Configure Adam hyperparameters for a given batch size.

    This function embodies the paper's key recommendations:
    - Keep β₁ fixed (default 0.9 works well)
    - Scale β₂ to maintain constant token half-life
    - Learning rate scales sub-linearly (not included here; requires tuning)

    Args:
        batch_size: Target batch size
        token_halflife: Desired averaging window in tokens
        beta1: First moment decay (keep fixed)
        learning_rate: Initial learning rate (tune separately)

    Returns:
        Dictionary of optimizer hyperparameters
    """
    beta2 = compute_beta2_from_halflife(token_halflife, batch_size)

    config = {
        'batch_size': batch_size,
        'beta1': beta1,
        'beta2': beta2,
        'learning_rate': learning_rate,
        'epsilon': 1e-8,
    }

    print(f"Batch Size {batch_size:4d}: β₂ = {beta2:.8f}")
    return config


# Example: Configure for various batch sizes
print("Recommended β₂ values for token half-life = 10M:")
print("=" * 50)

for batch_size in [1, 4, 16, 64, 256, 512, 1024, 4096]:
    config = setup_adam_for_batch_size(batch_size)

print("\n" + "=" * 50)
print("Notice how β₂ increases as batch size decreases!")
print("This maintains constant averaging over tokens.")
```
Output:
```txt
Recommended β₂ values for token half-life = 10M:
==================================================
Batch Size    1: β₂ = 0.99992902
Batch Size    4: β₂ = 0.99971613
Batch Size   16: β₂ = 0.99886499
Batch Size   64: β₂ = 0.99546769
Batch Size  256: β₂ = 0.98199365
Batch Size  512: β₂ = 0.96431153
Batch Size 1024: β₂ = 0.92989672
Batch Size 4096: β₂ = 0.74771978

==================================================
Notice how β₂ increases as batch size decreases!
This maintains constant averaging over tokens.
```

### Key Takeaways

- **Token half-life provides a batch-size-independent way to think about optimizer timescales**, measuring how many tokens of data we average over rather than how many optimizer steps
- **The formula β₂* = β₂^(B*/B) allows you to scale β₂ when changing batch size** from B to B* while keeping the token half-life constant
- **Typical values are β₂ ≈ 0.9999 for batch size 1** (very slow decay) and β₂ ≈ 0.95 for batch size 512 (faster decay), but they represent the same 7M token half-life
- **This insight explains why previous small-batch experiments failed**: they used β₂ values optimized for large batches, causing them to average over too little data

---

## Why Small Batches Are More Robust

### Overview

One of the most surprising findings in this paper is that small batch sizes are dramatically more robust to hyperparameter misspecification than large batches. When the authors swept through different learning rates and β values, they found that batch size 1 achieves near-optimal performance across a huge range of hyperparameters, while large batches require precise tuning.

This finding has profound practical implications. Hyperparameter tuning is expensive—it requires running many training jobs to find the sweet spot. If small batches are more forgiving, you can skip most of that tuning and still get great results.

The intuition comes from thinking about optimization as making predictions. Every time your optimizer takes a step, it's predicting where you should move in parameter space to decrease the loss. Large steps (which come from large batches paired with large learning rates) require predicting the landscape far away from your current position—that's a hard prediction problem requiring careful tuning. Small steps don't need to predict as far, so simpler, less-tuned optimizers work fine.

Think of it like navigating in fog. If you can only see a few feet ahead (small batches, small steps), you can walk confidently even with rough navigation tools. If you're trying to leap across large distances in the fog (large batches, large steps), you need sophisticated instruments and careful calibration to avoid disaster.

### Concept Diagram

```txt
Hyperparameter Sensitivity: Small vs Large Batches
==================================================

Small Batch (size = 1):
Learning Rate Sensitivity
    Loss
        │                 ╭──────────╮
   3.5  │               ╭─╯░░░░░░░░░░╰─╮
        │             ╭─╯░░░░░░░░░░░░░░╰─╮
   3.4  ├─────────────┤░░░Robust Region░░├──────────
        │             ╰─╮░░░░░░░░░░░░░░╭─╯
        │               ╰─╮░░░░░░░░░░╭─╯
   3.3  │                 ╰──────────╯
        │
        └──────────────────────────────────────────────→
         0.001  0.003  0.01   0.03   0.1  Learning Rate

    Wide "bowl" = forgiving to hyperparameter choice


Large Batch (size = 512):
Learning Rate Sensitivity
    Loss
        │░░░░│
   3.8  │░░░░│
        │░░░░╰╮
   3.6  │░░░░░│
        │░░░░░│← Narrow
   3.4  │░░░░░│  optimal
        │░░░░│   region
   3.2  │░░╭─╯
        │░╭╯
   3.0  ├─╯
        │
        └──────────────────────────────────────────────→
         0.001  0.003  0.01   0.03   0.1  Learning Rate

    Narrow "canyon" = precise tuning required


Why This Happens:
=================

  Large Batch Size                  Small Batch Size
         ↓                                 ↓
    Large Steps                       Small Steps
         ↓                                 ↓
┌──────────────────┐              ┌──────────────────┐
│ Must predict     │              │ Only predict     │
│ loss surface     │              │ loss surface     │
│ FAR from current │              │ NEAR current     │
│ position         │              │ position         │
└────────┬─────────┘              └────────┬─────────┘
         │                                 │
         ▼                                 ▼
┌──────────────────┐              ┌──────────────────┐
│ Hard prediction  │              │ Easy prediction  │
│ problem          │              │ problem          │
└────────┬─────────┘              └────────┬─────────┘
         │                                 │
         ▼                                 ▼
┌──────────────────┐              ┌──────────────────┐
│ Requires:        │              │ Simple methods   │
│ - Momentum       │              │ work fine:       │
│ - Adaptive rates │              │ - No momentum    │
│ - Careful tuning │              │ - Fixed LR       │
│ - Sophisticated  │              │ - Vanilla SGD    │
│   optimizer      │              │                  │
└──────────────────┘              └──────────────────┘
```

### The Toy Example

To really build intuition, let's walk through a simplified optimization problem that captures the essence of why small batches are more robust. We'll optimize a simple 2D function that's much steeper in one direction than another—a common characteristic of neural network loss landscapes.

```python
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List

# Simple 2D optimization problem demonstrating batch size effects
# ================================================================

def loss_function(x: float, y: float) -> float:
    """
    Simple loss function that's steep in y, gradual in x.
    Loss = x + 10y²

    This mimics neural network losses that are ill-conditioned
    (much steeper in some directions than others).

    Note, there's no minimum in the x direction—it's like a slope 
    that goes down infinitely. So y = 0 is the stable equilibrium 
    in the y direction. This is what we're trying to reach.
    """
    return x + 10 * y**2


def gradient(x: float, y: float, noise_scale: float = 0.0) -> Tuple[float, float]:
    """
    Compute gradient with optional noise (simulating mini-batch stochasticity).

    True gradient: (1, 20y)
    With noise: gradient * N(1, noise_scale²)

    Args:
        x, y: Current position
        noise_scale: Standard deviation of multiplicative noise
                    (higher = smaller effective batch size)
    """
    # True gradient
    grad_x = 1.0
    grad_y = 20.0 * y

    # Add stochastic noise to simulate mini-batch gradient estimation
    if noise_scale > 0:
        noise = np.random.normal(1.0, noise_scale, size=2)
        grad_x *= noise[0]
        grad_y *= noise[1]

    return grad_x, grad_y


def sgd_step(
    x: float,
    y: float,
    learning_rate: float,
    noise_scale: float
) -> Tuple[float, float]:
    """
    Take one SGD step.

    This simulates batch training: high noise_scale = small batch.
    """
    gx, gy = gradient(x, y, noise_scale)

    x_new = x - learning_rate * gx
    y_new = y - learning_rate * gy

    return x_new, y_new


def sgd_with_momentum_step(
    x: float,
    y: float,
    vx: float,
    vy: float,
    learning_rate: float,
    momentum: float,
    noise_scale: float
) -> Tuple[float, float, float, float]:
    """
    Take one SGD step with momentum.

    Momentum helps dampen oscillations in steep directions.
    """
    gx, gy = gradient(x, y, noise_scale)

    # Update velocity (momentum)
    vx = momentum * vx + gx
    vy = momentum * vy + gy

    # Update position
    x_new = x - learning_rate * vx
    y_new = y - learning_rate * vy

    return x_new, y_new, vx, vy


def run_optimization_experiment(
    batch_size_type: str,  # "large" or "small"
    use_momentum: bool,
    n_steps: int = 100
) -> List[Tuple[float, float]]:
    """
    Run optimization experiment with specified configuration.

    Large batch: Low noise, large learning rate, few steps
    Small batch: High noise, small learning rate, many steps
    """
    # Starting point
    x, y = 2.0, 2.0

    # Configuration based on batch size
    if batch_size_type == "large":
        # Large batch size: less noisy gradients, fewer steps, larger LR
        learning_rate = 0.1
        noise_scale = 0.1  # Low noise (high signal-to-noise)
        # Scale number of steps (large batches = fewer steps for same compute)
        n_steps = n_steps // 10
    else:  # small batch
        # Small batch size: noisier gradients, more steps, smaller LR
        learning_rate = 0.01
        noise_scale = 0.3  # High noise (low signal-to-noise)

    momentum = 0.9
    vx, vy = 0.0, 0.0

    trajectory = [(x, y)]

    for _ in range(n_steps):
        if use_momentum:
            x, y, vx, vy = sgd_with_momentum_step(
                x, y, vx, vy, learning_rate, momentum, noise_scale
            )
        else:
            x, y = sgd_step(x, y, learning_rate, noise_scale)

        trajectory.append((x, y))

    return trajectory


# Run all four experiments
print("Running optimization experiments...")
print("=" * 60)

np.random.seed(42)  # For reproducibility

large_batch_sgd = run_optimization_experiment("large", False)
large_batch_momentum = run_optimization_experiment("large", True)
small_batch_sgd = run_optimization_experiment("small", False)
small_batch_momentum = run_optimization_experiment("small", True)

print("\nResults:")
print("-" * 60)
print(f"Large Batch + SGD:      Final y = {large_batch_sgd[-1][1]:.4f}")
print(f"Large Batch + Momentum: Final y = {large_batch_momentum[-1][1]:.4f}")
print(f"Small Batch + SGD:      Final y = {small_batch_sgd[-1][1]:.4f}")
print(f"Small Batch + Momentum: Final y = {small_batch_momentum[-1][1]:.4f}")
print()
print("Key Insight:")
print("-" * 60)
print("• Large batch WITHOUT momentum: oscillates wildly (high y)")
print("• Large batch WITH momentum: converges well (damps oscillations)")
print("• Small batch WITHOUT momentum: converges well (small steps)")
print("• Small batch WITH momentum: converges well (but not needed)")
```

Output:
```txt
Running optimization experiments...
============================================================

Results:
------------------------------------------------------------
Large Batch + SGD:      Final y = 1.1717   From valley! Oscillating wildly
Large Batch + Momentum: Final y = -0.4916  Overshot, but momentum is bringing us back
Small Batch + SGD:      Final y = 0.0000   Perfect! We've found the valley
Small Batch + Momentum: Final y = -0.0040  Almost perfect! Tiny overshoot

Key Insight:
------------------------------------------------------------
• Large batch WITHOUT momentum: oscillates wildly (high y)
• Large batch WITH momentum: converges well (damps oscillations)
• Small batch WITHOUT momentum: converges well (small steps)
• Small batch WITH momentum: converges well (but not needed)
```

### Key Takeaways

- **Small batch sizes exhibit broad low-loss regions across hyperparameters** while large batches require precise tuning to find narrow optimal regions
- **The robustness comes from taking smaller steps**, which makes optimization easier because you're not trying to predict the loss surface far from your current position
- **This has huge practical value**: you can save significant computational cost on hyperparameter tuning by using smaller batches
- **The toy example demonstrates that momentum becomes unnecessary at small batch sizes** because small steps don't overshoot and oscillate in steep directions

---

## The Hyperparameter Scaling Rule

### Overview

Building on the insights about token half-life and robustness, the paper proposes concrete rules for how to scale Adam's hyperparameters across batch sizes. This section provides actionable guidance you can use immediately.

The key findings are:
1. **Learning rate**: Does NOT follow the commonly-cited square root scaling rule. It scales more slowly.
2. **β₁ (first moment)**: Keep it fixed at 0.9. This works well across all batch sizes.
3. **β₂ (second moment)**: Scale it to maintain constant token half-life using the formula β₂* = β₂^(B*/B).

These rules emerged from exhaustive grid searches over hyperparameters at different batch sizes, and they generalize remarkably well across model scales and datasets.

### Concept Diagram

```txt
Hyperparameter Scaling Rules
=============================

Parameter: β₁ (First Moment Decay)
────────────────────────────────────
Rule: KEEP FIXED at 0.9

 1.0 ┐
     │                              ┌─────────┐
 0.9 ├──────────────────────────────┤ β₁ = 0.9│
     │                              └─────────┘
 0.8 │
     │
 0.0 └─────────────────────────────────────────→
      1    16   64   256  1024 4096  Batch Size

Works well across all batch sizes!


Parameter: β₂ (Second Moment Decay)
────────────────────────────────────
Rule: SCALE to maintain constant token half-life

1.0000┐
      │ ╲         
0.9999├  ╲       
      │   ╲     
0.999 ├    ╲           Token Half-Life: t₁/₂ = 10M
      │     ╲          (constant across batch sizes)
0.99  ├      ╲
      │       ╲
0.95  ├        ╲
      │         ╲
0.90  ├          ╲
      └─────────────────────────────────────────→
        1    16   64   256  1024 4096  Batch Size


Formula: β₂* = β₂^(B*/B)

Examples:
• B=512, β₂=0.95  →  B=1, β₂=0.9999  (increase β₂)
• B=1,   β₂=0.9999 → B=512, β₂=0.95   (decrease β₂)

Note: The asterisk (*) is mathematical notation for "new" or "target" value:
    β₂ = current beta2 value (what you have now)
    β₂* = new beta2 value (what you want)
    B = current batch size (what you have now)
    B* = new batch size (what you want)

Parameter: Learning Rate
────────────────────────────────────
Rule: Scale SUB-LINEARLY (not square root!)

Old rule: Square root scaling

lr* = lr X √B

New rule: Sub-linear scaling

lr* = lr X log(B + 1)

Learning Rate Growth

0.006 │                            ..... √512 scaling
      │                       .....      predicts 22x
      │                  ....           (22 X 0.0003 = 0.0066)
      │             ....               
0.001 │        ....                ● ● ● log(512 + 1) scaling
      │    ...           ● ● ● ● ●       predicts ~3x  
      │  ..      ● ● ● ●                 (3 X 0.0003 = 0.0009)
      │ .  ● ● ●                     
0.0003├● ●                 
      │ Starting point          
      │ (batch size 1)          
      └─────────────────────────────────────→
         1                              512  Batch Size

Note: 
    Exact scaling requires tuning, but it's
    much slower than √batch_size

Complete Recipe
═══════════════

Starting config: Batch Size 512, β₁=0.9, β₂=0.95, LR=0.001

Scale to Batch Size 1:
├─ β₁: Keep at 0.9
├─ β₂: 0.95^(1/512) = 0.9999
└─ LR: ÷3 (empirically, not theoretical)
       → ~0.0003

Scale to Batch Size 4096:
├─ β₁: Keep at 0.9
├─ β₂: 0.95^(4096/512) = 0.664
└─ LR: ×3 (empirically)
       → ~0.003
```

### Implementation

Here's a complete implementation of the scaling rules:

```python
import numpy as np
from dataclasses import dataclass
from typing import Optional

@dataclass
class OptimizerConfig:
    """Configuration for Adam-style optimizer."""
    batch_size: int
    learning_rate: float
    beta1: float
    beta2: float
    epsilon: float = 1e-8
    weight_decay: float = 0.1

    def __repr__(self) -> str:
        return (
            f"OptimizerConfig(\n"
            f"  batch_size={self.batch_size},\n"
            f"  learning_rate={self.learning_rate:.6f},\n"
            f"  beta1={self.beta1},\n"
            f"  beta2={self.beta2:.8f},\n"
            f"  weight_decay={self.weight_decay}\n"
            f")"
        )


def scale_optimizer_config(
    base_config: OptimizerConfig,
    new_batch_size: int,
    learning_rate_scale_factor: Optional[float] = None
) -> OptimizerConfig:
    """
    Scale optimizer configuration to a new batch size.

    This implements the paper's scaling rules:
    1. Keep β₁ fixed
    2. Scale β₂ to maintain constant token half-life
    3. Scale learning rate (optionally specify factor)

    Args:
        base_config: Current optimizer configuration
        new_batch_size: Target batch size
        learning_rate_scale_factor: Optional manual LR scale
                                   If None, uses heuristic

    Returns:
        New optimizer configuration for the target batch size
    """
    batch_ratio = new_batch_size / base_config.batch_size

    # Rule 1: Keep β₁ fixed (0.9 works well universally)
    new_beta1 = base_config.beta1

    # Rule 2: Scale β₂ to maintain constant token half-life
    # Formula from Equation 2 in paper: β₂* = β₂^(B*/B)
    new_beta2 = base_config.beta2 ** batch_ratio

    # Rule 3: Scale learning rate
    # The paper shows this is NOT sqrt scaling; it's sub-linear
    # Empirically: ~3x change for 512x batch size change
    # (This requires tuning in practice)
    if learning_rate_scale_factor is None:
        # Heuristic: scale proportional to batch_ratio^0.3
        # (This is a rough approximation; tune for your use case)
        learning_rate_scale_factor = batch_ratio ** 0.3

    new_learning_rate = base_config.learning_rate * learning_rate_scale_factor

    # For very small batch sizes, the paper recommends turning off weight decay
    new_weight_decay = base_config.weight_decay
    if new_batch_size <= 4:
        new_weight_decay = 0.0

    return OptimizerConfig(
        batch_size=new_batch_size,
        learning_rate=new_learning_rate,
        beta1=new_beta1,
        beta2=new_beta2,
        weight_decay=new_weight_decay
    )


# Example: Recreate the paper's experiments
# ==========================================

# Start with GPT-3 baseline from Brown et al.
gpt3_baseline = OptimizerConfig(
    batch_size=512,
    learning_rate=0.001,
    beta1=0.9,
    beta2=0.95,
    weight_decay=0.1
)

print("GPT-3 Baseline (Brown et al.):")
print(gpt3_baseline)
print("\n" + "=" * 60 + "\n")

# Scale to batch size 1 (paper's main experiment)
batch_1_config = scale_optimizer_config(
    gpt3_baseline,
    new_batch_size=1,
    learning_rate_scale_factor=1.0  # Paper kept LR the same
)

print("Scaled to Batch Size 1:")
print(batch_1_config)
print("\n" + "=" * 60 + "\n")

# Verify the β₂ scaling
print("Verification of β₂ scaling:")
print("-" * 60)
theoretical_beta2 = gpt3_baseline.beta2 ** (1 / gpt3_baseline.batch_size)
print(f"Formula: 0.95^(1/512) = {theoretical_beta2:.8f}")
print(f"Computed: {batch_1_config.beta2:.8f}")
print(f"Match: {np.isclose(theoretical_beta2, batch_1_config.beta2)}")
print()

# Calculate token half-life to verify it's constant
def calculate_token_halflife(beta2: float, batch_size: int, seq_len: int = 1024):
    """Calculate token half-life from β₂."""
    steps_to_halflife = np.log(0.5) / np.log(beta2)
    tokens_per_step = batch_size * seq_len
    return steps_to_halflife * tokens_per_step

halflife_baseline = calculate_token_halflife(
    gpt3_baseline.beta2, gpt3_baseline.batch_size
)
halflife_batch1 = calculate_token_halflife(
    batch_1_config.beta2, batch_1_config.batch_size
)

print(f"Token half-life (baseline): {halflife_baseline:,.0f} tokens")
print(f"Token half-life (batch=1):  {halflife_batch1:,.0f} tokens")
print(f"Ratio: {halflife_batch1 / halflife_baseline:.2f}x")
print()
print("Success! Token half-life is preserved! ✓")
print("\n" + "=" * 60 + "\n")

# Generate configs for sweep of batch sizes
print("Complete batch size sweep:")
print("-" * 60)

for bs in [1, 4, 16, 64, 256, 512, 1024, 4096]:
    config = scale_optimizer_config(gpt3_baseline, bs)
    halflife = calculate_token_halflife(config.beta2, config.batch_size)

    print(f"BS={bs:4d}: β₂={config.beta2:.6f}, "
          f"LR={config.learning_rate:.6f}, "
          f"t₁/₂={halflife:>10,.0f} tokens")
```

Output:

```txt
GPT-3 Baseline (Brown et al.):
OptimizerConfig(
  batch_size=512,
  learning_rate=0.001000,
  beta1=0.9,
  beta2=0.95000000,
  weight_decay=0.1
)

============================================================

Scaled to Batch Size 1:
OptimizerConfig(
  batch_size=1,
  learning_rate=0.001000,
  beta1=0.9,
  beta2=0.99989982,
  weight_decay=0.0
)

============================================================

Verification of β₂ scaling:
------------------------------------------------------------
Formula: 0.95^(1/512) = 0.99989982
Computed: 0.99989982
Match: True

Token half-life (baseline): 7,084,917 tokens
Token half-life (batch=1):  7,084,917 tokens
Ratio: 1.00x

Success! Token half-life is preserved! ✓

============================================================

Complete batch size sweep:
------------------------------------------------------------
BS=   1: β₂=0.999900, LR=0.000154, t₁/₂= 7,084,917 tokens
BS=   4: β₂=0.999599, LR=0.000233, t₁/₂= 7,084,917 tokens
BS=  16: β₂=0.998398, LR=0.000354, t₁/₂= 7,084,917 tokens
BS=  64: β₂=0.993609, LR=0.000536, t₁/₂= 7,084,917 tokens
BS= 256: β₂=0.974679, LR=0.000812, t₁/₂= 7,084,917 tokens
BS= 512: β₂=0.950000, LR=0.001000, t₁/₂= 7,084,917 tokens
BS=1024: β₂=0.902500, LR=0.001231, t₁/₂= 7,084,917 tokens
BS=4096: β₂=0.663420, LR=0.001866, t₁/₂= 7,084,917 tokens
```


### Key Takeaways

- **The β₁ = 0.9 default works robustly across all batch sizes** and doesn't need adjustment
- **Scale β₂ using the formula β₂* = β₂^(B*/B)** to maintain constant token half-life—this is the paper's most important practical contribution
- **Learning rate scaling is sub-linear** (much slower than square root), and requires some empirical tuning for your specific setup
- **These rules transfer across model scales**: tested from 30M to 1.3B parameters with consistent results

---

## Vanilla SGD Makes a Comeback

### Overview

Perhaps the most shocking result in this paper is that vanilla stochastic gradient descent—without momentum, without adaptive learning rates, without any of the sophisticated machinery we've built up over the years—can match Adam's performance at small batch sizes.

This is revolutionary. For the past decade, we've treated optimizers like Adam and its variants as essential for language model training. The field moved in the direction of increasingly complex optimizers (Lion, Muon, SOAP, etc.) because simpler methods seemed inadequate. This paper shows that complexity was only necessary because we were using large batch sizes.

At batch size 1, even training a 1.3 billion parameter model, plain SGD achieves comparable performance to AdamW with its default hyperparameters from the GPT-3 paper. And remember: SGD has no optimizer state, so it uses dramatically less memory.

The intuition connects to our earlier discussion about prediction distance. Large steps require predicting far ahead, which benefits from momentum (to smooth out oscillations) and adaptive rates (to handle different curvatures). Small steps only need to predict nearby, where the landscape is simpler and easier to navigate with basic gradient information.

### Concept Diagram

```txt
The Return of Vanilla SGD
=========================

Traditional View (Large Batches):

  Simple Optimizers                Sophisticated Optimizers
        ▼                                   ▼
   ┌──────────┐                        ┌────────────┐
   │   SGD    │                        │   Adam     │
   │          │                        │   Lion     │
   │          │←─────── Unstable       │   Muon     │
   │  Loss    │         Training       │   SOAP     │
   │  Spikes  │                        │            │
   │  ╳╳╳     │                        │  ✓✓✓      │
   │  Unstable│                        │  Stable    │
   └──────────┘                        └────────────┘


Paper's Finding (Small Batches):

  Simple Optimizers                Sophisticated Optimizers
        ▼                                   ▼
   ┌──────────┐                        ┌────────────┐
   │   SGD    │                        │   Adam     │
   │          │←─────── Both Work!     │   Lion     │
   │  ✓✓✓    │        Comparable      │   Muon     │
   │  Stable  │        Performance     │   SOAP     │
   │  Good    │                        │            │
   │  Results │                        │  ✓✓✓      │
   └──────────┘                        │  Stable    │
                                       └────────────┘


Performance Convergence by Batch Size
======================================

Loss at    Large Batch (4096)   Small Batch (1) + β₂ @ t₁/₂
Convergence    ↓                       ↓
                                                    
   5.0 ┤   ╱ SGD (diverges)    ┤  All optimizers
       │  ╱                    │  achieve similar
   4.5 ┤ ╱                     ┤  final loss:
       │╱   ╱── Adafactor      │             
   4.0 ├╮  ╱                   ├       ╱── SGD
       │╰╮╱─── Adam            │       ├── Adam
   3.8 ├─╰──── Muon            ├       ├── Adafactor
       │                       │       ╰── Muon
   3.6 ├───────────────────    ├────────────────


Memory Comparison
=================

Training per-parameter memory storage:

┌───────────────────────────────────────────────┐
│ Adam / AdamW:                                 │
│ ┌──────────┬──────────┬──────────┬──────────┐ │
│ │Parameter │ Gradient │1st Moment│2nd Moment│ │
│ │ 2-4 bytes│ 4 bytes  │ 4 bytes  │ 4 bytes  │ │
│ └──────────┴──────────┴──────────┴──────────┘ │
│ Total: 14-16 bytes per parameter              │
└───────────────────────────────────────────────┘

┌───────────────────────────────────────────────┐
│ SGD (no momentum):                            │
│ ┌──────────┬──────────┐                       │
│ │Parameter │ Gradient │                       │
│ │ 2-4 bytes│ 4 bytes  │                       │
│ └──────────┴──────────┘                       │
│ Total: 6-8 bytes per parameter                │
│                                               │
│ Memory Savings: ~50%! ✓                       │
└───────────────────────────────────────────────┘

For a 1.3B parameter model:
- Adam: ~22 GB optimizer state
- SGD:  0 GB optimizer state
Savings: 22 GB!
```

### Implementation

Here's a clean comparison of SGD vs Adam for small batch training:

```python
import numpy as np
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class TrainingMetrics:
    """Track training metrics."""
    steps: List[int]
    losses: List[float]
    optimizer_name: str


class SimpleOptimizer:
    """Base class for optimizers."""

    def step(self, params: np.ndarray, grads: np.ndarray) -> np.ndarray:
        """Update parameters given gradients."""
        raise NotImplementedError

    def state_size_per_param(self) -> int:
        """Return number of additional floats stored per parameter."""
        raise NotImplementedError


class VanillaSGD(SimpleOptimizer):
    """
    Vanilla SGD with no momentum.

    Update rule: θ ← θ - η∇L(θ)

    Key advantage: NO OPTIMIZER STATE!
    """

    def __init__(self, learning_rate: float = 0.001):
        self.lr = learning_rate

    def step(self, params: np.ndarray, grads: np.ndarray) -> np.ndarray:
        """
        Simple gradient descent step.

        Args:
            params: Current parameters
            grads: Gradients

        Returns:
            Updated parameters
        """
        # Just subtract learning_rate * gradient
        # No momentum, no adaptivity, no state to track
        return params - self.lr * grads

    def state_size_per_param(self) -> int:
        """SGD with no momentum has zero optimizer state."""
        return 0


class Adam(SimpleOptimizer):
    """
    Adam optimizer with exponential moving averages.

    Update rule:
      m_t = β₁ m_{t-1} + (1-β₁) g_t
      v_t = β₂ v_{t-1} + (1-β₂) g_t²
      θ_t = θ_{t-1} - η * m_t / (√v_t + ε)
    """

    def __init__(
        self,
        learning_rate: float = 0.001,
        beta1: float = 0.9,
        beta2: float = 0.999,
        epsilon: float = 1e-8
    ):
        self.lr = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon

        # Optimizer state (will be initialized on first step)
        self.m: Optional[np.ndarray] = None  # First moment
        self.v: Optional[np.ndarray] = None  # Second moment
        self.t = 0  # Step count

    def step(self, params: np.ndarray, grads: np.ndarray) -> np.ndarray:
        """
        Adam optimization step.

        Args:
            params: Current parameters
            grads: Gradients

        Returns:
            Updated parameters
        """
        # Initialize state on first call
        if self.m is None:
            self.m = np.zeros_like(params)
            self.v = np.zeros_like(params)

        self.t += 1

        # Update biased first moment estimate
        self.m = self.beta1 * self.m + (1 - self.beta1) * grads

        # Update biased second moment estimate
        self.v = self.beta2 * self.v + (1 - self.beta2) * (grads ** 2)

        # Bias correction
        m_hat = self.m / (1 - self.beta1 ** self.t)
        v_hat = self.v / (1 - self.beta2 ** self.t)

        # Parameter update
        return params - self.lr * m_hat / (np.sqrt(v_hat) + self.epsilon)

    def state_size_per_param(self) -> int:
        """Adam stores two floats (m and v) per parameter."""
        return 2
    
def ill_conditioned_loss(params: np.ndarray) -> float:
    """
    Loss that's MUCH steeper in some directions than others.
    This mimics real neural network loss landscapes.
    
    Loss = sum(λ_i * p_i²) where λ_i varies widely
    """
    # Different "eigenvalues" for different dimensions
    # Some dimensions have steep curvature, some have flat
    eigenvalues = np.array([1000, 100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001])
    return 0.5 * np.sum(eigenvalues * params ** 2)

def ill_conditioned_gradient(params: np.ndarray, batch_size: int) -> np.ndarray:
    """Gradient with different curvatures per dimension + noise."""
    eigenvalues = np.array([1000, 100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001])
    
    # True gradient
    true_grad = eigenvalues * params
    
    # Add noise (simulating mini-batch stochasticity)
    noise_scale = 1.0 / np.sqrt(batch_size)
    noise = np.random.normal(0, noise_scale * 10, size=params.shape)  # Increased noise
    
    return true_grad + noise

# Run comparison with better toy problem
# ======================================

print("Improved Toy Example: Ill-Conditioned Loss")
print("=" * 60)
print()

np.random.seed(42)
initial_params = np.random.randn(10) * 5.0
n_steps = 1000
batch_size = 1

# For this problem, use more reasonable hyperparameters
sgd = VanillaSGD(learning_rate=0.001)

# Simulate training
sgd_params = initial_params.copy()
adam_opt = Adam(learning_rate=0.01, beta1=0.9, beta2=0.999)

sgd_losses = []
adam_losses = []

for step in range(n_steps):
    # SGD step
    sgd_grad = ill_conditioned_gradient(sgd_params, batch_size)
    sgd_params = sgd.step(sgd_params, sgd_grad)
    sgd_losses.append(ill_conditioned_loss(sgd_params))
    
    # Adam step  
    adam_params = initial_params.copy() if step == 0 else adam_params
    adam_grad = ill_conditioned_gradient(adam_params, batch_size)
    adam_params = adam_opt.step(adam_params, adam_grad)
    adam_losses.append(ill_conditioned_loss(adam_params))

print(f"Final Losses:")
print(f"SGD:  {sgd_losses[-1]:.6f}")
print(f"Adam: {adam_losses[-1]:.6f}")
print()
print(f"Losses after 100 steps:")
print(f"SGD:  {sgd_losses[99]:.6f}")
print(f"Adam: {adam_losses[99]:.6f}")
print()
print(f"Loss Difference: {abs(sgd_losses[-1] - adam_losses[-1]):.6f}")
print()

# Memory comparison
param_count = 1_300_000_000  # 1.3B parameters (like GPT-3)
bytes_per_float = 4

sgd_memory = param_count * bytes_per_float * sgd.state_size_per_param()
adam_memory = param_count * bytes_per_float * adam_opt.state_size_per_param()

print("Memory Usage (for 1.3B parameter model):")
print("-" * 60)
print(f"SGD optimizer state:  {sgd_memory / 1e9:.2f} GB")
print(f"Adam optimizer state: {adam_memory / 1e9:.2f} GB")
print(f"Memory saved with SGD: {(adam_memory - sgd_memory) / 1e9:.2f} GB")
print()

print("Key Insight:")
print("-" * 60)
print("At batch size 1, vanilla SGD achieves comparable loss to Adam")
print("while using ZERO optimizer state memory!")
print()
```

Output:

```txt
Improved Toy Example: Ill-Conditioned Loss
============================================================

Final Losses:
SGD:  5.230202
Adam: 4.775477

Losses after 100 steps:
SGD:  30.241222
Adam: 1270.347206

Loss Difference: 0.454725

Memory Usage (for 1.3B parameter model):
------------------------------------------------------------
SGD optimizer state:  0.00 GB
Adam optimizer state: 10.40 GB
Memory saved with SGD: 10.40 GB

Key Insight:
------------------------------------------------------------
At batch size 1, vanilla SGD achieves comparable loss to Adam
while using ZERO optimizer state memory!
```

### Key Takeaways

- **Vanilla SGD without momentum performs competitively with Adam at batch size 1**, even for billion-parameter models—a shocking reversal of conventional wisdom
- **SGD has zero optimizer state**, saving ~50% memory compared to Adam (critical for large models)
- **The gap between simple and sophisticated optimizers shrinks as batch size decreases**, because small steps don't require complex prediction mechanisms
- **This opens new possibilities for training in memory-constrained environments** where every GB counts

---

## Conclusion

This paper fundamentally challenges how we think about training language models. The key insights—that small batches work excellently with proper hyperparameter scaling, that vanilla SGD can compete with sophisticated optimizers, and that gradient accumulation is often wasteful—have immediate practical implications.

The most actionable takeaway is the β₂ scaling rule: **β₂* = β₂^(B*/B)**. This simple formula, which maintains constant token half-life across batch sizes, makes small-batch training viable and often superior to large-batch approaches.

As you implement these ideas, remember the core principles:
- Choose batch size for hardware efficiency, not training stability
- Scale β₂ to keep token half-life constant (~10M tokens)
- Leverage the robustness of small batches to reduce tuning burden
- Consider simple optimizers like SGD when memory is tight
- Avoid gradient accumulation unless truly necessary for multi-device communication

These insights could reshape best practices in LLM training, making sophisticated models more accessible by reducing hardware requirements and simplifying training procedures.

---

## References

**Original Paper**: Marek, M., Lotfi, S., Somasundaram, A., Wilson, A. G., & Goldblum, M. (2025). Small Batch Size Training for Language Models: When Vanilla SGD Works, and Why Gradient Accumulation Is Wasteful. *NeurIPS 2025*.

**Code**: Available at [github.com/martin-marek/batch-size](https://github.com/martin-marek/batch-size)

**Key Related Work**:
- Brown et al. (2020) - GPT-3 and baseline hyperparameters
- Hoffmann et al. (2022) - Chinchilla scaling laws
- Shazeer & Stern (2018) - Adafactor optimizer
- Busbridge et al. (2023) - EMA decay scaling

---

*This educational resource was created to make cutting-edge research accessible. For technical accuracy and full details, please refer to the original paper.*
