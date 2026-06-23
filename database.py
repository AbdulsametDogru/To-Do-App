import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

TASKS_SHEET_ID = "1h94-V1bQvD6B9uqOLT8VO8La7rs6e0dL161AcFgMxS0"
USERS_SHEET_ID = "1FlAraTsfGcDwxGiLa_18UeJMf31lqp_s_TvWd03oydw"


def get_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        dict(st.secrets),
        scopes=scopes
    )

    return gspread.authorize(creds)


def get_tasks_sheet():
    client = get_client()
    return client.open_by_key(TASKS_SHEET_ID).sheet1


def get_users_sheet():
    client = get_client()
    return client.open_by_key(USERS_SHEET_ID).sheet1


# ---------------- GÖREVLER ----------------

def db_getir_gorevler():
    sheet = get_tasks_sheet()
    return sheet.get_all_records()


def db_ekle_gorev(data):
    sheet = get_tasks_sheet()

    sheet.append_row([
        data["id"],
        data["ad"],
        data["durum"],
        data["zorluk"],
        data["son_tarih"],
        data["user_id"]
    ])


def db_sil_gorev(task_id):
    sheet = get_tasks_sheet()

    records = sheet.get_all_records()

    for i, row in enumerate(records, start=2):
        if row["id"] == task_id:
            sheet.delete_rows(i)
            break


def db_guncelle_gorev(task_id, data):
    sheet = get_tasks_sheet()

    records = sheet.get_all_records()

    for i, row in enumerate(records, start=2):
        if row["id"] == task_id:

            eski = row.copy()
            eski.update(data)

            sheet.update(
                f"A{i}:F{i}",
                [[
                    eski["id"],
                    eski["ad"],
                    eski["durum"],
                    eski["zorluk"],
                    eski["son_tarih"],
                    eski["user_id"]
                ]]
            )

            break


# ---------------- KULLANICILAR ----------------

def db_getir_kullanicilar():
    sheet = get_users_sheet()
    return sheet.get_all_records()


def db_kullanici_ekle(data):
    sheet = get_users_sheet()

    sheet.append_row([
        data["username"],
        data["password"]
    ])