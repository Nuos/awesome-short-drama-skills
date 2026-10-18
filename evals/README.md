# 实测对比

列表里的「人工核对」只说明项目信息准确。这里放实测：同一个题材交给不同的 skill，把产出并排摆出来，让读者自己判断。

## 实测规范

每轮实测：

1. **同一份输入，越少越好**：需求放在 `premises/` 下，所有参赛 skill 共用。从第二轮起，需求只写篇幅和交付物，不给题材、人物和情节，留给 skill 自己发挥。
2. **只有 skill 一个变量**：同一个 agent（Claude Code）、同一个模型、同样的推理强度、同样的工具权限，记录版本号。对照组用同样的环境，只是不装 skill。
3. **固定 skill 版本**：记录每个仓库的 commit hash。
4. **按 skill 自己的流程走**：开场只调用入口 skill，不额外加指令。skill 停下来问问题时，统一回复同一句话：给了几个题材或故事方案的，第 n 次运行选第 n 个；其他问题按 skill 自己的推荐。
5. **能跑 skill 自带的脚本**：命令在 Claude Code 的系统沙箱里运行，不能联网、不能读工作目录以外的文件，也看不到其他参赛者的产出。
6. **每个跑多次，全部保留**：不挑最好的一次，跑几次就放几次。
7. **匿名盲评**：评审看不到产出来自哪个 skill。

## 目录结构

```
evals/
├── run.py                     # 运行器：在隔离目录里用 Claude Code 无头模式跑一个 skill
├── judge.py                   # 评审：拼匿名稿、抽故事卡、两两盲比、揭晓
├── premises/
│   └── 002-<名字>.md          # 需求：篇幅和交付物
└── runs/
    └── 002-<名字>/
        ├── contestants.toml   # 参赛名单、入口 skill、每个跑几次
        ├── run.md             # 环境、版本、统一指令、参赛 skill 的 commit、限制
        ├── <owner>__<repo>/run-<n>/  # 第 n 次运行的产出（output/）、问答记录（transcript.md）、运行信息（run.json）
        ├── deliverables.toml  # 每次运行里哪些文件是三项交付
        ├── cards.jsonl        # 每次运行的故事卡
        ├── duels.jsonl        # 两两盲比的结果
        ├── blind_key.json     # 匿名编号和运行的对应关系
        └── review.md          # 点评摘要
```

## 已完成的轮次

- [第二轮：剧本类 skill · 开放题](runs/002-open-brief/review.md)（2026-10-18）：10 个剧本 skill 加 1 个不装 skill 的对照组，需求只给篇幅和交付物，每个跑 3 次，和对照组两两盲比
- [第一轮：剧本类 skill · 《双面绣》](runs/001-rebirth-revenge/review.md)（2026-10-17）：同样的参赛者，梗概写得太细、各跑一次，看不出 skill 改不改变故事（见那一页的更正）

## 复现

```bash
python evals/run.py 002-open-brief zenstory-ai/drama-skills --run 1 --work /tmp/evals
```

需要已登录的 `claude` CLI 和 git。agent 只能写自己的工作目录；命令在沙箱里运行，不能联网、不能读主目录和其他工作目录；不连 MCP。第一轮用的是[旧版运行器](https://github.com/UnderleveledBuilder/awesome-short-drama-skills/blob/116df92/evals/run.py)。

## 点评维度

| 维度 | 看什么 |
|---|---|
| 钩子 | 开头 / 每集结尾能不能让人想往下看 |
| 人物 | 动机是否清楚，行为是否前后一致 |
| 结构 | 节奏、冲突升级、反转是否成立 |
| 对白 | 像不像人说的话，有没有角色区分度 |
| AI 味 | 套话、排比、空洞形容词的多少 |
| 可用性 | 产出离能直接用还差多少修改；流程是否顺手 |

点评只写观察和例子，不打总分。
