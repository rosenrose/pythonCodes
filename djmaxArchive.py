import subprocess
import json
import requests
import re
from pathlib import Path

mv_path = Path("e:/djmax mv/")
archive_path = mv_path / "archive"
key = subprocess.run(
    ["git", "config", "--get", "key.youtube"], capture_output=True
).stdout.decode("utf-8")

# subprocess.run(
#     [
#         "yt-dlp",
#         "https://www.youtube.com/playlist?list=UUyWiQldYO_-yeLJC0j5oq2g",
#         "--download-archive",
#         archive_path / "archive.txt",
#         "-o",
#         archive_path / "%(title)s.%(ext)s",
#         "--embed-subs",
#     ]
# )

names = json.load(open(archive_path / "name.json", encoding="utf-8"))

new_id = open(archive_path / "archive.txt", encoding="utf-8").read().splitlines()
new_id = [id.split(" ")[-1] for id in new_id[-int(input("length: ")) :]]

old_id = json.load(open("d:/git/djmax/random_bga/list_fhd.json", encoding="utf-8"))
category = input("category: ")
old_id = list(old_id[category].keys())

infos = {}
for id in new_id:
    info = json.loads(
        requests.get(
            f"https://www.googleapis.com/youtube/v3/videos?id={id}&key={key}&part=snippet,contentDetails"
        ).text
    )
    infos[id] = info
    title = info["items"][0]["snippet"]["title"]
    names[id] = title

    (cut_path := Path(mv_path / "cut" / id)).mkdir(exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            archive_path
            / f"{title.replace('/', '_').replace(':', ' -').replace('?', '')}.webm",
            "-vf",
            "fps=12",
            "-q:v",
            "4",
            cut_path / "%04d.jpg",
        ]
    )
    subprocess.run(["rclone", "copy", cut_path, f"z:/djmax/cut/{id}", "-P"])

json.dump(
    names,
    open(archive_path / "name.json", "w", encoding="utf-8"),
    ensure_ascii=False,
    indent=2,
)

input("list.json")
cuts = json.load(open("d:/git/djmax/random_bga/list.json", encoding="utf-8"))
for id in new_id:
    info = infos[id]
    duration = info["items"][0]["contentDetails"]["duration"]
    result = re.search(r"PT(\d+)M((\d+)S)?", duration)
    duration = int(result[1]) * 60 + (int(result[3]) if result[2] else 0)
    cut = len(list(cut_path.iterdir()))
    print(id, "length", duration, "cut", cut)
    cuts[category][id]["cut"] = cut

json.dump(
    cuts,
    open("d:/git/djmax/random_bga/list.json", "w", encoding="utf-8"),
    ensure_ascii=False,
    indent=2,
)

for id in old_id:
    subprocess.run(["rclone", "purge", f"e:/djmax mv/cut/{id}", "-P"])
    subprocess.run(["rclone", "purge", f"z:/djmax/cut/{id}", "-P"])
