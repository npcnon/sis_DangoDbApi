from django_cron import CronJobBase, Schedule
import requests
from django.utils import timezone

class FetchAPIDataCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # Run every minute for testing

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'DangoDBApp.fetch_api_data'  # A unique code

    def do(self):
        print(f"Cron job running at {timezone.now()}")
        # Simulating API fetch
        response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
        if response.status_code == 200:
            data = response.json()
            print(f"Fetched data: {data}")
        else:
            print(f"Failed to fetch data: {response.status_code}")