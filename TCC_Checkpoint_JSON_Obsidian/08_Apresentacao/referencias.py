"""Referências do artigo (sem "Disponível em/Acesso em") e slides que as exibem."""

from __future__ import annotations

from pptx_kit import *

REFS = [
    ("ali", "ALI, Mohammed; ABDALLAH, Abdelrahman; JATOWT, Adam. **MemRevise: A Self-Revising "
     "Memory for Conversational Search**. arXiv:2610.24672v1, 2026."),
    ("arriola", "ARRIOLA, Marianne et al. **Block Diffusion: Interpolating Between "
     "Autoregressive and Diffusion Language Models**. arXiv:2503.09573v3, 2025."),
    ("demsar", "DEMŠAR, Janez. Statistical Comparisons of Classifiers over Multiple Data Sets. "
     "**Journal of Machine Learning Research**, v. 7, n. 1, p. 1–30, 2006."),
    ("fioresi", "FIORESI, Joseph et al. **Learning to Share: Selective Memory for Efficient "
     "Parallel Agentic Systems**. arXiv:2602.05965v2, 2026."),
    ("geng23", "GENG, Saibo et al. Grammar-Constrained Decoding for Structured NLP Tasks "
     "without Finetuning. In: **Proceedings of the 2023 Conference on Empirical Methods in "
     "Natural Language Processing**. Singapore: ACL, 2023. p. 10932–10952."),
    ("geng25", "GENG, Saibo et al. **JSONSchemaBench: A Rigorous Benchmark of Structured "
     "Outputs for Language Models**. arXiv:2501.10868v3, 2025."),
    ("gong", "GONG, Shansan et al. **Scaling Diffusion Language Models via Adaptation from "
     "Autoregressive Models**. arXiv:2410.17891v3, 2024."),
    ("holm", "HOLM, Sture. A Simple Sequentially Rejective Multiple Test Procedure. "
     "**Scandinavian Journal of Statistics**, v. 6, n. 2, p. 65–70, 1979."),
    ("hu", "HU, Yuanzhe; WANG, Yu; MCAULEY, Julian. **Evaluating Memory in LLM Agents via "
     "Incremental Multi-Turn Interactions**. arXiv:2507.05257, 2025."),
    ("hwang24", "HWANG, EunJeong et al. Enhancing Incremental Summarization with Structured "
     "Representations. In: **Findings of the Association for Computational Linguistics: EMNLP "
     "2024**. Miami: ACL, 2024. p. 3830–3842."),
    ("hwang25", "HWANG, EunJeong et al. SUMIE: A Synthetic Benchmark for Incremental Entity "
     "Summarization. In: **Proceedings of the 31st International Conference on Computational "
     "Linguistics**. Abu Dhabi: ACL, 2025. p. 10839–10864."),
    ("hwangdiao", "HWANG, Tao; DIAO, Yishi. **AMU: Admission and Memory Update for "
     "Personalized Conversations — Structured Memory with SLM Guided Control**. "
     "arXiv:2609.36976v2, 2026."),
    ("jayalath", "JAYALATH, Dulhan et al. PRISM: Efficient Long-Range Reasoning With "
     "Short-Context LLMs. In: **Proceedings of the 2025 Conference on Empirical Methods in "
     "Natural Language Processing**. Suzhou: ACL, 2025. p. 10196–10218."),
    ("kang", "KANG, Jingyi et al. **MemReader: From Passive to Active Extraction for Long-Term "
     "Agent Memory**. arXiv:2604.07877v2, 2026."),
    ("khanal", "KHANAL, Aja et al. **Agents of Diffusion: Enhancing Diffusion Language Models "
     "with Multi-Agent Reinforcement Learning for Structured Data Generation (Extended "
     "Version)**. arXiv:2601.07152v1, 2026."),
    ("leepfister", "LEE, Chunggi; PFISTER, Hanspeter. **AVERT: Audio-Verified Adjudication "
     "for Spoken Dialogue State Tracking**. arXiv:2609.01828v1, 2026."),
    ("leej", "LEE, Jemin et al. Exploring the Trade-Offs: Quantization Methods, Task "
     "Difficulty, and Model Size in Large Language Models From Edge to Giant. In: "
     "**Proceedings of the Thirty-Fourth International Joint Conference on Artificial "
     "Intelligence**. IJCAI, 2025. p. 8113–8121."),
    ("li", "LI, Jingguang et al. **CoEM: Empowering Long-Context Reasoning with "
     "Commit-on-Evidence Memory**. arXiv:2609.36935v2, 2026."),
    ("luq", "LU, Qingyu et al. **The Bitter Lesson of Diffusion Language Models for Agentic "
     "Workflows: A Comprehensive Reality Check**. arXiv:2601.12979v3, 2026."),
    ("luz", "LU, Zhenyan et al. **Small Language Models: Survey, Measurements, and "
     "Insights**. arXiv:2409.15790v3, 2025."),
    ("maharana", "MAHARANA, Adyasha et al. **Evaluating Very Long-Term Conversational Memory "
     "of LLM Agents**. arXiv:2402.17753, 2024."),
    ("muhoberac", "MUHOBERAC, Matthew et al. **State and Memory is All You Need for Robust "
     "and Reliable AI Agents**. arXiv:2507.00081, 2025."),
    ("mundler", "MÜNDLER, Niels; DEKONINCK, Jasper; VECHEV, Martin. **Constrained Decoding "
     "of Diffusion LLMs with Context-Free Grammars**. arXiv:2508.10111v1, 2025."),
    ("nie", "NIE, Shen et al. **Scaling up Masked Diffusion Models on Text**. "
     "arXiv:2410.18514v3, 2024."),
    ("petersen", "PETERSEN, Kai; VAKKALANKA, Sairam; KUZNIARZ, Ludwik. Guidelines for "
     "conducting systematic mapping studies in software engineering: An update. "
     "**Information and Software Technology**, v. 64, p. 1–18, 2015."),
    ("qin", "QIN, Bowen; LU, Yao. **MoM: Memory of Memory**. arXiv:2609.25054v1, 2026."),
    ("sharma", "SHARMA, Raghav; MEHTA, Manan. **Small Language Models for Agentic Systems: "
     "A Survey of Architectures, Capabilities, and Deployment Trade offs**. "
     "arXiv:2510.03847, 2025."),
    ("sumers", "SUMERS, Theodore R. et al. Cognitive Architectures for Language Agents. "
     "**Transactions on Machine Learning Research**, 2024."),
    ("wang", "WANG, Yubo et al. **CMI-Mem: Toward Generalizable Long-Term Memory Management "
     "via CMI-Augmented Reinforcement Learning**. arXiv:2607.20553v2, 2026."),
    ("wu", "WU, Di et al. **LongMemEval: Benchmarking Chat Assistants on Long-Term "
     "Interactive Memory**. arXiv:2410.10813v2, 2024."),
    ("xu", "XU, Xiucheng et al. **Chain-of-Memory: Lightweight Memory Construction with "
     "Dynamic Evolution for LLM Agents**. arXiv:2601.14287, 2026."),
    ("yang", "YANG, An et al. **Qwen3 Technical Report**. arXiv:2505.09388v1, 2025."),
    ("yuen", "YUEN, Sizhe et al. **Intrinsic Memory Agents: Heterogeneous Multi-Agent LLM "
     "Systems through Structured Contextual Memory**. arXiv:2508.08997v2, 2025."),
    ("zeng", "ZENG, Ruihong et al. **On the Structural Memory of LLM Agents**. "
     "arXiv:2412.15266, 2024."),
    ("zhangb", "ZHANG, Biao et al. **Encoder-Decoder Gemma: Improving the Quality-Efficiency "
     "Trade-Off via Adaptation**. arXiv:2504.06225v1, 2025."),
    ("zhangk", "ZHANG, Kehao et al. **Learning to Remember: End-to-End Training of Memory "
     "Agents for Long-Context Reasoning**. arXiv:2602.18493v2, 2026."),
    ("zhao", "ZHAO, Runze et al. **Accept Changes, Reject Attacks: Robust Memory Management "
     "for LLM Agents**. arXiv:2610.41056v1, 2026."),
    ("zheng", "ZHENG, Haobo et al. **SpeakerMem-R1: Speaker-Centered Dual-Track Memory for "
     "Multi-Party Dialogue**. arXiv:2609.26780v2, 2026."),
    ("zhou", "ZHOU, Qisheng; XIONG, Zhen; TAN, Qiaoyu. **DiffuPlan: Editable Planning State "
     "for Diffusion Language Model Agents**. arXiv:2610.24717v1, 2026."),
]
assert len(REFS) == 39

