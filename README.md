<p align="center">
  <img src="assets/readme/hero.svg" alt="youtube-to-weixin-article: from YouTube transcripts and video frames to WeChat articles and long images" width="100%">
</p>

# youtube-to-weixin-article

`youtube-to-weixin-article` is a Codex/Agent Skill for turning YouTube videos, podcast interviews, webinars, subtitles, screenshots, and reference WeChat articles into Chinese public-account drafts and publish-preview long images.

It is built from real comparison work: original YouTube titles and timelines, bilingual subtitles, `article.md` drafts, video screenshots, and downloaded WeChat long images were compared, distilled, tested, and written into a reusable Skill.

## What It Produces

| Output | What It Is For |
| --- | --- |
| `article.md` | A Chinese WeChat-style article with title, opening quotes, thematic sections, screenshot placements, source line, and `写在最后`. |
| `images/` | Curated video frames or screenshots used by the article. |
| `article.long.png` | A vertical long image preview suitable for WeChat publishing review. |

The Skill does not translate subtitles line by line. It rewrites long video material into judgment-driven Chinese editorial prose.

## Why This Exists

Most long-video summarizers stop at chronology: what happened at 00:00, 05:00, 12:00. The learned reference articles work differently.

They:

- rename the English title into a Chinese reader-facing hook;
- select three grounded opening quotes;
- compress host questions into context;
- reorganize subtitles into six to eight thematic sections;
- choose screenshots because they prove, clarify, or humanize a point;
- render a readable 1200px-wide long image without text overflow;
- show public source links, not local file names.

## Evidence Trail

| Document | Purpose |
| --- | --- |
| [`EXPERIMENT.md`](EXPERIMENT.md) | Records the experiment goal, sample material, comparison method, learned rules, iteration history, and validation. |
| [`EVALUATION.md`](EVALUATION.md) | Defines how independent AI/window/manual scoring should be collected without cross-contamination. |
| [`youtube-to-weixin-article/SKILL.md`](youtube-to-weixin-article/SKILL.md) | The actual reusable Skill instructions. |

## Install

```bash
npx skills add https://github.com/GhostWHO2012/podcast-article-full-flow --skill youtube-to-weixin-article
```

Then call it naturally:

```text
使用 youtube-to-weixin-article，把这个视频资料生成公众号图文和长图。
```

## Recommended Input Folder

```text
video-case/
  youtube链接.txt
  video.bilingual.srt
  video.srt
  video.zh.srt
  video.mp4
  images/
    01.png
    02.png
  article.md
  原文长图.png
  raw.html
```

Minimum input: one transcript/subtitle file or a video source that can be transcribed. For publish-ready long images, provide either screenshots or the source video so frames can be selected.

## Typical Request

```text
使用 youtube-to-weixin-article。
请只读取这个文件夹里的资料，生成：
1. article.md
2. 可用的视频截图或截图建议
3. 一张公众号竖向长图 PNG

要求：
- 不要编造事实。
- 不要按时间线翻译字幕。
- 如果有截图或视频源，长图里必须嵌入视频截图。
- 页尾给公开来源链接，不要显示本地视频文件名或字幕文件名。
```

## Learned Writing Rules

| Area | Rule |
| --- | --- |
| Title | Do not directly translate the YouTube title. Reframe it around authority, number, tension, reader problem, and source marker. |
| Structure | Convert subtitles into thematic editorial sections instead of chronological notes. |
| Density | Keep common finished drafts around 4,000 to 5,500 Chinese characters even when subtitles are very long. |
| Screenshots | Prefer proof, demos, charts, workflow screens, life/work scenes, gesture frames, and only then generic talking-head frames. |
| Long image | Default to 1200px width, single-column layout, readable Chinese type, and visual inspection after rendering. |
| Attribution | Show public source links. Never print local paths, MP4 file names, SRT file names, or screenshot file names in reader-facing output. |

## Repository Structure

```text
.
├─ README.md
├─ EXPERIMENT.md
├─ EVALUATION.md
├─ assets/
│  └─ readme/
│     └─ hero.svg
└─ youtube-to-weixin-article/
   ├─ SKILL.md
   ├─ agents/
   │  └─ openai.yaml
   └─ scripts/
      └─ render_weixin_long_image.py
```

## Long Image Requirements

The long-image output is part of the deliverable, not a decorative preview.

- Use a clean single-column article layout.
- Keep body text out of narrow cards.
- Wrap text by the actual container width.
- Embed usable screenshots when screenshots or video are available.
- Inspect the rendered PNG for overflow, cropped text, missing images, overlapping captions, and unreadable type.
- Use public source links in the footer.

## Evaluation Workflow

Scoring can happen in separate AI chats, separate windows, or manual review sessions. To prevent one score from influencing another, each reviewer should only see:

1. the input material;
2. the generated output;
3. the scoring rubric.

They should not see previous scores, another AI's critique, or the planned Skill change before submitting their own review. The consolidated scoring record belongs in [`EVALUATION.md`](EVALUATION.md).

## Status

Current Skill validation:

```text
Skill is valid!
```

This repository is maintained as both a usable Skill package and a record of the experiment that produced it.
