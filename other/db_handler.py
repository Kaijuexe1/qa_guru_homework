import psycopg2

class DataBaseHandler():
    def __init__(self,config):
        self.db_name = config.db_name
        self.connection = None
        self.cursor = None

    def _get_connection_params(self):
        if self.db_name == "postgres":
            return {
                "host": self.config.server,
                "database": self.config.database,
                "user": self.config.user,
                "password": self.config.password,
                "port": self.config.port,


            }
        elif self.db_name == "sqlite":
            return {"database": self.config.database}
        else:
            raise ValueError("Поддерживается только Postgres")

    def connect(self):
        params = self._get_connection_params()
        if self.db_name == "postgres":
            self.connection = connector.connect()
        
