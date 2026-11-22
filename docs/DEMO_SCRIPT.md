# Panduan & Naskah Demonstrasi / Rekaman Video Aplikasi
## BPIC17 Event Log Analyzer & Process Mining System

Dokumen ini disusun khusus sebagai **naskah panduan (*speech script*)** dan **urutan aksi visual (*screenplay cue*)** untuk keperluan rekaman video singkat (durasi ideal: **3 hingga 5 menit**) atau demonstrasi langsung di hadapan dosen/penguji.

---

### 1. Checklist Persiapan Teknis Sebelum Rekaman

1. **Jalankan Aplikasi:**
   ```bash
   # Masuk ke direktori dan aktifkan environment
   cd /Users/mac/Docs/Projects/Datmin
   source .venv/bin/activate
   python main.py
   ```
2. **Siapkan Dataset XES:** Pastikan file `BPI_Challenge_2017.xes` atau `BPI_Challenge_2017.xes.gz` tersimpan di lokasi yang mudah dipilih saat dialog file picker terbuka (misal: di Desktop atau folder proyek).
3. **Perekaman Layar:** Gunakan perekam layar (misal: QuickTime Player, OBS Studio, atau CleanShot X) dengan resolusi minimal 1080p dan tangkapan audio mikrofon yang jernih.
4. **Siapkan Folder Ekspor:** Buat folder kosong (misal: `Hasil_Ekspor/`) untuk mendemonstrasikan penyimpanan file CSV hasil ekspor.

---

### 2. Lembar Acuan Angka Kunci (*Ground Truth Cheat-Sheet*)

Gunakan angka-angka ini sebagai acuan saat berbicara agar penyampaian terdengar sangat meyakinkan dan presisi:

| Indikator / Soal | Hasil Komputasi Aplikasi | Keterangan Metodologi Ilmiah |
| :--- | :--- | :--- |
| **Total Kasus (11.7 A)** | **31.509 kasus** | Dihitung dari ID kasus unik pada log utuh. |
| **Total Event Log** | **1.202.267 event** | Normalisasi *timestamp* ke format UTC. |
| **Rata-rata Durasi (11.7 B)** | **21,89 hari** | Dihitung dari trace utuh sebelum filter apa pun. |
| **11.7 C (Accepted)** | **16.897 kasus (53,63%)** | Mengandung aktivitas `O_Accepted` (non-eksklusif). |
| **11.7 D (Refused)** | **4.729 kasus (15,01%)** | Mengandung aktivitas `O_Refused` (non-eksklusif). |
| **11.7 E (Cancelled)** | **14.352 kasus (45,55%)** | Aktivitas terakhir tepat bernilai `O_Cancelled`. |
| **11.15 (Fraud Multi-Complete)** | **88 kasus** | Kasus dengan $\ge 2$ `W_Assess Potential Fraud` status `complete`. |
| **11.18 (Fraud Same Resource)** | **12 kasus** | Dilakukan oleh `org:resource` valid yang sama ($\ge 2$ kali). |
| **11.22 (Cancelled $\rightarrow$ Accepted)** | **414 kasus (1,31%)** | Pola *eventually follows* ($i < j$) pada level trace. |

---

### 3. Naskah Adegan per Adegan (*Scene-by-Scene Screenplay*)

```
TOTAL DURASI: ~3 – 5 Menit
GAYA BICARA: Formal, Lugas, Percaya Diri, dan Ilmiah
```

---

#### SCENE 1: Pembukaan & Impor Event Log XES (00:00 – 00:45)

* **Aksi di Layar (Visual Cue):**
  1. Tampilkan jendela utama aplikasi dalam kondisi kosong (*Empty Idle*).
  2. Klik tombol biru **"Impor File XES..."** di pojok kiri atas.
  3. Pilih file `BPI_Challenge_2017.xes` atau `.xes.gz`.
  4. Perlihatkan *progress bar* bergerak di status bar bawah dan badge berubah menjadi `MEMUAT DATASET...`.

