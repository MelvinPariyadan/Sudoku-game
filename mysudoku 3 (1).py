from sudoku import Sudoku
from tkinter import *
from tkinter import filedialog as reader
import random

# IMPORTANT: press Return after entering value into sudoku for the event to be handled

#when loadfile or clear input is pressed 
# On console invalid command name "2611699664704counter"
#                         while executing ("after" script)

# But this is harmless as for functionality 

font = ("times bold",12)

def start():
    
    root = Tk() 
    root.title("Play Sudoku")
    root.geometry("300x350+580+300")
    
    label_generate = Label(root,text ="Generate a new puzzle", font =("times bold",12))
    label_generate.grid(row=0,column=0,columnspan = 2,padx = 20,pady=20)
    
    label_difficulty = Label(root,text = "Difficulty: ")
    label_difficulty.grid(row = 1,column = 0)
    
    label_or = Label(root,text = "or",font =("times bold",10))
    label_or.grid(row = 3,column = 0,pady = 3,columnspan = 2)
    
    scale_widget = Scale(root, from_=1, to = 5, orient = HORIZONTAL)
    scale_widget.grid(row = 1, column = 1)
    
    
    
    start = Button(
        root,
        text = "Generate and Play",
        width = 20,
        font =("times bold",9),
        command = lambda: [root.after(0,root.destroy),set_board(scale_widget.get())]  
    )
    
    start.grid(row=2,column=0,padx = 80,pady = (30,10),ipady= 10,columnspan = 2)
    

    
    
    load = Button(
        root,
        text = "Load puzzle from a text file",
        width = 20,
        font =("times bold",9),
        command = lambda: load_file(root)
    )
    
    load.grid(row=4,column=0,padx = 80,pady = 10,ipady= 10,columnspan = 2)
    
    
    
    root.mainloop()






def set_board(level = 0, sudoku_list = [], random_number = random.randint(1, 100), root1 = None, root2 = None, root3 = None):
   
    if (root2 !=None and root3 != None):
        root2.destroy()
        root3.destroy()
   
    try:    
        # This method was called by pressing Play
        if(level != 0):
            
            if (level == 5):
                level = level - 0.5
            
            #Sudoku engine takes in levels from [0.0 - 1.0[
            level = level/5
            
            board = Sudoku(3,seed = random_number).difficulty(level)    
        
        # This method was called by pressing load
        else:
            board = Sudoku(3,3,board = sudoku_list)
        
        sudoku = board.board
        solution = board.solve(raising = True).board
        

        sudoku_ui(sudoku,solution,root1,level)
    
    except:
        print("Text File is an invalid Sudoku")
    
  
        



def load_file(root,root_dialog = None):
    if root_dialog != None:
        root_dialog.destroy()
    
    #If user cancels the pop up to select folder. File defaults to ""
    file = reader.askopenfilename()

    mylist = []
    try:
        with open(file,"r") as f:      
            
            temp_1 = f.readlines()
            for rows in temp_1:
                rows = ",".join(rows.strip())
                rows = rows.split(",")
                temp_list = []
                for chars in rows:
                        temp_list.append(int(chars))
    
                mylist.append(temp_list)
        

        set_board(0,mylist,root1 = root)


    except:
        print("Load failed")



