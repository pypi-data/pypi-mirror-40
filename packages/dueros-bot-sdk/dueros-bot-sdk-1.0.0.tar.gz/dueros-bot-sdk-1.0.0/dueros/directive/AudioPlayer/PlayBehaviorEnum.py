# encoding: utf8

from enum import Enum, unique


@unique
class PlayBehaviorEnum(Enum):
    REPLACE_ALL = 'REPLACE_ALL'
    REPLACE_ENQUEUED = 'REPLACE_ENQUEUED'
    ENQUEUE = 'ENQUEUE'


    @staticmethod
    def inEnum(playBehavior):
        return playBehavior in PlayBehaviorEnum.__members__.values()

    pass


if __name__ == '__main__':
    print(PlayBehaviorEnum.REPLACE_ALL.value)