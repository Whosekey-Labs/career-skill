<p align="center">
  <img src="assets/readme/hero.svg" alt="kr-career-skill. 저녁 창가 책상 위 노트북에 공고 목록이 떠 있어요. 퇴근하고 지친 저녁에도 이직 준비를 이어 갈 수 있게 돕는 AI 에이전트 스킬." width="100%">
</p>

<p align="center">
  <a href="https://github.com/Whosekey-Labs/kr-career-skill/actions/workflows/tests.yml"><img src="https://github.com/Whosekey-Labs/kr-career-skill/actions/workflows/tests.yml/badge.svg" alt="tests" height="20"></a>
  &nbsp;
  <a href="#준비물"><img src="https://img.shields.io/badge/python-optional%2C_3.9%2B-C7861F?style=flat" alt="python optional, 3.9+" height="20"></a>
  &nbsp;
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-C7861F?style=flat" alt="MIT license" height="20"></a>
</p>

<p align="center">
  AI 에이전트에게 링크 하나만 주면 <b>맞춤 공고 찾기 → 회사 분석 → 자소서·이력서 초안(내 구글 문서) → 매일 새 공고 알림</b>까지 해 주는 AI 에이전트 스킬이에요.<br>
  피클, 뮤즈, ChatGPT, Codex, Claude 등 링크를 읽을 수 있는 에이전트에서 쓰도록 만들었어요.
</p>

<p align="center">
  <a href="#사용법"><b>사용법</b></a>
  &nbsp;&nbsp;&nbsp;
  <a href="#이렇게-진행돼요"><b>진행 순서</b></a>
  &nbsp;&nbsp;&nbsp;
  <a href="#준비물"><b>준비물</b></a>
  &nbsp;&nbsp;&nbsp;
  <a href="#지원-플랫폼"><b>지원 플랫폼</b></a>
  &nbsp;&nbsp;&nbsp;
  <a href="#자주-묻는-것"><b>자주 묻는 것</b></a>
  &nbsp;&nbsp;&nbsp;
  <a href="#주의사항"><b>주의사항</b></a>
</p>

## 만든 이유

이직 준비를 어려워하는 친구가 있었어요. 퇴근하고 나면 체력이 바닥나고, 저녁 먹고 나면 준비할 여력이 없다고 했어요. 그 친구에게 도움이 되길 바라며 만들었어요.

## 사용법

에이전트에 아래 한 줄을 보내세요. 그다음은 에이전트가 묻는 대로 답하면 돼요.

```
https://raw.githubusercontent.com/Whosekey-Labs/kr-career-skill/main/SKILL.md 이 지침 읽고 그대로 해줘. 나 취업(이직) 준비 도와줘.
```

<details>
<summary><b>Claude Code에서 스킬로 두고 쓰기</b></summary>

- 위 한 줄을 그대로 보내도 돼요(링크를 읽어 지침대로 시작해요).
- 스킬로 두려면 작업 폴더에서 아래처럼 받아 두세요. 새로 시작한 Claude Code의 스킬 목록에 `kr-career-skill`로 잡혀요.

```bash
git clone https://github.com/Whosekey-Labs/kr-career-skill .claude/skills/kr-career-skill
```

</details>

## 이렇게 진행돼요

<p align="center">
  <img src="assets/readme/flow.svg" alt="진행 순서: 처음 한 번 연결 점검과 최소 프로필을 정한 뒤, 1 맞춤 공고 찾기, 2 고른 공고 1~2개의 회사 분석과 요건 정리, 3 자소서·이력서 초안을 내 구글 문서로, 4 원하면 매일 새 공고 알림." width="100%">
</p>

## 준비물

| 준비물 | 필요 | 하는 일 |
|---|---|---|
| **에이전트** | 필수 | 링크(웹 페이지)를 읽을 수 있으면 돼요. |
| **파이썬 3.9+** | 있으면 좋아요 | `career.py`로 공고를 찾아요(설치할 것 없음). |
| **브라우저** | 없으면 스크립트만 | 스크립트로 안 되는 사이트를 열어요. |
| **구글 계정 연결** | 선택 | 결과가 내 구글 문서로 생겨요. |

<details>
<summary>준비물 자세히</summary>

