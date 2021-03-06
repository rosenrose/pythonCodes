from PIL import Image, ImageChops
from pathlib import Path
import sys
import shutil

path = Path("D:/git/djmax/ignore/Sprite")

arg2 = sys.argv[2] if len(sys.argv) > 2 else ""

if sys.argv[1] == "crop":
    if arg2 == "mv":
        width, height = 230, 130
        img1 = Image.open(path / "MvThumbnails_9.png")
        img2 = Image.open(path / "MvThumbnails_10.png")
        (path / "mvthumb1").mkdir(exist_ok=True)
        (path / "mvthumb2").mkdir(exist_ok=True)
        for i in range(31):
            for j in range(12 if i < 8 else 13 if i < 9 else 17):
                img1.crop(
                    (
                        0 + (j * width) + (j * 2),
                        6 + (i * height) + (i * 2),
                        0 + (j * width) + (j * 2) + width,
                        6 + (i * height) + (i * 2) + height,
                    )
                ).save(path / f"mvthumb1/{i+1:02}_{j+1:02}.png")
            for j in range(12 if i < 6 else 13 if i < 9 else 17):
                img2.crop(
                    (
                        0 + j * width + j,
                        36 + i * height + i,
                        0 + j * width + width + j,
                        36 + i * height + height + i,
                    )
                ).save(path / f"mvthumb2/{i+1:02}_{j+1:02}.png")
    elif arg2 == "song":
        width = height = 120
        img1 = Image.open(path / "CommonThumbnails_9.png")
        img2 = Image.open(path / "CommonThumbnails_10.png")
        (path / "songthumb1").mkdir(exist_ok=True)
        (path / "songthumb2").mkdir(exist_ok=True)
        for i in range(33):
            for j in range(8 if i < 10 else 9 if i < 24 else 33):
                img1.crop(
                    (
                        0 + (j * width) + (j * 2),
                        72 + (i * height) + (i * 2),
                        0 + (j * width) + (j * 2) + width,
                        72 + (i * height) + (i * 2) + height,
                    )
                ).save(path / f"songthumb1/{i+1:02}_{j+1:02}.png")
        for i in range(33):
            for j in range(8 if i < 8 else 9 if i < 24 else 33):
                img2.crop(
                    (
                        0 + j * width + j,
                        104 + i * height + i,
                        0 + j * width + width + j,
                        104 + i * height + height + i,
                    )
                ).save(path / f"songthumb2/{i+1:02}_{j+1:02}.png")

elif sys.argv[1] == "black":
    black = [
        (j.filename, k)
        for j in [Image.open(i) for i in (path / "thumb2").iterdir()]
        if (k := j.getcolors()) and len(k) < 5
    ]
    # print(len(black))
    # print(*[(Path(i[0]).name, i[1]) for i in black],sep="\n")
    for b in black:
        Path(b[0]).unlink()
