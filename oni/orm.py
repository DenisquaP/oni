import psycopg2


class Singleton(object):
    """Singleton base class"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class BaseManager:
    '''Selfmade an orm class'''
    __CREATED = []

    def __init__(
            self,
            database_conf: dict
            ) -> None:
        self.database_conf = database_conf
        # Вношу список существующих таблиц в переменную
        conn = self._get_connection()
        curr = conn.cursor()
        curr.execute("select table_name from information_schema.tables where table_schema = 'public'")  # noqa 501
        self.__CREATED = [i[0] for i in curr.fetchall()]

    def _get_connection(self):
        '''Creating connection with database'''
        conn = psycopg2.connect(**self.database_conf)
        return conn

    def create_tables(self, structure: dict) -> None:
        table_name = structure['table_name']
        if table_name in self.__CREATED:
            assert ValueError('Table already exists')
        conn = self._get_connection()
        table_name = structure['table_name']
        variables = structure['variables']
        desc = structure['desc']
        v = ', '.join([i + ' ' + j for i, j in zip(variables, desc)])
        request = f'create table {table_name} ({v})'
        curr = conn.cursor()
        curr.execute(request)
        conn.commit()

    def select(self, params, table):
        '''Simple select query'''
        conn = self._get_connection()
        curr = conn.cursor()
        # Соединяю нужные столбцы, чтоб сделать запрос к бд
        params = ', '.join(params) if params else '*'
        curr.execute(f"select {params} from {table}")
        # Возвращаю списком
        result = list(map(list, curr.fetchall()))
        return result


class MetaModel(type):
    manager_class = BaseManager

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()


class BaseModel(metaclass=MetaModel):
    table_name = ""


DB_SETTINGS = {
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

a = BaseManager(DB_SETTINGS)
# print(a.create_tables({'tablename': 'bd'}))
print(a.select([], table='ks'))
