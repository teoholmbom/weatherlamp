
from forecastiopy import *
from time import sleep
from repeatedtimer import *
from blinkt import set_brightness, set_pixel, set_all, show
import json
import time

# Reading config from json
with open('config.json', 'r') as f:
	data = json.load(f)

# Set config data
apikey = data['apikey']

# Set location as array with longitude latitude
location = data['location']

# Set colors to dictionary for each degree with an array defining 
# the color [red, green, blue]
colors = data['colors']

# Define number of pixels in strip
pixels = data['pixels']

# Set brightness for pixels
brightness = data['brightness']

currentTemp = 0
currentCloudCover = 0

#fio = ForecastIO.ForecastIO(apikey,
#    units = ForecastIO.ForecastIO.UNITS_SI,
#    lang = ForecastIO.ForecastIO.LANG_ENGLISH,
#    latitude = location[0], 
#    longitude = location[1])


def set_pixels(inTemp, inCloudCover = 0):
    # Set all pixels to black and brightness 0
    set_all(0, 0, 0, 0)
    
    # Calculate number of pixels to show
    activePixels = (100 - inCloudCover) / 12
    modulus = (100 - inCloudCover) % 12

	# Add one active pixel if modulus is over 6 or if there are 
	# no active pixels
    if (modulus >= 6 or activePixels == 0):
		activePixels = activePixels + 1
		
    print str(activePixels) + " active pixels"
    
    color = colors[str(inTemp)]

    print "Red: " + str(color[0]) 
    print "Green: " + str(color[1]) 
    print "Blue: " + str(color[2]) 
    print
    
    #Loop through pixels and set their color
    for x in range(0, activePixels):
		set_pixel(x, color[0], color[1], color[2], brightness)
	
    show()

def get_weather():
	fio	= ForecastIO.ForecastIO(apikey, units = ForecastIO.ForecastIO.UNITS_SI, 
		lang = ForecastIO.ForecastIO.LANG_ENGLISH, 
		time = str(int(time.time())),
		latitude = location[0], 
		longitude = location[1])
		
	print int(time.time())
	
	if fio.has_currently() is True:
		currently = FIOCurrently.FIOCurrently(fio)

		# Set current temperature
		currentTemp = int(round(currently.temperature))

		# Set current cloud coverage
		currentCloudCover = int(round(currently.cloudCover * 100))
		
		print "Current temperature: " + str(currentTemp)
		print "Current cloud coverage: " + str(currentCloudCover)

		set_pixels(currentTemp, currentCloudCover)
	else:
		print 'No Currently data'

# Start        
get_weather()
rt = RepeatedTimer(300, get_weather)

while 1:
    sleep(120)

rt.stop() # better in a try/finally block to make sure the program ends!
