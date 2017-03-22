#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SocketServer
import struct
import os

# Format: name_len      --- one byte
#         name          --- name_len bytes
#         data          --- variable length

# Save data to name into current directory
# Refer to: http://blog.csdn.net/g__gle/article/details/8144968
addr = ('', 7819)
class MyTCPHandler (SocketServer.StreamRequestHandler):
    def handle(self):
        name_len = ord(self.rfile.read(1))
        name = self.rfile.read(name_len)
        print "Get request: %s" % name
        file_size = struct.unpack(">l", self.rfile.read(4))[0]
        restfile = file_size
        fd = open(name, 'wb')
        package_cnt = 0
        while restfile > 4096:
            package_cnt += 1

            cont = self.rfile.read(4096)
            fd.write(cont)
            restfile -= 4096

            if package_cnt >= 5:
                self.request.send(struct.pack('>l', file_size - restfile))
                package_cnt = 0

        self.request.send(struct.pack('>l', file_size - restfile))

        fd.write(self.rfile.read(restfile))
        fd.close()
        print "Out: %s\n" % name

server = SocketServer.TCPServer(addr, MyTCPHandler)
print "Serving on port %s ..." % addr[1]
server.serve_forever()
