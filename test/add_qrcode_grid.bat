@echo off
set _path=%~dp0
for %%a in ("%_path%") do set "p_dir=%%~dpa"
for %%a in (%p_dir:~0,-2%) do set "root=%%~dpa"
set serial=blobs_%RANDOM%
set script_path=%root%src\main.py 
set input_image=%root%test\input\png\billy_decor_1.png
set asset_id=8946
set output_path=%root%test\output\add_qrcodes\billy_decor_1_qrcode_%serial%.png
echo.%script_path% 
python %script_path% -add_qrcode %asset_id% -i %input_image% -oi %output_path% -im grid
echo.NEXT
set serial=blobs_%RANDOM%
set script_path=%root%src\main.py 
set input_image=%root%test\input\png\billy_decor_2.png
set asset_id=2075
set output_path=%root%test\output\add_qrcodes\billy_decor_2_qrcode_%serial%.png
echo.%script_path% 
python %script_path% -add_qrcode %asset_id% -i %input_image% -oi %output_path% -im grid
echo.NEXT
set serial=blobs_%RANDOM%
set script_path=%root%src\main.py 
set input_image=%root%test\input\png\billy_decor_3095.png
set asset_id=3095
set output_path=%root%test\output\add_qrcodes\billy_decor_3095_%serial%.png
echo.%script_path% 
python %script_path% -add_qrcode %asset_id% -i %input_image% -oi %output_path% -im grid
echo.NEXT
set serial=blobs_%RANDOM%
set script_path=%root%src\main.py 
set input_image=%root%test\input\png\billy_decor_6039.png
set asset_id=6039
set output_path=%root%test\output\add_qrcodes\billy_decor_6039_%serial%.png
echo.%script_path% 
python %script_path% -add_qrcode %asset_id% -i %input_image% -oi %output_path% -im grid