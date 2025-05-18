import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, date
import json
import os
import uuid


DATA_FILE = "keuangan_peternakan_streamlit.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"jurnal_umum": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def tambah_jurnal_umum(data):
    st.subheader("Tambah Jurnal Umum")

    with st.form("form_jurnal"):
        tanggal = st.date_input("Tanggal", value=date.today())
        deskripsi = st.text_input("Deskripsi Transaksi")

        daftar_akun = [
            "Kas", "Bank", "Piutang", "Hutang",
            "Hutang Karyawan", "Hutang Pajak",
            "Penjualan Susu",  
            "Pendapatan dari Penjualan Perlengkapan",
            "Pendapatan dari Penjualan Tanah",
            "Pendapatan Saham",
            "Biaya Pakan", "Biaya Obat", "Biaya Listrik",
            "Biaya Air",
            "Beban Pokok Pendapatan", "Biaya Operasional",
            "Biaya Amortisasi Pajak", "Biaya Depresiasi Kendaraan", "Biaya Depresiasi Bangunan",
            "Biaya Pembelian Perlengkapan", "Biaya Pembelian Tanah",
            "Biaya Pembelian Kendaraan", "Biaya Pembelian Bangunan",
            "Biaya Dividen",
            "Persediaan"
        ]

        entri = []
        baris_entri = st.number_input("Jumlah Entri Akun", min_value=2, max_value=20, value=2, step=1)

        for i in range(baris_entri):
            st.markdown(f"*Entri {i+1}*")
            akun = st.selectbox(f"Akun {i+1}", daftar_akun, key=f"akun_{i}")
            debit = st.number_input(f"Debit {i+1} (Rp)", min_value=0.0, format="%.2f", key=f"debit_{i}")
            kredit = st.number_input(f"Kredit {i+1} (Rp)", min_value=0.0, format="%.2f", key=f"kredit_{i}")
            entri.append({"akun": akun, "debit": debit, "kredit": kredit})

        submit = st.form_submit_button("Simpan Jurnal")

        if submit:
            for idx, e in enumerate(entri):
                if e["debit"] > 0 and e["kredit"] > 0:
                    st.warning(f"Pada entri {idx+1}, kolom Debit dan Kredit tidak boleh diisi bersamaan.")
                    return

            total_debit = sum(e["debit"] for e in entri)
            total_kredit = sum(e["kredit"] for e in entri)
            if total_debit == 0 and total_kredit == 0:
                st.warning("Masukkan minimal satu nominal debit atau kredit.")
            elif abs(total_debit - total_kredit) > 0.01:
                st.warning(f"Total debit (Rp {total_debit:,.2f}) dan kredit (Rp {total_kredit:,.2f}) harus sama.")
            else:
                jurnal_baru = {
                    "id": str(uuid.uuid4()),
                    "tanggal": tanggal.strftime("%Y-%m-%d"),
                    "deskripsi": deskripsi.strip(),
                    "entri": [e for e in entri if e["debit"] > 0 or e["kredit"] > 0]
                }
                data["jurnal_umum"].append(jurnal_baru)
                save_data(data)
                st.success("Jurnal berhasil disimpan.")

