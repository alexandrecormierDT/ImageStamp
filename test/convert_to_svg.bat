@echo off
set _path=%~dp0
for %%a in ("%_path%") do set "p_dir=%%~dpa"
for %%a in (%p_dir:~0,-2%) do set "root=%%~dpa"
set serial=%RANDOM%
set script_path=%root%src\main.py 
set input_image=%root%test\input\png\single_images\convert_me_1.png
set output_path=%root%test\output\convert_to_svg\10591_image_%serial%.tvg
echo.%script_path% 
python %script_path% -convert_to_svg -i %input_image% -oi %output_path% 

%output_path% 
