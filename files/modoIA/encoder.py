
import json
import numpy as np
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, dict):
            return {str(key): self.default(value) for key, value in obj.items()}
        elif isinstance(obj, np.int64):
            return int(obj)  # Convierte int64 a int
        return super().default(obj)