@echo off
set _path=%~dp0
for %%a in ("%_path%") do set "p_dir=%%~dpa"
for %%a in (%p_dir:~0,-2%) do set "root=%%~dpa"
set serial=%RANDOM%
set script_path=%root%src\main.py 
set input_A=%root%test\input\png\single_images\image_A.png
set input_B=%root%test\input\png\single_images\image_B.png
set output_path=%root%test\output\create_diff_map\diff_map_%serial%.png
echo.%script_path% 
python %script_path% -create_diff_map -i %input_A% -i %input_B% -oi %output_path% 
%output_path%