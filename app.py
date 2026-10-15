import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

# 設定網頁標題與版面
st.set_page_config(page_title="台北一月氣溫分析網頁", page_icon="🌡️", layout="wide")

st.title("🌡️ 台北一月氣溫數據分析與地圖")
st.markdown("本應用程式正讀取您的 **TaipeiWeatherJan(1).csv** 溫度資料。")


# 讀取 CSV 檔案
@st.cache_data
def load_data():
  return pd.read_csv("TaipeiWeatherJan(1).csv")


try:
  df = load_data()

  # 顯示資料摘要（已將參數更新為 width='stretch'）
  st.subheader("📊 台北一月每日氣溫數據")
  st.dataframe(df, width="stretch")

  # 上下排版：左邊放折線圖，右邊放地圖與指標
  col1, col2 = st.columns(2)

  with col1:
    st.subheader("📈 一月每日氣溫趨勢圖")
    chart_data = df.set_index("Date")[
        ["HighTemperature", "MeanTemperature", "LowTemperature"]
    ]
    st.line_chart(chart_data)

  with col2:
    st.subheader("🗺️ 台北觀測站地理位置")
    taipei_lat, taipei_lon = 25.0330, 121.5654

    m = folium.Map(location=[taipei_lat, taipei_lon], zoom_start=12)
    folium.Marker(
        location=[taipei_lat, taipei_lon],
        popup="<b>台北氣象觀測點</b><br>一月份氣溫記錄分析",
        tooltip="台北市",
        icon=folium.Icon(color="red", icon="temperature-high", prefix="fa"),
    ).add_to(m)

    st_folium(m, width=500, height=350)

  # 快速統計數據
  st.subheader("📌 溫度重點摘要")
  m1, m2, m3 = st.columns(3)
  with m1:
    st.metric(
        label="最高溫紀錄",
        value=f"{df['HighTemperature'].max()} °C",
        delta="極端高溫",
    )
  with m2:
    st.metric(
        label="平均氣溫",
        value=f"{df['MeanTemperature'].mean():.1f} °C",
    )
  with m3:
    st.metric(
        label="最低溫紀錄",
        value=f"{df['LowTemperature'].min()} °C",
        delta="寒冷",
        delta_color="inverse",
    )

except FileNotFoundError:
  st.error(
      "找不到 `TaipeiWeatherJan(1).csv` 檔案！請確認它是否有和 `app.py`"
      " 放在同一個資料夾中。"
  )
except Exception as e:
  st.error(f"發生錯誤：{e}")