def edit_jurnal_form(data, jurnal_id):
    jurnal = next((j for j in data["jurnal_umum"] if j["id"] == jurnal_id), None)
    if not jurnal:
        st.error("Jurnal tidak ditemukan.")
        return

    st.subheader("Edit Jurnal Umum")

    with st.form(f"form_edit_{jurnal_id}"):
        tanggal = st.date_input("Tanggal", datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date())
        deskripsi = st.text_input("Deskripsi Transaksi", value=jurnal["deskripsi"])

        daftar_akun = [
            "Kas", "Bank", "Piutang", "Hutang",
            "Hutang Karyawan", "Hutang Pajak",
            "Penjualan Susu",  
            "Pendapatan dari Penjualan Perlengkapan",
            "Pendapatan dari Penjualan Tanah",
            "Pendapatan Saham",
            "Biaya Pakan", "Biaya Obat", "Biaya Listrik",
            "Biaya Air",
            "Beban Pokok Pendapatan", "Biaya Operasional",
            "Biaya Amortisasi Pajak", "Biaya Depresiasi Kendaraan", "Biaya Depresiasi Bangunan",
            "Biaya Pembelian Perlengkapan", "Biaya Pembelian Tanah",
            "Biaya Pembelian Kendaraan", "Biaya Pembelian Bangunan",
            "Biaya Dividen",
            "Persediaan"
        ]

        baris_entri = len(jurnal["entri"])
        baris_entri = st.number_input("Jumlah Entri Akun", min_value=2, max_value=20, value=baris_entri, step=1)

        entri_baru = []
        for i in range(baris_entri):
            st.markdown(f"*Entri {i+1}*")
            akun_default = jurnal["entri"][i]["akun"] if i < len(jurnal["entri"]) else daftar_akun[0]
            debit_default = jurnal["entri"][i]["debit"] if i < len(jurnal["entri"]) else 0.0
            kredit_default = jurnal["entri"][i]["kredit"] if i < len(jurnal["entri"]) else 0.0

            akun = st.selectbox(f"Akun {i+1}", daftar_akun, index=daftar_akun.index(akun_default), key=f"edit_akun_{jurnal_id}_{i}")
            debit = st.number_input(f"Debit {i+1} (Rp)", min_value=0.0, format="%.2f", value=debit_default, key=f"edit_debit_{jurnal_id}_{i}")
            kredit = st.number_input(f"Kredit {i+1} (Rp)", min_value=0.0, format="%.2f", value=kredit_default, key=f"edit_kredit_{jurnal_id}_{i}")
            entri_baru.append({"akun": akun, "debit": debit, "kredit": kredit})

        submit = st.form_submit_button("Update Jurnal")

        if submit:
            for idx, e in enumerate(entri_baru):
                if e["debit"] > 0 and e["kredit"] > 0:
                    st.warning(f"Pada entri {idx+1}, kolom Debit dan Kredit tidak boleh diisi bersamaan.")
                    return

            total_debit = sum(e["debit"] for e in entri_baru)
            total_kredit = sum(e["kredit"] for e in entri_baru)
            if total_debit == 0 and total_kredit == 0:
                st.warning("Masukkan minimal satu nominal debit atau kredit.")
            elif abs(total_debit - total_kredit) > 0.01:
                st.warning(f"Total debit (Rp {total_debit:,.2f}) dan kredit (Rp {total_kredit:,.2f}) harus sama.")
            else:
                jurnal["tanggal"] = tanggal.strftime("%Y-%m-%d")
                jurnal["deskripsi"] = deskripsi.strip()
                jurnal["entri"] = [e for e in entri_baru if e["debit"] > 0 or e["kredit"] > 0]
                save_data(data)
                st.session_state.pop("edit_jurnal_id", None)
                st.success("Jurnal berhasil diperbarui.")
                st.experimental_rerun()

def lihat_jurnal_umum(data):
    st.subheader("Daftar Jurnal Umum")

    if "edit_jurnal_id" in st.session_state:
        edit_jurnal_form(data, st.session_state["edit_jurnal_id"])
        st.write("---")

    if not data["jurnal_umum"]:
        st.info("Belum ada jurnal umum.")
        return

    jurnal_urut = sorted(data["jurnal_umum"], key=lambda x: x["tanggal"], reverse=True)

    for jurnal in jurnal_urut:
        st.markdown(f"*Tanggal:* {jurnal['tanggal']}  |  *Deskripsi:* {jurnal['deskripsi']}")

        cols = st.columns([6, 1, 1])

        with cols[0]:
            st.write("| Akun | Debit (Rp) | Kredit (Rp) |")
            st.write("|-------|------------|-------------|")
            for e in jurnal["entri"]:
                st.write(f"| {e['akun']} | {e['debit']:,.2f} | {e['kredit']:,.2f} |")

        with cols[1]:
            if st.button("Edit", key=f"edit_{jurnal['id']}"):
                st.session_state["edit_jurnal_id"] = jurnal["id"]
                st.rerun()()

        with cols[2]:
            if st.button("Hapus", key=f"hapus_{jurnal['id']}"):
                data["jurnal_umum"] = [j for j in data["jurnal_umum"] if j["id"] != jurnal["id"]]
                save_data(data)
                st.success("Jurnal berhasil dihapus.")
                st.experimental_rerun()

