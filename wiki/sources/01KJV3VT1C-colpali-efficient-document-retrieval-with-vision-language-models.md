---
type: source
title: 'ColPali: Efficient Document Retrieval with Vision Language Models'
source_id: 01KJV3VT1CZCW1CH2F11Y2B6ND
source_type: paper
authors:
- Manuel Faysse
- Hugues Sibille
- Tony Wu
- Bilel Omrani
- Gautier Viaud
- Céline Hudelot
- Pierre Colombo
published_at: '2024-06-27 00:00:00'
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- knowledge_and_memory
- multimodal_models
- retrieval_augmented_generation
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# ColPali: Efficient Document Retrieval with Vision Language Models

**Authors:** Manuel Faysse, Hugues Sibille, Tony Wu, Bilel Omrani, Gautier Viaud, Céline Hudelot, Pierre Colombo
**Published:** 2024-06-27 00:00:00
**Type:** paper

## Analysis

# ColPali: Efficient Document Retrieval with Vision Language Models
2024-06-27 · paper · Manuel Faysse, Hugues Sibille, Tony Wu, Bilel Omrani, Gautier Viaud et al. (7 total)
https://arxiv.org/pdf/2407.01449

---

### Motivation & Prior Limitations
Modern document retrieval systems are fundamentally bottlenecked not by embedding model quality but by the brittle, multi-stage ingestion pipeline required to extract text from visually rich PDFs before any embedding occurs.
- Standard industrial RAG pipelines chain together PDF parsers, layout detection models, OCR engines, chunking strategies, and optional captioning steps — each adding latency and failure surface, with captioning alone taking dozens of seconds per page.
  - Experiments show that optimizing the ingestion pipeline yields larger ViDoRe performance gains than optimizing the text embedding model, making the pipeline itself the primary constraint.
- Text-centric retrieval systems discard or poorly handle key visual signals: figures, tables, infographics, page layouts, and fonts that human readers rely on to understand documents.
  - Contrastive VLMs evaluated on ViDoRe (Jina-CLIP, Nomic Embed Vision) score as low as 12.9–17.7 avg nDCG@5, far below pipeline-based systems, because their visual encoders are not optimized for text understanding within images.
- No prior benchmark evaluated document retrieval end-to-end across diverse document types, visual modalities, and languages in realistic industrial settings.
  - Existing benchmarks either target natural images (COCO, Flickr) or text passages (BEIR, MTEB), leaving the visually rich document retrieval regime unmeasured.

---

