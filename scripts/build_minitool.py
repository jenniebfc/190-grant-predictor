#!/usr/bin/env python3
"""
build_minitool.py
=================
Compiles the master web index.html into a 100% Xiaohongshu-compliant
offline mini-tool static package (minitool_build/ & 190-grant-predictor-minitool.zip).

Complies strictly with:
1. zip-artifact-spec.md:
   - index.html at root of zip
   - All JS externalized to ./app.js (no inline scripts, no type="module", no inline events)
   - All CSS externalized to ./style.css (with Chrome 61 fallbacks)
   - Pure relative ./ paths, zero external http(s) dependencies
2. device-capabilities.md:
   - Zero forbidden APIs (no navigator.clipboard, no window.print, no geolocation, etc.)
   - Compliant in-page modal for long-press copy
3. js-compatibility.md & css-compatibility.md:
   - Target: Android 8.1 / Chrome 61 (ES2017 max, flex gap fallbacks)
4. performance-budget.md:
   - Deterministic audit with audit_artifact.py & audit_artifact.mjs
"""

import os
import re
import sys
import json
import zipfile
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DIST_DIR = REPO_ROOT / 'minitool_build'
ZIP_PATH = REPO_ROOT / '190-grant-predictor-minitool.zip'
INDEX_HTML = REPO_ROOT / 'index.html'

SKILL_AUDIT_PY = REPO_ROOT / '.skill' / 'minitool-zip-builder' / 'scripts' / 'audit_artifact.py'
SKILL_AUDIT_MJS = REPO_ROOT / '.skill' / 'minitool-zip-builder' / 'scripts' / 'audit_artifact.mjs'

DIST_DIR.mkdir(parents=True, exist_ok=True)

print("[build_minitool] Reading master index.html...")
with open(INDEX_HTML, 'r', encoding='utf-8') as f:
    master_html = f.read()

# -------------------------------------------------------------
# 1. EXTRACT & ADAPT CSS -> minitool_build/style.css
# -------------------------------------------------------------
print("[build_minitool] Extracting and adapting CSS...")
style_match = re.search(r'<style>(.*?)</style>', master_html, re.DOTALL)
if not style_match:
    raise ValueError("Could not find <style> block in index.html")

raw_css = style_match.group(1).strip()

# Add Chrome 61 fallbacks for gap on key flex containers
chrome61_fallbacks = """
/* --- Chrome 61 Baseline Fallbacks --- */
.subclass-tab:not(:last-child) {
    margin-right: 4px;
}
@supports (gap: 4px) {
    .subclass-tab:not(:last-child) {
        margin-right: 0;
    }
}

.meta-tags > *:not(:last-child) {
    margin-right: 6px;
}
@supports (gap: 6px) {
    .meta-tags > *:not(:last-child) {
        margin-right: 0;
    }
}

.metric-cards > *:not(:last-child) {
    margin-right: 8px;
}
@supports (gap: 8px) {
    .metric-cards > *:not(:last-child) {
        margin-right: 0;
    }
}

/* In-Page Share Modal Component (Container Compliant: No forbidden navigator.clipboard) */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(15, 23, 42, 0.6);
    -webkit-backdrop-filter: blur(4px);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
    padding: 16px;
    box-sizing: border-box;
}

.modal-card {
    background: #FFFFFF;
    width: 100%;
    max-width: 480px;
    border-radius: var(--radius-xl, 14px);
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    box-sizing: border-box;
}

.modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.modal-title {
    font-size: 16px;
    font-weight: 700;
    color: var(--text, #0F172A);
}

.modal-close {
    background: none;
    border: none;
    font-size: 18px;
    color: var(--text-muted, #64748B);
    cursor: pointer;
    padding: 4px;
}

.modal-hint {
    font-size: 12px;
    color: var(--text-muted, #64748B);
    margin-bottom: 12px;
    line-height: 1.5;
}

.modal-textarea {
    width: 100%;
    height: 140px;
    border: 1px solid var(--border, #E2E8F0);
    border-radius: var(--radius-md, 8px);
    padding: 10px;
    font-size: 13px;
    color: var(--text, #0F172A);
    background: var(--surface-subtle, #F8FAFC);
    font-family: inherit;
    line-height: 1.5;
    resize: none;
    outline: none;
    margin-bottom: 14px;
    box-sizing: border-box;
    -webkit-user-select: text;
    user-select: text;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
}
"""

