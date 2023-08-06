import socketserver
from utils import Utils
import chardet


class echorequestserver(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        print(self.client_address[0], 'connectted!')
        while True:
            client_data = conn.recv(10240)
            if not client_data:
                print('connect interrupt')
                break
            print(client_data.decode(chardet.detect(client_data).get("encoding")).strip('\n'))
            # output = input('你的回话：')
            # conn.sendall(output.encode("utf-8"))


if __name__ == '__main__':
    port = int(input("please input your port:"))
    # server =socketserver.TCPServer(("192.168.10.207", 8080),echorequestserver)  # 使用处理单连接的TCPServer
    server = socketserver.ThreadingTCPServer((Utils.get_host_ip(), port), echorequestserver)  # 使用处理多连接的TCPServer
    print('tcp server starting successfully...')
    server.serve_forever()
