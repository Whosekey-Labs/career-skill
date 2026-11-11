#!/usr/bin/env python3
"""career.py — AI 에이전트용 취업·이직 도우미 스크립트 (파이썬 기본 기능만 사용).

명령:
  search  공고 검색 (사람인·잡코리아·원티드·점핏·리멤버·자소설닷컴·금투협·리츠협회·잡알리오·나라일터·월드잡).
          결과를 마감순 짧은 마크다운으로 출력
  links   스크립트로 못 여는 사이트(캐치·링커리어·고용24 등)의 검색 링크 — 에이전트 브라우저로 연다
  job     공고 URL 하나의 본문을 텍스트로 출력
  docx    마크다운 파일을 워드(.docx)로 변환 (python-docx 있을 때)

동작 원칙:
  - 본인 구직용 도구. 일반 브라우저 User-Agent 하나를 고정해서 쓴다.
  - 같은 사이트는 1초 + 0~0.8초 랜덤 간격, 한 번 실행에 요청 12번까지 (접속 차단 방지).
  - 끊김·시간 초과·5xx는 한 번 더 시도한다.
  - 허용 목록(ALLOWED_HOSTS)에 있는 채용 사이트 주소만 연다.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import http.client
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

VERSION = "0.3.0"
REPO = "https://github.com/Whosekey-Labs/career-skill"
# 일반 브라우저와 같은 값 하나만 쓴다 (바꿔 가며 속이지 않는다).
USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
MAX_REQUESTS = 12         # 한 번 실행에서 보낼 수 있는 최대 요청 수 (사이트 부담·IP 차단 방지)
SAME_HOST_GAP = 1.0       # 같은 사이트 요청 사이 기본 간격(초)
GAP_JITTER = 0.8          # 여기에 0~0.8초 랜덤을 더한다 (일정한 간격은 기계처럼 보인다)
DATA_DIR = os.environ.get("CAREER_DATA_DIR", "career_data")

_last_hit: dict[str, float] = {}
_request_count = 0


# ---------------------------------------------------------------- 공통 HTTP

# 스크립트가 직접 여는 사이트 목록. 여기에 없는 주소는 에이전트 브라우저로 연다.
# (임의 주소를 열지 않으므로 로컬 파일·내부망 접근이 원천적으로 불가능하다.)
ALLOWED_HOSTS = ("saramin.co.kr", "jobkorea.co.kr", "kofia.or.kr", "alio.go.kr", "gojobs.go.kr",
                 "worldjob.or.kr", "kareit.or.kr", "wanted.co.kr", "rememberapp.co.kr", "jasoseol.com",
                 "jumpit-api.saramin.co.kr")


def check_url(url: str) -> None:
    """https/http + 허용된 채용 사이트 호스트만 통과시킨다."""
    u = urllib.parse.urlparse(url)
    netloc = u.netloc.lower()
    if u.scheme not in ("http", "https") or not netloc or re.search(r"[^a-z0-9.\-]", netloc):
        raise RuntimeError("공고 주소 형식이 아니에요.")
    if not any(netloc == h or netloc.endswith("." + h) for h in ALLOWED_HOSTS):
        raise RuntimeError("스크립트가 여는 사이트가 아니에요.")


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_opener = urllib.request.build_opener(_SafeRedirect)


def fetch(url: str, accept: str = "text/html", data: bytes | None = None) -> str:
    """같은 사이트는 간격을 두고, 실행당 요청 수를 제한해서 가져온다."""
    global _request_count
    if _request_count >= MAX_REQUESTS:
        raise RuntimeError(f"한 번 실행에 요청은 {MAX_REQUESTS}번까지예요. 키워드를 줄여 주세요.")
    check_url(url)
    host = urllib.parse.urlparse(url).netloc
    wait = SAME_HOST_GAP + random.uniform(0, GAP_JITTER) - (time.time() - _last_hit.get(host, 0))
    if wait > 0:
        time.sleep(wait)
    headers = {"User-Agent": USER_AGENT, "Accept": accept, "Accept-Language": "ko-KR,ko;q=0.9"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    _request_count += 1
    for attempt in range(2):          # 끊김·시간 초과·5xx는 잠깐 쉬고 한 번 더
        try:
            with _opener.open(req, timeout=20) as res:
                body = res.read().decode(res.headers.get_content_charset() or "utf-8", "replace")
            return body
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt:
                raise RuntimeError(f"{host} 응답 오류 {e.code}") from e
        except (http.client.IncompleteRead, TimeoutError, urllib.error.URLError, ConnectionError) as e:
            if attempt:
                raise RuntimeError(f"{host} 연결이 불안정해요: {e}") from e
        finally:
            _last_hit[host] = time.time()
        time.sleep(2 + random.uniform(0, 1))
    raise RuntimeError(f"{host} 연결 실패")


def strip_tags(s: str) -> str:
    s = re.sub(r"(?is)<(script|style|noscript|iframe)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</(p|div|li|tr|h\d)>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


def job(**kw) -> dict:
    base = dict(title="", company=None, location=None, experience=None, salary=None,
                deadline=None, url=None, employmentType=None, postedDate=None, site=None)
    for k, v in kw.items():
        if isinstance(v, str):
            v = " ".join(v.split())     # 줄바꿈·연속 공백 정리
        if v not in ("", None):
            base[k] = v
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
    qs = {"recruitPageCount": "40", "recruitSort": "relation"}
    if keyword:
        qs.update(searchType="search", searchword=keyword)
    if f.get("jobCode"):      # 사람인 직무 코드 (guides/jobs/*.md 의 S숫자, 쉼표로 여러 개 = OR)
        qs["cat_kewd"] = f["jobCode"]
    if f.get("industry"):     # 사람인 산업 코드 (ind_cd)
        qs["ind_cd"] = f["industry"]
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
    page = fetch("https://www.saramin.co.kr/zf_user/search/recruit?" + urllib.parse.urlencode(qs))
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


# ---------------------------------------------------------------- 잡알리오 (공공기관)

def alio(keyword: str, f: dict, limit: int) -> list[dict]:
    qs = {"pageNo": "1", "ing": "2", "search_type": "title", "keyword": keyword}
    page = fetch("https://job.alio.go.kr/recruit.do?" + urllib.parse.urlencode(qs))
    out = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", page, re.S):
        m = re.search(r'href="/recruitview\.do\?idx=(\d+)"[^>]*>(.*?)</a>', row, re.S)
        if not m:
            continue
        cells = [strip_tags(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
        # 칸 순서: 선택, 번호, 제목, 기관, 지역, 고용형태, 등록일, 마감일
        tail = cells[3:] + [None] * 5
        dl = tail[4] and re.sub(r"^(\d{2})\.", r"20\1.", tail[4].split()[0])
        out.append(job(title=strip_tags(m.group(2)), company=tail[0], location=tail[1],
                       employmentType=tail[2], postedDate=tail[3], deadline=dl,
                       url=f"https://job.alio.go.kr/recruitview.do?idx={m.group(1)}", site="잡알리오"))
        if len(out) >= limit:
            break
    return out


# ---------------------------------------------------------------- 나라일터 (공무원 임기제·경력경쟁·공무직)

def gojobs(keyword: str, f: dict, limit: int) -> list[dict]:
    qs = {"menuNo": "401", "mngrMenuYn": "N", "searchKeyword": keyword, "pageIndex": "1"}
    page = fetch("https://www.gojobs.go.kr/apmList.do?" + urllib.parse.urlencode(qs))
    body = page.split("<tbody>", 1)[-1]
    out = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S):
        m = re.search(r"fn_apmView\('\d+',\s*'(\d+)'\)\"[^>]*>(.*?)</a>", row, re.S)
        if not m:
            continue
        cells = [strip_tags(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
        out.append(job(title=strip_tags(m.group(2)), company=cells[2] if len(cells) > 2 else None,
                       postedDate=cells[3] if len(cells) > 3 else None,
                       deadline=cells[4] if len(cells) > 4 else None,
                       url=f"https://www.gojobs.go.kr/apmView.do?empmnsn={m.group(1)}&menuNo=401", site="나라일터"))
        if len(out) >= limit:
            break
    return out


# ---------------------------------------------------------------- 월드잡플러스 (해외 취업, 공식 공개 API)

def worldjob(keyword: str, f: dict, limit: int) -> list[dict]:
    xml = fetch("https://www.worldjob.or.kr/openapi/openapi.do?dobType=1&pageIndex=1&showItemListCount=100",
                accept="application/xml")
    out = []
    for item in re.findall(r"<ITEM>(.*?)</ITEM>", xml, re.S):
        def tag(name):
            m = re.search(rf"<{name}>(.*?)</{name}>", item, re.S)
            return m and strip_tags(re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", m.group(1), flags=re.S))
        title, country, kind = tag("rctntcSj") or "", tag("dsptcNationScd") or "", tag("dsptcKsco") or ""
        hay = " ".join((title, country, kind, tag("entNm") or ""))
        if keyword and not all(w in hay for w in keyword.split()):
            continue
        link = html.unescape(tag("linkUrl") or "")
        link = re.sub(r"&rtnIp=[^&]*", "", link)   # API가 호출자 IP를 링크에 넣으므로 지운다
        out.append(job(title=title, company=tag("entNm"), location=country, experience=tag("joDemandCareerStleScd"),
                       employmentType=tag("joEmplymStleScd"), deadline=tag("rctntcEndDe"),
                       postedDate=tag("rctntcBgnDe"), url=link or None, site="월드잡"))
        if len(out) >= limit:
            break
    return out


# ---------------------------------------------------------------- 한국리츠협회 회원사 채용 (리츠·부동산 운용·개발)

def kareit(keyword: str, f: dict, limit: int) -> list[dict]:
    page = fetch("https://www.kareit.or.kr/community/page4.php")
    out = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", page, re.S):
        m = re.search(r'href="(/community/page4\.php\?boardid=jobsm&mode=view&idx=(\d+))[^"]*"[^>]*title="([^"]*)"', row)
        if not m:
            continue
        cells = [strip_tags(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
        title = html.unescape(m.group(3)).replace("﻿", "").strip()
        if keyword and not any(w in title for w in keyword.split()):
            continue
        dl = re.search(r"~\s*(\d{1,2}/\d{1,2})", title)
        out.append(job(title=title, company=cells[2] if len(cells) > 2 else None,
                       postedDate=cells[3] if len(cells) > 3 else None, deadline=dl and dl.group(1),
                       url=f"https://www.kareit.or.kr/community/page4.php?boardid=jobsm&mode=view&idx={m.group(2)}",
                       site="리츠협회"))
        if len(out) >= limit:
            break
    return out


# ---------------------------------------------------------------- 원티드 (IT·기획·디자인·마케팅, 스타트업·경력)

def wanted(keyword: str, f: dict, limit: int) -> list[dict]:
    qs = {"country": "kr", "locations": "all", "years": "-1", "limit": str(min(limit, 20)), "offset": "0",
          "job_sort": "job.latest_order", "query": keyword}
    if f.get("experience") and "신입" in f["experience"]:
        qs["years"] = "0"
    data = json.loads(fetch("https://www.wanted.co.kr/api/v4/jobs?" + urllib.parse.urlencode(qs),
                            accept="application/json"))
    out = []
    for d in data.get("data", []):
        addr = d.get("address") or {}
        loc = " ".join(x for x in (addr.get("location"), addr.get("district")) if x)
        exp = None
        if d.get("annual_from") is not None:
            exp = "신입" if d["annual_from"] == 0 and (d.get("annual_to") or 0) <= 1 else \
                _years(d["annual_from"], d.get("annual_to"))
        out.append(job(title=d.get("position", ""), company=(d.get("company") or {}).get("name"), location=loc,
                       experience=exp, deadline=d.get("due_time") or "상시",
                       url=f'https://www.wanted.co.kr/wd/{d["id"]}', site="원티드"))
    return _loc_filter(out, f)[:limit]


# ---------------------------------------------------------------- 점핏 (개발자)

def jumpit(keyword: str, f: dict, limit: int) -> list[dict]:
    qs = {"keyword": keyword, "sort": "rsp_rate", "page": "1"}
    data = json.loads(fetch("https://jumpit-api.saramin.co.kr/api/positions?" + urllib.parse.urlencode(qs),
                            accept="application/json"))
    out = []
    for d in (data.get("result") or {}).get("positions", []):
        lo, hi = d.get("minCareer"), d.get("maxCareer")
        exp = "신입" if d.get("newcomer") and not lo else (_years(lo, hi) if lo is not None else None)
        out.append(job(title=strip_tags(d.get("title", "")), company=d.get("companyName"),
                       location=", ".join(d.get("locations") or []),
                       experience=exp, deadline="상시" if d.get("alwaysOpen") else (d.get("closedAt") or "")[:10],
                       url=f'https://jumpit.saramin.co.kr/position/{d["id"]}', site="점핏"))
        if len(out) >= limit * 2:
            break
    return _loc_filter(out, f)[:limit]


# ---------------------------------------------------------------- 리멤버 (경력직·헤드헌팅)

def remember(keyword: str, f: dict, limit: int) -> list[dict]:
    body = {"search": {"keywords": [keyword]}, "page": 1, "per": min(limit * 2, 30)}
    data = json.loads(fetch("https://career-api.rememberapp.co.kr/job_postings/search", accept="application/json",
                            data=json.dumps(body).encode()))
    out = []
    for d in data.get("data", []):
        a = d.get("normalized_address") or {}
        lo, hi = d.get("min_experience"), d.get("max_experience")
        exp = _years(lo, hi) if lo is not None else None
        sal = None
        if d.get("min_salary") or d.get("max_salary"):
            sal = "~".join(str(x) for x in (d.get("min_salary"), d.get("max_salary")) if x) + "만원"
        out.append(job(title=d.get("title", ""), company=(d.get("organization") or {}).get("name"),
                       location=" ".join(x for x in (a.get("level1"), a.get("level2")) if x), experience=exp, salary=sal,
                       deadline=(d.get("ends_at") or "")[:10] or "상시", postedDate=(d.get("starts_at") or "")[:10],
                       url=f'https://career.rememberapp.co.kr/job/posting/{d["id"]}', site="리멤버"))
    return _loc_filter(out, f)[:limit]


# ---------------------------------------------------------------- 자소설닷컴 (대기업·공기업 공채, 신입·인턴)

def jasoseol(keyword: str, f: dict, limit: int) -> list[dict]:
    now = dt.datetime.now(dt.timezone.utc)
    # 달력은 기간 안에 시작한 공고를 준다 → 한 달 전부터 받아서 마감 안 된 것만 남긴다
    body = {"start_time": (now - dt.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "end_time": (now + dt.timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%S.000Z")}
    data = json.loads(fetch("https://jasoseol.com/employment/calendar_list.json", accept="application/json",
                            data=json.dumps(body).encode()))
    words = keyword.split()
    out, seen = [], set()
    for e in data.get("employment", []):
        hay = json.dumps(e, ensure_ascii=False)
        if e["id"] in seen or (words and not all(w in hay for w in words)):
            continue
        seen.add(e["id"])
        out.append(job(title=e.get("title", ""), company=e.get("name"), deadline=(e.get("end_time") or "")[:10],
                       url=f'https://jasoseol.com/recruit/{e["id"]}', site="자소설닷컴"))
        if len(out) >= limit:
            break
    return out


def _years(lo, hi):
    if hi is None or hi >= 30:
        return f"{lo}년 이상" if lo else "경력무관"
    return f"{lo}~{hi}년"


def _loc_filter(jobs, f):
    want = LOC_RE.findall(f.get("location") or "")
    if not want:
        return jobs
    return [j for j in jobs if not j["location"] or any(w in j["location"] for w in want)]


def _kofia_url(href):
    seq = re.search(r"seq=(\d+)", html.unescape(href))
    return f"https://www.kofia.or.kr/brd/m_96/view.do?seq={seq.group(1)}" if seq else None


SITES = {"saramin": saramin, "jobkorea": jobkorea, "kofia": kofia, "alio": alio, "gojobs": gojobs,
         "worldjob": worldjob, "kareit": kareit, "wanted": wanted, "jumpit": jumpit, "remember": remember,
         "jasoseol": jasoseol}


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
    keywords = [k.strip() for k in ",".join(a.keyword or []).split(",") if k.strip()]
    if not keywords and not (a.job_code or a.industry):
        raise RuntimeError("--keyword 또는 --job-code 가 필요해요.")
    sites = [s.strip() for s in a.sites.split(",") if s.strip()]
    f = {"location": a.location, "experience": a.experience, "salary": a.salary, "empType": a.emp_type,
         "jobCode": a.job_code, "industry": a.industry}
    if not keywords and (a.job_code or a.industry):
        keywords = [""]          # 사람인 코드만으로 검색
    found, errors = [], []
    for kw in keywords:
        for s in sites:
            if not kw and s != "saramin":
                continue             # 코드 검색은 사람인만 지원
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
    label = ", ".join(k for k in keywords if k) or f"사람인 직무코드 {a.job_code or ''} {a.industry or ''}".strip()
    head = f"## 공고 {len(jobs)}건 — {label}" + (f" ({cond})" if cond else "") + \
        (" · 새 공고만" if a.new_only else "")
    print(render(jobs, today, head))
    if errors:
        print("\n(일부 실패: " + " / ".join(errors) + ")")


def cmd_links(a):
    q = urllib.parse.quote(a.keyword)
    print(f"""## 브라우저로 열어 볼 검색 링크 — {a.keyword}
