import threading
import requests
import time
import json
import random

with open(__file__.replace("main.py","")+"json_files/main.json","r") as main_json:
    main = json.load(main_json)
auth = main["authorization"]
channel = main["channel_id"]
guild_id = main["guild_id"]

a = []
def auto_farm(channel_id,auth_token,guild_id):
    header = {"authorization": auth_token}
    message = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=header)
    with open(__file__.replace("main.py", "")+"json_files/data.json","r") as js:
        timing = json.loads(js.read())
    jso = json.loads(message.text)
    js1 = jso[0]["content"]
    if js1 in timing:
        move = timing[js1]
        confirmation(channel_id , jso , move,auth_token,guild_id)

def confirmation(channel_id,message,move,auth,guild_id):
    payload = {
            "application_id": 270904126974590976,
            "channel_id": channel_id,
            "data": {"component_type": 2,"custom_id": message[0]["components"][0]["components"][move]["custom_id"]},
            "guild_id": guild_id,
            "session_id": "0bbaac62023c017a8c355e21400d0124",
            "message_id": message[0]["id"],
            "type": 3
    }
    headers = {"authorization":auth}
    r = requests.post("https://discord.com/api/v9/interactions",json = payload,headers=headers)
    now = time.localtime(time.time())
    timen = (time.strftime("%y/%m/%d %H:%M:", now))
    print(f"\33[93m{timen}Caught something")


def message_sent(authorization,channelid,main,guild_id):
    pls_ran = (False, False, False, False, False, False, True)
    pls_cord = main["distraction"]
    pls_cmd = main["commands"]
    while True:
        if random.choice(pls_ran) == True:
            payload = {"content": random.choice(pls_cord)}
            channel_id = channelid
            header = {"authorization": authorization}
            r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers=header)
            time.sleep(5)
        for pay in pls_cmd:
            now = time.localtime(time.time())
            timen = (time.strftime("%y/%m/%d %H:%M:", now))
            payload = {"content": pay}
            channel_id = channelid
            header = {"authorization": authorization}
            r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers=header)
            if r.status_code == 200:
                print("\33[92m"+timen+pls_cmd[pay])
                auto_farm(channelid, authorization,guild_id)
            else:
                print("\33[91mError"+timen+pls_cmd[pay])
        time.sleep(random.randint(35, 50))

def horseshoe(author_id,channel_id):
    time.sleep(5)
    while True:
        now = time.localtime(time.time())
        timen = (time.strftime("%y/%m/%d %H:%M:", now))
        payload = {"content":"pls use horseshoe"}
        header = {"authorization":author_id}
        r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers=header)
        print(f"\33[34m{timen}Horseshoe Activated")
        time.sleep(60*30)

for i in range(len(auth)):
    a.append(threading.Thread(target=message_sent,args=(auth[i],channel[i],main,guild_id[i])))
    if main["Horseshoe_activation"] == True:
        a.append(threading.Thread(target=horseshoe , args= (auth[i],channel[i])))
for i in a:
    i.start()
for i in a:
    i.join()
