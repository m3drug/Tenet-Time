# C:\Users\Heisenberg\AppData\Local\Programs\Python\Python38-32\python.exe
# Iran/Tehran
# With the location, Astral calculates the desired times, by default in UTC.
# Title: Proof-of-concept for dynamically adjusting social clock to sun clock
import math
from astral import LocationInfo
from astral.sun import sun
from astral import Observer
import datetime
import time
from tkinter import *
from tkinter.ttk import *

# -------------------------------------
# 1. Setting up 
    # a) the timezone 
timezone = datetime.timedelta(hours = 3, minutes = 30)

    # b) location (latitude, longitude of Tehran, Iran)
city = LocationInfo("Tehran", "Iran", "Asia/Tehran", 35.6892523, 51.3896004)

    # c) observer (Defines the location of an observer on Earth.)
observer = Observer(latitude = 35.6892523, # city.latitude, 
                    longitude = 51.3896004) # city.longitude)

    # d) in UTC
current_utc = datetime.datetime.now().date()

    # e) in the current Tehran timezone
current_local = datetime.datetime.utcnow() + timezone
#tomorrow = current_local + datetime.timedelta(days=1)
#yesterday = current_local - datetime.timedelta(days=1)

# -------------------------------------------------------
# 2. Storing the time of dawn, sunrise, noon and sunset and dusk in UTC:
    # a) today
c_data = sun(observer, date = current_utc)

    # b) tomorrow
t_data = sun(observer, date = current_utc + datetime.timedelta(days = 1))

    # c) yesterday
y_data = sun(observer, date = current_utc - datetime.timedelta(days = 1))
# -------------------------------------
# 3. Extracting the sunrise, noon and sunset times for today, tomorrow and yesterday in UTC
    # a) Today's sunrise
utc_sunrise = c_data["sunrise"]
#utc_noon = (c_data["noon"])

    # b) Today's sunset
utc_sunset = c_data["sunset"]

    # c) Tomorrow's sunrise
utc_sunrise_t = t_data["sunrise"]

    # d) Yesterday's sunset
utc_sunset_y = y_data["sunset"]
# -------------------------------------
# 4. Calculating the duration of sunlight for today, tomorrow and yesterday in UTC
    # a) Today's sunlight duration
sunlight_duration = (c_data["sunset"])-(c_data["sunrise"])

    # b) Tomorrow's sunlight duration
sunlight_duration_t = (t_data["sunset"])-(t_data["sunrise"])

    # c) Yesterday's sunlight duration
sunlight_duration_y = (y_data["sunset"])-(y_data["sunrise"])
# -------------------------------------
# 5. Calculating sunrise and sunset times as in step 4) to the current timezone
    # a) Today's sunrise time in Tehran timezone
real_sunrise = utc_sunrise + timezone
#real_noon = utc_noon + timezone

    # b) Today's sunset time in Tehran timezone
real_sunset = utc_sunset + timezone

    # c) Tomorrow's sunrise time in Tehran timezone
real_sunrise_t = utc_sunrise_t + timezone

    # d) Yesterday's sunset time in Tehran timezone
real_sunset_y = utc_sunset_y + timezone
# -------------------------------------
# 6. Extracting the time from the datetime objects
    # a) Exact sunrise time in Tehran
sunrise_time = datetime.datetime.time(real_sunrise)
#noon_time = datetime.datetime.time(real_noon)

    # b) Exact sunset time in Tehran
sunset_time = datetime.datetime.time(real_sunset)

    # c) Exact sunrise time in Tehran for tomorrow
sunrise_time_t = datetime.datetime.time(real_sunrise_t)

    # d) Exact sunset time in Tehran for yesterday
sunset_time_y = datetime.datetime.time(real_sunset_y)
# -------------------------------------
# 7. Calculating the average noon time
av_noon = datetime.timedelta(hours=12)
# -------------------------------------
# 8. Calculating Tenet Time for today

# Convert sunlight_duration to total seconds (a float)
sunlight_seconds = sunlight_duration.total_seconds()

# Define the transition points in seconds (using pi)
lower_transition_seconds = 3 * math.pi * 3600  # ~9.42 hours in seconds
upper_transition_seconds = (24 - 3 * math.pi) * 3600  # ~14.58 hours in seconds

