from flask import Flask, render_template, redirect, request, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from tempconvert import kelvin_to_celsius
from geopy import Nominatim
import requests


# initializing flask app instance 
app = Flask(__name__)

# funtion that can return latitude and longitude for the given city
def get_lat_lan(city):
    geolocator = Nominatim(user_agent="WeatherApi")
    location = geolocator.geocode(city)

    if location is not None:
        return location.latitude, location.longitude
    return None, None


class MyForm(FlaskForm):
    city = StringField("City:", validators=[InputRequired()], render_kw={"placeholder":"enter city name"})
    submit = SubmitField()


# first route
@app.route('/')
@app.route('/index', methods = ['POST', 'GET'])
def index():
    form = MyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            city = form.city.data
            return redirect(url_for("weather", city=city))
    return render_template("index.html", form=form)

# second route
@app.route('/weather/<city>', methods = ["POST", "GET"])
def weather(city):
    if request.method == "GET":
        api_key = "your_api_key"
        lat, lon = get_lat_lan(city=city)
        response = response = (requests.post(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"))
        if response.status_code==200:
            data = response.json()
            weather_desc = (data["weather"][0]["description"])
            temp = kelvin_to_celsius(data["main"]["temp"])
            feels_like = kelvin_to_celsius(data["main"]["feels_like"])
            min = kelvin_to_celsius(data["main"]["temp_min"])
            max= kelvin_to_celsius(data["main"]["temp_max"])
            humid = (data["main"]["humidity"])
            flash(f"Temperature of {city} is:{round(temp,2)}degree celsius")
            flash(f"Weather Description:{weather_desc}")
            flash(f"Feels like:{round(feels_like,2)}degree celsius")
            flash(f"Minimum:{round(min,2)}degree celsius")
            flash(f"Maximum:{round(max,2)}degree celsius")
            flash(f"Humidity:{humid}%")
        else:
            flash(f"Error: {response.status_code} - {response.text}")
        return render_template("weather.html")
    return redirect(url_for("index"))


if __name__=="__main__":
    app.secret_key="93953hchf948c3chx94"
    app.run(debug=True)
