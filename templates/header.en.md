# Awesome Short Drama Skills

[中文](README.md) · **English** · Website: [shortdramaskills.com](https://shortdramaskills.com/en/)

> A curated list of agent skills for AI short drama (micro drama / vertical drama) and AI manju: screenwriting, adaptation, storyboards, video prompts and production. Install them into Claude Code, Codex, OpenClaw, Qwen, Doubao or WorkBuddy and start producing.

This list collects short-drama skills for AI agents. Most use the standard SKILL.md format, so they work in Claude Code, Codex and OpenClaw, and in Chinese agents such as QwenWork, Doubao desktop, WorkBuddy, Kimi Code, Qwen Code, CodeBuddy, Trae and Qoder; see the [FAQ](#faq) for how to install them. They cover adapting novels, episode outlines, hooks and paywall points, script review, storyboards, character assets, and prompts for video models such as Seedance, MiniMax and Kling. Every project has been checked by hand and sorted by type, production stage and supported video model.

Most projects come from China's short-drama scene (Hongguo, Douyin and others), and many are documented in Chinese; the descriptions below are translated. "Manju" (漫剧) is a serialized comic-style drama, now usually generated with AI image and video models.

{{count}} skill projects + {{platforms}} related open-source platforms · metadata updated {{updated}}

## Which skill to install for scripts

Round 1 (2026-10-18): 10 screenwriting skills and a control with no skill installed each wrote the same open brief 3 times, judged blind by AI. These 5 wrote scripts that beat the control in all 3 runs:

| Skill | Good for | Watch out for |
|---|---|---|
| [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills) | Short, restrained dialogue; reversals that turn on evidence you can film | A few outline episodes are overloaded |
| [Shanyin-ai/shanyin-screenwriting-master](https://github.com/Shanyin-ai/shanyin-screenwriting-master) | Dialogue with subtext; few scenes; believable runtimes | Understated hooks; slow openings |
| [jtydhr88/screenwriting-skills](https://github.com/jtydhr88/screenwriting-skills) | Fresh premises; three or four scenes an episode; small casts and few locations | Some paywall cliffhangers are weak |
| [Hao0321/ai-short-drama](https://github.com/Hao0321/ai-short-drama) | Dialogue that fits the characters; settings that drive conflict | Some episodes run past 2 minutes |
| [adoria111/emma-screenwriting-skills](https://github.com/adoria111/emma-screenwriting-skills) | Concrete everyday detail; supporting characters who change | Soft episode-ending hooks |

zenstory, Shanyin and screenwriting-skills won all 3 runs on both the script and the character bible and outline, and a GPT re-judge agreed on both.

Limits of this round:
- The control often had stronger episode-ending hooks.
- A GPT re-judge disagreed on 18 of the 60 pairs.
- Only one model was tested: claude-opus-5-5.
- Every skill's drafts carry numbering and checklists that must be deleted before a crew can use them.

The full record and per-skill reviews (in Chinese): [Round 1](https://shortdramaskills.com/evals/round-1/).

**Legend**: 🌟 featured · 📝 prompt files (not a standard skill) · 🧩 full app · 🎬 supported video models · 💤 not updated for 180+ days · 📦 archived · ⚠️ repo unavailable

**Let your agent choose**: this list is also a skill. Run `npx skills add UnderleveledBuilder/awesome-short-drama-skills` to install short-drama-skill-finder, then ask your agent "I use Codex to adapt novels into short dramas. Which skill should I install?"

> [!NOTE]
> "Checked by hand" means the README, directory structure and classification were reviewed; it does not mean the output was tested. Side-by-side tests live in [evals/](evals/). A skill may ship scripts, so read its SKILL.md before installing it.
