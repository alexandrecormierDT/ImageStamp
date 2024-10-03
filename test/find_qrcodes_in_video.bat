@echo off
set _path=%~dp0
for %%a in ("%_path%") do set "p_dir=%%~dpa"
for %%a in (%p_dir:~0,-2%) do set "root=%%~dpa"
set serial=blobs_%RANDOM%
set script_path=%root%src\main.py 
set input=%root%test\input\video\scene_with_qrcodes.mov
set output_path=%root%test\output\find_qrcodes\video_qrcodes_%serial%.json
echo.%script_path% 
python %script_path% -find_qrcodes -i %input% -o %output_path%
