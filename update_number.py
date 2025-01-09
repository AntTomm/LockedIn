#!/usr/bin/env python3
import os
import random
import subprocess
import schedule
import time
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def read_number():
    with open('number.txt', 'r') as f:
        return int(f.read().strip())

def write_number(num):
    with open('number.txt', 'w') as f:
        f.write(str(num))

def git_commit():
    # stage
    subprocess.run(['git', 'add', 'number.txt'])

    # create commit with current date
    date = datetime.now().strftime('%Y-%m-%d')
    commit_message = f"Update number: {date}"
    subprocess.run(['git', 'commit', '-m', commit_message])

def git_push():
    # push commits 
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Changes pushed to GitHub successfully.")
    else:
        print("Error pushing to GitHub:")
        print(result.stderr)

def update_number():
    try:
        current_number = read_number()
        new_number = current_number + 1
        write_number(new_number)

        git_commit()
        git_push()
        print(f"Number updated successfully to {new_number}")
    except Exception as e:
        print(f"Error updating number: {e}")

# schedule every day at specific time
schedule.every(1).minutes.do(update_number)

print("Scheduler is running. The script will execute daily at 6:00 AM.")

# repeat schedule
while True:
    schedule.run_pending()
    time.sleep(1)
