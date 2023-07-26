import streamlit as st
import pandas as pd
import numpy as np
from redshift_connection import RedshiftConnection
st.title('Amazon Redshift Connector Test')

conn = st.experimental_connection('pets_db', type=RedshiftConnection)
pet_owners = conn.query('SELECT * FROM sample_data_dev.tickit.users limit 5')
st.dataframe(pet_owners)