#!/usr/bin/env python3
"""实测评审：把每次运行的三项交付拼成匿名稿，抽故事卡，再让评审两两盲比。

用法（在仓库根目录，按顺序）：
  python evals/judge.py locate 002-open-brief --work /tmp/judge   # 找出每次运行里哪些文件是小传、大纲、剧本
  python evals/judge.py pack   002-open-brief --work /tmp/judge   # 拼成匿名稿，随机编号，对应关系存在 --work 里
  python evals/judge.py cards  002-open-brief --work /tmp/judge   # 每份匿名稿抽一张故事卡
  python evals/judge.py cluster 002-open-brief --work /tmp/judge  # 按故事卡把所有剧分成故事类型，看谁和谁是同一个套路
  python evals/judge.py duel   002-open-brief --work /tmp/judge   # 每个 skill 和对照组同一运行编号两两比，两种顺序各比一次
  python evals/judge.py reveal 002-open-brief --work /tmp/judge   # 评完后揭晓：把故事卡、比较结果和对应关系写进 evals/runs/<premise>/

评审和故事卡都用和参赛者相同的模型，不给任何工具，只看匿名稿。
locate 的结果写在 evals/runs/<premise>/deliverables.toml，可以人工改。只用标准库。
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import tomllib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
MODEL = "claude-opus-5-5"
EFFORT = "high"
PARTS = {"bios": "人物小传", "outline": "分集大纲", "scripts": "第 1–3 集剧本"}
TEXT = {".md", ".txt", ".markdown", ".fountain", ".json", ".yaml", ".yml", ".csv", ".html"}

LOCATE = """下面是一次短剧创作留下的文件清单，每个文件附了开头。需求要三项交付：人物小传、60 集分集大纲、第 1–3 集完整剧本。
请指出每项交付对应哪些文件（相对路径，按阅读顺序）。只选最终交付的正文；过程文件、检查报告、设定草稿、方案备选、
配置和数据文件都不选。一个文件同时包含几项交付时，几项都写它。某项找不到就给空列表。

{listing}"""

CARD = """下面是一部竖屏短剧的人物小传、分集大纲和前三集剧本。请如实抽出这部剧的基本信息，只写稿子里有的内容，不评价好坏。

{text}"""

CLUSTER = """下面是 {n} 部竖屏短剧的简介，每部有一个编号。请按「故事类型」把它们分组：同一组的剧，核心设定和主线冲突属于同一种套路（比如「全职主妇离婚时拿账本清算婆家」「入殓师从遗体上发现命案」），换个名字和细节就差不多是同一个故事。分组要尽量细，宁可多分几组；每部只进一组；只有一部的也单独成组。给每组起一个短名字，再写一句这一组的共同套路。

{lines}"""

DUEL = """你是有经验的竖屏短剧编辑。下面是两份{part}，甲和乙，各自来自一部不同的竖屏短剧（全剧 60 集，每集 1–2 分钟）。
两部剧的题材和故事可能完全不同；你不知道它们出自谁。请只比较写作本身的质量，按下面几个维度逐项判断哪份更好：

{dims}

注意：
- 篇幅长、格式花哨、自带检查清单或说明文字都不加分；夹在正文里的元数据、编号、检查点要拿掉才能用，算缺点。
- 剧本按每集 1–2 分钟衡量：明显超时、拍不出来的心理描写、靠大段旁白推进，都是缺点。
- 两份差不多就判「平」。理由要引用原文。

=== 甲 ===
{a}

