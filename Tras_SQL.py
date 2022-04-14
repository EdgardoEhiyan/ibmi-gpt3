#-----------------------------------------------------------------------
# TRAIGO DATA DEL  IBM i
# CON CONSULTA SQL en lenguaje natural , implemenando API de OPEN IA
# y tiene la opcion de convertir  vos a texto
# #                                                Edgardo-Ehiyan
#----------------------------------------------------------------------

from ast import Return
from asyncio.windows_events import NULL
from gettext import find
from tkinter import *
from tkinter import ttk
from types import DynamicClassAttribute
from numpy import isnan, record
import pyodbc
pyodbc.pooling = False


import csv           


from tkinter.ttk import Treeview, Style
import tkinter as tk
from tkinter import messagebox as mb
import os
import shutil

import openai
import canvas
import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()



def login():
 global login_screen
 global dsnname_verify
 global username_verify
 global password_verify
 global username_login_entry
 global password_login_entry
 global user_entry
 global tv1
 global tv2
 
 login_screen = Toplevel(main_screen)
 login_screen.title("IBMi Login")
 login_screen.geometry("350x250")
 
 Label(login_screen, text="Enter Log-in details").grid(column=1, row=0, columnspan=2) 

 username_verify = StringVar()
 password_verify = StringVar()
 dsnname_verify = StringVar()
 
 Label(login_screen, text="DSN Name * ").grid(column=0, row=2)
 dsn_name = Entry(login_screen, textvariable=dsnname_verify)
 dsn_name.insert(0,"pub400.com")
 dsn_name.grid(column=1, row=2)
 
 Label(login_screen, text="Username * ").grid(column=0, row=3)
 username_login_entry = Entry(login_screen, textvariable=username_verify)
 username_login_entry.focus_set()
 username_login_entry.grid(column=1, row=3)
 
 Label(login_screen, text="Password * ").grid(column=0, row=4)
 password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
 password_login_entry.grid(column=1, row=4)
 
 Label(login_screen, text="").grid(column=0, row=5)
 Button(login_screen, text="Login", width=10, height=1, command = login_verify).grid(column=1, row=6, columnspan=2, sticky="ew")
 
 login_screen.bind("<Return>", login_verify)


def login_verify(*args):
 
 global errormsg
 global conn
 global conn2

 dsnname1 = dsnname_verify.get()
 username1 = username_verify.get()
 password1 = password_verify.get()

 if username1 != "" and password1 != '': 
 

      # cambie Login Edgardo  EHiyan (cambie DSN por driver='{iSeries Access ODBC Driver} )
    try:
        #con ssl
        #conn = pyodbc.connect(driver='{iSeries Access ODBC Driver}',system = dsnname1 + '; USERID='+ username1 + '; PASSWORD=' + password1 + ';SSL= true'  , autocommit=True )
        conn = pyodbc.connect(driver='{iSeries Access ODBC Driver}',system = dsnname1 + '; USERID='+ username1 + '; PASSWORD=' + password1 + ';SSL= true' )
        conn2 = pyodbc.connect(driver='{iSeries Access ODBC Driver}',system = dsnname1 + '; USERID='+ username1 + '; PASSWORD=' + password1 + ';SSL= true' + ';autocommit= True' )
        conn2.autocommit = False
        #sin SSL
        #conn = pyodbc.connect(driver='{iSeries Access ODBC Driver}',system = dsnname1 + '; USERID='+ username1 + '; PASSWORD=' + password1  )
        
        login_screen.destroy()
        btn_login["state"] = "disabled"
        btn_login["text"] = "Logged-in"
        btn_run1["state"] = "normal"
        btn_run9["state"] = "normal"
        #user_entry["state"] = "normal"
        tv1["state"] = "normal"
        #tv2["state"] = "normal"
        btn_logoff["state"] = "normal"
        btn_logoff["state"] = "enabled"  
    
    except pyodbc.InterfaceError as e :
        print("Connection failed - pyodbc.InterfaceError")
        print(e)
        errormsg = e
        login_error() 
    except pyodbc.OperationalError as e :
        print("Connection failed - pyodbc.OperationalError")
        print(e)
        errormsg = e
        login_error() 
    except pyodbc.DatabaseError as e:
        print("pyodbc.DatabaseError")
        print(e)
        errormsg = e
        login_error() 

