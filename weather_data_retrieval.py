import requests
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

# Database connection parameters
HOST = '' # Your local PostgreSQL server url; needs to be inputted
DATABASE = 'weather_database' # Specific database to connect
USER = '' # needs to be inputted
PASSWORD = '' # needs to be inputted
SCHEMA = 'weather'

# API details
API_KEY = '' # needs to be inputted
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast?'

def fetch_weather_data(city):
    url = f"{BASE_URL}appid={API_KEY}&q={city}&units=metric"

    try:
        # Send the request to the OpenWeatherMap API
        response = requests.get(url)

        # Check if the response was successful
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"City '{city}' not found. Please check the city name and try again.")
        else:
            print(f"Failed to fetch weather data. Status code: {response.status_code}, Reason: {response.reason}")
    except requests.RequestException as e:
        # Handle any errors that occur during the HTTP request
        print(f"An error occurred: {e}")

    return None

def connect_to_db():
    engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
    return engine

def store_weather_data(engine, data, schema='public'):
    with engine.connect() as conn:
        city = data['city']['name']
        for item in data['list']:
            # Extract relevant data from the response
            temp = item['main']['temp']
            humidity = item['main']['humidity']
            description = item['weather'][0]['description']
            timestamp = item['dt_txt']

            # Prepare SQL query to insert data
            postgres_insert_query = text(f"""
                INSERT INTO {schema}.weather_data (city, temperature, humidity, weather_description, timestamp) 
                VALUES (:city, :temp, :humidity, :weather_description, :timestamp)
            """)

            # Execute the query with actual data
            conn.execute(postgres_insert_query, {
                'city': city,
                'temp': temp,
                'humidity': humidity,
                'weather_description': description,
                'timestamp': timestamp
            })
            conn.commit()

def analyze_and_plot_data():
    conn = connect_to_db()
    query = """
        SELECT city, timestamp, temperature, humidity
        FROM weather_data.weather_data
        WHERE timestamp >= CURRENT_DATE
        ORDER BY city, timestamp;
        """
    df = pd.read_sql(query, conn)
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date  # Convert timestamp to date

    # Assuming forecast data includes today and the next 5 days
    future_dates = df['timestamp'].unique()[:6]  # Slice the first 6 unique future dates
    forecast_data = df[df['timestamp'].isin(future_dates)]

    # Compute daily averages for the forecast period
    daily_avg = forecast_data.groupby(['city', 'timestamp']).mean()

    # Cluster the data for plotting
    temperature_pivot = daily_avg.pivot_table(index='timestamp', columns='city', values='temperature')
    humidity_pivot = daily_avg.pivot_table(index='timestamp', columns='city', values='humidity')

    # Plotting temperature trends
    plt.figure(figsize=(20, 15))
    temperature_pivot.plot(kind='bar')
    plt.title('Forecasted Daily Average Temperature Trends by City')
    plt.xlabel('Date')
    plt.ylabel('Average Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('forecast_temperature_trends_by_city.png')

    # Plotting humidity trends
    plt.figure(figsize=(20, 15))
    humidity_pivot.plot(kind='bar', color=['blue', 'green', 'red', 'purple', 'orange'])
    plt.title('Forecasted Daily Average Humidity Trends by City')
    plt.xlabel('Date')
    plt.ylabel('Average Humidity (%)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('forecast_humidity_trends_by_city.png')

    # Print average temperature and humidity values by city
    for city in daily_avg.index.get_level_values('city').unique():
        city_data = daily_avg.xs(city, level='city')
        avg_temp = city_data['temperature'].mean()
        avg_humidity = city_data['humidity'].mean()
        print(f"City: {city}")
        print(f"Average Temperature for the past 7 days: {avg_temp:.2f}°C")
        print(f"Average Humidity for the past 7 days: {avg_humidity:.2f}%")
        print("-----")

def main():
    while True:
        city = input("Enter the city: ")
        weather_data = fetch_weather_data(city)

        if weather_data is not None:
            conn = connect_to_db()
            store_weather_data(conn, weather_data, SCHEMA)
            analyze_and_plot_data()
            break
        else:
            print("Failed to fetch data for the provided city. Please try again.")

if __name__ == "__main__":
    main()
