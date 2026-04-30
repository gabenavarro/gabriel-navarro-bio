@{id = "de0ddce7-b63b-4c12-a554-bdbafd5eedb5"
  title = "Foundation Models Improve Perturbation Response Prediction"
  date = "2026-01-20T00:00:00Z"
  tags = ['journal club', 'machine learning', 'arxiv', 'language models']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/cover_art_0020.svg"
  description = ""This entry is a summary of the paper "Foundation Models Improve Perturbation Response Prediction" where Cole et al. tackles a central question in computational biology: can foundation models — large pretrained neural networks — actually help predict how cells respond to genetic or chemical perturbations? ""
  type = "note"
  disabled = "False"
}

<p align="center">
  <img src="https://storage.googleapis.com/gn-portfolio/images/cover_art_0020.svg" max-width="700">
</p>


# Foundation Models Improve Perturbation Response Prediction

*Analysis of Cole et al. (2026), GenBio AI — bioRxiv preprint*
*Generated on March 20, 2026*

---

## Table of Contents

- [Abstract](#abstract)
- [Introduction](#introduction)
- [Results](#results)
  - [Embeddings Vary Dramatically in Utility](#embeddings-vary-dramatically-in-utility)
  - [Fine-Tuning Improves Performance for Some Models](#fine-tuning-improves-performance-for-some-models)
  - [Complex Translation Methods Don't Beat Simple Ones](#complex-translation-methods-dont-beat-simple-ones)
  - [FMs Can Also Improve Small Molecule Predictions](#fms-can-also-improve-small-molecule-predictions)
  - [Integrating Diverse FMs Further Improves Performance](#integrating-diverse-fms-further-improves-performance)
- [Methods](#methods)
  - [Log Fold-Change Regression Formulation](#log-fold-change-regression-formulation)
  - [Differentially Expressed Gene (DEG) Classification](#differentially-expressed-gene-deg-classification)
  - [Datasets](#datasets)
  - [Embedding Sources](#embedding-sources)
  - [Fusion Architecture](#fusion-architecture)
- [Discussion](#discussion)
- [Key Takeaways](#key-takeaways-summary)

---

## Abstract

### Overview

This paper tackles a central question in computational biology: can foundation models (FMs) — large pretrained neural networks — actually help predict how cells respond to genetic or chemical perturbations? Recent literature has given contradictory answers, with some groups claiming FMs are no better than simple baselines like PCA. The authors resolve this by running an exhaustive benchmark of over 600 models.

The key finding is nuanced: **some** FMs do fail to beat baselines, but **others** — particularly those trained on protein-protein interaction networks (interactome data) — significantly outperform simple methods. Furthermore, combining embeddings from multiple FMs through an attention-based fusion model pushes performance even further, in some cases reaching the theoretical limit set by experimental noise.

This matters because accurate perturbation prediction is foundational for drug discovery, understanding disease mechanisms, and building "virtual cell" models that simulate biology in silico.

### Concept Diagram

<svg viewBox="0 0 720 420" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="fm-1-title">
  <title id="fm-1-title">The central question: can foundation models predict cellular response to perturbations?</title>
  <defs>
    <marker id="arrow1" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#64748b"/></marker>
    <marker id="arrow1g" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#22c55e"/></marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="16" font-weight="700" fill="#1e293b">The Central Question</text>
  <!-- Perturbation box -->
  <rect x="40" y="50" width="180" height="70" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="130" y="78" text-anchor="middle" font-weight="600" fill="#1e40af">Perturbation</text>
  <text x="130" y="96" text-anchor="middle" font-size="11" fill="#64748b">(gene KO or drug)</text>
  <!-- Arrow with ? -->
  <line x1="220" y1="85" x2="370" y2="85" stroke="#64748b" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#arrow1)"/>
  <text x="295" y="78" text-anchor="middle" font-size="20" font-weight="700" fill="#ef4444">?</text>
  <!-- Response box -->
  <rect x="380" y="50" width="200" height="70" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="480" y="78" text-anchor="middle" font-weight="600" fill="#92400e">Cellular Response</text>
  <text x="480" y="96" text-anchor="middle" font-size="11" fill="#64748b">(gene expression)</text>
  <!-- Down arrow -->
  <line x1="130" y1="120" x2="130" y2="170" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow1)"/>
  <text x="230" y="152" font-size="11" fill="#64748b">Represented as...</text>
  <!-- Embedding box -->
  <rect x="55" y="178" width="150" height="55" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="130" y="200" text-anchor="middle" font-weight="600" fill="#166534">Embedding</text>
  <text x="130" y="218" text-anchor="middle" font-size="11" fill="#64748b">from FM</text>
  <!-- Branch lines -->
  <line x1="130" y1="233" x2="130" y2="270" stroke="#22c55e" stroke-width="1.5"/>
  <line x1="130" y1="270" x2="90" y2="270" stroke="#22c55e" stroke-width="1.5"/>
  <line x1="130" y1="270" x2="630" y2="270" stroke="#22c55e" stroke-width="1.5"/>
  <!-- DNA -->
  <line x1="90" y1="270" x2="90" y2="300" stroke="#22c55e" stroke-width="1.5" marker-end="url(#arrow1g)"/>
  <rect x="30" y="308" width="120" height="80" rx="8" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="90" y="332" text-anchor="middle" font-weight="600" fill="#991b1b">DNA FMs</text>
  <text x="90" y="352" text-anchor="middle" font-size="12" fill="#dc2626">weak</text>
  <text x="90" y="372" text-anchor="middle" font-size="16">✗</text>
  <!-- Protein -->
  <line x1="270" y1="270" x2="270" y2="300" stroke="#22c55e" stroke-width="1.5" marker-end="url(#arrow1g)"/>
  <rect x="210" y="308" width="120" height="80" rx="8" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="270" y="332" text-anchor="middle" font-weight="600" fill="#991b1b">Protein FMs</text>
  <text x="270" y="352" text-anchor="middle" font-size="12" fill="#dc2626">weak</text>
  <text x="270" y="372" text-anchor="middle" font-size="16">✗</text>
  <!-- Expression -->
  <line x1="450" y1="270" x2="450" y2="300" stroke="#22c55e" stroke-width="1.5" marker-end="url(#arrow1g)"/>
  <rect x="390" y="308" width="120" height="80" rx="8" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="450" y="332" text-anchor="middle" font-weight="600" fill="#854d0e">scRNA FMs</text>
  <text x="450" y="352" text-anchor="middle" font-size="12" fill="#ca8a04">medium</text>
  <text x="450" y="372" text-anchor="middle" font-size="16">◐</text>
  <!-- Interactome -->
  <line x1="630" y1="270" x2="630" y2="300" stroke="#22c55e" stroke-width="1.5" marker-end="url(#arrow1g)"/>
  <rect x="560" y="308" width="140" height="80" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="630" y="332" text-anchor="middle" font-weight="700" fill="#166534">Interactome FMs</text>
  <text x="630" y="352" text-anchor="middle" font-size="12" font-weight="700" fill="#16a34a">STRONG</text>
  <text x="630" y="372" text-anchor="middle" font-size="16">✓</text>
  <!-- Side label -->
  <text x="480" y="148" font-size="11" fill="#475569" font-style="italic">Which FM embeddings actually</text>
  <text x="480" y="164" font-size="11" fill="#475569" font-style="italic">help predict the response?</text>
</svg>

### Key Takeaways

- **Not all FMs are equal**: Prior knowledge / interactome-based FMs dramatically outperform sequence-based and expression-based FMs for perturbation prediction.
- **Over 600 models tested**: The most comprehensive benchmark of FM embeddings for perturbation response to date.
- **Fusion helps**: Combining multiple FM embeddings with attention-based fusion reaches experimental error limits in some cell lines.
- **Simple predictors suffice**: Even kNN regression works well when paired with the right embedding — the embedding choice matters more than model complexity.

---

## Introduction

### Overview

Predicting how cells respond to perturbations — whether you knock out a gene, overexpress it, or treat the cell with a drug — is one of the holy grails of molecular biology. If we could accurately simulate these responses computationally, it would transform drug discovery by letting researchers screen interventions *in silico* before running expensive wet-lab experiments.

The field has evolved from differential equation-based models of gene regulatory networks, through classical ML approaches (ElasticNet, matrix factorization), to deep learning methods (Dr.VAE, scGen, CPA, GEARS). Most recently, transformer-based foundation models pretrained on massive single-cell atlases — Geneformer, scGPT, scFoundation — have entered the scene, claiming strong results. But a counter-narrative has emerged: papers like PerturbBench and Ahlmann-Eltze et al. argue that FMs don't outperform simple linear baselines.

This paper resolves the contradiction by showing that **the answer depends on which FM you use**. The authors take an "embedding-centric" view: rather than comparing complex end-to-end architectures, they extract embeddings from various FMs and feed them into simple predictors (kNN). This isolates the quality of the embedding itself — the core biological knowledge captured by the FM.

### Concept Diagram

<svg viewBox="0 0 700 340" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="fm-2-title">
  <title id="fm-2-title">Evolution of Perturbation Prediction Methods</title>
  <defs>
    <marker id="arrow2" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#64748b"/></marker>
    <marker id="arrow2b" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#3b82f6"/></marker>
  </defs>
  <text x="350" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Evolution of Perturbation Prediction Methods</text>
  <!-- Row 1: Three eras -->
  <rect x="20" y="50" width="170" height="65" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="105" y="74" text-anchor="middle" font-weight="600" fill="#334155">Differential Eqns</text>
  <text x="105" y="92" text-anchor="middle" font-size="11" fill="#64748b">(GRNs)</text>
  <line x1="190" y1="82" x2="240" y2="82" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow2)"/>
  <rect x="250" y="50" width="170" height="65" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="335" y="74" text-anchor="middle" font-weight="600" fill="#334155">Classical ML</text>
  <text x="335" y="92" text-anchor="middle" font-size="11" fill="#64748b">(ElasticNet, MatFact)</text>
  <line x1="420" y1="82" x2="470" y2="82" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow2)"/>
  <rect x="480" y="50" width="190" height="65" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="575" y="74" text-anchor="middle" font-weight="600" fill="#334155">Deep Learning</text>
  <text x="575" y="92" text-anchor="middle" font-size="11" fill="#64748b">(scGen, CPA, GEARS)</text>
  <!-- Arrow down -->
  <line x1="575" y1="115" x2="575" y2="155" stroke="#3b82f6" stroke-width="2" marker-end="url(#arrow2b)"/>
  <!-- Foundation Models box -->
  <rect x="460" y="162" width="230" height="60" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
  <text x="575" y="187" text-anchor="middle" font-weight="700" font-size="14" fill="#1e40af">Foundation Models</text>
  <text x="575" y="205" text-anchor="middle" font-size="11" fill="#3b82f6">(This work)</text>
  <!-- Branch down -->
  <line x1="575" y1="222" x2="575" y2="255" stroke="#3b82f6" stroke-width="2"/>
  <line x1="350" y1="255" x2="680" y2="255" stroke="#3b82f6" stroke-width="1.5"/>
  <!-- Three outcomes -->
  <line x1="350" y1="255" x2="350" y2="275" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arrow2b)"/>
  <rect x="280" y="282" width="140" height="45" rx="8" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="350" y="304" text-anchor="middle" font-size="12" fill="#991b1b">Some FMs fail</text>
  <text x="350" y="318" text-anchor="middle" font-size="10" fill="#b91c1c">✗ No gain over baselines</text>
  <line x1="520" y1="255" x2="520" y2="275" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arrow2b)"/>
  <rect x="440" y="282" width="160" height="45" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="520" y="304" text-anchor="middle" font-size="12" fill="#166534">Some FMs excel</text>
  <text x="520" y="318" text-anchor="middle" font-size="10" fill="#16a34a">✓ Interactome-based</text>
  <line x1="680" y1="255" x2="680" y2="275" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arrow2b)"/>
  <rect x="605" y="282" width="150" height="45" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5"/>
  <text x="680" y="304" text-anchor="middle" font-size="12" fill="#6b21a8">Fusion is best</text>
  <text x="680" y="318" text-anchor="middle" font-size="10" fill="#7c3aed">★ Multi-modal</text>
</svg>

### Key Takeaways

- **Perturbation prediction** connects to both basic biology (understanding networks) and applied biology (drug discovery, side effect detection).
- **Contradictory claims** in the literature motivated this comprehensive study.
- **Embedding-centric approach** decouples the FM representation from the prediction model, enabling fair comparison.

---

## Results

### Embeddings Vary Dramatically in Utility

#### Overview

The most striking finding is that embedding quality varies enormously across FM types, and this variation is primarily explained by the **modality** of the training data. The authors benchmarked embeddings on the Essential dataset (4 cell lines, ~2000 perturbations each) — much larger than the commonly used Norman dataset, which had masked real performance differences.

Interactome-based embeddings (WaveGC, STRING GNN, GenotypeVAE, GenePT) consistently rank at the top. These capture how genes interact with each other in cellular networks. Expression-based FMs (scGPT, AIDO.Cell) are middling, while protein sequence and DNA sequence FMs generally perform worst. The intuition is that knowing what a gene's protein *looks like* matters less than knowing what it *does* and *who it talks to* in the cell.

Remarkably, on the K562 cell line, the best single embedding closes 77% of the gap between a naive baseline and the estimated experimental error limit — using nothing more than kNN regression. This tells us the embedding is doing the heavy lifting, not the prediction algorithm.

#### Concept Diagram

<svg viewBox="0 0 680 460" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="fm-3-title">
  <title id="fm-3-title">Embedding Performance Ranking (Best to Worst)</title>
  <text x="340" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Embedding Performance Ranking (Best → Worst)</text>
  <text x="340" y="42" text-anchor="middle" font-size="11" fill="#64748b">Key insight: Modality matters more than model architecture</text>
  <!-- Category 1: Prior Knowledge -->
  <rect x="30" y="60" width="620" height="115" rx="10" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="50" y="82" font-weight="700" fill="#166534" font-size="14">★ PRIOR KNOWLEDGE (Interactome)</text>
  <circle cx="60" cy="100" r="5" fill="#22c55e"/><text x="75" y="105" fill="#334155">STRING WaveGC</text>
  <rect x="230" y="93" width="160" height="16" rx="3" fill="#22c55e" opacity="0.8"/><text x="400" y="105" font-size="11" fill="#16a34a" font-weight="600">← Best overall</text>
  <circle cx="60" cy="120" r="5" fill="#22c55e"/><text x="75" y="125" fill="#334155">STRING GNN</text>
  <rect x="230" y="113" width="148" height="16" rx="3" fill="#22c55e" opacity="0.65"/>
  <circle cx="60" cy="140" r="5" fill="#22c55e"/><text x="75" y="145" fill="#334155">GenotypeVAE</text>
  <rect x="230" y="133" width="140" height="16" rx="3" fill="#22c55e" opacity="0.55"/>
  <circle cx="60" cy="160" r="5" fill="#22c55e"/><text x="75" y="165" fill="#334155">GenePT variants</text>
  <rect x="230" y="153" width="132" height="16" rx="3" fill="#22c55e" opacity="0.45"/>
  <!-- Category 2: Expression -->
  <rect x="30" y="190" width="620" height="95" rx="10" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="50" y="212" font-weight="700" fill="#854d0e" font-size="14">● EXPRESSION (scRNA-seq FMs)</text>
  <circle cx="60" cy="232" r="5" fill="#eab308"/><text x="75" y="237" fill="#334155">scGPT</text>
  <rect x="230" y="225" width="100" height="16" rx="3" fill="#eab308" opacity="0.6"/>
  <circle cx="60" cy="252" r="5" fill="#eab308"/><text x="75" y="257" fill="#334155">AIDO.Cell 100M</text>
  <rect x="230" y="245" width="94" height="16" rx="3" fill="#eab308" opacity="0.5"/>
  <text x="400" y="257" font-size="11" fill="#ca8a04" font-style="italic">Bigger = better</text>
  <circle cx="60" cy="272" r="5" fill="#eab308"/><text x="75" y="277" fill="#334155">scPRINT</text>
  <rect x="230" y="265" width="88" height="16" rx="3" fill="#eab308" opacity="0.4"/>
  <!-- Category 3: Protein -->
  <rect x="30" y="300" width="620" height="75" rx="10" fill="#fff1f2" stroke="#f97316" stroke-width="1.5"/>
  <text x="50" y="322" font-weight="700" fill="#9a3412" font-size="14">○ PROTEIN SEQUENCE</text>
  <circle cx="60" cy="342" r="5" fill="#f97316"/><text x="75" y="347" fill="#334155">STRING Sequence / ESM2 / AIDO.ProteinRAG</text>
  <rect x="330" y="335" width="64" height="16" rx="3" fill="#f97316" opacity="0.4"/>
  <!-- Category 4: DNA -->
  <rect x="30" y="390" width="620" height="55" rx="10" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="50" y="412" font-weight="700" fill="#991b1b" font-size="14">△ DNA SEQUENCE</text>
  <circle cx="60" cy="432" r="5" fill="#ef4444"/><text x="75" y="437" fill="#334155">AIDO.DNA</text>
  <rect x="230" y="425" width="42" height="16" rx="3" fill="#ef4444" opacity="0.4"/>
  <text x="282" y="437" font-size="11" fill="#dc2626" font-style="italic">← Weakest</text>
</svg>

#### Implementation

```python
import numpy as np
from typing import Dict, List, Tuple

def knn_perturbation_prediction(
    train_embeddings: np.ndarray,   # (N_train, d) - embeddings of training perturbations
    train_lfc: np.ndarray,          # (N_train, G) - observed LFC for training perturbations
    test_embeddings: np.ndarray,    # (N_test, d)  - embeddings of test perturbations
    k: int = 20
) -> np.ndarray:
    """
    Predict perturbation response using kNN in embedding space.

    The core idea: perturbations with similar embeddings should
    produce similar cellular responses. The FM embedding encodes
    biological similarity — kNN leverages that to predict LFC.

    Args:
        train_embeddings: FM embeddings for seen perturbations
        train_lfc: Log fold-change vectors for seen perturbations
        test_embeddings: FM embeddings for unseen perturbations
        k: Number of neighbors

    Returns:
        Predicted LFC vectors for test perturbations (N_test, G)
    """
    predictions = []

    for test_emb in test_embeddings:
        # Step 1: Compute distances in embedding space
        distances = np.linalg.norm(train_embeddings - test_emb, axis=1)

        # Step 2: Find k nearest neighbors
        nn_indices = np.argsort(distances)[:k]

        # Step 3: Average their observed responses
        predicted_lfc = train_lfc[nn_indices].mean(axis=0)
        predictions.append(predicted_lfc)

    return np.array(predictions)

# Example: evaluate with L2 error
def evaluate_l2(true_lfc: np.ndarray, pred_lfc: np.ndarray) -> float:
    """Average L2 error across perturbations."""
    return np.mean(np.linalg.norm(true_lfc - pred_lfc, axis=1))
```

#### Key Takeaways

- **Interactome-based FMs dominate**: The top 10 embeddings in ranked performance are all derived from prior knowledge (interaction networks, functional annotations, or text descriptions of genes).
- **Modality matters more than architecture**: Models trained on the same data type cluster together in performance, even when their architectures differ substantially.
- **Bigger models help**: Within the expression FM category, AIDO.Cell 100M > 10M > 3M, suggesting scaling laws apply.
- **Simple baselines can mislead**: On the small Norman dataset, differences are hard to detect; larger datasets like Essential reveal robust trends.

---

### Fine-Tuning Improves Performance for Some Models

#### Overview

Can you improve an FM's perturbation predictions by fine-tuning it on the actual perturbation data? The answer is: it depends. The authors tested two approaches for AIDO.Cell (3M) and one for STRING GNN.

For AIDO.Cell, the "In-Silico KO" method — where the target gene's expression is masked and the model predicts the downstream effect — provided a significant boost, outperforming both the frozen kNN baseline and an MLP ablation. However, a simpler "Indexing" approach (extracting the gene's embedding and training a head on top) actually hurt performance. For STRING GNN, fine-tuning degraded results relative to using frozen embeddings.

The takeaway is sobering: current perturbation datasets may be too small to reliably fine-tune large models. Overfitting is a real risk. Using frozen FM embeddings as features for simple predictors is often the safer bet.

#### Concept Diagram

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="fm-4-title">
  <title id="fm-4-title">Fine-Tuning Results on K562</title>
  <text x="340" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Fine-Tuning Results on K562</text>
  <!-- Axis labels -->
  <text x="100" y="56" font-size="11" fill="#64748b" font-weight="600">Method</text>
  <text x="630" y="56" font-size="11" fill="#64748b" font-weight="600" text-anchor="end">L2 Error (lower = better)</text>
  <!-- Bars -->
  <!-- STRING GNN Frozen -->
  <text x="240" y="85" text-anchor="end" fill="#334155" font-size="12">STRING GNN Frozen + kNN</text>
  <rect x="250" y="72" width="280" height="20" rx="4" fill="#3b82f6" opacity="0.7"/>
  <text x="538" y="87" font-size="11" fill="#1e40af" font-weight="600">Good</text>
  <!-- STRING GNN FT -->
  <text x="240" y="115" text-anchor="end" fill="#334155" font-size="12">STRING GNN Fine-Tuned</text>
  <rect x="250" y="102" width="320" height="20" rx="4" fill="#ef4444" opacity="0.6"/>
  <text x="578" y="117" font-size="11" fill="#dc2626" font-weight="600">Worse ✗</text>
  <!-- Spacer -->
  <line x1="30" y1="135" x2="650" y2="135" stroke="#e2e8f0" stroke-width="1"/>
  <!-- AIDO.Cell Frozen kNN -->
  <text x="240" y="160" text-anchor="end" fill="#334155" font-size="12">AIDO.Cell 3M Frozen + kNN</text>
  <rect x="250" y="147" width="300" height="20" rx="4" fill="#94a3b8" opacity="0.5"/>
  <text x="558" y="162" font-size="11" fill="#64748b">Baseline</text>
  <!-- AIDO.Cell Frozen MLP -->
  <text x="240" y="190" text-anchor="end" fill="#334155" font-size="12">AIDO.Cell 3M Frozen + MLP</text>
  <rect x="250" y="177" width="274" height="20" rx="4" fill="#3b82f6" opacity="0.55"/>
  <text x="532" y="192" font-size="11" fill="#1e40af">Better</text>
  <!-- AIDO.Cell FT Indexing -->
  <text x="240" y="220" text-anchor="end" fill="#334155" font-size="12">AIDO.Cell 3M FT (Indexing)</text>
  <rect x="250" y="207" width="330" height="20" rx="4" fill="#ef4444" opacity="0.5"/>
  <text x="588" y="222" font-size="11" fill="#dc2626" font-weight="600">Worse ✗</text>
  <!-- AIDO.Cell FT In-Silico KO -->
  <text x="240" y="250" text-anchor="end" fill="#334155" font-size="12">AIDO.Cell 3M FT (In-Silico KO)</text>
  <rect x="250" y="237" width="248" height="20" rx="4" fill="#22c55e" opacity="0.7"/>
  <text x="506" y="252" font-size="11" fill="#166534" font-weight="700">Best ✓</text>
  <!-- Experimental Error line -->
  <line x1="470" y1="62" x2="470" y2="270" stroke="#a855f7" stroke-width="1.5" stroke-dasharray="5,4"/>
  <text x="475" y="280" font-size="10" fill="#7c3aed">Exptl. Error Limit</text>
  <!-- Legend box -->
  <rect x="30" y="298" width="620" height="32" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
  <text x="50" y="318" font-size="11" fill="#475569" font-style="italic">Lesson: Fine-tuning can help OR hurt depending on method and architecture. Data scarcity makes overfitting a major risk.</text>
</svg>

#### Implementation

```python
import numpy as np
from typing import Optional

def in_silico_ko_prediction(
    control_expression: np.ndarray,  # (G,) mean expression of control cells
    target_gene_idx: int,            # index of knocked-out gene
    encoder_fn,                      # FM encoder: (G,) → (G, d)
    prediction_head_fn               # head: (d,) → (G,)
) -> np.ndarray:
    """
    In-Silico Knockout: mask the target gene, encode with FM,
    then predict LFC from the contextualized embedding.

    This approach works because the FM learns to propagate
    information through gene-gene relationships. When a gene
    is masked, the FM's output captures what the network
    'expects' should change.

    Args:
        control_expression: Average control cell profile
        target_gene_idx: Which gene to knock out
        encoder_fn: Foundation model encoder
        prediction_head_fn: Learned prediction head

    Returns:
        Predicted log fold-change vector (G,)
    """
    # Step 1: Mask the target gene (simulate knockout)
    masked_expression = control_expression.copy()
    masked_expression[target_gene_idx] = 0.0

    # Step 2: Run through FM encoder to get gene embeddings
    gene_embeddings = encoder_fn(masked_expression)  # (G, d)

    # Step 3: Extract embedding at target position
    # The FM contextualizes this based on other genes
    target_embedding = gene_embeddings[target_gene_idx]  # (d,)

    # Step 4: Predict LFC from contextualized embedding
    predicted_lfc = prediction_head_fn(target_embedding)  # (G,)

    return predicted_lfc
```

#### Key Takeaways

- **Fine-tuning is a double-edged sword**: In-Silico KO for AIDO.Cell helps; other approaches hurt.
- **Overfitting is the main risk**: Perturbation datasets have ~2000 perturbations — tiny by deep learning standards.
- **Frozen embeddings are robust**: For most practical purposes, using fixed FM embeddings with simple predictors is the safest choice.

---

### Complex Translation Methods Don't Beat Simple Ones

#### Overview

Given a perturbation embedding, how should you translate it into a predicted expression change? The literature proposes sophisticated generative approaches — Latent Diffusion, Flow Matching, Schrödinger Bridge — that model the full distribution of perturbed single cells. The authors benchmarked simple implementations of each against kNN.

The result: **none of these advanced methods outperform kNN paired with the best embedding**. This is remarkable because the generative methods use the same embedding as input but are far more computationally expensive (~1000 GPU-hours each to train). Similarly, GEARS, a published GNN-based perturbation model, didn't beat the embedding+kNN approach.

The implication is clear: for predicting average perturbation effects, the bottleneck is the embedding quality, not the prediction model complexity.

#### Concept Diagram

<svg viewBox="0 0 700 380" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="fm-5-title">
  <title id="fm-5-title">Same Embedding, Different Prediction Methods</title>
  <defs>
    <marker id="arrow5" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#64748b"/></marker>
  </defs>
  <text x="350" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Same Embedding, Different Prediction Methods</text>
  <!-- Source embedding -->
  <rect x="250" y="48" width="200" height="55" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
  <text x="350" y="72" text-anchor="middle" font-weight="700" fill="#1e40af">Perturbation Embedding</text>
  <text x="350" y="90" text-anchor="middle" font-size="11" fill="#3b82f6">(e.g. WaveGC)</text>
  <!-- Branch lines -->
  <line x1="350" y1="103" x2="350" y2="130" stroke="#64748b" stroke-width="1.5"/>
  <line x1="90" y1="130" x2="610" y2="130" stroke="#64748b" stroke-width="1.5"/>
  <!-- kNN -->
  <line x1="90" y1="130" x2="90" y2="155" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow5)"/>
  <rect x="30" y="163" width="120" height="45" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="90" y="188" text-anchor="middle" font-weight="700" fill="#166534">kNN</text>
  <!-- Latent Diffusion -->
  <line x1="260" y1="130" x2="260" y2="155" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow5)"/>
  <rect x="190" y="163" width="140" height="45" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="260" y="188" text-anchor="middle" fill="#475569">Latent Diffusion</text>
  <!-- Flow Matching -->
  <line x1="430" y1="130" x2="430" y2="155" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow5)"/>
  <rect x="360" y="163" width="140" height="45" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="430" y="188" text-anchor="middle" fill="#475569">Flow Matching</text>
  <!-- Schrödinger Bridge -->
  <line x1="590" y1="130" x2="590" y2="155" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow5)"/>
  <rect x="510" y="163" width="160" height="45" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="590" y="188" text-anchor="middle" fill="#475569">Schrödinger Bridge</text>
  <!-- Results arrows -->
  <line x1="90" y1="208" x2="90" y2="245" stroke="#22c55e" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="260" y1="208" x2="260" y2="245" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow5)"/>
  <line x1="430" y1="208" x2="430" y2="245" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow5)"/>
  <line x1="590" y1="208" x2="590" y2="245" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow5)"/>
  <!-- Result boxes -->
  <rect x="40" y="252" width="100" height="50" rx="8" fill="#dcfce7" stroke="#22c55e" stroke-width="2"/>
  <text x="90" y="273" text-anchor="middle" font-weight="700" fill="#166534">~4.2 L2</text>
  <text x="90" y="292" text-anchor="middle" font-size="12" font-weight="700" fill="#16a34a">BEST!</text>
  <rect x="210" y="252" width="100" height="50" rx="8" fill="#fef2f2" stroke="#fca5a5" stroke-width="1.5"/>
  <text x="260" y="273" text-anchor="middle" fill="#991b1b">~4.3 L2</text>
  <text x="260" y="292" text-anchor="middle" font-size="11" fill="#dc2626">Worse</text>
  <rect x="380" y="252" width="100" height="50" rx="8" fill="#fef2f2" stroke="#fca5a5" stroke-width="1.5"/>
  <text x="430" y="273" text-anchor="middle" fill="#991b1b">~4.3 L2</text>
  <text x="430" y="292" text-anchor="middle" font-size="11" fill="#dc2626">Worse</text>
  <rect x="540" y="252" width="100" height="50" rx="8" fill="#fef2f2" stroke="#fca5a5" stroke-width="1.5"/>
  <text x="590" y="273" text-anchor="middle" fill="#991b1b">~4.3 L2</text>
  <text x="590" y="292" text-anchor="middle" font-size="11" fill="#dc2626">Worse</text>
  <!-- GPU hours row -->
  <text x="90" y="326" text-anchor="middle" font-size="11" fill="#22c55e" font-weight="600">~0 GPU-hrs</text>
  <text x="260" y="326" text-anchor="middle" font-size="11" fill="#dc2626">~1000 GPU-hrs</text>
  <text x="430" y="326" text-anchor="middle" font-size="11" fill="#dc2626">~1000 GPU-hrs</text>
  <text x="590" y="326" text-anchor="middle" font-size="11" fill="#dc2626">~1000 GPU-hrs</text>
  <!-- Bottom note -->
  <rect x="80" y="345" width="540" height="26" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
  <text x="350" y="363" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">The embedding quality is the bottleneck — not the prediction model complexity.</text>
</svg>

#### Key Takeaways

- **kNN wins**: Simple kNN regression with the right embedding beats expensive generative models.
- **Embedding quality is the bottleneck**: Improving the input representation matters more than improving the decoder.
- **Computational cost matters**: Generative models are orders of magnitude more expensive with no accuracy gain for average effect prediction.

---

### FMs Can Also Improve Small Molecule Predictions

#### Overview

Chemical perturbations present a harder prediction problem than genetic ones. A small molecule may hit multiple targets, the chemical space is enormous (~10^60 possible molecules), and we have less network knowledge for drugs.

The authors tested molecular fingerprints, SMILES-based FMs (ChemBERTa, Uni-Mol, MiniMol), target-based embeddings (embedding the drug's predicted protein target with a gene FM), and LLM-based text embeddings of drug descriptions.

In the LFC regression formulation, no embedding clearly outperformed baselines — the signal was weak. But in the DEG (differentially expressed gene) classification formulation, target-based embeddings worked best: if you know (or can predict) what protein a drug binds, embedding that protein with an scRNA-seq FM gives you useful information. Traditional molecular structure fingerprints (ECPF:2) were also competitive. Interestingly, SMILES-based FMs generally underperformed, likely because they were trained for chemical — not biological — property prediction.

#### Concept Diagram

<svg viewBox="0 0 700 420" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="fm-6-title">
  <title id="fm-6-title">Small Molecule Embedding Strategies</title>
  <defs>
    <marker id="arrow6" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#64748b"/></marker>
  </defs>
  <text x="350" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Small Molecule Embedding Strategies</text>
  <!-- Drug pill icon -->
  <rect x="20" y="55" width="120" height="50" rx="25" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
  <text x="80" y="85" text-anchor="middle" font-weight="700" fill="#1e40af">Drug</text>
  <!-- Branch lines -->
  <line x1="140" y1="80" x2="195" y2="80" stroke="#64748b" stroke-width="1.5"/>
  <line x1="195" y1="80" x2="195" y2="370" stroke="#64748b" stroke-width="1"/>
  <!-- Strategy 1: SMILES -->
  <line x1="195" y1="80" x2="240" y2="80" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <rect x="250" y="55" width="160" height="50" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="330" y="76" text-anchor="middle" font-weight="600" fill="#334155">SMILES String</text>
  <text x="330" y="94" text-anchor="middle" font-size="10" fill="#64748b">CC(=O)Oc1ccccc1...</text>
  <line x1="410" y1="80" x2="460" y2="80" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <rect x="470" y="58" width="130" height="44" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="535" y="78" text-anchor="middle" font-size="12" fill="#475569">ChemBERTa</text>
  <text x="535" y="94" text-anchor="middle" font-size="10" fill="#64748b">Uni-Mol, MiniMol</text>
  <rect x="610" y="62" width="72" height="28" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1"/>
  <text x="646" y="81" text-anchor="middle" font-size="11" font-weight="600" fill="#dc2626">weak</text>
  <!-- Strategy 2: Fingerprint -->
  <line x1="195" y1="160" x2="240" y2="160" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <rect x="250" y="135" width="160" height="50" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="330" y="156" text-anchor="middle" font-weight="600" fill="#334155">Molecular Structure</text>
  <text x="330" y="174" text-anchor="middle" font-size="10" fill="#64748b">Morgan Fingerprints</text>
  <line x1="410" y1="160" x2="460" y2="160" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <rect x="470" y="138" width="130" height="44" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="535" y="164" text-anchor="middle" font-size="12" fill="#475569">ECPF:2</text>
  <rect x="610" y="142" width="72" height="28" rx="6" fill="#fefce8" stroke="#eab308" stroke-width="1"/>
  <text x="646" y="161" text-anchor="middle" font-size="11" font-weight="600" fill="#ca8a04">decent</text>
  <!-- Strategy 3: Target -->
  <line x1="195" y1="250" x2="240" y2="250" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <rect x="250" y="222" width="160" height="56" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="330" y="244" text-anchor="middle" font-weight="700" fill="#166534">Protein Target</text>
  <text x="330" y="262" text-anchor="middle" font-size="10" fill="#16a34a">COX-1 / COX-2 etc.</text>
  <line x1="410" y1="250" x2="460" y2="250" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <rect x="470" y="228" width="130" height="44" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="535" y="248" text-anchor="middle" font-size="12" fill="#166534">scRNA FM</text>
  <text x="535" y="264" text-anchor="middle" font-size="10" fill="#16a34a">(AIDO.Cell)</text>
  <rect x="610" y="232" width="72" height="28" rx="6" fill="#dcfce7" stroke="#22c55e" stroke-width="1.5"/>
  <text x="646" y="251" text-anchor="middle" font-size="11" font-weight="700" fill="#16a34a">BEST</text>
  <!-- Strategy 4: Text -->
  <line x1="195" y1="340" x2="240" y2="340" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <rect x="250" y="315" width="160" height="50" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="330" y="336" text-anchor="middle" font-weight="600" fill="#334155">Text Description</text>
  <text x="330" y="354" text-anchor="middle" font-size="10" fill="#64748b">"NSAID, inhibits..."</text>
  <line x1="410" y1="340" x2="460" y2="340" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <rect x="470" y="318" width="130" height="44" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="535" y="344" text-anchor="middle" font-size="12" fill="#475569">LLM Embed</text>
  <rect x="610" y="322" width="72" height="28" rx="6" fill="#fefce8" stroke="#eab308" stroke-width="1"/>
  <text x="646" y="341" text-anchor="middle" font-size="11" font-weight="600" fill="#ca8a04">variable</text>
</svg>

#### Key Takeaways

- **Chemical perturbation is harder** than genetic perturbation: weaker signals across all methods.
- **Target-based embeddings work best**: Representing a drug by its protein target (embedded with a gene FM) outperforms direct molecular embeddings.
- **SMILES FMs underperform**: Models trained on chemical properties don't capture biological function well.
- **DEG formulation reveals signal** that LFC regression misses for chemical perturbations.

---

### Integrating Diverse FMs Further Improves Performance

#### Overview

Since different FM types capture different aspects of gene biology (sequence, structure, interactions, function), the authors hypothesized that combining them could be more powerful than any single embedding. They designed an attention-based fusion model that ingests embeddings from all sources and learns to weight them dynamically.

The results are impressive: fusion consistently beats the best unimodal embedding (WaveGC) on all four cell lines in Essential. For K562 and Jurkat, the fusion model actually matches the estimated experimental error limit — meaning **the model is as accurate as the experiment itself**. For the other two cell lines, it bridges 86% (Hep-G2) and 53% (hTERT-RPE1) of the gap between random performance and the experimental error bound.

However, fusion did not help for chemical perturbations, likely because individual drug embeddings were too weak to provide meaningful complementary information.

#### Concept Diagram

<svg viewBox="0 0 700 520" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="fm-7-title">
  <title id="fm-7-title">Attention-Based Embedding Fusion</title>
  <defs>
    <marker id="arrow7" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#64748b"/></marker>
    <marker id="arrow7p" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#a855f7"/></marker>
  </defs>
  <text x="350" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Attention-Based Embedding Fusion</text>
  <!-- Source embedding boxes -->
  <rect x="30" y="48" width="120" height="50" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="90" y="70" text-anchor="middle" font-weight="600" fill="#166534" font-size="12">WaveGC</text>
  <text x="90" y="86" text-anchor="middle" font-size="10" fill="#64748b">(d₁)</text>
  <rect x="175" y="48" width="120" height="50" rx="8" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="235" y="70" text-anchor="middle" font-weight="600" fill="#854d0e" font-size="12">scGPT</text>
  <text x="235" y="86" text-anchor="middle" font-size="10" fill="#64748b">(d₂)</text>
  <rect x="320" y="48" width="120" height="50" rx="8" fill="#fff1f2" stroke="#f97316" stroke-width="1.5"/>
  <text x="380" y="70" text-anchor="middle" font-weight="600" fill="#9a3412" font-size="12">ESM2</text>
  <text x="380" y="86" text-anchor="middle" font-size="10" fill="#64748b">(d₃)</text>
  <rect x="465" y="48" width="120" height="50" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="525" y="70" text-anchor="middle" font-weight="600" fill="#166534" font-size="12">GenePT</text>
  <text x="525" y="86" text-anchor="middle" font-size="10" fill="#64748b">(d₄)</text>
  <text x="620" y="76" text-anchor="middle" font-size="16" fill="#94a3b8">...</text>
  <!-- Projection arrows -->
  <line x1="90" y1="98" x2="90" y2="138" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow7)"/>
  <line x1="235" y1="98" x2="235" y2="138" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow7)"/>
  <line x1="380" y1="98" x2="380" y2="138" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow7)"/>
  <line x1="525" y1="98" x2="525" y2="138" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow7)"/>
  <!-- Projection boxes -->
  <rect x="40" y="146" width="100" height="35" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1"/>
  <text x="90" y="168" text-anchor="middle" font-size="11" fill="#475569">Project → d</text>
  <rect x="185" y="146" width="100" height="35" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1"/>
  <text x="235" y="168" text-anchor="middle" font-size="11" fill="#475569">Project → d</text>
  <rect x="330" y="146" width="100" height="35" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1"/>
  <text x="380" y="168" text-anchor="middle" font-size="11" fill="#475569">Project → d</text>
  <rect x="475" y="146" width="100" height="35" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1"/>
  <text x="525" y="168" text-anchor="middle" font-size="11" fill="#475569">Project → d</text>
  <!-- Merge line -->
  <line x1="90" y1="181" x2="90" y2="210" stroke="#64748b" stroke-width="1"/>
  <line x1="235" y1="181" x2="235" y2="210" stroke="#64748b" stroke-width="1"/>
  <line x1="380" y1="181" x2="380" y2="210" stroke="#64748b" stroke-width="1"/>
  <line x1="525" y1="181" x2="525" y2="210" stroke="#64748b" stroke-width="1"/>
  <line x1="90" y1="210" x2="525" y2="210" stroke="#64748b" stroke-width="1.5"/>
  <line x1="310" y1="210" x2="310" y2="232" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow7)"/>
  <!-- Cell line token addition -->
  <rect x="210" y="240" width="200" height="40" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5"/>
  <text x="310" y="264" text-anchor="middle" font-weight="600" fill="#6b21a8">+ Cell Line Token</text>
  <line x1="310" y1="280" x2="310" y2="310" stroke="#a855f7" stroke-width="2" marker-end="url(#arrow7p)"/>
  <!-- Transformer -->
  <rect x="170" y="318" width="280" height="55" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
  <text x="310" y="342" text-anchor="middle" font-weight="700" fill="#1e40af" font-size="14">Transformer Encoder</text>
  <text x="310" y="362" text-anchor="middle" font-size="11" fill="#3b82f6">Self-attention across embedding sources</text>
  <line x1="310" y1="373" x2="310" y2="403" stroke="#3b82f6" stroke-width="2" marker-end="url(#arrow7)"/>
  <!-- CLS output -->
  <rect x="210" y="410" width="200" height="40" rx="8" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="310" y="430" text-anchor="middle" font-size="12" fill="#854d0e">[CLS] → Prediction Head</text>
  <line x1="310" y1="450" x2="310" y2="478" stroke="#eab308" stroke-width="2" marker-end="url(#arrow7)"/>
  <!-- Output -->
  <rect x="210" y="484" width="200" height="30" rx="8" fill="#dcfce7" stroke="#22c55e" stroke-width="2"/>
  <text x="310" y="504" text-anchor="middle" font-weight="700" fill="#166534">Predicted LFC (G dims)</text>
