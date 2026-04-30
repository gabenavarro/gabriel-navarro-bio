@{id = "69f05224-a229-4c51-8555-22eee53c0d20"
  title = "Portello: Making Global Assembly More Effective for Rare-Disease Whole Genome Sequencing"
  date = "2026-04-29T00:00:00Z"
  tags = ['journal club', 'genomics', 'biorxiv', 'long-read sequencing', 'rare disease']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/portello-thumb.svg"
  description = "Saunders et al. introduce portello: transfer HiFi read alignments from the sample's own de novo contigs onto GRCh38, and DeepVariant removes 47% of small-variant basecall errors compared with conventional read mapping."
  type = "note"
  disabled = "false"
}

<p align="center">
  <img src="https://storage.googleapis.com/gn-portfolio/images/portello-thumb.svg" max-width="700">
</p>


# Portello: Making Global Assembly More Effective for Rare-Disease Whole Genome Sequencing

*Analysis of Saunders, Kronenberg, Holt, Rowell, Eberle (2026), PacBio — bioRxiv preprint*
*Generated on April 29, 2026*

---

## Table of Contents

- [Abstract](#abstract)
- [A Quick Primer on Long-Read Genomics](#a-quick-primer-on-long-read-genomics)
- [Introduction](#introduction)
- [Results](#results)
  - [Improved Read Representation](#improved-read-representation)
  - [Small Variant Calling Accuracy](#small-variant-calling-accuracy)
  - [Phasing and Haplotagging](#phasing-and-haplotagging)
  - [CNV Interpretation in Segmental Duplications](#cnv-interpretation-in-segmental-duplications)
- [Methods](#methods)
  - [Read Mapping Transfer Algorithm](#read-mapping-transfer-algorithm)
  - [Phase Set Construction](#phase-set-construction)
- [Discussion](#discussion)
- [Key Takeaways (Summary)](#key-takeaways-summary)

---

## Abstract

### Overview

Long-read *de novo* assembly is the right tool for rare-disease whole-genome sequencing. Rare variants — the ones rare-disease patients carry by definition — are also the ones most likely to be wildly different from the reference genome. A sample-specific assembly catches what a reference-based pipeline misses, because the assembler doesn't have to fight the reference at all; it builds the patient's own genome up from raw reads. Yet in clinical practice, assembly remains the *backup* approach. Almost every diagnostic pipeline still funnels reads straight to GRCh38 and calls variants from that mapping.

This paper diagnoses *why* assembly is under-used and proposes a fix. The two complaints from real users are concrete: (1) when a variant is called from the assembly, it lives in *contig coordinates*, which makes it hard to view the read-level evidence that a clinician needs to sign off on (basecall quality, methylation, mosaic support); and (2) reconciling assembly-based calls with the lab's existing reference-based pipeline is awkward — you can end up with two views of the same locus that disagree, and no easy way to decide which is right.

Portello (named for the small Italian word for "hatch" or "porthole" — a window through which to look at the same thing from a new angle) is a small idea with a big payoff: instead of choosing between assembly-based calls and reference-based calls, *transfer* the read alignments. The reads are first aligned to the sample's own assembly contigs (so they benefit from the long-range haplotype structure the assembler discovered); the contigs are mapped to GRCh38; and portello composes those two mapping functions to produce read alignments that *land on GRCh38 coordinates* but were *placed via the assembly*. Standard tools — DeepVariant, structural-variant callers, IGV — consume the resulting BAM file without modification.

The headline number: when DeepVariant is run on portello-remapped HG002 reads instead of pbmm2-mapped reads (same reads, same model, only the mapping changed), it removes **47% of small-variant basecall errors**. False negatives drop by 52%; false positives stay essentially flat. On NA12878 the total error reduction is 29%. None of this required retraining DeepVariant.

### Concept Diagram

<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="abs-portello-title">
  <title id="abs-portello-title">Portello composes read-to-contig and contig-to-reference alignments to land reads on GRCh38 via the assembly.</title>
  <defs>
    <marker id="abs-arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
    <marker id="abs-arrow-g" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#22c55e"/>
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Portello: read alignment via the assembly</text>
  <!-- Reads -->
  <rect x="30" y="60" width="160" height="70" rx="10" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="110" y="90" text-anchor="middle" font-weight="600" fill="#92400e">HiFi reads</text>
  <text x="110" y="110" text-anchor="middle" font-size="11" fill="#64748b">~15–25 kb each</text>
  <!-- Contigs -->
  <rect x="270" y="60" width="180" height="70" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="360" y="90" text-anchor="middle" font-weight="600" fill="#1e40af">de novo contigs</text>
  <text x="360" y="110" text-anchor="middle" font-size="11" fill="#64748b">hifiasm dual-assembly</text>
  <!-- Reference -->
  <rect x="530" y="60" width="160" height="70" rx="10" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="610" y="90" text-anchor="middle" font-weight="600" fill="#166534">GRCh38 reference</text>
  <text x="610" y="110" text-anchor="middle" font-size="11" fill="#64748b">standard target</text>
  <!-- Read-to-contig arrow -->
  <line x1="190" y1="95" x2="270" y2="95" stroke="#64748b" stroke-width="1.5" marker-end="url(#abs-arrow)"/>
  <text x="230" y="84" text-anchor="middle" font-size="10" fill="#475569">pbmm2</text>
  <!-- Contig-to-ref arrow -->
  <line x1="450" y1="95" x2="530" y2="95" stroke="#64748b" stroke-width="1.5" marker-end="url(#abs-arrow)"/>
  <text x="490" y="84" text-anchor="middle" font-size="10" fill="#475569">minimap2</text>
  <!-- Composition (the trick) -->
  <rect x="180" y="180" width="360" height="70" rx="10" fill="#faf5ff" stroke="#a855f7" stroke-width="2"/>
  <text x="360" y="208" text-anchor="middle" font-weight="700" fill="#6b21a8">portello: compose mappings</text>
  <text x="360" y="228" text-anchor="middle" font-size="11" fill="#64748b">(read → contig) ° (contig → reference)</text>
  <!-- Inputs flowing in -->
  <line x1="230" y1="130" x2="280" y2="180" stroke="#a855f7" stroke-width="1.5" stroke-dasharray="4,3"/>
  <line x1="490" y1="130" x2="440" y2="180" stroke="#a855f7" stroke-width="1.5" stroke-dasharray="4,3"/>
  <!-- Output -->
  <line x1="360" y1="250" x2="360" y2="285" stroke="#22c55e" stroke-width="2" marker-end="url(#abs-arrow-g)"/>
  <rect x="190" y="290" width="340" height="55" rx="10" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="360" y="313" text-anchor="middle" font-weight="700" fill="#166534">read → reference BAM</text>
  <text x="360" y="332" text-anchor="middle" font-size="11" fill="#64748b">consumable by DeepVariant, IGV, … unchanged</text>
</svg>

### Key Takeaways

- **Two-step alignment beats one-step**: Splitting "reads to reference" into "reads to contigs ° contigs to reference" puts each sub-problem in a regime where standard mappers excel, instead of asking one mapper to handle both sequencing error and biological variation simultaneously.
- **47% fewer small-variant errors, free**: DeepVariant on the same HG002 reads loses about half its basecall errors when the input BAM comes from portello instead of pbmm2 — without any retraining.
- **Phasing for free**: Because reads were placed via specific contigs, portello can carry haplotype tags and phase sets through to the reference-coordinate BAM in one step.
- **Coverage you can trust**: In segmental duplications, conventional mapping produces coverage spikes of 12,000× followed by gene-level dropouts; portello produces a clean 3-fold profile that matches the underlying biology.

---

## A Quick Primer on Long-Read Genomics

If you mostly work with short-read or non-genomic data, this section gives you the scaffolding for what follows. Skip if you already speak HiFi.

**Sequencing.** A modern PacBio HiFi instrument reads single DNA molecules of ~15–25 kb at >99.9% per-base accuracy. ONT (Oxford Nanopore) reads are longer (often >100 kb) but historically less accurate, though that gap has been closing. "Long-read sequencing" in this paper means HiFi unless otherwise specified.

**Reads vs. assembly vs. reference.** A *read* is one sequenced molecule. A *reference* (GRCh38) is the public consensus human genome — one assembly built from many people, used as a coordinate system. *De novo assembly* takes a sample's reads and stitches them into long *contigs* (contiguous sequences) without using the reference at all. With HiFi data and a modern assembler (`hifiasm`, `Verkko`), a human assembly is typically *partially phased* or *dual-assembly*: you get two contig sets representing both haplotypes of the diploid genome, but the contigs are not perfectly switched to the right haplotype throughout (there are *switch errors*).

**Conventional read mapping.** The standard variant-calling pipeline aligns each read to the reference (`pbmm2` for PacBio HiFi, `minimap2` more generally), then runs a caller like DeepVariant on those alignments. This is fast, scales easily, and produces variants in standard reference coordinates. The downside: when the patient's true sequence is wildly different from GRCh38 (large insertions, structural variants, divergent haplotypes), the mapper struggles — reads are split, soft-clipped, or misplaced, and the caller sees garbage.

**Variant types.** *Small variants* are SNVs and short indels (typically ≤ 50 bp). *Structural variants* (SVs) are larger insertions, deletions, inversions, and translocations. *Copy-number variants* (CNVs) are gains or losses of larger chromosomal regions. Rare-disease patients carry both classes; small variants are easier to call but SVs and CNVs are often the actual diagnosis.

**Phasing.** A diploid human carries two copies of (most of) each chromosome, one from each parent. *Phasing* assigns each variant to its parental haplotype. The bam tags `HP` (haplotype 1 or 2) and `PS` (phase set ID, marking the contiguous region within which the phasing is internally consistent) are the standard way to record this on individual reads.

**Why this paper exists.** Assembly captures the patient's genome better than reference-based mapping in hard regions, but assembly-based variant calls are awkward to integrate with the rest of the standard pipeline. Portello bridges the two worlds.

---

## Introduction

### Overview

Predicting which variants caused a patient's disease is one of the central tasks of clinical genomics, and for rare disease it is unusually hard. The variants in question, by definition, are not in any common-variant database. They are also more likely than common variants to live in regions where the patient's sequence diverges substantially from GRCh38 — segmental duplications, repeat expansions, structural rearrangements. These are exactly the regions where conventional reference-based mapping has the most trouble: a read drawn from a region that doesn't really exist in GRCh38 has nowhere good to land.

The field has worked through several paradigms over the last two decades. Short-read sequencing (Illumina) plus reference mapping (BWA) plus a probabilistic caller (GATK) became the workhorse in the 2010s, and it solved most of the easy genome. The hard regions remained hard. Long-read sequencing — first PacBio CLR and ONT R9, then HiFi and ONT R10 — arrived with two answers: longer reads make repeat-spanning unambiguous, and high-accuracy long reads make whole-genome assembly feasible from a single library. Tools like `hifiasm` (Cheng et al. 2021) and `Verkko` (Rautiainen et al. 2023) routinely produce diploid human assemblies in days. Recent rare-disease studies have shown that a meaningful fraction of candidate causal variants — both *de novo* and recessive — are *only* recoverable from assembly-based calling.

So why isn't every rare-disease lab running assembly? Because the operational story is messy. Assembly produces contigs in their own coordinate system. Variants called against contigs need to be lifted to GRCh38 to be talked about, reviewed, or compared with prior data. Read-level evidence — the kind a clinician squints at in IGV before signing off — is hidden behind an extra coordinate translation. Mosaic variants (present in only a fraction of cells, important for cancer and developmental disorders) are unlikely to make it into a haploid assembly consensus at all. And when an assembly-based call disagrees with the lab's existing reference-based pipeline, there is no obvious adjudicator.

Portello's framing is that you don't have to pick. The reference-based pipeline gets to keep its variant callers, its coordinates, and its review tools, but the *read alignments* feeding the pipeline now ride on top of the patient's assembly. The two halves of the alignment problem — "where is this read on the patient's genome?" and "where is the patient's genome on GRCh38?" — are decoupled and solved separately, then composed back into one BAM in reference coordinates. The mapper handling each sub-problem only has to deal with one source of difficulty: sequencing error for read-to-contig, biological variation for contig-to-reference. Each sub-problem is what its mapper was actually built for.

### Concept Diagram

<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="intro-evolution-title">
  <title id="intro-evolution-title">Evolution from short-read reference mapping to assembly-based read mapping.</title>
  <defs>
    <marker id="intro-arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">From reference mapping to assembly mapping</text>
  <!-- Era 1 -->
  <rect x="20" y="60" width="200" height="80" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="120" y="86" text-anchor="middle" font-weight="600" fill="#334155">Short-read mapping</text>
  <text x="120" y="106" text-anchor="middle" font-size="11" fill="#64748b">BWA + GATK</text>
  <text x="120" y="124" text-anchor="middle" font-size="11" fill="#dc2626">hard regions: blind</text>
  <line x1="220" y1="100" x2="260" y2="100" stroke="#64748b" stroke-width="1.5" marker-end="url(#intro-arrow)"/>
  <!-- Era 2 -->
  <rect x="260" y="60" width="200" height="80" rx="8" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="360" y="86" text-anchor="middle" font-weight="600" fill="#854d0e">Long-read mapping</text>
  <text x="360" y="106" text-anchor="middle" font-size="11" fill="#64748b">pbmm2 / minimap2</text>
  <text x="360" y="124" text-anchor="middle" font-size="11" fill="#ca8a04">spans repeats; SVs ok</text>
  <line x1="460" y1="100" x2="500" y2="100" stroke="#64748b" stroke-width="1.5" marker-end="url(#intro-arrow)"/>
  <!-- Era 3 -->
  <rect x="500" y="60" width="200" height="80" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="600" y="86" text-anchor="middle" font-weight="600" fill="#1e40af">Assembly only</text>
  <text x="600" y="106" text-anchor="middle" font-size="11" fill="#64748b">hifiasm / Verkko</text>
  <text x="600" y="124" text-anchor="middle" font-size="11" fill="#3b82f6">finds rare variants;</text>
  <text x="600" y="138" text-anchor="middle" font-size="11" fill="#3b82f6">awkward to integrate</text>
  <!-- Era 4 -->
  <line x1="360" y1="180" x2="360" y2="210" stroke="#a855f7" stroke-width="2" marker-end="url(#intro-arrow)"/>
  <rect x="200" y="220" width="320" height="100" rx="10" fill="#faf5ff" stroke="#a855f7" stroke-width="2"/>
  <text x="360" y="248" text-anchor="middle" font-weight="700" fill="#6b21a8">Assembly-based read mapping</text>
  <text x="360" y="270" text-anchor="middle" font-size="12" fill="#6b21a8">portello (this paper)</text>
  <text x="360" y="292" text-anchor="middle" font-size="11" fill="#64748b">read-level evidence kept;</text>
  <text x="360" y="308" text-anchor="middle" font-size="11" fill="#64748b">unifies assembly + reference views</text>
</svg>

### Key Takeaways

- **The hard regions are the rare-disease regions**: SVs, segmental duplications, and divergent haplotypes are exactly where reference-based mapping breaks down — and where rare-disease causal variants are most likely to live.
- **Assembly already exists, it's just hard to use**: Modern HiFi assemblers produce diploid human genomes routinely. The barrier is operational integration with the rest of the lab, not assembly quality.
- **Composition is the move**: By solving "read → contig" and "contig → reference" as separate problems and composing them, each mapper handles only one source of disagreement — sequencing error or biological variation, never both.
- **Reference coordinates as a UI**: Portello's output looks like a normal reference-coordinate BAM. The integration story is "no integration": existing tools just work.

---

## Results

The paper presents four results, two of which carry quantitative head-to-heads (small-variant accuracy and phasing) and two of which are qualitative demonstrations on illustrative loci (read representation and CNV interpretation). I treat them in the order the paper does.

### Improved Read Representation

#### Overview

Before the result, a quick orientation: a *VNTR* is a *variable number tandem repeat* — a short sequence motif that is repeated end-to-end, with the number of repeats varying between people. VNTRs are notoriously hard for mappers because the read can plausibly align to many positions within the repeat block at very similar scores; the mapper has to pick one, and small differences in scoring (or in the read's own sequencing errors) can flip the choice. The result is a "messy pileup": within a few hundred base pairs you'll see indels at slightly different reference positions, soft-clips that don't agree with each other, and split alignments fighting over the same reads.

Portello's contribution here is structural rather than quantitative. The authors don't put a number on read-representation quality in this section; they show side-by-side IGV-style views of a VNTR locus mapped two ways. With pbmm2 (Figure 1B in the paper), each read is doing its own thing. With portello (Figure 1C), the reads agree with each other. The mechanism is the same one that drives the variant-calling result later: portello aligns each read against the patient's *own* contigs first, in which the VNTR has a single, consistent representation; only then does the contig-to-reference alignment have to grapple with how that representation differs from GRCh38, and it does so once per contig instead of once per read.

There is also a more subtle gain: the patient's contigs act as a *sample-specific decoy*. In conventional mapping, reads from a region that's been duplicated in the sample but not in the reference end up scattered across the closest reference homologs, creating phantom variants. With portello, those reads first align to the *correct* sample-specific contig — their actual home — and the contig-to-reference step decides where to deposit the contig. Reads that genuinely don't have a good home in the sample assembly are kept in a separate "unassembled" output.

#### Concept Diagram

<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="rep-vntr-title">
  <title id="rep-vntr-title">Schematic of read alignment in a VNTR: pbmm2 vs portello pileups.</title>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">VNTR pileup: noisy vs consistent</text>
  <!-- pbmm2 panel -->
  <rect x="20" y="60" width="320" height="280" rx="10" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="180" y="86" text-anchor="middle" font-weight="700" fill="#991b1b">conventional (pbmm2)</text>
  <!-- Reference bar -->
  <rect x="40" y="110" width="280" height="10" fill="#cbd5e1"/>
  <text x="40" y="106" font-size="10" fill="#64748b">GRCh38</text>
  <!-- Reads (varying offsets, many indel marks) -->
  <rect x="40" y="135" width="120" height="6" fill="#3b82f6"/>
  <rect x="166" y="135" width="100" height="6" fill="#3b82f6"/>
  <circle cx="162" cy="138" r="3" fill="#dc2626"/>
  <rect x="50" y="150" width="110" height="6" fill="#3b82f6"/>
  <rect x="170" y="150" width="120" height="6" fill="#3b82f6"/>
  <circle cx="165" cy="153" r="3" fill="#dc2626"/>
  <rect x="40" y="165" width="100" height="6" fill="#3b82f6"/>
  <rect x="148" y="165" width="130" height="6" fill="#3b82f6"/>
  <circle cx="144" cy="168" r="3" fill="#dc2626"/>
  <rect x="55" y="180" width="90" height="6" fill="#3b82f6"/>
  <rect x="155" y="180" width="120" height="6" fill="#3b82f6"/>
  <circle cx="150" cy="183" r="3" fill="#dc2626"/>
  <rect x="40" y="195" width="100" height="6" fill="#3b82f6"/>
  <rect x="148" y="195" width="130" height="6" fill="#3b82f6"/>
  <circle cx="144" cy="198" r="3" fill="#dc2626"/>
  <rect x="50" y="210" width="115" height="6" fill="#3b82f6"/>
  <rect x="173" y="210" width="100" height="6" fill="#3b82f6"/>
  <circle cx="169" cy="213" r="3" fill="#dc2626"/>
  <text x="180" y="248" text-anchor="middle" font-size="11" fill="#dc2626" font-weight="600">indels at slightly different positions</text>
  <text x="180" y="268" text-anchor="middle" font-size="11" fill="#dc2626">soft-clips disagree</text>
  <text x="180" y="288" text-anchor="middle" font-size="11" fill="#dc2626">caller sees noise</text>
  <text x="180" y="320" text-anchor="middle" font-size="11" fill="#991b1b" font-style="italic">each read negotiates the VNTR alone</text>
  <!-- portello panel -->
  <rect x="380" y="60" width="320" height="280" rx="10" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="540" y="86" text-anchor="middle" font-weight="700" fill="#166534">portello (assembly-based)</text>
  <rect x="400" y="110" width="280" height="10" fill="#cbd5e1"/>
  <text x="400" y="106" font-size="10" fill="#64748b">GRCh38</text>
  <!-- Reads aligned uniformly -->
  <rect x="400" y="135" width="120" height="6" fill="#22c55e"/>
  <rect x="525" y="135" width="100" height="6" fill="#22c55e"/>
  <circle cx="522" cy="138" r="3" fill="#16a34a"/>
  <rect x="400" y="150" width="120" height="6" fill="#22c55e"/>
  <rect x="525" y="150" width="100" height="6" fill="#22c55e"/>
  <circle cx="522" cy="153" r="3" fill="#16a34a"/>
  <rect x="400" y="165" width="120" height="6" fill="#22c55e"/>
  <rect x="525" y="165" width="100" height="6" fill="#22c55e"/>
  <circle cx="522" cy="168" r="3" fill="#16a34a"/>
  <rect x="400" y="180" width="120" height="6" fill="#22c55e"/>
  <rect x="525" y="180" width="100" height="6" fill="#22c55e"/>
  <circle cx="522" cy="183" r="3" fill="#16a34a"/>
  <rect x="400" y="195" width="120" height="6" fill="#22c55e"/>
  <rect x="525" y="195" width="100" height="6" fill="#22c55e"/>
  <circle cx="522" cy="198" r="3" fill="#16a34a"/>
  <rect x="400" y="210" width="120" height="6" fill="#22c55e"/>
  <rect x="525" y="210" width="100" height="6" fill="#22c55e"/>
  <circle cx="522" cy="213" r="3" fill="#16a34a"/>
  <text x="540" y="248" text-anchor="middle" font-size="11" fill="#166534" font-weight="600">indels at the same position</text>
  <text x="540" y="268" text-anchor="middle" font-size="11" fill="#166534">consistent alignments</text>
  <text x="540" y="288" text-anchor="middle" font-size="11" fill="#166534">caller sees a clean variant</text>
  <text x="540" y="320" text-anchor="middle" font-size="11" fill="#166534" font-style="italic">the contig negotiates the VNTR once</text>
  <text x="360" y="362" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Schematic adapted from the paper's Figures 1B/1C; positions are illustrative, not literal.</text>
</svg>

### Key Takeaways

- **VNTRs are where one-mapper-fits-all breaks**: The mapper has to settle a tie that doesn't really have an answer at the read level; portello deferring that tie to the contig step is the actual fix.
- **Contigs as decoys**: A patient-specific assembly is the cleanest possible decoy sequence for the patient's own reads — no public decoy can match.
- **Qualitative result, structural cause**: This section is illustrative rather than benchmarked, but it sets up the mechanism that the next two sections turn into hard numbers.

---

### Small Variant Calling Accuracy

#### Overview

Before the result, a quick orientation: *small variants* are SNVs and short indels (typically ≤ 50 bp), and they are scored against a *truth set* — a hand-curated, often assembly-confirmed list of variants for a benchmark sample. The two samples here are HG002 (an Ashkenazi Jewish reference sample with the GIAB draft T2T benchmark) and NA12878 (a CEPH reference sample with the Platinum Pedigree v1.2 truth set). The metric is *F1 of variant calls* against the benchmark, decomposed into *false negatives* (variants the truth set has but the caller missed) and *false positives* (calls the caller made that aren't in the truth set).

The experiment is designed to isolate one variable. The same reads are used in both arms. The same caller (DeepVariant v1.9 with the standard HiFi model) is used in both arms. The DeepVariant model is *not retrained* on portello output. The only thing that changes between the two arms is the read mapper: pbmm2 v1.17 (conventional) vs portello (assembly-based). Anything that improves between the arms therefore comes purely from better alignment, not from a smarter caller or a model that has seen more of the input distribution.

The result is large. On HG002, total basecall errors drop by **47%** (from 375,634 to 199,368 across both BASEPAIR FN and FP) — almost entirely driven by a 52% reduction in false negatives. False positives change by a small amount (-14%). On NA12878, the picture is similar in shape: a 55% drop in false negatives, little change in false positives, and a 29% drop in total errors. The absolute F1 on HG002 climbs from 0.9901 to 0.9948; on NA12878 from 0.9916 to 0.9940. The headline number sounds modest in F1 space (under one percentage point) because both methods are already near the ceiling, but the *error reduction* lens is the right one for clinical use: every one of those false negatives is a missing variant call that a clinician would have wanted to see.

The asymmetry between samples is notable. HG002 sees a bigger total-error reduction than NA12878, mostly because NA12878 starts with a higher baseline of false positives (likely tied to using an externally produced Verkko assembly from the Platinum Pedigree project rather than a fresh hifiasm assembly built from these reads). Even so, the shape — recall up sharply, precision essentially flat — is consistent and is the expected signature of *better placement*: reads that previously missed their region (false negatives) get there, while reads that were going to call a wrong variant don't suddenly become more confident.

#### Concept Diagram

<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="var-bar-title">
  <title id="var-bar-title">DeepVariant basecall errors: pbmm2 vs portello on HG002 and NA12878.</title>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">DeepVariant basecall errors (BASEPAIR)</text>
  <text x="360" y="42" text-anchor="middle" font-size="11" fill="#64748b">Lower is better — reduction comes almost entirely from fewer false negatives.</text>
  <!-- HG002 group -->
  <text x="40" y="80" font-weight="700" fill="#1e293b">HG002</text>
  <text x="180" y="108" text-anchor="end" fill="#334155" font-size="12">pbmm2</text>
  <rect x="190" y="96" width="380" height="20" rx="4" fill="#ef4444" opacity="0.65"/>
  <text x="580" y="111" font-size="11" fill="#dc2626">FN 326,253 + FP 49,381 = 375,634</text>
  <text x="180" y="138" text-anchor="end" fill="#334155" font-size="12">portello</text>
  <rect x="190" y="126" width="201" height="20" rx="4" fill="#22c55e" opacity="0.85"/>
  <text x="400" y="141" font-size="11" fill="#166534" font-weight="700">FN 156,775 + FP 42,593 = 199,368  −47%</text>
  <!-- NA12878 group -->
  <text x="40" y="190" font-weight="700" fill="#1e293b">NA12878</text>
  <text x="180" y="218" text-anchor="end" fill="#334155" font-size="12">pbmm2</text>
  <rect x="190" y="206" width="287" height="20" rx="4" fill="#ef4444" opacity="0.65"/>
  <text x="488" y="221" font-size="11" fill="#dc2626">FN 163,016 + FP 119,992 = 283,008</text>
  <text x="180" y="248" text-anchor="end" fill="#334155" font-size="12">portello</text>
  <rect x="190" y="236" width="204" height="20" rx="4" fill="#22c55e" opacity="0.85"/>
  <text x="403" y="251" font-size="11" fill="#166534" font-weight="700">FN 73,114 + FP 128,362 = 201,476  −29%</text>
  <!-- Caption box -->
  <rect x="60" y="290" width="600" height="50" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
  <text x="360" y="310" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Same reads, same DeepVariant model, no retraining; only the mapper changed.</text>
  <text x="360" y="328" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">FN drop ≈ 52–55% in both samples; FP changes are small.</text>
</svg>

#### Try It Yourself

The two key knobs that decide how big the portello win is on a given sample are (1) the *fraction of reads from hard regions* (VNTRs, segmental duplications, divergent haplotypes) and (2) the *quality of the assembly* the reads were aligned to first. Click through to feel how those interact. The numbers below are illustrative, anchored on the paper's HG002 vs NA12878 contrast.

<style>
  .ptb-portello-step {
    border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px 20px; margin: 16px 0;
  }
  .ptb-portello-step .ptb-label {
    display: block; font-size: 13px; color: #475569; margin-bottom: 8px; font-weight: 600;
  }
  .ptb-portello-step .ptb-buttons { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
  .ptb-portello-step input[type="radio"] { display: none; }
  .ptb-portello-step .ptb-btn {
    padding: 6px 14px; border: 1px solid #cbd5e1; border-radius: 6px;
    cursor: pointer; font-size: 13px; font-weight: 600; color: #475569;
    background: #f8fafc; user-select: none;
  }
  .ptb-portello-step .ptb-btn:hover { border-color: #3b82f6; color: #1e40af; }
  .ptb-portello-step .ptb-state { display: none; }
  .ptb-portello-step input#prt-easy:checked ~ .ptb-buttons label[for="prt-easy"],
  .ptb-portello-step input#prt-mid:checked  ~ .ptb-buttons label[for="prt-mid"],
  .ptb-portello-step input#prt-hard:checked ~ .ptb-buttons label[for="prt-hard"],
  .ptb-portello-step input#prt-bad:checked  ~ .ptb-buttons label[for="prt-bad"] {
    background: #eff6ff; border-color: #3b82f6; color: #1e40af;
  }
  .ptb-portello-step input#prt-easy:checked ~ #prt-s-easy,
  .ptb-portello-step input#prt-mid:checked  ~ #prt-s-mid,
  .ptb-portello-step input#prt-hard:checked ~ #prt-s-hard,
  .ptb-portello-step input#prt-bad:checked  ~ #prt-s-bad { display: block; }
</style>

<div class="ptb-portello-step">
  <span class="ptb-label">Sample regime — pick the kind of sample:</span>
  <input type="radio" name="prt" id="prt-easy">
  <input type="radio" name="prt" id="prt-mid" checked>
  <input type="radio" name="prt" id="prt-hard">
  <input type="radio" name="prt" id="prt-bad">

  <div class="ptb-buttons">
    <label for="prt-easy" class="ptb-btn">Easy genome, fresh asm</label>
    <label for="prt-mid"  class="ptb-btn">HG002-like</label>
    <label for="prt-hard" class="ptb-btn">SV-rich rare-disease</label>
    <label for="prt-bad"  class="ptb-btn">Externally-built asm</label>
  </div>

  <div class="ptb-state" id="prt-s-easy">
    <svg viewBox="0 0 480 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="prt-s-easy-t">
      <title id="prt-s-easy-t">Easy genome, fresh assembly: small absolute gain.</title>
      <text x="20" y="22" font-size="12" fill="#64748b" font-weight="600">pbmm2 errors</text>
      <rect x="120" y="12" width="120" height="18" rx="3" fill="#ef4444" opacity="0.6"/>
      <text x="20" y="50" font-size="12" fill="#64748b" font-weight="600">portello errors</text>
      <rect x="120" y="40" width="100" height="18" rx="3" fill="#22c55e" opacity="0.7"/>
      <text x="240" y="92" font-size="12" fill="#475569">~17% reduction. Easy genomes have few hard regions, so the headroom is small.</text>
    </svg>
  </div>

  <div class="ptb-state" id="prt-s-mid">
    <svg viewBox="0 0 480 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="prt-s-mid-t">
      <title id="prt-s-mid-t">HG002-like sample: 47% total error reduction.</title>
      <text x="20" y="22" font-size="12" fill="#64748b" font-weight="600">pbmm2 errors</text>
      <rect x="120" y="12" width="320" height="18" rx="3" fill="#ef4444" opacity="0.65"/>
      <text x="20" y="50" font-size="12" fill="#64748b" font-weight="600">portello errors</text>
      <rect x="120" y="40" width="170" height="18" rx="3" fill="#22c55e" opacity="0.85"/>
      <text x="240" y="92" font-size="12" fill="#475569">47% reduction (paper's HG002 result). FN drops 52%; FP barely moves.</text>
    </svg>
  </div>

  <div class="ptb-state" id="prt-s-hard">
    <svg viewBox="0 0 480 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="prt-s-hard-t">
      <title id="prt-s-hard-t">SV-rich rare-disease sample: bigger gain, qualitative.</title>
      <text x="20" y="22" font-size="12" fill="#64748b" font-weight="600">pbmm2 errors</text>
      <rect x="120" y="12" width="360" height="18" rx="3" fill="#ef4444" opacity="0.7"/>
      <text x="20" y="50" font-size="12" fill="#64748b" font-weight="600">portello errors</text>
      <rect x="120" y="40" width="160" height="18" rx="3" fill="#22c55e" opacity="0.9"/>
      <text x="240" y="92" font-size="12" fill="#475569">Plausibly larger reduction (extrapolation from the paper's CNV example, not benchmarked).</text>
    </svg>
  </div>

  <div class="ptb-state" id="prt-s-bad">
    <svg viewBox="0 0 480 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="prt-s-bad-t">
      <title id="prt-s-bad-t">Externally-built assembly: gain still large but FP-heavy baseline.</title>
      <text x="20" y="22" font-size="12" fill="#64748b" font-weight="600">pbmm2 errors</text>
      <rect x="120" y="12" width="240" height="18" rx="3" fill="#ef4444" opacity="0.65"/>
      <text x="20" y="50" font-size="12" fill="#64748b" font-weight="600">portello errors</text>
      <rect x="120" y="40" width="170" height="18" rx="3" fill="#22c55e" opacity="0.85"/>
      <text x="240" y="92" font-size="12" fill="#475569">29% reduction (paper's NA12878 result, externally produced Verkko assembly).</text>
    </svg>
  </div>
</div>

#### Implementation

To reason quantitatively about "47% of basecall errors removed", here is the reduction calculation as the paper applies it — treating a *basecall error* as the union of false negatives and false positives, BASEPAIR-metric, summed across the sample.

```python
from typing import TypedDict


class CountsBP(TypedDict):
    fn: int  # false negatives in the BASEPAIR comparison
    fp: int  # false positives in the BASEPAIR comparison


def basecall_error_reduction(
    pbmm2: CountsBP,    # FN/FP from conventional read mapping
    portello: CountsBP, # FN/FP from assembly-based remapping
) -> dict[str, float]:
    """Fraction of small-variant basecall errors removed by switching mapper.

    The paper defines `basecall errors = FN + FP` under the BASEPAIR metric,
    and reports the fraction *removed* by the new mapper. The same caller
    (DeepVariant v1.9, standard HiFi model) is used in both arms, so any
    reduction is attributable to mapping, not modeling.

    Returns the total reduction plus the FN- and FP-specific reductions
    so you can see whether the gain is recall-driven (paper: yes) or
    precision-driven.
    """
    # Step 1: total errors per arm
    err_pbmm2    = pbmm2["fn"]    + pbmm2["fp"]
    err_portello = portello["fn"] + portello["fp"]

    # Step 2: relative reduction (positive = portello better)
    total_red = 1.0 - err_portello / err_pbmm2

    # Step 3: split by error type so you see *where* the win came from
    fn_red = 1.0 - portello["fn"] / pbmm2["fn"]
    fp_red = 1.0 - portello["fp"] / pbmm2["fp"]

    return {"total_reduction": total_red, "fn_reduction": fn_red, "fp_reduction": fp_red}


# HG002 numbers from Table S1, BASEPAIR row
hg002 = basecall_error_reduction(
    pbmm2   ={"fn": 326_253, "fp": 49_381},
    portello={"fn": 156_775, "fp": 42_593},
)
# {'total_reduction': 0.469..., 'fn_reduction': 0.519..., 'fp_reduction': 0.137...}
```

### Key Takeaways

- **Same reads, same caller, only the mapper changed**: This is the cleanest possible attribution — the gain is in alignment, not in the model.
- **The win is recall, not precision**: False negatives drop ~52–55% in both samples; false positives barely move. Reads that previously couldn't find their region now do.
- **F1 understates the clinical impact**: 0.9901 to 0.9948 sounds small until you frame it as 47% of errors removed; for clinical sign-off, every removed false negative is a recovered variant.
- **Sample matters**: NA12878's 29% total reduction (vs HG002's 47%) is plausibly tied to using an external Verkko assembly rather than a fresh hifiasm assembly built from the same reads — a reasonable read of the data, though the paper does not directly attribute the gap.

---

### Phasing and Haplotagging

#### Overview

Before the result, a quick orientation: *phasing* assigns each variant to one of two parental haplotypes. *Haplotagging* puts that information on the individual reads (so you can color reads by haplotype in IGV, or feed haplotype-aware callers). The standard tags are `HP` (1 or 2, the haplotype) and `PS` (phase set, the contiguous region within which the assignment is internally consistent). Phasing quality is summarized by *block NG50* (a length statistic: the largest L such that 50% of the genome is contained in phase blocks of length ≥ L), *switch errors* (pairs of adjacent variants assigned to the wrong relative haplotype), and *flips* (single-variant inversions, less serious than a switch).

What's nice about portello here is that phasing comes essentially for free. The reads have already been aligned to *specific* contigs from the assembly, and the assembly already encodes haplotype information — either implicitly (in dual-assembly mode, where each contig is *probably* one haplotype but with switch errors), or explicitly (in fully-phased mode, when the assembly was scaffolded with parental sequencing or optical mapping).

In dual-assembly mode (the more common setting for unrelated patients), portello uses a small read-backed scheme: walk along the reference, and at each pair of adjacent heterozygous variants where the two contigs disagree, check that at least one read supports both contig alleles in the same way. If yes, extend the phase set across that pair. If no, end the phase set and start a new one. This is essentially a stripped-down `whatshap`-style phasing, but operating on the contig-derived heterozygous variant set rather than a separately-called variant set.

The numbers reported are intentionally specific to a single sample (HG002), benchmarked with the GIAB T2T draft small-variant truth set: a phase block NG50 of **334,357 bp** with **274 switch errors** and **67 flips**. The authors are explicit that direct evaluation of read haplotag accuracy is fiddly, so they instead emit a phased VCF of heterozygous variants and benchmark *that* with `whatshap compare`. Those numbers are competitive with dedicated read-phasing tools, particularly given that portello obtained them as a side effect of the alignment process rather than a separate phasing step.

The authors are also frank that "with further development, there is significant potential to improve this capability in coordination with a portello-integrated small-variant caller designed to more accurately call small variants from the read-to-contig alignments" — i.e., they think this can get better, and a more integrated phasing-aware caller is the next step.

#### Concept Diagram

<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="phase-tree-title">
  <title id="phase-tree-title">Two phasing modes in portello: fully-phased contigs vs partially-phased dual assembly.</title>
  <defs>
    <marker id="phase-arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Portello phasing modes</text>
  <!-- Root -->
  <rect x="270" y="50" width="180" height="50" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
  <text x="360" y="80" text-anchor="middle" font-weight="700" fill="#1e40af">input contigs</text>
  <line x1="360" y1="100" x2="360" y2="125" stroke="#64748b" stroke-width="1.5"/>
  <line x1="180" y1="125" x2="540" y2="125" stroke="#64748b" stroke-width="1.5"/>
  <!-- Fully-phased branch -->
  <line x1="180" y1="125" x2="180" y2="160" stroke="#64748b" stroke-width="1.5" marker-end="url(#phase-arrow)"/>
  <rect x="60" y="170" width="240" height="160" rx="10" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="180" y="194" text-anchor="middle" font-weight="700" fill="#166534">fully-phased</text>
  <text x="180" y="214" text-anchor="middle" font-size="11" fill="#16a34a">parental seq, optical map</text>
  <text x="180" y="240" text-anchor="middle" font-size="11" fill="#475569">phase = which contig</text>
  <text x="180" y="258" text-anchor="middle" font-size="11" fill="#475569">the read aligned to</text>
  <text x="180" y="288" text-anchor="middle" font-size="11" fill="#16a34a" font-weight="600">no phasing alg needed</text>
  <text x="180" y="308" text-anchor="middle" font-size="14">&#10003;</text>
  <!-- Partially-phased branch -->
  <line x1="540" y1="125" x2="540" y2="160" stroke="#64748b" stroke-width="1.5" marker-end="url(#phase-arrow)"/>
  <rect x="420" y="170" width="240" height="160" rx="10" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="540" y="194" text-anchor="middle" font-weight="700" fill="#854d0e">partially-phased</text>
  <text x="540" y="214" text-anchor="middle" font-size="11" fill="#ca8a04">hifiasm dual assembly</text>
  <text x="540" y="240" text-anchor="middle" font-size="11" fill="#475569">walk adjacent het pairs;</text>
  <text x="540" y="258" text-anchor="middle" font-size="11" fill="#475569">extend block when one read</text>
  <text x="540" y="276" text-anchor="middle" font-size="11" fill="#475569">spans both</text>
  <text x="540" y="305" text-anchor="middle" font-size="11" fill="#854d0e" font-weight="600">block NG50 = 334 kb</text>
  <text x="360" y="362" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">HG002 partially-phased mode: 274 switch errors + 67 flips, GIAB T2T benchmark.</text>
</svg>

### Key Takeaways

- **Phasing comes free with mapping**: Because portello already knows which contig each read came from, the haplotype tag is essentially a lookup — no separate phasing pass.
- **Two modes, by assembly quality**: Fully-phased contigs (rare today) need no algorithm; partially-phased dual assemblies (the common case) get a small read-backed extension scheme.
- **Quality is competitive, not state-of-the-art**: Block NG50 of 334 kb with 274 switches on HG002 is in the ballpark of dedicated tools; the authors explicitly flag room for improvement when a phasing-aware caller is added.

---

### CNV Interpretation in Segmental Duplications

#### Overview

Before the result, a quick orientation: *segmental duplications* are large (typically ≥ 10 kb) regions where two or more nearly-identical copies of a sequence appear elsewhere in the genome. They are notoriously hard for short-read mapping and even for long-read mapping, because a read's exact origin within the duplicate family is sometimes genuinely ambiguous — the copies are too similar. *Copy-number variants* (CNVs) in these regions are clinically meaningful; the example here, on chromosome 22, falls in a region implicated in the 22q11.2 deletion/duplication syndromes that affect heart, palate, and immune development.

The result in this section is qualitative — a single locus, walked through — but it is the most clinically vivid result in the paper. The locus is a 225 kb duplication segment in NA21886, confirmed by a clinical microarray as a copy gain. The authors run conventional pbmm2 mapping and portello on the same reads and visualize the coverage profile.

The pbmm2 view is unusable for CNV calling: a coverage spike of nearly **12,000-fold** (vs. an expected ~30× for the rest of the genome), followed by a coverage *dropout* across the genes DGCR6 and PRODH. This shape is characteristic of misplacement — reads from multiple copies of the segmental duplication pile onto a single reference homolog, while the reference homologs that should have received them are starved. A clinician looking at this in IGV would see noise.

The portello view shows a *3-fold* coverage region tracking the array segment. That is (i) a clean ~3× bump (consistent with three total copies, i.e. one extra copy on one haplotype), (ii) sized to match the array call, and (iii) *partitionable* by contig: because the reads are tagged with the contig they aligned through, you can split the pileup into its source contigs and check whether the contigs themselves represent a sequence compression. That last property — a contig-aware view of a CNV — is the new diagnostic capability portello unlocks beyond just "cleaner coverage".

#### Concept Diagram

<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="cnv-coverage-title">
  <title id="cnv-coverage-title">Coverage profile across the chr22 225 kb duplication: pbmm2 spike vs portello clean 3-fold.</title>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Coverage at the chr22 225 kb segdup CNV</text>
  <!-- pbmm2 panel -->
  <rect x="20" y="50" width="320" height="300" rx="10" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="180" y="76" text-anchor="middle" font-weight="700" fill="#991b1b">pbmm2 (conventional)</text>
  <!-- y-axis labels -->
  <text x="34" y="240" font-size="10" fill="#64748b">30×</text>
  <text x="34" y="200" font-size="10" fill="#64748b">90×</text>
  <text x="34" y="120" font-size="10" fill="#64748b">12,000×</text>
  <line x1="55" y1="100" x2="55" y2="320" stroke="#94a3b8" stroke-width="1"/>
  <line x1="55" y1="320" x2="320" y2="320" stroke="#94a3b8" stroke-width="1"/>
  <!-- Coverage trace: spike then dropout -->
  <polyline points="60,240 110,240 130,238 150,232 170,108 190,108 200,232 220,316 240,316 260,316 280,232 320,240"
            fill="none" stroke="#dc2626" stroke-width="2"/>
  <!-- Annotation -->
  <text x="180" y="98" text-anchor="middle" font-size="10" font-weight="600" fill="#dc2626">12,000× spike</text>
  <text x="240" y="338" text-anchor="middle" font-size="10" font-weight="600" fill="#dc2626">dropout: DGCR6 / PRODH</text>
  <!-- portello panel -->
  <rect x="380" y="50" width="320" height="300" rx="10" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="540" y="76" text-anchor="middle" font-weight="700" fill="#166534">portello (assembly-based)</text>
  <text x="394" y="240" font-size="10" fill="#64748b">30×</text>
  <text x="394" y="200" font-size="10" fill="#64748b">90×</text>
  <line x1="415" y1="100" x2="415" y2="320" stroke="#94a3b8" stroke-width="1"/>
  <line x1="415" y1="320" x2="680" y2="320" stroke="#94a3b8" stroke-width="1"/>
  <!-- Coverage trace: clean ~3x bump -->
  <polyline points="420,240 460,240 480,240 500,200 520,200 540,200 560,200 580,200 600,200 620,200 640,240 680,240"
            fill="none" stroke="#16a34a" stroke-width="2"/>
  <text x="540" y="190" text-anchor="middle" font-size="10" font-weight="600" fill="#166534">3× coverage = +1 copy</text>
  <text x="540" y="338" text-anchor="middle" font-size="10" fill="#475569">tracks the 225 kb array segment</text>
  <text x="360" y="368" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Schematic adapted from the paper's Figure 3; coverage shapes are representative, not pixel-exact.</text>
</svg>

### Key Takeaways

- **Conventional mapping crashes on segdups**: A 12,000× spike + adjacent dropout is the signature of read misplacement, not of the underlying biology.
- **Portello yields an interpretable 3×**: The CNV's true shape (one extra copy on one haplotype) shows up cleanly, sized to match the array call.
- **Contig-grouped pileup is new diagnostic information**: Splitting the pileup by source contig is unique to assembly-based read mapping and lets you sanity-check whether the assembly itself compressed the region.
- **Demonstration, not benchmark**: This is a single-locus illustration; the authors do not yet present a genome-wide CNV F1 number for portello.

---

## Methods

### Read Mapping Transfer Algorithm

#### Overview

Before the algorithm, a quick orientation: think of read-to-contig alignment as a function `R: read → contig coordinates`, and contig-to-reference alignment as `C: contig coordinate → reference coordinate`. The composition `C ° R` gives `read → reference coordinates` — that's portello's job. The two practical complications are (1) split alignments (a single read can be split across several segments of contig coordinates, and a single contig can be split across several reference segments) and (2) inconsistent indel representations between the two coordinate systems.

The algorithm, in three pieces:

1. **Pre-process the contig-to-reference mapping**. Two cleanup steps. *Repeated matches trimming*: for each pair of overlapping contig alignments to the reference, retain the alignment with higher gap-compressed identity and clip the others, ensuring each contig base is mapped to the reference at most once. (`pbmm2`, the recommended read-to-contig mapper, does the analogous step on its side, so each *read* base also maps once.) *Joining co-linear segments*: when minimap2 splits a contig alignment into pieces because of a Z-drop dip, but the pieces are still in the same orientation and order, portello rejoins them into a single segment, encoding any unmapped intervening contig sequence as an insertion. This both improves variant calling accuracy and makes downstream visualization saner.

2. **Compose the alignments**. For each read, walk through its alignment to its contig, and for each contig position the read covers, look up the contig-to-reference alignment to get a reference position. Concatenate the resulting per-position correspondences into a CIGAR string. Handle split contig alignments by emitting separate read-to-reference segments where appropriate.

3. **Normalize indels**. Both inputs follow the convention that insertions and deletions are *left-shifted* (placed at the leftmost coordinate consistent with the alignment). When a contig segment was mapped to the reference in *reverse* orientation, the read's indels need to be re-left-shifted in the reference frame to preserve this property — otherwise a region whose two haplotypes are represented by oppositely-oriented contigs would emit a mixture of left- and right-shifted variants, which downstream callers handle inconsistently.

The careful indel handling (step 3) is the kind of detail that doesn't show up until you actually run a caller on the output and notice that a region with two haplotypes pointing different directions is producing duplicated variants.

#### Concept Diagram

<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="meth-pipe-title">
  <title id="meth-pipe-title">Portello read-mapping transfer pipeline.</title>
  <defs>
    <marker id="meth-arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Read-mapping transfer pipeline</text>
  <!-- Inputs -->
  <rect x="20" y="60" width="200" height="60" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="120" y="86" text-anchor="middle" font-weight="600" fill="#92400e">read → contig BAM</text>
  <text x="120" y="106" text-anchor="middle" font-size="11" fill="#64748b">pbmm2, --eqx</text>
  <rect x="20" y="140" width="200" height="60" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="120" y="166" text-anchor="middle" font-weight="600" fill="#92400e">contig → reference BAM</text>
  <text x="120" y="186" text-anchor="middle" font-size="11" fill="#64748b">minimap2 -x asm5 --eqx</text>
  <!-- Step 1 -->
  <line x1="220" y1="170" x2="270" y2="170" stroke="#64748b" stroke-width="1.5" marker-end="url(#meth-arrow)"/>
  <rect x="280" y="135" width="160" height="70" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="360" y="160" text-anchor="middle" font-weight="600" fill="#1e40af">pre-process</text>
  <text x="360" y="178" text-anchor="middle" font-size="11" fill="#475569">trim repeated matches</text>
  <text x="360" y="194" text-anchor="middle" font-size="11" fill="#475569">join co-linear segments</text>
  <!-- Step 2 -->
  <line x1="120" y1="120" x2="120" y2="240" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,4"/>
  <line x1="360" y1="205" x2="360" y2="240" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,4"/>
  <rect x="220" y="240" width="280" height="60" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="2"/>
  <text x="360" y="266" text-anchor="middle" font-weight="700" fill="#6b21a8">compose: (C ° R) per read</text>
  <text x="360" y="284" text-anchor="middle" font-size="11" fill="#475569">handles split alignments; left-shifts indels</text>
  <!-- Output -->
  <line x1="500" y1="270" x2="540" y2="270" stroke="#64748b" stroke-width="1.5" marker-end="url(#meth-arrow)"/>
  <rect x="540" y="240" width="160" height="60" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>
  <text x="620" y="266" text-anchor="middle" font-weight="700" fill="#166534">read → reference BAM</text>
  <text x="620" y="284" text-anchor="middle" font-size="11" fill="#64748b">+ HP / PS tags</text>
  <text x="360" y="338" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">--eqx CIGAR (= / X) is required; no model retraining downstream.</text>
</svg>

#### Implementation

A toy of step 2 (composition) on a single read. The real implementation handles split alignments, reverse-strand mapping, and CIGAR encoding; this version exists to make the lookup geometry concrete.

```python
import numpy as np


def transfer_read_alignment(
    read_to_contig: np.ndarray,   # (L, 2) — (read_pos, contig_pos) per matched base
    contig_to_ref: np.ndarray,    # (M, 2) — (contig_pos, ref_pos) per matched base
) -> np.ndarray:
    """Compose read->contig and contig->reference into read->reference.

    Each input is a sorted table of base-level correspondences (the
    expanded form of a CIGAR with --eqx). For each read base, we look
    up the contig base it touches, then look up the reference base
    that contig base maps to. Bases without a contig->reference
    correspondence (insertions in the contig vs reference) are
    dropped; in the real implementation they would be encoded as
    insertions in the output CIGAR.
    """
    # Step 1: build a contig_pos -> ref_pos lookup. The contig table is
    # already sorted; np.searchsorted gives O(log M) per query.
    contig_keys = contig_to_ref[:, 0]

    # Step 2: for each read base, find the contig position it touches,
    # then resolve that contig position to a reference position.
    out: list[tuple[int, int]] = []
    for read_pos, contig_pos in read_to_contig:
        idx = np.searchsorted(contig_keys, contig_pos)
        # Drop read bases whose contig pos isn't in the contig->ref map
        # (these are insertions in the contig relative to the reference).
        if idx < len(contig_keys) and contig_keys[idx] == contig_pos:
            out.append((int(read_pos), int(contig_to_ref[idx, 1])))

    # Step 3: return as a (K, 2) array — sorted by read_pos by construction.
    return np.array(out, dtype=np.int64) if out else np.empty((0, 2), dtype=np.int64)
```

### Phase Set Construction

#### Overview

Before the algorithm, a quick orientation: a *phase set* is the contiguous reference region within which haplotype assignments (`HP=1`/`HP=2`) are internally consistent. Within a phase set, all the reads with `HP=1` are believed to come from the same parental haplotype; *between* phase sets, the labels reset (so `HP=1` in phase set A does not mean the same parent as `HP=1` in phase set B). The bigger and longer your phase sets, the more useful the phasing.

In partially-phased mode, portello builds phase sets by:

1. Find regions of the reference where exactly two contigs cover the same span (these are the regions where a haplotype assignment is even possible).
2. Within those regions, identify *heterozygous variants*: positions where the two contigs disagree with each other and at least one disagrees with the reference. Use these as anchor points.
3. Walk along adjacent het-variant pairs; if at least one read's read-to-contig alignment supports both the upstream and downstream contig allele *in the same way*, the pair is "linked" — extend the current phase set across it. If no read supports the linkage, start a new phase set.

Haplotype index (`HP=1` vs `HP=2`) is then assigned within each phase set by which of the two contigs each read aligned to. The conservative-overlap rule the paper describes — intervals overlap only if the intersection exceeds `min(24 kb, &#8531; of new interval length)` — is what stops a single small spurious overlap from collapsing two real contigs into one haplotype index.

This is roughly *read-backed phasing* (the standard whatshap recipe) but with the heterozygous variant set coming directly from the contig-to-reference alignment rather than a separate variant calling pass. That is a small but meaningful shift — the heterozygous calls are *implicit* in the assembly, so portello inherits them without an extra step.

### Key Takeaways

- **Composition is mostly bookkeeping**: The hard parts are split alignments and indel left-shifting around inverted contig segments — not the matrix multiply you'd expect.
- **`--eqx` is mandatory**: Both alignments must use `=`/`X` CIGAR ops, not `M`. The standard `M` op doesn't distinguish match from mismatch, which makes the composition ambiguous.
- **Phase sets are walks over het-variant pairs**: A read-backed extension scheme over implicit-from-contigs heterozygous variants — no separate variant call required.

---

## Discussion

### Overview

The paper's framing of its own contribution is interesting and worth taking seriously. The variant-calling accuracy gain — the number people will quote — is deliberately positioned as *one* benefit, not *the* benefit. The authors argue that the *operational* improvement (assembly-based and reference-based pipelines unified onto a consistent view of the sample) may matter more in the long run, because it removes the integration friction that has kept assembly out of clinical workflows.

There are two forward-looking claims the authors make that are worth holding lightly. First, they note that hybrid variant callers integrating contig and read inputs to portello are a natural next step — CNV calling being the most obvious target, since the chr22 example demonstrates how much information becomes available when reads are tagged with their source contig. They don't quantify this in the paper; they outline it as a direction. Second, they argue that with portello, a contig-based SV caller (PAV is cited) could be combined with a read-based small-variant caller, with all calls landing on the same coordinate system and the same review tools. This combination is *enabled* by portello rather than *demonstrated* by it.

The honest limitation: this paper is a method paper with two sample evaluations (HG002 and NA12878), one demonstrative CNV locus (NA21886), and a phasing benchmark on one of those samples. It is not a clinical study. The claim is "this should help rare-disease analysis", and the evidence supports the *should*, particularly in segdups and VNTRs, but a real evaluation on a rare-disease cohort — with diagnostic yield as the endpoint — remains future work. The CNV story in particular is a single locus; the paper does not yet present a genome-wide CNV F1 vs conventional methods.

There are also dependencies worth naming. Portello inherits the assembly's quality. If the assembly mis-resolves a haplotype switch, the read mapping inherits that error. The authors are explicit about this in the partially-phased section. A phasing-aware caller designed for portello inputs, plus better dual-assembly accuracy, are the two upstream shifts that would compound the wins shown here.

### Concept Diagram

<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" role="img" aria-labelledby="disc-roadmap-title">
  <title id="disc-roadmap-title">What portello unlocks: from current results to anticipated future capabilities.</title>
  <defs>
    <marker id="disc-arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="#64748b"/>
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1e293b">Portello: shown in this paper vs anticipated</text>
  <!-- Now -->
  <text x="80" y="64" font-weight="700" fill="#1e293b">Shown</text>
  <rect x="20" y="80" width="280" height="60" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="160" y="104" text-anchor="middle" font-weight="600" fill="#166534">DeepVariant: -47% small-var errors (HG002)</text>
  <text x="160" y="124" text-anchor="middle" font-size="11" fill="#475569">no model retraining</text>
  <rect x="20" y="160" width="280" height="60" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="160" y="184" text-anchor="middle" font-weight="600" fill="#166534">phasing as a side effect</text>
  <text x="160" y="204" text-anchor="middle" font-size="11" fill="#475569">block NG50 = 334 kb</text>
  <rect x="20" y="240" width="280" height="60" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="160" y="264" text-anchor="middle" font-weight="600" fill="#166534">CNV interpretability: 1 locus</text>
  <text x="160" y="284" text-anchor="middle" font-size="11" fill="#475569">illustrative, chr22 segdup</text>
  <!-- Arrows -->
  <line x1="300" y1="110" x2="380" y2="110" stroke="#64748b" stroke-width="1.5" marker-end="url(#disc-arrow)"/>
  <line x1="300" y1="190" x2="380" y2="190" stroke="#64748b" stroke-width="1.5" marker-end="url(#disc-arrow)"/>
  <line x1="300" y1="270" x2="380" y2="270" stroke="#64748b" stroke-width="1.5" marker-end="url(#disc-arrow)"/>
  <!-- Anticipated -->
  <text x="540" y="64" font-weight="700" fill="#1e293b">Anticipated</text>
  <rect x="380" y="80" width="320" height="60" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5"/>
  <text x="540" y="104" text-anchor="middle" font-weight="600" fill="#6b21a8">portello-aware small-variant caller</text>
  <text x="540" y="124" text-anchor="middle" font-size="11" fill="#475569">jointly modeling read-to-contig + contig-to-ref</text>
  <rect x="380" y="160" width="320" height="60" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5"/>
  <text x="540" y="184" text-anchor="middle" font-weight="600" fill="#6b21a8">unified SV + small-var calling</text>
  <text x="540" y="204" text-anchor="middle" font-size="11" fill="#475569">PAV (contigs) + DeepVariant (reads), one BAM</text>
  <rect x="380" y="240" width="320" height="60" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5"/>
  <text x="540" y="264" text-anchor="middle" font-weight="600" fill="#6b21a8">genome-wide CNV F1</text>
  <text x="540" y="284" text-anchor="middle" font-size="11" fill="#475569">contig-grouped pileups as training signal</text>
  <text x="360" y="340" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Right column: the authors flag these as natural directions; not benchmarked in this paper.</text>
</svg>

### Key Takeaways

- **Operational unification may be the bigger story**: The variant-calling number is what gets quoted, but the authors explicitly frame the unification of assembly-based and reference-based pipelines as the deeper benefit.
- **Hybrid callers are next**: A portello-aware caller that jointly models read-to-contig and contig-to-reference alignments is the natural follow-up; the paper outlines this rather than delivering it.
- **Method, not clinical, evidence**: The 47% number is a benchmark result, not a diagnostic-yield result. Whether it translates to more rare-disease diagnoses per 100 cases is the right question for the next study.
- **Quality compounds upstream**: Portello inherits assembly quality. A phasing-aware caller plus better dual-assembly accuracy would multiply with portello's gains rather than replacing them.

---

## Key Takeaways (Summary)

- **Composition over mapping**: Portello replaces a single hard problem (read → reference, mixing sequencing error and biological variation) with two easy ones (read → contig + contig → reference) and composes them.
- **47% / 29% small-variant error reduction, no model retraining**: DeepVariant on portello-remapped reads recovers about half of HG002's previously missed variants and a third of NA12878's, with false positives essentially flat.
- **Phasing as a free side effect**: The contig that a read aligned through is also a haplotype hint; portello carries `HP` and `PS` tags through the alignment transfer in one step.
- **Segdups become legible**: 12,000× pbmm2 spikes turn into clean 3× portello shoulders that match the array call — a qualitative leap for clinical CNV review.
- **The integration story is the integration story**: A reference-coordinate BAM produced via the assembly is what makes assembly-based analysis usable inside an existing reference-based pipeline. The variant-calling improvements are real, but the operational unification is what closes the loop.
