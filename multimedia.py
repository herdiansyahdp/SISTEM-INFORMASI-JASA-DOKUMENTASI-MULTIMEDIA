from datetime import datetime
from decimal import Decimal, InvalidOperation

import mysql.connector
from mysql.connector import Error


DB_CONFIG = {"host": "localhost", "user": "root", "password": "", "database": "db_multimedia"}
STATUS_TRANSAKSI = ("Berhasil", "Pending", "Gagal")


def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as err:
        print(f"\nGAGAL TERHUBUNG KE DATABASE: {err}")
        return None


def pause():
    input("\nTekan ENTER untuk kembali...")


def input_int(prompt, minimum=1):
    while True:
        try:
            value = int(input(prompt).strip())
            if minimum is not None and value < minimum:
                raise ValueError
            return value
        except ValueError:
            print(f"Input harus berupa bilangan bulat minimal {minimum}.")


def input_required(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Field ini wajib diisi.")


def input_date(prompt, optional=False):
    while True:
        value = input(prompt).strip()
        if optional and not value:
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("Tanggal harus berformat YYYY-MM-DD dan valid.")


def input_time(prompt):
    while True:
        try:
            return datetime.strptime(input(prompt).strip(), "%H:%M:%S").time().isoformat()
        except ValueError:
            print("Waktu harus berformat HH:MM:SS dan valid.")


def input_money(prompt, minimum=Decimal("0")):
    while True:
        try:
            value = Decimal(input(prompt).strip().replace(",", ""))
            if not value.is_finite() or value < minimum:
                raise InvalidOperation
            return value
        except InvalidOperation:
            print(f"Nominal harus berupa angka valid minimal Rp {minimum:,.0f}.")


def input_status(prompt):
    valid_status = {status.lower(): status for status in STATUS_TRANSAKSI}
    while True:
        status = valid_status.get(input(prompt).strip().lower())
        if status:
            return status
        print("Status transaksi harus Berhasil, Pending, atau Gagal.")


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


def run_write(query, params, success, not_found, error):
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        print(success if cursor.rowcount else not_found)
    except Error as err:
        conn.rollback()
        print(f"{error}: {err}")
    finally:
        cursor.close()
        conn.close()


def create_tim():
    print_title("TAMBAH DATA TIM MULTIMEDIA")
    run_write(
        "INSERT INTO Tim_Multimedia (id_tim, nama, divisi) VALUES (%s, %s, %s)",
        (input_int("ID TIM              : "), input_required("Nama                : "), input_required("Divisi              : ")),
        "\nDATA TIM MULTIMEDIA BERHASIL DITAMBAHKAN!", "", "GAGAL MENAMBAHKAN DATA",
    )


def read_tim():
    print_title("DAFTAR TIM MULTIMEDIA")
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_tim, nama, divisi FROM Tim_Multimedia ORDER BY id_tim")
        rows = cursor.fetchall()
        if not rows:
            print("BELUM ADA DATA TIM MULTIMEDIA.")
            return
        print(f"{'ID':<6}{'NAMA':<25}{'DIVISI':<25}\n" + "-" * 54)
        for row in rows:
            print(f"{row[0]:<6}{row[1]:<25}{row[2]:<25}")
    except Error as err:
        print(f"GAGAL MENAMPILKAN DATA: {err}")
    finally:
        cursor.close()
        conn.close()


def update_tim():
    print_title("UBAH DATA TIM MULTIMEDIA")
    id_tim = input_int("ID TIM yang diubah  : ")
    run_write(
        "UPDATE Tim_Multimedia SET nama = %s, divisi = %s WHERE id_tim = %s",
        (input_required("Nama baru           : "), input_required("Divisi baru         : "), id_tim),
        "\nDATA TIM MULTIMEDIA BERHASIL DIUBAH!", "\nID TIM TIDAK DITEMUKAN.", "GAGAL MENGUBAH DATA",
    )


def delete_tim():
    print_title("HAPUS DATA TIM MULTIMEDIA")
    id_tim = input_int("ID TIM yang dihapus : ")
    if confirm_delete():
        run_write("DELETE FROM Tim_Multimedia WHERE id_tim = %s", (id_tim,), "\nDATA TIM MULTIMEDIA BERHASIL DIHAPUS!", "\nID TIM TIDAK DITEMUKAN.", "GAGAL MENGHAPUS DATA")
    else:
        print("Penghapusan dibatalkan.")


def menu_tim():
    menu_crud("MENU TIM MULTIMEDIA", create_tim, read_tim, update_tim, delete_tim)


def create_pemesanan():
    print_title("TAMBAH DATA PEMESANAN")
    data = (
        input_int("ID Pemesanan                   : "), input_required("Nama Pelanggan                 : "),
        input_required("Nama Kegiatan                  : "), input_required("Lokasi Kegiatan                : "),
        input_date("Tanggal Kegiatan [YYYY-MM-DD] : "), input_time("Waktu Kegiatan [HH:MM:SS]      : "),
        input_money("Total Biaya (Rp)               : ", Decimal("0.01")),
    )
    run_write(
        "INSERT INTO Pemesanan (id_pemesanan, nama_pelanggan, nama_kegiatan, lokasi_kegiatan, tanggal_pemesanan, waktu_kegiatan, total_biaya) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        data, "\nDATA PEMESANAN BERHASIL DITAMBAHKAN!", "", "GAGAL MENAMBAHKAN DATA",
    )


def read_pemesanan():
    print_title("DAFTAR PEMESANAN")
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_pemesanan, nama_pelanggan, nama_kegiatan, lokasi_kegiatan, tanggal_pemesanan, waktu_kegiatan, total_biaya, status_pelunasan FROM Pemesanan ORDER BY id_pemesanan")
        rows = cursor.fetchall()
        if not rows:
            print("BELUM ADA DATA PEMESANAN.")
            return
        for row in rows:
            print(f"ID Pemesanan     : {row[0]}\nNama Pelanggan   : {row[1]}\nNama Kegiatan    : {row[2]}\nLokasi           : {row[3]}\nTanggal Kegiatan : {row[4]}\nWaktu Kegiatan   : {row[5]}\nTotal Biaya      : Rp {row[6]:,.0f}\nStatus Pelunasan : {row[7]}")
            print("-" * 70)
    except Error as err:
        print(f"GAGAL MENAMPILKAN DATA: {err}")
    finally:
        cursor.close()
        conn.close()


def update_pemesanan():
    print_title("UBAH DATA PEMESANAN")
    id_pemesanan = input_int("ID Pemesanan yang diubah       : ")
    data = (
        input_required("Nama Pelanggan baru            : "), input_required("Nama Kegiatan baru             : "),
        input_required("Lokasi Kegiatan baru           : "), input_date("Tanggal Kegiatan [YYYY-MM-DD] : "),
        input_time("Waktu Kegiatan [HH:MM:SS]      : "), input_money("Total Biaya baru (Rp)          : ", Decimal("0.01")),
        id_pemesanan,
    )
    run_write(
        "UPDATE Pemesanan SET nama_pelanggan = %s, nama_kegiatan = %s, lokasi_kegiatan = %s, tanggal_pemesanan = %s, waktu_kegiatan = %s, total_biaya = %s WHERE id_pemesanan = %s",
        data, "\nDATA PEMESANAN BERHASIL DIUBAH!", "\nID PEMESANAN TIDAK DITEMUKAN.", "GAGAL MENGUBAH DATA",
    )


def delete_pemesanan():
    print_title("HAPUS DATA PEMESANAN")
    id_pemesanan = input_int("ID Pemesanan yang dihapus : ")
    if confirm_delete():
        run_write("DELETE FROM Pemesanan WHERE id_pemesanan = %s", (id_pemesanan,), "\nDATA PEMESANAN BERHASIL DIHAPUS!", "\nID PEMESANAN TIDAK DITEMUKAN.", "GAGAL MENGHAPUS DATA")
    else:
        print("Penghapusan dibatalkan.")


def menu_pemesanan():
    menu_crud("MENU PEMESANAN", create_pemesanan, read_pemesanan, update_pemesanan, delete_pemesanan)


def create_jadwal():
    print_title("TAMBAH DATA JADWAL")
    data = (input_int("ID Jadwal                    : "), input_int("ID Pemesanan                 : "), input_int("ID Tim                       : "), input_time("Waktu Kegiatan [HH:MM:SS]    : "))
    run_write("INSERT INTO Jadwal (id_jadwal, id_pemesanan, id_tim, waktu_kegiatan) VALUES (%s, %s, %s, %s)", data, "\nDATA JADWAL BERHASIL DITAMBAHKAN!", "", "GAGAL MENAMBAHKAN DATA")


def read_jadwal():
    print_title("DAFTAR JADWAL")
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT j.id_jadwal, j.id_pemesanan, p.nama_pelanggan, p.nama_kegiatan, j.id_tim, t.nama, j.waktu_kegiatan FROM Jadwal j JOIN Pemesanan p ON j.id_pemesanan = p.id_pemesanan JOIN Tim_Multimedia t ON j.id_tim = t.id_tim ORDER BY j.id_jadwal")
        rows = cursor.fetchall()
        if not rows:
            print("BELUM ADA DATA JADWAL.")
            return
        for row in rows:
            print(f"ID Jadwal       : {row[0]}\nID Pemesanan    : {row[1]}\nNama Pelanggan  : {row[2]}\nNama Kegiatan   : {row[3]}\nID Tim          : {row[4]}\nNama Tim        : {row[5]}\nWaktu Kegiatan  : {row[6]}")
            print("-" * 70)
    except Error as err:
        print(f"GAGAL MENAMPILKAN DATA: {err}")
    finally:
        cursor.close()
        conn.close()


def update_jadwal():
    print_title("UBAH DATA JADWAL")
    id_jadwal = input_int("ID Jadwal yang diubah         : ")
    data = (input_int("ID Pemesanan baru             : "), input_int("ID Tim baru                   : "), input_time("Waktu Kegiatan [HH:MM:SS]    : "), id_jadwal)
    run_write("UPDATE Jadwal SET id_pemesanan = %s, id_tim = %s, waktu_kegiatan = %s WHERE id_jadwal = %s", data, "\nDATA JADWAL BERHASIL DIUBAH!", "\nID JADWAL TIDAK DITEMUKAN.", "GAGAL MENGUBAH DATA")


def delete_jadwal():
    print_title("HAPUS DATA JADWAL")
    id_jadwal = input_int("ID Jadwal yang dihapus : ")
    if confirm_delete():
        run_write("DELETE FROM Jadwal WHERE id_jadwal = %s", (id_jadwal,), "\nDATA JADWAL BERHASIL DIHAPUS!", "\nID JADWAL TIDAK DITEMUKAN.", "GAGAL MENGHAPUS DATA")
    else:
        print("Penghapusan dibatalkan.")


def menu_jadwal():
    menu_crud("MENU JADWAL", create_jadwal, read_jadwal, update_jadwal, delete_jadwal)


def create_pembayaran():
    print_title("TAMBAH DATA PEMBAYARAN")
    data = (input_int("ID Pembayaran                         : "), input_int("ID Pemesanan                          : "), input_date("Tanggal Bayar [YYYY-MM-DD] (kosong = NULL): ", optional=True), input_money("Total Bayar (Rp)                      : "), input_status("Status Transaksi                      : "))
    run_write("INSERT INTO Pembayaran (id_pembayaran, id_pemesanan, tanggal_bayar, total_bayar, status_transaksi) VALUES (%s, %s, %s, %s, %s)", data, "\nDATA PEMBAYARAN BERHASIL DITAMBAHKAN!", "", "GAGAL MENAMBAHKAN DATA")


def read_pembayaran():
    print_title("DAFTAR PEMBAYARAN")
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT b.id_pembayaran, b.id_pemesanan, p.nama_pelanggan, p.nama_kegiatan, b.tanggal_bayar, b.total_bayar, b.status_transaksi FROM Pembayaran b JOIN Pemesanan p ON b.id_pemesanan = p.id_pemesanan ORDER BY b.id_pembayaran")
        rows = cursor.fetchall()
        if not rows:
            print("BELUM ADA DATA PEMBAYARAN.")
            return
        for row in rows:
            print(f"ID Pembayaran     : {row[0]}\nID Pemesanan      : {row[1]}\nNama Pelanggan    : {row[2]}\nNama Kegiatan     : {row[3]}\nTanggal Bayar     : {row[4]}\nTotal Bayar       : Rp {row[5]:,.2f}\nStatus Transaksi  : {row[6]}")
            print("-" * 70)
    except Error as err:
        print(f"GAGAL MENAMPILKAN DATA: {err}")
    finally:
        cursor.close()
        conn.close()


def update_pembayaran():
    print_title("UBAH DATA PEMBAYARAN")
    id_pembayaran = input_int("ID Pembayaran yang diubah                : ")
    data = (input_int("ID Pemesanan baru                         : "), input_date("Tanggal Bayar [YYYY-MM-DD] (kosong = NULL): ", optional=True), input_money("Total Bayar baru (Rp)                     : "), input_status("Status Transaksi baru                     : "), id_pembayaran)
    run_write("UPDATE Pembayaran SET id_pemesanan = %s, tanggal_bayar = %s, total_bayar = %s, status_transaksi = %s WHERE id_pembayaran = %s", data, "\nDATA PEMBAYARAN BERHASIL DIUBAH!", "\nID PEMBAYARAN TIDAK DITEMUKAN.", "GAGAL MENGUBAH DATA")


def delete_pembayaran():
    print_title("HAPUS DATA PEMBAYARAN")
    id_pembayaran = input_int("ID Pembayaran yang dihapus : ")
    if confirm_delete():
        run_write("DELETE FROM Pembayaran WHERE id_pembayaran = %s", (id_pembayaran,), "\nDATA PEMBAYARAN BERHASIL DIHAPUS!", "\nID PEMBAYARAN TIDAK DITEMUKAN.", "GAGAL MENGHAPUS DATA")
    else:
        print("Penghapusan dibatalkan.")


def read_ringkasan_pembayaran():
    print_title("RINGKASAN PEMBAYARAN")
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM v_ringkasan_pembayaran ORDER BY id_pemesanan")
        rows = cursor.fetchall()
        if not rows:
            print("BELUM ADA DATA PEMESANAN.")
            return
        for row in rows:
            print(f"ID Pemesanan       : {row[0]}\nNama Pelanggan     : {row[1]}\nNama Kegiatan      : {row[2]}\nTotal Biaya        : Rp {row[3]:,.0f}\nTotal Terbayar     : Rp {row[4]:,.0f}\nSisa Pembayaran    : Rp {row[5]:,.0f}\nStatus Pelunasan   : {row[6]}")
            print("-" * 70)
    except Error as err:
        print(f"GAGAL MENAMPILKAN RINGKASAN: {err}")
    finally:
        cursor.close()
        conn.close()


def menu_pembayaran():
    while True:
        print_title("MENU PEMBAYARAN")
        print("1. Tambah Data\n2. Tampilkan Data\n3. Ubah Data\n4. Hapus Data\n5. Ringkasan Pembayaran\n0. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1":
            create_pembayaran()
        elif pilihan == "2":
            read_pembayaran()
        elif pilihan == "3":
            update_pembayaran()
        elif pilihan == "4":
            delete_pembayaran()
        elif pilihan == "5":
            read_ringkasan_pembayaran()
        elif pilihan == "0":
            break
        else:
            print("PILIHAN TIDAK VALID!")
        pause()


def create_dokumentasi():
    print_title("TAMBAH HASIL DOKUMENTASI")
    data = (input_int("ID Dokumentasi     : "), input_int("ID Pemesanan       : "), input_required("Link File          : "))
    run_write("INSERT INTO Hasil_Dokumentasi (id_dokumentasi, id_pemesanan, link_file) VALUES (%s, %s, %s)", data, "\nDATA HASIL DOKUMENTASI BERHASIL DITAMBAHKAN!", "", "GAGAL MENAMBAHKAN DATA")


def read_dokumentasi():
    print_title("DAFTAR HASIL DOKUMENTASI")
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT h.id_dokumentasi, h.id_pemesanan, p.nama_pelanggan, p.nama_kegiatan, h.link_file FROM Hasil_Dokumentasi h JOIN Pemesanan p ON h.id_pemesanan = p.id_pemesanan ORDER BY h.id_dokumentasi")
        rows = cursor.fetchall()
        if not rows:
            print("BELUM ADA HASIL DOKUMENTASI.")
            return
        for row in rows:
            print(f"ID Dokumentasi  : {row[0]}\nID Pemesanan    : {row[1]}\nNama Pelanggan  : {row[2]}\nNama Kegiatan   : {row[3]}\nLink File       : {row[4]}")
            print("-" * 70)
    except Error as err:
        print(f"GAGAL MENAMPILKAN DATA: {err}")
    finally:
        cursor.close()
        conn.close()


def update_dokumentasi():
    print_title("UBAH HASIL DOKUMENTASI")
    id_dokumentasi = input_int("ID Dokumentasi yang diubah : ")
    data = (input_int("ID Pemesanan baru          : "), input_required("Link File baru             : "), id_dokumentasi)
    run_write("UPDATE Hasil_Dokumentasi SET id_pemesanan = %s, link_file = %s WHERE id_dokumentasi = %s", data, "\nDATA HASIL DOKUMENTASI BERHASIL DIUBAH!", "\nID DOKUMENTASI TIDAK DITEMUKAN.", "GAGAL MENGUBAH DATA")


def delete_dokumentasi():
    print_title("HAPUS HASIL DOKUMENTASI")
    id_dokumentasi = input_int("ID Dokumentasi yang dihapus : ")
    if confirm_delete():
        run_write("DELETE FROM Hasil_Dokumentasi WHERE id_dokumentasi = %s", (id_dokumentasi,), "\nDATA HASIL DOKUMENTASI BERHASIL DIHAPUS!", "\nID DOKUMENTASI TIDAK DITEMUKAN.", "GAGAL MENGHAPUS DATA")
    else:
        print("Penghapusan dibatalkan.")


def menu_dokumentasi():
    menu_crud("MENU HASIL DOKUMENTASI", create_dokumentasi, read_dokumentasi, update_dokumentasi, delete_dokumentasi)


def menu_crud(title, create, read, update, delete):
    actions = {"1": create, "2": read, "3": update, "4": delete}
    while True:
        print_title(title)
        print("1. Tambah Data\n2. Tampilkan Data\n3. Ubah Data\n4. Hapus Data\n0. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "0":
            return
        action = actions.get(pilihan)
        if action is None:
            print("Pilihan tidak valid.")
        else:
            action()
        pause()


def main_menu():
    actions = {"1": menu_tim, "2": menu_pemesanan, "3": menu_jadwal, "4": menu_pembayaran, "5": menu_dokumentasi}
    while True:
        print_title("SISTEM INFORMASI JASA DOKUMENTASI MULTIMEDIA")
        print("1. Tim Multimedia\n2. Pemesanan\n3. Jadwal\n4. Pembayaran\n5. Hasil Dokumentasi\n0. Keluar\n" + "-" * 70)
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "0":
            print("\nTERIMA KASIH TELAH MENGGUNAKAN PROGRAM.")
            return
        action = actions.get(pilihan)
        if action is None:
            print("Pilihan tidak valid.")
            pause()
        else:
            action()


if __name__ == "__main__":
    main_menu()    