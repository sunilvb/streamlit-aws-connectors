import streamlit as st
import pandas as pd
import numpy as np
from redshift_connection import RedshiftConnection
st.title('Amazon Redshift Connector Test - by Sunil Vishnubhotla')

conn = st.experimental_connection('pets_db', type=RedshiftConnection)
pet_owners = conn.query('SELECT * FROM dev.public.pets')
st.dataframe(pet_owners)
