import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Data
# Dataset per hari
day_df = pd.read_csv("day.csv")
day_df.head()

# Dataset per jam
hour_df = pd.read_csv("hour.csv")
hour_df.head()

# Mengubah tipe data object menjadi datetime

# Dataset per hari
for column1 in ["dteday"]:
  day_df[column1] = pd.to_datetime(day_df[column1])

# Dataset per jam
for column2 in ["dteday"]:
  hour_df[column2] = pd.to_datetime(hour_df[column2])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Bagian Header
st.header('Bike Sharing Dashboard :sparkles:')
st.subheader('Growth of Bike Sharing Users Each Month (2011 vs 2012)')

# Membuat duplikat dataset
day_df_vis = day_df.copy()
hour_df_vis = hour_df.copy()

# Melakukan mapping kolom 'yr' menggunakan dictionary
yr_change = {0: '2011', 1: '2012'}
day_df_vis['yr'] = day_df_vis['yr'].map(yr_change)
hour_df_vis['yr'] = hour_df_vis['yr'].map(yr_change)

# Mengkonversi bulan dalam integer ke dalam bentuk bulan
mnth_change = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
day_df_vis['mnth'] = day_df_vis['mnth'].map(mnth_change)
hour_df_vis['mnth'] = hour_df_vis['mnth'].map(mnth_change)

# Melakukan sorting dengan bulan
months_in_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
day_df_vis['mnth'] = pd.Categorical(day_df_vis['mnth'], categories=months_in_order, ordered=True)
day_df_vis.sort_values(by ="mnth", inplace=True)
hour_df_vis['mnth'] = pd.Categorical(hour_df_vis['mnth'], categories=months_in_order, ordered=True)
hour_df_vis.sort_values(by ="mnth", inplace=True)

# Menggabungkan kedua data csv day.csv dan hour.csv menjadi satu data dan menghilangkan data duplikat
bike_combined_df = pd.concat([day_df_vis, hour_df_vis], ignore_index=True).drop_duplicates(subset=['dteday'])

# Mendefinisikan dataset untuk tiap tahunnya
bike_2011 = bike_combined_df[bike_combined_df['yr'] == "2011"]  # 2011
bike_2012 = bike_combined_df[bike_combined_df['yr'] == "2012"]  # 2012

# Mengelompokkan data berdasarkan jumlah pengguna tiap bulannya untuk tahun 2011 dan 2012
months_2011 = bike_2011.groupby('mnth')['cnt'].sum()
months_2012 = bike_2012.groupby('mnth')['cnt'].sum()

# Plot data
plt.plot(months_2011.index, months_2011.values, label='2011')
plt.plot(months_2012.index, months_2012.values, label='2012')


# Menambahkan label dan judul
plt.xlabel('Month')
plt.ylabel('Total of Bike Users ')
plt.title('Numbers of Bike Users Each Month (2011 vs 2012)')

# Menambahkan legenda
plt.legend()

# Menampilkan plot data
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.show()
st.pyplot()

# Berdasarkan Cuaca
st.subheader('Number of Total Customers Based on Weather Condition')

# Membuat duplikat dataset
day_df_new = day_df.copy()
hour_df_new = hour_df.copy()

# Melakukan pendefinisian dictionary untuk tiap keys (int) dan values (cuaca)
weather_change = {1: 'Clear, Few clouds, Partly cloudy, Partly cloudy', 2: 'Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist', 3: 'Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds', 4: 'Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'}

# Mengubah nilai int pada kolom "weathersit" menjadi string berupa cuaca
day_df_new['weathersit'] = day_df_new['weathersit'].map(weather_change)
hour_df_new['weathersit'] = hour_df_new['weathersit'].map(weather_change)


# Mengelompokan data berdasarkan kondisi cuaca dan menghitung total jumlah pengguna untuk tiap kondisi cuaca
grouped_df = hour_df_new.groupby('weathersit')['cnt'].sum().reset_index()

# Mengurutkan data berdasarkan jumlah pengguna
grouped_df.sort_values(by='cnt', inplace=True)

