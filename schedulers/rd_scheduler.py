"""
APScheduler Daily 00:00 UTC trigger for R&D.
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from agents.rd_agent import run_rd_cycle
from agents.calibration_agent import run_calibration
import logging

logging.basicConfig(level=logging.INFO)

def start_scheduler():
    scheduler = BlockingScheduler()
    # R&D daily
    scheduler.add_job(run_rd_cycle, 'cron', hour=0, minute=0, timezone='UTC')
    # Calibration weekly on Monday at 02:00 UTC
    scheduler.add_job(run_calibration, 'cron', day_of_week='mon', hour=2, minute=0, timezone='UTC')
    
    logging.info("Starting R&D and Calibration Scheduler...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    start_scheduler()