def buku_besar(data):
    st.subheader("Buku Besar")

    if not data["jurnal_umum"]:
        st.info("Belum ada data jurnal umum.")
        return

    akun_set = set()
    for jurnal in data["jurnal_umum"]:
        for e in jurnal["entri"]:
            akun_set.add(e["akun"])
    daftar_akun = sorted(list(akun_set))

    akun_terpilih = st.selectbox("Pilih Akun", daftar_akun)

    jurnal_sorted = sorted(data["jurnal_umum"], key=lambda x: x["tanggal"])
    tgl_awal_default = datetime.strptime(jurnal_sorted[0]["tanggal"], "%Y-%m-%d").date() if jurnal_sorted else date.today()
    col1, col2 = st.columns(2)
    with col1:
        tgl_mulai = st.date_input("Dari Tanggal", value=tgl_awal_default)
    with col2:
        tgl_akhir = st.date_input("Sampai Tanggal", value=date.today())

    if tgl_akhir < tgl_mulai:
        st.warning("Tanggal akhir harus sama atau setelah tanggal mulai.")
        return

    entri_akun = []
    for jurnal in data["jurnal_umum"]:
        tgl = datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date()
        if not (tgl_mulai <= tgl <= tgl_akhir):
            continue
        for e in jurnal["entri"]:
            if e["akun"] == akun_terpilih:
                entri_akun.append({
                    "tanggal": jurnal["tanggal"],
                    "deskripsi": jurnal["deskripsi"],
                    "debit": e["debit"],
                    "kredit": e["kredit"]
                })

    if not entri_akun:
        st.warning(f"Tidak ada mutasi pada akun '{akun_terpilih}' untuk periode ini.")
        return

    saldo = 0.0
    rows = []
    for e in sorted(entri_akun, key=lambda x: x["tanggal"]):
        saldo += e["debit"] - e["kredit"]
        rows.append({
            "Tanggal": e["tanggal"],
            "Deskripsi": e["deskripsi"],
            "Debit": f"Rp {e['debit']:,.2f}" if e["debit"] else "",
            "Kredit": f"Rp {e['kredit']:,.2f}" if e["kredit"] else "",
            "Saldo": f"Rp {saldo:,.2f}"
        })

    st.markdown(f"### Mutasi Akun: {akun_terpilih}")
    st.table(rows)

def neraca_saldo(data):
    st.subheader("Neraca Saldo")

    if not data["jurnal_umum"]:
        st.info("Belum ada data jurnal umum.")
        return

    jurnal_sorted = sorted(data["jurnal_umum"], key=lambda x: x["tanggal"])
    tgl_awal_default = datetime.strptime(jurnal_sorted[0]["tanggal"], "%Y-%m-%d").date() if jurnal_sorted else date.today()
    col1, col2 = st.columns(2)
    with col1:
        tgl_mulai = st.date_input("Dari Tanggal", value=tgl_awal_default)
    with col2:
        tgl_akhir = st.date_input("Sampai Tanggal", value=date.today())

    if tgl_akhir < tgl_mulai:
        st.warning("Tanggal akhir harus sama atau setelah tanggal mulai.")
        return

    akun_set = set()
    for jurnal in data["jurnal_umum"]:
        for e in jurnal["entri"]:
            akun_set.add(e["akun"])

    saldo_per_akun = {}
    for akun in akun_set:
        saldo_per_akun[akun] = {"debit": 0.0, "kredit": 0.0}

    for jurnal in data["jurnal_umum"]:
        tgl = datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date()
        if not (tgl_mulai <= tgl <= tgl_akhir):
            continue
        for e in jurnal["entri"]:
            saldo_per_akun[e["akun"]]["debit"] += e["debit"]
            saldo_per_akun[e["akun"]]["kredit"] += e["kredit"]

    rows = []
    total_debit = 0.0
    total_kredit = 0.0

    for akun in sorted(saldo_per_akun.keys()):
        debit = saldo_per_akun[akun]["debit"]
        kredit = saldo_per_akun[akun]["kredit"]
        saldo = debit - kredit

        saldo_debit = saldo if saldo > 0 else 0
        saldo_kredit = -saldo if saldo < 0 else 0

        total_debit += saldo_debit
        total_kredit += saldo_kredit

        rows.append({
            "Akun": akun,
            "Saldo Debit (Rp)": f"Rp {saldo_debit:,.2f}" if saldo_debit else "",
            "Saldo Kredit (Rp)": f"Rp {saldo_kredit:,.2f}" if saldo_kredit else ""
        })

    st.table(rows)
    st.markdown("---")
    st.write(f"*Total Saldo Debit:* Rp {total_debit:,.2f}")
    st.write(f"*Total Saldo Kredit:* Rp {total_kredit:,.2f}")

    if abs(total_debit - total_kredit) > 0.01:
        st.error("⚠ Neraca Saldo tidak seimbang! Total Debit tidak sama dengan Total Kredit.")
    else:
        st.success("Neraca Saldo seimbang (Total Debit = Total Kredit).")

