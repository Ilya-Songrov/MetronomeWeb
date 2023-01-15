import datetime

class Utils:
    _id: int = 0

    def getCurrentTsMs() -> int:
        return round(datetime.datetime.utcnow().timestamp() * 1000)

    def getCurrentTsSec() -> int:
        return int(datetime.datetime.utcnow().timestamp())
        
    def getCurrentMidnightTsSec() -> int:
        todayDatetime: datetime.datetime = datetime.datetime.utcnow()
        midnightDatetime: datetime.datetime = datetime.datetime(year=todayDatetime.year, month=todayDatetime.month, day=todayDatetime.day)
        return int(midnightDatetime.timestamp())

    def getNextId() -> int:
        Utils._id += 1
        return Utils._id
