import time
import logging

# 分配位置
WORKER_BITS = 5
DATACENTER_BITS = 5
SEQUENCE_BITS = 12

# 设定设备数量上限
WORKER_UPPER_LIMIT = -1 ^ (-1 << WORKER_BITS)
DATACENTER_UPPER_TIMIT = -1 ^ (-1 << DATACENTER_BITS)


# 组合是的位运算偏移量
WORKER_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_BITS + DATACENTER_BITS

SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)  # 掩码
EPOCH = 1577808001000  # 元时间戳 此处元设为 2020-01-01 00:00:01


class SnowFlake(object):

    def __init__(self, data_center_id, worker_id, sequence=0):
        """
        :param data_center_id: 数据中心编号
        :param worker_id: 机器编号
        :param sequence: 序号
        """
        if worker_id > WORKER_UPPER_LIMIT:
            raise ValueError("WORKER ID 高于上限")
        if worker_id < 0:
            raise ValueError("WORKER ID 低于下限")
        if data_center_id > DATACENTER_UPPER_TIMIT:
            raise ValueError("DATA CENTER ID 高于上限")
        if data_center_id < 0:
            raise ValueError("DATA CENTER ID 低于上限")
        self.worker_id = worker_id
        self.datacenter_id = data_center_id
        self.sequence = sequence

        self.last_timestamp = -1  # 最近一次生成编号的时间戳

    @staticmethod
    def _timestamp(n=1e3) -> int:
        """指定位数时间戳
        :param n:
        :return:
        """
        return int(time.time() * n)

    def _check(self, timestamp):
        """
        超限检查
        :param timestamp:
        :return:
        """
        self._time_back_off_check(timestamp)
        self._number_check(timestamp)

    def _number_check(self, timestamp):
        """
        数超限检查，检查当前时间生成的编号是否超过上限，超过上限则的等到下一个时间生成
        :param timestamp:
        :return:
        """
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._wait_next_time(self.last_timestamp)
        else:
            self.sequence = 0

    def _time_back_off_check(self, timestamp):
        if timestamp < self.last_timestamp:
            logging.error('发现时钟回退，记录到最近一次的时间戳为 {}'.format(self.last_timestamp))
            raise Exception("时钟回拨异常")

    def task(self) -> int:
        """
        获取一个编号
        :return:
        """
        timestamp = self._timestamp()
        self._check(timestamp)
        self.last_timestamp = timestamp
        return self._generate(timestamp)

    def _generate(self, timestamp) -> int:
        """ 生成一个编号
        :param timestamp:
        :return:
        """
        number = ((timestamp - EPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.datacenter_id << DATACENTER_ID_SHIFT) | (
                    self.worker_id << WORKER_SHIFT) | self.sequence
        return number

    def _wait_next_time(self, last_timestamp):
        """等到下一次单位时间
        :param last_timestamp:
        :return:
        """
        timestamp = self._timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._timestamp()
        return timestamp