# Weather Data Pipeline Project

## Objective
Objective:
Develop a comprehensive data pipeline that automatically fetches weather data from an API,
stores it in a PostgreSQL database, analyzes it with Python, and visualizes the results using
Power BI.

## Installation & Setup

### PostgreSQL Setup
1. **Login to PostgreSQL**:
   ```bash
   psql -U username -d postgres
   ```
2. **Create the Database**:
   ```sql
   CREATE DATABASE weather_database;
   ```
3. **Create Schema and Table**:
   ```sql
   \c weather_database
   CREATE SCHEMA weather;
   CREATE TABLE weather.weather_data (
       id SERIAL PRIMARY KEY,
       city VARCHAR(255),
       temperature FLOAT,
       humidity INT,
       description TEXT,
       timestamp TIMESTAMP
   );
   ```

### Python Environment Setup

#### Optional: Setting up Anaconda Environment for the project
If you have Anaconda installed, create a new virtual environment for prevention of library conflicts.
```bash
conda create --name weather_data_project python=3.8
conda activate weather_data_project
```

Install the required Python libraries:
```bash
pip install requests sqlalchemy pandas matplotlib schedule
```

## Usage

### Running the Scripts
- **Execute the Data Retrieval Script for a daily fetch at 8:00 AM**:
  ```bash
  python "weather_data_retrieval.py"
  ```

### Power BI Connection
1. Open Power BI Desktop.
2. Select **Get Data** > **PostgreSQL database**.
3. Enter your connection details:
   - **Host**: your_host_address
   - **Database**: weather_database
   - **Username**: your_username
   - **Password**: your_password
4. Import the `weather_data` table.

## Design Approach
The design integrates:
- **OpenWeatherMap API** for obtaining real-time weather forecast data.
- **PostgreSQL** for reliable and secure data storage.
- **Python** for its flexibility in fetching and processing data.
- **Power BI** for dynamic and interactive data visualizations.