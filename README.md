# 취업·이직 AI 에이전트 스킬 (career-skill)

AI 에이전트에게 링크 하나만 주면 **맞춤 공고 찾기 → 회사 분석 → 자소서 초안(내 구글 문서) → 매일 새 공고 알림**까지 해 주는 AI 에이전트 스킬이에요. 피클, 뮤즈, ChatGPT, Codex, Claude 등 어떤 에이전트든 쓸 수 있어요.

## 사용법 (피클 기준)

피클에 아래 한 줄을 보내세요.

```
https://raw.githubusercontent.com/Whosekey-Labs/career-skill/main/SKILL.md 이 지침 읽고 그대로 해줘. 나 취업(이직) 준비 도와줘.
```

그다음은 피클이 묻는 대로 답하면 돼요.

## 들어 있는 것

| 파일 | 내용 |
|---|---|
| `SKILL.md` | 에이전트가 처음 읽는 파일 (순서와 규칙) |
| `guides/00-connect.md` | 처음 연결 점검 (구글 문서·캘린더·메일·채용 사이트 로그인) |
| `guides/01-profile.md` | 경력·강점 정리 (연결된 사이트 이력서 불러오기) |
| `guides/02-find-jobs.md` | 공고 찾기 (스크립트 / 브라우저) |
| `guides/jobs/index.md` | 직군 목차 (25개 직군 파일: 세부 직무·검색 키워드·사람인 코드·전문 사이트) |
| `guides/03-analyze.md` | 회사 분석 + 공고 요건 정리 |
| `guides/04-cover-letter.md` | 자소서 초안 → 내 구글 문서 (구글 계정 연결 안내) |
| `guides/05-daily.md` | 매일 새 공고 알림 |
| `guides/fix-phrases.md` | 결과를 고쳐 달라는 말 예시 |
| `guides/feedback.md` | 빠진 사이트·오류를 저장소 이슈로 제보 |
| `career.py` | 파이썬 기본 기능만 쓰는 검색 도우미 (설치 필요 없음) |

<!-- sites:start -->
## 지원 플랫폼

스크립트 검색 11곳 + 직군별 전문 사이트·협회·공공·앱 236곳(직군 간 중복 포함).


### 스크립트로 바로 검색 (`career.py search --sites`)

| `--sites` 값 | 사이트 |
|---|---|
| `saramin` | 사람인 — 전 직군, 직무 코드 검색 |
| `jobkorea` | 잡코리아 — 전 직군 |
| `kofia` | 금융투자협회 — 증권·자산운용 |
| `alio` | 잡알리오 — 공공기관 |
| `gojobs` | 나라일터 — 공무원 임기제·경력경쟁·공무직 |
| `worldjob` | 월드잡플러스 — 해외 취업 |
| `kareit` | 한국리츠협회 — 리츠·부동산 운용·개발 |
| `wanted` | 원티드 — IT·기획·디자인·마케팅, 스타트업·경력 |
| `jumpit` | 점핏 — 개발자 |
| `remember` | 리멤버 — 경력직·헤드헌팅 |
| `jasoseol` | 자소설닷컴 — 대기업·공기업 신입 공채 |

### 직군별 전문 사이트 (에이전트 브라우저로 열거나 링크로 확인)

직군 파일마다 세부 직무·사람인 직무 코드·검색 주소가 더 자세히 있어요. 빠진 사이트는 오픈채팅방으로 알려 주세요.

#### 01 경영·기획·전략

