from tkinter import *             # This has all the code for GUIs.


import psycopg2

db=psycopg2.connect(host='localhost',user='postgres',password='datab427869',database='postgres')

c=db.cursor()

def center_window_on_screen():

    x_cord = int((screen_width/2) - (width/2))
    y_cord = int((screen_height/2) - (height/2))
    root.geometry("{}x{}+{}+{}".format(width, height, x_cord, y_cord))





root = Tk()
root.title("Kino")




width, height = 500, 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_window_on_screen()


class Start(): 
    
    def __init__(self,master): 
        
        self.start_frame= Frame(master)
        

        self.start_frame.pack()
        

        self.lbl_heading_start = Label(self.start_frame,text='Welcome to the cinema')
        self.lbl_heading_start.pack()
        self.lbl_login_start_use=Label(self.start_frame,text='Browse movies and Seances').pack()
        self.seans_btn_start=Button(self.start_frame,text='Browse',command=self.switch_to_seanse)
        
        self.seans_btn_start.pack()
        
        self.lbl_start_view=Label(self.start_frame,text='Check reservation status').pack()
        self.btn_start_view=Button(self.start_frame,text='Check',command=self.switch_to_check).pack()

        self.lbl_login_start_log=Label(self.start_frame,text='Login for staff').pack()
        self.login_btn_start=Button(self.start_frame,text='Login',command=self.switch_to_login)
        self.login_btn_start.pack()

    def switch_to_check(self):
        self.start_frame.forget()
        Check(root)
        
    

    def switch_to_login(self):
        
        self.start_frame.forget()
        Login(root)
    def switch_to_seanse(self):
        self.start_frame.forget()
        Seanse(root)

class Check():
    def __init__(self,master):
        self.check_frame=Frame(master)
        self.check_frame.pack()

        self.lbl_check=Label(self.check_frame,text='Enter your reservation number').grid(row=0,column=0,columnspan=2)
        self.e_check=Entry(self.check_frame)
        self.e_check.grid(row=1,column=0)
        self.btn_check=Button(self.check_frame,text='OK',command=self.check).grid(row=1,column=1)
        self.btn_back=Button(self.check_frame,text='<- Back',command= self.back_to_start).grid(row=100)
#these labels are defined here but used in another function (check)
        #I have no idea why but apparently if a widget is defined inside a function
        #then it cannot be removed with .grid_forget().
        #tkinter is a bit buggy

        self.lbl_check_acc=Label(self.check_frame,text='Your reservation has been accepted')
        self.lbl_check_table=Label(self.check_frame,text='ID   Seats taken    Movie title     Date and time    Room nr.')
        self.lbl_check_pen=Label(self.check_frame,text='Your reservation is pending acceptance')
        self.lbl_check_declined=Label(self.check_frame,text='Your reservation has been declined or it never existed.')
    def check(self):
        id=int(self.e_check.get())
        
        
        
        


        
        c.execute("select id_rezerwacji, zajmowane_miejsca, sea_film, godzina_rozpoczecia, sea_sala  from rezerwacje join seanse on rez_seans=id_seansu where id_rezerwacji='{}'".format(id))
        res=c.fetchall()
        c.execute("select id_ocz_rezerwacji, zajmowane_miejsca, sea_film, godzina_rozpoczecia, sea_sala  from ocz_rezerwacje join seanse on rez_seans=id_seansu where id_ocz_rezerwacji='{}'".format(id))
        ocz_res=c.fetchall()
        
        if res!=[] and ocz_res==[]:
            self.lbl_check_declined.grid_forget()
            self.lbl_check_acc.grid(row=2,column=1,columnspan=3)
            self.lbl_check_table.grid(row=3,column=0,columnspan=4)
            self.lbl_check_show=Label(self.check_frame,text=f'{res[0][0]}    {res[0][1]}     {res[0][2]}    {res[0][3]}     {res[0][4]}')
            self.lbl_check_show.grid(row=4,column=0,columnspan=5)
            
        elif res==[] and ocz_res!=[]:
            self.lbl_check_declined.grid_forget()
            self.lbl_check_pen.grid(row=2,column=1,columnspan=3)
            self.lbl_check_table.grid(row=3,column=0,columnspan=4)
            self.lbl_check_show=Label(self.check_frame,text=f'{res[0][0]}    {res[0][1]}     {res[0][2]}    {res[0][3]}     {res[0][4]}')
            self.lbl_check_show.grid(row=4,column=0,columnspan=5)
        elif res==[] and ocz_res==[]:
            self.lbl_check_show.grid_forget()
            self.lbl_check_pen.grid_forget()
            self.lbl_check_acc.grid_forget()
            
            self.lbl_check_table.grid_forget()
            self.lbl_check_declined.grid(row=2,columnspan=5)
            
    def back_to_start(self):
        self.check_frame.destroy()
        Start(root)
            

