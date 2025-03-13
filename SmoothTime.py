# C:\Users\Heisenberg\AppData\Local\Programs\Python\Python38-32\python.exe
# Iran/Tehran
# With the location, Astral calculates the desired times, by default in UTC.
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

# 2. Storing the time of dawn, sunrise, noon and sunset and dusk for the given timezone + location for:
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
    # Exact sunrise time in Tehran
sunrise_time = datetime.datetime.time(real_sunrise)
#noon_time = datetime.datetime.time(real_noon)
sunset_time = datetime.datetime.time(real_sunset)
sunrise_time_t = datetime.datetime.time(real_sunrise_t)
sunset_time_y = datetime.datetime.time(real_sunset_y)
# -------------------------------------
av_noon = datetime.timedelta(hours=12)
# -------------------------------------
# new points today
if datetime.timedelta(seconds=1) <= sunlight_duration < datetime.timedelta(hours=3):
    d_prime = 2 * sunlight_duration
    new_sunrise = av_noon - (d_prime / 2)
    new_sunset = av_noon + (d_prime / 2)
elif sunlight_duration < datetime.timedelta(hours=9):
    d_prime = sunlight_duration + datetime.timedelta(hours=3)
    new_sunrise = av_noon - (d_prime / 2)
    new_sunset = av_noon + (d_prime / 2)
elif sunlight_duration < datetime.timedelta(hours=15):
    d_prime = datetime.timedelta(hours=12)
    new_sunrise = av_noon - (d_prime / 2)
    new_sunset = av_noon + (d_prime / 2)
elif sunlight_duration < datetime.timedelta(hours=21):
    d_prime = sunlight_duration - datetime.timedelta(hours=3)
    new_sunrise = av_noon - (d_prime / 2)
    new_sunset = av_noon + (d_prime / 2)
elif sunlight_duration < datetime.timedelta(hours=24):
    d_prime = 2 * sunlight_duration - datetime.timedelta(hours=24)
    new_sunrise = av_noon - (d_prime / 2)
    new_sunset = av_noon + (d_prime / 2)
else:
    print("polar circle")

# new points tomorrow
if datetime.timedelta(seconds=1) <= sunlight_duration_t < datetime.timedelta(hours=3):
    d_prime_t = 2 * sunlight_duration_t
    new_sunrise_t = av_noon - (d_prime_t / 2)
elif sunlight_duration_t < datetime.timedelta(hours=9):
    d_prime_t = sunlight_duration_t + datetime.timedelta(hours=3)
    new_sunrise_t = av_noon - (d_prime_t / 2)
elif sunlight_duration_t < datetime.timedelta(hours=15):
    d_prime_t = datetime.timedelta(hours=12)
    new_sunrise_t = av_noon - (d_prime_t / 2)
elif sunlight_duration_t < datetime.timedelta(hours=21):
    d_prime_t = sunlight_duration_t - datetime.timedelta(hours=3)
    new_sunrise_t = av_noon - (d_prime_t / 2)
elif sunlight_duration_t < datetime.timedelta(hours=24):
    d_prime_t = 2 * sunlight_duration_t - datetime.timedelta(hours=24)
    new_sunrise_t = av_noon - (d_prime_t / 2)

# new points yesterday
if datetime.timedelta(seconds=1) <= sunlight_duration_y < datetime.timedelta(hours=3):
    d_prime_y = 2 * sunlight_duration_y
    new_sunset_y = av_noon + (d_prime_y / 2)
elif sunlight_duration_y < datetime.timedelta(hours=9):
    d_prime_y = sunlight_duration_y + datetime.timedelta(hours=3)
    new_sunset_y = av_noon + (d_prime_y / 2)
elif sunlight_duration_y < datetime.timedelta(hours=15):
    d_prime_y = datetime.timedelta(hours=12)
    new_sunset_y = av_noon + (d_prime_y / 2)
elif sunlight_duration_y < datetime.timedelta(hours=21):
    d_prime_y = sunlight_duration_y - datetime.timedelta(hours=3)
    new_sunset_y = av_noon + (d_prime_y / 2)
