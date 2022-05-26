# Python Libraries
import sys, os, errno, requests, datetime, pytz, csv


# Human-Readable Date
boston_time = datetime.datetime.now(pytz.timezone('America/New_York')).strftime("%b %d %Y, %I:%M %p")
print("Boston Time:", boston_time)

london_time = datetime.datetime.now(pytz.timezone('Europe/London')).strftime("%b %d %Y, %I:%M %p")
print("London Time:", london_time)

san_f_time = datetime.datetime.now(pytz.timezone('America/Los_Angeles')).strftime("%b %d %Y, %I:%M %p")
print("San Francisco Time:", san_f_time)


# Commandline Args
file_name = sys.argv[0]
api_key_arg = sys.argv[1]
dir_arg = sys.argv[2]

# Dir Location Config
default_dir_location = './'
add_dir = os.path.join(default_dir_location, dir_arg)

try:
    os.mkdir(add_dir)
except OSError as e:
    if e.errno == errno.EEXIST:
        print('New folder not created.')
    else:
        raise

# Open Weather Endpoint
base_url = "https://api.openweathermap.org/data/2.5/weather?"
cities = ["Boston", "San Francisco", "London"]
city_times = [boston_time, san_f_time, london_time]
# api_key = "31101bf3e1b7ce54c79f91ce86ff1b8c"
fahrenheit = "imperial"


def list_of_cities():
    empty_list = []
    for city, city_time in zip(cities, city_times):
        url = base_url + "q=" + city + "&units=" + fahrenheit + "&appid=" + api_key_arg
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            main = data['main']
            name = data['name']
            temperature = main['temp']
            humidity = main['humidity']
            pressure = main['pressure']
            report = data['weather']

            # data store in dict
            data = {
                "name": name,
                "date": city_time,
                "temperature": temperature,
                "weather_desc": report[0]['description'],
                "pressure": pressure,
                "humidity": humidity
            }
            empty_list.append(data)

        else:
            print("Error in the HTTP request")
    return empty_list


results = list_of_cities()
print(results)
print(add_dir)

# csv
data_file = open(add_dir + '/' + 'openweather.csv', 'w', newline='')
csv_writer = csv.writer(data_file)
count = 0

for r in results:
    if count == 0:
        header = ['City Name', 'Date', 'Temp', 'Weather Description', 'Pressure', 'Humidity']
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(r.values())

data_file.close()




