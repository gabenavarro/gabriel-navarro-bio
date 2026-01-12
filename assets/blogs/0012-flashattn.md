@{id = "1badff63-f31f-40c3-b508-d1381bcd9f47"
  title = "FlashAttention: Accelerating Deep Learning with Docker"
  date = "2025-05-11T00:00:00Z"
  tags = ['machine learning', 'deep-learning', 'flashattention']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/flashattn-thumb.svg"
  description = "A concise, step-by-step demo of how to containerize FlashAttention and train a simple autoregressive Transformer on minimally preprocessed Bitcoin minute-by-minute data."
  type = "note"
  disabled = "false"
}
# Accelerating Deep Learning with FlashAttention and Docker

*By Gabriel Navarro*

---

## Introduction

Transformer models and the FlashAttention kernel have revolutionized natural-language processing by making self-attention faster and more memory-efficient. In this quick study, we treat minute-by-minute Bitcoin market data as if it were a “language”—each price/volume snapshot is like a token—and build a small autoregressive Transformer that learns to predict the next step.

Because this is a proof-of-concept on a small, minimally featurized dataset, we skip more advanced techniques—such as learned embeddings of engineered technical indicators, multi-scale tokenization (e.g. grouping minutes into hours), or external data fusion (order-book depth, sentiment)—that could further boost forecasting accuracy. For the sake of clarity and simplicity, we’ll leave those extensions for another deep dive and focus here purely on demonstrating how FlashAttention can power an autoregressive Transformer on raw market data.

We’ll cover:
1. **Containerizing FlashAttention** with Docker
2. **Processing raw BTC–USD data** into z-scored, autoregressive sequences
3. **Defining a lightweight Transformer** using the FlashAttention MHA operator
4. **Training & evaluating** with PyTorch Lightning
5. **Inspecting performance** via loss curves, test metrics, and prediction plots
6. **Conclusions & next steps** for improving the model

---

## 1. FlashAttention in Docker

Rather than wrestling with CUDA builds on your host machine, we package FlashAttention in a dedicated Docker image:

```bash
# 1. Clone the MLContainerLab repo
git clone https://github.com/gabenavarro/MLContainerLab.git
cd MLContainerLab

# 2. Build FlashAttention image (CUDA 12.8, Python 3.12)
docker build -f ./assets/build/Dockerfile.flashattn.cu128py26cp312 \
             -t flash-attention:cu128-py312 .

# 3. Run container with GPUs & mount code
docker run -dt --gpus all \
      -v "$(pwd):/workspace" \
      --name flash-attn-dev \
      flash-attention:cu128-py312

# 4. Attach VSCode to container
code --folder-uri vscode-remote://dev-container+flash-attn-dev/workspace
````

This setup ensures you can iterate on CPU/GPU code, experiment with FlashAttention, and easily extend to cloud environments later.

---

## 2. Data Preparation

We download a minute-resolution Bitcoin CSV from Kaggle, then:

1. **Log-transform** price columns to tame exponential growth
2. **Log₁ₚₗᵤₛ**-transform volume to reduce skew
3. **Z-score** each feature (mean 0, std 1)
4. **Window** into autoregressive sequences of length 2048

```python
import pandas as pd, numpy as np

df = pd.read_csv("btc_usd_1-min.csv").sort_values("Timestamp")
for col in ["Open","High","Low","Close"]:
    df[col] = np.log(df[col].clip(lower=0.01))
df["Volume"] = np.log1p(df["Volume"].clip(lower=0))

# Z-score normalization per feature
stats = {}
for feat in ["Open","High","Low","Close","Volume"]:
    μ, σ = df[feat].mean(), df[feat].std() or 1.0
    stats[feat] = (μ, σ)
    df[feat] = (df[feat] - μ) / σ
```

We then slide a 2 048-step window across the timeline (25% overlap), filter out any NaNs, and materialize the dataset with `litdata.optimize`.

---

## 3. Model Architecture

We build an **autoregressive Transformer**:

* **Input projection**: Maps five features to a 64-dim embedding
* **4× Transformer layers** with:

  * **FlashAttention MHA** for O( N · d ) memory
  * **RMSNorm** and FusedMLP blocks
* **Output projection**: Predicts the next step’s five features
* **Smooth L₁ loss** (Huber) with per-feature weighting (volume down-weighted)

```python
from flash_attn.modules.mha import MHA
from flash_attn.ops.rms_norm import RMSNorm
import torch.nn as nn

