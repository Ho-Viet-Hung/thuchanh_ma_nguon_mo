import numpy as np
import tkinter as tk
from tkinter import messagebox


def giai_he_pttt():
    try:
        n = int(nhap_n.get())
        phuong_trinh = []
        for i in range(n):
            pt = []
            for j in range(n):
                pt.append(float(nhap_bien[i][j].get()))
            phuong_trinh.append(pt)

        he_so = np.array(phuong_trinh)
        hang_so = np.array([float(nhap_hang_so[i].get()) for i in range(n)])

        ket_qua = np.linalg.solve(he_so, hang_so)

        ket_qua_text.delete(1.0, tk.END)
        ket_qua_text.insert(tk.END, "Nghiệm của hệ:\n{}".format(ket_qua))
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


def reset_fields():
    nhap_n.delete(0, tk.END)
    ket_qua_text.delete(1.0, tk.END)
    for khung_phuong_trinh in cua_so.winfo_children():
        if isinstance(khung_phuong_trinh, tk.Frame):
            khung_phuong_trinh.destroy()
    nhap_bien.clear()
    nhap_hang_so.clear()


def xoa_truong_phuong_trinh():
    for danh_sach_bien in nhap_bien:
        for nhap_bien_var in danh_sach_bien:
            nhap_bien_var.delete(0, tk.END)
    for nhap_hang_so_var in nhap_hang_so:
        nhap_hang_so_var.delete(0, tk.END)
    ket_qua_text.delete(1.0, tk.END)


def tao_cac_truong_phuong_trinh():
    try:
        ket_qua_text.delete(1.0, tk.END)
        for khung_phuong_trinh in cua_so.winfo_children():
            if isinstance(khung_phuong_trinh, tk.Frame):
                khung_phuong_trinh.destroy()
        nhap_bien.clear()
        nhap_hang_so.clear()

        n = int(nhap_n.get())
        nhap_bien.clear()
        nhap_hang_so.clear()

        for i in range(n):
            khung_phuong_trinh = tk.Frame(cua_so)
            khung_phuong_trinh.pack()

            danh_sach_bien = []
            for j in range(n):
                nhap_bien_var = tk.Entry(khung_phuong_trinh, width=5)
                nhap_bien_var.pack(side=tk.LEFT)
                danh_sach_bien.append(nhap_bien_var)

            nhap_bien.append(danh_sach_bien)

            nhan_hang_so = tk.Label(khung_phuong_trinh, text=" = ")
            nhan_hang_so.pack(side=tk.LEFT)

            nhap_hang_so_var = tk.Entry(khung_phuong_trinh, width=5)
            nhap_hang_so_var.pack(side=tk.LEFT)
            nhap_hang_so.append(nhap_hang_so_var)

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


# Tạo cửa sổ giao diện
cua_so = tk.Tk()
cua_so.title("Giải Hệ Phương Trình Tuyến Tính NHÓM 5")
cua_so.geometry("1000x1000")

# Nhập số hệ phương trình
nhan_n = tk.Label(cua_so, text="Nhập số hệ phương trình (n):")
nhan_n.pack()
nhap_n = tk.Entry(cua_so)
nhap_n.pack()

# Tạo danh sách các biến và hằng số
nhap_bien = []
nhap_hang_so = []

tao_button = tk.Button(cua_so, text="Tạo", command=tao_cac_truong_phuong_trinh)
tao_button.pack()

xoa_button = tk.Button(cua_so, text="Xóa", command=xoa_truong_phuong_trinh)
xoa_button.pack()

reset_button = tk.Button(cua_so, text="Reset", command=reset_fields)
reset_button.pack()

nut_giai = tk.Button(cua_so, text="Giải", command=giai_he_pttt)
nut_giai.pack()

# Kết quả
nhan_ket_qua = tk.Label(cua_so, text="Kết quả:")
nhan_ket_qua.pack()
ket_qua_text = tk.Text(cua_so, height=5, width=30)
ket_qua_text.pack()

# Chạy chương trình
cua_so.mainloop()