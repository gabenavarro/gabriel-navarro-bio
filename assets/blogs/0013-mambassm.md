@{id = "28b30727-8521-4637-acfc-4c48747e2fe2"
  title = "Forecasting Bitcoin with Mamba State Space Models"
  date = "2025-05-17T00:00:00Z"
  tags = ['machine learning', 'deep-learning', 'state-space-models']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/mamba-statespace-thumb.svg"
  description = "An intuitive guide to forecasting minute-by-minute Bitcoin OHLCV data using the fast, memory-efficient Mamba State Space Model—from Docker setup and minimal preprocessing to PyTorch Lightning training and comparison against Transformer baselines."
  type = "note"
  disabled = false
}

<p align="center">
  <img src="https://storage.googleapis.com/gn-portfolio/images/mamba-statespace-thumb.svg" max-width="700">
</p>


# Forecasting Bitcoin with Mamba State Space Models

*By Gabriel Navarro*<br/>
May 17, 2025

---

This post demonstrates how to forecast minute-by-minute Bitcoin OHLCV data using the **Mamba State Space Model (SSM)**—a linear-time, hardware-aware sequence model that rivals Transformers on long contexts. We’ll:

* **Build intuition** for state-space forecasting and why it excels on noisy financial series
* **Set up** your environment with `mamba-ssm` and key dependencies
* **Ingest & preprocess** Bitcoin data: log-scaling, z-scoring, and windowing
* **Define** a stacked Mamba2 architecture for autoregression
* **Train** with PyTorch Lightning: mixed-precision, gradient clipping, and scheduler tricks
* **Evaluate** via regression metrics and compare against a FlashAttention baseline

By the end, you’ll understand not just *how* to implement Mamba SSM, but *why* it works—and where to go next.

---

## 1. Why State-Space Models for Finance?

Traditional time-series methods (ARIMA, exponential smoothing) excel at short-range forecasts under stationarity, but struggle with latent dynamics and non-stationarity common in finance ([Medium][1]).

**State-space models** (SSMs) introduce hidden “state” vectors that evolve via linear or nonlinear dynamics, while observations are noisy functions of those states ([mfe.baruch.cuny.edu][2]). This separation of signal vs. noise yields:

* **Adaptive memory**: long-range dependencies learned without quadratic attention costs
* **Robustness**: explicit modeling of process & measurement noise
* **Interpretability**: clear transition vs. observation equations

SSMs have powered Kalman filters in control, robotics, and economics since the 1960s—yet only recently have they matched Transformers on raw sequence tasks ([arXiv][3]).

---

## 2. Introducing Mamba SSM

**Mamba** is a next-generation SSM that combines selective state updates with hardware-aware kernels, achieving linear time and memory complexity while retaining strong performance on language, audio, and genomic data ([arXiv][4]).

Key innovations:

1. **Selective state propagation**
2. **Control-theory inspired dynamics**
3. **Kernel fusion** akin to FlashAttention for GPU efficiency ([The Gradient][5])

Empirically, Mamba rivals or outperforms Transformers with 5× higher throughput at 2K–16K contexts ([Goomba Lab][6]) and exhibits Lyapunov stability under mixed precision ([arXiv][7]).

---

## 3. Installation & Setup

We recommend **Mamba** (fast Conda) to isolate dependencies:

```bash
# Install mamba in base
conda install -n base -c conda-forge mamba   # :contentReference[oaicite:7]{index=7}

# Create env & install PyTorch, Lightning, etc.
mamba create -n mamba-ssm python=3.10
conda activate mamba-ssm
mamba install pytorch lightning numpy pandas matplotlib \
             -c pytorch -c conda-forge
pip install mamba-ssm litdata kaggle
```

Verify your NVIDIA drivers + CUDA match your PyTorch build to leverage Mamba’s Triton kernels. See our MLContainer Lab for a full Dockerfile with FlashAttention, Triton, and Mamba ([MLContainer Lab][10]).

---

## 4. Data Sourcing & Preprocessing

We use the **mczielinski/bitcoin-historical-data** Kaggle dataset (1-min OHLCV) spanning multiple years, ideal for long-context models. Download via the Kaggle API:

```bash
kaggle datasets download mczielinski/bitcoin-historical-data \
  -f btcusd_1-min_data.csv -p ./datasets/   # requires Kaggle credentials
```

### Preprocessing Steps

1. **Log-transform prices** to stabilize variance
2. **Log₁ₚₗᵤₛ transform volume** to reduce skew
3. **Z-score** each feature:

   $$
     x' = \frac{x - \mu}{\sigma}
   $$
4. **Windowing** into 2 048-step sequences (75 % overlap)
5. **Mask** any window containing NaNs

We then stream and serialize with `litdata.optimize()`, producing \~100 k valid windows for training ([Medium][1]).

---

## 5. Model Architecture

