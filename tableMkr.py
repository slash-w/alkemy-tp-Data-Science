import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2


def add_table(df, psqltable):
    # Crea y se conecta al engine de SQLAlchemy
    engine = create_engine("postgresql://postgres:123@localhost:5432/datosCulturaArg")
    psqlcon = engine.connect()

    try:
        # Transforma el dataframe a nuestra tabla de SQL
        df.to_sql(name=psqltable, con=psqlcon, index=False)
    # En caso de que algo saliera mal, que lo muestre por consola
    except ValueError as vx:
        print(vx)
    except Exception as ex:
        print(ex)
    else:
        print('Tabla', psqltable, 'generada')
    finally:
        psqlcon.close()

