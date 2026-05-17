"""Bug regression tests for instagram_followback.py (no credentials needed)."""

import os
import pathlib
import sys
import unittest
import unittest.mock as mock
import instaloader

with mock.patch("builtins.input"), mock.patch("webbrowser.open"):
    import instagram_followback as app


def _make_report(non_verified, verified, username="testuser"):
    all_dict = dict(non_verified + verified)
    return app.save_html_report(all_dict, non_verified, verified, username)


class TestSaveHtmlReport(unittest.TestCase):

    def test_basic_output(self):
        non_v = [
            ("user_a", {"full_name": "Alice", "is_verified": False, "userid": 1}),
            ("user_c", {"full_name": "", "is_verified": False, "userid": 3}),
        ]
        verified = [
            ("user_b", {"full_name": "Bob", "is_verified": True, "userid": 2}),
        ]
        filename = _make_report(non_v, verified)
        try:
            content = open(filename, encoding="utf-8").read()
            self.assertIn("@user_a", content)
            self.assertIn("@user_b", content)
            self.assertIn("@user_c", content)
            self.assertIn("VERIFIED", content)
            self.assertIn("https://www.instagram.com/user_a/", content)
            self.assertIn("3", content)  # total count
        finally:
            os.remove(filename)

    def test_full_name_html_escaped(self):
        """full_name with HTML special chars must be escaped to avoid broken HTML."""
        evil = "<script>alert(1)</script>"
        non_v = [("evil_user", {"full_name": evil, "is_verified": False, "userid": 99})]
        filename = _make_report(non_v, [])
        try:
            content = open(filename, encoding="utf-8").read()
            self.assertNotIn("<script>alert(1)</script>", content, "raw HTML tag found in output")
            self.assertIn("&lt;script&gt;", content, "escaped form not found")
        finally:
            os.remove(filename)

    def test_ampersand_in_full_name_escaped(self):
        name = "Ben & Jerry"
        non_v = [("user_x", {"full_name": name, "is_verified": False, "userid": 10})]
        filename = _make_report(non_v, [])
        try:
            content = open(filename, encoding="utf-8").read()
            self.assertNotIn("Ben & Jerry", content)
            self.assertIn("Ben &amp; Jerry", content)
        finally:
            os.remove(filename)

    def test_empty_full_name_does_not_render_dash(self):
        non_v = [("user_empty", {"full_name": "", "is_verified": False, "userid": 5})]
        filename = _make_report(non_v, [])
        try:
            content = open(filename, encoding="utf-8").read()
            self.assertIn("@user_empty", content)
            self.assertNotIn('class="fullname"', content)
        finally:
            os.remove(filename)

    def test_no_verified_section_when_empty(self):
        """The verified <h2> section must be omitted when there are no verified users."""
        non_v = [("user_a", {"full_name": "Alice", "is_verified": False, "userid": 1})]
        filename = _make_report(non_v, [])
        try:
            content = open(filename, encoding="utf-8").read()
            self.assertNotIn("Verified Accounts</h2>", content)
        finally:
            os.remove(filename)


class TestFileUri(unittest.TestCase):

    def test_file_uri_correct_format(self):
        """pathlib.as_uri() must produce file:/// with forward slashes."""
        dummy = "dummy_test.html"
        open(dummy, "w").close()
        try:
            uri = pathlib.Path(os.path.abspath(dummy)).as_uri()
            self.assertTrue(uri.startswith("file:///"), f"Bad URI: {uri}")
            self.assertNotIn("\\", uri, f"Backslash in URI: {uri}")
        finally:
            os.remove(dummy)


