import pandas as pd
from ibis import impala
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import datetime as dt
import random
import numpy as np


user = "p_ds"
password = "genios"
host = 'bda1agea03.agea.sa'
port = 21050
client = impala.connect(host=host, port=port, user=user, password=password) 



# Funcion para traer cuantas altas genero una nota.
def traer_altas(content_id,start_date, end_date):
    '''
    Se inserta un content_id, busca todos los pases_id que se suscribieron el mismo dia en el que chocaron con el paywall viendo la nota seleccionada.
    De estos usuarios, se descarta a los usuarios que se suscribieron ANTES de chocar con el paywall. 
    '''


# Creamos el query
    query =  f'''

    SELECT DISTINCT pase_id
    FROM hd_p_vw.vw_navegacion_analytics AS a
    WHERE day_partition between '{start_date}' AND '{end_date}'
    AND page_url LIKE '%bienvenida%'
    AND dataset = 'Clarín'
    AND page_type = 'OTROS'
    AND EXISTS ( SELECT 1
                FROM hd_p_vw.vw_navegacion_analytics AS b
                WHERE page_url LIKE '%{content_id}%'
                AND pase_id > 0
                AND page_type = 'OTROS'
                AND a.pase_id = b.pase_id
                AND a.day_partition = b.day_partition )
    

       '''


    altas_con_nota = client.sql(query).execute(limit=None)

    todos = altas_con_nota.pase_id.to_list()


    query =  f'''

    SELECT pase_id,tipo, day_partition,f_minute, RANK() OVER (PARTITION BY pase_id ORDER BY day_partition, f_hour, f_minute) as rank
    FROM
    (SELECT pase_id,day_partition,f_hour,f_minute,page_url, 
    CASE WHEN page_url LIKE '%{content_id}%' THEN 'nota' else 'bienvenida' END as tipo
    FROM hd_p_vw.vw_navegacion_analytics 
    WHERE day_partition between '{start_date}' AND '{end_date}'
    AND dataset = 'Clarín'
    AND pase_id IN {tuple(todos)}
    AND page_type = 'OTROS'
    AND (page_url LIKE '%{content_id}%' or page_url LIKE '%bienvenida%')
    GROUP BY 1,2,3,4,5) AS a
        '''

    if len(todos) > 1:     # <--- activamos el query solo si hay mas de un pase_id suscripto
        bienvenida_vs_notas = client.sql(query).execute(limit=None)
    
        altas = bienvenida_vs_notas.pivot_table(index='pase_id', columns='tipo', values='rank',aggfunc=np.min).reset_index()


        def es_alta(df):

            bienvenida = df.bienvenida.values
            notas = df.nota.values

            es_alta = []

            for bienv, nota in zip(bienvenida,notas):

                if nota - bienv == 1:                             # <--- Si se suscribe INMEDIATAMENTE antes de leer la nota, le damos una probabilidad de 50% de que sea suscripto POR la nota
                    if random.uniform(1,0) > 0.5:
                        es_alta.append(1)
                    else:
                        es_alta.append(0)
                elif bienv - nota < 0:                            # <--- Si se suscribe ANTES de leer la nota, lo descartamos.
                    es_alta.append(0)
                else:
                    es_alta.append(1)

            df['es_alta'] = es_alta

            return df



        altas = es_alta(altas)
    
        return altas.es_alta.sum()
    else:
        return 0


# La funcion traer_info nos trae cuantas pageview tuvo la nota, cuantos usuarios registrados la leyeron, 
# cuantos usuarios suscriptos la leyeron y cuantos Choques tuvo la nota.

def traer_info(autor,start_date,end_date):
    '''
    Insertamos un autor y un periodo, para traer la info de todas las notas publicadas del mismo.
    '''


    queri =    f'''

    SELECT content_id, author_name AS autor, title, section_1 AS seccion, tag1, to_date(publish_date) as fecha
    FROM hd_p_vw.vw_notas_cms
    WHERE to_date(publish_date) between '{start_date}' AND '{end_date}'
    AND author_name = '{autor}'
    
                  '''

    global notas_autor

    notas_autor = client.sql(queri).execute(limit=None)

    content_id_lista = notas_autor.content_id.to_list()   # <-- lista de todos los content_id

    notas_autor_lista = notas_autor.title.to_list()  # <-- Lista de todos los títulos


    valores_nota = []

    for content_id in content_id_lista:

        suscriptores = f'''

            SELECT COUNT(distinct page_visit_header) as cookies, COUNT(distinct pase_id) as usuarios
            FROM hd_p_vw.vw_navegacion_analytics AS a
            WHERE day_partition between '{start_date}' AND '{end_date}'
            AND content_id = '{content_id}'
            '''
        
        cantidad_usuarios = client.sql(suscriptores).execute(limit=None)   # <-- query busca la cantidad de pageviews totales, y la cantidad de pases registrados

                        
        suscriptores += '''
                        AND EXISTS ( SELECT 1
                            FROM hd_p_vw.vw_pase_usuario_bp AS b
                            WHERE flag_suscriptor = 'Si'
                            AND a.pase_id = b.p_id_usuario)
                        '''
                
                
        cantidad_usuarios_suscriptos = client.sql(suscriptores).execute(limit=None)  # <-- agrega al query anterior para obtener los usuarios suscriptos

        query_choques =  f'''

            SELECT COUNT( DISTINCT pase_id ) as choques
            FROM hd_p_vw.vw_navegacion_analytics AS a
            WHERE day_partition between '{start_date}' AND '{end_date}'
            AND page_url LIKE '%{content_id}%'
            AND dataset = 'Clarín'
            AND page_type = 'OTROS'

            '''


        cantidad_choques = client.sql(query_choques).execute(limit=None)    # <--- la cantidad de usuarios que tuvo al menos un choque en esa nota
            

                    
    
        pageviews = cantidad_usuarios.iloc[0,0]
        cantidad_pases = cantidad_usuarios.iloc[0,1]
        suscriptos = cantidad_usuarios_suscriptos.iloc[0,0]
        choques = cantidad_choques.iloc[0,0]
        altas = traer_altas(content_id, start_date, end_date)    # <-- agregamos las altas de la nota

        valores_nota.append((pageviews,cantidad_pases, suscriptos,choques, altas))

        

    tabla_info = pd.DataFrame(valores_nota, columns=['PageViews', 'Usuarios', 'Suscriptos','Choques', 'Altas'])
    tabla_info['content_id'] = content_id_lista
    df = notas_autor.merge(tabla_info, on=['content_id'])



    return df