@echo off
set _path=%~dp0
for %%a in ("%_path%") do set "p_dir=%%~dpa"
for %%a in (%p_dir:~0,-2%) do set "root=%%~dpa"
set serial=blobs_%RANDOM%
set script_path=%root%src\main.py 
set input_image=%root%test\input\png\billy_decor.png
set asset_id=8946
set output_path=%root%test\output\generate\billy_decor_qrcode_%serial%.png
echo.%script_path% 
python %script_path% -add_qrcode %asset_id% -i %input_image% -oi %output_path% -im grid
