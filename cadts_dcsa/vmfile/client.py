# coding=utf-8


class VmFileClient(object):
    def __init__(self, vm_server):
        self.vm_server = vm_server

    def begin_download(self, vm_path, guest_path):
        download_url = 'http://<HOST>/vm_files/f2395ffe-68f1-48b4-a50c-a5e75fcbd8fa'
        return download_url

    def download(self, url, local_path, progress_listener=None):
        # report progress
        progress_listener(self, url, 0.1)
        # on error
        progress_listener(self, url, 0.1, '404')

    def cancel(self, url):
        pass

    def report_progress(self, url, progress):
        pass


def fetch_file(vm_server, vm_path, local_path, guest_path):
    def on_progress(c, url, progress, error=None):
        c.report_progress(url, progress)
        timeout = False
        if timeout or error:
            c.cancel(url)

    client = VmFileClient(vm_server)
    url = client.begin_download(vm_path, guest_path)
    client.download(url, local_path, on_progress)
