import random
import time


class sleeper:
    @classmethod
    def short(cls) -> None:
        """interval: [0.2, 1.5]"""
        from_ = 0.2
        to_ = 1.5

        rnd = random.random()
        time.sleep(rnd * (to_ - from_) + from_)

    @classmethod
    def medium(cls) -> None:
        """interval: [1.5, 3]"""
        from_ = 1.5
        to_ = 3

        rnd = random.random()
        time.sleep(rnd * (to_ - from_) + from_)

    @classmethod
    def medium_long(cls) -> None:
        """interval: [3.5, 5]"""
        from_ = 3.5
        to_ = 5

        rnd = random.random()
        time.sleep(rnd * (to_ - from_) + from_)

    @classmethod
    def long(cls) -> None:
        """interval: [5, 6.5]"""
        from_ = 5
        to_ = 6.5

        rnd = random.random()
        time.sleep(rnd * (to_ - from_) + from_)
