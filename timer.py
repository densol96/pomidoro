from tkinter import *
from tkinter import simpledialog
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
REPS = 0
MARK = "✔"
timer = None
# ---------------------------- SET UP ALARM -------------------------------#
pygame.init()
alarm_sound = pygame.mixer.Sound("alarm.wav")
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global REPS
    window.after_cancel(timer)
    canvas.itemconfig(text_id, text=f"{WORK_MIN}:00")
    check_mark.config(text="")
    label_for_check.config(text="TIMER", fg=GREEN)
    start_button.config(state="active")
    REPS = 0
# ---------------------------- TIMER MECHANISM ------------------------------- # 
def count_down(amount_of_time):
    global REPS
    minutes = amount_of_time // 60
    seconds = amount_of_time % 60
    canvas.itemconfig(text_id, text=f"{minutes:02d}:{seconds:02d}")
    if amount_of_time > 0:
        global timer
        timer = window.after(1000, count_down, amount_of_time - 1)
    else:
        alarm_sound.play()
        start_button.config(state="active")
        if REPS >= 7:
            start_button.config(state="disabled")
            label_for_check.config(text="END")
        if REPS % 2 == 0:
            marks = check_mark.cget("text")
            if len(marks) != 4:
                marks += MARK
                check_mark.config(text=marks)
        REPS += 1
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def start_timer():
    start_button.config(state="disabled")
    if REPS == 7:
        label_for_check.config(text="BREAK", font=(FONT_NAME, 45, "bold"), fg=PINK)
        count_down(LONG_BREAK_MIN * 60)
    elif REPS % 2 == 0:
        label_for_check.config(text="WORK", font=(FONT_NAME, 45, "bold"), fg=RED)
        count_down(WORK_MIN * 60)
    else:
        label_for_check.config(text="BREAK", font=(FONT_NAME, 45, "bold"), fg=GREEN)
        count_down(SHORT_BREAK_MIN * 60)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.geometry("500x500")
window.resizable(0, 0)
window.config(padx=115, pady=75, bg=YELLOW)


canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
image_object = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=image_object)

text_id = canvas.create_text(100, 130, text="25:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

label_for_check = Label(text="TIMER", font=(FONT_NAME, 45, "bold"), bg=YELLOW, fg=GREEN)
label_for_check.grid(row=0, column=1)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=3)

check_mark = Label(text="", font=(FONT_NAME, 25, "normal"), bg=YELLOW, fg=GREEN)
check_mark.config(pady=15)
check_mark.grid(row=2, column=1)

WORK_MIN = simpledialog.askinteger(title="Work", prompt="Please, provide a number of minutes for work session: ", parent=window)
if WORK_MIN is not None:
    canvas.itemconfig(text_id, text=f"{WORK_MIN}:00")
else:
    WORK_MIN = 25

SHORT_BREAK_MIN = simpledialog.askinteger(title="Short break", prompt="Please, provide a number of minutes for short break: ", parent=window)
if SHORT_BREAK_MIN is None:
    SHORT_BREAK_MIN = 5

LONG_BREAK_MIN = simpledialog.askinteger(title="Long break", prompt="Please, provide a number of minutes for long break: ", parent=window)
if LONG_BREAK_MIN is None:
    WORK_MIN = 20

window.mainloop()