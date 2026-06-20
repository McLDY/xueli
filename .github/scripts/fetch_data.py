"""Fetch Bilibili user data and write to data.json."""
import urllib.request, json, time, sys
from datetime import datetime, timezone

UID = sys.argv[1] if len(sys.argv) > 1 else "394065596"
HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com"}

def fetch(url, ref=None):
    h = dict(HEADERS)
    if ref: h["Referer"] = ref
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

data = {}

try:
    j = fetch(f"https://api.bilibili.com/x/relation/stat?vmid={UID}")
    if j.get("code") == 0:
        data["fans"] = j["data"]["follower"]
        data["following"] = j["data"]["following"]
except Exception as e:
    print(f"fans: {e}", file=sys.stderr)

time.sleep(1)

try:
    j = fetch(
        f"https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid={UID}",
        ref="https://live.bilibili.com"
    )
    if j.get("code") == 0:
        d = j["data"]
        data["live_status"] = d.get("live_status", 0)
        data["live_title"] = d.get("title", "")
        data["room_id"] = d.get("roomid", 0)
        data["online"] = d.get("online", 0)
        data["name"] = d.get("uname", "雪梨")
except Exception as e:
    print(f"live: {e}", file=sys.stderr)

time.sleep(1)

try:
    j = fetch(
        f"https://api.bilibili.com/x/space/navnum?mid={UID}",
        ref=f"https://space.bilibili.com/{UID}"
    )
    if j.get("code") == 0:
        d = j["data"]
        data["works"] = d.get("video", 0)
        data["albums"] = d.get("album", 0)
        data["articles"] = d.get("article", 0)
        data["dynamics"] = d.get("opus", 0)
except Exception as e:
    print(f"navnum: {e}", file=sys.stderr)

data["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

with open("data.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(json.dumps(data, ensure_ascii=False))