</svg>

#### Implementation

```python
import numpy as np
from typing import List, Dict, Optional

class EmbeddingFusionModel:
    """
    Simplified attention-based fusion of multiple FM embeddings.
    
    Each perturbation is represented by J embeddings from different 
    FMs. A transformer learns to attend across these sources and 
    produce a unified prediction.
    """
    
    def __init__(self, embedding_dims: List[int], common_dim: int = 100,
                 n_heads: int = 5, n_genes: int = 1000):
        """
        Args:
            embedding_dims: Dimension of each source embedding
            common_dim: Shared projection dimension
            n_heads: Attention heads in transformer
            n_genes: Number of genes to predict
        """
        self.common_dim = common_dim
        self.n_sources = len(embedding_dims)
        
        # Per-source projection matrices: map each to common_dim
        self.projections = [
            np.random.randn(d, common_dim) * 0.1
            for d in embedding_dims
        ]
        
        # Learnable cell line embeddings
        self.cell_line_embeddings: Dict[str, np.ndarray] = {}
        
        # Prediction head weights (simplified)
        self.pred_weights = np.random.randn(common_dim, n_genes) * 0.01
    
    def project_embeddings(
        self, 
        embeddings: List[Optional[np.ndarray]]
    ) -> np.ndarray:
        """
        Project each source embedding to the common space.
        Handles missing embeddings (not all sources cover all genes).
        
        Returns:
            tokens: (n_valid + 1, common_dim) including CLS token
        """
        tokens = []
        
        # CLS token for aggregation
        cls_token = np.zeros(self.common_dim)
        tokens.append(cls_token)
        
        # Project each available embedding
        for i, emb in enumerate(embeddings):
            if emb is not None:
                projected = emb @ self.projections[i]
                tokens.append(projected)
        
        return np.array(tokens)  # (n_tokens, common_dim)
    
    def predict(
        self, 
        embeddings: List[Optional[np.ndarray]],
        cell_line: str
    ) -> np.ndarray:
        """
        Predict LFC by fusing all available embeddings.
        
        Returns:
            predicted_lfc: (n_genes,) vector
        """
        # Step 1: Project to common space + add cell line embedding
        tokens = self.project_embeddings(embeddings)
        if cell_line in self.cell_line_embeddings:
            tokens += self.cell_line_embeddings[cell_line]
        
        # Step 2: Self-attention (simplified as mean for illustration)
        # In practice: multi-head self-attention transformer layers
        cls_output = tokens.mean(axis=0)  # (common_dim,)
        
        # Step 3: Predict LFC from CLS output
        predicted_lfc = cls_output @ self.pred_weights  # (n_genes,)
        
        return predicted_lfc
```

