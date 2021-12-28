import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date
import numpy as np
from funciones_app import *
from funciones_plot import *


# Listas para utilizar despues

radio_items = ['PageViews', 'Usuarios', 'Suscriptos','Choques', 'Altas']
columnas_tabla = ['Título', 'Publicación', 'Sección', 'Tema']


# Iniciamos la app

app = dash.Dash(
    __name__,
    external_stylesheets=[ dbc.themes.LITERA ]
                )


app.title = 'Dash Autores Analytics'


# Creamos la arquitectura

app.layout = dbc.Container([

    dbc.Spinner(color="primary",  #<--- Bootstrap para cuando tiene que cargar algo de lo que esta adentro de Children
                type="grow",    #<--- Tipos de animaciones 
                children=[

    dbc.Row(
            html.H1('Autor Analytics', className='text-primary mb-4'),  #<--- título
                    justify='center', #<-- Style para que quede centrado en la pagina
            ),
    
    dbc.Row(
        dbc.Col(
            html.Div('Seleccione un periodo:'),
                    className='text-center text-primary mb-4'
                    )
                
            ),

    dbc.Row(
        dbc.Col(
            dcc.DatePickerRange(                  # <--- Para seleccionar las fechas
                    id='my-date-picker-range',
                    end_date=date(2020, 12, 31),
                    start_date=date(2020,12,1),
                    min_date_allowed=date(2017, 1, 1),
                    max_date_allowed=date(2021, 4, 1),
                    display_format='D MMM , YYYY')
                ,className='text-center mb-4'
                )
            ),
    
    dbc.Row(
        dbc.Col(               # <---- Botón para comenzar a correr la función
            dbc.Button(
                    "Analizar",
                    id='button', 
                    color="primary", 
                    size='lg'),
                className='text-center mb-3')
            ),
    
    dbc.Row([ 
        dbc.Col([

            dbc.Input(id="input_1",                   #<--- input para escribir el primer autor
                        type="text", 
                        value='Alejandro Borensztein', 
                        className='text-center'),

            dash_table.DataTable(                     #<--- df para el primer autor
                        id='datatable1',
                        page_size=6,
                        style_cell_conditional=[
                            {'if': {'column_id': i},'textAlign': 'left'} for i in columnas_tabla],
                        style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0},
                        sort_action="native",
                        sort_mode="multi",
                        row_selectable="multi",
                        row_deletable=False,
                        selected_rows=[])
                ],className='text-center mb-4'
                ),
        
        dbc.Col([

            dbc.Input(id="input_2",                     #<--- input para escribir el segundo autor
                        value='Eduardo Paladini',
                        type="text", 
                        className='text-center'),

            dash_table.DataTable(                       #<--- df para el segundo autor
                        id='datatable2',
                        page_size= 6,
                        style_cell_conditional=[
                            {'if': {'column_id': i},'textAlign': 'left'} for i in columnas_tabla],
                        style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0},
                        tooltip_duration=None,
                        sort_action="native",
                        sort_mode="multi",
                        row_selectable="multi",
                        row_deletable=False,
                        selected_rows=[],
                        fixed_rows={ 'headers': True, 'data': 0 },
                        virtualization=False,
                        page_action='none')
                ],className='text-center mb-4')
        ]),

            
    dbc.Row([
            html.Br(),html.Br()   # <--- espacio
            ]),

    dbc.Row([
        dbc.Col([                 # <--- Primera columna para insertar las cards

                dbc.CardGroup([
                
                    dbc.Card([
                        html.H3('PageViews', className='card-title'),
                        html.H4(id='pageviews1', className='card-text'),
                        ],className='mini_container'),

                    dbc.Card([
                        html.H3('Suscriptos', className='card-title'),
                        html.H4(id='suscriptos1', className='card-text'),
                    ],className='mini_container') 
                            ]),

                dbc.CardGroup([

                    dbc.Card([
                        html.H3('Usuarios', className='card-title'),
                        html.H4(id='usuarios1', className='card-text'),
                    ],className='mini_container'),

                    dbc.Card([
                        html.H3('Choques', className='card-title'),
                        html.H4(id='choques1', className='card-text'),
                    ],className='mini_container') 
                            ]),

                dbc.Card([
                    html.H2('Altas', className='card-title'),
                    html.H3(id='altas1', className='card-text'),
                ],className='mini_container'),
                
        ],className='text-center mr-4'   # <--- Clase para la primer columna
        ),
        
        dbc.Col([               # <--- Segunda columna para insertar las cards

            dbc.CardGroup([
                                
                dbc.Card([
                    html.H3('PageViews', className='card-title'),
                    html.H4(id='pageviews2', className='card-text')
                ],className='mini_container'),

                dbc.Card([
                    html.H3('Suscriptos', className='card-title'),
                    html.H4(id='suscriptos2', className='card-text'),
                ],className='mini_container') 
                        ]),
            
            dbc.CardGroup([

                dbc.Card([
                    html.H3('Usuarios', className='card-title'),
                    html.H4(id='usuarios2', className='card-text'),
                ],className='mini_container'),

                dbc.Card([
                    html.H3('Choques', className='card-title'),
                    html.H4(id='choques2', className='card-text'),
                ],className='mini_container') 
                        ]),

            dbc.Card([
                html.H2('Altas', className='card-title'),
                html.H3(id='altas2', className='card-text'),
            ],className='mini_container'),
                            
        ],className='text-center mr-4'          # <--- Clase para la segunda columna
        )
                                    
    ],no_gutters=True, justify='around'),

    dbc.Row([
            html.Br()
            ]),
]),
    dbc.Row(                         # <--- Boton para crear los graficos
        dbc.Col(
            dbc.Button("Crear Gráficos",
                               id='button2',
                               color="primary", 
                               className="mr-1",
                               size='lg'),
                    className='text-center mb-3')),

    dbc.Row(                        # <--- radio items para modificar los gráficos
        dbc.Col(
        dcc.RadioItems(id='radio_item',
                        options=[
                        {'label': i, 'value': i} for i in radio_items], # 'radio_items' es la lista creada arriba
                       value='PageViews',
                       labelStyle={'display': 'inline-block', 'font-weight': 'bold', 'padding': '6px 7px'},),
                 className='text-center mb-4')
            ),

    dbc.Row([           # En esta fila insertamos los dos primeros graficos
        dbc.Col(
            dcc.Graph(id='grafico1'), className='graf_container'),

        dbc.Col(
            dcc.Graph(id='grafico2'), className='graf_container')
            ]),

    dbc.Row(
        html.Br()
        ),
    
    dbc.Row(               # <--- Dejamos una fila para insertar los nombres de los autores para comparar
        dbc.Col(
            html.H3(id='vs',children='vs.'),
                className='text-center text-primary mb-4',
                width={'size':12},
            ),className='text-center mr-4'),

    dbc.Row(                # <--- Insertamos el tercer grafico
        dbc.Col(
            dcc.Graph(id='grafico3'), className='graf_container')
        ),

    dbc.Row([
            html.Br(),html.Br()
            ]),
    
]) 

