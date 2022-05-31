import time
import logging


def run_time_wrapper(outer_args):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(str(outer_args))

    def outer(func):
        """
        :param func: 传入一个函数
        :return:
        """

        def inner(*args, **kwargs):
            start_time = time.time()
            ret = func(*args, **kwargs)
            end_time = time.time()
            logger.info("%s接口任务耗时 %.2f秒" % (outer_args, end_time - start_time))
            return ret
        return inner
    return outer


class Haha:
    @run_time_wrapper
    def addok(self):
        print("hello")
        # print(type())
        return "addok"


if __name__ == '__main__':
    a = Haha()
    print(a.addok(), type(a.addok))
