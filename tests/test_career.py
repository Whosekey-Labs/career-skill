import datetime as dt
import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location("career", pathlib.Path(__file__).parent.parent / "career.py")
career = importlib.util.module_from_spec(spec)
spec.loader.exec_module(career)

TODAY = dt.date(2026, 11, 11)


class DeadlineTest(unittest.TestCase):
    def test_formats(self):
        self.assertEqual(career.parse_deadline("~ 11/19(목)", TODAY), dt.date(2026, 11, 19))
        self.assertEqual(career.parse_deadline("2026-11-15", TODAY), dt.date(2026, 11, 15))
        self.assertEqual(career.parse_deadline("오늘마감", TODAY), TODAY)
        self.assertIsNone(career.parse_deadline("상시채용", TODAY))

    def test_year_rollover(self):
        self.assertEqual(career.parse_deadline("~ 01/05", dt.date(2026, 12, 20)), dt.date(2027, 1, 5))


class TidyTest(unittest.TestCase):
    def test_expired_and_dedupe(self):
        jobs = [
            career.job(title="마케터 채용", company="(주)카카오", deadline="~ 11/20", url="a", site="사람인"),
            career.job(title="마케터 채용", company="카카오", deadline="2026-11-20", url="b", site="잡코리아"),
            career.job(title="[마감] 디자이너", company="X", url="c", site="사람인"),
            career.job(title="개발자", company="Y", deadline="2026-11-01", url="d", site="잡코리아"),
        ]
        out = career.tidy(jobs, TODAY)
        self.assertEqual([j["url"] for j in out], ["a"])
        self.assertEqual(out[0]["alsoOn"], ["잡코리아: b"])


class UrlCheckTest(unittest.TestCase):
    def test_rejects_unsafe(self):
        for bad in ("file:///etc/passwd", "http://127.0.0.1/", "http://169.254.169.254/latest", "ftp://x.com/",
                    "https://evil.com/", "https://saramin.co.kr.evil.com/", "https://www.saramin.co.kr%2e@127.0.0.1/",
                    "https://user@www.saramin.co.kr/"):
            with self.assertRaises(RuntimeError):
                career.check_url(bad)

    def test_allows_job_sites(self):
        career.check_url("https://www.saramin.co.kr/zf_user/search")
        career.check_url("https://www.kofia.or.kr/brd/m_96/list.do")
        for ok in ("https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do",
                   "https://www.nursejob.co.kr/recruit/search.php", "https://kr.linkedin.com/jobs/view/1",
                   "https://okky.kr/articles/1", "http://lawlandr.kabl.kr/modules/kabl/job/list_json.kabl"):
            career.check_url(ok)

    def test_rejects_lookalike_new_hosts(self):
        for bad in ("https://nursejob.co.kr.evil.com/", "https://evilokky.kr/", "https://work24.go.kr@evil.com/"):
            with self.assertRaises(RuntimeError):
                career.check_url(bad)


class DateHelperTest(unittest.TestCase):
    def test_iso(self):
        self.assertEqual(career._iso("2026/11/11"), "2026-11-11")
        self.assertEqual(career._iso("2026.1.5"), "2026-01-05")
        self.assertEqual(career._iso("26-11-06"), "2026-11-06")
        self.assertEqual(career._iso("상시채용"), "상시채용")
        self.assertIsNone(career._iso(None))

    def test_date_and_dates(self):
        self.assertEqual(career._date("등록 2026.11.05 마감 2026.11.30"), "2026-11-05")
        self.assertEqual(career._dates("26.11.10 ~ 26.11.20"), ["2026-11-10", "2026-11-20"])
        self.assertIsNone(career._date("날짜 없음"))

    def test_ago(self):
        today = dt.date.today()
        self.assertEqual(career._ago("4분전"), today.isoformat())
        self.assertEqual(career._ago("3일전"), (today - dt.timedelta(days=3)).isoformat())
        self.assertEqual(career._ago("2026.10.29"), "2026-10-29")
        self.assertIsNone(career._ago(""))

    def test_match(self):
        self.assertTrue(career._match("간호사 병동", "병동 간호사 모집"))
        self.assertFalse(career._match("간호사 수술실", "병동 간호사 모집"))
        self.assertTrue(career._match("", "아무거나"))


class PageTextTest(unittest.TestCase):
    def test_skips_menu(self):
        page = ("<html><head><title>[ABC병원] 병동 간호사 모집 - 널스잡</title></head><body>"
                "<nav>채용정보 인재정보 알바정보</nav><div>로그인</div><div>회원가입</div>"
                "<h1>병동 간호사 모집</h1><p>근무조건 3교대</p><footer>회사소개</footer></body></html>")
        text = career._page_text(page)
        self.assertTrue(text.startswith("병동 간호사 모집"))
        self.assertIn("근무조건", text)
        self.assertNotIn("회사소개", text)


class RegistryTest(unittest.TestCase):
    def test_every_site_has_name_and_host(self):
        for key in career.SITES:
            self.assertIn(key, career.SITE_NAMES)


if __name__ == "__main__":
    unittest.main()
