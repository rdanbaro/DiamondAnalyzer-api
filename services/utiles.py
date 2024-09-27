def convertir_horas_wh_a_entero(horas_wh):
    
    h = float(horas_wh.split(':')[0])
    min = float(horas_wh.split(':')[1]) / 60
    new_format = h+min
        
    return new_format
