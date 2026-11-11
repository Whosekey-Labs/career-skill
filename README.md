# 취업·이직 비서 스킬 (career-skill)

AI 에이전트에게 링크 하나만 주면 **맞춤 공고 찾기 → 회사 분석 → 자소서 초안(워드 파일) → 매일 새 공고 알림**까지 해 주는 지침서예요. 피클, 뮤즈, ChatGPT, Codex, Claude 등 어떤 에이전트든 쓸 수 있어요.

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
| `guides/01-profile.md` | 경력·강점 정리 |
| `guides/02-find-jobs.md` | 공고 찾기 (스크립트 / 브라우저) |
| `guides/industries.md` | 직군별 검색 키워드·사이트 |
| `guides/03-analyze.md` | 회사 분석 + 공고 요건 정리 |
| `guides/04-cover-letter.md` | 자소서 초안 → 워드 파일 |
| `guides/05-daily.md` | 매일 새 공고 알림 |
| `guides/fix-phrases.md` | 결과를 고쳐 달라는 말 예시 |
| `career.py` | 파이썬 기본 기능만 쓰는 검색 도우미 (설치 필요 없음) |

## 약관 지키기

이 스킬은 채용 사이트 약관을 지키도록 만들었어요.

- 사용자가 요청할 때만 검색하고, 한 번에 요청 8번까지, 같은 사이트는 1초 이상 간격을 둬요.
- 스크립트는 자기 이름과 이 저장소 주소를 밝히고 접속해요. 다른 브라우저인 척하거나 차단을 피해 가지 않아요.
- 리멤버·자소설닷컴은 약관으로 자동 수집을 금지해서 스크립트로 긁지 않아요. 링크만 주고, 필요하면 에이전트 브라우저로 사람처럼 한 페이지씩만 봐요.
- 결과는 본인 구직에만 쓰세요. 공고를 모아서 다른 곳에 다시 올리면 각 사이트 약관 위반이에요.

## 직접 실행 (셸이 있는 환경)

```bash
python3 career.py search -k "퍼포먼스 마케터" --location 서울 --experience 경력
python3 career.py search -k "부동산 PF,자산운용" --sites saramin,jobkorea,kofia
python3 career.py links -k "간호사"
python3 career.py job --url "공고 링크"
python3 career.py docx -i 자소서.md      # python-docx 필요
python3 -m unittest discover tests      # 테스트
```

## 문의

써 보다가 막히거나 내 직군에서 이상하게 나오면 오픈채팅방으로 알려 주세요: https://open.kakao.com/o/g3vAeBWi