def login_error():
 global login_error_screen
 global errormsg
 
 username_login_entry.delete(0, END)
 password_login_entry.delete(0, END)
 
 login_error_screen = Toplevel(login_screen)
 login_error_screen.title("Error")
 login_error_screen.geometry("850x200")
 Label(login_error_screen, text="Login Error").grid()
 err_screen = Text(login_error_screen, height=10, width=120)
 err_screen.grid()
 err_screen.insert(END,errormsg)
 Button(login_error_screen, text="OK", command=delete_login_error_screen).grid()
 
def delete_login_error_screen():
 login_error_screen.destroy()
 
def gpt3(ingreso):
  openai.api_key = 'sk- here , please put you api_key generated from openai'
  response = openai.Completion.create(
    #engine='davinci-instruct-beta-v3', 
    engine='text-davinci-001',
    prompt=ingreso,
    temperature=0.7,  #antes 0.3
    max_tokens=150,  #antes =2000
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0)
  return response.choices[0].text




def service1():
  
  


#--------------------------

# muestro en una nueva ventana
  my_w=tk.Tk()
  
  my_w.geometry("1200x600")
  
  dato=''
  #entrysql=''

  dato = tv1.get("1.0",'end-1c')
  
  paso=1
  print(dato)
  bandera = 1
  
  query=dato
  if paso==1:
   
  
   workx=gpt3(query)  # pruebo lo que grabao aca para ver si sirve (SE PASA A LA LINEA 201 PROBAR SINO SACAR)
   print(gpt3(query))
   paso=paso+1
  # ----------------------------------------------------------- #

  
  #pruebo limpieza de entrysql ------------------------------
  limpio=''
  entrysql.insert('1.0',limpio)
  # --------------------------------------------------------

  entrysql.delete('1.0', END)
  
  
   

  entrysql.insert('1.0',workx) # pruebo lo que grabao aca para ver si sirve (SE PASA A LA LINEA 201 PROBAR SINO SACAR)
  
    
  c1 = conn.cursor()
  # BUSCA LA PALABRA 'SQL' DENTRO DEL STRING query
  
  if query.find("sql") != -1 or query.find("SQL") != -1:
   work=gpt3(query)
   work=workx         # pruebo esto es una prueba sino borrar y borrar linea 182
   veo=work[0:7]
   bandera=1
   


   if veo == '\n\nCREAT' or veo == '\n\nALTER' or veo == '\n\nDROP ' or veo == '\n\nINSER' or veo == '\n\nDELET' :
     c2 = conn2.cursor()
     work2=work.replace(';','')  
     work3=work2.replace('"','')
     work4=work3.replace('`','')
     work5=work4.replace('ENGINE=InnoDB DEFAULT CHARSET=utf8;','')
     
     
     c2.execute(work5)
     c2.commit()   # ESTE ES EL SECRETO PARA QUE CONFIRME LA CREACION DE UNA TABLA
     c2.close()
     
     del c2
    
    
   else:
     work2=work.replace(';','')
     c1.execute(work2)
     c1.commit()
     c1.close
  else:
   bandera=2
   query='no es una sentencia sql'
   
   entrysql.delete('1.0', END)
   
   entrysql.insert('1.0',gpt3(query))
  
 
 # ---------------------------------------------------------------------
 # MUESTRO COLUMNAS (NOMBRE Y DATOS)
 # ---------------------------------------------------------------------
  
  try:
        records = c1.fetchall()
        records = [['' if i is None else i for i in record] for record in records]

        column_names = [i[0] for i in c1.description]
        for i in range(len(column_names)):
         second_frame=Entry(my_w, width=20, bg="white")
         second_frame.grid(row=0, column=i)
         second_frame.insert(0,column_names[i])
 

 #    SHOW DATA
        row_num = 1
        for row in records:
          for col in range(len(row)):
            second_frame=Entry(my_w, width=20, bg="white")
            second_frame.grid(row=row_num, column=col)
            second_frame.insert(END,row[col])
     
          row_num += 1
        
  except Exception as e:
        print("Skipping non rs message: {}".format(e))
        
        
    
   
   
  
  
 # GRABO CSV ---------------------------------------------------------------------------------
  
  try:
    column_names = [i[0] for i in c1.description]
    fp = open('C:/python/ia/FILECSV.csv', 'w')
    myFile = csv.writer(fp, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator = '\n')
    myFile.writerow(column_names)

   
    for row in records:
      myFile.writerow(row)
    

    
  
    fp.close()
  
  


    my_w.wm_attributes("-topmost", True) # Esta es la línea importante.
    
    mb.showinfo("Información", "Archivo CSV generado en C:\python\ia\FILECSV.csv.")
    my_w.mainloop()
  except Exception as e:
    print("no hay datos")
    my_w.wm_attributes("-topmost", True) # Esta es la línea importante , MANTIENE LA VENTANA POR ENCIMA DE LAS DEMAS.
   
    
    #mb.showinfo("No hay que mostrar")
    mb.showinfo("Información", "No hay datos para mostrar.")
    #mb.Messagebox.showinfo("Información", "No hay datos para mostrar.")
    my_w.mainloop()