=== 乙 ===
{b}"""

DIMS = {
    "bios": {"人物": "动机清不清楚，有没有缺点和成长，配角是不是工具人",
             "新意": "人物设定和关系有没有新鲜感，是不是常见套路"},
    "outline": {"结构": "冲突升级、反转成不成立，有没有连续塌腰",
                "卡点": "付费卡点卡得准不准，卡点前有没有足够的钩子",
                "新意": "设定和桥段有没有新鲜感，是不是常见套路"},
    "scripts": {"钩子": "开头和每集结尾能不能让人想往下看",
                "对白": "像不像人说的话，角色之间有没有区别",
                "AI 味": "套话、排比、空洞形容词多不多",
                "可拍性": "每集时长对不对，场景和演员数量是否合理，离能直接拍还差多少修改"},
}

TRACKS = {"script": ["scripts"], "outline": ["bios", "outline"]}

CARD_SCHEMA = {"type": "object", "additionalProperties": False,
               "required": ["title", "genre", "logline", "era_place", "hook_device", "protagonist", "names",
                            "opening", "first_paywall_episode", "ending"],
               "properties": {
                   "title": {"type": "string", "description": "剧名"},
                   "genre": {"type": "string", "description": "题材标签，如「女频·重生·复仇」"},
                   "logline": {"type": "string", "description": "一句话梗概，40 字以内"},
                   "era_place": {"type": "string", "description": "时代和地点"},
                   "hook_device": {"type": "string", "description": "核心设定或金手指，一句话"},
                   "protagonist": {"type": "string", "description": "主角姓名和身份"},
                   "names": {"type": "array", "items": {"type": "string"}, "description": "所有有名字的角色姓名"},
                   "opening": {"type": "string", "description": "第 1 集开场画面，一句话"},
                   "first_paywall_episode": {"type": ["integer", "null"], "description": "第一个付费卡点在第几集"},
                   "ending": {"type": "string", "description": "结局，一句话"}}}

CLUSTER_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["groups"],
                  "properties": {"groups": {"type": "array", "items": {
                      "type": "object", "additionalProperties": False, "required": ["name", "pattern", "codes"],
                      "properties": {"name": {"type": "string"}, "pattern": {"type": "string"},
                                     "codes": {"type": "array", "items": {"type": "string"}}}}}}}

DIM_ENUM = {"type": "string", "enum": ["甲", "乙", "平"]}


def track_dims(track: str) -> dict[str, str]:
    """一个比较项目要看的维度；人物小传和大纲都有「新意」，合并时只留一个。"""
    return {d: why for part in TRACKS[track] for d, why in DIMS[part].items()}


def duel_schema(track: str) -> dict:
    dims = list(track_dims(track))
    return {"type": "object", "additionalProperties": False, "required": ["dims", "winner", "reason"],
            "properties": {"dims": {"type": "object", "additionalProperties": False, "required": dims,
                                    "properties": {d: DIM_ENUM for d in dims}},
                           "winner": DIM_ENUM, "reason": {"type": "string", "description": "三到五句，引用原文"}}}


LOCATE_SCHEMA = {"type": "object", "additionalProperties": False, "required": list(PARTS),
                 "properties": {k: {"type": "array", "items": {"type": "string"}} for k in PARTS}}


def ask(prompt: str, schema: dict, system: str) -> dict:
    """无工具、无项目设置的单次调用，返回按 schema 校验过的 JSON。"""
    with tempfile.TemporaryDirectory() as empty:
        cmd = ["claude", "-p", "--output-format", "json", "--model", MODEL, "--effort", EFFORT, "--tools", "",
               "--setting-sources", "project", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
               "--no-session-persistence", "--system-prompt", system, "--json-schema", json.dumps(schema)]
        env = {k: v for k, v in os.environ.items() if not k.startswith("CLAUDE")}
        for attempt in range(3):
            p = subprocess.run(cmd, input=prompt, cwd=empty, env=env, capture_output=True, text=True, timeout=1800)
            try:
                out = json.loads(p.stdout)
                data = out.get("structured_output") or json.loads(out["result"])
                return data | {"_cost_usd": out.get("total_cost_usd")}
            except (json.JSONDecodeError, KeyError, TypeError):
                err = (p.stdout or p.stderr)[-500:]
        raise RuntimeError(f"调用失败：{err}")


def runs_of(premise: str) -> list[tuple[str, int, Path]]:
    base = EVALS / "runs" / premise
    return sorted((d.parent.name, int(d.name.split("-")[1]), d) for d in base.glob("*/run-*") if (d / "output").is_dir())


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def cmd_locate(premise: str, work: Path) -> None:
    target = EVALS / "runs" / premise / "deliverables.toml"
    done = tomllib.loads(read_text(target)) if target.exists() else {}
    todo = [(s, n, d) for s, n, d in runs_of(premise) if f"{s}.run-{n}" not in done]

    def one(item):
        s, n, d = item
        files = [p for p in sorted((d / "output").rglob("*")) if p.is_file() and p.suffix.lower() in TEXT]
        listing = "\n\n".join(f"## {p.relative_to(d / 'output')}（{len(read_text(p))} 字）\n{read_text(p)[:400]}"
                              for p in files)
        r = ask(LOCATE.format(listing=listing), LOCATE_SCHEMA, "你负责整理文件，只按要求输出。")
        return f"{s}.run-{n}", {k: [f for f in r[k] if (d / "output" / f).is_file()] for k in PARTS}

    with ThreadPoolExecutor(8) as ex:
        for key, parts in ex.map(one, todo):
            done[key] = parts
            print(key, {k: len(v) for k, v in parts.items()}, flush=True)
    lines = ["# 每次运行里，哪些文件是三项交付。由 judge.py locate 生成，人工核对过；改了要重新 pack。", ""]
    for key in sorted(done):
        lines.append(f'["{key}"]')
        lines += [f"{k} = {json.dumps(done[key][k], ensure_ascii=False)}" for k in PARTS]
        lines.append("")
    target.write_text("\n".join(lines), encoding="utf-8")


def scrub(text: str, names: list[str]) -> str:
    """去掉能认出 skill 的字样：仓库名、skill 名、作者名。"""
    for n in sorted(set(names), key=len, reverse=True):
        if len(n) >= 3:
            text = re.sub(re.escape(n), "■", text, flags=re.I)
    return text


def cmd_pack(premise: str, work: Path) -> None:
    deliv = tomllib.loads(read_text(EVALS / "runs" / premise / "deliverables.toml"))
    roster = tomllib.loads(read_text(EVALS / "runs" / premise / "contestants.toml"))
    names = ["skills", "skill"]
    for c in roster["contestants"]:
        if c["repo"] != "baseline":
            names += c["repo"].split("/") + [c.get("entry", "")]
    for s, n, d in runs_of(premise):
        names += json.loads(read_text(d / "run.json")).get("installed", [])
    rng = random.Random()
    keys = sorted(deliv)
    codes = rng.sample(range(100, 1000), len(keys))
    blind = work / "blind"
    blind.mkdir(parents=True, exist_ok=True)
    key_map = {}
    for key, code in zip(keys, codes):
        s, run = key.rsplit(".", 1)
        d = EVALS / "runs" / premise / s / run / "output"
        key_map[str(code)] = key
        for part in PARTS:
            text = "\n\n".join(f"<!-- {f} -->\n{read_text(d / f)}" for f in deliv[key][part])
            (blind / f"{code}.{part}.md").write_text(scrub(text, names), encoding="utf-8")
    (work / "key.json").write_text(json.dumps(key_map, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(keys)} 份匿名稿写到 {blind}")


def packet(work: Path, code: str, parts: list[str]) -> str:
    return "\n\n".join(f"## {PARTS[p]}\n\n{read_text(work / 'blind' / f'{code}.{p}.md')}" for p in parts)


def cmd_cards(premise: str, work: Path) -> None:
    key_map = json.loads(read_text(work / "key.json"))
    out = work / "cards.jsonl"
    done = {json.loads(l)["code"] for l in out.open(encoding="utf-8")} if out.exists() else set()

    def one(code):
        r = ask(CARD.format(text=packet(work, code, list(PARTS))), CARD_SCHEMA, "你负责如实摘录信息。")
        return {"code": code} | r

    with ThreadPoolExecutor(8) as ex, out.open("a", encoding="utf-8") as f:
        for row in ex.map(one, [c for c in key_map if c not in done]):
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            print(row["code"], row["title"], row["genre"], flush=True)


def cmd_cluster(premise: str, work: Path) -> None:
    rows = [json.loads(l) for l in (work / "cards.jsonl").open(encoding="utf-8")]
    random.shuffle(rows)
    lines = "\n".join(f"- {r['code']}：《{r['title']}》 {r['genre']}。{r['logline']} 主角：{r['protagonist']}。"
                      f"核心设定：{r['hook_device']}" for r in rows)
    r = ask(CLUSTER.format(n=len(rows), lines=lines), CLUSTER_SCHEMA, "你是短剧行业编辑，只按要求输出。")
    (work / "clusters.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(r['groups'])} 个故事类型")


def cmd_duel(premise: str, work: Path) -> None:
    key_map = json.loads(read_text(work / "key.json"))
    code_of = {v: k for k, v in key_map.items()}
    runs = tomllib.loads(read_text(EVALS / "runs" / premise / "contestants.toml")).get("runs", 1)
    slugs = sorted({k.rsplit(".", 1)[0] for k in code_of} - {"baseline"})
    out = work / "duels.jsonl"
    done = {(r["track"], r["a"], r["b"]) for r in map(json.loads, out.open(encoding="utf-8"))} if out.exists() else set()
    jobs = []
    for track, parts in TRACKS.items():
        dims = "\n".join(f"- {d}：{why}" for d, why in track_dims(track).items())
        part = "、".join(PARTS[p] for p in parts)
        for s in slugs:
            for n in range(1, runs + 1):
                x, y = code_of.get(f"{s}.run-{n}"), code_of.get(f"baseline.run-{n}")
                if x and y:
                    for a, b in ((x, y), (y, x)):
                        if (track, a, b) not in done:
                            jobs.append((track, part, dims, parts, a, b))

    def one(job):
        track, part, dims, parts, a, b = job
        prompt = DUEL.format(part=part, dims=dims, a=packet(work, a, parts), b=packet(work, b, parts))
        r = ask(prompt, duel_schema(track), "你是严格、公正的短剧编辑，只按要求输出。")
        return {"track": track, "a": a, "b": b} | r

    print(f"{len(jobs)} 场比较", flush=True)
    with ThreadPoolExecutor(8) as ex, out.open("a", encoding="utf-8") as f:
        for row in ex.map(one, jobs):
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            print(row["track"], row["a"], row["b"], row["winner"], flush=True)


def cmd_reveal(premise: str, work: Path) -> None:
    key_map = json.loads(read_text(work / "key.json"))
    base = EVALS / "runs" / premise
    (base / "blind_key.json").write_text(json.dumps(key_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name in ("cards.jsonl", "duels.jsonl"):
        rows = [json.loads(l) for l in (work / name).open(encoding="utf-8")]
        for r in rows:
            for k in ("code", "a", "b"):
                if k in r:
                    r[k + "_run"] = key_map[r[k]]
        (base / name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    if (work / "clusters.json").exists():
        groups = json.loads(read_text(work / "clusters.json"))["groups"]
        for g in groups:
            g["runs"] = [key_map[c] for c in g["codes"]]
        (base / "clusters.json").write_text(json.dumps({"groups": groups}, ensure_ascii=False, indent=1) + "\n",
                                            encoding="utf-8")
    print(f"写入 {base}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["locate", "pack", "cards", "cluster", "duel", "reveal"])
    ap.add_argument("premise")
    ap.add_argument("--work", required=True, type=Path, help="放匿名稿和中间结果的目录（仓库之外）")
    args = ap.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    globals()[f"cmd_{args.step}"](args.premise, args.work.resolve())


if __name__ == "__main__":
    main()
