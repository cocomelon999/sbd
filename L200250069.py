import tkinter as tk
from tkinter import ttk, messagebox

# data penyewa
def buka_penyewa(root, conn):
    win_penyewa = tk.Toplevel(root)
    win_penyewa.title("Form Data Penyewa - Adam")
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
        selected = tree.selection() #memeriksa baris mana yg sedang dipilihh
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


#data lapangan
def buka_lapangan(root, conn):
    win_lapangan = tk.Toplevel(root)
    win_lapangan.title("Form Data Lapangan - Adam") 
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