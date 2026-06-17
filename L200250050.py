import tkinter as tk
from tkinter import ttk, messagebox

def buka_penyewaan(root, conn):
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