# jtydhr88/screenwriting-skills · 第 1 次运行

- 仓库：https://github.com/jtydhr88/screenwriting-skills/tree/51115f18d160aa8b2ac5813e4432b6f0b425358f
- 安装的 skill：chekhov-dramaturgy、ozu-screenplay-style、succession-series-writing、sw-american-case-studies、sw-character-conflict、sw-chinese-opera-banqiang、sw-chinese-opera-banqiang-cases、sw-chinese-opera-qupai、sw-chinese-opera-qupai-cases、sw-chinese-series-practice、sw-dialogue、sw-format-adaptation、sw-genre-anatomy、sw-industry-business、sw-japanese-screenwriting、sw-korean-french-screenwriting、sw-premise-theme、sw-scene-craft、sw-series-case-studies、sw-series-engine-bible、sw-series-structure、sw-sitcom-comedy、sw-story-structure、sw-truby-anatomy、sw-workflow、sw-writers-room
- 环境：2.1.302 (Claude Code)，模型 claude-opus-5-5，推理强度 high
- 开始：2026-10-17T22:33:01-07:00，结束：2026-10-17T22:47:11-07:00
- 轮数：2，总耗时 14 分钟，按 API 价格折算 $5.27

## 第 1 轮

**用户：**

我要用已安装的 skill 写一部短剧，要求在 premise.md 里。

**工具调用：**Bash×7、Skill(sw-chinese-series-practice)×1、Skill(sw-workflow)×1、Write×3

**Agent 最后的回复：**

剧名《哑妻》，三份交付文件都已写好，放在当前目录。

**故事**：沈禾装哑三年，嫁进了害死她父亲的顾家。结婚三周年那天，丈夫逼她离婚。冷静期一满她就不再是"顾家人"，婆婆就能让她永远闭嘴，所以她只有 30 天找证据。核心看点是：她不说话，所以所有人都在她面前说真话。观众知道她会说话，剧里的人不知道。高潮放在冷静期最后一天：婆婆的直播庆典上，她当众开口，被婆婆逼着闭嘴的人一个接一个站起来作证。

**交付文件**：
1. **`人物小传.md`**：8 个人物（含已故的父亲），附关系图。每人写了欲望、错误信念、弧线和标志动作。反派婆婆周曼华有前史、口头禅（"闭嘴的人，活得长"），手里有五样能制住女主的东西。
2. **`分集大纲.md`**：项目页（一句话故事、戏核、主题、四段结构）加 60 集分集，每集都有集尾钩子。从第 2 集起每集打字幕"离婚冷静期 第 X 天"，当全剧的倒计时。三个付费卡点：
   - **第 10 集末（首卡）**：丈夫锁上车门说"别装了，你会说话，三年前我就知道"。前 10 集免费，约 15 分钟。
   - **第 30 集末（中点）**：拼命抢到的三亿转账授权书上，签字人是她丈夫。
   - **第 45 集末（谷底）**：丈夫在看守所里对着认罪书落笔，画面定格。
   
   第 46–60 集集中兑现，不再设卡。
3. **`剧本_第1-3集.txt`**：中文场号制，纯文本。每集约 800–1200 字（含动作描写），每集 3–5 场。每集结尾的钩子分别是：女主在浴室开口说话、门外的地板上留下一滴汤、在丈夫抽屉里翻出父亲带血的工牌。

**用到的 skill**：sw-workflow 定流程，sw-chinese-series-practice 定文档格式和集尾悬念的写法，sw-premise-theme 定戏核和主题，sw-character-conflict 写对手，sw-format-adaptation 定剧本格式，sw-dialogue 用来写对白。

**需要你知道的几点**：
- 这些 skill 里都没有讲竖屏短剧，单集时长、卡点位置是我按短剧平台的常见做法定的。如果你要投的平台规定了免费集数，卡点得跟着挪。
- 剧本里没写镜头术语，这是 skill 里的格式规矩。如果你们的平台要求标特写、景别，需要再加一遍。
- 结局情节牵涉经侦办案、精神鉴定、离婚冷静期的流程，都写得比较简略，正式送审前最好请人核实一下。

## 第 2 轮

**用户：**

如果要我在几个题材或故事方案里选，就选第 1 个（没有第 1 个就选最后一个）；其他要我定的，都按你推荐的来，不用再问我。请继续，直到 premise.md 列出的三项交付都写成文件。

**工具调用：**Bash×1

**Agent 最后的回复：**

premise.md 要的三项都已经写成文件，放在当前目录。我刚核对过，三个文件都在，内容完整：

| 交付项 | 文件 | 内容 |
|---|---|---|
| 1. 主要人物小传 | `人物小传.md` | 8 个人物（含已故的父亲），附人物关系图 |
| 2. 60 集分集大纲，标出付费卡点 | `分集大纲.md` | 60 集分集，每集带集尾钩子；三个付费卡点在第 10、30、45 集，大纲开头有一张表说明各卡在什么情节上、为什么放在那里 |
| 3. 第 1–3 集完整剧本 | `剧本_第1-3集.txt` | 中文场号制，纯文本，每集约 800–1200 字 |

上一轮我只出了一个故事方案，就是《哑妻》，没有几个题材让你选，所以"选第 1 个"就是它，不用改动。其余需要定的地方，上一轮都已经按我的推荐定下了：
- 题材是女频的悬疑复仇加先婚后爱，结局是女主当众开口说话；
- 前 10 集免费，三个付费卡点放在开头反转、中点和全剧谷底，第 46–60 集集中兑现，不再设卡；
- 剧本用中文场号制写，纯文本，不写镜头术语。

上一轮提醒的几点还没处理：
- 你要投的平台如果规定了免费集数，卡点得跟着挪；
- 平台如果要求标景别，剧本还要再加一遍；
- 剧情里经侦办案、精神鉴定、离婚冷静期这几处流程写得比较简略，送审前需要找人核实。