(로그인·보안 확인이 있거나 화면을 브라우저가 그려야 해서 스크립트로는 못 여는 곳이에요. 에이전트 브라우저로 열어 주세요.)
- 캐치 (대기업·중견 신입 공채): https://www.catch.co.kr/NCS/RecruitSearch
- 링커리어 (인턴·신입·대외활동): https://linkareer.com/list/recruit
- 고용24 (중소기업·현장직·중장년): https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do?keyword={q}
- 로켓펀치 (스타트업·인턴): https://www.rocketpunch.com/jobs
- 링크드인 (외국계·해외): https://www.linkedin.com/jobs/search?keywords={q}&location=South%20Korea
- 직군별 전문 사이트는 guides/jobs/ 의 해당 직군 파일을 보세요.""")


def cmd_job(a):
    url = a.url.strip()
    host = urllib.parse.urlparse(url).netloc.lower()
    try:
        check_url(url)
    except RuntimeError as e:
        print(str(e) + " 에이전트 브라우저로 이 공고를 열어서 읽어 주세요.")
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
    elif "wanted.co.kr" in host and re.search(r"/wd/(\d+)", url):
        wid = re.search(r"/wd/(\d+)", url).group(1)
        d = json.loads(fetch(f"https://www.wanted.co.kr/api/v4/jobs/{wid}", accept="application/json")).get("job", {})
        det = d.get("detail") or {}
        text = "\n".join(x for x in (d.get("position"), (d.get("company") or {}).get("name"), det.get("intro"),
                                     "주요업무\n" + (det.get("main_tasks") or ""), "자격요건\n" + (det.get("requirements") or ""),
                                     "우대사항\n" + (det.get("preferred_points") or ""), det.get("benefits")) if x)
    elif "rememberapp.co.kr" in host and re.search(r"/posting/(\d+)", url):
        rid = re.search(r"/posting/(\d+)", url).group(1)
        d = json.loads(fetch(f"https://career-api.rememberapp.co.kr/job_postings/{rid}", accept="application/json"))
        d = d.get("data", d)
        text = "\n".join(str(x) for x in (d.get("title"), (d.get("organization") or {}).get("name"), d.get("introduction"),
                                          "담당업무\n" + (d.get("job_description") or ""), "자격요건\n" + (d.get("qualifications") or ""),
                                          "우대사항\n" + (d.get("preferred_qualifications") or ""), d.get("recruiting_process")) if x)
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
    s.add_argument("--keyword", "-k", action="append", help="키워드 (쉼표로 여러 개)")
    s.add_argument("--sites", default="saramin,jobkorea",
                   help="saramin,jobkorea,wanted,jumpit,remember,jasoseol,kofia,kareit,alio,gojobs,worldjob 중 쉼표로")
    s.add_argument("--job-code", help="사람인 직무 코드 (guides/jobs 의 S숫자에서 S 빼고, 쉼표로 여러 개)")
    s.add_argument("--industry", help="사람인 산업 코드 ind_cd (guides/jobs/index.md)")
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
