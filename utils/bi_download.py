import json
import os
from pathlib import Path

import requests
from tqdm import tqdm


def call_back_c_id(c_id: str, url: str):
    video_url = get_video_url(c_id, url)


def download_bi_video(url: str):
    get_c_id(url, callback=get_video_url)


def get_c_id(url: str, callback: call_back_c_id):
    qn_url = f"https://api.bilibili.com/x/player/pagelist?bvid={url}&jsonp=jsonp"
    res = requests.get(qn_url, headers=get_header(url))
    c_id = json.loads(res.text)['data'][0]['cid']
    callback(c_id, url)


def get_video_url(c_id: str, url: str):
    url = f"https://api.bilibili.com/x/player/playurl?avid=&cid={c_id}&bvid={url}&qn=240&type=&otype=json"
    res = requests.get(url, headers=get_header(url))
    video_url = json.loads(res.text)["data"]["durl"][0]["url"]
    download_file(video_url, "save_bi.mp4")
    return video_url


def get_header(url: str):
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
        'Referer': f'https://www.bilibili.com/video/{url}',
        'Cookie': "bsource=share_source_copy_link; share_source_origin=COPY; CURRENT_FNVAL=4048; b_lsid=A72F81076_18A3A023455; sid=8gvot3lu; browser_resolution=1324-945; header_theme_version=CLOSE; home_feed_column=4; PVID=2; bili_ticket=eyJhbGciOiJFUzM4NCIsImtpZCI6ImVjMDIiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2OTMzMjM2MTMsImlhdCI6MTY5MzA2NDQxMywicGx0IjotMX0.aaJXnPZ30dJMkVdMR9Aso5ydpGJtTFWByAWQotSSFyQWLALCdalGJP07ENBLjEu3vkYyJV0_WXO_1qqdfVaUN5sf_Z4RaM70Vde6sgDzJ5_M-VHU6R-07AxrM0Rz3lPw; bili_ticket_expires=1693323613; hit-dyn-v2=1; bp_video_offset_38147721=834175214042480691; hit-new-style-dyn=1; buvid_fp=0b313ce6baf1a3dee7b101bcccfb1284; buvid4=C5785A36-CAD1-2C7F-FD53-B667A2AF136459263-023082617-OfYXh40jerEug7duM5b2ow%3D%3D; _uuid=3A101E616-CEEE-D253-5DCE-A8BFA3BDEB2758996infoc; DedeUserID=38147721; DedeUserID__ckMd5=c79b538037a1fd99; SESSDATA=715757ba%2C1706494819%2C8215b%2A82DhFmaItyNiZslWFkeJO42KCHPgBszMbNtWE2CemErf_0jFn840-TQlMb1fBFISNMyWyEqAAAFQA; bili_jct=cbfdbdc5e52b6b5d8a9b12338840b924; rpdid=|(J|~J)J|m|k0J'uYm|))Rlu); b_nut=1690884489; buvid3=9CD13614-3413-C880-2FC6-486F216B944A89221infoc"
    }


def download_file(url: str, file_save_name: str):
    path_file = Path(file_save_name)
    os.remove(path_file)
    if not path_file.is_file():
        path_file.parent.mkdir(parents=True, exist_ok=True)
        resp = requests.get(url, stream=True, headers=get_header(url))
        total = int(resp.headers.get("content-length", 0))

        with open(file_save_name, 'wb') as file, tqdm(
                desc=file_save_name,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    else:
        print("文件已经存在了")
