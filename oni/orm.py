import psycopg2


class Singleton(object):
    """Singleton base class"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)
        return cls._instance


class ORM(Singleton):
    '''Selfmade an orm class'''
    __CREATED = []

    def __init__(
            self,
            database_conf: dict
            ) -> None:
        """_summary_

        Args:
            database_conf (dict): database settings
        """
        self.database_conf = database_conf
        # Вношу список существующих таблиц в переменную
        with self._get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute("select table_name from information_schema.tables where table_schema = 'public'")  # noqa 501
                self.__CREATED = [i[0] for i in curr.fetchall()]

    def _get_connection(self):
        '''Creating connection with database'''
        conn = psycopg2.connect(**self.database_conf)
        return conn

    def create_tables(self, structure: dict) -> None:
        """_summary_

        Args:
            structure (dict): classical structure of table
            {
                'table_name': 'test_table',
                'variables': ['id', 'name', 'age'],
                'desc': ['serial', 'varchar (128)', 'integer']
            }

        Raises:
            ValueError: occurs if you try to create an existing table
        """
        table_name = structure['table_name']
        if table_name in self.__CREATED:
            raise ValueError('Table already exists')
        elif not structure:
            raise ValueError('Empty structure')
        with self._get_connection() as conn:
            with conn.cursor() as curr:
                table_name = structure['table_name']
                variables = structure['variables']
                desc = structure['desc']
                v = ', '.join([i + ' ' + j for i, j in zip(variables, desc)])
                request = f'create table {table_name} ({v})'
                curr = conn.cursor()
                curr.execute(request)

    def select(self, params: list[str], table: str) -> list[str]:
        """_summary_

        Args:
            params (list[str]): list of requires
            table (str): name of a table

        Returns:
            list[str]: query result
        """
        with self._get_connection() as conn:
            with conn.cursor() as curr:
                # Соединяю нужные столбцы, чтоб сделать запрос к бд
                params = ', '.join(params) if params else '*'
                curr.execute(f"select {params} from {table}")
                # Возвращаю списком
                result = list(map(list, curr.fetchall()))
                return result

    def insert(self, params: dict, table: str) -> None:
        """_summary_

        Args:
            params (dict): A list of keys and values that you want
            to insert into a table
            table (str): A name of table
        """        
        with self._get_connection() as conn:
            with conn.cursor() as curr:
                dict_keys = ', '.join(params.keys())
                vals = []
                for i in params.values():
                    if i[0].isalpha():
                        i = '\'' + i + '\''
                    vals.append(i)

                vals = ', '.join(vals)
                query = f'insert into {table} ({dict_keys}) values ({vals})'
                curr.execute(query)

    def update(self, params: dict, table: str, where: dict) -> None:
        """_summary_

        Args:
            params (dict): A list of keys and values that you want
            to change in a table
            table (str): Name of a table
            where (dict): Condition
        """
        with self._get_connection() as conn:
            with conn.cursor() as curr:
                params = [' = '.join([key, str(val)]) for key, val in params.items()]  # noqa 501
                params = ', '.join(params)
                wh = [' = '.join([key, str(val)]) for key, val in where.items()]  # noqa 501
                wh = ', '.join(wh)
                query = f'update {table} set {params} where {wh}'
                curr.execute(query)

    def delete(self, params: dict, table: str) -> None:
        """_summary_

        Args:
            params (dict): _description_
            table (str): Name of a table

        Raises:
            ValueError: _description_
        """
        if params:
            with self._get_connection() as conn:
                with conn.cursor() as curr:
                    # Соединяю нужные столбцы, чтоб сделать запрос к бд
                    params = [' = '.join([key, str(val)]) for key, val in params.items()]  # noqa 501
                    query = ', '.join(params)
                    curr.execute(f"delete from {table} where {query}")
        else:
            raise ValueError('Empty request')


DB_SETTINGS = {
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}
