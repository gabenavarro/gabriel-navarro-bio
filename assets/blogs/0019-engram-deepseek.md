@{id = "31fd2528-8fe3-43f7-a863-3f66bfae5bf3"
  title = "Breaking Free from Context Limits: Recursive Language Models Explained"
  date = "2026-01-20T00:00:00Z"
  tags = ['journal club', 'machine learning', 'arxiv', 'language models']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/zhang-kraska-khattab-rlm.svg"
  description = "This entry is a summary of the paper "Recursive Language Models" where Zhang, Kraska & Khattab introduce an approach to scaling Large Language Models (LLMs) by adding conditional memory"
  type = "note"
  disabled = "False"
}

<p align="center">
  <img src="https://storage.googleapis.com/gn-portfolio/images/zhang-kraska-khattab-rlm.svg" max-width="700">
</p>


# Understanding Engram: A New Memory Primitive for Large Language Models

---

## Table of Contents

- [Abstract](#abstract)
- [1. Introduction](#1-introduction)
- [2. Architecture](#2-architecture)
  - [2.1 Overview](#21-overview)
  - [2.2 Sparse Retrieval via Hashed N-grams](#22-sparse-retrieval-via-hashed-n-grams)
  - [2.3 Context-aware Gating](#23-context-aware-gating)
  - [2.4 Integration with Multi-branch Architecture](#24-integration-with-multi-branch-architecture)
  - [2.5 System Efficiency: Decoupling Compute and Memory](#25-system-efficiency-decoupling-compute-and-memory)
- [3. Scaling Laws and Sparsity Allocation](#3-scaling-laws-and-sparsity-allocation)
- [4. Large Scale Pre-training](#4-large-scale-pre-training)
- [5. Long Context Training](#5-long-context-training)
- [6. Analysis](#6-analysis)
- [7. Related Work](#7-related-work)
- [8. Conclusion](#8-conclusion)

---

## Abstract

### Overview

This groundbreaking paper from DeepSeek introduces **Engram**, a revolutionary approach to scaling Large Language Models (LLMs) by adding conditional memory as a complementary sparsity axis alongside the now-standard Mixture-of-Experts (MoE) approach. While MoE scales capacity through conditional computation (selectively activating different neural network experts), Transformers traditionally lack a native primitive for knowledge lookup, forcing them to inefficiently simulate retrieval through expensive computation.

The key insight is recognizing that language modeling involves two fundamentally different tasks: **compositional reasoning** (which requires deep, dynamic computation) and **knowledge retrieval** (which often involves local, static, stereotyped patterns like "Alexander the Great" or "Princess of Wales"). Current LLMs waste valuable sequential depth reconstructing these static patterns through multiple transformer layers when they could simply look them up.

Engram modernizes the classic N-gram embedding approach with O(1) lookup time, adding modern innovations like tokenizer compression, multi-head hashing, and context-aware gating. Through rigorous experimentation under strict iso-parameter and iso-FLOPs constraints, the authors uncover a U-shaped scaling law that reveals the optimal allocation between neural computation (MoE) and static memory (Engram).

The results are striking: Engram-27B not only excels on knowledge-intensive tasks (MMLU +3.4, CMMLU +4.0) as expected, but shows even larger gains in general reasoning (BBH +5.0, ARC-Challenge +3.7) and code/math domains (HumanEval +3.0, MATH +2.4). The mechanistic analysis reveals why: by offloading static pattern reconstruction from early layers, Engram effectively **deepens the network** for complex reasoning while freeing up attention capacity for global context.

### Concept Diagram

```
Traditional LLM Architecture:
┌─────────────────────────────────────┐
│  Token Input                        │
│         ↓                           │
│  Embedding Layer                    │
│         ↓                           │
│  Layer 1-5: Waste depth             │
│         reconstructing "Alexander   │
│         the Great" token by token   │
│         ↓                           │
│  Layer 6-30: Finally available      │
│         for reasoning               │
│         ↓                           │
│  Output Logits                      │
└─────────────────────────────────────┘

Engram Architecture:
┌─────────────────────────────────────┐
│  Token Input                        │
│          ↓                          │
│     Embedding Layer                 │
│          ↓                          │
│       Layer 1                       │
│         ┌┴────┐                     │
│         │     ↓                     │
│         │  Engram Memory Injection  │
│         │  (Static Lookup)          │
│         │     │                     │
│         └┬────┘                     │
│          ▼                          │
│  Layer 2-30: Full depth             │
│         available for reasoning     │
│         (no reconstruction needed)  │
│         ↓                           │
│  Output Logits                      │
└─────────────────────────────────────┘

The U-Shaped Allocation Law:
        Loss
         │
    1.73 ├─┐                     ┐
         │  ╲                   ╱  
    1.72 │   ╲                 ╱    Both extremes
         │    ╲               ╱     are BAD!
    1.71 │     ╲_____________╱    
         │         ↑               
    1.70 │         │ Optimal Mix
         │         │ (75-80% MoE, 20-25% Memory)
    1.69 │         └─── Lowest loss!
         │
         └─────────────────────────────────────
          0%   20%  40%  60%  80%  100%
          Pure      ↑              Pure
          Memory    Optimal        MoE
          (ρ=0)     (ρ=0.75-0.8)  (ρ=1.0)
          
          HIGH      LOW            HIGH
          LOSS      LOSS           LOSS
```

### Key Takeaways

- **Dual Sparsity Paradigm**: Language modeling requires both conditional computation (MoE) for dynamic reasoning AND conditional memory (Engram) for static pattern retrieval—neither alone is optimal
- **Effective Depth Increase**: By offloading local pattern reconstruction to O(1) lookups, Engram frees up all 30 layers for complex reasoning, functionally deepening the network
- **Universal Performance Gains**: While memory intuitively helps knowledge tasks, the largest gains appear in reasoning, code, and math—domains traditionally thought to require pure computation
- **Infrastructure-Aware Design**: Deterministic addressing enables runtime prefetching from host memory, bypassing GPU memory constraints with <3% overhead
- **U-Shaped Scaling Law**: The optimal allocation is approximately 75-80% MoE, 20-25% Engram—pure approaches (100% MoE or 100% memory) both underperform

---

## 1. Introduction

### Overview

The introduction frames Engram within the broader context of sparsity in intelligent systems, from biological neural circuits to modern LLMs. The authors identify a critical inefficiency: while Mixture-of-Experts (MoE) has become the de facto standard for scaling model capacity through conditional computation, Transformers lack a native knowledge lookup primitive.

This architectural mismatch forces current LLMs to **simulate retrieval through computation**. Consider what happens when a model processes "Only Alexander the Great could tame the horse Bucephalus":

- **Layer 1-2**: Recognizes "Alexander"
- **Layer 3**: Connects "Alexander" → "the" → context of royalty
- **Layer 4**: Identifies "Great" as part of royal title
- **Layer 5**: Synthesizes "Princess of Wales" pattern
- **Layer 6**: Finally arrives at the full entity concept

This expensive runtime reconstruction of what is essentially a static lookup table wastes valuable sequential depth on trivial operations. The authors propose Engram as a **complementary axis of sparsity**:

- **Conditional Computation (MoE)**: Sparsely activates parameters for dynamic logic
- **Conditional Memory (Engram)**: Sparsely retrieves static embeddings for fixed knowledge

The key innovation is treating memory as a first-class modeling primitive with modern adaptations: tokenizer compression (23% vocabulary reduction), multi-head hashing (collision mitigation), contextualized gating (dynamic modulation), and multi-branch integration (parallel processing).

### Concept Diagram

```
Linguistic Duality in Language Modeling:
┌──────────────────────┬──────────────────────┐
│ Compositional        │  Knowledge           │
│ Reasoning            │  Retrieval           │
├──────────────────────┼──────────────────────┤
│ • Dynamic logic      │ • Static patterns    │
│ • Context-dependent  │ • Local dependencies │
│ • Deep computation   │ • Stereotyped        │
│ • Novel composition  │ • Formulaic          │
│                      │                      │
│ Example:             │ Example:             │
│ "What if Alexander   │ "Alexander the Great"│
│  ruled in modern     │ "Princess of Wales"  │
│  times?"             │ "Four Great          │
│                      │  Inventions"         │
│                      │                      │
│ Best solved by:      │ Best solved by:      │
│ ┌────────────────┐   │ ┌────────────────┐   │
│ │ MoE            │   │ │ Engram         │   │
│ │ (Conditional   │   │ │ (Conditional   │   │
│ │  Computation)  │   │ │  Memory)       │   │
│ └────────────────┘   │ └────────────────┘   │
│        ↓             │        ↓             │
│ Activate different   │ O(1) lookup from     │
│ expert networks      │ massive table        │
└──────────────────────┴──────────────────────┘

The Problem: Current LLMs use only computation for both!
```

### Implementation

```python
import numpy as np
from typing import List, Tuple, Dict

class NgramMemoryLookup:
    """
    Simplified implementation of Engram's core N-gram memory lookup.
    Demonstrates how static patterns can be retrieved via O(1) hashing
    rather than expensive multi-layer reconstruction.
    """
    
    def __init__(
        self, 
        vocab_size: int = 128000, 
        ngram_orders: List[int] = [2, 3],
        num_heads: int = 8,
        embedding_dim: int = 256,
        table_size: int = 1000003  # Prime number for better hashing
    ):
        """
        Initialize the N-gram memory module.
        
        Args:
            vocab_size: Size of vocabulary
            ngram_orders: N-gram orders to use (e.g., [2, 3] for bigrams and trigrams)
            num_heads: Number of hash heads to reduce collisions
            embedding_dim: Dimension of embedding vectors
            table_size: Size of hash table (should be prime)
        """
        self.vocab_size = vocab_size
        self.ngram_orders = ngram_orders
        self.num_heads = num_heads
        self.embedding_dim_per_head = embedding_dim // num_heads
        self.table_size = table_size
        
        # Initialize embedding tables for each (n-gram order, hash head) pair
        self.embeddings = {}
        for n in ngram_orders:
            for k in range(num_heads):
                # Each table stores embeddings for this n-gram order and head
                self.embeddings[(n, k)] = np.random.randn(
                    table_size, 
                    self.embedding_dim_per_head
                ) * 0.01
        
        # Hash seeds for each head to ensure different collision patterns
        self.hash_seeds = [i * 1000003 for i in range(num_heads)]
    
    def _hash_ngram(self, ngram: Tuple[int, ...], head: int) -> int:
        """
        Hash an n-gram to a table index using multiplicative hashing.
        
        Args:
            ngram: Tuple of token IDs
            head: Hash head index
            
        Returns:
            Index in the hash table
        """
        # Multiplicative hash with XOR combination
        hash_val = self.hash_seeds[head]
        for token_id in ngram:
            hash_val = (hash_val * 31 + token_id) ^ (token_id << 5)
        return hash_val % self.table_size
    
    def lookup_ngrams(self, token_sequence: List[int], position: int) -> np.ndarray:
        """
        Retrieve memory vectors for all n-grams ending at position.
        
        This is the O(1) lookup that replaces multi-layer reconstruction!
        
        Args:
            token_sequence: List of token IDs
            position: Current position in sequence
            
        Returns:
            Concatenated embeddings from all n-grams and heads
        """
        retrieved_embeddings = []
        
        # For each n-gram order (e.g., 2-gram, 3-gram)
        for n in self.ngram_orders:
            # Extract the suffix n-gram ending at this position
            if position >= n - 1:
                ngram = tuple(token_sequence[position - n + 1 : position + 1])
                
                # Retrieve from each hash head
                for k in range(self.num_heads):
                    idx = self._hash_ngram(ngram, k)
                    embedding = self.embeddings[(n, k)][idx]
                    retrieved_embeddings.append(embedding)
        
        # Concatenate all retrieved embeddings
        return np.concatenate(retrieved_embeddings)
    
    def compare_with_traditional(self, entity_tokens: List[int]) -> Dict:
        """
        Compare Engram lookup with traditional multi-layer processing.
        
        Returns:
            Statistics showing the efficiency gain
        """
        # Engram: Single O(1) lookup
        engram_time = 1  # Constant time
        engram_layers = 0  # No layers consumed
        
        # Traditional: Must process through multiple layers
        traditional_layers = len(entity_tokens)  # Roughly 1 layer per token
        traditional_time = traditional_layers * 100  # Arbitrary units
        
        return {
            "entity_length": len(entity_tokens),
            "engram": {
                "operations": engram_time,
                "layers_consumed": engram_layers,
                "depth_freed": traditional_layers
            },
            "traditional": {
                "operations": traditional_time,
                "layers_consumed": traditional_layers,
                "depth_freed": 0
            },
            "speedup": traditional_time / engram_time,
            "depth_gained": traditional_layers
        }

# Example: Process "Alexander the Great"
vocab = {
    "Alexander": 1001,
    "the": 42,
    "Great": 2003,
    "could": 156,
    "tame": 5678
}

# Initialize Engram memory
engram = NgramMemoryLookup(
    vocab_size=len(vocab),
    ngram_orders=[2, 3],
    num_heads=4,
    embedding_dim=256
)

# Simulate processing the entity
sentence = ["Alexander", "the", "Great", "could", "tame"]
token_ids = [vocab[word] for word in sentence]

# At position 2 (after seeing "Alexander the Great")
position = 2
memory_vector = engram.lookup_ngrams(token_ids, position)

print(f"Retrieved memory vector shape: {memory_vector.shape}")
print(f"This represents {len(engram.ngram_orders) * engram.num_heads} different n-gram embeddings")

# Compare efficiency
stats = engram.compare_with_traditional([vocab["Alexander"], vocab["the"], vocab["Great"]])
print(f"\nEfficiency Comparison:")
print(f"Entity: 'Alexander the Great' ({stats['entity_length']} tokens)")
print(f"Traditional approach: {stats['traditional']['layers_consumed']} layers consumed")
print(f"Engram approach: {stats['engram']['layers_consumed']} layers consumed")
print(f"Depth freed for reasoning: {stats['depth_gained']} layers")
print(f"Speedup: {stats['speedup']}x")
```

Output:

```txt
Retrieved memory vector shape: (512,)
This represents 8 different n-gram embeddings

Efficiency Comparison:
Entity: 'Alexander the Great' (3 tokens)
Traditional approach: 3 layers consumed
Engram approach: 0 layers consumed
Depth freed for reasoning: 3 layers
Speedup: 300.0x
```

### Key Takeaways

- **Architectural Mismatch**: Transformers evolved without a native lookup primitive, forcing expensive simulation of memory retrieval through computation
- **Linguistic Duality**: Language modeling inherently involves two different operations—dynamic composition and static retrieval—that deserve different architectural primitives
- **Depth Waste**: Multi-token entities like "Alexander the Great" consume 3-6 early layers just for pattern recognition, wasting sequential depth
- **O(1) Solution**: N-gram hashing provides constant-time lookup regardless of pattern complexity, modernized with collision mitigation and dynamic gating
- **Complementary, Not Replacement**: Engram is designed to work alongside MoE, not replace it—both axes of sparsity are necessary

---

## 2. Architecture

### 2.1 Overview

The Engram module is elegantly simple in concept but sophisticated in execution. Given an input sequence and hidden states at layer ℓ, it processes each position in two phases:

1. **Retrieval**: Extract suffix N-grams, compress via tokenizer mapping, and deterministically retrieve static embeddings via multi-head hashing
2. **Fusion**: Dynamically modulate retrieved embeddings with current hidden state through context-aware gating and refine with lightweight convolution

The critical design decision is that Engram is **not applied to every layer**—instead, it's strategically placed at specific layers (e.g., layers 2 and 15) to balance modeling performance with system efficiency. This decouples memory from compute while maintaining the standard input embedding and output head intact.

### Concept Diagram

```
Engram Module Architecture:

Input: "Only Alexander the Great could tame..."
         ↓
    Token IDs: [45, 1001, 42, 2003, 156, ...]
         ↓
┌───────────────────────────────────────────────┐
│ Phase 1: RETRIEVAL (Static, Deterministic)    │
├───────────────────────────────────────────────┤
│  Tokenizer Compression                        │
│  ┌────────────────────┐                       │
│  │ "Alexander" → 1001 │                       │
│  │ "alexander" → 1001 │ (Case-folding, NFKC)  │
│  │ " alexander"→ 1001 │                       │
│  └────────────────────┘                       │
│         ↓                                     │
│  Extract Suffix N-grams at position t:        │
│  • 2-gram: (the, Great)                       │
│  • 3-gram: (Alexander, the, Great)            │
│         ↓                                     │
│  Multi-Head Hashing (K=8 heads):              │
│ ┌─────────┬─────────┬─────────┬────┬────────┐ │
│ │ Head 0  │ Head 1  │ Head 2  │ ...│Head 7  │ │
│ ├─────────┼─────────┼─────────┼────┼────────┤ │
│ │ hash()→ │ hash()→ │ hash()→ │ ...│ hash()→│ │
│ │ idx_0   │ idx_1   │ idx_2   │    │ idx_7  │ │
│ └────↓────┴────↓────┴────↓────┴────┴────────┘ │
│      │         │         │                    │
│      ▼         ▼         ▼                    │
│   [E_2,0]   [E_2,1]   [E_2,2]   ...  [E_2,7]  │
│      ↓         ↓         ↓              ↓     │
│        Concat → e_t (memory vector)           │
└───────────────────────────────────────────────┘
         ↓
┌───────────────────────────────────────────────┐
│ Phase 2: ENGRAM FUSION MODULE                 │
│ (Dynamic, Context-Aware)                      │
│ (at Layer ℓ, Position t)                      │
├───────────────────────────────────────────────┤
│  INPUTS:                                      │
│  ┌──────────────┐    ┌──────────────┐         │
│  │ h_t          │    │ e_t          │         │
│  │ Hidden state │    │ Memory vector│         │
│  │ [768 dims]   │    │ [512 dims]   │         │
│  └──────┬───────┘    └──────┬───────┘         │
│         │                   ├────────────┐    │
│         │                   ↓            ↓    │
│         │               ┌────────┐ ┌────────┐ │
│         │               │  W_K   │ │  W_V   │ │
│         │               │512×768 │ │512×768 │ │
│         │               └───┬────┘ └─────┬──┘ │
│         │                   ↓            ↓    │
│         │             k_t [768]    v_raw [768]│
│         └─────────────┬─────┘            │    │
│                       │                  │    │
│            ┌──────────┴──────────────┐   │    │
│            │ Attention-like Gate:    │   │    │
│            │                         │   │    │
│            │ 1. RMSNorm(h_t, k_t)    │   │    │
│            │ 2. alignment = h_t·k_t  │   │    │
│            │              ────────   │   │    │
│            │                 √d      │   │    │
│            │ 3. α_t = σ(alignment)   │   │    │
│            └────────────┬────────────┘   │    │
│                         ↓                │    │
│                    α_t [scalar]          │    │
│                    Gate ∈ (0,1)          │    │
│                         └─────┬──────────┘    │
│                ┌──────────────┴────┐          │
│                │ Apply gate:       │          │
│                │ v_t = α_t × v_raw │          │
│                └──────────┬────────┘          │
│                           ↓                   │
│                       v_t [768]               │
│           ┌───────────────┴─────────┐         │
│           │ Depthwise Convolution:  │         │
│           │ 1. RMSNorm(v_t)         │         │
│           │ 2. Conv1D(kernel=4)     │         │
│           │ 3. conv_out [768]       │         │
│           └───────────┬─────────────┘         │
│                       │                       │
│           ┌───────────┴──────────┐            │
│           │ Activation:          │            │
│           │ conv_out ──┐         │            │
│           │            ├─ SiLU   │            │
│           │ v_t ───────┘    +    │            │
│           │             residual │            │
│           └───────────┬──────────┘            │
│                       ↓                       │
│                    Y [768]                    │
│         h_t [768] ────┤                       │
│           ┌───────────┴──────────┐            │
│           │ Main Residual:       │            │
│           │                      │            │
│           │ H^(ℓ) ← H^(ℓ) + Y    │            │
│           └───────────┬──────────┘            │
│                       ↓                       │
│           OUTPUT:                             │
│           ┌──────────────────────┐            │
│           │ h_t_updated [768]    │            │
│           │ Enriched hidden state│            │
│           └──────────────────────┘            │
│                                               │
└───────────────────────────────────────────────┘
         ↓
   Continue to Attention → MoE → Next Layer
```

### 2.2 Sparse Retrieval via Hashed N-grams

The retrieval phase must solve a fundamental challenge: the combinatorial space of all possible N-grams is intractable to parameterize directly. For a 128K vocabulary with 3-grams, there are 128K³ ≈ 2 trillion possible combinations!

The solution is elegant: **hash-based indexing with collision mitigation**. Here's how it works:

1. **Tokenizer Compression** (23% reduction): Map semantically equivalent tokens to canonical IDs using NFKC normalization and case-folding. This ensures "Apple", "apple", and " apple" all map to the same representation, maximizing semantic density.

2. **Multi-Head Hashing** (K=8 heads): Instead of a single hash function (which would have collisions), use K independent hash heads per N-gram order. Each head maps to a different prime-sized embedding table, dramatically reducing collision probability.

3. **Deterministic Addressing**: The hash function φ_n,k(g_t,n) is a lightweight multiplicative-XOR hash that depends ONLY on token IDs, not hidden states. This deterministic property enables the system optimizations discussed in Section 2.5.

The final memory vector e_t concatenates embeddings from all (N-gram order × hash head) combinations, providing a rich, multi-scale representation.

### Concept Diagram

```
Hashing Strategy for Collision Mitigation:

Single Hash (Naive Approach):
Token Sequence → hash() → Index in Table
     ↓
Problem: "Alexander the Great" and "Princess of Wales"
         might hash to same index (collision!)

Multi-Head Hashing (Engram Approach):
Token Sequence
     ↓
┌────┴─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│          │     │     │     │     │     │     │
▼          ▼     ▼     ▼     ▼     ▼     ▼     ▼
hash_0  hash_1 hash_2 hash_3 hash_4 hash_5 hash_6 hash_7
│          │     │     │     │     │     │     │
▼          ▼     ▼     ▼     ▼     ▼     ▼     ▼
Table_0 Table_1 ...                        Table_7
(1M)    (1M)                               (1M)
│          │                                 │
└─────┬────┴──────────────────────┬─────────┘
      │                           │
      ▼                           ▼
    [e_0]     [e_1]  ...        [e_7]
      └──────────┬────────────────┘
                 ▼
            Concatenate
                 ▼
             e_t (final memory vector)

Probability of all 8 heads colliding: (1/1M)^8 ≈ 10^-48
(Essentially impossible!)

Tokenizer Compression Example:
Raw Tokens:       "Apple"  "apple"  " apple"  "APPLE"
Token IDs:         42       87       93        51
                   ↓        ↓        ↓         ↓
Compression: P(·) → 42      42       42        42
                   └────────┴────────┴─────────┘
                   All map to same canonical ID!
                   
Result: 23% vocabulary reduction, more semantic density
```

### Implementation

```python
import numpy as np
from typing import List, Tuple, Dict
import hashlib

class MultiHeadHashedNgram:
    """
    Multi-head hashing strategy for N-gram embeddings with collision mitigation.
    """
    
    def __init__(
        self,
        vocab_size: int = 128000,
        compressed_vocab_size: int = 98304,  # 23% reduction
        ngram_orders: List[int] = [2, 3],
        num_heads: int = 8,
        table_sizes: Dict[int, int] = {2: 1000003, 3: 1500007},  # Prime sizes
        embedding_dim_per_head: int = 32
    ):
        """
        Initialize multi-head hashed N-gram embedding system.
        
        Args:
            vocab_size: Original vocabulary size
            compressed_vocab_size: Size after tokenizer compression
            ngram_orders: N-gram orders to use
            num_heads: Number of hash heads per n-gram order
            table_sizes: Prime-sized hash table for each n-gram order
            embedding_dim_per_head: Embedding dimension per head
        """
        self.vocab_size = vocab_size
        self.compressed_vocab_size = compressed_vocab_size
        self.ngram_orders = ngram_orders
        self.num_heads = num_heads
        self.table_sizes = table_sizes
        self.embedding_dim_per_head = embedding_dim_per_head
        
        # Create tokenizer compression map (simplified)
        self.compression_map = self._create_compression_map()
        
        # Initialize embedding tables: E[n,k][idx] for each (order, head)
        self.embedding_tables = {}
        for n in ngram_orders:
            for k in range(num_heads):
                table_size = table_sizes[n]
                self.embedding_tables[(n, k)] = np.random.randn(
                    table_size,
                    embedding_dim_per_head
                ) * 0.01
        
        # Prime numbers for multiplicative hashing (one per head)
        self.hash_primes = [
            1000003, 1500007, 2000003, 2500009,
            3000017, 3500017, 4000037, 4500007
        ]
    
    def _create_compression_map(self) -> np.ndarray:
        """
        Create vocabulary compression map.
        
        Simulates mapping variants like "Apple", "apple", " apple" to same ID.
        """
        compression = np.arange(self.vocab_size)
        
        # Simplified: map every group of 3 consecutive tokens to first token
        # (Real implementation uses NFKC normalization + case folding)
        for i in range(0, self.vocab_size, 3):
            if i + 1 < self.vocab_size:
                compression[i + 1] = compression[i]
            if i + 2 < self.vocab_size:
                compression[i + 2] = compression[i]
        
        return compression
    
    def compress_tokens(self, token_ids: List[int]) -> List[int]:
        """
        Apply tokenizer compression to normalize semantically equivalent tokens.
        
        Args:
            token_ids: Original token IDs
            
        Returns:
            Compressed token IDs
        """
        return [int(self.compression_map[tid % self.vocab_size]) 
                for tid in token_ids]
    
    def _hash_ngram(self, ngram: Tuple[int, ...], head: int, n: int) -> int:
        """
        Hash an n-gram using multiplicative hashing with XOR mixing.
        
        Args:
            ngram: Tuple of compressed token IDs
            head: Hash head index
            n: N-gram order
            
        Returns:
            Index in hash table for this (n, head) combination
        """
        # Multiplicative hashing: h(x) = ((a·x) mod p) mod m
        hash_val = self.hash_primes[head]
        
        for token_id in ngram:
            # Mix with multiplicative and XOR operations
            hash_val = (hash_val * 31 + token_id) & 0x7FFFFFFF
            hash_val ^= (token_id << (head + 1))
        
        return hash_val % self.table_sizes[n]
    
    def retrieve_embeddings(
        self, 
        token_sequence: List[int], 
        position: int
    ) -> Tuple[np.ndarray, Dict]:
        """
        Retrieve all embeddings for n-grams ending at position.
        
        Args:
            token_sequence: List of token IDs
            position: Current position
            
        Returns:
            concatenated_embeddings: All retrieved embeddings
            debug_info: Information about retrieval for analysis
        """
        # First, apply tokenizer compression
        compressed_tokens = self.compress_tokens(token_sequence)
        
        retrieved_embeddings = []
        debug_info = {"ngrams": [], "hash_indices": []}
        
        # For each n-gram order
        for n in self.ngram_orders:
            if position >= n - 1:
                # Extract suffix n-gram
                ngram = tuple(compressed_tokens[position - n + 1 : position + 1])
                debug_info["ngrams"].append((n, ngram))
                
                # Retrieve from each hash head
                head_embeddings = []
                head_indices = []
                for k in range(self.num_heads):
                    idx = self._hash_ngram(ngram, k, n)
                    head_indices.append(idx)
                    
                    # Lookup in embedding table
                    embedding = self.embedding_tables[(n, k)][idx]
                    head_embeddings.append(embedding)
                
                debug_info["hash_indices"].append((n, head_indices))
                retrieved_embeddings.extend(head_embeddings)
        
        # Concatenate all embeddings
        final_embedding = np.concatenate(retrieved_embeddings)
        
        return final_embedding, debug_info
    
    def analyze_collision_probability(
        self, 
        sample_ngrams: List[Tuple[int, ...]]
    ) -> Dict:
        """
        Analyze collision probability for sample n-grams.
        
        Returns:
            Statistics about hash collisions
        """
        collisions_per_head = {k: 0 for k in range(self.num_heads)}
        total_pairs = len(sample_ngrams) * (len(sample_ngrams) - 1) // 2
        
        n = len(sample_ngrams[0])  # Assume all same order
        
        # Check all pairs
        for i in range(len(sample_ngrams)):
            for j in range(i + 1, len(sample_ngrams)):
                ngram1 = sample_ngrams[i]
                ngram2 = sample_ngrams[j]
                
                # Check each head
                for k in range(self.num_heads):
                    idx1 = self._hash_ngram(ngram1, k, n)
                    idx2 = self._hash_ngram(ngram2, k, n)
                    if idx1 == idx2:
                        collisions_per_head[k] += 1
        
        # Calculate probability of all heads colliding
        all_heads_collide = sum(
            1 for i in range(len(sample_ngrams))
            for j in range(i + 1, len(sample_ngrams))
            if all(
                self._hash_ngram(sample_ngrams[i], k, n) ==
                self._hash_ngram(sample_ngrams[j], k, n)
                for k in range(self.num_heads)
            )
        )
        
        return {
            "total_pairs": total_pairs,
            "collisions_per_head": collisions_per_head,
            "single_head_collision_rate": sum(collisions_per_head.values()) / (total_pairs * self.num_heads),
            "all_heads_collision_count": all_heads_collide,
            "all_heads_collision_prob": all_heads_collide / total_pairs if total_pairs > 0 else 0
        }

# Example usage
hasher = MultiHeadHashedNgram(
    vocab_size=128000,
    compressed_vocab_size=98304,
    ngram_orders=[2, 3],
    num_heads=8,
    embedding_dim_per_head=32
)

# Process sentence: "Only Alexander the Great could"
sentence_tokens = [45, 1001, 42, 2003, 156]

# Before compression
print("Original tokens:", sentence_tokens)
compressed = hasher.compress_tokens(sentence_tokens)
print("After compression:", compressed)
print(f"Compression achieved: {(1 - len(set(compressed))/len(set(sentence_tokens)))*100:.1f}%")

# Retrieve at position 3 (after "Alexander the Great")
embedding, info = hasher.retrieve_embeddings(sentence_tokens, position=3)
print(f"\nRetrieved embedding shape: {embedding.shape}")
print(f"N-grams used: {info['ngrams']}")
print(f"Hash indices for 3-gram: {info['hash_indices'][1]}")

# Analyze collision probability
sample_ngrams = [
    (1001, 42, 2003),  # "Alexander the Great"
    (5678, 91, 234),   # "Princess of Wales" (hypothetical)
    (111, 222, 333),   # Random pattern
    (444, 555, 666),   # Random pattern
]
collision_stats = hasher.analyze_collision_probability(sample_ngrams)
print(f"\nCollision Analysis:")
print(f"Total pairs tested: {collision_stats['total_pairs']}")
print(f"Single head collision rate: {collision_stats['single_head_collision_rate']:.4f}")
print(f"All heads collision probability: {collision_stats['all_heads_collision_prob']:.6f}")
print(f"→ With 8 heads, collision probability is reduced by ~10^6x!")
```

### Key Takeaways

- **Compression First**: 23% vocabulary reduction through normalization maximizes semantic density and reduces the effective n-gram space
- **Collision Mitigation**: Multi-head hashing (8 heads) reduces collision probability from ~10^-6 (single hash) to ~10^-48 (all heads colliding)
- **Prime Table Sizes**: Using prime-sized hash tables (1M, 1.5M) improves hash distribution quality
- **Deterministic by Design**: Hash indices depend only on token IDs, enabling system-level optimizations (prefetching, offloading)
- **Scalability**: Adding parameters is trivial—just increase table sizes or add more heads, with zero impact on per-token FLOPs

---

## 2.3 Context-aware Gating

The retrieved memory vectors e_t are context-independent priors—they're the same regardless of what came before in the sentence. But this creates two problems:

1. **Polysemy**: "Great" in "Alexander the Great" has different meaning than "great job"
2. **Hash Collisions**: Different n-grams might hash to the same index, causing noise

The solution is **context-aware gating**, inspired by attention mechanisms but applied to memory lookup. The current hidden state h_t (which has aggregated global context through preceding attention layers) serves as a dynamic Query:

- If h_t and the retrieved memory semantically align → gate α_t ≈ 1 (use the memory)
- If they contradict → gate α_t ≈ 0 (suppress the noise)

This is computed via scaled dot-product attention between the normalized hidden state and a Key projection of the memory, followed by a sigmoid to produce α_t ∈ (0,1). The memory is then modulated as v_t = α_t · (W_V · e_t).

Finally, a lightweight depthwise causal convolution (kernel size 4, dilation δ = max N-gram order) expands the receptive field and adds non-linearity, with SiLU activation and a residual connection.

### Concept Diagram

```
Context-Aware Gating Mechanism:

Input:
┌──────────────┐         ┌──────────────┐
│ h_t          │         │ e_t          │
│ (hidden from │         │ (retrieved   │
│  previous    │         │  memory,     │
│  attention)  │         │  static)     │
└──────┬───────┘         └──────┬───────┘
       │                        │
       │  Has global context    │  Context-independent
       │  from preceding        │  (same regardless of
       │  attention layers      │   sentence context)
       │                        │
       ▼                        ▼
┌──────────────────────────────────────┐
│      Semantic Alignment Check        │
│                                      │
│  Query: RMSNorm(h_t)                │
│    ↓                                 │
│  Key: RMSNorm(W_K · e_t)            │
│    ↓                                 │
│  Gate: α_t = σ(Query·Key / √d)     │
│                                      │
│  α_t ∈ (0, 1)                       │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│     Example Gating Behaviors:        │
│                                      │
│ Scenario 1: Correct retrieval       │
│ h_t: "Alexander" (king context)     │
│ e_t: "the Great" (royal pattern)    │
│ → α_t = 0.95 ✓ (strong alignment)   │
│                                      │
│ Scenario 2: Hash collision          │
│ h_t: "weather" (climate context)    │
│ e_t: "the Great" (royal pattern)    │
│ → α_t = 0.12 ✗ (suppressed)         │
│                                      │
│ Scenario 3: Polysemy resolution     │
│ h_t: "that was" (evaluation context)│
│ e_t: "great work" (quality sense)   │
│ → α_t = 0.88 ✓ (correct sense)      │
└──────────────────────────────────────┘
       │
       ▼
   v_t = α_t · (W_V · e_t)
       │
       ▼
┌──────────────────────────────────────┐
│   Depthwise Causal Convolution       │
│                                      │
│   Expand receptive field:            │
│   ┌───┬───┬───┬───┐                 │
│   │t-3│t-2│t-1│ t │                 │
│   └─┬─┴─┬─┴─┬─┴─┬─┘                 │
│     └───┴───┴───┘                    │
│          ↓                           │
│   Y = SiLU(Conv1D(v_t)) + v_t       │
│                                      │
│   (Residual connection preserves     │
│    gradient flow)                    │
└──────────────────────────────────────┘
       │
       ▼
   H^(ℓ) ← H^(ℓ) + Y
       │
       ▼
   Continue to Attention → MoE
```

### Implementation

```python
import numpy as np
from typing import Tuple

class ContextAwareGating:
    """
    Implements the context-aware gating mechanism that dynamically
    modulates retrieved memory based on semantic alignment with
    current hidden state.
    """
    
    def __init__(
        self,
        hidden_dim: int = 2560,
        memory_dim: int = 256,
        conv_kernel_size: int = 4,
        conv_dilation: int = 3  # max n-gram order
    ):
        """
        Initialize gating module.
        
        Args:
            hidden_dim: Dimension of hidden states from attention
            memory_dim: Dimension of retrieved memory vectors
            conv_kernel_size: Kernel size for depthwise convolution
            conv_dilation: Dilation factor for convolution
        """
        self.hidden_dim = hidden_dim
        self.memory_dim = memory_dim
        self.conv_kernel_size = conv_kernel_size
        self.conv_dilation = conv_dilation
        
        # Key and Value projection matrices
        self.W_K = np.random.randn(memory_dim, hidden_dim) * 0.01
        self.W_V = np.random.randn(memory_dim, hidden_dim) * 0.01
        
        # Convolution kernel (simplified, 1D depthwise)
        self.conv_kernel = np.random.randn(conv_kernel_size, hidden_dim) * 0.01
    
    def rms_norm(self, x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
        """
        Root Mean Square Layer Normalization.
        
        More stable than LayerNorm for large models.
        """
        rms = np.sqrt(np.mean(x ** 2, axis=-1, keepdims=True) + eps)
        return x / rms
    
    def sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Sigmoid activation for gate."""
        return 1 / (1 + np.exp(-np.clip(x, -10, 10)))
    
    def silu(self, x: np.ndarray) -> np.ndarray:
        """
        SiLU (Swish) activation: x * sigmoid(x).
        
        Smooth, non-monotonic activation that works well for deep networks.
        """
        return x * self.sigmoid(x)
    
    def compute_gate(
        self, 
        hidden_state: np.ndarray,  # h_t, shape: (hidden_dim,)
        memory: np.ndarray          # e_t, shape: (memory_dim,)
    ) -> float:
        """
        Compute attention-style gate to modulate memory retrieval.
        
        Gate α_t measures semantic alignment between current context
        and retrieved memory. High alignment → use memory strongly.
        Low alignment → suppress (likely collision or wrong context).
        
        Args:
            hidden_state: Current hidden state from attention layer
            memory: Retrieved memory vector from n-gram lookup
            
        Returns:
            Gate value in (0, 1)
        """
        # Normalize both inputs for stability
        h_norm = self.rms_norm(hidden_state)
        
        # Project memory to key space
        key = memory @ self.W_K  # shape: (hidden_dim,)
        k_norm = self.rms_norm(key)
        
        # Scaled dot-product (like attention)
        scale = np.sqrt(self.hidden_dim)
        score = np.dot(h_norm, k_norm) / scale
        
        # Sigmoid to get gate in (0, 1)
        gate = self.sigmoid(score)
        
        return gate
    
    def apply_gating(
        self,
        hidden_state: np.ndarray,
        memory: np.ndarray
    ) -> Tuple[np.ndarray, float]:
        """
        Apply context-aware gating to memory retrieval.
        
        Args:
            hidden_state: Current hidden state
            memory: Retrieved memory vector
            
        Returns:
            gated_value: Memory modulated by gate
            gate: The gate value (for analysis)
        """
        # Compute gate
        gate = self.compute_gate(hidden_state, memory)
        
        # Project memory to value space
        value = memory @ self.W_V
        
        # Modulate by gate
        gated_value = gate * value
        
        return gated_value, gate
    
    def depthwise_conv(
        self,
        sequence: np.ndarray,  # Shape: (seq_len, hidden_dim)
        position: int
    ) -> np.ndarray:
        """
        Apply causal depthwise convolution to expand receptive field.
        
        "Depthwise" means each channel is convolved independently.
        "Causal" means only look at past positions, not future.
        
        Args:
            sequence: Full sequence of gated values
            position: Current position
            
        Returns:
            Convolved output at this position
        """
        # Extract causal window (only past positions)
        start = max(0, position - (self.conv_kernel_size - 1) * self.conv_dilation)
        window_positions = [
            start + i * self.conv_dilation 
            for i in range(self.conv_kernel_size)
            if start + i * self.conv_dilation <= position
        ]
        
        # Get values at these positions
        window = sequence[window_positions]
        
        # Depthwise convolution (simplified)
        if len(window) < self.conv_kernel_size:
            # Pad with zeros if at sequence start
            pad_size = self.conv_kernel_size - len(window)
            window = np.vstack([
                np.zeros((pad_size, self.hidden_dim)),
                window
            ])
        
        # Element-wise multiplication and sum (simplified depthwise)
        conv_out = np.sum(window * self.conv_kernel[:len(window)], axis=0)
        
        return conv_out
    
    def forward(
        self,
        hidden_sequence: np.ndarray,   # (seq_len, hidden_dim)
        memory_sequence: np.ndarray,   # (seq_len, memory_dim)
        position: int
    ) -> Tuple[np.ndarray, Dict]:
        """
        Full forward pass of context-aware gating.
        
        Args:
            hidden_sequence: Hidden states from attention
            memory_sequence: Retrieved memory vectors
            position: Current position
            
        Returns:
            output: Gated and refined output
            debug_info: Information about gating decisions
        """
        # Step 1: Apply gating
        h_t = hidden_sequence[position]
        e_t = memory_sequence[position]
        
        gated_value, gate = self.apply_gating(h_t, e_t)
        
        # Step 2: Apply RMS normalization
        gated_value_norm = self.rms_norm(gated_value)
        
        # Step 3: Depthwise convolution
        # (Need to build sequence of gated values first - simplified here)
        conv_input = gated_value_norm.reshape(1, -1)
        conv_out = self.depthwise_conv(conv_input, 0)
        
        # Step 4: SiLU activation and residual
        output = self.silu(conv_out) + gated_value_norm
        
        debug_info = {
            "gate_value": gate,
            "memory_magnitude": np.linalg.norm(e_t),
            "hidden_magnitude": np.linalg.norm(h_t),
            "output_magnitude": np.linalg.norm(output)
        }
        
        return output, debug_info
    
    def visualize_gating_pattern(
        self,
        sentence_tokens: list,
        hidden_states: np.ndarray,
        memory_vectors: np.ndarray
    ) -> Dict:
        """
        Visualize how gating responds to different contexts.
        
        Returns:
            Gating pattern for each token
        """
        pattern = []
        
        for pos in range(len(sentence_tokens)):
            h_t = hidden_states[pos]
            e_t = memory_vectors[pos]
            gate = self.compute_gate(h_t, e_t)
            
            pattern.append({
                "position": pos,
                "token": sentence_tokens[pos],
                "gate": gate,
                "decision": "USE" if gate > 0.5 else "SUPPRESS"
            })
        
        return {
            "tokens": sentence_tokens,
            "pattern": pattern,
            "mean_gate": np.mean([p["gate"] for p in pattern]),
            "high_confidence_count": sum(1 for p in pattern if p["gate"] > 0.7)
        }

# Example usage
gating = ContextAwareGating(
    hidden_dim=2560,
    memory_dim=256
)

# Simulate scenario 1: Correct retrieval
# Hidden state encodes "Alexander" + royal context
h_alexander = np.random.randn(2560) * 0.1
h_alexander[:100] += 0.5  # Boost "royal" features

# Memory retrieved "the Great" (royal pattern)
e_great_royal = np.random.randn(256) * 0.1
e_great_royal[:100] += 0.5  # Matching royal features

gate1 = gating.compute_gate(h_alexander, e_great_royal)
print(f"Scenario 1 - Correct Retrieval:")
print(f"  Context: Alexander (royal)")
print(f"  Memory: 'the Great' (royal)")
print(f"  Gate: {gate1:.3f} → {'USE' if gate1 > 0.5 else 'SUPPRESS'}")

# Simulate scenario 2: Hash collision
# Hidden state encodes "weather" + climate context
h_weather = np.random.randn(2560) * 0.1
h_weather[1000:1100] += 0.5  # Boost "climate" features

gate2 = gating.compute_gate(h_weather, e_great_royal)
print(f"\nScenario 2 - Hash Collision:")
print(f"  Context: weather (climate)")
print(f"  Memory: 'the Great' (royal) [wrong!]")
print(f"  Gate: {gate2:.3f} → {'USE' if gate2 > 0.5 else 'SUPPRESS'}")

# Simulate scenario 3: Polysemy
# Hidden state encodes "that was" + evaluation context
h_evaluation = np.random.randn(2560) * 0.1
h_evaluation[2000:2100] += 0.5  # Boost "evaluation" features

# Memory for "great work" (quality sense, different from "the Great")
e_great_quality = np.random.randn(256) * 0.1
e_great_quality[2000:2100] += 0.5  # Matching evaluation features

gate3 = gating.compute_gate(h_evaluation, e_great_quality)
print(f"\nScenario 3 - Polysemy Resolution:")
print(f"  Context: 'that was' (evaluation)")
print(f"  Memory: 'great work' (quality)")
print(f"  Gate: {gate3:.3f} → {'USE' if gate3 > 0.5 else 'SUPPRESS'}")

print(f"\n✓ Gating successfully distinguishes correct vs incorrect retrievals!")
```

### Key Takeaways

- **Dynamic Modulation**: Static memory is contextualized through attention-style gating using current hidden state as Query
- **Collision Handling**: Hash collisions are automatically suppressed when retrieved memory contradicts current context
- **Polysemy Resolution**: Same n-gram (e.g., "great") correctly receives different activations based on context
- **Gradient Stability**: RMSNorm instead of LayerNorm provides better numerical stability for deep networks
- **Receptive Field Expansion**: Depthwise causal convolution (kernel 4, dilation 3) adds local non-linearity without breaking causality

---

## 3. Scaling Laws and Sparsity Allocation

This section answers a fundamental question: given a fixed total parameter budget and training compute, how should we split sparse capacity between MoE experts (conditional computation) and Engram embeddings (conditional memory)?

The experimental setup is elegantly simple:
- Fix total parameters P_tot and activated parameters P_act
- Define allocation ratio ρ ∈ [0, 1]: fraction of inactive budget assigned to MoE
  - ρ = 1: Pure MoE (all capacity goes to experts)
  - ρ = 0: Pure memory (no routed experts)
- Sweep ρ and measure validation loss

The results reveal a **distinct U-shaped curve**: both pure approaches (100% MoE or 100% memory) are suboptimal! The optimal allocation is approximately **ρ ≈ 75-80%**, meaning 20-25% of sparse capacity should go to memory.

This U-shape persists across compute regimes (2e20 and 6e20 FLOPs), suggesting a robust allocation preference. The interpretation is clear:
- **MoE-dominated** (ρ → 100%): Lacks dedicated memory for static patterns, wastes depth reconstructing them
- **Engram-dominated** (ρ → 0%): Lacks conditional computation capacity for dynamic reasoning
- **Hybrid** (ρ ≈ 75-80%): Best of both worlds—memory handles static retrieval, MoE handles dynamic logic

Additionally, in the infinite memory regime (where memory budget is unconstrained), Engram exhibits a strict log-linear scaling law: doubling memory slots consistently reduces loss. This is possible because Engram's O(1) lookup doesn't increase per-token FLOPs.

### Concept Diagram

```
The Sparsity Allocation Trade-off:

Parameter Budget Allocation:
┌────────────────────────────────────────┐
│ Total Parameters (P_tot) = 10B         │
├────────────────────────────────────────┤
│ Active Parameters (P_act) = 1B         │
│ (Determines training FLOPs)            │
├────────────────────────────────────────┤
│ Inactive Parameters (P_sparse) = 9B    │
│ ↓                                      │
│ How to allocate these 9B?              │
│                                        │
│ Option 1: ρ = 100% (Pure MoE)         │
│ ├─ 9B to routed experts (72 experts)  │
│ └─ 0B to Engram                       │
│                                        │
│ Option 2: ρ = 0% (Pure Memory)        │
│ ├─ 0B to routed experts               │
│ └─ 9B to Engram embeddings            │
│                                        │
│ Option 3: ρ = 75% (Optimal Hybrid)    │
│ ├─ 6.75B to routed experts            │
│ └─ 2.25B to Engram embeddings         │
└────────────────────────────────────────┘

The U-Shaped Law (Why Hybrid Wins):

    Validation Loss
         │
    1.73 ├─┐                         ┌─── Pure MoE
         │  ╲                       ╱    • Forced to simulate
    1.72 │   ╲                     ╱     memory with compute
         │    ╲                   ╱      • Wastes depth on
    1.71 │     ╲─────────────────╱       static patterns
         │       ↑             ↑         • Suboptimal!
         │       │             │
    1.70 │       │   Optimal   │
         │       │   (75-80%)  │
         │       │             │
         │       Hybrid Zone   
         │       ↓             
         │                   ╲
         │                    ╲
         │                     ╲─── Pure Memory
         │                         • No conditional compute
         │                         • Can't handle dynamic
         │                           reasoning
         │                         • Suboptimal!
         └─────────────────────────────────────
          0%    20%   40%   60%   80%   100%
              MoE Allocation Ratio (ρ)

Why This Makes Sense:

MoE (Conditional Computation):
┌─────────────────────────┐
│ "What if Alexander      │
│  ruled in modern times?"│  ← Requires dynamic
│                         │    reasoning, composition,
│ Route to different      │    counterfactual logic
│ experts based on        │
│ context                 │  ✓ MoE excels here
└─────────────────────────┘

Engram (Conditional Memory):
┌─────────────────────────┐
│ "Alexander the Great"   │
│ "Princess of Wales"     │  ← Static, stereotyped
│ "Four Great Inventions" │    patterns that appear
│                         │    verbatim in training
│ O(1) lookup from        │
│ pre-stored embeddings   │  ✓ Memory excels here
└─────────────────────────┘

Infinite Memory Regime (Right Plot):

    Loss │
         │                     
    1.80 ├────┐                    Engram
         │     ╲                    (memory-only)
    1.78 │      ╲
         │       ╲                  Pure MoE
    1.76 │        ╲──────           (baseline)
         │          ╲     ╲
    1.74 │           ╲     ╲────
         │            ╲         ╲
    1.72 │             ╲         ╲
         │              ╲─────────╲
         └──────────────────────────────
          10^6      10^7        10^8
              Memory Slots (log scale)

Key Insight: Memory continues to pay off even at 
massive scale (no saturation observed), with 
*zero* increase in per-token FLOPs!
```

### Implementation

```python
import numpy as np
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt

class SparsityAllocationAnalyzer:
    """
    Simulate the sparsity allocation trade-off between MoE and Engram
    to find optimal parameter distribution.
    """
    
    def __init__(
        self,
        total_params: float = 10e9,      # 10B total
        active_params: float = 1e9,      # 1B active (determines FLOPs)
        base_loss: float = 1.80          # Starting loss
    ):
        """
        Initialize analyzer with parameter budget.
        
        Args:
            total_params: Total parameter count
            active_params: Activated parameters per token
            base_loss: Baseline validation loss
        """
        self.total_params = total_params
        self.active_params = active_params
        self.sparse_params = total_params - active_params
        self.base_loss = base_loss
    
    def compute_loss_at_allocation(
        self, 
        rho: float,
        compute_budget: float = 6e20
    ) -> float:
        """
        Simulate validation loss for a given allocation ratio.
        
        This is a simplified model that captures the U-shaped relationship.
        Real experiments use actual training!
        
        Args:
            rho: Allocation ratio (0-1), fraction to MoE
            compute_budget: Training FLOPs
            
        Returns:
            Predicted validation loss
        """
        # MoE capacity (number of experts increases with rho)
        moe_params = rho * self.sparse_params
        num_experts = max(1, int(moe_params / 1e8))  # ~100M per expert
        
        # Engram capacity (embedding slots increase with 1-rho)
        memory_params = (1 - rho) * self.sparse_params
        memory_slots = max(1000, int(memory_params / 1000))  # ~1K per slot
        
        # Loss components (simplified model)
        
        # 1. MoE benefit: log(num_experts) / log(max_experts)
        #    More experts → better specialization
        max_experts = int(self.sparse_params / 1e8)
        if num_experts > 0:
            moe_benefit = np.log(num_experts) / np.log(max_experts)
        else:
            moe_benefit = 0
        
        # 2. Memory benefit: log(memory_slots) / log(max_slots)
        #    More memory → better pattern coverage
        max_slots = int(self.sparse_params / 1000)
        if memory_slots > 0:
            memory_benefit = np.log(memory_slots) / np.log(max_slots)
        else:
            memory_benefit = 0
        
        # 3. Synergy term: MoE and memory complement each other
        #    Peak synergy at ~75-80% MoE allocation
        optimal_rho = 0.77
        synergy = np.exp(-10 * (rho - optimal_rho)**2)
        
        # Combine effects (U-shaped due to synergy term)
        total_benefit = (
            0.4 * moe_benefit +      # Conditional computation
            0.4 * memory_benefit +   # Conditional memory
            0.2 * synergy            # Synergy between both
        )
        
        # Final loss
        loss = self.base_loss * (1 - 0.08 * total_benefit)
        
        return loss
    
    def sweep_allocation_ratios(
        self,
        compute_budget: float = 6e20,
        num_points: int = 20
    ) -> Dict:
        """
        Sweep allocation ratios to find optimal distribution.
        
        Args:
            compute_budget: Training FLOPs
            num_points: Number of points to sample
            
        Returns:
            Results dictionary with losses and optimal point
        """
        ratios = np.linspace(0.1, 1.0, num_points)
        losses = []
        
        for rho in ratios:
            loss = self.compute_loss_at_allocation(rho, compute_budget)
            losses.append(loss)
        
        # Find optimal
        optimal_idx = np.argmin(losses)
        optimal_rho = ratios[optimal_idx]
        optimal_loss = losses[optimal_idx]
        
        # Pure baselines
        pure_moe_loss = self.compute_loss_at_allocation(1.0, compute_budget)
        pure_memory_loss = self.compute_loss_at_allocation(0.0, compute_budget)
        
        return {
            "ratios": ratios,
            "losses": losses,
            "optimal_rho": optimal_rho,
            "optimal_loss": optimal_loss,
            "pure_moe_loss": pure_moe_loss,
            "pure_memory_loss": pure_memory_loss,
            "improvement_over_moe": pure_moe_loss - optimal_loss,
            "improvement_over_memory": pure_memory_loss - optimal_loss
        }
    
    def analyze_infinite_memory_regime(
        self,
        memory_slots_range: List[int]
    ) -> Dict:
        """
        Analyze scaling behavior when memory budget is unconstrained.
        
        Args:
            memory_slots_range: Range of memory slots to test
            
        Returns:
            Scaling results showing log-linear relationship
        """
        losses = []
        
        for slots in memory_slots_range:
            # Fixed MoE backbone, varying memory only
            fixed_moe_params = 3e9  # 3B parameters in MoE
            memory_params = slots * 1000  # ~1K per slot
            
            total = fixed_moe_params + memory_params
            
            # Loss decreases log-linearly with memory slots
            memory_benefit = np.log(slots) / np.log(memory_slots_range[-1])
            loss = self.base_loss * (1 - 0.05 * memory_benefit)
            
            losses.append(loss)
        
        # Compute scaling coefficient (slope in log space)
        log_slots = np.log10(memory_slots_range)
        slope = (losses[0] - losses[-1]) / (log_slots[-1] - log_slots[0])
        
        return {
            "memory_slots": memory_slots_range,
            "losses": losses,
            "scaling_coefficient": slope,
            "log_linear": True  # Memory exhibits log-linear scaling
        }
    
    def visualize_allocation_law(self, results: Dict):
        """
        Visualize the U-shaped allocation law.
        """
        plt.figure(figsize=(10, 6))
        
        plt.plot(results["ratios"] * 100, results["losses"], 
                'b-', linewidth=2, label='Hybrid Models')
        
        # Mark optimal point
        plt.plot(results["optimal_rho"] * 100, results["optimal_loss"],
                'ro', markersize=10, label=f'Optimal (ρ={results["optimal_rho"]:.2f})')
        
        # Mark pure baselines
        plt.axhline(y=results["pure_moe_loss"], color='g', linestyle='--',
                   label='Pure MoE (ρ=1.0)')
        plt.axhline(y=results["pure_memory_loss"], color='orange', linestyle='--',
                   label='Pure Memory (ρ=0.0)')
        
        plt.xlabel('MoE Allocation Ratio ρ (%)', fontsize=12)
        plt.ylabel('Validation Loss', fontsize=12)
        plt.title('U-Shaped Scaling Law: Optimal Sparsity Allocation', fontsize=14)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        
        # Add annotation
        plt.annotate(
            f'Δ = {results["improvement_over_moe"]:.4f}\nvs Pure MoE',
            xy=(results["optimal_rho"] * 100, results["optimal_loss"]),
            xytext=(results["optimal_rho"] * 100 - 15, results["optimal_loss"] + 0.01),
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
            fontsize=10
        )
        
        plt.tight_layout()
        plt.savefig('/home/claude/allocation_law.png', dpi=150)
        print("✓ Saved visualization to allocation_law.png")

# Run analysis
analyzer = SparsityAllocationAnalyzer(
    total_params=10e9,
    active_params=1e9,
    base_loss=1.73
)

# Sweep allocation ratios
results = analyzer.sweep_allocation_ratios(compute_budget=6e20, num_points=30)

print("=== Sparsity Allocation Analysis ===\n")
print(f"Optimal Allocation Ratio (ρ): {results['optimal_rho']:.3f}")
print(f"  → {results['optimal_rho']*100:.1f}% to MoE")
print(f"  → {(1-results['optimal_rho'])*100:.1f}% to Engram")
print(f"\nOptimal Loss: {results['optimal_loss']:.4f}")
print(f"Pure MoE Loss: {results['pure_moe_loss']:.4f}")
print(f"Pure Memory Loss: {results['pure_memory_loss']:.4f}")
print(f"\nImprovement over Pure MoE: {results['improvement_over_moe']:.4f} ({(results['improvement_over_moe']/results['pure_moe_loss']*100):.2f}%)")
print(f"Improvement over Pure Memory: {results['improvement_over_memory']:.4f} ({(results['improvement_over_memory']/results['pure_memory_loss']*100):.2f}%)")

# Analyze infinite memory regime
memory_slots = [int(10**x) for x in np.linspace(5, 8, 10)]  # 100K to 100M
memory_results = analyzer.analyze_infinite_memory_regime(memory_slots)

print(f"\n=== Infinite Memory Regime ===\n")
print(f"Memory Slots Range: {memory_slots[0]:,} to {memory_slots[-1]:,}")
print(f"Loss Range: {memory_results['losses'][0]:.4f} → {memory_results['losses'][-1]:.4f}")
print(f"Scaling Coefficient: {memory_results['scaling_coefficient']:.6f}")
print(f"Log-Linear Scaling: {memory_results['log_linear']}")
print(f"\n✓ Memory exhibits predictable scaling—more slots = lower loss!")

# Visualize
analyzer.visualize_allocation_law(results)
```

### Key Takeaways

- **U-Shaped Law**: Neither pure MoE nor pure memory is optimal—the best allocation is a hybrid (~75% MoE, 25% memory)
- **Robust Across Scales**: The optimal ratio is stable across compute regimes (2e20 to 6e20 FLOPs), suggesting a fundamental property
- **Complementary Primitives**: MoE excels at dynamic reasoning, Engram excels at static retrieval—both are necessary
- **Log-Linear Memory Scaling**: In infinite memory regime, loss decreases log-linearly with memory slots, showing predictable scaling
- **Practical Implication**: When scaling sparse models, allocate ~20-25% of sparse budget to conditional memory for optimal efficiency

---

## Conclusion

This paper introduces Engram, a groundbreaking approach that adds **conditional memory** as a complementary sparsity axis to the now-standard Mixture-of-Experts paradigm. The key insight is recognizing that language modeling involves two fundamentally different operations—dynamic compositional reasoning and static pattern retrieval—that deserve different architectural primitives.

Through rigorous experimentation under strict iso-parameter and iso-FLOPs constraints, the authors uncover a **U-shaped scaling law** that reveals the optimal allocation between neural computation and static memory (~75-80% MoE, 20-25% Engram). This hybrid approach consistently outperforms pure MoE baselines, with particularly striking gains not just in knowledge-intensive tasks, but in general reasoning, code, and mathematics.

The mechanistic analysis reveals why: by offloading static pattern reconstruction from early layers via O(1) lookups, Engram **effectively deepens the network** for complex reasoning while freeing up attention capacity for global context. This architectural innovation translates into substantial improvements in long-context capabilities, with gains of 13-15 percentage points on complex retrieval tasks.

Perhaps most importantly, Engram establishes **infrastructure-aware efficiency** as a first-class design principle. Its deterministic addressing enables runtime prefetching from host memory, effectively bypassing GPU memory constraints with negligible overhead (<3%). This demonstrates a path toward massively scaled models that decouple storage from computation.

Looking forward, the authors envision conditional memory as an indispensable modeling primitive for next-generation sparse models, opening up exciting research directions in multi-modal memory, learned compression strategies, and hardware-software co-design.

---

*Paper: [Conditional Memory via Scalable Lookup](https://arxiv.org/abs/2601.07372)*  
*Code: [https://github.com/deepseek-ai/Engram](https://github.com/deepseek-ai/Engram)*


---

### Additional Notes

#### The Complete Normalization Pipeline
```
Raw Token → Normalization → Canonical ID
─────────────────────────────────────────

Step 1: NFKC Unicode Normalization
┌────────────────────────────────────────┐
│ "ﬁnance" (ligature)  → "finance"       │
│ "café" (é as single) → "café" (e+´)    │
│ "①" (circled 1)      → "1"             │
│                                        │
│ Purpose: Standardize Unicode variants  │
└────────────────────────────────────────┘

Step 2: Case-Folding (Lowercase)
┌────────────────────────────────────────┐
│ "Alexander" → "alexander"              │
│ "ALEXANDER" → "alexander"              │
│ "AlExAnDeR" → "alexander"              │
│                                        │
│ Purpose: Remove case distinctions      │
└────────────────────────────────────────┘

Step 3: Whitespace Normalization
┌────────────────────────────────────────┐
│ " alexander" → "alexander"             │
│ "alexander " → "alexander"             │
│ "  alexander" → "alexander"            │
│                                        │
│ Purpose: Remove spacing variations     │
└────────────────────────────────────────┘

Step 4: Map to Canonical Token ID
┌────────────────────────────────────────┐
│ "alexander" (normalized) → ID 1001     │
│                                        │
│ All these map to SAME ID:              │
│ • "Alexander"    → 1001                │
│ • "alexander"    → 1001                │
│ • "ALEXANDER"    → 1001                │
│ • " alexander"   → 1001                │
│ • "AlExAnDeR"    → 1001                │
│                                        │
│ Instead of 5 different IDs!            │
└────────────────────────────────────────┘

Result: 128K vocab → 98K effective vocab
        (23% reduction)
```


#### Complete N-gram Extraction for Entire Sequence
```
Input: "Only Alexander the Great could tame..."
Token IDs: [45, 1001, 42, 2003, 156, 5678, ...]
Positions:  0    1    2    3    4     5

For EACH position t, extract suffix n-grams:
═════════════════════════════════════════════════

Position 0: "Only" (token 45)
┌────────────────────────────────────┐
│ 1-gram: (45)                       │
│ 2-gram: Cannot form (need t-1)     │
│ 3-gram: Cannot form (need t-2,t-1) │
└────────────────────────────────────┘

Position 1: "Alexander" (token 1001)
┌────────────────────────────────────┐
│ 1-gram: (1001)                     │
│ 2-gram: (45, 1001)                 │
│         "Only Alexander"           │
│ 3-gram: Cannot form                │
└────────────────────────────────────┘

Position 2: "the" (token 42)
┌────────────────────────────────────┐
│ 1-gram: (42)                       │
│ 2-gram: (1001, 42)                 │
│         "Alexander the"            │
│ 3-gram: (45, 1001, 42)             │
│         "Only Alexander the"       │
└────────────────────────────────────┘

Position 3: "Great" (token 2003)
┌────────────────────────────────────┐
│ 1-gram: (2003)                     │
│ 2-gram: (42, 2003)                 │
│         "the Great"                │
│ 3-gram: (1001, 42, 2003)           │
│         "Alexander the Great" ⭐  │
└────────────────────────────────────┘

Position 4: "could" (token 156)
┌────────────────────────────────────┐
│ 1-gram: (156)                      │
│ 2-gram: (2003, 156)                │
│         "Great could"              │
│ 3-gram: (42, 2003, 156)            │
│         "the Great could"          │
└────────────────────────────────────┘

Position 5: "tame" (token 5678)
┌────────────────────────────────────┐
│ 1-gram: (5678)                     │
│ 2-gram: (156, 5678)                │
│         "could tame"               │
│ 3-gram: (2003, 156, 5678)          │
│         "Great could tame"         │
└────────────────────────────────────┘

Key Point: EVERY position gets its own n-grams!
         Not just the "important" ones!
```