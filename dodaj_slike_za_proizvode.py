from TaskRestAPI.models import *
import shelve
import urllib.request
import re
sablon = re.compile(r'(https://www.*/)(.*jpg$|.*JPG$)')
knjige = shelve.open("zabazu\\podaci.dat","r")
knjigeS = knjige.get('knjige')
knjigeBaza = Knjige.objects.filter().all()
for i in range(len(knjigeBaza)):
    naziv = knjigeBaza[i].naslov

    for i2 in range(len(knjigeS)):
        if(naziv==knjigeS[i2][0]):
            ime = sablon.findall(knjigeS[i2][1])[0][1]
            lokacija = "media\\images\\slike_proizvoda\\"+str(ime)
            # try:
            #     urllib.request.urlretrieve(knjigeS[i2][1],lokacija)
            # except:
            #     print(knjigeS[i2][1])
            #     # url = knjigeS[i2][1].replace("jpg","JPG")
            #     # print(url)
            #     # urllib.request.urlretrieve(url, lokacija)
            #     knjigeBaza[i].slika = "/images/slike_proizvoda/"+str(ime)
            #     knjigeBaza[i].save()
            #     print("sacuvano")
            #     continue
            knjigeBaza[i].slika = "/images/slike_proizvoda/"+str(ime)
            knjigeBaza[i].save()
print("gotovo")