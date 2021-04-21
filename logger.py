import logging

def log_conf(logger_name, log_path):
    # 创建Logger实例
    demo = logging.getLogger(logger_name)
    # 禁止向上一级传播
    demo.propagate = False

    # 日志输出样式
    # 2021-03-09 13:51:23 united_front_news.py[line:65] INFO 数据写入失败,goodsId为:170993398564
    fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    formatter = logging.Formatter(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S')

    # 设置日志输出级别
    demo.setLevel(logging.INFO)

    if not demo.handlers:
        # 文件输出配置
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        demo.addHandler(file_handler)

        # 屏幕输出配置
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        demo.addHandler(console_handler)

    return demo