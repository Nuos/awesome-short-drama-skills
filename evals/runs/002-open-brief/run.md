# 第二轮：剧本类 skill · 开放题

- 需求：[premises/002-open-brief.md](../../premises/002-open-brief.md)。只写了「写一部竖屏短剧」、篇幅（60 集，每集 1–2 分钟）和三项交付（人物小传、60 集分集大纲并标出付费卡点、第 1–3 集完整剧本），不给题材、人物和情节。
- 运行时间：2026-10-18（北京时间）
- 环境：Claude Code 2.1.302，模型 claude-opus-5-5，推理强度 high。所有参赛者和对照组用同一个模型、同样的工具权限，唯一的变量是装了哪个 skill。
- 每个参赛者跑 3 次，33 次运行全部保留，没有挑选。
- skill 版本和第一轮相同（同一个 commit）。
- 运行器：[evals/run.py](../../run.py)；评审：[evals/judge.py](../../judge.py)。任何人都可以用同样的命令复现。

## 统一指令

每次运行用同一条开场指令，skill 停下来时用同一条固定回复，不额外加指令：

- 开场（有入口 skill 的）：`/<入口 skill> 我要写一部短剧，要求在 premise.md 里。`
- 开场（工具箱型仓库）：`我要用已安装的 skill 写一部短剧，要求在 premise.md 里。`
- 对照组：`我要写一部短剧，要求在 premise.md 里。`
- 固定回复（n 是运行编号）：`如果要我在几个题材或故事方案里选，就选第 n 个（没有第 n 个就选最后一个）；其他要我定的，都按你推荐的来，不用再问我。请继续，直到 premise.md 列出的三项交付都写成文件。`

agent 在一轮里没有提问、也没有再改文件，就算写完；连续三轮没有动静也停。

## 和第一轮比，改了什么

| 第一轮的问题 | 第二轮的做法 |
|---|---|
| 梗概写定了主角、重生节点、退婚、火场和结局，留给 skill 的空间很小 | 只给篇幅和交付物 |
| 每个 skill 只跑一次，分不清是 skill 的影响还是偶然 | 每个跑 3 次 |
| 开场指令要求「直接交文件」，固定回复让 agent 自己定，skill 让用户挑方案的环节被跳过 | 开场只说要写什么；skill 给出几个方案时，第 n 次运行选第 n 个 |
| 不能运行命令，带校验脚本的 skill 走不完流程 | 命令在 Claude Code 的系统沙箱里运行，可以跑 skill 自带的脚本 |

## 安全隔离

- 命令在 Claude Code 的系统沙箱里运行：不能联网，不能读主目录，也不能读其他参赛者的工作目录；只能写自己的工作目录。绕过沙箱的开关已关闭。开跑前用一个便宜的模型逐项试过这些限制，子 agent 同样受限。
- Read、Write、Edit 工具另外用权限规则限制在同样的范围内。不连任何 MCP，不能用网页搜索和抓取。

## 参赛名单

