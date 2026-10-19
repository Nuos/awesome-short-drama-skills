#!/usr/bin/env python3
"""实测结果的统计：胜负、评审体检（换序一致、位置偏差、篇幅偏差、引文核对）、两位评审的一致度、故事分组的一致度。

网站的实测记录页和 evals/verify.py 都调这里，页面上的数字是生成网站时从 evals/runs/<轮次>/ 现算的。
也可以直接运行，打印一轮的全部数字：
  python evals/stats.py 001-open-brief

只用标准库。
"""
from __future__ import annotations

import json
import math
import re
import sys
import tomllib
from collections import Counter
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import judge  # noqa: E402

EVALS = Path(__file__).resolve().parent
JUDGES = {"opus": ("duels.jsonl", "clusters.json"), "gpt": ("duels-gpt.jsonl", "clusters-gpt.json")}
QUOTE = re.compile(r"“([^”]+)”|「([^」]+)」|『([^』]+)』|\"([^\"]+)\"")
ELLIPSIS = re.compile(r"……|…|\.\.\.")
SPACE = re.compile(r"\s+")


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """二项比例的 95% 置信区间（Wilson 法），样本很少时也不会跑出 0 到 1 之外。"""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    mid = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, mid - half), min(1.0, mid + half)


def kappa(a: list[str], b: list[str]) -> float:
    """Cohen's kappa：两位评审的一致度扣掉碰巧一致的部分。1 是完全一致，0 是和瞎猜一样。"""
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def ari(x: dict[str, int], y: dict[str, int]) -> float:
    """调整兰德指数：两种分组有多像。1 是完全一样，0 是和随机分组一样。x、y 是「编号 → 组号」。"""
    items = sorted(x)
    pairs = lambda n: n * (n - 1) // 2  # noqa: E731
    table = Counter((x[i], y[i]) for i in items)
    sum_ij = sum(pairs(v) for v in table.values())
    sum_a = sum(pairs(v) for v in Counter(x[i] for i in items).values())
    sum_b = sum(pairs(v) for v in Counter(y[i] for i in items).values())
    expected = sum_a * sum_b / pairs(len(items))
    top = (sum_a + sum_b) / 2
    return 1.0 if top == expected else (sum_ij - expected) / (top - expected)


