from psycopg2 import connect


class Singleton(object):
    """Singleton base class"""
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class Orm(Singleton):
    '''Selfmade an orm class'''
    def __init__(
            self,
            database_conf: dict
            ) -> None:
        self.database_conf = database_conf

    def select(self):
        '''Simple select query'''
        pass
