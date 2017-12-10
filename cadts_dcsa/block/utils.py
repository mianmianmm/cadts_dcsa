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
            data = f.read(BUF_SIZE)
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


def encode_response(success=True, error=None):
    return encode_header({
        'success': success,
        'reason': error
    })


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


def file_size_string(size):
    size_units = ['', 'K', 'M', 'G', 'T']
    unit_count = len(size_units)
    size = float(size)

    unit_index = 0
    while size > 1024 and unit_index < unit_count:
        unit_index += 1
        size /= 1024.

    return '{:.2f}{}'.format(size, size_units[unit_index])