#### Key Takeaways

- **Fusion always beats the best single embedding** for genetic perturbations on Essential.
- **Two cell lines hit the experimental error ceiling**: K562 and Jurkat predictions are as good as replicate experiments.
- **Attention-based integration** learns to weight different modalities dynamically, outperforming simple concatenation.
- **Fusion doesn't help for drugs**: Individual chemical embeddings are too weak to provide complementary signal.

---

## Methods

### Log Fold-Change Regression Formulation

#### Overview

The paper frames perturbation prediction as a regression problem: given a perturbation (gene knockout or drug treatment), predict the vector of per-gene expression changes. Specifically, they predict the "batch-aware average treatment effect" (BA-ATE), which they call log fold-change (LFC) for simplicity.

The key idea is to compare the average expression of perturbed cells to the average expression of control cells, accounting for batch effects by weighting each batch equally. For datasets with large batches, per-batch control means are subtracted. For datasets with small batches (like Essential), a global control mean is used instead to avoid noisy per-batch estimates.

The primary evaluation metric is the L2 error between predicted and observed LFC vectors, averaged across all test perturbations.

#### Concept Diagram

<svg viewBox="0 0 700 340" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="fm-8-title">
  <title id="fm-8-title">Computing Log Fold-Change (LFC)</title>
  <defs>
    <marker id="arrow8" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#64748b"/></marker>
  </defs>
  <text x="350" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Computing Log Fold-Change (LFC)</text>
  <!-- Batch 1 -->
  <rect x="30" y="52" width="260" height="90" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="160" y="74" text-anchor="middle" font-weight="700" fill="#1e40af">Batch 1</text>
  <text x="105" y="98" text-anchor="middle" font-size="12" fill="#334155">Control cells: x̄₁</text>
  <text x="105" y="118" text-anchor="middle" font-size="12" fill="#334155">Perturbed:     x̄'₁</text>
  <!-- Batch 2 -->
  <rect x="410" y="52" width="260" height="90" rx="10" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5"/>
  <text x="540" y="74" text-anchor="middle" font-weight="700" fill="#6b21a8">Batch 2</text>
  <text x="490" y="98" text-anchor="middle" font-size="12" fill="#334155">Control cells: x̄₂</text>
  <text x="490" y="118" text-anchor="middle" font-size="12" fill="#334155">Perturbed:     x̄'₂</text>
  <!-- Arrows down -->
  <line x1="160" y1="142" x2="160" y2="178" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arrow8)"/>
  <line x1="540" y1="142" x2="540" y2="178" stroke="#a855f7" stroke-width="1.5" marker-end="url(#arrow8)"/>
  <!-- Per-batch delta -->
  <rect x="80" y="185" width="160" height="35" rx="8" fill="#dbeafe" stroke="#3b82f6" stroke-width="1"/>
  <text x="160" y="207" text-anchor="middle" font-size="12" fill="#1e40af">δ₁ = x̄'₁ − x̄₁</text>
  <rect x="460" y="185" width="160" height="35" rx="8" fill="#ede9fe" stroke="#a855f7" stroke-width="1"/>
  <text x="540" y="207" text-anchor="middle" font-size="12" fill="#6b21a8">δ₂ = x̄'₂ − x̄₂</text>
  <!-- Merge -->
  <line x1="160" y1="220" x2="160" y2="245" stroke="#64748b" stroke-width="1"/>
  <line x1="540" y1="220" x2="540" y2="245" stroke="#64748b" stroke-width="1"/>
  <line x1="160" y1="245" x2="540" y2="245" stroke="#64748b" stroke-width="1.5"/>
  <line x1="350" y1="245" x2="350" y2="268" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow8)"/>
  <!-- LFC result -->
  <rect x="220" y="275" width="260" height="45" rx="10" fill="#dcfce7" stroke="#22c55e" stroke-width="2"/>
  <text x="350" y="296" text-anchor="middle" font-weight="700" fill="#166534">LFC = mean(δ₁, δ₂)</text>
  <text x="350" y="312" text-anchor="middle" font-size="11" fill="#16a34a">∆ₖ ∈ ℝᴳ  (one value per gene)</text>
  <!-- Metric -->
  <text x="350" y="340" text-anchor="middle" font-size="12" fill="#475569">Evaluation:  L2 = (1/K) Σₖ ‖∆ₖ − ∆̂ₖ‖₂</text>
