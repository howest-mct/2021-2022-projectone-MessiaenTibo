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
    def create_HistoryBadkamer(DeviceId, ActieDatum, Waarde, Commentaar):
        sql = "INSERT INTO HistoriekBadkamer (DeviceId, ActieDatum, Waarde, Commentaar) VALUES (%s,%s,%s,%s)"
        params = [DeviceId, ActieDatum, Waarde, Commentaar]
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
        sql = "SELECT * FROM HistoriekBadkamer where DeviceId = 3 order by Volgnummer desc limit 1"
        result = Database.get_one_row(sql)
        return result

    @staticmethod
    def read_HistoryWaterflow():
        sql = "SELECT * FROM Historiek where DeviceId = 1 order by Volgnummer desc limit 1"
        result = Database.get_one_row(sql)
        return result

    @staticmethod
    def read_HistoryRoomTemp():
        sql = "SELECT * FROM HistoriekBadkamer where DeviceId = 4 order by Volgnummer desc limit 1"
        result = Database.get_one_row(sql)
        return result

    @staticmethod
    def read_WaterUsage():
        sql = "SELECT DATE_FORMAT(ActieDatum, '%Y-%m-%d') AS 'ActieDatum', GebruikerId, DeviceId ,format(sum(Waarde),2) AS 'Totaal', format(avg(Waarde),2) AS 'Gemmiddelde', Commentaar FROM Projectone.Historiek WHERE DeviceId = 1 GROUP BY DATE_FORMAT(ActieDatum, '%Y%m%d');"
        result = Database.get_rows(sql)
        return result

    @staticmethod
    def read_TotalGoal():
        sql = "SELECT SUM(Goal) AS 'TotalGoal' FROM Projectone.Gebruiker where Magneetcontact < 5;"
        result = Database.get_one_row(sql)
        return result

    @staticmethod
    def read_TodaysWaterUsage():
        sql = "SELECT DATE_FORMAT(ActieDatum, '%Y-%m-%d') AS 'ActieDatum', GebruikerId ,format(sum(Waarde),2) AS 'Totaal' FROM Projectone.Historiek where date(ActieDatum) = curdate() AND DeviceId = 1 GROUP BY DATE_FORMAT(ActieDatum, '%Y%m%d'), GebruikerId"
        result = Database.get_rows(sql)
        return result