## DTS File Duplikat (Nama File)

## Deskripsi

**DTS File Duplikat (Nama File)** adalah program Python yang dirancang untuk mendeteksi dan menangani file duplikat di Google Drive berdasarkan **nama file**. Program ini membaca semua folder utama dan subfolder di My Drive, termasuk folder berbagi yang telah ditambahkan sebagai pintasan ke My Drive. 

**Fitur Utama**:
1. **Deteksi File Duplikat**: Mengidentifikasi file dengan nama yang sama di folder utama dan subfolder.
2. **Pemilihan File Terlama**: Dari file duplikat yang terdeteksi, program akan memilih satu file yang **terlama diunggah** untuk dipertahankan.
3. **Penghapusan dari Folder**: File lainnya akan **dikeluarkan dari folder** namun tetap tersedia di Google Drive Anda (tidak dihapus permanen).
4. **Kompatibilitas dengan Pintasan**: Program dapat membaca folder berbagi jika telah ditambahkan sebagai pintasan ke My Drive.

Proses ini memastikan setiap nama file hanya muncul sekali dalam setiap folder, menghindari duplikasi dan menjaga keteraturan Google Drive Anda.

## Cara Instalasi dan Penggunaan

### 1. **Kunjungi Google Colab**  
Buka [Google Colab](https://colab.research.google.com/) untuk menjalankan program ini. Google Colab memungkinkan Anda menjalankan skrip Python langsung di cloud tanpa perlu pengaturan lokal.  

Setelah membuka Google Colab, klik tombol **Notebook Baru** di pojok kanan bawah untuk membuat file notebook baru.  

### 2. **Unduh Skrip dengan cURL**
Jalankan perintah berikut di Google Colab untuk mengunduh skrip Python ini dari GitHub:  
```bash
!wget https://raw.githubusercontent.com/Andik252/DriveDuplicateHandler/refs/heads/main/script.py
```
### 3. **Jalankan Program**
Setelah skrip diunduh, jalankan program menggunakan perintah berikut:  
```python
exec(open('script.py').read())
```

### 4. **Ikuti Langkah-langkah Berikut**
1. **Login ke Akun Google Drive**: Saat program meminta otentikasi, ikuti petunjuk untuk login.
2. **Pilih Folder untuk Dipindai**: Program akan menampilkan daftar folder utama dan pintasan di My Drive Anda. Pilih folder dengan mengetikkan nomor atau nama folder.
3. **Proses File Duplikat**: Program akan memindai folder dan subfolder, mendeteksi file duplikat berdasarkan nama, memilih file terlama untuk dipertahankan, dan mengeluarkan file lain dari folder.
4. **Unduh Laporan (Opsional)**: Setelah proses selesai, Anda dapat mengunduh laporan hasil scan sebagai file teks.

## Catatan Penting

- **File Tidak Dihapus Permanen**: File yang dikeluarkan dari FOLDER tidak akan dihapus secara permanen dari Google Drive Anda. Mereka tetap akan ada di Halaman My Drive Anda. Namun,
  >Jika file tersebut diupload oleh orang lain (file shering), **FILE BISA HILANG.** alias File akan *kembali muncul di My Drive orang yang **Mengunggahnya**, bukan My Drive Anda*.

- **Folder Pintasan**: Program ini dapat membaca folder yang telah Anda tambahkan sebagai pintasan di My Drive, termasuk folder berbagi. Pastikan folder yang ingin dipindai telah ditambahkan sebagai pintasan di My Drive.
>Jika Anda hanya ingin memindai folder tertentu dan bukan seluruh struktur folder, Anda dapat membuat pintasan untuk folder yang diinginkan saja. Misalnya, jika Anda memiliki Folder **A** yang berisi Subfolder **B** dan **C**, dan hanya ingin memindai Subfolder **C**, Anda cukup membuat pintasan untuk **Subfolder C** di My Drive. Dengan cara ini, program hanya akan memindai folder yang telah Anda pilih, tanpa memindai folder yang lebih besar atau seluruh hierarki folder.

- **Persiapkan My Drive Anda**: Sebelum menjalankan program, disarankan untuk merapikan My Drive Anda. Hal ini akan membantu menghindari kebingungan saat file yang dikeluarkan dari folder muncul kembali di halaman utama My Drive Anda. Jika My Drive Anda berantakan, bisa jadi Anda kesulitan menemukan file tersebut setelah dipindahkan.

- **Pengujian Sebelum Penggunaan**: Sebaiknya, uji program ini terlebih dahulu pada folder percobaan sebelum menggunakannya pada folder yang berisi data penting. Ini akan membantu Anda memahami cara kerja program dan menghindari kesalahan yang tidak diinginkan.
