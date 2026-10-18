#!/usr/bin/env python3
"""实测运行器：把同一份需求交给一个 skill，在隔离目录里用 Claude Code 无头模式跑完，保存产出和问答记录。

用法（在仓库根目录）：
  python evals/run.py 001-open-brief eternityspring/shuohao-skills --run 1 --work /tmp/evals
  python evals/run.py 001-open-brief baseline --run 1 --work /tmp/evals        # 不装任何 skill 的对照组
  python evals/run.py 001-open-brief <repo> --run 1 --work /tmp/evals --more   # 对已有会话再发一次固定回复

参赛名单、入口 skill 和每个 skill 跑几次写在 evals/runs/<premise>/contestants.toml。
每个 skill 用同一条开场指令和同一条固定回复，不额外加指令。skill 给出几个题材或故事方案时，固定回复按运行编号选：
第 1 次运行选第 1 个，第 2 次选第 2 个，依此类推；其他问题一律按 skill 自己的推荐。
为了安全，agent 只能写自己的工作目录。命令在 Claude Code 的系统沙箱里运行：不能联网，不能读主目录，
也不能读 --work 旁边的东西和其他参赛者的工作目录。不连任何 MCP。
--work 请用一个专门的目录。依赖：已登录的 claude CLI、git。只用标准库。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import uuid
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"

MODEL = "claude-opus-5-5"
EFFORT = "high"
MAX_TURNS = 12
TURN_TIMEOUT = 60 * 60

TASK = "我要写一部短剧，要求在 premise.md 里。"
TASK_TOOLKIT = "我要用已安装的 skill 写一部短剧，要求在 premise.md 里。"
REPLY = ("如果要我在几个题材或故事方案里选，就选第 {k} 个（没有第 {k} 个就选最后一个）；其他要我定的，都按你推荐的来，"
         "不用再问我。请继续，直到 premise.md 列出的三项交付都写成文件。")

ALLOWED = ["Bash", "Skill", "TodoWrite", "Agent"]  # Bash 全部放行，但都关在沙箱里，见 fence()
DENIED = ["WebFetch", "WebSearch", "Read(~/**)", "Edit(~/**)", "Write(~/**)"]
ASKING = re.compile(r"[？?]|确认|请选择|请回复|是否|要不要|哪一个|哪个方案|告诉我")


def slug(repo: str) -> str:
    return repo.replace("/", "__")


def roster(premise: str) -> dict:
    return tomllib.loads((EVALS / "runs" / premise / "contestants.toml").read_text(encoding="utf-8"))


def contestant(premise: str, repo: str) -> dict:
    for c in roster(premise)["contestants"]:
        if c["repo"].lower() == repo.lower():
            return c
    sys.exit(f"{repo} 不在 evals/runs/{premise}/contestants.toml 里")


def fetch(repo: str, src_root: Path) -> tuple[Path, str]:
    """浅克隆到 src_root 下，返回目录和 commit。已克隆过就复用，保证同一轮用同一个版本。"""
    dest = src_root / slug(repo)
    if not dest.exists():
        subprocess.run(["git", "clone", "-q", "--depth", "1", f"https://github.com/{repo}.git", str(dest)], check=True)
    commit = subprocess.run(["git", "-C", str(dest), "rev-parse", "HEAD"], check=True, capture_output=True,
                            text=True).stdout.strip()
    return dest, commit


def skill_dirs(src: Path) -> dict[str, Path]:
    """仓库里的 skill 目录（同名只取最短路径），和 skills CLI 的默认安装范围一致。"""
    found: dict[str, Path] = {}
    for p in sorted(src.rglob("*"), key=lambda p: len(p.parts)):
        if ".git" in p.parts or p.name.lower() != "skill.md":
            continue
        name = src.name.split("__", 1)[-1] if p.parent == src else p.parent.name
        found.setdefault(name, p.parent)
    return found


def install(src: Path, ws: Path) -> list[str]:
    target = ws / ".claude" / "skills"
    target.mkdir(parents=True)
    dirs = skill_dirs(src)
    if not dirs:  # 有的仓库把 skill 打包成 .skill（zip）
        unpacked = Path(tempfile.mkdtemp(dir=src.parent, prefix=src.name + ".unpacked."))
        for pkg in src.glob("*.skill"):
            with zipfile.ZipFile(pkg) as z:
                z.extractall(unpacked / pkg.stem)
        dirs = skill_dirs(unpacked)
    ignore = shutil.ignore_patterns(".git")
    for name, d in dirs.items():
        shutil.copytree(d, target / name, ignore=ignore)
    return sorted(dirs)


def fence(ws: Path, work: Path, others: list[Path]) -> tuple[list[str], list[str], dict]:
    """权限围栏：工具的允许和拒绝规则，加上 Bash 沙箱的设置。两层分开管，所以两边都要写。
    写权限用绝对路径：agent 用 cd 换了目录以后，相对路径 ./ 会跟着变。"""
    allow = ALLOWED + [f"Edit(/{ws}/**)", f"Write(/{ws}/**)"]
    blocked = [p for p in work.parent.iterdir() if p.is_dir() and p != work]
    blocked += [work / "src", work / "logs", *others]
    deny = DENIED + [f"Read(/{p}/**)" for p in blocked]
    settings = {"sandbox": {"enabled": True, "failIfUnavailable": True, "autoAllowBashIfSandboxed": True,
                            "allowUnsandboxedCommands": False,
                            "network": {"allowedDomains": [], "allowLocalBinding": False},
                            "filesystem": {"denyRead": ["~/", str(work.parent)], "allowRead": [str(ws)]}}}
    return allow, deny, settings


def claude(ws: Path, prompt: str, session: str, resume: bool, log: Path, allow: list[str], deny: list[str],
           settings: dict) -> dict:
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--model", MODEL, "--effort", EFFORT, "--setting-sources", "project", "--settings", json.dumps(settings),
           "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
           "--permission-mode", "dontAsk", "--allowedTools", *allow, "--disallowedTools", *deny]
    cmd += ["--resume", session] if resume else ["--session-id", session]
    env = {k: v for k, v in os.environ.items() if not k.startswith("CLAUDE")}
    tools: dict[str, int] = {}
    result: dict = {}
    with log.open("a", encoding="utf-8", buffering=1) as f, subprocess.Popen(cmd, cwd=ws, env=env, stdout=subprocess.PIPE,
                                                                 stderr=subprocess.STDOUT, text=True) as proc:
        try:
            for line in proc.stdout:
                f.write(line)
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if ev.get("type") == "assistant":
                    for block in ev.get("message", {}).get("content", []):
                        if block.get("type") == "tool_use":
                            name = block["name"]
                            if name == "Skill":
                                name = f"Skill({block.get('input', {}).get('skill', '?')})"
                            tools[name] = tools.get(name, 0) + 1
                elif ev.get("type") == "result":
                    result = ev
            proc.wait(timeout=TURN_TIMEOUT)
        except subprocess.TimeoutExpired:
            proc.kill()
            result = {"is_error": True, "result": "（超时，进程已终止）"}
    result["tools"] = tools
    return result


def deliverables(ws: Path) -> list[Path]:
    return sorted(p for p in ws.rglob("*") if p.is_file() and ".claude" not in p.relative_to(ws).parts
                  and p.name != "premise.md")


def snapshot(ws: Path) -> dict[str, tuple[int, int]]:
    return {str(p): (p.stat().st_mtime_ns, p.stat().st_size) for p in deliverables(ws)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("premise", help="evals/premises/ 下的文件名，不带 .md")
    ap.add_argument("repo", help="owner/repo，或 baseline")
    ap.add_argument("--run", type=int, default=1, help="第几次运行，从 1 开始；也决定固定回复里选第几个方案")
    ap.add_argument("--work", required=True, type=Path, help="放克隆仓库、工作目录和日志的专门目录（仓库之外）")
    ap.add_argument("--more", action="store_true", help="对已有会话再发一次固定回复")
    args = ap.parse_args()

    work = args.work.resolve()
    c = contestant(args.premise, args.repo)
    runs = roster(args.premise).get("runs", 1)
    if not 1 <= args.run <= runs:
        sys.exit(f"--run 要在 1 到 {runs} 之间")
    tag = f"run-{args.run}"
    ws_root = work / "ws" / args.premise
    ws = ws_root / slug(c["repo"]) / tag
    others = [ws_root / slug(o["repo"]) / f"run-{n}" for o in roster(args.premise)["contestants"]
              for n in range(1, runs + 1)]
    others = [p for p in others if p != ws]
    out = EVALS / "runs" / args.premise / slug(c["repo"]) / tag
    logs = work / "logs" / args.premise
    logs.mkdir(parents=True, exist_ok=True)
    state_path = logs / f"{slug(c['repo'])}.{tag}.state.json"
    log = logs / f"{slug(c['repo'])}.{tag}.jsonl"
    reply = REPLY.format(k=args.run)

    if args.more:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        prompts = [reply]
    else:
        if ws.exists():
            sys.exit(f"{ws} 已存在；要重跑请先删掉它")
        ws.mkdir(parents=True)
        shutil.copy(EVALS / "premises" / f"{args.premise}.md", ws / "premise.md")
        state = {"repo": c["repo"], "premise": args.premise, "run": args.run, "session": str(uuid.uuid4()),
                 "turns": [], "model": MODEL, "effort": EFFORT,
                 "started": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                 "claude_code": subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip()}
        if c["repo"] == "baseline":
            state.update(commit=None, installed=[])
            first = TASK
        else:
            src, state["commit"] = fetch(c["repo"], work / "src")
            state["installed"] = install(src, ws)
            first = f"/{c['entry']} {TASK}" if c.get("entry") else TASK_TOOLKIT
        prompts = [first] + [reply] * (MAX_TURNS - 1)

    allow, deny, settings = fence(ws, work, others)
    idle = 0
    for prompt in prompts:
        resume = bool(state["turns"])
        before = snapshot(ws)
        r = claude(ws, prompt, state["session"], resume, log, allow, deny, settings)
        changed = snapshot(ws) != before
        state["turns"].append({"user": prompt, "agent": r.get("result", ""), "tools": r["tools"], "changed": changed,
                               "denied": [d.get("tool_name") for d in r.get("permission_denials", [])],
                               "cost_usd": r.get("total_cost_usd"), "duration_s": round(r.get("duration_ms", 0) / 1000),
                               "error": r.get("is_error", False)})
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[{c['repo']} {tag}] 第 {len(state['turns'])} 轮：{len(deliverables(ws))} 个文件，"
              f"{'有' if changed else '无'}改动，{state['turns'][-1]['duration_s']}s", flush=True)
        if r.get("is_error"):
            break
        # agent 没在问问题、这一轮也没再改文件，说明它认为写完了；连续三轮没动静也停。
        if not changed and not ASKING.search(r.get("result", "")[-400:]) and deliverables(ws):
            break
        idle = 0 if changed else idle + 1
        if idle >= 3:
            break

    state["finished"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    save(ws, out, state)


def save(ws: Path, out: Path, state: dict) -> None:
    if out.exists():
        shutil.rmtree(out)
    (out / "output").mkdir(parents=True)
    for p in deliverables(ws):
        dest = out / "output" / p.relative_to(ws)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(p, dest)
    lines = [f"# {state['repo']} · 第 {state.get('run', 1)} 次运行", ""]
    if state["repo"] != "baseline":
        lines += [f"- 仓库：https://github.com/{state['repo']}/tree/{state['commit']}",
                  f"- 安装的 skill：{'、'.join(state['installed']) or '（无）'}"]
    else:
        lines += ["- 对照组：不安装任何 skill"]
    total = sum(t["cost_usd"] or 0 for t in state["turns"])
    lines += [f"- 环境：{state['claude_code']}，模型 {state['model']}，推理强度 {state['effort']}",
              f"- 开始：{state['started']}，结束：{state.get('finished', '—')}",
              f"- 轮数：{len(state['turns'])}，总耗时 {sum(t['duration_s'] for t in state['turns']) // 60} 分钟，"
              f"按 API 价格折算 ${total:.2f}", ""]
    for i, t in enumerate(state["turns"], 1):
        tools = "、".join(f"{k}×{v}" for k, v in sorted(t["tools"].items())) or "无"
        lines += [f"## 第 {i} 轮", "", "**用户：**", "", t["user"], "", f"**工具调用：**{tools}", ""]
        if t["denied"]:
            lines += [f"**被拒绝的工具：**{'、'.join(t['denied'])}", ""]
        lines += ["**Agent 最后的回复：**", "", t["agent"].strip() or "（空）", ""]
    (out / "transcript.md").write_text("\n".join(lines), encoding="utf-8")
    meta = {k: v for k, v in state.items() if k != "turns"} | {"turns": len(state["turns"])}
    (out / "run.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