class Login():
    def __init__(self,master):
        self.login_frame=Frame(master)
        self.login_frame.pack()

        self.lbl_login_id=Label(self.login_frame,text='Id:').pack()
        self.e_login_id=Entry(self.login_frame)
        self.e_login_id.pack()
        self.lbl_login_pswd=Label(self.login_frame,text='Password:').pack()
        self.e_login_pswd=Entry(self.login_frame)
        self.e_login_pswd.pack()
        self.btn_login_enter=Button(self.login_frame,text='OK',command=self.login).pack()
        self.btn_login_back=Button(self.login_frame,text='Back to start',command=self.back_to_start).pack()
        self.lbl_login_tip=Label(self.login_frame,text='psst.. you can just leave it empty and press "OK" ').pack()
    def back_to_start(self):
        self.login_frame.forget()
        Start(root)
        
    def login(self):
        global c
        id=self.e_login_id.get()
        pswd=self.e_login_pswd.get()
        c.execute("SELECT id_pracownika,haslo FROM pracownicy")
        data=c.fetchall()
        for person in data:

            if id==person[0] and  pswd==person[1]:
                self.login_frame.forget()
                Admin(root)
        if (id=='' and pswd==''):
                self.login_frame.forget()
                Admin(root)
        if id not in  data[:][0]:
            lbl_login_err=Label(self.login_frame,text='Wrong login').pack()
        if pswd not in  data[:][1]:
            lbl_login_err1=Label(self.login_frame,text='Wrong password').pack()




class Admin():
    def __init__(self,master):
        self.admin_frame=Frame(master)
        self.admin_frame.pack()

        self.lbl_admin=Label(self.admin_frame,text='Select an option:').pack()
        self.btn_admin_accept_req=Button(self.admin_frame,text='Review orders',command=self.switch_to_accept).pack()
        self.btn_admin_add_seans=Button(self.admin_frame,text='Add Seances',command=self.switch_to_add_seans).pack()
        self.btn_admin_add_movie=Button(self.admin_frame,text='Add Movies',command=self.switch_to_add_movie).pack()
        self.btn_admin_add_admin=Button(self.admin_frame,text='Add staff members',command=self.switch_to_add_admin).pack()
        self.btn_admin_res=Button(self.admin_frame,text='See reservations',command=self.switch_to_res).pack()
        self.btn_admin_back=Button(self.admin_frame,text='<- Back',command=self.back_to_login).pack()
    def switch_to_accept(self):
        self.admin_frame.forget()
        Accept(root)
    def switch_to_add_seans(self):
        self.admin_frame.forget()
        Add_seanse(root)
    def switch_to_add_movie(self):
        self.admin_frame.forget()
        Add_movie(root)
    def switch_to_add_admin(self):
        self.admin_frame.forget()
        Add_admin(root)
    def switch_to_res(self):
        self.admin_frame.forget()
        Reservations(root)
    def back_to_login(self):
        self.admin_frame.forget()
        Login(root)

class Reservations():
    def __init__(self,master):
        self.res_frame=Frame(master)
        self.res_frame.pack()
        Label(self.res_frame,text='ID   Seats taken    Movie title     Date and time    Room nr.').pack()
        c.execute("select id_rezerwacji, zajmowane_miejsca, sea_film, godzina_rozpoczecia, sea_sala from rezerwacje join seanse on rez_seans=id_seansu")
        for i in c.fetchall():
            Label(self.res_frame,text=i).pack()


