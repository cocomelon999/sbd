import tkinter as tk
from koneksi import connect_db 

import L200250069 as adam
import L200250050 as habibi
import L200250187 as mahib
import L200250070 as arman
import L200250138 as aldio

# Koneksi Database Utama
conn = connect_db()

root = tk.Tk()
root.title("Sistem Penyewaan Lapangan")
root.geometry("500x480")

judul = tk.Label(root, text="SISTEM PENYEWAAN LAPANGAN", font=("Arial", 16, "bold"))
judul.pack(pady=20)

# Menghubungkan tombol ke modul NIM masing-masing anak
btn_penyewa = tk.Button(root, text="Data Penyewa (Adam)", width=40, 
                        command=lambda: adam.buka_penyewa(root, conn))
btn_penyewa.pack(pady=5)

btn_lapangan = tk.Button(root, text="Data Lapangan (Adam)", width=40, 
                         command=lambda: adam.buka_lapangan(root, conn))
btn_lapangan.pack(pady=5)

btn_penyewaan = tk.Button(root, text="Transaksi Penyewaan (Habibi)", width=40, 
                          command=lambda: habibi.buka_penyewaan(root, conn))
btn_penyewaan.pack(pady=5)

btn_pembayaran = tk.Button(root, text="Pembayaran (Mahib)", width=40, 
                           command=lambda: mahib.buka_pembayaran(root, conn))
btn_pembayaran.pack(pady=5)

btn_ringkasan = tk.Button(root, text="Ringkasan & Omset (Arman)", width=40, 
                          command=lambda: arman.buka_ringkasan(root, conn))
btn_ringkasan.pack(pady=5)

btn_laporan = tk.Button(root, text="Laporan Utama (Aldio)", width=40, 
                        command=lambda: aldio.buka_laporan(root, conn))
btn_laporan.pack(pady=5)

btn_keluar = tk.Button(root, text="Keluar", width=40, bg="red", fg="white", command=root.destroy)
btn_keluar.pack(pady=15)

root.mainloop()