#---------------------------------------------------------------------------------------#
#Configuramos los decoradores#


# El primer decorador, obtiene los valores de los autores seleccionados, y el rango de fechas.
# Pero para comenzar a activar la funcion, es necesario hacer click en el boton 'analizar'.
# Los outputs de este decorador son las tablas para cada autor. Donde cada tabla necesita el nombre de sus
# columnas y un diccionario que le pase la 'data'. Ademas, le pasamos los datos para el component_property
# 'tooltip_data', que nos permite pasar el mouse por arriba del texto y que nos muestre el texto completo.

@app.callback([
     dash.dependencies.Output(component_id='datatable1',component_property= 'columns'),
     dash.dependencies.Output(component_id='datatable1',component_property= 'data'),
     dash.dependencies.Output(component_id='datatable2',component_property= 'columns'),
     dash.dependencies.Output(component_id='datatable2',component_property= 'data'),
     dash.dependencies.Output(component_id='datatable1',component_property= 'tooltip_data'),
     dash.dependencies.Output(component_id='datatable2',component_property= 'tooltip_data'),
     dash.dependencies.Output(component_id='vs',component_property= 'children')],  # <--- pasa el nombre de los autores seleccionados
    [dash.dependencies.Input(component_id='button',component_property= 'n_clicks'),
     dash.dependencies.State(component_id='input_1',component_property= 'value'),
     dash.dependencies.State(component_id='input_2',component_property= 'value'),
     dash.dependencies.State('my-date-picker-range', 'start_date'),
     dash.dependencies.State('my-date-picker-range', 'end_date')
     ],prevent_initial_call=True)