# MODULO DE RECONOCIMIENTO DE VOZ -------------------------------------------------------------
# LLAMADA A LA API DE GOOGLE recognize_google                                               ---
def SpeakText():
    r = sr.Recognizer() 
 
    with sr.Microphone() as source:
      print('Speak Anything : ')
      r.adjust_for_ambient_noise(source, duration=0.3)
      audio = r.listen(source)
 
    try:
        
        #dato=''
        #entrysql=''

        #dato = tv1.get("1.0",'end-1c')
        tv1.delete('1.0', END)
        text = r.recognize_google(audio,language='es-AR')  # USO DE Google Speech API using the Google Speech Recognition API
        
        print('You said: {}'.format(text))

        # Aca reeplazo las palabras por los signos que necesito que salgan en una instruccion SQL cuando uso Google Speech Recognition API
        text2=text.replace('punto','.')
        text3=text2.replace('coma',',') 
        text4=text3.replace('dos puntos',':')
        text5=text4.replace('abro paréntesis','(')
        text6=text5.replace('cierro paréntesis',')')
        text7=text6.replace('comilla simple',"'")
        text8=text7.replace('barra','/')
        text9=text8.replace('guión bajo','_')
        text10=text9.replace('sea igual a','=')
        text11=text10.replace('cusis 2','QSYS2')
        text12=text11.replace('cusi 2','QSYS2')
        text13=text12.replace('koma',',')
        text14=text13.replace('Charles','char')  
        text15=text14.replace('sharp','char')
        text16=text15.replace('dos .s',':')
        text17=text16.replace('comillas simples',"'")
        text18=text17.replace('comillas',"'")
        text19=text18.replace('comilla',"'")
        text20=text19.replace('sea igual','=')
        text21=text20.replace('comida',"'")
        text22=text21.replace(' . ', '.')
        # convert text to upper case
        text23=text22.upper()
        
        tv1.insert(END, text23)
    except Exception as e:
        print("error es: {}".format(e))
    #except:
        #print('Sorry could not hear')



def logoff():
 btn_login["state"] = "active"
 btn_login["text"] = "Log-in to IBMi"
 btn_run1["state"] = "disabled"
 btn_run9["state"] = "disabled"
 user_entry["state"] = "disabled" 
 #btn_logoff["state"] = "disabled"
 conn.close()
 conn2.close()


