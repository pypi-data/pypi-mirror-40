import CO2Signal
import time

token = "6fb40a7e9dceccb7"

sleep_time = 2

print(CO2Signal.get_latest(token, country_code = "FR"))
time.sleep(sleep_time)
print(CO2Signal.get_latest_carbon_intensity(token, country_code = "FR"))
time.sleep(sleep_time)

print(CO2Signal.get_latest(token, longitude=2.34, latitude=48.86)) # Paris coordinates
time.sleep(sleep_time)
print(CO2Signal.get_latest_carbon_intensity(token, longitude=2.34, latitude=48.86)) # Paris coordinates
time.sleep(sleep_time)
print(CO2Signal.get_latest_carbon_intensity(token, country_code = "BE"))
time.sleep(sleep_time)