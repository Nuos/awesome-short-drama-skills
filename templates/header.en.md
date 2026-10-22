# Awesome Short Drama Skills

[中文](README.md) · **English** · Website: [shortdramaskills.com](https://shortdramaskills.com/en/)

> A curated list of agent skills for AI short drama (micro drama / vertical drama) and AI manju: screenwriting, adaptation, storyboards, video prompts and production. Install them into Claude Code, Codex, OpenClaw, Qwen, Doubao or WorkBuddy and start producing.

This list collects short-drama skills for AI agents. Most use the standard SKILL.md format, so they work in Claude Code, Codex and OpenClaw, and in Chinese agents such as QwenWork, Doubao desktop, WorkBuddy, Kimi Code, Qwen Code, CodeBuddy, Trae and Qoder; see the [FAQ](#faq) for how to install them. They cover adapting novels, episode outlines, hooks and paywall points, script review, storyboards, character assets, and prompts for video models such as Seedance, MiniMax and Kling. Every project has been checked by hand and sorted by type, production stage and supported video model.

Most projects come from China's short-drama scene (Hongguo, Douyin and others), and many are documented in Chinese; the descriptions below are translated. "Manju" (漫剧) is a serialized comic-style drama, now usually generated with AI image and video models.

{{count}} skill projects + {{platforms}} related open-source platforms · metadata updated {{updated}}

## Which skill to install for scripts

Round 1 (2026-10-18): 10 screenwriting skills and a control with no skill installed each wrote the same open brief 3 times, judged blind by two AI reviewers (Opus and GPT). The reviewers judge as if AI will make the whole drama, so effects, crowd scenes and many locations cost no points. Both reviewers found that these 4 beat the control in all 3 runs, on both the scripts and the character bible and outline:

| Skill | Good for | Watch out for |
|---|---|---|
| [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills) | Short lines, characters who each sound different, emotion carried by objects | Understated episode-ending hooks |
| [Shanyin-ai/shanyin-screenwriting-master](https://github.com/Shanyin-ai/shanyin-screenwriting-master) | Short dialogue with subtext; emotion carried by actions | Restrained hooks; quiet openings |
| [jtydhr88/screenwriting-skills](https://github.com/jtydhr88/screenwriting-skills) | Emotion in actions, not inner monologue; side characters with a history | Episode-ending hooks are sometimes too mild |
| [adoria111/emma-screenwriting-skills](https://github.com/adoria111/emma-screenwriting-skills) | Restrained dialogue; side characters with motives who change | Soft episode-ending hooks; weak paywall cliffhangers |

[Hao0321/ai-short-drama](https://github.com/Hao0321/ai-short-drama) also won all 3 runs on the character bible and outline, but its scripts were uneven (Opus: one win, two ties; GPT: two wins, one loss).

Limits of this round:
- On episode-ending hooks, Opus often preferred the control and GPT did the opposite.
- On the other 6 skills' scripts, the two reviewers were far apart.
- Only one model was tested: claude-opus-5-5.
- Every skill's drafts carry numbering and checklists that must be deleted before AI production.

The full record and per-skill reviews (in Chinese): [Round 1](https://shortdramaskills.com/evals/round-1/).

## Which skill to install for premises

Round 2 (2026-10-20): 11 web novel and short drama premise skills and a control with no skill installed each chose a premise 3 times for the same kind of revenge-fantasy story, one that could become a web novel or a vertical short drama. Every entry was compared blind with every other and ranked by points. The reviewers ask whether viewers would keep watching once AI makes it. Both AI reviewers (Opus and GPT) put the same three skills on top, and all three beat the control in all 3 runs:

| Skill | Place (Opus / GPT) | Good for | Watch out for |
|---|---|---|---|
| [Tomsawyerhu/Chinese-WebNovel-Skill](https://github.com/Tomsawyerhu/Chinese-WebNovel-Skill) | 1 / 2 | Rare legal jobs and reversals of status; pitches you get in one line; payoffs that land on the opponent's face | One run is the familiar hidden-expert formula; limited fuel for a long serial |
| [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer) | 2 / 3 | Powers with rules that cost something; the hero's flaw tied to the power | All 3 runs let the hero see numbers over people's heads; repetitive in the middle |
| [Hao0321/ai-short-drama](https://github.com/Hao0321/ai-short-drama) | 3 / 1 | The freshest premises; powers with rules; hooks with strong images | The rules leave the hero too passive, so payoffs come slowly |

The first two are in the [novel list](https://github.com/UnderleveledBuilder/awesome-novel-skills/blob/main/README.en.md). From this list, [0xsline/short-drama](https://github.com/0xsline/short-drama) placed 4th / 7th: clever use of the law, but long pitches.

Limits of this round:
- Both reviewers placed the no-skill control 9th, with 3 skills below it.
- There was no network, so the two skills that start by checking the charts had no chart data, and they placed near the bottom.
- The two reviewers disagreed on 63 of 198 pair results, mostly in the middle of the table.
- Only one model was tested: claude-opus-5-5.

The full record and per-skill reviews (in Chinese): [Round 2](https://shortdramaskills.com/evals/round-2/).

**Legend**: 🌟 featured · 📝 prompt files (not a standard skill) · 🧩 full app · 🎬 supported video models · 💤 not updated for 180+ days · 📦 archived · ⚠️ repo unavailable

**Let your agent choose**: this list is also a skill. Run `npx skills add UnderleveledBuilder/awesome-short-drama-skills` to install short-drama-skill-finder, then ask your agent "I use Codex to adapt novels into short dramas. Which skill should I install?"

> [!NOTE]
> "Checked by hand" means the README, directory structure and classification were reviewed; it does not mean the output was tested. Side-by-side tests live in [evals/](evals/). A skill may ship scripts, so read its SKILL.md before installing it.
