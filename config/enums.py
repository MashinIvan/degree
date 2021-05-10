from enum import Enum


class EOS(str, Enum):
    UBUNTU = "ubuntu"
    WINDOWS = "windows"


class EBrowser(str, Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"


class ECountry(str, Enum):
    RUSSIA = "ru"
    GERMANY = "de"
    CHINA = "cn"
    USA = "com"
    ENGLAND = "uk"
    FRANCE = "fr"
    ITALY = "it"


class ESearchPlace(str, Enum):
    SOCHI = "Sochi"
    PARIS = "Paris"
    LONDON = "London"
    MAIAMI = "Miami"
    CAIRO = "Cairo"
    BANGKOK = "Bangkok"
    SYDNEY = "Sydney"


class EUserAgentChrome(str, Enum):
    MAC = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
    WINDOWS = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
    LINUX = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
    MOBILE = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.163 Mobile/15E148 Safari/604.1"


class EUserAgentFirefox(str, Enum):
    MAC = "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0"
    WINDOWS = "Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0"
    LINUX = "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0"
    MOBILE = "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4"


class ERivals(str, Enum):
    TRIPADVISOR = "https://www.tripadvisor.com/"
    EXPEDIA = "https://www.expedia.com/"
    HOTELS = "https://ru.hotels.com/"
