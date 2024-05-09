import pyodbc

# Kapcsolat létrehozása az adatbázissal
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=bit.uni-corvinus.hu;'
    'DATABASE=szallashely;'
    'UID=Hallgato;'
    'PWD=Password123;'
)

# Cursor objektum létrehozása SQL lekérdezésekhez
cursor = conn.cursor()

# Lekérdezés 1.: Melyik szálláshelyen található a legtöbb olyan foglalás, amely legalább 5 éjszakára szól, és a foglalás időszakában volt legalább 2 gyermek is?
cursor.execute("""
SELECT TOP 1 s.szallas_nev, COUNT(f.foglalas_pk) AS foglalas_szam, SUM(f.felnott_szam + f.gyermek_szam) AS osszes_resztvevo
FROM szallashely s
JOIN szoba sz ON s.szallas_id = sz.szallas_fk
JOIN foglalas f ON sz.szoba_id = f.szoba_fk
WHERE DATEDIFF(DAY, f.mettol, f.meddig) >= 5 AND f.gyermek_szam >= 2
GROUP BY s.szallas_nev
ORDER BY foglalas_szam DESC
""")

# Output kiírása
print("Lekérdezés 1.")
for row in cursor.fetchall():
    print(row)

# Lekérdezés 2.: Melyik szálláshelyen található a legtöbb olyan foglalás, amelynek összesített vendégszáma eléri vagy meghaladja az átlagos foglalások vendégszámának kétszeresét?
cursor.execute("""
SELECT TOP 1 s.szallas_nev, COUNT(f.foglalas_pk) AS foglalas_szam
FROM szallashely s
JOIN szoba sz ON s.szallas_id = sz.szallas_fk
JOIN foglalas f ON sz.szoba_id = f.szoba_fk
GROUP BY s.szallas_nev
HAVING SUM(f.felnott_szam + f.gyermek_szam) >= (SELECT 2 * AVG(f2.felnott_szam + f2.gyermek_szam) FROM foglalas f2)
ORDER BY foglalas_szam DESC
""")

# Output kiírása
print("Lekérdezés 2.")
for row in cursor.fetchall():
    print(row)
    
# Lekérdezés 3.: Melyik szálláshelyen található a legtöbb olyan foglalás, ahol van legalább 1 gyermek, és legalább 2 felnőtt résztvevő?
cursor.execute("""
SELECT TOP 1 s.szallas_nev, COUNT(f.foglalas_pk) AS foglalas_szam
FROM szallashely s
JOIN szoba sz ON s.szallas_id = sz.szallas_fk
JOIN foglalas f ON sz.szoba_id = f.szoba_fk
WHERE f.felnott_szam >= 2 AND f.gyermek_szam >= 1
GROUP BY s.szallas_nev
ORDER BY foglalas_szam DESC
""")

# Output kiírása
print("Lekérdezés 3.")
for row in cursor.fetchall():
    print(row)

# Lekérdezés 4.: Melyik szálláshelyen található a legtöbb pótágyas szoba?
cursor.execute("""
SELECT TOP 1 s.szallas_nev, COUNT(*) AS potalyas_szoba_szam
FROM szallashely s
JOIN szoba sz ON s.szallas_id = sz.szallas_fk
WHERE sz.potagy > 0
GROUP BY s.szallas_nev
ORDER BY potalyas_szoba_szam DESC
""")

# Output kiírása
print("Lekérdezés 4.")
for row in cursor.fetchall():
    print(row)

# Lekérdezés 5.: Melyik szálláshelyeknek van legalább egy olyan szobájuk, amelyben van légkondicionáló, és legalább 2 férőhely van a foglalásra?
cursor.execute("""
SELECT s.szallas_nev
FROM szallashely s
JOIN szoba sz ON s.szallas_id = sz.szallas_fk
JOIN foglalas f ON sz.szoba_id = f.szoba_fk
WHERE sz.klimas = 'i' AND f.felnott_szam + f.gyermek_szam >= 2
GROUP BY s.szallas_nev;
""")

# Output kiírása
print("Lekérdezés 5.")
for row in cursor.fetchall():
    print(row)

# Kapcsolat bezárása
conn.close()