@echo off
set _path=%~dp0
for %%a in ("%_path%") do set "p_dir=%%~dpa"
for %%a in (%p_dir:~0,-2%) do set "root=%%~dpa"
set serial=blobs_%RANDOM%
set script_path=%root%src\main.py 
set input_image=%root%test\input\png\simple_shape.png
set asset_id=8946
set output_path=%root%test\output\generate\simple_%serial%.png
echo.%script_path% 
python %script_path% -generate -i %input_image% -c %asset_id% -oi %output_path% -im grid
