

from tkinter import *             # This has all the code for GUIs.
import tkinter.font as font      # This lets us use different fonts.

import psycopg2

db=psycopg2.connect(host='localhost',user='postgres',password='your pswd',database='kino')
c=db.cursor()

def center_window_on_screen():

    x_cord = int((screen_width/2) - (width/2))
    y_cord = int((screen_height/2) - (height/2))
    root.geometry("{}x{}+{}+{}".format(width, height, x_cord, y_cord))




for i in range(5): print(i)


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
        

        self.lbl_heading_start = Label(self.start_frame,
                                    text='Witaj w kinie')
        self.lbl_heading_start.pack(pady=20)
        self.lbl_login_start_log=Label(self.start_frame,text='Login dla pracowników').pack()
        self.login_btn_start=Button(self.start_frame,text='Login',command=self.switch_to_login)
        self.login_btn_start.pack()
        self.lbl_login_start_use=Label(self.start_frame,text='Przegladaj filmy i seanse').pack()
        self.seans_btn_start=Button(self.start_frame,text='Przegladaj',command=self.switch_to_seanse)
        
        self.seans_btn_start.pack()
    

    def switch_to_login(self):
        
        self.start_frame.forget()
        Login(root)
    def switch_to_seanse(self):
        self.start_frame.forget()
        Seanse(root)

class Login():
    def __init__(self,master):
        self.login_frame=Frame(master)
        self.login_frame.pack()

        self.lbl_login_id=Label(self.login_frame,text='wpisz id:').pack()
        self.e_login_id=Entry(self.login_frame)
        self.e_login_id.pack()
        self.lbl_login_pswd=Label(self.login_frame,text='wpisz haslo:').pack()
        self.e_login_pswd=Entry(self.login_frame)
        self.e_login_pswd.pack()
        self.btn_login_enter=Button(self.login_frame,text='Dalej',command=self.login).pack()
        self.btn_login_back=Button(self.login_frame,text='Powrot do startu',command=self.back_to_start).pack()
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
            lbl_login_err=Label(self.login_frame,text='Zly login').pack()
        if pswd not in  data[:][1]:
            lbl_login_err1=Label(self.login_frame,text='Zle haslo').pack()




class Admin():
    def __init__(self,master):
        self.admin_frame=Frame(master)
        self.admin_frame.pack()

        self.lbl_admin=Label(self.admin_frame,text='Wybierz opcję:').pack()
        self.btn_admin_accept_req=Button(self.admin_frame,text='Akceptuj zamowienia',command=self.switch_to_accept).pack()
        self.btn_admin_add_seans=Button(self.admin_frame,text='Dodawanie seansow',command=self.switch_to_add_seans).pack()
        self.btn_admin_add_admin=Button(self.admin_frame,text='Dodawanie pracownikow',command=self.switch_to_add_admin).pack()
        self.btn_admin_back=Button(self.admin_frame,text='Powrot',command=self.back_to_login).pack()
    def switch_to_accept(self):
        self.admin_frame.forget()
        Accept(root)
    def switch_to_add_seans(self):
        self.admin_frame.forget()
        Add_seanse(root)
    def switch_to_add_admin(self):
        self.admin_frame.forget()
        Add_admin(root)
    def back_to_login(self):
        self.admin_frame.forget()
        Login(root)

class Accept():
    
    def __init__(self,master):
        self.accept_frame=Frame(master)
        self.accept_frame.pack()
        self.lbl_accept=Label(self.accept_frame,text='Akceptowanie zamowien').grid(row=0,column=0,columnspan=4)
        self.lbl_accept_desc_id=Label(self.accept_frame,text='Id:').grid(row=1,column=0)
        self.lbl_accept_desc_id=Label(self.accept_frame,text='Id seansu:').grid(row=1,column=1)
        self.lbl_accept_desc_id=Label(self.accept_frame,text='Zamowione miejsca:').grid(row=1,column=2)
        self.lbl_accept_desc_id=Label(self.accept_frame,text='Wolne miejsca:').grid(row=1,column=3)

        c.execute("select * from ocz_rezerwacje")
        pending=c.fetchall()

        #i need to name my buttons, but exec() doesnt allow the 'lambda res=res' trick.
        #button dictionary sounds weird but works
        self.button_dict={}
        for res in pending:
            self.button_dict[f'btn_accept{res[0]}']=Button(self.accept_frame,text='Akceptuj',command=lambda res=res: self.accept(res))

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

            self.button_dict[f'btn_accept{res[0]}'].grid(row=count,column=4)

            count+=1
        self.btn_accept_back=Button(self.accept_frame,text='powrot do wyboru',command=self.back_to_admin).grid(row=count,column=0)
    def accept(self,res):
        c.execute(f"insert into rezerwacje values ('{res[0]}','{res[1]}','{res[2]}')")
        c.execute(f"delete from ocz_rezerwacje where id_ocz_rezerwacji='{res[0]}'")
        #reloading to update seats taken
        self.accept_frame.destroy()
        Accept(root)

        
    
    def back_to_admin(self):
        self.accept_frame.forget()
        Admin(root)

