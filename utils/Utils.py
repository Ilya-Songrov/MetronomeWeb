from datetime import datetime

class Utils:
    def getCurrentTimestampMs() -> int:
        return round(datetime.now().timestamp() * 1000)