import discord
from discord.ext import commands
from discord.utils import get
import datetime
import time,datetime
from datetime import datetime,timezone,timedelta
import requests
import json
import random

# 時間 船長 船員 戰利品... 賣出前 賣出後


#     cpulimit --pid 2902 --limit 90      
#     nohup python testbot.py &>myout.txt &      
#     nohup cpulimit --pid 2902 --limit 90 &>myout.txt &  
#     nohup python testbot.py > nohup.log 2>&1 &    

#       nohup python -u bot.py > bot.out 2> bot.err < /dev/null &
#       nohup cpulimit --pid 1841 --limit 90 > cpulimitlog.out 2> cpulimitlog.err < /dev/null &

google_db_url="https://script.google.com/macros/s/{{api}}"
passwd = {{passwd}}
TOKEN = {{TOKEN}}


week_day_dict = {
    0 : '星期一',
    1 : '星期二',
    2 : '星期三',
    3 : '星期四',
    4 : '星期五',
    5 : '星期六',
    6 : '星期日',
}

# Trophydict = {
#     '金塊1000g' :0 ,
#     '怪獸內丹'  :0 ,
#     '赫卡魯的突起':0,
#     '漂流追蹤者的外皮'  :0,
#     '幽冥鐵牙的顎骨' :0 ,
#     '納恩薩克的角破片'  :0 ,
#     '坎迪杜姆的甲殼':0,
#     '古德蒙特海賊團的金幣'  :0
# }

Trophydict_2_ch = {
    '<:1000g:476274938395885568>' : '金塊1000g',
    '<:blue:476262599177011240>' : '怪獸內丹',
    '<:red:476262607335063552>' : '赫卡魯的突起',
    '<:skin:476262626519941120>' : '漂流追蹤者的外皮',
    '<:tooth:476262644287012865>' : '幽冥鐵牙的顎骨',
    '<:nashark:476262658669281294>' : '納恩薩克的角破片',
    '<:Carapace:476262683189182464>' : '坎迪杜姆的甲殼',
    '<:coin:476262700532367371>' : '古德蒙特海賊團的金幣'
}

# Trophydict_2_eng = {
#     '金塊1000g' :'<:1000g:476274938395885568>' ,
#     '怪獸內丹'  :'<:blue:476262599177011240>' ,
#     '赫卡魯的突起':'<:red:476262607335063552>',
#     '漂流追蹤者的外皮'  :'<:skin:476262626519941120>',
#     '幽冥鐵牙的顎骨' :'<:tooth:476262644287012865>' ,
#     '納恩薩克的角破片'  :'<:nashark:476262658669281294>' ,
#     '坎迪杜姆的甲殼':'<:Carapace:476262683189182464>',
#     '古德蒙特海賊團的金幣'  :'<:coin:476262700532367371>'
# }

def whatdayistoday(n): 
    """n=0回傳年月日&星期幾，n=其他數字，回傳星期幾""" 
    dt = datetime.utcnow()
    dt = dt.replace(tzinfo=timezone.utc)
    tzutc_8 = timezone(timedelta(hours=8))
    local_dt = dt.astimezone(tzutc_8)
    today = (str(local_dt)[:10])#今天幾月幾號  '2018-08-08'
    
    day = local_dt.weekday()
    if (n == 0):
        return (today + week_day_dict[day]) # week_day_dict[day] 星期三
    return (week_day_dict[day]) #  星期三


def addTrophy(time,username,Trophydict,before,after,username2 = "NULL"):  #登記戰利品
    """登記戰利品"""
    payload = {'passwd': passwd ,'method': 'write','time': time ,'username': username,'username2': username2 ,'before':before,'after':after}
    #無須擔心玩家家門="NULL"，因為黑沙不准許
    payload.update(Trophydict)
    print(payload)
    r = requests.post(google_db_url, params=payload)
# 時間 船長 船員 戰利品... 賣出前 賣出後

