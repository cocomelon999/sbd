import tkinter as tk
from tkinter import ttk, messagebox

def buka_ringkasan(root, conn):
    win_ringkasan = tk.Toplevel(root)
    win_ringkasan.title("Ringkasan Omset")
    win_ringkasan.geometry("700x450")

    tree = ttk.Treeview(win_ringkasan, columns=("Lapangan", "Transaksi", "Omset"), show="headings")
    tree.heading("Lapangan", text="Nama Lapangan")
    tree.heading("Transaksi", text="Jumlah Transaksi")
    tree.heading("Omset", text="Total Omset")

    tree.column("Lapangan", width=250)
    tree.column("Transaksi", width=150)
    tree.column("Omset", width=200)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    lbl_total = tk.Label(win_ringkasan, text="", font=("Arial", 12, "bold"))
    lbl_total.pack(pady=10)

    try:
        cursor = conn.cursor()
        sql = """
        SELECT
            l.nama_lapangan,
            COUNT(pb.id_pembayaran) AS jumlah_transaksi,
            IFNULL(SUM(pb.total_bayar),0) AS total_omset
        FROM lapangan l
        LEFT JOIN penyewaan p ON l.id_lapangan = p.id_lapangan
        LEFT JOIN pembayaran pb ON p.id_penyewaan = pb.id_penyewaan
        GROUP BY l.nama_lapangan
        """
        cursor.execute(sql)
        total_omset_semua = 0

        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
            total_omset_semua += row[2]

        lbl_total.config(text=f"Total Omset Keseluruhan : Rp {total_omset_semua:,}")
    except Exception as e:
        messagebox.showerror("Error", str(e))