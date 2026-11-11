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


class SmallSiteParserTest(unittest.TestCase):
    def test_gnuboard_table_row(self):
        page = ('<table><tbody><tr><td> 2026-11-06 </td>'
                '<td><a class="com_name" href="https://x.com/bbs/board.php?bo_table=guin&amp;wr_id=4479">부천다온요양병원</a></td>'
                '<td><a href="https://x.com/bbs/board.php?bo_table=guin&amp;wr_id=4479">단체<b class="sch_word">급식</b> 조리사 구인</a></td>'
                '<td>조리사</td><td> 경기 부천 </td><td></td></tr></tbody></table>')
        r = career.gnu_parse(page, "x.com", "guin", "영양사잡", 5)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["title"], "단체급식 조리사 구인")
        self.assertEqual(r[0]["company"], "부천다온요양병원")
        self.assertEqual(r[0]["postedDate"], "2026-11-06")
        self.assertEqual(r[0]["location"], "경기 부천")
        self.assertTrue(r[0]["url"].endswith("bo_table=guin&wr_id=4479"))

    def test_gnuboard_single_quote_and_plain_company(self):
        page = ("<tr><td><img src='u.gif'></td><td>포쉬네일AK광명점</td>"
                "<td><a class='b1' href='../bbs/board.php?bo_table=guin&wr_id=15298'><span>함께 할 선생님 모셔요</span></a></td>"
                "<td>네일아트</td><td>경기 광명시</td></tr>")
        r = career.gnu_parse(page, "y.com", "guin", "네일링크", 5)
        self.assertEqual(r[0]["company"], "포쉬네일AK광명점")
        self.assertEqual(r[0]["title"], "함께 할 선생님 모셔요")

    def test_new_hosts_allowed(self):
        for url in ("https://xn--vb0b9ha655ovjk91aba684a.com/bbs/board.php", "https://www.gisuljob.co.kr/employ/search2.html",
                    "https://jokyungjob.mycafe24.com/bbs/board.php", "https://api.bookjob.co.kr/api/v1/job-posting"):
            career.check_url(url)
        with self.assertRaises(RuntimeError):
            career.check_url("https://other.mycafe24.com/")


class RegistryTest(unittest.TestCase):
    def test_every_site_has_name(self):
        for key in career.SITES:
            self.assertIn(key, career.SITE_NAMES)


class CountTest(unittest.TestCase):
    def test_count_chars(self):
        self.assertEqual(career.count_chars("가나 다\n라"), (6, 4))


class DeadlineMoreTest(unittest.TestCase):
    def test_past_dates_are_returned(self):
        self.assertEqual(career.parse_deadline("10/20", TODAY), dt.date(2026, 10, 20))
        self.assertEqual(career.parse_deadline("~ 10.25(토)", TODAY), dt.date(2026, 10, 25))

    def test_two_digit_year_and_compact(self):
        self.assertEqual(career.parse_deadline("26.11.20", TODAY), dt.date(2026, 11, 20))
        self.assertEqual(career.parse_deadline("20261130", TODAY), dt.date(2026, 11, 30))
        self.assertEqual(career.parse_deadline(20261130, TODAY), dt.date(2026, 11, 30))

    def test_range_takes_last(self):
        self.assertEqual(career.parse_deadline("2026-11-01 ~ 2026-11-30", TODAY), dt.date(2026, 11, 30))
        self.assertEqual(career.parse_deadline("11/05 ~ 11/20", TODAY), dt.date(2026, 11, 20))

    def test_nearest_year(self):
        self.assertEqual(career.parse_deadline("12/28", dt.date(2027, 1, 5)), dt.date(2026, 12, 28))
        self.assertEqual(career.parse_deadline("01/05", dt.date(2026, 12, 20)), dt.date(2027, 1, 5))

    def test_tidy_reads_title_deadline_and_drops_past(self):
        jobs = [career.job(title="[A운용] 리츠 운용역 채용 (~11/9)", company="A운용", url="p", site="금투협"),
                career.job(title="[B운용] PF 심사역 (~11/16)", company="B운용", url="q", site="금투협"),
                career.job(title="C 공고", company="C", deadline="10/20", url="r", site="사람인")]
        out = career.tidy(jobs, TODAY)
        self.assertEqual([j["url"] for j in out], ["q"])
        self.assertEqual(out[0]["_d"], dt.date(2026, 11, 16))

    def test_non_string_values(self):
        j = career.job(title="t", deadline=20261130, experience=3, url="x", site="s")
        self.assertEqual(j["experience"], "3")
        career.render(career.tidy([j], TODAY), TODAY, "h")

    def test_dedupe_without_company_uses_url(self):
        jobs = [career.job(title="간호조무사 구인", url="u1", site="X"), career.job(title="간호조무사 구인", url="u2", site="X")]
        self.assertEqual(len(career.tidy(jobs, TODAY)), 2)


