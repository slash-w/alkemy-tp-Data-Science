import scrapper as scr
import tableMkr as tbmkr
import pandas as pd
import functions as fun

def main():
    #   --- DESCARGAR LOS CSVs ---      
    scr.sheet_to_csv('museos'       ,'Datos Argentina - Museos!A1:Z'                ,'https://docs.google.com/spreadsheets/d/1PS2_yAvNVEuSY0gI8Nky73TQMcx_G1i18lm--jOGfAA/edit#gid=514147473')      
    scr.sheet_to_csv('cines'        ,'Datos Argentina - Salas de Cine!A1:Z'         ,'https://docs.google.com/spreadsheets/d/1o8QeMOKWm4VeZ9VecgnL8BWaOlX5kdCDkXoAph37sQM/edit#gid=1691373423')                       
    scr.sheet_to_csv('bibliotecas'  ,'Datos Argentina - Bibliotecas Populares!A1:Z' ,'https://docs.google.com/spreadsheets/d/1udwn61l_FZsFsEuU8CMVkvU2SpwPW3Krt1OML3cYMYk/edit#gid=1605800889')   
    
    #   --- PASAR LOS CSVs A DATAFRAMES ---
    mus = pd.read_csv(scr.new_namer('museos'),      skiprows=1)
    cin = pd.read_csv(scr.new_namer('cines'),       skiprows=1)
    bib = pd.read_csv(scr.new_namer('bibliotecas'), skiprows=1)
    
    #   --- NORMALIZAR LA INFO DE LOS DFs ---
    mus = mus.drop(columns=['0'])
    cin = cin.drop(columns=['0'])
    bib = bib.drop(columns=['0'])

    mus.columns = fun.normalize(mus.columns.str.capitalize())
    cin.columns = fun.normalize(cin.columns.str.capitalize())
    bib.columns = fun.normalize(bib.columns.str.capitalize())

    mus = mus.rename(columns = {'Direccion':'Domicilio'})
    cin = cin.rename(columns = {'Direccion':'Domicilio'})
    bib = bib.rename(columns = {'Cod_tel':'Cod_area'})

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    #   --- GENERAL DATAFRAME ---
    df = pd.concat([mus,cin,bib])
    filter_df = ((mus.columns.intersection(cin.columns)).intersection(bib.columns))
    df = df[filter_df]

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    #   --- AGRUPACIONES DATAFRAME ---
    categ =  df['Categoria'].value_counts()
    fuente = df['Fuente'].value_counts()

    prov = []
    cate = []
    pyc = df.groupby(['Provincia', 'Categoria']).size()
    for i in ((pyc.index).tolist()):
        prov.append(i[0])
        cate.append(i[1])

    cat_df = pd.DataFrame({
        'Categoria': (categ.index).tolist(),
        'Cant_reg':   categ.tolist()
    })
    fuente_df = pd.DataFrame({
        'Fuente':  (fuente.index).tolist(),
        'Cant_reg': fuente.tolist()
    })

    prov_cat_df = pd.DataFrame({
        'Provincia': prov,
        'Categoria': cate,
        'Cant_reg':  pyc.tolist()
    })

    tipo_arr = []
    for i in range(len(cat_df)):
        tipo_arr.append('Categoria')
    for i in range(len(fuente_df)):
        tipo_arr.append('Fuente')
    for i in range(len(prov_cat_df)):
        tipo_arr.append('Provincia_Categoria')

    agrup_df = pd.DataFrame({
        'Tipo': tipo_arr,

        'Agrupador':    cat_df['Categoria'].tolist() +                      # por categoria
                        fuente_df['Fuente'].tolist() +                      # por fuente
                        [str(x) + '-' + str(y) for x, y in zip(prov, cate)],# por provincia y categoria
                        
        'Cantidad':     cat_df['Cant_reg'].tolist() +
                        fuente_df['Cant_reg'].tolist() +
                        prov_cat_df['Cant_reg'].tolist()
    })

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    #   --- DATOS CINE DATAFRAME ---
    datos_cine_df = pd.DataFrame({
        'Provincia': [],
        'Cant_pantallas': [],
        'Cant_butacas': [],
        'Cant_espacios_incaa': []
    })

    datos_cine_df['Provincia'] =            pd.unique(cin['Idprovincia'])
    datos_cine_df['Cant_pantallas'] =       fun.adder(cin, 'Idprovincia', datos_cine_df.columns.get_loc('Cant_pantallas')+1)
    datos_cine_df['Cant_butacas'] =         fun.adder(cin, 'Idprovincia', datos_cine_df.columns.get_loc('Cant_butacas')+1)
    datos_cine_df['Cant_espacios_incaa'] =  fun.counter(cin, 'Idprovincia', 'si', 'Espacio_incaa')

    #   --- Generacion de tablas al final ---
    tbmkr.add_table(df, 'Datos_Argentina')
    tbmkr.add_table(agrup_df, 'Agrupacion_datos')
    tbmkr.add_table(datos_cine_df, 'Datos_Cine')

main()