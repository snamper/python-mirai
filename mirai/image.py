from pathlib import Path

class InternalImage:
    path: Path

    def __init__(self, path):
        if isinstance(path, str):
            self.path = Path(path)
        elif isinstance(path, Path):
            self.path = path
        