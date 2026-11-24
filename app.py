import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Sistem Pendukung Keputusan - SMART",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Helper function to remove leading spaces from HTML lines
# Preventing markdown from treating indented HTML as code blocks (<pre><code>)
def clean_html(html_str: str) -> str:
    return "".join(line.strip() for line in html_str.strip().splitlines())

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #1E293B;
        background-color: #F8FAFC;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }
    
    /* Header Navbar Banner */
    .smart-header {
        background: linear-gradient(105deg, #0D6938 0%, #15803D 55%, #16A34A 100%);
        border-radius: 12px;
        padding: 16px 22px;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(21, 128, 61, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .smart-header::after {
        content: "";
        position: absolute;
        right: -30px;
        top: -40px;
        width: 320px;
        height: 180px;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .header-icon-box {
        font-size: 2.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.15));
    }
    
    .header-title-text {
        font-size: 1.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    
    .header-subtitle-text {
        font-size: 0.9rem;
        color: #DCFCE7;
        margin: 2px 0 0 0;
        font-weight: 500;
    }
    
    .header-badge-pill {
        background-color: #064E26;
        color: #DCFCE7;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        display: flex;
        align-items: center;
        gap: 6px;
        border: 1px solid rgba(220, 252, 231, 0.3);
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Card Container */
    .dashboard-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    
    /* Mode Pill Indicator */
    .mode-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 14px;
    }
    
    .mode-input {
        background-color: #F1F5F9;
        color: #475569;
        border: 1px solid #CBD5E1;
    }
    
    .mode-result {
        background-color: #DCFCE7;
        color: #15803D;
        border: 1px solid #86EFAC;
    }
    
    /* Section Title with Green Circle Badge */
    .sec-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 2px;
    }
    
    .sec-badge {
        background-color: #15803D;
        color: #FFFFFF;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.88rem;
        font-weight: 800;
        flex-shrink: 0;
    }
    
    .sec-badge-result {
        background: linear-gradient(135deg, #15803D 0%, #047857 100%);
        color: #FFFFFF;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
        font-weight: 800;
        flex-shrink: 0;
        box-shadow: 0 2px 5px rgba(21, 128, 61, 0.2);
    }
    
    .sec-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
    }
    
    .sec-desc {
        color: #64748B;
        font-size: 0.82rem;
        margin: 2px 0 14px 38px;
        line-height: 1.4;
    }
    
    /* Table Styling */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        overflow: hidden;
        font-size: 0.84rem;
        background-color: #FFFFFF;
        margin: 4px 0 10px 0;
    }
    
    .custom-table th {
        background-color: #F1F5F9;
        color: #334155;
        font-weight: 700;
        padding: 8px 12px;
        text-align: left;
        border-bottom: 1px solid #E2E8F0;
    }
    
    .custom-table td {
        padding: 8px 12px;
        border-bottom: 1px solid #F1F5F9;
        color: #1E293B;
    }
    
    .custom-table tr:last-child td {
        border-bottom: none;
    }
    
    .custom-table tr.total-row td {
        background-color: #F8FAFC;
        font-weight: 700;
        border-top: 1.5px solid #CBD5E1;
        color: #0F172A;
    }
    
    /* Light Mint Info Card */
    .mint-card {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 10px;
        padding: 14px 16px;
        height: 100%;
    }
    
    .mint-card-title {
        color: #166534;
        font-weight: 700;
        font-size: 0.88rem;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 6px;
    }
    
    /* Total Bobot Box */
    .total-bobot-box {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 8px;
        padding: 12px 14px;
        text-align: center;
        margin-top: 14px;
    }
    
    /* Buttons */
    div.stButton > button {
        background-color: #15803D !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 0.86rem !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 7px 16px !important;
        transition: background-color 0.15s ease !important;
    }
    
    div.stButton > button:hover {
        background-color: #166534 !important;
        color: white !important;
    }
    
    /* Big Process Button */
    .big-process-btn div.stButton > button {
        background: linear-gradient(135deg, #15803D 0%, #166534 100%) !important;
        color: white !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        padding: 12px 28px !important;
        border-radius: 8px !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 12px rgba(21, 128, 61, 0.25) !important;
    }
    
    .big-process-btn div.stButton > button:hover {
        background: #166534 !important;
        box-shadow: 0 6px 16px rgba(21, 128, 61, 0.35) !important;
    }
    
    /* Secondary Action Button */
    .btn-secondary div.stButton > button {
        background-color: #F8FAFC !important;
        color: #475569 !important;
        border: 1px solid #CBD5E1 !important;
    }
    .btn-secondary div.stButton > button:hover {
        background-color: #F1F5F9 !important;
        color: #1E293B !important;
    }
    
    /* Delete Trash Button Styling */
    .delete-btn div.stButton > button {
        background-color: transparent !important;
        color: #EF4444 !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        font-size: 1.1rem !important;
        box-shadow: none !important;
        min-height: 32px !important;
        height: 32px !important;
        line-height: 32px !important;
    }
    
    .delete-btn div.stButton > button:hover {
        color: #DC2626 !important;
        background-color: #FEE2E2 !important;
        border-radius: 6px !important;
    }
    
    /* Table cell text vertical align */
    .cell-text {
        display: flex;
        align-items: center;
        height: 32px;
        font-size: 0.85rem;
    }
    
    /* Best Rank Pill */
    .badge-terbaik {
        background-color: #DCFCE7;
        color: #15803D;
        font-weight: 700;
        padding: 3px 12px;
        border-radius: 999px;
        font-size: 0.78rem;
        display: inline-block;
        border: 1px solid #86EFAC;
    }
    
    /* Winner Banner Card */
    .winner-card {
        background: linear-gradient(135deg, #15803D 0%, #047857 100%);
        border-radius: 12px;
        padding: 20px 24px;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        box-shadow: 0 6px 18px -2px rgba(21, 128, 61, 0.3);
    }
    
    .winner-title {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #DCFCE7;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .winner-name {
        font-size: 1.6rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0;
    }
    
    .winner-score {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 10px 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.25);
    }
    
    /* Bottom Conclusion Banner */
    .conclusion-banner {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 10px;
        padding: 14px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 14px;
        color: #166534;
        font-size: 0.92rem;
    }
    
    .conclusion-icon {
        width: 26px;
        height: 26px;
        background-color: #15803D;
        color: #FFFFFF;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.85rem;
        flex-shrink: 0;
    }
    
    /* Compact inputs */
    div[data-testid="stTextInput"] input, 
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        font-size: 0.86rem;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# INITIAL STATE INITIALIZATION
# ==========================================
def init_state():
    if 'has_calculated' not in st.session_state:
        st.session_state.has_calculated = False
        
    if 'calc_results' not in st.session_state:
        st.session_state.calc_results = None
        
    if 'calculated_snapshot' not in st.session_state:
        st.session_state.calculated_snapshot = None
        
    if 'input_changed_alert' not in st.session_state:
        st.session_state.input_changed_alert = False

    if 'alternatives' not in st.session_state:
        st.session_state.alternatives = [
            {"Kode": "A1", "Nama Alternatif": "Alternatif A"},
            {"Kode": "A2", "Nama Alternatif": "Alternatif B"},
            {"Kode": "A3", "Nama Alternatif": "Alternatif C"},
        ]
        
    if 'criteria' not in st.session_state:
        st.session_state.criteria = [
            {"Kode": "C1", "Nama Kriteria": "Harga", "Jenis": "Cost", "Bobot": 40.0},
            {"Kode": "C2", "Nama Kriteria": "Kualitas", "Jenis": "Benefit", "Bobot": 35.0},
            {"Kode": "C3", "Nama Kriteria": "Pelayanan", "Jenis": "Benefit", "Bobot": 25.0},
        ]
        
    if 'matrix_data' not in st.session_state:
        st.session_state.matrix_data = {
            "A1": {"C1": 50000.0, "C2": 90.0, "C3": 85.0},
            "A2": {"C1": 45000.0, "C2": 85.0, "C3": 90.0},
            "A3": {"C1": 55000.0, "C2": 95.0, "C3": 80.0},
        }

init_state()

# Helper to invalidate calculation when inputs change
def invalidate_calculation():
    if st.session_state.has_calculated:
        st.session_state.has_calculated = False
        st.session_state.calc_results = None
        st.session_state.input_changed_alert = True

# Helper to compute input snapshot signature
def get_input_snapshot():
    alts_sig = tuple((a["Kode"], a["Nama Alternatif"]) for a in st.session_state.alternatives)
    crits_sig = tuple((c["Kode"], c["Nama Kriteria"], c["Jenis"], c["Bobot"]) for c in st.session_state.criteria)
    matrix_sig = tuple(sorted((k, tuple(sorted(v.items()))) for k, v in st.session_state.matrix_data.items()))
    return (alts_sig, crits_sig, matrix_sig)

# Sync matrix keys
for alt in st.session_state.alternatives:
    code = alt["Kode"]
    if code not in st.session_state.matrix_data:
        st.session_state.matrix_data[code] = {}
    for crit in st.session_state.criteria:
        c_code = crit["Kode"]
        if c_code not in st.session_state.matrix_data[code]:
            st.session_state.matrix_data[code][c_code] = 50.0

# ==========================================
# TOP NAVBAR / HEADER
# ==========================================
st.markdown(clean_html("""
<div class="smart-header">
    <div class="header-left">
        <div class="header-icon-box">⚖️</div>
        <div>
            <h1 class="header-title-text">Sistem Pendukung Keputusan</h1>
            <p class="header-subtitle-text">06TPLP002</p>
            <p class="header-subtitle-text">KELOMPOK 1</p>
            <p class="header-subtitle-text">Metode SMART (Simple Multi-Attribute Rating Technique)</p>
        </div>
    </div>
    <div class="header-badge-pill">
        📊 SPK SMART
    </div>
</div>
"""), unsafe_allow_html=True)

# Mode Indicator Banner
if st.session_state.has_calculated:
    st.markdown(clean_html("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div class="mode-indicator mode-result">
            <span>●</span> <span>RESULT MODE: Perhitungan SMART Selesai</span>
        </div>
        <div style="font-size: 0.82rem; color: #64748B;">
            Tahapan perhitungan dan hasil ranking ditampilkan di bawah bagian input.
        </div>
    </div>
    """), unsafe_allow_html=True)
else:
    st.markdown(clean_html("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div class="mode-indicator mode-input">
            <span>○</span> <span>INPUT MODE: Silakan Masukkan & Sesuaikan Data</span>
        </div>
        <div style="font-size: 0.82rem; color: #64748B;">
            Hasil perhitungan akan ditampilkan setelah tombol 'Proses Perhitungan SMART' ditekan.
        </div>
    </div>
    """), unsafe_allow_html=True)

if st.session_state.input_changed_alert:
    st.warning("⚠️ Data input telah diperbarui. Hasil perhitungan lama tidak berlaku. Silakan klik **Proses Perhitungan SMART** untuk menghitung ulang.")
    st.session_state.input_changed_alert = False

# =========================================================================
# BAGIAN INPUT DATA (SELALU DITAMPILKAN DI ATAS)
# =========================================================================

# -------------------------------------------------------------------------
# BARIS INPUT 1: (1) Data Alternatif & (2) Data Kriteria
# -------------------------------------------------------------------------
r1_col1, r1_col2 = st.columns(2, gap="medium")

# 1. Data Alternatif
with r1_col1:
    st.markdown(clean_html("""
    <div class="dashboard-card">
        <div class="sec-header">
            <div class="sec-badge">1</div>
            <h3 class="sec-title">Data Alternatif</h3>
        </div>
        <div class="sec-desc">
            Alternatif merupakan objek atau pilihan yang akan dievaluasi.
        </div>
    """), unsafe_allow_html=True)
    
    in_alt_col, tbl_alt_col = st.columns([1.1, 1.4], gap="small")
    
    with in_alt_col:
        next_alt_idx = len(st.session_state.alternatives) + 1
        alt_code_val = f"A{next_alt_idx}"
        in_kode_alt = st.text_input("Kode Alternatif", value=alt_code_val, key="input_kode_alt")
        in_nama_alt = st.text_input("Nama Alternatif", value=f"Alternatif {chr(64 + next_alt_idx)}", key="input_nama_alt")
        
        if st.button("+ Tambah Alternatif", key="btn_add_alt", use_container_width=True):
            if in_kode_alt.strip() and in_nama_alt.strip():
                if any(a["Kode"] == in_kode_alt.strip() for a in st.session_state.alternatives):
                    st.error(f"Kode '{in_kode_alt.strip()}' sudah ada!")
                else:
                    st.session_state.alternatives.append({
                        "Kode": in_kode_alt.strip(),
                        "Nama Alternatif": in_nama_alt.strip()
                    })
                    invalidate_calculation()
                    st.rerun()
            else:
                st.warning("Semua kolom harus diisi.")
                
    with tbl_alt_col:
        alt_rows_html = ""
        for i, alt in enumerate(st.session_state.alternatives):
            alt_rows_html += f"<tr><td>{i+1}</td><td style='font-weight:600;'>{alt['Kode']}</td><td>{alt['Nama Alternatif']}</td></tr>"
        st.markdown(clean_html(f"""
        <table class="custom-table">
            <thead>
                <tr><th>No</th><th>Kode</th><th>Nama Alternatif</th></tr>
            </thead>
            <tbody>{alt_rows_html}</tbody>
        </table>
        """), unsafe_allow_html=True)

        alt_options = [f"{a['Kode']} - {a['Nama Alternatif']}" for a in st.session_state.alternatives]
        sel_del_alt = st.selectbox("Pilih alternatif untuk dihapus", alt_options, key="sel_del_alt", label_visibility="collapsed")
        if st.button("🗑️ Hapus Alternatif Terpilih", key="btn_del_alt_sel", use_container_width=True):
            if len(st.session_state.alternatives) <= 2:
                st.error("Minimal harus terdapat 2 alternatif.")
            else:
                del_alt_idx = alt_options.index(sel_del_alt)
                removed_code = st.session_state.alternatives[del_alt_idx]["Kode"]
                st.session_state.alternatives.pop(del_alt_idx)
                if removed_code in st.session_state.matrix_data:
                    del st.session_state.matrix_data[removed_code]
                invalidate_calculation()
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# 2. Data Kriteria
with r1_col2:
    st.markdown(clean_html("""
    <div class="dashboard-card">
        <div class="sec-header">
            <div class="sec-badge">2</div>
            <h3 class="sec-title">Data Kriteria</h3>
        </div>
        <div class="sec-desc">
            Kriteria adalah faktor penilaian yang digunakan untuk evaluasi.
        </div>
    """), unsafe_allow_html=True)
    
    in_crit_col, tbl_crit_col = st.columns([1.1, 1.4], gap="small")
    
    with in_crit_col:
        next_crit_idx = len(st.session_state.criteria) + 1
        crit_code_val = f"C{next_crit_idx}"
        in_kode_crit = st.text_input("Kode Kriteria", value=crit_code_val, key="input_kode_crit")
        in_nama_crit = st.text_input("Nama Kriteria", value="", placeholder="Contoh: Garansi", key="input_nama_crit")
        in_jenis_crit = st.selectbox("Jenis Kriteria", ["Benefit", "Cost"], index=0, key="input_jenis_crit")
        
        if st.button("+ Tambah Kriteria", key="btn_add_crit", use_container_width=True):
            if in_kode_crit.strip() and in_nama_crit.strip():
                if any(c["Kode"] == in_kode_crit.strip() for c in st.session_state.criteria):
                    st.error(f"Kode '{in_kode_crit.strip()}' sudah ada!")
                else:
                    st.session_state.criteria.append({
                        "Kode": in_kode_crit.strip(),
                        "Nama Kriteria": in_nama_crit.strip(),
                        "Jenis": in_jenis_crit,
                        "Bobot": 20.0
                    })
                    invalidate_calculation()
                    st.rerun()
            else:
                st.warning("Semua kolom harus diisi.")
                
    with tbl_crit_col:
        crit_rows_html = ""
        for i, crit in enumerate(st.session_state.criteria):
            crit_rows_html += f"<tr><td>{i+1}</td><td style='font-weight:600;'>{crit['Kode']}</td><td>{crit['Nama Kriteria']}</td><td>{crit['Jenis']}</td></tr>"
        st.markdown(clean_html(f"""
        <table class="custom-table">
            <thead>
                <tr><th>No</th><th>Kode</th><th>Nama Kriteria</th><th>Jenis</th></tr>
            </thead>
            <tbody>{crit_rows_html}</tbody>
        </table>
        """), unsafe_allow_html=True)

        crit_options = [f"{c['Kode']} - {c['Nama Kriteria']}" for c in st.session_state.criteria]
        sel_del_crit = st.selectbox("Pilih kriteria untuk dihapus", crit_options, key="sel_del_crit", label_visibility="collapsed")
        if st.button("🗑️ Hapus Kriteria Terpilih", key="btn_del_crit_sel", use_container_width=True):
            if len(st.session_state.criteria) <= 1:
                st.error("Minimal harus terdapat 1 kriteria.")
            else:
                del_crit_idx = crit_options.index(sel_del_crit)
                removed_crit = st.session_state.criteria[del_crit_idx]["Kode"]
                st.session_state.criteria.pop(del_crit_idx)
                for alt_code in st.session_state.matrix_data:
                    if removed_crit in st.session_state.matrix_data[alt_code]:
                        del st.session_state.matrix_data[alt_code][removed_crit]
                invalidate_calculation()
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# BARIS INPUT 2: (3) Pembobotan Kriteria & (4) Matriks Penilaian
# -------------------------------------------------------------------------
r2_col1, r2_col2 = st.columns([1, 1.4], gap="medium")

# 3. Pembobotan Kriteria
with r2_col1:
    st.markdown(clean_html("""
    <div class="dashboard-card" style="height: 100%;">
        <div class="sec-header">
            <div class="sec-badge">3</div>
            <h3 class="sec-title">Pembobotan Kriteria</h3>
        </div>
        <div class="sec-desc">
            Tentukan tingkat kepentingan setiap kriteria (bobot awal).
        </div>
    """), unsafe_allow_html=True)
    
    for i, crit in enumerate(st.session_state.criteria):
        lbl_col, inp_col = st.columns([1.5, 1.5])
        lbl_col.markdown(f"<div style='padding-top:6px; font-weight:600; font-size:0.9rem;'>{crit['Kode']} - {crit['Nama Kriteria']}</div>", unsafe_allow_html=True)
        old_val = float(crit.get("Bobot", 20.0))
        new_w = inp_col.number_input(
            label=f"Bobot {crit['Kode']}",
            min_value=0.01,
            max_value=1000.0,
            value=old_val,
            step=5.0,
            key=f"weight_inp_{crit['Kode']}",
            label_visibility="collapsed"
        )
        if new_w != old_val:
            st.session_state.criteria[i]["Bobot"] = new_w
            invalidate_calculation()

    total_bobot_awal = sum(c["Bobot"] for c in st.session_state.criteria)
    
    st.markdown(clean_html(f"""
    <div class="total-bobot-box">
        <div style="font-size: 0.85rem; font-weight: 700; color: #166534;">Total Bobot Awal:</div>
        <div style="font-size: 1.45rem; font-weight: 800; color: #15803D; margin-top:2px;">{total_bobot_awal:.0f}</div>
    </div>
    </div>
    """), unsafe_allow_html=True)

# 4. Matriks Penilaian
with r2_col2:
    st.markdown(clean_html("""
    <div class="dashboard-card" style="height: 100%;">
        <div class="sec-header">
            <div class="sec-badge">4</div>
            <h3 class="sec-title">Matriks Penilaian Alternatif</h3>
        </div>
        <div class="sec-desc">
            Masukkan dan sesuaikan nilai masing-masing alternatif pada tabel di bawah:
        </div>
    """), unsafe_allow_html=True)
    
    matrix_rows = []
    for alt in st.session_state.alternatives:
        code = alt["Kode"]
        row_dict = {"Alternatif": code}
        for c in st.session_state.criteria:
            c_code = c["Kode"]
            c_col_name = f"{c['Nama Kriteria']} ({c['Jenis']})"
            val = st.session_state.matrix_data.get(code, {}).get(c_code, 50.0)
            row_dict[c_col_name] = float(val)
        matrix_rows.append(row_dict)
        
    df_input = pd.DataFrame(matrix_rows)
    
    edited_matrix = st.data_editor(
        df_input,
        disabled=["Alternatif"],
        use_container_width=True,
        hide_index=True,
        key="smart_matrix_editor"
    )
    
    # Detect changes in matrix
    matrix_has_changed = False
    for _, r in edited_matrix.iterrows():
        a_code = r["Alternatif"]
        if a_code not in st.session_state.matrix_data:
            st.session_state.matrix_data[a_code] = {}
        for c in st.session_state.criteria:
            c_code = c["Kode"]
            c_col_name = f"{c['Nama Kriteria']} ({c['Jenis']})"
            curr_val = float(r[c_col_name])
            if st.session_state.matrix_data[a_code].get(c_code) != curr_val:
                st.session_state.matrix_data[a_code][c_code] = curr_val
                matrix_has_changed = True
                
    if matrix_has_changed:
        invalidate_calculation()

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# TOMBOL PROSES PERHITUNGAN SMART / CONTROL BAR
# -------------------------------------------------------------------------
st.write("")
col_btn_center, col_btn_right = st.columns([3, 1])

with col_btn_center:
    st.markdown("<div class='big-process-btn'>", unsafe_allow_html=True)
    if st.button("▶ PROSES PERHITUNGAN SMART", key="btn_run_smart", use_container_width=True):
        # 1. Validation
        valid = True
        if len(st.session_state.alternatives) < 2:
            st.error("⚠️ Validasi Gagal: Minimal harus terdapat 2 alternatif untuk dievaluasi.")
            valid = False
        elif len(st.session_state.criteria) < 1:
            st.error("⚠️ Validasi Gagal: Minimal harus terdapat 1 kriteria penilaian.")
            valid = False
        elif any(c["Bobot"] <= 0 for c in st.session_state.criteria) or total_bobot_awal <= 0:
            st.error("⚠️ Validasi Gagal: Semua bobot kriteria harus bernilai lebih besar dari 0.")
            valid = False
            
        if valid:
            # 2. SMART Computation
            # Step A: Normalization of Weights
            norm_weights = {}
            for c in st.session_state.criteria:
                norm_weights[c["Kode"]] = c["Bobot"] / total_bobot_awal
                
            # Step B: Min & Max per Criteria
            crit_stats = {}
            for c in st.session_state.criteria:
                c_code = c["Kode"]
                vals = [st.session_state.matrix_data[a["Kode"]][c_code] for a in st.session_state.alternatives]
                c_min = min(vals)
                c_max = max(vals)
                crit_stats[c_code] = {
                    "min": c_min,
                    "max": c_max,
                    "diff": c_max - c_min,
                    "type": c["Jenis"]
                }
                
            # Step C: Utility Matrix Uij
            utility_matrix = {}
            utility_steps = {}
            for alt in st.session_state.alternatives:
                a_code = alt["Kode"]
                utility_matrix[a_code] = {}
                utility_steps[a_code] = {}
                for c in st.session_state.criteria:
                    c_code = c["Kode"]
                    val = st.session_state.matrix_data[a_code][c_code]
                    c_min = crit_stats[c_code]["min"]
                    c_max = crit_stats[c_code]["max"]
                    diff = crit_stats[c_code]["diff"]
                    
                    if diff == 0:
                        u_val = 1.0
                        step_str = f"Semua nilai identik = 1.0000"
                    else:
                        if c["Jenis"] == "Benefit":
                            u_val = (val - c_min) / diff
                            step_str = f"({val:,.0f} - {c_min:,.0f}) / {diff:,.0f} = {u_val:.4f}"
                        else:  # Cost
                            u_val = (c_max - val) / diff
                            step_str = f"({c_max:,.0f} - {val:,.0f}) / {diff:,.0f} = {u_val:.4f}"
                    utility_matrix[a_code][c_code] = u_val
                    utility_steps[a_code][c_code] = step_str
                    
            # Step D: Final Scores Vi = sum(Wj * Uij)
            final_results = []
            score_steps = {}
            for alt in st.session_state.alternatives:
                a_code = alt["Kode"]
                a_name = alt["Nama Alternatif"]
                score = 0.0
                weighted_details = {}
                step_parts = []
                for c in st.session_state.criteria:
                    c_code = c["Kode"]
                    u_val = utility_matrix[a_code][c_code]
                    w_norm = norm_weights[c_code]
                    part = w_norm * u_val
                    score += part
                    weighted_details[c_code] = part
                    step_parts.append(f"({w_norm:.2f} × {u_val:.2f})")
                    
                score_steps[a_code] = " + ".join(step_parts) + f" = {score:.4f}"
                final_results.append({
                    "Kode": a_code,
                    "Nama Alternatif": a_name,
                    "Nilai Akhir": round(score, 4),
                    "Utility": utility_matrix[a_code],
                    "Weighted": weighted_details
                })
                
            final_results_sorted = sorted(final_results, key=lambda x: x["Nilai Akhir"], reverse=True)
            for rank, item in enumerate(final_results_sorted, 1):
                item["Ranking"] = rank
                item["Status"] = "Terbaik" if rank == 1 else "Direkomendasikan" if rank == 2 else "Pertimbangan"
                
            st.session_state.calc_results = {
                "total_bobot_awal": total_bobot_awal,
                "norm_weights": norm_weights,
                "crit_stats": crit_stats,
                "utility_matrix": utility_matrix,
                "utility_steps": utility_steps,
                "score_steps": score_steps,
                "final_results": final_results,
                "final_results_sorted": final_results_sorted,
            }
            st.session_state.calculated_snapshot = get_input_snapshot()
            st.session_state.has_calculated = True
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_btn_right:
    if st.session_state.has_calculated:
        st.markdown("<div class='btn-secondary'>", unsafe_allow_html=True)
        if st.button("🔄 Reset Hasil (Ke Mode Input)", key="btn_reset_results", use_container_width=True):
            st.session_state.has_calculated = False
            st.session_state.calc_results = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================================
# RESULT MODE: TAMPILKAN SELURUH TAHAPAN PERHITUNGAN SECARA BERURUTAN
# =========================================================================
if st.session_state.has_calculated and st.session_state.calc_results is not None:
    res = st.session_state.calc_results
    total_bobot_awal = res["total_bobot_awal"]
    norm_weights = res["norm_weights"]
    crit_stats = res["crit_stats"]
    utility_matrix = res["utility_matrix"]
    utility_steps = res["utility_steps"]
    score_steps = res["score_steps"]
    final_results = res["final_results"]
    final_results_sorted = res["final_results_sorted"]

    st.markdown("<hr style='margin: 32px 0 24px 0; border: none; border-top: 2px dashed #15803D;' />", unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <span style="background-color: #DCFCE7; color: #15803D; font-weight: 800; font-size: 0.85rem; padding: 4px 12px; border-radius: 999px; border: 1px solid #86EFAC;">
            HASIL PERHITUNGAN LENGKAP METODE SMART
        </span>
        <h2 style="font-size: 1.65rem; font-weight: 800; color: #0F172A; margin: 8px 0 4px 0;">
            Tahapan Perhitungan & Rekomendasi Keputusan
        </h2>
        <p style="color: #64748B; font-size: 0.92rem; margin: 0;">
            Berikut adalah uraian lengkap tahapan perhitungan metode SMART mulai dari pembobotan, normalisasi, utility, nilai akhir, hingga perankingan.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # TAHAP 1: PEMBOBOTAN KRITERIA
    # ---------------------------------------------------------------------
    st.markdown(clean_html("""
    <div class="dashboard-card">
        <div class="sec-header">
            <div class="sec-badge-result">01</div>
            <h3 class="sec-title">Tahap 1: Pembobotan Kriteria</h3>
        </div>
        <div class="sec-desc">
            Pembobotan digunakan untuk menentukan tingkat kepentingan setiap kriteria dalam proses pengambilan keputusan. Semakin besar bobot, semakin dominan pengaruh kriteria terhadap hasil akhir.
        </div>
    """), unsafe_allow_html=True)
    
    t1_col1, t1_col2 = st.columns([1.6, 1.2], gap="medium")
    with t1_col1:
        th_t1 = "<tr><th>Kode</th><th>Nama Kriteria</th><th>Jenis</th><th>Bobot Awal (wj)</th></tr>"
        rows_t1 = ""
        for c in st.session_state.criteria:
            rows_t1 += f"<tr><td style='font-weight:700;'>{c['Kode']}</td><td>{c['Nama Kriteria']}</td><td>{c['Jenis']}</td><td style='font-weight:700;'>{c['Bobot']:.0f}</td></tr>"
        rows_t1 += f"<tr class='total-row'><td colspan='3'>Total Bobot Awal (&Sigma;wj)</td><td>{total_bobot_awal:.0f}</td></tr>"
        
        st.markdown(clean_html(f"""
        <table class="custom-table">
            <thead>{th_t1}</thead>
            <tbody>{rows_t1}</tbody>
        </table>
        """), unsafe_allow_html=True)
        
    with t1_col2:
        st.markdown(clean_html("""
        <div class="mint-card">
            <div class="mint-card-title">💡 Penjelasan Tingkat Kepentingan:</div>
            <div style="font-size: 0.83rem; color: #166534; line-height: 1.55;">
                Nilai bobot awal mencerminkan prioritas pengambil keputusan. Pada metode SMART, bobot awal tidak harus berjumlah 100 karena sistem akan melakukan normalisasi otomatis ke dalam skala 0 – 1 pada Tahap 2.
            </div>
        </div>
        """), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # TAHAP 2: NORMALISASI BOBOT
    # ---------------------------------------------------------------------
    st.markdown(clean_html("""
    <div class="dashboard-card">
        <div class="sec-header">
            <div class="sec-badge-result">02</div>
            <h3 class="sec-title">Tahap 2: Normalisasi Bobot Kriteria</h3>
        </div>
        <div class="sec-desc">
            Normalisasi adalah proses mengubah bobot awal menjadi bobot relatif agar seluruh bobot memiliki total sebesar 1 (atau 100%).
        </div>
    """), unsafe_allow_html=True)
    
    t2_col1, t2_col2 = st.columns([1.6, 1.2], gap="medium")
    with t2_col1:
        rows_t2 = ""
        total_w_norm = sum(norm_weights.values())
        for c in st.session_state.criteria:
            c_code = c["Kode"]
            c_name = c["Nama Kriteria"]
            w_raw = c["Bobot"]
            w_norm = norm_weights[c_code]
            pct = w_norm * 100
            rows_t2 += f"<tr><td style='font-weight:700;'>{c_code} - {c_name}</td><td>{w_raw:.0f}</td><td style='font-weight:700; color:#15803D;'>{w_norm:.4f}</td><td>{pct:.2f}%</td></tr>"
            
        full_table_t2 = f"""
        <table class="custom-table">
            <thead>
                <tr>
                    <th>Kriteria</th>
                    <th>Bobot Awal (wj)</th>
                    <th>Bobot Normalisasi (Wj)</th>
                    <th>Persentase</th>
                </tr>
            </thead>
            <tbody>
                {rows_t2}
                <tr class="total-row">
                    <td>Total</td>
                    <td>{total_bobot_awal:.0f}</td>
                    <td>{total_w_norm:.4f}</td>
                    <td>100.00%</td>
                </tr>
            </tbody>
        </table>
        """
        st.markdown(clean_html(full_table_t2), unsafe_allow_html=True)
        
    with t2_col2:
        card_t2 = """
        <div class="mint-card">
            <div class="mint-card-title">ℹ️ Rumus Normalisasi:</div>
            <div style="font-size: 1.15rem; font-weight: 700; text-align: center; margin: 10px 0; color: #15803D;">
                <i>W<sub>j</sub></i> = 
                <span style="display: inline-block; vertical-align: middle; text-align: center; margin: 0 4px;">
                    <span style="display: block; border-bottom: 1.5px solid #15803D; padding: 0 4px; font-size: 0.95rem;"><i>w<sub>j</sub></i></span>
                    <span style="display: block; padding: 0 4px; font-size: 0.95rem;">&sum; <i>w<sub>j</sub></i></span>
                </span>
            </div>
            <div style="font-size: 0.8rem; color: #166534; line-height: 1.5;">
                <strong>Substitusi Angka:</strong><br>
        """
        for c in st.session_state.criteria:
            c_code = c["Kode"]
            card_t2 += f"• <em>W<sub>{c_code}</sub></em> = {c['Bobot']:.0f} / {total_bobot_awal:.0f} = <strong>{norm_weights[c_code]:.4f}</strong><br>"
        card_t2 += "</div></div>"
        st.markdown(clean_html(card_t2), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # TAHAP 3: PERHITUNGAN UTILITY
    # ---------------------------------------------------------------------
    st.markdown(clean_html("""
    <div class="dashboard-card">
        <div class="sec-header">
            <div class="sec-badge-result">03</div>
            <h3 class="sec-title">Tahap 3: Perhitungan Nilai Utility (Uij)</h3>
        </div>
        <div class="sec-desc">
            Nilai utility mentransformasikan nilai asli kriteria ke dalam skala baku 0 sampai 1 berdasarkan sifat kriteria (Benefit atau Cost).
        </div>
    """), unsafe_allow_html=True)
    
    # Formulas and Extreme Values
    u_f_col1, u_f_col2 = st.columns([1.1, 1.4], gap="medium")
    with u_f_col1:
        st.markdown(clean_html("""
        <div class="mint-card">
            <div class="mint-card-title">Rumus Utility Kriteria:</div>
            <div style="font-size: 0.84rem; margin: 8px 0; color: #1E293B;">
                <strong>• Benefit</strong> (semakin tinggi semakin baik):<br>
                <span style="display: inline-flex; align-items: center; margin-top: 4px;">
                    <i>U<sub>ij</sub></i> = 
                    <span style="display: inline-block; vertical-align: middle; text-align: center; margin: 0 6px;">
                        <span style="display: block; border-bottom: 1.5px solid #1E293B; padding: 0 4px; font-size: 0.8rem;"><i>C<sub>out</sub></i> &minus; <i>C<sub>min</sub></i></span>
                        <span style="display: block; padding: 0 4px; font-size: 0.8rem;"><i>C<sub>max</sub></i> &minus; <i>C<sub>min</sub></i></span>
                    </span>
                </span>
            </div>
            <div style="font-size: 0.84rem; margin: 10px 0 4px 0; color: #1E293B;">
                <strong>• Cost</strong> (semakin rendah semakin baik):<br>
                <span style="display: inline-flex; align-items: center; margin-top: 4px;">
                    <i>U<sub>ij</sub></i> = 
                    <span style="display: inline-block; vertical-align: middle; text-align: center; margin: 0 6px;">
                        <span style="display: block; border-bottom: 1.5px solid #1E293B; padding: 0 4px; font-size: 0.8rem;"><i>C<sub>max</sub></i> &minus; <i>C<sub>out</sub></i></span>
                        <span style="display: block; padding: 0 4px; font-size: 0.8rem;"><i>C<sub>max</sub></i> &minus; <i>C<sub>min</sub></i></span>
                    </span>
                </span>
            </div>
        </div>
        """), unsafe_allow_html=True)
        
    with u_f_col2:
        st.markdown("<div style='font-size: 0.88rem; font-weight: 700; color: #0F172A; margin-bottom: 6px;'>Nilai Minimum & Maksimum Kriteria:</div>", unsafe_allow_html=True)
        stat_rows = ""
        for c in st.session_state.criteria:
            c_code = c["Kode"]
            s = crit_stats[c_code]
            stat_rows += f"<tr><td style='font-weight:700;'>{c_code} - {c['Nama Kriteria']}</td><td>{s['type']}</td><td>{s['min']:,.0f}</td><td>{s['max']:,.0f}</td><td>{s['diff']:,.0f}</td></tr>"
            
        st.markdown(clean_html(f"""
        <table class="custom-table">
            <thead>
                <tr>
                    <th>Kriteria</th>
                    <th>Jenis</th>
                    <th>Cmin</th>
                    <th>Cmax</th>
                    <th>Rentang (Cmax - Cmin)</th>
                </tr>
            </thead>
            <tbody>
                {stat_rows}
            </tbody>
        </table>
        """), unsafe_allow_html=True)
        
    # Utility Table
    st.write("")
    st.markdown("<div style='font-size: 0.9rem; font-weight: 700; color: #0F172A; margin-bottom: 6px;'>Tabel Hasil Nilai Utility (Uij):</div>", unsafe_allow_html=True)
    th_u = "".join([f"<th>{c['Kode']} - {c['Nama Kriteria']} ({c['Jenis']})</th>" for c in st.session_state.criteria])
    rows_u = ""
    for alt in st.session_state.alternatives:
        a_code = alt["Kode"]
        tds = "".join([f"<td style='font-weight:600;'>{utility_matrix[a_code][c['Kode']]:.4f}</td>" for c in st.session_state.criteria])
        rows_u += f"<tr><td style='font-weight:700;'>{a_code}</td><td>{alt['Nama Alternatif']}</td>{tds}</tr>"
        
    st.markdown(clean_html(f"""
    <table class="custom-table">
        <thead>
            <tr>
                <th>Kode</th>
                <th>Nama Alternatif</th>
                {th_u}
            </tr>
        </thead>
        <tbody>
            {rows_u}
        </tbody>
    </table>
    """), unsafe_allow_html=True)
    
    with st.expander("🔍 Lihat Detail Substitusi Angka Perhitungan Utility Setiap Alternatif"):
        for alt in st.session_state.alternatives:
            a_code = alt["Kode"]
            st.markdown(f"**Alternatif {a_code} ({alt['Nama Alternatif']}):**")
            for c in st.session_state.criteria:
                c_code = c["Kode"]
                st.caption(f"• **{c_code} ({c['Nama Kriteria']} - {c['Jenis']})**: {utility_steps[a_code][c_code]}")
            st.write("")
            
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # TAHAP 4: PERHITUNGAN NILAI AKHIR
    # ---------------------------------------------------------------------
    st.markdown(clean_html("""
    <div class="dashboard-card">
        <div class="sec-header">
            <div class="sec-badge-result">04</div>
            <h3 class="sec-title">Tahap 4: Perhitungan Nilai Akhir (Vi)</h3>
        </div>
        <div class="sec-desc">
            Nilai akhir setiap alternatif diperoleh dengan menjumlahkan perkalian antara nilai utility kriteria dengan bobot normalisasinya.
        </div>
    """), unsafe_allow_html=True)
    
    st.markdown(clean_html("""
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 16px; margin-bottom: 12px; font-size: 0.9rem;">
        <strong>Rumus Nilai Akhir:</strong> &nbsp;&nbsp; 
        <span style="color: #15803D; font-weight: 700;"><i>V<sub>i</sub></i> = &sum; (<i>W<sub>j</sub></i> &times; <i>U<sub>ij</sub></i>)</span>
        &nbsp;&nbsp; <em>(Jumlah seluruh perkalian Bobot Normalisasi dengan Utility)</em>
    </div>
    """), unsafe_allow_html=True)
    
    th_calc = "".join([f"<th>{c['Kode']} (×{norm_weights[c['Kode']]:.4f})</th>" for c in st.session_state.criteria])
    rows_calc = ""
    for item in final_results:
        a_code = item["Kode"]
        tds = "".join([f"<td>{item['Weighted'][c['Kode']]:.4f}</td>" for c in st.session_state.criteria])
        rows_calc += f"<tr><td style='font-weight:700;'>{a_code}</td><td>{item['Nama Alternatif']}</td>{tds}<td style='font-weight:800; color:#15803D; font-size:0.95rem;'>{item['Nilai Akhir']:.4f}</td></tr>"
        
    st.markdown(clean_html(f"""
    <table class="custom-table">
        <thead>
            <tr>
                <th>Kode</th>
                <th>Nama Alternatif</th>
                {th_calc}
                <th style="background-color:#DCFCE7; color:#15803D;">Nilai Akhir (Vi)</th>
            </tr>
        </thead>
        <tbody>
            {rows_calc}
        </tbody>
    </table>
    """), unsafe_allow_html=True)
    
    with st.expander("🔍 Lihat Detail Penjumlahan Aljabar Nilai Akhir (Vi)"):
        for alt in st.session_state.alternatives:
            a_code = alt["Kode"]
            st.markdown(f"• **{a_code} ({alt['Nama Alternatif']})**: `{score_steps[a_code]}`")
            
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # TAHAP 5: HASIL PERANGKINGAN
    # ---------------------------------------------------------------------
    st.markdown(clean_html("""
    <div class="dashboard-card">
        <div class="sec-header">
            <div class="sec-badge-result">05</div>
            <h3 class="sec-title">Tahap 5: Hasil Perangkingan & Rekomendasi</h3>
        </div>
        <div class="sec-desc">
            Alternatif diurutkan dari nilai akhir tertinggi ke terendah untuk menentukan rekomendasi keputusan terbaik.
        </div>
    """), unsafe_allow_html=True)
    
    best_alt_item = final_results_sorted[0]
    
    # Winner Card
    st.markdown(clean_html(f"""
    <div class="winner-card">
        <div>
            <div class="winner-title">👑 Rekomendasi Alternatif Terbaik (Peringkat 1)</div>
            <h3 class="winner-name">{best_alt_item['Kode']} — {best_alt_item['Nama Alternatif']}</h3>
            <p style="margin: 4px 0 0 0; color: #DCFCE7; font-size: 0.92rem;">
                Terpilih sebagai alternatif optimal berdasarkan evaluasi seluruh kriteria metode SMART.
            </p>
        </div>
        <div class="winner-score">
            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #DCFCE7;">Nilai Akhir (Vi)</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #FFFFFF; line-height: 1.1;">{best_alt_item['Nilai Akhir']:.4f}</div>
        </div>
    </div>
    """), unsafe_allow_html=True)
    
    t5_col1, t5_col2 = st.columns([1.1, 1.2], gap="large")
    
    with t5_col1:
        st.markdown("<div style='font-size: 0.92rem; font-weight: 700; color: #0F172A; margin-bottom: 6px;'>Tabel Peringkat Lengkap:</div>", unsafe_allow_html=True)
        tbl_rows_res = ""
        for r in final_results_sorted:
            rank_badge = "🥇" if r["Ranking"] == 1 else f"{r['Ranking']}"
            status_badge = "<span class='badge-terbaik'>Terbaik</span>" if r["Ranking"] == 1 else r["Status"]
            bg_highlight = "style='background-color: #F0FDF4; font-weight: 600;'" if r["Ranking"] == 1 else ""
            
            tbl_rows_res += f"""
            <tr {bg_highlight}>
                <td style="text-align: center; font-size: 1rem;">{rank_badge}</td>
                <td style="font-weight:700;">{r['Kode']}</td>
                <td>{r['Nama Alternatif']}</td>
                <td style="font-weight:800; font-size:0.95rem; color:#15803D;">{r['Nilai Akhir']:.4f}</td>
                <td>{status_badge}</td>
            </tr>
            """
            
        st.markdown(clean_html(f"""
        <table class="custom-table">
            <thead>
                <tr>
                    <th style="text-align: center;">Ranking</th>
                    <th>Kode</th>
                    <th>Nama Alternatif</th>
                    <th>Nilai Akhir (Vi)</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {tbl_rows_res}
            </tbody>
        </table>
        """), unsafe_allow_html=True)
        
        # Download Button
        df_download = pd.DataFrame(final_results_sorted)[["Ranking", "Kode", "Nama Alternatif", "Nilai Akhir", "Status"]]
        csv_bytes = df_download.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Hasil Keputusan (.CSV)",
            data=csv_bytes,
            file_name="hasil_spk_smart.csv",
            mime="text/csv",
            use_container_width=True
        )

    with t5_col2:
        st.markdown("<div style='font-size: 0.92rem; font-weight: 700; color: #0F172A; margin-bottom: 6px;'>Grafik Ranking Alternatif:</div>", unsafe_allow_html=True)
        
        chart_colors = ['#15803D', '#0284C7', '#9333EA', '#D97706', '#0D9488', '#E11D48']
        
        x_labels = [f"{r['Kode']} ({r['Nama Alternatif']})" for r in final_results_sorted]
        y_vals = [r["Nilai Akhir"] for r in final_results_sorted]
        bar_colors = [chart_colors[i % len(chart_colors)] for i in range(len(final_results_sorted))]
        
        fig = go.Figure(data=[
            go.Bar(
                x=x_labels,
                y=y_vals,
                text=[f"{v:.4f}" for v in y_vals],
                textposition='outside',
                marker=dict(
                    color=bar_colors,
                    line=dict(color='rgba(0,0,0,0.1)', width=1)
                ),
                width=0.45
            )
        ])
        
        max_y = max(y_vals) if y_vals else 1.0
        y_limit = max(0.8, round(max_y + 0.15, 1))
        
        fig.update_layout(
            margin=dict(l=20, r=20, t=25, b=25),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            yaxis=dict(
                range=[0, y_limit],
                dtick=0.2,
                gridcolor="#E2E8F0",
                zeroline=True,
                zerolinecolor="#94A3B8"
            ),
            xaxis=dict(
                gridcolor="rgba(0,0,0,0)",
                tickfont=dict(size=11, color="#1E293B", family="Plus Jakarta Sans")
            ),
            font=dict(family="Plus Jakarta Sans", color="#1E293B", size=12),
            height=260
        )
        
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Kesimpulan Banner
    conclusion_html = f"""
    <div class="conclusion-banner">
        <div class="conclusion-icon">✔</div>
        <div>
            <strong>Kesimpulan:</strong> Berdasarkan hasil perhitungan metode SMART, alternatif <strong>{best_alt_item['Kode']} ({best_alt_item['Nama Alternatif']})</strong> memperoleh nilai tertinggi sebesar <strong>{best_alt_item['Nilai Akhir']:.4f}</strong> dan menjadi rekomendasi keputusan utama.
        </div>
    </div>
    """
    st.markdown(clean_html(conclusion_html), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)