class TestSourceChecks(unittest.TestCase):

    def setUp(self):
        self.src = open("instagram_followback.py", encoding="utf-8").read()

    def test_sys_not_imported(self):
        self.assertNotIn("import sys", self.src, "sys is imported but never used")

    def test_empty_username_validated(self):
        self.assertIn("Username cannot be empty", self.src)

    def test_2fa_exception_caught(self):
        self.assertIn("_do_two_factor_login", self.src)
        self.assertIn("BadCredentialsException", self.src)
        self.assertIn("InvalidArgumentException", self.src)

    def test_uses_pathlib_uri(self):
        self.assertIn("as_uri()", self.src, "pathlib.as_uri() not used for browser URL")

    def test_login_exception_handled(self):
        self.assertIn("LoginException", self.src)
        self.assertIn("checkpoint", self.src)

    def test_too_many_requests_handled(self):
        self.assertIn("TooManyRequestsException", self.src)

    def test_bad_credentials_handled(self):
        self.assertIn("BadCredentialsException", self.src)
        self.assertIn("Wrong password", self.src)

    def test_null_login_result_handled(self):
        self.assertIn("_print_null_login_help", self.src)
        self.assertIn("instagram.com", self.src)

    def test_session_login_attempted(self):
        self.assertIn("_try_session_login", self.src)
        self.assertIn("save_session_to_file", self.src)


class TestSessionLogin(unittest.TestCase):

    def _make_loader(self):
        return instaloader.Instaloader(), app

    def test_valid_session_returns_true(self):
        L, app = self._make_loader()
        with mock.patch.object(L, "load_session_from_file"), \
             mock.patch.object(L, "test_login", return_value="myuser"):
            result = app._try_session_login(L, "myuser")
        self.assertTrue(result)

    def test_no_session_file_returns_false(self):
        L, app = self._make_loader()
        with mock.patch.object(L, "load_session_from_file", side_effect=FileNotFoundError):
            result = app._try_session_login(L, "myuser")
        self.assertFalse(result)

    def test_expired_session_returns_false(self):
        L, app = self._make_loader()
        with mock.patch.object(L, "load_session_from_file"), \
             mock.patch.object(L, "test_login", return_value=None):
            result = app._try_session_login(L, "myuser")
        self.assertFalse(result)

    def test_session_username_mismatch_returns_false(self):
        """Session file for a different user must not be accepted."""
        L, app = self._make_loader()
        with mock.patch.object(L, "load_session_from_file"), \
             mock.patch.object(L, "test_login", return_value="other_user"):
            result = app._try_session_login(L, "myuser")
        self.assertFalse(result)


class TestTwoFactorLogin(unittest.TestCase):

    def _make_loader(self):
        L = instaloader.Instaloader()
        return L, app

    def test_correct_code_succeeds(self):
        L, app = self._make_loader()
        with mock.patch.object(L, "two_factor_login", return_value=None) as m, \
             mock.patch("builtins.input", return_value="123456"):
            result = app._do_two_factor_login(L)
        self.assertTrue(result)
        m.assert_called_once_with("123456")

    def test_wrong_code_retries_then_fails(self):
        L, app = self._make_loader()
        # 3 code attempts + 1 "Press Enter to exit" prompt
        inputs = iter(["000000", "111111", "222222", ""])
        with mock.patch.object(L, "two_factor_login",
                               side_effect=instaloader.exceptions.BadCredentialsException("bad")), \
             mock.patch("builtins.input", side_effect=inputs):
            result = app._do_two_factor_login(L, max_attempts=3)
        self.assertFalse(result)

    def test_expired_session_aborts(self):
        L, app = self._make_loader()
        with mock.patch.object(L, "two_factor_login",
                               side_effect=instaloader.exceptions.InvalidArgumentException("expired")), \
             mock.patch("builtins.input", return_value="123456"):
            result = app._do_two_factor_login(L, max_attempts=3)
        self.assertFalse(result)

    def test_succeeds_on_second_attempt(self):
        L, app = self._make_loader()
        calls = [instaloader.exceptions.BadCredentialsException("bad"), None]
        inputs = iter(["wrong", "correct"])
        with mock.patch.object(L, "two_factor_login", side_effect=calls), \
             mock.patch("builtins.input", side_effect=inputs):
            result = app._do_two_factor_login(L, max_attempts=3)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
