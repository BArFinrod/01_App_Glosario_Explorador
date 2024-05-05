#%%
dfglos['Process_n1_cod_nan'] = dfglos['Process_n1_cod'].map({'PE02.03':'PE02.02',
         'PO01.04':'PO01.02','PO02.02':'PO02.01',
         'PO02.03':'PO02.01','PO04.04':'PO04.E4','PO04.05':'PO04.E4',
         'PS03.02':'PS03.E1','PS04.03':'PS04.02',
         'PO01.01':'PO01.E2','PO04.01':'PO04.E4'} # cambios de nombres
)
# %%

dfglos.loc[(~dfglos['Process_n1_cod_nan'].isna()),'Process_n1_cod'] = dfglos.loc[(~dfglos['Process_n1_cod_nan'].isna()),'Process_n1_cod_nan']

dfglos['Process_n1_cod_nan'] = dfglos['Código'].map({'GD000105':'PO01.07','GD000109':'PO01.07','GD000310':'PO01.07'})
dfglos.loc[(~dfglos['Process_n1_cod_nan'].isna()),'Process_n1_cod'] = dfglos.loc[(~dfglos['Process_n1_cod_nan'].isna()),'Process_n1_cod_nan']
dfglos['Process_n1_cod_nan'] = dfglos['Código'].map({'GD000077':'PO01.E1','GD000367':'PO01.E1','GD000453':'PO01.E1','GD000454':'PO01.E1','GD000455':'PO01.E1'})
dfglos.loc[(~dfglos['Process_n1_cod_nan'].isna()),'Process_n1_cod'] = dfglos.loc[(~dfglos['Process_n1_cod_nan'].isna()),'Process_n1_cod_nan']
dfglos['Process_n1_cod_nan'] = dfglos['Código'].map({'GD000347':'PO03.E3','GD000348':'PO03.E3','GD000356':'PO03.E3','GD000397':'PO03.E3','GD000398':'PO03.E3','GD000399':'PO03.E3','GD000400':'PO03.E3','GD000401':'PO03.E3'})
dfglos.loc[(~dfglos['Process_n1_cod_nan'].isna()),'Process_n1_cod'] = dfglos.loc[(~dfglos['Process_n1_cod_nan'].isna()),'Process_n1_cod_nan']

dfglos = dfglos.drop('Process_n1_cod_nan',axis=1)

dfnew = pd.read_csv('C:/Users/saico/OneDrive/Proyectos/Gobierno de datos - MINEDU/Glosario de negocio/Visualización/01. App/00.Data/process_domains_04_2024.csv', sep='\t')

dfglos2 = dfglos.merge(dfnew, left_on=['Process_n1_cod'], right_on=['Cod'], how='left')
# dfglos2 = dfglos2.rename({'Process_n1_cod':'Código_old', 'Cod_new.2':'Código'}, axis=1)

dfglos2 = dfglos2[['orden', 'Cod_new',
       'Nombre_new', 'Cod_new.1', 'Nombre_new.1', 'Cod_new.2',
       'Nombre_new.2', 'Código', 'Nombre', 'Definición', 'codigo documento normativo',
       'documento normativo', 'Observación', 'embedding']]

dfglos2 = dfglos2.rename({'documento normativo':'Documento normativo',
                          'codigo documento normativo':'Código documento normativo'}, axis=1)

dfglos2 = dfglos2.rename({'Cod_new':'Dom_tipo_cod', 'Nombre_new':'Dom_tipo_name',
                          'Cod_new.1':'Dom_n0_cod', 'Nombre_new.1':'Dom_n0_name',
                          'Cod_new.2':'Dom_n1_cod', 'Nombre_new.2':'Dom_n1_name'}, axis=1)

dfglos2.to_pickle(path_str /"00.Data/dfglos_embedd_clustered_dominios.pickle")



###############################
dfproc = pd.read_excel(path_str / "00.Data/05. Dominios_codigos_nombres.xlsx", sheet_name='Dominios')


dftipos = dfproc[['Dom_tipo_cod','Dom_tipo_name']].drop_duplicates(keep='first')
dfn0 = dfproc[['Dom_tipo_cod','Dom_n0_cod','Dom_n0_name']].drop_duplicates(keep='first')
dfn1 = dfproc[['Dom_tipo_cod','Dom_n0_cod','Dom_n1_cod','Dom_n1_name']].drop_duplicates(keep='first')

tree = []
for tipo in dftipos.index:
    tipo_name = dftipos.loc[tipo,'Dom_tipo_name']
    tipo_cod = dftipos.loc[tipo,'Dom_tipo_cod']
    dct_tipo = {'label': tipo_name,
                'value': tipo_cod}
    children = []
    dfni = dfn0.loc[dfn0['Dom_tipo_cod']==tipo_cod]
    for n0 in dfni.index:
        n0_name = dfni.loc[n0, 'Dom_n0_name']
        n0_cod = dfni.loc[n0, 'Dom_n0_cod']
        dct_n0 = {'label': n0_name,
                    'value': n0_cod}
        n0_children = []
        dfn1i = dfn1.loc[(dfn1['Dom_tipo_cod']==tipo_cod) & (dfn1['Dom_n0_cod']==n0_cod)]
        for n1 in dfn1i.index:
            n1_name = dfn1i.loc[n1, 'Dom_n1_name']
            n1_cod = dfn1i.loc[n1, 'Dom_n1_cod']
            dct_n1 = {'label': n1_name,
                      'value': n1_cod}
            n0_children.append(dct_n1)
        dct_n0['children'] = n0_children
        children.append(dct_n0)
    dct_tipo['children'] = children
    tree.append(dct_tipo)

############################
with open(path_str / "00.Data/06._Tree_dominios.pickle",'wb') as f:
    pickle.dump(tree, f)


##########################

#%%
dftipos = dfproc[['Tipo_cod','Tipo_name']].drop_duplicates(keep='first')
dfn0 = dfproc[['Tipo_cod','Process_n0_cod','Process_n0_name']].drop_duplicates(keep='first')
dfn1 = dfproc[['Tipo_cod','Process_n0_cod','Process_n1_cod','Process_n1_name']].drop_duplicates(keep='first')

tree = []
for tipo in dftipos.index:
    tipo_name = dftipos.loc[tipo,'Tipo_name']
    tipo_cod = dftipos.loc[tipo,'Tipo_cod']
    dct_tipo = {'label': tipo_name,
                'value': tipo_cod}
    children = []
    dfni = dfn0.loc[dfn0['Tipo_cod']==tipo_cod]
    for n0 in dfni.index:
        n0_name = dfni.loc[n0, 'Process_n0_name']
        n0_cod = dfni.loc[n0, 'Process_n0_cod']
        dct_n0 = {'label': n0_name,
                    'value': n0_cod}
        n0_children = []
        dfn1i = dfn1.loc[(dfn1['Tipo_cod']==tipo_cod) & (dfn1['Process_n0_cod']==n0_cod)]
        for n1 in dfn1i.index:
            n1_name = dfn1i.loc[n1, 'Process_n1_name']
            n1_cod = dfn1i.loc[n1, 'Process_n1_cod']
            dct_n1 = {'label': n1_name,
                      'value': n1_cod}
            n0_children.append(dct_n1)
        dct_n0['children'] = n0_children
        children.append(dct_n0)
    dct_tipo['children'] = children
    tree.append(dct_tipo)