- **에이전트**: 링크(웹 페이지)를 읽을 수 있으면 돼요.
- **파이썬 (있으면 좋아요)**: 에이전트가 파이썬을 실행할 수 있으면 `career.py`로 공고를 찾아요(스크립트 모드). 표준 라이브러리만 써서 설치할 것은 없고, 파이썬 3.9 이상이 필요해요(3.10·3.12에서 자동 테스트). Windows에서는 `python3` 대신 `python`으로 실행하세요.
- **브라우저 (없으면 스크립트만)**: 파이썬을 못 쓰거나 스크립트가 실패하면, 그리고 스크립트가 지원하지 않는 사이트(캐치·링커리어·직군 전문 사이트 일부)는 에이전트의 브라우저로 열어요(브라우저 모드).
- **구글 계정 연결 (선택)**: 연결하면 자소서·회사 분석이 내 구글 드라이브에 문서로 생겨요.

</details>

## 결과 예시

`career.py search` 실제 출력이에요(2026-11-13 실행, 일부 생략).

```
$ python career.py search -k "백엔드" --sites saramin,wanted,jumpit --location 서울 --experience 경력 --title-has "백엔드,backend" --max 5
## 공고 5건 — 백엔드 (서울 · 경력)
(확인 시각 2026-11-13 06:49 · 마감·급여는 사이트에 적힌 그대로)
(제목 조건에 맞지 않는 공고 4건 뺌)

### 마감 임박 (7일 안)
1. **(주)앰진** (주)앰진 백엔드 신입·경력 채용공고
   - 신입·경력 · 서울 송파구 · 정규직 · 마감 ~ 11/16(월)
   - 사람인: https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx=55516193

### 그 외
2. **(주)드림어스컴퍼니** 콘텐츠 플랫폼 백엔드 개발(3년 이상)
   - 경력 3~20년 · 서울전체 , 강남구 · 정규직 · 마감 ~ 11/21(토)
   - 사람인: https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx=55354215
…
5. **니우스엔** AI 교육 플랫폼 시니어 백엔드 클라우드 엔지니어
   - 7년 이상 · 서울 강남구 · 마감 2026-12-11
   - 원티드: https://www.wanted.co.kr/wd/397823

사이트별(스크립트, 보여 준 수/찾은 수): 사람인 3/10 · 원티드 2/5 · 점핏 0
```

- 마감·급여·지역은 사이트에 적힌 그대로 옮기고, 마감 지난 공고는 빼요.
- 에이전트는 이 목록을 형식 그대로 보여 주고, 맨 아래에 어느 사이트를 확인했는지 적어요.

## 자주 묻는 것

<details>
<summary><b>준비물이 있나요?</b></summary>