class SelectionTest(unittest.TestCase):
    def test_each_site_kept(self):
        jobs = [career.job(title=f"s{i}", company=f"c{i}", deadline="2026-11-20", url=f"s{i}", site="사람인") for i in range(20)]
        jobs += [career.job(title=f"k{i}", company=f"k{i}", url=f"k{i}", site="금투협") for i in range(3)]
        out = career.pick_balanced(career.tidy(jobs, TODAY), 15)
        self.assertEqual(len(out), 15)
        self.assertEqual(sum(1 for j in out if j["site"] == "금투협"), 2)


class NewOnlyTest(unittest.TestCase):
    def test_record_only_shown(self):
        import tempfile
        d = tempfile.mkdtemp()
        old = career.DATA_DIR
        career.DATA_DIR = d
        try:
            jobs = [career.job(title=f"t{i}", url=f"u{i}", site="s") for i in range(10)]
            new = career.filter_new(jobs)
            career.record_seen(new[:3])
            self.assertEqual(len(career.filter_new(jobs)), 7)
        finally:
            career.DATA_DIR = old


class LocationTest(unittest.TestCase):
    def test_subregion(self):
        spec = career.loc_spec("판교")
        self.assertEqual(spec[0], "경기")
        self.assertTrue(career.loc_keep({"location": "경기 성남시 분당구"}, spec))
        self.assertFalse(career.loc_keep({"location": "경기 수원시"}, spec))
        self.assertFalse(career.loc_keep({"location": "서울 강남구"}, spec))
        self.assertIsNone(career.loc_keep({"location": ""}, spec))

    def test_sido(self):
        spec = career.loc_spec("부산")
        self.assertTrue(career.loc_keep({"location": "부산 해운대구"}, spec))
        self.assertFalse(career.loc_keep({"location": "경기 성남"}, spec))
        self.assertTrue(career.loc_keep({"location": "부산광역시 부산진구"}, spec))
        self.assertIsNone(career.loc_spec("어딘가"))
        self.assertFalse(career.title_loc_keep("[강남구청역] 피부과 간호조무사", spec))
        self.assertTrue(career.title_loc_keep("해운대 피부과 간호조무사", spec))
        self.assertIsNone(career.title_loc_keep("피부과 간호조무사", spec))


class CountBlankTest(unittest.TestCase):
    def test_blanks_not_counted(self):
        self.assertEqual(career.count_chars("가나[직접 입력: 숫자]다 [추정]"), (3, 3))


class UrlScopeTest(unittest.TestCase):
    def test_company_hosts_separated(self):
        with self.assertRaises(RuntimeError):
            career.check_url("https://web.archive.org/web/2024/https://evil.com/", resolve=False)
        with self.assertRaises(RuntimeError):
            career.check_url("https://bizno.net/?query=x", resolve=False)
        career.check_url("https://bizno.net/?query=x", career.COMPANY_HOSTS, resolve=False)

    def test_private_ip_rejected(self):
        orig = career.socket.getaddrinfo
        career.socket.getaddrinfo = lambda *a, **k: [(2, 1, 6, "", ("127.0.0.1", 0))]
        try:
            with self.assertRaises(RuntimeError):
                career.check_url("https://www.saramin.co.kr/")
        finally:
            career.socket.getaddrinfo = orig
        career.socket.getaddrinfo = lambda *a, **k: [(2, 1, 6, "", ("198.18.0.5", 0))]   # 프록시 가짜 IP는 허용
        try:
            career.check_url("https://www.saramin.co.kr/")
        finally:
            career.socket.getaddrinfo = orig


if __name__ == "__main__":
    unittest.main()
