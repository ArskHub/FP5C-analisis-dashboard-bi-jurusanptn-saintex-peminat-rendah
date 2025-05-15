import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ======================= CONFIG & LOAD ========================
st.set_page_config(page_title="Dashboard Analisis Jurusan", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('Data/Data Jurusan Peminat Saintex.csv')
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.rename(columns={
        "nama_ptn": "asal_univ",
        "jurusan": "nama",
        "daya_tampung_(tahun_2025)": "daya_tampung_2025",
        "jumlah_peminat": "peminat"
    }, inplace=True)
    return df
df = load_data()

# ======================= SIDEBAR ========================
st.sidebar.title("🔍 Sistem Pencarian")
st.sidebar.markdown("Gunakan filter berikut untuk eksplorasi data:")

# Text input untuk mencari jurusan
search_jurusan = st.sidebar.text_input("Cari Jurusan:")

# Select box untuk memilih universitas
selected_univ = st.sidebar.selectbox("Pilih Universitas", ['Semua'] + sorted(df['asal_univ'].unique()))

# Select box untuk memilih jenjang
selected_jenjang = st.sidebar.selectbox("Pilih Jenjang", ['Semua'] + sorted(df['jenjang'].unique()))

# Select box untuk memilih provinsi (jika tersedia)
if 'provinsi' in df.columns:
    selected_provinsi = st.sidebar.selectbox("Pilih Provinsi", ['Semua'] + sorted(df['provinsi'].dropna().unique()))
else:
    selected_provinsi = 'Semua'

# Slider untuk jumlah peminat
min_peminat, max_peminat = int(df['peminat'].min()), int(df['peminat'].max())
range_peminat = st.sidebar.slider("Jumlah Peminat", min_peminat, max_peminat, (min_peminat, max_peminat))

# Slider untuk daya tampung
min_daya, max_daya = int(df['daya_tampung_2025'].min()), int(df['daya_tampung_2025'].max())
range_daya = st.sidebar.slider("Daya Tampung", min_daya, max_daya, (min_daya, max_daya))

# Slider untuk rasio keketatan
min_rasio, max_rasio = float(df['rasio_keketatan'].min()), float(df['rasio_keketatan'].max())
range_rasio = st.sidebar.slider("Rasio Keketatan", float(min_rasio), float(max_rasio), (float(min_rasio), float(max_rasio)))

# --- Filter Data ---
filtered_df = df.copy()

if search_jurusan:
    filtered_df = filtered_df[filtered_df['nama'].str.contains(search_jurusan, case=False, na=False)]

if selected_univ != 'Semua':
    filtered_df = filtered_df[filtered_df['asal_univ'] == selected_univ]

if selected_jenjang != 'Semua':
    filtered_df = filtered_df[filtered_df['jenjang'] == selected_jenjang]

if selected_provinsi != 'Semua':
    filtered_df = filtered_df[filtered_df['provinsi'] == selected_provinsi]

filtered_df = filtered_df[
    (filtered_df['peminat'] >= range_peminat[0]) & (filtered_df['peminat'] <= range_peminat[1]) &
    (filtered_df['daya_tampung_2025'] >= range_daya[0]) & (filtered_df['daya_tampung_2025'] <= range_daya[1]) &
    (filtered_df['rasio_keketatan'] >= range_rasio[0]) & (filtered_df['rasio_keketatan'] <= range_rasio[1])
]

# ======================= PROFIL KELOMPOK ========================
st.markdown("## 👥 Kelompok Analisis Data Jurusan")
colA, colB, colC, colD = st.columns(4)
with colA:
    st.image("images/eka.jpg", width=130, caption="Ni Putu Eka Martini - 568")
    st.markdown("`Data Sains`")
with colB:
    st.image("images/go.jpg", width=130, caption="Pande Komang Bhargo Anantha Yogiswara - 569")
    st.markdown("`Data Sains`")
with colC:
    st.image("images/ardi.jpg", width=130, caption="Putu Ardi Sudarmika - 570")
    st.markdown("`Data Sains`")
with colD:
    st.image("images/oni.jpg", width=130, caption="Putu Chandra Mayoni - 571")
    st.markdown("`Data Sains`")
st.success("**Nama Kelompok: Mini Time 5C**-Jurusan MIPA di Perguruan Tinggi yang sepi peminat namun mempunyai prospek kerja yang bagus ")

# ======================= STORYTELLING ========================
st.title("🎓 Dashboard Analisis Jurusan dengan Peminat Rendah namun Prospek Tinggi")
st.markdown("""
Pada era modern ini, pemilihan jurusan tidak hanya dilihat dari jumlah peminat, namun juga **prospek kerja** ke depan.  
Dashboard ini dirancang untuk membantu:
- 📊 Menganalisis jurusan dengan peminat rendah namun peluang kerja tinggi
- 🏫 Melihat distribusi daya tampung dan keketatan seleksi
- 💼 Meninjau gaji lulusan sebagai pertimbangan strategis
""")

# ======================= STATISTICS ========================
st.markdown("## 📌 Ringkasan Data")
col1, col2, col3 = st.columns(3)
col1.metric("Jumlah Jurusan Unik", filtered_df['nama'].nunique())
col2.metric("Jumlah PTN", filtered_df['asal_univ'].nunique())
col3.metric("Total Daya Tampung", filtered_df['daya_tampung_2025'].sum())

# ======================= VISUALISASI ========================
st.markdown("## 📈 Visualisasi Data")
# Top 10 Jurusan Peminat Terbanyak
st.markdown("### 1. 🔝 Top 10 Jurusan dengan Peminat Terendah")
top_jurusan = filtered_df.groupby('nama')['peminat'].sum().sort_values(ascending=True).head(10)
fig1, ax1 = plt.subplots(figsize=(12, 5))
sns.barplot(x=top_jurusan.values, y=top_jurusan.index, palette='viridis', ax=ax1)
ax1.set_title("Top 10 Jurusan Berdasarkan Peminat")
ax1.set_xlabel("Jumlah Peminat")
ax1.set_ylabel("Jurusan")
st.pyplot(fig1)
st.markdown("###### Keterangan: Grafik “Jurusan dengan Peminat Terendah” menampilkan sepuluh program studi dengan jumlah peminat paling sedikit, sebagian hanya 1-3 orang. Jurusan seperti Agrowisata Bahari, Budidaya Ternak, Tanaman Pangan, Pengelola Hutan, dan Ilmu Perpustakaan termasuk dalam daftar ini, kebanyakan terkait pertanian, kehutanan, perikanan, dan konservasi lingkungan.")


# Daya Tampung
st.markdown("### 2. 📚 Top 10 Jurusan dengan Daya Tampung Tertinggi")
top_daya = filtered_df.groupby('nama')['daya_tampung_2025'].sum().sort_values(ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(12, 5))
sns.barplot(x=top_daya.values, y=top_daya.index, palette='magma', ax=ax2)
ax2.set_title("Top 10 Jurusan Berdasarkan Daya Tampung 2025")
st.pyplot(fig2)
st.markdown("###### Keterangan: Visualisasi sepuluh jurusan saintek dengan daya tampung terbanyak di PTN Indonesia menunjukkan bahwa jurusan sains murni seperti Fisika, Biologi, Matematika, dan Kimia tetap memiliki daya tampung besar meskipun peminatnya sedikit. Teknik Elektro, Budidaya Perairan, dan Ilmu Kelautan tampil di dua grafik, tetapi daya tampungnya lebih kecil dari jumlah peminat, menandakan seleksi yang ketat. Pendidikan Kimia dan Teknik Mesin juga memiliki daya tampung tinggi tetapi tidak masuk daftar terfavorit, menunjukkan persaingan yang lebih longgar. ")


# Pie Chart Jenjang
st.markdown("### 3. 🏫 Distribusi Jenjang Pendidikan")
jenjang_count = filtered_df['jenjang'].value_counts()
fig3, ax3 = plt.subplots()
ax3.pie(jenjang_count, labels=jenjang_count.index, autopct='%1.1f%%', startangle=140)
ax3.set_title("Distribusi Jenjang Pendidikan")
st.pyplot(fig3)
st.markdown("###### Keterangan: Visualisasi menunjukkan distribusi jenjang pendidikan berdasarkan data. Berdasarkan visualisasi tersebut, Mayoritas program studi berada pada jenjang S1 (86,7%), sedangkan jenjang D3 dan D4 masing-masing hanya mencakup 8,9% dan 4,4%. Ini menunjukkan fokus utama institusi adalah pada pendidikan sarjana (S1). ")


st.markdown("### 4. Perbandingan Peminat dengan Daya Tampung")
# Hitung Top 8 dan Bottom 8 berdasarkan jumlah peminat
top_8 = filtered_df.groupby('nama')[['peminat', 'daya_tampung_2025']].sum().sort_values(by='peminat', ascending=False).head(8)
bottom_8 = filtered_df.groupby('nama')[['peminat', 'daya_tampung_2025']].sum().sort_values(by='peminat', ascending=True).head(8)
# Fungsi untuk menampilkan bar chart di Streamlit
def plot_dual_bar(data, title):
    fig, ax = plt.subplots(figsize=(12,6))
    data.plot(kind='bar', ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Jurusan")
    ax.set_ylabel("Jumlah")
    ax.set_xticklabels(data.index, rotation=45, ha='right')
    ax.legend(["Peminat", "Daya Tampung"])
    ax.grid(True)
    st.pyplot(fig)
# Tampilkan grafik untuk top 8
plot_dual_bar(top_8, "Top 8 Jurusan: Peminat vs Daya Tampung")
# Tampilkan grafik untuk bottom 8
plot_dual_bar(bottom_8, "Bottom 8 Jurusan: Peminat vs Daya Tampung")

st.markdown("###### Keterangan: Visualisasi menunjukkan semua jurusan memiliki peminat melebihi kapasitas, dengan jurusan seperti Fisika, Biologi, dan Matematika menunjukkan persaingan sangat ketat. Bahkan jurusan dengan peminat lebih sedikit, seperti Budidaya Perairan dan Ilmu Kelautan, tetap menunjukkan kompetisi tinggi akibat daya tampung terbatas, menandakan tingginya minat yang belum sejalan dengan kapasitas tersedia. Visualisasi menunjukkan bahwa banyak jurusan, seperti Budidaya Ternak, Tanaman Pangan, dan Tanaman Perkebunan, memiliki daya tampung sekitar 56 orang tetapi diminati hanya 1-3 orang, menunjukkan kurangnya minat calon mahasiswa. Demikian pula, jurusan seperti Agrowisata Bahari, Pengelola Hutan, dan Teknologi Budidaya Perikanan menunjukkan ketimpangan serupa, dengan kapasitas besar tetapi minim peminat. ")


st.markdown("### 5. Top 10 Jurusan dengan Rata-rata Gaji Tertinggi")
# Cek apakah kolom gaji tersedia
if 'rata-rata_gaji_lulusan' in df.columns:
    # Bersihkan nilai agar numerik
    filtered_df['gaji_bersih'] = filtered_df['rata-rata_gaji_lulusan'].replace('[^0-9]', '', regex=True).astype(float)
    # Ambil data dengan gaji tertinggi per jurusan
    data_filtered = filtered_df.loc[filtered_df.groupby('nama')['gaji_bersih'].idxmax()]
    # Top 10 jurusan dengan gaji tertinggi
    top_gaji_langsung = data_filtered[['nama', 'gaji_bersih']].sort_values(by='gaji_bersih', ascending=False).head(10)
    # Tampilkan tabel
    st.dataframe(top_gaji_langsung.rename(columns={"nama": "Jurusan", "gaji_bersih": "Gaji (Rp)"}))
    # Visualisasi bar chart horizontal
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='gaji_bersih', y='nama', data=top_gaji_langsung, palette='viridis', ax=ax)
    ax.set_title("Top 10 Jurusan dengan Gaji Tertinggi")
    ax.set_xlabel("Gaji (Rp)")
    ax.set_ylabel("Nama Jurusan")
    st.pyplot(fig)
else:
    st.warning("Kolom 'rata-rata_gaji_lulusan' tidak ditemukan dalam dataset. Harap periksa kembali nama kolom.")
    
st.markdown("### 💰 Jurusan dengan Rata-Rata Gaji Lulusan Tertinggi")
top_gaji = filtered_df.sort_values(by="rata-rata_gaji_lulusan", ascending=True).head(10)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_gaji, x="rata-rata_gaji_lulusan", y="nama", palette="crest", ax=ax)
ax.set_xlabel("Gaji (Rata-Rata)")
ax.set_ylabel("Jurusan")
st.pyplot(fig)  