class Accept():
    
    def __init__(self,master):
        self.accept_frame=Frame(master)
        self.accept_frame.pack()
        self.lbl_accept=Label(self.accept_frame,text='Accepting orders').grid(row=0,column=0,columnspan=4)
        self.lbl_accept_desc_id=Label(self.accept_frame,text='Id:').grid(row=1,column=0)
        self.lbl_accept_desc_id=Label(self.accept_frame,text='Seance id:').grid(row=1,column=1)
        self.lbl_accept_desc_id=Label(self.accept_frame,text='Ordered seats:').grid(row=1,column=2)
        self.lbl_accept_desc_id=Label(self.accept_frame,text='Free seats:').grid(row=1,column=3)

        c.execute("select * from ocz_rezerwacje")
        pending=c.fetchall()

        #i need to name my buttons, but exec() doesnt allow the 'lambda res=res' trick.
        #button dictionary sounds weird but works
        self.button_dict_ac={}
        self.button_dict_dec={}
        for res in pending:
            self.button_dict_ac[f'btn_accept{res[0]}']=Button(self.accept_frame,text='Accept',command=lambda res=res: self.accept(res))
            self.button_dict_dec[f'btn_decline{res[0]}']=Button(self.accept_frame,text='Decline',command=lambda res=res: self.decline(res))

        count=2
        for res in pending:
            exec(f'self.lbl_accept_p_id{res[0]}=Label(self.accept_frame,text={res[0]})')
            exec(f'self.lbl_accept_p_id{res[0]}.grid(row=count,column=0)')

            exec(f'self.lbl_accept_p_seats{res[0]}=Label(self.accept_frame,text={res[1]})')
            exec(f'self.lbl_accept_p_seats{res[0]}.grid(row=count,column=2)')

            exec(f'self.lbl_accept_p_idsea{res[0]}=Label(self.accept_frame,text={res[2]})')
            exec(f'self.lbl_accept_p_idsea{res[0]}.grid(row=count,column=1)')

            c.execute(f'select sprawdz_miejsca({res[2]})')
            self.seats=c.fetchall()
            
            if self.seats[0][0]==None:
                c.execute(f"select liczba_miejsc from sale join Seanse on numer_sali=sea_sala where id_seansu={res[2]}")
                exec(f'self.free_seats_{res[0]}=c.fetchall()')
            else:
                exec(f'self.free_seats_{res[0]}=self.seats')

            exec(f'self.lbl_accept_free_seats{res[0]}=Label(self.accept_frame,text=self.free_seats_{res[0]})')
            exec(f'self.lbl_accept_free_seats{res[0]}.grid(row=count,column=3)')

            

            #using the button dicitonary

            self.button_dict_ac[f'btn_accept{res[0]}'].grid(row=count,column=4)
            self.button_dict_dec[f'btn_decline{res[0]}'].grid(row=count,column=5)
            

            count+=1
        self.btn_accept_back=Button(self.accept_frame,text='<- Back',command=self.back_to_admin).grid(row=count,column=0)
    def accept(self,res):
        
        
        c.execute(f"insert into rezerwacje values ('{res[0]}','{res[1]}','{res[2]}')")
        #ideally we would want to delete a reviewed order from 'awaiting orders' table, but that adds free seats in the Seanse section,
        #which is not a good thing
        
        c.execute(f"delete from ocz_rezerwacje where id_ocz_rezerwacji='{res[0]}'")
        
        
        
        #reloading to update seats taken
        self.accept_frame.destroy()
        Accept(root)

    def decline(self,res):
        c.execute(f"delete from ocz_rezerwacje where id_ocz_rezerwacji='{res[0]}'")
        self.accept_frame.destroy()
        Accept(root)

    
    def back_to_admin(self):
        self.accept_frame.forget()
        Admin(root)