class Add_seanse():
    def __init__(self,master):

        self.add_seanse_frame=Frame(master)
        self.add_seanse_frame.pack()

        self.lbl_add_seans=Label(self.add_seanse_frame,text='Dodawanie seansow').pack()

        self.lbl_title=Label(self.add_seanse_frame,text='Wpisz tytul').pack()
        self.e_add_title=Entry(self.add_seanse_frame)
        self.e_add_title.pack()

        self.lbl_time=Label(self.add_seanse_frame,text="Wpisz czas rozpoczecia (YYYY-MM-DD HH:MM:SS").pack()
        self.e_add_time=Entry(self.add_seanse_frame)
        self.e_add_time.pack()

        self.lbl_room=Label(self.add_seanse_frame,text='Wpisz numer sali').pack()
        self.e_add_room=Entry(self.add_seanse_frame)
        self.e_add_room.pack()

        
        

        self.btn_add=Button(self.add_seanse_frame,text="Dodaj seans",command=self.add).pack()

        

        self.btn_add_seans_back=Button(self.add_seanse_frame,text='Powrot do wyboru',command=self.back_to_admin).pack()
    def add(self):
        global c
        title=self.e_add_title.get()
        time=self.e_add_time.get()
        room=self.e_add_room.get()
        self.lbl_add_seans_err=Label(self.add_seanse_frame,text='Nie ma takiej sali')
        self.lbl_add_seans_err.forget()
        rooms=[1,2,3,4,5]

        if (int(room) in rooms):
            
            c.execute("Select add_seans('{a}','{b}','{c}')".format(a=title,b=time,c=room))
            result=c.fetchall()
            self.lbl_succesr=Label(self.add_seanse_frame,text='Dodano Seans z id {}'.format(result[0][0])).pack()


        elif (int(room) not in rooms):
            
            self.lbl_add_seans_err.pack()


    def back_to_admin(self):
        self.add_seanse_frame.forget()
        Admin(root)


class Add_admin():
    def __init__(self,master):

        self.add_admin_frame=Frame(master)
        self.add_admin_frame.pack()



        self.lbl_add_admin=Label(self.add_admin_frame,text='Dodawanie pracownikow').pack()
        self.lbl_name=Label(self.add_admin_frame,text='Wpisz imie nowego pracownika').pack()
        self.e_name=Entry(self.add_admin_frame)
        self.e_name.pack()
        self.lbl_surname=Label(self.add_admin_frame,text='Wpisz nazwisko nowego pracownika').pack()
        self.e_surname=Entry(self.add_admin_frame)
        self.e_surname.pack()
        self.lbl_id=Label(self.add_admin_frame,text='Wpisz id nowego pracownika (6 cyfr)').pack()
        self.e_id=Entry(self.add_admin_frame)
        self.e_id.pack()
        self.lbl_pswd=Label(self.add_admin_frame,text='Wpisz haslo dla nowego pracownika').pack()
        self.e_pswd=Entry(self.add_admin_frame)
        self.e_pswd.pack()
        self.btn_add=Button(self.add_admin_frame,text='Dodaj',command=self.add).pack()
        self.lbl_empty=Label(self.add_admin_frame,text=' ').pack()

        self.btn_add_admin_back=Button(self.add_admin_frame,text='powrot do wyboru', command=self.back_to_admin).pack()
    def add(self):
        name=self.e_name.get()
        surname=self.e_surname.get()
        id=self.e_id.get()
        pswd=self.e_pswd.get()
        
        c.execute("Insert into pracownicy values ('{a}','{b}','{c}','{d}')".format(a=id,b=pswd,c=name,d=surname))
        self.lbl_succes=Label(self.add_admin_frame,text='Dodano pracownika').pack()
    
    def back_to_admin(self):
        self.add_admin_frame.forget()
        Admin(root)

