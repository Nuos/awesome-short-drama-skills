# jtydhr88/screenwriting-skills · 第 3 次运行

- 仓库：https://github.com/jtydhr88/screenwriting-skills/tree/51115f18d160aa8b2ac5813e4432b6f0b425358f
- 安装的 skill：chekhov-dramaturgy、ozu-screenplay-style、succession-series-writing、sw-american-case-studies、sw-character-conflict、sw-chinese-opera-banqiang、sw-chinese-opera-banqiang-cases、sw-chinese-opera-qupai、sw-chinese-opera-qupai-cases、sw-chinese-series-practice、sw-dialogue、sw-format-adaptation、sw-genre-anatomy、sw-industry-business、sw-japanese-screenwriting、sw-korean-french-screenwriting、sw-premise-theme、sw-scene-craft、sw-series-case-studies、sw-series-engine-bible、sw-series-structure、sw-sitcom-comedy、sw-story-structure、sw-truby-anatomy、sw-workflow、sw-writers-room
- 环境：2.1.302 (Claude Code)，模型 claude-opus-5-5，推理强度 high
- 开始：2026-10-17T23:08:43-07:00，结束：2026-10-17T23:27:04-07:00
- 轮数：2，总耗时 18 分钟，按 API 价格折算 $7.89

## 第 1 轮

**用户：**

我要用已安装的 skill 写一部短剧，要求在 premise.md 里。

**工具调用：**Bash×11、Edit×3、Read×7、Skill(sw-workflow)×1、Write×3

**Agent 最后的回复：**

三份文件已经写好，放在当前目录：

| 文件 | 内容 |
|---|---|
| `01_人物小传.md` | 11 个人物的小传，附人物关系图和"地雷表"（每个人藏着什么秘密、在第几集揭开） |
| `02_分集大纲.md` | 开头一页总纲（logline、主题、前提、引擎、四段结构、付费卡点表），后面是 60 集，每集写剧情和集尾钩子 |
| `03_第1-3集剧本.txt` | 前三集完整剧本，用中文场号制，纯文本 |

**故事：《擦痕》**（投放备用名《保洁妈妈》）
女儿在富豪江家的露台坠亡，被定为自杀。保洁员母亲周桂兰隐瞒身份，进江家做保洁。她懂各种污渍，第一集就从大理石上的酸蚀斑看出：有人半夜拿洁厕灵擦过露台。真凶江振海是人人称道的"江善人"，他其实早就知道她是谁，一直留着她，是想借"当妈的一定找得到"替他把女儿藏起来的账本找出来。主题落在：这位一辈子不求人的母亲，最后要靠 487 个"看不见的"保姆阿姨一起开口，才能让凶手当众认罪。

**付费卡点**：首个卡点放在第 10 集（前 9 集免费，大约 15 分钟），之后在第 20、30、33、40、50、56 集各设一个强卡点。其余每集集尾也都留了钩子。

**几点说明：**
- **用了哪些 skill**：按 sw-workflow 的剧集流程走，前提和主题用 sw-premise-theme，引擎和人物网用 sw-series-engine-bible，人物用 sw-character-conflict，开篇规则、每集收尾的钩子和内容红线用 sw-chinese-series-practice，对白用 sw-dialogue，格式用 sw-format-adaptation。这是一次性交付，所以没有建 story-bible。
- **卡点位置是我的判断**：已安装的 skill 里没有专讲竖屏微短剧或付费卡点的内容。卡点按"第 10 集首充、之后约每 10 集一个"的常见做法排，平台规则不同的话需要再调。
- **时长是估算的**：三集正文分别约 610、800、750 字。我按每分钟约 400 字折算，并逐场掐读复核，得出约 1 分 30 秒、2 分钟、1 分 50 秒，没有经过实拍验证。这个折算速度比 skill 给长剧的数字（每分钟 270–330 字）快，理由是竖屏切换更快。如果按长剧速度算，第 2 集会超过 2 分钟。
- **自查时改掉的几处漏洞**：
  - 微信群语音通话人数有上限，大高潮里 487 人"一起听"改成了群直播。
  - 别墅后门的密码，改成"保洁走的门没人想得起来改"。
  - 第 50 集主角不在场，改成她在电话那头听着。
- **内容合规**：警察写成讲证据的正面人物，最后到场是因为主角事先布好了局；主角没有用私刑；沈曼作为包庇者要承担法律后果；剧中没有怪力乱神。

## 第 2 轮

**用户：**

如果要我在几个题材或故事方案里选，就选第 3 个（没有第 3 个就选最后一个）；其他要我定的，都按你推荐的来，不用再问我。请继续，直到 premise.md 列出的三项交付都写成文件。

**工具调用：**Bash×1

**Agent 最后的回复：**

premise.md 要的三项交付上一轮都已经写成文件，刚才又检查了一遍，都在、都完整：

| 交付项 | 文件 | 检查结果 |
|---|---|---|
| 1. 主要人物小传 | `01_人物小传.md` | 11 个人物的小传都在，附人物关系图和地雷表 |
| 2. 60 集分集大纲，标出付费卡点 | `02_分集大纲.md` | 共 60 集；首个付费卡点在第 10 集，之后在第 20、30、33、40、50、56 集各有一个卡点 |
| 3. 第 1–3 集完整剧本 | `03_第1-3集剧本.txt` | 三集都写到结尾（"第 N 集完"） |

**关于"选第 3 个"**：我之前没有给过多个题材或故事方案，一开始就直接定了《擦痕》（保洁妈妈进凶手家查女儿的死），所以没有可选的。按你说的"没有第 3 个就选最后一个"，这里只有这一个方案，就沿用它，内容不用改。

**其他需要定的事，都按我的推荐办**：
- 剧名用《擦痕》，《保洁妈妈》留作投放备用名。
- 付费卡点按"第 10 集首充、之后约每 10 集一个"排，就是大纲里标出的那几集。
- 剧本用中文场号制，交纯文本。

这三项都已经写在文件里，不用再改。三项交付到这里就完成了。
