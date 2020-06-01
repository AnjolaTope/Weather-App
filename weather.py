from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
from PIL import Image, ImageTk
import requests   


# thius is the url to access the weather API and get information about the current temprature 
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'


#here we will get api key from our congig file 
config_file = 'config.ini'
config = ConfigParser()
read = config.read(config_file)
api_key = config['api_key']['key']

# we will create a function to access the weather API and retreive some data from the API
def get_weather(city):
    result = requests.get(url.format(city,api_key))
    name = city
    retrieve  = result.json()
    if result:
         #print(result.content) 
         temp =  retrieve['main']['temp'] #temprature in kelvin 
         temp_cel = int(temp) - 273.15 #temprature in Celcius 
         temp_fah = int(temp) * (9/5) - 459.67 #temprature in fahrenheit
         country =  retrieve['sys']['country'] #country 
         city =  retrieve['name'] # city's name
         icon =  retrieve['weather'][0]['icon']  #number id of the icon
         weather =  retrieve['weather'][0]['main'] #weather condition
         final = ( city, temp_cel, temp_fah,icon,weather,country)
         return final     
    else:
        return None

#cretae the app window 
app = Tk()
app.title = ("Weather App")
app.geometry("700x350")

#set an input box that takes in string varaibles
city_text = StringVar() #the input varaible 
city_entry = Entry(app, textvariable = city_text)
city_entry.pack()

#this is a label on the app that shows the location of the city you are searching for
location_lbl = Label(app, text ="", font =( 'bold',20))
location_lbl.pack()

#this is a label on the app that shows the image of the weather condition 
image1 = Label(app, image='')
image1.pack()

#this is a label on the app that shows the temprature 
temp_lbl =Label(app, text= '')
temp_lbl.pack()

#this is a label on the app that shows the weather condition 
weather_lbl= Label(app, text = '')
weather_lbl.pack()


#here  we use the city entered to get the required infroemation from the API
#this is the search funtion that we use to display results gotten from the weather API
def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather :
        location_lbl['text'] = '{}, {}'.format(weather[0],weather[5])
        img = Image.open("{}@2x.jpg".format(weather[3]))
        photo =  ImageTk.PhotoImage(img)
        print(photo)
        image1.image = photo
        image1['image'] = photo
        temp_lbl['text'] = '{:.2f}C, {:.2f}F'.format(weather[1],weather[2])
        weather_lbl['text'] = '{}'.format(weather[4])
    
    else:
        messagebox.showerror('Error','Cannot find city {}'.format(city))


    
    pass

 

#create a button to run the appp and produce resukts 
search_btn = Button(app, text ="Search weather", width =12, command = search)
search_btn.pack()

app.mainloop()