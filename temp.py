import json
import sys
import shutil
import re
import pyperclip
from pathlib import Path
from functools import reduce

path = Path("d:/git/djmax/list.json")

# data = json.loads(path.read_text(encoding="utf-8"))
# songs = reduce(lambda x,y: [*x, *y], data["songs"].values())
# # print(len(songs))
# regex = re.compile(r"[^[]+")

# notes = pyperclip.paste().replace("Elastic Star","Elastic STAR").replace("Super lovely","Super Lovely").replace("Running Girl","Running girl").replace("Nine point eight","Nine Point Eight").replace("I want You ~반짝 반짝 Sunshine~","I want You ~반짝★반짝 Sunshine~").splitlines()

# # if len(notes) % 18 == 0:
# #     print(len(notes), len(notes)//18)

# notes = [[j for j in notes[i*18:(i+1)*18]] for i in range(442)]

# # print(regex.match(notes[1][1])[0])

# noteList = [
#     {
#         "title": regex.match(note[1])[0],
#         "note": {
#             "4B": {
#                 "NM": note[2] if note[2] == "-" else int(note[2]),
#                 "HD": note[3] if note[3] == "-" else int(note[3]),
#                 "MX": note[4] if note[4] == "-" else int(note[4]),
#                 "SC": note[5] if note[5] == "-" else int(note[5])
#             },
#             "5B": {
#                 "NM": note[6] if note[6] == "-" else int(note[6]),
#                 "HD": note[7] if note[7] == "-" else int(note[7]),
#                 "MX": note[8] if note[8] == "-" else int(note[8]),
#                 "SC": note[9] if note[9] == "-" else int(note[9])
#             },
#             "6B": {
#                 "NM": note[10] if note[10] == "-" else int(note[10]),
#                 "HD": note[11] if note[11] == "-" else int(note[11]),
#                 "MX": note[12] if note[12] == "-" else int(note[12]),
#                 "SC": note[13] if note[13] == "-" else int(note[13])
#             },
#             "8B": {
#                 "NM": note[14] if note[14] == "-" else int(note[14]),
#                 "HD": note[15] if note[15] == "-" else int(note[15]),
#                 "MX": note[16] if note[16] == "-" else int(note[16]),
#                 "SC": note[17] if note[17] == "-" else int(note[17])
#             },
#         }
#     }
#     for note in notes
# ]
# # print(noteList[-1])

# a = set([i["title"] for i in noteList]) - set([i["title"] for i in songs])
# # print(*a,sep="\n")
# i = 0
# for song in songs:
#     for note in noteList:
#         if song["title"] == note["title"]:
#             song["note"] = note["note"]
#             for btn in song["level"]:
#                 for rank in list(note["note"][btn].keys()):
#                     if rank not in song["level"][btn]:
#                         # print(rank, note["note"][btn][rank])
#                         del note["note"][btn][rank]
#                 if not song["level"][btn].keys() == note["note"][btn].keys():
#                     print("!!!!", song["title"])
#             break
#     else:
#         print("???")

# path.with_stem("list_").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
data = json.loads(path.read_text(encoding="utf-8"))
songs = reduce(lambda x,y: [*x, *y], data["songs"].values())
for song in songs:
    for btn in song["level"]:
        for rank in song["level"][btn]:
            if rank not in song["note"][btn]:
                print("!!!!", song["title"])
    for btn in song["note"]:
        for rank in song["note"][btn]:
            if rank not in song["level"][btn]:
                print("?????", song["title"])
    # for category in song["artist"]:
    #     if category == "visualize":
    #         if isinstance(song["artist"][category], list):
    #             print(song["title"])
    #         elif isinstance(song["artist"][category], dict):
    #             for subcat in song["artist"][category]:
    #                 if not isinstance(song["artist"][category][subcat], str):
    #                     print(song["title"])
    #     else:
    #         if not isinstance(song["artist"][category], str):
    #             print(song["title"])