</svg>

#### Implementation

```python
import numpy as np
from typing import Dict, List

def compute_batch_aware_ate(
    expression_matrix: np.ndarray,       # (N, G) normalized expression
    cell_labels: np.ndarray,             # (N,) perturbation ID or 'ctrl'
    batch_labels: np.ndarray,            # (N,) batch assignment
    perturbation_id: str,
    use_global_control: bool = False     # True for small-batch datasets
) -> np.ndarray:
    """
    Compute Batch-Aware Average Treatment Effect (BA-ATE).

    For large batches: per-batch control subtraction
    For small batches: global control subtraction (more stable)

    Args:
        expression_matrix: log1p-normalized scRNA-seq data
        cell_labels: Which perturbation each cell received
        batch_labels: Batch assignment for each cell
        perturbation_id: Target perturbation to compute ATE for
        use_global_control: Use global vs per-batch control mean

    Returns:
        lfc: (G,) vector of per-gene treatment effects
    """
    ctrl_mask = cell_labels == 'ctrl'
    pert_mask = cell_labels == perturbation_id
    G = expression_matrix.shape[1]

    if use_global_control:
        # Small-batch mode: compute global control mean
        batches = np.unique(batch_labels)
        global_ctrl = np.mean([
            expression_matrix[ctrl_mask & (batch_labels == b)].mean(axis=0)
            for b in batches
            if np.any(ctrl_mask & (batch_labels == b))
        ], axis=0)

    # Find batches containing both control and perturbed cells
    valid_batches = []
    for b in np.unique(batch_labels):
        has_ctrl = np.any(ctrl_mask & (batch_labels == b))
        has_pert = np.any(pert_mask & (batch_labels == b))
        if has_ctrl and has_pert:
            valid_batches.append(b)

    # Average treatment effect across batches
    batch_effects = []
    for b in valid_batches:
        pert_mean = expression_matrix[pert_mask & (batch_labels == b)].mean(axis=0)
        if use_global_control:
            batch_effects.append(pert_mean - global_ctrl)
        else:
            ctrl_mean = expression_matrix[ctrl_mask & (batch_labels == b)].mean(axis=0)
            batch_effects.append(pert_mean - ctrl_mean)

    return np.mean(batch_effects, axis=0)  # (G,)
```

