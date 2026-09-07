<p align="center">
  <img src="assets/readme/hero.svg" alt="youtube-to-weixin-article：把视频字幕和截图变成公众号文章与长图" width="100%">
</p>

# youtube-to-weixin-article

`youtube-to-weixin-article` 是一个面向内容团队的 Agent Skill，用来把 YouTube 视频、播客访谈、线上分享、字幕和截图，生成中文公众号图文稿，并输出可检查的公众号竖向长图。

它不是一个临时提示词，而是一个经过样本学习、独立生成、独立评分和反馈整改的 Skill 项目。项目包装参考了 [oil-skill-creator](https://github.com/oil-oil/oil-skill-creator) 的“创建、评审、整改、发布”思路，并参考 [beautify-github-readme](https://github.com/oil-oil/beautify-github-readme) 的 README 呈现方式：首页先讲清楚价值、证据链、使用路径和边界。

## 你会得到什么

| 交付物 | 说明 |
| --- | --- |
| 公众号文章 | 从字幕和视频资料中重组出中文标题、金句、导入、小节、截图位置和结尾。 |
| 公众号长图 | 生成 1200px 宽、单栏、字号稳定、不出框、可预览的竖向 PNG。 |
| 截图判断 | 识别哪些视频帧适合证明观点、解释界面、增强现场感，而不是随便配图。 |
| 来源控制 | 页尾显示公开来源链接，不暴露本地视频名、字幕名、截图名或本地路径。 |
| 评估流程 | 用实验组、测试组和独立评分窗口记录 Skill 是否真的有效。 |

## 三种使用模式

| 模式 | 什么时候使用 | 默认结果 |
| --- | --- | --- |
| 生成 | 用户提供视频、字幕、截图或链接，需要公众号文章和长图 | 输出 `article.md`、截图建议或截图文件、`article.long.png` |
| 评审 | 只想知道某次生成结果哪里不够好 | 只读评分与问题清单，不修改 Skill |
| 整改 | 用户确认某些问题要变成通用规则 | 修改 Skill，复验后更新文档并提交 |

评审默认不写文件。只有用户确认“写入 Skill”后，才把共性问题或明显缺陷沉淀成规则。

## 它重点解决什么

### 不是字幕翻译，而是公众号重写

普通总结容易按时间线复述字幕。这个 Skill 要求把材料改写成中文公众号读者能读下去的判断型文章：标题要有钩子，小节要像结论，截图要服务论证。

### 不是纯文字稿，而是图文成品

如果输入里有截图或视频源，长图不能只生成纯文字版本。可用截图必须进入长图，并且渲染后要检查文字出框、图片缺失、字号过小和来源展示问题。

### 不是自我打分，而是隔离评估

实验组是下载保存的原始公众号长图，测试组是在完全独立对话框里使用 Skill 生成的结果。评分窗口只看指定输入、输出和评分标准，不读取主对话分析或旧评分。

## 安装

```bash
npx skills add https://github.com/GhostWHO2012/podcast-article-full-flow --skill youtube-to-weixin-article
```

安装后可以这样调用：

```text
使用 youtube-to-weixin-article。
请只读取我指定的视频资料文件夹，生成公众号文章、截图建议和公众号竖向长图。
要求事实只来自我提供的材料；有截图或视频源时长图必须包含视频截图；页尾给公开来源链接，不要显示本地文件名。
```

## 推荐输入目录

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

最少需要提供字幕、转写文本或视频内容说明。若要生成可检查的公众号长图，最好同时提供截图目录，或者提供视频文件让智能体从视频中抽帧。

## 仓库结构

```text
.
├─ README.md
├─ PROJECT.md
├─ EXPERIMENT.md
├─ EVALUATION.md
├─ SKILL_REVIEW.md
├─ references/
│  ├─ README.md
│  ├─ weixin-article-rules.md
│  └─ project-packaging-standard.md
├─ evals/
│  ├─ README.md
│  └─ 2026-09-07-long-image-independent-review.md
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

## 证据链

| 文件 | 作用 |
| --- | --- |
| [`PROJECT.md`](PROJECT.md) | 项目定位、目标用户、能力边界和使用方式。 |
| [`EXPERIMENT.md`](EXPERIMENT.md) | 实验设计、样本材料、对比方法、主要发现和迭代记录。 |
| [`EVALUATION.md`](EVALUATION.md) | 独立评分流程、评分标准和汇总规则。 |
| [`SKILL_REVIEW.md`](SKILL_REVIEW.md) | 技能评审、问题定位、整改状态和发布检查。 |
| [`references/weixin-article-rules.md`](references/weixin-article-rules.md) | 从样本中沉淀出的标题、结构、截图、长图和来源规则。 |
| [`evals/2026-09-07-long-image-independent-review.md`](evals/2026-09-07-long-image-independent-review.md) | 独立窗口长图重评记录。 |
| [`youtube-to-weixin-article/SKILL.md`](youtube-to-weixin-article/SKILL.md) | 真正可安装、可复用的 Skill 指令。 |

## 实验流程

```text
原始公众号长图（实验组）
        ↓
提取目标风格：标题、结构、截图、排版、来源
        ↓
同源视频 + 字幕 + 截图资料
        ↓
独立对话框使用 Skill 生成长图（测试组）
        ↓
独立评分窗口盲评
        ↓
汇总反馈，用户确认后写回 Skill
```

这个流程的关键是隔离：生成窗口不读取评分结论，评分窗口不读取主对话分析，最终只把可复查、可确认的问题写回 Skill。

## 已沉淀规则

| 模块 | 规则 |
| --- | --- |
| 标题 | 不直译 YouTube 标题，而是围绕人物身份、数字、反差、读者问题和频道来源重新命名。 |
| 结构 | 不按时间线总结，把字幕重组为六到八个主题小节和中文判断句。 |
| 篇幅 | 常规成稿控制在约 4000 到 5500 中文字，即使字幕很长也要强压缩。 |
| 截图 | 优先选择数据、演示、工作流、生活/工作现场、动作手势帧，再考虑普通人物访谈帧。 |
| 长图 | 默认 1200px 宽，单栏排版，中文字号可读，渲染后必须人工检查。 |
| 来源 | 展示公开来源链接，不在正文或长图页尾显示本地路径、视频文件名、字幕文件名或截图文件名。 |

## 当前边界

- 不承诺自动找到所有 YouTube 原视频；如果材料中没有公开链接，需要用户提供或允许检索。
- 不把评分窗口的单次审美偏好直接写入 Skill。
- 不上传原始公众号长图、字幕、视频文件或本地受限素材到仓库。
- 不把“静态校验通过”说成“效果已经被完全证明”。
- 当前仓库没有伪造自动化 benchmark；已有评估记录来自独立窗口评分和人工整理。

## 当前状态

最近一次 Skill 静态校验：通过。

本仓库现在同时包含三类资产：可安装 Skill、可复查实验文档、可持续迭代的评分与整改记录。
