#!/usr/bin/env python3
"""career.py — AI 에이전트용 취업·이직 도우미 스크립트 (파이썬 기본 기능만 사용).

명령:
  search  공고 검색 (사람인·잡코리아·금투협). 결과를 짧은 마크다운으로 출력
  links   자동 수집을 약관으로 막은 사이트의 검색 링크 (리멤버·자소설닷컴 등)
  job     공고 URL 하나의 본문을 텍스트로 출력
  docx    마크다운 파일을 워드(.docx)로 변환 (python-docx 있을 때)

원칙 (README '약관 지키기' 참고):
  - 사용자가 요청할 때만, 한 번 실행에 요청 수를 제한하고, 같은 사이트는 1초 이상 간격.
  - 우리를 숨기지 않는다: 고정된 User-Agent에 이 저장소 주소를 밝힌다.
  - 자동 수집을 약관으로 금지한 사이트(리멤버·자소설닷컴)는 긁지 않고 링크만 준다.
  - 결과는 사용자 본인의 구직에만 쓴다. 다른 곳에 다시 게시하지 않는다.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import ipaddress
import json
import os
import re
import socket
import sys
import time
import urllib.parse
import urllib.request

VERSION = "0.1.0"
REPO = "https://github.com/Whosekey-Labs/career-skill"
USER_AGENT = f"career-skill/{VERSION} (+{REPO}; personal job search helper)"
MAX_REQUESTS = 8          # 한 번 실행에서 보낼 수 있는 최대 요청 수
SAME_HOST_GAP = 1.0       # 같은 사이트 요청 사이 최소 간격(초)
DATA_DIR = os.environ.get("CAREER_DATA_DIR", "career_data")

_last_hit: dict[str, float] = {}
_request_count = 0


# ---------------------------------------------------------------- 공통 HTTP

def check_url(url: str) -> None:
    """http/https만, 내부망·로컬 주소는 거부한다 (로컬 파일 읽기·내부망 접근 방지)."""
    u = urllib.parse.urlparse(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        raise RuntimeError("http/https 공고 주소만 열 수 있어요.")
    try:
        infos = socket.getaddrinfo(u.hostname, None)
    except socket.gaierror as e:
        raise RuntimeError(f"주소를 찾을 수 없어요: {u.hostname}") from e
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            raise RuntimeError("내부망·로컬 주소는 열 수 없어요.")


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_opener = urllib.request.build_opener(_SafeRedirect)


def fetch(url: str, accept: str = "text/html") -> str:
    """같은 사이트는 간격을 두고, 실행당 요청 수를 제한해서 가져온다."""
    global _request_count
    if _request_count >= MAX_REQUESTS:
        raise RuntimeError(f"한 번 실행에 요청은 {MAX_REQUESTS}번까지예요. 키워드를 줄여 주세요.")
    check_url(url)
    host = urllib.parse.urlparse(url).netloc
    wait = SAME_HOST_GAP - (time.time() - _last_hit.get(host, 0))
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": accept,
        "Accept-Language": "ko-KR,ko;q=0.9",
    })
    _request_count += 1
    try:
        with _opener.open(req, timeout=20) as res:
            body = res.read().decode(res.headers.get_content_charset() or "utf-8", "replace")
    finally:
        _last_hit[host] = time.time()
    return body


def strip_tags(s: str) -> str:
    s = re.sub(r"(?is)<(script|style|noscript|iframe)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</(p|div|li|tr|h\d)>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


def job(**kw) -> dict:
    base = dict(title="", company=None, location=None, experience=None, salary=None,
                deadline=None, url=None, employmentType=None, postedDate=None, site=None)
    base.update({k: v for k, v in kw.items() if v not in ("", None)})
    return base


# ---------------------------------------------------------------- 사람인

SARAMIN_LOC = {
    "서울": "101000", "경기": "102000", "인천": "108000", "부산": "106000", "대구": "104000",
    "광주": "103000", "대전": "105000", "울산": "107000", "세종": "118000", "강원": "109000",
    "충북": "114000", "충남": "115000", "전북": "113000", "전남": "112000", "경북": "111000",
    "경남": "110000", "제주": "116000",
}
SARAMIN_EXP = {"신입": "1", "경력무관": "3", "경력": "2"}
SARAMIN_SAL = [(10000, "22"), (9000, "21"), (8000, "20"), (7000, "19"), (6000, "18"),
               (5000, "17"), (4000, "16"), (3800, "15"), (3600, "14"), (3400, "13"),
               (3200, "12"), (3000, "11"), (2800, "10"), (2600, "9"), (2400, "8")]
SARAMIN_EMP = {"정규직": "1", "계약직": "2", "인턴": "3", "파견": "4", "프리랜서": "6", "아르바이트": "7"}
LOC_RE = re.compile(r"서울|경기|인천|부산|대구|광주|대전|울산|세종|강원|충북|충남|전북|전남|경북|경남|제주")
EMP_RE = re.compile(r"정규직|계약직|인턴|파견|프리랜서|아르바이트")


def saramin(keyword: str, f: dict, limit: int) -> list[dict]:
    qs = {"searchType": "search", "searchword": keyword, "recruitPageCount": "40",
          "recruitSort": "relation"}
    if f.get("location"):
        for name, code in SARAMIN_LOC.items():
            if name in f["location"]:
                qs["loc_mcd"] = code
                break
    if f.get("experience"):
        for name, code in SARAMIN_EXP.items():
            if name in f["experience"]:
                qs["exp_cd"] = code
                break
    if f.get("salary"):
        n = int(re.sub(r"\D", "", f["salary"]) or 0)
        for th, code in SARAMIN_SAL:
            if n >= th:
                qs["sal_min"] = code
                break
    if f.get("empType"):
        for name, code in SARAMIN_EMP.items():
            if name in f["empType"]:
                qs["job_type"] = code
                break
    page = fetch("https://www.saramin.co.kr/zf_user/search?" + urllib.parse.urlencode(qs))
    out = []
    for block in page.split('class="item_recruit"')[1:]:
        m = re.search(r'class="job_tit">\s*<a[^>]*href="([^"]+)"[^>]*title="([^"]*)"', block) or \
            re.search(r'class="job_tit">\s*<a[^>]*title="([^"]*)"[^>]*href="([^"]+)"', block)
        if not m:
            continue
        href, title = (m.group(1), m.group(2)) if m.group(1).startswith(("/", "http")) else (m.group(2), m.group(1))
        rec = re.search(r"rec_idx=(\d+)", href)
        url = f"https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx={rec.group(1)}" if rec else \
            urllib.parse.urljoin("https://www.saramin.co.kr", html.unescape(href))
        cm = re.search(r'class="corp_name">\s*<a[^>]*>([^<]+)', block)
        conds = [strip_tags(x) for x in re.findall(r"<span[^>]*>(.*?)</span>",
                 (re.search(r'class="job_condition">(.*?)</div>', block, re.S) or [None, ""])[1], re.S)]
        loc = exp = emp = sal = None
        for t in conds:
            if not exp and re.search(r"신입|경력|년", t):
                exp = t
            elif not loc and LOC_RE.search(t):
                loc = t
            elif not emp and EMP_RE.search(t):
                emp = t
            elif not sal and ("만원" in t or "억" in t):
                sal = t
        dm = re.search(r'class="date">([^<]+)', block)
        out.append(job(title=html.unescape(title).strip(), company=cm and html.unescape(cm.group(1)).strip(),
                       location=loc, experience=exp, employmentType=emp, salary=sal,
                       deadline=dm and dm.group(1).strip(), url=url, site="사람인"))
        if len(out) >= limit:
            break
    return out


# ---------------------------------------------------------------- 잡코리아

JK_AREA_PREFIX = {"I": "서울", "B": "경기", "K": "인천", "H": "부산", "F": "대구", "E": "광주",
                  "G": "대전", "J": "울산", "Q": "세종", "A": "강원", "P": "충북", "O": "충남",
                  "M": "전북", "L": "전남", "D": "경북", "C": "경남", "N": "제주"}
JK_CAREER = {"0": "경력무관", "1": "신입", "2": "경력", "3": "신입·경력", "4": "경력무관"}


def jobkorea(keyword: str, f: dict, limit: int) -> list[dict]:
    qs = {"stext": keyword, "tabType": "recruit"}
    if f.get("experience"):
        qs["careerType"] = "1" if "신입" in f["experience"] else "4" if "무관" in f["experience"] else "2"
    page = fetch("https://www.jobkorea.co.kr/Search/?" + urllib.parse.urlencode(qs))
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.+?)"\]\)', page)
    merged = "".join(chunks).replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")
    out, seen = [], set()
    for m in re.finditer(r'"id":"(\d+)","legacyJobNo":"[^"]*","title":"([^"]*)"', merged):
        pid, title = m.group(1), m.group(2)
        if pid in seen:
            continue
        seen.add(pid)
        ctx = merged[m.start(): m.start() + 900]

        def field(name):
            s = re.search(rf'"{name}":"([^"]*)"', ctx) or re.search(rf'"{name}":(\d+)', ctx)
            return s.group(1) if s else None

        ct, cr = field("careerType"), field("careerRange")
        exp = JK_CAREER.get(ct or "", "")
        if ct == "2" and cr and cr not in ("0", "100"):
            exp += f" {cr}년 이상"
        end = re.search(r'"end":"([^"]+)"', ctx)
        area = re.search(r'"areaCodeList":\[([^\]]*)\]', ctx)
        loc = None
        if area:
            codes = [c for c in area.group(1).replace('"', "").split(",") if c]
            loc = ", ".join(dict.fromkeys(JK_AREA_PREFIX.get(c[:1], c) for c in codes))
        out.append(job(title=_u(title), company=_u(field("companyName") or field("postingCompanyName")),
                       experience=exp.strip(), deadline=end and end.group(1)[:10], location=loc,
                       url=f"https://www.jobkorea.co.kr/Recruit/GI_Read/{pid}", site="잡코리아"))
    if f.get("location"):
        out = [j for j in out if not j["location"] or any(x in j["location"] for x in LOC_RE.findall(f["location"]) or [f["location"]])]
    return out[:limit]


def _u(s):
    if not s:
        return s
    try:
        return json.loads(f'"{s}"')
    except Exception:
        return s


# ---------------------------------------------------------------- 금융투자협회

def kofia(keyword: str, f: dict, limit: int) -> list[dict]:
    url = "https://www.kofia.or.kr/brd/m_96/list.do"
    if keyword:
        url += "?" + urllib.parse.urlencode({"srchTp": "0", "srchWord": keyword})
    page = fetch(url)
    out = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", page, re.S):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
        if len(cells) < 5:
            continue
        title = strip_tags(cells[2])
        link = re.search(r'href="([^"]*view\.do[^"]*)"', cells[2])
        if not title:
            continue
        out.append(job(title=title, company=strip_tags(cells[1]), postedDate=strip_tags(cells[4]),
                       url=link and _kofia_url(link.group(1)),
                       site="금투협"))
        if len(out) >= limit:
            break
    return out


def _kofia_url(href):
    seq = re.search(r"seq=(\d+)", html.unescape(href))
    return f"https://www.kofia.or.kr/brd/m_96/view.do?seq={seq.group(1)}" if seq else None


SITES = {"saramin": saramin, "jobkorea": jobkorea, "kofia": kofia}


# ---------------------------------------------------------------- 정리 (만료·중복·정렬)

EXPIRED_RE = re.compile(r"[\(\[]\s*(채용\s*마감|마감|모집\s*(마감|종료|완료)|접수\s*(마감|완료)|종료)\s*[\)\]]|D\s*-\s*(종료|마감)")


def parse_deadline(text, today):
    if not text:
        return None
    if "오늘" in text:
        return today
    if "내일" in text:
        return today + dt.timedelta(days=1)
    m = re.search(r"(\d{4})[-./](\d{1,2})[-./](\d{1,2})", text)
    if m:
        try:
            return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    m = re.search(r"(\d{1,2})[/.월]\s*(\d{1,2})", text)
    if m:
        try:
            d = dt.date(today.year, int(m.group(1)), int(m.group(2)))
        except ValueError:
            return None
        if d < today - dt.timedelta(days=14):   # 연도 넘김(12월→1월)만 다음 해로 본다
            d = d.replace(year=today.year + 1) if today.month >= 11 and d.month <= 2 else None
        return d
    return None


def norm_company(s):
    s = re.sub(r"주식회사|\(주\)|㈜|\(유\)|유한회사|co\.?,?\s*ltd\.?|inc\.?|corp\.?", " ", (s or ""), flags=re.I)
    return re.sub(r"[\W_]+", "", s.lower())


def tidy(jobs, today):
    live, seen = [], {}
    for j in jobs:
        if EXPIRED_RE.search(j["title"] or "") or EXPIRED_RE.search(j["deadline"] or ""):
            continue
        d = parse_deadline(j["deadline"], today)
        if d and d < today:
            continue
        posted = parse_deadline(j["postedDate"], today) if j["postedDate"] else None
        if posted and (today - posted).days > 90:
            continue
        key = norm_company(j["company"]) + "|" + re.sub(r"[\W_]+", "", (j["title"] or "").lower())
        if key in seen:
            other = seen[key]
            if j["url"] != other["url"]:
                other.setdefault("alsoOn", []).append(f'{j["site"]}: {j["url"]}')
            continue
        j["_d"] = d
        seen[key] = j
        live.append(j)
    live.sort(key=lambda j: (j["_d"] or dt.date.max))
    return live


def render(jobs, today, header):
    if not jobs:
        return header + "\n\n조건에 맞는 공고를 찾지 못했어요. 키워드를 넓히거나 지역·경력 조건을 줄여 보세요."
    soon = [j for j in jobs if j["_d"] and (j["_d"] - today).days <= 7]
    rest = [j for j in jobs if j not in soon]
    lines, n = [header], 0
    for name, group in (("마감 임박 (7일 안)", soon), ("그 외", rest)):
        if not group:
            continue
        lines.append(f"\n### {name}")
        for j in group:
            n += 1
            meta = " · ".join(x for x in (j["experience"], j["salary"], j["location"], j["employmentType"],
                                         j["deadline"] and f'마감 {j["deadline"]}') if x)
            lines.append(f'{n}. **{j["company"] or "회사명 없음"}** {j["title"]}')
            if meta:
                lines.append(f"   - {meta}")
            lines.append(f'   - {j["site"]}: {j["url"]}')
            for extra in j.get("alsoOn", []):
                lines.append(f"   - {extra}")
    return "\n".join(lines)


# ---------------------------------------------------------------- 새 공고만 (매일 알림용)

def seen_path():
    return os.path.join(DATA_DIR, "seen.json")


def filter_new(jobs):
    try:
        with open(seen_path(), encoding="utf-8") as fp:
            seen = set(json.load(fp))
    except (OSError, ValueError):
        seen = set()
    new = [j for j in jobs if j["url"] not in seen]
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(seen_path(), "w", encoding="utf-8") as fp:
        json.dump(sorted(seen | {j["url"] for j in jobs if j["url"]}), fp, ensure_ascii=False)
    return new


# ---------------------------------------------------------------- 명령

def cmd_search(a):
    today = dt.date.today()
    keywords = [k.strip() for k in ",".join(a.keyword).split(",") if k.strip()]
    sites = [s.strip() for s in a.sites.split(",") if s.strip()]
    f = {"location": a.location, "experience": a.experience, "salary": a.salary, "empType": a.emp_type}
    found, errors = [], []
    for kw in keywords:
        for s in sites:
            if s not in SITES:
                errors.append(f"{s}: 지원하지 않는 사이트 (가능: {', '.join(SITES)}) — 다른 사이트는 links 명령 사용")
                continue
            try:
                found += SITES[s](kw, f, a.limit)
            except Exception as e:  # 한 사이트가 실패해도 나머지는 계속
                errors.append(f"{s}/{kw}: {e}")
    jobs = tidy(found, today)
    if a.new_only:
        jobs = filter_new(jobs)
    jobs = jobs[: a.max]
    if a.json:
        for j in jobs:
            j.pop("_d", None)
        print(json.dumps({"jobs": jobs, "errors": errors}, ensure_ascii=False))
        return
    cond = " · ".join(x for x in (a.location, a.experience, a.salary and f"{a.salary}만원 이상", a.emp_type) if x)
    head = f"## 공고 {len(jobs)}건 — {', '.join(keywords)}" + (f" ({cond})" if cond else "") + \
        (" · 새 공고만" if a.new_only else "")
    print(render(jobs, today, head))
    if errors:
        print("\n(일부 실패: " + " / ".join(errors) + ")")


def cmd_links(a):
    q = urllib.parse.quote(a.keyword)
    print(f"""## 직접 열어 볼 검색 링크 — {a.keyword}
