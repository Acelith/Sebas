from tkinter.filedialog import askdirectory
from pytube import YouTube
from pytube import Playlist
import tkinter as tk
import os
import animeworld as aw

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
    
    if url == "":
        tk.messagebox.showerror(title="Link", message="Nessun link inserito. ")

    else:
        tk.messagebox.showinfo(title="Download in corso", message="Download in corso, attendere")
        scaricaEpisodi(url, directory)


"""
@Name: scaricaVideo
@desc: si occupa di scaricare il video dal link passato e lo mette nella posizione di directory
@parameters: 
    url{String}: URL del video da scaricare
    directory {String}: percorso dove inserire il video

@return {int}
"""
def scaricaEpisodi(url, directory):
    try:
        anime = aw.Anime(link=url)
    
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


#-------------------------------------------Guy---------------------------------------------------------#
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

path_button = tk.Button(text="...",  width=4,height=1,command=askDirectory)
path_button.pack()
path_button.place(x=445, y=117)

download_btn = tk.Button(text="Download UwU ",  width=10,height=4,command=scaricaMedia)
download_btn.pack()



#opzioni supplementari
finestra.resizable(False, False)
finestra.geometry("500x300")


finestra.mainloop()