class Seanse():
    def __init__(self,master):

        self.seanse_frame=Frame(master)
        self.seanse_frame.pack()
        
        self.lbl_seanse=Label(self.seanse_frame,text='Dostepne filmy:').grid(row=0,column=0,columnspan=2)
        c.execute("select tytul, opis, czas_wyswietlania from filmy")
        self.list=c.fetchall()
     
        count=1
        for i in self.list:
           
            Label(self.seanse_frame,text='{}'.format(i[0])).grid(row=count,column=0)
            Button(self.seanse_frame,text='info',command=lambda i=i: self.show_info(i[0],i[1],i[2])).grid(row=count,column=1)
            Button(self.seanse_frame,text='Seanse',command=lambda i=i: self.show_seans(i[0])).grid(row=count,column=2)
            count+=1

        self.btn_seanse_back=Button(self.seanse_frame,text='Powrot',command=self.back_to_start).grid(row=count,column=1)

    def show_info(self,title,desc,time):
        global root
        self.movie_frame=Frame(root)
        self.movie_frame.pack()
        self.lbl_mv_title=Label(self.movie_frame,text=title).grid(row=0,column=0,columnspan=2)
        self.lbl_mv_desc=Label(self.movie_frame,text="OPIS:").grid(row=1,column=0)
        self.lbl_mv_desc1=Label(self.movie_frame,text=desc).grid(row=2,column=0)
        self.lbl_mv_time=Label(self.movie_frame,text='CZAS WYSWIETLANIA:').grid(row=1,column=1)
        self.lbl_mv_time=Label(self.movie_frame,text='{} min'.format(time)).grid(row=2,column=1)
        

        self.btn_mv_back=Button(self.movie_frame,text='Powrot',command=self.mv_back).grid(row=3,column=1)
        self.seanse_frame.forget()
    
    def show_seans(self,title):
        c.execute("select godzina_rozpoczecia,sea_sala,id_seansu from seanse where sea_film='{}'".format(title))
        data=c.fetchall()
        self.seanse_frame.forget()
        self.show_seanse_frame=Frame(root)
        self.show_seanse_frame.pack()
        self.lbl_show_time=Label(self.show_seanse_frame,text='Data i godzina wyswietlania:').grid(row=0,column=0)
        self.lbl_show_room=Label(self.show_seanse_frame,text='Nr sali:').grid(row=0,column=1)
        self.lbl_show_seats=Label(self.show_seanse_frame,text='Wpisz ile chcesz miejsc').grid(row=0,column=3)
        self.lbl_show_freeseats=Label(self.show_seanse_frame,text='Wolne miejsca:').grid(row=0,column=2)
        self.count1=1
        
        for k in data:
            
            exec(f'self.lbl_time_{k[2]}=Label(self.show_seanse_frame,text=k[0]).grid(row=self.count1,column=0)')
            exec(f'self.lbl_room_{k[2]}=Label(self.show_seanse_frame,text=k[1]).grid(row=self.count1,column=1)')
            c.execute(f"select * from rezerwacje where rez_seans={k[2]}")
            result=c.fetchall()
            
            if result==[]:
                c.execute(f"select liczba_miejsc from sale where numer_sali={k[1]}")
                exec(f'self.free_seats_{k[2]}=c.fetchall()')
            else:
                c.execute(f"select sprawdz_miejsca({k[2]})")
                exec(f'self.free_seats_{k[2]}=c.fetchall()')
            
            exec(f'self.lbl_free_seats_{k[2]}=Label(self.show_seanse_frame,text=self.free_seats_{k[2]}[0]).grid(row=self.count1,column=2)')

            exec(f'self.e_seats_{k[2]}=Entry(self.show_seanse_frame)')
            exec(f'self.e_seats_{k[2]}.grid(row=self.count1,column=3)')
            # Button is not in exec because for some reason
            # exec doesn't allow the 'lambda k=k' trick. 
            # Luckily buttons dont have to be distinguishible
            Button(self.show_seanse_frame,text="Wybierz",command= lambda k=k: self.reserve(k[2])).grid(row=self.count1,column=4)
            self.count1+=1
        self.btn_show_seans_back=Button(self.show_seanse_frame,text='Powrot',command=self.sh_back).grid(row=100,column=2)
    def reserve(self,id):
        
        

        a=[]
        b=[]
        exec(f'a.append(self.e_seats_{id}.get())')
        exec(f'b.append(self.free_seats_{id})')

        lbl_res_err=Label(self.show_seanse_frame,text='Nie ma tyle miejsc')
        lbl_res_err.grid_forget()
        if int(a[0])>b[0][0][0]:
            
            lbl_res_err.grid(row=101,column=0,columnspan=5)
        else:
        
            c.execute(f"insert into ocz_rezerwacje(zajmowane_miejsca,rez_seans) values('{a[0]}','{id}') returning id_ocz_rezerwacji")
            pending=c.fetchall()
            exec(f'self.e_seats_{id}.delete(0,END)')
            exec(f'self.e_seats_{id}.insert(0,"Zarezerwowano!")')
            Label(self.show_seanse_frame,text="Twoja rezerwacja oczekuje na zaakceptowanie przez pracownika.").grid(row=self.count1,column=0,columnspan=5)
            Label(self.show_seanse_frame,text=f" Numer twojej rezerwacji to {pending[0][0]}").grid(row=self.count1+1,column=0,columnspan=5)



        
        

        



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
