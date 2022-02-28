from tkinter import *
from tkinter import messagebox
import math
from tkinter.font import ITALIC

Width=600
Height=600
turn_angle_value=0              # ātrums radinos sekundē
turn_angle_per_tick=0           # pa cik grādiem pulksteņrādītājs tiek pagriezts pēc katras operācijas izpildīšanas, jeb "tick"
run=bool                        # mainīgais, kas attiecās uz darbības statusu - pulksteņrādītājs vai nu kustas (TRUE), vai nēkustas (FALSE)

def start():
    global run
    run = True
    
def pause():
    global run
    run = False

def confirm():
    global angle_input, turn_angle_value, current_speed_value, run, turn_angle_per_tick
    try:
        turn_angle_value=float(angle_input.get())/8
        current_speed_value.config(text=str(turn_angle_value*8))
        run=False
        turn_angle_per_tick = abs(turn_angle_value)
        
    except ValueError:
        turn_angle_value=0
        angle_input.delete(0,"end")
        current_speed_value.config(text=str(turn_angle_value))
        messagebox.showwarning("Warning", "Must be a Number, not a String")

def reset():
    global run, second_end, minute_end, hour_end, angle_input, canvas, turn_angle_value, current_speed, turn_angle_per_tick
    run=False
    turn_angle_value=0
    turn_angle_per_tick = turn_angle_value
    angle_input.delete(0,"end")
    current_speed_value.config(text=str(turn_angle_value))
    second_end = [0, 280]
    minute_end = [0, 200]
    hour_end   = [0, 180]
    canvas.coords(line_sec, Width/2.0, Height/2.0, second_end[0]+center_x, -1*(second_end[1])+center_y)
    canvas.coords(line_min, Width/2.0, Height/2.0, minute_end[0]+center_x, -1*(minute_end[1])+center_y)
    canvas.coords(line_hour, Width/2.0, Height/2.0, hour_end[0]+center_x, -1*(hour_end[1])+center_y)

def move_clock(): #pulksteņrādītāja pagriešana
    global second_end, turn_angle_per_tick, line_sec,line_min, line_hour, Width, Height, center_x, center_x, canvas, hour_end, minute_end
    if run: 
        x1=float(second_end[0] * (math.cos(math.radians(turn_angle_per_tick))) - second_end[1] * (math.sin(math.radians(turn_angle_per_tick))) )
        y1=float(second_end[0] * (math.sin(math.radians(turn_angle_per_tick))) + second_end[1] * (math.cos(math.radians(turn_angle_per_tick))) )
        second_end[0]=x1
        second_end[1]=y1
        x1=float(minute_end[0] * (math.cos(math.radians(turn_angle_per_tick/60.0))) - minute_end[1] * (math.sin(math.radians(turn_angle_per_tick/60.0))) )
        y1=float(minute_end[0] * (math.sin(math.radians(turn_angle_per_tick/60.0))) + minute_end[1] * (math.cos(math.radians(turn_angle_per_tick/60.0))) )
        minute_end[0]=x1
        minute_end[1]=y1
        x1=float(hour_end[0] * (math.cos(math.radians(turn_angle_per_tick/720.0)))) - hour_end[1] * (math.sin(math.radians(turn_angle_per_tick/720.0)))
        y1=float(hour_end[0] * (math.sin(math.radians(turn_angle_per_tick/720.0)))) + hour_end[1] * (math.cos(math.radians(turn_angle_per_tick/720.0))) 
        hour_end[0]=x1
        hour_end[1]=y1
        if turn_angle_value >0:
            canvas.coords(line_sec, Width/2.0, Height/2.0, -1*(second_end[0])+center_x, -1*(second_end[1])+center_y)
            canvas.coords(line_min, Width/2.0, Height/2.0, -1*(minute_end[0])+center_x, -1*(minute_end[1])+center_y)
            canvas.coords(line_hour, Width/2.0, Height/2.0, -1*(hour_end[0])+center_x, -1*(hour_end[1])+center_y)
        elif turn_angle_value <0:
            canvas.coords(line_sec, Width/2.0, Height/2.0, (second_end[0])+center_x, -1*(second_end[1])+center_y)
            canvas.coords(line_min, Width/2.0, Height/2.0, (minute_end[0])+center_x, -1*(minute_end[1])+center_y)
            canvas.coords(line_hour, Width/2.0, Height/2.0, (hour_end[0])+center_x, -1*(hour_end[1])+center_y)
    root.after(125, move_clock)

