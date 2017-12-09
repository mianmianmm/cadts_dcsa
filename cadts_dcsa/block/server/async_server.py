# coding=utf-8
import json
import struct
import os
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol

from cadts_dcsa.block.utils import calc_sha1, encode_response

clients=[]


SAVE_DIR = 'E:\\tmp'

class MyProtocol(Protocol):
    _buffer = ""  # 接收缓冲区
    tmpbuf = ''  # 暂存上次未接受完的内容
    response = False
    header_len = 0
    file_len = 0
    file_sha1 = 0
    file_name = ''
    recv_size = 0  # 初始化已接收文件的长度
    recv_sha1 = ''
    recv_file_name = ''
    recv_file_name_sha1 = ''
    recv_info = ''

    def connectionMade(self):
        self.factory.numPorts +=1
        self.number=self.factory.numPorts-1
        print 'connection %d ....' % (self.number,), 'from: ', self.transport.client
        self.sendData('you are client %d...' % (self.factory.numPorts-1,))
        clients.append(self)


    def connectionLost(self, reason):
        self.factory.numPorts -= 1
        clients.remove(self)
        print self.transport.client, 'disconnected  '

    def dataReceived(self, data):
        self._buffer = data
        # leng=len(self._buffer)
        # print leng
        if len(self.tmpbuf) != 0:
            self._buffer = self.tmpbuf + self._buffer
            self.tmpbuf = ''

        if self.recv_size == self.file_len:  # 准备开始接收第1个文件（或当前文件接收完成）
            self.recv_size = 0  # 已接收大小置0，准备接受下一个文件
            if len(self._buffer) < 4:
                print 'cilent %d :pack header_len error of ...' % (self.factory.numPorts-1,)
                return
            self.header_len, = struct.unpack('!I', self._buffer[0:4])  # unpack header_len
            if len(self._buffer) < 4 + self.header_len:
                print 'cilent %d :pack header error of ...' % (self.factory.numPorts-1,)
                return
            header_string = self._buffer[4:4 + self.header_len]  # unpack headers
            header = json.loads(header_string)
            self.recv_info = header
            self.file_name = header['file_name']
            self.file_len = header['file_len']
            self.file_sha1 = header['file_sha1']
            self.recv_file_name = os.path.join(SAVE_DIR, self.file_name)
            self.recv_file_name_sha1 = os.path.join(SAVE_DIR, self.file_name + '.sha1')
            self._buffer = self._buffer[4 + self.header_len:]  # 开始接收文件内容
            with open(self.recv_file_name, 'wb+') as f:
                self.recv_size += len(self._buffer)
                f.write(self._buffer)
            if self.recv_size == self.file_len:  # 当前文件接收完毕，则校验sha1值
                self.recv_sha1 = calc_sha1(self.recv_file_name)
                if self.recv_sha1 == self.file_sha1:
                    print 'cilent %d :\"%s\" receive done , calc sha1 ok!' % (self.factory.numPorts-1,self.file_name)
                    self.response = True
                    with open(self.recv_file_name_sha1, 'wb+') as ff:
                        ff.write(self.recv_sha1)
                else:
                    print 'client %d :\"%s\"receive done ,calc sha1 failed!' % (self.factory.numPorts-1,self.file_name)
                    self.response = False
                self.recv_info['success'] = self.response  # 返回给客户端
                response = encode_response(self.recv_info)
                # print response
                self.sendData(response)
        elif self.recv_size < self.file_len:  # 当前文件未接收完毕
            self.recv_size += len(self._buffer)
            if self.recv_size <= self.file_len:  # 文件未接收完毕（或恰好接收完毕）
                with open(self.recv_file_name, 'ab+') as f:
                    f.write(self._buffer)
                if self.recv_size == self.file_len:  # 文件恰好接收完毕，则校验sha1值
                    self.recv_sha1 = calc_sha1(self.recv_file_name)
                    if self.recv_sha1 == self.file_sha1:
                        print 'cilent %d :\"%s\" receive done , calc sha1 ok!' % (self.factory.numPorts - 1, self.file_name)
                        self.response = True
                        with open(self.recv_file_name_sha1, 'wb+') as ff:
                            ff.write(self.recv_sha1)
                    else:
                        print 'client %d :\"%s\"receive done ,calc sha1 failed!' % (self.factory.numPorts - 1, self.file_name)
                        self.response = False
                    self.recv_info['success'] = self.response  # 返回给客户端
                    response = encode_response(self.recv_info)
                    # print response
                    self.sendData(response)
            else:  # 接收内容超出当前文件大小
                with open(self.recv_file_name, 'ab+') as f:
                    f.write(self._buffer[0:self.file_len - self.recv_size])
                    self.tmpbuf = self._buffer[self.recv_size - self.file_len]  # 暂存超出的部分，用来进行下一个文件的接收
                    self.recv_size = self.file_len  # 当前文件接收完毕，则校验sha1值
                    self.recv_sha1 = calc_sha1(self.recv_file_name)
                    if self.recv_sha1 == self.file_sha1:
                        print 'cilent %d :\"%s\" receive done , calc sha1 ok!' % (self.factory.numPorts - 1, self.file_name)
                        self.response = True
                        with open(self.recv_file_name_sha1, 'wb+') as ff:
                            ff.write(self.recv_sha1)
                    else:
                        print 'client %d :\"%s\"receive done ,calc sha1 failed!' % (self.factory.numPorts - 1, self.file_name)
                        self.response = False
                    self.recv_info['success'] = self.response  # 返回给客户端
                    response = encode_response(self.recv_info)
                    # print response
                    self.sendData(response)

        self._buffer = ''

    def sendData(self, data):
        self.transport.write(data)


if __name__ == '__main__':
    if os.name!='nt':
        from twisted.internet import epollreactor
        epollreactor.install()
    from twisted.internet import reactor
    factory = Factory()
    factory.protocol = MyProtocol
    reactor.listenTCP(1234, factory)
    reactor.run()