@echo off
cd /d "C:\Users\mwanji\Desktop\AI project"
kotlinc "MainActivity.kt" -include-runtime -d "MainActivity.jar" && java -jar "MainActivity.jar"
