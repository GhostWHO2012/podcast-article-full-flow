# Evaluation Workflow

This file records how generated articles and long images should be scored before the observations are written back into `youtube-to-weixin-article`.

## Purpose

The evaluation workflow prevents the Skill from being changed based on one impression, one chat window, or one model's preference. Reviews can come from independent AI windows or manual reviewers, but the scoring record should make the process auditable.

## Independence Rule

Each reviewer should score independently.

Give each reviewer only:

- the original input material or a clear link to it;
- the generated article/long image being evaluated;
- the rubric below.

Do not show a reviewer previous scores, another AI's critique, or the planned Skill change before they submit their own judgment.

## Rubric

Use a 1-5 score for each dimension.

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Title | Direct translation or vague topic | Has a hook but weak tension | Strong Chinese reader-facing hook with authority, number, or tension |
| Source fidelity | Unsupported claims | Mostly grounded with a few vague areas | Claims, quotes, numbers, and examples are traceable to supplied materials |
| Article structure | Chronological summary or Q&A | Some thematic grouping | Clear judgment-driven sections with a readable editorial arc |
| Quote selection | Generic or invented | Useful but not central | Three grounded quotes that frame the article |
| Screenshot choice | Decorative or missing | Some useful placements | Screenshots prove, clarify, or humanize nearby points |
| Long-image layout | Text overflow, cramped type, missing images | Readable but uneven | 1200px-style single-column layout, readable type, no overflow, images embedded |
| Attribution | Local file names or unclear source | Source present but incomplete | Public title/channel/guest/link shown; no local filenames |

## Review Record Template

Copy one block per independent review.

```text
Review ID:
Reviewer type: AI / human
Reviewer name or tool:
Review date:
Sample/video:
Input shown to reviewer:
Output reviewed:

Scores:
- Title:
- Source fidelity:
- Article structure:
- Quote selection:
- Screenshot choice:
- Long-image layout:
- Attribution:

Main praise:
Main problems:
Suggested Skill change:
Should write back into Skill: yes / no / needs more evidence
```

## Consolidation Rule

Only write a finding into the Skill when one of these is true:

- multiple independent reviewers identify the same issue;
- the issue is directly visible in the output, such as text overflow, missing screenshots, or local filenames in the source line;
- the user explicitly chooses a preference after seeing the trade-off.

Do not write back isolated style preferences as universal rules.

## Current Verified Issues

| Issue | Evidence | Status |
| --- | --- | --- |
| Long image text can overflow narrow containers | Visual check from generated long image | Written into Skill |
| Long image can omit video screenshots | Generated long image had no screenshot despite source material | Written into Skill |
| Footer can expose local MP4/SRT filenames | Generated source line displayed local file names | Written into Skill |
| Subtitle length can tempt overlong articles | Comparison across learned samples | Written into Skill |

## Next Data To Add

When more external scoring is available, add:

- reviewer identity or model type;
- sample/video tested;
- scores per rubric dimension;
- exact issue observed;
- whether the issue was written into Skill.
