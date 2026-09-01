# Podcast Article Full Flow

本项目用于把本地播客/视频字幕整理成中文公众号风格的图文文章，并结合视频抽帧生成可预览的长图。

## 核心内容

- `题纲图文版/skills/podcast-article-with-screenshots/`：Codex Skill，定义完整文章生成流程。
- `outputs/svg_articles/local_html/_build_full_flow_package.py`：本地批量生成脚本。
- `outputs/svg_articles/local_html/_article_md_to_html.py`：Markdown 转长图 HTML 的渲染脚本。
- `outputs/svg_articles/local_html/_screenshot_local.py`：使用本机 Chrome 截取长图 PNG。
- `outputs/podcast_article_full_flow/`：完整流程生成的 Markdown 示例包。

## 生成原则

- 使用本地视频和字幕作为主要事实来源。
- 参考已下载文章的节奏、标题、配图克制程度，但不复制参考公众号名称、发布时间、微信链接或宣传内容。
- 自动抽帧只作为候选，最终配图应少而准。
- 配图必须有语义化图注，不显示技术文件名。

## 示例命令

```powershell
python "outputs/svg_articles/local_html/_build_full_flow_package.py" 04
```

输出默认放在：

```text
outputs/podcast_article_full_flow/<video-id>/
```
