
import streamlit as st
import pandas as pd

st.set_page_config(page_title="LGS Tercih Robotu 2025 - Aralıklı Tahmin", layout="wide")
st.title("🎯 LGS Tercih Robotu 2025 (Okul Bazlı Aralıklı Tahmin)")

# Veri yükleme
df = pd.read_csv("veri_2025_tahminli_aralikli.csv")

# İlçe seçimi
ilceler = sorted(df["İLÇE"].dropna().unique())
secili_ilceler = st.multiselect("📍 İlçeleri Seçin", options=ilceler, default=ilceler)

# Okul türü seçimi
turler = sorted(df["OKUL TÜRÜ"].dropna().unique())
secili_turler = st.multiselect("🏫 Okul Türünü Seçin", options=turler, default=turler)

# Filtreleme (ikisini birden uygula)
df_filtreli = df[
    (df["İLÇE"].isin(secili_ilceler)) &
    (df["OKUL TÜRÜ"].isin(secili_turler))
]

# Kullanıcı girişi
st.sidebar.header("🎯 Kendi Bilgilerin")
yuzdelik = st.sidebar.number_input("📌 Yüzdelik Diliminiz (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)

# Aralık filtresi: 2025 tahmini aralığı içinde kalanlar
def eslesiyor_mu(satir):
    try:
        aralik = satir["2025 Tahmin"]
        alt, ust = aralik.split("–")
        alt = float(alt.strip())
        ust = float(ust.strip())
        return alt <= yuzdelik <= ust
    except:
        return False

eslesen_okullar = df_filtreli[df_filtreli.apply(eslesiyor_mu, axis=1)]

# Sonuçları göster
st.subheader(f"📋 {yuzdelik} yüzdelik dilimine uygun okullar")
st.markdown("📉 *2025 tahminleri okul bazlı geçmiş verilere dayalıdır. Her okul için hata payı farklıdır.*")

st.dataframe(eslesen_okullar[["İLÇE", "OKUL ADI", "2022", "2023", "2024", "2025 Tahmin", "OKUL TÜRÜ"]])
