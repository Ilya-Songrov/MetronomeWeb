from datetime import datetime

class Utils:
    _id: int = 0

    def getCurrentTimestampMs() -> int:
        return round(datetime.now().timestamp() * 1000)

    def getNextId() -> int:
        return Utils._id + 1