import tkinter as tk
from tkinter import ttk, messagebox
from koneksi import connect_db 

# Koneksi Database Utama
conn = connect_db()

# Adam - data penyewa 
def buka_penyewa():
    win_penyewa = tk.Toplevel(root)
    win_penyewa.title("Form Data Penyewa")
    win_penyewa.geometry("600x450")

    def tampilkan_data():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM penyewa")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def tambah_penyewa():
        if not entry_nama.get() or not entry_telp.get() or not entry_email.get():
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO penyewa (nama, no_telepon, email) VALUES (%s, %s, %s)"
            cursor.execute(sql, (entry_nama.get(), entry_telp.get(), entry_email.get()))
            conn.commit()
            messagebox.showinfo("Sukses", "Data Penyewa Berhasil Ditambahkan!")
            tampilkan_data()
            bersihkan_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ubah_penyewa():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data pada tabel terlebih dahulu!")
            return
        id_penyewa = tree.item(selected)['values'][0]
        try:
            cursor = conn.cursor()
            sql = "UPDATE penyewa SET nama=%s, no_telepon=%s, email=%s WHERE id_penyewa=%s"
            cursor.execute(sql, (entry_nama.get(), entry_telp.get(), entry_email.get(), id_penyewa))
            conn.commit()
            messagebox.showinfo("Sukses", "Data Penyewa Berhasil Diubah!")
            tampilkan_data()
            bersihkan_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def hapus_penyewa():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data pada tabel terlebih dahulu!")
            return
        id_penyewa = tree.item(selected)['values'][0]
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?"):
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM penyewa WHERE id_penyewa=%s", (id_penyewa,))
                conn.commit()
                messagebox.showinfo("Sukses", "Data Penyewa Berhasil Dihapus!")
                tampilkan_data()
                bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", "Gagal hapus! Data sedang digunakan di transaksi.")

    def bersihkan_form():
        entry_nama.delete(0, tk.END)
        entry_telp.delete(0, tk.END)
        entry_email.delete(0, tk.END)

    def isi_form_dari_tabel(event):
        selected = tree.selection()
        if selected:
            data = tree.item(selected)['values']
            entry_nama.delete(0, tk.END)
            entry_nama.insert(0, data[1])
            entry_telp.delete(0, tk.END)
            entry_telp.insert(0, data[2])
            entry_email.delete(0, tk.END)
            entry_email.insert(0, data[3])

    frame_input = tk.Frame(win_penyewa)
    frame_input.pack(pady=10)
    tk.Label(frame_input, text="Nama:").grid(row=0, column=0, padx=5, pady=5)
    entry_nama = tk.Entry(frame_input, width=30)
    entry_nama.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(frame_input, text="No. Telp:").grid(row=1, column=0, padx=5, pady=5)
    entry_telp = tk.Entry(frame_input, width=30)
    entry_telp.grid(row=1, column=1, padx=5, pady=5)
    tk.Label(frame_input, text="Email:").grid(row=2, column=0, padx=5, pady=5)
    entry_email = tk.Entry(frame_input, width=30)
    entry_email.grid(row=2, column=1, padx=5, pady=5)

    frame_btn = tk.Frame(win_penyewa)
    frame_btn.pack(pady=10)
    tk.Button(frame_btn, text="Tambah", bg="green", fg="white", command=tambah_penyewa).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Ubah", bg="orange", fg="white", command=ubah_penyewa).grid(row=0, column=1, padx=5)
    tk.Button(frame_btn, text="Hapus", bg="red", fg="white", command=hapus_penyewa).grid(row=0, column=2, padx=5)

    tree = ttk.Treeview(win_penyewa, columns=("ID", "Nama", "No_Telp", "Email"), show="headings")
    tree.heading("ID", text="ID"); tree.heading("Nama", text="Nama Penyewa"); tree.heading("No_Telp", text="No Telepon"); tree.heading("Email", text="Email")
    tree.column("ID", width=40)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    tree.bind("<<TreeviewSelect>>", isi_form_dari_tabel)
    tampilkan_data()