위 [준비물](#준비물)을 보세요. 예전에 쓴 이력서·자소서가 있으면 내 경험과 말투를 살려 써 줘요(없어도 돼요).

</details>

<details>
<summary><b>다음 날에는 어떻게 이어 쓰나요?</b></summary>

그냥 "오늘 새 공고 찾아줘", "이 공고로 자소서 써줘"라고 말하면 돼요. 에이전트가 설정을 잊은 것 같으면 위 링크 문장을 한 번 더 보내세요. 기억 기능이 없는 에이전트는 처음에 받은 내 설정 문서를 같이 붙여 주세요.

</details>

<details>
<summary><b>결과물은 어디에 생기나요?</b></summary>

구글을 연결했으면 내 구글 드라이브에 문서로 생겨요. 아니면 워드·PDF 파일이나 채팅으로 받아요.

</details>

<details>
<summary><b>매일 알림은 어떻게 끄나요?</b></summary>

"알림 꺼줘"라고 말하면 돼요. "알림 시간 바꿔줘"도 돼요.

</details>

<details>
<summary><b>내 정보는 어디에 저장되나요?</b></summary>

쓰는 에이전트의 기억(메모리)에만 요약으로 저장돼요. 이력서·자소서 원문은 저장하지 않고, 이 저장소나 개발자에게 보내지 않아요.

</details>

<details>
<summary><b>대신 지원도 해 주나요?</b></summary>

아니요. 지원서 제출은 본인이 직접 해요.

</details>

## 들어 있는 것

<details>
<summary>파일 구성 보기</summary>

| 파일 | 내용 |
|---|---|
| `SKILL.md` | 에이전트가 처음 읽는 파일 (순서와 규칙) |
| `guides/00-connect.md` | 처음 연결 점검 (구글 문서·캘린더·메일·채용 사이트 로그인) |
| `guides/01-profile.md` | 최소 프로필 + 직군·검색할 사이트 고르기, 나중에 예전 이력서·자소서로 경험·말투 기록 |
| `guides/02-find-jobs.md` | 공고 찾기 (스크립트 / 브라우저) |
| `guides/jobs/index.md` | 직군 목차 (25개 직군 파일: 세부 직무·검색 키워드·사람인 코드·전문 사이트) |
| `guides/03-analyze.md` | 회사 분석 + 공고 요건 정리 |
| `guides/04-cover-letter.md` | 자소서·이력서·지원 메시지 초안 → 내 구글 문서 |
| `guides/05-daily.md` | 매일 새 공고 알림 |
| `guides/fix-phrases.md` | 결과를 고쳐 달라는 말 예시 |
| `guides/feedback.md` | 빠진 사이트·오류를 저장소 이슈로 제보 |
| `career.py` | 파이썬 기본 기능만 쓰는 검색 도우미 (설치 필요 없음) |
| `SITES.md` | 지원 플랫폼 전체 목록 (자동 생성) |

</details>

<!-- sites:start -->
## 지원 플랫폼

- 스크립트로 바로 검색: **104곳** (사람인·잡코리아·원티드·리멤버·자소설닷컴·고용24·잡알리오 등 + 간호·제빵·건설·미용 등 직군 전문 사이트)
- 직군 25개마다 전문 사이트·협회·공공·앱 안내: **중복 없이 213곳** (직군별로 세면 328곳)
- 전체 목록: [SITES.md](SITES.md)

| 직군 | 대표 전문 사이트 (일부) |
|---|---|
| [01 경영·기획·전략](guides/jobs/01-%EA%B2%BD%EC%98%81%EA%B8%B0%ED%9A%8D.md) | 피플앤잡, 링크드인, 비즈니스피플, 랠릿 |
| [02 사무·총무·법무](guides/jobs/02-%EC%82%AC%EB%AC%B4%EB%B2%95%EB%AC%B4.md) | 고용24, 대한변협 취업정보센터, 서울지방변호사회 채용정보, 법무잡 |
| [03 회계·세무·재무](guides/jobs/03-%ED%9A%8C%EA%B3%84%EC%84%B8%EB%AC%B4.md) | 한국공인회계사회 구인, 한국세무사회 구인게시판, 한국관세사회 구인/구직, 고용24 |
| [04 인사·노무·HR](guides/jobs/04-%EC%9D%B8%EC%82%AC.md) | 한국공인노무사회 채용정보, 피플앤잡, 링크드인, 인디스워크 |
| [05 마케팅·광고·홍보·MD](guides/jobs/05-%EB%A7%88%EC%BC%80%ED%8C%85MD.md) | 광고정보센터 채용, 한국PR협회 취업정보, 미디어잡, 랠릿 |
| [06 영업·판매·매장](guides/jobs/06-%EC%98%81%EC%97%85%ED%8C%90%EB%A7%A4.md) | 팜리쿠르트, 패션인잡, 알바몬, 알바천국 |
| [07 고객상담·TM·CS](guides/jobs/07-%EA%B3%A0%EA%B0%9D%EC%83%81%EB%8B%B4.md) | 알바몬, 알바천국, 유베이스 채용, 효성ITX 두드리미 |
| [08 IT개발·데이터·AI](guides/jobs/08-IT%EA%B0%9C%EB%B0%9C.md) | 랠릿, OKKY Jobs 계약직, OKKY Jobs 정규직, 로켓펀치 |
| [09 디자인](guides/jobs/09-%EB%94%94%EC%9E%90%EC%9D%B8.md) | 디자인DB 채용, 디자이너잡, 랠릿, 피플앤잡 |
| [10 구매·물류·무역 (사무·관리)](guides/jobs/10-%EA%B5%AC%EB%A7%A4%EB%AC%BC%EB%A5%98%EB%AC%B4%EC%97%AD.md) | 포워더잡, 링크드인, 고용24, 경기 잡아바 |
| [11 운전·운송·배송·물류 현장](guides/jobs/11-%EC%9A%B4%EC%A0%84%EC%9A%B4%EC%86%A1.md) | 고용24, 알바몬, 알바천국, 당근알바 |
| [12 생산·제조 (현장)](guides/jobs/12-%EC%83%9D%EC%82%B0%EC%A0%9C%EC%A1%B0.md) | 디맨드, 고용24, 알바몬, 알바천국 |
| [13 엔지니어링·설계·품질·연구](guides/jobs/13-%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4%EB%A7%81%EC%97%B0%EA%B5%AC.md) | 하이브레인넷, NST 출연연 통합 채용, 알앤디잡, 알앤디잡 전문연구요원 채용관 |
| [14 건설·건축·부동산(중개·개발)](guides/jobs/14-%EA%B1%B4%EC%84%A4%EB%B6%80%EB%8F%99%EC%82%B0.md) | 건설워커, 콘잡, 산군잡스, 기술잡 |
| [15 설치·정비·수리](guides/jobs/15-%EC%84%A4%EC%B9%98%EC%A0%95%EB%B9%84.md) | 잡카, 카파인드잡, 모터스잡, 설치기사잡 |
| [16 의료·보건](guides/jobs/16-%EC%9D%98%EB%A3%8C%EB%B3%B4%EA%B1%B4.md) | 널스잡, 너스케입, 메디잡, 널스빌리지 |
| [17 돌봄·사회복지·공공](guides/jobs/17-%EB%8F%8C%EB%B4%84%EB%B3%B5%EC%A7%80%EA%B3%B5%EA%B3%B5.md) | 복지넷 구인정보, 한국사회복지관협회 구인/구직, 고용24, 요양나라 |
| [18 교육](guides/jobs/18-%EA%B5%90%EC%9C%A1.md) | 훈장마을, 알바몬, 당근알바, 강사닷컴 |
| [19 음식·조리·식음료](guides/jobs/19-%EC%9D%8C%EC%8B%9D%EC%A1%B0%EB%A6%AC.md) | 푸드앤잡, 고용24, 요리사잡, 일식조리사닷컴 |
| [20 미용·뷰티·예식·반려동물 (생활서비스)](guides/jobs/20-%EB%AF%B8%EC%9A%A9%EC%83%9D%ED%99%9C%EC%84%9C%EB%B9%84%EC%8A%A4.md) | 헤어99, 뷰티인잡, 헤어인잡, 헤어커플 |
| [21 여행·숙박·항공·레저](guides/jobs/21-%EC%97%AC%ED%96%89%EC%88%99%EB%B0%95%ED%95%AD%EA%B3%B5.md) | 관광인, 국외여행인솔자 인력관리시스템, 여행사잡, 호텔인네트워크 |
| [22 경비·청소·시설관리](guides/jobs/22-%EA%B2%BD%EB%B9%84%EC%B2%AD%EC%86%8C%EC%8B%9C%EC%84%A4.md) | 고용24, 씨큐인, 올워크 경비·미화 일자리 (앱), 대한주택관리사협회 소장구인 |
| [23 미디어·문화·예술·스포츠](guides/jobs/23-%EB%AF%B8%EB%94%94%EC%96%B4%EB%AC%B8%ED%99%94%EC%8A%A4%ED%8F%AC%EC%B8%A0.md) | 미디어잡, 다음 카페 아랑 채용정보방, 방송작가협회 시사교양연구회, 필름메이커스 |
| [24 금융·보험 (부동산 금융·운용 포함)](guides/jobs/24-%EA%B8%88%EC%9C%B5%EB%B3%B4%ED%97%98.md) | 금융인력네트워크센터(한국금융연구원) 구인정보, 한국벤처캐피탈협회 채용공고, 여신금융협회 회원사 채용, 새마을금고 채용 |
| [25 농림어업](guides/jobs/25-%EB%86%8D%EB%A6%BC%EC%96%B4%EC%97%85.md) | 도농인력중개플랫폼, 알바몬 농업 일자리, 일가자인력 (앱), 고용24 |
<!-- sites:end -->

## 직접 실행 (셸이 있는 환경)

```bash
python3 career.py search -k "퍼포먼스 마케터" --location 서울 --experience 경력
python3 career.py search -k "부동산 PF,자산운용" --sites saramin,jobkorea,kofia
python3 career.py links -k "간호사"
python3 career.py job --url "공고 링크"
python3 career.py company -n "회사명" --place "회사명 지역"   # 사업자·종업원·영업 상태·매출·위치
python3 career.py wayback 회사도메인.com                   # 홈페이지 과거 버전
python3 career.py count -i 자소서.md      # 문항별 글자 수 (공백 포함·제외)
python3 -m unittest discover tests      # 테스트 (실제 사이트에 요청하지 않아요)
```

<details>
<summary><b>스크립트가 사이트를 여는 방식</b></summary>

- 허용 목록(`ALLOWED_HOSTS`)에 있는 채용 사이트 주소만 열어요. 회사 조회(`company`·`wayback`)용 사이트는 따로 두고, 공고 검색·본문 읽기에서는 열지 않아요.
- 같은 사이트는 1초 + 0~0.8초 랜덤 간격을 두고 열어요.
- 한 번 실행에 요청은 16번까지예요(다시 시도 포함). 그래서 `키워드 수 × 사이트 수`를 16 아래로 잡아요(다시 시도가 생기면 더 일찍 멈출 수 있어요).
- robots.txt는 읽지 않아요. 허용 목록·간격·요청 수 제한만 둬요.
- 연결 끊김·시간 초과·5xx 오류는 한 번만 다시 시도해요.
- 일반 브라우저 User-Agent 하나를 고정해서 써요(바꿔 가며 쓰지 않아요).
- 로그인이나 보안 확인이 필요한 사이트는 스크립트로 열지 않고 에이전트 브라우저에 맡겨요.

</details>

## 주의사항

> [!IMPORTANT]
> - **본인 구직용으로만 쓰세요.** 공고 내용의 권리는 각 채용 사이트와 회사에 있어요. 찾은 공고를 모아서 다른 곳에 다시 올리거나 팔지 마세요.
> - **지원은 본인이 직접 해요.** 이 스킬은 대신 지원하지 않아요.

- **지원 전에 공고 원문을 한 번 열어 보세요.** 마감일·급여·조건은 사이트에 적힌 그대로 가져오고, 자소서 쓰기 전에 마감 여부를 다시 확인해요. 다만 이미지로 된 공고에서 읽은 값에는 "(이미지에서 읽음)"이 붙는데, 이건 꼭 원문과 대조하세요. 공고는 회사 사정으로 바뀔 수 있어요.
- **자소서는 초안이에요.** 숫자와 경험은 본인이 확인하고 고쳐서 내세요. AI로 쓴 자소서를 제한하는 회사도 있으니 공고 안내를 확인하세요.
- **민감한 정보는 채팅에 쓰지 마세요.** 주민등록번호, 계좌·카드 번호, 비밀번호는 입력하지 마세요. 채용 사이트 로그인은 에이전트 앱의 로그인·금고 기능으로만 연결하세요.
- **취업 사기를 조심하세요.** 선입금·교육비·장비값 요구, 통장·체크카드 요구, 하는 일이 불분명한 고수익 재택, 인수금을 내야 하는 지입은 의심하세요. 에이전트가 이런 공고를 보면 알려 드려요.
- **천천히 쓰세요.** 스크립트는 같은 사이트를 1~1.8초 간격으로 천천히 열어요. 그래도 짧은 시간에 너무 많이 검색하면 사이트가 접속을 막을 수 있고, 에이전트의 하루 무료 사용량도 빨리 줄어요.
- **제보할 때 개인정보를 적지 마세요.** 이슈는 누구나 보는 공개 글이에요.

## 참고한 공개 자료

회사 분석·자소서 지침은 아래 공개 자료의 아이디어를 참고해 우리 말로 새로 썼어요. 문장을 그대로 옮기지 않았어요.

- [thesun4sky/jobstack](https://github.com/thesun4sky/jobstack) (MIT) — 치환 테스트, 수치는 확보한 것만, 예상 면접 질문
- [KangRyun/jasoseo-plugin](https://github.com/KangRyun/jasoseo-plugin) (MIT) — 회사 사실과 내 경험을 짝짓는 표, 문항 구성·글자 수 규칙, 문체 규칙
- [djfksjd/cover-letter-team](https://github.com/djfksjd/cover-letter-team) (MIT) — 경험 검증 질문, 지원동기 따로 묻기, 공고의 AI 사용 규정 확인
- [useful-skills/job-application-skills](https://github.com/useful-skills/job-application-skills) (MIT) — 출처 등급, 같은 이름 법인 확인, 회사 규모별 확인 항목
- [wing0828/ai-job-search-kr](https://github.com/wing0828/ai-job-search-kr) (MIT) — 문항별 경험 배분, 글자 수 목표

## 라이선스

[MIT](LICENSE) — 누구나 자유롭게 쓰고, 고치고, 나눌 수 있어요. 저작권 표시만 남겨 주세요. 검색 결과나 사이트 동작은 보증하지 않아요(사이트가 바뀌면 검색이 안 될 수 있어요).

## 제보·문의

- 빠진 사이트, 검색 오류, 개선 의견은 [이슈](https://github.com/Whosekey-Labs/kr-career-skill/issues/new/choose)로 남겨 주세요. 에이전트에게 "이거 제보해줘"라고 하면 대신 정리해서 올려 줘요(올리기 전에 내용을 보여 줘요).
- 이슈는 공개 글이에요. 이름·연락처·이력서 같은 개인정보는 적지 마세요.
- 깃헙 계정이 없으면 오픈채팅방으로 알려 주세요: https://open.kakao.com/o/g3vAeBWi