* **Naskah Narasi (Audio Voiceover):**
  > *"Selamat pagi/siang Bapak/Ibu dosen dan rekan-rekan sekalian. Pada kesempatan ini, saya akan mendemonstrasikan **BPIC17 Event Log Analyzer**, aplikasi desktop berbasis Python, PM4Py, dan PySide6 yang dirancang secara mandiri dan 100% offline untuk menganalisis proses bisnis kredit perbankan BPIC 2017.*
  >
  > *Sebagai langkah pertama, saya akan mengimpor dataset event log BPIC 2017 berformat XES. Sistem ini mengadopsi prinsip **Single-Parse In-Memory**. Artinya, parsing file berukuran lebih dari 1,2 juta event ini dijalankan murni di latar belakang melalui QThread berkecepatan tinggi tanpa membekukan antarmuka pengguna sedikit pun."*

---

#### SCENE 2: Ringkasan Dataset & Log Overview (00:45 – 01:20)

* **Aksi di Layar (Visual Cue):**
  1. Saat dataset selesai dimuat, badge otomatis berubah hijau: `DATASET TERSEDIA`.
  2. Sorot kursor ke 5 Kartu Metrik di atas (31.509 kasus, 1.202.267 event, rentang waktu 2016–2017, mean duration 21,89 hari).
  3. Arahkan kursor ke tabel kiri: **Distribusi Frekuensi Aktivitas**.
  4. Pada tabel kanan: Ketikkan ID kasus (misal: `Application_1000000000`) di kotak input **"Cari Case ID:"** untuk menunjukkan penyaringan instan.

* **Naskah Narasi (Audio Voiceover):**
  > *"Setelah parsing selesai, aplikasi langsung menyajikan halaman **Overview**. Terlihat total kasus aktif sebanyak **31.509 kasus**, mencakup **1.202.267 event**, dengan rata-rata cycle time sebesar **21,89 hari**.*
  >
  > *Di panel kiri, distribusi frekuensi aktivitas tersaji secara terurut dengan cakupan persentase kasus. Dan di panel kanan, pengguna dapat melakukan pencarian cepat terhadap 31 ribu ringkasan kasus menggunakan fitur pencarian Case ID berbasis virtualized table model yang sangat responsif."*

---

#### SCENE 3: Eksekusi Analisis Soal Bab 11 (01:20 – 02:30)

* **Aksi di Layar (Visual Cue):**
  1. Klik tombol hijau **"Jalankan Analisis"** di bilah atas.
  2. Status bar bawah akan memproses seluruh soal dan badge berubah biru: `ANALISIS SELESAI`.
  3. Klik menu sidebar: **"Exercise 11.7 (A-E)"**.
     - Tunjukkan kartu metrik 11.7 A, B, C, D, E.
     - Klik radio button / tab kategori C (`O_Accepted` - 16.897 kasus) lalu kategori D (`O_Refused` - 4.729 kasus).
  4. Klik menu sidebar: **"Exercise 11.15 & 11.18"**.
     - Jelaskan hasil Fraud Analysis (88 kasus pada 11.15 vs 12 kasus pada 11.18).
  5. Klik menu sidebar: **"Exercise 11.22"**.
     - Tunjukkan 414 kasus (1,31%) yang mengalami pola anomali pembatalan diikuti penerimaan tawaran.

