import streamlit as st
import pandas as pd 
import random
from datetime import date
import datetime
from template import *

st.set_page_config(page_title='Dashboard', page_icon=None, layout='wide', initial_sidebar_state='auto')
st.markdown("##")

UI()
st.markdown("##")

todayDate = datetime.date.today()
#currentYear = date.today().year
rondomNumber=(random.randint(0,10000))

#load excel file
df=pd.read_excel('data.xlsx', sheet_name='Sheet1')



#top analytics
def Analytics():
 purchasing_price_ = float(df['purchasing_price'].sum())
 selling_price_ = float(df['selling_price'].sum())
 profit = float(df['expected_profit'].sum())

#3. columns
 total1,total2,total3= st.columns(3,gap='small')
 with total1:

    st.info('Harga Pembelian', icon="🔍")
    st.metric(label = 'IDR', value= f"{purchasing_price_:,.0f}")
    
 with total2:
    st.info('Harga Penjualan', icon="🔍")
    st.metric(label= 'IDR', value=f"{selling_price_:,.0f}")

 with total3:
    st.info('Keuntungan yang Diharapkan', icon="🔍")
    st.metric(label= 'IDR',value=f"{profit:,.0f}")

Analytics()
st.markdown("""---""")


#form
st.sidebar.header("Tambahkan Produk Baru")
options_form=st.sidebar.form("Pilihan Formulir")
product_name=options_form.text_input("Nama")
product_type=options_form.selectbox("Tipe Barang",{"Baru","Bekas"})
category=options_form.selectbox("Jenis Barang",{"Sabun","Parfum","Krim","Lainnya"})
serial_number=options_form.text_input("ID Produk",value=rondomNumber,disabled=True)
date_added=options_form.text_input("Tanggal Pendaftaran",value=todayDate,disabled=True)
purchasing_price=options_form.number_input("Harga Beli")
selling_price=options_form.number_input("Harga Jual")
add_data=options_form.form_submit_button(label="Tambahkan Produk Baru")

#when button is clicked
if add_data:
 if product_name  !="":
     df = pd.concat([df, pd.DataFrame.from_records([{ 
         'nama_produk': product_name,
         'tipe':product_type,
         'kategori':category,
         'no_id':serial_number,
         'tanggal_pendaftaran':date_added,
         'harga_beli':float(purchasing_price),
         'harga_jual':float(selling_price),
         'keuntungan':selling_price-purchasing_price
         }])])
     try:
        df.to_excel("data.xlsx",index=False)
     except:
        st.warning("Unable to write, Please close your dataset !!")
 else:
    st.sidebar.error("product name required")

with st.expander("Riwayat"):
  shwdata = st.multiselect('Filter :', df.columns, default=['product_name','type','category','serialNo','date_added','purchasing_price','selling_price','expected_profit'])
  st.dataframe(df[shwdata],use_container_width=True)

with st.expander("Riwayat tab"):
     tab=pd.crosstab([df.category],df.type, margins=True)
     st.dataframe(tab) 