st.markdown("### 📦 Distribusi Gaji Lulusan Berdasarkan Jenjang")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=filtered_df, x="jenjang", y="rata-rata_gaji_lulusan", palette="pastel", ax=ax)
ax.set_xlabel("Jenjang")
ax.set_ylabel("Gaji Lulusan")
st.pyplot(fig)
st.markdown("###### Keterangan: Visualisasi ini menunjukkan 10 jurusan dengan gaji bersih tertinggi, tanpa memperhitungkan rata-rata. Kehutanan berada di puncak dengan Rp14 juta, diikuti Kimia Rp12,5 juta, dan Ilmu Tanah muncul dua kali dengan Rp12 juta, menunjukkan variasi gaji dalam jurusan yang sama. Jurusan lain seperti Ilmu Kelautan, Teknik Elektro, dan Teknik Listrik juga menawarkan gaji tinggi. Bahkan jurusan yang kurang diminati seperti Budidaya Peternakan, Akuakultur, dan Proteksi Tanaman tetap memberikan gaji kompetitif sekitar Rp9-9,5 juta, menandakan prospek kerja yang menjanjikan meskipun minatnya rendah. ")


# Heatmap Provinsi
if 'provinsi' in df.columns:
    st.markdown("### 6. 🗺️ Heatmap Peminat per Provinsi")
    provinsi_data = filtered_df.groupby('provinsi')['peminat'].sum().reset_index()
    heatmap_data = provinsi_data.set_index('provinsi').T
    fig5, ax5 = plt.subplots(figsize=(12, 2))
    sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt=",.0f", cbar_kws={'label': 'Peminat'})
    ax5.set_title('Jumlah Peminat per Provinsi')
    st.pyplot(fig5)
