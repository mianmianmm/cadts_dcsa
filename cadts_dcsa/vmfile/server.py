import uuid

import os


class VmFileServer(object):
    def __init__(self, http_host, http_base_dir):
        self.http_host = http_host
        self.http_base_dir = http_base_dir
        self.files_dir = 'vm_files'

    def on_download_request(self, vm_path, guest_path):
        file_name = uuid.uuid4()
        file_path = os.path.join(self.http_base_dir, self.files_dir, file_name)
        # TODO download file to file_path
        url = 'http://{}/{}/{}'.format(self.http_host, self.files_dir, file_name)
        # response url
        # register timeout
        timeout_seconds = max(os.path.getsize(file_path) / (1024 * 1024), 30)
        self.begin_timeout(timeout_seconds)

    def begin_timeout(self, timeout_seconds):
        pass

    def on_progress(self, url):
        pass

    def on_timeout(self, url):
        self.clear_file(url)

    def on_cancel(self, url):
        self.clear_file(url)

    def clear_file(self, url):
        file_name = self.extract_file_name(url)
        if os.path.exists(file_name):
            os.remove(file_name)