def main_account_screen():
 global main_screen
 global display_screen
 global btn_login
 global btn_run1
 global btn_run9
 global user_entry
 global tv1
 global tv2
 
 global user_entry2
 global entrysql

 global btn_logoff
 #main_screen.protocol("WM_DELETE_WINDOW", handler) 
 main_screen = Tk()
 main_screen.state('zoomed')
 main_screen.geometry()
 main_screen.title("IBMi - GPT-3 INTELIGENCIA ARTIFICIAL PARA GENERAR CONSULTAS SQL CON LENGUAJE NATURAL  ")
 
 


 
 # configure the main panel
  
 main_screen.rowconfigure(0, minsize=800, weight=1 )
 main_screen.columnconfigure(1, minsize=0, weight=1)
 #main_screen.protocol("WM_DELETE_WINDOW", handler) 
 #main_screen.configure(bg='red')
 
 side_bar = Frame(main_screen, borderwidth=5, background="lightgrey")
 side_bar.grid(column=0, row=0,padx=0,ipady=0, sticky="N,W,S")
 side_bar.configure(bg='LIGHT SLATE BLUE')  # SLATE BLUE  // MEDIUM SLATE BLUE  // LIGHT SLATE BLUE
 
 # add label to side_bar
 lbl_side_bar = Label(side_bar, text="                      [ IBMi - GPT3 ]  Inteligencia Artificial para generar consultas SQL ", font=("Helvetica", 16), background="lightgrey")
 lbl_side_bar.grid(column=1, row=0, sticky="W,S", padx=5, pady=5)
 lbl_side_bar.configure(bg='LIGHT SLATE BLUE')  # SLATE BLUE  // MEDIUM SLATE BLUE  // LIGHT SLATE BLUE


 
  
  


 btn_login = Button(side_bar, text="Log-in to IBMi",command=login,bg="grey", fg="white", font=('Sans','8','bold'))
 btn_login.grid(row=0, column=0, sticky="ew", padx=5, pady=30)
 

 
 btn_run1 = Button(side_bar, text="GPT-3 I.A",command=service1,bg="yellow", fg="black", font=('Sans','8','bold'))
 btn_run1.grid(row=1, column=0, sticky="ew", padx=5, pady=10)

 
 # CAJA DE TEXTO PARA SQL DE IA
 


 btn_run9 = Button(side_bar, text="CONVIERTE VOZ A TEXTO",command=SpeakText,bg="yellow", fg="black", font=('Sans','8','bold'))
 btn_run9.grid(row=2, column=0, sticky="ew", padx=5, pady=10)  
 
 btn_logoff = Button(side_bar, text="Log-off",command=logoff,bg="grey", fg="white", font=('Sans','8','bold'))
 btn_logoff.grid(row=13, column=0, sticky="ew", padx=5, pady=130)
 
 

 




 ttk.Label(side_bar, text="Consulta SQL / Lenguaje Natural : ",background="LIGHT SLATE BLUE",
          font=("Times New Roman", 12)).grid(
  column=0, row=10, padx=10, pady=1)

 tv1 = tk.Entry(side_bar,width=163,  bg="white", fg="black", font=('Sans','8','bold'),) 
 tv1 = tk.Text(side_bar, width=128, height=8)
 tv1.grid(column=1, row=10)
 #tv1.insert(END, "hola mundo")

 ttk.Label(side_bar, text="Consulta SQL                              : ",background="LIGHT SLATE BLUE",
          font=("Times New Roman", 12)).grid(
  column=0, row=11, padx=10, pady=1)
 entrysql=tk.Entry(side_bar)
 entrysql = tk.Text(side_bar, width=128, height=9)
 entrysql.grid(column=1, row=12)

 

 
 
 
# -----------------------------------------------------

#-----------------------------------------------------
 display_screen = Frame(main_screen)
 display_screen.grid(column=1, row=0, sticky="N,W,S,E")
 
 
 
 
 
 # start off disabled = correct login activates these buttons
 btn_run1["state"] = "disabled"
 btn_run9["state"] = "disabled"

 #btn_logoff["state"] = "disabled"
 
 
 

 

 

 
 

         
 main_screen.mainloop()
 
main_account_screen()