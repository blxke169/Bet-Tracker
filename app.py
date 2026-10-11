



import streamlit as st
import pandas as pd
import altair as alt
import sqlite3, os, json, math, requests, html, tempfile, hashlib
from datetime import datetime, date
from pathlib import Path

st.set_page_config(page_title="StakeLab | Bet Tracker", page_icon="🧪", layout="wide", initial_sidebar_state="collapsed")

st.markdown(r"""
<style>
:root{--bg:#061018;--panel:#0b1724;--line:#173149;--text:#f5f8fb;--muted:#8da2b7;--teal:#32b5ff;--green:#35e985;--red:#ff5e6c;--amber:#ffcc4d;--blue:#4bb8ff;}
html,body,[class*="css"]{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}
[data-testid="stAppViewContainer"]{background:radial-gradient(circle at 24% -10%,rgba(13,87,111,.22),transparent 33%),radial-gradient(circle at 90% 0%,rgba(0,185,145,.10),transparent 28%),linear-gradient(180deg,#061018 0%,#050b12 100%);color:var(--text);}
[data-testid="stHeader"]{background:rgba(6,16,24,.84);backdrop-filter:blur(14px);border-bottom:1px solid rgba(32,65,93,.38);}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#06111a 0%,#050c13 100%);border-right:1px solid #10273a;}
.block-container{max-width:1600px;padding-top:1rem;padding-bottom:3rem;} h1,h2,h3{letter-spacing:-.035em;color:#f8fbff;} h1{font-size:2rem!important;} h2{font-size:1.45rem!important;} p,li{color:#c8d4df;}
[data-testid="stMetric"]{background:linear-gradient(145deg,rgba(14,29,44,.96),rgba(8,19,30,.96));border:1px solid #17344d;border-radius:14px;padding:14px 16px;box-shadow:0 10px 32px rgba(0,0,0,.18);}
[data-testid="stMetricLabel"]{color:#9db0c2;} [data-testid="stMetricValue"]{font-weight:850;letter-spacing:-.035em;} [data-testid="stMetricDelta"]{color:var(--teal)!important;}
.stButton>button,.stDownloadButton>button,[data-testid="stFormSubmitButton"]>button{min-height:43px;border-radius:9px;border:1px solid #22435f;background:linear-gradient(180deg,#102235,#0b1928);color:#eef7fb;font-weight:750;box-shadow:none;}
[data-testid="stFormSubmitButton"]>button{background:linear-gradient(90deg,#08d9a4,#33efa9);color:#022c23;border:0;font-weight:900;}
[data-testid="stForm"]{background:linear-gradient(145deg,rgba(11,23,36,.98),rgba(8,18,29,.96));border:1px solid #17344d;border-radius:14px;padding:1rem;}
[data-baseweb="input"]>div,[data-baseweb="select"]>div,[data-testid="stTextArea"] textarea,[data-testid="stNumberInput"] input{background:#0a1623!important;border-color:#1b3952!important;border-radius:8px!important;}
[data-testid="stDataFrame"]{border:1px solid #17344d;border-radius:12px;overflow:hidden;background:#08131f;}
.top-shell{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:10px 14px;margin:0 0 12px;border:1px solid #163249;border-radius:13px;background:linear-gradient(180deg,rgba(10,24,36,.96),rgba(7,18,28,.94));}
.brand{display:flex;align-items:center;gap:10px;min-width:220px}.brand-mark{width:29px;height:29px;border-radius:8px;display:grid;place-items:center;background:linear-gradient(135deg,#21f0b7,#0ea97f);color:#003b2e;font-weight:950}.brand-name{font-size:1.22rem;font-weight:900}.brand-sub{font-size:.62rem;color:#7890a6;letter-spacing:.16em;text-transform:uppercase}
.search-shell{flex:1;max-width:560px;padding:9px 13px;border-radius:9px;border:1px solid #18364f;color:#8fa6ba;background:#081521}.status-strip{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}.status-chip{padding:7px 10px;border:1px solid #17354d;border-radius:9px;background:#081521;min-width:110px}.status-chip b{display:block;color:#21e7b2;font-size:.94rem}.status-chip span{font-size:.65rem;color:#8199ad;text-transform:uppercase;letter-spacing:.08em}
.page-kicker{color:#20e2ae;font-size:.7rem;font-weight:850;letter-spacing:.15em;text-transform:uppercase;margin-bottom:3px}.page-title{font-size:1.62rem;font-weight:900;letter-spacing:-.04em;color:#f7fbff}.page-copy{color:#8fa5ba;margin-top:3px;margin-bottom:12px}
.panel-title{font-size:.95rem;font-weight:850;color:#f3f8fb;margin-bottom:7px}.panel-sub{font-size:.76rem;color:#8399ae}.kpi-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:8px 0 14px}.kpi-card{background:linear-gradient(145deg,#0c1b29,#08131f);border:1px solid #17364f;border-radius:12px;padding:13px 14px;min-height:93px}.kpi-label{font-size:.72rem;color:#90a6ba;margin-bottom:8px}.kpi-value{font-size:1.55rem;font-weight:900;color:#f4fbff}.kpi-delta{font-size:.72rem;color:#20e2ae;margin-top:6px}
.alert-card,.signal{border:1px solid #183a53;border-radius:11px;padding:10px 11px;margin:7px 0;background:#081621}.alert-row{display:flex;gap:10px;align-items:flex-start}.alert-dot{width:8px;height:8px;border-radius:50%;margin-top:6px;flex:0 0 8px}.alert-title{font-weight:800;font-size:.82rem;color:#f4f7fa}.alert-copy,.signal-meta{font-size:.72rem;color:#89a0b4;margin-top:2px;line-height:1.35}.signal-head{display:flex;align-items:center;justify-content:space-between;gap:8px}.badge{display:inline-block;padding:3px 8px;border-radius:6px;font-size:.68rem;font-weight:900}.badge-bet{background:#20e2ae;color:#023b2e}.badge-lean{background:#ffcf4d;color:#423000}.badge-nobet{background:#263748;color:#dbe5ed}.green{color:#22e6b0}.muted{color:#8da2b7}
.sidebar-logo{padding:8px 5px 10px}.sidebar-logo .x{font-weight:950;font-size:1.25rem;color:#f7fbff}.sidebar-logo .y{font-size:.65rem;color:#6f8aa1;letter-spacing:.14em}.ai-off{padding:8px 10px;border-radius:9px;border:1px solid #493e18;background:#1e1b0d;color:#ffd66a;font-size:.76rem}.ai-on{padding:8px 10px;border-radius:9px;border:1px solid #164836;background:#0b211a;color:#63efbf;font-size:.76rem}
@media(max-width:1100px){.kpi-grid{grid-template-columns:repeat(2,1fr)}.status-strip,.search-shell{display:none}}

/* --- Mockup polish pass --- */
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child{display:none!important;}
[data-testid="stSidebar"] [role="radiogroup"] label{
  width:100%!important; padding:9px 11px!important; margin:2px 0!important;
  border-radius:9px!important; border:1px solid transparent!important;
  background:transparent!important; transition:.16s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{
  background:#0a1c2a!important; border-color:#153d55!important; transform:translateX(2px);
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){
  background:linear-gradient(90deg,rgba(20,226,176,.14),rgba(20,226,176,.04))!important;
  border-color:#1cae8c!important; box-shadow:inset 3px 0 0 #20e2ae;
}
[data-testid="stSidebar"] [role="radiogroup"] label p{font-size:.87rem!important;font-weight:800!important;color:#dfeaf2!important;}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p{color:#4df0c2!important;}
[data-testid="stSidebar"] hr{margin:14px 0!important;}
.block-container{padding-left:1.2rem!important;padding-right:1.2rem!important;max-width:1540px!important;}
[data-testid="stHorizontalBlock"]{gap:.8rem!important;}
[data-testid="stMetric"]{min-height:108px;display:flex;justify-content:center;}
[data-testid="stMetricValue"]{font-size:1.7rem!important;}
[data-testid="stMetricLabel"]{font-size:.73rem!important;text-transform:uppercase;letter-spacing:.06em;}
[data-testid="stDataFrame"]{box-shadow:0 8px 28px rgba(0,0,0,.16);}
.mock-table{width:100%;border-collapse:separate;border-spacing:0;background:#08141f;border:1px solid #17344d;border-radius:12px;overflow:hidden;font-size:.77rem;}
.mock-table th{background:#0d1b29;color:#91a8ba;text-align:left;padding:10px;border-bottom:1px solid #1a354c;font-weight:800;text-transform:uppercase;font-size:.66rem;letter-spacing:.05em;}
.mock-table td{padding:10px;border-bottom:1px solid #10283a;color:#d7e3ec;}
.mock-table tr:last-child td{border-bottom:0}.mock-table tr:hover td{background:#0a1a28;}
.status-pill{display:inline-block;padding:3px 8px;border-radius:999px;font-weight:850;font-size:.67rem;border:1px solid transparent;}
.status-won{background:#0b3a2d;color:#53efbd;border-color:#176a52}.status-lost{background:#3a141a;color:#ff7b86;border-color:#722a34}.status-pending{background:#3d3210;color:#ffd769;border-color:#6c5717}.status-push{background:#1d2a38;color:#bdcede;border-color:#30465b}
.section-shell{background:linear-gradient(145deg,rgba(10,24,36,.96),rgba(7,16,26,.96));border:1px solid #17344d;border-radius:14px;padding:14px 15px;margin-bottom:12px;box-shadow:0 12px 32px rgba(0,0,0,.14)}
.alert-card{box-shadow:inset 0 1px 0 rgba(255,255,255,.02)}
.alert-card:hover,.signal:hover{border-color:#24516f;transform:translateY(-1px);}


.sample-warning{padding:8px 10px;border:1px solid #5b4b18;background:#1d190d;border-radius:8px;color:#ffd76a;font-size:.72rem;margin-top:7px;}
.quick-actions{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:8px 0 14px;}
.quick-card{padding:12px 14px;border:1px solid #193a52;border-radius:11px;background:linear-gradient(145deg,#0d1c2a,#08131f);}
.quick-card b{display:block;color:#f4f9fc;font-size:.86rem;margin-bottom:3px}.quick-card span{font-size:.72rem;color:#89a1b5}
.score-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:8px 0 10px;}
.score-card{padding:12px;border:1px solid #193950;border-radius:11px;background:#081621;}
.score-label{font-size:.68rem;color:#8299ad;margin-bottom:5px}.score-value{font-size:1.18rem;font-weight:900;color:#f6fbff}.score-note{font-size:.68rem;color:#20dfad;margin-top:4px;}
@media(max-width:900px){.quick-actions,.score-grid{grid-template-columns:1fr 1fr}}

</style>
""", unsafe_allow_html=True)

st.markdown("""<style>\n:root{--bg:#080e1c;--panel:#121c30;--line:#263651;--text:#edf3ff;--muted:#a9b7d0;--teal:#32b5ff;--green:#32b5ff;--red:#ff7188;--amber:#ffd16c;--blue:#65b4ff}
[data-testid="stAppViewContainer"]{background:#080e1c;color:#edf3ff}
[data-testid="stHeader"]{background:#080e1ce8;border:0}
[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"]{display:none}
.block-container{max-width:1400px;padding-top:1.8rem}h1,h2,h3,p,li{color:#edf3ff}h1,h2,h3{font-weight:650}
.tracker-brand{font-size:25px;letter-spacing:-1px;font-weight:750;margin-bottom:16px;color:#edf3ff}.tracker-brand span{font-size:11px;letter-spacing:2px;color:#a9b7d0;margin-left:12px;font-weight:550}
.st-key-top_navigation,.st-key-sport_navigation{margin-bottom:8px}
.st-key-top_navigation [role="radiogroup"],.st-key-sport_navigation [role="radiogroup"]{flex-wrap:nowrap!important;overflow-x:auto;gap:6px;padding:5px 0 9px;scrollbar-width:thin}
.st-key-top_navigation [role="radiogroup"] label,.st-key-sport_navigation [role="radiogroup"] label{flex-shrink:0;white-space:nowrap;margin:0!important;padding:9px 13px;border-radius:9px;border-bottom:3px solid transparent;min-height:44px;transition:background .18s ease,border-color .18s ease}
.st-key-top_navigation [role="radiogroup"] label>div:first-child,.st-key-sport_navigation [role="radiogroup"] label>div:first-child{display:none}
.st-key-top_navigation [role="radiogroup"] label:has(input:checked),.st-key-sport_navigation [role="radiogroup"] label:has(input:checked){background:#173b40;border-bottom-color:#32b5ff}
.st-key-top_navigation{border-bottom:1px solid #263651}.st-key-sport_navigation label p{font-size:13px}
[data-testid="stMetric"],.kpi-card,.panel,.alert-card,.signal,.quick-card,.score-card,[data-testid="stForm"]{background:#121c30!important;border:1px solid #263651!important;border-radius:16px;box-shadow:0 2px 4px #00000018;color:#edf3ff;transition:transform .18s ease,box-shadow .18s ease}
[data-testid="stMetric"]:hover,.kpi-card:hover{transform:translateY(-3px);box-shadow:0 9px 24px #00000040}
[data-testid="stMetricLabel"],.kpi-label,.panel-sub,.score-label,.alert-copy,.signal-meta,.muted,.page-copy,.quick-card span{color:#a9b7d0!important}
[data-testid="stMetricValue"],.kpi-value,.panel-title,.page-title,.score-value,.alert-title,.quick-card b{color:#edf3ff!important}
.kpi-value{font-size:1.8rem;font-weight:650}.kpi-card{padding:20px}.page-kicker,.green,.kpi-delta,.score-note{color:#32b5ff}.page-title{font-weight:650}
[data-baseweb="input"]>div,[data-baseweb="select"]>div,[data-testid="stTextArea"] textarea,[data-testid="stNumberInput"] input{background:#121c30!important;border-color:#344564!important;color:#edf3ff!important}
.stButton>button,.stDownloadButton>button{background:#121c30;color:#edf3ff;border:1px solid #344564;border-radius:10px;min-height:44px;transition:background .18s ease,transform .18s ease}.stButton>button:hover{background:#173b40;border-color:#32b5ff}.stButton>button:active{transform:scale(.98)}
[data-testid="stFormSubmitButton"]>button{background:#32b5ff;color:#121c30;border-radius:10px}
[data-testid="stDataFrame"]{background:#121c30;border-color:#263651}.sample-warning{background:#302811;color:#f2d58b;border-color:#66532a}.badge-bet{background:#133b34;color:#72f1cd}.badge-lean{background:#3d3019;color:#f2d58b}.badge-nobet{background:#273249;color:#bac9e5}
.top-shell,.search-shell{display:none}.alert-card:hover,.signal:hover{transform:none;border-color:#455f88}
@media(max-width:700px){.block-container{padding:1rem}.kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.kpi-value{font-size:1.4rem}.kpi-card{padding:14px}[data-testid="stHorizontalBlock"]{flex-wrap:wrap}[data-testid="stColumn"]{min-width:min(100%,260px)!important;flex:1 1 260px!important}.tracker-brand{margin-bottom:10px}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation:none!important}.kpi-card:hover,[data-testid="stMetric"]:hover,.stButton>button:active{transform:none!important}}
\n
[data-testid="stAppViewContainer"]{background:radial-gradient(ellipse at 12% 0%,#6049dd18,transparent 42%),radial-gradient(ellipse at 88% 10%,#0fbaac14,transparent 42%),#080e1c}
.tracker-brand{color:#edf3ff}.tracker-brand span{color:#99aaff}
.kpi-card,[data-testid="stMetric"]{background:linear-gradient(140deg,#18233b,#101a2d)!important;border-top:3px solid #32b5ff!important}
.kpi-card:nth-child(2){border-top-color:#aa8cff!important}.kpi-card:nth-child(3){border-top-color:#65b4ff!important}.kpi-card:nth-child(4){border-top-color:#ffd16c!important}.kpi-card:nth-child(5){border-top-color:#ff8bba!important}
.kpi-card:hover,[data-testid="stMetric"]:hover{border-color:#546d98!important;box-shadow:0 12px 30px #00000055,0 0 18px #32b5ff10}
.st-key-top_navigation [role="radiogroup"] label:has(input:checked){background:linear-gradient(110deg,#3c2a67,#243d64);border-bottom-color:#ac8cff}
.st-key-sport_navigation [role="radiogroup"] label:has(input:checked){background:#163b3c;border-bottom-color:#32b5ff}
.st-key-top_navigation label:hover,.st-key-sport_navigation label:hover{background:#1e2b45}
.stButton>button[kind="primary"],[data-testid="stFormSubmitButton"]>button{background:linear-gradient(110deg,#32b5ff,#65b4ff);color:#07131e;border:0}
[data-testid="stMetricDelta"]{color:#72f1cd!important}.page-kicker{color:#ac8cff}.panel-title{color:#edf3ff}
.stButton>button:hover{background:#243550;box-shadow:0 0 14px #65b4ff1a}
input,textarea{caret-color:#32b5ff}::selection{background:#6950ad;color:#fff}
</style>""",unsafe_allow_html=True)

st.markdown('''<style>
.sl-brand{display:flex;align-items:center;gap:13px;padding:8px 0 14px;font-size:29px}.sl-brand b{color:#42bdff;font-weight:750}.sl-brand img{border-radius:14px}.sl-brand small{display:block;font-size:10px;font-weight:550;letter-spacing:2.8px;color:#a9b7d0;margin-top:3px}.sl-brand img:hover{box-shadow:0 0 24px #32b5ff24;transition:box-shadow .2s ease}@media(prefers-reduced-motion:reduce){.sl-brand img{transition:none!important}}
</style>''',unsafe_allow_html=True)

st.markdown("""<style>
.st-key-sport_navigation [role="radiogroup"],.st-key-entry_sport_buttons [role="radiogroup"],.st-key-journal_sport_buttons [role="radiogroup"]{display:flex;flex-wrap:nowrap!important;gap:9px!important;overflow-x:auto;padding:7px 3px 13px!important;scrollbar-width:thin;scrollbar-color:#35476b transparent}
.st-key-sport_navigation [role="radiogroup"] label,.st-key-entry_sport_buttons [role="radiogroup"] label,.st-key-journal_sport_buttons [role="radiogroup"] label{flex-shrink:0;margin:0!important;min-height:46px;padding:10px 18px!important;background:#121d32;border:1px solid #2b3b58!important;border-radius:999px!important;transition:background .18s ease,border-color .18s ease,box-shadow .18s ease,transform .18s ease}
.st-key-entry_sport_buttons [role="radiogroup"] label>div:first-child,.st-key-journal_sport_buttons [role="radiogroup"] label>div:first-child,.st-key-wager_buttons [role="radiogroup"] label>div:first-child{display:none}
.st-key-sport_navigation [role="radiogroup"] label p,.st-key-entry_sport_buttons [role="radiogroup"] label p,.st-key-journal_sport_buttons [role="radiogroup"] label p{color:#b9c9e2!important;font-weight:600;font-size:13px}
.st-key-sport_navigation [role="radiogroup"] label:has(input:checked),.st-key-entry_sport_buttons [role="radiogroup"] label:has(input:checked),.st-key-journal_sport_buttons [role="radiogroup"] label:has(input:checked){background:linear-gradient(125deg,#153e42,#193b51)!important;border:1px solid #32b5ff!important;box-shadow:0 0 0 2px #32b5ff12,0 5px 18px #32b5ff12}
.st-key-sport_navigation label:has(input:checked) p,.st-key-entry_sport_buttons label:has(input:checked) p,.st-key-journal_sport_buttons label:has(input:checked) p{color:#83ffe0!important}
.st-key-wager_buttons{margin:12px 0 18px}
.st-key-wager_buttons [role="radiogroup"]{display:flex!important;flex-wrap:nowrap!important;gap:5px!important;background:#0c1424;padding:6px!important;border:1px solid #293a57;border-radius:18px;width:fit-content;max-width:100%}
.st-key-wager_buttons [role="radiogroup"] label{display:flex;align-items:center;justify-content:center;min-height:48px;min-width:120px;padding:12px 22px!important;margin:0!important;border:1px solid transparent;border-radius:13px;transition:background .18s ease,box-shadow .18s ease,transform .18s ease}
.st-key-wager_buttons label p{color:#a9b7d0!important;font-weight:600}
.st-key-wager_buttons label:has(input:checked){background:linear-gradient(120deg,#554080,#2e4f75)!important;border-color:#42bdff70!important;box-shadow:0 3px 15px #00000035}
.st-key-wager_buttons label:has(input:checked) p{color:#f4efff!important}
@media(hover:hover){.st-key-sport_navigation label:hover,.st-key-entry_sport_buttons label:hover,.st-key-journal_sport_buttons label:hover{transform:translateY(-2px);border-color:#607ca5!important;background:#1c2d47!important}.st-key-wager_buttons label:hover{background:#1e2941}}
.st-key-sport_navigation label:has(input:focus-visible),.st-key-entry_sport_buttons label:has(input:focus-visible),.st-key-journal_sport_buttons label:has(input:focus-visible),.st-key-wager_buttons label:has(input:focus-visible){outline:2px solid #42bdff;outline-offset:3px}
@media(max-width:500px){.st-key-wager_buttons [role="radiogroup"]{width:100%}.st-key-wager_buttons [role="radiogroup"] label{flex:1;min-width:0;padding:12px!important}.st-key-sport_navigation label,.st-key-entry_sport_buttons label,.st-key-journal_sport_buttons label{padding:10px 15px!important}}
@media(prefers-reduced-motion:reduce){.st-key-sport_navigation label,.st-key-entry_sport_buttons label,.st-key-journal_sport_buttons label,.st-key-wager_buttons label{transition:none!important;transform:none!important}}

</style>""",unsafe_allow_html=True)

try:
    storage_path = os.environ.get("STAKELAB_DATA_DIR") or st.secrets.get("STAKELAB_DATA_DIR", "")
except Exception:
    storage_path = os.environ.get("STAKELAB_DATA_DIR", "")
DB = Path(storage_path).expanduser() / "betting.db" if storage_path else Path("betting.db")
DB.parent.mkdir(parents=True, exist_ok=True)

def database_backup():
    """SQLite's backup API captures a consistent snapshot, including committed WAL data."""
    with tempfile.TemporaryDirectory() as folder:
        snapshot = Path(folder) / "backup.db"
        with sqlite3.connect(DB) as source, sqlite3.connect(snapshot) as target:
            source.backup(target)
        return snapshot.read_bytes()

