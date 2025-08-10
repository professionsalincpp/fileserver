from logger import MultiLogger

_logger = MultiLogger("datachecker")

class DataChecker:
    @classmethod
    def check_upload_data(cls, data: dict) -> bool:
        _keys = [
            "path",
            "data",
            "hash",
            "mode"
        ]
        return cls.check_keys(cls, _keys, data)
    
    @classmethod
    def check_download_data(cls, data: dict) -> bool:
        _keys = [
            "path",
            "mode"
        ]
        return cls.check_keys(cls, _keys, data)
    
    @classmethod
    def check_copy_data(cls, data: dict) -> bool:
        _keys = [
            "path",
            "mode"
        ] 
        _path_keys = [
            "source",
            "destination"
        ]
        if cls.check_keys(cls, _keys, data) and cls.check_keys(cls, _path_keys, data):
            if data["source"] != data["destination"]:
                return True
            else:
                _logger.error("Source and destination are the same", context="check_data")
                return False
            
        return False
    
    @classmethod
    def check_move_data(cls, data: dict) -> bool:
        return cls.check_copy_data(cls, data) # Used check_copy_data, because it's the same

    @classmethod
    def check_create_dir_data(cls, data: dict) -> bool:
        _keys = [
            "path",
            "mode"
        ]
        return cls.check_keys(cls, _keys, data)
    
    @classmethod
    def check_keys(cls, keys: list, data: dict) -> bool:
        if all([key in data for key in keys]):
            return True
        else:
            _logger.error(f"Missing keys in data: {list(set(keys) - set(data.keys()))}", context="check_keys")
            return False