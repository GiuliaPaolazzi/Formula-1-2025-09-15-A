from database.DB_connect import DBConnect
from model.arco import Arco
from model.driver import Driver


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(anno1, anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.*
                    from drivers d, results r , races r2 
                    where d.driverId = r.driverId and r.raceId =r2.raceId 
                    and r2.`year` between %s and %s
                    and r.position is not null
                    order by d.driverId 
                    """

        cursor.execute(query,(anno1,anno2))

        for row in cursor:
            results.append(Driver(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(anno1, anno2, idMapD):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select r1.driverId as d1,r2.driverId as d2, count(*) as peso
                    from results r1, results r2, races r
                    where r1.raceId = r.raceId and r2.raceId = r.raceId
                    and r1.constructorId = r2.constructorId 
                    and r1.driverId < r2.driverId
                    and r1.`position` is not null 
                    and r2.`position` is not null 
                    and r.`year` between %s and %s
                    group by r1.driverId, r2.driverId"""

        cursor.execute(query, (anno1, anno2))

        for row in cursor:
            results.append(Arco(idMapD[row["d1"]], idMapD[row["d2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results

