import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Data pelanggan
customer_id = ['06b8999e2fba1a1fbc88172c00ba8bc7', 
               '18955e83d337fd6b2def6b18a428ac77', 
               '4e7b3e00288586ebd08712fdd0374a03', 
               'b2b6027bc5c5109e529d4dc6358b12c3', 
               '4f2d8ab171c80ec8364f7c12e35b23ad']

customer_unique_id = ['861eff4711a542e4b93843c6dd7febb0', 
                      '290c77bc529b7ac935b93aa66c333dc3', 
                      '060e732b5b29e8181a18229c7b0b2b5e', 
                      '259dac757896d24d7702b9acbbff3f3c', 
                      '345ecd01c38d18a9036ed96c73b8d066']

customer_zip_code_prefix = [14409, 9790, 1151, 8775, 13056]
customer_city = ['franca', 'sao bernardo do campo', 'sao paulo', 'mogi das cruzes', 'campinas']
customer_state = ['SP', 'SP', 'SP', 'SP', 'SP']

customers_df = pd.DataFrame({
    'Customer ID': customer_id,
    'Customer Unique ID': customer_unique_id,
    'Zip Code': customer_zip_code_prefix,
    'Customer City': customer_city,
    'Customer State': customer_state
})

st.title('Visualisasi Jumlah Pelanggan berdasarkan Kota')

plt.figure(figsize=(10, 6))
sns.countplot(data=customers_df, x='Customer City', hue='Customer City', palette='Set2', legend=False)
plt.title('Jumlah Pelanggan berdasarkan Kota')
plt.xlabel('Kota')
plt.ylabel('Jumlah Pelanggan')
plt.xticks(rotation=45)

st.pyplot(plt)

# Data pesanan
order_id = ['e481f51cbdc54678b7cc49136f2d6af7', '53cdb2fc8bc7dce0b6741e2150273451', 
            '47770eb9100c2d0c44946d9cf07ec65d', '949d5b44dbf5de918fe9c16f97b45f8a', 
            'ad21c59c0840e6cb83a9ceb5573f8159']

customer_id = ['9ef432eb6251297304e76186b10a928d', 'b0830fb4747a6c6d20dea0b8c802d7ef', 
               '41ce2a54c0b03bf3443c3d931a367089', 'f88197465ea7920adcdbec7375364d82', 
               '8ab97904e6daea8866dbdbc4fb7aad2c']

order_status = ['delivered', 'delivered', 'delivered', 'delivered', 'delivered']

order_purchase_timestamp = ['10/2/2017 10:56', '7/24/2018 20:41', '8/8/2018 8:38', 
                            '11/18/2017 19:28', '2/13/2018 21:18']

order_approved_at = ['10/2/2017 11:07', '7/26/2018 3:24', '8/8/2018 8:55', 
                     '11/18/2017 19:45', '2/13/2018 22:20']

order_delivered_carrier_date = ['10/4/2017 19:55', '7/26/2018 14:31', '8/8/2018 13:50', 
                                '11/22/2017 13:39', '2/14/2018 19:46']

order_delivered_customer_date = ['10/10/2017 21:25', '8/7/2018 15:27', '8/17/2018 18:06', 
                                 '12/2/2017 0:28', '2/16/2018 18:17']

order_estimated_delivery_date = ['10/18/2017 0:00', '8/13/2018 0:00', '9/4/2018 0:00', 
                                 '12/15/2017 0:00', '2/26/2018 0:00']

orders_df = pd.DataFrame({
    'Order ID': order_id,
    'Customer ID': customer_id,
    'Order Status': order_status,
    'Order Purchase Timestamp': order_purchase_timestamp,
    'Order Approved At': order_approved_at,
    'Order Delivered Carrier Date': order_delivered_carrier_date,
    'Order Delivered Customer Date': order_delivered_customer_date,
    'Order Estimated Delivery Date': order_estimated_delivery_date
})

orders_df['Order Purchase Timestamp'] = pd.to_datetime(orders_df['Order Purchase Timestamp'])
orders_df['Order Delivered Customer Date'] = pd.to_datetime(orders_df['Order Delivered Customer Date'])

orders_df['Delivery Time'] = (orders_df['Order Delivered Customer Date'] - orders_df['Order Purchase Timestamp']).dt.days

st.title('Visualisasi Waktu Pengiriman Pesanan')

plt.figure(figsize=(10, 6))
sns.boxplot(y=orders_df['Delivery Time'])
plt.title('Waktu Pengiriman Pesanan (dalam hari)')
plt.ylabel('Waktu Pengiriman (hari)')
plt.grid()

st.pyplot(plt)