#%%
# INITIALIZATION
import pandas as pd
import numpy as np
# import pickle
# import copy
# import pdb
import streamlit as st
from streamlit_tree_select import tree_select
# from openai.embeddings_utils import get_embedding
# import tiktoken
from scipy.spatial import distance
from pathlib import Path
import openai
from openai import OpenAI



def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

st.set_page_config(layout="wide")
#%%

path_str = Path(__file__).parent.parent
key_ = st.secrets["akey"]

client = OpenAI(api_key = key_)
# openai.api_key = key_
#%%
def _from_stringlist_to_array(serie):
    return serie.map(lambda x: np.array(eval(x)))


def _get_similitud(x, emb):
    return (1-distance.cosine(x, emb))

@st.cache_data
def _find(str_buscado, dfglos):
    emb_buscar = get_embedding(str_buscado, model="text-embedding-ada-002")
        # calcular distancias/similitud
    dfglos['similitud'] = dfglos['embedding'].apply(_get_similitud, args=(emb_buscar,))
    dffinded = dfglos.loc[dfglos['similitud']>0.8].sort_values(['similitud'], ascending=False)
    return dffinded

#%%
# procesos
dfproc = pd.read_excel(path_str / "00.Data/04. Procesos_codigos_nombres.xlsx", sheet_name='Hoja1')

dfglos = pd.read_pickle(path_str /"00.Data/dfglos_embedd_clustered.pickle")
dfglos = dfglos.rename({'codigo termino':'Código','termino':'Nombre','definicion termino':'Definición'}, axis=1)

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
#%% 


# %%
st.title("Glosario de términos del MINEDU")
st.subheader("Equipo de Gobierno de Datos")

explorer, table = st.columns((1,3))

with explorer:
    return_select = tree_select(tree)

with table:
    selected = return_select['checked'] #.values())
    str_buscar = st.text_input("Búsqueda de términos con AI")
    bool_buscar = st.button("Buscar")
    # st.text(bool_buscar)
    # st.text(str_buscar!="")
    if  bool_buscar | (str_buscar!=""):
        dffinded = _find(str_buscar, dfglos)
        # ordenar la base
        subtable = dffinded.loc[dffinded['Process_n1_cod'].apply(lambda x: x in selected),['Código','Nombre','Definición']]
        st.table(subtable)
    else:
        # if buscar, get embedding, get normas, ordenar de mayor a menor similaridad
        # quedarnos con los mayores a 4 # da igual ya que usamos in
        subtable = dfglos.loc[dfglos['Process_n1_cod'].apply(lambda x: x in selected),['Código','Nombre','Definición']]
        st.table(subtable)
    