# Data lapangan
def buka_lapangan():
    win_lapangan = tk.Toplevel(root)
    win_lapangan.title("Form Data Lapangan") 
    win_lapangan.geometry("600x450")

    def tampilkan_data():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lapangan")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def tambah_lapangan():
        if not entry_nama.get() or not entry_jenis.get() or not entry_tarif.get():
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO lapangan (nama_lapangan, jenis_lapangan, tarif_per_jam) VALUES (%s, %s, %s)"
            cursor.execute(sql, (entry_nama.get(), entry_jenis.get(), int(entry_tarif.get())))
            conn.commit()
            messagebox.showinfo("Sukses", "Data Lapangan Berhasil Ditambahkan!")
            tampilkan_data()
            bersihkan_form()
        except ValueError:
            messagebox.showwarning("Input Salah", "Tarif harus berupa angka!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ubah_lapangan():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data pada tabel terlebih dahulu!")
            return
        if not entry_nama.get() or not entry_jenis.get() or not entry_tarif.get():
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return
        id_lapangan = tree.item(selected)['values'][0]
        try:
            cursor = conn.cursor()
            sql = "UPDATE lapangan SET nama_lapangan=%s, jenis_lapangan=%s, tarif_per_jam=%s WHERE id_lapangan=%s"
            cursor.execute(sql, (entry_nama.get(), entry_jenis.get(), int(entry_tarif.get()), id_lapangan))
            conn.commit()
            messagebox.showinfo("Sukses", "Data Lapangan Berhasil Diubah!")
            tampilkan_data()
            bersihkan_form()
        except ValueError:
            messagebox.showwarning("Input Salah", "Tarif harus berupa angka!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def hapus_lapangan():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data pada tabel terlebih dahulu!")
            return
        id_lapangan = tree.item(selected)['values'][0]
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?"):
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM lapangan WHERE id_lapangan=%s", (id_lapangan,))
                conn.commit()
                messagebox.showinfo("Sukses", "Data Lapangan Berhasil Dihapus!")
                tampilkan_data()
                bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", "Gagal hapus! Data sedang digunakan di transaksi.")

    def bersihkan_form():
        entry_nama.delete(0, tk.END)
        entry_jenis.delete(0, tk.END)
        entry_tarif.delete(0, tk.END)

    def isi_form_dari_tabel(event):
        selected = tree.selection()
        if selected:
            data = tree.item(selected)['values']
            entry_nama.delete(0, tk.END)
            entry_nama.insert(0, data[1])
            entry_jenis.delete(0, tk.END)
            entry_jenis.insert(0, data[2])
            entry_tarif.delete(0, tk.END)
            entry_tarif.insert(0, data[3])

    frame_input = tk.Frame(win_lapangan)
    frame_input.pack(pady=10)
    tk.Label(frame_input, text="Nama Lapangan:").grid(row=0, column=0, padx=5, pady=5)
    entry_nama = tk.Entry(frame_input, width=30)
    entry_nama.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(frame_input, text="Jenis Lapangan:").grid(row=1, column=0, padx=5, pady=5)
    entry_jenis = tk.Entry(frame_input, width=30)
    entry_jenis.grid(row=1, column=1, padx=5, pady=5)
    tk.Label(frame_input, text="Tarif / Jam:").grid(row=2, column=0, padx=5, pady=5)
    entry_tarif = tk.Entry(frame_input, width=30)
    entry_tarif.grid(row=2, column=1, padx=5, pady=5)

    frame_btn = tk.Frame(win_lapangan)
    frame_btn.pack(pady=10)
    tk.Button(frame_btn, text="Tambah", bg="green", fg="white", command=tambah_lapangan).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Ubah", bg="orange", fg="white", command=ubah_lapangan).grid(row=0, column=1, padx=5)
    tk.Button(frame_btn, text="Hapus", bg="red", fg="white", command=hapus_lapangan).grid(row=0, column=2, padx=5)

    tree = ttk.Treeview(win_lapangan, columns=("ID", "Nama", "Jenis", "Tarif"), show="headings")
    tree.heading("ID", text="ID"); tree.heading("Nama", text="Nama Lapangan"); tree.heading("Jenis", text="Jenis"); tree.heading("Tarif", text="Tarif / Jam")
    tree.column("ID", width=40)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    tree.bind("<<TreeviewSelect>>", isi_form_dari_tabel)
    tampilkan_data()


