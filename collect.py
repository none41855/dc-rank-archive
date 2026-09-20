import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path

URL = "https://gall.dcinside.com/n"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

ranking = {}

for a in soup.select('a[href*="/mini/board/lists/?id="]'):
    num = a.select_one(".num")

    if not num:
        continue

    try:
        rank = int(num.get_text(strip=True).rstrip("."))
    except ValueError:
        continue

    if not 1 <= rank <= 300:
        continue

    name = a.get_text(" ", strip=True)
    name = name.replace(num.get_text(strip=True), "").strip()

    ranking[rank] = {
        "rank": rank,
        "name": name,
        "url": "https://gall.dcinside.com" + a["href"]
    }

if len(ranking) != 300:
    raise RuntimeError(f"300개를 수집하지 못했습니다: {len(ranking)}개")

KST = timezone(timedelta(hours=9))
date = datetime.now(KST).strftime("%Y-%m-%d")

Path("data").mkdir(exist_ok=True)

with open(f"data/{date}.json", "w", encoding="utf-8") as f:
    json.dump(
        [ranking[i] for i in range(1, 301)],
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"{date}: 300개 저장 완료")
