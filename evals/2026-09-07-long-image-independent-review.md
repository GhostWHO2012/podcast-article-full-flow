# 2026-09-07 长图独立重评

## 评估设置

评分任务：`独立评分-内容生成测试版长图-重评`

评分任务 ID：`01a079c3-735c-77a2-815b-9d9e3e1d2671`

评分方式：

- 新建独立任务窗口。
- 只查看 `N:\C\提纲图文版\内容生成测试版` 每个子文件夹里的 `article.long.png`。
- 不读取正文、字幕、README、技能文件、实验文档或旧评分。
- 不参考主对话里的历史判断。

## 实际查看文件

- `11_MichaelKratsios_WhiteHouseAI_重新生成长图/article.long.png`
- `12_AIEvals_ClaudeCode_公众号长图/article.long.png`
- `AndrewAmbrosino_OpenAI_CodexChatGPT_公众号长图/article.long.png`
- `ChatGPTWork_GPT56_Beginner_公众号长图/article.long.png`
- `DiannePenn_Anthropic_VerticalAI_公众号长图/article.long.png`

## 评分结果

| 长图 | 分数 | 一句判断 |
| --- | ---: | --- |
| `12_AIEvals_ClaudeCode_公众号长图` | 91 | 标题、观点和结构都很强，“eval 不是打分而是判断系统”有明确传播钩子，素材也服务论证。 |
| `DiannePenn_Anthropic_VerticalAI_公众号长图` | 87 | “AI 又要垂直化了”切口清晰，产品、组织和工作流观点连贯，公众号可读性很高。 |
| `ChatGPTWork_GPT56_Beginner_公众号长图` | 84 | 实用价值强，适合转给新手或团队管理者，但观点锋利度略弱。 |
| `AndrewAmbrosino_OpenAI_CodexChatGPT_公众号长图` | 82 | 对 Codex 和 ChatGPT 分工讲得完整，但标题抓力和章节差异化不够突出。 |
| `11_MichaelKratsios_WhiteHouseAI_重新生成长图` | 79 | 主题重要、结构完整，但政策表达偏稳，视觉节奏和观点冲击力相对弱。 |

## 总排名

1. `12_AIEvals_ClaudeCode_公众号长图`
2. `DiannePenn_Anthropic_VerticalAI_公众号长图`
3. `ChatGPTWork_GPT56_Beginner_公众号长图`
4. `AndrewAmbrosino_OpenAI_CodexChatGPT_公众号长图`
5. `11_MichaelKratsios_WhiteHouseAI_重新生成长图`

## 共性优点

- 标题区都有 2 到 3 条灰底金句，开头进入速度快，适合公众号长图首屏阅读。
- 章节标题普遍明确，基本能做到“每段一个判断”，不是纯摘要。
- 截图素材占比合理，能打断长文本疲劳。
- 版式统一，1200px 宽、正文栏宽、标题层级、图注和来源区都比较稳定，发布完成度高。

## 共性问题

- 多数长图视觉节奏偏固定：标题、金句、正文、截图、正文循环，后半段容易疲劳。
- 截图大多只是原始视频帧，少量图缺少二次标注、圈点或局部放大，信息增量还可以更高。
- 有些章节标题已经有观点，但正文仍偏解释型，缺少更短、更强的结论句。
- 结尾普遍偏总结来源，缺少公众号传播常见的强收束：一句可转发判断、行动建议或反常识回扣。

## 可考虑写回 Skill 的建议

- 首屏标题优先生成“反常识判断 + 对谁重要”，不要只概括主题。
- 每张长图至少加入 1 到 2 个“高亮解释型截图”，比如局部放大、圈点、标注关键界面或人物发言。
- 章节标题尽量写成完整判断句，例如“X 不是 Y，而是 Z”。
- 中后段加入一次视觉变奏，比如数据卡、对比表、流程图或大号结论条，缓解长图阅读疲劳。
- 结尾增加“可转发的最后一句”，把全文观点压成一句明确判断。

写回状态：暂未写回 Skill。需要用户确认哪些建议要作为通用规则。
