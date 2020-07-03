sveKnjigeDetaljno = """
SELECT * FROM (
SELECT TaskRestAPI_knjige.id,naslov,strana,cena,godinaIzdanja,isbn,kategorija,auth_user.first_name|| ' ' ||auth_user.last_name AS "autor",TaskRestAPI_izdavaci.ime,kategorija
FROM TaskRestAPI_knjige
INNER JOIN auth_user ON auth_user.id = TaskRestAPI_knjige.autor_id
INNER JOIN TaskRestAPI_izdavaci ON TaskRestAPI_izdavaci.id = TaskRestAPI_knjige.izdavac_id)
WHERE id<151
"""


najpKnjige = """
SELECT id,isbn,naslov,cena,autor,izdavac,kategorija FROM(
SELECT * FROM (
		SELECT TaskRestAPI_knjige.id,TaskRestAPI_knjige.isbn,naslov,cena,auth_user.first_name|| ' ' ||auth_user.last_name AS "autor",TaskRestAPI_izdavaci.ime AS "izdavac",SUM(kolicina) AS "ukupno",kategorija
		FROM TaskRestAPI_knjige
		INNER JOIN TaskRestAPI_stavkenarudzbine ON TaskRestAPI_stavkenarudzbine.knjiga_id = TaskRestAPI_knjige.id
		INNER JOIN auth_user ON auth_user.id = TaskRestAPI_knjige.autor_id
		INNER JOIN TaskRestAPI_izdavaci ON TaskRestAPI_izdavaci.id = TaskRestAPI_knjige.izdavac_id
		GROUP BY TaskRestAPI_knjige.id
		) AS t1
		WHERE id<151
		GROUP BY id
		ORDER BY ukupno DESC
		)
LIMIT 7;
"""

besplKnjige = """
SELECT * FROM (
		SELECT TaskRestAPI_knjige.id,TaskRestAPI_knjige.isbn,naslov,cena,auth_user.first_name|| ' ' ||auth_user.last_name AS "autor",TaskRestAPI_izdavaci.ime AS "izdavac",kategorija
		FROM TaskRestAPI_knjige
		INNER JOIN auth_user ON auth_user.id = TaskRestAPI_knjige.autor_id
		INNER JOIN TaskRestAPI_izdavaci ON TaskRestAPI_izdavaci.id = TaskRestAPI_knjige.izdavac_id
		GROUP BY TaskRestAPI_knjige.id
		) AS t1
		 WHERE cena = 0.0
		; 
"""

hronLista = """
SELECT * FROM (
SELECT TaskRestAPI_knjige.id,isbn,naslov,cena,auth_user.first_name|| ' ' ||auth_user.last_name AS "autor",TaskRestAPI_izdavaci.ime AS "izdavac",kategorija
FROM TaskRestAPI_knjige
INNER JOIN auth_user ON auth_user.id = TaskRestAPI_knjige.autor_id
INNER JOIN TaskRestAPI_izdavaci ON TaskRestAPI_izdavaci.id = TaskRestAPI_knjige.izdavac_id
WHERE TaskRestAPI_knjige.id<151
ORDER BY RANDOM()
);
"""

mojeKnjige = """
SELECT korisnik_id,isbn,knjiga_id,naslov,autor,cena FROM (
SELECT TaskRestAPI_korisnici.korisnik_id AS "korisnik_id",TaskRestAPI_knjige.isbn,TaskRestAPI_knjige.id AS "knjiga_id", TaskRestAPI_knjige.naslov,auth_user.first_name|| ' ' ||auth_user.last_name AS "autor",TaskRestAPI_knjige.cena,TaskRestAPI_narudzbine.datumNarucivanja
FROM TaskRestAPI_korisnici
LEFT JOIN TaskRestAPI_narudzbine ON TaskRestAPI_narudzbine.korisnik_id = TaskRestAPI_korisnici.id+1
LEFT JOIN TaskRestAPI_stavkenarudzbine ON TaskRestAPI_stavkenarudzbine.narudzbina_id = TaskRestAPI_narudzbine.id
LEFT JOIN TaskRestAPI_knjige ON TaskRestAPI_knjige.id = TaskRestAPI_stavkenarudzbine.knjiga_id
LEFT JOIN auth_user ON auth_user.id = TaskRestAPI_knjige.autor_id
WHERE TaskRestAPI_knjige.id<151
ORDER BY datumNarucivanja DESC)
WHERE korisnik_id = nesto
;
"""

idd = """
SELECT * FROM (
SELECT TaskRestAPI_knjige.id,naslov,strana,cena,godinaIzdanja,isbn,kategorija,auth_user.first_name|| ' ' ||auth_user.last_name AS "autor",TaskRestAPI_izdavaci.ime
FROM TaskRestAPI_knjige
INNER JOIN auth_user ON auth_user.id = TaskRestAPI_knjige.autor_id
INNER JOIN TaskRestAPI_izdavaci ON TaskRestAPI_izdavaci.id = TaskRestAPI_knjige.izdavac_id)
WHERE kolona = nesto;
"""

komentari = """
SELECT * FROM (
SELECT komentar,TaskRestAPI_knjige.isbn,auth_user.first_name|| ' ' ||auth_user.last_name AS "korisnik",TaskRestAPI_knjige.id
FROM TaskRestAPI_komentarinaknjigama
INNER JOIN auth_user ON auth_user.id = TaskRestAPI_komentarinaknjigama.korisnik_id
INNER JOIN TaskRestAPI_knjige ON TaskRestAPI_knjige.id = TaskRestAPI_komentarinaknjigama.knjiga_id)
WHERE id = nesto;
"""

kategorija = "SELECT id,isbn,naslov,cena,autor,ime,godinaizdanja FROM (" + sveKnjigeDetaljno + ") WHERE kategorija = nesto AND id<151;"

getUser = """SELECT username,id FROM auth_user WHERE username = nesto1 AND password = nesto2 ;"""

getCountOsoba = """SELECT COUNT(id)+1 as 'ukupno' FROM auth_osoba;"""

countNarudzbine = """SELECT COUNT(id)+1 as 'ukupno' FROM TaskRestAPI_narudzbine;"""

upitiZaTab1 = ["najpKnjige\n","besplKnjige\n","hronLista\n","countNarudzbine\n"]

