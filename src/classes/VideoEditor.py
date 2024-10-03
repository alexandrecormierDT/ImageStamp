import os
from classes.PathManager import PathManager
import subprocess
from subprocess import PIPE
from pathlib import Path

class VideoEditor():

    _PM:PathManager = PathManager()
    _ffmpeg_path:str = "P:/pipeline/extra_soft/ffmpeg/bin/ffmpeg.exe"
    _extraction_rate:int = 1
    
    def __init__(self):

        ...

    def extract_frames(self,_video_path:str)->list:
        frames = []
        temp_folder_path = self._PM.create_temp_folder()
        cmd = self._format_get_frames_cmd_line(_video_path,temp_folder_path)
        result = subprocess.run(cmd, stdout=PIPE)
        print(result)
        frames = self._get_folder_frames(temp_folder_path)
        self._delete_folder(temp_folder_path)
        return frames
    
    def _get_folder_frames(self,_folder_path:str)->list:
        frame_paths = []
        image_formats = ["png","tga","jpg"]
        for file in os.listdir(_folder_path):
            if file.split(".")[-1] not in image_formats:
                continue
            full_path = _folder_path+"\\"+file
            frame_paths.append(full_path)
            #self._PM.add_as_temp_path(full_path)
        return frame_paths

    def _delete_folder(self,_folder:str):
        ...
    
    def _format_get_frames_cmd_line(self,_video_path:str,_temp_folder:str="")->list:
        # ffmpeg -i video.mp4 -r 1 frame%d.png
        cmd = []
        cmd.append(self._ffmpeg_path)
        cmd.append("-i")
        cmd.append(_video_path)
        #cmd.append("-r")
        #cmd.append(str(self._extraction_rate))
        cmd.append(_temp_folder+"/frame_%4d.png")
        return cmd



'''
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -o "P:/projects/riv/temp_no_backup/image_stamp"
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -apply_filter "BW" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0003.png" -add_text "this is my text" -o "P:/projects/riv/temp_no_backup/image_stamp" 

'''