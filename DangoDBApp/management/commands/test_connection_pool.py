from django.core.management.base import BaseCommand
from django.db import connections
import threading
import time

def test_connection():
    # Open and close a connection multiple times
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT 1")
        time.sleep(0.1)  # Simulate some work

class Command(BaseCommand):
    help = 'Test database connection pooling'

    def handle(self, *args, **options):
        threads = []
        # Create multiple concurrent connections
        for _ in range(50):
            thread = threading.Thread(target=test_connection)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        self.stdout.write(self.style.SUCCESS('Connection pool test complete'))