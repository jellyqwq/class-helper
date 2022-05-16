from class_helper import daily_plan, config
import schedule
import time

if __name__ == '__main__':
    schedule.every().day.at(config['PushTime']).do(daily_plan.sendTomorrowClass)
    while True:
        schedule.run_pending()
        time.sleep(1)
