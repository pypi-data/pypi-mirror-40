import attr
import re
import requests
from typing import ClassVar
from bs4 import BeautifulSoup as bs

__all__ = ("Login",)


@attr.s(slots=True, kw_only=True)
class Login:
    """Core methods for logging in to and out of Facebook"""

    _session = attr.ib(type=requests.Session)

    BASE_URL = "https://facebook.com"
    MOBILE_URL = "https://m.facebook.com"
    LOGIN_URL = "{}/login.php?login_attempt=1".format(MOBILE_URL)
    FIND_FB_DTSG = re.compile(r'name="fb_dtsg" value="(.*?)"')
    FIND_CLIENT_REVISION = re.compile(r'"client_revision":(.*?),')
    FIND_LOGOUT_VALUE = re.compile(r'name=\\"h\\" value=\\"(.*?)\\"')

    def _set_fb_dtsg_html(self, html: str) -> None:
        soup = bs(html, "html.parser")

        elem = soup.find("input", {"name": "fb_dtsg"})
        if elem:
            fb_dtsg = elem.get("value")
        else:
            # Fallback to regex
            fb_dtsg = self.FIND_FB_DTSG.search(html).group(1)

        self._session.params["fb_dtsg"] = fb_dtsg

    def _set_default_params(self) -> None:
        resp = self._session.get(self.BASE_URL)

        rev = self.FIND_CLIENT_REVISION.search(resp.text).group(1)

        self._session.params = {
            "__rev": rev,
            "__user": self._session.cookies["c_user"],
            "__a": "1",
        }

        self._set_fb_dtsg_html(resp.text)

    @classmethod
    def login(cls, email: str, password: str) -> "Login":
        """Initialize and login, storing the cookies in the session

        Args:
            email: Facebook `email`, `id` or `phone number`
            password: Facebook account password
        """
        self = cls(session=requests.Session())

        r = self._session.get(self.MOBILE_URL)

        soup = bs(r.text, "html.parser")
        data = {
            elem["name"]: elem["value"]
            for elem in soup.find_all("input")
            if elem.has_attr("value") and elem.has_attr("name")
        }
        data["email"] = email
        data["pass"] = password
        data["login"] = "Log In"

        r = self._session.post(self.LOGIN_URL, data=data)

        if "c_user" not in self._session.cookies:
            raise ValueError("Could not login, failed on: {}".format(r.url))

        self._set_default_params()

        return self

    def logout(self) -> None:
        """Properly log out and invalidate the session"""

        r = self._session.post("/bluebar/modern_settings_menu/", data={"pmid": "4"})
        logout_h = self.FIND_LOGOUT_VALUE.search(r.text).group(1)

        self._session.get("/logout.php", params={"ref": "mb", "h": logout_h})

    def is_logged_in(self) -> bool:
        """Check the login status

        Return:
            Whether the session is still logged in
        """
        # Call the login url, and see if we're redirected to the home page
        r = self._session.get(self.LOGIN_URL, allow_redirects=False)

        return "Location" in r.headers and "home" in r.headers["Location"]