#### Key Takeaways

- **BA-ATE** accounts for batch effects by averaging per-batch deltas, preventing confounding.
- **Two variants** handle datasets with different batch sizes: per-batch control for large batches, global control for small ones.
- **L2 error** is the primary metric, though the paper also considers MAE, MSE, and correlation metrics.

---

### Differentially Expressed Gene (DEG) Classification

#### Overview

An alternative to predicting exact expression changes is to classify each gene as upregulated (+1), downregulated (−1), or unchanged (0). This is the DEG formulation. For large-batch datasets, a Student's t-test with Benjamini-Hochberg correction is run per batch, then majority-voted. For small-batch datasets, all cells are pooled. The metric is macro F1 score.

This formulation is particularly useful for chemical perturbations where the continuous LFC signal is weak but discrete changes can still be detected.

#### Key Takeaways

- **DEG classification** captures perturbation effects that LFC regression may miss, especially for drugs.
- **Majority voting across batches** ensures robust classification.
- **Macro F1** accounts for class imbalance (most genes are unchanged).

---

### Datasets

#### Overview

Four datasets span different perturbation types, cell lines, and scales:

<svg viewBox="0 0 700 220" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="fm-9-title">
  <title id="fm-9-title">Perturbation datasets compared by type, scale, and cell coverage</title>
  <!-- Header row -->
  <rect x="20" y="10" width="660" height="36" rx="6" fill="#1e293b"/>
  <text x="95" y="33" text-anchor="middle" font-weight="700" fill="white">Dataset</text>
  <text x="230" y="33" text-anchor="middle" font-weight="700" fill="white">Type</text>
  <text x="365" y="33" text-anchor="middle" font-weight="700" fill="white">Cell Lines</text>
  <text x="490" y="33" text-anchor="middle" font-weight="700" fill="white">Perturbations</text>
  <text x="620" y="33" text-anchor="middle" font-weight="700" fill="white">Cells</text>
  <!-- Row 1 -->
  <rect x="20" y="48" width="660" height="36" rx="0" fill="#f8fafc"/>
  <text x="95" y="71" text-anchor="middle" fill="#334155" font-weight="600">Norman</text>
  <text x="230" y="71" text-anchor="middle" fill="#64748b">CRISPRa</text>
  <text x="365" y="71" text-anchor="middle" fill="#64748b">1 (K562)</text>
  <text x="490" y="71" text-anchor="middle" fill="#64748b">105 single</text>
  <text x="620" y="71" text-anchor="middle" fill="#64748b">~100K</text>
  <!-- Row 2 (highlighted) -->
  <rect x="20" y="86" width="660" height="36" rx="0" fill="#eff6ff" stroke="#3b82f6" stroke-width="1"/>
  <text x="95" y="109" text-anchor="middle" fill="#1e40af" font-weight="700">Essential</text>
  <text x="230" y="109" text-anchor="middle" fill="#1e40af">CRISPRkd</text>
  <text x="365" y="109" text-anchor="middle" fill="#1e40af">4</text>
  <text x="490" y="109" text-anchor="middle" fill="#1e40af">~2000/line</text>
  <text x="620" y="109" text-anchor="middle" fill="#1e40af">~964K</text>
  <!-- Row 3 -->
  <rect x="20" y="124" width="660" height="36" rx="0" fill="#f8fafc"/>
  <text x="95" y="147" text-anchor="middle" fill="#334155" font-weight="600">Sciplex-3</text>
  <text x="230" y="147" text-anchor="middle" fill="#64748b">Chemical</text>
  <text x="365" y="147" text-anchor="middle" fill="#64748b">3</text>
  <text x="490" y="147" text-anchor="middle" fill="#64748b">188 drugs</text>
  <text x="620" y="147" text-anchor="middle" fill="#64748b">~800K</text>
  <!-- Row 4 -->
  <rect x="20" y="162" width="660" height="36" rx="0" fill="#f8fafc"/>
  <text x="95" y="185" text-anchor="middle" fill="#334155" font-weight="600">Tahoe-100M</text>
  <text x="230" y="185" text-anchor="middle" fill="#64748b">Chemical</text>
  <text x="365" y="185" text-anchor="middle" fill="#64748b">50</text>
  <text x="490" y="185" text-anchor="middle" fill="#64748b">379 drugs</text>
  <text x="620" y="185" text-anchor="middle" fill="#64748b">~100M</text>
  <!-- Note -->
  <text x="350" y="215" text-anchor="middle" font-size="11" fill="#3b82f6" font-style="italic">Essential (highlighted) is the primary benchmark for genetic perturbation evaluation</text>
