from tkinter.filedialog import askdirectory
import tkinter as tk
import os
import animeworld as aw
import threading


"""
@Name: createDirectory
@desc: si occupa di creare una directory nella posizione deisderata con il nome desiderata,
    se dovesse già esistere una directory con lo stesso nome aggiunge un numero al nome
@parameters: 
    path{String}: path dove creare la directory
    name {String}: nome della directory

@return: 
    finalDirectory{String}: Path completo dove è stata creata la directory
"""

def createDirectory(path, name):
    try:
        caratteri = {"<", ">", ":", '"', "/", "|", "?", "*", " "}
        # Rimpiazzo i caratteri vietati da windows
        for carattere in caratteri:
           name = name.replace(carattere, "_")

        #Check esistenza cartella
        if os.path.exists(path + "/" + name):
            i = 0
            digit = 1
            while i < 1:
                if os.path.isdir(path + "/" + name + " - " + str(digit)):
                    digit = digit + 1
                else:
                    #Crea la cartella nella posizione data e con un nome non usato
                    os.makedirs(path + "/" + name + " - " + str(digit))
                    break

        else:
            os.makedirs(path + "/" + name)
            
        new_name = name
        return new_name
    except Exception:
        tk.messagebox.showerror(title="Errore cartella", message="Impossibile creare la cartella di destinazione.")

"""
@Name: scaricaMedia
@desc: Si occupa di scaricare gli episodi dell'anime

"""

def scaricaMedia():

    try:
        thread = threading.Thread(target=scaricaEpisodi)
        thread.start()

        print("startato")
       
    except Exception:
        tk.messagebox.showerror(title="Errore download", message="Non è stato possibile scaricare l'anime richiesto, mi dispiace")

    tk.messagebox.showinfo(title="Download inziato", message="Download di iniziato")
"""
@Name: scaricaEpisodi
@desc: si occupa di scaricare l'espidoio dal link passato e lo mette nella posizione di directory
@parameters: 
    url{String}: URL del video da scaricare
    directory {String}: percorso dove inserire il video

@return {int}
"""
def scaricaEpisodi():
    directory = path_field.get()
    url = url_field.get()
    episodio = def_episodes.get()

    anime = aw.Anime(link=url)
    episodi = anime.getEpisodes()

    #Controlla se l'utente ha scelto di creare la cartella 
    if create_directory.get() == 1:
        
        new_name = createDirectory(directory, anime.getName())
        directory = directory + "/" + new_name

    #Controlla se c'è solo 1 episodio da scaricare 
    if episodio != '':
    
        if episodio.find("+")!=-1:
            episodio = episodio.replace("+", '')
            episodiToDownload = int(episodio)

            for x in episodi:
                ep = int(x.number)
                if ep >= episodiToDownload:
                    x.download(anime.getName() + "_Ep." + x.number, directory)
        
        else:
              episodioToDownload = episodi[int(episodio)]
              episodioToDownload.download(anime.getName() + "_Ep." + episodio, directory)
    else:
        try:
            try:
                episodi = anime.getEpisodes()
            except (aw.ServerNotSupported, aw.AnimeNotAvailable) as error:
                print("Errore:", error)
            else:
                for x in episodi:
                    x.download(anime.getName() + "_Ep." + x.number, directory)
        except (aw.DeprecatedLibrary, aw.Error404) as error:
            print(error)



"""
@Name: askDirectory
@desc: si occupa di chiedere all'utente il percorso della cartella, nel caso nulla viene passato
    sceglie come percorso la directory corrente dove sta girando lo script

@return: 
    directory{String}: Path scelto dall'utente oppure path dove lo script sta girando
"""

def askDirectory():
    directory = askdirectory()
        
    if directory == '':
        directory = os.getcwd()
    path_field.insert(0, directory) 


#-------------------------------------------Gui---------------------------------------------------------#

 # gui
finestra = tk.Tk()
finestra.title("Sebas - Anime Downloader")

#setting window size
width=600
height=500
screenwidth = finestra.winfo_screenwidth()
screenheight = finestra.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
finestra.geometry(alignstr)
finestra.resizable(width=False, height=False)

lbl_download_video=tk.Label(finestra)
lbl_download_video["fg"] = "#333333"
lbl_download_video["justify"] = "center"
lbl_download_video["text"] = "Inserisci URL dell'anime da Animeworld"
lbl_download_video.place(x=10,y=10,width=231,height=36)

url_field=tk.Entry(finestra)
url_field["borderwidth"] = "1px"
url_field["fg"] = "#333333"
url_field["justify"] = "center"
url_field["text"] = "URL"
url_field.place(x=240,y=10,width=351,height=30)

lbl_path_video=tk.Label(finestra)
lbl_path_video["fg"] = "#333333"
lbl_path_video["justify"] = "center"
lbl_path_video["text"] = "Percorso di installazione"
lbl_path_video.place(x=0,y=60,width=172,height=30)

path_field=tk.Entry(finestra)
path_field["borderwidth"] = "1px"
path_field["fg"] = "#333333"
path_field["justify"] = "center"
path_field["text"] = "Path"
path_field.place(x=240,y=60,width=352,height=30)

GButton_956=tk.Button(finestra, command=askDirectory)
GButton_956["bg"] = "#efefef"
GButton_956["fg"] = "#000000"
GButton_956["justify"] = "center"
GButton_956["text"] = "..."
GButton_956.place(x=170,y=60,width=63,height=30)

create_directory = tk.IntVar()
crea_cartella=tk.Checkbutton(finestra, variable=create_directory, onvalue=1, offvalue=0)
crea_cartella["fg"] = "#333333"
crea_cartella["justify"] = "center"
crea_cartella["text"] = "Crea Sottocartella"
crea_cartella.place(x=410,y=350,width=154,height=30)
crea_cartella["offvalue"] = "0"
crea_cartella["onvalue"] = "1"

download_btn=tk.Button(finestra, command=scaricaMedia)
download_btn["bg"] = "#efefef"
download_btn["fg"] = "#000000"
download_btn["justify"] = "center"
download_btn["text"] = "Scarica"
download_btn.place(x=430,y=400,width=160,height=86)

lbl_def_espidodes=tk.Label(finestra)
lbl_def_espidodes["fg"] = "#333333"
lbl_def_espidodes["justify"] = "center"
lbl_def_espidodes["text"] = "Scarica solo 1 episodio"
lbl_def_espidodes.place(x=0,y=450,width=172,height=31)

def_episodes=tk.Entry(finestra)
def_episodes["borderwidth"] = "1px"
def_episodes["fg"] = "#333333"
def_episodes["justify"] = "center"
def_episodes["text"] = "Episodio"
def_episodes.place(x=180,y=450,width=162,height=36)

finestra.mainloop()