::  ------------------------------------------------------------------------------------I
::											I
:: This Script is for copying All RAW CSV-files from VideoLogger			I
:: to a merged CSV file to be used by the Capjet Sword Speed software			I
::											I
:: 2 parameters should be set in this script. srcLoc and destLoc			I
::											I
::											I
::							Daniel 23.06.2018		I
:: History:										I
:: 22.06.2018 - Replaced XCOPY with ROBOCOPY						I
:: 23.06.2018 - Copy only CSV files from source destination				I
::											I
::											I
:: -------------------------------------------------------------------------------------I

@ECHO OFF

:: choose source location from where the videofiles are stored, either Option, VisualSoft PC or NAS
SET srcLoc=D:\temp\TID328\Option
:: choose destination location from where the files should be copied. I.e. the entire path of 'CapjetSwordSpeed\InputData'
SET destLoc=D:\temp\InputData

:: Do not change these parameters
SET taskplan=%1
:: choose date for which CSV files to copy from source yyyymmdd(robocopy), This is defined in ini file
SET startDate=%2
:: choose date for which CSV files to copy from source yyyymmdd(robocopy), This is defined in ini file
SET endDate=%3

:: if not exist "%destLoc%" mkdir %destLoc%
if not exist %destLoc%\RAW_TID%taskplan% mkdir %destLoc%\RAW_TID%taskplan%

SET rawDest=%destLoc%\RAW_TID%taskplan%

ECHO Start Copy files from remote location
robocopy "%srcLoc% " "%rawDest% " file *.csv /maxage:%startDate% /minage:%endDate% /it /S 

:: copy files to same folder (move would be better, but is it safe enough???
for /r "%rawDest%" %%x in (*.csv) do copy "%%x" "%rawDest%"

ECHO Start Merging files into input file
copy "%rawDest%"\*.csv "%destLoc%"\input_TID"%taskplan%".csv

:: Outputting filename to python
ECHO %destLoc%\input_TID%taskplan%.csv