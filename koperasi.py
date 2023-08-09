import pandas as pd # library open source pada Python, digunakan untuk memproses data, mulai pembersihan data, manipulasi data, melakukan analisis data.
import math #menyediakan fungsi-fungsi matematika dasar untuk digunakan pada operasi matematika sederhana
import copy #Untuk membuat salinan dari objek asli

#fungsi untuk membaca file csv
dataset = pd.read_csv('koperasi.csv')
X = dataset.iloc[:, 1:].values #iloc untuk menyeleksi data pada lokasi tertentu.

# Atribut yang digunakan dalam analisis
attribute = ["Kehadiran","Melaksanakan ADART","Pembukuan"]

#class Node untuk mewakili simpul dalam pohon keputusan
class Node(object):
    def __init__(self):
        self.value = None    # Nilai atribut pada simpul
        self.decision = None # Keputusan yang terkait dengan simpul (hanya digunakan pada simpul akhir)
        self.childs = None   # Daftar simpul anak

 #Menghitung entropi dari subset data
def findEntropy(data, rows):
    ya = 0
    tidak = 0
    ans = -1
    idx = len(data[0]) - 1
    entropy = 0
    for i in rows:
        if data[i][idx] == 'Ya':
            ya = ya + 1
        else:
            tidak = tidak + 1

    x = ya/(ya+tidak)
    y = tidak/(ya+tidak)
    if x != 0 and y != 0:
        entropy = -1 * (x*math.log2(x) + y*math.log2(y))
    if x == 1:
        ans = 1
    if y == 1:
        ans = 0
    return entropy, ans

#Mencari atribut dengan nilai gain maksimum
def findMaxGain(data, rows, columns):
    maxGain = 0
    retidx = -1
    entropy, ans = findEntropy(data, rows)
    if entropy == 0:
        """if ans == 1:
            print("Ya")
        else:
            print("Tidak")"""
        return maxGain, retidx, ans

    for j in columns:
        mydict = {}
        idx = j
        for i in rows:
            key = data[i][idx]
            if key not in mydict:
                mydict[key] = 1
            else:
                mydict[key] = mydict[key] + 1
        gain = entropy

        # print(mydict)
        for key in mydict:
            ya = 0
            tidak = 0
            for k in rows:
                if data[k][j] == key:
                    if data[k][-1] == 'Ya':
                        ya = ya + 1
                    else:
                        tidak = tidak + 1
            # print(ya, tidak)
            x = ya/(ya+tidak)
            y = tidak/(ya+tidak)
            # print(x, y)
            if x != 0 and y != 0:
                gain += (mydict[key] * (x*math.log2(x) + y*math.log2(y)))/14
        # print(gain)
        if gain > maxGain:
            # print("hello")
            maxGain = gain
            retidx = j

    return maxGain, retidx, ans

#Membangun pohon keputusan secara rekursif
def buildTree(data, rows, columns):

    maxGain, idx, ans = findMaxGain(X, rows, columns)
    root = Node()
    root.childs = []

    #Jika entropi adalah 0, buat simpul akhir dengan keputusan
    if maxGain == 0:
        if ans == 1:
            root.value = 'Ya'
        else:
            root.value = 'Tidak'
        return root

    root.value = attribute[idx]
    mydict = {}
    for i in rows:
        key = data[i][idx]
        if key not in mydict:
            mydict[key] = 1
        else:
            mydict[key] += 1

    newcolumns = copy.deepcopy(columns)
    newcolumns.remove(idx)
    for key in mydict:
        newrows = []
        for i in rows:
            if data[i][idx] == key:
                newrows.append(i)
        # print(newrows)
        temp = buildTree(data, newrows, newcolumns)
        temp.decision = key
        root.childs.append(temp)
    return root

#Menjelajahi pohon keputusan yang dibangun
def traverse(root):
    print(root.decision)
    print(root.value)

    n = len(root.childs)
    if n > 0:
        for i in range(0, n):
            traverse(root.childs[i])

#Fungsi untuk engatur dan memanggil semua langkah di atas
def calculate():
    rows = [i for i in range(0, 11)]   # Menggunakan indeks semua baris
    columns = [i for i in range(0, 3)] # Menggunakan indeks atribut
    root = buildTree(X, rows, columns)
    root.decision = 'Start'
    traverse(root)

# Memanggil fungsi untuk memulai analisis
calculate()
