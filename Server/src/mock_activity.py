import dao
import datetime
import pytz

tz = pytz.timezone('Asia/Kolkata')
Time = (datetime.datetime.now())
Time=Time.replace(tzinfo=tz)


#print(str(Time))
dao.store_new_alert(26, "Suspicious Activity Mock", "Mock_location",str(Time) )