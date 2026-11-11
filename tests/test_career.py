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
        for bad in ("file:///etc/passwd", "http://127.0.0.1/", "http://169.254.169.254/latest", "ftp://x.com/"):
            with self.assertRaises(RuntimeError):
                career.check_url(bad)


if __name__ == "__main__":
    unittest.main()
