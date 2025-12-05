from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd
import numpy as np

with open('pipe.pkl', 'rb') as f:
    model = pickle.load(f)


app = FastAPI()

class UserInput(BaseModel):
    company: Literal['Apple', 'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'MSI', 'Toshiba', 'Samsung', 'Razer', 'Microsoft', 'Google', 'Huawei', 'LG', 'Sony', 'Chuwi'] = Field(description="Laptop manufacturer")
    type_name: Literal['Ultrabook', 'Notebook', 'Gaming', '2 in 1 Convertible', 'Workstation', 'Netbook', 'Tablet'] = Field(description="Type of the laptop")
    weight: Annotated[float, Field(gt=0, description="Weight of the laptop in kg")]
    ram: Literal[4, 8, 16, 32, 64] = Field(description="RAM size in GB")
    touchscreen: Literal['Yes', 'No'] = Field(description="Whether the laptop has a touchscreen or not")
    ips: Literal['Yes', 'No'] = Field(description="Whether the laptop has an IPS display or not")
    cpu_brand: Literal['Intel Core i7','Intel Core i5','Other Intel Processor','Intel Core i3','AMD Processor','Other'] = Field(description="Brand of the CPU")
    hdd: Literal[0,128,256,512,1024,2048] = Field(description="HDD size in GB")
    ssd: Literal[0,8,128,256,512,1024] = Field(description="SSD size in GB")
    gpu_brand: Literal['Intel', 'Nvidia', 'AMD', 'Other'] = Field(description="Brand of the GPU")
    os: Literal['Windows', 'Mac', 'Linux', 'No OS', 'Other'] = Field(description="Operating System")
    screen_resolution: Literal['1920x1080', '1366x768', '2560x1440', '3840x2160', '2256x1504', '3000x2000', '3200x1800', '2736x1824', '2400x1600'] = Field(description="Screen resolution of the laptop")

    @computed_field
    @property
    def touchscreen_binary(self) -> int:
        return 1 if self.touchscreen == 'Yes' else 0
    
    @computed_field
    @property
    def ips_binary(self) -> int:
        return 1 if self.ips == 'Yes' else 0
    
    @computed_field
    @property
    def ppi(self) -> float:
        width, height = map(int, self.screen_resolution.split('x'))
        diagonal = ((width ** 2) + (height ** 2)) ** 0.5
        return diagonal / (self.weight if self.weight > 0 else 1)

@app.post('/predict')
def predict_price(user_input: UserInput):
    input_data = pd.DataFrame([{  
        'Company': user_input.company,
        'TypeName': user_input.type_name,
        'Ram': user_input.ram,
        'Weight': user_input.weight,
        'Touchscreen': user_input.touchscreen_binary,
        'Ips': user_input.ips_binary,
        'ppi': user_input.ppi,
        'Cpu brand': user_input.cpu_brand,
        'HDD': user_input.hdd,
        'SSD': user_input.ssd,
        'Gpu brand': user_input.gpu_brand,
        'os': user_input.os
    }])
    predicted_price = np.exp(model.predict(input_data)[0])
    return JSONResponse(status_code=200, content={"predicted_price": round(predicted_price, 2)})