st.markdown("###### Keterangan: Heatmap jumlah peminat berdasarkan provinsi di Indonesia menunjukkan bahwa Lampung memiliki peminat terbanyak, dengan warna paling gelap. Aceh, Jawa Tengah, dan Jawa Timur juga menunjukkan tingkat peminat tinggi, sedangkan Banten, Maluku, dan Sulawesi Barat menunjukkan jumlah peminat yang lebih rendah, terlihat dari warna yang lebih terang. ")


# Scatter Plot Keketan vs Gaji
# st.markdown("### 7. 💵 Gaji vs Keketatan")
# scatter_df = filtered_df[['rasio_keketatan', 'rata-rata_gaji_lulusan', 'nama']].dropna()
# scatter_df['rasio_keketatan'] = pd.to_numeric(scatter_df['rasio_keketatan'], errors='coerce')
# scatter_df['rata-rata_gaji_lulusan'] = pd.to_numeric(scatter_df['rata-rata_gaji_lulusan'], errors='coerce')
# scatter_df = scatter_df.dropna()
# fig4 = px.scatter(
#     scatter_df,
#     x='rasio_keketatan',
#     y='rata-rata_gaji_lulusan',
#     color='nama',
#     hover_name='nama',
#     title='Rasio Keketatan vs Rata-rata Gaji Lulusan',
#     labels={
#         "rasio_keketatan": "Rasio Keketatan",
#         "rata-rata_gaji_lulusan": "Gaji Lulusan (Rp)"
#     }
# )
# st.plotly_chart(fig4)
# st.markdown("##### Keterangan: ")


