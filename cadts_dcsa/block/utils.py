import hashlib
import struct
import json
import os

BUF_SIZE = 4096


def calc_sha1(file_path):
    with open(file_path, 'rb') as f:
        sha1 = hashlib.sha1()
        data = f.read(BUF_SIZE)
        while data:
            sha1.update(data)
            data=f.read(BUF_SIZE)
        return sha1.hexdigest()


def encode_header(header):
    header_string = json.dumps(header)
    header_len_string = struct.pack('!I', len(header_string))
    return header_len_string + header_string


def encode_file_header(file_path):
    return encode_header({
        'file_name': os.path.basename(file_path),
        'file_len': os.path.getsize(file_path),
        'file_sha1': calc_sha1(file_path)
    })


def encode_response(recv_info):
    return encode_header(recv_info)


def receive_all(s, length):
    buf = ''
    remain = length
    while remain > 0:
        data = s.recv(remain)
        remain -= len(data)
        buf += data

    return buf


def send_all(s, data):
    s.sendall(data)
