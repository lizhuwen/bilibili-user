import random
import requests
import json
import time
import numpy as np

def get_UserAgent():
    agents = []
    with open('user_agents.txt', 'rb') as f:
        for agent in f.readlines():
            if agent:
                agents.append(agent.strip()[1:-1 -1])
    random.shuffle(agents)
    return agents

def Bilibili_spider():
    url = 'https://space.bilibili.com/ajax/member/GetInfo'
    code = {
        "name": "None",
        "mid": "None",
        "face": "None",
        "birthday": "None",
        "sex": "None",
        "playNum": "None",
        "current_level": "None",
        "currten_exp": "None",
        "description": "None",
        "article": "None",
        "video": "None",
        "album": "None",
        "channel": "None",
        "favourite": "None"
    }

    #数字是每个用户的id号，越大id号，说明是最近创建的用户
    for m in range(1,322283999):
        header = {
            'User-Agent': random.choice(get_UserAgent()),
            'Host': 'space.bilibili.com',
            'Origin': 'https://space.bilibili.com',
            'Referer': 'https://space.bilibili.com/100931805/',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        }
        payload = {
            'mid': m
        }
        time.sleep(np.random.rand() * 5)
        response = requests.post(url=url, headers=header, data=payload)
        print('----------')
        print(response.status_code)
        #print(response.text)

        result = json.loads(response.text)
        status = result['status'] if 'status' in result.keys() else False
        if status == True:
            if 'data' in result.keys():
                data = result['data']
                code['name'] = data['name'] #用户名
                code['mid'] = data['mid']   #uid用户id
                code['face'] = data['face']   #用户头像下载link
                code['birthday'] = data['birthday'] if 'birthday' in data.keys() else 'nobirthday'#用户生日
                code['sex'] = data['sex'] #用户性别
                code['sign'] = data['sign'] #个性签名
                code['playNum'] = data['playNum']   #播放数
                code['current_level'] = data['level_info']['current_level'] #用户等级
                code['urrent_exp'] = data['level_info']['current_exp'] #用户经验值
                code['description'] = data['description']
                code['article'] = data['article']

                try:
                    res = requests.get(url='https://api.bilibili.com/x/space/navnum?mid='+ str(mid))
                    fans_data = json.loads(res.text)['data']
                    code['video'] = fans_data['video']  #用户的视频数
                    code['album'] = fans_data['album']  #用户的相册数
                    code['channel'] = fans_data['channel']    #用户频道数
                    code['favourite'] = fans_data['favourite']  #用户收藏夹数
                except:
                    code['video'] = 0
                    code['album'] = 0
                    code['channel'] = 0
                    code['favourite'] = 0
                # print('用户名：%s' % name)
                # print('用户uid：%s' % mid)
                # print('头像下载link：%s' % avatar)
                # print('生日：%s' % birthday)
                # print('性别：%s' % sex)
                # print('个性签名：%s' % sign)
                # print('播放数：%s' % playNum)
                # print('用户等级：%s' % current_level)
                # print('用户经验值：%s' % current_exp)
                # print('用户的相册数：%s' % video)
                # print('用户经验值：%s' % album)
                # print('用户频道数：%s' % channel)
                # print('用户收藏夹数：%s' % favourite)
            else:
                print('No data now')
        yield code

def process_json():
    """
    存取为json文件
    :return:
    """
    items = Bilibili_spider()
    fileName = open("Bilibili_user.json", 'wb')
    for code in items:
        print(code)
        text = json.dumps(dict(code), ensure_ascii=False) + "\n"
        fileName.write(text.encode('utf-8'))
    fileName.close()

if __name__ == '__main__':
    Bilibili_spider()
    process_json()