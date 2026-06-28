from database.DB_connect import DBConnect
from model.teams import Teams


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.`year` 
                        from teams t 
                        where t.`year` >="1980"
                        order by t.`year` asc """
        cursor.execute(query)
        for row in cursor:
            results.append(row["year"])
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllTeamsByYear(year):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select t.*
                    from teams t 
                    where t.`year` =%s
                    order by t.teamCode asc """
        cursor.execute(query, (year,))
        for row in cursor:
            results.append(Teams(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getSalariesByTeam(year, idMapTeams):
        conn = DBConnect.get_connection()
        results = {}
        cursor = conn.cursor(dictionary=True)
        query = """SELECT t.ID, t.teamCode, SUM(s.salary) AS totSalary
                FROM salaries s, teams t, appearances a
                WHERE s.year = t.year
                  AND t.year = a.year
                  AND a.year = %s
                  AND t.ID = a.teamID
                  AND a.playerID = s.playerID
                GROUP BY t.ID, t.teamCode
                                            """
        cursor.execute(query, (year,))
        for row in cursor:
            results[idMapTeams[row["ID"]]] = row["totSalary"]
        cursor.close()
        conn.close()
        return results
