# coding=utf-8
import hashlib
import json
import struct
import os
import sys
import logging
import logging.config
from twisted.internet.protocol import Factory, connectionDone
from twisted.internet.protocol import Protocol

from cadts_dcsa.block.utils import calc_sha1, encode_response, file_size_string

LOG = logging.getLogger(__name__)

SAVE_DIR = 'E:\\tmp'

STATE_LEN = 0
STATE_HEADER = 1
STATE_CONTENT = 2

ERROR_SHA1_MISMATCH = 'SHA1 mismatch'


class FileInfo(object):
    def __init__(self, header_json):
        self.file_name = header_json['file_name']
        self.file_len = header_json['file_len']
        self.file_sha1 = header_json['file_sha1']
        self.file_path = os.path.join(SAVE_DIR, self.file_name)
        self.sha1_path = os.path.join(SAVE_DIR, self.file_name + '.sha1')

        self.file = open(self.file_path, 'wb')
        self.bytes_written = 0
        self.finished = False
        self.error = None
        self.sha1 = hashlib.sha1()

    def write(self, data):
        remain = self.file_len - self.bytes_written
        more = ''

        if remain < data:
            more = data[remain:]
            data = data[0:remain]

        self.bytes_written += len(data)
        self.file.write(data)
        self.sha1.update(data)

        if self.bytes_written == self.file_len:
            self.close()
            self.finished = True

            real_sha1 = self.sha1.hexdigest()
            LOG.debug('SHA1: %s vs %s', real_sha1, self.file_sha1)
            if real_sha1 == self.file_sha1:
                with open(self.sha1_path, 'wb') as sha1_file:
                    sha1_file.write(real_sha1)
            else:
                self.error = ERROR_SHA1_MISMATCH

        return more

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


class FileReceiveProtocol(Protocol):

    def __init__(self):
        self.state = STATE_LEN
        self.buffer = ''
        self.header_len = 0
        self.file_info = None

    def connectionMade(self):
        self.state = STATE_LEN
        LOG.info('Connection from %s', self.transport.getPeer())

    def connectionLost(self, reason=connectionDone):
        self.close_file()
        LOG.info('Connection lost %s: %s', self.transport.getPeer(), reason)

    def dataReceived(self, data):
        if self.state != STATE_CONTENT:
            self.buffer += data
        else:
            self.buffer = data

        if self.state == STATE_LEN:
            if len(self.buffer) >= 4:
                self.header_len = struct.unpack('!I', self.buffer[0:4])[0]
                self.buffer = self.buffer[4:]
                self.state = STATE_HEADER
                LOG.debug('Header len: %d', self.header_len)

        if self.state == STATE_HEADER:
            if len(self.buffer) >= self.header_len:
                header_string = self.buffer[0:self.header_len]
                header_json = json.loads(header_string)
                self.file_info = FileInfo(header_json)
                self.buffer = self.buffer[self.header_len:]
                self.state = STATE_CONTENT
                LOG.debug('Header: %s', header_json)
                if self.buffer:
                    LOG.debug('ADD %d', len(self.buffer))
                    self.buffer = self.file_info.write(self.buffer)

        if self.state == STATE_CONTENT:
            self.buffer = self.file_info.write(self.buffer)
            if self.file_info.finished:
                self.state = STATE_LEN
                if not self.file_info.error:
                    self.transport.write(encode_response())
                    LOG.debug('Successfully sent %sBytes', file_size_string(self.file_info.file_len))
                else:
                    self.transport.write(encode_response(False, self.file_info.error))
                    LOG.debug('Failed to send %sBytes: %s', file_size_string(self.file_info.file_len),
                              self.file_info.error)
                self.close_file()

    def close_file(self):
        if self.file_info:
            self.file_info.close()
            self.file_info = None


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    if os.name != 'nt':
        from twisted.internet import epollreactor

        epollreactor.install()

    from twisted.internet import reactor

    factory = Factory()
    factory.protocol = FileReceiveProtocol
    reactor.listenTCP(1234, factory)
    reactor.run()
