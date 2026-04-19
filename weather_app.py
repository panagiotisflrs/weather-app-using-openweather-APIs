import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt #for alignment.
from PyQt5.QtGui import QPixmap # turn data["main"][0]["icon"] into png.


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        #I create a label that says to the user what to type.
        self.city_label = QLabel("Enter city name: ", self)

        #Then i create a box where the user can type the name of a city.
        self.city_input = QLineEdit(self)

        #Then create a button which will show certain things about the weather.
        self.get_weather_button = QPushButton("Get weather", self)

        #Some things about the weather are: temperature, humidity,
        #description of the weather etc.
        self.temperature_label = QLabel("Temperature: ", self)
        self.emoji_label = QLabel(self)
        self.humidity_label = QLabel("Humidity: ", self)
        self.description_label = QLabel("The weather is: ", self)
        self.visibility_label = QLabel("Visibility: ", self)
        self.wind_speed_label = QLabel("Wind speed: ", self)
        self.cloudiness_label = QLabel("Cloudiness: ", self)
        self.atmospheric_pressure_label = QLabel("Atmosphere: ", self)

        #Because all the labels, the city input and the button overlap,
        #i will create a function that helps us solve the problem.
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Weather App")

        #Create a box/window where i can add widgets.
        #The order which i place the widgets matter.
        #For example first things first will be the city_label.
        #Then city_input. Then get_weather_button and so on.
        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.humidity_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.visibility_label)
        vbox.addWidget(self.wind_speed_label)
        vbox.addWidget(self.cloudiness_label)
        vbox.addWidget(self.atmospheric_pressure_label)
        vbox.addWidget(self.emoji_label)
        self.setLayout(vbox)

        #Now i can align everything to the center of my box/window.
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.visibility_label.setAlignment(Qt.AlignCenter)
        self.wind_speed_label.setAlignment(Qt.AlignCenter)
        self.cloudiness_label.setAlignment(Qt.AlignCenter)
        self.atmospheric_pressure_label.setAlignment(Qt.AlignCenter)
        self.humidity_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setMinimumSize(50, 50)

        # Now i can temper with the font and size of everything individually.
        # I access setAlignment, then access Qt and then i access AlignCenter.
        #In order to apply styles the name of the object is needed.
        #But there are no names for the widgets. I have to do that first.
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.humidity_label.setObjectName("humidity_label")
        self.visibility_label.setObjectName("visibility_label")
        self.wind_speed_label.setObjectName("wind_speed_label")
        self.cloudiness_label.setObjectName("cloudiness_label")
        self.atmospheric_pressure_label.setObjectName("atmospheric_pressure_label")
        self.description_label.setObjectName("description_label")
        self.emoji_label.setObjectName("emoji_label")

        self.setStyleSheet(""" 
            QLabel,QPushButton{
                    font-family: New Times Roman;
                    }
            QLabel#city_label{
                    font-size: 15px;}
            QLineEdit#city_input{
                    font-size: 15px;}
            QPushButton#get_weather_button{
                    font-size: 15px;}
            QLabel#temperature_label{
                    font-size: 15px;}
            QLabel#humidity_label{
                    font-size: 15px;}
            QLabel#description_label{
                    font-size: 15px;}
            QLabel#visibility_label{
                    font-size: 15px;}
            QLabel#wind_speed_label{
                    font-size: 15px;}
            QLabel#cloudiness_label{
                    font-size: 15px;}
            QLabel#atmospheric_pressure_label{
                    font-size: 15px;}
                    
        """)

        #I have to connect: clicking the get_weather_button with
        #Actually clicking it once and getting my result.
        #Unlike here, if i created a window and a button with tkinter
        #then clicking it actually gets the job done.
        #But here i have to make the connection!
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        #Now i have to somehow connect: clicking the get_weather_button
        #with actually getting information about the weather.
        api_key = "this_should_be_your_api_key_not_mine"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"


        #I will use the try and catch method for my dangerous code.
        #Dangerous code is the code that might cause an error.
        try:
            #I make an api request and i get a response
            #which i will store in response variable.
            response = requests.get(url)
            
            #Normaly the try and catch method isn't able to catch
            #HTTPError. So i need to add an extra command for this error.
            response.raise_for_status()

            #Now i take my response and convert it into a
            #json format and then store it in data.
            #I need this type of format because that's how openai weather works.
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_err:
            match response.status_code:
                case 400:
                    self.display_error("Bad request: \nPlease check your input.")
                case 401:
                    self.display_error("Unauthorized: \nInvalid API key.")
                case 403:
                    self.display_error("Forbidden: \nAccess denied.")
                case 404:
                    self.display_error("Not found: \nCity not found.")
                case 500:
                    self.display_error("Internal server error: \nPlease try again later.")
                case 502:
                    self.display_error("Bad Gateway: \nInvalid response from server.")
                case 503:
                    self.display_error("Service Unavailable: \nServer is down.")
                case 504:
                    self.display_error("Gateway Timeout: \nNo response from server.")
                case _:
                    self.display_error("HTTP error")

        except requests.exceptions.ConnectionError as connection_err:
            self.display_error("Connection error: \nPlease check your Internet connection.")

        except requests.exceptions.Timeout as timeout_err:
            self.display_error("Timeout error: \nRequest timed out.")

        except requests.exceptions.ToomanyRedirects as too_many_redirects_err:
            self.display_error("Too many redirects error:\nCheck the URL.")

        except requests.exceptions.RequestException as request_err:
            self.display_error("Request error:\n{request_err}")

    def display_error(self, message):
        self.temperature_label.setText(message)
        labels_to_clear = [
            self.humidity_label,
            self.description_label,
            self.emoji_label,
            self.visibility_label,
            self.wind_speed_label,
            self.cloudiness_label,
            self.atmospheric_pressure_label
        ]

        for label in labels_to_clear:
            label.clear()

    def display_weather(self,data):
        #print(data) helps alot throughout this proccess.

        #For temperature.
        temperature_k = data["main"]["temp"]
        temperature_c = "{:.1f}".format(temperature_k - 273.15) + "C"

        temperature_k_min = data["main"]["temp_min"]
        temperature_c_min = "{:.1f}".format(temperature_k_min - 273.15) + "C"

        temperature_k_max = data["main"]["temp_max"]
        temperature_c_max = "{:.1f}".format(temperature_k_max - 273.15) + "C"

        self.temperature_label.setText( "Maximum temperature " + temperature_c_max
            + ", current temperature: " + temperature_c +
            ", minimum temperature: " + temperature_c_min
                                       )

        #For humidity.
        humidity = data["main"]["humidity"]
        self.humidity_label.setText("Humidity: " + f"{humidity}" + " %")

        #For description. I notice that its like this ' ': [{}]
        description = data["weather"][0]["description"]
        self.description_label.setText("The weather is: " + description)

        #For visibility.
        visibility = data["visibility"]
        self.visibility_label.setText("Visibility: " + f"{visibility}" + " m")

        #For wind speed.
        wind_speed = data["wind"]["speed"]
        self.wind_speed_label.setText("Wind speed: " + f"{wind_speed}" + " m/s")

        #For cloudiness.
        cloudiness = data["clouds"]["all"]
        self.cloudiness_label.setText("Cloudiness: " + f"{cloudiness}" + " %")

        #For atmospheric pressure.
        atm_pressure = data["main"]["pressure"]
        self.atmospheric_pressure_label.setText("Atmosphere: " + f"{atm_pressure}" + " hPa")

        weather_id = data["weather"][0]["id"]

        emoji = data["weather"][0]["icon"]
        #Once the code form icon is retrieved, we use the url to get
        #a response and then use that response to plug it in our
        #emoji label. However we are going to use .setPixmap and so
        #i need to define it using QPixmap().
        url_for_emoji = f"https://openweathermap.org/img/wn/{emoji}@2x.png"
        response_for_emoji = requests.get(url_for_emoji)
        pixmap = QPixmap()
        pixmap.loadFromData(response_for_emoji.content)
        self.emoji_label.clear()
        self.emoji_label.setPixmap(pixmap)


#If running this exact file directly then and only then can the weather app be created.
if __name__ == '__main__':
    
    #Access the module of sys and then access the argv = arguments.
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    
    #I don't want the app to just pop up for like a milliseconds.
    #I want to be able to close it by my self.
    #app.exec_() is a method that handles events within my application. For example clicking x to close.
    sys.exit(app.exec_())
    
