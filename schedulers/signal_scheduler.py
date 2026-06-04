"""
APScheduler M5 trigger.
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from agents.signal_agent import generate_signal
import logging

logging.basicConfig(level=logging.INFO)

def start_scheduler():
    scheduler = BlockingScheduler()
    # Run every 5 minutes during Tunis business hours (08:00 - 22:00)
    scheduler.add_job(generate_signal, 'cron', minute='*/5', hour='8-22', timezone='Africa/Tunis')
    
    logging.info("Starting M5 Signal Scheduler...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    start_scheduler()