st.markdown("### 8. Top 20 Jurusan dengan Rasio Keketatan Tertinggi")
# Contoh data (Ganti dengan df = pd.read_csv() atau df asli Anda)
# df = pd.read_csv('path_dataset.csv')
# Pastikan kolom yang dibutuhkan ada
if 'rasio_keketatan' in df.columns and 'nama' in df.columns:
    # Urutkan data berdasarkan rasio keketatan tertinggi
    top_rasio = df.sort_values(by="rasio_keketatan", ascending=False).head(20)
    # Plot barplot horizontal
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(data=top_rasio, x="rasio_keketatan", y="nama", palette="viridis", ax=ax)
    ax.set_title("Top 20 Jurusan dengan Rasio Keketatan Tertinggi", fontsize=14)
    ax.set_xlabel("Rasio Keketatan (Peminat / Daya Tampung)", fontsize=12)
    ax.set_ylabel("Nama Jurusan", fontsize=12)
    st.pyplot(fig)
else:
    st.warning("Kolom 'rasio_keketatan' atau 'nama' tidak ditemukan dalam dataset. Harap pastikan nama kolom sesuai.")
st.markdown("###### Keterangan: Visualisasi ini menampilkan 20 jurusan dengan rasio keketatan tertinggi, dimana Fisika berada di posisi pertama, menandakan persaingan sangat ketat karena peminat jauh melebihi daya tampung. Jurusan lain seperti Budidaya Ternak, Tanaman Pangan, Pendidikan Fisika, Teknik Listrik, Agrowisata Bahari, dan Teknologi Perikanan juga menunjukkan tingkat persaingan tinggi. Umumnya, jurusan terkait pertanian, peternakan, dan perikanan mendominasi daftar ini, menggambarkan tingginya minat di bidang tersebut dibanding kapasitas yang tersedia.")

