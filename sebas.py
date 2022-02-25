from tkinter.filedialog import askdirectory
import tkinter as tk
import os
import animeworld as aw
import threading
import eel

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
        finalDirectory = 0
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
                    finalDirectory  = path + "/" + name + " - " + str(digit)
                    break

        else:
            os.makedirs(path + "/" + name)
            finalDirectory  = path + "/" + name

        return finalDirectory
    except Exception:
        tk.messagebox.showerror(title="Errore cartella", message="Impossibile creare la cartella di destinazione.")

"""
@Name: scaricaMedia
@desc: Si occupa di scaricare gli episodi dell'anime

"""

def scaricaMedia():
    directory = path_field.get()
    url = url_field.get()
    episodio = def_episodes.get()

    args_download = {
        directory: directory, 
        url: url, 
        episodio: episodio
         }

    url = url.split(",")
    if len(url) > 1:
        for season in url:   
           args_download["url"] = season
           thread = threading.Thread(target=scaricaEpisodi,args=args_download)
           thread.start()
           lbl_status.config(text = "Scaricamente in corso ... 5%")
           thread.join()
           lbl_status.config(text = "Scaricamento completato")
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
        createDirectory(directory, anime.getName())
        directory = directory + "/" + anime.getName()

    #Controlla se c'è solo 1 episodio da scaricare 
    if episodio != '':
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

#titolo
finestra.title("Sebas - Anime Downloader")  
#widget

lbl_download_video = tk.Label(text="Inserisci url dell'anime da AnimeWorld", width=50, height=3)
lbl_download_video.pack()


url_field = tk.Entry(finestra,width=50)
url_field.pack()

lbl_path_video = tk.Label(text="path dove scaricare gli episodi", width=50, height=3)
lbl_path_video.pack()


path_field = tk.Entry(finestra,width=50)
path_field.pack()

path_button = tk.Button(text="...",  width=4,height=3,command=askDirectory)
path_button.pack()
path_button.place(x=445, y=117)



download_btn = tk.Button(text="Download UwU ",  width=10,height=3,command=scaricaMedia)
download_btn.pack()

lbl_def_espidodes = tk.Label(text="Scarica solo 1 episodio specifico", width=50, height=5)
lbl_def_espidodes.pack()

def_episodes = tk.Entry(finestra,width=5,)
def_episodes.pack()
def_episodes.place(x=375, y=235)

create_directory = tk.IntVar()

crea_cartella = tk.Checkbutton(finestra, text="Crea cartella con nome dell'anime?",variable=create_directory, onvalue=1, offvalue=0)
crea_cartella.pack()
crea_cartella.place(x=375, y=225)

lbl_status = tk.Label(text="", width=50, height=3)
lbl_status.pack()
lbl_status.place(x=450, y=225)

#opzioni supplementari
finestra.resizable(False, False)
finestra.geometry("700x600")


finestra.mainloop()
