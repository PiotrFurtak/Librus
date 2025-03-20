import requests,json
from urllib.parse import urljoin
# from grades import get_grade_info

class LibrusSession():

    def __init__(self):
        self._html_session = None

    def login(self, username, password):
        self._html_session = requests.session()
        self._html_session.get(url='https://api.librus.pl/OAuth/Authorization?client_id=46&response_type=code&scope=mydata')
        response = self._html_session.post(url='https://api.librus.pl/OAuth/Authorization?client_id=46',
                                           data={'action': 'login', 'login': username, 'pass': password})
        if not response.json().get('status') == 'ok' or not response.json().get('goTo'):
            raise RuntimeError("Login failed")
        self._html_session.get(url=urljoin(response.url, response.json()['goTo']))

    def get(self,url) -> str:
        res = self._html_session.get(url)
        res.raise_for_status()
        return res.text

    def get_lesson(self,id):
        res = self.get("https://synergia.librus.pl/gateway/api/2.0/Lessons/%s"%id)
        return json.loads(res)["Lesson"]

    def get_subject(self,id):
        res = self.get("https://synergia.librus.pl/gateway/api/2.0/Subjects/%s"%id)
        return json.loads(res)["Subject"]["Name"]

    def get_teacher(self,id):
        res = self.get("https://synergia.librus.pl/gateway/api/2.0/Users/%s"%id)
        data = json.loads(res)["User"]
        return " ".join((data["FirstName"],data["LastName"]))

    def get_type(self,id):
        res = self.get("https://synergia.librus.pl/gateway/api/2.0/Attendances/Types/%s"%id)
        return json.loads(res)["Type"]["Name"]




if __name__ == "__main__":

    Librus = LibrusSession()
    login = input("Podaj login: ")
    password = input("Podaj hasło: ")
    Librus.login(login, password)
    print("Zalogowano pomyślnie")
    attendances = {}
    types = {}
    lessons = {}
    res = Librus.get("https://synergia.librus.pl/gateway/api/2.0/Attendances?showPresences=true")
    data = json.loads(res)
    for x in data["Attendances"]:
        if x["Semester"] == 1:
            continue
        lesson_id = x["Lesson"]["Id"]
        type_id = x["Type"]["Id"]
        if type_id not in types:
            types.setdefault(type_id,Librus.get_type(type_id))
        attendance_type = types[type_id]
        if lesson_id not in lessons:
            lesson = Librus.get_lesson(lesson_id)
            subject_id = lesson["Subject"]["Id"]
            subject = Librus.get_subject(subject_id)
            lessons.setdefault(lesson_id, subject)
            attendances.setdefault(subject, {"Presences":0, "Abscences":0})
        if attendance_type in ("Obecność","Spóźnienie", "Zwolnienie"):
            attendances[lessons[lesson_id]]["Presences"] += 1
        elif attendance_type in ("Nieobecność","Nieobecność uspr."):
            attendances[lessons[lesson_id]]["Abscences"] += 1

    for x in sorted(attendances):
        if (attendances[x]["Presences"]+attendances[x]["Abscences"]) == 0:
            print(x,attendances[x],"0%")
            continue
        ratio = attendances[x]["Presences"]/(attendances[x]["Presences"]+attendances[x]["Abscences"])
        procent = str(int(ratio*100))+"%"
        print(x,attendances[x],procent)
    abscences = 0
    presences = 0
    for x in attendances.values():
        presences += x["Presences"]
        abscences += x["Abscences"]
    print("Łączna frekwencja: ","%s"%int(presences*100/(presences+abscences)),"%",sep="")

