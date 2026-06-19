import streamlit as st
from supabase import create_client

# Supabase bilgilerini kontrol et
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

def db_getir_gorevler(user_id):

    return supabase.table("tasks").select("*").eq("user_id", user_id).execute().data


def db_ekle_gorev(data):
    try:
        response = supabase.table("tasks").insert(data).execute()
        return response
    except Exception as e:
        # Hatanın detayını ekrana basıyoruz
        st.error(f"DETAYLI HATA: {str(e)}") 
        return None

def db_sil_gorev(task_id):
    try:
        response = supabase.table("tasks").delete().eq("id", task_id).execute()
        return response
    except Exception as e:
        st.error(f"DETAYLI HATA: {str(e)}")
        return None

def db_guncelle_gorev(task_id, data):
    try:
        response = supabase.table("tasks").update(data).eq("id", task_id).execute()
        return response
    except Exception as e:
        st.error(f"DETAYLI HATA: {str(e)}")
        return None