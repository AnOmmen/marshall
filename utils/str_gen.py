from random import randrange


class StrGen:

    _mistake_inj = ['whoops', 'oopsy', 'uh-oh', 'yikes', 'meow', 'er', 'shucks']
    _mistake_inj_num = len(_mistake_inj)

    @staticmethod
    def mistake_inj() -> str:
        return StrGen._mistake_inj[randrange(StrGen._mistake_inj_num)]