# Habibi - transaksi
def buka_penyewaan():
    win_sewa = tk.Toplevel(root)
    win_sewa.title("Transaksi Penyewaan Lapangan")
    win_sewa.geometry("800x500")

    def tampilkan_data():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conn.cursor()
            sql = """
            SELECT p.id_penyewaan, py.nama, l.nama_lapangan, p.tanggal_sewa, p.jam_mulai, p.durasi_jam, p.status_penyewaan
            FROM penyewaan p
            JOIN penyewa py ON p.id_penyewa = py.id_penyewa
            JOIN lapangan l ON p.id_lapangan = l.id_lapangan
            """
            cursor.execute(sql)
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_penyewa():
        cursor = conn.cursor()
        cursor.execute("SELECT id_penyewa, nama FROM penyewa")
        data = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        combo_penyewa['values'] = data

    def load_lapangan():
        cursor = conn.cursor()
        cursor.execute("SELECT id_lapangan, nama_lapangan FROM lapangan")
        data = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        combo_lapangan['values'] = data

    def tambah_penyewaan():
        if not combo_penyewa.get() or not combo_lapangan.get() or not entry_tanggal.get() or not entry_jam.get() or not entry_durasi.get():
            messagebox.showwarning("Peringatan", "Semua data harus diisi!")
            return
        try:
            id_penyewa = combo_penyewa.get().split(" - ")[0]
            id_lapangan = combo_lapangan.get().split(" - ")[0]
            cursor = conn.cursor()
            sql = "INSERT INTO penyewaan (id_penyewa, id_lapangan, tanggal_sewa, jam_mulai, durasi_jam, status_penyewaan) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (id_penyewa, id_lapangan, entry_tanggal.get(), entry_jam.get(), int(entry_durasi.get()), "Dipesan"))
            conn.commit()
            messagebox.showinfo("Sukses", "Transaksi penyewaan berhasil ditambahkan!")
            tampilkan_data()
            bersihkan_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def hapus_penyewaan():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data terlebih dahulu!")
            return
        id_penyewaan = tree.item(selected)['values'][0]
        if messagebox.askyesno("Konfirmasi", "Apakah anda yakin ingin menghapus data ini?"):
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM penyewaan WHERE id_penyewaan=%s", (id_penyewaan,))
                conn.commit()
                messagebox.showinfo("Sukses", "Data penyewaan berhasil dihapus!")
                tampilkan_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def bersihkan_form():
        combo_penyewa.set("")
        combo_lapangan.set("")
        entry_tanggal.delete(0, tk.END)
        entry_jam.delete(0, tk.END)
        entry_durasi.delete(0, tk.END)

    frame_input = tk.Frame(win_sewa)
    frame_input.pack(pady=10)
    tk.Label(frame_input, text="Penyewa").grid(row=0, column=0, padx=5, pady=5)
    combo_penyewa = ttk.Combobox(frame_input, width=30)
    combo_penyewa.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(frame_input, text="Lapangan").grid(row=1, column=0, padx=5, pady=5)
    combo_lapangan = ttk.Combobox(frame_input, width=30)
    combo_lapangan.grid(row=1, column=1, padx=5, pady=5)
    tk.Label(frame_input, text="Tanggal Sewa").grid(row=2, column=0, padx=5, pady=5)
    entry_tanggal = tk.Entry(frame_input, width=33)
    entry_tanggal.grid(row=2, column=1)
    tk.Label(frame_input, text="Jam Mulai").grid(row=3, column=0, padx=5, pady=5)
    entry_jam = tk.Entry(frame_input, width=33)
    entry_jam.grid(row=3, column=1)
    tk.Label(frame_input, text="Durasi (Jam)").grid(row=4, column=0, padx=5, pady=5)
    entry_durasi = tk.Entry(frame_input, width=33)
    entry_durasi.grid(row=4, column=1)

    frame_btn = tk.Frame(win_sewa)
    frame_btn.pack(pady=10)
    tk.Button(frame_btn, text="Tambah Penyewaan", bg="green", fg="white", command=tambah_penyewaan).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Hapus Penyewaan", bg="red", fg="white", command=hapus_penyewaan).grid(row=0, column=1, padx=5)

    tree = ttk.Treeview(win_sewa, columns=("ID", "Penyewa", "Lapangan", "Tanggal", "Jam", "Durasi", "Status"), show="headings")
    tree.heading("ID", text="ID"); tree.heading("Penyewa", text="Penyewa"); tree.heading("Lapangan", text="Lapangan")
    tree.heading("Tanggal", text="Tanggal"); tree.heading("Jam", text="Jam Mulai"); tree.heading("Durasi", text="Durasi"); tree.heading("Status", text="Status")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    load_penyewa()
    load_lapangan()
    tampilkan_data()