# a) For short days:
if 1 <= sunlight_seconds < lower_transition_seconds:
    # (i) 'd_prime' is scaled by 4/pi (result is in seconds)
    d_prime_seconds = (4 / math.pi) * sunlight_seconds
    # Convert back to a timedelta for sunrise/sunset calculation
    d_prime = datetime.timedelta(seconds=d_prime_seconds)
    # (ii) & (iii) The new sunrise/sunset are calculated around noon
    new_sunrise = av_noon - (d_prime / 2)
    new_sunset = av_noon + (d_prime / 2)

# b) For mid-range days:
elif lower_transition_seconds <= sunlight_seconds < upper_transition_seconds:
    # (i) 'd_prime' is fixed at 12 hours
    d_prime = datetime.timedelta(hours=12)
    # (ii) & (iii) Fix sunrise at 6 AM and sunset at 6 PM
    new_sunrise = av_noon - (d_prime / 2)
    new_sunset = av_noon + (d_prime / 2)

# c) For long days:
elif upper_transition_seconds <= sunlight_seconds < 86400: # 86400 sec = 24 hours
    # (i) 'd_prime' is scaled by 4/pi and adjusted (all in seconds)
    d_prime_seconds = (4 / math.pi) * sunlight_seconds - ( (96/math.pi) - 24 ) * 3600
    d_prime = datetime.timedelta(seconds=d_prime_seconds)
    # (ii) & (iii) The new sunrise/sunset are calculated around noon
    new_sunrise = av_noon - (d_prime / 2)
    new_sunset = av_noon + (d_prime / 2)
    
# For absolute at the poles:
else:
    if sunlight_seconds <= 0:
        print("polar night")
    else: # sunlight_seconds >= 86400
        print("polar day")
# -------------------------------------
# 9. Calculating Tenet Time for tomorrow

# Convert sunlight_duration_t to total seconds (a float)
sunlight_seconds_t = sunlight_duration_t.total_seconds()

# a) For short days tomorrow:
if 1 <= sunlight_seconds_t < lower_transition_seconds:
    # (i) 'd_prime_t' is scaled by 4/pi (result is in seconds)
    d_prime_seconds_t = (4 / math.pi) * sunlight_seconds_t
    # Convert back to a timedelta
    d_prime_t = datetime.timedelta(seconds=d_prime_seconds_t)
    # (ii) The new sunrise time is calculated as the average noon time minus half of d_prime_t
    new_sunrise_t = av_noon - (d_prime_t / 2)

# b) For mid-range days tomorrow:
elif lower_transition_seconds <= sunlight_seconds_t < upper_transition_seconds:
    # (i) 'd_prime_t' is fixed at 12 hours
    d_prime_t = datetime.timedelta(hours=12)
    # (ii) The new sunrise time is calculated as the average noon time minus half of d_prime_t
    new_sunrise_t = av_noon - (d_prime_t / 2)
    
# c) For long days tomorrow:
elif upper_transition_seconds <= sunlight_seconds_t < 86400: # 86400 sec = 24 hours
    # (i) 'd_prime_t' is scaled by 4/pi and adjusted (all in seconds)
    d_prime_seconds_t = (4 / math.pi) * sunlight_seconds_t - ( (96/math.pi) - 24 ) * 3600
    d_prime_t = datetime.timedelta(seconds=d_prime_seconds_t)
    # (ii) The new sunrise time is calculated as the average noon time minus half of d_prime_t
    new_sunrise_t = av_noon - (d_prime_t / 2)
    
# For absolute at the poles tomorrow:
else:
    if sunlight_seconds_t <= 0:
        print("polar night (tomorrow)")
    else: # sunlight_seconds_t >= 86400
        print("polar day (tomorrow)")
# -------------------------------------
# 10. Calculating Tenet Time for yesterday

# Convert sunlight_duration_y to total seconds (a float)
sunlight_seconds_y = sunlight_duration_y.total_seconds()

# a) For short days yesterday:
if 1 <= sunlight_seconds_y < lower_transition_seconds:
    # (i) 'd_prime_y' is scaled by 4/pi (result is in seconds)
    d_prime_seconds_y = (4 / math.pi) * sunlight_seconds_y
    # Convert back to a timedelta
    d_prime_y = datetime.timedelta(seconds=d_prime_seconds_y)
    # (ii) New sunset time is 12pm + half of d_prime_y
    new_sunset_y = av_noon + (d_prime_y / 2)

