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

**图例**：🌟 精选 · 📝 提示词文件（非标准 skill）· 🧩 完整应用 · 🎬 适配的视频模型 · 💤 超过 180 天未更新 · 📦 已归档 · ⚠️ 仓库失效

**让 agent 帮你挑**：这份清单也是一个 skill。运行 `npx skills add UnderleveledBuilder/awesome-short-drama-skills` 装上 short-drama-skill-finder，再问你的 agent「我用 Codex 做小说改编短剧，装哪个 skill？」。

> [!NOTE]
> 「人工核对」指核对过仓库说明、目录结构和分类，不等于实测过效果，实测对比见 [evals/](evals/)。skill 可能附带脚本，安装前请先读一遍它的 SKILL.md。
