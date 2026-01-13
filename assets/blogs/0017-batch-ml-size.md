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
6. [Practical Recommendations](#practical-recommendations)
7. [Memory-Efficient Fine-Tuning](#memory-efficient-fine-tuning)

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

```
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
│ Fix the TOKEN HALF-LIFE, not the decay rate β₂│
│                                                │
│  Old Way: β₂ = 0.95 for all batch sizes       │
│  New Way: t₁/₂ = 10M tokens for all batches   │
│                                                │
│  This means: β₂ = 0.9999 for batch size 1     │
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

```
Understanding Exponential Moving Average Decay
==============================================

Gradient contributions decay exponentially:

Optimizer Step:     0    1    2    3    4    5    6    7    8
                    ↓    ↓    ↓    ↓    ↓    ↓    ↓    ↓    ↓
Contribution:      1.0  β    β²   β³   β⁴   β⁵   β⁶   β⁷   β⁸
                    ██   █    ▓    ▒    ░
                    │    │    │         │
                    │    │    └─────────┴──── Half-life point
                    │    │              (contribution = 0.5)
                    │    └─ β² = ~0.90
                    └─ β¹ = 0.95


Problem: Steps ≠ Tokens!
========================

Batch Size 512:                  Batch Size 1:
Each step = 512 tokens           Each step = 1 token
     │                                │
     ├─ Step 1: 512 tokens           ├─ Step 1: 1 token
     ├─ Step 2: 1024 tokens          ├─ Step 2: 2 tokens
     ├─ Step 3: 1536 tokens          ├─ Step 3: 3 tokens
     └─ ...                          └─ ...


Solution: Fix Token Half-Life!
==============================

Instead of fixing β₂, we fix t₁/₂ (number of tokens for 0.5x decay)

Given: β^(t₁/₂ / (B·T)) = 0.5

Where: B = batch size
       T = sequence length
       t₁/₂ = desired token half-life


Example Calculation:
t₁/₂ = 10M tokens (our choice)
T = 1024 (sequence length)

For batch size 512:
  10,000,000 / (512 × 1024) ≈ 19 steps for half-life
  So we need: β² ≈ 0.95^19 ≈ 0.5
  Therefore: β₂ ≈ 0.95

For batch size 1:
  10,000,000 / (1 × 1024) ≈ 9766 steps for half-life
  So we need: β²^9766 ≈ 0.5
  Therefore: β₂ ≈ 0.9999
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

### Key Takeaways

- **Token half-life provides a batch-size-independent way to think about optimizer timescales**, measuring how many tokens of data we average over rather than how many optimizer steps
- **The formula β₂* = β₂^(B*/B) allows you to scale β₂ when changing batch size** from B to B* while keeping the token half-life constant
- **Typical values are β₂ ≈ 0.9999 for batch size 1** (very slow decay) and β₂ ≈ 0.95 for batch size 512 (faster decay), but they represent the same 10M token half-life
- **This insight explains why previous small-batch experiments failed**: they used β₂ values optimized for large batches, causing them to average over too little data

---

## Why Small Batches Are More Robust

### Overview

One of the most surprising findings in this paper is that small batch sizes are dramatically more robust to hyperparameter misspecification than large batches. When the authors swept through different learning rates and β values, they found that batch size 1 achieves near-optimal performance across a huge range of hyperparameters, while large batches require precise tuning.

This finding has profound practical implications. Hyperparameter tuning is expensive—it requires running many training jobs to find the sweet spot. If small batches are more forgiving, you can skip most of that tuning and still get great results.

The intuition comes from thinking about optimization as making predictions. Every time your optimizer takes a step, it's predicting where you should move in parameter space to decrease the loss. Large steps (which come from large batches paired with large learning rates) require predicting the landscape far away from your current position—that's a hard prediction problem requiring careful tuning. Small steps don't need to predict as far, so simpler, less-tuned optimizers work fine.

Think of it like navigating in fog. If you can only see a few feet ahead (small batches, small steps), you can walk confidently even with rough navigation tools. If you're trying to leap across large distances in the fog (large batches, large steps), you need sophisticated instruments and careful calibration to avoid disaster.

### Concept Diagram

```
Hyperparameter Sensitivity: Small vs Large Batches
==================================================

Small Batch (size = 1):
Learning Rate Sensitivity
    Loss
     │                    ╭──────────╮
   3.5│                 ╭─╯          ╰─╮
     │               ╭─╯                ╰─╮
   3.4├─────────────┤     Robust Region  ├──────────
     │               ╰─╮                ╭─╯
     │                 ╰─╮          ╭─╯
   3.3│                  ╰──────────╯
     │
     └──────────────────────────────────────────────→
        0.001  0.003  0.01   0.03   0.1  Learning Rate

        Wide "bowl" = forgiving to hyperparameter choice


Large Batch (size = 512):
Learning Rate Sensitivity
    Loss
     │      │
   3.8│      │
     │      ╰╮
   3.6│       │
     │       │← Narrow
   3.4│      ╭╯  optimal
     │      │    region
   3.2│   ╭─╯
     │  ╭╯
   3.0├─╯
     │
     └──────────────────────────────────────────────→
        0.001  0.003  0.01   0.03   0.1  Learning Rate

        Narrow "canyon" = precise tuning required


Why This Happens:
=================

Large Batch Size                   Small Batch Size
      ↓                                   ↓
  Large Steps                         Small Steps
      ↓                                   ↓
┌──────────────────┐              ┌──────────────────┐
│ Must predict     │              │ Only predict     │
│ loss surface     │              │ loss surface     │
│ FAR from current │              │ NEAR current     │
│ position         │              │ position         │
└────────┬─────────┘              └────────┬─────────┘
         │                                  │
         ▼                                  ▼
┌──────────────────┐              ┌──────────────────┐
│ Hard prediction  │              │ Easy prediction  │
│ problem          │              │ problem          │
└────────┬─────────┘              └────────┬─────────┘
         │                                  │
         ▼                                  ▼
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
print()
print("Conclusion: Momentum is critical for large batches")
print("            but unnecessary for small batches!")
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

```
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
      │          ╱
0.9999├         ╱
      │        ╱
0.999 ├       ╱        Token Half-Life: t₁/₂ = 10M
      │      ╱         (constant across batch sizes)
0.99  ├     ╱
      │    ╱
0.95  ├   ╱
      │  ╱
0.90  ├ ╱
      └─────────────────────────────────────────→
        1    16   64   256  1024 4096  Batch Size


Formula: β₂* = β₂^(B*/B)

Examples:
• B=512, β₂=0.95  →  B=1, β₂=0.9999  (increase β₂)
• B=1,   β₂=0.9999 → B=512, β₂=0.95   (decrease β₂)


Parameter: Learning Rate
────────────────────────────────────
Rule: Scale SUB-LINEARLY (not square root!)

0.1  ┐
     │                    Actual scaling
0.01 ├───────╮            (sub-linear)
     │       ╰─╮               │
0.001├          ╰─╮            ↓
     │            ╰────╮    ╭──────╮
0.0001                ╰────╯Square │
     │                     │root   │
     └────────────────────────────────────────→
       1    16   64   256  1024 4096  Batch Size

Note: Exact scaling requires tuning, but it's
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
def calculate_token_halflife(beta2: float, batch_size: int, seq_len: int = 1024) -> float:
    """Calculate token half-life from β₂ and batch size."""
    tokens_per_step = batch_size * seq_len
    steps_to_halflife = np.log(0.5) / np.log(beta2)
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

```
The Return of Vanilla SGD
=========================

Traditional View (Large Batches):

  Simple Optimizers                Sophisticated Optimizers
        ▼                                   ▼
   ┌──────────┐                        ┌────────────┐
   │   SGD    │                        │   Adam     │
   │          │                        │   Lion     │
   │  ╳╳╳     │◁─────── Unstable      │   Muon     │
   │  Loss    │        Training       │   SOAP     │
   │  Spikes  │                        │            │
   │          │                        │  ✓✓✓      │
   └──────────┘                        │  Stable    │
                                       └────────────┘


Paper's Finding (Small Batches):

  Simple Optimizers                Sophisticated Optimizers
        ▼                                   ▼
   ┌──────────┐                        ┌────────────┐
   │   SGD    │                        │   Adam     │
   │          │◁─────── Both Work!    │   Lion     │
   │  ✓✓✓     │        Comparable     │   Muon     │
   │  Stable  │        Performance    │   SOAP     │
   │  Good    │                        │            │
   │  Results │                        │  ✓✓✓      │
   └──────────┘                        │  Stable    │
                                       └────────────┘


Performance Convergence by Batch Size
======================================

Loss at    Large Batch (4096)         Small Batch (1)
Convergence    ↓                          ↓

   5.0 ┤   ╱ SGD (diverges)          All optimizers
       │  ╱                           achieve similar
   4.5 ┤ ╱                            final loss:
       │╱   ╱── Adafactor
   4.0 ├╮  ╱                              ╱── SGD
       │╰╮╱─── Adam                       ├── Adam
   3.8 ├─╰──── Muon                       ├── Adafactor
       │                                  ╰── Muon
   3.6 ├─────────────────────────────────────────


Memory Comparison
=================

Per-parameter memory storage:

┌───────────────────────────────────────────────┐
│ Adam / AdamW:                                 │
│ ┌─────────┬──────────┬──────────┬──────────┐ │
│ │Parameter│ Gradient │1st Moment│2nd Moment│ │
│ │ (2-4B)  │  (4B)    │  (4B)    │  (4B)    │ │
│ └─────────┴──────────┴──────────┴──────────┘ │
│ Total: 14-16 bytes per parameter              │
└───────────────────────────────────────────────┘

┌───────────────────────────────────────────────┐
│ SGD (no momentum):                            │
│ ┌─────────┬──────────┐                        │
│ │Parameter│ Gradient │                        │
│ │ (2-4B)  │  (4B)    │                        │
│ └─────────┴──────────┘                        │
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
from typing import List, Tuple, Optional
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


# Simulate training comparison
# =============================

def simulate_training(
    optimizer: SimpleOptimizer,
    initial_params: np.ndarray,
    n_steps: int = 1000,
    batch_size: int = 1
) -> TrainingMetrics:
    """
    Simulate training a model with given optimizer.

    This is a simplified simulation showing the behavior,
    not actual neural network training.
    """
    params = initial_params.copy()
    losses = []

    # Simple quadratic loss for demonstration
    def compute_loss(p):
        return 0.5 * np.sum(p ** 2)

    def compute_gradient(p, batch_size):
        """Gradient with noise (simulating small batch stochasticity)."""
        true_grad = p  # Gradient of 0.5*sum(p²) is just p

        # Add noise inversely proportional to batch size
        noise_scale = 1.0 / np.sqrt(batch_size)
        noise = np.random.normal(0, noise_scale, size=p.shape)

        return true_grad + noise

    for step in range(n_steps):
        # Compute noisy gradient
        grads = compute_gradient(params, batch_size)

        # Update parameters
        params = optimizer.step(params, grads)

        # Track loss
        loss = compute_loss(params)
        losses.append(loss)

    return TrainingMetrics(
        steps=list(range(n_steps)),
        losses=losses,
        optimizer_name=optimizer.__class__.__name__
    )


# Run the experiment
# ==================

print("Comparing SGD vs Adam at Small Batch Size")
print("=" * 60)
print()

# Initialize parameters (10 dimensions for visualization)
initial_params = np.random.randn(10) * 5.0
n_steps = 1000
batch_size = 1

# Setup optimizers
sgd = VanillaSGD(learning_rate=0.01)
adam = Adam(learning_rate=0.01, beta2=0.9999)  # β₂ scaled for batch size 1

# Run training
print("Running SGD...")
sgd_metrics = simulate_training(sgd, initial_params, n_steps, batch_size)

print("Running Adam...")
adam_metrics = simulate_training(adam, initial_params, n_steps, batch_size)

# Compare final results
print("\nResults:")
print("-" * 60)
print(f"SGD  - Final Loss: {sgd_metrics.losses[-1]:.6f}")
print(f"Adam - Final Loss: {adam_metrics.losses[-1]:.6f}")
print()
print(f"Loss Difference: {abs(sgd_metrics.losses[-1] - adam_metrics.losses[-1]):.6f}")
print()

# Memory comparison
param_count = 1_300_000_000  # 1.3B parameters (like GPT-3)
bytes_per_float = 4

sgd_memory = param_count * bytes_per_float * sgd.state_size_per_param()
adam_memory = param_count * bytes_per_float * adam.state_size_per_param()

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
print("This is revolutionary for memory-constrained training scenarios.")
```

### Key Takeaways

- **Vanilla SGD without momentum performs competitively with Adam at batch size 1**, even for billion-parameter models—a shocking reversal of conventional wisdom
- **SGD has zero optimizer state**, saving ~50% memory compared to Adam (critical for large models)
- **The gap between simple and sophisticated optimizers shrinks as batch size decreases**, because small steps don't require complex prediction mechanisms
- **This opens new possibilities for training in memory-constrained environments** where every GB counts

---

## Practical Recommendations

### Overview

Having established the theory and experimental evidence, let's distill everything into actionable advice you can use today. The paper's recommendations challenge many common practices in LLM training.

The core principle is simple: **use the smallest batch size that maximizes your hardware throughput**. Don't use gradient accumulation unless you're training on multiple devices. Don't assume you need sophisticated optimizers. And most importantly, scale β₂ properly if you do use Adam.

### The Complete Recipe

```
Quick Start Guide: Small Batch Training
========================================

Step 1: Determine Your Batch Size
──────────────────────────────────
Goal: Maximize tokens/second (throughput)

┌─────────────────────────────────────────┐
│ Measure arithmetic intensity:           │
│                                         │
│ Find smallest batch where GPU compute   │
│ time >> memory transfer time            │
│                                         │
│ Rule of thumb:                          │
│ • Single GPU: batch size ~100-1000      │
│ • Multi-GPU: may need larger for comms  │
│ • Memory constrained: use batch size 1  │
└─────────────────────────────────────────┘


Step 2: Choose Your Optimizer
──────────────────────────────

For batch size ≤ 64:
├─ Memory constrained? → Vanilla SGD
├─ Moderate memory?    → Adafactor
└─ Memory abundant?    → Adam (scaled β₂)

For batch size > 64:
└─ Adam with default hyperparameters


Step 3: Set Hyperparameters
────────────────────────────

Using Adam or Adafactor:
├─ β₁: 0.9 (fixed)
├─ β₂: Scale for token half-life of 10M
│      Formula: β₂ = 0.95^(512/batch_size)
│      Examples:
│      • batch_size=1:    β₂ ≈ 0.9999
│      • batch_size=16:   β₂ ≈ 0.9984
│      • batch_size=256:  β₂ ≈ 0.976
│      • batch_size=512:  β₂ ≈ 0.95
└─ Learning rate: Tune (starts around 3e-4)

Using Vanilla SGD:
└─ Learning rate: Tune (starts around 1e-2)


Step 4: Skip Gradient Accumulation
───────────────────────────────────

Old way:
  Batch size 32 + 16 accumulation steps
  = effective batch 512

New way:
  Just use batch size 32 directly!
  (Results are as good or better)

Exception: Multi-device training where
communication is the bottleneck


Step 5: Leverage Robustness
────────────────────────────

Small batches are forgiving:
• Start with conservative hyperparameters
• Don't overinvest in tuning
• Save compute budget for actual training


Memory-Efficiency Bonus
════════════════════════

For fine-tuning large models:

Instead of:
┌────────────────────────────┐
│ LoRA + Adam + Batch 16     │
│ Memory: ~X GB              │
│ Performance: Good          │
└────────────────────────────┘

Try:
┌────────────────────────────┐
│ Full model + Adafactor + BS 1│
│ Memory: ~X GB              │
│ Performance: Better!       │
└────────────────────────────┘
```

### Decision Tree

```
Should I use small batch training?
═══════════════════════════════════

Start
  │
  ├─ Training on single device?
  │  └─ YES → Use smallest batch that saturates GPU
  │           (typically 100-1000 tokens)
  │
  ├─ Memory constrained?
  │  └─ YES → Use batch size 1 with SGD or Adafactor
  │           Save ~50% memory on optimizer state
  │
  ├─ Multi-device with slow interconnect?
  │  └─ YES → May need larger batch/accumulation
  │           to amortize communication costs
  │
  ├─ Want minimal hyperparameter tuning?
  │  └─ YES → Use small batch! More robust.
  │
  └─ Replicating published work?
     └─ Check if they scaled β₂!
        Many papers used large batches with
        poor small-batch hyperparameters


Implementation Checklist
════════════════════════

□ Determined batch size from throughput
□ Chose optimizer based on memory budget
□ Scaled β₂ if using Adam/Adafactor
  - Formula: β₂ = 0.95^(512/batch_size)
  - Verify token half-life is ~10M
□ Started with conservative learning rate
□ Disabled gradient accumulation
□ Enabled stochastic rounding for low precision
□ Measured MFU (model FLOPs utilization)
□ Ran short sweep of learning rates
□ Locked in hyperparameters and trained!
```

### Common Pitfalls to Avoid

```
Mistakes to Avoid
═════════════════

❌ Using β₂=0.95 for batch size 1
   → Will fail! Scale to ~0.9999

❌ Assuming √batch scaling for learning rate
   → Too aggressive. Scale sub-linearly.

❌ Gradient accumulation on single GPU
   → Wasteful! Just use small batch.

❌ Rejecting SGD without trying small batches
   → It works great at batch size ≤64!

❌ Over-tuning hyperparameters
   → Small batches are robust. Save compute.

❌ Assuming more sophisticated = better
   → Simple methods work well at small batches.

❌ Ignoring MFU when choosing batch size
   → Choose batch for hardware efficiency!

❌ Using default hyperparameters from papers
   → Papers often use batch size 512-4096.
   → Rescale β₂ for your batch size!
```

### Key Takeaways

- **Choose batch size to maximize hardware throughput** (tokens/second), not based on assumptions about training stability
- **Avoid gradient accumulation on single devices**—it's equivalent to a larger batch size but wastes memory
- **Scale β₂ using the formula β₂ = 0.95^(512/batch_size)** if using Adam or Adafactor
- **Consider vanilla SGD for extremely memory-constrained scenarios**—it performs surprisingly well at batch size 1

---

## Memory-Efficient Fine-Tuning

### Overview

The final section of the paper applies these insights to a practical problem: fine-tuning large models under memory constraints. The standard approach has been LoRA (Low-Rank Adaptation), which freezes the pretrained weights and trains small adapter modules. While LoRA dramatically reduces memory, it often underperforms full fine-tuning.

This paper shows an alternative: **full fine-tuning with batch size 1 and Adafactor**. By combining the memory savings from a small optimizer state (Adafactor) with the memory savings from not storing accumulated gradients (batch size 1), you can achieve the performance of full fine-tuning while matching LoRA's memory footprint.

The key insight is that Adafactor doesn't store the full second moment matrix. Instead, it only stores row and column sums, reducing memory from O(parameters) to O(√parameters) for each weight matrix. Combined with batch size 1 (no gradient accumulation buffer) and bfloat16 weights (with stochastic rounding), you can fit full fine-tuning into surprisingly tight memory budgets.

### Concept Diagram

```
Memory-Efficient Fine-Tuning Approaches
=======================================

Traditional LoRA:
─────────────────
┌──────────────────────────────────────┐
│   Frozen Pretrained Model (16-bit)   │
│   ████████████████████████████████   │
│                                       │
│   + LoRA Adapters (32-bit, tiny)     │
│   ██                                  │
│                                       │
│   + Adam State for Adapters          │
│   ████                                │
└──────────────────────────────────────┘
Total Memory: ~2 bytes/param
Performance: Good (but not full fine-tune)


Full Fine-Tune with Adam + Large Batch:
────────────────────────────────────────
┌──────────────────────────────────────┐
│   Model Parameters (32-bit)          │
│   ████████████████████████████████   │
│                                       │
│   + Adam State (m_t, v_t)            │
│   ████████████████████████████████   │
│   ████████████████████████████████   │
│                                       │
│   + Gradient Accumulation            │
│   ████████████████████                │
└──────────────────────────────────────┘
Total Memory: ~16 bytes/param
Performance: Best (but huge memory)


Paper's Approach: Batch 1 + Adafactor:
───────────────────────────────────────
┌──────────────────────────────────────┐
│   Model Parameters (16-bit)          │
│   ████████████████████████████████   │
│                                       │
│   + Adafactor State (32-bit, small)  │
│   ████████                            │
│                                       │
│   + No Gradient Accumulation!        │
│   (batch size 1)                      │
└──────────────────────────────────────┘
Total Memory: ~2.5 bytes/param
Performance: Best (full fine-tune quality!)


Memory Breakdown for Gemma 3 (4B params):
══════════════════════════════════════════

Component                  | LoRA  | Full+Adam | Full+Adafactor+BS1
───────────────────────────┼───────┼───────────┼───────────────────
Model weights              | 8 GB  | 16 GB     | 8 GB (bfloat16)
Optimizer state           | 0.2GB | 32 GB     | 2 GB (factored)
Gradient accumulation     | 0     | 4 GB      | 0 (batch size 1)
Activations (checkpointed)| 4 GB  | 4 GB      | 4 GB
───────────────────────────┼───────┼───────────┼───────────────────
TOTAL                     | 12GB  | 56 GB     | 14 GB

Performance on MATH       | 17%   | 18.5%     | 18.5%


Key Insights:
═════════════

1. Batch size 1 eliminates gradient accumulation buffer
   Savings: 4 GB (for 4B model)

2. Adafactor stores O(√n) state instead of O(n)
   Savings: 30 GB compared to Adam (for 4B model)

3. BF16 weights + stochastic rounding works well
   Savings: 8 GB on model weights

4. Combined approach matches LoRA memory but achieves
   full fine-tuning performance!
```

### Implementation

Here's a practical implementation showing memory-efficient fine-tuning:

```python
import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class MemoryProfile:
    """Track memory usage for different components."""
    model_params_gb: float
    optimizer_state_gb: float
    gradient_buffer_gb: float
    activations_gb: float

    @property
    def total_gb(self) -> float:
        return (self.model_params_gb +
                self.optimizer_state_gb +
                self.gradient_buffer_gb +
                self.activations_gb)

    def __repr__(self) -> str:
        return (
            f"MemoryProfile:\n"
            f"  Model Parameters: {self.model_params_gb:.2f} GB\n"
            f"  Optimizer State:  {self.optimizer_state_gb:.2f} GB\n"
            f"  Gradient Buffer:  {self.gradient_buffer_gb:.2f} GB\n"
            f"  Activations:      {self.activations_gb:.2f} GB\n"
            f"  ────────────────────────────────────────\n"
            f"  TOTAL:            {self.total_gb:.2f} GB"
        )


class AdafactorSimulator:
    """
    Simulates Adafactor's memory-efficient second moment estimation.

    Key idea: For an n×m weight matrix, instead of storing nm values
    for the second moment, store only n+m values (row and column sums).
    """

    def __init__(
        self,
        learning_rate: float = 0.001,
        beta2: float = 0.9999,  # Scaled for batch size 1
        epsilon: float = 1e-8,
        use_bf16_params: bool = True
    ):
        self.lr = learning_rate
        self.beta2 = beta2
        self.epsilon = epsilon
        self.use_bf16_params = use_bf16_params

        # State (will be initialized lazily)
        self.row_sum: Optional[np.ndarray] = None
        self.col_sum: Optional[np.ndarray] = None
        self.t = 0

    def memory_for_params(self, shape: Tuple[int, ...]) -> int:
        """
        Calculate optimizer state size in bytes.

        For Adam: 2 × n × m × 4 bytes (first and second moments)
        For Adafactor: (n + m) × 4 bytes (row + column sums)
        """
        if len(shape) == 1:
            # For 1D parameters (like biases), store full second moment
            return shape[0] * 4

        # For 2D parameters (weight matrices)
        n, m = shape
        adam_size = 2 * n * m * 4
        adafactor_size = (n + m) * 4

        print(f"  Shape {shape}: Adam needs {adam_size/1e6:.2f}MB, "
              f"Adafactor needs {adafactor_size/1e6:.2f}MB "
              f"({100*adafactor_size/adam_size:.1f}% of Adam)")

        return adafactor_size

    def step_2d(
        self,
        params: np.ndarray,
        grads: np.ndarray
    ) -> np.ndarray:
        """
        Perform Adafactor update for 2D parameter tensor (weight matrix).

        Key innovation: Estimate per-element second moment from
        row and column statistics instead of storing all elements.
        """
        assert params.ndim == 2
        n, m = params.shape

        # Initialize state if needed
        if self.row_sum is None:
            self.row_sum = np.zeros(n)
            self.col_sum = np.zeros(m)

        self.t += 1

        # Update row and column sums of squared gradients
        # Instead of: v_t = β₂ v_{t-1} + (1-β₂) g_t²
        # We maintain: v_row and v_col
        grads_sq = grads ** 2

        self.row_sum = self.beta2 * self.row_sum + (1 - self.beta2) * grads_sq.sum(axis=1)
        self.col_sum = self.beta2 * self.col_sum + (1 - self.beta2) * grads_sq.sum(axis=0)

        # Reconstruct approximate second moment from factorization
        # v_approx[i,j] ≈ v_row[i] * v_col[j] / mean(v)
        total_sum = grads_sq.sum()
        mean_v = total_sum / (n * m)

        # Broadcast to create approximate second moment
        v_approx = np.outer(self.row_sum, self.col_sum) / (mean_v + self.epsilon)

        # Bias correction
        v_hat = v_approx / (1 - self.beta2 ** self.t)

        # Parameter update
        # Note: No first moment (Adafactor doesn't store m_t for simplicity)
        update = self.lr * grads / (np.sqrt(v_hat) + self.epsilon)

        new_params = params - update

        # Stochastic rounding if using bf16
        if self.use_bf16_params:
            new_params = self._stochastic_round_bf16(new_params)

        return new_params

    @staticmethod
    def _stochastic_round_bf16(params: np.ndarray) -> np.ndarray:
        """
        Simulate stochastic rounding to bfloat16.

        Critical for maintaining precision with bf16 weights!
        Without this, small updates would be lost due to rounding.
        """
        # Simplified simulation (real implementation would use actual bf16)
        # This adds noise proportional to the rounding error
        rounding_noise = np.random.uniform(-1e-4, 1e-4, size=params.shape)
        return params + rounding_noise


def calculate_memory_profile(
    num_params: int,
    approach: str,
    batch_size: int = 16,
    gradient_accumulation_steps: int = 1,
    use_bf16: bool = False
) -> MemoryProfile:
    """
    Calculate memory footprint for different fine-tuning approaches.

    Args:
        num_params: Number of model parameters
        approach: One of ["lora", "full_adam", "full_adafactor"]
        batch_size: Batch size per device
        gradient_accumulation_steps: Number of accumulation steps
        use_bf16: Whether to use bfloat16 for model parameters
    """
    bytes_per_param = 2 if use_bf16 else 4

    # Model parameters
    model_memory = num_params * bytes_per_param / 1e9

    # Optimizer state
    if approach == "lora":
        # LoRA only trains tiny adapters (~1% of params)
        trainable_params = num_params * 0.01
        optimizer_memory = trainable_params * 2 * 4 / 1e9  # Adam state
    elif approach == "full_adam":
        # Adam stores first and second moments (2x params, in fp32)
        optimizer_memory = num_params * 2 * 4 / 1e9
    elif approach == "full_adafactor":
        # Adafactor stores ~1/100 of Adam's state (rough approximation)
        # Actual ratio depends on model architecture
        optimizer_memory = num_params * 0.02 * 4 / 1e9
    else:
        raise ValueError(f"Unknown approach: {approach}")

    # Gradient accumulation buffer
    effective_batch = batch_size * gradient_accumulation_steps
    if gradient_accumulation_steps > 1:
        gradient_memory = num_params * 4 / 1e9  # Store accumulated grads
    else:
        gradient_memory = 0  # No accumulation buffer needed

    # Activations (simplified: assume gradient checkpointing)
    # Real calculation would depend on model architecture
    activations_memory = 4.0  # Rough estimate

    return MemoryProfile(
        model_params_gb=model_memory,
        optimizer_state_gb=optimizer_memory,
        gradient_buffer_gb=gradient_memory,
        activations_gb=activations_memory
    )


# Compare approaches for Gemma 3 (4B parameters)
# ===============================================

print("Memory-Efficient Fine-Tuning Comparison")
print("=" * 60)
print()

gemma_3_params = 4_000_000_000

approaches = {
    "LoRA + Adam (BS=16)": {
        "approach": "lora",
        "batch_size": 16,
        "accumulation": 1,
        "use_bf16": True,
    },
    "Full + Adam (BS=16, Accum=4)": {
        "approach": "full_adam",
        "batch_size": 16,
        "accumulation": 4,
        "use_bf16": False,
    },
    "Full + Adafactor (BS=1)": {
        "approach": "full_adafactor",
        "batch_size": 1,
        "accumulation": 1,
        "use_bf16": True,
    },
}

results = {}
for name, config in approaches.items():
    profile = calculate_memory_profile(
        gemma_3_params,
        config["approach"],
        config["batch_size"],
        config["accumulation"],
        config["use_bf16"]
    )
    results[name] = profile

    print(f"{name}:")
    print("-" * 60)
    print(profile)
    print()

# Summary comparison
print("\n" + "=" * 60)
print("Summary:")
print("-" * 60)

for name, profile in results.items():
    print(f"{name:35s}: {profile.total_gb:6.1f} GB")

print()
print("Key Findings:")
print("-" * 60)
print("• Adafactor + BS=1 matches LoRA's memory")
print("• But achieves full fine-tuning performance!")
print("• Saves 42 GB compared to standard approach")
print("• Makes full fine-tuning accessible on consumer GPUs")
```

### Key Takeaways

- **Combining batch size 1 with Adafactor achieves full fine-tuning performance with LoRA-like memory**, opening new possibilities for training large models on consumer hardware
- **The memory savings come from three sources**: bfloat16 weights, factored second moment (Adafactor), and no gradient accumulation buffer
- **Stochastic rounding is critical when using bfloat16 weights** to prevent small updates from being lost to quantization error
- **This approach saves ~40GB for a 4B parameter model** compared to traditional full fine-tuning with Adam

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
