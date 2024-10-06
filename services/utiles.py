from datetime import datetime

def convertir_horas_wh_a_entero(horas_wh):
    
    h = float(horas_wh.split(':')[0])
    min = float(horas_wh.split(':')[1]) / 60
    new_format = h+min
        
    return new_format

def convertir_fecha_a_datetime(fecha):
    meses = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
    'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    
    dia, mes, año, hora = fecha.replace(' de ', ' ').split()
    mes = meses[mes]
    fecha_date = datetime.strptime(f'{dia} {mes} {año} {hora}', '%d %m %Y %H:%M')
    
    return fecha_date