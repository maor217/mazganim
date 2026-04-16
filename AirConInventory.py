import streamlit as st
import pandas as pd
import os

# הגדרות דף
st.set_page_config(page_title="מחסן מזגנים", page_icon="❄️", layout="wide")

# נתיב לקובץ הנתונים
FILENAME = 'inventory.csv'

# פונקציה לטעינת נתונים
def load_data():
    if os.path.exists(FILENAME):
        return pd.read_csv(FILENAME)
    else:
        return pd.DataFrame(columns=['part_id', 'part_name', 'quantity'])

# טעינת הנתונים
df = load_data()

st.title("❄️ מערכת ניהול מחסן מזגנים")

# --- חלק 1: עדכון מלאי ---
st.subheader("➕ עדכון מלאי נכנס/יוצא")
col1, col2, col3 = st.columns(3)

with col1:
    part_id = st.text_input("מק\"ט (למשל: 101)")
with col2:
    part_name = st.text_input("שם החלק")
with col3:
    quantity_to_add = st.number_input("כמות (השתמש במינוס להורדה)", value=1, step=1)

if st.button("עדכן את המחסן!"):
    if part_id and part_name:
        # בדיקה אם החלק כבר קיים
        df['part_id'] = df['part_id'].astype(str)
        if part_id in df['part_id'].values:
            df.loc[df['part_id'] == part_id, 'quantity'] += quantity_to_add
        else:
            new_row = pd.DataFrame({'part_id': [part_id], 'part_name': [part_name], 'quantity': [quantity_to_add]})
            df = pd.concat([df, new_row], ignore_index=True)
        
        # שמירה לקובץ
        df.to_csv(FILENAME, index=False)
        st.success(f"המלאי עבור {part_name} עודכן בהצלחה!")
        st.rerun()
    else:
        st.error("חובה להזין מק\"ט ושם חלק")

st.divider()

# --- חלק 2: הצגת מלאי וחיפוש ---
st.subheader("📦 מה יש כרגע במלאי?")

# שורת חיפוש
search_term = st.text_input("🔍 חיפוש מהיר (לפי שם או מק\"ט):")

# סינון הנתונים
if search_term:
    df_filtered = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]
else:
    df_filtered = df

# הצגת הטבלה
st.dataframe(df_filtered, use_container_width=True)

# הודעה אם המלאי ריק
if df.empty:
    st.info("המחסן ריק כרגע. הוסף חלקים למעלה.")