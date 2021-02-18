from pathlib import Path

class PathHelper():
    
    @staticmethod
    def JsonRoot():
        return f"{Path().absolute()}\io\json"