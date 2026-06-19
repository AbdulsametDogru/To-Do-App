import streamlit as st
from supabase import create_client

# Supabase bağlantısı (Streamlit secrets'tan okur)
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def db_getir_gorevler(user_id):
    # RLS sayesinde user_id ile sadece o kullanıcıya ait veriler gelir
    return supabase.table("tasks").select("*").eq("user_id", user_id).execute().data

def db_ekle_gorev(task_dict):
    return supabase.table("tasks").insert(task_dict).execute()

def db_sil_gorev(task_id):
    return supabase.table("tasks").delete().eq("id", task_id).execute()

def db_guncelle_gorev(task_id, task_dict):
    return supabase.table("tasks").update(task_dict).eq("id", task_id).execute()