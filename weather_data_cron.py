import schedule
import time
import subprocess
import os

def job():
    script_path = os.path.join(os.getcwd(), "weather_data_retrieval.py")
    subprocess.run(['python', script_path], shell=True)

# Schedule the job every day at 8:00 AM
schedule.every().day.at("08:00").do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check for scheduled tasks every minute