def user_total_money(username):

    payload = {'passwd': passwd ,'method': 'read','username': username}
    r = requests.get(google_db_url, params=payload)
    # allmoney = json.loads(r.text)
    # print(r.text)
    return r.text

description = '''Bot in Python'''
bot = commands.Bot(command_prefix='$', description=description)

print (whatdayistoday(0)) #2018-08-08 星期三
print("hi 你好 本呆呆機器人將為您服務")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_resumed():
    print('reconnected')



@bot.command(pass_context=True)
async def hello(ctx):
    """Says world"""    
    await bot.say('hi {}'.format(ctx.message.author.display_name))    
    # await bot.say('hi {}'.format(ctx.message.channel))    #hi bot-test測試頻道


@bot.command(pass_context=True)
async def game(ctx):
    """game"""    
    await bot.say('請輸入1~10的數字')   
    def guess_check(m):
        # print(m)
        return m.content.isdigit()
    guess = await bot.wait_for_message(timeout=5.0, author=ctx.message.author, check=guess_check)
    answer = random.randint(1, 10)
    if guess is None:
        await bot.say('必須輸入1~10的數字喔，別問為什麼，我只是在測試怎麼讓bot限定時間內回應')
        return
    if int(guess.content) == answer:
        await bot.say('你猜對了')
    else:
        await bot.say("猜錯了喔 正確答案是 "+str(answer))

@bot.command(pass_context=True)
async def total(ctx):
    """查詢玩家一個禮拜以來的總收入"""    
    # await bot.say('hi {}'.format(ctx.message.author.display_name))
    display_name = str(ctx.message.author.display_name)
    total_money = int(user_total_money(display_name))

    if (total_money <= 0):
        print(display_name+" 查詢收入失敗，因為當周尚未有收入")
        await bot.say("還沒有收入喔")
    elif (total_money > 0):
        # print(display_name+" 的收入是:"+str(total_money))
        # "{:,}".format(99999999)
        print(display_name+" 的收入是:"+"{:,}".format(total_money))
        await bot.say("hi "+display_name+" 你這禮拜目前的總收入是:"+"{:,}".format(total_money))

    if ( total_money > 1000000000  ):
        await bot.say("挖! 恭喜打完10e囉(可以剩下的可以分給我了3Q")
    elif ( total_money > 850000000):
        await bot.say("加油喔 只差一點點快要打完了")
    elif ( total_money > 500000000):
        await bot.say("耶 還剩下不到一半了 ")

