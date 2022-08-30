import tkinter as tk
window=tk.Tk()
window.geometry("250x250")

def college():
    newwindow2=tk.Toplevel()
    newwindow2.geometry("550x550")
    #T = tk.Text(newwindow2, height = 5, width = 52)
    l1=tk.Label("1. What is most challenging aspect that you have faced in a project?")
    #start1= tk.Button(newwindow2,text="START",font=("Courier", 8),width=35,height=2,bg='white',activebackground='deep sky blue')
    #stop1= tk.Button(newwindow2,text="STOP",font=("Courier", 8),width=35,height=2,bg='white',activebackground='deep sky blue')    
    #l2=tk.Label(quest2="2. This is the second question")
    #start2= tk.Button(newwindow2,text="START",font=("Courier", 8),width=35,height=2,bg='white',activebackground='deep sky blue')
    #stop2 = tk.Button(newwindow2,text="STOP",font=("Courier", 8),width=35,height=2,bg='white',activebackground='deep sky blue')
    l1.pack()
    #start1.pack(pady=15)
    #stop1.pack(pady=15)
    #l2.pack()
    #start2.pack(pady=15)
    #stop2.pack(pady=15)



def student():
    newwindow1=tk.Toplevel()
    newwindow1.geometry("350x350")
    fnd = tk.Button(newwindow1,text="FOUNDATION LEVEL",font=("Courier", 8),width=35,height=2,bg='white',activebackground='deep sky blue')
    fnd.pack(pady=15)
    prep = tk.Button(newwindow1,text="PREPARATORY LEVEL ",font=("Courier", 8),width=35,height=2,bg='white',activebackground='deep sky blue')
    prep.pack(pady=15)
    mid = tk.Button(newwindow1,text="MIDDLE LEVEL",font=("Courier", 8),width=35,height=2,bg='white',activebackground='deep sky blue')
    mid.pack(pady=15)
    sec = tk.Button(newwindow1,text="SECONDARY LEVEL",font=("Courier", 8),width=35,height=2,bg='white',activebackground='deep sky blue')
    sec.pack(pady=15)
    clg = tk.Button(newwindow1,text="COLLEGE YOUTH LEVEL",font=("Courier", 8),width=35,height=2,bg='white',activebackground='deep sky blue', command=college)
    clg.pack(pady=15)


teacher = tk.Button(window,text="TEACHER",font=("Courier", 8),width=25,height=5,bg='white',activebackground='deep sky blue')  # command missing
teacher.pack(pady=15)
student = tk.Button(window,text="STUDENT",font=("Courier", 8),width=25,height=5,bg='white',activebackground='deep sky blue',command=student)
student.pack()
window.mainloop()
