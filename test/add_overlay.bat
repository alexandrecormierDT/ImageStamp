@echo off
set _path=%~dp0
for %%a in ("%_path%") do set "p_dir=%%~dpa"
for %%a in (%p_dir:~0,-2%) do set "root=%%~dpa"
set serial=blobs_%RANDOM%
set script_path=%root%src\main.py 
set input_image=%root%test\input\png\sequence\image_0001.png
set overlay_json=%root%test\input\json\sequence\image_0001.png
set output_path=%root%test\output\add_overlay\billy_decor_1_watermark_%serial%.png
echo.%script_path% 
python %script_path% -add_overlay %serial% -i %input_image% -oi %output_path% -oj %overlay_json%
%output_path%