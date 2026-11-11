# 2. 맞춤 공고 찾기

## 1) 검색 계획 (생각만, 출력하지 않음)

- 처음 한 번 `guides/jobs/index.md`를 열어 사용자 직무에 맞는 직군 파일 **하나**를 고르고 그 파일을 연다(세부 직무·검색 키워드·사람인 직무 코드·전문 사이트). 고른 직군은 기억해 두고 다음에는 다시 고르지 않는다.
- 키워드 2~3개를 정한다. 사람인은 키워드 대신 `--job-code`로 찾으면 더 정확하다.
- 조건: 지역, 경력(신입/경력/경력무관), 연봉 하한(만원), 고용형태. 말하지 않은 조건은 넣지 않는다.
- 사이트 고르기 (`--sites`, 3~4개. 키워드 수 × 사이트 수 ≤ 12):
  - 기본: `saramin,jobkorea`
  - IT·기획·디자인·마케팅: `+wanted` / 개발자: `+jumpit`
  - 경력직·헤드헌팅: `+remember`
  - 대기업·공기업 신입 공채: `+jasoseol`
  - 금융·증권·운용: `+kofia` / 리츠·부동산 운용·개발: `+kareit,kofia`
  - 공공기관: `alio` / 공무원 임기제·경력경쟁·공무직: `gojobs` / 해외: `worldjob`

## 2) 실행

### 스크립트 모드

```bash
python3 career.py search -k "퍼포먼스 마케터,그로스 마케터" --location 서울 --experience 경력 --max 15
python3 career.py search -k "부동산 PF,자산운용" --sites saramin,jobkorea,kofia --experience 경력
python3 career.py search -k "백엔드" --sites saramin,wanted,jumpit,remember --experience 경력
python3 career.py links -k "퍼포먼스 마케터"     # 브라우저로 볼 사이트 링크 (캐치·링커리어·고용24 등)
```

- 한 번 실행에 요청은 12번까지다(키워드 수 × 사이트 수 ≤ 12).
- 결과 목록은 **그대로** 보여 준다. 다시 요약하거나 표로 바꾸지 않는다.
- 결과가 3건 미만이면 키워드를 넓히거나(예: "퍼포먼스 마케터" → "마케팅") 조건을 하나 빼고 한 번만 다시 한다.
- 오류가 나면 그 사이트만 브라우저 모드로 한다.

### 브라우저 (기본 흐름에 포함)

- **직군 전문 사이트**: 해당 직군 파일(`guides/jobs/NN-*.md`)의 "브라우저" 목록에서 2~3곳을 골라 사용자가 시키지 않아도 연다. 검색 결과 1~2페이지에서 공고를 골라 스크립트 결과와 합친다.
- **스크립트가 실패했을 때**: 같은 사이트를 브라우저로 연다.
  - 사람인: `https://www.saramin.co.kr/zf_user/search/recruit?searchword={키워드}` (서울 `&loc_mcd=101000`, 경기 `102000` / 경력 `&exp_cd=2`, 신입 `1` / 직무 코드 `&cat_kewd={코드}`)
  - 잡코리아: `https://www.jobkorea.co.kr/Search/?stext={키워드}&tabType=recruit`
  - 원티드: `https://www.wanted.co.kr/search?query={키워드}&tab=position`
  - 리멤버: `https://career.rememberapp.co.kr/job/postings` → 검색창에 키워드
  - 자소설닷컴: `https://jasoseol.com/search?keyword={키워드}`
- **스크립트가 지원하지 않는 종합 사이트**: 캐치, 링커리어, 고용24 (`python3 career.py links -k 키워드`로 주소 확인)

출력 형식(스크립트와 같게):

```
### 마감 임박 (7일 안)
1. **회사명** 공고 제목
   - 경력 · 연봉 · 지역 · 고용형태 · 마감 11/15
   - 사이트: 링크
### 그 외
...
```

마감이 지난 공고, '마감'·'모집완료' 표시 공고는 뺀다.

## 3) 마무리 안내 (한 줄씩)

- "마음에 드는 공고 번호 1~2개 골라 주시면 회사 분석이랑 자소서까지 해 드릴게요."
- "조건 바꾸고 싶으면 '판교만', '신입으로', '연봉 4천 이상'처럼 말씀해 주세요."
