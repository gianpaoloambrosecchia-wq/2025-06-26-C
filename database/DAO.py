from database.DB_connect import DBConnect
from model.arco import Arco
from model.costruttore import Costruttore
from model.piazzamento import Piazzamento


class DAO():
    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT s.year
                    from seasons s"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["year"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllConstructors():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from constructors"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Costruttore(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getPiazzamenti(idMap, year1, year2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select coalesce(re.position,0) as pos, re.driverId as driver, c.constructorId, year(ra.`date`) as year
                    from constructors c
                    join results re on re.constructorId = c.constructorId 
                    join races ra on ra.raceId = re.raceId 
                    where year(ra.`date`) between %s and %s """
        cursor.execute(query, (year1, year2))


        for row in cursor:
            c = idMap[row["constructorId"]]
            key = row["year"]
            if key not in c.result:
                if int(row["pos"])!=0:
                    c.result[key] = [Piazzamento(row["driver"], row["pos"])]
            else:
                if int(row["pos"]) != 0:
                    c.result[key].append(Piazzamento(row["driver"], row["pos"]))

        cursor.close()
        cnx.close()


    @staticmethod
    def getAllEdges(idMap, year1, year2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT re1.constructorId as c1, re2.constructorId as c2
            FROM results re1
            JOIN races ra1 ON re1.raceId = ra1.raceId
            JOIN results re2 ON re1.raceId = re2.raceId  -- Uniamo sulla stessa gara per trovare i rivali
            WHERE ra1.year BETWEEN %s AND %s
              AND re1.position IS NOT NULL 
              AND re2.position IS NOT NULL
              AND re1.constructorId < re2.constructorId
            GROUP BY re1.constructorId, re2.constructorId"""
        cursor.execute(query, (year1, year2))

        res = []
        for row in cursor:
            res.append(Arco(
                idMap[row["c1"]],
                idMap[row["c2"]]
            ))

        cursor.close()
        cnx.close()
        return res


