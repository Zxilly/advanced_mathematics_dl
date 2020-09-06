import time

import aria2p
import requests

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret=""
    )
)

cookies = {
    'JSESSIONID': '83F3ACB32A75687DFF12CF6A9EF5D33A.cxvideo_web_17.30',
    'route': '439c20e914199fc09f0b0f397ea0e048'
}

referer = 'https://ssvideo.superlib.com/api/video/play/mobile?seriesid=4705&vid=90624&sign=videoplay_faxian&enc=79e2e065ddfc181eae0f72f8d1df8f15&appId=1000'

dl_list = []


def dl(urls):
    while True:
        if len(aria2.get_downloads()) <= 13:
            aria2.add_uris(urls, options={
                'referer': 'https://ssvideo.superlib.com/api/video/play/mobile?seriesid=4705&vid=90624&sign=videoplay_faxian&enc=79e2e065ddfc181eae0f72f8d1df8f15&appId=1000',
            })
            break
        else:
            for one_dl in aria2.get_downloads():
                if one_dl.is_complete:
                    aria2.remove([one_dl])
                elif one_dl.has_failed:
                    if aria2.resume([one_dl]):
                        time.sleep(1)
                        if one_dl.has_failed:
                            # self.failure_name.append(one_dl.name)
                            aria2.remove([one_dl])
            time.sleep(5)


for episode in range(90741, 90911): # start with 90625
    print(f'start {episode}\n')
    url = f'https://ssvideo.superlib.com/api/video/play/video/url/{episode}'
    resp = requests.get(url=url, cookies=cookies, headers={
        'Referer': referer
    }).json()
    if resp['success']:
        pass
    else:
        continue
    dl_url = resp['data']['download']
    dl([dl_url])