</svg>

Essential is the primary benchmark for genetic perturbations because it has enough perturbations (~2000 per cell line) to reliably distinguish embedding quality. Norman is included for comparison with prior work, but its small size masks performance differences. Tahoe is the largest chemical perturbation dataset, enabling more robust evaluation of drug embeddings.

#### Key Takeaways

- **Dataset size matters**: Small datasets (Norman) don't distinguish FMs from baselines; larger ones (Essential) do.
- **Essential** is the key genetic perturbation benchmark: 4 cell lines × ~2000 perturbations each.
- **Tahoe-100M** is the largest single-cell chemical perturbation dataset (~100M cells, 379 drugs, 50 cell lines).

---

### Embedding Sources

#### Overview

The paper evaluates embeddings from four modalities for genetic perturbation prediction: expression (scRNA-seq FMs), DNA sequence, protein sequence/structure, and prior knowledge (interaction networks, annotations, text). For chemical perturbations, additional sources include molecular fingerprints, SMILES-based FMs, target-based embeddings, and text embeddings from LLMs.

A key methodological contribution is the systematic evaluation across all these sources using a unified framework (same datasets, metrics, cross-validation splits).

#### Key Takeaways

- **Expression FMs**: AIDO.Cell, scGPT, scPRINT, Geneformer, TranscriptFormer — contextualized on control cells.
- **Interactome FMs**: WaveGC, STRING GNN, STRING Spectral — trained on protein-protein interaction networks.
- **GenePT**: Embeds textual gene descriptions with GPT-3.5 — a "soft" form of interactome knowledge.
- **Chemical embeddings**: Morgan fingerprints, ChemBERTa, Uni-Mol, and target-based approaches using gene FMs.

