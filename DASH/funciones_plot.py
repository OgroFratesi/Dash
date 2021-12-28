import plotly.graph_objects as go   
import pandas as pd
from plotly.subplots import make_subplots




def barchart(df,checklist,rows,autor1):
    '''
    Creamos un barchart con los titulos de las notas y la cantidad total seleccionada en el checklist. Pasamos las filas seleccionadas
    para resaltar su color en el barchart.
    '''

    
    valor = df[checklist]   # <-- tomamos el valor del checklist

    titulos = []            # Si el titulo es muy largo lo acortamos.
    for tit in df.title:
        if len(tit) > 40:
            titulos.append(tit[:40]+'..')
        else:
            titulos.append(tit)



    colors = ['#7FDBFF' if i in rows else '#0074D9'
              for i in range(len(df))]                    # Pintamos de distinto color las filas seleccionadas


    fig = go.Figure()

    fig.add_trace(go.Bar(x=valor,
                    y=titulos,
                    orientation='h'))

    fig.update_xaxes(showgrid=False,showticklabels=True, title='Cantidad Usuarios')
    fig.update_yaxes(showgrid=False, title='Notas',showticklabels=False)
    fig.update_traces(marker_color=colors, hovertemplate="<b>%{y}</b><extra></extra>, Cantidad:<b>%{x}</b>")
    fig.update_layout(title=f'<b>{autor1}<b>. {checklist}')



    fig.update_layout(
        xaxis_title='<b>Cantidad Usuarios</b>',
        font=dict(
            family="Courier New, Monospace",
            size=15,
            color='#000000'
        )
    )


    return fig



def subplot(df1_p,df2_p,autor1,autor2):
    '''
    Creamos 4 graficos de barras para comprar los valores entre los dos autores.
    '''

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

    dfplot = pd.DataFrame([autor1,autor2], columns=['autor'])
    dfplot['PageViews'] = [pageviews1,pageviews2]
    dfplot['Usuarios'] = [usuarios1,usuarios2]
    dfplot['Suscriptos'] = [suscriptos1,suscriptos2]
    dfplot['Choques'] = [choques1,choques2]
    dfplot['Altas'] = [altas1,altas2]

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("PageViews","Usuarios", "Suscriptos", 'Choques')
    )

    fig.add_trace(go.Bar(y=dfplot.PageViews,x=dfplot.autor),
                row=1, col=1)

    fig.add_trace(go.Bar(y=dfplot.Usuarios,x=dfplot.autor),
                row=1, col=2)

    fig.add_trace(go.Bar(y=dfplot.Suscriptos,x=dfplot.autor),
                row=2, col=1)

    fig.add_trace(go.Bar(y=dfplot.Choques,x=dfplot.autor),
                row=2, col=2)

    fig.update_layout( showlegend=False)

    return fig


    