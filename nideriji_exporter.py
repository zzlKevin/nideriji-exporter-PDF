'''
你的日记导出用脚本
nideriji_exporter.py
'''

import os
from pathlib import Path
import json
import time
import requests


class ApiUrl():
    '''
    储存所需要的 Api
    '''
    LOGIN: str = "https://nideriji.cn/api/login/"
    ALL_DIARY: str = 'https://nideriji.cn/api/diary/all/'
    AVATAR: str = 'https://f.nideriji.cn/'
    IMG: str = "https://f.nideriji.cn/api/image/"


class FileDir():
    '''
    储存所需要的文件地址
    '''
    IMG: str = './.exported/img/'
    JSON: str = './.exported/json/'


class User():
    '''
    用于存储 email 和 password 的用户类
    '''
    email: str
    password: str

    def init(self):
        '''
        初始化
        '''
        self.email = input('> 请输入邮箱: ')
        self.password = input('> 请输入密码: ')
        return self

    def __str__(self) -> str:
        return json.dumps(
            {
                "email": self.email,
                "password": self.password,
            },
            ensure_ascii=False,
        )


class UserInfo():
    '''
    传入 login_res_json 获取个人信息
    '''
    # 自己部分
    token: str
    description: str
    diary_count: int
    word_count: int
    name: str
    user_id: int
    paired: bool
    gender: str
    avatar: str
    image_count: int

    # 对方部分
    paired_user_description: str
    paired_user_diary_count: int
    paired_user_word_count: int
    paired_user_name: str
    paired_user_user_id: int
    paired_user_gender: str
    paired_user_avatar: str
    paired_user_image_count: int

    def __init__(self, login_res_json: json) -> None:
        # 将传入的 login_res_json 分配给类
        self.token = login_res_json['token']
        self.description = login_res_json['user_config']['description']
        self.diary_count = login_res_json['user_config']['diary_count']
        self.word_count = login_res_json['user_config']['word_count']
        self.name = login_res_json['user_config']['name']
        self.user_id = login_res_json['user_config']['userid']
        self.paired = login_res_json['user_config']['paired']
        self.gender = login_res_json['user_config']['role']
        self.avatar = login_res_json['user_config']['avatar']
        self.image_count = login_res_json['user_config']['image_count']

        # 处理对方部分
        if login_res_json['user_config']['paired']:
            self.paired_user_description = login_res_json['user_config'][
                'paired_user_config']['description']
            self.paired_user_diary_count = login_res_json['user_config'][
                'paired_user_config']['diary_count']
            self.paired_user_word_count = login_res_json['user_config'][
                'paired_user_config']['word_count']
            self.paired_user_name = login_res_json['user_config'][
                'paired_user_config']['name']
            self.paired_user_user_id = login_res_json['user_config'][
                'paired_user_config']['userid']
            self.paired_user_gender = login_res_json['user_config'][
                'paired_user_config']['role']
            self.paired_user_avatar = login_res_json['user_config'][
                'paired_user_config']['avatar']
            self.paired_user_image_count = login_res_json['user_config'][
                'paired_user_config']['image_count']

    def __str__(self) -> str:
        return json.dumps(
            {
                "token": self.token,
                "description": self.description,
                "diary_count": self.diary_count,
                "word_count": self.word_count,
                "name": self.name,
                "user_id": self.user_id,
                "paired": self.paired,
                "gender": self.gender,
                "avatar": self.avatar,
                "image_count": self.image_count,
                "paired_user_description": self.paired_user_description,
                "paired_user_diary_count": self.paired_user_diary_count,
                "paired_user_word_count": self.paired_user_word_count,
                "paired_user_name": self.paired_user_name,
                "paired_user_user_id": self.paired_user_user_id,
                "paired_user_gender": self.paired_user_gender,
                "paired_user_avatar": self.paired_user_avatar,
                "paired_user_image_count": self.paired_user_image_count,
            },
            ensure_ascii=False,
        )


class Header():
    '''
    API 提交时的表头
    '''
    auth: str
    user_agent: str

    def __init__(self, auth: str) -> None:
        self.auth = f"token {auth}"
        self.user_agent = 'Dalvik/2.1.0 (Linux; U; Android 12; FIG-AL10 Build/HUAWEIFIG-AL10)'

    def __str__(self) -> str:
        return json.dumps(
            {
                "auth": self.auth,
                "user-agent": self.user_agent,
            },
            ensure_ascii=False,
        )


def get_login_res_json() -> json:
    '''
    提交全局 USER 并尝试获取 json
    '''
    res = json.loads('{"error": -1}')
    while res['error'] != 0:
        res = json.loads(
            requests.post(
                url=ApiUrl.LOGIN,
                data=json.loads(str(USER)),
                timeout=None,
            ).text)
        if res['error'] == 0:
            return res
        else:
            print(f'> 请检查帐号信息，错误代码为 {res["error"]}')

        USER.init()