# Mahib - pembayaran
def buka_pembayaran():
    win_bayar = tk.Toplevel(root)
    win_bayar.title("Form Pembayaran")
    win_bayar.geometry("800x500")

    def tampilkan_data():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conn.cursor()
            sql = """
            SELECT pb.id_pembayaran, py.nama, l.nama_lapangan, pb.total_bayar, pb.status_pembayaran, pb.tanggal_pembayaran
            FROM pembayaran pb
            JOIN penyewaan p ON pb.id_penyewaan = p.id_penyewaan
            JOIN penyewa py ON p.id_penyewa = py.id_penyewa
            JOIN lapangan l ON p.id_lapangan = l.id_lapangan
            """
            cursor.execute(sql)
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_penyewaan():
        cursor = conn.cursor()
        sql = """
        SELECT p.id_penyewaan, py.nama, l.nama_lapangan
        FROM penyewaan p
        JOIN penyewa py ON p.id_penyewa = py.id_penyewa
        JOIN lapangan l ON p.id_lapangan = l.id_lapangan
        """
        cursor.execute(sql)
        data = [f"{row[0]} - {row[1]} - {row[2]}" for row in cursor.fetchall()]
        combo_penyewaan['values'] = data

    def tambah_pembayaran():
        if not combo_penyewaan.get() or not entry_total.get() or not entry_tanggal.get():
            messagebox.showwarning("Peringatan", "Semua data harus diisi!")
            return
        try:
            id_penyewaan = combo_penyewaan.get().split(" - ")[0]
            cursor = conn.cursor()
            sql = "INSERT INTO pembayaran (id_penyewaan, total_bayar, status_pembayaran, tanggal_pembayaran, jumlah_refund) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql, (id_penyewaan, int(entry_total.get()), "Lunas", entry_tanggal.get(), 0))
            conn.commit()
            messagebox.showinfo("Sukses", "Pembayaran berhasil ditambahkan!")
            tampilkan_data()
            bersihkan_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def hapus_pembayaran():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data terlebih dahulu!")
            return
        id_pembayaran = tree.item(selected)['values'][0]
        if messagebox.askyesno("Konfirmasi", "Apakah anda yakin menghapus data pembayaran ini?"):
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM pembayaran WHERE id_pembayaran=%s", (id_pembayaran,))
                conn.commit()
                messagebox.showinfo("Sukses", "Data pembayaran berhasil dihapus!")
                tampilkan_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def bersihkan_form():
        combo_penyewaan.set("")
        entry_total.delete(0, tk.END)
        entry_tanggal.delete(0, tk.END)

    frame_input = tk.Frame(win_bayar)
    frame_input.pack(pady=10)
    tk.Label(frame_input, text="Penyewaan").grid(row=0, column=0, padx=5, pady=5)
    combo_penyewaan = ttk.Combobox(frame_input, width=35)
    combo_penyewaan.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(frame_input, text="Total Bayar").grid(row=1, column=0, padx=5, pady=5)
    entry_total = tk.Entry(frame_input, width=38)
    entry_total.grid(row=1, column=1)
    
    # DISESUAIKAN: Input Tanggal (Format: YYYY-MM-DD)
    tk.Label(frame_input, text="Tanggal (YYYY-MM-DD)").grid(row=2, column=0, padx=5, pady=5)
    entry_tanggal = tk.Entry(frame_input, width=38)
    entry_tanggal.grid(row=2, column=1)

    frame_btn = tk.Frame(win_bayar)
    frame_btn.pack(pady=10)
    tk.Button(frame_btn, text="Tambah Pembayaran", bg="green", fg="white", command=tambah_pembayaran).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Hapus Pembayaran", bg="red", fg="white", command=hapus_pembayaran).grid(row=0, column=1, padx=5)

    tree = ttk.Treeview(win_bayar, columns=("ID", "Penyewa", "Lapangan", "Total", "Status", "Tanggal"), show="headings")
    tree.heading("ID", text="ID"); tree.heading("Penyewa", text="Penyewa"); tree.heading("Lapangan", text="Lapangan")
    tree.heading("Total", text="Total Bayar"); tree.heading("Status", text="Status"); tree.heading("Tanggal", text="Tanggal Bayar")
    tree.column("ID", width=50)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    load_penyewaan()
    tampilkan_data()