st.markdown("### 9. Rata-rata Rasio Keketatan per Universitas (Top 15)")
# Pastikan kolom yang dibutuhkan tersedia
if 'asal_univ' in df.columns and 'rasio_keketatan' in df.columns:
    # Hitung rata-rata rasio keketatan per universitas
    avg_rasio_univ = df.groupby("asal_univ")["rasio_keketatan"].mean().sort_values(ascending=False).head(15)
    # Visualisasi
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=avg_rasio_univ.values, y=avg_rasio_univ.index, palette="mako", ax=ax)
    ax.set_title("Rata-rata Rasio Keketatan per Universitas (Top 15)", fontsize=14)
    ax.set_xlabel("Rata-rata Rasio Keketatan", fontsize=12)
    ax.set_ylabel("Asal Universitas", fontsize=12)
    st.pyplot(fig)
else:
    st.warning("Kolom 'asal_univ' atau 'rasio_keketatan' tidak ditemukan dalam dataset.")
st.markdown("###### Keterangan: Visualisasi ini memperlihatkan 15 universitas dengan rata-rata rasio keketatan tertinggi, yang menandakan persaingan masuk yang sangat ketat di program studi masing-masing. Universitas Papua berada di posisi teratas, menunjukkan bahwa daya tampung sangat terbatas dibandingkan minat calon mahasiswa. Diikuti oleh Politeknik Perikanan Negeri Tual, Universitas Pattimura, dan Politeknik Negeri FakFak. Mayoritas universitas dalam daftar ini berasal dari wilayah Indonesia Timur, seperti Papua, Maluku, dan Nusa Tenggara, mencerminkan tingginya minat terhadap pendidikan tinggi di daerah tersebut meskipun kapasitasnya kecil.")


# Bubble Chart
st.markdown("### 10. 🧼 Bubble Chart: Peminat vs Daya Tampung")
# Cek apakah semua kolom tersedia
required_columns = ["peminat", "daya_tampung_2025", "rasio_keketatan", "jenjang"]
if all(col in df.columns for col in required_columns):
    # Konversi kategori jenjang ke kode numerik
    df["jenjang_kode"] = df["jenjang"].astype('category').cat.codes
    # Buat bubble chart
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(
        df["peminat"],
        df["daya_tampung_2025"],
        s=df["rasio_keketatan"] * 100,
        c=df["jenjang_kode"],
        alpha=0.6,
        cmap='Set3'
    )
    ax.set_xlabel("Jumlah Peminat")
    ax.set_ylabel("Daya Tampung")
    ax.set_title("Bubble Chart Rasio Keketatan per Jurusan")
    plt.colorbar(scatter, label="Jenjang (kode numerik)")
    ax.grid(True)
    plt.tight_layout()
    # Tampilkan plot di Streamlit
    st.pyplot(fig)
