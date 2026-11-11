#!/usr/bin/env python3
"""지원 플랫폼 목록을 직군 파일(guides/jobs/*.md)과 career.py에서 다시 만든다.

- SITES.md: 전체 목록을 통째로 새로 쓴다.
- README.md: <!-- sites:start --> ~ <!-- sites:end --> 사이에 요약만 넣는다.
사용: python3 tools/gen_sites_readme.py
직군 파일이나 career.py의 SITES·SITE_NAMES를 바꾸면 이걸 다시 돌린다.
"""

import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import career  # noqa: E402

URL_RE = re.compile(r"`(?:POST\s+)?(https?://[^`\s]+)`")


def human_url(url: str) -> str:
    """에이전트용 주소(JSON·API·{키워드})를 사람이 여는 주소로 바꾼다."""
    u = urllib.parse.urlsplit(url.replace("{키워드}", ""))
    if re.search(r"api|json|\.json|_json", u.path, re.I):
        return f"{u.scheme}://{u.netloc}"
    q = [(k, v) for k, v in urllib.parse.parse_qsl(u.query, keep_blank_values=True) if v]
    return urllib.parse.urlunsplit((u.scheme, u.netloc, u.path, urllib.parse.urlencode(q, safe="{}%"), ""))


def short(desc: str) -> str:
    desc = re.split(r"[.(]|\s—\s|키워드는|검색은|화면은", desc)[0].strip(" ,—-")
    return desc[:60]


def parse_job_file(path: pathlib.Path):
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^#\s+(.*)", text, re.M)
    title = m.group(1).strip() if m else path.stem
    sec = text.split("## 어디서 찾나", 1)[-1].split("## 검색 예시", 1)[0]
    script_line, sites = "", []
    for line in sec.splitlines():
        s = line.strip()
        if not s.startswith("- "):
            continue
        body = s[2:]
        if body.startswith("스크립트"):
            script_line = ", ".join(sorted(set(re.findall(r"[a-z0-9]+", " ".join(re.findall(r"`([^`]+)`", body))))))
            continue
        if body.startswith("표시:") or (body.endswith(":") and "`" not in body):
            continue                                   # 묶음 제목 줄
        m = URL_RE.search(body)
        if m:
            name = body[: m.start()].strip().rstrip(":").strip()
            if ": " in name:
                name = name.split(": ")[-1]
            name = re.sub(r"\s*\(.*?\)\s*$", "", name).strip()
            if "(" in name and ")" not in name:          # "이름 (설명: `URL`" 꼴
                name = name.split("(")[0].strip()
            name = name or urllib.parse.urlsplit(m.group(1)).netloc
            desc = body[m.end():].lstrip(" :—-)")
            if desc.startswith(("전국", "JSON")) or desc.startswith("`"):
                desc = ""
            sites.append((name, human_url(m.group(1)), short(desc)))
        elif "(앱 전용" in body:
            name = body.split("(앱 전용")[0].split(": ")[-1].strip(" -")
            desc = body.split("—", 1)[-1] if "—" in body else ""
            sites.append((name + " (앱)", None, short(desc)))
    return title, script_line, sites


SUMMARY: list = []


def build():
    names = {k: v for k, v in getattr(career, "SITE_NAMES", {}).items()}
    out = ["# 지원 플랫폼 전체 목록", "", "이 파일은 `python3 tools/gen_sites_readme.py`가 직군 파일과 career.py에서 자동으로 만들어요. 손으로 고치지 마세요.", ""]
    out.append("### 스크립트로 바로 검색 (`career.py search --sites`)")
    out.append("")
    keys = list(career.SITES)
    engine = set(getattr(career, "GNU_SITES", {})) | set(getattr(career, "S2_SITES", {})) \
        | set(getattr(career, "LINK_SITES", {}))
    # career.py는 주요 사이트를 먼저, 직군 전문 사이트를 공통 엔진 등록부터 뒤에 등록한다.
    cut = min((keys.index(k) for k in engine), default=len(keys))
    groups = (("종합·공공·주요 사이트", keys[:cut]), ("직군 전문 사이트", keys[cut:]))
    for gname, keys in groups:
        out.append(f"**{gname}** ({len(keys)}곳)")
        out.append("")
        out.append("| `--sites` 값 | 사이트 — 강점 |")
        out.append("|---|---|")
        for key in keys:
            out.append(f"| `{key}` | {names.get(key, key)} |")
        out.append("")
    out.append("### 직군별 전문 사이트 (에이전트 브라우저로 열거나 링크로 확인)")
    out.append("")
    out.append("직군 파일마다 세부 직무·사람인 직무 코드·검색 주소가 더 자세히 있어요. 빠진 사이트는 오픈채팅방으로 알려 주세요.")
    out.append("")
    total = 0
    for path in sorted((ROOT / "guides" / "jobs").glob("[0-9][0-9]-*.md")):
        title, script_keys, sites = parse_job_file(path)
        out.append(f"#### {title}")
        out.append("")
        if script_keys:
            out.append(f"- 스크립트: `{script_keys}`")
        seen = set()
        for name, url, desc in sites:
            if (name, url) in seen:
                continue
            seen.add((name, url))
            total += 1
            link = f"[{name}]({url})" if url else name
            out.append(f"- {link}" + (f" — {desc}" if desc else ""))
        out.append(f"- 자세히: [`guides/jobs/{path.name}`](guides/jobs/{urllib.parse.quote(path.name)})")
        SUMMARY.append((title, [n for n, _, _ in sites][:4], path.name))
        out.append("")
    out.insert(4, f"스크립트 검색 {len(career.SITES)}곳 + 직군별 전문 사이트·협회·공공·앱 {total}곳(직군 간 중복 포함).\n")
    return "\n".join(out).rstrip() + "\n", total


def readme_summary(total: int) -> str:
    keys = list(career.SITES)
    out = ["## 지원 플랫폼", "",
           f"- 스크립트로 바로 검색: **{len(keys)}곳** (사람인·잡코리아·원티드·리멤버·자소설닷컴·고용24·잡알리오 등 + 간호·제빵·건설·미용 등 직군 전문 사이트)",
           f"- 직군 25개마다 전문 사이트·협회·공공·앱 안내: **{total}곳** (직군 간 중복 포함)",
           "- 전체 목록: [SITES.md](SITES.md)", "",
           "| 직군 | 대표 전문 사이트 (일부) |", "|---|---|"]
    for title, names, fname in SUMMARY:
        out.append(f"| [{title}](guides/jobs/{urllib.parse.quote(fname)}) | {', '.join(names) or '-'} |")
    return "\n".join(out) + "\n"


def main():
    full, total = build()
    (ROOT / "SITES.md").write_text(full, encoding="utf-8")
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    block = "<!-- sites:start -->\n" + readme_summary(total) + "<!-- sites:end -->"
    if "<!-- sites:start -->" not in text:
        raise SystemExit("README.md에 <!-- sites:start --> / <!-- sites:end --> 표시가 없어요.")
    text = re.sub(r"<!-- sites:start -->.*?<!-- sites:end -->", lambda _: block, text, flags=re.S)
    readme.write_text(text, encoding="utf-8")
    print(f"SITES.md·README 요약 갱신 완료 (스크립트 {len(career.SITES)}곳, 직군별 {total}곳)")


if __name__ == "__main__":
    main()
