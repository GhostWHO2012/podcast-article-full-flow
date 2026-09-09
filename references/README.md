# references 说明

这个目录保存 `youtube-to-weixin-article` 的可复用规则和项目包装标准。

这里不存放晚点原文全文、原始公众号长图、字幕、视频文件或本地样本材料。原始材料只用于实验观察，仓库中只保留已经抽象成通用方法的规则，方便别人安装 Skill 后在不阅读学习样本的前提下复用。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `weixin-article-rules.md` | 标题、正文结构、截图、长图和来源展示规则。 |
| `wandian-learning-sources.md` | 晚点学习样本来源说明和对照关系。 |
| `project-packaging-standard.md` | 之后维护同类 Skill 项目时采用的 GitHub 包装标准。 |

## 使用原则

- `SKILL.md` 保留执行时最重要的指令。
- `references/` 保存更完整的判断依据和规则解释。
- 新评分或新样本不能直接进入规则库，必须先进入 `evals/` 或实验文档，经过确认后再沉淀。