```python
class Mamba2Model(pl.LightningModule):
    def __init__(…):
        super().__init__()
        self.in_proj = nn.Linear(5, 64)
        self.layers  = nn.ModuleList([
            Mamba2Layer(64,64,4,4,16,i) for i in range(4)
        ])
        self.out_proj = nn.Linear(64, 5)

    def forward(self, x):
        x = self.in_proj(x)
        for l in self.layers: x = l(x)
        return self.out_proj(x)
```

* **Input**: 5 features → 64-dim embedding
* **4× Mamba2 layers** (d\_state=64, d\_conv=4, expand=4, headdim=16)
* **Output**: 64 → 5 features
* **Loss**: Autoregressive Smooth L₁ + per-feature weighting (volume 0.25×)

This lean design eschews attention and MLP blocks—yet matches Transformers on nonlinear tasks ([Hugging Face][8]).

---

## 6. Training Loop

We leverage **PyTorch Lightning** for:

* **Autoregressive Huber loss** (shifted predictions)
* **AdamW** + **ReduceLROnPlateau**
* **Gradient clipping** (0.5)
* **Mixed precision** (`bf16-mixed`)
* **Batch size**: 32 × accumulation 8 → effective 256

```python
trainer = pl.Trainer(
    max_epochs=100,
    accelerator="gpu", devices=1,
    precision="bf16-mixed",
    accumulate_grad_batches=8,
    gradient_clip_val=0.5,
    callbacks=[EarlyStopping("val_loss", patience=10),
               ModelCheckpoint(monitor="val_loss", save_top_k=1)]
)
trainer.fit(model, train_loader, val_loader)
```

### Loss Curves
<p align="center">
  <img src="https://storage.googleapis.com/gn-portfolio/images/13-ssm-mamba/mamba_tensorBoard_scalars.svg" max-width="700">
</p>

The training (blue) and validation (orange) curves track closely, indicating stable generalization without heavy overfitting.

---

## 7. Evaluation & Baseline Comparison

After `trainer.test()`, we compute per-feature **MSE, RMSE, MAE, MAPE, R²** and compare against a FlashAttention Transformer trained on the same data.

|   Feature  | Mamba R² | Mamba MAPE (%) | FlashAttn R² | FlashAttn MAPE (%) |
| :--------: | :------: | -------------: | -----------: | -----------------: |
|  **Close** |  0.9901  |           1.45 |       0.8242 |               2.42 |
|  **Open**  |  0.9903  |           1.31 |       0.9900 |               2.54 |
|  **High**  |  0.9918  |           1.09 |       0.9918 |               2.47 |
|   **Low**  |  0.9799  |           1.27 |       0.9798 |               3.48 |
| **Volume** |  0.1692  |         330.00 |       0.1692 |             393.19 |

Mamba matches or slightly exceeds FlashAttention on price series, cutting percentage errors nearly in half—and both struggle on noisy volume ([Maarten Grootendorst Substack][9]).

<p align="center">
  <img src="https://storage.googleapis.com/gn-portfolio/images/13-ssm-mamba/mamba_all_features_predictions.svg" max-width="700">
</p>


---

## 8. Next Steps

To push forecasting further:

* **Feature engineering**: technical indicators, regime‐change flags
* **Hybrid models**: combine Mamba SSM with sparse attention
* **Zero-shot forecasting**: explore Mamba4Cast’s synthetic training paradigm ([arXiv][3])
* **Hyperparameter sweeps**: integrate Lightning’s tuner for optimal d_state, layers, etc.
* **Theoretical analysis**: leverage Lyapunov stability for robust mixed-precision training ([arXiv][7])

By uniting Mamba’s linear scaling with domain-aware preprocessing, you can tackle million-step horizons in finance and beyond. Happy modeling! 🚀

[1]: https://medium.com/pythons-gurus/exploring-state-space-models-for-time-series-forecasting-f33b576ce6d7 "Exploring State-Space Models for Time Series Forecasting - Medium"
[2]: https://mfe.baruch.cuny.edu/wp-content/uploads/2014/12/TS_Lecture5_2019.pdf "[PDF] Time Series Analysis - 5. State space models and Kalman filtering"
[3]: https://arxiv.org/pdf/2410.09385 "[PDF] Efficient Zero-Shot Time Series Forecasting with State Space Models"
[4]: https://arxiv.org/abs/2312.00752 "Mamba: Linear-Time Sequence Modeling with Selective State Spaces"
[5]: https://thegradient.pub/mamba-explained/ "Mamba Explained - The Gradient"
[6]: https://goombalab.github.io/blog/2024/mamba2-part1-model/ "State Space Duality (Mamba-2) Part I - The Model | Goomba Lab"
[7]: https://arxiv.org/pdf/2406.00209 "[PDF] Mamba State-Space Models Are Lyapunov-Stable Learners - arXiv"
[8]: https://huggingface.co/docs/transformers/en/model_doc/mamba "Mamba - Hugging Face"
[9]: https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-mamba-and-state "A Visual Guide to Mamba and State Space Models"
[10]: https://github.com/gabenavarro/MLContainerLab "MLContainer Lab"