class Round:
    """一轮实测的全部数据，从 evals/runs/<轮次>/ 读。"""

    def __init__(self, premise: str) -> None:
        self.premise = premise
        self.dir = EVALS / "runs" / premise
        self.key: dict[str, str] = json.loads((self.dir / "blind_key.json").read_text(encoding="utf-8"))
        self.code_of = {v: k for k, v in self.key.items()}
        self.roster = tomllib.loads((self.dir / "contestants.toml").read_text(encoding="utf-8"))
        self.runs_per = self.roster.get("runs", 1)
        self.cards = [json.loads(l) for l in (self.dir / "cards.jsonl").open(encoding="utf-8")]
        self.duels: dict[str, list[dict]] = {}
        self.groups: dict[str, list[dict]] = {}
        for j, (duels, clusters) in JUDGES.items():
            if (self.dir / duels).exists():
                self.duels[j] = [json.loads(l) for l in (self.dir / duels).open(encoding="utf-8")]
            if (self.dir / clusters).exists():
                self.groups[j] = json.loads((self.dir / clusters).read_text(encoding="utf-8"))["groups"]
        self.slugs = [c["repo"].replace("/", "__") for c in self.roster["contestants"] if c["repo"] != "baseline"]
        self._packets: dict[tuple[str, str], str] = {}

    # ── 稿子 ──

    def packet(self, code: str, track: str) -> str:
        """评审看到的那份匿名稿，和 judge.py 拼给评审的一字不差。"""
        if (code, track) not in self._packets:
            self._packets[code, track] = judge.packet(self.dir, code, judge.TRACKS[track])
        return self._packets[code, track]

    def prompt(self, track: str, a: str, b: str) -> str:
        return judge.duel_prompt(self.dir, track, a, b)

    # ── 胜负 ──

    def verdicts(self, j: str) -> dict[tuple[str, str], list[tuple[dict, str]]]:
        """每一对（项目，参赛者某次运行）的两次比较，换算成参赛者的「赢 W / 平 T / 输 L」。"""
        out: dict[tuple[str, str], list[tuple[dict, str]]] = {}
        for d in self.duels.get(j, []):
            mine, side = (d["a_run"], "甲") if not d["a_run"].startswith("baseline.") else (d["b_run"], "乙")
            v = "W" if d["winner"] == side else "T" if d["winner"] == "平" else "L"
            out.setdefault((d["track"], mine), []).append((d, v))
        return out

    def outcomes(self, j: str) -> dict[tuple[str, str], str]:
        """两种顺序都判它赢才算赢，都判对照组赢才算输，其余算平。"""
        out = {}
        for k, pair in self.verdicts(j).items():
            vs = [v for _, v in pair]
            out[k] = "W" if all(v == "W" for v in vs) else "L" if all(v == "L" for v in vs) else "T"
        return out

    def record(self, j: str) -> dict[tuple[str, str], list[int]]:
        """每个参赛者每个项目的「赢、平、输」次数。"""
        out: dict[tuple[str, str], list[int]] = {}
        for (track, run), o in self.outcomes(j).items():
            r = out.setdefault((run.rsplit(".", 1)[0], track), [0, 0, 0])
            r["WTL".index(o)] += 1
        return out

    def disputed(self) -> set[tuple[str, str]]:
        """两位评审给出的最终结果不一样的对子，页面上标「有争议」。"""
        if "gpt" not in self.duels:
            return set()
        a, b = self.outcomes("opus"), self.outcomes("gpt")
        return {k for k in a if k in b and a[k] != b[k]}

    # ── 评审体检 ──

    def consistency(self, j: str, track: str | None = None) -> dict:
        """换序一致：同一对稿子甲乙对调后，评审的结论是否不变。"""
        c = Counter()
        for (t, _), pair in self.verdicts(j).items():
            if track and t != track:
                continue
            vs = sorted(v for _, v in pair)
            c["same" if vs[0] == vs[1] else "flip" if vs == ["L", "W"] else "half"] += 1
        c["pairs"] = sum(c.values())
        return dict(c)

    def position(self, j: str, track: str | None = None) -> Counter:
        """判甲、判乙、判平各多少次。不偏的评审，甲和乙应该差不多。"""
        return Counter(d["winner"] for d in self.duels.get(j, []) if not track or d["track"] == track)

    def length(self, j: str, track: str | None = None) -> dict:
        """分出胜负的比较里，判篇幅长的那份赢的次数。"""
        longer = total = 0
        for d in self.duels.get(j, []):
            if d["winner"] == "平" or (track and d["track"] != track):
                continue
            la, lb = len(self.packet(d["a"], d["track"])), len(self.packet(d["b"], d["track"]))
            if la == lb:
                continue
            total += 1
            longer += (d["winner"] == "甲") == (la > lb)
        return {"longer": longer, "decided": total}

    def quotes(self, j: str) -> dict:
        """评审理由里加了引号的原文，能不能在两份稿子里找到。省略号两边分开找，空白不计。"""
        found = total = 0
        misses = []
        for d in self.duels.get(j, []):
            text = SPACE.sub("", self.packet(d["a"], d["track"]) + self.packet(d["b"], d["track"]))
            for m in QUOTE.finditer(d["reason"]):
                q = SPACE.sub("", next(g for g in m.groups() if g))
                bits = [b for b in ELLIPSIS.split(q) if len(b) >= 2]
                if len(q) < 4 or not bits:
                    continue
                total += 1
                if all(b in text for b in bits):
                    found += 1
                else:
                    misses.append((d, q))
        return {"found": found, "total": total, "misses": misses}

    def agreement(self) -> dict:
        """两位评审逐场比较的一致度：每场的胜负、每个维度，以及每对的最终结果。"""
        if "gpt" not in self.duels:
            return {}
        g = {(d["track"], d["a"], d["b"]): d for d in self.duels["gpt"]}
        both = [(d, g[d["track"], d["a"], d["b"]]) for d in self.duels["opus"] if (d["track"], d["a"], d["b"]) in g]
        dims = Counter()
        dims_n = Counter()
        for o, p in both:
            for k, v in o["dims"].items():
                dims_n[k] += 1
                dims[k] += v == p["dims"].get(k)
        oa, ga = self.outcomes("opus"), self.outcomes("gpt")
        keys = [k for k in oa if k in ga]
        return {"calls": len(both), "same": sum(o["winner"] == p["winner"] for o, p in both),
                "kappa": kappa([o["winner"] for o, _ in both], [p["winner"] for _, p in both]),
                "dims": {k: (dims[k], dims_n[k]) for k in dims_n},
                "pairs": len(keys), "pairs_same": sum(oa[k] == ga[k] for k in keys),
                "pairs_kappa": kappa([oa[k] for k in keys], [ga[k] for k in keys]) if keys else 0.0}

    # ── 故事分组 ──

    def group_of(self, j: str) -> dict[str, int]:
        return {c: i for i, g in enumerate(self.groups[j]) for c in g["codes"]}

    def same_type(self, j: str) -> dict:
        """同一个参赛者的几次运行落进同一种故事类型的比例，和不同参赛者之间比。"""
        gid = self.group_of(j)
        within = between = within_n = between_n = 0
        for a, b in combinations(sorted(gid), 2):
            same = gid[a] == gid[b]
            if self.key[a].rsplit(".", 1)[0] == self.key[b].rsplit(".", 1)[0]:
                within_n += 1
                within += same
            else:
                between_n += 1
                between += same
        return {"groups": len(self.groups[j]), "within": within, "within_n": within_n,
                "between": between, "between_n": between_n}

    def cluster_agreement(self) -> float | None:
        if "gpt" not in self.groups:
            return None
        return ari(self.group_of("opus"), self.group_of("gpt"))

    # ── 故事卡里的默认偏好 ──

    def name_count(self, name: str) -> tuple[int, int]:
        """故事卡人名里含某个名字的稿子数，和写过它的参赛者数（含对照组）。"""
        codes = [c["code"] for c in self.cards if any(name in n for n in c["names"])]
        return len(codes), len({self.key[c].rsplit(".", 1)[0] for c in codes})

    def paywalls(self) -> Counter:
        return Counter(c["first_paywall_episode"] for c in self.cards)


