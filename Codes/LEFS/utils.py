import logging
from pathlib import Path
import os


def create_logger(path, logger_name='default_logger'):
    """
    Logger创建函数
    :param
        name: (String) Logger创建路径
        logger_name: (String) Logger名，默认'default_logger'
    :return:
        logger: (Logger) 日志
    """
    # 创建一个logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(path)
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    formatter = logging.Formatter(
        '[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger


# 获取文件的META信息
def get_file_meta(filename: str):
    """
    获取文件meta信息函数
    :param
        filename: (String) File name and path
    :return:
        file_meta: (dict):
            filename: (String) path of file
            last_mtime: (Float) last modified time
            file_size: (Int) size of file
    """
    last_mtime = os.path.getmtime(filename)
    file_size = os.path.getsize(filename)
    file_meta = {"filename": filename, "last_mtime": last_mtime, "file_size": file_size}
    
    return file_meta


def check_share_info(share_path: str="./Share"):
    """
    遍历Share目录下的所有文件并检查其META信息
    :param
        share_path: (String) /Share目录的路径，默认为"./Share"
    :return
       file_info: (List[String]) /Share目录的所有文件记录列表
    """
    # 遍历目录下的所有文件
    file_info = []

    for root, dirs, files in os.walk(share_path):
        for name in files:
            path = os.path.join(root, name)
            file_info.append(get_file_meta(path))
    return file_info


def write_share_info(file_info: str, file_info_w: list):
    """
    记录Share目录下所有文件的META信息
    :param
        file_info: (String) 文件信息日志的地址
        file_info_w: (List[String]) 文件信息记录列表，包含了/Share目录下的所有文件meta信息
    """
    with open(file_info, "w") as f:
        for line in file_info_w:
            f.write(str(line)+'\n')


def update_scan(ip_list: list, logger):
    """
    文件更新扫描函数，用于周期性检查/Share目录下的文件变化
    :param
        ip_list: (List[String]) ip地址列表，包含两个需要发送更新的目标ip地址
        logger: (Logger) 日志对象
    """
    # 检查是否存在 file_info, 如果不存在则初始化，如果存在则读取之前记录的文件META信息
    file_info = Path("./log/file_info.log")
    if not file_info.is_file():
        # 获取现在的文件META信息 并写入文件
        file_info_w = check_share_info()
        write_share_info(file_info, file_info_w)
        logger.warning("==> Can not find meta info, init the file_info.log")
    else:
        file_info_r = []
        with open("./log/file_info.log", "r") as f:
            for line in f.readlines():
                file_info_r.append(eval(line))

        # 获取现在的文件META信息
        file_info_w = check_share_info()
    
        # 对比两个META信息检查是否有文件变化
        if file_info_r == file_info_w:
            pass
        else:
            logger.info("==> Found update, prepare to send new files")

            # ToDo 通知其他的伙伴
            logger.info(f"==> Send update to {ip_list[0]}")
            logger.info(f"==> Send update to {ip_list[1]}")

            # 并传递文件更新，然后

            # 更新文件META信息
            write_share_info(file_info_w)