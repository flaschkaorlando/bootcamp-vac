import os

def porcentaje(parte, total):

    if parte == 0:
        return 0
    elif total == 0:
        return None
    else: 
        return round((100 * float(parte)/float(total)), 2)
    


def pre_procesamiento(datos_formateados, parametros):

#---------------------------------análisis por sexo----------------------------------
    print("1----------------------------ANÁLISIS POR SEXO----------------------------")

    #calculo y formateo la variable "sexo" de cada registro
    for x in datos_formateados:
        #si está bien formateado no lo toco
        if x["sexo"] == "M" or x["sexo"] == "F":
            x.update({"observaciones": "---"})
        elif x["sexo"] != "M" and x["sexo"] != "F":
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

    print("2----------------------------ANÁLISIS POR TIPO DE VACUNA----------------------------")

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
    print("3y4---------------------------ANÁLISIS POR JURISDICCIÓN/PROVINCIA----------------------------")
    jurisdiccionesdic={}

    for reg in datos_formateados:
        jurisdiccionesdic.update({reg["jurisdiccion_residencia"]: reg["jurisdiccion_residencia_id"]})


    for dis in jurisdiccionesdic.items():
        if dis[1] == "S.I." :
            print(f"{sum((i["jurisdiccion_residencia_id"] == dis[1]) for i in datos_formateados)} dosis sin registro de jurisdicción")

        else:
            #imprimo las dosis con provincias registradas
            if dis[0] != "S.I.":
                print(f"{sum((i["jurisdiccion_residencia_id"] == dis[1]) for i in datos_formateados)} dosis en la provincia de {dis[0]}")
                print(f"{sum((i["jurisdiccion_residencia_id"] == dis[1] and i["nombre_dosis_generica"] == "2da") for i in datos_formateados)}  fueron 2da dosis en la provincia de {dis[0]}")
            
            #imprimo las dosis sin provincias registradas
            else:
                print(f"{sum((i["jurisdiccion_residencia_id"] == dis[1]) for i in datos_formateados)} dosis sin registro de provincia {dis[0]}")
                print(f"{sum((i["jurisdiccion_residencia_id"] == dis[1] and i["nombre_dosis_generica"] == "2da") for i in datos_formateados)}  fueron 2da dosis sin registro de provincia")
  


#--------------------------------------análisis por edad---------------------------------------
    print("5---------------------------ANÁLISIS POR EDAD----------------------------")

    mayores_edad=[]

    for reg in datos_formateados:
        if len(str.split(reg["grupo_etario"] , "-")) < 2:
            if reg["grupo_etario"] == ">=100" and reg["nombre_dosis_generica"] == "Refuerzo":
                mayores_edad.append(reg)          
            continue
        elif int(str.split(reg["grupo_etario"] , "-")[0]) < 60 :
            continue
        elif reg["nombre_dosis_generica"] == "Refuerzo" :
            mayores_edad.append(reg)
        else:
            continue 


    print(f"{len(mayores_edad)} mayores de 60 años que recibieron dosis de refuerzo")

#--------------------------------------CREACION DEL CSV---------------------------------------
    print("----------------------------CREACION DEL CSV----------------------------")


    parametros.append("observaciones")

    encabezado= (",".join(parametros))
    

    inconsistencias = open("inconsistencias.csv","w")

    inconsistencias.write(encabezado+"\n")

    for reg in datos_formateados:
        if reg["observaciones"] != "---":
            lista_params=[]
            for par in parametros:
                lista_params.append(reg.get(par,"---"))
            registro_formateado= ",".join(lista_params).replace("\n","")
            inconsistencias.write(registro_formateado+"\n")
    inconsistencias.close()  



def cargarArchivos():

    muestra = open("datos_nomivac_parte1.csv", "r", encoding="utf-8")
    # muestra = open("modelo_muestra.csv", "r", encoding="utf-8")

    if  muestra.mode == 'r':

        parametros = []
        datos_formateados = []

        for ix, lin in enumerate(muestra.readlines()):
            lin.replace("\n", "")            
            #cargo los encabezados para definirlos como claves de un arreglo de diccionarios

            #si es la primer fila, lo tomo como encabezado
            if ix == 0:
                parametros = lin.replace("\n", "").split(",")
            #sino, lo cargo como un registro                     
            else:
                
                #verifico que los registros tengan la misma cantidad de propiedades que el encabezado
                if len(lin.split(",")) != len(parametros):
                    print("----roto-----")
                    #falta
                    #       el 
                    #           código
                    #               de tratamiento
                    #                   de ésta cosa
                    print(lin)
                    print("---finroto---")
                    # print("intento arreglar")
                    # lin.replace('"','')
                    # lin.replace("'", "")

                    # if len(lin.replace("'","").split(",")) != len(parametros):
                    #     print("no funcionó")
                    #     print(lin)

                    # else:
                    #     print("funcionó")
                    #     print(lin)
                    # quit()
                    #NUNCA FUNCIONÓ LO QUE INTENÉ ARREGLAR

                else:
                
                    #creo un diccionario usando los encabezados como claves y celdas de las filas
                    registro = {}

                    for ix, par in enumerate(parametros):
                            registro.update({par: lin.split(",")[ix]})                  


                    #agrego el nuevo diccionario a la lista
                    datos_formateados.append(registro)
 

        pre_procesamiento(datos_formateados, parametros) 
    



                


if __name__ == "__main__":

    #limpio la consola antes de cada nueva ejecución
    #os.system('cls' if os.name == 'nt' else 'clear')

    cargarArchivos()