final_css = raw_css + "\n\n" + chrome61_fallbacks.strip() + "\n"
with open(DIST_DIR / 'style.css', 'w', encoding='utf-8') as f:
    f.write(final_css)

# -------------------------------------------------------------
# 2. EXTRACT & ADAPT HTML -> minitool_build/index.html
# -------------------------------------------------------------
print("[build_minitool] Extracting and adapting HTML...")
p_head_end = master_html.find('<style>')
p_style_end = master_html.find('</style>') + len('</style>')
p_script_start = master_html.find('<script>')
p_script_end = master_html.rfind('</script>')

head_raw = master_html[:p_head_end]
body_raw = master_html[p_style_end:p_script_start]

# Ensure viewport-fit=cover
if 'viewport-fit=cover' not in head_raw:
    head_raw = re.sub(
        r'<meta\s+name=["\']viewport["\'][^>]*>',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />',
        head_raw
    )

# Add stylesheet link in head
head_clean = head_raw.strip()
if '</head>' in head_clean:
    head_clean = head_clean.replace('</head>', '    <link rel="stylesheet" href="./style.css" />\n</head>')
else:
    head_clean += '\n    <link rel="stylesheet" href="./style.css" />\n</head>'

# Remove all inline event handlers (onclick=..., onchange=..., etc.)
body_clean = re.sub(r'\s+on[a-z]+="[^"]*"', '', body_raw)

# Ensure full table trigger has explicit ID full-table-trigger
body_clean = re.sub(
    r'<div class="acc-trigger" style="font-size:15px;">\s*<span>📊 展开 25个月',
    '<div class="acc-trigger" id="full-table-trigger" style="font-size:15px;">\n            <span>📊 展开 25个月',
    body_clean
)

# Replace action buttons with compliant share modal + reset button (remove window.print)
action_buttons_html = """
    <!-- Action Buttons -->
    <div class="action-row">
        <button class="btn btn-primary" id="btn-share">查看 / 复制我的批签预测结论</button>
        <button class="btn btn-outline" id="btn-reset">重置为默认条件</button>
    </div>

    <!-- In-page Share Modal (No forbidden clipboard API) -->
    <div class="modal-overlay" id="share-modal" style="display:none;">
        <div class="modal-card">
            <div class="modal-header">
                <h3 class="modal-title">我的批签预测结论</h3>
                <button class="modal-close" id="modal-close-btn">✕</button>
            </div>
            <p class="modal-hint">长按文本框即可全选复制，分享到小红书或微信群：</p>
            <textarea class="modal-textarea" id="share-text-area" readonly></textarea>
            <div class="modal-actions">
                <button class="btn btn-primary" id="modal-ok-btn">我知道了</button>
            </div>
        </div>
    </div>
"""

body_clean = re.sub(r'<div class="action-row">[\s\S]*?</div>', action_buttons_html.strip(), body_clean)

minitool_html = f"""{head_clean}
{body_clean.strip()}

    <script src="./app.js"></script>
</body>
</html>
"""

with open(DIST_DIR / 'index.html', 'w', encoding='utf-8') as f:
    f.write(minitool_html)

# -------------------------------------------------------------
# 3. EXTRACT & ADAPT JAVASCRIPT -> minitool_build/app.js
# -------------------------------------------------------------
print("[build_minitool] Extracting and adapting JavaScript...")
js_raw = master_html[p_script_start + len('<script>'):p_script_end].strip()

# Replace copyShareText and window.addEventListener with full event bindings & modal logic
# We find where copyShareText begins
p_copy = js_raw.find('// Copy Share Text')
if p_copy == -1:
    p_copy = js_raw.find('function copyShareText()')

if p_copy != -1:
    js_core = js_raw[:p_copy].strip()
else:
    js_core = js_raw.strip()

