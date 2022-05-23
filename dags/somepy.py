from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Hey vad, the current Time =", current_time)