# b) For mid-range days yesterday:
elif lower_transition_seconds <= sunlight_seconds_y < upper_transition_seconds:
    # (i) 'd_prime_y' is fixed at 12 hours
    d_prime_y = datetime.timedelta(hours=12)
    # (ii) New sunset time is 12pm + half of d_prime_y
    new_sunset_y = av_noon + (d_prime_y / 2)
    
# c) For long days yesterday:
elif upper_transition_seconds <= sunlight_seconds_y < 86400: # 86400 sec = 24 hours
    # (i) 'd_prime_y' is scaled by 4/pi and adjusted (all in seconds)
    d_prime_seconds_y = (4 / math.pi) * sunlight_seconds_y - ( (96/math.pi) - 24 ) * 3600
    d_prime_y = datetime.timedelta(seconds=d_prime_seconds_y)
    # (ii) New sunset time is 12pm + half of d_prime_y
    new_sunset_y = av_noon + (d_prime_y / 2)
    
# For absolute at the poles yesterday:
else:
    if sunlight_seconds_y <= 0:
        print("polar night (yesterday)")
    else: # sunlight_seconds_y >= 86400
        print("polar day (yesterday)")

# -------------------------------------
# 11. Converting sunrise and sunset times to seconds
    # a) Today's sunrise time converted to seconds
va = time.strptime(str(sunrise_time).split(',')[0], '%H:%M:%S.%f')
sunrise_time_s = (datetime.timedelta(hours = va.tm_hour, minutes = va.tm_min, seconds = va.tm_sec).total_seconds())
    # b) Today's newly-set sunrise time in seconds
vb = time.strptime(str(new_sunrise).split(',')[0], '%H:%M:%S')
new_sunrise_s = (datetime.timedelta(hours=vb.tm_hour, minutes=vb.tm_min, seconds=vb.tm_sec).total_seconds())
    # c) Tomorrow's sunrise time converted to seconds
vc = time.strptime(str(sunrise_time_t).split(',')[0], '%H:%M:%S.%f')
sunrise_time_t_s = (datetime.timedelta(hours=vc.tm_hour, minutes=vc.tm_min, seconds=vc.tm_sec).total_seconds())
    # d) Yesterday's sunset time converted to seconds
vd = time.strptime(str(sunset_time_y).split(',')[0], '%H:%M:%S.%f')
sunset_time_y_s = (datetime.timedelta(hours=vd.tm_hour, minutes=vd.tm_min, seconds=vd.tm_sec).total_seconds())
    # e) Today's sunset time converted to seconds
ve = time.strptime(str(sunset_time).split(',')[0], '%H:%M:%S.%f')
sunset_time_s = (datetime.timedelta(hours=ve.tm_hour, minutes=ve.tm_min, seconds=ve.tm_sec).total_seconds())
    # f) Today's newly-set sunset time in seconds
vf = time.strptime(str(new_sunset).split(',')[0], '%H:%M:%S')
new_sunset_s = (datetime.timedelta(hours=vf.tm_hour, minutes=vf.tm_min, seconds=vf.tm_sec).total_seconds())
    # g) Yesterday's newly-set sunset time converted to seconds
vg = time.strptime(str(new_sunset_y).split(',')[0], '%H:%M:%S')
new_sunset_y_s = (datetime.timedelta(hours = vg.tm_hour, minutes=vg.tm_min, seconds=vg.tm_sec).total_seconds())
    # h) Tomorrow's newly-set sunrise time in seconds
vh = time.strptime(str(new_sunrise_t).split(',')[0], '%H:%M:%S')
new_sunrise_t_s = (datetime.timedelta(hours=vh.tm_hour, minutes=vh.tm_min, seconds=vh.tm_sec).total_seconds())

# -------------------------------------
# 12. Calculating velocity of time passing in Tenet Time:
# velocity s'/s; 86400 being the no. of seconds in a day
    # 1. Yesterday's sunset → Today's sunrise (nighttime)