def validate_backup(payload):
    if not payload.startswith(b"SQLite format 3\x00"):
        raise ValueError("Choose a StakeLab SQLite backup (.db).")
    with tempfile.TemporaryDirectory() as folder:
        candidate = Path(folder) / "candidate.db"
        candidate.write_bytes(payload)
        try:
            with sqlite3.connect(candidate) as source:
                if source.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                    raise ValueError("This backup failed its integrity check.")
                required = {"bets", "bankroll_settings", "multi_legs", "weekly_budget_settings", "weekly_budget_weeks", "weekly_budget_spend"}
                tables = {r[0] for r in source.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                if not required.issubset(tables):
                    raise ValueError("This file is not a complete current StakeLab backup.")
                for table in required:
                    with sqlite3.connect(DB) as current_db:
                        current = {r[1] for r in current_db.execute(f'PRAGMA table_info({table})')}
                    uploaded = {r[1] for r in source.execute(f'PRAGMA table_info({table})')}
                    if not current.issubset(uploaded):
                        raise ValueError(f"The backup has an incompatible {table} schema.")
                return source.execute("SELECT COUNT(*) FROM bets").fetchone()[0]
        except sqlite3.DatabaseError as exc:
            raise ValueError("This backup cannot be read safely.") from exc

def restore_backup(payload):
    validate_backup(payload)
    # Keep a recovery snapshot before replacing any user data.
    recovery = DB.parent / "backups"
    recovery.mkdir(exist_ok=True)
    previous = recovery / ("before-restore-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db")
    previous.write_bytes(database_backup())
    with tempfile.TemporaryDirectory() as folder:
        candidate = Path(folder) / "candidate.db"
        candidate.write_bytes(payload)
        with sqlite3.connect(candidate) as source, sqlite3.connect(DB) as target:
            source.backup(target)
    return previous
SPORTS = ["NBA","NFL","NHL","MLB","NCAAB","NCAAF","AFL","Soccer","Tennis","Horses","Greyhounds","Other"]
BET_TYPES = {
    "NBA":["3PT","Points","Rebounds","Assists","PRA","Steals","Blocks","Threes+","Moneyline","Spread","Total","Other"],
    "NFL":["Passing Yards","Rushing Yards","Receiving Yards","Receptions","TD","Pass Attempts","Moneyline","Spread","Total","Other"],
    "NHL":["Goals","Assists","Points","Shots","SOG","Saves","Moneyline","Puck Line","Total","Other"],
    "MLB":["Hits","Runs","RBI","HR","Strikeouts","Pitcher Outs","Moneyline","Run Line","Total","Other"],
    "NCAAB":["3PT","Points","Rebounds","Assists","PRA","Moneyline","Spread","Total","Other"],
    "NCAAF":["Passing Yards","Rushing Yards","Receiving Yards","TD","Moneyline","Spread","Total","Other"],
    "AFL":["Disposals","Kicks","Handballs","Marks","Tackles","Goals","CBA","Fantasy Score","Team Total","Line","Total","Other"],
    "Soccer":["Goals","Shots","Shots on Target","Assists","Cards","Corners","Moneyline","Draw No Bet","Total","Other"],
    "Tennis":["Match Winner","Games","Sets","Aces","Double Faults","Total Games","Handicap","Other"],
    "Horses":["Win","Place","Top 3","Top 4","Each Way","Exacta","Quinella","Trifecta","First 4","Other"],
    "Greyhounds":["Win","Place","Top 2","Top 3","Top 4","Exacta","Quinella","Trifecta","Other"]
}
FACTOR_HINTS = {
    "NBA":"minutes, usage, matchup, pace, injuries, role, recent hit rate, rest, line movement",
    "NFL":"snap share, route share, target share, carries, matchup, injuries, weather, game script",
    "NHL":"TOI, line assignment, PP role, shots, opponent, goalie, injuries, pace",
    "MLB":"plate appearances, splits, pitcher matchup, park, handedness, bullpen, weather",
    "NCAAB":"minutes, usage, pace, matchup, injuries, rebounding, recent role",
    "NCAAF":"snap share, target share, rushing role, matchup, injuries, weather, game script",
    "AFL":"time on ground, CBA, role, disposals, matchup, venue, weather, injuries",
    "Soccer":"minutes, xG/xA, shots, role, opponent, home/away, lineup, cards, corners",
    "Tennis":"surface, hold/break rates, serve points, return points, fatigue, head-to-head, injury",
    "Horses":"barrier, speed/sectionals, distance, class, weight, track/going, jockey, trainer, pace, market",
    "Greyhounds":"box, early speed, split times, distance, grade, track, interference, recent times, market"
}

def conn():
    c=sqlite3.connect(DB)
    c.row_factory=sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS bets(
      id INTEGER PRIMARY KEY AUTOINCREMENT, placed_at TEXT, event_date TEXT, sport TEXT, league TEXT,
      event TEXT, book TEXT, bet_type TEXT, market TEXT, selection TEXT, line TEXT,
      odds REAL, closing_odds REAL, stake REAL, result TEXT, pnl REAL,
      reasoning TEXT, post_game_reason TEXT, clv REAL, ai_review TEXT, process_grade TEXT,
      factors_json TEXT, source_note TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS odds_snapshots(
      id INTEGER PRIMARY KEY AUTOINCREMENT, captured_at TEXT, sport TEXT, event TEXT,
      market TEXT, selection TEXT, line TEXT, bookmaker TEXT, odds REAL, source TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS event_data(
      id INTEGER PRIMARY KEY AUTOINCREMENT, captured_at TEXT, sport TEXT, event TEXT,
      subject TEXT, data_json TEXT, source TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS reviews(
      id INTEGER PRIMARY KEY AUTOINCREMENT, bet_id INTEGER, created_at TEXT,
      review TEXT, grade TEXT, tags TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS bankroll_settings(
      id INTEGER PRIMARY KEY CHECK(id=1), starting_bankroll REAL DEFAULT 1000,
      unit_percent REAL DEFAULT 1.0, staking_mode TEXT DEFAULT 'Flat units',
      kelly_fraction REAL DEFAULT 0.25)""")
    c.execute("""CREATE TABLE IF NOT EXISTS bankroll_transactions(
      id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT, txn_date TEXT,
      txn_type TEXT, amount REAL, note TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS multi_legs(
      id INTEGER PRIMARY KEY AUTOINCREMENT, bet_id INTEGER, leg_no INTEGER, sport TEXT, event TEXT,
      bet_type TEXT, market TEXT, selection TEXT, line TEXT, odds REAL, closing_odds REAL, result TEXT DEFAULT 'Pending',
      clv REAL, notes TEXT, FOREIGN KEY(bet_id) REFERENCES bets(id))""")
    # Lightweight migration for existing V4 databases created before multi-leg bet types were added.
    multi_cols={row[1] for row in c.execute("PRAGMA table_info(multi_legs)").fetchall()}
    if "bet_type" not in multi_cols:
        c.execute("ALTER TABLE multi_legs ADD COLUMN bet_type TEXT")
    c.execute("""CREATE TABLE IF NOT EXISTS analysis_log(
      id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT, sport TEXT, selection TEXT, market TEXT,
      odds REAL, user_probability REAL, implied_probability REAL, edge REAL, gate TEXT,
      evidence_quality TEXT, evidence TEXT, reason TEXT)""")
    c.execute("INSERT OR IGNORE INTO bankroll_settings(id,starting_bankroll,unit_percent,staking_mode,kelly_fraction) VALUES(1,1000,1.0,'Flat units',0.25)")
    c.commit()
    return c

def clv(bet, close):
    try:
        b=float(bet); c=float(close)
        # Decimal-odds CLV in implied-probability percentage points.
        # Positive means the closing market implied a higher probability than your entry price.
        return ((1/c)-(1/b))*100
    except: return None

def q(sql,args=()):
    c=conn(); rows=c.execute(sql,args).fetchall(); c.close()
    frame=pd.DataFrame([dict(r) for r in rows])
    if not frame.empty and {'sport','factors_json'}.issubset(frame.columns):
        def custom_name(value):
            try:return str(json.loads(value or '{}').get('custom_sport',''))
            except (ValueError,TypeError,AttributeError):return ''
        frame['Custom sport']=frame.factors_json.map(custom_name)
    return frame

def execsql(sql,args=()):
    c=conn(); cur=c.execute(sql,args); c.commit(); out=cur.lastrowid; c.close(); return out

def profit_chart(frame, x, y):
    data=frame.reset_index()
    data[x]=pd.to_datetime(data[x],errors="coerce")
    data=data.dropna(subset=[x])
    point=alt.selection_point(fields=[x],nearest=True,on="pointerover",empty=False)
    tap=alt.selection_point(fields=[x],nearest=True,on="click",empty=False)
    base=alt.Chart(data).encode(x=alt.X(f"{x}:T",title="Date"),y=alt.Y(f"{y}:Q",title=f"{y} ($)"),tooltip=[alt.Tooltip(f"{x}:T",title="Date"),alt.Tooltip(f"{y}:Q",format="$.2f")])
    line=base.mark_line(color="#32b5ff",strokeWidth=3)
    dots=base.mark_circle(size=90,color="#32b5ff").encode(opacity=alt.condition(point|tap,alt.value(1),alt.value(0))).add_params(point,tap)
    st.altair_chart((line+dots).properties(height=260),use_container_width=True)

def money(x):
    try:return f"${x:,.2f}" if x>=0 else f"-${abs(x):,.2f}"
    except:return "$0.00"

def pct(x):
    try:return f"{x:.2f}%"
    except:return "—"

def save_event_snapshot(sport,event,subject,payload,source):
    execsql("INSERT INTO event_data(captured_at,sport,event,subject,data_json,source) VALUES(?,?,?,?,?,?)",
            (datetime.now().isoformat(),sport,event,subject,json.dumps(payload),source))

def latest_context(sport, search_text="", limit=8):
    df=q("SELECT * FROM event_data WHERE sport=? ORDER BY captured_at DESC LIMIT 80",(sport,))
    if df.empty: return []
    if search_text.strip():
        term=search_text.strip().lower()
        mask=df.apply(lambda r: term in (str(r.get("event",""))+" "+str(r.get("subject",""))+" "+str(r.get("data_json",""))).lower(),axis=1)
        hit=df[mask]
        if not hit.empty: df=hit
    return df.head(limit).to_dict("records")


# ---------------- UNIFIED SPORTS DATA LAYER ----------------
# ESPN's public site endpoints are useful free starting sources but are not a
# contracted/guaranteed API. StakeLab labels the source accurately and never
# treats absent fields as verified facts.

ESPN_FEEDS = {
    "NBA": ("basketball","nba"),
    "NFL": ("football","nfl"),
    "NHL": ("hockey","nhl"),
    "MLB": ("baseball","mlb"),
    "NCAAB": ("basketball","mens-college-basketball"),
    "NCAAF": ("football","college-football"),
}
SOCCER_LEAGUES = {
    "EPL":"eng.1",
    "UEFA Champions League":"uefa.champions",
    "La Liga":"esp.1",
    "Serie A":"ita.1",
    "Bundesliga":"ger.1",
    "Ligue 1":"fra.1",
    "MLS":"usa.1",
    "A-League Men":"aus.1",
}
TENNIS_CIRCUITS = {"ATP":"atp","WTA":"wta"}

def _date_token(day):
    if hasattr(day,"strftime"):
        return day.strftime("%Y%m%d")
    return str(day).replace("-","")

@st.cache_data(ttl=300, show_spinner=False)
def fetch_espn_scoreboard(sport, day=None, league_code=None):
    day_token=_date_token(day or date.today())
    if sport in ESPN_FEEDS:
        category,league=ESPN_FEEDS[sport]
    elif sport=="Soccer":
        category,league="soccer",(league_code or SOCCER_LEAGUES["EPL"])
    elif sport=="Tennis":
        category,league="tennis",(league_code or TENNIS_CIRCUITS["ATP"])
    else:
        return []
    url=f"https://site.api.espn.com/apis/site/v2/sports/{category}/{league}/scoreboard?dates={day_token}"
    r=requests.get(url,timeout=18,headers={"User-Agent":"StakeLab/1.0"})
    r.raise_for_status()
    raw=r.json()
    out=[]
    for e in raw.get("events",[]):
        comp=(e.get("competitions") or [{}])[0]
        competitors=[]
        for c in comp.get("competitors",[]):
            competitors.append({
                "id":c.get("id"),
                "name":c.get("team",{}).get("displayName") or c.get("athlete",{}).get("displayName"),
                "homeAway":c.get("homeAway"),
                "score":c.get("score"),
                "winner":c.get("winner"),
                "records":c.get("records"),
            })
        out.append({
            "id":e.get("id"),
            "name":e.get("name") or e.get("shortName"),
            "date":e.get("date"),
            "status":e.get("status",{}).get("type",{}).get("description"),
            "competitors":competitors,
            "league":league,
            "category":category,
        })
    return out

@st.cache_data(ttl=600, show_spinner=False)
def fetch_espn_summary(sport, event_id, league_code=None):
    if sport in ESPN_FEEDS:
        category,league=ESPN_FEEDS[sport]
    elif sport=="Soccer":
        category,league="soccer",(league_code or SOCCER_LEAGUES["EPL"])
    elif sport=="Tennis":
        category,league="tennis",(league_code or TENNIS_CIRCUITS["ATP"])
    else:
        return {}
    url=f"https://site.api.espn.com/apis/site/v2/sports/{category}/{league}/summary?event={event_id}"
    r=requests.get(url,timeout=20,headers={"User-Agent":"StakeLab/1.0"})
    r.raise_for_status()
    return r.json()

def _collect_named_athletes(obj, found=None):
    """Extract player/athlete names and nearby stat objects from nested JSON."""
    if found is None: found=[]
    if isinstance(obj,dict):
        name=None
        if isinstance(obj.get("athlete"),dict):
            name=obj["athlete"].get("displayName") or obj["athlete"].get("fullName")
        name=name or obj.get("displayName") if obj.get("displayName") and any(k in obj for k in ("stats","statistics","athlete")) else name
        if name:
            found.append({"name":name,"data":obj})
        for v in obj.values():
            _collect_named_athletes(v,found)
    elif isinstance(obj,list):
        for v in obj:
            _collect_named_athletes(v,found)
    return found


def _flatten_numeric_stats(obj, prefix=""):
    """Flatten nested numeric-ish stat fields into a simple dict for inspection."""
    out={}
    if isinstance(obj,dict):
        for k,v in obj.items():
            key=f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v,(int,float)):
                out[key]=v
            elif isinstance(v,str):
                vv=v.strip().replace(",","")
                try:
                    if vv and re.fullmatch(r"-?\d+(?:\.\d+)?",vv):
                        out[key]=float(vv)
                except Exception:
                    pass
            elif isinstance(v,(dict,list)):
                out.update(_flatten_numeric_stats(v,key))
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            out.update(_flatten_numeric_stats(v,f"{prefix}[{i}]"))
    return out

def _extract_receiving_line(player_obj):
    """Best-effort extraction of receiving stats from an ESPN player/stat object.
    Returns only values that are explicitly present in the source object."""
    text_blob=json.dumps(player_obj,default=str).lower()
    nums=_flatten_numeric_stats(player_obj)
    result={}
    # Direct named-stat objects sometimes exist.
    for k,v in nums.items():
        lk=k.lower()
        if "receiving" in lk and ("yard" in lk or "recyd" in lk):
            result.setdefault("receiving_yards",v)
        if "target" in lk:
            result.setdefault("targets",v)
        if "reception" in lk or (lk.endswith(".rec") and "receiv" in lk):
            result.setdefault("receptions",v)
    # ESPN summary often exposes stat groups as labels + stats arrays.
    def walk(o):
        if isinstance(o,dict):
            labels=o.get("labels")
            stats=o.get("stats")
            if isinstance(labels,list) and isinstance(stats,list) and len(labels)==len(stats):
                low=[str(x).lower() for x in labels]
                for i,label in enumerate(low):
                    raw=stats[i]
                    try:
                        val=float(str(raw).replace(",",""))
                    except Exception:
                        continue
                    if label in ("rec","receptions"):
                        result.setdefault("receptions",val)
                    elif label in ("tgts","tgt","targets"):
                        result.setdefault("targets",val)
                    elif label in ("yds","yards") and "receiv" in text_blob:
                        result.setdefault("receiving_yards",val)
            for v in o.values():
                walk(v)
        elif isinstance(o,list):
            for v in o:
                walk(v)
    walk(player_obj)
    return result


@st.cache_data(ttl=1800, show_spinner=False)
def _nflverse_player_assets():
    """Discover current nflverse player-stat assets from the official GitHub release."""
    api="https://api.github.com/repos/nflverse/nflverse-data/releases/tags/player_stats"
    r=requests.get(api,timeout=20,headers={"User-Agent":"StakeLab/1.0","Accept":"application/vnd.github+json"})
    r.raise_for_status()
    return {
        a.get("name"): a.get("browser_download_url")
        for a in r.json().get("assets",[])
        if a.get("name") and a.get("browser_download_url")
    }

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_nflverse_weekly_player_stats(season):
    """Load nflverse weekly player stats for one season using discovered release assets."""
    season=int(season)
    assets=_nflverse_player_assets()
    preferred=[
        # nflverse's current player_stats release uses player_stats_YEAR.*
        # These files contain week-level player rows plus season metadata.
        f"player_stats_{season}.csv",
        f"player_stats_{season}.csv.gz",
        f"player_stats_{season}.parquet",
        # Older/alternate layouts used these names.
        f"stats_player_week_{season}.csv",
        f"stats_player_week_{season}.csv.gz",
        f"stats_player_week_{season}.parquet",
    ]
    for name in preferred:
        url=assets.get(name)
        if not url:
            continue
        if name.endswith(".parquet"):
            return pd.read_parquet(url)
        return pd.read_csv(url)
    # Final direct-URL fallback for older/alternate release layouts.
    direct=f"https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats_{season}.csv"
    return pd.read_csv(direct)

def build_nflverse_player_packet(player_name, max_games=10):
    """Build an NFL receiving packet from nflverse weekly player stats."""
    player_name=(player_name or "").strip()
    if not player_name:
        return None
    frames=[]
    source_errors=[]
    for season in [date.today().year, date.today().year-1, date.today().year-2, date.today().year-3]:
        try:
            df=fetch_nflverse_weekly_player_stats(season)
            if df is not None and not df.empty:
                df=df.copy()
                df["season_source"]=season
                frames.append(df)
        except Exception as ex:
            source_errors.append(f"{season}: {type(ex).__name__}")
    if not frames:
        return {
            "player":player_name,
            "games":[],
            "summary":{},
            "source":"nflverse player_stats release (week-level rows)",
            "diagnostic":"No season files loaded. " + "; ".join(source_errors[:4])
        }

    df=pd.concat(frames,ignore_index=True)

    name_col=None
    for c in ["player_display_name","player_name","player"]:
        if c in df.columns:
            name_col=c
            break
    if not name_col:
        return None

    def _norm_name(s):
        return re.sub(r"[^a-z0-9]","",str(s).lower())
    target=_norm_name(player_name)
    norm_series=df[name_col].astype(str).map(_norm_name)
    mask=norm_series.eq(target)
    if not mask.any():
        # surname + first-name containment fallback
        tokens=[_norm_name(t) for t in player_name.split() if len(_norm_name(t))>=3]
        mask=norm_series.map(lambda x: all(t in x for t in tokens)) if tokens else mask
    p=df.loc[mask].copy()
    if p.empty:
        return {
            "player":player_name,
            "games":[],
            "summary":{},
            "source":"nflverse weekly player stats",
            "diagnostic":f"Player name not found in loaded nflverse files using column {name_col}."
        }

    sort_cols=[c for c in ["season","week"] if c in p.columns]
    if sort_cols:
        p=p.sort_values(sort_cols,ascending=False)
    p=p.head(max_games)

    games=[]
    for _,r in p.iterrows():
        row={
            "season": int(r["season"]) if "season" in p.columns and pd.notna(r.get("season")) else None,
            "week": int(r["week"]) if "week" in p.columns and pd.notna(r.get("week")) else None,
            "player": str(r.get(name_col,"")),
            "team": str(r.get("recent_team","")) if "recent_team" in p.columns else "",
        }
        for col,out_name in [
            ("targets","targets"),
            ("receptions","receptions"),
            ("receiving_yards","receiving_yards"),
            ("receiving_tds","receiving_tds"),
            ("receiving_air_yards","receiving_air_yards"),
            ("receiving_yards_after_catch","receiving_yards_after_catch"),
            ("target_share","target_share"),
            ("air_yards_share","air_yards_share"),
        ]:
            if col in p.columns and pd.notna(r.get(col)):
                try:
                    row[out_name]=float(r.get(col))
                except Exception:
                    row[out_name]=r.get(col)
        games.append(row)

    pdf=pd.DataFrame(games)
    summary={}
    for col,label in [
        ("receiving_yards","receiving_yards"),
        ("targets","targets"),
        ("receptions","receptions"),
        ("target_share","target_share"),
    ]:
        if col in pdf.columns:
            vals=pd.to_numeric(pdf[col],errors="coerce").dropna()
            if not vals.empty:
                summary[f"games_with_{label}"]=int(vals.size)
                summary[f"avg_{label}"]=float(vals.mean())
                summary[f"median_{label}"]=float(vals.median())

    return {
        "player":player_name,
        "games":games,
        "summary":summary,
        "source":"nflverse weekly player stats",
        "source_url":"https://github.com/nflverse/nflverse-data/releases/tag/player_stats"
    }

def build_player_history_packet(sport, player_name, lookback_days=45, max_games=10, league_code=None):
    """Fetch recent player history using the strongest free structured source available."""
    player_name=(player_name or "").strip()
    if not player_name:
        return {"player":player_name,"games":[],"summary":{},"source":"No player selected"}

    if sport=="NFL":
        try:
            packet=build_nflverse_player_packet(player_name,max_games=max_games)
            if packet and packet.get("games"):
                return packet
            nflverse_diag=packet.get("diagnostic") if packet else None
        except Exception as ex:
            nflverse_diag=f"nflverse error: {type(ex).__name__}: {ex}"
    else:
        nflverse_diag=None
    games=[]
    for offset in range(int(lookback_days)):
        if len(games)>=max_games:
            break
        d=date.today()-pd.Timedelta(days=offset)
        try:
            events=fetch_espn_scoreboard(sport,d,league_code)
        except Exception:
            continue
        for ev in events:
            if len(games)>=max_games:
                break
            try:
                summary=fetch_espn_summary(sport,ev.get("id"),league_code)
            except Exception:
                continue
            matches=[]
            for item in _collect_named_athletes(summary):
                nm=str(item.get("name") or "").strip()
                if nm and player_name.lower() in nm.lower():
                    stats=_extract_receiving_line(item.get("data"))
                    if stats:
                        matches.append((nm,stats,item.get("data")))
            if matches:
                nm,stats,raw=matches[0]
                games.append({
                    "date":ev.get("date"),
                    "event":ev.get("name"),
                    "player":nm,
                    **stats
                })
    df=pd.DataFrame(games)
    summary={}
    if not df.empty:
        if "receiving_yards" in df:
            vals=pd.to_numeric(df["receiving_yards"],errors="coerce").dropna()
            if not vals.empty:
                summary["games_with_receiving_yards"]=int(vals.size)
                summary["avg_receiving_yards"]=float(vals.mean())
                summary["median_receiving_yards"]=float(vals.median())
        if "targets" in df:
            vals=pd.to_numeric(df["targets"],errors="coerce").dropna()
            if not vals.empty:
                summary["games_with_targets"]=int(vals.size)
                summary["avg_targets"]=float(vals.mean())
                summary["median_targets"]=float(vals.median())
        if "receptions" in df:
            vals=pd.to_numeric(df["receptions"],errors="coerce").dropna()
            if not vals.empty:
                summary["games_with_receptions"]=int(vals.size)
                summary["avg_receptions"]=float(vals.mean())
    return {
        "player":player_name,
        "games":games,
        "summary":summary,
        "source":"ESPN public event summaries",
        "lookback_days":lookback_days,
        "diagnostic": nflverse_diag if sport=="NFL" and not games else None
    }


def sample_grade(n):
    n=int(n or 0)
    if n >= 10:
        return "Strong", "10+ recent games"
    if n >= 6:
        return "Moderate", "6–9 recent games"
    if n >= 3:
        return "Weak", "3–5 recent games"
    return "Very weak", "Fewer than 3 games"

def recent_form_summary(packet, market_text):
    games=(packet or {}).get("games") or []
    if not games:
        return {}
    m=(market_text or "").lower()
    stat=None
    if "receiving" in m and "yard" in m:
        stat="receiving_yards"
    elif "reception" in m:
        stat="receptions"
    elif "target" in m:
        stat="targets"
    elif "rushing" in m and "yard" in m:
        stat="rushing_yards"
    elif "passing" in m and "yard" in m:
        stat="passing_yards"
    if not stat:
        return {}

    vals=[]
    for g in games:
        v=g.get(stat)
        if v is not None and pd.notna(v):
            try:
                vals.append(float(v))
            except Exception:
                pass
    if not vals:
        return {}

    nums=re.findall(r"\d+(?:\.\d+)?",m)
    line=float(nums[-1]) if nums else None
    is_over="over" in m
    is_under="under" in m

    def is_hit(v):
        if line is None:
            return None
        if is_over:
            return v > line
        if is_under:
            return v < line
        return None

    s=pd.Series(vals,dtype="float64")
    out={
        "stat":stat,
        "sample":len(vals),
        "avg":float(s.mean()),
        "median":float(s.median()),
        "last5":vals[:5],
        "last10":vals[:10],
    }
    if line is not None and (is_over or is_under):
        flags=[is_hit(v) for v in vals]
        out["line"]=line
        out["hits"]=sum(bool(x) for x in flags)
        out["hit_rate"]=sum(bool(x) for x in flags)/len(flags)*100
        flags5=[is_hit(v) for v in vals[:5]]
        flags10=[is_hit(v) for v in vals[:10]]
        out["hit_rate_5"]=sum(bool(x) for x in flags5)/len(flags5)*100 if flags5 else None
        out["hit_rate_10"]=sum(bool(x) for x in flags10)/len(flags10)*100 if flags10 else None

    if len(vals) >= 6:
        split=max(3,len(vals)//2)
        recent=vals[:split]
        older=vals[split:]
        if older:
            out["trend_delta"]=float(pd.Series(recent).mean()-pd.Series(older).mean())
    return out

def detect_claim_conflicts(evidence, form):
    if not evidence or not form:
        return []
    text=evidence.lower()
    conflicts=[]

    # Numeric average claim.
    m=re.search(r"averag(?:e|ing)\s+(?:around\s+|about\s+)?(\d+(?:\.\d+)?)", text)
    if m and form.get("avg") is not None:
        claimed=float(m.group(1))
        actual=float(form["avg"])
        tol=max(2.0,abs(actual)*0.12)
        if abs(claimed-actual) > tol:
            conflicts.append(f"Claimed average ≈ {claimed:.1f}, but verified sample average is {actual:.1f}.")

    # Explicit hit-rate claim.
    m=re.search(r"(\d+(?:\.\d+)?)\s*%\s*(?:hit rate|of the time)", text)
    if m and form.get("hit_rate") is not None:
        claimed=float(m.group(1))
        actual=float(form["hit_rate"])
        if abs(claimed-actual) > 10:
            conflicts.append(f"Claimed hit rate {claimed:.1f}%, but verified sample hit rate is {actual:.1f}%.")

    # Explicit target range claim.
    m=re.search(r"(\d+)\s*[-–]\s*(\d+)\s*targets", text)
    if m and form.get("stat")=="targets" and form.get("avg") is not None:
        lo,hi=int(m.group(1)),int(m.group(2))
        actual=float(form["avg"])
        if not (lo <= actual <= hi):
            conflicts.append(f"Claimed target range {lo}–{hi}, but verified recent average is {actual:.1f} targets.")

    # Straight-hit claim.
    m=re.search(r"(?:over|hit|cleared).{0,12}(\d+)\s*(?:straight|in a row)", text)
    if m and form.get("line") is not None:
        claimed=int(m.group(1))
        vals=form.get("last10") or []
        line=float(form["line"])
        actual=0
        for v in vals:
            if v > line:
                actual += 1
            else:
                break
        if actual < claimed:
            conflicts.append(f"Claimed {claimed} straight overs, but verified recent rows show {actual} straight over this line.")

    return conflicts

def evidence_confidence_score(player_packet, form, data_ctx, conflicts):
    score=0
    reasons=[]
    n=len((player_packet or {}).get("games") or [])
    if n >= 10:
        score += 35; reasons.append("10+ verified player rows")
    elif n >= 6:
        score += 25; reasons.append("6–9 verified player rows")
    elif n >= 3:
        score += 15; reasons.append("3–5 verified player rows")
    elif n:
        score += 5; reasons.append("very small verified sample")

    if form.get("hit_rate") is not None:
        score += 20; reasons.append("market-specific hit rate")
    if form.get("avg") is not None and form.get("median") is not None:
        score += 15; reasons.append("average + median")
    if form.get("trend_delta") is not None:
        score += 10; reasons.append("measurable recent trend")
    if data_ctx:
        score += 10; reasons.append("connected context")
    if conflicts:
        score -= min(20,8*len(conflicts))
        reasons.append(f"{len(conflicts)} claim conflict(s)")
    else:
        score += 10; reasons.append("no numeric claim conflicts")
    return max(0,min(100,score)), reasons

def derive_market_hit_rate(packet, market_text):
    """Calculate a simple hit rate only when the market and required stat are explicit."""
    m=(market_text or "").lower()
    nums=re.findall(r"\d+(?:\.\d+)?",m)
    if not nums:
        return None
    line=float(nums[-1])
    games=packet.get("games") or []
    if "receiving" in m and "yard" in m:
        vals=[g.get("receiving_yards") for g in games if g.get("receiving_yards") is not None]
        vals=[float(v) for v in vals]
        if not vals:
            return None
        if "over" in m:
            hits=sum(v>line for v in vals)
        elif "under" in m:
            hits=sum(v<line for v in vals)
        else:
            return None
        return {"line":line,"sample":len(vals),"hits":hits,"hit_rate":hits/len(vals)*100.0}
    return None

def save_espn_event_bundle(sport, event, league_code=None, include_summary=True):
    event_name=event.get("name") or f"{sport} event"
    save_event_snapshot(sport,event_name,"scoreboard",event,f"ESPN public {sport} scoreboard")
    if include_summary and event.get("id"):
        try:
            summary=fetch_espn_summary(sport,event["id"],league_code)
            save_event_snapshot(sport,event_name,"event summary",summary,f"ESPN public {sport} summary")
            seen=set()
            for item in _collect_named_athletes(summary):
                nm=str(item.get("name") or "").strip()
                if nm and nm.lower() not in seen:
                    seen.add(nm.lower())
                    save_event_snapshot(sport,event_name,nm,item.get("data"),f"ESPN public {sport} summary")
        except Exception:
            pass

def sync_espn_sport(sport, days=1, league_code=None, include_summary=True, max_events=40):
    saved=0
    event_count=0
    for offset in range(max(1,int(days))):
        d=date.today()-pd.Timedelta(days=offset)
        try:
            games=fetch_espn_scoreboard(sport,d,league_code)
        except Exception:
            continue
        for g in games:
            if event_count>=max_events:
                return saved,event_count
            save_espn_event_bundle(sport,g,league_code,include_summary)
            event_count+=1
            saved+=1
    return saved,event_count

@st.cache_data(ttl=900, show_spinner=False)
def fetch_squiggle_games(year=None):
    year=int(year or date.today().year)
    url=f"https://api.squiggle.com.au/?q=games;year={year}"
    r=requests.get(url,headers={"User-Agent":"StakeLab-Betting-Tracker/1.0"},timeout=18)
    r.raise_for_status()
    games=r.json().get("games",[])
    return sorted(games,key=lambda x:str(x.get("date","")),reverse=True)

def fetch_configured_json(url_secret, key_secret=None, params=None):
    url=_secret(url_secret)
    if not url:
        return None
    headers={"User-Agent":"StakeLab/1.0","Accept":"application/json"}
    key=_secret(key_secret) if key_secret else ""
    if key:
        headers["Authorization"]=f"Bearer {key}"
        headers["X-API-Key"]=key
    r=requests.get(url,params=params or {},headers=headers,timeout=25)
    r.raise_for_status()
    return r.json()

def save_generic_feed(sport,payload,source_name):
    if payload is None:
        return 0
    rows=payload if isinstance(payload,list) else payload.get("data") if isinstance(payload,dict) and isinstance(payload.get("data"),list) else [payload]
    n=0
    for i,row in enumerate(rows[:500]):
        if not isinstance(row,(dict,list)):
            row={"value":row}
        if isinstance(row,dict):
            event=(row.get("event") or row.get("race") or row.get("meeting") or row.get("name") or row.get("fixture") or f"{sport} data")
            subject=(row.get("player") or row.get("runner") or row.get("dog") or row.get("horse") or row.get("selection") or row.get("subject") or "structured feed")
            if isinstance(subject,dict):
                subject=subject.get("name") or subject.get("displayName") or "structured feed"
        else:
            event=f"{sport} data"; subject="structured feed"
        save_event_snapshot(sport,str(event),str(subject),row,source_name)
        n+=1
    return n

def import_structured_csv(sport, uploaded_file, source_name="User imported structured CSV"):
    df=pd.read_csv(uploaded_file)
    n=0
    for _,row in df.head(1000).iterrows():
        data=row.to_dict()
        event=str(data.get("event") or data.get("race") or data.get("fixture") or data.get("match") or f"{sport} imported row")
        subject=str(data.get("player") or data.get("runner") or data.get("horse") or data.get("greyhound") or data.get("selection") or data.get("subject") or "imported row")
        save_event_snapshot(sport,event,subject,data,source_name)
        n+=1
    return n

def source_status_for_sport(sport):
    if sport in ESPN_FEEDS:
        return "Free public ESPN scoreboard + event summaries/player stat objects where supplied"
    if sport=="AFL":
        return "Free Squiggle fixtures/results + optional AFL_PLAYER_API_URL or CSV for player-level verification"
    if sport=="Soccer":
        return "Free public ESPN league scoreboards/summaries + optional provider import"
    if sport=="Tennis":
        return "Free public ESPN ATP/WTA scoreboards/summaries + optional provider import"
    if sport=="Horses":
        return "Configured HORSE_DATA_API_URL or structured CSV import required for runner-level verification"
    if sport=="Greyhounds":
        return "Configured GREYHOUND_DATA_API_URL or structured CSV import required for runner-level verification"
    return "Connector available through structured import"

@st.cache_data(ttl=300, show_spinner=False)
def fetch_nba_scoreboard(day=None):
    day=(day or date.today()).strftime("%Y%m%d") if hasattr((day or date.today()),"strftime") else str(day).replace("-","")
    url=f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={day}"
    r=requests.get(url,timeout=15); r.raise_for_status(); raw=r.json()
    out=[]
    for e in raw.get("events",[]):
        comp=(e.get("competitions") or [{}])[0]
        teams=[]
        for c in comp.get("competitors",[]):
            teams.append({"team":c.get("team",{}).get("displayName"),"homeAway":c.get("homeAway"),"score":c.get("score")})
        out.append({"id":e.get("id"),"name":e.get("name"),"date":e.get("date"),"status":e.get("status",{}).get("type",{}).get("description"),"teams":teams})
    return out

@st.cache_data(ttl=900, show_spinner=False)
def fetch_afl_games(year=None):
    year=int(year or date.today().year)
    url=f"https://api.squiggle.com.au/?q=games;year={year}"
    r=requests.get(url,headers={"User-Agent":"StakeLab-Betting-Tracker/1.0"},timeout=15); r.raise_for_status()
    games=r.json().get("games",[])
    games=sorted(games,key=lambda x:str(x.get("date","")),reverse=True)
    return games[:120]

conn().close()

def _secret(name):
    v=os.getenv(name,"")
    if v:
        return v
    try:
        return st.secrets.get(name,"")
    except Exception:
        return ""

def evidence_audit(sport,evidence,data_ctx):
    """Free deterministic evidence checks; never invents data."""
    e=(evidence or "").lower()
    checks={
        "volume / opportunity":["target","targets","attempt","attempts","minutes","routes","carries","usage","volume","touches"],
        "recent form / sample":["last 5","last 10","recent","season","average","avg","3/3","hit rate","form"],
        "matchup / opponent":["matchup","opponent","defense","defence","coverage","pace","allowed","vs "],
        "role / availability":["role","starter","starting","injury","injuries","questionable","probable","out","minutes"],
        "price / market":["odds","price","line","market","closing","movement","implied"],
    }
    if sport in ("Horses","Greyhounds"):
        checks.update({
            "barrier / box / map":["barrier","box","speed map","map","draw"],
            "track / going":["track","going","heavy","soft","good","distance","course"],
            "class / grade":["class","grade","weight"],
            "sectionals / speed":["sectional","split","early speed","speed figure","time"],
        })
    found=[name for name,keys in checks.items() if any(k in e for k in keys)]
    missing=[name for name in checks if name not in found]
    return found,missing,bool(data_ctx)


def _summary():
    bets=q("SELECT * FROM bets")
    settings=q("SELECT * FROM bankroll_settings WHERE id=1").iloc[0]
    tx=q("SELECT * FROM bankroll_transactions ORDER BY txn_date,id")
    settled=bets[bets.result.isin(["Won","Lost","Push"])].copy() if not bets.empty else pd.DataFrame()
    start=float(settings.starting_bankroll)
    dep=float(tx.loc[tx.txn_type=="Deposit","amount"].sum()) if not tx.empty else 0
    wd=float(tx.loc[tx.txn_type=="Withdrawal","amount"].sum()) if not tx.empty else 0
    pnl=float(settled.pnl.sum()) if not settled.empty else 0
    bank=start+dep-wd+pnl
    stake=float(settled.stake.sum()) if not settled.empty else 0
    roi=pnl/stake*100 if stake else 0
    clv_avg=float(settled.clv.mean()) if not settled.empty and settled.clv.notna().any() else 0
    wl=settled[settled.result.isin(["Won","Lost"])] if not settled.empty else pd.DataFrame()
    win=(wl.result.eq("Won").mean()*100) if not wl.empty else 0
    pending=bets[bets.result.eq("Pending")] if not bets.empty else pd.DataFrame()
    open_stake=float(pending.stake.sum()) if not pending.empty else 0
    return dict(bets=bets,settled=settled,settings=settings,tx=tx,bank=bank,pnl=pnl,roi=roi,clv=clv_avg,win=win,pending=pending,open_stake=open_stake)

from zoneinfo import ZoneInfo
from datetime import timedelta
LOCAL_ZONE=ZoneInfo("Australia/Melbourne")
execsql("CREATE TABLE IF NOT EXISTS weekly_budget_settings(id INTEGER PRIMARY KEY CHECK(id=1),active INTEGER DEFAULT 0,unit_value REAL DEFAULT 20,unit_limit REAL DEFAULT 20)")
execsql("INSERT OR IGNORE INTO weekly_budget_settings(id) VALUES(1)")
execsql("CREATE TABLE IF NOT EXISTS weekly_budget_weeks(week_start TEXT PRIMARY KEY,unit_value REAL NOT NULL,unit_limit REAL NOT NULL)")
execsql("CREATE TABLE IF NOT EXISTS weekly_budget_spend(id INTEGER PRIMARY KEY,bet_id INTEGER UNIQUE,week_start TEXT NOT NULL,placed_at TEXT NOT NULL,units REAL NOT NULL,stake REAL NOT NULL)")

def weekly_budget_status(now=None,database=None):
    owns=database is None
    db=database or conn()
    try:
        settings=dict(db.execute('SELECT * FROM weekly_budget_settings WHERE id=1').fetchone())
        now=now or datetime.now(LOCAL_ZONE)
        if now.tzinfo is None:now=now.replace(tzinfo=LOCAL_ZONE)
        local=now.astimezone(LOCAL_ZONE)
        monday=local.date()-timedelta(days=local.weekday())
        week=monday.isoformat()
        if settings['active']:
            db.execute('INSERT OR IGNORE INTO weekly_budget_weeks(week_start,unit_value,unit_limit) VALUES(?,?,?)',(week,settings['unit_value'],settings['unit_limit']))
        snapshot=db.execute('SELECT * FROM weekly_budget_weeks WHERE week_start=?',(week,)).fetchone()
        config=dict(snapshot) if snapshot else dict(unit_value=settings['unit_value'],unit_limit=settings['unit_limit'])
        spent=float(db.execute('SELECT COALESCE(SUM(units),0) FROM weekly_budget_spend WHERE week_start=?',(week,)).fetchone()[0])
        if owns:db.commit()
        return dict(active=bool(settings['active']),week_start=week,next_reset=monday+timedelta(days=7),unit_value=float(config['unit_value']),limit=float(config['unit_limit']),used=spent,remaining=float(config['unit_limit'])-spent,settings=settings)
    finally:
        if owns:db.close()

def save_budget_bet(sql,args):
    db=conn()
    try:
        db.execute('BEGIN IMMEDIATE')
        now=datetime.now(LOCAL_ZONE)
        budget=weekly_budget_status(now,db)
        args=list(args);stake=float(args[12])
        if not math.isfinite(stake) or stake<=0:raise ValueError('Enter a stake greater than zero.')
        factors=json.loads(args[20] or '{}')
        if budget['active']:
            unit=budget['unit_value'];units=stake/unit
            if units>budget['remaining']+1e-9:raise ValueError(f"This bet uses {units:.2f}u, but only {max(0,budget['remaining']):.2f}u remains this week.")
            factors.update(unit_value=unit,stake_units=units,budget_mode='Weekly unit limit',budget_week=budget['week_start'])
        else:
            settings=dict(db.execute('SELECT * FROM bankroll_settings WHERE id=1').fetchone())
            cash=float(db.execute("SELECT COALESCE(SUM(CASE WHEN txn_type='Deposit' THEN amount ELSE -amount END),0) FROM bankroll_transactions").fetchone()[0])
            pnl=float(db.execute("SELECT COALESCE(SUM(pnl),0) FROM bets WHERE result IN ('Won','Lost','Push')").fetchone()[0])
            unit=(float(settings['starting_bankroll'])+cash+pnl)*float(settings['unit_percent'])/100
            if unit>0:factors.update(unit_value=unit,stake_units=stake/unit,budget_mode='Bankroll')
        args[0]=now.isoformat();args[20]=json.dumps(factors)
        bet_id=db.execute(sql,tuple(args)).lastrowid
        if budget['active']:db.execute('INSERT INTO weekly_budget_spend(bet_id,week_start,placed_at,units,stake) VALUES(?,?,?,?,?)',(bet_id,budget['week_start'],now.isoformat(),units,stake))
        db.commit();return bet_id
    except Exception:
        db.rollback();raise
    finally:db.close()

def placement_unit(value):
    try:
        unit=float(json.loads(value or '{}').get('unit_value',0))
        return unit if math.isfinite(unit) and unit>0 else None
    except (ValueError,TypeError,AttributeError):return None

def net_unit_results(bets):
    if bets.empty:return None,0
    units=pd.to_numeric(bets.factors_json.map(placement_unit),errors='coerce')
    valid=units.notna()&units.gt(0)
    return (float(pd.to_numeric(bets.loc[valid,'pnl'],errors='coerce').div(units[valid]).sum()),int(valid.sum())) if valid.any() else (None,0)

def attempt_budget_save(sql,args):
    try:return save_budget_bet(sql,args)
    except ValueError as error:
        st.error(str(error));return None

budget=weekly_budget_status()
summary=_summary()
if budget['active']:summary['bank']=0.0
# TOP NAVIGATION
st.markdown("<div class='tracker-brand sl-brand'><img src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5NiA5NiIgcm9sZT0iaW1nIiBhcmlhLWxhYmVsPSJTdGFrZUxhYiBmbGFzayBhbmQgY2hhcnQgbG9nbyI+CjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0ic2wiIHgxPSIwIiB5MT0iMSIgeDI9IjEiIHkyPSIwIj48c3RvcCBzdG9wLWNvbG9yPSIjMzJiNWZmIi8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjOGRkOGZmIi8+PC9saW5lYXJHcmFkaWVudD48L2RlZnM+CjxyZWN0IHg9IjIiIHk9IjIiIHdpZHRoPSI5MiIgaGVpZ2h0PSI5MiIgcng9IjI0IiBmaWxsPSIjMWExYzIwIi8+CjxwYXRoIGQ9Ik0zNSAyMWgyNk0zOSAyMXYyMEwyNCA2NWMtNCA3IDAgMTIgOCAxMmgzMmM4IDAgMTItNSA4LTEyTDU3IDQxVjIxIiBmaWxsPSJub25lIiBzdHJva2U9InVybCgjc2wpIiBzdHJva2Utd2lkdGg9IjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8cGF0aCBkPSJtMzMgNjIgMTAtMTAgMTAgNiAxMC0xNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMzJiNWZmIiBzdHJva2Utd2lkdGg9IjQiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8Y2lyY2xlIGN4PSI2MyIgY3k9IjQ0IiByPSIzIiBmaWxsPSIjOGRkOGZmIi8+Cjwvc3ZnPgo=' alt='StakeLab logo' width='52' height='52'><div>Stake<b>Lab</b><small>TRACK YOUR EDGE</small></div></div>",unsafe_allow_html=True)
# Small vector icons are embedded, so app.py remains the only replacement file.
import base64
ICON_PATHS={
    'NBA':'<circle cx="16" cy="16" r="12.5"/><path d="M3.5 16h25M16 3.5v25M7.2 7.2c7 4 7 13.6 0 17.6M24.8 7.2c-7 4-7 13.6 0 17.6"/>',
    'NFL':'<g transform="rotate(-32 16 16)"><path d="M2 16C8 4 24 4 30 16C24 28 8 28 2 16Z"/><path d="M7 9v14M25 9v14M10 16h12M12 13.5v5M16 13.5v5M20 13.5v5"/></g>',
    'AFL':'<g transform="rotate(-32 16 16)"><ellipse cx="16" cy="16" rx="14" ry="8.5" stroke="#42bdff"/><path d="M3 16c7-4 19-4 26 0M3 16c7 4 19 4 26 0" stroke="#42bdff"/><text x="16" y="18" fill="#f1bdc3" stroke="none" text-anchor="middle" font-family="Arial,sans-serif" font-size="6" font-weight="bold">AFL</text></g>',
    'Horses':'<path d="M6 29C5 20 7 12 14 7L17 5l1-3 2 5 3 2 5 7v3l-3 2-5-3-3 2 3 9M14 7c-5 1-8 6-9 12M17 11l3 1M25 16h1"/><path d="M17 20c-2 2-3 5-2 9"/>',
    'Greyhounds':'<g transform="translate(0 1)"><path d="M2 15c3 1 5-2 8-3 4-2 7 1 10 0l4-4 1-3 2 3 4 2v2l-5 1-3 5c-1 3-3 4-5 3l-4-3-4 1-4 5-4 1 5-7 1-3"/><path d="m13 18 3 8 5 1m1-8 5 5 4-1M9 15l-5-2-3-3"/></g>',
    'chart':'<path d="M5 4v24h24M9 21l6-7 5 3 8-11"/>',
    'plus':'<circle cx="16" cy="16" r="12"/><path d="M16 9v14M9 16h14"/>',
    'layers':'<path d="m16 3 13 7-13 7-13-7Zm-13 15 13 7 13-7M3 24l13 7 13-7"/>',
    'notes':'<rect x="7" y="4" width="21" height="24" rx="3"/><path d="M4 9h6M4 16h6M4 23h6M14 10h8M14 16h8M14 22h5"/>',
    'calendar':'<rect x="4" y="6" width="24" height="23" rx="3"/><path d="M10 3v7M22 3v7M4 14h24M10 20h3M19 20h3M10 25h3"/>',
    'report':'<path d="M7 3h13l6 6v20H7ZM20 3v7h6M12 23v-5M17 23v-9M22 23v-7"/>',
    'wallet':'<rect x="4" y="7" width="24" height="21" rx="3"/><path d="M4 11h24M28 17h-8v6h8M7 7V4h18v3M23 20h.1"/>',
    'tag':'<path d="M3 4h12l14 14-11 11L3 14Z"/><circle cx="9" cy="10" r="2"/>',
    'check':'<circle cx="16" cy="16" r="12"/><path d="m9 16 5 5 9-10"/>',
    'cross':'<circle cx="16" cy="16" r="12"/><path d="m11 11 10 10m0-10-10 10"/>',
    'clock':'<circle cx="16" cy="16" r="12"/><path d="M16 8v9l6 3"/>',
    'settings':'<circle cx="16" cy="16" r="5"/><path d="M16 3v4M16 25v4M3 16h4M25 16h4M7 7l3 3M22 22l3 3M7 25l3-3M22 10l3-3"/>',
    'database':'<ellipse cx="16" cy="7" rx="11" ry="4"/><path d="M5 7v18c0 6 22 6 22 0V7M5 16c0 6 22 6 22 0"/>',
    'ball':'<circle cx="16" cy="16" r="12"/><path d="m16 9 6 5-2 7h-8l-2-7Z"/>',
    'ticket':'<path d="M3 8h26v6a3 3 0 0 0 0 6v5H3v-5a3 3 0 0 0 0-6ZM21 8v17"/>',
}
def icon_data(name):
    svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="none" stroke="#42bdff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'+ICON_PATHS.get(name,ICON_PATHS['ball'])+'</svg>'
    return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()

nav_items=["Dashboard","Log Bet","Multis","Results & Notes","Performance","Monthly Reports","Bet Calendar","Bankroll","Bet History","Today","Analyse Bet","Settings"]
if "requested_nav" in st.session_state:
    st.session_state["main_nav"]=st.session_state.pop("requested_nav")
if st.session_state.get("main_nav") not in nav_items:
    st.session_state["main_nav"]="Dashboard"
with st.container(key="top_navigation"):
    page=st.radio("Navigation",nav_items,horizontal=True,label_visibility="collapsed",key="main_nav")
with st.container(key="sport_navigation"):
    selected_sport=st.radio("Sport",["All"]+SPORTS+["Multi"],horizontal=True,label_visibility="collapsed",key="top_sport")
st.caption("Choose a sport for its analytics. Sport tabs also filter Today, Performance, Monthly Reports, Bet Calendar and Bet History. Bankroll shows your whole account.")
if budget['active']:
    st.info(f"Weekly allowance: {max(0,budget['remaining']):.2f}u left / {budget['limit']:.2f}u · 1u = {money(budget['unit_value'])} · Resets Monday {budget['next_reset'].strftime('%d %b')} at 00:00 Melbourne time")
icon_styles=[]
for container,sports in [('sport_navigation',['All']+SPORTS+['Multi']),('entry_sport_buttons',SPORTS)]:
    for index,sport_name in enumerate(sports,1):
        icon_name=sport_name if sport_name in ICON_PATHS else 'layers' if sport_name=='Multi' else 'chart' if sport_name=='All' else 'plus' if sport_name=='Other' else 'ball'
        icon_styles.append(f'.st-key-{container} [role="radiogroup"] > div:nth-child({index}) label::before,.st-key-{container} [role="radiogroup"] > label:nth-child({index})::before{{background-image:url("{icon_data(icon_name)}")}}')
nav_icons=['chart','plus','layers','notes','chart','report','calendar','wallet','notes','clock','chart','settings']
for index,name in enumerate(nav_icons,1):
    icon_styles.append(f'.st-key-top_navigation [role="radiogroup"] > div:nth-child({index}) label::before,.st-key-top_navigation [role="radiogroup"] > label:nth-child({index})::before{{background-image:url("{icon_data(name)}")}}')
for index,name in enumerate(['ticket','layers'],1):
    icon_styles.append(f'.st-key-wager_buttons [role="radiogroup"] > div:nth-child({index}) label::before,.st-key-wager_buttons [role="radiogroup"] > label:nth-child({index})::before{{background-image:url("{icon_data(name)}")}}')
for widget,name in [('sreason','notes'),('mreason','notes'),('sstake','wallet'),('mstake','wallet')]:
    icon_styles.append(f'.st-key-{widget} [data-testid="stWidgetLabel"]::before{{content:"";display:inline-block;width:18px;height:18px;margin-right:8px;background:url("{icon_data(name)}") center/contain no-repeat}}')
for status,name in [('won','check'),('lost','cross'),('pending','clock')]:
    icon_styles.append(f'.status-{status}::before{{content:"";display:inline-block;width:14px;height:14px;margin-right:5px;background:url("{icon_data(name)}") center/contain no-repeat;vertical-align:middle}}')
st.markdown('''<style>
.st-key-top_navigation [role="radiogroup"] label,.st-key-sport_navigation [role="radiogroup"] label,.st-key-entry_sport_buttons [role="radiogroup"] label,.st-key-wager_buttons [role="radiogroup"] label{display:flex!important;align-items:center;gap:8px!important;min-width:max-content!important;width:max-content!important;white-space:nowrap!important}
.st-key-top_navigation [role="radiogroup"],.st-key-sport_navigation [role="radiogroup"],.st-key-entry_sport_buttons [role="radiogroup"]{display:flex!important;flex-wrap:wrap!important;overflow-x:visible!important;gap:8px!important}
.st-key-top_navigation [role="radiogroup"] > div,.st-key-sport_navigation [role="radiogroup"] > div,.st-key-entry_sport_buttons [role="radiogroup"] > div,.st-key-wager_buttons [role="radiogroup"] > div{flex:0 0 auto!important;width:auto!important;min-width:max-content!important}
.st-key-top_navigation [role="radiogroup"] label p,.st-key-sport_navigation [role="radiogroup"] label p,.st-key-entry_sport_buttons [role="radiogroup"] label p,.st-key-wager_buttons [role="radiogroup"] label p{white-space:nowrap!important;word-break:normal!important;overflow-wrap:normal!important;width:auto!important;margin:0!important}
.st-key-top_navigation [role="radiogroup"] label > div:not(:has(p)),.st-key-sport_navigation [role="radiogroup"] label > div:not(:has(p)),.st-key-entry_sport_buttons [role="radiogroup"] label > div:not(:has(p)),.st-key-wager_buttons [role="radiogroup"] label > div:not(:has(p)){display:none!important}
.st-key-top_navigation [role="radiogroup"] label::before,.st-key-sport_navigation [role="radiogroup"] label::before,.st-key-entry_sport_buttons [role="radiogroup"] label::before,.st-key-wager_buttons [role="radiogroup"] label::before{content:"";display:block;flex:0 0 20px;width:20px;height:20px;background-position:center;background-size:contain;background-repeat:no-repeat;opacity:.7}
.st-key-sport_navigation [role="radiogroup"] label::before,.st-key-entry_sport_buttons [role="radiogroup"] label::before{width:24px;height:24px;flex-basis:24px}
.st-key-top_navigation label:has(input:checked)::before,.st-key-sport_navigation label:has(input:checked)::before,.st-key-entry_sport_buttons label:has(input:checked)::before,.st-key-wager_buttons label:has(input:checked)::before{opacity:1;filter:drop-shadow(0 0 4px #32b5ff45)}
[data-testid="stPills"] button{background:#1a1c20!important;border:1px solid #3c424b!important;color:#bac8d8!important;border-radius:6px!important;min-height:44px!important}
[data-testid="stPills"] button[aria-selected="true"],[data-testid="stPills"] button[aria-pressed="true"],[data-testid="stBaseButton-pillsActive"]{background:#142f43!important;color:#b6e7ff!important;border-color:#32b5ff!important;box-shadow:0 0 10px #32b5ff18!important}
[data-testid="stPills"] button p{font-size:13px!important}
@media(prefers-reduced-motion:reduce){[data-testid="stPills"] button{transition:none!important}}
</style>'''+ '<style>'+''.join(icon_styles)+'</style>',unsafe_allow_html=True)
if "saved_notice" in st.session_state:
    st.toast(st.session_state.pop("saved_notice"),icon="✅")

def sport_rows(df):
    return df if df.empty or selected_sport=="All" else df[df.sport.eq(selected_sport)].copy()

def notify_saved(message):
    st.session_state["saved_notice"]=message
    st.rerun()

# Account balance stays global; sports metrics use only the selected sport.
if page in ("Dashboard","Today") and selected_sport!="All":
    summary=summary.copy()
    for name in ("bets","settled","pending"):
        summary[name]=sport_rows(summary[name])
    settled=summary["settled"]
    summary["pnl"]=float(settled.pnl.sum()) if not settled.empty else 0
    total_stake=float(settled.stake.sum()) if not settled.empty else 0
    summary["roi"]=summary["pnl"]/total_stake*100 if total_stake else 0
    summary["clv"]=float(settled.clv.mean()) if not settled.empty and settled.clv.notna().any() else 0
    wins_losses=settled[settled.result.isin(["Won","Lost"])] if not settled.empty else settled
    summary["win"]=float(wins_losses.result.eq("Won").mean()*100) if not wins_losses.empty else 0
    summary["open_stake"]=float(summary["pending"].stake.sum()) if not summary["pending"].empty else 0

# TODAY
if page=="Today":
    st.markdown("<div class='page-kicker'>Daily workspace</div><div class='page-title'>Today</div><div class='page-copy'>Open bets, exposure, latest alerts and items that need attention today.</div>",unsafe_allow_html=True)
    s=summary
    today_str=str(date.today())

    t1,t2,t3,t4=st.columns(4)
    todays_bets=s["bets"][s["bets"]["event_date"].astype(str).eq(today_str)] if not s["bets"].empty else pd.DataFrame()
    todays_settled=todays_bets[todays_bets.result.isin(["Won","Lost","Push"])] if not todays_bets.empty else pd.DataFrame()
    todays_pnl=float(todays_settled.pnl.sum()) if not todays_settled.empty else 0.0
    t1.metric("Today's bets",len(todays_bets))
    t2.metric("Open bets",len(s["pending"]))
    t3.metric("Open stake",money(s["open_stake"]))
    t4.metric("Today's P&L",money(todays_pnl))

    st.markdown("<div class='panel-title'>Quick Actions</div>",unsafe_allow_html=True)
    qa1,qa2,qa3=st.columns(3)
    with qa1:
        if st.button("🔎 Analyse Bet",use_container_width=True,key="today_analyse"):
            st.session_state["requested_nav"]="Analyse Bet"; st.rerun()
    with qa2:
        if st.button("＋ Log Bet",use_container_width=True,key="today_log"):
            st.session_state["requested_nav"]="Log Bet"; st.rerun()
    with qa3:
        if st.button("🧩 Add Multi",use_container_width=True,key="today_multi"):
            st.session_state["requested_nav"]="Multis"; st.rerun()

    left,right=st.columns([2.1,1],gap="large")
    with left:
        st.markdown("<div class='panel-title'>Open / Pending Bets</div>",unsafe_allow_html=True)
        if s["pending"].empty:
            st.info("No open bets right now.")
        else:
            cols=["event_date","sport","event","bet_type","selection","odds","stake","result"]
            st.dataframe(s["pending"][cols].sort_values(["event_date","id"],ascending=False),use_container_width=True,hide_index=True,height=260)

        st.markdown("<div class='panel-title'>Today's Bets</div>",unsafe_allow_html=True)
        if todays_bets.empty:
            st.info("No bets dated today yet.")
        else:
            show=todays_bets.copy()
            show["P&L"]=show["pnl"].map(money)
            st.dataframe(show[["sport","event","bet_type","selection","odds","stake","result","P&L"]],use_container_width=True,hide_index=True)

    with right:
        st.markdown("<div class='panel-title'>⚠ Attention</div>",unsafe_allow_html=True)
        msgs=[]
        if s["bank"]>0 and s["open_stake"]/s["bank"]>0.10:
            msgs.append(("Bankroll exposure",f"{s['open_stake']/s['bank']*100:.1f}% of bankroll is currently open."))
        if s["clv"] < -1 and len(s["settled"])>=3:
            msgs.append(("Negative CLV trend",f"Average implied-probability CLV is {s['clv']:.2f}%."))
        old_pending=s["pending"][pd.to_datetime(s["pending"]["event_date"],errors="coerce") < pd.Timestamp(date.today())] if not s["pending"].empty else pd.DataFrame()
        if not old_pending.empty:
            msgs.append(("Needs settlement",f"{len(old_pending)} past-dated pending bet(s) may need a result entered."))
        latest=q("SELECT MAX(captured_at) AS latest FROM event_data")
        if not latest.empty and pd.notna(latest.iloc[0]["latest"]):
            try:
                last=pd.to_datetime(latest.iloc[0]["latest"])
                hrs=(pd.Timestamp.now()-last).total_seconds()/3600
                if hrs>12:
                    msgs.append(("Data may be stale",f"Latest structured sports data is about {hrs:.0f} hours old."))
            except Exception:
                pass
        if not msgs:
            msgs=[("All clear","No urgent rule-based alerts right now.")]
        for title,copy in msgs:
            st.markdown(f"<div class='alert-card'><div class='alert-title'>{title}</div><div class='alert-copy'>{copy}</div></div>",unsafe_allow_html=True)

# DASHBOARD
if page=="Dashboard" and selected_sport=="All":
    st.markdown("<div class='page-kicker'>Overview & insights</div><div class='page-title'>Dashboard</div><div class='page-copy'>Your bankroll, process quality, open exposure and latest StakeLab signals in one view.</div>",unsafe_allow_html=True)

    qa1,qa2,qa3=st.columns(3)
    with qa1:
        if st.button("🔎 Analyse Bet",use_container_width=True,key="dash_analyse"):
            st.session_state["requested_nav"]="Analyse Bet"; st.rerun()
    with qa2:
        if st.button("＋ Log Bet",use_container_width=True,key="dash_log"):
            st.session_state["requested_nav"]="Log Bet"; st.rerun()
    with qa3:
        if st.button("🧩 Add Multi",use_container_width=True,key="dash_multi"):
            st.session_state["requested_nav"]="Multis"; st.rerun()
    s=summary; open_count=len(s["pending"])
    account_label='Weekly units left' if budget['active'] else 'Bankroll'
    account_value=f"{max(0,budget['remaining']):.2f}u" if budget['active'] else money(s['bank'])
    st.markdown(f"""<div class='kpi-grid'><div class='kpi-card'><div class='kpi-label'>{account_label}</div><div class='kpi-value'>{account_value}</div><div class='kpi-delta'>{money(s['pnl'])} betting P&L</div></div><div class='kpi-card'><div class='kpi-label'>ROI</div><div class='kpi-value'>{pct(s['roi'])}</div><div class='kpi-delta'>{len(s['settled'])} settled bets</div></div><div class='kpi-card'><div class='kpi-label'>CLV</div><div class='kpi-value'>{pct(s['clv'])}</div><div class='kpi-delta'>Implied-probability CLV</div></div><div class='kpi-card'><div class='kpi-label'>Win Rate</div><div class='kpi-value'>{pct(s['win'])}</div><div class='kpi-delta'>Won / lost bets only</div></div><div class='kpi-card'><div class='kpi-label'>Open Bets</div><div class='kpi-value'>{open_count}</div><div class='kpi-delta'>{money(s['open_stake'])} currently staked</div></div></div>""",unsafe_allow_html=True)
    main,right=st.columns([3.15,1.05],gap="large")
    with main:
        c1,c2=st.columns([1.45,1],gap="large")
        with c1:
            st.markdown("<div class='panel-title'>"+("Profit Growth" if budget["active"] else "Bankroll Growth")+"</div><div class='panel-sub'>"+("Cumulative settled P&L" if budget["active"] else "Settled P&L plus cash movements")+"</div>",unsafe_allow_html=True)
            events=[]
            if not budget["active"] and not s["tx"].empty:
                for _,r in s["tx"].iterrows(): events.append({"date":pd.to_datetime(r.txn_date,errors="coerce"),"change":float(r.amount) if r.txn_type=="Deposit" else -float(r.amount)})
            if not s["settled"].empty:
                for _,r in s["settled"].iterrows(): events.append({"date":pd.to_datetime(r.event_date,errors="coerce"),"change":float(r.pnl or 0)})
            ev=pd.DataFrame(events); start=0.0 if budget["active"] else float(s["settings"].starting_bankroll)
            if not ev.empty:
                ev=ev.dropna(subset=["date"]).sort_values("date"); ev["Bankroll"]=start+ev["change"].cumsum(); st.area_chart(ev.set_index("date")[["Bankroll"]],use_container_width=True,height=290,color="#32b5ff")
            else: st.info("Settle a bet or add a bankroll transaction to start the growth chart.")
        with c2:
            st.markdown("<div class='panel-title'>Performance by Sport</div><div class='panel-sub'>ROI from settled bets</div>",unsafe_allow_html=True)
            if not s["settled"].empty:
                perf=s["settled"].groupby("sport").agg(Bets=("id","count"),Stake=("stake","sum"),PnL=("pnl","sum")); perf["ROI"]=perf.apply(lambda r:(r.PnL/r.Stake*100) if r.Stake else 0,axis=1); st.bar_chart(perf[["ROI"]],use_container_width=True,height=290,color="#32b5ff")
            else: st.info("No settled bets yet.")

        st.markdown("<div class='panel-title'>Model / Process Scorecard</div><div class='panel-sub'>Process metrics from your settled history</div>",unsafe_allow_html=True)
        settled=s["settled"].copy()
        if settled.empty:
            st.info("Settle more bets to build your process scorecard.")
        else:
            pos_clv=int((settled["clv"].fillna(0)>0).sum())
            neg_clv=int((settled["clv"].fillna(0)<0).sum())
            avg_stake_pct=(settled["stake"].mean()/s["bank"]*100) if s["bank"] else 0
            by_type=settled.groupby("bet_type").agg(Stake=("stake","sum"),PnL=("pnl","sum"),Bets=("id","count"))
            by_type["ROI"]=by_type.apply(lambda r:(r.PnL/r.Stake*100) if r.Stake else 0,axis=1)
            best_type=by_type["ROI"].idxmax() if not by_type.empty else "—"
            worst_type=by_type["ROI"].idxmin() if not by_type.empty else "—"
            score_html=f"""
            <div class="score-grid">
              <div class="score-card"><div class="score-label">Avg CLV</div><div class="score-value">{pct(s['clv'])}</div><div class="score-note">{pos_clv} positive / {neg_clv} negative</div></div>
              <div class="score-card"><div class="score-label">Avg Stake / Bankroll</div><div class="score-value">{avg_stake_pct:.1f}%</div><div class="score-note">Exposure discipline</div></div>
              <div class="score-card"><div class="score-label">Best Bet Type</div><div class="score-value">{best_type}</div><div class="score-note">By ROI</div></div>
              <div class="score-card"><div class="score-label">Worst Bet Type</div><div class="score-value">{worst_type}</div><div class="score-note">Review for leaks</div></div>
            </div>"""
            st.markdown(score_html,unsafe_allow_html=True)
            st.dataframe(by_type.reset_index()[["bet_type","Bets","ROI","PnL"]],use_container_width=True,hide_index=True,height=220)

        st.markdown("<div class='panel-title'>Recent Bets</div>",unsafe_allow_html=True)
        if not s["bets"].empty:
            recent=s["bets"].sort_values(["event_date","id"],ascending=False).head(10).copy(); recent["P&L"]=recent["pnl"].map(money); recent["CLV"]=recent["clv"].map(pct)
            rows=[]
            for _,r in recent.iterrows():
                result=str(r.get("result","Pending")); cls={"Won":"status-won","Lost":"status-lost","Pending":"status-pending","Push":"status-push"}.get(result,"status-push")
                rows.append(f"<tr><td>{html.escape(str(r.get('event_date','')))}</td><td>{html.escape(str(r.get('sport','')))}</td><td>{html.escape(str(r.get('event','')))}</td><td>{html.escape(str(r.get('bet_type','')))}</td><td>{html.escape(str(r.get('selection','')))}</td><td>{float(r.get('odds') or 0):.2f}</td><td>{money(float(r.get('stake') or 0))}</td><td><span class='status-pill {cls}'>{html.escape(result)}</span></td><td>{html.escape(str(r.get('P&L','')))}</td><td>{html.escape(str(r.get('CLV','')))}</td></tr>")
            table="<table class='mock-table'><thead><tr><th>Date</th><th>Sport</th><th>Event</th><th>Bet type</th><th>Selection</th><th>Odds</th><th>Stake</th><th>Result</th><th>P&L</th><th>CLV</th></tr></thead><tbody>"+"".join(rows)+"</tbody></table>"
            st.markdown(table,unsafe_allow_html=True)
        else: st.info("Log your first bet to populate this table.")
    with right:
        st.markdown("<div class='panel-title'>🔔 Tracker Alerts</div><div class='panel-sub'>Rule-based alerts from stored data and bankroll</div>",unsafe_allow_html=True)
        alerts=[]
        # Stronger rule-based alerts that work without paid AI.
        if s["bank"]>0 and s["open_stake"]/s["bank"]>0.10:
            alerts.append(("amber","Bankroll warning",f"Open stake is {s['open_stake']/s['bank']*100:.1f}% of bankroll. Consider concentration risk."))
        if not s["pending"].empty:
            exp=s["pending"].groupby("sport")["stake"].sum().sort_values(ascending=False)
            if len(exp) and s["bank"]>0 and float(exp.iloc[0])/s["bank"]>0.08:
                alerts.append(("amber","Sport concentration",f"{exp.index[0]} accounts for {float(exp.iloc[0])/s['bank']*100:.1f}% of bankroll in open stake."))
        if s["clv"] < -1 and len(s["settled"])>=3:
            alerts.append(("red","Price warning",f"Average CLV is {s['clv']:.2f}%. Your entries have been worse than the close on average."))
        elif s["clv"] > 1 and len(s["settled"])>=3:
            alerts.append(("green","Positive CLV trend",f"Average CLV is {s['clv']:.2f}% across settled bets."))
        if not s["settled"].empty:
            recent_results=s["settled"].sort_values(["event_date","id"],ascending=False).head(5)["result"].tolist()
            loss_streak=0
            for r in recent_results:
                if r=="Lost": loss_streak+=1
                else: break
            if loss_streak>=3:
                alerts.append(("red","Losing streak",f"{loss_streak} consecutive losses. Avoid stake escalation and review process quality."))
            bt=s["settled"].groupby("bet_type").agg(Stake=("stake","sum"),PnL=("pnl","sum"),Bets=("id","count"))
            bt["ROI"]=bt.apply(lambda r:(r.PnL/r.Stake*100) if r.Stake else 0,axis=1)
            bad=bt[(bt["Bets"]>=5)&(bt["ROI"]<-10)]
            if not bad.empty:
                name=bad["ROI"].idxmin()
                alerts.append(("red","Bet-type leak",f"{name} is running at {bad.loc[name,'ROI']:.1f}% ROI over {int(bad.loc[name,'Bets'])} bets."))
        data_latest=q("SELECT captured_at,sport,event,source FROM event_data ORDER BY captured_at DESC LIMIT 1")
        if not data_latest.empty:
            rr=data_latest.iloc[0]
            alerts.append(("blue","Data updated",f"{rr.sport}: {rr.event} · {rr.source}"))
            try:
                hrs=(pd.Timestamp.now()-pd.to_datetime(rr.captured_at)).total_seconds()/3600
                if hrs>12:
                    alerts.append(("amber","Data freshness warning",f"Latest structured sports data is about {hrs:.0f} hours old."))
            except Exception:
                pass
        if open_count:
            alerts.append(("green","Open positions",f"{open_count} pending bet{'s' if open_count!=1 else ''} with {money(s['open_stake'])} at risk."))
        if not alerts: alerts=[("#4bb8ff","No active alerts","Log bets and fetch data to generate alerts.")]
        for col,title,copy in alerts[:5]: st.markdown(f"<div class='alert-card'><div class='alert-row'><div class='alert-dot' style='background:{col}'></div><div><div class='alert-title'>{title}</div><div class='alert-copy'>{copy}</div></div></div></div>",unsafe_allow_html=True)
        st.markdown("<div class='panel-title' style='margin-top:14px'>📊 Analysis Signals</div><div class='panel-sub'>Latest BET / LEAN / NO BET signals from your analysis engine</div>",unsafe_allow_html=True)
        signals=q("SELECT * FROM analysis_log ORDER BY id DESC LIMIT 5")
        if signals.empty: st.markdown("<div class='signal'><div class='signal-head'><span class='badge badge-nobet'>WAITING</span><span class='muted'>No analyses yet</span></div><div class='signal-meta'>Run Analyse Bet to populate this panel.</div></div>",unsafe_allow_html=True)
        else:
            for _,r in signals.iterrows():
                cls="badge-bet" if r.gate=="BET" else "badge-lean" if r.gate=="LEAN" else "badge-nobet"; edge=f"{float(r.edge):+.1f} pp" if pd.notna(r.edge) else "edge unknown"
                st.markdown(f"<div class='signal'><div class='signal-head'><span class='badge {cls}'>{r.gate}</span><span class='green'>{edge}</span></div><div class='alert-title' style='margin-top:7px'>{r.sport} · {r.selection or r.market}</div><div class='signal-meta'>{r.market} @ {float(r.odds):.2f}</div></div>",unsafe_allow_html=True)

def bet_type_statistics(bets):
    if bets.empty:return pd.DataFrame()
    data=bets[bets.result.isin(["Won","Lost","Push"])].copy()
    if data.empty:return pd.DataFrame()
    data['bet_type']=data.bet_type.fillna('Unspecified').replace('','Unspecified')
    if 'Custom sport' in data.columns:
        other=data.sport.eq('Other')&data['Custom sport'].ne('')
        data.loc[other,'sport']='Other · '+data.loc[other,'Custom sport']
    for column in ['stake','pnl','clv']:data[column]=pd.to_numeric(data[column],errors='coerce')
    for result in ['Won','Lost','Push']:data[result]=data.result.eq(result).astype(int)
    grouped=data.groupby(['sport','bet_type'],dropna=False).agg(Bets=('id','count'),Wins=('Won','sum'),Losses=('Lost','sum'),Pushes=('Push','sum'),Stake=('stake','sum'),Profit=('pnl','sum'),CLV=('clv','mean'),CLV_samples=('clv','count')).reset_index()
    grouped['ROI (%)']=grouped.Profit.div(grouped.Stake.where(grouped.Stake.gt(0)))*100
    decisive=grouped.Wins+grouped.Losses
    grouped['Win rate (%)']=grouped.Wins.div(decisive.where(decisive.gt(0)))*100
    data['unit_value']=pd.to_numeric(data.factors_json.map(placement_unit),errors='coerce')
    data['Net units']=data.pnl.div(data.unit_value)
    unit_stats=data.groupby(['sport','bet_type'],dropna=False)['Net units'].agg(['sum','count']).reset_index().rename(columns={'sum':'Net units','count':'Unit samples'})
    grouped=grouped.merge(unit_stats,on=['sport','bet_type'],how='left')
    grouped.loc[grouped['Unit samples'].eq(0),'Net units']=float('nan')
    return grouped.sort_values(['sport','ROI (%)','Profit','Bets'],ascending=[True,False,False,False],na_position='last')

def show_best_bet_types(bets,key):
    st.markdown('### Best-performing bet types')
    table=bet_type_statistics(bets)
    if table.empty:
        st.info('Settle a bet to see bet-type statistics. Open bets are excluded.')
        return
    minimum=st.number_input('Minimum settled bets for best-type highlights',min_value=1,max_value=1000,value=5,step=1,key=key+'_minimum')
    st.caption('Ranked by ROI within each sport. All bet types remain visible; highlights require the minimum sample. Win rate excludes pushes. Missing CLV is not counted as zero.')
    for sport,group in table.groupby('sport',sort=True):
        st.markdown('#### '+str(sport))
        eligible=group[group.Bets.ge(minimum)&group['ROI (%)'].notna()]
        if not eligible.empty:
            best=eligible.iloc[0]
            st.info(f"Highest ROI: {best.bet_type} · {best['ROI (%)']:+.2f}% · {money(best.Profit)} profit · {int(best.Bets)} bets")
            profit_best=eligible.sort_values(['Profit','ROI (%)'],ascending=False).iloc[0]
            st.caption(f"Largest net profit among qualifying types: {profit_best.bet_type} ({money(profit_best.Profit)}). Historical results do not establish a predictive edge.")
        else:st.caption(f'No bet type has {minimum} settled bets yet. Statistics below are preliminary.')
        view=group.copy()
        view['Highlight eligible']=view.Bets.ge(minimum)&view['ROI (%)'].notna()
        view.insert(0,'ROI rank',range(1,len(view)+1))
        view=view.rename(columns={'bet_type':'Bet type','CLV':'Avg CLV (pp)','CLV_samples':'CLV samples'})
        st.dataframe(view[['ROI rank','Bet type','Bets','Wins','Losses','Pushes','Stake','Profit','Net units','Unit samples','ROI (%)','Win rate (%)','Avg CLV (pp)','CLV samples','Highlight eligible']].round(2),hide_index=True,use_container_width=True)

# PERFORMANCE
if page=="Performance":
    if len(summary["settled"]) < 20:
        st.warning(f"Low sample: {len(summary['settled'])} settled bets. Treat ROI, win rate and sport splits as preliminary.")
    df=q("SELECT * FROM bets")
    settings=q("SELECT * FROM bankroll_settings WHERE id=1").iloc[0]
    tx=q("SELECT * FROM bankroll_transactions ORDER BY txn_date,id")
    start_bank=float(settings.starting_bankroll)
    deposits=float(tx.loc[tx.txn_type=="Deposit","amount"].sum()) if not tx.empty else 0
    withdrawals=float(tx.loc[tx.txn_type=="Withdrawal","amount"].sum()) if not tx.empty else 0
    settled_all=df[df.result.isin(["Won","Lost","Push"])].copy() if not df.empty else pd.DataFrame()
    total_pnl=float(settled_all.pnl.sum()) if not settled_all.empty else 0
    current_bank=start_bank+deposits-withdrawals+total_pnl
    settled_all=sport_rows(settled_all)
    total_pnl=float(settled_all.pnl.sum()) if not settled_all.empty else 0
    unit_value=budget['unit_value'] if budget['active'] else current_bank*float(settings.unit_percent)/100

    a,b,c,d,e=st.columns(5)
    if budget['active']:a.metric("Weekly units remaining",f"{max(0,budget['remaining']):.2f}u")
    else:a.metric("Current Bankroll",money(current_bank),money(current_bank-start_bank-deposits+withdrawals))
    b.metric("Total P&L",money(total_pnl))
    total_stake=float(settled_all.stake.sum()) if not settled_all.empty else 0
    b_roi=total_pnl/total_stake*100 if total_stake else 0
    c.metric("ROI",pct(b_roi))
    avg_clv=float(settled_all.clv.mean()) if not settled_all.empty and settled_all.clv.notna().any() else 0
    d.metric("Avg CLV",pct(avg_clv))
    e.metric("1 Unit",money(unit_value))
    performance_units,performance_unit_samples=net_unit_results(settled_all)
    st.metric('Net units',f'{performance_units:+.2f}u' if performance_units is not None else '—')
    st.caption(f'Unit results cover {performance_unit_samples} settled bets with a recorded unit size. Historical dollar profit, ROI and CLV include all saved settled bets.')

    if df.empty:
        st.info("Your dashboard is empty. Log your first bet to start building your performance history.")
    else:
        sport_filter=selected_sport
        dff=df if sport_filter=="All" else df[df.sport==sport_filter]
        settled=dff[dff.result.isin(["Won","Lost","Push"])].copy()
        if not settled.empty:
            st.markdown("### Performance overview")
            c1,c2=st.columns(2)
            with c1:
                daily=settled.copy(); daily["event_date"]=pd.to_datetime(daily.event_date,errors="coerce")
                daily=daily.dropna(subset=["event_date"]).sort_values(["event_date","id"])
                if not daily.empty:
                    daily["Cumulative P&L"]=daily.pnl.cumsum()
                    st.caption("Cumulative profit / loss")
                    profit_chart(daily[["event_date","Cumulative P&L"]],"event_date","Cumulative P&L")
            with c2:
                outcomes=settled[settled.result.isin(["Won","Lost","Push"])].groupby("result").size()
                st.caption("Bet outcomes")
                if not outcomes.empty: st.bar_chart(outcomes,use_container_width=True)

            c3,c4=st.columns(2)
            with c3:
                sport_perf=settled.groupby("sport").agg(PnL=("pnl","sum")).sort_values("PnL",ascending=False)
                st.caption("P&L by sport")
                if not sport_perf.empty: st.bar_chart(sport_perf,use_container_width=True)
            with c4:
                type_perf=settled.groupby("bet_type").agg(PnL=("pnl","sum")).sort_values("PnL",ascending=False).head(12)
                st.caption("P&L by bet type")
                if not type_perf.empty: st.bar_chart(type_perf,use_container_width=True)

            show_best_bet_types(settled,'performance_types')
            st.markdown("### Recent bets")
            cols=["id","event_date","sport","event","bet_type","selection","line","odds","closing_odds","result","pnl","clv"]
            show=settled.sort_values(["event_date","id"],ascending=False)[cols].copy()
            show["pnl"]=show.pnl.map(money); show["clv"]=show.clv.map(pct)
            st.dataframe(show,use_container_width=True,hide_index=True)
        else:
            st.info("No settled bets for this filter yet.")

# BANKROLL MANAGER
if page=="Bankroll":
    def switch_budget_mode():
        execsql('UPDATE weekly_budget_settings SET active=? WHERE id=1',(int(st.session_state.money_mode=='Weekly unit limit'),))
    st.radio('Money management mode',['Bankroll','Weekly unit limit'],index=1 if budget['active'] else 0,key='money_mode',horizontal=True,on_change=switch_budget_mode)

if page=="Bankroll" and budget['active']:
    st.markdown("<div class='page-kicker'>Weekly staking budget</div><div class='page-title'>Weekly Unit Limit</div>",unsafe_allow_html=True)
    a,b,c,d=st.columns(4)
    a.metric('Weekly limit',f"{budget['limit']:.2f}u")
    b.metric('Units used',f"{budget['used']:.2f}u")
    c.metric('Units remaining',f"{max(0,budget['remaining']):.2f}u")
    d.metric('Fixed unit size',money(budget['unit_value']))
    st.caption(f"Week begins {budget['week_start']}. Fresh allowance each Monday at 00:00 Australia/Melbourne; unused units do not carry over. No background task is needed.")
    with st.form('weekly_settings'):
        unit_size=st.number_input('Fixed unit size ($)',min_value=0.01,value=float(budget['settings']['unit_value']),step=1.0,key='weekly_unit_size')
        unit_limit=st.number_input('Weekly unit limit',min_value=0.1,value=float(budget['settings']['unit_limit']),step=1.0,key='weekly_unit_limit')
        if st.form_submit_button('Save weekly settings',use_container_width=True):
            fresh=weekly_budget_status()
            if unit_limit+1e-9<fresh['used']:st.error('The weekly limit cannot be lower than the units already used this week.')
            else:
                execsql('UPDATE weekly_budget_settings SET unit_value=?,unit_limit=? WHERE id=1',(unit_size,unit_limit))
                execsql('UPDATE weekly_budget_weeks SET unit_limit=? WHERE week_start=?',(unit_limit,fresh['week_start']))
                if fresh['used']==0:execsql('UPDATE weekly_budget_weeks SET unit_value=? WHERE week_start=?',(unit_size,fresh['week_start']))
                notify_saved('Weekly settings saved. Unit-size changes after a bet has been logged apply from next Monday.')
    st.caption('Stakes consume units when logged, using the Melbourne placement week—not the event date. Wins, losses and pushes do not refill the allowance. Multis use their total stake once. Bets logged before this mode was enabled keep their existing analytics and do not consume the new allowance. Deleting a bet does not refund units already logged.')
    if abs(float(budget['settings']['unit_value'])-budget['unit_value'])>1e-9:st.info(f"Next week's unit size: {money(float(budget['settings']['unit_value']))}. This week stays at {money(budget['unit_value'])}.")
    units_to_stake=st.number_input('Stake calculator (units)',min_value=0.0,value=1.0,step=0.25,key='weekly_stake_calculator')
    st.metric('Stake amount',money(units_to_stake*budget['unit_value']))
    st.markdown('### Weekly usage history')
    history=q('SELECT w.week_start,w.unit_value,w.unit_limit,COALESCE(SUM(s.units),0) AS units_used,COALESCE(SUM(s.stake),0) AS stake_logged FROM weekly_budget_weeks w LEFT JOIN weekly_budget_spend s ON s.week_start=w.week_start GROUP BY w.week_start ORDER BY w.week_start DESC')
    st.dataframe(history,hide_index=True,use_container_width=True)
    st.caption('Budget usage is stake allocation. Performance / sport analytics still use settled results for profit, ROI, win rate and CLV.')

if page=="Bankroll" and not budget['active']:
    st.markdown("<div class='page-kicker'>Money management</div><div class='page-title'>Bankroll</div>",unsafe_allow_html=True)
    st.caption("Manage your bankroll, staking rules, cash movements and risk. Settled bet P&L is included automatically.")
    settings=q("SELECT * FROM bankroll_settings WHERE id=1").iloc[0]
    tx=q("SELECT * FROM bankroll_transactions ORDER BY txn_date,id")
    allbets=q("SELECT * FROM bets")
    settled=allbets[allbets.result.isin(["Won","Lost","Push"])].copy() if not allbets.empty else pd.DataFrame()
    start_bank=float(settings.starting_bankroll)
    dep=float(tx.loc[tx.txn_type=="Deposit","amount"].sum()) if not tx.empty else 0
    wd=float(tx.loc[tx.txn_type=="Withdrawal","amount"].sum()) if not tx.empty else 0
    bpnl=float(settled.pnl.sum()) if not settled.empty else 0
    current=start_bank+dep-wd+bpnl
    unit=current*float(settings.unit_percent)/100

    m1,m2,m3,m4,m5=st.columns(5)
    m1.metric("Starting Bankroll",money(start_bank)); m2.metric("Current Bankroll",money(current))
    m3.metric("Betting P&L",money(bpnl)); m4.metric("1 Unit",money(unit)); m5.metric("Net Cash Flow",money(dep-wd))

    left,right=st.columns([1,1])
    with left:
        st.markdown("### Bankroll settings")
        with st.form("bankroll_settings_form"):
            sb=st.number_input("Starting bankroll",min_value=0.0,value=float(settings.starting_bankroll),step=50.0)
            up=st.number_input("Unit size (% of current bankroll)",min_value=0.1,max_value=10.0,value=float(settings.unit_percent),step=0.1)
            mode=st.selectbox("Staking mode",["Flat units","% bankroll","Fractional Kelly"],index=["Flat units","% bankroll","Fractional Kelly"].index(settings.staking_mode) if settings.staking_mode in ["Flat units","% bankroll","Fractional Kelly"] else 0)
            kf=st.select_slider("Kelly fraction",options=[0.10,0.20,0.25,0.33,0.50,0.75,1.0],value=float(settings.kelly_fraction) if float(settings.kelly_fraction) in [0.10,0.20,0.25,0.33,0.50,0.75,1.0] else 0.25)
            if st.form_submit_button("Save bankroll settings",use_container_width=True):
                execsql("UPDATE bankroll_settings SET starting_bankroll=?,unit_percent=?,staking_mode=?,kelly_fraction=? WHERE id=1",(sb,up,mode,kf))
                notify_saved("Bankroll settings saved")
    with right:
        st.markdown("### Deposit / withdrawal")
        with st.form("cash_form"):
            td=st.date_input("Date",date.today(),key="cashdate")
            typ=st.selectbox("Transaction",["Deposit","Withdrawal"])
            amt=st.number_input("Amount",min_value=0.01,value=50.0,step=10.0)
            note=st.text_input("Note",placeholder="Optional note")
            if st.form_submit_button("Add transaction",use_container_width=True):
                execsql("INSERT INTO bankroll_transactions(created_at,txn_date,txn_type,amount,note) VALUES(?,?,?,?,?)",(datetime.now().isoformat(),str(td),typ,amt,note))
                notify_saved(f"{typ} recorded")

    st.markdown("### Bankroll growth")
    events=[]
    if not tx.empty:
        for _,r in tx.iterrows():
            events.append({"date":pd.to_datetime(r.txn_date,errors="coerce"),"change":float(r.amount) if r.txn_type=="Deposit" else -float(r.amount),"kind":r.txn_type})
    if not settled.empty:
        for _,r in settled.iterrows():
            events.append({"date":pd.to_datetime(r.event_date,errors="coerce"),"change":float(r.pnl or 0),"kind":"Bet P&L"})
    ev=pd.DataFrame(events)
    peak=start_bank; max_dd=0.0
    if not ev.empty:
        ev=ev.dropna(subset=["date"]).sort_values("date")
        ev["Bankroll"]=start_bank+ev.change.cumsum()
        ev["Peak"]=ev.Bankroll.cummax().clip(lower=start_bank)
        ev["Drawdown"]=ev.Bankroll-ev.Peak
        peak=max(start_bank,float(ev.Bankroll.max()))
        max_dd=float(ev.Drawdown.min()) if not ev.empty else 0
        profit_chart(ev[["date","Bankroll"]],"date","Bankroll")
    else:
        st.info("Your bankroll chart will appear after you settle a bet or add a transaction.")
    x1,x2,x3,x4=st.columns(4)
    x1.metric("Peak Bankroll",money(peak)); x2.metric("Max Drawdown",money(max_dd))
    winrate=(settled.result.eq("Won").sum()/settled.result.isin(["Won","Lost"]).sum()*100) if not settled.empty and settled.result.isin(["Won","Lost"]).sum() else 0
    x3.metric("Win Rate",pct(winrate)); x4.metric("Settled Bets",len(settled))

    if not settled.empty:
        trend=settled.copy(); trend["event_date"]=pd.to_datetime(trend.event_date,errors="coerce"); trend=trend.dropna(subset=["event_date"]).set_index("event_date")
        if not trend.empty:
            st.markdown("### P&L by period")
            period=st.radio("View",["Daily","Weekly","Monthly"],horizontal=True,key="pnlperiod")
            rule={"Daily":"D","Weekly":"W","Monthly":"ME"}[period]
            try: period_pnl=trend["pnl"].resample(rule).sum().to_frame("P&L")
            except ValueError: period_pnl=trend["pnl"].resample("M").sum().to_frame("P&L")
            st.bar_chart(period_pnl,use_container_width=True)

    st.markdown("### Performance breakdown")
    p1,p2=st.columns(2)
    with p1:
        if not settled.empty:
            bysport=settled.groupby("sport").agg(PnL=("pnl","sum"),Stake=("stake","sum"),Bets=("id","count"))
            bysport["ROI"]=bysport.apply(lambda r:r.PnL/r.Stake*100 if r.Stake else 0,axis=1)
            st.caption("Profit / loss by sport")
            st.bar_chart(bysport[["PnL"]],use_container_width=True)
    with p2:
        if not settled.empty:
            allocation=settled.groupby("sport")["stake"].sum().sort_values(ascending=False)
            st.caption("Stake allocation by sport")
            # Streamlit has no native pie chart, so use Altair if available through Streamlit.
            try:
                import altair as alt
                pie=allocation.reset_index(); pie.columns=["Sport","Stake"]
                chart=alt.Chart(pie).mark_arc(innerRadius=55).encode(theta=alt.Theta("Stake:Q"),color=alt.Color("Sport:N"),tooltip=["Sport:N",alt.Tooltip("Stake:Q",format="$.2f")]).properties(height=330)
                st.altair_chart(chart,use_container_width=True)
            except Exception:
                st.bar_chart(allocation,use_container_width=True)

    st.markdown("### Stake calculator")
    sc1,sc2,sc3=st.columns(3)
    calc_odds=sc1.number_input("Bet odds",min_value=1.01,value=1.90,step=0.01,key="calcodds")
    est_prob=sc2.number_input("Your estimated win probability (%)",min_value=0.1,max_value=99.9,value=55.0,step=0.5)
    units=sc3.number_input("Flat units",min_value=0.1,value=1.0,step=0.25)
    flat_stake=unit*units
    pct_stake=current*float(settings.unit_percent)/100*units
    b=calc_odds-1; p=est_prob/100; qv=1-p
    full_kelly=max(0,(b*p-qv)/b) if b>0 else 0
    kelly_stake=current*full_kelly*float(settings.kelly_fraction)
    recommended=flat_stake if settings.staking_mode=="Flat units" else pct_stake if settings.staking_mode=="% bankroll" else kelly_stake
    st.metric(f"Suggested stake · {settings.staking_mode}",money(recommended))
    if current>0 and recommended/current>0.05:
        st.warning(f"This stake is {recommended/current*100:.1f}% of your bankroll. Large single-bet exposure can create severe drawdowns.")
    st.caption("Kelly staking depends on your probability estimate being well calibrated. It is a sizing tool, not a guarantee of profit.")

    if not tx.empty:
        st.markdown("### Cash transaction history")
        st.dataframe(tx[["txn_date","txn_type","amount","note"]].sort_values("txn_date",ascending=False),use_container_width=True,hide_index=True)

SPORT_TAGS={
    "NBA":["Role change","Injury replacement","Minutes increase","Starting lineup","Pace matchup","Back-to-back","Usage increase"],
    "NFL":["Workload increase","Injury replacement","Snap share","Target share","Defensive matchup","Weather","Game script"],
    "AFL":["Role change","Midfield time","CBA increase","Injury replacement","Team selection","Ground matchup","Wet weather"],
    "Horses":["Track bias","Wet track","Distance change","Class drop","Barrier draw","Jockey change","Gear change","Fresh run"],
    "Greyhounds":["Box draw","Early speed","Track record","Distance change","Class drop","First-up","Track conditions"],
    "Multi":["Same game","Cross sport","Correlated legs","Boosted odds","Promotional bet"]}
GENERAL_TAGS=["Own research","Model pick","Tipster pick","Early price","Line movement","Boosted odds","Pre-game","Live bet"]

def saved_bet_tags(value):
    try:
        items=json.loads(value or "{}").get("tags",[])
        return list(dict.fromkeys(str(t) for t in items if isinstance(t,str))) if isinstance(items,list) else []
    except (ValueError,TypeError,AttributeError):return []

def tag_picker(sport,prefix):
    execsql("CREATE TABLE IF NOT EXISTS custom_tag_catalog(sport TEXT NOT NULL,name TEXT NOT NULL,PRIMARY KEY(sport,name))")
    def create_tag():
        tag=st.session_state.get(prefix+"_new_tag","").strip()[:40]
        if tag:
            execsql("INSERT OR IGNORE INTO custom_tag_catalog(sport,name) VALUES(?,?)",(sport,tag))
            key=prefix+"_tags_"+sport
            current=st.session_state.get(key,[])
            st.session_state[key]=list(dict.fromkeys(current+[tag]))
            st.session_state[prefix+"_new_tag"]=""
    st.markdown("#### Custom tags")
    custom=q("SELECT name FROM custom_tag_catalog WHERE sport=? ORDER BY name",(sport,))
    choices=list(dict.fromkeys(([] if sport=='Other' else SPORT_TAGS.get(sport,[])+GENERAL_TAGS)+(custom.name.tolist() if not custom.empty else [])))
    if hasattr(st,"pills"):
        picked=st.pills(f"Tags for {sport}",choices,selection_mode="multi",key=prefix+"_tags_"+sport)
    else:
        picked=st.multiselect(f"Tags for {sport}",choices,key=prefix+"_tags_"+sport)
    a,b=st.columns([3,1])
    a.text_input("Create your own tag",max_chars=40,key=prefix+"_new_tag",placeholder="e.g. Injury replacement")
    b.button("Add tag",key=prefix+"_add_tag",on_click=create_tag,use_container_width=True)
    st.caption("Optional. Select several tags; your own tags are saved for this sport.")
    return picked

# LOG BET
if page in ("Log Bet","Multis"):
    st.markdown("<div class='page-kicker'>Track your wagers</div><div class='page-title'>Log Bet / Multi</div>",unsafe_allow_html=True)
    st.caption("Log a single or a multi. Multi legs are stored individually so you can later see which markets are helping or hurting your parlays.")
    if st.session_state.get("wager_page")!=page:
        st.session_state["wager_type"]="Multi / Parlay" if page=="Multis" else "Single"
        st.session_state["wager_page"]=page
    with st.container(key="wager_buttons"):
        wager_type=st.radio("Wager type",["Single","Multi / Parlay"],horizontal=True,label_visibility="collapsed",key="wager_type")
    if wager_type=="Single":
        with st.container(key="entry_sport_buttons"):
            sport=st.radio("Sport",SPORTS,horizontal=True,key="ssport",label_visibility="collapsed")
        custom_sport=st.text_input('Custom sport name',key='scustom_sport',placeholder='e.g. Cricket, Boxing, Esports') if sport=='Other' else ''
        c1,c2,c3=st.columns(3)
        event_date=c1.date_input("Event date",date.today(),key="sdate")

        league=c3.text_input("League",value="",key="sleague")

        c1,c2,c3=st.columns(3)
        bt=c1.text_input('Custom bet type',key='scustom_type',placeholder='e.g. Runs, Map winner, Round total') if sport=='Other' else c1.selectbox("Bet type",BET_TYPES.get(sport,["Other"]),key="sbt")
        market=c2.text_input("Market",placeholder="Over/Under, handicap, win, place...",key="smarket")
        selection=c3.text_input("Selection / Player / Runner",key="ssel")

        event=st.text_input("Event / Race",key="sevent")
        book=st.text_input("Sportsbook",value="Sportsbet",key="sbook")

        c1,c2,c3=st.columns(3)
        line=c1.text_input("Line",key="sline")
        odds=c2.number_input("Odds taken (decimal)",min_value=1.01,value=1.91,step=0.01,key="sodds")
        known_close=c3.checkbox("Closing odds are known",value=False,key="sclose_known")
        close=c3.number_input("Closing odds",min_value=1.01,value=1.91,step=0.01,key="sclose") if known_close else None
        stake=st.number_input("Stake",min_value=0.0,value=20.0,step=5.0,key="sstake")
        if budget['active']:st.caption(f"This stake: {stake/budget['unit_value']:.2f}u · Remaining weekly allowance: {max(0,budget['remaining']):.2f}u")
        reasoning=st.text_area("Analysis & reasoning",placeholder="Why this bet? Include your research, stats, matchup, recent form and risks.",key="sreason",height=150)
        tags=tag_picker(sport,"single")
        source_note=st.text_input("Data source / note",value="Manual entry",key="ssource")

        if st.button("Save Single",use_container_width=True,key="save_single"):
            if sport=='Other' and (not custom_sport.strip() or not bt.strip()):
                st.error('Enter a custom sport name and bet type.');st.stop()
            cv=clv(odds,close)
            bet_id=attempt_budget_save("""INSERT INTO bets(placed_at,event_date,sport,league,event,book,bet_type,market,selection,line,odds,closing_odds,stake,result,pnl,reasoning,post_game_reason,clv,ai_review,process_grade,factors_json,source_note)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (datetime.now().isoformat(),str(event_date),sport,league,event,book,bt.strip(),market,selection,line,odds,close,stake,"Pending",0,reasoning,"",cv,"","",json.dumps({"wager_type":"single","tags":tags,"custom_sport":custom_sport.strip()}),source_note))
            if bet_id is None:st.stop()
            notify_saved("Bet saved")
    else:
        st.info("Choose the number of legs. Each leg's Bet type changes immediately when you change that leg's sport.")
        nlegs=st.number_input("Number of legs",min_value=2,max_value=12,value=3,step=1,key="nlegs")
        c1,c2,c3=st.columns(3)
        event_date=c1.date_input("Bet date / main event date",date.today(),key="mdate")
        book=c2.text_input("Sportsbook",value="Sportsbet",key="mbook")
        stake=c3.number_input("Stake",min_value=0.0,value=20.0,step=5.0,key="mstake")
        if budget['active']:st.caption(f"Total multi stake: {stake/budget['unit_value']:.2f}u · Remaining weekly allowance: {max(0,budget['remaining']):.2f}u")
        multi_name=st.text_input("Multi name",placeholder="e.g. Wednesday NBA 4-leg",key="mname")
        reasoning=st.text_area("Analysis & reasoning",placeholder="Why do these legs belong together? Include your research, correlations and risks.",key="mreason",height=150)
        tags=tag_picker("Multi","multi")

        legs=[]
        for i in range(int(nlegs)):
            st.markdown(f"#### Leg {i+1}")
            a,b,c,d=st.columns(4)
            lsport=a.selectbox("Sport",SPORTS,key=f"lsport{i}")
            lbet_type=b.text_input('Custom bet type',key=f'lcustom_type{i}') if lsport=='Other' else b.selectbox("Bet type",BET_TYPES.get(lsport,["Other"]),key=f"lbt{i}")
            lcustom=st.text_input(f'Leg {i+1} custom sport name',key=f'lcustom_sport{i}') if lsport=='Other' else ''
            levent=c.text_input("Event",key=f"levent{i}")
            lodds=d.number_input("Odds",min_value=1.01,value=1.50,step=0.01,key=f"lodds{i}")
            e,f,g,h=st.columns(4)
            lmarket=e.text_input("Market",placeholder="Over/Under, handicap, win, place...",key=f"lmarket{i}")
            lselection=f.text_input("Selection",key=f"lsel{i}")
            lline=g.text_input("Line",key=f"lline{i}")
            lnotes=h.text_input("Notes",key=f"lnotes{i}")
            legs.append((lsport,lbet_type,levent,lmarket,lselection,lline,lodds,lnotes))
            if lsport=='Other':legs[-1]=legs[-1]+(lcustom.strip(),)

        source_note=st.text_input("Data source / note",value="Manual entry",key="msource")
        combined=math.prod([x[6] for x in legs]) if legs else 1.0
        m1,m2,m3=st.columns(3)
        m1.metric("Combined odds",f"{combined:.2f}")
        m2.metric("Potential return",money(stake*combined))
        m3.metric("Potential profit",money(stake*(combined-1)))

        if st.button("Save Multi",use_container_width=True,key="save_multi"):
            if any(leg[0]=='Other' and (not leg[1].strip() or not leg[8]) for leg in legs):
                st.error('Enter a sport name and bet type for every Other leg.');st.stop()
            label=multi_name.strip() or f"{len(legs)}-Leg Multi"
            bet_id=attempt_budget_save("""INSERT INTO bets(placed_at,event_date,sport,league,event,book,bet_type,market,selection,line,odds,closing_odds,stake,result,pnl,reasoning,post_game_reason,clv,ai_review,process_grade,factors_json,source_note)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (datetime.now().isoformat(),str(event_date),"Multi","",label,book,"Multi / Parlay","Multi",label,f"{len(legs)} legs",combined,None,stake,"Pending",0,reasoning,"",None,"","",json.dumps({"wager_type":"multi","legs":len(legs),"tags":tags}),source_note))
            if bet_id is None:st.stop()
            for i,leg in enumerate(legs,1):
                execsql("INSERT INTO multi_legs(bet_id,leg_no,sport,bet_type,event,market,selection,line,odds,closing_odds,result,clv,notes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (bet_id,i,leg[0],leg[1],leg[2],leg[3],leg[4],leg[5],leg[6],None,"Pending",None,(f"Sport: {leg[8]}\n" if leg[0]=='Other' else '')+leg[7]))
            notify_saved("Multi saved")

# PRE-BET ANALYST
if page=="Analyse Bet":
    st.markdown("<div class='page-kicker'>Decision engine</div><div class='page-title'>Analyse Bet</div>",unsafe_allow_html=True)
    st.caption("A decision gate, not a pick generator. It can return BET, LEAN or NO BET and must not invent missing evidence.")
    with st.form("prebet"):
        st.caption("Rule Gate = market math using your probability estimate. Evidence Verdict = whether the thesis is supported by verified data. These can disagree, and that is intentional.")
        c1,c2,c3=st.columns(3)
        asport=c1.selectbox("Sport",SPORTS,key="asport")
        aselection=c2.text_input("Selection",placeholder="Player / team / runner")
        amarket=c3.text_input("Market + line",placeholder="Over 2.5 threes")
        aodds=c1.number_input("Available decimal odds",min_value=1.01,value=1.90,step=0.01)
        aprob=c2.number_input("Your estimated win probability % (optional)",min_value=0.0,max_value=100.0,value=0.0,step=0.5)
        confidence=c3.selectbox("Evidence quality",["Low / incomplete","Medium","High / well sourced"])
        evidence=st.text_area("Evidence / reasoning",placeholder="Paste the stats and information you actually have. Missing data is okay — the analyst should say NO BET when evidence is insufficient.")
        submitted=st.form_submit_button("Analyse Bet",use_container_width=True)
    if submitted:
        implied=100/aodds
        edge=(aprob-implied) if aprob>0 else None
        # deterministic safety gate before AI
        if not evidence.strip() or confidence=="Low / incomplete" or aprob<=0:
            gate="NO BET"; reason="Insufficient reliable evidence or no probability estimate."
        elif edge < 2:
            gate="NO BET"; reason=f"Estimated edge is only {edge:.1f} percentage points."
        elif edge < 5:
            gate="LEAN"; reason=f"Estimated edge is {edge:.1f} percentage points, but not strong enough for a full BET signal."
        else:
            gate="BET"; reason=f"Estimated edge is {edge:.1f} percentage points, subject to the evidence being accurate."
        execsql("""INSERT INTO analysis_log(created_at,sport,selection,market,odds,user_probability,implied_probability,edge,gate,evidence_quality,evidence,reason) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",(datetime.now().isoformat(),asport,aselection,amarket,float(aodds),float(aprob),float(implied),float(edge) if edge is not None else None,gate,confidence,evidence,reason))
        st.markdown(f"<div class='page-kicker'>Recommendation</div><div class='page-title'>{gate}</div><div class='page-copy'>{reason}</div>",unsafe_allow_html=True)
        x1,x2,x3=st.columns(3)
        x1.metric("Market implied probability",f"{implied:.1f}%")
        x2.metric("Your probability",f"{aprob:.1f}%" if aprob else "Not supplied")
        x3.metric("Estimated edge",f"{edge:.1f} pp" if edge is not None else "Unknown")
        data_ctx=latest_context(asport, aselection or amarket, 8)
        player_packet=None
        player_hit=None
        if asport in ("NFL","NBA","NHL","MLB","NCAAB","NCAAF","Soccer","Tennis") and aselection.strip():
            try:
                with st.spinner(f"Checking recent {asport} player data for {aselection}…"):
                    player_packet=build_player_history_packet(asport,aselection,lookback_days=45,max_games=10)
                    player_hit=derive_market_hit_rate(player_packet,amarket)
                    if player_packet.get("games"):
                        # Store the exact extracted packet so it can be reused and audited.
                        save_event_snapshot(asport,amarket or f"{asport} analysis",aselection,player_packet,f"Auto player history · {player_packet.get('source')}")
                        data_ctx=latest_context(asport,aselection,12)
            except Exception:
                player_packet=None
                player_hit=None

        form_summary={}
        conflicts=[]
        conf_score=0
        if player_packet and player_packet.get("games"):
            st.markdown("### Verified recent player data")
            st.caption(f"Source: {player_packet.get('source','Unknown')} · fetched during this analysis")
            packet_df=pd.DataFrame(player_packet["games"])
            st.dataframe(packet_df,use_container_width=True,hide_index=True)
            sm=player_packet.get("summary") or {}
            st.caption(f"Sample: {len(player_packet.get('games') or [])} recent game rows returned by the source.")
            m1,m2,m3=st.columns(3)
            m1.metric("Avg receiving yards",f"{sm.get('avg_receiving_yards',0):.1f}" if "avg_receiving_yards" in sm else "—")
            m2.metric("Avg targets",f"{sm.get('avg_targets',0):.1f}" if "avg_targets" in sm else "—")
            if player_hit:
                m3.metric(f"Hit rate vs {player_hit['line']}",f"{player_hit['hit_rate']:.1f}% ({player_hit['hits']}/{player_hit['sample']})")
            else:
                m3.metric("Market hit rate","—")

            form_summary=recent_form_summary(player_packet,amarket)
            if form_summary:
                st.markdown("### Recent form snapshot")
                f1,f2,f3,f4=st.columns(4)
                f1.metric("Average",f"{form_summary.get('avg',0):.1f}")
                f2.metric("Median",f"{form_summary.get('median',0):.1f}")
                f3.metric("Hit rate",f"{form_summary['hit_rate']:.1f}%" if form_summary.get("hit_rate") is not None else "—")
                grade,grade_note=sample_grade(form_summary.get("sample",0))
                f4.metric("Sample grade",grade)
                st.caption(grade_note)

                c1,c2=st.columns(2)
                with c1:
                    st.markdown("**Last 5**")
                    st.write(" · ".join(f"{x:.0f}" if float(x).is_integer() else f"{x:.1f}" for x in form_summary.get("last5",[])) or "—")
                    if form_summary.get("hit_rate_5") is not None:
                        st.caption(f"Last-5 hit rate: {form_summary['hit_rate_5']:.1f}%")
                with c2:
                    st.markdown("**Last 10**")
                    st.write(" · ".join(f"{x:.0f}" if float(x).is_integer() else f"{x:.1f}" for x in form_summary.get("last10",[])) or "—")
                    if form_summary.get("hit_rate_10") is not None:
                        st.caption(f"Last-10 hit rate: {form_summary['hit_rate_10']:.1f}%")

                if form_summary.get("trend_delta") is not None:
                    st.caption(f"Recent-vs-older average trend: {float(form_summary['trend_delta']):+.1f}")

                conflicts=detect_claim_conflicts(evidence,form_summary)
                st.markdown("### Claim verification")
                if conflicts:
                    for c in conflicts:
                        st.error(f"Conflict: {c}")
                else:
                    st.success("No obvious numeric conflicts detected between your reasoning and the verified recent sample.")

                conf_score,conf_reasons=evidence_confidence_score(player_packet,form_summary,data_ctx,conflicts)
                st.markdown("### Evidence confidence")
                st.progress(conf_score/100)
                st.caption(f"{conf_score}/100 · " + " · ".join(conf_reasons))
        elif asport in ("NFL","NBA","NHL","MLB","NCAAB","NCAAF","Soccer","Tennis") and aselection.strip():
            st.caption("No exact recent player stat rows were found automatically. StakeLab will not mark player claims as verified unless the source returns the exact player/stat fields.")
            if player_packet and player_packet.get("diagnostic"):
                st.warning(f"Player-data diagnostic: {player_packet.get('diagnostic')}")
        st.caption(f"Verification source: {source_status_for_sport(asport)}")
        if data_ctx:
            st.markdown("### Connected data context")
            st.caption("Recent structured snapshots stored by StakeLab. These are context only unless they contain the exact player/market information needed.")
            st.dataframe(pd.DataFrame(data_ctx)[["captured_at","event","subject","source"]],use_container_width=True,hide_index=True)

        found,missing,has_ctx=evidence_audit(asport,evidence,data_ctx)
        st.markdown("### Evidence check")
        a1,a2=st.columns(2)
        with a1:
            st.markdown("**Covered in your reasoning**")
            if found:
                for item in found[:6]:
                    st.markdown(f"✓ {item}")
            else:
                st.caption("No structured evidence categories detected.")
        with a2:
            st.markdown("**Still worth verifying**")
            if missing:
                for item in missing[:6]:
                    st.markdown(f"• {item}")
            else:
                st.caption("Your write-up covers the main evidence categories.")
        if not has_ctx:
            st.caption("StakeLab does not currently have exact connected player/market data for this selection, so it cannot independently verify those claims yet.")

# RESULTS AND PERSONAL NOTES
if page=="Results & Notes":
    st.markdown("<div class='page-kicker'>Settle your bets</div><div class='page-title'>Results & Notes</div>",unsafe_allow_html=True)
    df=q("SELECT * FROM bets ORDER BY event_date DESC,id DESC")
    if df.empty:
        st.info("Log a bet first.")
    else:
        chosen=st.selectbox("Bet",df.id.tolist(),format_func=lambda x: f"#{x} — {df[df.id==x].iloc[0].event} — {df[df.id==x].iloc[0].selection}")
        r=df[df.id==chosen].iloc[0]
        result=st.selectbox("Result",["Pending","Won","Lost","Push"],index=["Pending","Won","Lost","Push"].index(r.result),key=f"result_{chosen}")
        calculated=float(r.stake)*(float(r.odds)-1) if result=="Won" else -float(r.stake) if result=="Lost" else 0.0
        st.metric("Calculated profit / loss",money(calculated))
        override=st.checkbox("Use custom profit / loss (cash out, dead heat, each way)",key=f"override_{chosen}")
        pnl=st.number_input("Net profit / loss",value=float(r.pnl or 0),step=1.0,key=f"pnl_{chosen}") if override else calculated
        known=st.checkbox("Closing odds are known",value=pd.notna(r.closing_odds),key=f"known_{chosen}")
        closing=st.number_input("Closing odds",min_value=1.01,value=float(r.closing_odds) if pd.notna(r.closing_odds) else float(r.odds),step=0.01,key=f"close_{chosen}") if known else None
        post=st.text_area("Your post-game / race notes",value=r.post_game_reason or "",key=f"notes_{chosen}")
        if st.button("Save result and notes",use_container_width=True):
            cv=clv(r.odds,closing) if known else None
            execsql("UPDATE bets SET result=?,pnl=?,closing_odds=?,clv=?,post_game_reason=? WHERE id=?",(result,pnl,closing,cv,post,int(chosen)))
            notify_saved("Result and notes updated")

# DATABASE
if page=="Bet History":
    st.markdown("<div class='page-kicker'>History & audit trail</div><div class='page-title'>Bet History</div>",unsafe_allow_html=True)
    st.caption("Your complete betting history and recorded analysis.")
    df=sport_rows(q("SELECT * FROM bets ORDER BY event_date DESC,id DESC"))
    if not df.empty:
        df["Tags"]=df.factors_json.map(saved_bet_tags).map(lambda t:", ".join(t))
        df['Unit size at placement']=pd.to_numeric(df.factors_json.map(placement_unit),errors='coerce')
        df['Stake units']=pd.to_numeric(df.stake,errors='coerce').div(df['Unit size at placement'])
        df['Net units']=pd.to_numeric(df.pnl,errors='coerce').div(df['Unit size at placement']).where(df.result.isin(['Won','Lost','Push']))
        available=sorted({t for value in df.factors_json for t in saved_bet_tags(value)})
        chosen_tags=st.multiselect("Filter by tags",available,key="history_tags")
        if chosen_tags:df=df[df.factors_json.map(lambda value:bool(set(chosen_tags)&set(saved_bet_tags(value))))]
        st.dataframe(df.drop(columns=["ai_review","process_grade"],errors="ignore"),use_container_width=True,hide_index=True)
        csv=df.drop(columns=["ai_review","process_grade"],errors="ignore").to_csv(index=False).encode()
        st.download_button("Download bets CSV",csv,"bets_export.csv","text/csv")
    od=q("SELECT * FROM odds_snapshots ORDER BY captured_at DESC")
    if not od.empty:
        st.subheader("Odds snapshots")
        st.dataframe(od,use_container_width=True,hide_index=True)

# DATA SOURCES
    st.markdown("---")
    st.markdown("### Remove past bets")
    st.caption("Delete an individual bet from StakeLab. For multis, linked leg records are removed too.")

    delete_df = q("SELECT id,event_date,sport,event,bet_type,selection,odds,stake,result,pnl FROM bets ORDER BY event_date DESC,id DESC")
    if delete_df.empty:
        st.info("There are no bets to remove.")
    else:
        def _bet_label(row):
            event = str(row["event"] or "").strip()
            selection = str(row["selection"] or "").strip()
            parts = [
                f"#{int(row['id'])}",
                str(row["event_date"]),
                str(row["sport"]),
                str(row["bet_type"]),
                selection or event or "Unnamed bet",
                f"@ {float(row['odds']):.2f}" if pd.notna(row["odds"]) else "",
                f"{money(float(row['stake']))}" if pd.notna(row["stake"]) else "",
                str(row["result"]),
            ]
            return " · ".join([x for x in parts if x])

        delete_options = {
            _bet_label(row): int(row["id"])
            for _, row in delete_df.iterrows()
        }
        selected_label = st.selectbox(
            "Choose a bet to remove",
            list(delete_options.keys()),
            key="delete_bet_select"
        )
        selected_id = delete_options[selected_label]
        selected_row = delete_df.loc[delete_df["id"] == selected_id].iloc[0]

        st.warning(
            f"You are about to permanently remove bet #{selected_id}: "
            f"{selected_row['sport']} · {selected_row['selection'] or selected_row['event']} · "
            f"{selected_row['result']}."
        )
        confirm_delete = st.checkbox(
            "I understand this will permanently delete this bet from the current database.",
            key="confirm_delete_bet"
        )

        if st.button(
            "🗑️ Delete selected bet",
            type="primary",
            disabled=not confirm_delete,
            use_container_width=True,
            key="delete_selected_bet"
        ):
            execsql("DELETE FROM multi_legs WHERE bet_id=?", (selected_id,))
            execsql("DELETE FROM reviews WHERE bet_id=?", (selected_id,))
            execsql("DELETE FROM bets WHERE id=?", (selected_id,))
            st.success(f"Bet #{selected_id} was removed.")
            st.rerun()

if page=="Data Hub":
    st.markdown("<div class='page-kicker'>Odds, stats & verification</div><div class='page-title'>Data Hub</div>",unsafe_allow_html=True)
    st.write("StakeLab can now store verification data for every supported sport. A claim is only marked verified when the exact supporting information exists in stored structured data.")

    st.markdown("### Coverage")
    coverage=pd.DataFrame([{"Sport":s,"Verification path":source_status_for_sport(s)} for s in SPORTS])
    st.dataframe(coverage,use_container_width=True,hide_index=True)

    st.markdown("### 1) US sports + soccer + tennis")
    c1,c2,c3=st.columns(3)
    sync_sport=c1.selectbox("Sport to sync",["NBA","NFL","NHL","MLB","NCAAB","NCAAF","Soccer","Tennis"],key="sync_sport")
    lookback=c2.number_input("Lookback days",min_value=1,max_value=45,value=7,step=1,key="sync_days")
    include_summary=c3.checkbox("Fetch event/player detail",value=True,key="sync_summary")

    league_code=None
    if sync_sport=="Soccer":
        label=st.selectbox("Soccer competition",list(SOCCER_LEAGUES.keys()),key="soccer_comp")
        league_code=SOCCER_LEAGUES[label]
    elif sync_sport=="Tennis":
        label=st.selectbox("Tennis circuit",list(TENNIS_CIRCUITS.keys()),key="tennis_circuit")
        league_code=TENNIS_CIRCUITS[label]

    if st.button("Sync selected sport",use_container_width=True,key="sync_selected"):
        with st.spinner(f"Fetching {sync_sport} structured data…"):
            try:
                saved,events=sync_espn_sport(sync_sport,lookback,league_code,include_summary,max_events=60)
                st.success(f"Stored {saved} {sync_sport} event bundle(s). Exact player fields are only verified when the source returned them.")
            except Exception as ex:
                st.error(f"{sync_sport} sync failed: {ex}")

    st.caption("ESPN site endpoints are a free public starting source, not a guaranteed contracted API. StakeLab records the source explicitly and does not invent fields that are absent.")

    st.markdown("### 2) AFL")
    a1,a2=st.columns(2)
    afl_year=a1.number_input("AFL season",min_value=2000,max_value=2100,value=date.today().year,step=1,key="afl_year_full")
    if a2.button("Sync Squiggle AFL fixtures/results",use_container_width=True,key="sync_afl"):
        try:
            games=fetch_squiggle_games(afl_year)
            for g in games[:250]:
                event=f"{g.get('hteam','')} v {g.get('ateam','')}"
                save_event_snapshot("AFL",event,"fixture/result",g,"Squiggle API")
            st.success(f"Stored {min(len(games),250)} AFL fixture/result snapshots.")
        except Exception as ex:
            st.error(f"AFL sync failed: {ex}")

    st.caption("For AFL player props such as disposals, marks, tackles, TOG or CBA, configure AFL_PLAYER_API_URL in Streamlit Secrets or import a structured CSV below.")
    if st.button("Fetch configured AFL player feed",use_container_width=True,key="afl_player_feed"):
        try:
            payload=fetch_configured_json("AFL_PLAYER_API_URL","AFL_PLAYER_API_KEY")
            if payload is None:
                st.info("No AFL_PLAYER_API_URL is configured.")
            else:
                n=save_generic_feed("AFL",payload,"Configured AFL player feed")
                st.success(f"Stored {n} AFL player-data row(s).")
        except Exception as ex:
            st.error(f"AFL player feed failed: {ex}")

    st.markdown("### 3) Australian horses + greyhounds")
    r1,r2=st.columns(2)
    with r1:
        st.markdown("#### 🐎 Horses")
        if st.button("Fetch configured horse feed",use_container_width=True,key="horse_feed"):
            try:
                payload=fetch_configured_json("HORSE_DATA_API_URL","HORSE_DATA_API_KEY")
                if payload is None:
                    st.info("No HORSE_DATA_API_URL is configured yet.")
                else:
                    n=save_generic_feed("Horses",payload,"Configured horse racing feed")
                    st.success(f"Stored {n} horse-racing row(s).")
            except Exception as ex:
                st.error(f"Horse feed failed: {ex}")
        horse_csv=st.file_uploader("Import horse data CSV",type=["csv"],key="horse_csv")
        if horse_csv is not None and st.button("Store horse CSV",key="store_horse_csv"):
            try:
                n=import_structured_csv("Horses",horse_csv)
                st.success(f"Stored {n} horse rows.")
            except Exception as ex:
                st.error(f"Horse import failed: {ex}")
    with r2:
        st.markdown("#### 🐕 Greyhounds")
        if st.button("Fetch configured greyhound feed",use_container_width=True,key="grey_feed"):
            try:
                payload=fetch_configured_json("GREYHOUND_DATA_API_URL","GREYHOUND_DATA_API_KEY")
                if payload is None:
                    st.info("No GREYHOUND_DATA_API_URL is configured yet.")
                else:
                    n=save_generic_feed("Greyhounds",payload,"Configured greyhound racing feed")
                    st.success(f"Stored {n} greyhound row(s).")
            except Exception as ex:
                st.error(f"Greyhound feed failed: {ex}")
        grey_csv=st.file_uploader("Import greyhound data CSV",type=["csv"],key="grey_csv")
        if grey_csv is not None and st.button("Store greyhound CSV",key="store_grey_csv"):
            try:
                n=import_structured_csv("Greyhounds",grey_csv)
                st.success(f"Stored {n} greyhound rows.")
            except Exception as ex:
                st.error(f"Greyhound import failed: {ex}")

    st.markdown("### 4) Odds / bookmaker layer")
    st.info("Sportsbet prices are only treated as verified when they come from an authorized feed you configure. StakeLab will not label scraped or unverified bookmaker prices as Sportsbet data.")
    if st.button("Fetch configured odds feed",use_container_width=True,key="odds_feed"):
        try:
            payload=fetch_configured_json("ODDS_API_URL","ODDS_API_KEY")
            if payload is None:
                st.info("No ODDS_API_URL is configured.")
            else:
                n=save_generic_feed("Odds",payload,"Configured authorized odds feed")
                st.success(f"Stored {n} odds-feed row(s).")
        except Exception as ex:
            st.error(f"Odds feed failed: {ex}")

    st.markdown("### Streamlit Secrets")
    st.code("""# Optional player/racing/bookmaker feeds
AFL_PLAYER_API_URL = "https://provider.example/..."
AFL_PLAYER_API_KEY = "..."

HORSE_DATA_API_URL = "https://provider.example/..."
HORSE_DATA_API_KEY = "..."

GREYHOUND_DATA_API_URL = "https://provider.example/..."
GREYHOUND_DATA_API_KEY = "..."

ODDS_API_URL = "https://authorized-provider.example/..."
ODDS_API_KEY = "..."

""",language="toml")
    st.caption("Do not copy the example URLs literally. Replace them only with real provider endpoints you are authorized to use.")

    stored=q("SELECT captured_at,sport,event,subject,source FROM event_data ORDER BY captured_at DESC LIMIT 100")
    if not stored.empty:
        st.markdown("### Latest stored verification data")
        st.dataframe(stored,use_container_width=True,hide_index=True,height=420)

if page=="Settings":
    st.markdown("<div class='page-kicker'>Preferences & system status</div><div class='page-title'>Settings</div><div class='page-copy'>Check your tracker and connected data sources.</div>",unsafe_allow_html=True)
    st.markdown("### Backup & restore")
    st.caption("A full backup includes bets, multi legs, reasoning, tags, results, bankroll settings and the weekly allowance ledger. Keep a downloaded copy somewhere safe.")
    st.download_button("Download full backup", database_backup(), file_name=f"StakeLab-backup-{date.today().isoformat()}.db", mime="application/octet-stream", key="full_backup")
    uploaded_backup = st.file_uploader("Choose a StakeLab backup", type=["db"], key="restore_upload")
    if uploaded_backup is not None:
        payload = uploaded_backup.getvalue()
        try:
            backup_count = validate_backup(payload)
            st.info(f"Valid backup: {backup_count} bets. Restore replaces your current tracker data, including weekly spending.")
            confirmed = st.checkbox("Replace my current tracker with this backup", key="restore_confirm_"+hashlib.sha256(payload).hexdigest())
            if st.button("Restore backup", disabled=not confirmed, key="restore_backup"):
                restore_backup(payload)
                for state_key in list(st.session_state):
                    if state_key not in {"main_nav", "top_sport"}:
                        del st.session_state[state_key]
                st.session_state["restore_completed"] = True
                st.rerun()
        except ValueError as exc:
            st.error(str(exc))
    if st.session_state.pop("restore_completed", False):
        st.success("Backup restored. A recovery copy of the previous database was kept on this host.")
    st.markdown("### Durable storage")
    if storage_path:
        st.info("A storage directory is configured. It is durable only if your host mounts persistent storage at that directory.")
    else:
        st.warning("Local storage is active. Download backups regularly; this host may lose local files on restart or redeploy.")
    with st.expander("Configure persistent storage"):
        st.write("On a host with a persistent disk, point this setting at its mounted directory. Setting a path alone does not make Streamlit Community Cloud storage permanent.")
        st.code('STAKELAB_DATA_DIR = "/your/persistent/mount/stakelab"', language="toml")
        st.caption("Download your backup before changing hosts or storage paths, then restore it into the new installation.")
    c1,c2=st.columns(2,gap="large")
    with c1:
        st.markdown("### Bet tracker")
        st.success("Manual results and notes. No AI feedback or AI API key required.")
        st.markdown("### Decision engine")
        st.caption("BET / LEAN / NO BET currently uses a transparent rule-based gate based on your probability estimate, market implied probability and evidence quality.")
    with c2:
        st.markdown("### Automatic player verification")
        st.caption("For supported sports, Analyse Bet now attempts to fetch recent player-level stats automatically from ESPN public event summaries and only verifies fields explicitly returned by the source.")
        st.markdown("### Data status")
        dc=q("SELECT sport,source,MAX(captured_at) AS latest,COUNT(*) AS rows FROM event_data GROUP BY sport,source ORDER BY latest DESC")
        st.dataframe(dc,use_container_width=True,hide_index=True) if not dc.empty else st.info("No structured sports data stored yet.")
        st.markdown("### Database")
        st.caption(f"Local database: {DB}")
        st.caption("Storage and backup controls are above.")

# SLEEK PREMIUM THEME
st.markdown("""
<style>
:root{--bg:#111214;--panel:#1a1c20;--line:#30343b;--text:#eceef2;--muted:#a3a9b4;--teal:#83d4ff;--green:#83d4ff;--red:#dca0ab;--blue:#94bddc;}
[data-testid="stAppViewContainer"]{background:#111214!important;color:#eceef2}
[data-testid="stHeader"]{background:rgba(17,18,20,.96)!important;border-bottom:1px solid #30343b;backdrop-filter:blur(10px)}
h1,h2,h3{font-weight:500!important;letter-spacing:-.025em;color:#eceef2!important}
p,li{color:#bac6d5}
[data-testid="stMetric"]{background:#1a1c20!important;border:1px solid #30343b!important;border-radius:9px!important;box-shadow:none!important;padding:18px!important}
[data-testid="stMetricValue"]{font-weight:500!important;font-variant-numeric:tabular-nums}
[data-testid="stMetricLabel"]{color:#a3a9b4!important}
[data-testid="stForm"]{background:#1a1c20!important;border:1px solid #30343b!important;border-radius:9px!important;box-shadow:none!important}
.stButton>button,.stDownloadButton>button,[data-testid="stFormSubmitButton"]>button{background:#1a1c20!important;border:1px solid #3c424b!important;border-radius:7px!important;color:#eceef2!important;font-weight:500!important;box-shadow:none!important;transition:background .15s ease,border-color .15s ease!important;transform:none!important}
.stButton>button:hover,.stDownloadButton>button:hover{background:#172230!important;border-color:#526379!important;transform:none!important}
[data-testid="stFormSubmitButton"]>button{background:#173346!important;border-color:#329fda!important;color:#b6e7ff!important}
[data-baseweb="input"]>div,[data-baseweb="select"]>div,[data-testid="stTextArea"] textarea,[data-testid="stNumberInput"] input{background:#15171a!important;border-color:#3c424b!important;border-radius:6px!important}
[data-testid="stDataFrame"]{border:1px solid #30343b!important;border-radius:8px!important;background:#1a1c20!important}
.st-key-top_navigation [role="radiogroup"] label{border-radius:0!important;background:transparent!important;border-bottom:2px solid transparent!important;box-shadow:none!important}
.st-key-top_navigation [role="radiogroup"] label:has(input:checked){background:transparent!important;border-bottom-color:#42bdff!important}
.st-key-top_navigation label p{font-weight:500!important;color:#a3a9b4!important}
.st-key-top_navigation label:has(input:checked) p{color:#d3eeff!important}
.st-key-top_navigation{border-bottom-color:#30343b!important}
.st-key-sport_navigation [role="radiogroup"] label,.st-key-entry_sport_buttons [role="radiogroup"] label{border-radius:7px!important;background:#1a1c20!important;border-color:#30343b!important;box-shadow:none!important;transform:none!important}
.st-key-sport_navigation [role="radiogroup"] label:has(input:checked),.st-key-entry_sport_buttons [role="radiogroup"] label:has(input:checked){background:#142f43!important;border-color:#32b5ff!important;box-shadow:none!important}
.st-key-sport_navigation label p,.st-key-entry_sport_buttons label p{font-weight:500!important;color:#a8b5c7!important}
.st-key-sport_navigation label:has(input:checked) p,.st-key-entry_sport_buttons label:has(input:checked) p{color:#b6e7ff!important}
.st-key-wager_buttons [role="radiogroup"]{background:#15171a!important;border-color:#30343b!important;border-radius:9px!important}
.st-key-wager_buttons [role="radiogroup"] label{border-radius:6px!important;box-shadow:none!important;transform:none!important}
.st-key-wager_buttons label:has(input:checked){background:#173346!important;border-color:#329fda!important;box-shadow:none!important}
.st-key-wager_buttons label p{font-weight:500!important}
.page-title{font-weight:500!important}.page-copy{color:#a3a9b4!important}
.kpi-card,.kpi-card:nth-child(n),.panel,.alert-card,.quick-card,.signal{background:#1a1c20!important;border:1px solid #30343b!important;border-radius:9px!important;box-shadow:none!important;transform:none!important}
.kpi-card:hover,[data-testid="stMetric"]:hover,.alert-card:hover,.signal:hover{border-color:#364555!important;box-shadow:none!important;transform:none!important}
.kpi-value,.panel-title,.score-value,.quick-card b{font-weight:500!important}
.page-kicker,.sl-brand b{color:#42bdff!important;font-weight:500!important}
.sl-brand img{border-radius:8px!important;box-shadow:none!important}
.green,.kpi-delta,.score-note,[data-testid="stMetricDelta"]{color:#83d4ff!important}
@media(hover:hover){.st-key-sport_navigation label:hover,.st-key-entry_sport_buttons label:hover{background:#172230!important;border-color:#425268!important;transform:none!important}}
@media(prefers-reduced-motion:reduce){.stButton>button,.stDownloadButton>button{transition:none!important}}
</style>
""",unsafe_allow_html=True)

st.markdown("""<style>
.sl-brand b{color:#42bdff!important;text-shadow:0 0 12px #32b5ff55}
.sl-brand img{filter:drop-shadow(0 0 7px #32b5ff35);display:block!important}
.tracker-brand.sl-brand{display:flex!important;align-items:center;gap:13px}
.st-key-top_navigation [role="radiogroup"] label:has(input:checked){border-bottom-color:#32b5ff!important;box-shadow:0 5px 8px -7px #32b5ff!important}
.st-key-sport_navigation [role="radiogroup"] label:has(input:checked),.st-key-entry_sport_buttons [role="radiogroup"] label:has(input:checked),.st-key-wager_buttons label:has(input:checked){background:#142f43!important;border-color:#32b5ff!important;box-shadow:0 0 12px #32b5ff18,inset 0 0 9px #32b5ff08!important}
.st-key-sport_navigation label:has(input:checked) p,.st-key-entry_sport_buttons label:has(input:checked) p,.st-key-wager_buttons label:has(input:checked) p{color:#b6e7ff!important}
.kpi-card:first-child{border-top-color:#32b5ff!important;box-shadow:0 -5px 20px -13px #32b5ff45!important}
.badge-bet{background:#173346!important;color:#b3e5ff!important}.badge-lean{background:#393124!important;color:#e7c997!important}.badge-nobet{background:#2c3036!important;color:#b7bec9!important}
.red,.negative{color:#e3a1a7!important}.green,.positive{color:#83d4ff!important}
[data-testid="stSidebar"]{background:#15171a!important;border-color:#30343b!important}
.st-key-sport_navigation label:has(input:focus-visible),.st-key-entry_sport_buttons label:has(input:focus-visible),.st-key-wager_buttons label:has(input:focus-visible){outline-color:#32b5ff!important}
input,textarea{caret-color:#32b5ff}::selection{background:#245b7a!important;color:#eceef2!important}
</style>""",unsafe_allow_html=True)

# MONTHLY REPORTS — EVENT-MONTH ACCOUNTING

def report_unit_value(row):
    try:
        factors=json.loads(row.get("factors_json") or "{}")
        value=float(factors.get("unit_value",0))
        return value if math.isfinite(value) and value>0 else None
    except (TypeError,ValueError,AttributeError):return None

def monthly_report_data(bets,month,sport="All",metadata=None):
    frame=bets.copy()
    if frame.empty:return dict(bets=frame,settled=frame,profit=0.,stake=0.,roi=None,win_rate=None,clv=None,clv_count=0,units=None,unit_count=0,pending_count=0,pending_stake=0.)
    dates=pd.to_datetime(frame.event_date,errors="coerce",utc=True)
    frame=frame[dates.dt.strftime("%Y-%m").eq(month)].copy()
    if sport!="All":frame=frame[frame.sport.eq(sport)].copy()
    frame["unit_at_placement"]=frame.apply(report_unit_value,axis=1) if not frame.empty else pd.Series(dtype=float)
    if metadata is not None and not metadata.empty and not frame.empty:
        mapping=metadata.set_index("bet_id").unit_value
        frame["unit_at_placement"]=pd.to_numeric(frame["unit_at_placement"],errors="coerce").fillna(frame.id.map(mapping))
    settled=frame[frame.result.isin(["Won","Lost","Push"])].copy()
    for column in ["stake","pnl","clv","unit_at_placement"]:
        settled[column]=pd.to_numeric(settled[column],errors="coerce")
    profit=float(settled.pnl.sum());stake=float(settled.stake.sum())
    decisive=settled[settled.result.isin(["Won","Lost"])]
    priced=settled[settled.clv.notna()]
    known_units=settled[settled.unit_at_placement.notna() & settled.unit_at_placement.gt(0)]
    settled["Net units"]=settled.pnl/settled.unit_at_placement.where(settled.unit_at_placement.gt(0))
    pending=frame[frame.result.eq("Pending")]
    return dict(bets=frame,settled=settled,profit=profit,stake=stake,roi=profit/stake*100 if stake else None,win_rate=float(decisive.result.eq("Won").mean()*100) if len(decisive) else None,clv=float(priced.clv.mean()) if len(priced) else None,clv_count=len(priced),units=float(known_units.pnl.div(known_units.unit_at_placement).sum()) if len(known_units) else None,unit_count=len(known_units),pending_count=len(pending),pending_stake=float(pd.to_numeric(pending.stake,errors="coerce").sum()))

def monthly_breakdown(settled,dimension):
    if settled.empty:return pd.DataFrame()
    d=settled.copy();d[dimension]=d[dimension].fillna("Unspecified").replace("","Unspecified")
    grouped=d.groupby(dimension,dropna=False).agg(Bets=("id","count"),Stake=("stake","sum"),Profit=("pnl","sum"),CLV=("clv","mean"),CLV_samples=("clv","count"))
    grouped["ROI (%)"]=grouped.Profit.div(grouped.Stake.where(grouped.Stake.gt(0)))*100
    return grouped.reset_index().sort_values("Profit",ascending=False)

if page=="Monthly Reports":
    st.markdown("<div class='page-kicker'>Your month in review</div><div class='page-title'>Monthly Reports</div><div class='page-copy'>Profit, ROI, price CLV and market performance from your saved bets.</div>",unsafe_allow_html=True)
    all_bets=q("SELECT * FROM bets ORDER BY event_date,id")
    current_month=date.today().strftime("%Y-%m")
    options={current_month}
    if not all_bets.empty:
        options.update(pd.to_datetime(all_bets.event_date,errors="coerce",utc=True).dropna().dt.strftime("%Y-%m").tolist())
    months=sorted(options,reverse=True)
    selected_month=st.selectbox("Report month",months,format_func=lambda x:datetime.strptime(x,"%Y-%m").strftime("%B %Y"),key="report_month")
    st.caption(f"Sport: {selected_sport}. Reports group bets by event date, not settlement date. Open bets are excluded from profit and ROI. Multis count once as complete wagers.")
    metadata=None
    db=conn()
    try:
        exists=db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='journal_metadata'").fetchone()
        if exists:metadata=pd.read_sql_query("SELECT bet_id,unit_value FROM journal_metadata WHERE mode='Real bets'",db)
    finally:db.close()
    report=monthly_report_data(all_bets,selected_month,selected_sport,metadata)
    if not report['bets'].empty:report['bets']["Tags"]=report['bets'].factors_json.map(saved_bet_tags).map(lambda t:", ".join(t))
    previous=(pd.Period(selected_month,freq="M")-1).strftime("%Y-%m")
    prior=monthly_report_data(all_bets,previous,selected_sport,metadata)
    a,b,c,d=st.columns(4)
    a.metric("Net profit",money(report['profit']),money(report['profit']-prior['profit'])+" vs prior month" if not prior['settled'].empty else None)
    b.metric("ROI",f"{report['roi']:+.2f}%" if report['roi'] is not None else "—")
    c.metric("Avg price CLV",f"{report['clv']:+.2f} pp" if report['clv'] is not None else "—")
    d.metric("Net units",f"{report['units']:+.2f}u" if report['units'] is not None else "—")
    st.caption(f"Units cover {report['unit_count']} of {len(report['settled'])} settled bets with a recorded unit value at placement. CLV covers {report['clv_count']} settled bets. Unknown values are not filled with zero.")
    a,b,c,d=st.columns(4)
    a.metric("Settled bets",len(report['settled']))
    b.metric("Win rate",f"{report['win_rate']:.1f}%" if report['win_rate'] is not None else "—",help="Wins divided by wins plus losses; pushes excluded.")
    c.metric("Settled stake",money(report['stake']))
    d.metric("Open bets",report['pending_count'],f"{money(report['pending_stake'])} at stake",delta_color="off")
    settled=report['settled']
    if report['bets'].empty:st.info("No bets recorded for this month and sport.")
    elif settled.empty:st.info("This month has open bets, but no settled results yet.")
    else:
        st.markdown("### Monthly profit curve")
        daily=settled.groupby("event_date",as_index=False).pnl.sum().sort_values("event_date")
        daily["Cumulative P&L"]=daily.pnl.cumsum()
        profit_chart(daily[["event_date","Cumulative P&L"]],"event_date","Cumulative P&L")
        for title,dimension in [("By sport","sport"),("By bet type","bet_type"),("By bookmaker","book")]:
            st.markdown("### "+title)
            breakdown=monthly_breakdown(settled,dimension)
            st.dataframe(breakdown.round(2),hide_index=True,use_container_width=True)
        sport_types=settled.assign(bet_type=settled.bet_type.fillna("Unspecified"),sport=settled.sport.fillna("Unspecified"))
        st.markdown("### Markets within each sport")
        combined=sport_types.groupby(["sport","bet_type"]).agg(Bets=("id","count"),Stake=("stake","sum"),Profit=("pnl","sum"),CLV=("clv","mean")).reset_index()
        combined["ROI (%)"]=combined.Profit.div(combined.Stake.where(combined.Stake.gt(0)))*100
        st.dataframe(combined.round(2),hide_index=True,use_container_width=True)
        st.caption("Largest profits show what happened in this sample; they do not establish a predictive edge.")
    st.markdown("### Export report")
    label=datetime.strptime(selected_month,"%Y-%m").strftime("%B %Y")
    vals={"Month":selected_month,"Sport":selected_sport,"Settled bets":len(settled),"Profit":report['profit'],"Settled stake":report['stake'],"ROI (%)":report['roi'],"Win rate (%)":report['win_rate'],"Avg CLV (pp)":report['clv'],"CLV samples":report['clv_count'],"Net units":report['units'],"Unit samples":report['unit_count'],"Open bets":report['pending_count'],"Open stake":report['pending_stake']}
    st.download_button("Download summary CSV",pd.DataFrame([vals]).to_csv(index=False),file_name=f"stakelab_{selected_month}_summary.csv",mime="text/csv")
    if not report['bets'].empty:
        export=report['bets'].drop(columns=["ai_review","process_grade"],errors="ignore")
        st.download_button("Download this month's bets",export.to_csv(index=False),file_name=f"stakelab_{selected_month}_bets.csv",mime="text/csv")
    summary_table=pd.DataFrame([vals]).T.reset_index();summary_table.columns=["Metric","Value"]
    sections=[summary_table.to_html(index=False,escape=True)]
    for title,dimension in [("By sport","sport"),("By bet type","bet_type"),("By bookmaker","book")]:
        breakdown=monthly_breakdown(settled,dimension)
        if not breakdown.empty:sections.append("<h2>"+html.escape(title)+"</h2>"+breakdown.round(2).to_html(index=False,escape=True))
    printable="<!doctype html><html><head><meta charset='utf-8'><title>StakeLab Monthly Report</title><style>body{font:14px system-ui;color:#18263b;max-width:1000px;margin:40px auto;padding:20px}table{border-collapse:collapse;width:100%;margin:16px 0}td,th{border-bottom:1px solid #ddd;padding:8px;text-align:left}h1{color:#17699c}@media print{body{margin:0}}</style></head><body><h1>StakeLab — "+html.escape(label)+"</h1><p>Sport: "+html.escape(selected_sport)+". Event-month accounting. Open bets excluded from profit. Unit and CLV coverage shown below.</p>"+"".join(sections)+"</body></html>"
    st.download_button("Download printable report",printable,file_name=f"stakelab_{selected_month}_report.html",mime="text/html")
    st.caption("Open the printable report in your browser and choose Print / Save as PDF.")

# BET CALENDAR — SAVED EVENT DATES
def calendar_day_data(bets,year,month,sport="All"):
    frame=bets.copy()
    if frame.empty:return frame,{}
    frame["calendar_date"]=pd.to_datetime(frame.event_date,errors="coerce",utc=True).dt.date
    frame=frame[frame.calendar_date.map(lambda d:pd.notna(d) and d.year==year and d.month==month)].copy()
    if sport!="All":frame=frame[frame.sport.eq(sport)].copy()
    days={}
    for day,rows in frame.groupby("calendar_date"):
        settled=rows[rows.result.isin(["Won","Lost","Push"])]
        days[day.day]={"profit":float(pd.to_numeric(settled.pnl,errors="coerce").sum()),"settled":len(settled),"open":int(rows.result.eq("Pending").sum()),"bets":len(rows)}
    return frame,days

if page=="Bet Calendar":
    import calendar
    st.markdown("<div class='page-kicker'>Your bets by day</div><div class='page-title'>Bet Calendar</div><div class='page-copy'>Select a date to see its bets, results and open stakes.</div>",unsafe_allow_html=True)
    today=date.today()
    st.session_state.setdefault("cal_year",today.year)
    st.session_state.setdefault("cal_month",today.month)
    def move_calendar(delta):
        current=pd.Period(f"{st.session_state.cal_year}-{st.session_state.cal_month:02d}",freq="M")+delta
        if 1900<=current.year<=2100:
            st.session_state.cal_year=current.year;st.session_state.cal_month=current.month
            st.session_state.cal_day=1
    def choose_calendar_day(day):st.session_state.cal_day=day
    controls=st.columns([1,2,2,1])
    controls[0].button("←",key="cal_previous",help="Previous month",on_click=move_calendar,args=(-1,),use_container_width=True)
    year=controls[1].selectbox("Year",range(1900,2101),key="cal_year")
    month=controls[2].selectbox("Month",range(1,13),format_func=lambda m:calendar.month_name[m],key="cal_month")
    controls[3].button("→",key="cal_next",help="Next month",on_click=move_calendar,args=(1,),use_container_width=True)
    all_bets=q("SELECT * FROM bets ORDER BY event_date,id")
    frame,days=calendar_day_data(all_bets,year,month,selected_sport)
    month_days=calendar.monthrange(year,month)[1]
    st.session_state.setdefault("cal_day",today.day if (year,month)==(today.year,today.month) else 1)
    if st.session_state.cal_day>month_days:st.session_state.cal_day=1
    st.caption(f"{calendar.month_name[month]} {year} · {selected_sport} · Event dates, not settlement dates. Multis count once as complete wagers.")
    st.markdown("""<style>
.st-key-bet_calendar_grid [data-testid="stHorizontalBlock"]{flex-wrap:nowrap!important;gap:5px!important}
.st-key-bet_calendar_grid [data-testid="stColumn"]{min-width:0!important;flex:1 1 0!important}
.st-key-bet_calendar_grid button{min-height:85px!important;padding:5px 2px!important;background:#1a1c20!important;border-color:#30343b!important;border-radius:7px!important;width:100%;white-space:pre-line!important}
.st-key-bet_calendar_grid button p{font-size:12px!important;white-space:pre-line!important;text-align:center!important}
.st-key-bet_calendar_grid .cal-weekday{text-align:center;color:#a3a9b4;font-size:12px;padding:7px 0}
@media(max-width:500px){.st-key-bet_calendar_grid button{min-height:78px!important}.st-key-bet_calendar_grid button p{font-size:11px!important}.st-key-bet_calendar_grid [data-testid="stHorizontalBlock"]{gap:3px!important}}
</style>""",unsafe_allow_html=True)
    styles=[]
    with st.container(key="bet_calendar_grid"):
        for col,name in zip(st.columns(7),["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]):col.markdown(f"<div class='cal-weekday'>{name}</div>",unsafe_allow_html=True)
        for week in calendar.Calendar(firstweekday=0).monthdayscalendar(year,month):
            for col,day in zip(st.columns(7),week):
                if not day:col.markdown("&nbsp;",unsafe_allow_html=True);continue
                item=days.get(day)
                label=str(day)
                if item:
                    if item['settled']:label+="\n"+money(item['profit'])
                    if item['open']:label+=f"\n{item['open']} open"
                key=f"cal_date_{day}"
                col.button(label,key=key,on_click=choose_calendar_day,args=(day,),help=f"{calendar.month_name[month]} {day}: {item['bets'] if item else 0} bets",use_container_width=True)
                if item:
                    bg="#142c3e" if item['profit']>0 else "#302027" if item['profit']<0 else "#222a35"
                    styles.append(f".st-key-{key} button{{background:{bg}!important}}")
                if day==st.session_state.cal_day:styles.append(f".st-key-{key} button{{border-color:#32b5ff!important;box-shadow:0 0 10px #32b5ff20!important}}")
    st.markdown("<style>"+"".join(styles)+"</style>",unsafe_allow_html=True)
    st.caption("Blue: net profit · Rose: net loss · Neutral: break-even or open only. Open bets are excluded from daily profit.")
    chosen=date(year,month,st.session_state.cal_day)
    st.markdown("### "+chosen.strftime("%A, %d %B"))
    daily=frame[frame.calendar_date.eq(chosen)] if not frame.empty else frame
    if daily.empty:st.info("No bets recorded for this date and sport.")
    else:
        item=days[chosen.day]
        a,b,c=st.columns(3)
        a.metric("Day profit",money(item['profit']))
        b.metric("Bets",item['bets'])
        pending=daily[daily.result.eq("Pending")]
        c.metric("Open stake",money(float(pd.to_numeric(pending.stake,errors="coerce").sum())))
        display=daily[["id","sport","event","selection","bet_type","market","odds","stake","result","pnl"]].copy()
        display.loc[~display.result.isin(["Won","Lost","Push"]),"pnl"]=None
        st.dataframe(display,hide_index=True,use_container_width=True)
        for _,bet in daily.iterrows():
            with st.expander(f"#{bet.id} · {bet.selection or bet.event or 'Bet'} · {bet.result}"):
                st.write("Reasoning: "+str(bet.reasoning or "Not recorded"))
                st.write("Tags: "+(", ".join(saved_bet_tags(bet.factors_json)) or "None"))
                st.write("Result notes: "+str(bet.post_game_reason or "Not recorded"))
                if bet.sport=="Multi":
                    legs=q("SELECT sport,event,selection,market,odds,result,notes FROM multi_legs WHERE bet_id=? ORDER BY leg_no",(int(bet.id),))
                    if not legs.empty:st.dataframe(legs,hide_index=True,use_container_width=True)
        st.download_button("Download this day's bets",daily.drop(columns=["ai_review","process_grade","calendar_date"],errors="ignore").to_csv(index=False),file_name=f"stakelab_{chosen.isoformat()}_bets.csv",mime="text/csv")

if page=="Performance":
    st.markdown("### Performance by custom tag")
    tagged=sport_rows(q("SELECT * FROM bets WHERE result IN ('Won','Lost','Push')"))
    rows=[]
    if not tagged.empty:
        for _,bet in tagged.iterrows():
            for tag in saved_bet_tags(bet.factors_json):
                unit=placement_unit(bet.factors_json)
                rows.append({"Tag":tag,"id":bet.id,"stake":bet.stake,"pnl":bet.pnl,"result":bet.result,"clv":bet.clv,"Net units":float(bet.pnl)/unit if unit else None})
    if rows:
        data=pd.DataFrame(rows)
        for column in ['stake','pnl','clv']:data[column]=pd.to_numeric(data[column],errors='coerce')
        results=data.groupby('Tag').agg(Bets=('id','count'),Stake=('stake','sum'),Profit=('pnl','sum'),CLV=('clv','mean'),CLV_samples=('clv','count')).reset_index()
        results['ROI (%)']=results.Profit.div(results.Stake.where(results.Stake.gt(0)))*100
        decisive=data[data.result.isin(['Won','Lost'])].copy()
        decisive['won']=decisive.result.eq('Won')
        wins=decisive.groupby('Tag').won.mean()*100
        results['Win rate (%)']=results.Tag.map(wins)
        tagged_units=data.groupby('Tag')['Net units'].agg(['sum','count'])
        results['Unit samples']=results.Tag.map(tagged_units['count'])
        results['Net units']=results.Tag.map(tagged_units['sum']).where(results['Unit samples'].gt(0))
        st.dataframe(results.round(2),use_container_width=True,hide_index=True)
        st.caption('Bets may carry several tags, so groups overlap. Pushes are excluded from win rate. CLV uses known closing prices only.')
    else:st.info('Settle a tagged bet to see its tag performance here.')

if page=="Dashboard" and selected_sport!="All":
    title=html.escape(selected_sport)
    st.markdown(f"<div class='page-kicker'>Sport analytics</div><div class='page-title'>{title} Analytics</div><div class='page-copy'>Your {title} bets, results and market performance.</div>",unsafe_allow_html=True)
    bets=summary['bets'].copy()
    if bets.empty:
        st.info(f'No {selected_sport} bets logged yet. Log a bet in this sport to start its analytics.')
    else:
        settled=summary['settled'].copy()
        pending=summary['pending']
        for column in ['stake','pnl','clv']:settled[column]=pd.to_numeric(settled[column],errors='coerce')
        profit=float(settled.pnl.sum());stake=float(settled.stake.sum())
        decisive=settled[settled.result.isin(['Won','Lost'])]
        a,b,c,d=st.columns(4)
        a.metric(f'{selected_sport} profit',money(profit))
        b.metric('ROI',f'{profit/stake*100:+.2f}%' if stake else '—')
        c.metric('Avg price CLV',f'{settled.clv.mean():+.2f} pp' if settled.clv.notna().any() else '—')
        d.metric('Win rate',f'{decisive.result.eq("Won").mean()*100:.1f}%' if not decisive.empty else '—')
        a,b,c=st.columns(3)
        a.metric('Settled bets',len(settled));b.metric('Open bets',len(pending))
        c.metric('Open stake',money(float(pd.to_numeric(pending.stake,errors='coerce').sum())))
        net_units,unit_samples=net_unit_results(settled)
        st.metric('Net units',f'{net_units:+.2f}u' if net_units is not None else '—')
        st.caption(f'Unit results cover {unit_samples} of {len(settled)} settled bets with a recorded unit size at placement.')
        st.caption(f'Only {selected_sport} wagers. Profit and ROI exclude open bets; win rate excludes pushes. CLV covers {int(settled.clv.notna().sum())} settled bets. Account bankroll remains in All / Bankroll.')
        if settled.empty:st.info('Your bets are still open. Settle a result to populate the profit chart and market analytics.')
        else:
            st.markdown('### Sport profit curve')
            curve=settled.groupby('event_date',as_index=False).pnl.sum().sort_values('event_date')
            curve['Cumulative P&L']=curve.pnl.cumsum()
            profit_chart(curve[['event_date','Cumulative P&L']],'event_date','Cumulative P&L')
            show_best_bet_types(settled,'sport_types')
            for heading,column in [('Performance by market','market'),('Performance by bookmaker','book')]:
                st.markdown('### '+heading)
                st.dataframe(monthly_breakdown(settled,column).round(2),hide_index=True,use_container_width=True)
            if len(settled)<20:st.caption('Small sample: these results describe your history and do not establish a predictive edge.')
        st.markdown('### Recent '+selected_sport+' bets')
        recent=bets.sort_values(['event_date','id'],ascending=False).head(20).copy()
        recent['Tags']=recent.factors_json.map(saved_bet_tags).map(lambda t:', '.join(t))
        recent.loc[~recent.result.isin(['Won','Lost','Push']),'pnl']=None
        st.dataframe(recent[['event_date','Custom sport','event','selection','bet_type','market','odds','stake','result','pnl','clv','Tags']],hide_index=True,use_container_width=True)
    if st.button('Log '+selected_sport+' bet',key='sport_log',use_container_width=True):
        st.session_state['requested_nav']='Multis' if selected_sport=='Multi' else 'Log Bet'
        if selected_sport in SPORTS:st.session_state['ssport']=selected_sport
        st.rerun()

# Compact mobile layout; calendar keeps its own seven-column layout.
st.markdown("""<style>
@media(max-width:640px){
.block-container{padding-left:.65rem!important;padding-right:.65rem!important}
.top-shell{flex-wrap:wrap;gap:8px;padding:10px}
.brand{min-width:0}.search-shell{display:none}.status-strip{justify-content:flex-start;width:100%}
.kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}
.kpi-card{min-width:0;padding:10px}.kpi-value{font-size:1.25rem}
.st-key-top_navigation [role="radiogroup"]{flex-wrap:nowrap!important;overflow-x:auto!important;-webkit-overflow-scrolling:touch;padding-bottom:12px}
.st-key-top_navigation label{min-height:44px!important;padding:9px 10px!important}
.st-key-sport_navigation label,.st-key-entry_sport_buttons label{min-height:44px!important;padding:8px 10px!important}
[data-testid="stMetric"]{padding:10px!important}[data-testid="stMetricValue"]{font-size:1.4rem!important}
[data-testid="stDataFrame"]{max-width:100%;overflow-x:auto}
[data-testid="stForm"]{padding:.7rem!important}
}
</style>""",unsafe_allow_html=True)