root = Tk()
root.title("TEMPUS FUGIT")
root.geometry('1000x600')
root.resizable(width=False, height=False)                               # lietotnes īpašibas

gui_text=Frame(root)
gui_text.place(relheight=0.4, relwidth=0.2)                             # Frame box tekstam saskarsnē

controls=Frame(root)
controls.place(rely=0.475, relheight=0.520, relwidth=0.2, relx=0.005 )  # Frame box pogām

############################################################## IEVADE ##############################################################

angle_text = Label(gui_text, text="Ātrums(grad/sec):", font='Ubuntu 16 bold', justify='center')
angle_text.pack(anchor='n')

#INPUT BOX
angle_input = Entry(gui_text, width=4, selectborderwidth=4)  
angle_input.pack(side="top", anchor="n", pady=4)

#CONFIRM BUTTON
confirm_image=PhotoImage(file='confirm.png')
confirm_button=Button(gui_text, text="Confirm", command=confirm, bg='#567',image=confirm_image)             # spiežot šo pogu lietotājs atstiprina, kā vēlas  
confirm_button.pack(side="top", anchor="n")                                                                 # lai pulksteņrādītāji kustas ar ievadīto ātrumu

#CURRENT SPEED LABEL
current_speed=Label(gui_text, text="Current set speed: " , font='Ubuntu 15', justify='center')              #
current_speed.pack(anchor="n")                                                                              #
                                                                                                            #
current_speed_value=Label(gui_text, text=str(turn_angle_value), font='Ubuntu 40 italic', justify='center' ) # izvada pašreizējo iestatīto ātrumu
current_speed_value.pack(pady=20)

#RESET
reset_image=PhotoImage(file='reset.png')                                                                    # Reset poga, kura pārtrauca pulksteņrādītāju kustību
reset_button=Button(controls, command=reset, image=reset_image)                                             # un atgriež to uz sākumpozīciju   
reset_button.grid(row=0, column=0)

#START
start_image=PhotoImage(file='start.png')                                                                    # Start poga
start_button=Button(controls, command=start, image=start_image)
start_button.grid(row=1, column=0)

#pause
pause_image=PhotoImage(file='pause.png')
pause_button=Button(controls, command=pause, image=pause_image)                                             # pauze, pulksteņrādītāji apstājas, bet iestatītais ātrums
pause_button.grid(row=2, column=0)                                                                          # un pēdējā pozicija saglabājas

########################################### CANVAS ########################################################
#right background
Salvador=PhotoImage(file='Salvador.png')
background=Canvas(root, width=200, height=600)
background.create_image(103,300,image=Salvador)
background.place(relx=0.8)

canvas=Canvas(root,height=600, width=600, bg='white')
#clock's background
bg = PhotoImage(file='roman3.png')
canvas.create_image(Width/2, Height/2, image=bg)
canvas.pack(anchor='center')

#clock's properties
center_x = Width/2.0                # Koordināšu nobīde. TKinter vidē koordināšu sistēma sākas ar (0,0) koordinātes un pieņem vērtības tikai I. kvadrantā(+,+).
center_y = Height/2.0               # Savukārt, pulksteņrādītāji pēc savas būtības atrodas visos 4 kvadrantos attiecībā pret (0,0) koordināšu  
                                    # Tādēļ nepieciešama nobīde I. kvadranta virzienā

second_end = [0, 280]               # Sekundes pulksteņrādītāja sākumpozīcija
minute_end = [0, 200]               # Minūtes pulksteņrādītāja sākumpozīcija
hour_end   = [0, 180]               # Stundas pulksteņrādītāja sākumpozīcija

line_sec=canvas.create_line(Width/2.0, Height/2.0, second_end[0]+center_x, -1*(second_end[1])+center_y,  width=3, fill='red')
line_min=canvas.create_line(Width/2.0, Height/2.0, minute_end[0]+center_x, -1*(minute_end[1])+center_y,  width=2, fill='black')
line_hour=canvas.create_line(Width/2.0, Height/2.0, hour_end[0]+center_x, -1*(hour_end[1])+center_y,  width=2, fill='green')
move_clock()
root.mainloop()