def laporan_laba_rugi(data):
    st.subheader("Proyeksi Laporan Laba Rugi")
    st.markdown("Untuk Periode yang berakhir")

    jurnal_sorted = sorted(data["jurnal_umum"], key=lambda x: x["tanggal"])
    if not jurnal_sorted:
        st.info("Belum ada data jurnal umum.")
        return

    tgl_awal_default = datetime.strptime(jurnal_sorted[0]["tanggal"], "%Y-%m-%d").date()
    col1, col2 = st.columns(2)
    with col1:
        tgl_mulai = st.date_input("Dari Tanggal", value=tgl_awal_default)
    with col2:
        tgl_akhir = st.date_input("Sampai Tanggal", value=date.today())

    if tgl_akhir < tgl_mulai:
        st.warning("Tanggal akhir harus sama atau setelah tanggal mulai.")
        return

    akun_pendapatan = {
        "Penjualan Susu",
        "Pendapatan dari Penjualan Perlengkapan",
        "Pendapatan dari Penjualan Tanah",
        "Pendapatan Saham"
    }

    akun_harga_pokok_penjualan = {
        "Beban Pokok Pendapatan",
    }
    akun_beban = {
        "Biaya Pakan",
        "Biaya Obat",
        "Biaya Listrik",
        "Biaya Air",
        "Biaya Operasional",
        "Biaya Amortisasi Pajak",
        "Biaya Depresiasi Kendaraan",
        "Biaya Depresiasi Bangunan"
    }

    total_pendapatan = 0.0
    total_persediaan_awal = 0.0
    total_persediaan_akhir = 0.0
    total_harga_pokok_penjualan = 0.0
    total_beban = 0.0

    for jurnal in data["jurnal_umum"]:
        tgl = datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date()
        for e in jurnal["entri"]:
            akun = e["akun"]
            debit = e["debit"]
            kredit = e["kredit"]

            if akun == "Persediaan":
                if tgl < tgl_mulai:
                    total_persediaan_awal += debit - kredit
                elif tgl <= tgl_akhir:
                    total_persediaan_akhir += debit - kredit

    for jurnal in data["jurnal_umum"]:
        tgl = datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date()
        if not (tgl_mulai <= tgl <= tgl_akhir):
            continue
        for e in jurnal["entri"]:
            akun = e["akun"]
            debit = e["debit"]
            kredit = e["kredit"]

            if akun in akun_pendapatan:
                total_pendapatan += kredit - debit
            elif akun in akun_harga_pokok_penjualan:
                total_harga_pokok_penjualan += debit - kredit
            elif akun in akun_beban:
                total_beban += debit - kredit

    hpp = total_harga_pokok_penjualan + total_persediaan_awal - total_persediaan_akhir
    laba_kotor = total_pendapatan - hpp
    laba_rugi_bersih = laba_kotor - total_beban

    laba_str = f"Rp {abs(laba_rugi_bersih):,.2f}"
    if laba_rugi_bersih >= 0:
        warna = "green"
        status = "Laba Bersih"
    else:
        warna = "red"
        status = "Rugi Bersih"

    laporan_md = f"""
| Keterangan                                         | Nilai (Rp)           |
|---------------------------------------------------|----------------------|
| *Pendapatan*                                     |                      |
| {'<br>'.join(akun_pendapatan)}                    |                      |
| Total Pendapatan                                   | Rp {total_pendapatan:,.2f}   |
|                                                   |                      |
| *Persediaan Awal*                                | Rp {total_persediaan_awal:,.2f}   |
| *Pembelian (Beban Pokok Pendapatan)*            | Rp {total_harga_pokok_penjualan:,.2f}   |
| *Persediaan Akhir*                               | Rp {total_persediaan_akhir:,.2f}   |
| *Harga Pokok Penjualan (HPP)*                    | *Rp {hpp:,.2f}*   |
| *Laba Kotor*                                     | *Rp {laba_kotor:,.2f}* |
|                                                   |                      |
| *Beban*                                          |                      |
| Total Beban                                        | Rp {total_beban:,.2f}   |
|                                                   |                      |
| <span style="color:{warna};"><b>Proyeksi {status}</b></span> | <span style="color:{warna};"><b>{laba_str}</b></span>   |
"""
    st.markdown(laporan_md, unsafe_allow_html=True)

