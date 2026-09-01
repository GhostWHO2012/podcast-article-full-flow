#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


ROOT = Path("N:/C/提纲图文版")
OUT_ROOT = ROOT / "outputs/podcast_article_full_flow"
SKILL_SCRIPT = ROOT / "题纲图文版/skills/podcast-article-with-screenshots/scripts/auto_screenshot.py"
HTML_RENDER = ROOT / "outputs/svg_articles/local_html/_article_md_to_html.py"
SCREENSHOT = ROOT / "outputs/svg_articles/local_html/_screenshot_local.py"


CONFIG = {
    "01": {
        "stem": "01_EnterpriseSales_JenAbel",
        "slug": "01_EnterpriseSales_JenAbel_full.png",
        "keywords": "企业销售,销售,客户,演示,采购,合同,SpaceX,法务,10万美元,Lenny,JJellyfish",
        "title": "JJellyfish 联合创始人：如何一步步拿下10万美元以上的企业级交易丨Lenny’s Podcast",
        "thesis": "Jen Abel 的核心方法是，把企业销售从五阶段漏斗还原成客户真实采购过程，用慢下来的前期情报换来更快、更稳的成交。",
        "final_image_count": 3,
        "captions": [
            "开场访谈画面。Jen Abel 用一笔面向 SpaceX 法务团队的假想订单，拆解企业销售真正发生的细节。",
            "中段讨论企业销售流程。画面用于承接“先理解客户采购过程，再安排演示和报价”的方法。",
            "后段观点转折。Jen 强调大单成交不是靠一次漂亮演示，而是靠多轮沟通建立内部共识。",
        ],
    },
    "02": {
        "stem": "02_Solopreneur_StarterStory",
        "slug": "02_Solopreneur_StarterStory_full.png",
        "keywords": "独立开发者,月收入,2.2万美元,工作方式,效率,夜猫子,旅居,客服,产品,Starter Story",
        "title": "月入2.2万美元，不早起、不卷自律：他是怎么工作的？丨Starter Story",
        "thesis": "Rob 的经验说明，一个人经营业务的关键不是复制效率模板，而是找到自己的有效时间、稳定环境和可长期重复的无聊动作。",
        "final_image_count": 3,
        "captions": [
            "Rob 的访谈画面。文章开篇用它建立人物感，并引出“反效率模板”的工作方式。",
            "讨论旅居和工作节奏的段落。画面用于说明独立开发者的难点不是自由，而是如何维持稳定交付。",
            "后段谈产品和日常运营。Rob 的经验提醒，真正推动业务的往往是客服、修 bug、做页面这类重复小事。",
        ],
    },
    "03": {
        "stem": "03_MarketingChannels_HitenShah",
        "slug": "03_MarketingChannels_HitenShah_full.png",
        "keywords": "营销,渠道,内容,融资,创业,AI,TikTok,Dropbox,Nira,Kissmetrics,Crazy Egg",
        "title": "Crazy Egg创始人：最佳营销渠道都是秘密丨Delphi",
        "thesis": "Hiten Shah 的核心提醒是，增长不是抄一个公开渠道，而是持续训练发现渠道、验证假设和接触真实用户的能力。",
        "final_image_count": 3,
        "captions": [
            "Hiten Shah 与主持人开场。嘉宾过往经历横跨 Crazy Egg、Kissmetrics、Nira 和 Dropbox，适合放在人物与背景介绍之后。",
            "访谈棚内的双人画面。Hiten 讨论自有资金、风险投资和公司环境时，强调创始人要直面现实反馈。",
            "中后段讨论 AI 和创业判断。画面用于承接“AI 让试错更快，但判断仍要靠行动校准”的主题。",
        ],
    },
    "04": {
        "stem": "04_ConsumerIdeas_YC",
        "slug": "04_ConsumerIdeas_YC_full.png",
        "keywords": "YC,创业点子,消费者,需求,用户,产品,创业,市场,Michael,Dalton",
        "title": "YC前负责人：如何找到 to C 的创业点子丨Dalton + Michael",
        "thesis": "Dalton 和 Michael 的核心提醒是，消费级创业点子不是靠头脑风暴憋出来，而是从真实痛点、强烈需求和创始人自己的生活缝隙里长出来。",
        "final_image_count": 3,
        "captions": [
            "YC 访谈开场画面。两位嘉宾围绕消费级创业点子，讨论为什么很多看似小的需求其实藏着大机会。",
            "中段讨论用户需求和创始人直觉。画面用于承接“先找到真实痛点，再判断产品是否值得做”的方法。",
            "后段观点收束。消费产品的关键不是概念漂亮，而是用户是否愿意反复回来。",
        ],
    },
    "05": {
        "stem": "05_AIWorkflow_SiliconValleyGirl",
        "slug": "05_AIWorkflow_SiliconValleyGirl_full.png",
        "keywords": "AI,工作流,Agent,自动化,产品,流程,提示词,Claude,ChatGPT,系统,Skill",
        "title": "把AI变成工作系统的6个步骤丨Silicon Valley Girl",
        "thesis": "这期内容的核心价值是，把 AI 从一次性问答变成可重复运行的工作系统：先拆流程，再写规则，最后让工具稳定执行。",
        "final_image_count": 3,
        "captions": [
            "开场画面。主题从“使用 AI 工具”转向“搭建可重复的 AI 工作系统”。",
            "中段讨论 Agent 和流程化工作。配图用于说明 AI 的价值来自被嵌入具体任务，而不是单次聊天。",
            "后段谈 Skill 与自动化。真正能复利的不是提示词灵感，而是可以每周重复调用的流程资产。",
        ],
    },
    "06": {
        "stem": "06_SocialAI_SarahTavel",
        "slug": "06_SocialAI_SarahTavel_full.png",
        "keywords": "AI,社交,网络效应,ChatGPT,Custom GPT,产品,社区,健康,Pinterest,Benchmark",
        "title": "Benchmark 合伙人：为什么下一个爆款AI产品将具备社交功能丨Every",
        "thesis": "Sarah Tavel 的判断是，当模型能力逐渐够用，消费级 AI 的竞争会从底层技术转向产品直觉、可信社区和可复用的使用方法。",
        "captions": [
            "Every 访谈开场。Sarah Tavel 从消费互联网周期切入，讨论 AI 产品何时从技术主导转向产品主导。",
            "Sarah Tavel 访谈画面。她强调普通用户不会长期研究提示词，产品应该把高手经验变成一眼可用的界面。",
            "后段讨论网络效应和消费级 AI。社交层的价值不在热闹，而在让方法、信任和声誉形成循环。",
        ],
    },
}