* **Naskah Narasi (Audio Voiceover):**
  > *"Sekarang kita beralih ke fitur analitik inti. Saya klik tombol **Jalankan Analisis**. Seluruh aturan analitik Bab 11 dievaluasi secara serempak di memori tanpa hardcoding.*
  >
  > *Pertama, pada **Exercise 11.7**, kita dapat melihat hasil yang 100% konsisten dengan benchmark Fluxicon Disco. Kategori 11.7 C menunjukkan 16.897 penawaran diterima, sementara 11.7 D mencatat 4.729 penawaran ditolak. Sesuai prinsip invariant sistem, evaluasi ini bersifat non-eksklusif sehingga kasus yang memiliki kedua status tetap dihitung secara independen dan akurat.*
  >
  > *Kedua, pada halaman **Exercise 11.15 dan 11.18**, kita menganalisis aktivitas investigasi penipuan ('W_Assess Potential Fraud'). Dengan filter ketat hanya pada status transisi 'complete', terdapat 88 kasus yang dinilai ganda. Namun pada 11.18, setelah membuang nilai resource kosong agar tidak terjadi bias, hanya ada 12 kasus yang benar-benar dinilai ganda oleh petugas atau resource yang sama.*
  >
  > *Ketiga, pada **Exercise 11.22**, algoritma mendeteksi pola 'eventually follows' di mana penawaran dibatalkan namun kemudian diterima. Terdapat 414 kasus atau 1,31% dari total populasi yang mengalami anomali ini."*

---

#### SCENE 4: Audit Bukti Jejak Kasus (*Case Evidence Explorer*) (02:30 – 03:20)

* **Aksi di Layar (Visual Cue):**
  1. Masih di halaman **Exercise 11.22** (atau 11.15), pilih salah satu baris kasus pada tabel.
  2. Klik tombol **"Lihat Rincian Case (Evidence)"** (atau klik ganda langsung pada baris kasus).
  3. Aplikasi otomatis berpindah ke halaman **Case Explorer**:
     - Sorot banner informasi di atas (menampilkan Case ID, durasi, dan *badge* alasan bukti).
     - Sorot tabel kronologis jejak: baris event pemicu disorot dengan **latar belakang kuning terang (`#FEF08A`)**, teks gelap tebal, dan kolom Evidence bertanda `[EVIDENCE]`.
     - Klik tombol **"Bersihkan Highlight Bukti"** lalu tunjukkan pencarian kasus manual di input Case Explorer.

* **Naskah Narasi (Audio Voiceover):**
  > *"Keunggulan utama aplikasi ini adalah kemampuan audit bukti atau **Case Evidence Explorer** secara one-click. Cukup dengan mengklik ganda baris kasus mana pun pada halaman soal, aplikasi langsung mengarahkan kita ke jejak audit kronologis kasus tersebut.*
  >
  > *Di sini, baris-baris event yang menjadi dasar pengambilan kesimpulan otomatis disorot dengan warna kuning berlabel [EVIDENCE]. Sistem mengurutkan jejak berdasarkan urutan deterministik nomor baris asli XES ('_orig_idx') dan timestamp UTC. Dengan demikian, analis tidak hanya disuguhi angka statistik agregat, melainkan dapat membuktikan fakta setiap event secara transparan."*

---

#### SCENE 5: Ekspor Hasil Analisis ke Format CSV (03:20 – 03:50)

* **Aksi di Layar (Visual Cue):**
  1. Klik tombol **"Ekspor CSV Ringkasan"** di bilah atas (Header Bar).
  2. Pilih folder penyimpanan, simpan file `summary_results.csv`.
  3. Masuk ke halaman **Exercise 11.7**, klik tombol **"Ekspor Daftar Case CSV"** untuk menyimpan `cases_11_7_C.csv`.
  4. *(Opsional)* Buka file CSV tersebut sebentar di Finder / Excel untuk membuktikan integritas datanya.

* **Naskah Narasi (Audio Voiceover):**
  > *"Selanjutnya untuk kebutuhan pelaporan bisnis, aplikasi menyediakan fitur **Ekspor CSV Atomik**. Kita dapat mengekspor ringkasan seluruh indikator ke dalam file `summary_results.csv`, lengkap dengan aturan filter, satuan waktu hari, dan persentase.*
  >
  > *Selain ringkasan, daftar kasus spesifik untuk setiap latihan juga dapat diekspor langsung per halaman. Proses penulisan file menggunakan mekanisme staging file sementara sehingga dijamin bebas dari korupsi data akibat interupsi I/O."*

