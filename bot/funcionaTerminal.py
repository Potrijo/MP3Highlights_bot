import os

'''Hay que cambiarlo para que entre el usuario los datos desde el chat
esto no nos sirve porque es para la terminal'''
filename = input("Name of file to clip: ")
startTime = input("Input the start time (HH:mm:ss): ")
fileLength = input("Input the length of the clip (HH:mm:ss): ")

startTimeHours = startTime[0:2]
startTimeMinutes = startTime[3:5]
startTimeSeconds = startTime[6:8]

try:
    startPoint = str(startTimeHours) + ":" + str(startTimeMinutes) + ":" + str(startTimeSeconds)
    print(startPoint)
    print(f"Length: {fileLength}")

    os.system(f"ffmpeg -ss {startPoint} -i {filename} -t {fileLength} {filename}_clip.mp3")
except Exception as e:
    print(e)
    print("Error, introdueix un format correcte. ")    