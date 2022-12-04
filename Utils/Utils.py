from datetime import datetime

class Utils:
    _id: int = 0

    def getCurrentTimestampMs() -> int:
        return round(datetime.now().timestamp() * 1000)

    def getNextId() -> int:
        Utils._id += 1
        return Utils._id

    def replaceStrInFile(data: dict[str, str], filePath: str):
        fileText: str = ""
        with open(filePath,'r',encoding = 'utf-8') as f:
            fileText: str = f.read()
            print(f'{fileText=}')
            print(f'{data=}')
            for key, value in data.items():
                fileText = fileText.replace(key, value)

        with open(filePath,'w') as f:
            f.write(fileText)