# Plot histogram
plt.barh(y=grouped_df["weathersit"], width=grouped_df["cnt"], color='gray')
max_index = grouped_df["cnt"].idxmax()
plt.barh(y=grouped_df.loc[max_index, "weathersit"], width=grouped_df.loc[max_index, "cnt"], color='blue')
plt.xlabel('Number of Users')
plt.ylabel('Weather')
plt.title('Number of Total Users For Each Weather Condition')


plt.show()
st.pyplot()

# Berdasarkan Musim
st.subheader('Number of Total Customers Based on Seasons')

# Melakukan pendefinisian dictionary untuk tiap keys (int) dan values (musim)
season_change = {1: 'spring', 2: 'summer', 3: 'fall', 4: 'winter'}

# Mengubah nilai int pada kolom "season" menjadi string berupa musim
day_df_new['season'] = day_df_new['season'].map(season_change)
hour_df_new['season'] = hour_df_new['season'].map(season_change)

# Mengelompokkan data berdasarkan musim (per hari)
day_df_new.groupby(by="season")['cnt'].sum().sort_values(ascending=False)

# Mengelompokkan data berdasarkan musim (per jam)
hour_df_new.groupby(by="season")['cnt'].sum().sort_values(ascending=False)

# Menggabungkan kedua data csv day.csv dan hour.csv menjadi satu data dan menghilangkan data duplikat
bike_combined_df = pd.concat([day_df_new, hour_df_new], ignore_index=True).drop_duplicates(subset=['dteday'])

# Mengelompokan data berdasarkan musim dan menghitung total jumlah pengguna untuk tiap musim
grouped_df = bike_combined_df.groupby('season')['cnt'].sum().reset_index()

# Mengurutkan data berdasarkan jumlah pengguna
grouped_df.sort_values(by='cnt', inplace=True)

# Plot histogram
plt.bar(x=grouped_df["season"], height=grouped_df["cnt"], color='gray')
max_index = grouped_df["cnt"].idxmax()
plt.bar(x=grouped_df.loc[max_index, "season"], height=grouped_df.loc[max_index, "cnt"], color='blue')
plt.xlabel('Season')
plt.ylabel('Number of Users')
plt.title('Number of Total Customers Based on Seasons')

plt.show()
st.pyplot()

# Berdasarkan Jenis Hari
st.subheader('Number of Total Customers Based on Working Days')

# Melakukan pendefinisian dictionary untuk tiap keys (int) dan values (jenis hari)
workingday_change = {0: 'hari libur', 1: 'hari kerja'}

# Mengubah nilai int pada kolom "workingday" menjadi string berupa jenis hari
day_df_new['workingday'] = day_df_new['workingday'].map(workingday_change)
hour_df_new['workingday'] = hour_df_new['workingday'].map(workingday_change)

# Mengelompokkan data berdasarkan hari kerja atau hari libur (per hari)
day_df_new.groupby(by="workingday")['cnt'].sum().sort_values(ascending=False)

# Mengelompokkan data berdasarkan hari kerja atau hari libur (per jam)
hour_df_new.groupby(by="workingday")['cnt'].sum().sort_values(ascending=False)

# Menghitung total jumlah pengguna untuk tiap kategori hari kerja (tidak termasuk weekend dan tanggal merah) dan hari libur

# Menggabungkan kedua data csv day.csv dan hour.csv menjadi satu data dan menghilangkan data duplikat
bike_combined_df = pd.concat([day_df_new, hour_df_new], ignore_index=True).drop_duplicates(subset=['dteday'])

# Menghitung rata-rata pengguna untuk tiap hari kerja (tidak termasuk weekend dan tanggal merah) dan hari libur

# Menggabungkan kedua data csv day.csv dan hour.csv menjadi satu data dan menghilangkan data duplikat
bike_combined_df = pd.concat([day_df_new, hour_df_new], ignore_index=True).drop_duplicates(subset=['dteday'])

# Mengelompokan data berdasarkan jenis hari dan menghitung total jumlah pengguna untuk tiap jenis hari
grouped_df = bike_combined_df.groupby('workingday')['cnt'].mean().round().reset_index()

