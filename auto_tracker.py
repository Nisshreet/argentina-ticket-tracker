import time
import subprocess

CHECK_INTERVAL_SECONDS = 300
HOURLY_UPDATE_EVERY_CHECKS = 12

check_count = 0

while True:
    print("Checking ticket prices...")

    subprocess.run(["python3", "tracker.py"])

    check_count += 1

    if check_count >= HOURLY_UPDATE_EVERY_CHECKS:
        print("Sending hourly Telegram update...")
        subprocess.run(["python3", "send_hourly_update.py"])
        check_count = 0

    print("Waiting 5 minutes...")
    time.sleep(CHECK_INTERVAL_SECONDS)
