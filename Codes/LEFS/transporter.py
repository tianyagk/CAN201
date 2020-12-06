import socket
import os


class FileSender:
    """ 文件接收器 """
    def __init(self):
        pass

    def recv_file(sock):
        """
        接收文件
        """
        # 接收欢迎消息:
        filename = sock.recv(buffsize).decode()
        sock.send(b"Recv filename")

        last_mtime = float(sock.recv(buffsize))
        sock.send(b"Recv last_mtime")

        filesize = int(sock.recv(buffsize))
        sock.send(b"Recv filesize")

        # 接收文件头
        file_info = {"filename": filename, "last_mtime": last_mtime, "file_size": filesize}
        print(file_info)

        # 接收文件
        filename = os.path.basename(filename)
        with open(filename, "wb") as fp:
            recv_size = 0
            print("==> Start receiving file")
            while not recv_size == filesize:
                if filesize - recv_size > buffsize:
                    data = sock.recv(buffsize)
                    recv_size += len(data)
                else:
                    data = socks.recv(filesize - recv_size)
                    recv_size = filesize
                sock.send(b"")
                fp.write(data)
                print(f"Process {round(recv_size/filesize, 4) * 100} %")
            print("==> Receive over")


class FileRecver:
    """ 文件发送器 """
    def __init(self):
        pass

    def send_file(sock, addr, filename):
        """
        TCP连接函数
        :param
            sock: (Socket) 连接对象
            addr: (String) IP地址
            filename: (String) 文件路径
        """
        print('Accept new connection from %s:%s...' % addr)
        
        file_info = get_file_meta(filename)
        filename = file_info["filename"]
        last_mtime = file_info["last_mtime"]
        filesize = file_info["file_size"]
        
        sock.send(filename.encode())
        print(sock.recv(buffsize).decode())
        
        sock.send(str(last_mtime).encode())
        print(sock.recv(buffsize).decode())
        
        sock.send(str(filesize).encode())
        print(sock.recv(buffsize).decode())
        
        # 传输文件
        with open(filename, 'rb') as fp:
            while True:
                data = fp.read(buffsize)
                if not data:
                    print("==> File send over")
                    break
                sock.send(data)
                
            sock.close()
            print('Connection from %s:%s closed.' % addr)