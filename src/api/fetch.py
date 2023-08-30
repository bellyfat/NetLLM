from goose3 import Goose


def fetch_url(url: str) -> str:
    return Goose().extract(url=url).cleaned_text


def fetch_first_url():
    pass


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Huawei"
    print(fetch_url(url))