class Add_seanse():
    def __init__(self,master):

        self.add_seanse_frame=Frame(master)
        self.add_seanse_frame.pack()

        self.lbl_add_seans=Label(self.add_seanse_frame,text='Add seances').pack()

        self.lbl_title=Label(self.add_seanse_frame,text='Title').pack()
        self.e_add_title=Entry(self.add_seanse_frame)
        self.e_add_title.pack()

        self.lbl_time=Label(self.add_seanse_frame,text="Date and time (YYYY-MM-DD HH:MM:SS").pack()
        self.e_add_time=Entry(self.add_seanse_frame)
        self.e_add_time.pack()

        self.lbl_room=Label(self.add_seanse_frame,text='Room nr (1-5)').pack()
        self.e_add_room=Entry(self.add_seanse_frame)
        self.e_add_room.pack()

        
        

        self.btn_add=Button(self.add_seanse_frame,text="Add seance",command=self.add).pack()

        

        self.btn_add_seans_back=Button(self.add_seanse_frame,text='<- Back',command=self.back_to_admin).pack()
    def add(self):
        global c
        title=self.e_add_title.get()
        time=self.e_add_time.get()
        room=self.e_add_room.get()
        self.lbl_add_seans_err=Label(self.add_seanse_frame,text='There is no such room')
        self.lbl_add_seans_err.forget()
        rooms=[1,2,3,4,5]

        if (int(room) in rooms):
            
            c.execute("Select add_seans('{a}','{b}','{c}')".format(a=title,b=time,c=room))
            result=c.fetchall()
            self.lbl_succesr=Label(self.add_seanse_frame,text='Seance with id {} has been added'.format(result[0][0])).pack()


        elif (int(room) not in rooms):
            
            self.lbl_add_seans_err.pack()


    def back_to_admin(self):
        self.add_seanse_frame.forget()
        Admin(root)

class Add_movie():
    def __init__(self,master):
        self.add_movie_frame=Frame(master)
        self.add_movie_frame.pack()

        self.lbl_add_movie=Label(self.add_movie_frame,text='Add movie').pack()

        self.lbl_title=Label(self.add_movie_frame,text='Title:').pack()
        self.e_add_title=Entry(self.add_movie_frame)
        self.e_add_title.pack()

        self.lbl_time=Label(self.add_movie_frame,text="Showing time (in minutes):").pack()
        self.e_add_time=Entry(self.add_movie_frame)
        self.e_add_time.pack()

        self.lbl_desc=Label(self.add_movie_frame,text="Description:").pack()
        self.e_add_desc=Entry(self.add_movie_frame)
        self.e_add_desc.pack()

        self.lbl_year=Label(self.add_movie_frame,text="Year of production:").pack()
        self.e_add_year=Entry(self.add_movie_frame)
        self.e_add_year.pack()
        self.btn_add=Button(self.add_movie_frame,text="Add seance",command=self.add).pack()

        

        self.btn_add_seans_back=Button(self.add_movie_frame,text='<- Back',command=self.back_to_admin).pack()

    def add(self):
        title=self.e_add_title.get()
        time=self.e_add_time.get()
        year=self.e_add_year.get()
        description=self.e_add_desc.get()
        
        c.execute("INSERT INTO filmy values ('{a}','{b}','{c}','{d}')".format(a=title,b=time,c=description,d=year))
        # this needs a bit more restrictions i guess
        self.lbl_add_mv_done=Label(self.add_movie_frame,text='Movie {} has been added successfully'.format(title)).pack()
    def back_to_admin(self):
        self.add_movie_frame.forget()
        Admin(root)
      