else:
    st.warning("Beberapa kolom yang dibutuhkan ('peminat', 'daya_tampung_2025', 'rasio_keketatan', 'jenjang') tidak ditemukan.")
st.markdown("###### Keterangan: Visualisasi ini menunjukkan bahwa jurusan dengan rasio keketatan tinggi umumnya memiliki daya tampung kecil dan tetap diminati, sehingga persaingan menjadi sangat ketat. Meskipun jurusan S1 lebih banyak, beberapa jurusan D3 dan D4 juga menunjukkan tingkat keketatan yang tinggi. Hal ini menegaskan bahwa tingkat keketatan dipengaruhi tidak hanya oleh jumlah peminat, tetapi juga oleh kapasitas daya tampung masing-masing jurusan. ")


st.markdown("### 11. Lollipop Chart: Rata-rata Rasio Keketatan per Universitas (Top 15)")
# Cek apakah kolom yang dibutuhkan tersedia
if "asal_univ" in df.columns and "rasio_keketatan" in df.columns:
    # Hitung rata-rata rasio keketatan per universitas
    avg_rasio_univ = df.groupby("asal_univ")["rasio_keketatan"].mean().sort_values(ascending=False).head(15)
    # Lollipop Chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.hlines(y=avg_rasio_univ.index, xmin=0, xmax=avg_rasio_univ.values, color='skyblue')
    ax.plot(avg_rasio_univ.values, avg_rasio_univ.index, "o", color='blue')
    ax.set_title("Rata-rata Rasio Keketatan per Universitas (Top 15)", fontsize=14)
    ax.set_xlabel("Rata-rata Rasio Keketatan", fontsize=12)
    ax.set_ylabel("Asal Universitas", fontsize=12)
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    # Tampilkan chart di Streamlit
    st.pyplot(fig)
else:
    st.warning("Kolom 'asal_univ' atau 'rasio_keketatan' tidak ditemukan dalam DataFrame.")
st.markdown("###### Keterangan: Visualisasi ini menampilkan 15 universitas dengan rasio keketatan tertinggi. Universitas Papua berada di posisi teratas dengan rasio sekitar 16, menunjukkan tingkat persaingan sangat tinggi. Politeknik Perikanan Negeri Tual dan Universitas Pattimura juga punya rasio tinggi, mendekati 11 dan 6. Sebaliknya, universitas seperti Tadulako, Timor, dan Malikussaleh memiliki rasio di bawah 2, menandakan selektivitas lebih rendah. Grafik ini menunjukkan variasi besar dalam tingkat persaingan masuk, terutama di kawasan timur dan tengah Indonesia.")


