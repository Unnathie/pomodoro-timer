from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#B9375D"
IMAGE_COLOR="#F7A7A9"
RED = "#e7305b"
BLUE = "#154D71"
PURPLE="#471396"
BROWN="#795757"
FONT=("OCR A Extended", 40, "bold")
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

reps=0
amt=0
work_timer=None
paused=False
remaining_time=0  # Store remaining time when paused

# ---------------------------- TIMER RESET ------------------------------- #
def reset_time():
    global reps, amt, paused, remaining_time
    if work_timer:
        window.after_cancel(work_timer)
    label.config(text="POMODORO TIMER")
    reps=0
    amt=0
    paused=False
    remaining_time=0
    check_mark.config(text="")
    canvas.itemconfig(timer_text, text="00:00")
    start_button.config(state="normal")
    pause_button.config(text="Pause", state="disabled")

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps, amt
    start_button.config(state="disabled")
    pause_button.config(state="normal")

    if reps % 2 != 0:
        amt += 1
    check_mark.config(text="☑" * amt)

    reps += 1
    if reps <= 7:
        if reps % 2 == 0:
            run_timer(SHORT_BREAK_MIN*60)
            label.config(text="Short-Break", fg=PINK)
        else:
            run_timer(WORK_MIN*60)
            label.config(text="Working", fg=BLUE)
    elif reps == 8:
        run_timer(LONG_BREAK_MIN*60)
        label.config(text="Long-Break", fg=PURPLE)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def run_timer(count):
    global work_timer, remaining_time
    remaining_time = count

    minutes = count // 60
    seconds = count % 60
    canvas.itemconfig(timer_text, text=f"{minutes:02}:{seconds:02}")

    if count > 0:
        work_timer = window.after(1000, run_timer, count-1)
    else:
        start_timer()

# ---------------------------- PAUSE/RESUME ------------------------------- #
def pause_resume():
    global paused, work_timer, remaining_time

    if not paused:
        # Pause
        paused = True
        if work_timer:
            window.after_cancel(work_timer)
        pause_button.config(text="Resume")
    else:
        # Resume
        paused = False
        run_timer(remaining_time)
        pause_button.config(text="Pause")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Study timer")
window.config(pady=60)
window.config(bg=IMAGE_COLOR)

label = Label(text="POMODORO TIMER", font=FONT, fg=RED, bg=IMAGE_COLOR)
label.grid(column=1, row=1)

canvas = Canvas(width=578, height=462, highlightthickness=0, bg=IMAGE_COLOR)
img_data = PhotoImage(file="pomodoro.png")
canvas.create_image(289,231,image=img_data)
canvas.grid(column=1,row=2)

check_mark = Label(text="", font=("OCR A Extended", 25, "bold"), fg=BROWN, background=IMAGE_COLOR)
check_mark.grid(row=0, column=1)

timer_text = canvas.create_text(265, 231, text="00:00", font=FONT)

start_button = Button(text="Start", command=start_timer, font=("OCR A Extended", 20, "bold"))
start_button.config(width=10)
start_button.grid(row=3, column=0)

pause_button = Button(text="Pause", command=pause_resume, font=("OCR A Extended", 20, "bold"))
pause_button.config(width=10, state="disabled")
pause_button.grid(row=3, column=1)

rest_button = Button(text="Reset", command=reset_time, font=("OCR A Extended", 20, "bold"))
rest_button.config(width=10)
rest_button.grid(row=3, column=3)

window.mainloop()
