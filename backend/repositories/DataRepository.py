from tkinter import W
from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_Device():
        sql = "SELECT * FROM Device"
        result = Database.get_rows(sql)
        return result

    @staticmethod
    def create_History(DeviceId, GebruikerId, ActieDatum, Waarde, Commentaar):
        sql = "INSERT INTO Historiek (DeviceId, GebruikerId, ActieDatum, Waarde, Commentaar) VALUES (%s,%s,%s,%s,%s)"
        params = [DeviceId, GebruikerId, ActieDatum, Waarde, Commentaar]
        result = Database.execute_sql(sql, params)
        return result

    @staticmethod
    def update_History(Volgnummer, DeviceId, GebruikerId, ActieDatum, Waarde, Commentaar):
        sql = "update Historiek set DeviceId = %s, GebruikerId = %s, ActieDatum = %s, Waarde = %s, Commentaar = %s where Volgnummer = %s"
        params = [DeviceId, GebruikerId, ActieDatum, Waarde, Commentaar, Volgnummer]
        result = Database.execute_sql(sql, params)
        return result

    @staticmethod
    def read_HistoryWaterTemp():
        sql = "SELECT * FROM Historiek where DeviceId = 2 order by Volgnummer desc limit 1"
        result = Database.get_one_row(sql)
        return result

    @staticmethod
    def read_HistoryHumidity():
        sql = "SELECT * FROM Historiek where DeviceId = 3 order by Volgnummer desc limit 1"
        result = Database.get_one_row(sql)
        return result

    @staticmethod
    def read_HistoryWaterflow():
        sql = "SELECT * FROM Historiek where DeviceId = 1 order by Volgnummer desc limit 1"
        result = Database.get_one_row(sql)
        return result 