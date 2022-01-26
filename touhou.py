import urllib.request
import requests
import re
import sys
from bs4 import BeautifulSoup 

data1 = []
data2 = []

strDic = {
    "Reimu Hakurei":"하쿠레이 레이무","Marisa Kirisame":"키리사메 마리사",
    "Rumia":"루미아","Daiyousei":"대요정","Cirno":"치르노","Hong Meiling":"홍 메이링","Koakuma":"소악마","Patchouli Knowledge":"파츄리 널릿지","Sakuya Izayoi":"이자요이 사쿠야","Remilia Scarlet":"레밀리아 스칼렛","Flandre Scarlet":"플랑드르 스칼렛",
    "Letty Whiterock":"레티 화이트락","Chen":"첸","Alice Margatroid":"앨리스 마가트로이드","Lily White":"릴리 화이트","Prismriver Sisters":"프리즘리버 자매","Lunasa Prismriver":"루나사 프리즘리버","Merlin Prismriver":"메를랑 프리즘리버","Lyrica Prismriver":"리리카 프리즘리버","Youmu Konpaku":"콘파쿠 요우무","Yuyuko Saigyouji":"사이교우지 유유코","Ran Yakumo":"야쿠모 란","Yukari Yakumo":"야쿠모 유카리",
    "Wriggle Nightbug":"리글 나이트버그","Mystia Lorelei":"미스티아 로렐라이","Keine Kamishirasawa":"카미시라사와 케이네","Tewi Inaba":"이나바 테위","Reisen Udongein Inaba":"레이센 우동게인 이나바","Eirin Yagokoro":"야고코로 에이린","Kaguya Houraisan":"호라이산 카구야","Fujiwara no Mokou":"후지와라노 모코우",
    "Suika Ibuki":"이부키 스이카","Yuka Kazami":"카자미 유카","Aya Shameimaru":"샤메이마루 아야","Medicine Melancholy":"메디슨 멜랑콜리","Komachi Onozuka":"오노즈카 코마치","Shikieiki Yamaxanadu":"시키에이키 야마자나두","Eiki Shiki, Yamaxanadu":"시키에이키 야마자나두","Eiki Shiki":"시키에이키 야마자나두",
    "Shizuha Aki":"아키 시즈하","Minoriko Aki":"아키 미노리코","Hina Kagiyama":"카기야마 히나","Nitori Kawashiro":"카와시로 니토리","Momiji Inubashiri":"이누바시리 모미지","Sanae Kochiya":"코치야 사나에","Kanako Yasaka":"야사카 카나코","Suwako Moriya":"모리야 스와코","Iku Nagae":"나가에 이쿠","Tenshi Hinanawi":"히나나위 텐시",
    "Kisume":"키스메","Yamame Kurodani":"쿠로다니 야마메","Parsee Mizuhashi":"미즈하시 파르시","Yuugi Hoshiguma":"호시구마 유기","Satori Komeiji":"코메이지 사토리","Rin Kaenbyou":"카엔뵤 린","Utsuho Reiuji":"레이우지 우츠호","Koishi Komeiji":"코메이지 코이시",
    "Nazrin":"나즈린","Kogasa Tatara":"타타라 코가사","Ichirin Kumoi":"쿠모이 이치린","Unzan":"운잔","Minamitsu Murasa":"무라사 미나미츠","Shou Toramaru":"토라마루 쇼","Byakuren Hijiri":"히지리 뱌쿠렌","Nue Houjuu":"호쥬 누에","Hatate Himekaidou":"히메카이도 하타테","Sunny Milk":"서니 밀크","Luna Child":"루나 차일드","Star Sapphire":"스타 사파이어","Three Fairies of Light":"서니 밀크 & 루나 차일드 & 스타 사파이어",
    "Kyouko Kasodani":"카소다니 쿄코","Yoshika Miyako":"미야코 요시카","Seiga Kaku":"곽청아","Soga no Tojiko":"소가노 토지코","Mononobe no Futo":"모노노베노 후토","Toyosatomimi no Miko":"토요사토미미노 미코","Mamizou Futatsuiwa":"후타츠이와 마미조","Hata no Kokoro":"하타노 코코로",
    "Wakasagihime":"와카사기히메","Sekibanki":"세키반키","Kagerou Imaizumi":"이마이즈미 카게로","Benben Tsukumo":"츠쿠모 벤벤","Yatsuhashi Tsukumo":"츠쿠모 야츠하시","Seija Kijin":"키진 세이자","Shinmyoumaru Sukuna":"스쿠나 신묘마루","Raiko Horikawa":"호리카와 라이코","Kasen Ibaraki":"이바라키 카센","Usami Sumireko":"우사미 스미레코","Sumireko Usami":"우사미 스미레코",
    "Seiran":"세이란","Ringo":"링고","Doremy Sweet":"도레미 스위트","Sagume Kishin":"키신 사구메","Clownpiece":"클라운피스","Junko":"순호","Hecatia Lapislazuli":"헤카티아 라피스라줄리",
    "Eternity Larva":"이터니티 라바","Nemuno Sakata":"사카타 네무노","Aunn Komano":"코마노 아운","Narumi Yatadera":"야타데라 나루미","Mai Teireida":"테이레이다 마이","Satono Nishida":"니시다 사토노","Okina Matara":"마타라 오키나","Joon Yorigami":"요리가미 조온","Shion Yorigami":"요리가미 시온",
    "Rinnosuke Morichika":"모리치카 린노스케","Hieda no Akyuu":"히에다노 아큐","Kosuzu Motoori":"모토오리 코스즈","Reisen":"레이센","Watatsuki no Toyohime":"와타츠키노 토요히메","Watatsuki no Yorihime":"와타츠키노 요리히메","Renko Usami":"우사미 렌코","Maribel Hearn":"마에리베리 한",
    "Monday":"월요일","Tuesday":"화요일","Wednesday":"수요일","Thursday":"목요일","Friday":"금요일","Saturday":"토요일","Sunday":"일요일","Wrong":"뒷","Nightmare":"악몽"
}

