from LibrusSession import LibrusSession
import json,time

output = "\n"

def dateComp(JSONformat,timeformat):
    JSONformat = [int(x) for x in JSONformat.split("-")]
    timeformat = [timeformat[x] for x in range(3)]
    return JSONformat == timeformat

Librus = LibrusSession()
login = input("Podaj login: ")
password = input("Podaj hasło: ")
Librus.login(login, password)
print("Zalogowano pomyślnie")


today = time.localtime()
tomorrow = target = time.strptime(str(today.tm_year) + " " + str(today.tm_yday+1),"%Y %j")
target = time.strptime(str(today.tm_year) + " " + str(today.tm_yday+1),"%Y %j")
while target.tm_wday > 0:
    if target.tm_yday == 1:
        target = time.strptime(str(target.tm_year) + " 12 31", "%Y %m %d")
        continue
    target = target = time.strptime(str(target.tm_year) + " " + str(target.tm_yday-1),"%Y %j")
date = "-".join([str(target[x]) for x in range(3)])

res = Librus.get("https://synergia.librus.pl/gateway/api/2.0/Timetables?weekStart="+date)
data = json.loads(res)
for key in data["Timetable"].keys():
    if dateComp(key,(tomorrow if today.tm_hour >= 12 else today)):
        day = data["Timetable"][key]
        break

res = Librus.get("https://synergia.librus.pl/gateway/api/2.0/Calendars")
data = json.loads(res)
res = Librus.get("https://synergia.librus.pl/gateway/api/2.0/Calendars/"+data['Calendars'][0]['Id'])
data = json.loads(res)
HomeWorksID = [str(x['Id']) for x in data['Calendar']['HomeWorks']]\

res = Librus.get("https://synergia.librus.pl/gateway/api/2.0/HomeWorks/"+",".join(HomeWorksID))
data = json.loads(res)
HomeWorks = {}
for x in data["HomeWorks"]:
    Date = x["Date"]
    if not dateComp(Date,tomorrow):
        continue
    Subject = Librus.get_subject(x["Subject"]["Id"])
    Content = x["Content"]
    HomeWorks.setdefault(Subject,Content)

for i,x in enumerate(day):
    if len(x) == 0:
        continue
    Subject = x[0]["Subject"]["Name"]
    output += str(i) + ". "
    if x[0]["IsSubstitutionClass"] == True:
        orgSub = Librus.get_subject(x[0]["OrgSubject"]["Id"])
        newTea = x[0]["Teacher"]["FirstName"] + " " + x[0]["Teacher"]["LastName"]
        output += "%s -> (%s) "%(orgSub,newTea)
    output += Subject + (" ---> "+HomeWorks[Subject] if Subject in HomeWorks.keys() else "")
    if x[0]["IsCanceled"] == True:
        output += " (Odwołana) "
    output += "\n"
output = output[:-1]
if __name__ == "__main__":
    print(output)