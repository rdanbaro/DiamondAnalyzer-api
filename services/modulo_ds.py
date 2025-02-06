from models.sprint import Diamante

from services.habitos import HabitoService
from services.diamantes import DiamanteService
from services.entreno import EntrenoService

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from services.utiles import convertir_horas_wh_a_entero
from matplotlib.figure import Figure


class DS:
    def __init__(self, db):
        self.db = db
    # Funcion utilizada en el apply para buscar habito con mas dias consecutivos

    def count_consecutive_yes(self, series):
        """
        Cuenta la cantidad de dias consecutivos de 'Yes' en una serie, es decir,
        cuantos dias seguidos se ha cumplido con el habito.

        Parameters
        ----------
        series: pd.Series
            Serie de valores que se quieren contar, estos pueden ser 'Yes' o 'No'.

        Returns
        -------
        int
            Cantidad de dias consecutivos de 'Yes' en la serie.

        Examples
        --------
        >>> count_consecutive_yes(['Yes', 'Yes', 'No', 'Yes'])
        2
        >>> count_consecutive_yes(['Yes', 'Yes', 'Yes', 'Yes'])
        4
        >>> count_consecutive_yes(['Yes', 'Yes', 'Yes', 'No'])
        3
        """
        max_consecutive_yes = 0
        current_consecutive_yes = 0
        for value in series:
            if value == 1:
                current_consecutive_yes += 1
                max_consecutive_yes = max(
                    max_consecutive_yes, current_consecutive_yes)
            else:
                current_consecutive_yes = 0
        return max_consecutive_yes

    def get_stats_habitos(self, sprint_id):
        
        habito = HabitoService(self.db)
        habitos = habito.get_habitos_sprint(sprint_id)
        habitos_dict = [d.__dict__ for d in habitos]
        df = pd.DataFrame(habitos_dict)
        
        me_interesa = df.pivot(index='date', columns='habito', values='realizado').reset_index()
        me_interesa = me_interesa.rename_axis(None, axis=1)

        # Habito mayor&menor frecuencia
        frec_habit = me_interesa.eq(1).sum()
        dict = frec_habit.to_dict()
        habits_maxfrec = [i for i in list(
            dict.keys()) if dict[i] == frec_habit.max()]
        habits_minfrec = [i for i in list(
            dict.keys()) if dict[i] == frec_habit.min()]
        habits_ordenados = frec_habit.sort_values()

        # Frecuencia x dia
        new_name = me_interesa.transpose().reset_index()

        new_name.columns = range(len(new_name.columns))
        frec_dia = new_name.eq(1).sum()

        dict_d = frec_dia.to_dict()
        days_maxfrec = [i for i in list(
            dict_d.keys()) if dict_d[i] == frec_dia.max()]
        days_minfrec = [i for i in list(
            dict_d.keys()) if dict_d[i] == frec_dia.min()]

        # Maximos dias consecutivos
        consecutive_yes_count = me_interesa.apply(self.count_consecutive_yes)

        dict_r = consecutive_yes_count.to_dict()
        habits_maxrach = [i for i in list(
            dict_r.keys()) if dict_r[i] == consecutive_yes_count.max()]

        # Porcentaje de dias cumplidos
        me_interesa.eq(1).sum().sum()
        habits_porcent = me_interesa.eq(1).sum().sum() / me_interesa.size * 100

        habits_ordenados = (
            habits_ordenados.drop(['date', 'Status'])
            .index.tolist()
            )

        return f'Habitos con mayor frecuencia: \n {habits_maxfrec}', f'Habitos con menor frecuencia: \n {habits_minfrec}', f'Dia con mas habitos cumplidos: \n {days_maxfrec}', f'Dia con menor habitos cumplidos \n {days_minfrec}', f'Habitos con mayor racha \n {habits_maxrach}', f'Porcentaje total de cumplimiento: {habits_porcent}', f'{habits_ordenados}', len(habits_ordenados)


    def get_graf_habitos(self, sprint_id):
        habito = HabitoService(self.db)
        habitos = habito.get_habitos_sprint(sprint_id)
        habitos_dict = [d.__dict__ for d in habitos]
        df = pd.DataFrame(habitos_dict)
    
        me_interesa = df.pivot(index='date', columns='habito', values='realizado').reset_index()
        me_interesa = me_interesa.rename_axis(None, axis=1)

        
        
        new_name = me_interesa.transpose().reset_index()

        new_name.columns = range(len(new_name.columns))
        frec_dia = new_name.eq(1).sum()
        
        
        frec_habit = me_interesa.eq(1).sum()
        habits_ordenados = frec_habit.sort_values()
        # GRAFICAR

        # Grafica 1
        colors = sns.color_palette("deep")
        fig1, ax = plt.subplots(1, 1, figsize=(5, 2))
        fig1.set_facecolor('#a8dadc')
        # Filtrar los datos para excluir los días con contador 0
        frec_dia_filtrado = frec_dia[frec_dia.values != 0]

        # Convertir los índices en cadenas
        frec_dia_filtrado.index = frec_dia_filtrado.index.astype(str)

        # Graficar un gráfico de barras en el primer eje
        ax.bar(frec_dia_filtrado.index, frec_dia_filtrado.values,
               alpha=0.75, color='#2a9d8f')
        ax.set_title('Hábitos por día')
        ax.set_xlabel('Numero del Día')
        ax.set_ylabel('Frecuencia')

        # Graficar un gráfico de líneas en el segundo eje
        ax.plot(frec_dia_filtrado.index, frec_dia_filtrado.values, alpha=0.85)
        plt.tight_layout()

        # Grafica 2
        fig2, ax = plt.subplots(1, 1, figsize=(6, 2))
        fig2.set_facecolor('#a8dadc')
        frec_habit_filtrado = habits_ordenados[habits_ordenados.values != 0]
        # colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']
        bars = ax.barh(frec_habit_filtrado.index,
                       frec_habit_filtrado.values, color=colors)
        ax.set_title('Total dias cumplidos ')
        ax.set_xlabel('Cantidad total de dias')
        ax.set_ylabel('Hábitos')
        ax.set_xticks(range(0, 16, 2))

        # Ajustar el diseño de las subtramas
        plt.tight_layout()

        return fig1, fig2


    def get_stats_diamantes(self, sprint_id):
        diamante = DiamanteService(self.db)
        diamantes = diamante.get_diamantes_sprint(sprint_id)
        diamantes_dict = [d.__dict__ for d in diamantes]
        df = pd.DataFrame(diamantes_dict)
        
        df_preparado = df.drop(columns=[df.columns[0], 'inicio', 'fin', 'sprint_id'])
        df_preparado['fecha'] = pd.to_datetime(df_preparado['fecha'])
        df_preparado['fecha'] = df_preparado['fecha'].dt.strftime('%Y-%m-%d')
        
        
        # Calculo total horas trackeadas
        total_horas_trackeadas = df_preparado['duracion'].sum()

        # Calculo categoria con mayor tiempo invertido
        tiempo_por_categoria = df_preparado.groupby(['etiqueta']).sum()

        cat_mayor_tiempo = tiempo_por_categoria['duracion'].idxmax()

        # Calculo actividad con mayor tiempo invertido
        tiempo_por_actividad = df_preparado.groupby(['actividad']).sum().reset_index()
        por_actividad_ordenado = tiempo_por_actividad.sort_values(
            by='duracion', ascending=False)

        act_mayor_tiempo = tiempo_por_actividad['duracion'].idxmax()

        # Calculo porcentaje de tiempo trackeado
        tiempo_por_dia = df_preparado.groupby(['fecha']).sum()
        tiempo_por_dia_por_categoria = df_preparado.groupby(
            ['fecha', 'etiqueta']).sum().reset_index()
        cant_de_dias = len(tiempo_por_dia)
        horas_totales = cant_de_dias * 24

        prct_tiempo_track = total_horas_trackeadas / horas_totales * 100
        
        return f'total_horas_trackeadas: {total_horas_trackeadas}', f'categoria_mayor_tiempo: {cat_mayor_tiempo}', f'actividad_mayor_tiempo: {act_mayor_tiempo}', f'porcentaje_tiempo_trackeado: {prct_tiempo_track}'
        
    
    def get_graf_diamantes(self, sprint_id):
  

        # Carga de datos

        
        diamante = DiamanteService(self.db)
        diamantes = diamante.get_diamantes_sprint(sprint_id)
        diamantes_dict = [d.__dict__ for d in diamantes]
        df = pd.DataFrame(diamantes_dict)
        
        df_preparado = df.drop(columns=[df.columns[0], 'inicio', 'fin', 'sprint_id'])
        df_preparado['fecha'] = pd.to_datetime(df_preparado['fecha'])
        df_preparado['fecha'] = df_preparado['fecha'].dt.strftime('%Y-%m-%d')
        
        
       # Calculo total horas trackeadas
        total_horas_trackeadas = df_preparado['duracion'].sum()
        
        # Agrupamientos
        tiempo_por_categoria = df_preparado.groupby(['etiqueta']).sum()
        tiempo_por_actividad = df_preparado.groupby(['actividad']).sum().reset_index()
        por_actividad_ordenado = tiempo_por_actividad.sort_values(
            by='duracion', ascending=False)

        tiempo_por_dia = df_preparado.groupby(['fecha']).sum()
        tiempo_por_dia_por_categoria = df_preparado.groupby(
            ['fecha', 'etiqueta']).sum().reset_index()


        # Graficas

        # Grafico de barras: tiempo invertido x categoria
        fig1 = plt.figure()
        fig1.set_facecolor('#8D99AE')
        ax = fig1.add_subplot(1, 1, 1)

        sns.barplot(data=tiempo_por_categoria, x=tiempo_por_categoria.index,
                    y=tiempo_por_categoria['duracion'], hue='etiqueta')

        plt.ylabel('Tiempo(h)')
        plt.xlabel('Categorías')

        plt.yticks(range(0, 50, 4))

        # Grafico de lineas: tiempo de categorias x dia
        fig2 = plt.figure()
        fig2.set_facecolor('#8D99AE')
        ax = fig2.add_subplot(1, 1, 1)

        sns.lineplot(data=tiempo_por_dia_por_categoria,
                     x=tiempo_por_dia_por_categoria['fecha'], y=tiempo_por_dia_por_categoria['duracion'], hue='etiqueta')

        plt.ylabel('Tiempo(h)')

        plt.xticks(rotation=45)
        plt.yticks(range(0, 10))

        # Grafico de barras: tiempo invertido x actividad
        fig3 = plt.figure(figsize=(3, 3))
        fig3.set_facecolor('#8D99AE')
        ax = fig3.add_subplot(1, 1, 1)
        sns.barplot(data=por_actividad_ordenado,
                    x=por_actividad_ordenado['duracion'], y=por_actividad_ordenado['actividad'], hue='actividad')

        plt.ylabel('Actividad')
        plt.xlabel('Tiempo(h)')

        # Grafico de pastel: tiempo invertido x categoria en prct
        porcentajes = [
            f'{(i/total_horas_trackeadas*100):.1f}' for i in tiempo_por_categoria['duracion']]
        porcentajes.sort()
        porcentajes.reverse()

        fig4 = plt.figure() #8D99AE
        fig4.set_facecolor('#8D99AE')
        ax = fig4.add_subplot(1, 1, 1)
        plt.pie(x=tiempo_por_categoria['duracion'].sort_values(ascending=False),
                shadow=True, wedgeprops={'width': 0.5}, pctdistance=0.85, autopct='%1.1f%%')

        plt.legend(labels=[f"{cat}- {p}%" for cat, p in zip(
            tiempo_por_categoria.sort_values(by='duracion', ascending=False).index, porcentajes)], loc='upper right', bbox_to_anchor=(1.5, 1))

        
        
        return fig1, fig2, fig3, fig4
        
    
    def get_stats_entreno(self, sprint_id):
        
        #df_rutinas_raw = pd.read_csv(r"C:\Users\User\Downloads\Datos de Entreno Notion\Trackeo Entrenamientos.csv")
        #df_ejercicios_raw = pd.read_csv(r"C:\Users\User\Downloads\Datos de Entreno Notion\Ejercicios-Tipos.csv")

        entreno = EntrenoService(self.db)
        entrenos, ejercicios = entreno.get_entrenamientos_sprint(sprint_id)
        
        entrenos_dict = [d.__dict__ for d in entrenos]
        df_rutinas_processed = pd.DataFrame(entrenos_dict)
        
        ejercicios_dict = [d.__dict__ for d in ejercicios]
        df_ejercicios_processed = pd.DataFrame(ejercicios_dict)


        #df_rutinas_processed = (
        #df_rutinas_raw.drop(columns=['Ejercicios'])
        #.rename(columns={'Title': 'Rutina', 'Músculos': 'Musculos'})
        #)
        
        # Total dias de entrenamiento
        total_dias_entreno = df_rutinas_processed.shape[0]

        df_musculos = df_rutinas_processed.groupby('musculos').count()
        df_musculos_split = df_rutinas_processed['musculos'].str.split(',').explode()
        conteo_por_musculo = df_musculos_split.str.strip().value_counts()

        # Musculo mas entrenado
        musculo_mas_entrenado = conteo_por_musculo.idxmax()
        # Musculo menos entrenado
        musculo_mnos_entrenado = conteo_por_musculo.idxmin()
        
        # Rutinas mas entrenadas
        rutinas_mas_entrenadas = df_rutinas_processed['rutina'].value_counts().idxmax()
        
        # df_ejercicios_processed = pd.melt(df_ejercicios_raw, var_name='ejercicio',id_vars=['fecha', 'ronda', 'rutina'], 
        #                           value_name='cant_repeticiones',
        #                           value_vars= df_ejercicios_raw.keys().tolist()[1:-1] 
        # ).dropna().sort_values(by=['fecha', 'ronda']).reset_index(drop=True)

        
        
        # Rondas
        rondas_por_dia = df_ejercicios_processed.groupby(['fecha'])['ronda'].nunique().reset_index()
        max_rondas_por_dia = df_ejercicios_processed.groupby(['fecha'])['ronda'].max().reset_index()
        total_rondas = int(max_rondas_por_dia['ronda'].sum())

        # Series
        series_por_dia = df_ejercicios_processed.groupby(['fecha']).count().reset_index()
        total_series = int(series_por_dia['ejercicio'].sum())

        # Total de series por ejercicio
        series_por_ejercicio = (
            df_ejercicios_processed.groupby(['ejercicio'])
            .count()
            .reset_index()
            .loc[:,['ejercicio', 'fecha']]
            .rename(columns={'fecha': 'Total de series'})
            .sort_values(by=['Total de series'], ascending=False)
            .reset_index(drop=True)
            )
        print('HOLA:',series_por_ejercicio)
        # Ejercicio con mas series
        ejercicio_mas_series = series_por_ejercicio['ejercicio'][0]
        # Ejercicio con menos series
        ejercicio_mnos_series = series_por_ejercicio['ejercicio'].iloc[-1]
        
        
        # Repeticiones
        total_repeticiones_x_ejercicio = (
            df_ejercicios_processed
            .loc[:,['ejercicio', 'repeticiones']]
            .groupby(['ejercicio'])
            .sum()
            .reset_index()
            .rename(columns={'repeticiones': 'Total de repeticiones'})
            .sort_values(by=['Total de repeticiones'], ascending=False)
            .reset_index(drop=True)
            )

        return f'Musculo mas entrenado: {musculo_mas_entrenado}', f'Musculo menos entrenado: {musculo_mnos_entrenado}', f'Total de dias entrenados: {total_dias_entreno}', f'Rutina mas entrenada: {rutinas_mas_entrenadas}', f'Total de rondas: {total_rondas}', f'Total de series: {total_series}', f'Ejercicio con mas series: {ejercicio_mas_series}', f'Ejercicio con mas repeticiones: {ejercicio_mnos_series}'
        
        
    def get_graf_entreno(self, sprint_id):
        
        entreno = EntrenoService(self.db)
        entrenos, ejercicios = entreno.get_entrenamientos_sprint(sprint_id)
        
        entrenos_dict = [d.__dict__ for d in entrenos]
        df_rutinas_processed = pd.DataFrame(entrenos_dict)
        
        ejercicios_dict = [d.__dict__ for d in ejercicios]
        df_ejercicios_processed = pd.DataFrame(ejercicios_dict)
        
        # Procesamiento para gráfico de pastel
        #df_rutinas_processed = df_rutinas_raw.rename(columns={'Músculos': 'Musculos'})
        df_musculos_split = df_rutinas_processed['musculos'].str.split(',').explode()
        conteo_por_musculo = df_musculos_split.str.strip().value_counts()

        # Gráfico de pastel
        fig1 = plt.figure(figsize=(10, 6))
        fig1.set_facecolor('#8D99AE')
        plt.pie(conteo_por_musculo.values, 
                labels=conteo_por_musculo.index,
                autopct='%1.1f%%',
                shadow=True)
        plt.title('Distribución de Músculos Entrenados')

        # Procesamiento para gráfico de barras
        # df_ejercicios_processed = pd.melt(
        #     df_ejercicios_raw, 
        #     var_name='ejercicio',
        #     id_vars=['fecha', 'ronda', 'rutina'], 
        #     value_name='Repeticiones',
        #     value_vars=df_ejercicios_raw.keys().tolist()[1:-1]
        # ).dropna()

        # Filtrar ejercicio específico
        df_ejercicios_processed = df_ejercicios_processed[df_ejercicios_processed['ejercicio'] != 'Sentadilla en Pared ( segs )']

        total_repeticiones = df_ejercicios_processed.groupby('ejercicio')['repeticiones'].sum().sort_values(ascending=True)

        # Gráfico de barras horizontales
        fig2 = plt.figure(figsize=(12, 8))
        fig2.set_facecolor('#8D99AE')
        barras = plt.barh(total_repeticiones.index, total_repeticiones.values, color='#2a9d8f')

        # Añadir etiquetas con el número de repeticiones
        for i, barra in enumerate(barras):
            width = barra.get_width()
            plt.text(width, i, f' {int(width)}', va='center')

        plt.title('Total de Repeticiones por Ejercicio')
        plt.xlabel('Número de Repeticiones')
        plt.ylabel('Ejercicios')
        
        return fig1, fig2