class Add_admin():
    def __init__(self,master):

        self.add_admin_frame=Frame(master)
        self.add_admin_frame.pack()



        self.lbl_add_admin=Label(self.add_admin_frame,text='Add staff members').pack()
        self.lbl_name=Label(self.add_admin_frame,text='Name:').pack()
        self.e_name=Entry(self.add_admin_frame)
        self.e_name.pack()
        self.lbl_surname=Label(self.add_admin_frame,text='Surname:').pack()
        self.e_surname=Entry(self.add_admin_frame)
        self.e_surname.pack()
        self.lbl_id=Label(self.add_admin_frame,text='New id (6 numbers)').pack()
        self.e_id=Entry(self.add_admin_frame)
        self.e_id.pack()
        self.lbl_pswd=Label(self.add_admin_frame,text='New password').pack()
        self.e_pswd=Entry(self.add_admin_frame)
        self.e_pswd.pack()
        self.btn_add=Button(self.add_admin_frame,text='Add',command=self.add).pack()
        self.lbl_empty=Label(self.add_admin_frame,text=' ').pack()

        self.btn_add_admin_back=Button(self.add_admin_frame,text='<- Back', command=self.back_to_admin).pack()
    def add(self):
        name=self.e_name.get()
        surname=self.e_surname.get()
        id=self.e_id.get()
        pswd=self.e_pswd.get()
        
        c.execute("Insert into pracownicy values ('{a}','{b}','{c}','{d}')".format(a=id,b=pswd,c=name,d=surname))
        self.lbl_succes=Label(self.add_admin_frame,text='Staff member has been added').pack()
    
    def back_to_admin(self):
        self.add_admin_frame.forget()
        Admin(root)

