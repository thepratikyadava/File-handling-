import streamlit as st
from pathlib import Path
import os

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="File Manager",
    page_icon="📁",
    layout="centered",
)

# ─── THEME TOGGLE ────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# ─── CSS INJECTION ───────────────────────────────────────────────────────────
def inject_css(dark: bool):
    if dark:
        bg        = "#0f1117"
        surface   = "#1c1e26"
        border    = "#2e3140"
        accent    = "#7c6af7"
        accent_h  = "#9d8fff"
        text      = "#e8e9f0"
        muted     = "#8b8fa8"
        success   = "#4ade80"
        error     = "#f87171"
        warning   = "#facc15"
        btn_bg    = "#7c6af7"
        btn_text  = "#ffffff"
    else:
        bg        = "#f5f6fa"
        surface   = "#ffffff"
        border    = "#dde1ef"
        accent    = "#5b4fcf"
        accent_h  = "#4338ca"
        text      = "#1a1b2e"
        muted     = "#6b7280"
        success   = "#16a34a"
        error     = "#dc2626"
        warning   = "#d97706"
        btn_bg    = "#5b4fcf"
        btn_text  = "#ffffff"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
        background-color: {bg} !important;
        color: {text} !important;
        font-family: 'Inter', sans-serif !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: {surface} !important;
        border-right: 1px solid {border} !important;
    }}

    [data-testid="stHeader"] {{
        background-color: {bg} !important;
    }}

    /* Cards */
    .fm-card {{
        background: {surface};
        border: 1px solid {border};
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
    }}

    .fm-title {{
        font-size: 28px;
        font-weight: 700;
        color: {text};
        margin: 0 0 4px 0;
        letter-spacing: -0.5px;
    }}

    .fm-subtitle {{
        font-size: 14px;
        color: {muted};
        margin: 0 0 24px 0;
    }}

    .fm-section-label {{
        font-size: 11px;
        font-weight: 600;
        color: {muted};
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }}

    /* Operation badges */
    .badge {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 16px;
    }}
    .badge-create  {{ background: {'#1a2e1a' if dark else '#dcfce7'}; color: {success}; }}
    .badge-read    {{ background: {'#1a1a2e' if dark else '#ede9fe'}; color: {accent}; }}
    .badge-update  {{ background: {'#2e2a1a' if dark else '#fef9c3'}; color: {warning}; }}
    .badge-delete  {{ background: {'#2e1a1a' if dark else '#fee2e2'}; color: {error}; }}

    /* Alert boxes */
    .alert {{
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 14px;
        margin-top: 16px;
        font-family: 'Inter', sans-serif;
    }}
    .alert-success {{ background: {'#1a2e1a' if dark else '#dcfce7'}; color: {success}; border-left: 3px solid {success}; }}
    .alert-error   {{ background: {'#2e1a1a' if dark else '#fee2e2'}; color: {error};   border-left: 3px solid {error}; }}
    .alert-info    {{ background: {'#1a1a2e' if dark else '#ede9fe'}; color: {accent};  border-left: 3px solid {accent}; }}

    /* File content box */
    .file-content {{
        background: {'#141520' if dark else '#f8fafc'};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        color: {text};
        white-space: pre-wrap;
        word-break: break-all;
        max-height: 300px;
        overflow-y: auto;
        margin-top: 12px;
    }}

    /* Divider */
    .fm-divider {{
        height: 1px;
        background: {border};
        margin: 20px 0;
    }}

    /* Streamlit overrides */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background-color: {'#141520' if dark else '#f8fafc'} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        color: {text} !important;
        font-family: 'Inter', sans-serif !important;
    }}

    .stTextInput > label, .stTextArea > label, .stRadio > label,
    .stSelectbox > label {{
        color: {muted} !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }}

    .stButton > button {{
        background-color: {btn_bg} !important;
        color: {btn_text} !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 8px 20px !important;
        transition: opacity 0.2s !important;
        font-family: 'Inter', sans-serif !important;
    }}

    .stButton > button:hover {{
        opacity: 0.85 !important;
    }}

    /* Radio buttons */
    .stRadio > div {{
        flex-direction: row !important;
        gap: 12px !important;
    }}

    .stRadio > div > label {{
        background: {surface} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        cursor: pointer !important;
        color: {text} !important;
        font-size: 14px !important;
    }}

    /* Theme toggle button special */
    .theme-btn > button {{
        background-color: transparent !important;
        border: 1px solid {border} !important;
        color: {text} !important;
        font-size: 13px !important;
        padding: 4px 12px !important;
    }}

    /* Hide streamlit branding */
    #MainMenu, footer, header {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

inject_css(st.session_state.dark_mode)