PRINCIPAIS = ["arriola", "demsar", "geng25", "holm", "hu", "hwang24", "hwang25", "jayalath",
              "luq", "luz", "yang", "zeng", "zhangb"]

_BY_KEY = dict(REFS)


def _two_columns(s, refs, y=1.5, h=5.35, size=11):
    half = (len(refs) + 1) // 2
    w = (CW - 0.35) / 2
    for i, chunk in enumerate((refs[:half], refs[half:])):
        text(s, MX + i * (w + 0.35), y, w, h, chunk, size=size, space_after=7,
             line_spacing=1.0)


def slide_principais(d):
    s = d.new("refs", "Referências", "Principais referências")
    _two_columns(s, [_BY_KEY[k] for k in PRINCIPAIS], h=4.95)
    text(s, MX, 6.5, CW, 0.4, "Lista completa (39 referências do artigo) no final do apêndice.",
         size=12, color=MUTED, italic=True, align="right")
    return s


def slides_apendice(d, first_code=21):
    per = 13
    for k in range(0, len(REFS), per):
        code = f"A{first_code + k // per}"
        part = k // per + 1
        s = d.new(f"refs_{part}", "Referências completas",
                  f"Referências do artigo ({part}/3)", code=code)
        _two_columns(s, [t for _, t in REFS[k:k + per]], size=10.5)
        d.apoio(s, [f"Referências {k + 1}–{min(k + per, len(REFS))} de {len(REFS)}, em "
                    "ordem alfabética, como no artigo (sem URL e data de acesso).",
                    "Use para localizar rapidamente a fonte citada em uma pergunta."])
