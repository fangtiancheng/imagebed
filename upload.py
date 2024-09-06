from abc import ABC, abstractmethod
from typing import Optional, Dict
import requests
import datetime
import base64
import json
from uuid import uuid4
import os

class ImageBed(ABC):
    @abstractmethod
    def upload_file(self, path:str, mime_type:str, orig_name:str)->Optional[str]:
        """upload file to remote image bed
        :param path: str, local file path
        :return: url if succeed, None if failed
        """

def file_to_b64(path:str)->str:
    f = open(path, 'rb')
    content = base64.b64encode(f.read()).decode()
    f.close()
    return content

## 第三方图床
class GithubImageBed(ImageBed):
    def __init__(self, github_name:str, github_repo:str, token:str) -> None:
        self.github_name = github_name
        self.github_repo = github_repo
        self.token = token

    def upload_file(self, path: str, mime_type: str, orig_name: str) -> Optional[str]:
        curr_time = datetime.datetime.now()
        remote_path = curr_time.strftime("%Y-%m-%d")
        remote_fname = str(uuid4()) + os.path.splitext(orig_name)[1]
        url = f"https://api.github.com/repos/{self.github_name}/{self.github_repo}/contents/images/" + remote_path + "/" + remote_fname
        headers = {"Authorization": "Bearer " + token}
        content = file_to_b64(path)
        data = {
            "message": "upload pictures",
            "content": content
        }
        data = json.dumps(data)
        req = requests.put(url=url, data=data, headers=headers)
        if not req.ok:
            print(req.text)
            return None
        response = req.json()
        return response['content']['download_url']

## 方法2：base64
    
if __name__ == '__main__':
    token = '********************'
    imgbed = GithubImageBed('fangtiancheng', 'imagebed', token)
    download_url = imgbed.upload_file('/tmp/gradio/916789ecc996fcf3e0040aedbe902a04c8c81a8a98bee783f0c61cbf1200d396/截图 2024-09-05 19-21-37.png',
                             'image/png', '截图 2024-09-05 19-21-37.png')
    print(download_url)