# ─── HELPER ──────────────────────────────────────────────────────────────────
def alert(msg, kind="info"):
    st.markdown(f'<div class="alert alert-{kind}">{msg}</div>', unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────
col_title, col_theme = st.columns([5, 1])
with col_title:
    st.markdown('<p class="fm-title">📁 File Manager</p>', unsafe_allow_html=True)
    st.markdown('<p class="fm-subtitle">Create · Read · Update · Delete files on your machine</p>', unsafe_allow_html=True)
with col_theme:
    st.markdown("")
    icon = "☀️ Light" if st.session_state.dark_mode else "🌙 Dark"
    st.markdown('<div class="theme-btn">', unsafe_allow_html=True)
    if st.button(icon, key="theme_toggle", on_click=toggle_theme):
        pass
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="fm-divider"></div>', unsafe_allow_html=True)

# ─── OPERATION PICKER ────────────────────────────────────────────────────────
st.markdown('<p class="fm-section-label">Select Operation</p>', unsafe_allow_html=True)
op = st.radio(
    "op",
    ["📄 Create", "👁️ Read", "✏️ Update", "🗑️ Delete"],
    horizontal=True,
    label_visibility="collapsed",
)

st.markdown('<div class="fm-divider"></div>', unsafe_allow_html=True)

# ─── CREATE ──────────────────────────────────────────────────────────────────
if op == "📄 Create":
    st.markdown('<span class="badge badge-create">CREATE FILE</span>', unsafe_allow_html=True)
    st.markdown('<div class="fm-card">', unsafe_allow_html=True)
    fname = st.text_input("File name (e.g. notes.txt)", placeholder="myfile.txt")
    content = st.text_area("Initial content (optional)", placeholder="Type something...", height=150)
    if st.button("Create File"):
        if not fname.strip():
            alert("Enter file name.", "error")
        else:
            path = Path(fname.strip())
            if path.exists():
                alert(f"File <b>{fname}</b> already exists. Choose another name.", "error")
            else:
                try:
                    with open(path, "w") as f:
                        f.write(content)
                    alert(f"✅ File <b>{fname}</b> created successfully!", "success")
                except Exception as e:
                    alert(f"Error: {e}", "error")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── READ ─────────────────────────────────────────────────────────────────────
elif op == "👁️ Read":
    st.markdown('<span class="badge badge-read">READ FILE</span>', unsafe_allow_html=True)
    st.markdown('<div class="fm-card">', unsafe_allow_html=True)
    fname = st.text_input("File name to read", placeholder="myfile.txt")
    if st.button("Read File"):
        if not fname.strip():
            alert("Enter file name.", "error")
        else:
            path = Path(fname.strip())
            if not path.exists():
                alert(f"File <b>{fname}</b> not found.", "error")
            else:
                try:
                    content = path.read_text()
                    if content.strip():
                        st.markdown(f'<div class="file-content">{content}</div>', unsafe_allow_html=True)
                    else:
                        alert("File is empty.", "info")
                except Exception as e:
                    alert(f"Error: {e}", "error")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── UPDATE ──────────────────────────────────────────────────────────────────
elif op == "✏️ Update":
    st.markdown('<span class="badge badge-update">UPDATE FILE</span>', unsafe_allow_html=True)
    st.markdown('<div class="fm-card">', unsafe_allow_html=True)
    fname = st.text_input("File name to update", placeholder="myfile.txt")

    update_op = st.radio(
        "What to do?",
        ["Append content", "Rename file", "Overwrite content"],
        horizontal=True,
    )

    if update_op == "Append content":
        new_data = st.text_area("Content to append", placeholder="New content...", height=120)
        if st.button("Append"):
            if not fname.strip():
                alert("Enter file name.", "error")
            else:
                path = Path(fname.strip())
                if not path.exists():
                    alert(f"File <b>{fname}</b> not found.", "error")
                else:
                    try:
                        with open(path, "a") as f:
                            f.write("\n" + new_data)
                        alert(f"✅ Content appended to <b>{fname}</b>.", "success")
                    except Exception as e:
                        alert(f"Error: {e}", "error")

    elif update_op == "Rename file":
        new_name = st.text_input("New file name", placeholder="newname.txt")
        if st.button("Rename"):
            if not fname.strip() or not new_name.strip():
                alert("Fill both fields.", "error")
            else:
                path = Path(fname.strip())
                new_path = Path(new_name.strip())
                if not path.exists():
                    alert(f"File <b>{fname}</b> not found.", "error")
                elif new_path.exists():
                    alert(f"File <b>{new_name}</b> already exists.", "error")
                else:
                    try:
                        path.rename(new_path)
                        alert(f"✅ Renamed <b>{fname}</b> → <b>{new_name}</b>.", "success")
                    except Exception as e:
                        alert(f"Error: {e}", "error")

    elif update_op == "Overwrite content":
        new_data = st.text_area("New content (replaces everything)", placeholder="Replacement content...", height=120)
        if st.button("Overwrite"):
            if not fname.strip():
                alert("Enter file name.", "error")
            else:
                path = Path(fname.strip())
                if not path.exists():
                    alert(f"File <b>{fname}</b> not found.", "error")
                else:
                    try:
                        with open(path, "w") as f:
                            f.write(new_data)
                        alert(f"✅ File <b>{fname}</b> overwritten.", "success")
                    except Exception as e:
                        alert(f"Error: {e}", "error")

    st.markdown('</div>', unsafe_allow_html=True)

# ─── DELETE ──────────────────────────────────────────────────────────────────
elif op == "🗑️ Delete":
    st.markdown('<span class="badge badge-delete">DELETE FILE</span>', unsafe_allow_html=True)
    st.markdown('<div class="fm-card">', unsafe_allow_html=True)
    fname = st.text_input("File name to delete", placeholder="myfile.txt")

    if fname.strip():
        path = Path(fname.strip())
        if path.exists():
            alert(f"⚠️ This will permanently delete <b>{fname}</b>. Cannot be undone.", "error")
            confirm = st.checkbox("Yes, I want to delete this file")
            if st.button("Delete File"):
                if not confirm:
                    alert("Check the confirmation box first.", "error")
                else:
                    try:
                        path.unlink()
                        alert(f"✅ File <b>{fname}</b> deleted.", "success")
                    except Exception as e:
                        alert(f"Error: {e}", "error")
        else:
            if st.button("Check File"):
                alert(f"File <b>{fname}</b> not found.", "error")
    else:
        st.button("Delete File")

    st.markdown('</div>', unsafe_allow_html=True)