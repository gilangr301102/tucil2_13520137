# Tugas Kecil 2 IF2211 Strategi Algoritma Semester II tahun 2023/2024
## Membangun Kurva Bézier dengan Algoritma Titik Tengah berbasis Divide and Conquer

# AUTHOR
- NAMA  : Muhammad Gilang Ramadhan 
- NIM   : 13520137
- KELAS : K-01

## Struktur Repository :
1. **doc** -> lokasi penyimpanan laporan tugas kecil.
2. **src** -> lokasi penyimpanan *source code* dari program.
3. **test** -> lokasi penyimpanan dokumen uji.
4. **bin** -> lokasi penyimpanan executable

## Requirement Program :
- Compiler Python3

## Cara menjalankan program
1. Buka terminal, arahkan ke direktori tempat program disimpan yaitu pada folder src
2. Jalankan perintah berikut
```
python3 main.py
```

## Interaksi Command Line:
Setelah itu program berhasil dijalankan,
1. Input lokasi file txt persoalan ketika program meminta input, beberapa data uji file txt tersedia file input.txt pada folder test (input ../test/input.txt) melalui interaksi command line
    jadi anda cukup memasukkan nama file tersebut saja dalam format .txt atau melalui input yang disediakan melalui command line
2. Program akan berjalan hingga menampilkan luaran berupa solusi permasalahan dan waktu eksekusi, serta anda bisa melakukan save pada terminal untuk solusi tersebut.

## Notes:
1. Untuk inputan brute force menggunakan parameter number of point pada kurva bezier yang diinginkan.
2. Untuk inputan divide and conquer menggunakan parameter number of iterasi, sehingga semakin banyak iterasi maka kurva akan semakin mulus dan semakin banyak number of pointnya (tetapi tidak bisa diatur lewat input secara langsung number of pointnya).

## Format Masukkan File txt
1. Brute Force:
```
n
x1 x2 x3 ... xn
y1 y2 y3 ... yn
n_point
```

2. Divide and Conquer
```
n
x1 x2 x3 ... xn
y1 y2 y3 ... yn
n_iterasi
```