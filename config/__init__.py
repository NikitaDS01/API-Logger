import json
import os


class Config(dict):
    def __init__(self, path_to_cfg: str) -> None:
        self._path = path_to_cfg
        with open(self._path, "r", encoding="utf-8") as cfg_file:
            data = json.load(cfg_file)
        super().__init__(data)

    def __getattr__(self, item):
        if item in self:
            value = self[item]
            if isinstance(value, dict):
                return ConfigWrapper(value, self, item)
            return value
        raise AttributeError(f"'Config' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        if key in {"_path"}:
            super().__setattr__(key, value)
        else:
            self[key] = value
            self._upload()

    def _upload(self) -> bool:
        try:
            with open(self._path, "w", encoding="utf-8") as cfg_file:
                json.dump(obj=self, fp=cfg_file, indent=4)
            return True
        except Exception as e:
            print(f"Error uploading config: {e}")
            return False


class ConfigWrapper:
    def __init__(self, data: dict, parent: Config, key: str) -> None:
        self._data = data
        self._parent = parent
        self._key = key

    def __getattr__(self, item):
        if item in self._data:
            value = self._data[item]
            if isinstance(value, dict):
                return ConfigWrapper(value, self._parent, self._key)
            return value
        raise AttributeError(f"'ConfigWrapper' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        if key in {"_data", "_parent", "_key"}:
            super().__setattr__(key, value)
        else:
            self._data[key] = value
            self._parent._upload()

    def _upload(self) -> bool:
        return self._parent._upload()


general_cfg = Config(os.path.join(os.path.dirname(__file__), "general.json"))