---

#### SCENE 6: Fitur Lanjutan (Filter Builder ala Disco) & Penutup (03:50 – 04:30)

* **Aksi di Layar (Visual Cue):**
  1. Klik menu sidebar: **"Filter Builder (Disco)"**.
  2. Klik tombol **"+ Tambah Filter"**, pilih tipe **"Attribute Filter"** (misal pilih aktivitas `A_Create Application` atau `O_Accepted`).
  3. Klik **"Terapkan Filter"**: tunjukkan kartu tumpukan filter aktif dan tabel data terupdate secara instan.
  4. Kembali ke halaman utama atau tampilkan menu **"Tentang Aplikasi"** (About).

* **Naskah Narasi (Audio Voiceover):**
  > *"Sebagai nilai tambah, aplikasi ini juga telah dilengkapi dengan modul **Generic Filter Builder** bertingkat menyerupai perangkat lunak industri Fluxicon Disco. Pengguna dapat menumpuk filter atribut, endpoints, durasi performa, follower langsung, hingga rentang waktu kalender.*
  >
  > *Demikian demonstrasi dari BPIC17 Event Log Analyzer. Aplikasi ini berhasil memenuhi seluruh kaidah reproduktibilitas, integritas cycle time dari trace utuh, dan kelulusan 100% unit testing.*
  >
  > *Terima kasih atas perhatian Bapak/Ibu dosen dan rekan-rekan sekalian. Saya siap menerima pertanyaan maupun masukan."*

---

### 4. Tanya-Jawab Kritis (*Defense Sheet*) untuk Menghadapi Dosen

| Pertanyaan Dosen / Penguji | Jawaban Teknis Tepat |
| :--- | :--- |
| **"Mengapa jumlah kasus di 11.7 C (Accepted) dan 11.7 D (Refused) kalau dijumlahkan tidak sama dengan total kasus?"** | *"Sesuai spesifikasi buku Bab 11, evaluasi C dan D bersifat **non-eksklusif**. Dalam satu kasus kredit, sebuah aplikasi pinjaman dapat memiliki penawaran yang sempat ditolak (O_Refused) lalu mengajukan penawaran baru yang akhirnya diterima (O_Accepted), atau sebaliknya. Oleh karena itu, satu kasus sah tercatat di kedua kategori tanpa mengganggu total unik kasus."* |
| **"Bagaimana cara Anda menghitung Cycle Time agar tidak terdistorsi?"** | *"Durasi kasus selalu kami hitung dari selisih timestamp event terakhir dan event pertama pada **trace utuh (whole trace)** sebelum filter soal diterapkan. Kami tidak pernah menghitung durasi dari event-event hasil filtering yang terpotong."* |
| **"Mengapa di 11.18 hanya 12 kasus, padahal di 11.15 ada 88 kasus?"** | *"Pada 11.15, syaratnya adalah $\ge 2$ penilaian fraud berstatus complete oleh siapa pun. Namun pada 11.18, syaratnya adalah dinilai oleh **petugas (resource) yang sama**. Data BPIC17 memiliki baris fraud dengan kolom `org:resource` kosong. Kami sengaja membuang missing resource ini agar nilai kosong tidak dianggap sebagai satu resource yang sama (*fallacy*), sehingga menyisakan 12 kasus valid."* |
| **"Mengapa antarmuka tabel tetap lancar saat menampilkan 31.000 baris?"** | *"Kami menggunakan arsitektur Qt Model/View dengan `QAbstractTableModel` virtual. Data tidak dibuatkan widget per sel, melainkan di-render secara dinamis hanya untuk baris yang tampak pada layar (viewport virtual), didukung backend vektorisasi Pandas/NumPy."* |