st.markdown("### 12. Jumlah Peminat Per Universitas dan Jurusan")
# Pastikan kolom yang dibutuhkan tersedia
required_columns = ['asal_univ', 'nama', 'peminat', 'jenjang']
if all(col in df.columns for col in required_columns):
    # Buat Treemap
    fig = px.treemap(
        df,
        path=['asal_univ', 'nama'],
        values='peminat',
        color='jenjang',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    # Tampilkan di Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Beberapa kolom yang dibutuhkan tidak ditemukan dalam DataFrame.")
st.markdown("###### Keterangan: Visualisasi ini menampilkan distribusi program studi sains di berbagai universitas Indonesia, dengan ukuran kotak menunjukkan jumlah program atau mahasiswa. Universitas Gadjah Mada, Diponegoro, dan Lampung memiliki keragaman terbesar, sementara jurusan Biologi, Fisika, dan Kimia paling umum. Beberapa universitas seperti Riau, Sriwijaya, dan Institut Teknologi Sumatera lebih fokus pada program tertentu. Warna-warna berbeda memudahkan identifikasi institusi, memberikan gambaran soal sebaran dan fokus program studi sains di tanah air. ")


st.markdown("### 13. Visualisasi Hirarki Universitas, Jenjang, dan Jurusan di Bali")
# Filter data for Bali province
df_bali = df[df['provinsi'].str.lower() == 'bali']
# Create the Sunburst chart
fig = px.sunburst(
    df_bali,
    path=['asal_univ', 'jenjang', 'nama'],  # Hierarchy: University > Level > Major
    values='peminat',
    color_discrete_sequence=px.colors.qualitative.Set2
)
# Update layout for better presentation
fig.update_layout(margin=dict(t=50, l=0, r=0, b=0))
# Display the plot
st.plotly_chart(fig)
st.markdown("###### Keterangan: Diagram sunburst ini menunjukkan program studi dengan jumlah peminat rendah di Universitas Udayana dan Universitas Ganesha. Di Udayana, seluruh program sepi peminat berada di jenjang S1 dan berasal dari rumpun sains dan teknologi, seperti Ilmu Kelautan dan Fisika. Di Ganesha, program sepi peminat tersebar di jenjang S1 dan D4, terutama bidang kependidikan seperti Pendidikan IPA dan Pendidikan Fisika, serta beberapa program non-kependidikan. Secara umum, program studi dari bidang sains dan kependidikan cenderung kurang diminati di kedua universitas, menjadi bahan evaluasi untuk meningkatkan daya tarik melalui inovasi kurikulum, prospek kerja, dan promosi. ")


# Visualisasi Tambahan

st.markdown("### 14. 📈 Histogram Distribusi Peminat")
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df['peminat'], bins=30, kde=True, color='skyblue', ax=ax)
ax.set_xlabel("Jumlah Peminat")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)
# st.markdown("##### Keterangan: ")

# ======================= FOOTER ========================
st.markdown("---")
st.markdown("""
📌 **Kesimpulan:**  
Data ini dapat menjadi panduan strategis bagi siswa maupun lembaga pendidikan dalam mengarahkan pilihan jurusan berbasis peluang karier.  
Dibuat oleh: `Mini Time 5C` | 2025
""")

# ======================= REKOMENDASI OTOMATIS ========================
st.markdown("## ✅ Rekomendasi Sistem")

if filtered_df.empty:
    st.warning("⚠️ Tidak ada jurusan yang sesuai dengan filter yang dipilih.")
else:
    lowest_peminat = filtered_df.nsmallest(5, 'peminat')
    st.markdown("### Jurusan dengan Peminat Terendah:")
    st.dataframe(lowest_peminat[['nama', 'asal_univ', 'peminat', 'daya_tampung_2025', 'rasio_keketatan']])

    highest_ratio = filtered_df.nlargest(5, 'rasio_keketatan')
    st.markdown("### Jurusan dengan Keketatan Tertinggi:")
    st.dataframe(highest_ratio[['nama', 'asal_univ', 'peminat', 'daya_tampung_2025', 'rasio_keketatan']])

    # Rekomendasi jurusan sepi peminat tapi prospek bagus
    rekomendasi = filtered_df[(filtered_df['peminat'] < 50) & (filtered_df['rasio_keketatan'] < 1)]
    if not rekomendasi.empty:
        st.markdown("### 🎯 Rekomendasi Jurusan Sepi Peminat & Peluang Masuk Besar:")
        st.dataframe(rekomendasi[['nama', 'asal_univ', 'peminat', 'daya_tampung_2025', 'rasio_keketatan']].sort_values(by='rasio_keketatan'))
    else:
        st.info("Tidak ditemukan jurusan dengan peminat rendah dan rasio keketatan rendah berdasarkan filter yang kamu pilih.")




import io

csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Unduh Hasil Pencarian (CSV)",
    data=csv_data,
    file_name='hasil_pencarian_jurusan.csv',
    mime='text/csv'
)