| 项目 | 测试版本 | 入口 | 装了几个 skill | 第 1 次 | 第 2 次 | 第 3 次 |
|---|---|---|---|---|---|---|
| 对照组（不装 skill）| — | — | 0 | 《别让他们烧了我》<br>2 轮 · 10 分钟 · $3.22<br>[产出](baseline/run-1/output/) · [记录](baseline/run-1/transcript.md) | 《来自明天的我》<br>4 轮 · 17 分钟 · $10.46<br>[产出](baseline/run-2/output/) · [记录](baseline/run-2/transcript.md) | 《扫尘》<br>2 轮 · 9 分钟 · $3.05<br>[产出](baseline/run-3/output/) · [记录](baseline/run-3/transcript.md) |
| [eternityspring/shuohao-skills](https://github.com/eternityspring/shuohao-skills) | [`d28a9c5`](https://github.com/eternityspring/shuohao-skills/tree/d28a9c539b40523d081794b25ff9113016bd98e0) | `/novel-outline` | 7 | 《掌眼》<br>2 轮 · 17 分钟 · $6.89<br>[产出](eternityspring__shuohao-skills/run-1/output/) · [记录](eternityspring__shuohao-skills/run-1/transcript.md) | 《闪婚老公藏不住了》<br>5 轮 · 11 分钟 · $20.97<br>[产出](eternityspring__shuohao-skills/run-2/output/) · [记录](eternityspring__shuohao-skills/run-2/transcript.md) | 《签字之前》<br>3 轮 · 16 分钟 · $21.24<br>[产出](eternityspring__shuohao-skills/run-3/output/) · [记录](eternityspring__shuohao-skills/run-3/transcript.md) |
| [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills) | [`dafe80e`](https://github.com/zenstory-ai/drama-skills/tree/dafe80ee390ec8be5a7ec8dd156a84d511f8e7dd) | `/short-drama` | 12 | 《七格药盒》<br>3 轮 · 17 分钟 · $9.44<br>[产出](zenstory-ai__drama-skills/run-1/output/) · [记录](zenstory-ai__drama-skills/run-1/transcript.md) | 《掌眼》<br>3 轮 · 20 分钟 · $11.65<br>[产出](zenstory-ai__drama-skills/run-2/output/) · [记录](zenstory-ai__drama-skills/run-2/transcript.md) | 《停炉》<br>5 轮 · 18 分钟 · $18.10<br>[产出](zenstory-ai__drama-skills/run-3/output/) · [记录](zenstory-ai__drama-skills/run-3/transcript.md) |
| [lixiaoxiao9888-create/manju-laoli-skill](https://github.com/lixiaoxiao9888-create/manju-laoli-skill) | [`370a236`](https://github.com/lixiaoxiao9888-create/manju-laoli-skill/tree/370a236ed47d29ef3bf356ced85a17cee2f117a4) | `/short-drama-director` | 13 | 《重生清算日》<br>5 轮 · 35 分钟 · $32.77<br>[产出](lixiaoxiao9888-create__manju-laoli-skill/run-1/output/) · [记录](lixiaoxiao9888-create__manju-laoli-skill/run-1/transcript.md) | 《重回高考前夜》<br>5 轮 · 24 分钟 · $27.77<br>[产出](lixiaoxiao9888-create__manju-laoli-skill/run-2/output/) · [记录](lixiaoxiao9888-create__manju-laoli-skill/run-2/transcript.md) | 《冷静期三十天》<br>3 轮 · 21 分钟 · $12.39<br>[产出](lixiaoxiao9888-create__manju-laoli-skill/run-3/output/) · [记录](lixiaoxiao9888-create__manju-laoli-skill/run-3/transcript.md) |
| [jtydhr88/screenwriting-skills](https://github.com/jtydhr88/screenwriting-skills) | [`51115f1`](https://github.com/jtydhr88/screenwriting-skills/tree/51115f18d160aa8b2ac5813e4432b6f0b425358f) | 不指定 | 26 | 《哑妻》<br>2 轮 · 14 分钟 · $5.27<br>[产出](jtydhr88__screenwriting-skills/run-1/output/) · [记录](jtydhr88__screenwriting-skills/run-1/transcript.md) | 《别在她面前说秘密》<br>2 轮 · 12 分钟 · $5.30<br>[产出](jtydhr88__screenwriting-skills/run-2/output/) · [记录](jtydhr88__screenwriting-skills/run-2/transcript.md) | 《擦痕》<br>2 轮 · 18 分钟 · $7.89<br>[产出](jtydhr88__screenwriting-skills/run-3/output/) · [记录](jtydhr88__screenwriting-skills/run-3/transcript.md) |
| [Shanyin-ai/shanyin-screenwriting-master](https://github.com/Shanyin-ai/shanyin-screenwriting-master) | [`ca20ce2`](https://github.com/Shanyin-ai/shanyin-screenwriting-master/tree/ca20ce245ae028e64418393d6cf4688b7dbe3d89) | `/screenwriting-master` | 1 | 《顶替》<br>4 轮 · 21 分钟 · $11.57<br>[产出](Shanyin-ai__shanyin-screenwriting-master/run-1/output/) · [记录](Shanyin-ai__shanyin-screenwriting-master/run-1/transcript.md) | 《替身入殓师》<br>2 轮 · 24 分钟 · $8.85<br>[产出](Shanyin-ai__shanyin-screenwriting-master/run-2/output/) · [记录](Shanyin-ai__shanyin-screenwriting-master/run-2/transcript.md) | 《末班代驾》<br>4 轮 · 32 分钟 · $17.15<br>[产出](Shanyin-ai__shanyin-screenwriting-master/run-3/output/) · [记录](Shanyin-ai__shanyin-screenwriting-master/run-3/transcript.md) |
| [lixiaoxiao9888-create/short-drama-factory](https://github.com/lixiaoxiao9888-create/short-drama-factory) | [`1a634aa`](https://github.com/lixiaoxiao9888-create/short-drama-factory/tree/1a634aa852cb976be1e6a915845480f6b1126693) | `/short-drama-factory` | 1 | 《这碗狮子头，你们不配吃》<br>2 轮 · 17 分钟 · $7.49<br>[产出](lixiaoxiao9888-create__short-drama-factory/run-1/output/) · [记录](lixiaoxiao9888-create__short-drama-factory/run-1/transcript.md) | 《离婚那天，我只带走了一坛老汤》<br>2 轮 · 20 分钟 · $9.41<br>[产出](lixiaoxiao9888-create__short-drama-factory/run-2/output/) · [记录](lixiaoxiao9888-create__short-drama-factory/run-2/transcript.md) | 《六十大寿，我把账本拍在了桌上》<br>2 轮 · 24 分钟 · $11.51<br>[产出](lixiaoxiao9888-create__short-drama-factory/run-3/output/) · [记录](lixiaoxiao9888-create__short-drama-factory/run-3/transcript.md) |
| [adoria111/emma-screenwriting-skills](https://github.com/adoria111/emma-screenwriting-skills) | [`919292c`](https://github.com/adoria111/emma-screenwriting-skills/tree/919292cabf7b5b3ebd1027c72f1d0b711a16c189) | `/em-story-architect` | 10 | 《我没死，我要离婚》<br>2 轮 · 22 分钟 · $7.27<br>[产出](adoria111__emma-screenwriting-skills/run-1/output/) · [记录](adoria111__emma-screenwriting-skills/run-1/transcript.md) | 《遗物会说话》<br>3 轮 · 18 分钟 · $9.64<br>[产出](adoria111__emma-screenwriting-skills/run-2/output/) · [记录](adoria111__emma-screenwriting-skills/run-2/transcript.md) | 《被结婚的登记员》<br>3 轮 · 24 分钟 · $12.88<br>[产出](adoria111__emma-screenwriting-skills/run-3/output/) · [记录](adoria111__emma-screenwriting-skills/run-3/transcript.md) |
| [zhu5859243-free/hongguo-shortdrama-screenwriting](https://github.com/zhu5859243-free/hongguo-shortdrama-screenwriting) | [`d9c235a`](https://github.com/zhu5859243-free/hongguo-shortdrama-screenwriting/tree/d9c235a6bc0be67d7563018cf3db49bcf58e72ab) | `/hongguo-shortdrama-screenwriting` | 1 | 《离婚当天，我把婆家的账查穿了》<br>2 轮 · 14 分钟 · $6.11<br>[产出](zhu5859243-free__hongguo-shortdrama-screenwriting/run-1/output/) · [记录](zhu5859243-free__hongguo-shortdrama-screenwriting/run-1/transcript.md) | 《离婚后，婆家招牌菜做不出来了》<br>2 轮 · 17 分钟 · $7.08<br>[产出](zhu5859243-free__hongguo-shortdrama-screenwriting/run-2/output/) · [记录](zhu5859243-free__hongguo-shortdrama-screenwriting/run-2/transcript.md) | 《这个家的账，我算了十五年》<br>2 轮 · 13 分钟 · $6.21<br>[产出](zhu5859243-free__hongguo-shortdrama-screenwriting/run-3/output/) · [记录](zhu5859243-free__hongguo-shortdrama-screenwriting/run-3/transcript.md) |
| [catyiqian/qianqianwriting](https://github.com/catyiqian/qianqianwriting) | [`436088b`](https://github.com/catyiqian/qianqianwriting/tree/436088b3bb2ebeae5cf26663fa92525512460f5b) | `/qianqianwriting` | 1 | 《叮，他在撒谎》<br>2 轮 · 15 分钟 · $5.29<br>[产出](catyiqian__qianqianwriting/run-1/output/) · [记录](catyiqian__qianqianwriting/run-1/transcript.md) | 《她妈来了》<br>3 轮 · 14 分钟 · $7.29<br>[产出](catyiqian__qianqianwriting/run-2/output/) · [记录](catyiqian__qianqianwriting/run-2/transcript.md) | 《五十岁，我从这个家辞职了》<br>2 轮 · 12 分钟 · $4.15<br>[产出](catyiqian__qianqianwriting/run-3/output/) · [记录](catyiqian__qianqianwriting/run-3/transcript.md) |
| [Hao0321/ai-short-drama](https://github.com/Hao0321/ai-short-drama) | [`a1a00d3`](https://github.com/Hao0321/ai-short-drama/tree/a1a00d3949fedd74edb6830a79d189a2c76920db) | `/ai-short-drama` | 1 | 《账不会忘》<br>3 轮 · 22 分钟 · $11.19<br>[产出](Hao0321__ai-short-drama/run-1/output/) · [记录](Hao0321__ai-short-drama/run-1/transcript.md) | 《老卤》<br>2 轮 · 19 分钟 · $6.44<br>[产出](Hao0321__ai-short-drama/run-2/output/) · [记录](Hao0321__ai-short-drama/run-2/transcript.md) | 《老卤》<br>2 轮 · 21 分钟 · $7.03<br>[产出](Hao0321__ai-short-drama/run-3/output/) · [记录](Hao0321__ai-short-drama/run-3/transcript.md) |

33 次运行按 API 价格折算共 $352.97；评审（找交付文件、抽故事卡、分故事类型、120 场盲比）另约 $45。

## 这一轮的限制

- **只用了一个模型。** 结论只说明在 claude-opus-5-5 下这些 skill 的表现，换模型可能不同。
- **大多数 skill 没有让用户挑方向。** 33 次运行里，只有漫剧老李、山音编剧大师和 shuohao 的个别几次给出了几个故事方案；其余都是 skill 自己定一个就写完了。所以三次运行之间的差别主要来自模型每次生成的随机性。
- **命令输出太长时读不全。** Claude Code 会把太长的命令输出存进主目录下的文件，主目录被隔离了，agent 只能改用分段查看。所有参赛者条件相同。
- **缺 matplotlib。** 漫剧老李有一个画情绪曲线的脚本要用 matplotlib，本机没装，沙箱也不能联网安装。
- **不联网。** 需要查榜单或热点的 skill 只能凭已有资料判断，有的稿子里写明了这一点。
- **评审是 AI。** 故事卡、故事类型和盲比都由同一个模型（claude-opus-5-5）完成，它看不到稿子出自谁。评审理由里的引文有 85% 能在原稿里逐字找到，其余多是把几处原话用省略号拼在一起，或者是转述。下一轮计划请人类编剧参与。

## 怎么评

1. **找交付文件**：每次运行里哪些文件是人物小传、大纲、剧本，见 [deliverables.toml](deliverables.toml)，人工核对过。
2. **匿名**：三项交付拼成匿名稿，去掉仓库名、skill 名和作者名，随机编成三位数编号。对应关系见 [blind_key.json](blind_key.json)。
3. **故事卡**：每份匿名稿抽出剧名、题材、一句话梗概、主角、所有人名、开场画面、第一个付费卡点和结局，见 [cards.jsonl](cards.jsonl)。
4. **故事类型**：把 33 张故事卡放在一起，按「换个名字就是同一个故事」的标准分组，见 [clusters.json](clusters.json)。
5. **盲比**：每个 skill 的第 n 次运行和对照组的第 n 次运行比，分剧本（第 1–3 集）和人物大纲（小传加分集大纲）两项，每场把先后顺序对调再比一次，两次都判它赢才算赢。剧本看钩子、对白、AI 味、可拍性；人物大纲看人物、新意、结构、卡点。见 [duels.jsonl](duels.jsonl)。
