import argparse
from pathlib import Path
import multiprocessing
import time

from utils import *
from transporter import FileSender, FileRecver

parser = argparse.ArgumentParser(description='LEFS')
parser.add_argument('--ip', help='ip address of two target machine')


def func_client(ip_addr: str):
    """
    客户端函数
    :param
        ip_addr: (String) ip地址
    """
    logger = create_logger(f"./log/client_log_{ip_addr}.log", logger_name=f"client_logger_{ip_addr}")
    logger.info(f"==> Prepare connect to {ip_addr}")

    while True:
        logger.info(f"Listen to {ip_addr}")
        time.sleep(3)

def func_server(ip_1: str, ip_2: str):
    """
    服务端函数
    :param
        ip_1: (String) ip地址1
        ip_2: (String) ip地址2
    """
    logger = create_logger("./log/server_log.log", logger_name="client_logger")
    logger.info("==> Server is ready")
    while True:
        time.sleep(3)
        update_scan([ip_1, ip_2], logger)



if __name__ == "__main__":
    # Create logger
    logger = create_logger("./log/main_log.log", logger_name="main_logger")

    # 解析参数
    args = parser.parse_args()
    
    ip_list = args.ip.split(',')
    if len(ip_list) != 2:
        logger.error("==> Ip address error, please input two ip addr")
    
    logger.info(f"==> Create TCP connect to {ip_list[0]} & {ip_list[1]}...")  

    # 建立双进程，一个作为服务端检查文件更新
    # 一个作为客户端接收文件更新
    p_client1 = multiprocessing.Process(target=func_client, args=(ip_list[0], ))
    p_client2 = multiprocessing.Process(target=func_client, args=(ip_list[1], ))
    p_server = multiprocessing.Process(target=func_server, args=(ip_list[0], ip_list[1]))

    p_client1.start()
    p_client2.start()
    p_server.start()
    
    
    