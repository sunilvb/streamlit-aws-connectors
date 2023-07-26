from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

import redshift_connector
import pandas as pd

class RedshiftConnection(ExperimentalBaseConnection[redshift_connector.Connection]):
    """Basic st.experimental_connection implementation for Amazon Redshift"""

    def _connect(self, **kwargs) -> redshift_connector.Connection:
        if 'database' in kwargs:
            db = kwargs.pop('database')
        else:
            db = self._secrets['database']
        return redshift_connector.connect(database=db, **kwargs)
    
    def cursor(self) -> redshift_connector.connect:
        return self._instance.cursor()

    def query(self, query: str, ttl: int = 3600, **kwargs) -> pd.DataFrame:
        @cache_data(ttl=ttl)
        def _query(query: str, **kwargs) -> pd.DataFrame:
            cursor = self.cursor()
            cursor.execute(query, **kwargs)
            return cursor.df()
        
        return _query(query, **kwargs)