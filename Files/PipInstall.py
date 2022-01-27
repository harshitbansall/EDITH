import os
command="@echo off"
for i in ["wikipedia","fpdf","python-magic-bin==0.4.14","docx2pdf","pyttsx3","matplotlib","numpy","clipboard","pyautogui","nltk","translate","pyqrcode","pypng"]:
    command+=" & pip install {}".format(i)
os.system(command)

#uninstall all modules -->
#pip freeze > requirements.txt
#pip uninstall -y -r requirements.txt 
