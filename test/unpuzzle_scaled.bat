@echo off
set _path=%~dp0
for %%a in ("%_path%") do set "p_dir=%%~dpa"
for %%a in (%p_dir:~0,-2%) do set "root=%%~dpa"
set serial=blobs_%RANDOM%
set script_path=%root%src\main.py 
set input_imageA=%root%test\input\png\puzzle\scale\scale_A.png
set input_imageB=%root%test\input\png\puzzle\scale\scale_B.png
set input_imageC=%root%test\input\png\puzzle\scale\scale_C.png
set input_imageD=%root%test\input\png\puzzle\scale\scale_D.png
set output_path=%root%test\output\unpuzzle\unpuzzle_%serial%.png
echo.%script_path% 
python %script_path% -unpuzzle %serial% -i %input_imageA% -i %input_imageB% -i %input_imageC% -i %input_imageD% -oi %output_path% 
%output_path%