- 스크립트: `alio, jasoseol, jobkorea, remember, saramin, wanted`
- [피플앤잡](https://www.peoplenjob.com/jobs?period=all&field=all) — 외국계 전략·사업개발, 서치펌 공고가 많다
- [링크드인](https://www.linkedin.com/jobs/search?location=South+Korea) — 외국계·Corporate Strategy·임원급
- [랠릿](https://www.rallit.com/) — IT 서비스 기획·PM·PO
- [로켓펀치](https://www.rocketpunch.com/jobs)
- [링커리어](https://linkareer.com/list/recruit) — 대기업·스타트업 전략기획·사업기획 인턴·신입
- [인디스워크](https://inthiswork.com/) — 기획·마케팅·조직문화 주니어 공고를 매일 모아 올린다
- [게임잡](https://www.gamejob.co.kr/Recruit/joblist?menucode=searchtot&searchtype=all) — 게임기획·BM·레벨디자인·사업PM
- [이벤트넷](https://www.eventnet.co.kr/job/recruit/index.php?search=title) — 행사대행사·MICE·BTL 기획자, 신입~팀장
- 자세히: [`guides/jobs/01-경영기획.md`](guides/jobs/01-%EA%B2%BD%EC%98%81%EA%B8%B0%ED%9A%8D.md)

#### 02 사무·총무·법무

- 스크립트: `alio, gojobs, jobkorea, remember, saramin`
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 중소기업 사무직·법률사무소 직원
- [대한변협 취업정보센터](https://www.klaw.or.kr/career/recruit1) — 로펌·사내변호사, 신입~경력
- [서울지방변호사회 채용정보](https://www.seoulbar.or.kr/site/employment/EmploymentAreaRecruit.do) — 변호사·사무직원 채용
- [지방법무사회 구인](https://kjaar.kabl.kr/mod/page/view.do?MID=kjaa_page_job)
- [대한변리사회 구인정보](https://www.kpaa.or.kr/kpaa/info/readJobOfferList.do?srch_job_type=4&th0005MngNo=16) — 변리사
- [피플앤잡](https://www.peoplenjob.com/jobs?field=all) — 외국계 비서·EA·Office Manager, 경력 위주
- [링크드인](https://www.linkedin.com/jobs/search?location=South+Korea) — 외국계 EA·Legal Counsel
- [하이브레인넷 직원 채용](https://www.hibrain.net/recruitment/categories/JOB/categories/EMP/recruits?sortType=SORTDTM) — 대학·연구기관·공공기관 직원
- [경기도교육청 구인구직](https://www.goe.go.kr/recruit/ad/func/pb/hnfpPbancList.do?mi=10502) — 학교 교무행정실무사·계약직
- [국가공무원 채용시스템](https://gongmuwon.gosi.kr/crrut/indexMain.do) — 국가직 경력경쟁·행정
- 자세히: [`guides/jobs/02-사무법무.md`](guides/jobs/02-%EC%82%AC%EB%AC%B4%EB%B2%95%EB%AC%B4.md)

#### 03 회계·세무·재무

- 스크립트: `alio, jobkorea, kofia, remember, saramin`
- [한국공인회계사회 구인](https://www.kicpa.or.kr/home/jobOffrSrchGnrl/list.face?listCnt=20) — 회계법인 인턴·경력 직원, 기업 회계팀
- [한국세무사회 구인게시판](https://www.kacta.or.kr/license_view/jobSearch/jobsearch_list_n.asp?rcode1=0101&rcode2=1701&rcode3={1%7C3%7C4}) — 1 세무사사무소 직원, 3 세무법인 직원, 4 수습·근무세무사
- [한국관세사회 구인/구직](https://krcaa.or.kr/_Document/Notify/N20201L.aspx?MenuCode=N20201) — 관세사·수습관세사·통관 사무원
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 경리·회계사무원·세무사무소 직원, 지역 소규모 사업장
- [피플앤잡](https://www.peoplenjob.com/jobs?period=all&field=all) — 외국계 Finance·Accountant·Controller, 서치펌 CFO·자금 공고
- [링크드인](https://www.linkedin.com/jobs/search?location=South+Korea) — 외국계 FP&A·Controller·Tax
- 자세히: [`guides/jobs/03-회계세무.md`](guides/jobs/03-%ED%9A%8C%EA%B3%84%EC%84%B8%EB%AC%B4.md)

#### 04 인사·노무·HR

- 스크립트: `alio, jasoseol, jobkorea, remember, saramin, wanted`
- [한국공인노무사회 채용정보](https://www.kcplaa.or.kr/worker/list?scd={3%7C2%7C1}) — 3 공인노무사 구인
- [피플앤잡](https://www.peoplenjob.com/jobs?period=all&field=all) — 외국계 HR Manager·C&B·Payroll·HRBP
- [링크드인](https://www.linkedin.com/jobs/search?location=South+Korea) — 외국계 HRBP·Talent Acquisition
- [인디스워크](https://inthiswork.com/hr) — 조직문화·채용 담당 인턴·신입·주니어 공고를 매일 모은다
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 직업상담사
- 자세히: [`guides/jobs/04-인사.md`](guides/jobs/04-%EC%9D%B8%EC%82%AC.md)

#### 05 마케팅·광고·홍보·MD

- 스크립트: `jasoseol, jobkorea, remember, saramin, wanted`
- [광고정보센터 채용](https://www.adic.or.kr/job/employee/list.do?speciality=2) — 대행사 AE·카피·매체·PR, 대리~부장 경력
- [한국PR협회 취업정보](https://www.koreapr.org/recruit-contest) — PR 대행사 신입~경력
- [미디어잡](https://www.mediajob.co.kr/search/search.htm?cmd=recruit) — 광고대행사·홍보·콘텐츠·SNS 운영
- [랠릿](https://www.rallit.com) — IT 서비스 회사 콘텐츠·그로스·퍼포먼스 마케터
- [피플앤잡](https://www.peoplenjob.com/jobs?field=all) — 외국계 브랜드·PMM·퍼포먼스, 헤드헌팅 경력직
- [로켓펀치](https://www.rocketpunch.com/jobs) — 스타트업 마케터·인턴
- [게임잡 직무별](https://www.gamejob.co.kr/Recruit/joblist?menucode=duty&duty=33) — 게임사 마케팅
- [패션인잡](https://www.fashioninjob.co.kr/all_search.php) — 패션·뷰티 MD·VMD·브랜드 마케팅
- [패션워크](https://www.fashionwork.co.kr/fjob/guin.asp?fset=job_110&jobCode=400100) — 패션 상품기획 MD, VMD는 `jobCode=700100`, 전체는 `fset=job_105`
- [아이보스 구인게시판](https://www.i-boss.co.kr/ab-2795) — 퍼포먼스·대행사 실무
- 자세히: [`guides/jobs/05-마케팅MD.md`](guides/jobs/05-%EB%A7%88%EC%BC%80%ED%8C%85MD.md)

#### 06 영업·판매·매장

- 스크립트: `jasoseol, jobkorea, remember, saramin, wanted, worldjob`
- [팜리쿠르트](https://recruit.dailypharm.com/Main/search.php?CateNum=3) — 제약영업
- [패션인잡](https://www.fashioninjob.co.kr/all_search.php) — 백화점·브랜드 매장 판매, 화장품 판매, 샵마스터
- [알바몬](https://www.albamon.com/total-search) — 매장 판매·캐셔·판촉 단기·시간제가 가장 많다
- [알바천국](https://www.alba.co.kr/search/Search) — 판매·판촉·주유원 알바, 브랜드 매장 상시모집
- [당근알바](https://jobs.daangn.com/s) — 동네 매장 판매·캐셔
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 지역 중소기업 영업·판매직, 중장년 판매직
- [링크드인](https://www.linkedin.com/jobs/search?location=South+Korea) — 외국계 영업·해외영업 경력
- 자세히: [`guides/jobs/06-영업판매.md`](guides/jobs/06-%EC%98%81%EC%97%85%ED%8C%90%EB%A7%A4.md)

#### 07 고객상담·TM·CS

- 스크립트: `alio, jobkorea, remember, saramin, wanted`
- [알바몬](https://www.albamon.com/total-search) — 콜센터 공고가 가장 많다
- [알바천국](https://www.alba.co.kr/search/Search) — 지역 콜센터·TM 단기
- [유베이스 채용](https://ubase.co.kr/Recruit/Notices) — 신한카드·코웨이·동양생명 등 대표번호 인바운드, 센터·역 위치 표시
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 지역 콜센터·중장년·장애인 채용
- [서울 일자리포털](https://job.seoul.go.kr/hmpg/rmim/rcmg/rcmgListPgng.do?region=11000&miv_pageNo=1&miv_pageSize=10) — 서울 지역
- [경기 잡아바](https://job.gg.go.kr/empmn/enterpriseEmployListNew.do) — 경기 지역
- [120다산콜재단 채용공고](https://www.120dasan.or.kr/dsnc/bbs/B0000009/list.do?menuNo=200028) — 서울시 공공 상담직
- [피플앤잡](https://www.peoplenjob.com/jobs?field=all) — 외국계·명품 브랜드 CS, 고객경험
- [링크드인](https://www.linkedin.com/jobs/search?location=South+Korea) — 외국계 Customer Support·영어·일어 상담
- 자세히: [`guides/jobs/07-고객상담.md`](guides/jobs/07-%EA%B3%A0%EA%B0%9D%EC%83%81%EB%8B%B4.md)

#### 08 IT개발·데이터·AI

- 스크립트: `jasoseol, jobkorea, jumpit, remember, saramin, wanted, worldjob`
- [랠릿](https://www.rallit.com) — 스타트업 백엔드·앱·임베디드, 주니어~미들
- [OKKY Jobs 계약직](https://jobs.okky.kr/contract) — SI·프리랜서 상주 개발, 단가·기간 표시, 중급~고급
- [OKKY Jobs 정규직](https://jobs.okky.kr/fulltime) — 정규직은 공고 수가 적음
- [로켓펀치](https://www.rocketpunch.com/jobs) — 스타트업·인턴
- [서핏](https://www.surfit.io/jobs/develop/back-end)
- [게임잡 직무별](https://www.gamejob.co.kr/Recruit/joblist?menucode=duty&duty=16) — 게임사 개발
- [링크드인](https://www.linkedin.com/jobs/search?location=South+Korea) — 외국계·대기업 영문 공고, 경력
- [피플앤잡](https://www.peoplenjob.com/jobs?field=all) — 외국계 IT·헤드헌팅 경력직
- [위시켓](https://www.wishket.com/project/) — 외주·상주 프로젝트, 월 단가·기간·기술 표시
- 자세히: [`guides/jobs/08-IT개발.md`](guides/jobs/08-IT%EA%B0%9C%EB%B0%9C.md)

#### 09 디자인

- 스크립트: `jobkorea, remember, saramin, wanted`
- [디자인DB 채용](https://www.designdb.com/?menuno=1436&key=bbstitle) — 시각·제품·영상·환경·패션 분야와 경력 구간 표시
- [디자이너잡](https://www.designerjob.co.kr/search/total-search) — UI/UX·시각·BX·VMD·전시·패션·인테리어까지 넓음
- [랠릿](https://www.rallit.com) — 스타트업 프로덕트·UI/UX·콘텐츠 디자이너
- [피플앤잡](https://www.peoplenjob.com/jobs?field=all&q=%EB%94%94%EC%9E%90%EC%9D%B4%EB%84%88) — 외국계·뷰티 브랜드 패키지·웹·공간 디자인 경력
- [서핏](https://www.surfit.io/jobs)
- [게임잡 직무별](https://www.gamejob.co.kr/Recruit/joblist?menucode=duty&duty=5) — 5 원화, 4 게임 UI, 6 모델링, 7 애니메이션, 8 이펙트, 13 플랫폼 디자인, 14 BX
- [CG랜드 구인](https://job.cgland.com/index.html?mode=recruit) — VFX·3D·애니메이터
- [미디어잡](https://www.mediajob.co.kr/search/search.htm?cmd=recruit) — 영상 편집·모션
- [패션인잡](https://www.fashioninjob.co.kr/all_search.php) — 패션·잡화·텍스타일·VMD
- [VMSPACE 잡](https://www.vmspace.com/job/job.html) — 건축 설계 위주, 인테리어·공간·조경 일부
- [노트폴리오 채용](https://notefolio.net/service/job/list) — 은 JS 전용이라 최근 공고를 확인하지 못했다
- 자세히: [`guides/jobs/09-디자인.md`](guides/jobs/09-%EB%94%94%EC%9E%90%EC%9D%B8.md)

#### 10 구매·물류·무역 (사무·관리)

- 스크립트: `jobkorea, remember, saramin, worldjob`
- [포워더잡](https://www.forwarder.kr/job/jobs.php) — 포워딩 오퍼레이터·해운/항공 수출입·물류 영업
- [링크드인](https://www.linkedin.com/jobs/search?location=South+Korea) — 외국계 SCM·구매·물류·무역 경력
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 중소 무역사무·물류사무·보세창고
- [경기 잡아바](https://job.gg.go.kr/empmn/enterpriseEmployListNew.do) — 경기 물류단지 사무·관리
- 자세히: [`guides/jobs/10-구매물류무역.md`](guides/jobs/10-%EA%B5%AC%EB%A7%A4%EB%AC%BC%EB%A5%98%EB%AC%B4%EC%97%AD.md)

#### 11 운전·운송·배송·물류 현장

- 스크립트: `alio, jobkorea, saramin`
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 버스·택시·화물·지게차·물류센터 현장직이 가장 많음
- [알바몬](https://www.albamon.com/total-search) — 물류센터 상하차·피킹, 지게차, 배송 기사
- [알바천국](https://www.alba.co.kr/search/Search) — 물류센터·지게차·배송 알바, 대형 물류허브 야간조
- [당근알바](https://jobs.daangn.com/s) — 동네 택배·배송 기사, 짐 옮기기
- [경기 잡아바](https://job.gg.go.kr/empmn/enterpriseEmployListNew.do) — 경기 물류단지 지게차·입출고
- [부산일자리정보망](https://www.busanjob.net) — 부산 운전·물류
- [노인일자리 여기](https://www.seniorro.or.kr/noin/searchWork.do) — 65세 이상
- [쿠팡CLS](https://job.coupangcorp.com/cls_fo) — curl은 403, 브라우저로
- [쿠팡플렉스](https://flex.coupang.com) — 자차 택배, 가입 후 일감 선택
- 배민커넥트 (앱) — 자차·도보 배달, 가입 후 일감 선택
- 전국24시콜화물·화물맨·원콜 (앱) — 화물정보망, 개인 차주·지입 오더
- [서울택시조합](https://www.stj.or.kr) — 택시취업안내 메뉴에 자치구별 택시회사 목록이 있다
- 자세히: [`guides/jobs/11-운전운송.md`](guides/jobs/11-%EC%9A%B4%EC%A0%84%EC%9A%B4%EC%86%A1.md)

#### 12 생산·제조 (현장)

- 스크립트: `jasoseol, jobkorea, saramin`
- [디맨드](https://www.dmand.co.kr) — 반도체·2차전지·석유화학·제약 생산·설비·품질, 교대형태 필터
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 중소 제조 현장직, 용접·CNC·사출 기능직
- [알바몬](https://www.albamon.com/total-search) — 단기·파견 생산직, 2교대·주야 공고, 기숙사 제공 공고
- [알바천국](https://www.alba.co.kr/search/Search) — 생산·포장·검품 알바
- [당근알바](https://jobs.daangn.com/s) — 동네 식품공장·포장·생산보조 파트타임
- [경기 잡아바](https://job.gg.go.kr/empmn/enterpriseEmployListNew.do) — 경기 산업단지
- [부산일자리정보망](https://www.busanjob.net) — 부산·녹산 산단 생산직
- 자세히: [`guides/jobs/12-생산제조.md`](guides/jobs/12-%EC%83%9D%EC%82%B0%EC%A0%9C%EC%A1%B0.md)

#### 13 엔지니어링·설계·품질·연구

- 스크립트: `alio, jasoseol, jobkorea, remember, saramin, worldjob`
- [하이브레인넷](https://www.hibrain.net/recruitment/recruits?listType=D3NEW) — 교수·연구원·포닥, 하루 수백 건
- [NST 출연연 통합 채용](https://www.nst.re.kr/www/selectBbsNttList.do?bbsNo=19&key=61&searchCnd=SJ) — 출연연 연구직·기술직
- [알앤디잡](https://www.rndjob.or.kr/info/entire_notice.asp) — 중소·중견 기업연구소 연구원·설계, 고용24 공고 연동
- [알앤디잡 전문연구요원 채용관](https://www.rndjob.or.kr/info/sp_rsch.asp) — 병역특례 석·박사 연구원
- [BioIN](https://www.bioin.or.kr/empmnInfo.do?bid=employ&cmd=list&s_key=all) — 바이오 기업·공공 연구
- [BRIC BioJob](https://www.ibric.org/bric/biojob/recruit.do?mode=list) — 바이오 연구원·포닥
- [바이오스펙테이터 채용](https://www.biospectator.com/section/job_list) — 바이오텍 경력
- [너스케입](https://recruit.nurscape.net/Home/Search?TOTAL_KEYWORD=CRA) — 임상
- [디맨드](https://www.dmand.co.kr/jd) — 생산·기능직 플랫폼, 반도체·2차전지 설비·공정 현장직
- [한국기술사회 구인](https://www.kpea.or.kr/kpea/member/OfferList.do?leftMenuCode=member&menu=07&sub=01) — 전기·소방·건축 등 기술사 구인
- [대한산업안전협회 구인](https://www.safety.or.kr/safety/bbsJob/list.do?menuNo=200116&searchCondition=nttSj) — 안전관리자
- 자세히: [`guides/jobs/13-엔지니어링연구.md`](guides/jobs/13-%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4%EB%A7%81%EC%97%B0%EA%B5%AC.md)

#### 14 건설·건축·부동산(중개·개발)

- 스크립트: `alio, jobkorea, kareit, remember, saramin`
- [건설워커](https://www.worker.co.kr/job/list.asp?searching=yes&jobid=all&key=jsubject) — 종합·전문건설 시공·공무·안전·CM 경력
- [콘잡](https://www.conjob.co.kr/searchModule_jnew.php?find=find) — 중소 건설 토목·건축
- [산군잡스](https://sankunjobs.com/jobs) — 건설 전 직무, 회사 시공능력 정보
- [건설워크넷](https://cworknet.kocea.or.kr/worknet/work/pgm/i-1183/work/recruit/recruitInfoList.do) — 감리·건설사업관리
- 가다 (앱) — 날짜·지역·직종 골라 지원, 일당 당일 지급
- [대한건축사협회 구인](https://www.kira.or.kr/jsp/main/03/02_01.jsp?jobId=BBS_00_GUIN&mode=main) — 건축사사무소 설계·감리
- [대한기계설비건설협회 구인정보](https://www.kmcca.or.kr/alarm/recruiting/guinList.do) — 기계설비·배관·공조 시공, 설비 유지관리자
- [소방산업 고용지원센터](http://fjob.ekffa.or.kr/fe/joboffer/NR_list.do) — 소방 감리원
- [한국전기기술인협회 구인정보](https://www.keea.or.kr/head/jobinfo/getWJO02R01List.do) — 전기안전관리자·전기감리
- [대한산업안전협회 구인](https://www.safety.or.kr/safety/bbsJob/list.do?menuNo=200116&searchCondition=nttSj) — 안전관리자
- [한국공인중개사협회 구인](https://www.kar.or.kr/pcommunity/jobofferlist.asp?pg=1) — 소속공인중개사·중개보조원, 전국
- [공실클럽 구인정보](https://www.gongsil.com/bbs/recruit/) — 서울 강남권 중개사무소 소속공인중개사·보조원, 합동사무실
- [분양라인](https://www.bunyangline.com/recruit/regional/0) — 모델하우스 분양상담사·팀장·본부장, 지역별
- [한국감정평가사협회 채용정보](https://www.kapanet.or.kr/notice/recruit) — 감정평가법인 감정평가사·사무직
- 자세히: [`guides/jobs/14-건설부동산.md`](guides/jobs/14-%EA%B1%B4%EC%84%A4%EB%B6%80%EB%8F%99%EC%82%B0.md)

#### 15 설치·정비·수리

- 스크립트: `alio, jobkorea, saramin`
- [잡카](https://www.jobcar.co.kr/jobs/list.asp?transfer=job_101) — 자동차정비 전문
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 지역 정비·설치 현장직, 승강기·보일러
- [알바몬](https://www.albamon.com/total-search) — 에어컨·가전 설치 기사, 설치 보조, 방문점검
- [알바천국](https://www.alba.co.kr/search/Search) — 에어컨 설치·인터넷 설치 보조
- [당근알바](https://jobs.daangn.com/s) — 동네 수리·설치 일감
- [경기 잡아바](https://job.gg.go.kr/empmn/enterpriseEmployListNew.do) — 경기 설비 보수·정비
- 자세히: [`guides/jobs/15-설치정비.md`](guides/jobs/15-%EC%84%A4%EC%B9%98%EC%A0%95%EB%B9%84.md)

#### 16 의료·보건

- 스크립트: `alio, gojobs, jobkorea, k, saramin`
- [널스잡](https://www.nursejob.co.kr/recruit/search.php) — 간호사·간호조무사, 의원~대학병원
- [너스케입](https://recruit.nurscape.net/Home/Search) — 간호사 전 직무
- [메디잡](https://www.medijob.cc/rec/rem/rec_rem_105) — 의원급 간호조무사·물리치료사·원무·코디
- [메디컬잡](https://www.medicaljob.co.kr/job/list.asp?jobid=all) — 의사 초빙
- [덴탈잡](https://www.dentaljob.co.kr/paeaa010) — 치과위생사·간호조무사·데스크·상담실장·기공사, 알바 많음
- [대한치과위생사협회 채용정보](https://www.kdha.or.kr/job/Recruit.aspx) — 치과위생사, 지역·연차·급여 필터
- [대한물리치료사협회 KPTA취업센터](https://www.kpta.co.kr/jobCenter/jobOfferList) — 물리·도수치료사, 실장·팀장, 보건소 계약직
- [대한방사선사협회 구인게시판](https://krta.or.kr/bbs/board.php?bo_table=guin&sfl=wr_subject) — 방사선사
- [대한임상병리사협회 구인정보](https://www.kamt.or.kr/job/opening/list.do?stNo=4&muNo=1890&muGpNo=1889) — 임상병리사
- [팜리쿠르트](https://recruit.dailypharm.com/Main/search.php?CateNum=1) — 약국 근무약사·파트·단기
- [데일리벳 리크루트](https://www.dailyvet.co.kr/recruit) — 수의사
- [대한수의사회 스탭 구인](https://www.kvma.or.kr/kvma_list?tbl=15) — 동물병원 테크니션·스탭
- [알바몬](https://www.albamon.com/total-search?keyword=%EC%88%98%EC%9D%98%ED%85%8C%ED%81%AC%EB%8B%88%EC%85%98) — 수의테크니션·동물보건사 알바·신입
- 자세히: [`guides/jobs/16-의료보건.md`](guides/jobs/16-%EC%9D%98%EB%A3%8C%EB%B3%B4%EA%B1%B4.md)

#### 17 돌봄·사회복지·공공

- 스크립트: `alio, gojobs, jobkorea, k, saramin`
- [복지넷 구인정보](https://www.bokji.net/job/off/01.bokji) — 복지관·요양·아동·장애인 시설 사회복지사·생활지도원·요양보호사
- [한국사회복지관협회 구인/구직](https://www.kaswc.or.kr/recruit) — 종합사회복지관 사회복지사·언어재활사·노인맞춤돌봄
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 방문요양·주야간보호·요양원, 중장년 일자리가 가장 많음
- [당근알바](https://jobs.daangn.com/s) — 동네 방문요양·간병·가사·등하원 도우미
- [알바몬](https://www.albamon.com/total-search) — 요양보호사·간병 시급직·주말
- 케어닥 (앱) — 간병·방문요양·가사·동행 일감을 골라 신청
- 케어네이션 (앱) — 병원·방문 간병, 산후·가사 돌봄 매칭
- [고용24 장애인 우대](https://www.work24.go.kr/wk/a/b/1700/themeEmpInfoSrchList.do?pageIndex=1&thmaHrplCd=F00036)
- [한국장애인고용공단 채용정보](https://www.kead.or.kr/bbs/jobinfo/bbsPage.do?menuId=MENU2201)
- [노인일자리 여기](https://www.seniorro.or.kr/noin/searchWork.do) — 65세 이상
- [서울시50플러스](https://www.50plus.or.kr/externalList.do) — 서울 50~64세
- [국가공무원 채용시스템](https://gongmuwon.gosi.kr/crrut/indexMain.do) — 국가직 경력경쟁·개방형·경찰·소방
- [지방자치단체 원서접수](https://local.gosi.go.kr) — 지방공무원
- [클린아이 잡플러스](https://job.cleaneye.go.kr/user/ypRecruitment.do) — 지방공기업·출자출연기관
- 자세히: [`guides/jobs/17-돌봄복지공공.md`](guides/jobs/17-%EB%8F%8C%EB%B4%84%EB%B3%B5%EC%A7%80%EA%B3%B5%EA%B3%B5.md)

#### 18 교육

- 스크립트: `alio, gojobs, jobkorea, saramin`
- [훈장마을](https://www.hunjang.com) — 학원 과목 강사·상담실장·보조강사
- [알바몬](https://www.albamon.com/total-search) — 학원 강사·보조·채점 알바
- [당근알바](https://jobs.daangn.com/s) — 동네 학원·공부방·방과후 보조
- [서울 일자리포털](https://work.sen.go.kr/work/search/recInfo/BD_selectSrchRecInfo.do?q_srchType=rcrtTtl)
- [경기](https://www.goe.go.kr/recruit/ad/func/pb/hnfpPbancList.do?mi=10502)
- [인천](https://www.ice.go.kr/ice/na/ntt/selectNttList.do?mi=10996&bbsId=1774)
- [세종](https://www.sje.go.kr/sje/na/ntt/selectNttList.do?mi=52132&bbsId=108)
- [충북 기간제교사 인력풀](https://www.cbe.go.kr/mpool/na/ntt/selectNttList.do?mi=12127&bbsId=1091)
- [충남 계약제교원](https://www.cne.go.kr/apply/list.do?s=cne&m=032101)
- [전북](https://www.jbe.go.kr/board/list.jbe?boardId=BBS_0000130&menuCd=DOM_000000103004006000)
- [경남 구인·구직포털](https://www.gne.go.kr/works/user/recruitment/BD_recruitmentList.do?q_searchKey=1001)
- [울산 통합인력풀](https://use.go.kr/job/user/bbs/BD_selectBbsList.do?q_bbsSn=2249)
- [제주](https://www.jje.go.kr/board/list.jje?boardId=BBS_0000985&menuCd=DOM_000000103003010000)
- [학교행정지원본부](https://home.pen.go.kr/bsss/main.do) — > 학교채용지원
- [나이스 교육청 온라인채용](https://edurecruit.go.kr) — 교육공무직 등 원서 접수
- [보육교직원 인력뱅크](https://chrd.childcare.go.kr/ctis/job/JobOfferSlPL.jsp) — 어린이집 보육교사·원장
- [복지넷 구인정보](https://www.bokji.net/job/off/01.bokji) — 어린이집·지역아동센터 교사 일부
- [하이브레인넷](https://www.hibrain.net/recruitment/recruits?listType=D3NEW) — 교수·강사·연구원·대학 직원
- [교수신문 교수초빙](https://www.kyosu.net/news/articleList.html?sc_sub_section_code=S2N145) — 전임·비전임 교원 초빙 공고
- 자세히: [`guides/jobs/18-교육.md`](guides/jobs/18-%EA%B5%90%EC%9C%A1.md)

#### 19 음식·조리·식음료

- 스크립트: `alio, gojobs, jobkorea, saramin, worldjob`
- [푸드앤잡](https://www.foodnjob.com/cms/search.php) — 조리사·주방장·주방보조·홀·단체급식 조리원·제과
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 급식·식당 현장직, 중장년
- [알바천국](https://www.alba.co.kr/search/Search) — 카페·프랜차이즈 매장 공고가 가장 많음
- [알바몬](https://www.albamon.com/total-search) — 식당·카페·베이커리 알바, 매니저
- [당근알바](https://jobs.daangn.com/s) — 동네 식당·카페 단기·파트
- [서울](https://work.sen.go.kr/work/search/recInfo/BD_selectSrchRecInfo.do?q_srchType=rcrtTtl&q_srchText=%EC%A1%B0%EB%A6%AC%EC%8B%A4%EB%AC%B4%EC%82%AC) — 대체인력·방학 중 공고 많음
- [대한영양사협회 채용정보](https://www.dietitian.or.kr/work/news/kn_careers.do) — 병원·학교·산업체 단체급식, 어린이급식관리지원센터, 산휴 대체
- [아워홈](https://ourhome.recruiter.co.kr)
- 자세히: [`guides/jobs/19-음식조리.md`](guides/jobs/19-%EC%9D%8C%EC%8B%9D%EC%A1%B0%EB%A6%AC.md)

#### 20 미용·뷰티·예식·반려동물 (생활서비스)

- 스크립트: `jobkorea, saramin`
- [헤어99](https://hair99.co.kr/jobs) — 헤어 디자이너·인턴, 살롱별
- [뷰티인잡](https://www.beautyinjob.kr/job/lists) — 헤어·네일·피부·왁싱·속눈썹·메이크업, 직종 체크 필터
- [헤어인잡](https://www.hairinjob.com/cms/search.php) — 헤어·네일·피부·메이크업
- [헤어커플](https://www.haircouple.co.kr/service/job_list.php) — 헤어 디자이너·스탭, 스페어
- [알바몬](https://www.albamon.com/total-search) — 웨딩플래너·웨딩홀, 애견미용, 네일·피부 보조
- [알바천국](https://www.alba.co.kr/search/Search) — 장례식장·상조 장례지도사, 웨딩홀·행사
- [당근알바](https://jobs.daangn.com/s) — 동네 미용실·네일숍·애견숍·세탁소
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 세탁·수선·현장직, 중장년
- 자세히: [`guides/jobs/20-미용생활서비스.md`](guides/jobs/20-%EB%AF%B8%EC%9A%A9%EC%83%9D%ED%99%9C%EC%84%9C%EB%B9%84%EC%8A%A4.md)

#### 21 여행·숙박·항공·레저

- 스크립트: `alio, jasoseol, jobkorea, saramin, worldjob`
- [관광인](https://academy.visitkorea.or.kr/job/recruit/srchTab1List.do) — 여행사 OP·상품기획, 관광통역안내, 호텔, 카지노
- [호텔인네트워크](https://www.hotelinnetwork.com/recruit/list.php) — 특급호텔·리조트 객실·프런트·세일즈·식음, 경력·관리자급
- [호텔업](https://m.hotelup.com/m/recruit/area) — 모텔·중소 숙박 프런트·실장·룸메이드·부부팀, 경력무관~1년
- [한국골프장경영협회 구인](https://www.kgba.co.kr/06sub01?sfl=wr_subject) — 골프장 프런트·경기팀·예약·코스관리
- [다음 카페 전국 골프장 직원·캐디모집](https://m.cafe.daum.net/golfjob/_rec) — 지역별 직원·캐디, 월 몇 건
- 골인, 시작캐 (앱) — 캐디 구인 앱, 공고 날짜는 확인 못 함
- [한국관광통역안내사협회](https://www.kotga.or.kr) — 관광통역안내사 채용, 월 1~2건
- [크루코리아](https://www.crewkorea.com/recruit/list.do) — 외항사 승무원 채용 대행
- [링커리어](https://linkareer.com/list/recruit) — 대학생 대상 종합, 호텔·항공 신입
- 자세히: [`guides/jobs/21-여행숙박항공.md`](guides/jobs/21-%EC%97%AC%ED%96%89%EC%88%99%EB%B0%95%ED%95%AD%EA%B3%B5.md)

#### 22 경비·청소·시설관리

- 스크립트: `alio, gojobs, jobkorea, saramin`
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 경비·미화·시설 현장직, 중장년이 가장 많음
- [대한주택관리사협회 소장구인](https://www.khma.org/portal/00011/00109/00111.web?stype=title) — 아파트 관리소장
- [같은 협회 직원구인](https://www.khma.org/portal/00011/00109/00114.web) — 관리사무소 경리·기전·과장
- [대한기계설비건설협회 구인정보](https://www.kmcca.or.kr/alarm/recruiting/guinList.do) — 기계설비 유지관리자
- [한국전기기술인협회 구인정보](https://www.keea.or.kr/head/jobinfo/getWJO02R01List.do) — 전기안전관리자
- [한국소방안전원 취업정보](https://www.kfsi.or.kr/customerservice/jobInfo/recruitList.do) — 소방안전관리자
- [노인일자리 여기](https://www.seniorro.or.kr/noin/searchWork.do) — 65세 이상
- [클린아이 잡플러스](https://job.cleaneye.go.kr/user/ypRecruitment.do) — 시설관리공단
- [경기 잡아바](https://job.gg.go.kr/empmn/enterpriseEmployListNew.do)
- 자세히: [`guides/jobs/22-경비청소시설.md`](guides/jobs/22-%EA%B2%BD%EB%B9%84%EC%B2%AD%EC%86%8C%EC%8B%9C%EC%84%A4.md)

#### 23 미디어·문화·예술·스포츠

- 스크립트: `alio, jasoseol, jobkorea, saramin, wanted`
- [미디어잡](https://www.mediajob.co.kr/search/search.htm?cmd=recruit) — 방송 PD·AD·FD·작가·기자·촬영·편집, 신입~경력
- [다음 카페 아랑 채용정보방](https://m.cafe.daum.net) — 기자·PD·작가·FD·언론사 인턴, 신입 위주
- [필름메이커스](https://www.filmmakers.co.kr/crewRecruitingOpen?search_target=title_content&hide_expired=Y) — 영화·영상 스태프, 음악감독, 사진·영상 작가, 단기 프리랜서
- [게임잡 직무별](https://www.gamejob.co.kr/Recruit/joblist?menucode=duty&duty=10) — 게임 사운드
- [아트모아](https://www.artmore.kr/sub/recruit/search_list.do?menu_cd=J) — 공연 기획·운영, 문화재단, 학예사, 단원, 무대 기술
- [한국박물관협회 채용](https://museum.or.kr/job2/?kboard_id=6&view_iframe=1&target=title) — 박물관·미술관 학예사, 월 몇 건
- [대한출판문화협회 출판구인구직](https://member.kpa21.or.kr/kpa/fromcorp-list/?mod=list&target=title) — 출판 편집자·기획, 공고 적음
- [북에디터](https://bookeditor.org) — 출판 편집자
- [대한체육회 스포츠채용정보](https://www.sports.or.kr/sports/bbs/BMSR00024/list.do?menuNo=200027&searchCondition=1) — 종목단체 지도자·트레이너·직원
- [다음 카페 스포드림](https://m.cafe.daum.net) — 헬스 트레이너 구인
- 자세히: [`guides/jobs/23-미디어문화스포츠.md`](guides/jobs/23-%EB%AF%B8%EB%94%94%EC%96%B4%EB%AC%B8%ED%99%94%EC%8A%A4%ED%8F%AC%EC%B8%A0.md)

#### 24 금융·보험 (부동산 금융·운용 포함)

- 스크립트: `alio, jasoseol, jobkorea, kareit, kofia, remember, saramin`
- [한국벤처캐피탈협회 채용공고](https://www.kvca.or.kr/Program/user_board/list.html?a_gb=board&a_cd=7&a_item=0&sm=3_2&keyfield=SUBJECT) — VC 투자심사역·관리역·운용 경력, 거의 매일
- [여신금융협회 회원사 채용](https://www.crefia.or.kr/portal/news/hire/hireList.xx?page=1&searchKey1=4&searchKey2=02) — 신기술금융 심사역·카드·캐피탈
- [새마을금고 채용](https://recruit.kfcc.co.kr/enga/ofcaList.do) — 지역 금고 정규·계약직 수시채용
- [신협 채용](https://www.cu.co.kr/cu/na/ntt/selectNttList.do?mi=100074&bbsId=1070) — 신협 공동채용
- [수협중앙회 인사·채용](https://www.suhyup.co.kr/suhyup/221/subview.do) — 중앙회·공판장·회원조합 일괄채용
- [농협 채용](https://with.nonghyup.com) — 농협중앙회·농협은행·지역농협
- [금융권 공동채용박람회](https://www.financejobfair.co.kr) — 매년 8~9월, 은행·증권·보험 신입
- [피플앤잡](https://www.peoplenjob.com/jobs) — 외국계 금융·헤드헌팅 경력
- [링크드인](https://www.linkedin.com/jobs/search?location=South+Korea) — 외국계 금융
- 자세히: [`guides/jobs/24-금융보험.md`](guides/jobs/24-%EA%B8%88%EC%9C%B5%EB%B3%B4%ED%97%98.md)

#### 25 농림어업

- 스크립트: `alio, gojobs, jobkorea, saramin`
- [도농인력중개플랫폼](https://www.agriwork.kr/front/agrijob/agriJob.do?menu_id=24)
- [알바몬 농업 일자리](https://www.albamon.com/total-search?keyword=%EB%86%8D%EC%B4%8C%EC%9D%B8%EB%A0%A5) — 2026년 5월부터 농식품부 연계, 농협 농촌인력센터 공고
- [고용24](https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do) — 양돈·양계·양식장·농장 상용직이 가장 많음
- [한국선원복지고용센터 모집공고](https://www.koswec.or.kr/koswec/job/marine/selectMarineList.do) — 원양·연근해 어선, 상선 선장·항해사·기관사·부원
- [농촌진흥청 채용공고](https://www.rda.go.kr/board/board.do?mode=list&prgId=acp_adopancmEntry) — 농업연구·기간제·해외농업 전문가
- [한국농어촌공사 채용](https://www.ekr.or.kr/index.krc?contentUid=8a8bb3529665d7140199501cd3ef6280) — 농업기반·수자원 기술직
- [한국임업진흥원 채용](https://www.kofpi.or.kr/notice/notice_04.do) — 산림 공무직·연구
- [경기 잡아바](https://job.gg.go.kr/empmn/enterpriseEmployListNew.do)
- 자세히: [`guides/jobs/25-농림어업.md`](guides/jobs/25-%EB%86%8D%EB%A6%BC%EC%96%B4%EC%97%85.md)
<!-- sites:end -->

## 직접 실행 (셸이 있는 환경)

```bash
python3 career.py search -k "퍼포먼스 마케터" --location 서울 --experience 경력
python3 career.py search -k "부동산 PF,자산운용" --sites saramin,jobkorea,kofia
python3 career.py links -k "간호사"
python3 career.py job --url "공고 링크"
python3 -m unittest discover tests      # 테스트
```

## 주의사항

- **본인 구직용으로만 쓰세요.** 공고 내용의 권리는 각 채용 사이트와 회사에 있어요. 찾은 공고를 모아서 다른 곳에 다시 올리거나 팔지 마세요.
- **AI 결과는 틀릴 수 있어요.** 마감일·급여·근무 조건은 지원 전에 꼭 공고 원문에서 확인하세요.
- **자소서는 초안이에요.** 숫자와 경험은 본인이 확인하고 고쳐서 내세요. AI로 쓴 자소서를 제한하는 회사도 있으니 공고 안내를 확인하세요.
- **민감한 정보는 채팅에 쓰지 마세요.** 주민등록번호, 계좌·카드 번호, 비밀번호는 입력하지 마세요. 채용 사이트 로그인은 에이전트 앱의 로그인·금고 기능으로만 연결하세요.
- **취업 사기를 조심하세요.** 선입금·교육비·장비값 요구, 통장·체크카드 요구, 하는 일이 불분명한 고수익 재택, 인수금을 내야 하는 지입은 의심하세요. 에이전트가 이런 공고를 보면 알려 드려요.
- **지원은 본인이 직접 해요.** 이 스킬은 대신 지원하지 않아요.
- **천천히 쓰세요.** 스크립트는 같은 사이트를 1~1.8초 간격으로 천천히 열어요. 그래도 짧은 시간에 너무 많이 검색하면 사이트가 접속을 막을 수 있고, 에이전트의 하루 무료 사용량도 빨리 줄어요.
- **제보할 때 개인정보를 적지 마세요.** 이슈는 누구나 보는 공개 글이에요.

## 라이선스

[MIT](LICENSE) — 누구나 자유롭게 쓰고, 고치고, 나눌 수 있어요. 저작권 표시만 남겨 주세요. 검색 결과나 사이트 동작은 보증하지 않아요(사이트가 바뀌면 검색이 안 될 수 있어요).

## 제보·문의

- 빠진 사이트, 검색 오류, 개선 의견은 [이슈](https://github.com/Whosekey-Labs/career-skill/issues/new/choose)로 남겨 주세요. 에이전트에게 "이거 제보해줘"라고 하면 대신 정리해서 올려 줘요(올리기 전에 내용을 보여 줘요).
- 이슈는 공개 글이에요. 이름·연락처·이력서 같은 개인정보는 적지 마세요.
- 깃헙 계정이 없으면 오픈채팅방으로 알려 주세요: https://open.kakao.com/o/g3vAeBWi
