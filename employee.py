import tkinter 
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import pymysql
import datetime
import time

root = Tk()
class WindowDraggable():
    def __init__(self, label):
        self.label = label
        label.bind("<ButtonPress-1>", self.StartMove)
        label.bind("<B1-Motion>", self.OnMotion)

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def OnMotion(self, event):
        x = (event.x_root - self.x - self.label.winfo_rootx() +
                self.label.winfo_rootx())
        y = (event.y_root - self.y - self.label.winfo_rooty() +
                self.label.winfo_rooty())
        root.geometry("+%s+%s" % (x, y))
    
column_title = ("EMPLOYEE_ID", "EMPLOYEE_NAME", "EMPLOYEE_BOD",
            "EMPLOYEE_ADDRESS", "EMPLOYEE_PHONE")

class employee:
    def __init__(self, parent):
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOWS", self.out)
        width = 650
        height = 500
        halfWidth = (self.parent.winfo_screenwidth() - width) // 2
        halfHeigth = (self.parent.winfo_screenheight() - height) // 2
        self.parent.overrideredirect(1)
        self.confComponent()
        self.auto()

    def out(self, event = None):
        self.parent.destroy()

    def OnDoubleClick(self, event):
        self.entCode.config(state = "normal")
        self.entCode.delete(0, END)
        self.entName.delete(0, END)
        self.entDay.delete(0, END)
        self.entAddress.delete('1.0', 'end')
        self.entPhone.delete(0, END)

        it = self.trvTabel.selection()[0]
        ck = str(self.trvTabel.item(it, "values"))[2:6]
        self.entCode.insert(END, ck)
        cKode = self.entCode.get()
        
        con = pymysql.connect(db = "EMPLOYEE_MANAGEMENT", user="root",
                passwd="root", host="localhost", port="3306", autocommit = True)
        cur = con.cursor()
        sql = "SELECT EMPLOYEE_NAME, EMPLOYEE_BOD, EMPLOYEE_ADDRESS, EMPLOYEE_PHONE FROM EMPLOYEE WHERE EMPLOYEE_ID = %s"
        cur.execute(sql, cKode)
        data = cur.fetchone()
        
        self.entName.insert(END, data[0])
        self.entDay.insert(END, data[1])
        cBod = self.entDay.get()
        
        splitYear = str(cBod[0] + cBod[1] + cBod[2] + cBod[3])
        splitMonth = str(cBod[5] + cBod[6])
        splitDay = str(cBod[8], cBod[9])
        
        self.entDay.delete(0, END)
        self.entMonth.delete(0, END)
        self.entYear.delete(0, END)
        
        self.entDay.insert(END, splitDay)
        self.entMonth.insert(END, splitMonth)
        self.entYear.insert(END, splitYear)
        
        self.entAddress.insert(END, data[2])
        self.entPhone.insert(END, data[3])
        
        self.entCode.config(state = "disable")
        self.btnSave.config(state = "disable")
        
        self.btnUpdate.config(state = "normal")
        self.btnDelete.config(state = "normal")
    
    def confComponent(self):
        frameWin = Frame(self.parent, bg = "#666")
        frameWin.pack(fill = X, side = TOP) 
        
        WindowDraggable(frameWin)
        
        Label(frameWin, text = "EMPLOYEE", bg = "#666", fg = "white").pack(side=LEFT,
                padx = 20)
        
        buttonx = Button(frameWin, text = "X", fg = "white", bg = "#FA8072",
                width = 6, height = 2, bd = 0, activebackground = "#FB8072",
                activeforeground = "white", command = self.onClose, relief = FLAT)
        buttonx.pack(side = RIGHT)

        mainframe = Frame(self.parent)
        mainframe.pack(side = TOP, fill = X)
        btnFrame = Frame(self.parent)
        btnFrame.pack(side = TOP, fill = X)
        tableFrame = Frame(self.parent)
        tableFrame.pack(expand = YES, side = TOP, fill = Y)
        
        Label(mainframe, text = " ").grid(row = 0, column = 0)
        Label(mainframe, text = " ").grid(row = 1, column = 0)
        
        # Component ID
        Label(mainframe, text = "EMPLOYEE ID").grid(row = 1, column = 0,
                sticky = W, padx = 20)
        Label(mainframe, text = ":").grid(row = 1, column = 1, sticky = W,
                pady = 5, padx = 10)
        self.entCode = Entry(mainframe, width = 20)
        self.entCode.grid(row = 1, column = 2, sticky = W)

        # Component Name
        Label(mainframe, text = "EMPLOYEE NAME").grid(row = 2, column = 0,
                sticky = W, padx = 20)
        Label(mainframe, text = ":").grid(row = 2, column = 1, sticky = W,
                pady = 5, padx = 10)
        self.entName = Entry(mainframe, width = 30)
        self.entName.grid(row = 2, column = 2, sticky = W)

        # Component Birth of Date
        Label(mainframe, text = "EMPLOYEE BOD").grid(row = 3, column = 0,
                sticky = W, padx = 20)
        Label(mainframe, text = ":").grid(row = 3, column = 1, sticky = W,
                pady = 5, padx = 10)
        Dt = Frame(mainframe)
        Dt.grid(row = 3, column = 2, sticky = W)

        # Component Day
        self.entDay = Entry(Dt, width = 5)
        self.entDay.grid(row = 1, column = 0, sticky = W)

        # Component Month  
        self.entMonth = Entry(Dt, width = 5)
        self.entMonth.grid(row = 1, column = 1, stick = W, padx = 2)
        
        # Component Year
        self.entYear = Entry(Dt, width = 5)
        self.entYear.grid(row = 1, column = 2, stick = W, padx = 2)

        Label(Dt, text = "(dd/mm/yyyy)").grid(row = 1, column = 3, sticky = E, padx = 5)

        # Component Address
        Label(mainframe, text = "EMPLOYEE ADDRESS").grid(row = 4, column = 0,
                sticky = NW, padx = 20)
        Label(mainframe, text = ":").grid(row = 4, column = 1, sticky = NW, 
                padx = 10, pady = 6)
        self.entAddress = ScrolledText(mainframe, height = 4, width = 35)
        self.entAddress.grid(row = 4, column = 2, sticky = W)
        
        # Component Phone Number
        Label(mainframe, text = "EMPLOYEE PHONE").grid(row = 5, column = 0,
                sticky = W, padx = 20)
        Label(mainframe, text = ":").grid(row = 5, column = 1, sticky = W,
                pady = 5, padx = 10)
        self.entPhone = Entry(mainframe, width = 20)
        self.entPhone.grid(row = 5, column = 2, sticky = W)

        # Component Save
        self.btnSave = Button(btnFrame, text = 'Save', command = self.onSave,
                width = 10, relief = FLAT, bd = 2, bg = "#666", fg = "white",
                activebackground = "#444", activeforeground = "white")
        self.btnSave.grid(row = 0, column = 1, padx = 5)

        # Component Update
        self.btnUpdate = Button(btnFrame, text = "Update", command = self.onUpdate,
                state = "disable", width = 10, relief = FLAT, bd = 2, bg = "#666",
                fg = "white", activebackground = "#444", activeforeground = "white")
        self.btnUpdate.grid(row = 0, column = 2, pady = 10, padx = 5)

        # Component Clear
        self.btnClear = Button(btnFrame, text = "Clear", command = self.onClear,
                width = 10, relief = FLAT, bd = 2, bg = "#666", fg = "white",
                activebackground = "#444", activeforeground = "white")
        self.btnClear.grid(row = 0, column = 3, pady = 10, padx = 5)

        # Component Delete
        self.btnDelete = Button(btnFrame, text = "Delete", command = self.onDelete,
                state = "disable", width = 10, relief = FLAT, bd = 2, 
                bg = "#FC6042", fg = "white", activebackground = "#444", 
                activeforeground = "white")
        self.btnDelete.grid(row = 0, column = 4, pady = 10, padx = 5)

        # Component table
        self.fr_data = Frame(tableFrame, bd = 10)
        self.fr_data.pack(fill = BOTH, expand = YES) 

        self.trvTabel = ttk.Treeview(self.fr_data, columns = column_title,
                show = 'headings')
        self.trvTabel.bind('<Double-1>', self.OnDoubleClick)

        sbVer = Scrollbar(self.fr_data, orient = 'vertical', 
                command = self.trvTabel.yview)
        sbVer.pack(side = RIGHT, fill = Y)
        self.trvTabel.pack(side = TOP, fill = BOTH)
        self.trvTabel.configure(yscrollcommand = sbVer.set)
        self.table()

    def table(self):
        con = pymysql.connect(db = "EMPLOYEE_MANAGEMENT", user = "root",
                password = "root", host = "localhost", port = 3306,
                autocommit = True)
        cur = con.cursor()
        cur.execute("SELECT * FROM EMPLOYEE")
        data_table = cur.fetchall()
        
        for column in column_title:
            self.trvTabel.heading(column, text = column)
            self.trvTabel.column("EMPLOYEE_ID", width = 110, anchor="w")
            self.trvTabel.column("EMPLOYEE_NAME", width = 120, anchor = "w")
            self.trvTabel.column("EMPLOYEE_BOD", width = 100, anchor = "w")
            self.trvTabel.column("EMPLOYEE_ADDRESS", width = 160, anchor = "w")
            self.trvTabel.column("EMPLOYEE_PHONE", width = 120, anchor = "w")
            i = 0
            for dat in data_table:
                if(i % 2):
                    row = "Even"
                else:
                    row = "Odd"

                self.trvTabel.insert('', 'end', values = dat, tags = row)
                i += 1

            self.trvTabel.tag_configure("Odd", background = "#FFFFFF")
            self.trvTabel.tag_configure("Even", background = "whitesmoke")
        cur.close()
        con.close()

    def auto(self):
        con = pymysql.connect(db = "EMPLOYEE_MANAGEMENT", user = "root",
                password = "root", host = 'localhost', port = 3306, 
                autocommit = True)
        cur = con.cursor()
        cuv = con.cursor()
        sqlquery = "SELECT MAX(EMP_ID) FROM EMPLOYEE"
        sql = "SELECT EMP_ID FROM EMPLOYEE"
        cur.execute(sqlquery)
        cuv.execute(sql)
        maxcode = cur.fetchone()
        if cuv.rowcount > 0:
            autohit = int(maxcode[0]) + 1
            hits = "000" + str(autohit)
            if(len(hits)) == 4:
                self.entCode.insert(0, hits)
                self.entName.focus_set()
            elif(len(hits)) == 5:
                hit = "00" + str(autohit)
                self.entCode.insert(0, hit)
                self.entName.focus_set()
            elif(len(hits)) == 6:
                hit = "0" + str(autohit)
                self.entCode.insert(0, hit)
                self.entName.focus_set()
            elif(len(hits)) == 7:
                hit = "" + str(autohit)
                self.entCode.insert(0, hit)
                self.entName.focus_set()
            else:
                messagebox.showwarning(title = "Warning!", 
                        message = " 4 digit only!!")
        else:
            hit = "0001"
            self.entCode.insert(0, hit)
            self.entName.focus_set()

        self.entCode.config(state = "readonly")

    def onClose(self, event = None):
        self.parent.destroy()
    def onDelete(self):
        con = pymysql.connect(db = "EMPLOYEE_MANAGEMENT", user = "root",
                password = "root", host = "localhost", port = 3306, 
                autocommit = True)
        cur = con.cursor()
        self.entCode.config(state = "normal")
        cKode = self.entCode.get()
        sql = "DELETE FROM EPLOYEE WHERE EMPLOYEE_ID = %s"
        cur.execute(sql)
        self.onClear()
        messagebox = showinfo(title = "Information!", 
                message = "Data has been deleted!")
        cur.close()
        con.close()

    def onClear(self):
        self.btnSave.config(state = "normal")
        self.btnUpdate.config(state = "disable")
        self.btnDelete.config(state = "disable")
        self.entCode.config(state = "normal")
        self.entCode.delete(0, END)
        self.entName.delete(0, END)
        self.entDay.delete(0, END)
        self.entMonth.delete(0, END)
        self.entYear.delete(0, END)
        self.entAddress.delete("1.0", "end")
        self.entPhone.delete(0, END)

        self.trvTabel.delete(*self.trvTabel.get_children())
        self.fr_data.after(0, self.table())
        self.auto()
        self.entName.focus_set()

    def onSave(self):
        con = pymysql.connect(db = "EMPLOYEE_MANAGEMENT", user = "root",
                password = "root", host = "localhost", port = 3306,
                autocommit = True)
        cKode = self.entCode.get()
        cName = self.entName.get()
        cDay = self.entDay.get()
        cMonth = self.entMonth.get()
        cYear = self.entYear.get()
        dBoD = datetime.date(int(cYear), int(cMonth), int(cDay))
        cAddress = self.entAddress.get('1.0', 'end')
        cPhone = self.entPhone.get()
        
        if(len(cDay) == 0 and len(cMonth) == 0 and len(cYear) == 0):
            messagebox.showwarning(title = "Warning!!", 
                    message = "Birth of Date may not be empty!!")
        else:
            cur = con.cursor()
            sql = "INSERT INTO EMPLOYEE (EMPLOYEE_ID, EMPLOYEE_NAME, EMPLOYEE_BOD, EMPLOYEE_ADDRESS, EMPLOYEE_PHONE)" + "VALUES (%s, %s, %s, %s, %s)"
            cur.execute(sql, cKode, cName, cBod, cAddress,cPhone)
            self.onClear()
            messagebox.showinfo(title = "Information!!", 
                    message = "Your information already saved!")
            cur.close()
            con.close()

    def onUpdate(self):
        cKode = self.entKode.get()
        if len(cKode) == 0:
            messagebox.showwarning(title = "Warning!", 
                    message = "Your Code is empty.")
            self.entCode.focus_set()
        else:
            con = pymysql.connect(db = "EMPLOYEE_MANAGEMENT", user = "root",
                    password = "root", host = "localhost", port = 3306, 
                    autocommit = True)
            cur = con.cursor()
            cKode = self.entCode.get()
            cName = self.entName.get()
            cDay = self.entDay.get()
            cMonth = self.entMonth.get()
            cYear = self.entYear.get()
            dBoD = datetime.date(int(cYear), int(cMonth), int(cDay))
            cAddress = self.entAddress.get("1.0", "end")
            cPhone = self.entPhone.get()
            sql = "UPDATE EMPLOYEE SET EMPLOYEE_NAME = %s, EMPLOYEE_BOD = %s, EMPLOYEE_ADDRESS = %s, EMPLOYEE_PHONE = %s WHERE EMPLOYEE_ID = %s"
            cur.execute(sql, (cName, dBoD, cAddress, cPhone, cKode))
            self.onClear()
            messagebox.showinfo(title = "Information!", 
                    message = "Your data has been updated!!")
            cur.close()
            con.close()

def main():
    employee(root)
    root.mainloop()

main()
