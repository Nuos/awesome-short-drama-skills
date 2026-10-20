# 第二轮：选题类 skill

- 需求：[premises/002-topic.md](../../premises/002-topic.md)。给一个新的爽文故事定选题，以后可以写成网文，也可以拍成竖屏短剧；这一步只定选题，不写大纲和正文。交付两项：一句话卖点，和选题说明（题材、写给谁看、主角和对手、核心冲突、开篇钩子、爽点从哪来、打算写多长和为什么撑得住）。题材、篇幅、平台都不给。
- 运行时间：2026-10-20（北京时间）
- 环境：Claude Code 2.1.304，模型 claude-opus-5-5，推理强度 high。所有参赛者和对照组用同一个模型、同样的工具权限，唯一的变量是装了哪个 skill。
- 每个参赛者跑 3 次，36 次运行全部保留，没有挑选。
- 运行器：[evals/run.py](../../run.py)；评审：[evals/judge.py](../../judge.py)。任何人都可以用同样的命令复现。
- 全过程的网页版：[第二轮实测记录](https://shortdramaskills.com/evals/round-2/)，每次运行的每一步、每场盲比的提示词和判决、评审体检和过程记录都能点开看。

## 和第一轮有什么不同

- **比选题，不比剧本。** 需求里不写集数和篇幅，写多长也交给 skill 定，看它自己的判断。
- **固定回复改成「选你最推荐的那个」。** 第一轮让第 n 次运行选第 n 个方案，为的是让三次运行写不同的故事；这一轮比的就是选题，从几个方案里挑出最好的那个，本来就是选题 skill 的本事。
- **所有参赛者两两比。** 第一轮每个 skill 只和对照组比；这一轮 12 个参赛者（含对照组）互相比，排出积分名次。
- **参赛者来自两个清单。** 短剧和小说清单里标了「选题」环节、能从零出选题的 skill，按星数挑了 11 个，没挑上的和原因见下面「没测的」。

## 统一指令

每次运行用同一条开场指令，skill 停下来时用同一条固定回复，不额外加指令：

- 开场（有入口 skill 的）：`/<入口 skill> 我要给一个新故事定选题，要求在 premise.md 里。` 仓库里有专门做选题的 skill，入口就用它；没有就用仓库的主入口。
- 开场（工具箱型仓库）：`我要用已安装的 skill 给一个新故事定选题，要求在 premise.md 里。`
- 对照组：`我要给一个新故事定选题，要求在 premise.md 里。`
- 固定回复：`如果要我在几个题材或故事方案里选，就选你最推荐的那个；其他要我定的，都按你推荐的来，不用再问我。请继续，直到 premise.md 列出的交付都写成文件。`

agent 在一轮里没有提问、也没有再改文件，就算写完；连续三轮没有动静也停；最多 12 轮。

## 安全隔离

- 开跑前用清单收录时那套安全检查脚本查了 11 个参赛仓库（不调模型，查二进制和压缩包、安装钩子、远程执行、读敏感文件）：8 个通过，3 个「要看」。逐个看过，被标出的是 Windows 启动脚本和抓榜单时读网页登录态的脚本，不是恶意代码，在沙箱里也用不上。详见 [timeline.toml](timeline.toml)。
- 命令在 Claude Code 的系统沙箱里运行：不能联网，不能读主目录，也不能读其他参赛者的工作目录；只能写自己的工作目录。绕过沙箱的开关已关闭。开跑前用一个便宜的模型逐项试过这些限制，子 agent 同样受限。
- Read、Write、Edit 工具另外用权限规则限制在同样的范围内。不连任何 MCP，不能用网页搜索和抓取。

## 参赛名单

表里的书名是故事卡里的第一个名字；不少选题同时起了网文名和短剧名，完整的见 [cards.jsonl](cards.jsonl)。

| 项目 | 测试版本 | 入口 | 装了几个 skill | 第 1 次 | 第 2 次 | 第 3 次 |
|---|---|---|---|---|---|---|
| 对照组（不装 skill）| — | — | 0 | 《冷静期》<br>5 轮 · 2 分钟 · $2.00<br>[产出](baseline/run-1/output/) · [记录](baseline/run-1/transcript.md) | 《她只是个记账的》<br>2 轮 · 1 分钟 · $0.52<br>[产出](baseline/run-2/output/) · [记录](baseline/run-2/transcript.md) | 《后座》<br>2 轮 · 1 分钟 · $0.53<br>[产出](baseline/run-3/output/) · [记录](baseline/run-3/transcript.md) |
| [zenstory-ai/oh-story-claudecode](https://github.com/zenstory-ai/oh-story-claudecode) | [`7408014`](https://github.com/zenstory-ai/oh-story-claudecode/tree/74080143dd1ac9a39a930fafd99a0dbbe61b946a) | `/story` | 13 | 《重生2006：包工头跑路前一天，我先把账收了》<br>2 轮 · 3 分钟 · $1.54<br>[产出](zenstory-ai__oh-story-claudecode/run-1/output/) · [记录](zenstory-ai__oh-story-claudecode/run-1/transcript.md) | 《重生后我掏出账本，全家都慌了》<br>3 轮 · 3 分钟 · $2.27<br>[产出](zenstory-ai__oh-story-claudecode/run-2/output/) · [记录](zenstory-ai__oh-story-claudecode/run-2/transcript.md) | 《开局接手破当铺，我能看穿每件宝贝的来路》<br>3 轮 · 2 分钟 · $2.04<br>[产出](zenstory-ai__oh-story-claudecode/run-3/output/) · [记录](zenstory-ai__oh-story-claudecode/run-3/transcript.md) |
| [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer) | [`9d8a6ea`](https://github.com/lingfengQAQ/webnovel-writer/tree/9d8a6ea92dd0f344763cc353b439d6ba7a454288) | `/webnovel-init` | 8 | 《欠我的，都得还》<br>3 轮 · 4 分钟 · $2.36<br>[产出](lingfengQAQ__webnovel-writer/run-1/output/) · [记录](lingfengQAQ__webnovel-writer/run-1/transcript.md) | 《全员有价》<br>3 轮 · 3 分钟 · $2.44<br>[产出](lingfengQAQ__webnovel-writer/run-2/output/) · [记录](lingfengQAQ__webnovel-writer/run-2/transcript.md) | 《欠我的，一分不少》<br>2 轮 · 3 分钟 · $1.54<br>[产出](lingfengQAQ__webnovel-writer/run-3/output/) · [记录](lingfengQAQ__webnovel-writer/run-3/transcript.md) |
| [0xsline/short-drama](https://github.com/0xsline/short-drama) | [`8979a42`](https://github.com/0xsline/short-drama/tree/8979a428c31a865421d661bdb606e24314b683a0) | `/short-drama` | 1 | 《冷静期三十天》<br>3 轮 · 3 分钟 · $1.96<br>[产出](0xsline__short-drama/run-1/output/) · [记录](0xsline__short-drama/run-1/transcript.md) | 《最后一份清单》<br>3 轮 · 2 分钟 · $1.97<br>[产出](0xsline__short-drama/run-2/output/) · [记录](0xsline__short-drama/run-2/transcript.md) | 《后座》<br>3 轮 · 2 分钟 · $1.73<br>[产出](0xsline__short-drama/run-3/output/) · [记录](0xsline__short-drama/run-3/transcript.md) |
| [Tomsawyerhu/Chinese-WebNovel-Skill](https://github.com/Tomsawyerhu/Chinese-WebNovel-Skill) | [`96709f4`](https://github.com/Tomsawyerhu/Chinese-WebNovel-Skill/tree/96709f477f4b59be856ebb10bec052dd0452b846) | `/Chinese-WebNovel-Skill` | 1 | 《净身出户三年，我成了前夫家的破产管理人》<br>2 轮 · 2 分钟 · $1.09<br>[产出](Tomsawyerhu__Chinese-WebNovel-Skill/run-1/output/) · [记录](Tomsawyerhu__Chinese-WebNovel-Skill/run-1/transcript.md) | 《封条》<br>2 轮 · 2 分钟 · $0.94<br>[产出](Tomsawyerhu__Chinese-WebNovel-Skill/run-2/output/) · [记录](Tomsawyerhu__Chinese-WebNovel-Skill/run-2/transcript.md) | 《本庭宣判，你们一分都拿不到》<br>4 轮 · 2 分钟 · $2.44<br>[产出](Tomsawyerhu__Chinese-WebNovel-Skill/run-3/output/) · [记录](Tomsawyerhu__Chinese-WebNovel-Skill/run-3/transcript.md) |
| [xindoo/sumeru](https://github.com/xindoo/sumeru) | [`334d8bc`](https://github.com/xindoo/sumeru/tree/334d8bc8d2ad6548a7c834a811f679378d7bf3bc) | `/sumeru-topic` | 7 | 《差评》<br>2 轮 · 3 分钟 · $1.40<br>[产出](xindoo__sumeru/run-1/output/) · [记录](xindoo__sumeru/run-1/transcript.md) | 《冷静期三十天》<br>4 轮 · 4 分钟 · $3.15<br>[产出](xindoo__sumeru/run-2/output/) · [记录](xindoo__sumeru/run-2/transcript.md) | 《落槌》<br>3 轮 · 6 分钟 · $3.32<br>[产出](xindoo__sumeru/run-3/output/) · [记录](xindoo__sumeru/run-3/transcript.md) |
| [LanyXiaosheng/bookflow-skill](https://github.com/LanyXiaosheng/bookflow-skill) | [`eb56fb5`](https://github.com/LanyXiaosheng/bookflow-skill/tree/eb56fb5c66ace4e0dd98027291c6912a2062c079) | `/bookflow-skill` | 1 | 《离婚要我净身出户那天，我把公司账本念到了第三页》<br>4 轮 · 2 分钟 · $2.59<br>[产出](LanyXiaosheng__bookflow-skill/run-1/output/) · [记录](LanyXiaosheng__bookflow-skill/run-1/transcript.md) | 《侯府当掉我的嫁妆那天，掌柜跪下叫我东家》<br>4 轮 · 3 分钟 · $2.99<br>[产出](LanyXiaosheng__bookflow-skill/run-2/output/) · [记录](LanyXiaosheng__bookflow-skill/run-2/transcript.md) | 《前夫的新妇揣着五十两，求我替她写和离书》<br>4 轮 · 3 分钟 · $3.24<br>[产出](LanyXiaosheng__bookflow-skill/run-3/output/) · [记录](LanyXiaosheng__bookflow-skill/run-3/transcript.md) |
| [dama-cyber/Distilled-Novel-Toolbox](https://github.com/dama-cyber/Distilled-Novel-Toolbox) | [`350f2bd`](https://github.com/dama-cyber/Distilled-Novel-Toolbox/tree/350f2bd2b23c7400509897742b22d0f2b139338d) | 不指定 | 13 | 《冷静期第三十天》<br>2 轮 · 2 分钟 · $1.01<br>[产出](dama-cyber__Distilled-Novel-Toolbox/run-1/output/) · [记录](dama-cyber__Distilled-Novel-Toolbox/run-1/transcript.md) | 《冷静期三十天，我清算了前夫全家》<br>3 轮 · 3 分钟 · $2.02<br>[产出](dama-cyber__Distilled-Novel-Toolbox/run-2/output/) · [记录](dama-cyber__Distilled-Novel-Toolbox/run-2/transcript.md) | 《这单，我不赔》<br>3 轮 · 3 分钟 · $1.82<br>[产出](dama-cyber__Distilled-Novel-Toolbox/run-3/output/) · [记录](dama-cyber__Distilled-Novel-Toolbox/run-3/transcript.md) |
| [tance-mang/chinese-webnovel-skills](https://github.com/tance-mang/chinese-webnovel-skills) | [`ecf552f`](https://github.com/tance-mang/chinese-webnovel-skills/tree/ecf552f6930e769d8bbf17818ad3d5a864a7a70b) | `/idea` | 33 | 《寿宴上，我说婆婆的镯子是假的》<br>3 轮 · 3 分钟 · $1.65<br>[产出](tance-mang__chinese-webnovel-skills/run-1/output/) · [记录](tance-mang__chinese-webnovel-skills/run-1/transcript.md) | 《开局查封首富婚车，我是他摇号摇来的破产管理人》<br>4 轮 · 4 分钟 · $2.74<br>[产出](tance-mang__chinese-webnovel-skills/run-2/output/) · [记录](tance-mang__chinese-webnovel-skills/run-2/transcript.md) | 《裁员当天我重生了，老板你别跪》<br>3 轮 · 3 分钟 · $1.63<br>[产出](tance-mang__chinese-webnovel-skills/run-3/output/) · [记录](tance-mang__chinese-webnovel-skills/run-3/transcript.md) |
| [xiaofeng-928/chinese-longnovel-skill](https://github.com/xiaofeng-928/chinese-longnovel-skill) | [`1277f1e`](https://github.com/xiaofeng-928/chinese-longnovel-skill/tree/1277f1e886ad1263562b0d85d828ece675c97417) | `/chinese-longnovel-skill` | 1 | 《清账》<br>3 轮 · 3 分钟 · $1.67<br>[产出](xiaofeng-928__chinese-longnovel-skill/run-1/output/) · [记录](xiaofeng-928__chinese-longnovel-skill/run-1/transcript.md) | 《头七之前》<br>4 轮 · 3 分钟 · $2.69<br>[产出](xiaofeng-928__chinese-longnovel-skill/run-2/output/) · [记录](xiaofeng-928__chinese-longnovel-skill/run-2/transcript.md) | 《绝当》<br>3 轮 · 3 分钟 · $1.82<br>[产出](xiaofeng-928__chinese-longnovel-skill/run-3/output/) · [记录](xiaofeng-928__chinese-longnovel-skill/run-3/transcript.md) |
| [Hao0321/ai-short-drama](https://github.com/Hao0321/ai-short-drama) | [`a1a00d3`](https://github.com/Hao0321/ai-short-drama/tree/a1a00d3949fedd74edb6830a79d189a2c76920db) | `/ai-short-drama` | 1 | 《失物招领》<br>3 轮 · 3 分钟 · $2.11<br>[产出](Hao0321__ai-short-drama/run-1/output/) · [记录](Hao0321__ai-short-drama/run-1/transcript.md) | 《这份人情，我收回了》<br>2 轮 · 3 分钟 · $1.21<br>[产出](Hao0321__ai-short-drama/run-2/output/) · [记录](Hao0321__ai-short-drama/run-2/transcript.md) | 《首富的良心，当在我家》<br>2 轮 · 3 分钟 · $1.30<br>[产出](Hao0321__ai-short-drama/run-3/output/) · [记录](Hao0321__ai-short-drama/run-3/transcript.md) |
| [qingyabailu-git/webfiction-write](https://github.com/qingyabailu-git/webfiction-write) | [`2c0128d`](https://github.com/qingyabailu-git/webfiction-write/tree/2c0128db58a608c27177b63d012ae4011f230967) | `/fiction-conceive` | 15 | 《七年账本》<br>4 轮 · 2 分钟 · $1.55<br>[产出](qingyabailu-git__webfiction-write/run-1/output/) · [记录](qingyabailu-git__webfiction-write/run-1/transcript.md) | 《账不会老》<br>3 轮 · 2 分钟 · $1.33<br>[产出](qingyabailu-git__webfiction-write/run-2/output/) · [记录](qingyabailu-git__webfiction-write/run-2/transcript.md) | 《头七之内，替死人讨债》<br>3 轮 · 2 分钟 · $1.37<br>[产出](qingyabailu-git__webfiction-write/run-3/output/) · [记录](qingyabailu-git__webfiction-write/run-3/transcript.md) |

36 次运行按 API 价格折算共 $67.98；Opus 评审另花 $42.20（抽故事卡 $2.29，396 场盲比 $39.91），找交付文件和分故事类型调用少，没有单独记花费。

## 没测的

小说和短剧两个清单里，标了「选题」环节的 skill 共 31 个。按星数从高到低挑，这些没进这一轮：

| 项目 | 星数 | 原因 |
|---|---|---|
| [zenstory-ai/oh-story-dsh](https://github.com/zenstory-ai/oh-story-dsh) | 553 | 把 oh-story 的 skill 装进 DeepSeek Harness 的工作台，选题部分和已参赛的 oh-story-claudecode 相同 |
| [VanGong1999/screen-creative-skills](https://github.com/VanGong1999/screen-creative-skills) | 466 | 做的是评估和改编已有的小说或 IP，要先有一部作品，不能从零出选题 |
| [lornshrimp/Lorn.NovelWriteSkills](https://github.com/lornshrimp/Lorn.NovelWriteSkills) | 238 | 按题材拆成多个技能包，共 350 个 skill，没有一个不分题材的选题入口 |
| [zhlmi/narrative-to-screen-reader](https://github.com/zhlmi/narrative-to-screen-reader) | 122 | 把手上已有的故事翻译成影视开发语言，要先有故事 |
| [ricky-theseus/DaisyWriter](https://github.com/ricky-theseus/DaisyWriter) | 75 | 开书用的 skill 和已参赛的 webnovel-writer 的初始化 skill 几乎一样（只差 23 行） |
| [qin1473692580-ux/oh-story-claudecode](https://github.com/qin1473692580-ux/oh-story-claudecode) | 65 | 从 oh-story 派生，选题部分相同 |
| [Wooooooooood/ai-fiction-writer](https://github.com/Wooooooooood/ai-fiction-writer) | 64 | 选题只能从扫榜开始，扫榜要联网 |
| [xiaotiewinner/xt-webnovel-writing](https://github.com/xiaotiewinner/xt-webnovel-writing) | 22 | 单入口全流程，「立书」一步连书名、人设、大纲和简介一起出；同为 22 星的 webfiction-write 有专门的构思 skill，这一轮取了它 |

另有 12 个不到 20 星的没排上：aby-aby111/fanqie-short-story.skill、hyi1233/wangwen-writing-skill-kit、duiniwukenaihe/novel-assistant-skill、Thatgfsj-easyRep/wangwenwrite-skill、huahuakandaima/human-novel-writer、liuxiao20051106-prog/novel-writer-skill、kongxcer555/open-novel-fanqie、tinylion1024/web-novel-master、dongyanyuxuana/novel-craft、xiaoyuCR7/general-novel-skill、jiangying3222880/novel-engine、adoria111/emma-screenwriting-skills（第一轮测过它的剧本）。

## 这一轮的限制

- **只用了一个模型。** 结论只说明在 claude-opus-5-5 下这些 skill 的表现，换模型可能不同。
- **只比纸面上的选题。** 选题好不好，最终要看写出来、上线以后的数据；这一轮只看选题文件本身。
- **不联网。** 好几个 skill 的选题流程第一步是扫榜（查起点、番茄等平台的榜单）。沙箱里不能联网，它们只能凭模型已有的知识判断：oh-story 每次都先走扫榜，在报告里写明没拿到榜单；chinese-longnovel-skill 每次都试着读番茄、起点、常读的榜单，被拦下后在选题文件开头标明「没经过市场验证」。
- **按 skill 装插件。** webnovel-writer 是按 Claude Code 插件写的，它的初始化脚本靠插件的环境变量找路径，按 skill 装上后找不到。它在三次运行里都说明了这一点；选题这一步不用跑初始化，交付不受影响。
- **记忆写不进去。** 有 8 次运行（含对照组 2 次）想把固定回复里的要求（「按你推荐的来，不用再问我」）记进 Claude Code 的记忆目录，那个目录在主目录下，被隔离规则拦下。不影响交付，每个参赛者条件相同。整轮被拦下的调用列在网站的评审体检页。
- **评审是 AI。** 故事卡、故事类型和盲比由和写稿相同的模型（claude-opus-5-5）完成，它看不到稿子出自谁。又请 GPT（gpt-6-astra）用一字不差的提示词复核：逐场的判断 290/396 一致，每对的最终结果 127/198 一致，不一致的标「有争议」；两位评审排出的名次相关系数 0.80，前四名是同样四个 skill，最后两名也一样。引文核对、位置和篇幅偏差见网站上的[评审体检](https://shortdramaskills.com/evals/round-2/checks/)。下一轮欢迎真人参赛。

## 怎么评

1. **找交付文件**：每次运行里哪些文件是最终交付的选题，见 [deliverables.toml](deliverables.toml)，人工核对过。扫榜报告、多方案对比报告、状态文件不算交付。
2. **匿名**：选题文件拼成匿名稿，去掉仓库名、skill 名和作者名，随机编成三位数编号。对应关系见 [blind_key.json](blind_key.json)。
3. **故事卡**：每份匿名稿抽出书名、题材、一句话梗概、时代地点、核心设定、主角、对手、所有人名、目标读者和篇幅，见 [cards.jsonl](cards.jsonl)。稿子里列了几个方案的，只抽它最终推荐的那个。
4. **故事类型**：把 36 张故事卡放在一起，按「换个名字就是同一个故事」的标准分组，见 [clusters.json](clusters.json)。
5. **盲比**：12 个参赛者（含对照组）两两比，每对比 3 次（第 n 次运行对第 n 次运行），每次把先后顺序对调再比一次，两次都判它赢才算赢，一胜一负算平。赢一次记 1 分，平一次记 0.5 分，按积分排名。只看它最终推荐的那个选题，看卖点、新意、冲突和爽点、续航、可执行五项；篇幅、排版和市场分析不加分。见 [duels.jsonl](duels.jsonl)。
6. **复核**：GPT（gpt-6-astra，经 Codex CLI，只读沙箱、空目录）用一字不差的提示词和输出格式重新分组、重判全部盲比，见 [clusters-gpt.json](clusters-gpt.json)、[duels-gpt.jsonl](duels-gpt.jsonl)。两位评审每次调用的提示词指纹和原始返回都在 [judge-raw/](judge-raw/)。

## 原始记录和核对

- [logs/runs/](logs/runs/)：36 次正式运行的原始日志（Claude Code 的 stream-json 输出）。
- [logs/pilots/](logs/pilots/)、[logs/checks/](logs/checks/)：正式运行前的 1 次试点（2 个参赛组）和 1 次沙箱自检，为什么做、发现了什么见 [timeline.toml](timeline.toml)。这些产出不进评审。
- 日志公开前用 [clean_logs.py](../../clean_logs.py) 清理过：去掉本机路径、用户名、额度用量和 Claude Code 的内部记录，其余原样保留。
- [blind/](blind/)：评审看到的 36 份匿名稿，原样。
- [MANIFEST.sha256](MANIFEST.sha256)：这一轮每个文件的 sha256 指纹。在仓库根目录运行 `python3 evals/verify.py 002-topic`，会核对指纹、从匿名稿重建两位评审每一次调用的提示词并和记录比对，再把网页上的数字重算一遍（统计代码见 [evals/stats.py](../../stats.py)）。
- skill 作者如果觉得自己的 skill 装错了、跑错了或者记录有误，可以提 issue，我们会对着原始日志核对，公开答复。