def update_app(n,autor1,autor2,start_date,end_date):

    global df1                                              # <--- hacemos los df globales asi podemos usarlos en otras funciones
    df1 = traer_info(autor1, start_date, end_date)

    global df2
    df2 = traer_info(autor2, start_date, end_date)


    df1_to_show = df1[['title','fecha','seccion','tag1']]
    df1_to_show.columns = ['Título', 'Publicación', 'Sección', 'Tag']
    columns1 = [{'name': col, 'id': col} for col in df1_to_show.columns]
    data1 = df1_to_show.to_dict(orient='records')

    df2_to_show = df2[['title','fecha','seccion','tag1']]
    df2_to_show.columns = ['Título', 'Publicación', 'Sección', 'Tag']
    columns2 = [{'name': col, 'id': col} for col in df2_to_show.columns]
    data2 = df2_to_show.to_dict(orient='records')

    tooltip_data1=[{column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                    } for row in df1_to_show.to_dict('records')]

    tooltip_data2=[{column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                    } for row in df2_to_show.to_dict('records')]


    return columns1,data1,columns2,data2,tooltip_data1,tooltip_data2,f'{autor1} vs. {autor2}'

# El segundo callback, obtiene las filas seleccionadas de la tabla, y devuelve la informacion dentro de las cartas.
# Establecemos que si no se selecciona ninguna fila, los valores de las cartas seran los totales de cada usuario.
# Ademas, para cada valor, se le asigna un color. Rojo si el valor es menor que el del autor a comparar, y verde si es mayor.

@app.callback(
    [dash.dependencies.Output(component_id='pageviews1',component_property= 'children'),
     dash.dependencies.Output(component_id='pageviews1',component_property= 'className'),
     dash.dependencies.Output(component_id='suscriptos1',component_property= 'children'),
     dash.dependencies.Output(component_id='suscriptos1',component_property= 'className'),
     dash.dependencies.Output(component_id='usuarios1',component_property= 'children'),
     dash.dependencies.Output(component_id='usuarios1',component_property= 'className'),
     dash.dependencies.Output(component_id='choques1',component_property= 'children'),
     dash.dependencies.Output(component_id='choques1',component_property= 'className'),
     dash.dependencies.Output(component_id='altas1',component_property= 'children'),
     dash.dependencies.Output(component_id='altas1',component_property= 'className'),
     dash.dependencies.Output(component_id='pageviews2',component_property= 'children'),
     dash.dependencies.Output(component_id='pageviews2',component_property= 'className'),
     dash.dependencies.Output(component_id='suscriptos2',component_property= 'children'),
     dash.dependencies.Output(component_id='suscriptos2',component_property= 'className'),
     dash.dependencies.Output(component_id='usuarios2',component_property= 'children'),
     dash.dependencies.Output(component_id='usuarios2',component_property= 'className'),
     dash.dependencies.Output(component_id='choques2',component_property= 'children'),
     dash.dependencies.Output(component_id='choques2',component_property= 'className'),
     dash.dependencies.Output(component_id='altas2',component_property= 'children'),
     dash.dependencies.Output(component_id='altas2',component_property= 'className')],
    [dash.dependencies.Input('datatable1', 'selected_rows'),
     dash.dependencies.Input('datatable2', 'selected_rows')]
     ,prevent_initial_call=True)