def sudoku_ui(sudoku,solution,root,level):
    if(root != None):
        root.destroy()
    if(level == 0 or level == "File loaded"): # In my implementation Clear input calls sudoku_ui
        level = "File loaded"
    elif(level == 0.9):
        level = 5

    else:
        level = int(level*5)
    
    sudoku_root = Tk()
    sudoku_root.title("Play Sudoku")
    sudoku_root.geometry("730x630+430+75")
    sudoku_root.resizable(False,False)
    
    frame = Frame(sudoku_root,bg = "#0617B1",bd = 3)
    frame.grid(row = 2, column = 0,columnspan = 10, padx=50)
    
    current_state = list() # 2D matrix of 2 tuples where tuble will be(Entry object or entered value,solution)

    for i in range(9):
       
        pad_horizontal = (0,0)  #Doing padding manipulation to make frame background look like sudoku borders.
        if (i ==2 or i==5):
            pad_horizontal = (0,3)
        
        current_row = list()
        for j in range(9):
            
            pad_vertical = (0,0)
            if ( j ==2 or j ==5):
                pad_vertical = (0,3)
            
            if sudoku[i][j] != None:
                textbox = Entry(frame,width = 7, bg ="#D3D3D3",font = font,justify = CENTER )
                textbox.grid(row = i, column = j,ipady = 13,padx=pad_vertical,pady = pad_horizontal)
                textbox.insert(END,sudoku[i][j])
                textbox.configure(state='disabled',disabledforeground="#000000")
                current_row.append((sudoku[i][j],(solution[i][j])))
                
                
            else:
                textbox = Entry(frame,width = 7, font = font,justify = CENTER)
                textbox.grid(row = i, column = j,ipady = 13,padx=pad_vertical,pady =pad_horizontal)
                current_row.append((textbox,solution[i][j]))
                textbox.bind("<Return>", lambda x: handle() )
                

        current_state.append(current_row)
    
    
    
    
    def handle():
        try:
            
            count = 0
            indexcount = 0 
            for row in current_state:
                for item in row:
                    
                    if (not isinstance(item[0],int)):
                        value = item[0].get()
                        
                        if(value != ""):
                            value = int(value) # try except later
                            
                            if(value == item[1]):
                                item[0].configure(state = "disabled",disabledbackground = "#C8FED2", disabledforeground="black")
                                item = (value,item[1])
                                x = int(indexcount / 9)
                                y = int(indexcount % 9)
                                current_state[x][y] = item
                                
                            else:
                                item[0].configure(bg = "#FFBDB3")
                                
      
                    
                    if(item[0] == item[1]):
                        count = count + 1 # Later we can check if this is 81
                    indexcount += 1
                                                
            
    
            if(count == 81):
                winner = Tk()
                winner.title("Winner")
                winner.geometry("400x400+430+75")
                
                
                label_generate = Label(winner,text ="Congratulations!!! That was amazing", font =("times bold",12))
                label_generate.pack()
                        
        except:
            print("Invalid input")
    

    font2 = ("times bold",8)  
      
    label_difficulty_text = Label(sudoku_root,text = f"You are now playing Sudoku level: {level}", font = font2)
    label_difficulty_text.grid(row = 0, column = 0,columnspan = 5,padx = 5,pady = 10)
    

    label_time = Label(sudoku_root, font = font2)
    label_time.grid(row = 0, column = 7,columnspan = 5,padx = 2, pady = 10)
    counter(0,label_time,sudoku_root)
    
    

    
    button_hint = Button(
        sudoku_root,
        text = "Get Hint",
        command = lambda: get_hint(current_state,sudoku_root)
    )
    button_hint.grid(row=1,column=0,padx = (90,5),pady = (3,30),ipadx = 10,ipady = 10)
    
    button_solution = Button(
        sudoku_root,
        text = "Show solution",
        command = lambda : show_solution(current_state,sudoku_root)#.........................
    )
    button_solution.grid(row=1,column=1,padx = 5,pady = (3,30),ipadx = 10,ipady = 10)
    

    
    button_load = Button(
        sudoku_root,
        text = "Load from file",
        command = lambda: load_file_dialogbox(sudoku_root)
    )
    button_load.grid(row=1,column=2,padx = 5,pady = (3,30),ipadx = 10,ipady = 10)

    
    button_generate = Button(
                             sudoku_root,
                             text = "Generate new",
                             command = lambda: generate_new(sudoku_root)
                        )
    button_generate.grid(row=1,column=3,padx = 5,pady = (3,30),ipadx = 10,ipady = 10)
    
    
    
    button_clear = Button(
        sudoku_root,
        text = "Clear Input",
        command = lambda : clear_input(sudoku,solution,sudoku_root,level)
    )
    button_clear.grid(row=1,column=4,padx = 5,pady = (3,30),ipadx = 10,ipady = 10)
    
    sudoku_root.mainloop()
    

def generate_new(source):
        
    root = Tk()
    root.title("Play Sudoku")
    root.geometry("300x350+580+300")
    
     
    label_generate = Label(root,text ="Are you sure you want a new Board? ",font =("times bold",11))
    label_generate.grid(row=0,column=0,padx = 18,pady = (25,0))
    
    label_generate2 = Label(root,text ="Set your difficulty ",font =("times bold",11))
    label_generate2.grid(row=1,column=0,padx = 18,pady = (25,0))
    
    scale = Scale(root, from_=1, to = 5, orient = HORIZONTAL)
    scale.grid(row = 2, column = 0)
    
    
    
    button_generate = Button(root,
                             text = "Generate and Play",
                             width = 20,
                             command = lambda: set_board(scale.get(),root2 = root,root3 = source)
                            )
    button_generate.grid(row =3, column = 0,ipady= 10,pady = (20,40))
    
    root.mainloop()





    