class TransformerLayer(nn.Module):
    def __init__(self, dim, heads):
        super().__init__()
        self.attn = MHA(dim, heads, causal=True, use_flash_attn=True)
        self.norm1 = RMSNorm(dim)
        self.mlp   = nn.Sequential(nn.Linear(dim, 4*dim), nn.GELU(), nn.Linear(4*dim, dim))
        self.norm2 = RMSNorm(dim)
    def forward(self, x):
        x = x + self.attn(self.norm1(x))
        x = x + self.mlp(self.norm2(x))
        return x

class BTCTransformer(nn.Module):
    def __init__(self):
        super().__init__()
        self.in_proj  = nn.Linear(5, 64)
        self.layers   = nn.ModuleList([TransformerLayer(64,8) for _ in range(4)])
        self.out_proj = nn.Linear(64, 5)
    def forward(self, x):
        x = self.in_proj(x)
        for l in self.layers: x = l(x)
        return self.out_proj(x)
```

This slim model fits in memory even with long (2 048) sequences, thanks to FlashAttention’s kernel fusion.

---

## 4. Training with Lightning

We wrap our model in a `pl.LightningModule` to handle:

* **Autoregressive loss** (shifted prediction)
* **AdamW + ReduceLROnPlateau**
* **Gradient clipping** & **mixed-precision (bf16)**
* **Early stopping** & **best-model checkpointing**

```python
trainer = pl.Trainer(
    max_epochs=10,
    accelerator="gpu", devices=1,
    precision="bf16-mixed",
    gradient_clip_val=0.5,
    callbacks=[EarlyStopping("val_loss", patience=5),
               ModelCheckpoint(monitor="val_loss")]
)
trainer.fit(model, train_loader, val_loader)
```

### Loss Curves

<p align="center">
  <img src="https://storage.googleapis.com/gn-portfolio/images/0012-flash-attn/flash_attn_tensorBoard_scalars.svg" max-width="700">
</p>

> **Insight:** Training loss (blue) drops rapidly, and validation loss (orange) follows—no signs of severe overfitting.

---

## 5. Evaluation & Results

After loading the best checkpoint, we run `trainer.test()` and compute:

| Metric       |   Value |
| ------------ | ------: |
| **Avg MSE**  |  0.2545 |
| **Avg RMSE** |  0.2472 |
| **Avg MAE**  |  0.1724 |
| **Avg MAPE** | 80.82 % |
| **Avg R²**   |  0.8242 |

* **Prices** (Open/High/Low/Close) achieve R² ≈ 0.99
* **Volume** is far noisier (R² ≈ 0.17), reflecting extreme spikes

### Prediction Examples

<p align="center">
  <img src="https://storage.googleapis.com/gn-portfolio/images/0012-flash-attn/flash_attn_all_features_predictions.svg" max-width="700">
</p>

> Notice that the model captures smooth price trends but underestimates sudden volume surges.

---

## 6. Conclusions & Next Steps

* **FlashAttention** makes long-sequence Transformers practical on a single GPU
* Treating financial time series “like language” yields strong predictive performance on prices
* Volume remains challenging—future work could explore:

  * Adaptive weighting or specialized volume heads
  * Incorporating external signals (order-book depth, sentiment)
  * Hierarchical time scales (minutes → hours → days)

By combining Docker-ized FlashAttention with PyTorch Lightning and streaming datasets, this proof of concept lays the groundwork for **scalable, production-ready** forecasting models in quantitative finance.

---

**Ready to try it yourself?**
The full notebook and Docker setup are on GitHub:
🔗 [https://github.com/gabenavarro/MLContainerLab/tree/main/examples/flash-attn-example](https://github.com/gabenavarro/MLContainerLab/blob/main/documentation/flash-attn.ipynb)

Feel free to fork, experiment with hyperparameters, or plug in your favorite time series!