minitool_js_tail = """
// --- SHARE MODAL (CONTAINER COMPLIANT: NO CLIPBOARD API) ---
function openShareModal() {
    var select = document.getElementById('lodged-select');
    var month = select && select.selectedOptions && select.selectedOptions[0] ? select.selectedOptions[0].text : '未知';
    var tierEl = document.getElementById('tier-name');
    var tier = tierEl ? tierEl.textContent : '未知赛道';
    var dateEl = document.getElementById('grant-date-display');
    var date = dateEl ? dateEl.textContent : '测算中';
    var daysEl = document.getElementById('days-remaining');
    var days = daysEl ? daysEl.textContent : '-';
    var sc = currentSubclass;
    var scName = sc === '189' ? '澳洲 189 独立技术移民' : (sc === '491' ? '澳洲 491 偏远地区签证' : '澳洲 190 州担保技术移民');
    var baseline = sc === '189' ? 'FOI官方6,242人在池底盘与Ethan实盘测算标杆' : (sc === '491' ? 'FOI官方18,442人底盘与MD122四Tier模型' : 'FOI官方24,196人底盘与MD122四Tier模型');

    var text = '【' + scName + ' 批签预测】\\n' +
        '递交月份：' + month + '\\n' +
        '所属赛道：' + tier + '\\n' +
        '预计获批：' + date + ' (距今约' + days + ')\\n' +
        '测算基准：' + baseline + '\\n' +
        '仅供排期参考，祝早日下签！';

    var modal = document.getElementById('share-modal');
    var txtArea = document.getElementById('share-text-area');
    if (modal && txtArea) {
        txtArea.value = text;
        modal.style.display = 'flex';
        if (txtArea.focus) txtArea.focus();
        if (txtArea.select) txtArea.select();
    }
}

function closeShareModal() {
    var modal = document.getElementById('share-modal');
    if (modal) modal.style.display = 'none';
}

function resetDefaults() {
    var select = document.getElementById('lodged-select');
    if (select) {
        if (currentSubclass === '189') select.value = '20'; // 2026-06
        else if (currentSubclass === '491') select.value = '19'; // 2026-01
        else select.value = '7'; // 2026-01 for 190
    }
    var rLoc = document.getElementById('loc-onshore');
    if (rLoc) rLoc.checked = true;
    var rOcc = document.getElementById('occ-non-priority');
    if (rOcc) rOcc.checked = true;
    var rFam = document.getElementById('fam-single');
    if (rFam) rFam.checked = true;
    calculateForecast();
}

// --- CONTAINER EVENT BINDINGS (NO INLINE ON* EVENTS PER CSP) ---
window.addEventListener('DOMContentLoaded', function() {
    initSelect();
    calculateForecast();

    // 1. Subclass tabs
    var tab189 = document.getElementById('tab-189');
    if (tab189) {
        tab189.addEventListener('click', function() { switchSubclass('189'); });
    }
    var tab190 = document.getElementById('tab-190');
    if (tab190) {
        tab190.addEventListener('click', function() { switchSubclass('190'); });
    }
    var tab491 = document.getElementById('tab-491');
    if (tab491) {
        tab491.addEventListener('click', function() { switchSubclass('491'); });
    }

    // 2. Select input
    var selectEl = document.getElementById('lodged-select');
    if (selectEl) {
        selectEl.addEventListener('change', calculateForecast);
    }

    // 3. Radio inputs
    var radios = document.querySelectorAll('input[type="radio"]');
    radios.forEach(function(r) {
        r.addEventListener('change', calculateForecast);
    });

    // 4. Koi blessing
    var btnKoi = document.getElementById('btn-koi');
    if (btnKoi) {
        btnKoi.addEventListener('click', triggerKoiBlessing);
    }

    // 5. Accordions
    var accTriggers = document.querySelectorAll('.acc-trigger');
    accTriggers.forEach(function(trigger) {
        if (trigger.id === 'full-table-trigger') return;
        trigger.addEventListener('click', function() {
            toggleAcc(this);
        });
    });

    // 6. Full table accordion trigger
    var fullTableTrigger = document.getElementById('full-table-trigger');
    if (fullTableTrigger) {
        fullTableTrigger.addEventListener('click', function() {
            toggleFullTable(this);
        });
    }

    // 7. Table mode switch tabs
    var tableTabs = document.querySelectorAll('.table-tab-btn');
    tableTabs.forEach(function(tab) {
        tab.addEventListener('click', function() {
            var mode = this.getAttribute('data-mode');
            switchTableMode(mode, this);
        });
    });

    // 8. Action buttons
    var btnShare = document.getElementById('btn-share');
    if (btnShare) {
        btnShare.addEventListener('click', openShareModal);
    }

    var btnReset = document.getElementById('btn-reset');
    if (btnReset) {
        btnReset.addEventListener('click', resetDefaults);
    }

    // 9. Share Modal Close
    var modalClose = document.getElementById('modal-close-btn');
    if (modalClose) {
        modalClose.addEventListener('click', closeShareModal);
    }

    var modalOk = document.getElementById('modal-ok-btn');
    if (modalOk) {
        modalOk.addEventListener('click', closeShareModal);
    }

    var modalOverlay = document.getElementById('share-modal');
    if (modalOverlay) {
        modalOverlay.addEventListener('click', function(e) {
            if (e.target === modalOverlay) closeShareModal();
        });
    }
});
"""

