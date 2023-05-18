import os
import subprocess
from twilio.rest import Client
import time

# Twilio account details
TWILIO_SID = 'your twilio SID'
TWILIO_AUTH_TOKEN = 'your twilio Auth_Token'
TWILIO_PHONE_NUMBER = 'Twilio phn number'
TO_PHONE_NUMBER = 'your phn number'

# IP addresses and their names to monitor
IP_ADDRESSES = {'10.0.22.20': 'VegScale1', '10.0.22.21': 'VegScale2', '10.0.22.22': 'VegScale3', '10.0.22.23': 'VegScale4', '10.0.22.24': 'VegScale5', '10.0.22.26': 'FishScale1', '10.0.22.27': 'FishScale2', '10.0.22.28': 'FishScale3', '10.0.22.31': 'ButcheryScale1', '10.0.22.32': 'ButcheryScale2', '10.0.22.33': 'ButcheryScale3', '10.0.22.35': 'RosteryScale1', '10.0.22.36': 'RosteryScale2', '10.0.22.37': 'RosteryScale3', '10.0.22.40': 'DeliScale1-ServerRoom', '10.0.22.41': 'DeliScale2', '10.0.22.42': 'BakeryScale1', '10.0.22.43': 'BakeryScale2', '10.0.22.23': 'HotFoodScale1', '10.0.22.45': 'HotFoodScale2'}

# Ping timeout (in seconds)
PING_TIMEOUT = 10

# Function to send SMS using Twilio
def send_sms(message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=TO_PHONE_NUMBER
    )

# Function to ping IP address and check for reachability
def ping_ip(ip_address):
    try:
        subprocess.check_output(['ping', '-c', '1', '-w', str(PING_TIMEOUT), ip_address])
        return True
    except subprocess.CalledProcessError:
        return False

# Main loop to continuously ping and send notifications
while True:
    # Get current hour
    current_hour = int(time.strftime('%H'))
    # Check if current hour is between 0 (midnight) and 6 (6 AM)
    if current_hour >= 0 and current_hour < 6:
        print('Sleeping...')
        # Calculate remaining time until 6 AM
        current_time = time.time()
        next_run_time = time.mktime(time.strptime(time.strftime('%Y-%m-%d 06:00:00'), '%Y-%m-%d %H:%M:%S'))
        remaining_time = next_run_time - current_time
        print(f'Next run time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(next_run_time))}')
        time.sleep(remaining_time)
    else:
        unreachable_ips = []
        for ip_address, name in IP_ADDRESSES.items():
            if not ping_ip(ip_address):
                # IP address is unreachable, add to the list
                unreachable_ips.append(f'{name} ({ip_address})')
        if unreachable_ips:
            # Send SMS notification with unreachable IP addresses and their names
            message = f'Below Scales Are Offline, Please check: {", ".join(unreachable_ips)}'
            send_sms(message)
        else:
            print('All servers are reachable.')
        # Sleep for 1 hour before pinging again
        next_run_time = time.time() + 3600
        print(f'Next run time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(next_run_time))}')
        time.sleep(3600)