enPrefix = "https://en.touhouwiki.net/wiki"
enSuffix = "Spell_Cards"
enStage = [["Stage_1","Stage_2","Stage_3","Stage_4","Stage_5","Stage_6","Extra","Phantasm","Last_Word","Overdrive",],
            ["Level_1","Level_2","Level_3","Level_4","Level_5","Level_6","Level_7","Level_8","Level_9","Level_10","Level_Ex","Level_11","Level_12","Level_EX","Level_Spoiler"],
            ["Stage_A-1","Stage_A1-2","Stage_A1-3","Stage_A2-2","Stage_A2-3","Stage_B-1","Stage_B1-2","Stage_B1-3","Stage_B2-2","Stage_B2-3","Stage_C-1","Stage_C1-2","Stage_C1-3","Stage_C2-2","Stage_C2-3"],
            ["1st_Day","2nd_Day","3rd_Day","4th_Day","5th_Day","6th_Day","7th_Day","8th_Day","9th_Day","Last_Day"],
            ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Wrong_","Nightmare_","Nightmare_Diary"]
            ]
namuPrefix = "https://namu.wiki/w"
namuSuffix = "스펠카드"
titleDic = {"th06":[["Embodiment_of_Scarlet_Devil","동방홍마향"],
            [["루미아"],["치르노"],["홍 메이링"],["파츄리 널릿지" for i in range(18)],["이자요이 사쿠야"],["이자요이 사쿠야","레밀리아 스칼렛"],["파츄리 널릿지","플랑드르 스칼렛"]],
            [[0],[0],[0],[0,1,2,3,3,0,1,0,2,1,1,0,3,0,0,1,0,1],[0],[1,1],[4,0]]
            ],
          "th07":[["Perfect_Cherry_Blossom","동방요요몽"],
            [["치르노","레티 화이트락"],["첸(동방 프로젝트)"],["앨리스 마가트로이드"],["프리즘리버 자매"],["콘파쿠 요우무"],["콘파쿠 요우무","사이교우지 유유코"],["첸(동방 프로젝트)","야쿠모 란"],["야쿠모 란","야쿠모 유카리"]],
            [[1,0],[0],[0],[0],[0],[1,0],[1,0],[1,0]]
            ],
          "th08":[["Imperishable_Night","동방영야초"],
            [["리글 나이트버그"],["미스티아 로렐라이"],["카미시라사와 케이네"],["하쿠레이 레이무","키리사메 마리사"],["레이센 우동게인 이나바"],["야고코로 에이린","야고코로 에이린","호라이산 카구야"],["카미시라사와 케이네","후지와라노 모코우"],
                ["리글 나이트버그","미스티아 로렐라이","카미시라사와 케이네","레이센 우동게인 이나바","야고코로 에이린","호라이산 카구야","후지와라노 모코우","이나바 테위","카미시라사와 케이네","하쿠레이 레이무","키리사메 마리사","이자요이 사쿠야","콘파쿠 요우무","앨리스 마가트로이드","레밀리아 스칼렛","사이교우지 유유코","야쿠모 유카리"]],
            [[0],[0],[0],[6,8],[0],[0,1,0],[1,0],[1,1,2,1,2,1,1,0,2,7,9,9,8,6,6,5,6]]
            ],
          "th10":[["Mountain_of_Faith","동방풍신록"],
            [["아키 미노리코"],["카기야마 히나"],["카와시로 니토리"],["샤메이마루 아야"],["코치야 사나에"],["야사카 카나코"],["야사카 카나코","모리야 스와코"]],
            [[7,0],[0],[0],[1],[0],[0],[1,0]]
            ],
          "th11":[["Subterranean_Animism","동방지령전"],
            [["쿠로다니 야마메"],["미즈하시 파르시"],["호시구마 유기"],["코메이지 사토리" for i in range(6)],["카엔뵤 린"],["카엔뵤 린","레이우지 우츠호"],["코치야 사나에","코메이지 코이시"]],
            [[7,0],[0],[0],[0,1,2,3,4,5],[0],[1,0],[1,0]]
            ],
          "th12":[["Undefined_Fantastic_Object","동방성련선"],
            [["나즈린"],["타타라 코가사"],["쿠모이 이치린"],["무라사 미나미츠"],["나즈린","토라마루 쇼"],["히지리 뱌쿠렌"],["타타라 코가사","호쥬 누에"]],
            [[0],[0],[0],[0],[1,0],[0],[1,0]]
            ],
          "th12.8":[["Fairy_Wars","요정대전쟁"],
            [["루나 차일드"],["스타 사파이어(동방 프로젝트)","서니 밀크"],["서니 밀크","스타 사파이어(동방 프로젝트)"],["서니 밀크"],["스타 사파이어(동방 프로젝트)","루나 차일드"],["루나 차일드","스타 사파이어(동방 프로젝트)"],["스타 사파이어(동방 프로젝트)"],["서니 밀크","루나 차일드"],["루나 차일드","서니 밀크"]],
            [[5],[6,8],[6,8],[5],[7,8],[6,9],[5],[7,9],[7,9],[19]]
            ],
          "th13":[["Ten_Desires","동방신령묘"],
            [["사이교우지 유유코"],["카소다니 쿄코"],["타타라 코가사","미야코 요시카"],["곽청아"],["모노노베노 후토"],["토요사토미미노 미코"],["호쥬 누에","후타츠이와 마미조"],
                ["사이교우지 유유코","카소다니 쿄코","미야코 요시카","곽청아","모노노베노 후토","토요사토미미노 미코","후타츠이와 마미조"]],
            [[10],[0],[3,0],[0],[8,0],[0],[2,0],[11,1,1,1,9,1,1,1]]
            ],
          "th14":[["Double_Dealing_Character","동방휘침성"],
            [["치르노","와카사기히메"],["세키반키"],["이마이즈미 카게로"],["츠쿠모 벤벤","츠쿠모 야츠하시"],["키진 세이자"],["스쿠나 신묘마루"],["츠쿠모 벤벤","호리카와 라이코"]],
            [[8,0],[0],[0],[0,0],[0],[0],[1,0]]
            ],
          "th15":[["Legacy_of_Lunatic_Kingdom","동방감주전"],
            [["세이란"],["링고(동방 프로젝트)"],["도레미 스위트"],["키신 사구메"],["클라운피스"],["순호"],["도레미 스위트","헤카티아 라피스라줄리","순호","헤카티아 라피스라줄리","순호","헤카티아 라피스라줄리"]],
            [[0],[0],[0],[0],[0],[0],[1,0,1,0,1,0]]
            ],
          "th16":[["Hidden_Star_in_Four_Seasons","동방천공장"],
            [["이터니티 라바"],["사카타 네무노"],["코마노 아운"],["야타데라 나루미"],["테이레이다 마이","니시다 사토노","테이레이다 마이","니시다 사토노","테이레이다 마이"],["마타라 오키나"],["니시다 사토노","마타라 오키나"]],
            [[0],[0],[8,0],[0],[0,0,0,0,0],[0],[1,1]]
            ],
           "th09.5":[["Shoot_the_Bullet","동방문화첩"],
            [["리글 나이트버그","루미아"],["치르노","레티 화이트락"],["앨리스 마가트로이드","카미시라사와 케이네"],["레이센 우동게인 이나바","메디슨 멜랑콜리","이나바 테위"],["홍 메이링","파츄리 널릿지"],["첸(동방 프로젝트)","콘파쿠 요우무"],["이자요이 사쿠야","레밀리아 스칼렛"],["야쿠모 란","사이교우지 유유코"],["야고코로 에이린","호라이산 카구야"],["오노즈카 코마치","시키에이키 야마자나두"],["플랑드르 스칼렛","야쿠모 유카리","후지와라노 모코우","이부키 스이카"]],
            [[2,1],[4,1],[7,3],[3,1,2],[3,8],[2,10],[11,7],[2,6],[3,2],[1,1],[1,7,2,3]],
            [[6,[[2,4],[3,5]]],[6,[[2,4],[3,5]]],[8,[[2,4,6],[1,3,5,7]]],[9,[[3,5,8],[1,4,6],[2,7]]],[8,[[2,4,6],[1,3,5,7]]],[8,[[2,4,6],[1,3,5,7]]],[8,[[2,4,6],[1,3,5,7]]],[8,[[2,4,6],[1,3,5,7]]],[8,[[2,4,6],[1,3,5,7]]],[8,[[2,4,6],[1,3,5,7]]],[8,[[0,1],[2,3],[4,5],[6,7]]]]
            ],
           "th12.5":[["Double_Spoiler","더블 스포일러"],
            [["아키 미노리코"],["미즈하시 파르시","카기야마 히나"],["쿠로다니 야마메","타타라 코가사"],["카와시로 니토리"],["쿠모이 이치린","무라사 미나미츠"],["호시구마 유기","이부키 스이카"],["토라마루 쇼","나즈린"],["카엔뵤 린","레이우지 우츠호"],["코메이지 사토리","코메이지 코이시"],["히나나위 텐시","나가에 이쿠"],["야사카 카나코","모리야 스와코"],["히지리 뱌쿠렌","호쥬 누에"],["하쿠레이 레이무","키리사메 마리사","코치야 사나에"],["샤메이마루 아야"]],
            [[1,8],[1,1],[1,2,8],[2,4],[1,1],[1,8],[1,2],[2,4],[6,1],[3,3],[2,4],[1,1],[17,18,6],[6,6]],
            [[6,[[3,5],[2,4]]],[6,[[2,4],[3,5]]],[8,[[3,6],[1,4,7],[2,5]]],[7,[[2,4,6],[3,5]]],[8,[[2,4,6],[3,5,7]]],[8,[[2,4,6],[3,5,7]]],[7,[[2,4,6],[3,5]]],[8,[[2,4,6],[1,3,5,7]]],[8,[[2,4,6],[1,3,5,7]]],[8,[[0,2,4,6],[1,3,5,7]]],[8,[[2,4,6],[1,3,5,7]]],[8,[[2,4,6],[1,3,5,7]]],[9,[[0,3,6],[1,4,7],[2,5,8]]],[9,[[1,2,3],[5,6,7,8]]]]
            ],
           "th14.3":[["Impossible_Spell_Card","탄막 아마노자쿠"],
            [["와카사기히메","치르노"],["카소다니 쿄코","세키반키"],["이마이즈미 카게로","카미시라사와 케이네","후지와라노 모코우"],["사이교우지 유유코","곽청아","미야코 요시카"],["호리카와 라이코","츠쿠모 야츠하시","츠쿠모 벤벤"],["샤메이마루 아야","카와시로 니토리"],["키리사메 마리사","이자요이 사쿠야","콘파쿠 요우무","코치야 사나에"],["스쿠나 신묘마루","하쿠레이 레이무","후타츠이와 마미조"],["야사카 카나코","모리야 스와코","모노노베노 후토","이부키 스이카"],["히지리 뱌쿠렌","토요사토미미노 미코","히나나위 텐시","레밀리아 스칼렛","야쿠모 유카리"]],
            [[1,9],[2,1],[1,4,3],[12,2,2],[1,2,2],[7,7,8,5],[26,16,15,8],[1,26,6],[3,5,7,9],[7,7,4,11,12]],
            [[6,[[1,3,5],[2,4]]],[6,[[0,2,4],[1,3,5]]],[7,[[1,4],[2,5],[3,6]]],[7,[[2,5],[1,4,6],[3]]],[8,[[3,6],[1,4,7],[2,5]]],[8,[[1,7],[2,6],[3,5],[4]]],[8,[[0,4],[1,5],[2,6],[3,7]]],[7,[[3,6],[1,4],[2,5]]],[8,[[0,4],[1,5],[2,6],[3,7]]],[10,[[0,5],[1,6],[2,7],[3,8],[4,9]]]]
            ],
           "th16.5":[["Violet_Detector","비봉 나이트메어 다이어리"],
            [[""],["세이란","링고(동방 프로젝트)"],["이터니티 라바"],["야타데라 나루미"],["사카타 네무노"],["코마노 아운"],[""],["","세이란","링고(동방 프로젝트)","이터니티 라바","야타데라 나루미","사카타 네무노","코마노 아운"],["클라운피스"],["키신 사구메"],["테이레이다 마이","니시다 사토노"],["헤카티아 라피스라줄리"],["순호"],["마타라 오키나"],["레밀리아 스칼렛","플랑드르 스칼렛","히지리 뱌쿠렌"],["사이교우지 유유코","시키에이키 야마자나두","야사카 카나코"],["야고코로 에이린","호라이산 카구야","히나나위 텐시"],["코메이지 사토리","레이우지 우츠호","코메이지 코이시"],["후타츠이와 마미조","호쥬 누에","호리카와 라이코"],["이부키 스이카","후지와라노 모코우","순호"],["마타라 오키나","야쿠모 유카리","하쿠레이 레이무"],["도레미 스위트","우사미 스미레코"]],
            [[-1],[1,1],[1],[1],[1],[1],[-1],[-1,1,1,1,1,1,1],[1],[1],[2,2],[1],[2],[2],[12,2,18],[13,2,4],[4,3,10],[7,5,15],[16,3,2],[10,14,2],[2,18,40],[7,10]],
            [[2,[[0]]],[4,[[0,2],[1,3]]],[3,[[1,2]]],[4,[[1,2,3]]],[3,[[1,2]]],[3,[[1,2]]],[1,[[0]]],[7,[[0],[1],[2],[3],[4],[5],[6]]],[4,[[1,2,3]]],[4,[[1,2,3]]],[6,[[1,3],[2,4]]],[5,[[0,1,2,3,4]]],[5,[[1,2,3,4]]],[6,[[0,1,2,3,4]]],[6,[[0,2,4],[3,5],[1]]],[6,[[0,2,4],[3,5],[1]]],[6,[[0,2,4],[3,5],[1]]],[6,[[0,2,4],[3,5],[1]]],[6,[[0,2,4],[3,5],[1]]],[6,[[0,2,4],[3,5],[1]]],[6,[[0,2,4],[3,5],[1]]],[4,[[0],[1,2]]]]
            ]
        }
        
