# coding=utf-8
import json
import socket

# c -> s: header_len | header(json) | content
# s -> c: header_len | header(json) {success: true | false}
import time
import struct

import os

from cadts_dcsa.block.utils import encode_file_header, send_all, receive_all, file_size_string

BUF_SIZE = 4096


def send_file(s, file_path):
    # send header and file content
    header_string = encode_file_header(file_path)
    file_len = os.path.getsize(file_path)
    send_all(s, header_string)
    with open(file_path, 'rb')as f:
        data = f.read(BUF_SIZE)
        while data:
            send_all(s, data)
            data = f.read(BUF_SIZE)

    # receive response
    len_string = receive_all(s, 4)
    if len_string:
        header_length, = struct.unpack('!I', len_string)
        json_string = receive_all(s, header_length)
        response = json.loads(json_string)
        if not response['success']:
            raise Exception(response.get('reason', None))

    return file_len


def send_files(host, port, *file_list):
    sent_size = 0
    s = socket.socket()
    try:
        s.connect((host, port))
        for file_path in file_list:
            sent_size += send_file(s, file_path)
    finally:
        s.close()

    return sent_size


if __name__ == '__main__':
    start = time.clock()
    total_size = send_files('127.0.0.1', 1234, u'E:\\Users\\LiRui\\Downloads\\cn_windows_10_multiple_editions_version_1607_updated_jul_2016_x64_dvd_9056935.iso')
    elapsed = time.clock() - start
    speed = total_size / elapsed
    print '''time: {:.2f}s
size: {}Bytes
speed: {}B/s
'''.format(elapsed, file_size_string(total_size), file_size_string(speed))
