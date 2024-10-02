import os
import uuid

class PathManager():

    _index:int = 0
    _session_id = str(uuid.uuid4())[-8:]
    _temp_paths = []
    
    def __init__(self):
        ...

    def get_temp_image_path(self):
        serial = self._get_serial()
        name = f"{self._session_id}_{serial}_{self._index}"
        path = f"{os.getenv('TEMP')}\{name}.png"
        self._index+=1
        self._temp_paths.append(path)
        return path
    
    def _get_serial(self):
        return str(uuid.uuid4())[-8:]
    
    def clean_temp(self):
        print("Temp Cleanup")
        for path in self._temp_paths:
            if os.path.exists(path)==False:
                continue
            print("Deleting temp file "+path)
            os.unlink(path)
        self._temp_paths = []
        


'''
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -o "P:/projects/riv/temp_no_backup/image_stamp"
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0003.png" -o "P:/projects/riv/temp_no_backup/image_stamp"

'''