def isRegular(title):
    if title != "th09.5" and title != "th12.5" and title != "th14.3" and title != "th16.5":
        return True
    else:
        return False

def entouhou():
    urlList = []
    if title == "th09.5":
        for i in range(11):
            urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[1][i]))
    elif title == "th12.5":
        for i in range(10):
            urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[1][i]))
        for i in range(11,15):
            urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[1][i]))
    elif title == "th12.8":
        for i in range(15):
            urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[2][i]))
        urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[0][6]))
    elif title == "th14.3":
        for i in range(10):
            urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[3][i]))
    elif title == "th16.5":
        for i in range(7):
            urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[4][i]))
        for i in range(7):
            urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[4][7]+enStage[4][i]))
        for i in range(7):
            urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[4][8]+enStage[4][i]))
        urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[4][9]))
    else:
        for i in range(7):
            urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[0][i]))
        if title == "th07":
            urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[0][7]))
        elif title == "th08":
            urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[0][8]))
            urlList[3]+="A"
            urlList.insert(4, "%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, "Stage_4B"))
            urlList[6]+="A"
            urlList.insert(7, "%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, "Stage_6B"))
        elif title == "th13":
            urlList.append("%s/%s/%s/%s" %(enPrefix, titleDic[title][0][0], enSuffix, enStage[0][9]))  

    p1 = re.compile('[a-zA-Z-, ()/]+')
    p2 = re.compile('(Easy|Normal|Hard|Lunatic|Extra|Phantasm|Last Word|Overdrive)')
        
    for url in urlList:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        divs = soup.find_all('div', { 'class': 'scwrapper' })

        for div in divs:
            contents = div.find_all('div', { 'class': 'sccontent' })
            numlabel = div.find('div', { 'class': 'sclabel' })
            num = numlabel.text[11:]
            num = num.replace("??", "SPOILER")
            if isRegular(title):
                if title == "th06":
                    num = "%02d" % int(num)
                else:
                    num = "%03d" % int(num)
                num = "No. " + num
            elif title == "th16.5":
                num = num.replace("Nightmare Diary", "나이트메어 다이어리")
                for item in strDic:
                    num = num.replace(item, strDic[item])

            if title == "th14.3":
                name = contents[1].text
                label = str(contents[2])
            else:
                name = contents[0].text
                label = str(contents[1])

            name = name[name.find('」')+1:]
            p3 = re.split('\[[0-9]+\]', name)
            tmp=""
            for i in p3: tmp += i
            name = tmp
            
            label = re.compile('>.*?<').findall(label)
            owner = []
            
            for i in label:
                if len(i) > 2:
                    owner.append(i[1:len(i)-1])
            diff = owner.pop()

            tmp = ""
            for i in owner: tmp += i
            owner = tmp

            if '|' in owner:
                owner = owner[owner.find('|')+1:]
                        
            for item in strDic:
                owner = owner.replace(item, strDic[item])
            owner = owner.replace("&amp;","&")
            owner = owner.replace("and","&")
            
            diff = diff[diff.find('—')+2:]
            if title == "th06":
                diff = p1.findall(diff)
                tmp=""
                for i in diff: tmp += i
                diff = tmp
            else:
                diff = p2.search(diff)
                if diff != None: diff = diff.group(0)
                else: diff = ""
            
            data1.append([num, name, diff, owner])
            if debug: print(num+"\n"+name+"\n"+diff+"\n"+owner+"\n")

def tdSave(td):
    spell = td.text
    if spell != "없음":
        span = 1
        if title != "th06" and td.get('colspan'):
            span = int(td.get('colspan'))
        
        if debug: print(td)
        for i in range(span):
            split = spell.find('」')
            jp=spell[:split+1]
            kr=spell[split+1:]
            data2.append([jp,kr])
                
        
def namu():
    urlList = []
    tableList = titleDic[title][2]
    regular = isRegular(title)

    for stage in range(len(titleDic[title][1])):
        urlList.append([])
        for n in range(len(titleDic[title][1][stage])):
            if title == "th12.8":
                urlList[stage].append("%s/%s" %(namuPrefix, titleDic[title][1][stage][n]))
            else:
                urlList[stage].append("%s/%s/%s" %(namuPrefix, titleDic[title][1][stage][n], namuSuffix))
    
    if title == "th10":
        urlList[0].insert(0, "%s/%s" %(namuPrefix, "아키 시즈하"))
    elif title == "th11":
        urlList[0].insert(0, "%s/%s" %(namuPrefix, "키스메"))
    elif title == "th13":
        urlList[4].insert(0, "%s/%s" %(namuPrefix, "소가노 토지코"))
        urlList[7].insert(4, "%s/%s" %(namuPrefix, "소가노 토지코"))
    elif title == "th16":
        urlList[2].insert(0, "%s/%s" %(namuPrefix, "릴리 화이트(동방 프로젝트)"))
    elif title == "th12.8":
        urlList.append(["%s/%s/%s" %(namuPrefix, "키리사메 마리사", namuSuffix)])
    elif title == "th12.5":
        urlList[0].append("%s/%s" %(namuPrefix, "아키 시즈하"))
        urlList[2].append("%s/%s" %(namuPrefix, "키스메"))
        urlList[3].append("%s/%s" %(namuPrefix, "이누바시리 모미지"))
        urlList[13].insert(0, "%s/%s" %(namuPrefix, "히메카이도 하타테"))
    elif title == "th14.3":
        urlList[5].insert(1, "%s/%s" %(namuPrefix, "히메카이도 하타테"))
        urlList[5].append("%s/%s" %(namuPrefix, "이누바시리 모미지"))

    for stage in range(len(urlList)):
        if not regular:
            tmpList = ["" for i in range(titleDic[title][3][stage][0])]

        for n in range(len(urlList[stage])):
            response = requests.get(urlList[stage][n])
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table', { 'class': 'wiki-table' })
            if tableList[stage][n] != -1:
                table = tables[tableList[stage][n]]
            else:
                continue
            trs = table.find_all('tr')
            trs = trs[1:]
            
            if title == "th06" and stage == 3:
                if n == 0: tr = trs[0]; td = tr.find_all('td')[1]
                elif n == 1: tr = trs[0]; td = tr.find_all('td')[1]
                elif n == 2: tr = trs[0]; td = tr.find_all('td')[1]
                elif n == 3: tr = trs[0]; td = tr.find_all('td')[1]
                elif n == 4: tr = trs[1]; td = tr.find_all('td')[2]
                elif n == 5: tr = trs[0]; td = tr.find_all('td')[2]
                elif n == 6: tr = trs[1]; td = tr.find_all('td')[2]
                elif n == 7: tr = trs[1]; td = tr.find_all('td')[2]
                elif n == 8: tr = trs[1]; td = tr.find_all('td')[3]
                elif n == 9: tr = trs[0]; td = tr.find_all('td')[2]
                elif n == 10: tr = trs[1]; td = tr.find_all('td')[3]
                elif n == 11: tr = trs[1]; td = tr.find_all('td')[3]
                elif n == 12: tr = trs[1]; td = tr.find_all('td')[3]
                elif n == 13: tr = trs[1]; td = tr.find_all('td')[1]
                elif n == 14: tr = trs[4]; td = tr.find_all('td')[2]
                elif n == 15: tr = trs[2]; td = tr.find_all('td')[2]
                elif n == 16: tr = trs[3]; td = tr.find_all('td')[2]
                elif n == 17: tr = trs[4]; td = tr.find_all('td')[2]
                tdSave(td)
            elif title == "th06" and stage == 4:
                tr = trs[0]
                tds = tr.find_all('td')
                tdSave(tds[1])
                tdSave(tds[2])
                for i in range(1,3):
                    for j in range(1,4):
                        tr = trs[j]
                        tds = tr.find_all('td')
                        tdSave(tds[i])
            elif title == "th06" and stage == 5 and n == 1:
                for i in range(1,3):
                    for j in range(0,5):
                        tr = trs[j]
                        tds = tr.find_all('td')
                        tdSave(tds[i])
            else:
                if title == "th08" and stage == 3:
                    trs = trs[1:3] + trs[4:8]
                elif title == "th08" and stage == 7:
                    if n == 2: trs = [trs[0]]
                    elif n== 8: trs = [trs[1]]
                elif title == "th11" and stage ==3 and n >=1:
                    trs = trs[1:]
                elif title == "th15" and stage == 6:
                    if n == 1: trs = trs[:3]
                    elif n == 2: trs = [trs[0]]
                    elif n == 3: trs = trs[3:6]
                    elif n == 4: trs = [trs[1]]
                    elif n == 5: trs = trs[6:]
                elif title == "th16" and stage == 4:
                    if n == 0 or n == 1: trs = [trs[0]]
                    elif n == 2 or n== 3: trs = [trs[1]]
                    else: trs = trs[2:]
                elif (title == "th14.3" and stage == 2 and n == 0) or \
                    (title == "th14.3" and stage == 3 and n == 0) or \
                    (title == "th14.3" and stage == 4 and n == 0) or \
                    (title == "th14.3" and stage == 4 and n == 1) or \
                    (title == "th14.3" and stage == 7 and n == 0) or \
                    (title == "th14.3" and stage == 7 and n == 2):
                    trs = trs[1:]
                elif (title == "th14.3" and stage == 4 and n == 2):
                    trs = trs[:2]
                elif (title == "th16.5" and stage in range(1,6)):
                    trs = trs[:len(trs)-1]
                elif (title == "th16.5" and stage == 7):
                    trs = [trs[len(trs)-1]]
                elif (title == "th16.5" and (stage == 11 or stage == 13)):
                    trs = trs[:5]
                elif (title == "th16.5" and stage == 12):
                    trs = trs[:4]
                elif (title == "th16.5" and stage == 19 and n == 2):
                    trs = trs[4:]
                elif (title == "th16.5" and stage == 20 and n == 0):
                    trs = trs[5:]
                elif (title == "th16.5" and stage == 20 and n == 1):
                    trs = trs[:3]

                if title == "th16.5" and (stage in range(14,21) and n == 1):
                    trs = trs[1:]
                elif title == "th16.5" and (stage in range(14,21) and n == 2):
                    trs = [trs[0]]

                for tr in range(len(trs)):
                    tds = trs[tr].find_all('td')
                    if title == "th08" and stage == 7:
                        tds = [tds[0]]
                    elif ((title == "th06" or title == "th07") and stage >= 6) or \
                        (title == "th11" and stage == 6) or \
                        (title == "th16" and stage == 5 and tr >= 6):
                        tds = [tds[1]]
                    elif title == "th14.3":
                        tds = [tds[2]]
                    elif (title == "th07" and (stage == 3 and tr == 1)) or \
                        (title == "th08" and (stage == 5 and tr == 5 and n==2)) or \
                        (title == "th16" and (stage == 5 and tr == 5)):
                        tds = tds[2:len(tds)-1]
                    else:
                        tds = tds[1:len(tds)-1]
                        
                    for td in tds:
                        if not regular:
                            tmpList[titleDic[title][3][stage][1][n][tr]] = td
                        else:
                            tdSave(td)
        
        if not regular:
            for td in tmpList:
                if td == "": data2.append(["",""])
                else: tdSave(td)
            
def printData():
    print(titleDic[title][0][1]+"의 스펠카드 목록")
    print("="*100)
    for i in range(len(data1)):
        print(data1[i][0])
        print(data2[i][0])
        print(data2[i][1])
        print(data1[i][1])
        print(data1[i][2])
        print(data1[i][3])
        print("="*100)
        
def printList(lists):
    for i in lists: print(i)

def spellOut():
    entouhou()
    namu()
    printData()
    #printList(data1)
    #printList(data2)

#th = ["th06","th07","th08","th10","th11","th12","th13","th14","th15","th16","th09.5","th12.5","th12.8","th14.3"]
# for i in th:
#     title = i
#     spellOut()
#     data1.clear()
#     data2.clear()

def namuOut(title):
    regular = isRegular(title)
    title=title.replace('t','T')
    title=title.replace('.','')
    with open ("D:/Touhou/Spell/%s/%s.txt" %(title, title),encoding="utf-8") as f1:
        lines1 = f1.readlines()    

    for i in range(len(lines1)):
        if i%7 == 0: num = lines1[i].strip()
        elif i%7 == 1: jp = lines1[i].strip()
        elif i%7 == 2:
            kr = lines1[i].strip()
            if kr:
                if kr[0] == '「': kr = kr.replace('「', "\"")
                else: kr = kr.replace('「', " \"")
                kr = kr.replace('」', "\"")
        elif i%7 == 3: en = lines1[i].strip()
        elif i%7 == 4:
            diff = lines1[i].strip()
            if diff == "Easy": color = "<#99FF99>"
            elif diff == "Normal": color = "<#9999FF>"
            elif diff == "Hard": color = "<#FF9999>"
            elif diff == "Lunatic": color = "<#FF99FF>"
            elif diff == "Extra": color = "<#FFFF99>"
            else: color = "<#99FFFF>"
        elif i%7 == 5: owner = lines1[i].strip()
        else:
            if not regular:
                scNum = int(i/7) + 1
                if title == "Th125" or title == "Th165":
                    scNum = "%03d" % int(scNum)
                else:
                    scNum = "%02d" % int(scNum)
                print("||<|5>[[파일:%sSC%s.jpg|width=300]]||\'\'\'%s\'\'\'||%s[br][br]%s[br][br]%s||" %(title, scNum, num, jp, kr, en))
                print("||소유자||[[%s]]||" % owner)
            else:
                print("||<|5>[[파일:%sSC%s.jpg|width=300]]||\'\'\'%s\'\'\'||%s[br][br]%s[br][br]%s||" %(title, num[4:], num, jp, kr, en))
                print("||등장 난이도||%s%s||" % (color,diff))

            if title == "Th08" or title == "Th095" or title == "Th165":
                print("||코멘트|| ||")
            elif title == "Th143":
                print("||장면 제목|| ||")
            elif title == "Th125":
                print("||아야의 코멘트|| ||")
                print("||하타테의 코멘트|| ||")
            print("||주석|| ||\n")

debug = False

if __name__ == "__main__":
    print("[th06, th07, th08, th10, th11, th12, th13, th14, th15, th16, th09.5, th12.5, th12.8, th14.3, th16.5]")
    title = input("코드를 입력하세요: ")
    print("데이터 수집중...\n")
    spellOut()
    #namuOut(title)