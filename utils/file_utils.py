import requests
from tqdm import tqdm
from pathlib import Path


def is_exist_file(file_path: str):
    path_file = Path(file_path)
    return path_file.is_file()


def download_file(url: str, file_save_name: str):
    path_file = Path(file_save_name)
    if not path_file.is_file():
        path_file.parent.mkdir(parents=True, exist_ok=True)
        resp = requests.get(url, stream=True)
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
