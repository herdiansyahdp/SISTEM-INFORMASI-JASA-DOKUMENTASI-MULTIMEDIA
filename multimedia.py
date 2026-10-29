import mysql.connector
from mysql.connector import Error

#untuk koneksi ke database
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "db_multimedia"
}

#jika ada eror atau gagal terhubung ke database
def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as err:
        print(f"\nGAGAL TERHUBUNG KE DATABASE: {err}")
        return None


def pause():
    input("\nTekan ENTER untuk kembali...")


def input_int(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Input harus berupa angka.")


def confirm_delete():
    while True:
        answer = input("Yakin ingin menghapus data ini? (y/n): ").strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("Masukkan y atau n.")


def print_title(title):
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)


#Tim_Multimedia
def create_tim():
    print_title("TAMBAH DATA TIM MULTIMEDIA")
    id_tim = input_int("ID TIM              : ")
    nama = input("Nama                 : ").strip()
    divisi = input("Divisi               : ").strip()
    if not nama or not divisi:
        print("Nama dan divisi wajib diisi.")
        return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Tim_Multimedia (id_tim, nama, divisi) VALUES (%s,%s,%s)",
                       (id_tim, nama, divisi))
        conn.commit()
        print("\nDATA TIM MULTIMEDIA BERHASIL DITAMBAHKAN!")
    except Error as err:
        conn.rollback(); print(f"GAGAL MENAMBAHKAN DATA: {err}")
    finally:
        cursor.close(); conn.close()


def read_tim():
    print_title("DAFTAR TIM MULTIMEDIA")
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_tim, nama, divisi FROM Tim_Multimedia ORDER BY id_tim")
        rows = cursor.fetchall()
        if not rows:
            print("BELUM ADA DATA TIM MULTIMEDIA."); return
        print(f"{'ID':<6}{'NAMA':<25}{'DIVISI':<25}")
        print("-" * 54)
        for r in rows: print(f"{r[0]:<6}{r[1]:<25}{r[2]:<25}")
    except Error as err: print(f"GAGAL MENAMPILKAN DATA: {err}")
    finally: cursor.close(); conn.close()


def update_tim():
    print_title("UBAH DATA TIM MULTIMEDIA")
    id_tim = input_int("ID TIM yang diubah : ")
    nama = input("Nama baru           : ").strip()
    divisi = input("Divisi baru         : ").strip()
    if not nama or not divisi:
        print("Nama dan divisi wajib diisi."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Tim_Multimedia SET nama=%s, divisi=%s WHERE id_tim=%s",
                       (nama, divisi, id_tim))
        conn.commit()
        print("\nDATA TIM MULTIMEDIA BERHASIL DIUBAH!" if cursor.rowcount else "\nID TIM TIDAK DITEMUKAN.")
    except Error as err:
        conn.rollback(); print(f"GAGAL MENGUBAH DATA: {err}")
    finally: cursor.close(); conn.close()


