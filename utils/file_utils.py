import requests
from tqdm import tqdm


def download_file(url: str, file_save_name: str):
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