class Seanse():
    def __init__(self,master):

        self.seanse_frame=Frame(master)
        self.seanse_frame.pack()
        
        self.lbl_seanse=Label(self.seanse_frame,text='Available movies:').grid(row=0,column=0,columnspan=2)
        c.execute("select tytul, opis, czas_wyswietlania from filmy")
        self.list=c.fetchall()
     
        count=1
        for i in self.list:
           
            Label(self.seanse_frame,text='{}'.format(i[0])).grid(row=count,column=0)
            Button(self.seanse_frame,text='info',command=lambda i=i: self.show_info(i[0],i[1],i[2])).grid(row=count,column=1)
            Button(self.seanse_frame,text='Seances',command=lambda i=i: self.show_seans(i[0])).grid(row=count,column=2)
            count+=1

        self.btn_seanse_back=Button(self.seanse_frame,text='<- Back',command=self.back_to_start).grid(row=count,column=1)

    def show_info(self,title,desc,time):
        global root
        self.movie_frame=Frame(root)
        self.movie_frame.pack()
        self.lbl_mv_title=Label(self.movie_frame,text=title).grid(row=0,column=0,columnspan=2)
        self.lbl_mv_desc=Label(self.movie_frame,text="Description:").grid(row=1,column=0)
        self.lbl_mv_desc1=Label(self.movie_frame,text=desc).grid(row=2,column=0)
        self.lbl_mv_time=Label(self.movie_frame,text='Duration:').grid(row=1,column=1)
        self.lbl_mv_time=Label(self.movie_frame,text='{} min'.format(time)).grid(row=2,column=1)
        

        self.btn_mv_back=Button(self.movie_frame,text='<- Back',command=self.mv_back).grid(row=3,column=1)
        self.seanse_frame.forget()
    
    def show_seans(self,title):
        c.execute("select godzina_rozpoczecia,sea_sala,id_seansu from seanse where sea_film='{}'".format(title))
        data=c.fetchall()
        self.seanse_frame.forget()
        self.show_seanse_frame=Frame(root)
        self.show_seanse_frame.pack()
        self.lbl_show_time=Label(self.show_seanse_frame,text='Date and time:').grid(row=0,column=0)
        self.lbl_show_room=Label(self.show_seanse_frame,text='Room nr:').grid(row=0,column=1)
        self.lbl_show_seats=Label(self.show_seanse_frame,text='How many seats to order?').grid(row=0,column=3)
        self.lbl_show_freeseats=Label(self.show_seanse_frame,text='Free seats:').grid(row=0,column=2)
        self.count1=1

        #this label is defined here but used in another function (reserve)
        #I have no idea why but apparently if a widget is defined inside a function
        #then it cannot be removed with .grid_forget().
        #tkinter is a bit buggy
        self.lbl_res_err=Label(self.show_seanse_frame,text='Not enough seats available')
         #the rest is where it belongs

        for k in data:
            
            exec(f'self.lbl_time_{k[2]}=Label(self.show_seanse_frame,text=k[0]).grid(row=self.count1,column=0)')
            exec(f'self.lbl_room_{k[2]}=Label(self.show_seanse_frame,text=k[1]).grid(row=self.count1,column=1)')
            c.execute(f"select * from ocz_rezerwacje where rez_seans={k[2]}")
            result1=c.fetchall()
            c.execute(f"select * from rezerwacje where rez_seans={k[2]}")
            result=c.fetchall()
            if result==[] and result1==[]:
                c.execute(f"select liczba_miejsc from sale where numer_sali={k[1]}")
                exec(f'self.free_seats_{k[2]}=c.fetchall()')
            elif result!=[] and result1==[]:
                c.execute(f'select sprawdz_miejsca({k[2]})')
                exec(f'self.free_seats_{k[2]}=c.fetchall()')
            elif result==[] and result1!=[]:
                c.execute(f'select sprawdz_ocz_miejsca({k[2]})')
                exec(f'self.free_seats_{k[2]}=c.fetchall()')

            elif result!=[] and result1!=[]:
                c.execute(f"select sprawdz_rezerwowane_miejsca({k[2]})")
                exec(f'self.free_seats_{k[2]}=c.fetchall()')
            
            exec(f'self.lbl_free_seats_{k[2]}=Label(self.show_seanse_frame,text=self.free_seats_{k[2]}[0]).grid(row=self.count1,column=2)')

            exec(f'self.e_seats_{k[2]}=Entry(self.show_seanse_frame)')
            exec(f'self.e_seats_{k[2]}.grid(row=self.count1,column=3)')
            # Button is not in exec because for some reason
            # exec doesn't allow the 'lambda k=k' trick. 
            # Luckily buttons dont have to be distinguishible
            Button(self.show_seanse_frame,text="Reserve",command= lambda k=k: self.reserve(k[2],title)).grid(row=self.count1,column=4)
            self.count1+=1
        self.btn_show_seans_back=Button(self.show_seanse_frame,text='<- Back',command=self.sh_back).grid(row=100,column=2)
    def reserve(self,id,title):
        
        
        #temporary solution to put data inside if statement
        a=[]
        b=[]

        exec(f'a.append(self.e_seats_{id}.get())')
        exec(f'b.append(self.free_seats_{id})')

        
        self.lbl_res_err.grid_forget()
        # and the data gets written in a weird way. I'll leave it as is since im not using it anywhere else
        if int(a[0])>b[0][0][0] and int(a[0])>0:
            
            self.lbl_res_err.grid(row=101,column=0,columnspan=5)
        elif int(a[0])<=b[0][0][0] and int(a[0])>0:
            exec(f'print(self.free_seats_{id}[0][0])')
            c.execute(f"insert into ocz_rezerwacje(zajmowane_miejsca,rez_seans) values('{a[0]}','{id}') returning id_ocz_rezerwacji")
            pending=c.fetchall()
            exec(f'self.e_seats_{id}.delete(0,END)')
            exec(f'self.e_seats_{id}.insert(0,"Zarezerwowano!")')
            #reloading to update available seats
            self.show_seanse_frame.destroy()
            self.show_seans(title)
            
            Label(self.show_seanse_frame,text="Your order is waiting for staff member to review.").grid(row=self.count1,column=0,columnspan=5)
            Label(self.show_seanse_frame,text=f"Your reservation number is {pending[0][0]}").grid(row=self.count1+1,column=0,columnspan=5)
        elif int(a[0])<=0:
            self.show_seanse_seaterr_lbl=Label(self.show_seanse_frame,text='Number of seats must be a positive integer!').grid(row=102,column=0,columnspan=5)
            

          




        
        

        



    def sh_back(self):
        self.show_seanse_frame.forget()
        self.seanse_frame.pack()
    
    def mv_back(self):
        self.movie_frame.forget()
        
        self.seanse_frame.pack()
    def back_to_start(self):
        self.seanse_frame.forget()
        Start(root)



Start(root)

root.mainloop()


db.commit()
db.close()
