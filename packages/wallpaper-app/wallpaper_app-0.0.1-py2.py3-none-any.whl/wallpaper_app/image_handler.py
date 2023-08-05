import time
import shutil
import tempfile
import subprocess

import requests


class UnsplashWrapper:
    def __init__(self, app_id=None):
        self.base_url = 'https://api.unsplash.com/'

        self.app_id = app_id
        if self.app_id is None:
            self.headers = None
        else:
            self.headers = {
                'Accept-Version': 'v1',
                'Authorization': f'Client-ID {app_id}'
            }

    def _request(self, endpoint, data=None):
        if self.app_id is None:
            raise RuntimeError('App ID must not be None')

        r = requests.get(
            f'{self.base_url}/{endpoint}',
            data=data, headers=self.headers)
        return r.json()

    def save_random_image(self, fd, collections=None):
        if self.app_id is None:
            cols = ','.join(collections or [])
            url = f'https://source.unsplash.com/collection/{cols}'

            r = requests.get(url, stream=True)
            shutil.copyfileobj(r.raw, fd)
        else:
            data = self._request(
                '/photos/random',
                data=dict(collections=','.join(collections or [])))

            img_url = data['urls']['full']
            r = requests.get(img_url, stream=True, headers=self.headers)
            shutil.copyfileobj(r.raw, fd)


def set_wallpaper(fname):
    script = f"""/usr/bin/osascript<<END
    tell application "Finder"
        set desktop picture to POSIX file "{fname}"
    end tell
    END"""
    subprocess.Popen(script, shell=True)
    time.sleep(1)  # otherwise script crashes (why?!)


def main():
    un = UnsplashWrapper()

    collections = {
        'desktop-wallpapers': '1065396',
        'mac-wallpapers': '1339119'
    }

    with tempfile.NamedTemporaryFile() as fd:
        un.save_random_image(fd, collections=collections.values())
        set_wallpaper(fd.name)


if __name__ == '__main__':
    main()