elif sys.argv[1] == "compare":
    # a=Image.open(path/"songthumb1/07_08.png")
    # b=Image.open(path/"songthumb2/01_07.png")
    # a=Image.open(path/"mvthumb1/01_01.png")
    # b=Image.open(path/"mvthumb2/17_08.png")
    # result = ImageChops.difference(a,b)
    # result.save(path/"_.png")
    # diff = result.getcolors(maxcolors=2048)
    # print(len(diff))
    # print(len([i for i in diff if i[1][0]<50 and i[1][1]<50 and i[1][2]<50]))
    # print(max([i[1][0] for i in diff]),max([i[1][1] for i in diff]),max([i[1][2] for i in diff]),max([i[1][3] for i in diff]))
    # input()
    if arg2 == "mv":
        images1 = [Image.open(i) for i in (path / "mvthumb1").iterdir()]
        images2 = [Image.open(i) for i in (path / "mvthumb2").iterdir()]
        comp, thumb1, thumb2 = "mvcomp", "mvthumb1", "mvthumb2"
    if arg2 == "song":
        images1 = [Image.open(i) for i in (path / "songthumb1").iterdir()]
        images2 = [Image.open(i) for i in (path / "songthumb2").iterdir()]
        comp, thumb1, thumb2 = "songcomp", "songthumb1", "songthumb2"
    result = []
    for img1 in images1:
        # if img1.getcolors(): shutil.copy(img1.filename, path/comp)
        for i, img2 in enumerate(images2):
            diff = ImageChops.difference(img1, img2).getcolors(maxcolors=2048)
            if diff:
                maxR, maxG, maxB = (
                    max([i[1][0] for i in diff]),
                    max([i[1][1] for i in diff]),
                    max([i[1][2] for i in diff]),
                )
            if diff and maxR < 100 and maxG < 100 and maxB < 100:
                # print(len(diff))
                stem = (path1 := Path(img1.filename)).stem
                shutil.copy(img1.filename, path / comp / f"{stem}_1.png")
                shutil.copy(img2.filename, path / comp / f"{stem}_2.png")
                result.append((path1, Path(img2.filename)))
                images2.remove(images2[i])
                break
    # print(*[(i[0].name, i[1].name) for i in result],sep="\n")
    print(len(result))
    new = set((path / thumb2).iterdir()) - set([i[1] for i in result])
    rest = set((path / thumb1).iterdir()) - set([i[0] for i in result])
    print(len(new), rest)
    (path / comp / "new").mkdir(exist_ok=True)
    for n in new:
        shutil.copy(n, path / comp / "new")
