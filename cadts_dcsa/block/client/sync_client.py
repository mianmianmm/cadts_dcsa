# coding=utf-8
import json
import socket

# c -> s: header_len | header(json) | content
# s -> c: header_len | header(json) {success: true | false}
import time
import struct

from cadts_dcsa.block.utils import encode_file_header


def send_file(host, port, *file_list):
    with socket.socket() as s:
        s.connect((host, port))
        print s.recv(1024)
        for file_path in file_list:
            # send header
            start = time.clock()
            header = encode_file_header(file_path)
            s.sendall(header)
            # send content
            # time.sleep(0.01)
            with open(file_path, 'rb')as f:
                data = f.read(4096)
                while data:
                    s.sendall(data)
                    data = f.read(4096)
                print '\"',file_path,'\"', '...send over..........................', time.clock() - start
                f.close()
                # recv response
                len_string = s.recv(4)
                if len_string:
                    length, = struct.unpack('!I', len_string)
                    json_string = s.recv(length)
                    response = json.loads(json_string)
                    if not response['success']:
                        print 'success: false........'
                        raise Exception()
                    else:
                        print 'success:true........'


if __name__ == '__main__':
    send_file('127.0.0.1', 1234, u'E:\\Users\\LiRui\\Downloads\\VanDyke.SecureCRT.and.SecureFX.8.3.0.Build.1514.rar')