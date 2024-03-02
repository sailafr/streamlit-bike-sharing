import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

day_df = pd.read_csv("day.csv")

def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
    })
    daily_rent_df = daily_rent_df.reset_index()
    return daily_rent_df

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Select Date',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

#Header
st.header('Bike Sharing Dashboard:bicyclist:')

#Sub header daily rent
st.subheader('Daily Rent')
 
col1, col2 = st.columns(2)
 
with col1:
    total_rent = main_df.cnt.sum()
    st.metric("Total rent", value=total_rent)
 
with col2:
    total_non_registered = main_df.casual.sum()
    total_registered = main_df.registered.sum()
    st.metric("Total non registered", value=total_non_registered)
    st.metric("Total registered", value=total_registered)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    main_df["dteday"],
    main_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#DC143C"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

#subheader Best Season and Weather
st.subheader("Best Season and Weather Rent")

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(30, 35))
plt.subplots_adjust(wspace=2)
seasons = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}
day_df['Musim'] = day_df['season'].map(seasons)

season = day_df.groupby('Musim')['cnt'].mean().reset_index().sort_values(by="cnt")

sns.barplot(y= 'Musim', x='cnt', data = season, palette = 'PuOr_r', hue='Musim', legend=False, ax= ax1)
ax1.set_xlabel("Number of Bikes Rented", fontsize=40)
ax1.set_title("Bikes to Rent in Every Season", fontsize=55)

weather_condi = {
    1: 'Clear',
    2: 'Cloudy',
    3: 'Light Rain',
    4: 'Heavy Rain'
}
day_df['weather_con'] = day_df['weathersit'].map(weather_condi)

weather = day_df.groupby('weather_con')['cnt'].mean().reset_index().sort_values("cnt", ascending = False)

label = weather['weather_con']
value = weather['cnt']
colors = ('#58cc0e', '#dcf135', '#f14a35')
explode = (0.1, 0, 0)

ax2.pie(
    x=value,
    labels=label,
    autopct='%1.1f%%',
    colors=colors,
    textprops = {'fontsize': 45},
    explode=explode,
)
plt.title("Best Weather", fontsize=60, loc ='left', pad=20)

st.pyplot(fig)

#subheader perbedaan jumlah sepeda yang disewa selama workingday dan selain workingday
st.subheader("Bicycles to Rent During Working Day and Non-Working Days")
days_work = {
    1: 'Working Day',
    0: 'Non Working Day'
}
day_df['day_work'] = day_df['workingday'].map(days_work)

year_work = {
    0: '2011',
    1: '2012'
}
day_df['year_work'] = day_df['yr'].map(year_work)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6,4))
sns.barplot(data=day_df, x=day_df['year_work'], y="cnt", hue=day_df['day_work'], errorbar=None, ax=ax)
st.pyplot(fig)

#Subheader performa 5 bulan terakhir
st.subheader("Performance of Bikes Rented Over the Last 5 Months")
# menampilkan lima baris pertama data bulanan
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df.set_index('dteday')

monthly_df = day_df.resample(rule='ME', on='dteday').agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
})

# mengubah format tanggal indeks monthly_df menjadi '%Y-%m-%d'
monthly_df.index = monthly_df.index.strftime('%Y-%m-%d')

# mengubah nama kolom
monthly_df.rename(columns={
    "casual": "Casual",
    "registered": "Registered",
    "cnt": "Count"
}, inplace=True)
monthly_df.tail()

monthly_tail = monthly_df.tail()

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(5, 5), constrained_layout=True)

#Membuat plot pengguna biasa
    ax.plot(monthly_tail.index, monthly_tail['Casual'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Casual')
    ax.set_title('Casual Bicycle Users in the Last 5 Months')
    st.pyplot(fig)

with col2:
#Membuat plot pengguna terdaftar
    fig, ax = plt.subplots(figsize=(5, 5), constrained_layout=True)
    ax.plot(monthly_tail.index, monthly_tail['Registered'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Registered')
    ax.set_title('Registered Bicycle Users in the Last 5 Months')
    st.pyplot(fig)

#Membuat plot pengguna total
fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
ax.plot(monthly_tail.index, monthly_tail['Count'])
ax.set_xlabel('Date')
ax.set_ylabel('Count')
ax.set_title('Total Bicycle Users in the Last 5 Months')
st.pyplot(fig)
 
#Analisis Lanjutan
fig2, ax2 = plt.subplots(figsize=(5,5), constrained_layout=True)
sns.heatmap(monthly_df.corr(), annot=True, cmap="Blues", ax=ax2)
ax2.set_title('Correlation of Total Bicycle Users with regular and registered users')
st.pyplot(fig2)

st.caption('Copyright (c) Dicoding 2024')