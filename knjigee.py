import requests
import bs4
import shelve
from concurrent.futures import ThreadPoolExecutor, as_completed
knjigeee = []
def addknjige():

    for i in range(73):
        print(i)
        stranica = "https://www.knjizare-vulkan.rs/domaci-autori/"
        slika = "https://www.knjizare-vulkan.rs/files/thumbs/files/images/slike_proizvoda/thumbs_600/NESTO_600_600px.jpg"
        if(i==0):
            stranica = bs4.BeautifulSoup(requests.get(stranica).text,features="html.parser")
        else:
            stranica = bs4.BeautifulSoup(requests.get(stranica+"page-"+str(i)).text, features="html.parser")
            # stranica+="page"+str(i)
        knjige = stranica.select(".wrapper-gridalt-view")
        with ThreadPoolExecutor(max_workers=5) as executor:
            for knjiga in knjige:
                att = knjiga.attrs
                naziv = att.get("data-productname")
                slika1 = slika.replace("NESTO",str(att.get("data-productcode")))
                cena = att.get("data-productprice")
                knjigeee.append((naziv,slika1,cena))
    with ThreadPoolExecutor(max_workers=5) as executor:
        fajl = shelve.open("zabazu\\podaci.dat", "w")
        fajl["knjige"] = knjigeee
        fajl.close()