def get_maximum_diaries(latest_date: str) -> json:
    '''
    获取比 latest_date 久远最大 20 个的日记部分 json
    '''
    time.sleep(0.01)
    return json.loads(
        requests.get(
            url=ApiUrl.ALL_DIARY,
            headers=json.loads(str(HEADER)),
            params={
                'latest_date': latest_date,
            },
            timeout=None,
        ).text)['diaries']


def get_all_diaries() -> tuple[list, list]:
    '''
    获取所有日记部分 json
    '''
    latest_date = '2100-01-01'
    self = []
    pair = []

    while len(get_maximum_diaries(latest_date)) != 0:
        get = get_maximum_diaries(latest_date)
        print(f"> 已获取比 {latest_date} 久远的 {len(get)} 个日记")
        for i in get:
            if i['space'] == USER_INFO.gender:
                print(f'> 自己 {i["createddate"]}')
                self.append(i)
            else:
                print(f'> 对方 {i["createddate"]}')
                pair.append(i)
        latest_date = get[-1]['createddate']
    return self, pair


def export_self_imgs() -> list:
    '''
    导出自己所有图片
    '''

    myself = []

    Path(f"{FileDir.IMG}{USER_INFO.name}/").mkdir(
        parents=True,
        exist_ok=True,
    )
    continued_blank = 0
    for i in range(0, int(USER_INFO.image_count * 1.25), 1):
        if continued_blank < 100:
            time.sleep(0.5)
            res = requests.get(
                url=f"{ApiUrl.IMG}{USER_INFO.user_id}/{i}",
                headers=json.loads(str(HEADER)),
                timeout=None,
            )
            if res.text != '':
                continued_blank = 0
                print(f'> 正在导出 {USER_INFO.name} 的图 {i}')

                with open(
                        f"{FileDir.IMG}{USER_INFO.name}/图{i}.jpg",
                        'wb',
                ) as pic:
                    img = res.content
                    pic.write(img)

                myself.append({f'图 {i}': str(res.content)})
            else:
                continued_blank = continued_blank + 1
                print(f'> {USER_INFO.name} 的图 {i} 为空')
        else:
            break

    return myself


def export_pair_imgs() -> list:
    '''
    导出对方所有照片
    '''

    pair = []

    if USER_INFO.paired:

        Path(f"{FileDir.IMG}{USER_INFO.paired_user_name}/").mkdir(
            parents=True,
            exist_ok=True,
        )

        continued_blank = 0
        for i in range(0, int(USER_INFO.paired_user_image_count * 1.25), 1):
            if continued_blank < 100:
                time.sleep(0.5)
                res = requests.get(
                    url=f"{ApiUrl.IMG}{USER_INFO.paired_user_user_id}/{i}",
                    headers=json.loads(str(HEADER)),
                    timeout=None,
                )
                if res.text != '':
                    continued_blank = 0
                    print(f'> 正在导出 {USER_INFO.paired_user_name} 的图 {i}')

                    with open(
                            f"{FileDir.IMG}{USER_INFO.paired_user_name}/图{i}.jpg",
                            'wb',
                    ) as pic:
                        img = res.content
                        pic.write(img)

                    pair.append({f'图 {i}': str(res.content)})
                else:
                    continued_blank = continued_blank + 1
                    print(f'> {USER_INFO.paired_user_name} 的图 {i} 为空')
            else:
                break

    return pair


def export_all_diaries(all_diaries: tuple) -> None:
    '''
    导出所有数据
    '''
    Path(FileDir.JSON).mkdir(parents=True, exist_ok=True)
    Path(FileDir.IMG).mkdir(parents=True, exist_ok=True)

    with open(
            f'{FileDir.JSON}{USER_INFO.name}.json',
            'w',
            encoding='utf-8',
    ) as file:
        file.write(json.dumps(all_diaries[0], ensure_ascii=False, indent=1))

    if USER_INFO.paired:

        with open(
                f'{FileDir.JSON}{USER_INFO.paired_user_name}.json',
                'w',
                encoding='utf-8',
        ) as file:
            file.write(
                json.dumps(
                    all_diaries[1],
                    ensure_ascii=False,
                    indent=2,
                ))


def export_all_imgs(self_imgs, pair_imgs) -> None:
    '''
    导出所有图片
    '''
    with open(
            f'{FileDir.IMG}{USER_INFO.name}.json',
            'w',
            encoding='utf-8',
    ) as file:
        file.write(json.dumps(self_imgs, ensure_ascii=False, indent=1))

    if USER_INFO.paired:

        with open(
                f'{FileDir.IMG}{USER_INFO.paired_user_name}.json',
                'w',
                encoding='utf-8',
        ) as file:
            file.write(json.dumps(pair_imgs, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    os.system('cls')

    USER = User().init()

    USER_INFO = UserInfo(get_login_res_json())

    HEADER = Header(USER_INFO.token)

    export_all_diaries(get_all_diaries())

    export_all_imgs(export_self_imgs(), export_pair_imgs())

    print('')