# Arman - ringkasan omset
def buka_ringkasan():
    win_ringkasan = tk.Toplevel(root)
    win_ringkasan.title("Ringkasan Data & Omset Lapangan")
    win_ringkasan.geometry("700x400")

    tk.Label(win_ringkasan, text="STATISTIK & OMSET PER LAPANGAN", font=("Arial", 14, "bold")).pack(pady=10)

    tree = ttk.Treeview(win_ringkasan, columns=("Nama", "Jenis", "Jumlah_Sewa", "Total_Omset"), show="headings")
    tree.heading("Nama", text="Nama Lapangan")
    tree.heading("Jenis", text="Jenis Lapangan")
    tree.heading("Jumlah_Sewa", text="Total Kali Disewa (COUNT)")
    tree.heading("Total_Omset", text="Total Omset Pendapatan (SUM)")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    try:
        cursor = conn.cursor()
        sql = """
        SELECT 
            l.nama_lapangan, 
            l.jenis_lapangan, 
            COUNT(p.id_penyewaan) AS jumlah_disewa, 
            IFNULL(SUM(pb.total_bayar), 0) AS total_omset
        FROM lapangan l
        LEFT JOIN penyewaan p ON l.id_lapangan = p.id_lapangan
        LEFT JOIN pembayaran pb ON p.id_penyewaan = pb.id_penyewaan
        GROUP BY l.id_lapangan, l.nama_lapangan, l.jenis_lapangan
        """
        cursor.execute(sql)
        
        total_seluruh_omset = 0
        for row in cursor.fetchall():
            formatted_row = (row[0], row[1], row[2], f"Rp {row[3]:,}")
            tree.insert("", "end", values=formatted_row)
            total_seluruh_omset += int(row[3])

        lbl_total = tk.Label(win_ringkasan, text=f"Total Omset Seluruh Lapangan: Rp {total_seluruh_omset:,}", font=("Arial", 12, "bold"), fg="green")
        lbl_total.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Aldio - laporan
def buka_laporan():
    win_laporan = tk.Toplevel(root)
    win_laporan.title("Laporan Utama")
    win_laporan.geometry("800x500")

    tree = ttk.Treeview(win_laporan, columns=("ID", "Penyewa", "Lapangan", "Tanggal", "Jam", "Durasi", "Status", "Total"), show="headings")
    tree.heading("ID", text="ID"); tree.heading("Penyewa", text="Penyewa"); tree.heading("Lapangan", text="Lapangan")
    tree.heading("Tanggal", text="Tanggal"); tree.heading("Jam", text="Jam Mulai"); tree.heading("Durasi", text="Durasi"); tree.heading("Status", text="Status")
    tree.heading("Total", text="Total Bayar")
    tree.column("ID", width=40)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    try:
        cursor = conn.cursor()
        sql = """
        SELECT p.id_penyewaan, py.nama, l.nama_lapangan, p.tanggal_sewa, p.jam_mulai, p.durasi_jam, p.status_penyewaan, IFNULL(pb.total_bayar, 0)
        FROM penyewaan p
        JOIN penyewa py ON p.id_penyewa = py.id_penyewa
        JOIN lapangan l ON p.id_lapangan = l.id_lapangan
        LEFT JOIN pembayaran pb ON p.id_penyewaan = pb.id_penyewaan
        """
        cursor.execute(sql)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Error", str(e))


# afrizal - menu/window utama
root = tk.Tk()
root.title("Sistem Penyewaan Lapangan")
root.geometry("500x480")

judul = tk.Label(root, text="SISTEM PENYEWAAN LAPANGAN", font=("Arial", 16, "bold"))
judul.pack(pady=20)

btn_penyewa = tk.Button(root, text="Data Penyewa (Adam)", width=35, command=buka_penyewa)
btn_penyewa.pack(pady=5)

btn_lapangan = tk.Button(root, text="Data Lapangan", width=35, command=buka_lapangan)
btn_lapangan.pack(pady=5)

btn_penyewaan = tk.Button(root, text="Transaksi Penyewaan (Habibi)", width=35, command=buka_penyewaan)
btn_penyewaan.pack(pady=5)

btn_pembayaran = tk.Button(root, text="Pembayaran (Mahib)", width=35, command=buka_pembayaran)
btn_pembayaran.pack(pady=5)

btn_ringkasan = tk.Button(root, text="Ringkasan & Omset (Arman)", width=35, command=buka_ringkasan)
btn_ringkasan.pack(pady=5)

btn_laporan = tk.Button(root, text="Laporan Utama (Aldio)", width=35, command=buka_laporan)
btn_laporan.pack(pady=5)

btn_keluar = tk.Button(root, text="Keluar", width=35, bg="red", fg="white", command=root.destroy)
btn_keluar.pack(pady=15)

root.mainloop()