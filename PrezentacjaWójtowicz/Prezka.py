import tkinter as tk
import time

# 🔧 Ustawienia labiryntu (0 = droga, 1 = ściana)
labirynt = [
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 0]
]

start = (0, 0)
meta = (9, 9)
ruchy = [(1, 0), (-1, 0), (0, 1), (0, -1)]
odwiedzone = set()
sciezka = []

ROZMIAR = 50  # rozmiar pola w px

#  Tworzenie okna
okno = tk.Tk()
okno.title("DFS - Labirynt 10x10 (naciśnij SPACJĘ)")
canvas = tk.Canvas(okno, width=len(labirynt[0]) * ROZMIAR,
                   height=len(labirynt) * ROZMIAR, bg="white")
canvas.pack()

#  Rysowanie labiryntu
def rysuj_labirynt():
    canvas.delete("all")
    for i in range(len(labirynt)):
        for j in range(len(labirynt[0])):
            x1, y1 = j * ROZMIAR, i * ROZMIAR
            x2, y2 = x1 + ROZMIAR, y1 + ROZMIAR

            if labirynt[i][j] == 1:
                kolor = "black"
            elif (i, j) in sciezka:
                kolor = "lightgreen"
            elif (i, j) in odwiedzone:
                kolor = "lightgray"
            else:
                kolor = "white"

            canvas.create_rectangle(x1, y1, x2, y2, fill=kolor, outline="gray")

    # meta
    mx, my = meta
    canvas.create_rectangle(my * ROZMIAR, mx * ROZMIAR,
                            (my + 1) * ROZMIAR, (mx + 1) * ROZMIAR, fill="red")

    # aktualna pozycja
    x, y = pozycja
    canvas.create_oval(y * ROZMIAR + 10, x * ROZMIAR + 10,
                       y * ROZMIAR + ROZMIAR - 10, x * ROZMIAR + ROZMIAR - 10, fill="blue")

    okno.update()
    time.sleep(0.15)

#  Algorytm DFS
def dfs(x, y):
    global pozycja
    if x < 0 or x >= len(labirynt) or y < 0 or y >= len(labirynt[0]):
        return False
    if labirynt[x][y] == 1 or (x, y) in odwiedzone:
        return False

    odwiedzone.add((x, y))
    sciezka.append((x, y))
    pozycja = (x, y)
    rysuj_labirynt()

    if (x, y) == meta:
        return True

    for dx, dy in ruchy:
        if dfs(x + dx, y + dy):
            return True

    sciezka.pop()
    rysuj_labirynt()
    return False

#  Start po naciśnięciu spacji
def start_dfs(event=None):
    canvas.delete("all")
    canvas.create_text(len(labirynt[0]) * ROZMIAR // 2,
                       len(labirynt) * ROZMIAR // 2,
                       text=" Szukam drogi...", font=("Arial", 20, "bold"), fill="gray")
    okno.update()
    global pozycja
    pozycja = start
    dfs(*start)
    canvas.create_text(len(labirynt[0]) * ROZMIAR // 2,
                       len(labirynt) * ROZMIAR // 2,
                       text=" ZNALAZŁEM WYJŚCIE! 🎉",
                       font=("Arial", 20, "bold"), fill="darkgreen")

# ️ Ekran startowy
pozycja = start
rysuj_labirynt()
canvas.create_text(len(labirynt[0]) * ROZMIAR // 2,
                   len(labirynt) * ROZMIAR // 2,
                   text="Naciśnij SPACJĘ, aby rozpocząć",
                   font=("Arial", 20, "bold"), fill="darkblue")

# ⌨ Reakcja na spację
okno.bind("<space>", start_dfs)

okno.mainloop()