### Proposed Approach
ColPali reframes document retrieval as retrieval in vision space: document pages are embedded directly as images using a Vision Language Model, producing multi-vector patch-level representations matched to queries via late interaction — eliminating the ingestion pipeline entirely.
- The model extends PaliGemma-3B (SigLIP-So400m/14 vision encoder projecting into Gemma-2B's text space) with a linear projection layer that maps each LLM output token embedding — whether from text or image patch tokens — to a shared 128-dimensional retrieval space.
  - This builds on the ColBERT late interaction paradigm: one embedding vector per image patch is stored offline; at query time, similarity is computed as the sum over query tokens of their maximum dot product with all document patch embeddings (MaxSim).
  - The critical insight is that PaliGemma's multimodal fine-tuning aligns image patch representations into the same latent space as text tokens, making the ColBERT late interaction operator meaningful across modalities without architectural surgery.
- Training uses 118,695 query-page pairs (63% open academic datasets, 37% VLM-synthesized pseudo-questions from web-crawled PDFs) with a pairwise cross-entropy contrastive loss over the hardest in-batch negative, LoRA adapters on transformer layers, and query augmentation tokens inherited from ColBERT.
  - The vision encoder is kept frozen during training; only LoRA adapters on the LLM and the projection layer are updated, keeping training tractable on 8 GPUs for 1 epoch.
- ViDoRe, the accompanying benchmark, evaluates page-level retrieval across 10 tasks spanning text, figures, infographics, tables, multiple domains (medical, scientific, financial, administrative), and two languages (English, French), with both repurposed VQA datasets and newly constructed practical RAG-style tasks.

---

### Results & Capabilities
ColPali achieves 81.3 avg nDCG@5 on ViDoRe, outperforming the best pipeline-based baseline (Unstructured + Captioning + BGE-M3 at 67.0) by over 14 points and all contrastive VLMs by large margins, while being dramatically simpler and faster to index.
- The largest gains appear on visually complex tasks: ArxivQA (+39 over best baseline), InfographicVQA (+10 over captioning), and TabFQuAD (+14.8 over captioning), confirming that multi-vector patch-level embeddings capture visual structure that text extraction cannot recover.
- Offline indexing latency is 0.39 seconds per page for ColPali versus 7.22 seconds for the full Unstructured pipeline (18× faster), because page images are encoded in a single forward pass with no preprocessing; online query latency is approximately 30 ms, comparable to BGE-M3's 22 ms.
- The ablation sequence reveals additive contributions: fine-tuning SigLIP alone on document data (BiSigLIP) reaches 58.6 avg; adding LLM contextualization as a bi-encoder (BiPali) reaches 58.8 but improves French zero-shot generalization substantially; adding late interaction (ColPali) jumps to 81.3, a +22.5 step-change attributable to per-patch multi-vector representations.
- Replacing PaliGemma-3B with Qwen2-VL-2B using the same training strategy (ColQwen2-VL) yields a further +5.3 nDCG@5, demonstrating that stronger generative VLMs directly translate to stronger visual retrievers.
- Token pooling reduces stored embeddings by 66.7% (pool factor 3) while retaining 97.8% of retrieval performance, making storage footprint (257.5 KB/page at full resolution) practically manageable.
- Late interaction heatmaps are interpretable: ColPali correctly focuses on OCR regions matching query terms and on non-trivial visual features like axis labels, enabling per-token attribution of retrieval scores to specific image patches.

---

### Implications
ColPali establishes a new paradigm — retrieval in vision space — that could make the entire document ingestion pipeline (OCR, layout detection, chunking, captioning) obsolete for RAG and search applications, substantially reducing system complexity and failure surface.
- The result that late interaction over patch embeddings outperforms captioning by a large margin suggests that dense visual token representations carry more retrieval signal than natural language descriptions of the same content, with implications for how multimodal RAG systems should be ar

## Key Claims

1. Modern document retrieval systems mainly rely on textual information extracted from document pages and struggle to exploit key visual cues efficiently.
2. In practical industrial settings, the primary performance bottleneck for efficient document retrieval stems from the data ingestion pipeline, not from embedding model performance.
3. Optimizing the data ingestion pipeline yields much better performance on visually rich document retrieval than optimizing the text embedding model.
4. No existing benchmark evaluates document retrieval systems in practical settings end-to-end, across several document types and topics, and by evaluating the use of both textual and visual document fea
5. ColPali achieves an average nDCG@5 of 81.3 on ViDoRe, outperforming the best text-based baseline (Unstructured + Captioning + BGE-M3) which scores 67.0.
6. ColPali offline document indexing latency is 0.39 seconds per page, compared to 7.22 seconds for a PDF parser pipeline with layout detection, OCR, and captioning.
7. ColPali architecture extends PaliGemma-3B by adding a projection layer that maps each language model output token embedding to a reduced dimension D=128, enabling ColBERT-style multi-vector representa
8. ColPali is trained using an in-batch contrastive loss based on the hardest negative sample (pairwise CE loss), which outperforms standard in-batch negative contrastive loss by 1.6 nDCG@5.
9. ColPali's training dataset consists of 118,695 query-page pairs: 63% from openly available academic datasets and 37% synthetic, generated from web-crawled PDFs with VLM-generated pseudo-questions.
10. ColPali is trained using LoRA with alpha=32 and rank=32 on transformer layers, enabling parameter-efficient fine-tuning of PaliGemma-3B for retrieval.

## Capabilities

- Vision Language Models can directly embed document page images into multi-vector representations for retrieval, bypassing OCR, layout detection, and chunking pipelines entirely
- Late interaction (ColBERT-style) applied to VLM image patch embeddings achieves 81.3 nDCG@5 on visual document retrieval, outperforming best text-based pipelines (67.0) by over 14 points across 10 tasks
- Image-based document indexing with VLMs achieves ~18x faster offline indexing versus standard PDF parsing pipelines (0.39s vs 7.22s per page)
- End-to-end differentiable document retrieval pipeline enabling domain-specific fine-tuning directly on the downstream retrieval objective — adding 1552 French table samples yielded +2.6 nDCG@5 improvement with no degradation elsewhere
- Token pooling on image patch embeddings reduces multi-vector storage by 66.7% with only 2.2% retrieval performance loss on average
- Visual document retrieval model trained only on English data generalizes zero-shot to French document retrieval tasks via LLM backbone's pretrained multilingual knowledge
- Late interaction scoring between query tokens and image patches provides interpretable visual heatmaps identifying which document regions are most relevant to specific query terms
- Stronger generative VLM backbones directly translate to stronger visual retrieval when adapted via ColPali training strategy — ColQwen2-VL 2B achieves +5.3 nDCG@5 over ColPali with same training procedure

## Limitations

- Standard document retrieval pipelines treat visual elements (figures, tables, images) as noise and filter them out entirely, losing critical information conveyed through non-textual means
- PDF parsing/ingestion pipelines (OCR, layout detection, chunking, captioning) are the actual primary bottleneck in document RAG at 7+ seconds per page — not the embedding model — so optimizing embedding models alone yields minimal gains
- Token pooling for multi-vector visual retrieval degrades significantly on text-dense documents — the Shift dataset (most text-dense) is a clear outlier with worse performance degradation relative to other datasets
- ColPali requires storing 257.5 KB per document page as multi-vector embeddings — a 10-100x storage overhead versus single-vector bi-encoders — limiting practical corpus scale without compression
- Halving image patch count from 1024 to 512 causes a severe -24.8 nDCG@5 performance degradation, creating a hard quality-efficiency tradeoff cliff with no graceful degradation regime
- Applying late interaction directly to contrastive vision model patch embeddings (ColSigLIP) completely fails — the approach works only when patch representations are LLM-aligned via next-token prediction pretraining
- No confidence estimation or abstention mechanism exists for visual retrieval systems, blocking reliable production deployment in RAG applications where hallucination control is critical
- No end-to-end visual RAG pipeline exists — visual retrieval (ColPali) and visual question answering are not yet combined into a system processing documents entirely from image features
- Contrastive VLMs (Jina-CLIP: 17.7, Nomic-vision: 12.9 nDCG@5) are near-complete failures on document retrieval tasks versus ColPali's 81.3 — these models are not optimized for text understanding within images
- VLMs adapted for retrieval via contrastive fine-tuning on 119K samples underperform natively contrastively pretrained models on English tasks — a 5-orders-of-magnitude gap in contrastive training data creates a structural disadvantage
- Unfreezing the vision encoder during retrieval fine-tuning slightly degrades performance at current training data scales, blocking full end-to-end optimization of the vision component
- ViDoRe evaluates only page-level retrieval; sub-page passage-level visual retrieval within long or multi-column documents is completely absent from the benchmark scope
- ColPali's multilingual capability is entirely dependent on zero-shot transfer from the LLM backbone — no multilingual visual retrieval training data exists, and benchmark coverage is limited to English and French

## Bottlenecks

- Document ingestion pipeline (OCR, layout detection, chunking, captioning) is the actual primary bottleneck in practical visual document RAG — 7+ seconds per page — not the embedding model; optimizing embeddings alone cannot address this
- Multi-vector storage footprint for visual document retrieval (257.5 KB/page) limits corpus scale; compression introduces quality tradeoffs that are particularly pronounced for text-dense documents
- Image patch count is a fundamental quality-efficiency tradeoff bottleneck: patch reduction causes severe performance degradation (-24.8 nDCG@5 for 512 vs 1024 patches) with no graceful degradation regime
- No benchmark existed for evaluating document retrieval systems end-to-end on visual elements in practical settings before ViDoRe, blocking systematic progress measurement and fair method comparison
- Absence of confidence estimation for visual retrieval outputs blocks reliable abstention in production RAG — systems cannot know when to withhold answers due to low retrieval confidence

## Breakthroughs

- ColPali demonstrates that document retrieval can be done purely from image embeddings via VLMs with late interaction, bypassing the entire OCR/parsing/chunking pipeline while achieving dramatically better performance on visually complex documents
- ViDoRe: first benchmark evaluating document retrieval end-to-end on visual elements across multiple domains, languages, and document types in practical industrial settings — revealing that contrastive VLMs nearly completely fail at this task

## Themes

- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/bm25|BM25]]
- [[entities/lora|LoRA]]
- [[entities/retrieval-augmented-generation|Retrieval Augmented Generation]]
- [[entities/siglip|SigLIP]]
