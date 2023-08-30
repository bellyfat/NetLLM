import json

import requests

from src.api.search_result import SearchResult

url = "https://google.serper.dev/search"


def google_search(query):
    payload = json.dumps({"q": query})
    headers = {
        "X-API-KEY": "",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


if __name__ == "__main__":
    # result = google_search("华为")
    # with open("google.json", "w", encoding="utf-8") as f:
    #     json.dump(result, f, ensure_ascii=False)
    with open("google.json") as f:
        result = json.load(f)
    res = SearchResult(result).useful_info
    print(res)
