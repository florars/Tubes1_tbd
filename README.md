# Tugas Besar IF2211 Strategi Algoritma TBD 

## Table of Contents
- [Tugas Besar IF221 Strategi Algoritma TBD](#tugas-besar-if2211-strategi-algoritma-tbd)
    - [Table of Contents](#table-of-contents)
    - [Deskirpsi Project](#deskripsi-project)
    - [Penjelasan Algoritma](#penjelasan-algoritma) 
    - [Running Program](#running-program)
    - [Authors](#authors)

## Deskripsi Project 
Project ini adalah Tugas dari mata kuliah Strategi Algoritma yang tujuannya untuk membuat sebuah bot dengan menggunakan algoritma greedy sebagai algoritma utama dari pengambilan keputusan dari bot. bot yang diimplementasikan berasal dari game etimo diamond yang mana setiap bot bertujuan untuk mengambil diamond sebanyak-banyaknya dengan inventory dan waktu yang terbatas. 

## Penjelasan Algoritma 

Algoritma utama dari project ini adalah algoritma greedy yang mana banyak sekali alternatif yang bisa digunakan salah satunya adalah untuk mengambil diamond yang paling dekat dengan bot. Beberapa macam alternatif algoritma greedy yang kami eksplor adalah greedy by value, greedy by distance, greedy by enemy. 

Jadi, inti dari algoritma greedy pada project ini adalah mencapai keuntungan maksimal dengan memperhitungan setiap gerakan yang diambil. 

## Running Program
Jalankan command dibawah dari directory src dari repository TUBES1_TBD
untuk windows 
```
.\run-bots.bat
```
untuk linux 
```
.\run-bots.sh
```
pada run-bots.bat dan run-bots.sh ini adalah perintah untuk menjalankan beberapa bot sekaligus disini kami membuat bot alternatif lainnya sebagai perbandingan pada bot TBD kami. 

Untuk perintah menjalankan bot secara terpisah bisa menjalankan perintah di bawah ini
```
python main.py --logic TBD --email="email"@gmail.com --name=tbd --password=123456 --team etimo"
```
pada bagian "email" (yang diberi tanda kutip) bisa diganti dengan email user.


## Authors 

| NIM       | Name                              |
| --------- | ----------------------------------|
| 13522010  | Maria Flora Renata Siringoringo   |
| 13522024  | Kristo Anugrah                    |
| 13522119  | Indraswara Galih Jayanegara       |
