---
name: pubmed-search-casp
description: Use when the user provides an Exercise Prescription for Special Populations assessment brief, course slides or highlighted teaching materials, and a topic/population, and wants a complete PubMed search strategy, PubMed saved results, PRISMA-style screening, CASP quality appraisal, and final medium/high-quality included article files.
metadata:
  short-description: EPSP PubMed search, PRISMA screening, and CASP appraisal
---

# EPSP PubMed, PRISMA, and CASP Workflow

Use this skill when the task is to reproduce the full evidence-search workflow for an Exercise Prescription for Special Populations assignment.

The expected inputs are:
- Assessment brief or marking criteria.
- Course slides, handouts, or highlighted teaching material.
- Topic, population, or condition, such as elderly, frailty, falls, sarcopenia, COPD, diabetes, pregnancy, cancer, cardiac rehabilitation, or neurological populations.
- Any user preference about article type, year range, intervention type, or number of final papers.

## Core Rule

Do not invent articles, PMIDs, authors, CASP scores, PRISMA counts, or PubMed results. If a step depends on access to PubMed, the browser, or file-system permissions and that access is unavailable, state the limitation and use the closest transparent fallback only after recording it in the output notes.

If screening is based on abstracts only, label the screening and CASP appraisal as abstract-based.

## Standard Workflow

1. Read the assessment brief first.
   - Extract the required population, assignment aim, expected evidence type, marking criteria, word/poster requirements, and any required frameworks.
   - Identify whether the assignment expects exercise prescription, assessment/testing, rehabilitation, risk management, adherence, or clinical outcome emphasis.

2. Read the course materials.
   - Extract the course's preferred terminology, special population focus, exercise prescription principles, assessment tools, outcome measures, contraindications, and key themes.
   - Use the course content to guide relevance decisions, not to replace database evidence.

3. Define the review question.
   - Convert the topic into a PICO/PICo-style question where appropriate.
   - State Population, Intervention, Comparator if relevant, Outcomes, Study types, and context.

4. Create one final PubMed search strategy.
   - Use a balanced mix of MeSH terms and title/abstract terms.
   - Include synonyms for the population, condition, intervention, and outcomes.
   - Add filters only when justified by the assessment brief or user instruction.
   - Avoid over-narrowing the search unless the user needs a small result set.
   - Save the final strategy as Markdown, ideally to `~/Desktop`, using a clear name such as:
     `检索策略_<Population>_<Topic>.md`

5. Run the PubMed search.
   - Prefer the PubMed website and PubMed's native Save function.
   - Use Save settings:
     - Selection: `All results`
     - Format: `Summary`
     - Output: `.txt`
   - Save the downloaded file, ideally to `~/Desktop`, using a clear name such as:
     `PubMed_<Population>_<Topic>_all_results_summary.txt`
   - If PubMed native Save cannot be used, use NCBI E-utilities or another transparent PubMed export fallback, and clearly label that it is a fallback rather than native PubMed Save.

6. Gather abstracts for screening.
   - Use PMIDs from the saved Summary results.
   - Retrieve abstracts when needed for eligibility screening and CASP appraisal.
   - Save the abstract set as:
     `PubMed_<Population>_<Topic>_abstracts.txt`

7. Write inclusion and exclusion criteria.
   - Base criteria on the assessment brief, course materials, and the final review question.
   - Include at minimum:
     - Population.
     - Intervention/exposure.
     - Outcomes.
     - Study design.
     - Publication type.
     - Language/date limits if used.
     - Exclusion reasons.
   - Save as Markdown:
     `纳排标准_PRISMA_CASP_<Population>_<Topic>.md`

8. Screen with a PRISMA-style flow.
   - Deduplicate if multiple sources are used. If only PubMed is used, state that duplicate removal was not required or record any PubMed duplicates found.
   - Record counts for:
     - Records identified.
     - Records screened by title/summary.
     - Records excluded at title/summary stage.
     - Reports/articles assessed by abstract.
     - Reports excluded with reasons.
     - Articles entering CASP appraisal.
     - Articles excluded after CASP as low quality.
     - Final included medium/high-quality articles.
   - Create a PRISMA-style flow chart as SVG, and optionally PNG:
     `PRISMA_flowchart_<Population>_<Topic>.svg`

9. Apply CASP quality appraisal.
   - Select the appropriate CASP checklist based on study design:
     - RCT checklist for randomized trials.
     - Cohort checklist for cohort studies.
     - Case-control checklist for case-control studies.
     - Systematic review checklist for systematic reviews.
     - Qualitative checklist only when qualitative evidence is intentionally included.
   - Score transparently using categories such as:
     - `High`: strong relevance and mostly yes/clear answers.
     - `Medium`: relevant but with some unclear or moderate methodological concerns.
     - `Low`: major concerns, weak relevance, missing key methods, or insufficient abstract detail.
   - Retain only `Medium` and `High` quality articles.
   - Save CASP results as CSV:
     `CASP_medium_high_included_articles.csv`

10. Save final included article set.
    - Create a final TXT containing only retained medium/high-quality articles.
    - Keep PubMed Summary-style bibliographic information where possible.
    - Include PMID, title, authors, journal/year, abstract summary if available, relevance note, and CASP rating.
    - Save as:
      `PubMed_final_included_medium_high_summary.txt`

## Output Checklist

At the end, provide the user with links to these files:
- Search strategy Markdown.
- PubMed all results Summary TXT.
- Abstracts TXT if used.
- Inclusion/exclusion criteria Markdown.
- PRISMA flow chart SVG.
- CASP CSV for medium/high-quality retained articles.
- Final included medium/high-quality Summary TXT.

Also include a concise note stating:
- Search date.
- Database searched.
- Whether PubMed native Save was used.
- Whether screening/CASP was full-text-based or abstract-based.
- Final number of included medium/high-quality articles.

## Suggested User Prompt

When the user wants to trigger this workflow, they can say:

```text
请使用 pubmed-search-casp 工作流。我的 assessment brief 是 [文件]，我想重点参考的课件是 [文件1、文件2、文件3]，主题/人群是 [主题]。请完成：
1. 确定最终 PubMed 检索策略并保存为 Markdown；
2. 用该策略在 PubMed 检索，并用 PubMed Save 保存 all results + Summary 格式 TXT；
3. 根据 brief 和课件写纳排标准；
4. 按 PRISMA 做筛选流程图；
5. 对筛选后的文章做 CASP 评价，只保留 medium 和 high quality；
6. 输出最终保留文章 TXT 和 CASP CSV。
如只能基于摘要筛选和评价，请明确标注 abstract-based。
```
