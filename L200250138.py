import tkinter as tk
from tkinter import ttk, messagebox

def buka_laporan(root, conn):
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