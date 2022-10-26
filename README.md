alphp 8.1
=========
alphp adalah [Apache](https://httpd.apache.org/) dan [PHP](https://www.php.net/) dalam sebuah wadah. Ini seperti [XAMPP](https://www.apachefriends.org/index.html), dengan keunggulan yaitu Apache dan pengguna tidak saling berebut perijinan. Tidak perlu selalu melakukan *chown* atau *chmod*. Karena alphp dipasang di direktori **/home/pengguna** bukan di **/opt**, dan dijalankan tanpa akses root.

Pemasangan Pada Perangkat 64 bit
---------------------------------

Pengunduhan versi "full" sekitar 70MB. Berisi Apache 2.4, PHP 7, PHP 8, MariaDB dan [phpMyAdmin](https://github.com/gnulinuxid/phpmyadmin).

    $ wget https://github.com/a6smile/alphp/releases/download/v8.1/fork-alphp-8.1-x86_64.run
    $ sh fork-alphp-8.1-x86_64.run

Setelah terpasang, jalankan dengan:

    $ alphp
Jika shortcut tidak terpasang, jalankan dengan:

    $ $HOME/.alphp/8.1-full/bin/alphp

Bantuan:

    $ alphp -h
    
Konfigurasi
-----------
File config ada di .alphp/8.1-full/[alphp.conf](8.1-full/alphp.conf)

Catatan
-------
Karena alphp *rootless*, tidak mendukung port dibawah 1024. Standarnya adalah 8080. Tetapi jika menginginkan port misal 80, bisa menggunakan port forwarding. Berikut contoh jika menggunakan [socat](https://linux.die.net/man/1/socat):

    # socat TCP-LISTEN:80,reuseaddr,fork TCP:localhost:8080
- MySQL / MariaDB?

PHP di alphp ada ekstensi *mysqli* untuk konek ke server database (terpisah). Jika menginginkan LAMP Stack silahkan unduh alphp versi "full".

- Versi PHP

Saat ini menggunakan PHP 7.4 dan 8.1. Bisa berpindah versi dengan mudah. Untuk informasi ketik "alphp -h".

Screenshot
----------
![alphp-gui](https://user-images.githubusercontent.com/12754914/198066727-747d9cfc-4f03-4513-895d-d45e3fdd5a6d.png)

![alphp-bash](https://user-images.githubusercontent.com/12754914/198066662-2690760f-14ec-4c58-84f4-7322a8995788.png)
