from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

import redshift_connector
import pandas as pd
from streamlit.logger import get_logger

logger = get_logger(__name__)



class RedshiftConnection(ExperimentalBaseConnection[redshift_connector.Connection]):
    """Basic st.experimental_connection implementation for Amazon Redshift"""

    def _connect(self, **kwargs) -> redshift_connector.Connection:
        logger.info("****** Inside _connect *****")
        
        if 'database' in kwargs:
            db = kwargs.pop('database')
        else:
            db = self._secrets['database']

        if 'user' in kwargs:
            uu = kwargs.pop('user')
            logger.info("****** got user in kwargs *****")
        else:
            uu = self._secrets['user']
            logger.info("****** got user in _secrets *****")

        if 'password' in kwargs:
            pp = kwargs.pop('password')
            logger.info("****** Inside _connect in kwargs *****")
        else:
            pp = self._secrets['password']
            logger.info("****** got password in _secrets *****")

        return redshift_connector.connect(database=db, user=uu, password=pp, **kwargs)
    
    def cursor(self) -> redshift_connector.connect:
        return self._instance.cursor()

    def query(self, query: str, ttl: int = 3600, **kwargs) -> pd.DataFrame:
        @cache_data(ttl=ttl)
        def _query(query: str, **kwargs) -> pd.DataFrame:
            cursor = self.cursor()
            cursor.execute(query, **kwargs)
            return cursor.df()
        
        return _query(query, **kwargs)