def laporan_arus_kas_terperinci(data):
    st.subheader("Laporan Arus Kas Terperinci")
    st.markdown("Laporan arus kas berdasarkan aktivitas operasi, investasi, dan pendanaan")

    if not data["jurnal_umum"]:
        st.info("Belum ada data jurnal umum.")
        return

    jurnal_sorted = sorted(data["jurnal_umum"], key=lambda x: x["tanggal"])
    tgl_awal_default = datetime.strptime(jurnal_sorted[0]["tanggal"], "%Y-%m-%d").date()
    col1, col2 = st.columns(2)
    with col1:
        tgl_mulai = st.date_input("Dari Tanggal", value=tgl_awal_default)
    with col2:
        tgl_akhir = st.date_input("Sampai Tanggal", value=date.today())

    if tgl_akhir < tgl_mulai:
        st.warning("Tanggal akhir harus sama atau setelah tanggal mulai.")
        return

    aktivitas_operasi = {
        "Pendapatan Bersih": ["Penjualan Susu", "Pendapatan dari Penjualan Perlengkapan", "Pendapatan dari Penjualan Tanah"],
        "Kenaikan Piutang": ["Piutang"],
        "Kenaikan Utang Usaha": ["Hutang"],
        "Kenaikan Utang Karyawan": ["Hutang Karyawan"],
        "Kenaikan Utang Pajak": ["Hutang Pajak"],
        "Keuntungan Dari Penjualan Perlengkapan": ["Pendapatan dari Penjualan Perlengkapan"],
        "Keuntungan Dari Penjualan Tanah": ["Pendapatan dari Penjualan Tanah"],
        "Beban Amortisasi Pajak": ["Biaya Amortisasi Pajak"],
        "Beban Depresiasi Kendaraan": ["Biaya Depresiasi Kendaraan"],
        "Beban Depresiasi Bangunan": ["Biaya Depresiasi Bangunan"],
        "Biaya Pakan": ["Biaya Pakan"],
        "Biaya Obat": ["Biaya Obat"],
        "Biaya Listrik": ["Biaya Listrik"],
        "Biaya Air": ["Biaya Air"],
        "Biaya Operasional": ["Biaya Operasional"]
    }

    aktivitas_investasi = {
        "Penjualan Perlengkapan": ["Pendapatan dari Penjualan Perlengkapan"],
        "Pembelian Perlengkapan": ["Biaya Pembelian Perlengkapan"],
        "Penjualan Tanah": ["Pendapatan dari Penjualan Tanah"],
        "Pembelian Tanah": ["Biaya Pembelian Tanah"],
        "Pembelian Kendaraan": ["Biaya Pembelian Kendaraan"],
        "Pembelian Bangunan": ["Biaya Pembelian Bangunan"]
    }

    aktivitas_pendanaan = {
        "Pembayaran Dividen": ["Biaya Dividen"],
        "Penerbitan Saham Biasa": ["Pendapatan Saham"]
    }

    def hitung_saldo(grup_akun):
        saldo_total = 0.0
        perinci = {k: 0.0 for k in grup_akun.keys()}

        for jurnal in data["jurnal_umum"]:
            tgl = datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date()
            if not (tgl_mulai <= tgl <= tgl_akhir):
                continue
            for e in jurnal["entri"]:
                for nama_aktivitas, akun_list in grup_akun.items():
                    if e["akun"] in akun_list:
                        arus = e["kredit"] - e["debit"]
                        perinci[nama_aktivitas] += arus
                        saldo_total += arus
        return saldo_total, perinci

    def tampilkan_tabel(judul, detail, total):
        st.markdown(f"### Aktivitas {judul}")
        if not any(nilai != 0 for nilai in detail.values()):
            st.info(f"Tidak ada transaksi pada aktivitas {judul}.")
            return

        df = pd.DataFrame({
            "Kategori": list(detail.keys()),
            "Jumlah (Rp)": [f"{v:,.2f}" for v in detail.values()]
        })
        st.table(df)

        label = "Kas Diterima" if total >= 0 else "Kas Digunakan"
        st.markdown(f"{label} dari Aktivitas {judul}:** Rp {total:,.2f}")

    saldo_op, detail_op = hitung_saldo(aktivitas_operasi)
    saldo_inv, detail_inv = hitung_saldo(aktivitas_investasi)
    saldo_pen, detail_pen = hitung_saldo(aktivitas_pendanaan)

    tampilkan_tabel("Operasi", detail_op, saldo_op)
    tampilkan_tabel("Investasi", detail_inv, saldo_inv)
    tampilkan_tabel("Pendanaan", detail_pen, saldo_pen)

    akun_kas = {"Kas", "Bank"}
    kas_awal = 0.0
    kas_akhir = 0.0
    for jurnal in data["jurnal_umum"]:
        tgl = datetime.strptime(jurnal["tanggal"], "%Y-%m-%d").date()
        for e in jurnal["entri"]:
            if e["akun"] in akun_kas:
                if tgl < tgl_mulai:
                    kas_awal += e["debit"] - e["kredit"]
                if tgl <= tgl_akhir:
                    kas_akhir += e["debit"] - e["kredit"]

    kas_bersih = saldo_op + saldo_inv + saldo_pen

    st.markdown("---")
    st.write(f"*Kas Awal Periode ({tgl_mulai}):* Rp {kas_awal:,.2f}")
    st.write(f"*Kas Bersih dari Semua Aktivitas:* Rp {kas_bersih:,.2f}")
    st.write(f"*Kas Akhir Periode ({tgl_akhir}):* Rp {kas_akhir:,.2f}")