def clear_input(sudoku,solution,sudoku_root,level):
    root = Tk()
    root.title("Play Sudoku")
    root.geometry("300x350+580+300")

    label_clear = Label(root,text ="Are you sure you want to clear Inputs?",font =("times bold",11))
    label_clear.grid(row=0,column=0,padx = 25,pady = (25,0))
    if (not str(level).isdigit()):
        level = "File loaded"
    else:
        level = level /5
    
    clear_button = Button(
        root,
        text = "Yes, Clear inputs",
        width = 20,
        command = lambda: [sudoku_root.destroy(),root.destroy(),sudoku_ui(sudoku,solution,None,level)]
    )
    clear_button.grid(row = 1, column = 0,ipady= 10,pady = 40)
    
    root.mainloop()

def show_solution(mylist,sudoku_root):
    
    root = Tk()
    root.title("Play Sudoku")
    root.geometry("300x350+580+300")
    

    label_generate = Label(root,text ="Are you sure you want to see the solution? ",font =("times bold",11))
    label_generate.grid(row=0,column=0,padx = 18,pady = (25,0))

    
    button_solution = Button(
        root,
        text = "Show solution",
        width = 20,
        command = lambda: [root.after(0,root.destroy),show_solution_2(mylist,sudoku_root)]  
    )
    button_solution.grid(row = 1, column = 0,ipady= 10,pady = 40)
    
    root.mainloop()
      
def show_solution_2(mylist,myrooot):
    for i in range (81): # Call get hint 81 times. In get hint if count = 81 that is solution = board -> then "Won"
        get_hint(mylist,myrooot)

def load_file_dialogbox(source):
    
    root = Tk()
    root.title("Play Sudoku")
    root.geometry("300x350+580+300")

    label_generate = Label(root,text ="Are you sure you want to load a new board? ",font =("times bold",11))
    label_generate.grid(row=0,column=0,padx = 12,pady = (25,0))
    
      
    
    button_load = Button(
        root,
        text = "Load puzzle from a text file",
        command = lambda: [load_file(source,root)] # destroys the original sudoku if sudoku_ui is called, and dialogbox
    )
    button_load.grid(row = 1, column = 0,ipady= 10,pady = (20,40))
    
    
    root.mainloop()
    

           
def counter(seconds,mylabel,myroot):
     
        x = str(seconds%60)
        if int(x) < 10: x = "0"+str(seconds%60)
        y = str(seconds // 60)
        if int(y) < 10: y = "0"+str(y)
        z = str(int(y) // 60)
        if int(z) < 10: z = "0"+str(z)
            
        time = z +":"+y+":"+x
        mylabel.config({"text": "Timer: " + time})
        myroot.after(1000, counter,seconds+1,mylabel,myroot)

def get_hint(current_list, myroot,myboolean = False):
    # Creating a list of empty textboxes with "ij" items
    
    try:
        
        count = 0
        mylist = [] 
        for i in range(9):
            for j in range(9):
                if not isinstance(current_list[i][j][0], int): # if its an Entry object
                    x = str(i)+str(j)
                    mylist.append(x)
                    
                  
        myhint = random.choice(mylist)
        
        x = int(myhint[0])
        y = int(myhint[1])
        
        item = (current_list[x][y][1],current_list[x][y][1])
        current_list[x][y][0].insert(END,current_list[x][y][1])
        current_list[x][y][0].configure(state='disabled',disabledforeground="#FC360C",disabledbackground = "#FEF9F8")
        
        current_list[x][y] = item
        
        for i in range(9):
            for j in range(9):
                  if(current_list[i][j][0] == current_list[i][j][1]):
                        count = count + 1 # Later we can check if this is 81
        
        
        if (count == 81):
            winner = Tk()
            winner.title("Winner")
            winner.geometry("400x400+430+75")
            
            
            label_generate = Label(winner,text ="Congratulations!!! That was amazing", font =("times bold",12))
            label_generate.pack()
    except:
         pass


start()
