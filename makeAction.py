import sys
import os
import re
import shutil
from glob import glob
from PIL import Image

path = sys.argv[1]
character = sys.argv[2]
os.chdir(path+"/"+character+"/temp")
regex = re.compile("\d{3}")

actions = [i[:-7] for i in glob("*.png") if regex.search(i)]
actions = list(set(actions))
singles = [i for i in glob("*.png") if not regex.search(i)]
if not os.path.exists("single"):
    os.mkdir("single")
for i in singles:
    shutil.copy(i,"single")
for i in actions:
    if len(glob(i+"???.png"))==1:
        shutil.copy(glob(i+"???.png")[0],"single")
actions = sorted([i for i in actions if len(glob(i+"???.png"))>1])

for action in actions:
    widthSet = set([Image.open(i).width for i in glob(action+"???.png")])
    heightSet = set([Image.open(i).height for i in glob(action+"???.png")])
    if len(widthSet)>1 or len(heightSet)>1:
        print(action+" not identical")
        for i in glob(action+"???.png"):
            print(f"{i} {Image.open(i).width}x{Image.open(i).height}")
        print(max(widthSet),max(heightSet),"\n")
    if "test" in action and action.replace("test_","").replace("test","") in actions:
        print(action+" test")

input(len(actions))
with open("c:/users/crazy/pictures/movedit/test.html") as f:
    images = re.compile("\[.*?\]").findall(f.read())
with open("c:/users/crazy/pictures/movedit/test.html","w") as f:
    for image in images:
        if "filename" not in image:
            input(image+" error")
        start = image.find("filename=\"")+len("filename=\"")
        end = image.rfind(".")
        fileName = image[start:end]
        f.write(image[:-4]+fileName+image[-4:]+"<p>&nbsp;</p>\n")

"""
exList = {"reimu":["occult_mask","reimu_occult_sotoba","samasoBLD"],
            "marisa":["atkHighUpper_blade","atkHigh_Blade","atkMid_Blade","climax_Arm","climax_BackDoor","occult_dr"],
            "ichirin":["cut","occultobject","test_occult"],
            "hijiri":[],"futo":["cut","occult_okiku"],"miko":["half_damage_spin"],
            "nitori":["occult_nessy","testr_climaxback","testr_occult","armHead","canonA"],
            "koishi":["atkHighFrontOB","skillOB","winB_Hat"],"mamizou":["occult_alian"],"kokoro":["climaxMaskA","occult_shot","spellMask_C"],
            "kasen":["tiger","tigerA","dragonB","test_azarashi","spellB_batage","atkUpperArm","climax_Typoon","kanda","occult_armB","occultArm","test_armShotUnder","test_armShotUpper"],
            "mokou":["wingA","wingAb","wingB","wingBb","wingC","wingD","wingE","wingF","test_lose"],
            "sinmyoumaru":["chargeShot_slash","chargeShot_slashB","occult_objectA","sprash"],
            "usami":["half_damage_spin","skillF_Object","atkFrontObject","atkUnderObject","atkUnderObjectB","bird","skillC_sprash","skillD_object","skillE_object","beginBattle_card"],
            "udonge":["kune_deadB","kune_deadC","kuneA","kuneA2P","kuneB","kuneB2P","kuneC","kuneC2P","kuneD","kuneD2P","kuneE","kuneE2P","kuneF","kuneF2P"],
            "doremy":["shot_makura","skill_balloon","spell_C_parts","ball_atk_under","ball_atk_underB","occult_stump","ride_sheep","skill_cushion"],
            "tenshi":["kaname_dorill","kaname_foot","kaname_pile","stone_koma"],
            "yukari":["battle_beginA_chen","test_skill_warpAttack"],
            "jyoon":["half_damage_spin","test_winB","taxi","test_attack_dash_lowB","test_climax_attack","test_gold_typhoon","test_money_fire","test_skillA","test_skillD","test_skillE","test_slide","test_spell_dance_A","test_spell_danceB","test_spell_danceC","test_spell_danceLoop","test_spellA","test_winA","test_winB","aura_tex"],"shion":[]}

actions = [i[:-8] for i in glob("*.png") if regex.search(i) and "hash" not in i and "effect" not in i and "Effect" not in i]
actions = list(set(actions))
singles = [i for i in glob("*.png") if not regex.search(i) and "palette" not in i and "effect" not in i and "Effect" not in i]
for i in singles:
    shutil.copy(i,"single")
for i in actions:
    if len(glob(i+"????.png"))==1:
        shutil.copy(glob(i+"????.png")[0],"single")
actions = [i for i in actions if len(glob(i+"????.png"))>1 and i not in exList[character]]

for action in actions:
    widthSet = set([Image.open(i).width for i in glob(action+"????.png")])
    heightSet = set([Image.open(i).height for i in glob(action+"????.png")])
    if len(widthSet)>1 or len(heightSet)>1:
        print(action+" not identical")
        for i in glob(action+"????.png"):
            print("%s %dx%d"%(i,Image.open(i).width,Image.open(i).height))
        input()
    if "test" in action and action.replace("test_","").replace("test","") in actions:
        print(action+" test")
"""