# Awesome Short Drama Skills

**中文** · [English](README.en.md) · 网站：[shortdramaskills.com](https://shortdramaskills.com)

> AI 短剧 · 漫剧 Skill（技能包）精选：从小说改编、分集剧本到分镜、视频提示词和出片，装进千问、豆包、龙虾（OpenClaw）、WorkBuddy、Claude Code、Codex 等智能体就能用。
>
> A curated list of agent skills for AI short drama (micro drama / vertical drama) and AI manju: screenwriting, adaptation, storyboards, video prompts and production.

这里收录给 AI 智能体（agent）用的短剧 skill，覆盖小说改编、集纲、钩子和付费卡点、剧本审稿、分镜、角色资产，以及给 Seedance、MiniMax、可灵等视频模型的提示词。大多是标准 SKILL.md 格式，千问办公、豆包电脑版、龙虾（OpenClaw）、WorkBuddy、Kimi Code、Qwen Code、CodeBuddy、Trae、Qoder、Claude Code、Codex 等支持技能的智能体都能装，装法见[常见问题](#faq)。每个项目都经过人工核对，按类型、创作阶段和适配的视频模型整理。

收录 {{count}} 个 skill 项目 + {{platforms}} 个相关开源平台 · 元数据更新于 {{updated}}

## 写剧本装哪个

第一轮实测（2026-10-18）：10 个剧本 skill 和一个不装 skill 的对照组，各写 3 次同一道开放题，由 AI 评审盲比。下面 5 个写的剧本，三次都赢了对照组：

| skill | 适合 | 要注意 |
|---|---|---|
| [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills) | 台词短而克制，翻盘落在拍得出来的物证上 | 大纲个别集信息量超载 |
| [Shanyin-ai/shanyin-screenwriting-master](https://github.com/Shanyin-ai/shanyin-screenwriting-master) | 对白有潜台词，场景少，时长可信 | 钩子偏收着，开场抓人慢 |
| [jtydhr88/screenwriting-skills](https://github.com/jtydhr88/screenwriting-skills) | 戏核新，每集三四场，人少景少 | 部分付费卡点偏弱 |
| [Hao0321/ai-short-drama](https://github.com/Hao0321/ai-short-drama) | 对白贴人物，设定能推动冲突 | 部分集 1–2 分钟拍不完 |
| [adoria111/emma-screenwriting-skills](https://github.com/adoria111/emma-screenwriting-skills) | 对白有生活细节，配角有转变 | 集尾钩子偏软 |

其中 zenstory、山音编剧大师和 screenwriting-skills 的剧本和人物大纲都三次全赢，换 GPT 复核也一样。

这一轮的局限：
- 每集结尾的钩子，反而常是对照组更强。
- 换 GPT 复核，60 对里有 18 对结论不同。
- 只测了 claude-opus-5-5 一个模型。
- 每个 skill 的稿子都夹着编号和自检表，交给剧组前要删掉。

全过程和逐个点评见[第一轮实测记录](https://shortdramaskills.com/evals/round-1/)。

## 定选题装哪个

第二轮实测（2026-10-20）：11 个网文和短剧的选题 skill 和一个不装 skill 的对照组，给同一个以后能写网文、也能拍短剧的爽文故事定选题，各定 3 次；所有参赛者两两盲比，按积分排名。两位 AI 评审（Opus 和 GPT）排出的前四名是同样四个 skill，只是顺序不同：

| skill | 名次（Opus / GPT） | 适合 | 要注意 |
|---|---|---|---|
| [Tomsawyerhu/Chinese-WebNovel-Skill](https://github.com/Tomsawyerhu/Chinese-WebNovel-Skill) | 1 / 4 | 少见的法律职业加身份翻转，一句话卖点就懂 | 爽点建在法律程序上，法条要逐条核实 |
| [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer) | 2 / 3 | 金手指配有代价的规则，主角的缺点和能力绑在一起 | 三次都是「头顶看见数字」；超自然设定有审核风险 |
| [LanyXiaosheng/bookflow-skill](https://github.com/LanyXiaosheng/bookflow-skill) | 3 / 1 | 场景少、人物少，最好落地 | 先写一两万字的短篇测题，有的设定撑不起六七十集 |
| [Hao0321/ai-short-drama](https://github.com/Hao0321/ai-short-drama) | 4 / 2 | 新意强，异能都有规矩 | 三次都靠异能，要特效或 AI 画面 |

前三个收在[小说清单](https://github.com/UnderleveledBuilder/awesome-novel-skills)里。本清单的 [0xsline/short-drama](https://github.com/0xsline/short-drama) 排第 6 / 第 7，现实题材，好拍，一句话卖点偏长。

这一轮的局限：
- 不装 skill 的对照组排第 7 / 第 10，两位评审都有 skill 排在它后面。
- 沙箱不能联网，要先扫榜的两个 skill 没拿到榜单，排在最后两名。
- 两位评审每对的结论，198 个里有 71 个不同。
- 只测了 claude-opus-5-5 一个模型。

全过程和逐个点评见[第二轮实测记录](https://shortdramaskills.com/evals/round-2/)。

**图例**：🌟 精选 · 📝 提示词文件（非标准 skill）· 🧩 完整应用 · 🎬 适配的视频模型 · 💤 超过 180 天未更新 · 📦 已归档 · ⚠️ 仓库失效

**让 agent 帮你挑**：这份清单也是一个 skill。运行 `npx skills add UnderleveledBuilder/awesome-short-drama-skills` 装上 short-drama-skill-finder，再问你的 agent「我用 Codex 做小说改编短剧，装哪个 skill？」。

> [!NOTE]
> 「人工核对」指核对过仓库说明、目录结构和分类，不等于实测过效果，实测对比见 [evals/](evals/)。skill 可能附带脚本，安装前请先读一遍它的 SKILL.md。