def pct(k: int, n: int) -> str:
    """百分比；不到 10% 的留一位小数。"""
    if not n:
        return "—"
    return f"{k / n:.1%}" if 0 < k / n < 0.1 else f"{k / n:.0%}"


def main() -> None:
    r = Round(sys.argv[1] if len(sys.argv) > 1 else "001-open-brief")
    for j in r.duels:
        print(f"== 评审 {j}")
        rec = r.record(j)
        for s in r.slugs:
            print(f"  {s:55} 剧本 {'-'.join(map(str, rec.get((s, 'script'), [0, 0, 0])))}"
                  f"  人物大纲 {'-'.join(map(str, rec.get((s, 'outline'), [0, 0, 0])))}")
        for t in judge.TRACKS:
            c, p, ln = r.consistency(j, t), r.position(j, t), r.length(j, t)
            print(f"  {t}: 换序一致 {c.get('same', 0)}/{c['pairs']}，判甲 {p['甲']} 判乙 {p['乙']} 判平 {p['平']}，"
                  f"判长的赢 {ln['longer']}/{ln['decided']}")
        q = r.quotes(j)
        print(f"  引文找得到 {q['found']}/{q['total']}（{pct(q['found'], q['total'])}）")
    a = r.agreement()
    if a:
        print(f"== 两位评审：逐场一致 {a['same']}/{a['calls']}，kappa {a['kappa']:.2f}；"
              f"最终结果一致 {a['pairs_same']}/{a['pairs']}，kappa {a['pairs_kappa']:.2f}；有争议 {len(r.disputed())} 对")
    for j in r.groups:
        s = r.same_type(j)
        print(f"== 故事分组 {j}：{s['groups']} 组；同一参赛者 {s['within']}/{s['within_n']}，"
              f"不同参赛者 {s['between']}/{s['between_n']}")
    if r.cluster_agreement() is not None:
        print(f"   两种分组的调整兰德指数 {r.cluster_agreement():.2f}")
    print(f"== 小满 {r.name_count('小满')}，第一个付费卡点 {dict(r.paywalls())}")


if __name__ == "__main__":
    main()