night_duration_y = (86400 + sunrise_time_s - sunset_time_y_s    # Real night duration (yesterday sunset → today sunrise)
tent_night_duration_y = (86400 + new_sunrise_s - new_sunset_y_s)     # Tenet night duration
v4_sunset_to_sunrise_y = tent_night_duration_y / night_duration_y  # Velocity for last night
    # 2. Today's sunrise → Today's sunset (daytime)
day_duration = sunset_time_s - sunrise_time_s  # Real day duration
tent_day_duration = new_sunset_s - new_sunrise_s  # Tenet day duration
v5_sunrise_to_sunset = tent_day_duration / day_duration  # Velocity for today's daylight
    # 3. Today's sunset → Tomorrow's sunrise (next nighttime)
night_duration_t = (86400 - sunset_time_s + sunrise_time_t_s)  # Real night duration (today sunset → tomorrow sunrise)
tent_night_duration_t = (86400 - new_sunset_s + new_sunrise_t_s)  # Tenet night duration 
v6_sunset_to_sunrise = tent_night_duration_t / night_duration_t  # Velocity for tonight

# -------------------------------------
# 13. Formulating the time_equation

def time_equation():
    # Getting the current local time
    h = datetime.datetime.time(current_local)
    # Calculating the no. of seconds from the current local time
    h_seconds = (h.hour * 60 + h.minute) * 60 + h.second
    # Case 1: Last night (yesterday's sunset → today's sunrise)
    if h <= sunrise_time:
        new_time_seconds = ((h_seconds + 86400 - sunset_time_y_s) * v4_sunset_to_sunrise_y + new_sunset_y_s) % 86400
        return new_time_seconds
    # Case 2: Today's daytime (sunrise → sunset)
    elif sunrise_time < h <= sunset_time:
        new_time_seconds = (h_seconds - sunrise_time_s) * v5_sunrise_to_sunset + new_sunrise_s
        return new_time_seconds
    # Case 3: Tonight (today's sunset → tomorrow's sunrise)
    elif sunset_time < h <= datetime.time(23, 59, 59, 999999):
        new_time_seconds = ((h_seconds - sunset_time_s) * v6_sunset_to_sunrise + new_sunset_s) % 86400
        return new_time_seconds
     
    root.after(60000, time_equation)
    root.after(60000, datetime.datetime.utcnow)

new_seconds = round(time_equation())
new_time2 = datetime.timedelta(seconds = time_equation())
new_time3 = (str(new_time2))
new_clock = new_time3.split('.')[0]

# ------------- digital clock -----------
# This function is used to display time on the label
root = Tk() # creating a tkinter window
root.title('Clock') # setting the title of the window
timero = [new_seconds//3600, (new_seconds % 3600)//60, (new_seconds % 60)] # setting the time to be displayed on the label
timestr = '00:00:00' # setting the initial time to be displayed on the label
pattern = '{0:02d}:{1:02d}:{2:02d}' # setting the pattern for the time to be displayed on the label

def speed():
    h = datetime.datetime.time(current_local)
    if h <= sunrise_time:
        new_speed = v4_sunset_to_sunrise_y
        return new_speed
    elif sunrise_time < h <= sunset_time:
        new_speed = v5_sunrise_to_sunset
        return new_speed
    elif sunset_time < h <= datetime.time(23, 59, 59, 999999):
        new_speed = v6_sunset_to_sunrise
        return new_speed
    root.after(60000, speed)
    root.after(60000, time_equation)
    root.after(60000, datetime.datetime.utcnow)

def time():
    current_local = datetime.datetime.utcnow() + timezone
    root.after(1000, speed)
    global timero, pattern
    timero[2] += 1
    if timero[2] >= 60:
        timero[1] += 1
        timero[2] = 0
        if timero[1] >= 60:
            timero[0] += 1
            timero[1] = 0
            if timero[0] >= 24:
                timero[0] = 0
                current_local += datetime.timedelta(days=1)
    string = pattern.format(timero[0], timero[1], timero[2])
    lbl.config(text=string)
    lbl.after(round(1000/speed()), time)
    root.after(60000, speed)
    root.after(60000, time_equation)
    root.after(60000, datetime.datetime.utcnow)

# Styling the label widget so that clock
# will look more attractive
lbl = Label(root, font=('calibri', 40, 'bold'),
            background='purple',
            foreground='white')
root.after(60000, speed)
root.after(60000, time_equation)
root.after(60000, datetime.datetime.utcnow)
# Placing clock at the centre
# of the tkinter window
lbl.pack(anchor='center')
time()
root.mainloop()

# -------------------------------------
print(new_clock)
print(time_equation())
print(new_seconds)
print(datetime.datetime.time(current_local))
print(new_sunrise)
print(new_sunset)
print("SunlightDuration: " + str(sunlight_duration))
print("Sunrise: " + str(c_data["sunrise"]))
print("Noon: " + str(c_data["noon"]))
print("Sunset: " + str(c_data["sunset"]))
