import os

def porcentaje(parte, total):

    if parte == 0:
        return 0
    elif total == 0:
        return None
    else: 
        return round((100 * float(parte)/float(total)), 2)
    


def pre_procesamiento(datos_formateados):

#---------------------------------análisis por sexo----------------------------------
    print("----------------------------ANÁLISIS POR SEXO----------------------------")

    #calculo y formateo la variable "sexo" de cada registro
    for x in datos_formateados:
        #si está bien formateado no lo toco
        if x["sexo"] != "M" and x["sexo"] != "F":
            #si se puede formatear considerando la primer letra lo hago
            x["sexo"] = str.upper(x["sexo"])
            if x["sexo"].startswith("F"):
                #formateo y comento el registro en observaciones
                x.update({"observaciones": "sexo formateado"})
                x.update({"sexo": "F"})
            elif x["sexo"].startswith("M"):
                #formateo y comento el registro en observaciones
                x.update({"observaciones": "sexo formateado"})
                x.update({"sexo": "M"})
            else:
                #comento el registro en observaciones
                x.update({"observaciones": "sexo mal registrado"})

    #imprimo el total de registros
    print(f"{len(datos_formateados)} registros en total ")

    #devuelvo los registros con sexo "M"
    print(f"{sum(i["sexo"] == "M" for i in datos_formateados)} registros masculinos, equivalen al {porcentaje(sum(i["sexo"] == "M" for i in datos_formateados),len(datos_formateados))}% de la muestra" )

    #devuelvo los registros con sexo "F"
    print(f"{sum(i["sexo"] == "F" for i in datos_formateados)} registros femeninos, equivalen al {porcentaje(sum(i["sexo"] == "F" for i in datos_formateados),len(datos_formateados))}% de la muestra")

    #devuelvo registros de "sexo" con error
    print(f"{sum((i["sexo"] != "F" and i["sexo"] != "M") for i in datos_formateados)} registros con campo 'sexo' mal cargado")    
  

#-------------------------------------análisis por vacuna--------------------------------------

    print("----------------------------ANÁLISIS POR TIPO DE VACUNA----------------------------")

    #creo un set para tomar todas las vacunas diferentes
    #sin un primer elemento me lo toma como un diccionario y se rompe
    vacunas={""}

    #recorro y agrego las vacunas al set para no tener duplicadas
    for reg in datos_formateados:
        vacunas.add(reg["vacuna"])
    
    #elimino el priemr elemento hardcodeado
    vacunas.discard("")

    #creo un diccionario para llevar la cuenta y seteo todas a 0
    vacunasdic = dict.fromkeys(vacunas, 0)

    #actualizo el diccionario por cada vacuna
    for reg in datos_formateados:
        vacunasdic.update({reg["vacuna"]: vacunasdic[reg["vacuna"]] +1 })

    for vac in vacunas:
        print(f"{vacunasdic[vac]} dosis de {vac}, equivale al { porcentaje(vacunasdic[vac], len(datos_formateados))}% de la muestra")


#--------------------------------------análisis por jurisdicción---------------------------------------
    print("----------------------------ANÁLISIS POR JURISDICCIÓN/PROVINCIA----------------------------")
    jurisdiccionesdic={}

    for reg in datos_formateados:
        jurisdiccionesdic.update({reg["jurisdiccion_residencia"]: reg["jurisdiccion_residencia_id"]})


    for dis in jurisdiccionesdic.items():
        if dis[1] == "S.I." :
            print(f"{sum((i["jurisdiccion_residencia_id"] == dis[1]) for i in datos_formateados)} dosis sin registro de jurisdicción")

        else:
            print(f"{sum((i["jurisdiccion_residencia_id"] == dis[1]) for i in datos_formateados)} dosis en la provincia de {dis[0]}")
            print(f"{sum((i["jurisdiccion_residencia_id"] == dis[1] and i["nombre_dosis_generica"] == "2da") for i in datos_formateados)}  fueron 2da dosis en la provincia de {dis[0]}")


  



def cargarArchivos():

    muestra = open("datos_nomivac_parte1.csv", "r", encoding="utf-8")
    # muestra = open("modelo_muestra.csv", "r", encoding="utf-8")

    if  muestra.mode == 'r':

        parametros = []
        datos_formateados = []

        for ix, lin in enumerate(muestra.readlines()):
            
            #cargo los encabezados para definirlos como claves de un arreglo de diccionarios
            if ix == 0:
                parametros = lin.split(",")

                #elimino el \n que define el salto de línea del último encabezado
                parametros[-1]  = lin.split(",")[-1][:-1]
                      
            else:
                
                #verifico que los registros no tengan comas que hayan roto la estructura de las celdas
                if len(lin.split(",")) != len(parametros):
                    print("----garca-----")
                    #falta
                    #       el 
                    #           código
                    #               de tratamiento
                    #                   de ésta cosa
                    print(lin)
                    print("---fingarca---")
                else:
                
                    #creo un diccionario usando los encabezados como claves y las filas como valores
                    registro = {}

                    for ix, par in enumerate(parametros):
                            registro.update({par: lin.split(",")[ix]})
                    
                    #elimino el \n, que define el salto de línea, del último elemento de la fila 
                    registro.update({parametros[-1]:registro[parametros[-1]][:-1]})

                    #agrego el nuevo diccionario a la lista
                    datos_formateados.append(registro)
 

        pre_procesamiento(datos_formateados) 


    



                


if __name__ == "__main__":

    #limpio la consola antes de cada nueva ejecución
    #os.system('cls' if os.name == 'nt' else 'clear')

    cargarArchivos()
