import streamlit as st
import csv
import os

FILENAME = 'inventory.csv'

# --- הגדרת תצוגת האפליקציה ---
st.set_page_config(page_title="מלאי מזגנים", page_icon="❄️")
st.title("❄️ מערכת ניהול מחסן מזגנים")

# --- הפונקציה שלך (מאחורי הקלעים) ---
def add_or_update_part(part_id, part_name, quantity_to_add):
    inventory = []
    part_found = False
    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r', newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                if row['part_id'] == str(part_id):
                    row['quantity'] = str(int(row['quantity']) + int(quantity_to_add))
                    part_found = True
                inventory.append(row)
    if not part_found:
        inventory.append({'part_id': str(part_id), 'part_name': part_name, 'quantity': str(quantity_to_add)})
    
    with open(FILENAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['part_id', 'part_name', 'quantity'])
        writer.writeheader()
        writer.writerows(inventory)

# --- חלק 1: הוספה או עדכון מלאי ---
st.subheader("➕ עדכון מלאי נכנס/יוצא")
col1, col2, col3 = st.columns(3)

with col1:
    p_id = st.text_input("מק\"ט (למשל: 101)")
with col2:
    p_name = st.text_input("שם החלק")
with col3:
    # מאפשר גם להכניס מינוס אם לקחת חלק ללקוח!
    qty = st.number_input("כמות (השתמש במינוס להורדה)", value=1, step=1)

if st.button("עדכן את המחסן!", use_container_width=True):
    if p_id and p_name:
        add_or_update_part(p_id, p_name, qty)
        st.success(f"העדכון בוצע בהצלחה! {qty} יחידות של {p_name}.")
    else:
        st.error("אנא הזן מק\"ט ושם חלק.")

st.divider()

# --- חלק 2: צפייה בכל המחסן בזמן אמת ---
st.subheader("📦 מה יש כרגע במלאי?")
if os.path.exists(FILENAME):
    with open(FILENAME, mode='r', newline='', encoding='utf-8') as file:
        data = list(csv.DictReader(file))
        if data:
            # מציג את הנתונים כטבלה יפה
            st.dataframe(data, use_container_width=True)
        else:
            st.info("המחסן ריק כרגע.")
else:
    st.info("קובץ המלאי עדיין לא קיים.")