elif sys.argv[1] == "song_pic":
    path = Path(
        "D:/SteamLibrary/steamapps/common/DJMAX RESPECT V/DJMAX RESPECT V_Data/StreamingAssets/Packs/assets/bundledatas/cover"
    )
    # fmt: off
    songDict = {
        "2nite":              "2Nite",
        "access":             "Access",
        "ad2222":             "AD2222",
        "adlong":             "AD2222 ~Extended Mix~",
        "ai":                 "A.I",
        "airwave":            "Airwave",
        "airwavefull":        "Airwave ~Extended Mix~",
        "alice":              "ALiCE",
        "alie":               "A Lie",
        "aliermx":            "A Lie ~Deep Inside Mix~",
        "allianceempire":     "???????????? ?????????",
        "alone":              "Alone (Marshmellow)",
        "alone2":             "Alone (Nauts)",
        "always":             "Always",
        "analys":             "ANALYS",
        "angel":              "Angel",
        "angelic":            "Angelic Sphere",
        "anima":              "ANiMA",
        "another":            "Another DAY",
        "apparition":         "Apparition",
        "arcadelove":         "Arcade Love (feat. KNVWN)",
        "area7":              "Area 7",
        "armoredphantom":     "Armored Phantom",
        "astro":              "Astro Fight",
        "attack":             "Attack",
        "aurora":             "Aurora Borealis",
        "axion":              "AXION",
        "bamboo":             "Bamboo on Bamboo",
        "baram":              "???????????? ?????????",
        "baram2":             "????????? ??????",
        "baramlive":          "???????????? ????????? ~Live Mix~",
        "barbarous":          "Barbarous Funera",
        "bdvoid":             "Void",
        "beatudown":          "Beat U Down",
        "beautifulday":       "Beautiful Day",
        "becomemy":           "Become Myself",
        "beeutiful":          "BEE-U-TIFUL",
        "beyondthe":          "Beyond the Future",
        "beyondyourself":     "Beyond Yourself",
        "binaryworld":        "Binary World",
        "blackcat":           "BlackCat",
        "blackgold":          "BLACK GOLD",
        "blackswan":          "Black Swan",
        "bleed":              "Bleed",
        "blythe":             "BlythE",
        "boom":               "Boom!",
        "brain":              "Brain Storm",
        "brandnew":           "Brandnew Days",
        "brave":              "Brave it Out",
        "break":              "Break!",
        "breakaspell":        "Break a Spell",
        "brightdream":        "Bright Dream",
        "bulletwanted":       "Bullet, Wanted!",
        "burnitdown":         "Burn it Down",
        "buyeo":              "????????? ~Blosso Remix~",
        "byebyermx":          "Bye Bye Love ~Nu Jazz Mix~",
        "byelove":            "Bye Bye Love",
        "canwetalk":          "Can We Talk",
        "catchme":            "Catch Me",
        "catchyou":           "Catch You",
        "chainof":            "Chain of Gravity",
        "chemical":           "Chemical Slave",
        "cherokee":           "Cherokee",
        "childof":            "Child of Night",
        "chrono":             "Chrono Breakers",
        "chrysanthemum":      "Chrysanthemum",
        "clearbluesky":       "The Clear Blue Sky",
        "closer":             "Closer",
        "cnp":                "CnP",
        "coastaltempo":       "Coastal Tempo",
        "cockedpistol":       "Cocked Pistol",
        "codenamezero":       "CODE NAME : ZERO",
        "collapsed":          "Tayberrs - Collapsed Paradise",
        "color":              "Color",
        "coloursofsorrow":    "Colours of Sorrow",
        "comet":              "??????",
        "cometome":           "????????? ???",
        "conflict":           "conflict",
        "cosmicfantastic":    "Cosmic Fantastic Lovesong",
        "cozyquilt":          "Cozy Quilt",
        "creator":            "Creator",
        "crommcruaich":       "????????? ??? : ????????? ????????????",
        "cselevator":         "Cosmic Elevator",
        "cyberozar":          "Cyberozar",
        "cyphergate":         "Cypher Gate",
        "d2":                 "D2",
        "darkenvy":           "DARK ENVY",
        "darkprism":          "Dark Prism",
        "daydream":           "Daydream",
        "dearmylady":         "Dear my Lady",
        "desperado":          "Desperado",
        "desperadormx1":      "Desperado ~Nu Skool Mix~",
        "divine":             "DIVINE SERVICE",
        "djmax":              "DJMAX",
        "doit":               "Do it",
        "dontdie":            "Don't Die",
        "dotd":               "Dance of the Dead",
        "doyouwantit":        "Do you want it",
        "dreadnought":        "Dreadnought",
        "dream":              "Dream",
        "dreamagain":         "Dream Again",
        "dreamit":            "Dream it",
        "dreamofwinds":       "Dream of Winds",
        "dreamofyou":         "Dream of You",
        "dualstrikers":       "Dual Strikers",
        "egg":                "EGG",
        "egglong":            "EGG ~Extended Mix~",
        "elastic":            "Elastic STAR",
        "electronics":        "Electronics",
        "ember":              "EMber",
        "emblem":             "Emblem",
        "endof":              "End of the Moonlight",
        "endofmyth":          "End of Mythology",
        "enemyrmx1":          "Enemy Storm ~Dark Jungle Mix~",
        "enemystorm":         "Enemy Storm",
        "entrance":           "Entrance",
        "eternalfantasy":     "Eternal Fantasy ~????????? ???~",
        "eternalmemory":      "Eternal Memory ~????????? ???~",
        "everything":         "Everything",
        "extreme":            "Extreme Z4",
        "fallenangel":        "Fallen Angel",
        "falling":            "Fallin' in LUV",
        "fallinlove":         "FALLING IN LOVE",
        "fancynight":         "Fancy Night",
        "fareast":            "Far East Princess",
        "fate":               "Fate",
        "fear":               "FEAR",
        "feel":               "Feel",
        "feelmabeat":         "Feel Ma Beat",
        "fentanest":          "Fentanest",
        "fermion":            "Fermion",
        "fevergj":            "Fever GJ",
        "feverpitch":         "Fever Pitch Girl",
        "fightnight":         "FIGHT NIGHT (feat. Calyae)",
        "finaldance":         "????????????",
        "firstkiss":          "First Kiss",
        "flea":               "Flea",
        "flowering":          "??????????????????",
        "floweringfull":      "?????????????????? ~Original Ver.~",
        "flyaway":            "Fly Away",
        "forever":            "??????",
        "forgotten":          "Forgotten",
        "forseasons":         "For Seasons",
        "forseasonsrmx":      "For Seasons ~Air Guitar Mix~",
        "freedom":            "Freedom",
        "frontline":          "Frontline",
        "ftr":                "FTR",
        "funkychups":         "Funky Chups",
        "fury":               "Fury",
        "futurism":           "Futurism",
        "garakuta":           "Garakuta Doll Play",
        "gcaxelration":       "HB-axeleration",
        "gcblackmind":        "Black MInD",
        "gcgnbl":             "Good Night, Bad Luck.",
        "gcgotmore":          "Got more raves?",
        "gcgrpray":           "Groove Prayer",
        "gcmarryme":          "Marry me, Nightmare",
        "gcouroboros":        "ouroboros -twin stroke of the end-",
        "gcoverthenight":     "OVER THE NIGHT",
        "gcsatisfiction":     "Satisfiction",
        "gcwarrior":          "Warrior",
        "getdown":            "Get Down",
        "getjinxed":          "Get Jinxed",
        "getontop":           "Get on Top",
        "getout":             "GET OUT",
        "getoutrmx":          "GET OUT ~Hip Noodle Mix~",
        "ghost":              "??????",
        "ghostvoices":        "Ghost Voices",
        "giveme5":            "Give Me 5",
        "glorydaykr":         "glory day",
        "gloryjhs":           "glory day -JHS Remix-",
        "gloryminto":         "glory day (Mintorment Remix)",
        "gobaek1":            "??????, ???, ??????",
        "gobaek2":            "??????, ???, ?????? part.2",
        "goneastray":         "Gone Astray",
        "gongseong":          "????????? ~Pierre Blanche, Yonce Remix~",
        "goodbye":            "Good Bye",
        "grandma":            "????????? ???????????? ???????????? ??? ??????",
        "graveconsequence":   "Grave Consequence",
        "gridsystem":         "Grid System",
        "groovinup":          "Groovin Up",
        "hamsin":             "HAMSIN",
        "hanzup":             "Hanz up!",
        "heartofwitch":       "Heart of Witch",
        "heavenly":           "Heavenly",
        "helix":              "HELIX",
        "hellopinky":         "Hello Pinky",
        "hereinthe":          "Here in the Moment",
        "hereinthefull":      "Here in the Moment ~Extended Mix~",
        "hexad":              "HEXAD",
        "higher":             "Higher",
        "holyorders":         "Holy Orders (Be Just Or Be Dead)",
        "honeymoon":          "Honeymoon",
        "id":                 "Imaginary dance",
        "if":                 "IF",
        "ikarus":             "For the IKARUS",
        "ikazuchi":           "Ikazuchi",
        "inmydream":          "In my Dream",
        "inmyheart":          "In My Heart",
        "inmyheartrmx":       "In My Heart ~ESTi Remix~",
        "ivgaf":              "I've got a feeling",
        "iwantyou":           "I want You",
        "iwantyourmx":        "I want You ~??????????????? Sunshine~",
        "jbg":                "JBG",
        "jealousy":           "Jealousy",
        "jupiter":            "Jupiter Driving",
        "karma":              "??????",
        "karmafull":          "?????? ~Original Ver.~",
        "kartmega":           "??????????????? Mashup ~Cosmograph Remix~",
        "kartpure":           "??????????????? Mashup ~Pure 100% Remix~",
        "kcb":                "???????????????, ????????????????????????, ??????????????? Main theme ~CHUCK Remix~",
        "kensei":             "Kensei",
        "keystothe":          "Keys to the World",
        "killerbee":          "KILLER BEE",
        "kingdom":            "Kingdom",
        "ksystem":            "Knowledge System",
        "kuda":               "KUDA",
        "kung":               "Kung Brother",
        "kungfu":             "Kung-Fu Rider",
        "l":                  "L",
        "lacamp":             "La Campanella : Nu Rave",
        "lacheln":            "Lacheln, The City of Dreams",
        "ladymade":           "Ladymade Star",
        "landscape":          "Landscape",
        "leaveme":            "Leave me alone",
        "legacy":             "Legacy",
        "lemonade":           "Lemonade",
        "lesparfumsdelamour": "Les Parfums de L'Amour",
        "letsgobaby":         "Let's Go Baby",
        "liar":               "Liar",
        "lifewithu":          "A Life With You",
        "liftyouup":          "Lift You Up",
        "lighthouse":         "Light House",
        "lisrim":             "Lisrim",
        "littleadventurer":   "The Little Adventurer",
        "longvacation":       "Long Vacation",
        "lost":               "Lost n' found",
        "lostserenity":       "Lost Serenity",
        "losttemple":         "Lost Temple",
        "loveis":             "Love is Beautiful",
        "lovelyhands":        "Lovely hands",
        "lovemode":           "Love Mode",
        "loverbs":            "Lover (BS Style)",
        "loverce":            "Lover (CE Style)",
        "lughlamhfada":       "????????? ??? : ??? ?????????",
        "luvflow":            "Luv Flow",
        "luvflowrmx1":        "Luv Flow ~Funky House Mix~",
        "luvistrue":          "Luv is True",
        "mabinogi":           "?????? ????????? ~SiNA Remix~",
        "magnolia":           "Magnolia",
        "maharajah":          "Maharajah -fenomeno edition-",
        "mammal":             "Mammal",
        "maplelogin":         "Start The Adventure ~SOPHI Remix~",
        "marionette":         "Marionette",
        "masai":              "MASAI",
        "masairmx1":          "MASAI ~Electro House Mix~",
        "mellowd":            "Mellow D Fantasy",
        "melody":             "Melody",
        "melonade":           "Melonaid",
        "memoirs":            "Memoirs",
        "memoryofbeach":      "Memory of Beach",
        "memoryofdream":      "?????? ?????? (feat. Jisun)",
        "messitup":           "Mess it Up",
        "midnight":           "Midnight Blood",
        "miles":              "Miles",
        "milles":             "????????? ????????? ??? ~VoidRover Remix~",
        "mindcontrol":        "Mind Control",
        "minimallife":        "Minimal Life",
        "minus3":             "Minus 3",
        "mistyera":           "Misty Er'A",
        "moderato":           "Constant Moderato",
        "monoxide":           "MonoXide",
        "morning":            "????????? ??????",
        "morning2":           "?????????",
        "moveyourself":       "Move Yourself",
        "mulch":              "Mulch",
        "myalias":            "My Alias",
        "myheart":            "My Heart, My Soul",
        "myjealousy":         "My Jealousy",
        "myosotis":           "Myosotis",
        "nanairo":            "NANAIRO",
        "nanorisk":           "NANO RISK",
        "nbgirl":             "NB Girls",
        "nbpower":            "NB POWER",
        "nbranger":           "NB RANGER",
        "nbranger2017":       "NB RANGER - Virgin Force",
        "nbrangernon":        "NB Ranger : Nonstop Remix",
        "nbreturn":           "NB Rangers -Returns-",
        "negative":           "Negative Nature",
        "neoege":             "?????????",
        "neon1989":           "NEON 1989 (ESTi Remix)",
        "neverdie":           "Never Die",
        "neverletyougo":      "Never let you go",
        "nevermind":          "Nevermind",
        "neversay":           "Never Say",
        "newday":             "Now a NEW Day",
        "nightmare":          "Nightmare",
        "ninepointeight":     "Nine Point Eight",
        "novarmx":            "Nova ~Mr.Funky Remix~",
        "obelisque":          "Obelisque",
        "obliterator":        "The Obliterator",
        "oblivion":           "OBLIVION",
        "oblivionrmx":        "OBLIVION ~Rockin' Night Style~",
        "odysseus":           "Odysseus",
        "oldgold":            "Old Gold",
        "on":                 "ON",
        "onethelove":         "One the Love",
        "onlyforyou":         "Only for you",
        "openfire":           "OPEN FIRE",
        "outlaw":             "Out Law",
        "outlawrmx1":         "Out Law : Reborn",
        "outofcont":          "Out of CTRL",
        "overme":             "Over Me",
        "overyourdream":      "Over Your Dream",
        "paraq":              "Para-Q",
        "pdm":                "PDM",
        "phantom":            "Phantom Of Sky",
        "piano":              "????????? ????????? 1???",
        "pitapet":            "?????????",
        "plastic":            "plastic method",
        "playthefuture":      "Play the Future",
        "popstars":           "POP/STARS",
        "putemup":            "Put'Em Up",
        "puzzler":            "Puzzler",
        "quixotic":           "quixotic",
        "rage":               "Rage Of Demon",
        "rainbow":            "Over the Rainbow",
        "raindropflower":     "The Raindrop Flower ~jam-jam Remix~",
        "rainmaker":          "The Rain Maker",
        "raisemeup":          "Raise me up",
        "rayof":              "Ray of Illuminati",
        "raytuning":          "Ray Tuning",
        "readynow":           "Ready Now",
        "realoverdrive":      "Real Over Drive",
        "red":                "RED",
        "redeyes":            "Red Eyes",
        "relationagain":      "Relation Again (ESTi's Remix)",
        "remain":             "Remains Of Doom",
        "remember":           "Remember",
        "rememberme":         "Remember Me",
        "reminiscence":       "Reminiscence",
        "revenge":            "REVENGE",
        "rightback":          "Right Back",
        "rightnow":           "Right Now",
        "risingthesonic":     "Rising The Sonic",
        "roadofdeath":        "Road Of Death",
        "rocka":              "Rocka-a-doodle-doo",
        "rockordie":          "Rock Or Die",
        "rockstar":           "RockSTAR",
        "rolling":            "Rolling On the Duck",
        "royalclown":         "Royal Clown",
        "runaway":            "Runaway",
        "runninggirl":        "Running girl",
        "rutin":              "Ruti'n",
        "rutinrmx":           "Ruti'n (GOTH Wild Electro Remix)",
        "sadmachine":         "Sad Machine",
        "sairai":             "Sairai",
        "savemydream":        "Save My Dream",
        "sayitfrom":          "Say it from your heart",
        "season":             "Season (Warm Mix)",
        "secretdejavu":       "Secret Dejavu",
        "secretworld":        "Secret World",
        "seeker":             "Seeker",
        "seolaim2":           "????????? Part.2",
        "shadowflower":       "Shadow Flower",
        "shootout":           "Shoot out",
        "shoreline":          "Shoreline",
        "showdown":           "Showdown",
        "showtime":           "Showtime",
        "signalize":          "SigNalize",
        "sin":                "SIN",
        "sinrmx":             "SIN ~The Last Scene~",
        "smoky":              "Smoky Quartz",
        "sohappy":            "So Happy",
        "someday":            "Someday",
        "somuch":             "sO mUCH iN LUV",
        "somuchrmx":          "sO mUCH iN LUV ~Melodic Twisted Mix~",
        "sonof":              "SON OF SUN",
        "sonoffull":          "SON OF SUN ~Extended Mix~",
        "soullady":           "????????????",
        "spacech":            "Space Challenger",
        "spaceofsoul":        "Space of Soul",
        "squeeze":            "SQUEEZE",
        "stalker":            "STALKER",
        "starfish":           "StarFish",
        "stay":               "Stay with me",
        "staywithme":         "?????? ~Stay With Me~",
        "stop":               "STOP",
        "streetlight":        "Streetlight",
        "sunnyside":          "Sunny Side",
        "sunnysidermx":       "Sunny Side ~Deepn' Soul Mix~",
        "sunset":             "Sunset Rider",
        "super2011":          "Supersonic 2011",
        "superlovely":        "Super Lovely",
        "supernova":          "Supernova",
        "supersonic":         "SuperSonic",
        "supersonicrmx1":     "SuperSonic ~Mr.Funky Dirty Planet Remix~",
        "sweetdream":         "Sweet Dream",
        "sweetonyou":         "Sweet On You",
        "sweetshining":       "Sweet Shining Shooting Star",
        "syriana":            "Syriana",
        "syrianarmx":         "Syriana ~Blast Wave Mix~",
        "taekwon":            "????????????",
        "talktalk":           "Talk! Talk!",
        "tellme":             "Tell Me",
        "temptation":         "Temptation",
        "thefeeling":         "The Feelings",
        "theguilty":          "The Guilty",
        "thelastdance":       "The Last Dance",
        "theloststory":       "The Lost Story",
        "thenightstage":      "The Night Stage",
        "theone":             "The One",
        "thewheel":           "The wheel to the right",
        "thor":               "Thor",
        "thorlong":           "Thor ~Extended Mix~",
        "tobewithyou":        "?????? ?????????",
        "toktoktok":          "Tok! Tok! Tok!",
        "trip":               "Trip",
        "triplezoe":          "Triple Zoe",
        "trrricksters":       "Trrricksters!!",
        "uad":                "U.A.D",
        "underwater":         "Underwater Castle",
        "undo":               "Undo",
        "unight":             "Urban Night (Electronic Boutique)",
        "universe":           "Enter The Universe",
        "univus":             "U-NIVUS",
        "urbannight":         "Urban Night (hYO)",
        "utopiosphere":       "Utopiosphere",
        "ventilator":         "Ventilator",
        "verticalflo":        "Vertical Floating",
        "ververg":            "Ververg",
        "vilerequiem":        "Vile Requiem",
        "voldenuit":          "v o l d e n u i t",
        "voyage":             "Voyage (makou)",
        "voyage2":            "Voyage (SOPHI)",
        "waitingfor":         "Waiting for the Sun",
        "waitingforme":       "waiting for me",
        "waitingforyou":      "Waiting for you",
        "wannabe":            "Wanna Be Your Lover",
        "warnow":             "It's my war now",
        "watchyour":          "Watch Your Step",
        "wereall":            "We're All Gonna Die",
        "whatami":            "What am I fighting for?",
        "whiteblue":          "WhiteBlue",
        "why":                "WHY",
        "wonderslot777":      "WONDER $LOT 777",
        "wontbackdown":       "Won't Back Down",
        "wtts":               "welcome to the space (feat. Jisun)",
        "xeus":               "Xeus",
        "xlasher":            "XLASHER",
        "yaparty":            "Ya! Party!",
        "ybs":                "Y (BS Style)",
        "yce":                "Y (CE Style)",
        "yellow2":            "Yellowberry -AJ Mix-",
        "ylong":              "Y ~Extended Mix~",
        "yocreo":             "Yo Creo Que Si",
        "yocreormx":          "Yo Creo Que Si ~Live House Version~",
        "yomax":              "Yo! Max!",
        "youandme":           "You & Me",
        "yourown":            "Your Own Miracle",
        "yourownrmx":         "Your Own Miracle ~Disco House Mix~",
        "yoursmile":          "Your Smile",
        "yubikiri":           "YUBIKIRI-GENMAN",
        "zet":                "ZET",
        "zetrmx1":            "ZET ~Mr.Funky Remix~",
        "ztth":               "Zero to the hunnit"
    }
    # fmt: on
    for i in path.iterdir():
        if (name := i.stem.removeprefix("song_pic_f_")[:-3]) in songDict:
            if arg2 == "rename":
                rename = i.stem[:-3].replace(name, songDict[name])
                num = int(i.stem[-2:])
                rename = f"{rename}_{num + 2}"
                i.rename(i.with_stem(rename))
            else:
                i.unlink()
        else:
            print(name)
            i.rename(i.with_stem(i.stem.removeprefix("song_pic_f_")))
    if arg2 == "rename":
        for i in path.iterdir():
            i.rename(i.with_stem(i.stem[:-1]))
