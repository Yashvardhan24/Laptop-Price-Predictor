import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict" 

st.title("Laptop Price Predictor")
st.markdown("Enter your details below:")

# Input fields
company = st.selectbox('Brand',options=['Apple', 'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'MSI', 'Toshiba', 'Samsung', 'Razer', 'Microsoft', 'Google', 'Huawei', 'LG', 'Sony', 'Chuwi'])
type = st.selectbox('Type',options=['Ultrabook', 'Notebook', 'Gaming', '2 in 1 Convertible', 'Workstation', 'Netbook', 'Tablet'])
ram = st.selectbox('RAM(in GB)',[4, 8, 16, 32, 64])
weight = st.number_input('Weight of the Laptop')
touchscreen = st.selectbox('Touchscreen', ['Yes', 'No'])
ips = st.selectbox('IPS',['No','Yes'])

# screen size
screen_size = st.slider('Scrensize in inches', 10.0, 18.0, 13.0)

# resolution
resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])

#cpu
cpu = st.selectbox('CPU',options=['Intel Core i7','Intel Core i5','Other Intel Processor','Intel Core i3','AMD Processor','Other'])

hdd = st.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])

ssd = st.selectbox('SSD(in GB)',[0,8,128,256,512,1024])

gpu = st.selectbox('GPU',options=['Intel', 'Nvidia', 'AMD', 'Other'])

os = st.selectbox('OS',options=['Windows', 'Mac', 'Linux', 'No OS', 'Other'])



    
    
if st.button("Predict Laptop Price"):
    input_data = {
        "company": company,
        "type_name": type,
        "weight": weight,
        "ram": ram,
        "touchscreen": touchscreen,
        "ips": ips,
        "cpu_brand": cpu,
        "hdd": hdd,
        "ssd": ssd,
        "gpu_brand": gpu,
        "os": os  ,
        "screen_resolution": resolution
    }

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200:
            result = response.json()
            prediction = result["predicted_price"]
            st.success(f"Predicted Laptop Price : **{prediction}**")
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(response.text)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")