---

### Fusion Architecture

#### Overview

The fusion model uses a transformer encoder to integrate variable numbers of embeddings per perturbation. Each embedding is projected to a common 100-dimensional space, a learnable cell line token is added, and a CLS token aggregates information through self-attention. The CLS output feeds into a prediction head that outputs the LFC vector.

A key design choice is handling missing embeddings — not every FM produces an embedding for every gene. The attention mechanism naturally handles this by operating on variable-length input sets. Training uses L2 loss with Optuna hyperparameter tuning (100 trials), and the model is trained jointly across cell lines.

#### Key Takeaways

- **Transformer-based attention** enables flexible integration of variable numbers of embeddings.
- **Cell line tokens** allow the same model to predict across different cell types.
- **100 Optuna trials** for hyperparameter tuning; same hyperparameters used across all CV folds.
- **Full fusion model** (more complex architecture) outperforms simple fusion on Essential.

---

## Discussion

### Overview

The authors conclude that foundation models **do** improve perturbation prediction — but only when you choose the right ones. The key findings paint a nuanced picture:

For genetic perturbations, interactome-based embeddings are the single most valuable information source. This has practical implications: organizations building "virtual cell" models should invest in **interaction data across contexts** (cell types, diseases, developmental stages), potentially even more than in additional single-cell expression data. Fusion of multiple FM types pushes performance to the experimental noise floor.

