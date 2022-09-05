from hashlib import md5
from datetime import datetime, timedelta

# 只需修改此处的导入文件名
from CQUPT import school    # 创建学校的对象并导入为 school
from CQUPT import classes   # 创建课表数组并导入为 classes

classTime = [None, *school.classTime]
weeks = [None]
starterDay = datetime(*school.starterDay)
for i in range(1, 30):
	singleWeek = [None]
	for d in range(0, 7):
		singleWeek.append(starterDay)
		starterDay += timedelta(days = 1)
	weeks.append(singleWeek)


uid_generate = lambda key1, key2: md5(f"{key1}{key2}".encode("utf-8")).hexdigest()

iCal = """BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0
X-WR-CALNAME:课表
X-WR-TIMEZONE:Asia/Shanghai
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:Asia/Shanghai
END:VTIMEZONE
"""

alarm = f"""
BEGIN:VALARM
X-WR-ALARMUID:B0A2DECC-0788-477C-99CA-2A235181AD3E
UID:B0A2DECC-0788-477C-99CA-2A235181AD3E
TRIGGER:-PT{school.alarmTime}M
ATTACH;VALUE=URI:Chord
ACTION:AUDIO
END:VALARM
"""

runtime = datetime.now().strftime('%Y%m%dT%H%M%SZ')

for Class in classes:
	[Name, Teacher, Location, classWeek, classWeekday, classOrder] = Class[:]
	Title = Name + " - " + Location

	for timeWeek in classWeek:
		classDate = weeks[timeWeek][classWeekday]
		startTime = classTime[classOrder[0]]; endTime = classTime[classOrder[-1]]
		classStartTime = classDate + timedelta(minutes = startTime[0] * 60 + startTime[1])
		classEndTime = classDate + timedelta(minutes = endTime[0] * 60 + endTime[1] + school.classPeriod)
		Description = "任课教师: " + Teacher + "。"

		StartTime = classStartTime.strftime('%Y%m%dT%H%M%S')
		EndTime = classEndTime.strftime('%Y%m%dT%H%M%S')
		singleEvent = f"""BEGIN:VEVENT
DTEND;TZID=Asia/Shanghai:{EndTime}
DESCRIPTION:{Description}
UID:{uid_generate(Name, StartTime)}
DTSTAMP:{runtime}
URL;VALUE=URI:
SUMMARY:{Title}
DTSTART;TZID=Asia/Shanghai:{StartTime}
{school.geo(Location)}
{alarm if school.alarmTime else ""}
END:VEVENT
"""
		iCal += singleEvent

iCal += "END:VCALENDAR"

with open(f"{school.name}.ics", "w", encoding = "utf-8") as w:
	w.write(iCal)