# Mengurutkan data berdasarkan jumlah pengguna
grouped_df.sort_values(by='cnt', inplace=True)

# Plot histogram
plt.bar(x=grouped_df["workingday"], height=grouped_df["cnt"], color='gray')
max_index = grouped_df["cnt"].idxmax()
plt.bar(x=grouped_df.loc[max_index, "workingday"], height=grouped_df.loc[max_index, "cnt"], color='blue')
plt.xlabel('Workdays or Non-Workdays')
plt.ylabel('Number of Average Users')
plt.title('Number of Average Users Based on Working Day')

plt.show()
st.pyplot()

# Berdasarkan Hari
st.subheader('Number of Total Customers Based on Days of The Week')

# Melakukan pendefinisian dictionary untuk tiap keys (int) dan values (hari)
weekday_change = {0: 'minggu', 1: 'senin', 2: 'selasa', 3: 'rabu', 4: 'kamis', 5: 'jumat', 6:'sabtu'}

# Mengubah nilai int pada kolom "weekday" menjadi string berupa hari
day_df_new['weekday'] = day_df_new['weekday'].map(weekday_change)
hour_df_new['weekday'] = hour_df_new['weekday'].map(weekday_change)

# Mengelompokkan data berdasarkan hari (day.csv)
day_df_new.groupby(by="weekday")['cnt'].sum().sort_values(ascending=False)

# Mengelompokkan data berdasarkan hari (hour.csv)
hour_df_new.groupby(by="weekday")['cnt'].sum().sort_values(ascending=False)

# Menggabungkan kedua data csv day.csv dan hour.csv menjadi satu data dan menghilangkan data duplikat
bike_combined_df = pd.concat([day_df_new, hour_df_new], ignore_index=True).drop_duplicates(subset=['dteday'])

# Mengelompokan data berdasarkan jenis hari dan menghitung total jumlah pengguna tiap harinya
grouped_df = bike_combined_df.groupby('weekday')['cnt'].mean().round().reset_index()

# Mengurutkan data berdasarkan jumlah pengguna
grouped_df.sort_values(by='cnt', inplace=True)

# Plot histogram
plt.bar(x=grouped_df["weekday"], height=grouped_df["cnt"], color='gray')
max_index = grouped_df["cnt"].idxmax()
plt.bar(x=grouped_df.loc[max_index, "weekday"], height=grouped_df.loc[max_index, "cnt"], color='blue')
plt.xlabel('Day of The Week')
plt.ylabel('Number of Users')
plt.title('Number of Users Based on Based on Working Day')

plt.show()
st.pyplot()

# Berdasarkan Hari
st.subheader('Percentage of Registered Users and casual Users')

# Menghitung persentase dari pengguna kasual terhadap pengguna total
bike_combined_df['registered_percentage'] = (bike_combined_df['registered'] / bike_combined_df['cnt']) * 100

# Menghitung persentase dari pengguna teregistrasi terhadap pengguna total
bike_combined_df['casual_percentage'] = (bike_combined_df['casual'] / bike_combined_df['cnt']) * 100

# Membuat pie plot
plt.figure(figsize=(8, 6))
explode = (0.1, 0)
plt.pie([bike_combined_df['registered_percentage'].sum(), bike_combined_df['casual_percentage'].sum()], labels=['Registered Users', 'Casual Users'], autopct='%1.1f%%', startangle=140, colors=['red', 'orange'], explode=explode)

# Judul
plt.title('Percentage of Registered Users and casual Users')

# Plot pie
plt.axis('equal')

plt.show()
st.pyplot()


# Analisis RFM
st.subheader('RFM Analysis')

# Parameter RFM
recency = len(bike_combined_df) - 1  
frequency = bike_combined_df['cnt'].mean()  
monetary = bike_combined_df['cnt'].sum()    

# Plot RFM scores
plt.bar(['Recency', 'Frequency', 'Monetary'], [recency, frequency, monetary], color=['blue', 'orange', 'green'])
plt.title('Analisis RFM')
plt.xlabel('Metrik RFM')
plt.ylabel('Nilai')

plt.show()
st.pyplot()

st.caption('Copyright © Caleb Effendi 2024')