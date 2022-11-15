from flask import Flask, render_template, request, jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask("car_model")

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/',methods=['GET'])

def Home():
    return render_template('index.html')

standard_to = StandardScaler()

@app.route("/predict", methods=['POST'])

def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':

        Year = int(request.form['Year'])
        Year = 2020 - Year
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']

        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0

        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0

        Transmission_Manual=request.form['Transmission_Manual']
        if(Transmission_Manual=='Mannual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        output=round(prediction[0],2)

        if output<0:
            return render_template('index.html',prediction_text="❌ Sorry you cannot sell this car. 🙁")

        else:
            return render_template('index.html',prediction_text="✅ You Can Sell the Car at {} lakhs 💰👍".format(output))

    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)
