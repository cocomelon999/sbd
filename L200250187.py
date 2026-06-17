import tkinter as tk
from tkinter import ttk, messagebox

def buka_pembayaran(root, conn):
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