For chemical perturbations, the picture is harder. Genetic perturbations are specific (one gene → one knockout), while drugs can hit multiple targets through complex pharmacology. The search space is vastly larger (~10^60 molecules vs ~20K genes), and we have much less interaction network data for small molecules. Off-the-shelf SMILES-based FMs perform poorly because they were trained to predict chemical, not biological, properties. The field needs a **biological function-aware molecular FM**.

Fine-tuning remains a challenge due to limited perturbation data. The authors suggest that jointly fine-tuning multiple FMs within a fusion framework could help, but overfitting risk is high without more training data.

### Concept Diagram

<svg viewBox="0 0 700 380" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="fm-10-title">
  <title id="fm-10-title">Summary: What Works and What Doesn't</title>
  <text x="350" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Summary: What Works and What Doesn't</text>
  <!-- Column headers -->
  <rect x="30" y="42" width="200" height="30" rx="6" fill="#1e293b"/>
  <text x="130" y="62" text-anchor="middle" font-weight="700" fill="white" font-size="12">Approach</text>
  <rect x="240" y="42" width="200" height="30" rx="6" fill="#166534"/>
  <text x="340" y="62" text-anchor="middle" font-weight="700" fill="white" font-size="12">Genetic Perturbations</text>
  <rect x="450" y="42" width="220" height="30" rx="6" fill="#92400e"/>
  <text x="560" y="62" text-anchor="middle" font-weight="700" fill="white" font-size="12">Chemical Perturbations</text>
  <!-- Row 1: Single FM -->
  <rect x="30" y="78" width="200" height="32" rx="4" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
  <text x="130" y="99" text-anchor="middle" fill="#334155" font-weight="600">Single FM</text>
  <rect x="240" y="78" width="200" height="32" rx="4" fill="#dcfce7" stroke="#86efac" stroke-width="1"/>
  <text x="340" y="99" text-anchor="middle" fill="#166534">★★★ interactome</text>
  <rect x="450" y="78" width="220" height="32" rx="4" fill="#fefce8" stroke="#fde047" stroke-width="1"/>
  <text x="560" y="99" text-anchor="middle" fill="#854d0e">★★ target-based</text>
  <!-- Row 2: Fusion -->
  <rect x="30" y="116" width="200" height="32" rx="4" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
  <text x="130" y="137" text-anchor="middle" fill="#334155" font-weight="600">FM Fusion</text>
  <rect x="240" y="116" width="200" height="32" rx="4" fill="#bbf7d0" stroke="#4ade80" stroke-width="1.5"/>
  <text x="340" y="137" text-anchor="middle" fill="#166534" font-weight="700">★★★★★</text>
  <rect x="450" y="116" width="220" height="32" rx="4" fill="#fef2f2" stroke="#fca5a5" stroke-width="1"/>
  <text x="560" y="137" text-anchor="middle" fill="#991b1b">★ no gain</text>
  <!-- Row 3: Fine-tuning -->
  <rect x="30" y="154" width="200" height="32" rx="4" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
  <text x="130" y="175" text-anchor="middle" fill="#334155" font-weight="600">Fine-tuning</text>
  <rect x="240" y="154" width="200" height="32" rx="4" fill="#dcfce7" stroke="#86efac" stroke-width="1"/>
  <text x="340" y="175" text-anchor="middle" fill="#166534">★★★ risky</text>
  <rect x="450" y="154" width="220" height="32" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
  <text x="560" y="175" text-anchor="middle" fill="#64748b">Not tested</text>
  <!-- Row 4: Complex decoders -->
  <rect x="30" y="192" width="200" height="32" rx="4" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
  <text x="130" y="213" text-anchor="middle" fill="#334155" font-weight="600">Complex decoders</text>
  <rect x="240" y="192" width="200" height="32" rx="4" fill="#fefce8" stroke="#fde047" stroke-width="1"/>
  <text x="340" y="213" text-anchor="middle" fill="#854d0e">★★ no gain</text>
  <rect x="450" y="192" width="220" height="32" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
  <text x="560" y="213" text-anchor="middle" fill="#64748b">Not tested</text>
  <!-- Key bottlenecks -->
  <text x="350" y="260" text-anchor="middle" font-size="14" font-weight="700" fill="#1e293b">Key Bottlenecks</text>
  <rect x="30" y="274" width="310" height="90" rx="10" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="185" y="298" text-anchor="middle" font-weight="700" fill="#166534" font-size="13">Genetic</text>
  <text x="185" y="318" text-anchor="middle" font-size="12" fill="#334155">Nearly solved for some cell lines!</text>
  <text x="185" y="338" text-anchor="middle" font-size="12" fill="#334155">Need harder benchmarks.</text>
  <rect x="360" y="274" width="310" height="90" rx="10" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="515" y="298" text-anchor="middle" font-weight="700" fill="#991b1b" font-size="13">Chemical</text>
  <text x="515" y="318" text-anchor="middle" font-size="12" fill="#334155">Need biology-aware molecular FMs.</text>
  <text x="515" y="338" text-anchor="middle" font-size="12" fill="#334155">Multi-target effects are hard.</text>
  <text x="515" y="355" text-anchor="middle" font-size="12" fill="#334155">Limited network data for drugs.</text>
</svg>

### Key Takeaways

- **Interactome data is king** for genetic perturbation prediction — invest in interaction networks.
- **Chemical perturbation prediction** remains an open challenge; current molecular FMs lack biological grounding.
- **Fusion reaches experimental limits** for some genetic perturbation settings, suggesting the need for harder benchmarks.
- **The field needs more perturbation data** to unlock the potential of fine-tuning and joint training.
- **Simple prediction methods suffice** — the embedding quality is the bottleneck, not model complexity.

---

## Key Takeaways Summary

### The Big Picture

1. **Foundation models DO improve perturbation prediction** — but only certain types. Interactome-based FMs (WaveGC, GenePT, GenotypeVAE) significantly outperform baselines, while DNA and protein sequence FMs add little value for this task.

2. **Embedding quality > model complexity**: kNN with the right embedding beats Latent Diffusion, Flow Matching, Schrödinger Bridge, and GEARS — all at a fraction of the compute cost.

3. **Multi-modal fusion reaches experimental limits**: Combining embeddings from diverse FMs via attention-based fusion matches the noise floor in 2 of 4 cell lines tested.

4. **Chemical perturbations remain hard**: Drug response prediction is fundamentally more difficult due to multi-target effects and the lack of biology-aware molecular FMs.

5. **Data and benchmarks need to scale up**: Small datasets mask real differences between methods; larger benchmarks like Essential reveal robust trends. The field needs both more perturbation data and harder evaluation splits.

---

## References

Original paper: Cole, E. et al. (2026). "Foundation Models Improve Perturbation Response Prediction." bioRxiv. DOI: 10.64898/2026.02.18.706454

Code and Data: https://github.com/genbio-ai/foundation-models-perturbation

## About This Analysis

This analysis was generated to make complex academic concepts more accessible. For complete technical details, mathematical formulations, supplementary figures, and all 600+ model results, please refer to the original paper.