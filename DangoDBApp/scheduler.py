# scheduler.py
from datetime import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
import pytz
import atexit
import logging
from django_apscheduler.models import DjangoJobExecution
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('scheduler')

# Global scheduler instance
scheduler = None

def fetch_api_data():
    """Execute the API fetch cron job"""
    logger.info(f"Starting scheduled API fetch at {datetime.now()}")
    try:
        from .cron import FetchAPIDataCronJob
        job = FetchAPIDataCronJob()
        job.do()
        logger.info(f"API fetch job completed successfully")
    except Exception as e:
        logger.error(f"Error executing API fetch job: {str(e)}")

def delete_old_job_executions(max_age=604_800):
    """Delete job execution entries older than `max_age` seconds."""
    try:
        DjangoJobExecution.objects.delete_old_job_executions(max_age)
        logger.info("Cleaned up old job executions")
    except Exception as e:
        logger.error(f"Error cleaning up job executions: {str(e)}")

def start():
    """Initialize and start the background scheduler"""
    global scheduler
    
    # Check if scheduler is already running
    if scheduler and scheduler.running:
        logger.warning("Scheduler is already running. Skipping initialization.")
        return

    try:
        # Add small delay to ensure Django is ready
        time.sleep(5)
        # Create a new scheduler
        scheduler = BackgroundScheduler(
            timezone=pytz.timezone('Asia/Manila'),
            job_defaults={
                'coalesce': True,
                'max_instances': 1,
                'misfire_grace_time': 300,  # Increased grace time
            }
        )
        
        # Add the Django job store
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # Add the main job - runs at 12 AM and 12 PM Manila time
        scheduler.add_job(
            fetch_api_data,
            trigger=CronTrigger(hour='0,12', timezone=pytz.timezone('Asia/Manila')),
            id='fetch_api_data',
            name='Fetch API Data',
            replace_existing=True
        )
        
        # Add cleanup job - runs every Monday at midnight
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00",
                timezone=pytz.timezone('Asia/Manila')
            ),
            id='delete_old_job_executions',
            max_instances=1,
            replace_existing=True
        )
        
        logger.info("Starting scheduler...")
        scheduler.start()
        logger.info("Scheduler started successfully")
        
        # Register the shutdown handler
        atexit.register(shutdown_scheduler)
        
    except Exception as e:
        logger.error(f"Error starting scheduler: {str(e)}")
        if scheduler and scheduler.running:
            shutdown_scheduler()
        raise

def shutdown_scheduler():
    """Gracefully shutdown the scheduler"""
    global scheduler
    try:
        if scheduler and scheduler.running:
            scheduler.shutdown(wait=False)
            logger.info("Scheduler shut down successfully")
    except Exception as e:
        logger.error(f"Error shutting down scheduler: {str(e)}")