PROMO_PATTERNS = [
    r"作者/公众号",
    r"发布时间",
    r"原文",
    r"mp\.weixin\.qq\.com",
    r"晚点再听",
    r"LaterCast",
    r"每天挑选一期",
    r"每天为你更新",
    r"收藏进\s*晚点再听",
    r"现在没空.*收藏",
    r"关注我",
    r"晚点再听.*通勤",
    r"通勤、走路或做家务",
    r"一次性听完",
    r"即刻收听",
    r"相关阅读",
    r"相关文章",
    r"如果你现在没空",
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, cwd=str(ROOT))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def choose_images(image_dir: Path, count: int = 3) -> list[Path]:
    images = sorted(path for path in image_dir.glob("*.png") if path.name.startswith("img"))
    if len(images) <= count:
        return images
    picks = [images[0], images[len(images) // 2], images[-1]]
    seen: set[Path] = set()
    unique = []
    for item in picks:
        if item not in seen:
            unique.append(item)
            seen.add(item)
    return unique[:count]


def section_indices(lines: list[str]) -> list[int]:
    result = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if 6 <= len(stripped) <= 32 and not stripped.endswith(("。", "！", "？", "；", ".", "!", "?")):
            result.append(i)
    return result


def build_article(src: Path, out: Path, images: list[Path], captions: list[str]) -> None:
    text = read(src).strip()
    lines = [
        line
        for line in text.splitlines()
        if not re.match(r"\s*!\[[^\]]*\]\([^)]+\)\s*$", line)
        and not is_promo_line(line)
    ]
    insert_at = section_indices(lines)
    targets = []
    if insert_at:
        targets.append(insert_at[0])
    if len(insert_at) > 2:
        targets.append(insert_at[len(insert_at) // 2])
    if len(insert_at) > 4:
        targets.append(insert_at[-3])

    blocks: dict[int, list[str]] = {}
    for img, caption, idx in zip(images, captions, targets):
        blocks.setdefault(idx, []).extend(
            [
                "",
                f"![{img.stem}](images/{img.name})",
                "",
                caption,
                "",
            ]
        )

    output = []
    for i, line in enumerate(lines):
        output.append(line)
        if i in blocks:
            output.extend(blocks[i])
    write(out, "\n".join(output).strip() + "\n")


def is_promo_line(line: str) -> bool:
    stripped = line.strip()
    return any(re.search(pattern, stripped, flags=re.I) for pattern in PROMO_PATTERNS)


def build_material(insight: Path, out: Path, cfg: dict[str, str]) -> None:
    insight_text = read(insight).strip()
    headings = re.findall(r"^##\s+\(?[0-9:]*\)?\s*(.+)$", insight_text, flags=re.M)
    body = [
        "# 素材提取",
        "",
        f"- 一句话主旨：{cfg['thesis']}",
        f"- 文章标题：{cfg['title']}",
        f"- 来源字幕：`{cfg['stem']}.zh.srt`",
        f"- 原视频：`outputs/videos/{cfg['stem']}.mp4`",
        "",
        "## Top Insights",
        "",
    ]
    for idx, heading in enumerate(headings[:8], 1):
        body.append(f"{idx}. {heading.strip()}")
    body.extend(
        [
            "",
            "## Source Notes",
            "",
            "本文件由本地字幕侧的洞见稿和播客稿整理，正式发布前应复核嘉宾身份、公司名、日期、金额、链接等外部元数据。",
            "",
            "## 原始洞见稿节选",
            "",
            insight_text,
        ]
    )
    write(out, "\n".join(body).strip() + "\n")


def build_shotlist(manifest: Path, out: Path, images: list[Path], captions: list[str]) -> None:
    manifest_text = read(manifest)
    cue_map = {
        match.group(1): (match.group(2), match.group(3).strip())
        for match in re.finditer(
            r"##\s+(img[^\n]+)\n\n-\s+Timestamp:\s+([0-9.]+)s\n-\s+Cue:\s+(.+?)\n-",
            manifest_text,
            flags=re.S,
        )
    }
    lines = [
        "# 截图清单",
        "",
        "| Image file | Timestamp | Subtitle cue | Article section | Reason selected | Caption |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for img, caption in zip(images, captions):
        ts, cue = cue_map.get(img.name, ("", ""))
        lines.append(
            f"| `images/{img.name}` | {ts}s | {cue} | 正文对应观点段落 | 与字幕主题匹配，并来自本地视频抽帧 | {caption} |"
        )
    lines.extend(["", "## 自动候选清单", "", manifest_text.strip()])
    write(out, "\n".join(lines).strip() + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("number", choices=sorted(CONFIG))
    args = parser.parse_args()
    cfg = CONFIG[args.number]
    stem = cfg["stem"]
    sub_dir = ROOT / "outputs/subtitles" / stem
    out_dir = OUT_ROOT / stem
    image_dir = out_dir / "images"
    article_src = sub_dir / f"{stem}.播客类型.md"
    insight_src = sub_dir / f"{stem}.洞见类型.md"
    srt = sub_dir / f"{stem}.zh.srt"
    video = ROOT / "outputs/videos" / f"{stem}.mp4"

    run(
        [
            "python",
            str(SKILL_SCRIPT),
            "--video",
            str(video),
            "--srt",
            str(srt),
            "--out",
            str(image_dir),
            "--keywords",
            cfg["keywords"],
            "--count",
            "10",
        ]
    )

    images = choose_images(image_dir, int(cfg.get("final_image_count", 3)))
    build_article(article_src, out_dir / "播客类型图文版.md", images, cfg["captions"])
    build_material(insight_src, out_dir / "素材提取.md", cfg)
    build_shotlist(image_dir / "screenshot_candidates.md", out_dir / "截图清单.md", images, cfg["captions"])

    html_out = out_dir / f"{stem}_full.html"
    png_out = out_dir / cfg["slug"]
    run(["python", str(HTML_RENDER), str(out_dir / "播客类型图文版.md"), str(html_out)])
    run(["python", str(SCREENSHOT), str(html_out), str(png_out)])

    print(out_dir)
    print(html_out)
    print(png_out)


if __name__ == "__main__":
    main()