def delete_tim():
    print_title("HAPUS DATA TIM MULTIMEDIA")
    id_tim = input_int("ID TIM yang dihapus : ")
    if not confirm_delete(): print("Penghapusan dibatalkan."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Tim_Multimedia WHERE id_tim=%s", (id_tim,))
        conn.commit()
        print("\nDATA TIM MULTIMEDIA BERHASIL DIHAPUS!" if cursor.rowcount else "\nID TIM TIDAK DITEMUKAN.")
    except Error as err:
        conn.rollback(); print(f"GAGAL MENGHAPUS DATA: {err}")
    finally: cursor.close(); conn.close()


def menu_tim():
    while True:
        print_title("MENU TIM MULTIMEDIA")
        print("1. Tambah Data\n2. Tampilkan Data\n3. Ubah Data\n4. Hapus Data\n0. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1": create_tim(); pause()
        elif pilihan == "2": read_tim(); pause()
        elif pilihan == "3": update_tim(); pause()
        elif pilihan == "4": delete_tim(); pause()
        elif pilihan == "0": break
        else: print("Pilihan tidak valid."); pause()


#PEMESANAN
def create_pemesanan():
    print_title("TAMBAH DATA PEMESANAN")
    data = (
        input_int("ID Pemesanan        : "),
        input("Nama Pelanggan      : ").strip(),
        input("Nama Kegiatan       : ").strip(),
        input("Lokasi Kegiatan     : ").strip(),
        input("Tanggal Pemesanan [YYYY-MM-DD] : ").strip(),
        input("Waktu Kegiatan [HH:MM:SS]      : ").strip()
    )
    if not all(data[1:]): print("Semua field wajib diisi."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO Pemesanan
            (id_pemesanan,nama_pelanggan,nama_kegiatan,lokasi_kegiatan,tanggal_pemesanan,waktu_kegiatan)
            VALUES (%s,%s,%s,%s,%s,%s)""", data)
        conn.commit(); print("\nDATA PEMESANAN BERHASIL DITAMBAHKAN!")
    except Error as err: conn.rollback(); print(f"GAGAL MENAMBAHKAN DATA: {err}")
    finally: cursor.close(); conn.close()


def read_pemesanan():
    print_title("DAFTAR PEMESANAN")
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_pemesanan,nama_pelanggan,nama_kegiatan,lokasi_kegiatan,tanggal_pemesanan,waktu_kegiatan FROM Pemesanan ORDER BY id_pemesanan")
        rows = cursor.fetchall()
        if not rows: print("BELUM ADA DATA PEMESANAN."); return
        for r in rows:
            print(f"ID Pemesanan   : {r[0]}\nNama Pelanggan : {r[1]}\nNama Kegiatan  : {r[2]}\nLokasi         : {r[3]}\nTanggal Pesan  : {r[4]}\nWaktu Kegiatan : {r[5]}")
            print("-" * 70)
    except Error as err: print(f"GAGAL MENAMPILKAN DATA: {err}")
    finally: cursor.close(); conn.close()


def update_pemesanan():
    print_title("UBAH DATA PEMESANAN")
    id_p = input_int("ID Pemesanan yang diubah : ")
    data = (
        input("Nama Pelanggan baru      : ").strip(),
        input("Nama Kegiatan baru       : ").strip(),
        input("Lokasi Kegiatan baru     : ").strip(),
        input("Tanggal Pemesanan [YYYY-MM-DD] : ").strip(),
        input("Waktu Kegiatan [HH:MM:SS]      : ").strip(), id_p)
    if not all(data[:-1]): print("Semua field wajib diisi."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("""UPDATE Pemesanan SET nama_pelanggan=%s,nama_kegiatan=%s,lokasi_kegiatan=%s,
            tanggal_pemesanan=%s,waktu_kegiatan=%s WHERE id_pemesanan=%s""", data)
        conn.commit(); print("\nDATA PEMESANAN BERHASIL DIUBAH!" if cursor.rowcount else "\nID PEMESANAN TIDAK DITEMUKAN.")
    except Error as err: conn.rollback(); print(f"GAGAL MENGUBAH DATA: {err}")
    finally: cursor.close(); conn.close()


def delete_pemesanan():
    print_title("HAPUS DATA PEMESANAN")
    id_p = input_int("ID Pemesanan yang dihapus : ")
    if not confirm_delete(): print("Penghapusan dibatalkan."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Pemesanan WHERE id_pemesanan=%s", (id_p,))
        conn.commit(); print("\nDATA PEMESANAN BERHASIL DIHAPUS!" if cursor.rowcount else "\nID PEMESANAN TIDAK DITEMUKAN.")
    except Error as err: conn.rollback(); print(f"GAGAL MENGHAPUS DATA: {err}")
    finally: cursor.close(); conn.close()


def menu_pemesanan():
    while True:
        print_title("MENU PEMESANAN")
        print("1. Tambah Data\n2. Tampilkan Data\n3. Ubah Data\n4. Hapus Data\n0. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1": create_pemesanan(); pause()
        elif pilihan == "2": read_pemesanan(); pause()
        elif pilihan == "3": update_pemesanan(); pause()
        elif pilihan == "4": delete_pemesanan(); pause()
        elif pilihan == "0": break
        else: print("Pilihan tidak valid."); pause()


#JADWAL
def create_jadwal():
    print_title("TAMBAH DATA JADWAL")
    data = (
        input_int("ID Jadwal           : "),
        input_int("ID Pemesanan        : "),
        input_int("ID Tim              : "),
        input("Waktu Kegiatan [HH:MM:SS] : ").strip()
    )
    if not data[3]: print("Waktu kegiatan wajib diisi."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Jadwal (id_jadwal,id_pemesanan,id_tim,waktu_kegiatan) VALUES (%s,%s,%s,%s)", data)
        conn.commit(); print("\nDATA JADWAL BERHASIL DITAMBAHKAN!")
    except Error as err: conn.rollback(); print(f"GAGAL MENAMBAHKAN DATA: {err}")
    finally: cursor.close(); conn.close()


def read_jadwal():
    print_title("DAFTAR JADWAL")
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT j.id_jadwal,j.id_pemesanan,p.nama_pelanggan,p.nama_kegiatan,
            j.id_tim,t.nama,j.waktu_kegiatan
            FROM Jadwal j JOIN Pemesanan p ON j.id_pemesanan=p.id_pemesanan
            JOIN Tim_Multimedia t ON j.id_tim=t.id_tim ORDER BY j.id_jadwal""")
        rows = cursor.fetchall()
        if not rows: print("BELUM ADA DATA JADWAL."); return
        for r in rows:
            print(f"ID Jadwal       : {r[0]}\nID Pemesanan    : {r[1]}\nNama Pelanggan  : {r[2]}\nNama Kegiatan   : {r[3]}\nID Tim          : {r[4]}\nNama Tim        : {r[5]}\nWaktu Kegiatan  : {r[6]}")
            print("-" * 70)
    except Error as err: print(f"GAGAL MENAMPILKAN DATA: {err}")
    finally: cursor.close(); conn.close()


def update_jadwal():
    print_title("UBAH DATA JADWAL")
    id_j = input_int("ID Jadwal yang diubah : ")
    data = (input_int("ID Pemesanan baru    : "), input_int("ID Tim baru          : "), input("Waktu Kegiatan [HH:MM:SS] : ").strip(), id_j)
    if not data[2]: print("Waktu kegiatan wajib diisi."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Jadwal SET id_pemesanan=%s,id_tim=%s,waktu_kegiatan=%s WHERE id_jadwal=%s", data)
        conn.commit(); print("\nDATA JADWAL BERHASIL DIUBAH!" if cursor.rowcount else "\nID JADWAL TIDAK DITEMUKAN.")
    except Error as err: conn.rollback(); print(f"GAGAL MENGUBAH DATA: {err}")
    finally: cursor.close(); conn.close()


def delete_jadwal():
    print_title("HAPUS DATA JADWAL")
    id_j = input_int("ID Jadwal yang dihapus : ")
    if not confirm_delete(): print("Penghapusan dibatalkan."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Jadwal WHERE id_jadwal=%s", (id_j,)); conn.commit()
        print("\nDATA JADWAL BERHASIL DIHAPUS!" if cursor.rowcount else "\nID JADWAL TIDAK DITEMUKAN.")
    except Error as err: conn.rollback(); print(f"GAGAL MENGHAPUS DATA: {err}")
    finally: cursor.close(); conn.close()


def menu_jadwal():
    while True:
        print_title("MENU JADWAL")
        print("1. Tambah Data\n2. Tampilkan Data\n3. Ubah Data\n4. Hapus Data\n0. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1": create_jadwal(); pause()
        elif pilihan == "2": read_jadwal(); pause()
        elif pilihan == "3": update_jadwal(); pause()
        elif pilihan == "4": delete_jadwal(); pause()
        elif pilihan == "0": break
        else: print("Pilihan tidak valid."); pause()


#PEMBAYARAN
def create_pembayaran():
    print_title("TAMBAH DATA PEMBAYARAN")
    data = (
        input_int("ID Pembayaran      : "),
        input_int("ID Pemesanan       : "),
        input("Tanggal Bayar [YYYY-MM-DD] (kosong = NULL): ").strip() or None,
        input("Total Bayar         : ").strip(),
        input("Status Bayar        : ").strip()
    )
    if not data[3] or not data[4]: print("Total bayar dan status bayar wajib diisi."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Pembayaran (id_pembayaran,id_pemesanan,tanggal_bayar,total_bayar,status_bayar) VALUES (%s,%s,%s,%s,%s)", data)
        conn.commit(); print("\nDATA PEMBAYARAN BERHASIL DITAMBAHKAN!")
    except Error as err: conn.rollback(); print(f"GAGAL MENAMBAHKAN DATA: {err}")
    finally: cursor.close(); conn.close()


def read_pembayaran():
    print_title("DAFTAR PEMBAYARAN")
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT b.id_pembayaran,b.id_pemesanan,p.nama_pelanggan,p.nama_kegiatan,
            b.tanggal_bayar,b.total_bayar,b.status_bayar FROM Pembayaran b
            JOIN Pemesanan p ON b.id_pemesanan=p.id_pemesanan ORDER BY b.id_pembayaran""")
        rows = cursor.fetchall()
        if not rows: print("BELUM ADA DATA PEMBAYARAN."); return
        for r in rows:
            print(f"ID Pembayaran  : {r[0]}\nID Pemesanan   : {r[1]}\nNama Pelanggan : {r[2]}\nNama Kegiatan  : {r[3]}\nTanggal Bayar  : {r[4]}\nTotal Bayar    : Rp {r[5]:,.2f}\nStatus Bayar   : {r[6]}")
            print("-" * 70)
    except Error as err: print(f"GAGAL MENAMPILKAN DATA: {err}")
    finally: cursor.close(); conn.close()


def update_pembayaran():
    print_title("UBAH DATA PEMBAYARAN")
    id_b = input_int("ID Pembayaran yang diubah : ")
    data = (
        input_int("ID Pemesanan baru        : "),
        input("Tanggal Bayar [YYYY-MM-DD] (kosong = NULL): ").strip() or None,
        input("Total Bayar baru         : ").strip(),
        input("Status Bayar baru        : ").strip(), id_b
    )
    if not data[2] or not data[3]: print("Total bayar dan status bayar wajib diisi."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Pembayaran SET id_pemesanan=%s,tanggal_bayar=%s,total_bayar=%s,status_bayar=%s WHERE id_pembayaran=%s", data)
        conn.commit(); print("\nDATA PEMBAYARAN BERHASIL DIUBAH!" if cursor.rowcount else "\nID PEMBAYARAN TIDAK DITEMUKAN.")
    except Error as err: conn.rollback(); print(f"GAGAL MENGUBAH DATA: {err}")
    finally: cursor.close(); conn.close()


def delete_pembayaran():
    print_title("HAPUS DATA PEMBAYARAN")
    id_b = input_int("ID Pembayaran yang dihapus : ")
    if not confirm_delete(): print("Penghapusan dibatalkan."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Pembayaran WHERE id_pembayaran=%s", (id_b,)); conn.commit()
        print("\nDATA PEMBAYARAN BERHASIL DIHAPUS!" if cursor.rowcount else "\nID PEMBAYARAN TIDAK DITEMUKAN.")
    except Error as err: conn.rollback(); print(f"GAGAL MENGHAPUS DATA: {err}")
    finally: cursor.close(); conn.close()


def menu_pembayaran():
    while True:
        print_title("MENU PEMBAYARAN")
        print("1. Tambah Data\n2. Tampilkan Data\n3. Ubah Data\n4. Hapus Data\n0. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1": create_pembayaran(); pause()
        elif pilihan == "2": read_pembayaran(); pause()
        elif pilihan == "3": update_pembayaran(); pause()
        elif pilihan == "4": delete_pembayaran(); pause()
        elif pilihan == "0": break
        else: print("Pilihan tidak valid."); pause()


#HASIL DOKUMENTASI
def create_dokumentasi():
    print_title("TAMBAH HASIL DOKUMENTASI")
    data = (input_int("ID Dokumentasi     : "), input_int("ID Pemesanan       : "), input("Link File           : ").strip())
    if not data[2]: print("Link file wajib diisi."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Hasil_Dokumentasi (id_dokumentasi,id_pemesanan,link_file) VALUES (%s,%s,%s)", data)
        conn.commit(); print("\nDATA HASIL DOKUMENTASI BERHASIL DITAMBAHKAN!")
    except Error as err: conn.rollback(); print(f"GAGAL MENAMBAHKAN DATA: {err}")
    finally: cursor.close(); conn.close()


def read_dokumentasi():
    print_title("DAFTAR HASIL DOKUMENTASI")
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT h.id_dokumentasi,h.id_pemesanan,p.nama_pelanggan,p.nama_kegiatan,h.link_file
            FROM Hasil_Dokumentasi h JOIN Pemesanan p ON h.id_pemesanan=p.id_pemesanan
            ORDER BY h.id_dokumentasi""")
        rows = cursor.fetchall()
        if not rows: print("BELUM ADA HASIL DOKUMENTASI."); return
        for r in rows:
            print(f"ID Dokumentasi  : {r[0]}\nID Pemesanan     : {r[1]}\nNama Pelanggan   : {r[2]}\nNama Kegiatan    : {r[3]}\nLink File        : {r[4]}")
            print("-" * 70)
    except Error as err: print(f"GAGAL MENAMPILKAN DATA: {err}")
    finally: cursor.close(); conn.close()


def update_dokumentasi():
    print_title("UBAH HASIL DOKUMENTASI")
    id_d = input_int("ID Dokumentasi yang diubah : ")
    data = (input_int("ID Pemesanan baru          : "), input("Link File baru             : ").strip(), id_d)
    if not data[1]: print("Link file wajib diisi."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Hasil_Dokumentasi SET id_pemesanan=%s,link_file=%s WHERE id_dokumentasi=%s", data)
        conn.commit(); print("\nDATA HASIL DOKUMENTASI BERHASIL DIUBAH!" if cursor.rowcount else "\nID DOKUMENTASI TIDAK DITEMUKAN.")
    except Error as err: conn.rollback(); print(f"GAGAL MENGUBAH DATA: {err}")
    finally: cursor.close(); conn.close()


def delete_dokumentasi():
    print_title("HAPUS HASIL DOKUMENTASI")
    id_d = input_int("ID Dokumentasi yang dihapus : ")
    if not confirm_delete(): print("Penghapusan dibatalkan."); return
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Hasil_Dokumentasi WHERE id_dokumentasi=%s", (id_d,)); conn.commit()
        print("\nDATA HASIL DOKUMENTASI BERHASIL DIHAPUS!" if cursor.rowcount else "\nID DOKUMENTASI TIDAK DITEMUKAN.")
    except Error as err: conn.rollback(); print(f"GAGAL MENGHAPUS DATA: {err}")
    finally: cursor.close(); conn.close()


def menu_dokumentasi():
    while True:
        print_title("MENU HASIL DOKUMENTASI")
        print("1. Tambah Data\n2. Tampilkan Data\n3. Ubah Data\n4. Hapus Data\n0. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1": create_dokumentasi(); pause()
        elif pilihan == "2": read_dokumentasi(); pause()
        elif pilihan == "3": update_dokumentasi(); pause()
        elif pilihan == "4": delete_dokumentasi(); pause()
        elif pilihan == "0": break
        else: print("Pilihan tidak valid."); pause()


#MENU UTAMA
def main_menu():
    while True:
        print_title("SISTEM INFORMASI JASA DOKUMENTASI MULTIMEDIA")
        print("1. Tim Multimedia")
        print("2. Pemesanan")
        print("3. Jadwal")
        print("4. Pembayaran")
        print("5. Hasil Dokumentasi")
        print("0. Keluar")
        print("-" * 70)
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1": menu_tim()
        elif pilihan == "2": menu_pemesanan()
        elif pilihan == "3": menu_jadwal()
        elif pilihan == "4": menu_pembayaran()
        elif pilihan == "5": menu_dokumentasi()
        elif pilihan == "0": print("\nTERIMA KASIH TELAH MENGGUNAKAN PROGRAM."); break
        else: print("Pilihan tidak valid."); pause()


if __name__ == "__main__":
    main_menu()