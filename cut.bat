@echo off

set /p start="Start: "
set /p end="End: "

set a=%~dpn1
set b=%~x1

ffmpeg -i "%~1" -ss %start% -to %end% -avoid_negative_ts make_zero -c copy "%a%cut%b%"