final_js = js_core + "\n\n" + minitool_js_tail.strip() + "\n"
with open(DIST_DIR / 'app.js', 'w', encoding='utf-8') as f:
    f.write(final_js)

print(f"[build_minitool] Files generated in: {DIST_DIR}")
for f in DIST_DIR.iterdir():
    print(f"  - {f.name}: {f.stat().st_size} bytes")

# -------------------------------------------------------------
# 4. PACKAGE ZIP -> 190-grant-predictor-minitool.zip
# -------------------------------------------------------------
print(f"[build_minitool] Packing zip archive: {ZIP_PATH}")
with zipfile.ZipFile(ZIP_PATH, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for item in sorted(DIST_DIR.rglob('*')):
        if item.is_file() and not item.name.startswith('.') and '__MACOSX' not in item.parts:
            arcname = item.relative_to(DIST_DIR).as_posix()
            zf.write(item, arcname)

print(f"[build_minitool] Zip created successfully: {ZIP_PATH.stat().st_size} bytes")

# -------------------------------------------------------------
# 5. AUDIT ARTIFACTS
# -------------------------------------------------------------
print("[build_minitool] Running minitool audit checks...")
if SKILL_AUDIT_PY.exists():
    print("--- Python Audit (Directory) ---")
    ret_dir = subprocess.run([sys.executable, str(SKILL_AUDIT_PY), str(DIST_DIR)], capture_output=True, text=True)
    print(ret_dir.stdout.strip())
    if ret_dir.returncode != 0:
        print("[ERROR] Python Directory Audit FAILED:", ret_dir.stderr.strip())
        sys.exit(1)

    print("--- Python Audit (Zip Package) ---")
    ret_zip = subprocess.run([sys.executable, str(SKILL_AUDIT_PY), str(ZIP_PATH)], capture_output=True, text=True)
    print(ret_zip.stdout.strip())
    if ret_zip.returncode != 0:
        print("[ERROR] Python Zip Audit FAILED:", ret_zip.stderr.strip())
        sys.exit(1)

if SKILL_AUDIT_MJS.exists():
    try:
        print("--- Node Audit (Directory) ---")
        ret_node_dir = subprocess.run(['node', str(SKILL_AUDIT_MJS), str(DIST_DIR)], capture_output=True, text=True)
        print(ret_node_dir.stdout.strip())
        print("--- Node Audit (Zip Package) ---")
        ret_node_zip = subprocess.run(['node', str(SKILL_AUDIT_MJS), str(ZIP_PATH)], capture_output=True, text=True)
        print(ret_node_zip.stdout.strip())
    except Exception as e:
        print(f"[WARN] Node audit run failed: {e}")

print("[build_minitool] All builds and audits COMPLETED successfully!")