(리멤버·자소설닷컴은 약관으로 자동 수집을 금지하고, 나머지는 아직 약관을 확인하지 않아서 스크립트로 긁지 않아요. 사용자가 원하면 링크를 열어 보거나, 에이전트 브라우저로 사람처럼 한 페이지씩만 보세요.)
- 리멤버 (경력직·헤드헌팅): https://career.rememberapp.co.kr/job/postings  ← 검색창에 "{a.keyword}" 입력
- 자소설닷컴 (대기업 공채·신입): https://jasoseol.com/search?keyword={q}
- 잡알리오 (공공기관): https://job.alio.go.kr/recruit.do
- 고용24 (공공·지역 일자리): https://www.work24.go.kr/
- 원티드 (IT·스타트업): https://www.wanted.co.kr/search?query={q}
- 링커리어 (대학생 인턴·대외활동): https://linkareer.com/list/intern""")


# 리멤버(약관 제13조①24호)·자소설닷컴(제14조 9호)은 자동 수집 금지. 원티드·링커리어는 미확인이라 보수적으로 막음.
BLOCKED_HOSTS = ("rememberapp.co.kr", "jasoseol.com", "wanted.co.kr", "linkareer.com")


def cmd_job(a):
    url = a.url.strip()
    host = urllib.parse.urlparse(url).netloc
    if any(h in host for h in BLOCKED_HOSTS):
        print("이 사이트는 약관상 자동 수집을 막고 있어요. 에이전트 브라우저로 이 공고 한 페이지만 열어서 읽거나, "
              "사용자에게 공고 내용을 복사해 붙여 달라고 하세요.")
        return
    text = ""
    rec = re.search(r"rec_idx=(\d+)", url)
    gno = re.search(r"GI_Read/(\d+)", url)
    if "saramin.co.kr" in host and rec:
        text = strip_tags(fetch(f"https://www.saramin.co.kr/zf_user/jobs/relay/view-detail?rec_idx={rec.group(1)}"))
    elif "jobkorea.co.kr" in host and gno:
        page = fetch(f"https://www.jobkorea.co.kr/Recruit/GI_Read/{gno.group(1)}")
        t = re.search(r"<title>([^<]+)", page)
        d = re.search(r'<meta name="description" content="([^"]*)', page)
        body = strip_tags(fetch(f"https://www.jobkorea.co.kr/Recruit/GI_Read_Comt_Ifrm?Gno={gno.group(1)}"))
        text = "\n".join(x for x in (t and html.unescape(t.group(1)), d and html.unescape(d.group(1)), body) if x)
    else:
        page = fetch(url)
        m = re.search(r"(?is)<(article|main)[^>]*>(.*?)</\1>", page)
        text = strip_tags(m.group(2) if m else page)
    if len(text) < 200:
        print(text + "\n\n(본문이 짧아요. 이미지로 된 공고일 수 있어요. 에이전트 브라우저로 공고를 열어 직접 읽어 주세요.)")
        return
    print(text[: a.max_chars] + ("\n…(뒤는 생략)" if len(text) > a.max_chars else ""))


