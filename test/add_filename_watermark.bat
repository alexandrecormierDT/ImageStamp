@echo off
set _path=%~dp0
for %%a in ("%_path%") do set "p_dir=%%~dpa"
for %%a in (%p_dir:~0,-2%) do set "root=%%~dpa"
set serial=blobs_%RANDOM%
set script_path=%root%src\main.py 
set input_folder=%root%test\input\png\folder
set output_folder=%root%test\output\add_filename_watermark\%serial%
mkdir %output_folder% 
robocopy %input_folder%  %output_folder%  
python %script_path% -add_filename_watermark -i %output_folder% 