def update_info(rows1, rows2):
    

    global df1_p
    global df2_p

    if len(rows1) == 0:                 # <--- Modificamos el df, para tener solo los datos de las filas seleccionadas.
        df1_p = df1
    else:
        df1_p = df1[df1.index.isin (rows1)]

    if len(rows2) == 0:
        df2_p = df2
    else:
        df2_p = df2[df2.index.isin (rows2)]

 

    pageviews1 = df1_p.PageViews.sum()
    pageviews2 = df2_p.PageViews.sum()

    usuarios1 = df1_p.Usuarios.sum()
    usuarios2 = df2_p.Usuarios.sum()

    suscriptos1 = df1_p.Suscriptos.sum()
    suscriptos2 = df2_p.Suscriptos.sum()

    choques1 = df1_p.Choques.sum()
    choques2 = df2_p.Choques.sum()

    altas1 = df1_p.Altas.sum()
    altas2 = df2_p.Altas.sum()

    if suscriptos1 > suscriptos2:                      # <-- vemos que valor es mayor y le asignamos el color
        s_suscr1 = 'font-weight-bold text-success'
        s_suscr2 = 'font-weight-bold text-danger'
    else:
        s_suscr1 = 'font-weight-bold text-danger'
        s_suscr2 = 'font-weight-bold text-success'

    if pageviews1 > pageviews2:
        s_pageviews1 = 'font-weight-bold text-success'
        s_pageviews2 = 'font-weight-bold text-danger'
    else:
        s_pageviews1 = 'font-weight-bold text-danger'
        s_pageviews2 = 'font-weight-bold text-success'

    if usuarios1 > usuarios2:
        s_pases1 = 'font-weight-bold text-success'
        s_pases2 = 'font-weight-bold text-danger'
    else:
        s_pases1 = 'font-weight-bold text-danger'
        s_pases2 = 'font-weight-bold text-success'
    
    if choques1 > choques2:
        s_choques1 = 'font-weight-bold text-success'
        s_choques2 = 'font-weight-bold text-danger'
    else:
        s_choques1 = 'font-weight-bold text-danger'
        s_choques2 = 'font-weight-bold text-success'
    
    if altas1 > altas2:
        s_altas1 = 'font-weight-bold text-success'
        s_altas2 = 'font-weight-bold text-danger'
    else:
        s_altas1 = 'font-weight-bold text-danger'
        s_altas2 = 'font-weight-bold text-success'


    return f'{pageviews1}',s_pageviews1,f'{suscriptos1}',s_suscr1, f'{usuarios1}',s_pases1, f'{choques1}',s_choques1, f'{altas1}', s_altas1, \
        f'{pageviews2}',s_pageviews2,f'{suscriptos2}',s_suscr2, f'{usuarios2}',s_pases2, f'{choques2}',s_choques2, f'{altas2}', s_altas2, 


# El tercer callback, tiene como inputs los nombres de los autors, las filas seleccionadas de la tabla, el valor del
# radio_item y si se clickeo o no el boton.
# Devuelve los graficos actualizados. 

@app.callback(
    [dash.dependencies.Output(component_id='grafico1',component_property= 'figure'),
     dash.dependencies.Output(component_id='grafico2',component_property= 'figure'),
     dash.dependencies.Output(component_id='grafico3',component_property= 'figure')],
    [dash.dependencies.Input(component_id='button2',component_property= 'n_clicks'),
     dash.dependencies.Input(component_id='radio_item',component_property= 'value'),
     dash.dependencies.State('datatable1', 'selected_rows'),
     dash.dependencies.State('datatable2', 'selected_rows'),
     dash.dependencies.State(component_id='input_1',component_property= 'value'),
     dash.dependencies.State(component_id='input_2',component_property= 'value')]
     ,prevent_initial_call=True)
def update_chart(n,value,rows1,rows2,autor1,autor2):


    fig1 = barchart(df1,value,rows1,autor1)
    fig2 = barchart(df2,value,rows2,autor2)
    fig3 = subplot(df1_p,df2_p,autor1,autor2)


    return fig1,fig2,fig3



if __name__ == '__main__':
    app.run_server(debug=True)