elif sunlight_duration_y < datetime.timedelta(hours=24):
    d_prime_y= 2 * sunlight_duration_y - datetime.timedelta(hours=24)
    new_sunset_y = av_noon + (d_prime_y / 2)

# -------------------------------------
va = time.strptime(str(sunrise_time).split(',')[0], '%H:%M:%S.%f')
sunrise_time_s = (datetime.timedelta(hours=va.tm_hour, minutes=va.tm_min, seconds=va.tm_sec).total_seconds())

vb = time.strptime(str(new_sunrise).split(',')[0], '%H:%M:%S')
new_sunrise_s = (datetime.timedelta(hours=vb.tm_hour, minutes=vb.tm_min, seconds=vb.tm_sec).total_seconds())

vc = time.strptime(str(sunrise_time_t).split(',')[0], '%H:%M:%S.%f')
sunrise_time_t_s = (datetime.timedelta(hours=vc.tm_hour, minutes=vc.tm_min, seconds=vc.tm_sec).total_seconds())

vd = time.strptime(str(sunset_time_y).split(',')[0], '%H:%M:%S.%f')
sunset_time_y_s = (datetime.timedelta(hours=vd.tm_hour, minutes=vd.tm_min, seconds=vd.tm_sec).total_seconds())

ve = time.strptime(str(sunset_time).split(',')[0], '%H:%M:%S.%f')
sunset_time_s = (datetime.timedelta(hours=ve.tm_hour, minutes=ve.tm_min, seconds=ve.tm_sec).total_seconds())

vf = time.strptime(str(new_sunset).split(',')[0], '%H:%M:%S')
new_sunset_s = (datetime.timedelta(hours=vf.tm_hour, minutes=vf.tm_min, seconds=vf.tm_sec).total_seconds())

vg = time.strptime(str(new_sunset_y).split(',')[0], '%H:%M:%S')
new_sunset_y_s = (datetime.timedelta(hours=vg.tm_hour, minutes=vg.tm_min, seconds=vg.tm_sec).total_seconds())

vh = time.strptime(str(new_sunrise_t).split(',')[0], '%H:%M:%S')
new_sunrise_t_s = (datetime.timedelta(hours=vh.tm_hour, minutes=vh.tm_min, seconds=vh.tm_sec).total_seconds())

# velocity s'/s
v5_sunrise_to_sunset = (new_sunset_s - new_sunrise_s) / (sunset_time_s - sunrise_time_s)
v6_sunset_to_sunrise = (86400 - new_sunset_s + new_sunrise_t_s) / (86400 - sunset_time_s + sunrise_time_t_s)
# -------------------------------------
# time_equation

def time_equation():
    h = datetime.datetime.time(current_local)
    h_seconds = (h.hour * 60 + h.minute) * 60 + h.second
    if h <= sunrise_time:
        new_time_seconds = ((h_seconds + 86400 - sunset_time_y_s) * v6_sunset_to_sunrise + new_sunset_y_s) % 86400
        return new_time_seconds

    elif sunrise_time < h <= sunset_time:
        new_time_seconds = (h_seconds - sunrise_time_s) * v5_sunrise_to_sunset + new_sunrise_s
        return new_time_seconds

    elif sunset_time < h <= datetime.time(23, 59, 59, 999999):
        new_time_seconds = ((h_seconds - sunset_time_s) * v6_sunset_to_sunrise + new_sunset_s) % 86400
        return new_time_seconds

    root.after(60000, time_equation)
    root.after(60000, datetime.datetime.utcnow)

new_seconds = round(time_equation())
new_time2 = datetime.timedelta(seconds=time_equation())
new_time3 = (str(new_time2))
new_clock = new_time3.split('.')[0]

# -------------digital clock -----------
# This function is used to
# display time on the label
root = Tk()
root.title('Clock')
timero = [new_seconds//3600, (new_seconds % 3600)//60, (new_seconds % 60)]
timestr = '00:00:00'
pattern = '{0:02d}:{1:02d}:{2:02d}'

def speed():
    h = datetime.datetime.time(current_local)
    if h <= sunrise_time:
        new_speed = v6_sunset_to_sunrise
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