def logout():
    st.session_state['login_status'] = False
    st.rerun()()

def main():
    st.set_page_config(page_title="Sistem Akuntansi Peternakan", layout="wide")
	
	

    if 'login_status' not in st.session_state:
        st.session_state['login_status'] = False

    if not st.session_state['login_status']:
        st.title("Login Sistem Akuntansi Peternakan")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "sapiperahungaran" and password == "ungaran1991":
                st.session_state['login_status'] = True
                st.rerun()()
            else:
                st.error("Username / Password salah!")
        return

    data = load_data()

    menu = st.sidebar.selectbox("Menu", [
        "Tambah Jurnal Umum",
        "Lihat Jurnal Umum",
        "Buku Besar",
        "Neraca Saldo",
        "Laporan Laba Rugi",
        "Laporan Arus Kas",
        "Logout"
    ])

    if menu == "Tambah Jurnal Umum":
        tambah_jurnal_umum(data)
    elif menu == "Lihat Jurnal Umum":
        if "edit_jurnal_id" in st.session_state:
            edit_jurnal_form(data, st.session_state["edit_jurnal_id"])
            st.write("---")
        else:
            lihat_jurnal_umum(data)
    elif menu == "Buku Besar":
        buku_besar(data)
    elif menu == "Neraca Saldo":
        neraca_saldo(data)
    elif menu == "Laporan Laba Rugi":
        laporan_laba_rugi(data)
    elif menu == "Laporan Arus Kas":
        laporan_arus_kas_terperinci(data)
    elif menu == "Logout":
        logout()


if __name__ == "__main__":
    main()