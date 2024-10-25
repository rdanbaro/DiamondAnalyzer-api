
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from analysis.personalizados import convertir_horas_wh_a_entero
from matplotlib.figure import Figure


class DS:
    # Funcion utilizada en el apply para buscar habito con mas dias consecutivos

    def count_consecutive_yes(series):
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
            if value == 'Yes':
                current_consecutive_yes += 1
                max_consecutive_yes = max(
                    max_consecutive_yes, current_consecutive_yes)
            else:
                current_consecutive_yes = 0
        return max_consecutive_yes



    def dame_graficas_habitos(ruta):
        """
        Funcion que devuelve un tuple de 7 valores:
        - str con los habitos con mayor frecuencia
        - str con los habitos con menor frecuencia
        - str con el dia con mas habitos cumplidos
        - str con el dia con menor habitos cumplidos
        - str con los habitos con mayor racha
        - str con el porcentaje total de cumplimiento
        - Una figura con un gráfico de barras que muestra la frecuencia de habitos por dia
        - Una figura con un gráfico de barras que muestra la cantidad total de dias cumplidos por cada habito

        Parameters
        ----------
        ruta: str
            Ruta del csv que contiene los datos de los habitos.

        Returns
        -------
        tuple
            7 valores: str con los habitos con mayor frecuencia, str con los habitos con menor frecuencia, str con el dia con mas habitos cumplidos, str con el dia con menor habitos cumplidos, str con los habitos con mayor racha, str con el porcentaje total de cumplimiento, una figura con un gráfico de barras que muestra la frecuencia de habitos por dia y una figura con un gráfico de barras que muestra la cantidad total de dias cumplidos por cada habito.
        """
        data_habit_example = pd.read
        me_interesa_d = data_habit_example.drop(columns=['Progress', 'Status', 'Day']).iloc[len(
            data_habit_example)-len(data_habit_example):len(data_habit_example)]
        me_interesa = data_habit_example.drop(columns=['Date', 'Progress', 'Status', 'Day']).iloc[len(
            data_habit_example)-len(data_habit_example):len(data_habit_example)]

        # Habito mayor&menor frecuencia
        frec_habit = me_interesa.eq('Yes').sum()
        dict = frec_habit.to_dict()
        habits_maxfrec = [i for i in list(
            dict.keys()) if dict[i] == frec_habit.max()]
        habits_minfrec = [i for i in list(
            dict.keys()) if dict[i] == frec_habit.min()]
        habits_ordenados = frec_habit.sort_values()

        # Frecuencia x dia
        new_name = me_interesa.transpose().reset_index()

        new_name.columns = range(len(new_name.columns))
        frec_dia = new_name.eq('Yes').sum()

        dict_d = frec_dia.to_dict()
        days_maxfrec = [i for i in list(
            dict_d.keys()) if dict_d[i] == frec_dia.max()]
        days_minfrec = [i for i in list(
            dict_d.keys()) if dict_d[i] == frec_dia.min()]

        # Maximos dias consecutivos
        consecutive_yes_count = me_interesa.apply(count_consecutive_yes)

        dict_r = consecutive_yes_count.to_dict()
        habits_maxrach = [i for i in list(
            dict_r.keys()) if dict_r[i] == consecutive_yes_count.max()]

        # Porcentaje de dias cumplidos
        me_interesa.eq('Yes').sum().sum()
        habits_porcent = me_interesa.eq('Yes').sum().sum() / me_interesa.size * 100

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

        return f'Habitos con mayor frecuencia: \n {habits_maxfrec}', f'Habitos con menor frecuencia: \n {habits_minfrec}', f'Dia con mas habitos cumplidos: \n {days_maxfrec}', f'Dia con menor habitos cumplidos \n {days_minfrec}', f'Habitos con mayor racha \n f{habits_maxrach}', f'Porcentaje total de cumplimiento: {habits_porcent}',  fig2, fig1, habits_ordenados


    def dame_graficas_diamantes(ruta):

        """
        Funcion que devuelve un tuple de 8 valores:
        - str con el total de horas trackeadas
        - str con la categoria con mayor tiempo invertido
        - str con la actividad con mayor tiempo invertido
        - str con el porcentaje de tiempo trackeado
        - una figura con un gráfico de barras que muestra el tiempo invertido x categoria
        - una figura con un gráfico de líneas que muestra el tiempo de categorias x dia
        - una figura con un gráfico de barras que muestra el tiempo invertido x actividad
        - una figura con un gráfico de pastel que muestra el tiempo invertido x categoria en porcentaje

        Parameters
        ----------
        ruta: str
            Ruta del csv que contiene los datos de los diamantes.

        Returns
        -------
        tuple
            8 valores: str con el total de horas trackeadas, str con la categoria con mayor tiempo invertido, str con la actividad con mayor tiempo invertido, str con el porcentaje de tiempo trackeado, una figura con un gráfico de barras que muestra el tiempo invertido x categoria, una figura con un gráfico de líneas que muestra el tiempo de categorias x dia, una figura con un gráfico de barras que muestra el tiempo invertido x actividad y una figura con un gráfico de pastel que muestra el tiempo invertido x categoria en porcentaje.
        """

        # Carga y preparacion de los datos

        df = pd.read_csv(ruta)

        df = df.drop(len(df)-1)
        df = df.fillna('Ocio')

        df_preparado = df.drop(columns=['Inicio', 'Fin'])
        df_preparado['Duración'] = df_preparado['Duración'].apply(
            convertir_horas_wh_a_entero)

        # Estadisticas

        # Calculo total horas trackeadas
        total_horas_trackeadas = df_preparado['Duración'].sum()

        # Calculo categoria con mayor tiempo invertido
        tiempo_por_categoria = df_preparado.groupby(['Etiquetas']).sum()

        cat_mayor_tiempo = tiempo_por_categoria['Duración'].idxmax()

        # Calculo actividad con mayor tiempo invertido
        tiempo_por_actividad = df_preparado.groupby(['Tarea']).sum().reset_index()
        por_actividad_ordenado = tiempo_por_actividad.sort_values(
            by='Duración', ascending=False)

        act_mayor_tiempo = tiempo_por_actividad['Duración'].idxmax()

        # Calculo porcentaje de tiempo trackeado
        tiempo_por_dia = df_preparado.groupby(['Día']).sum()
        tiempo_por_dia_por_categoria = df_preparado.groupby(
            ['Día', 'Etiquetas']).sum().reset_index()
        cant_de_dias = len(tiempo_por_dia)
        horas_totales = cant_de_dias * 24

        prct_tiempo_track = total_horas_trackeadas / horas_totales * 100

        # Graficas

        # Grafico de barras: tiempo invertido x categoria
        fig1 = plt.figure()
        fig1.set_facecolor('#8D99AE')
        ax = fig1.add_subplot(1, 1, 1)

        sns.barplot(data=tiempo_por_categoria, x=tiempo_por_categoria.index,
                    y=tiempo_por_categoria['Duración'], hue='Etiquetas')

        plt.ylabel('Tiempo(h)')
        plt.xlabel('Categorías')

        plt.yticks(range(0, 50, 4))

        # Grafico de lineas: tiempo de categorias x dia
        fig2 = plt.figure()
        fig2.set_facecolor('#8D99AE')
        ax = fig2.add_subplot(1, 1, 1)

        sns.lineplot(data=tiempo_por_dia_por_categoria,
                     x=tiempo_por_dia_por_categoria['Día'], y=tiempo_por_dia_por_categoria['Duración'], hue='Etiquetas')

        plt.ylabel('Tiempo(h)')

        plt.xticks(rotation=45)
        plt.yticks(range(0, 10))

        # Grafico de barras: tiempo invertido x actividad
        fig3 = plt.figure(figsize=(3, 3))
        fig3.set_facecolor('#8D99AE')
        ax = fig3.add_subplot(1, 1, 1)
        sns.barplot(data=por_actividad_ordenado,
                    x=por_actividad_ordenado['Duración'], y=por_actividad_ordenado['Tarea'], hue='Tarea')

        plt.ylabel('Actividad')
        plt.xlabel('Tiempo(h)')

        # Grafico de pastel: tiempo invertido x categoria en prct
        porcentajes = [
            f'{(i/total_horas_trackeadas*100):.1f}' for i in tiempo_por_categoria['Duración']]
        porcentajes.sort()
        porcentajes.reverse()

        fig4 = plt.figure() #8D99AE
        fig4.set_facecolor('#8D99AE')
        ax = fig4.add_subplot(1, 1, 1)
        plt.pie(x=tiempo_por_categoria['Duración'].sort_values(ascending=False),
                shadow=True, wedgeprops={'width': 0.5}, pctdistance=0.85, autopct='%1.1f%%')

        plt.legend(labels=[f"{cat}- {p}%" for cat, p in zip(
            tiempo_por_categoria.sort_values(by='Duración', ascending=False).index, porcentajes)], loc='upper right', bbox_to_anchor=(1.5, 1))

        return f'{total_horas_trackeadas}', f'{cat_mayor_tiempo}', f'{act_mayor_tiempo}', f'{prct_tiempo_track}', fig1, fig2, fig3, fig4
