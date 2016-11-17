import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG, filename='debug.log')


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*"]
    head = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Connection': 'keep-alive', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate'}
    url = 'url-where-you-want-to-upload-file'

    def process(self, event):
        try:
            if not event.is_directory:
                files = {'file': open(event.src_path, 'rb')}
                # any extra data if you want to send
                data = {"api_key": "xxxxxxxxxxxxxxxxxxxxx"}
                print("-----Sending file : ", event.src_path)
                response = requests.post(self.url, files=files, data=data, headers=self.head)
                print("--------Response-----------")
                print(response.text)
            else:
                print("its a directory : ", event.src_path)
        except Exception as e:
            print(e)
            logging.exception(e)

    def on_created(self, event):
        self.process(event)


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