@bot.command(pass_context=True)
async def eat(ctx,*args):
    bot_message_channel = str(ctx.message.channel) #判斷是否在指定伺服器頻道裡面
    display_name = str(ctx.message.author.display_name)

    if( bot_message_channel == "戰利品上傳區new") or (bot_message_channel == "bot-test測試區-已不使用") or (bot_message_channel == "test"):   #判斷是否在指定伺服器頻道裡面
        print(display_name)
        print('{} arguments: {}'.format(len(args), ', '.join(args)))
        await bot.say('{} arguments: {}'.format(len(args), ', '.join(args)))
    else:
        await bot.say('不好意思喔 這裡不是授權的頻道')
        print('這裡不是授權的頻道',str(ctx.message.channel))
        return

    if(len(args)%2 != 0):
        print("輸入錯誤 資料不對襯")
        await bot.say("輸入錯誤 別亂餵我好嗎?\n\n\n(注意記得表情符號後面要加空白再加數量或家門名喔\n 例如: (水手表情圖案)[我是空白建]Serapin 或是(內單表情圖案)[我是空白建]9487")
        return


    Trophydict = {
        '金塊1000g' :0 ,
        '怪獸內丹'  :0 ,
        '赫卡魯的突起':0,
        '漂流追蹤者的外皮'  :0,
        '幽冥鐵牙的顎骨' :0 ,
        '納恩薩克的角破片'  :0 ,
        '坎迪杜姆的甲殼':0,
        '古德蒙特海賊團的金幣'  :0
    }

    total = 0 #輸入總金額
    before = -1
    after = -1

    username2 = "NULL"

    for i in range(0,len(args)):
        # print(args[i])
        if( len(args) >= 6):
            # if(i < len(args)-1): #意義不明 先註解好了
            if ((i % 2) == 0):  # i%2==0 代表戰利品欄位(單數0,2,4,6,8) i+1代表數量(雙數1,3,5,7)
                if(args[i+1].isdigit()):    #如果數量欄位(1,3,5,7)是數字  

                    if ( args[i] == "<:before:481675536868048903>"):
                        # print("販賣前的工會資金")
                        if (before > 0 ): #如果>0代表已經輸入過了
                            print("販賣前公會資金已經輸入過了")
                            await bot.say("販賣前公會資金已經輸入過了，最好別亂輸入喔")
                            return                        
                        if ( int(args[i+1]) <= 0 ):
                            print("販賣前公會資金輸入異常")
                            await bot.say("販賣前公會資金輸入異常，最好別亂輸入喔")
                            return
                        before = int(args[i+1])
                        continue 

                    if ( args[i] == "<:after:481675646225874956>"):
                        # print("販賣後的工會資金")
                        if (after > 0): #如果>0代表已經輸入過了
                            print("販賣後公會資金已經輸入過了")
                            await bot.say("販賣後公會資金已經輸入過了，最好別亂輸入喔")
                            return
                        if ( int(args[i+1]) <= 0 ):
                            print("販賣後公會資金輸入異常")
                            await bot.say("販賣後公會資金輸入異常，最好別亂輸入喔")
                            return
                        after = int(args[i+1])
                        continue 


                    if( int(args[i+1]) > 100000000 or int(args[i+1]) <= 0 ):
                        print("數量異常")
                        await bot.say("數量異常，最好別亂輸入喔")
                        return             

                    if (emojis2money(args[i]) == -1):
                        print("戰利品欄位錯誤")
                        await bot.say("戰利品欄位錯誤，必須是戰利品表情符號")
                        return
                    elif (emojis2money(args[i]) != -1):
                        total += emojis2money(args[i])*int(args[i+1]) #物品價錢*數量
                        Trophydict[Trophydict_2_ch[args[i]]] = int(args[i+1]) #登記海怪戰利品到字典

                elif(args[i+1].isdigit() == False): #如果數量欄位(1,3,5,7)不是數字
                    if (args[i] =="<:sailor:482780266562191380>"):
                        username2 = args[i+1]
                    else:
                        print("數量錯誤，必須是數字"+args[i]+args[i+1])
                        await bot.say("數量錯誤，必須是數字")
                        return        
        else:
            print('len(args) 必須大於 6')
            await bot.say("別耍我喔ˋˊ \n必須輸入販賣前販賣後的公會資金，還有要餵我的海怪戰利品和數量等等")
            return

    # print("args",args)

    if ( before < 0 or after < 0):
        print('沒有輸入公會資金販賣前或販賣後')
        await bot.say("必須要輸入公會資金販賣前的金額和公會資金販賣之後的金額喔")
        return

    addTrophy(time = whatdayistoday(0),username = display_name, Trophydict = Trophydict,before = before,after = after,username2 = username2)#把戰利品存入資料庫
    # print(display_name+" today("+ whatdayistoday(0) +") ur inpurt money:"+str(total))
    week_money = int(user_total_money(display_name)) #當周累積的收入

    if (username2=="NULL"):
        print(display_name+" today("+ whatdayistoday(0) +")  這次輸入的金額為: {:,} ".format(total))
        await bot.say("hi "+display_name+" 你這次輸入的金額為: {:,} \n這禮拜目前總共餵了我 {:,}元".format(total,week_money))
    else:
        print(display_name+" today("+ whatdayistoday(0) +") 和水手: "+ username2+" 這次輸入的金額為: {:,} ".format(total))
        await bot.say("hi "+display_name+" 你這次輸入的金額為: {:,} \n和水手 {} 平分後獲得金額為: {} \n這禮拜目前總共餵了我 {:,}元".format(total,username2,int(total)/2,week_money))

    # {0,"1階";250000000,"2階";300000000,"3階";350000000,"4階";400000000,"5階";500000000,"6階";650000000,"7階";850000000,"8階";1000000000,"10階"}
    if ( week_money > 1000000000  ):
        await bot.say("挖! 恭喜打完10e囉(可以剩下的可以分給我了3Q")
    elif ( week_money > 850000000):
        await bot.say("加油喔 只差一點點快要打完了")
    elif ( week_money > 500000000):
        await bot.say("耶 還剩下不到一半了 ")

    After_sale = after - before 
    error_money = After_sale - total 
    # if ( error_money != 0):
    #     print(display_name + "的金額出現問題!!販賣前的金額為: {:,}  販賣後的金額為: {:,} 而物品轉換後的資金為: {:,} ".format(before,after,total))
    #     await bot.say("不過"+display_name + " 你的金額可能出現問題囉!! \n販賣前的金額為: {:,} \n販賣後的金額為: {:,} \n而物品轉換後的資金為: {:,} \n販賣後-販賣前-物品轉換後資金為: {:,}".format(before,after,total,after-before-total))
    #     await bot.say("已登記錯誤紀錄了，麻煩請會長協助幫忙喔3Q")
    if( error_money > 0):
        print("核對金額有錯誤\n販賣後資金金額 - 物品截圖金額 = {:,} - {:,} = {:,}\n多了{:,}元".format(After_sale,total,error_money,error_money))
        await bot.say("此筆收入已登記!核對後金額有錯誤\n販賣後資金金額 - 物品截圖金額 = {:,} - {:,} = {:,}\n多了{:,}元\n請確認是否多賣物品沒有截圖!".format(After_sale,total,error_money,error_money))
    elif( error_money < 0 ):
        print("核對金額有錯誤\n販賣後資金金額 - 物品截圖金額 = {:,} - {:,} = {:,}\n少了{:,}元".format(After_sale,total,error_money,-1*error_money))
        await bot.say("此筆收入已登記!核對後金額有錯誤\n販賣後資金金額 - 物品截圖金額 = {:,} - {:,} = {:,}\n少了{:,}元\n請確認是否少賣物品!還是有人領薪水!".format(After_sale,total,error_money,-1*error_money))
    # update_money(display_name,whatdayistoday(1),total)#把收入存入資料庫
    # user_total_money(display_name)#計算總收入


