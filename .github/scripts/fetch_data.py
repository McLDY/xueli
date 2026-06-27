"""Fetch Bilibili user data + dynamics (opus + video)."""
import urllib.request, json, time, sys, os
from datetime import datetime, timezone

UID = sys.argv[1] if len(sys.argv) > 1 else "394065596"
COOKIE = os.environ.get("BILI_COOKIE", "")

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch(url, ref=None, auth=False):
    h = dict(HEADERS)
    if ref: h["Referer"] = ref
    if auth and COOKIE:
        h["Cookie"] = COOKIE
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
    j = fetch(f"https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid={UID}", ref="https://live.bilibili.com")
    if j.get("code") == 0:
        d = j["data"]
        data["live_status"] = d.get("live_status", 0)
        data["live_title"] = d.get("title", "")
        data["room_id"] = d.get("roomid", 0)
        data["online"] = d.get("online", 0)
        data["name"] = d.get("uname", "\u96ea\u68a8")
except Exception as e:
    print(f"live: {e}", file=sys.stderr)
time.sleep(1)

try:
    j = fetch(f"https://api.bilibili.com/x/space/navnum?mid={UID}", ref=f"https://space.bilibili.com/{UID}")
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
print("data.json:", json.dumps(data, ensure_ascii=False))

# Dynamics
dynamics = []
if not COOKIE:
    print("No BILI_COOKIE, skipping dynamics", file=sys.stderr)
else:
    time.sleep(1)
    try:
        j = fetch(
            f"https://api.bilibili.com/x/polymer/web-dynamic/v1/opus/feed/space?host_mid={UID}&type=all",
            ref=f"https://space.bilibili.com/{UID}",
            auth=True
        )
        for item in j.get("data", {}).get("items", []):
            content = (item.get("content") or "").strip()
            cover = item.get("cover")
            oid = item.get("opus_id", "") or ""
            sid = oid[-12:] if len(oid) >= 12 else oid
            entry = {"id": sid, "type": "text", "content": content, "date": ""}
            if cover and cover.get("url"):
                entry["type"] = "image"
                entry["images"] = [{"src": cover["url"].replace("http://", "https://"), "width": cover.get("width", 0), "height": cover.get("height", 0)}]
            dynamics.append(entry)
    except Exception as e:
        print(f"opus: {e}", file=sys.stderr)

    time.sleep(1)
    try:
        j = fetch(
            f"https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid={UID}",
            ref=f"https://space.bilibili.com/{UID}/dynamic",
            auth=True
        )
        for item in j.get("data", {}).get("items", []):
            if item.get("type") != "DYNAMIC_TYPE_AV":
                continue
            mod = item.get("modules", {})
            dyn = mod.get("module_dynamic", {})
            major = dyn.get("major") or {}
            arc = major.get("archive") if major.get("type") == "MAJOR_TYPE_ARCHIVE" else None
            if not arc or not arc.get("title"):
                continue
            ts = mod.get("module_author", {}).get("pub_ts") or 0
            date = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d") if ts else ""
            sid = (item.get("id_str") or "")[-12:]
            dynamics.append({"id": sid, "type": "video", "content": "", "date": date, "video": {"title": arc["title"], "bvid": arc.get("bvid", "")}})
    except Exception as e:
        print(f"dynamics: {e}", file=sys.stderr)

    dynamics.sort(key=lambda x: x.get("date", ""), reverse=True)
    with open("dynamics.json", "w") as f:
        json.dump(dynamics, f, ensure_ascii=False, indent=2)
    print(f"dynamics.json: {len(dynamics)} items")
