#%%
# INITIALIZATION
import pandas as pd
import numpy as np
import pickle
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

#%%


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
######################################
# procesos
# dfproc = pd.read_excel(path_str / "00.Data/04. Procesos_codigos_nombres.xlsx", sheet_name='Hoja1')
# dfproc = pd.read_excel(path_str / "00.Data/05. Dominios_codigos_nombres.xlsx", sheet_name='Dominios')

dfglos = pd.read_pickle(path_str /"00.Data/dfglos_embedd_clustered_dominios.pickle")
# dfglos = dfglos.rename({'codigo termino':'Código','termino':'Nombre','definicion termino':'Definición'}, axis=1)

#%% 
#########################

with open(path_str / "00.Data/06._Tree_dominios.pickle",'rb') as f:
    tree = pickle.load(f)

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
        subtable = dffinded.loc[dffinded['Dom_n1_cod'].apply(lambda x: x in selected),['Código','Nombre','Definición']]
        st.table(subtable)
    else:
        # if buscar, get embedding, get normas, ordenar de mayor a menor similaridad
        # quedarnos con los mayores a 4 # da igual ya que usamos in
        subtable = dfglos.loc[dfglos['Dom_n1_cod'].apply(lambda x: x in selected),['Código','Nombre','Definición']]
        st.table(subtable)
    