# hi Serapin 你輸入的金額為:123,456,789
# 這禮拜目前總共餵了:789,546,123

def emojis2money(emojis):
    if emojis =="<:1000g:476274938395885568>":
        return 100000000
    if emojis == "<:blue:476262599177011240>":
        return 100000
    if emojis == "<:red:476262607335063552>":
        return 82000
    if emojis == "<:skin:476262626519941120>":
        return 42800
    if emojis == "<:tooth:476262644287012865>":
        return 52400
    if emojis == "<:nashark:476262658669281294>":
        return 53700
    if emojis == "<:Carapace:476262683189182464>":
        return 409200
    if emojis == "<:coin:476262700532367371>":
        return 100000

    # print("戰利品欄位錯誤!")
    return -1

while True:
    try:
        bot.loop.run_until_complete(bot.start(TOKEN))
    except BaseException:
        print("try reconnect")
        time.sleep(20)



# <:before:481675536868048903>
# <:after:481675646225874956>
# ('<:1000g:476274938395885568>', 
# '<:blue:476262599177011240>', 
# '<:Carapace:476262683189182464>', 
# '<:coin:476262700532367371>', 
# '<:nashark:476262658669281294>', 
# '<:nashark:476262658669281294>', 
# '<:red:476262607335063552>', 
# '<:skin:476262626519941120>', 
# '<:tooth:476262644287012865>')
