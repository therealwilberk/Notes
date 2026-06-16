# Paper & Article Summaries

Use this process when the user provides a URL, PDF, or paper to summarize.

## Process

1. **Fetch** the content (webfetch for URLs, read for local files, websearch if needed)
2. **Analyze** -- extract the core thesis, key arguments, methodology (if research paper), and conclusions
3. **Summarize** in the vault's note style: plain third-person, no fluff, no emojis

## Summary Structure

A summary file goes in an appropriate `Notes/<Category>/` directory. For a paper on ML monitoring, that's `Notes/Programming/ML/`. For a general article, use `Notes/Reference/`.

### Header

```yaml
---
tags: [summary, topic1, topic2]
aliases: ["Paper Title (short)"]
source: "https://..." or "path/to/file.pdf"
created: YYYY-MM-DD
status: complete
---
```

### Content Sections

```
# Paper Title

Source: [link](url)

## Thesis

One or two sentences. What is the paper/article trying to prove or do?

## Key Points

- Bullet 1: major finding or argument
- Bullet 2: supporting evidence
- Bullet 3: counterpoint or limitation acknowledged
- ...

## How It Applies

If the paper is directly relevant to the user's stack, this section is critical:
- Specific techniques to adopt or avoid
- Code patterns or architecture decisions influenced by this paper
- Contradictions with current project approach

## Caveats & Limitations

- What the paper does NOT address
- Assumptions that may not hold in production
- Conflicts with other known sources
```

## Style Rules

- Do not pad -- keep summary under 1/10 the original length
- Quote sparingly (1-2 direct quotes max). Paraphrase everything else.
- Link to the original source prominently at the top
- The "How It Applies" section is the most valuable part for future reference
- If the paper introduces a technique the vault already covers (e.g., PSI drift detection), cross-link: `See [[ml-evidently]] for PSI thresholds`

## Git Commits

After adding a summary, commit with:
```
summary: add <Paper/Article Title>
```
