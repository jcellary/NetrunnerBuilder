@echo off
echo Download ocgtn files for your decks and name them current_corp.o8d, next_corp.o8d, current_runner.o8d, next_runner.o8d. Result will be stored as output.csv
pause
del output.csv
python netrunner.py >> output.csv