def cmd_docx(a):
    try:
        import docx  # python-docx
    except ImportError:
        print("python-docx가 없어요. 마크다운 파일을 그대로 전달하거나, 에이전트의 문서 만들기 기능을 쓰세요.")
        sys.exit(1)
    doc = docx.Document()
    with open(a.input, encoding="utf-8") as fp:
        for line in fp.read().splitlines():
            s = line.rstrip()
            if not s or s.strip() == "---":
                continue
            h = re.match(r"^(#{1,4})\s+(.*)", s)
            if h:
                doc.add_heading(h.group(2), level=min(len(h.group(1)), 3))
                continue
            li = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)", s)
            p = doc.add_paragraph(style="List Bullet" if li else None)
            for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", li.group(1) if li else s)):
                if part:
                    p.add_run(part).bold = bool(i % 2)
    out = a.output or os.path.splitext(a.input)[0] + ".docx"
    doc.save(out)
    print(out)


def main():
    ap = argparse.ArgumentParser(description="AI 에이전트용 취업·이직 도우미")
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="공고 검색")
    s.add_argument("--keyword", "-k", action="append", required=True, help="키워드 (쉼표로 여러 개)")
    s.add_argument("--sites", default="saramin,jobkorea", help="saramin,jobkorea,kofia 중 쉼표로")
    s.add_argument("--location")
    s.add_argument("--experience", help="신입 / 경력 / 경력무관")
    s.add_argument("--salary", help="최소 연봉(만원), 사람인만 적용")
    s.add_argument("--emp-type", help="정규직 / 계약직 / 인턴 …")
    s.add_argument("--limit", type=int, default=10, help="사이트·키워드당 최대")
    s.add_argument("--max", type=int, default=15, help="최종 출력 최대")
    s.add_argument("--new-only", action="store_true", help="이전에 보여준 공고 빼기")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_search)

    l = sub.add_parser("links", help="직접 열어 볼 사이트 검색 링크")
    l.add_argument("--keyword", "-k", required=True)
    l.set_defaults(fn=cmd_links)

    j = sub.add_parser("job", help="공고 본문 가져오기")
    j.add_argument("--url", required=True)
    j.add_argument("--max-chars", type=int, default=6000)
    j.set_defaults(fn=cmd_job)

    d = sub.add_parser("docx", help="마크다운 → 워드")
    d.add_argument("--input", "-i", required=True)
    d.add_argument("--output", "-o")
    d.set_defaults(fn=cmd_docx)

    a = ap.parse_args()
    try:
        a.fn(a)
    except Exception as e:
        print(f"오류: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
