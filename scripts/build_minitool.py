import os
import sys
import json
import zipfile
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DIST_DIR = REPO_ROOT / 'minitool_build'
ZIP_PATH = REPO_ROOT / '190-grant-predictor-minitool.zip'

DIST_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load forecast data
forecast_file = SCRIPT_DIR / 'forecast_data.json'
if not forecast_file.exists():
    forecast_file = REPO_ROOT / 'forecast_data.json'

with open(forecast_file, 'r', encoding='utf-8') as f:
    fdata = json.load(f)

json_data_str = json.dumps(fdata, ensure_ascii=False)

# 2. Build style.css
css_content = '''/* --- BASE THEME & RESET --- */
:root {
    --bg: #F8FAFC;
    --surface: #FFFFFF;
    --surface-muted: #F1F5F9;
    --surface-subtle: #F8FAFC;
    --border: #E2E8F0;
    --border-hover: #CBD5E1;
    --text: #0F172A;
    --text-secondary: #475569;
    --text-muted: #64748B;
    --text-subtle: #94A3B8;
    --primary: #0F172A;
    --primary-hover: #1E293B;
    --accent: #2563EB;
    --accent-light: #EFF6FF;
    --accent-border: #BFDBFE;
    --t1: #EA580C;
    --t1-bg: #FFF7ED;
    --t1-border: #FFEDD5;
    --t2: #2563EB;
    --t2-bg: #EFF6FF;
    --t2-border: #DBEAFE;
    --t3: #059669;
    --t3-bg: #ECFDF5;
    --t3-border: #D1FAE5;
    --t4: #9333EA;
    --t4-bg: #FAF5FF;
    --t4-border: #F3E8FF;
    --radius-xl: 14px;
    --radius-lg: 10px;
    --radius-md: 8px;
    --radius-sm: 6px;
}

*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-tap-highlight-color: transparent;
}

html {
    height: 100%;
    touch-action: manipulation;
}

body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    -webkit-font-smoothing: antialiased;
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    user-select: none;
    line-height: 1.5;
    padding: 0;
    margin: 0;
}

/* Allow text selection where helpful */
input, select, textarea, .modal-textarea, td, .feed-row, .app-desc, .blessing-msg, .tracker-val {
    -webkit-user-select: text;
    user-select: text;
}

.app-layout {
    max-width: 900px;
    margin: 0 auto;
    padding-top: calc(20px + var(--safe-area-inset-top, env(safe-area-inset-top, 0px)));
    padding-bottom: calc(40px + var(--safe-area-inset-bottom, env(safe-area-inset-bottom, 0px)));
    padding-left: calc(16px + var(--safe-area-inset-left, env(safe-area-inset-left, 0px)));
    padding-right: calc(16px + var(--safe-area-inset-right, env(safe-area-inset-right, 0px)));
}

/* Header */
.app-header {
    margin-bottom: 24px;
}

.meta-tags {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 8px;
}

.meta-tags > * {
    margin-right: 8px;
    margin-bottom: 8px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 500;
    background: #ECFDF5;
    color: #065F46;
    border: 1px solid #A7F3D0;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #059669;
    margin-right: 6px;
}

.info-pill {
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 500;
    background: var(--surface-muted);
    color: var(--text-secondary);
    border: 1px solid var(--border);
}

.app-title {
    font-size: 26px;
    font-size: clamp(24px, 4.5vw, 32px);
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text);
    margin-bottom: 8px;
}

.app-desc {
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.6;
}

/* Panels */
.panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    padding: 20px;
    margin-bottom: 16px;
}

.panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}

.panel-title {
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
}

/* Form Controls */
.control-grid {
    display: flex;
    flex-direction: column;
}

.control-grid > * {
    margin-bottom: 16px;
}

.control-grid > *:last-child {
    margin-bottom: 0;
}

.field-label {
    display: block;
    font-size: 13px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 8px;
}

.field-desc {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 6px;
    line-height: 1.4;
}

.select-shell {
    position: relative;
    width: 100%;
}

.custom-select {
    width: 100%;
    appearance: none;
    -webkit-appearance: none;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 10px 14px;
    font-size: 14px;
    color: var(--text);
    cursor: pointer;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 10 6'%3E%3Cpath stroke='%2364748B' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m1 1 4 4 4-4'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 14px center;
    background-size: 10px 6px;
    outline: none;
}

.custom-select:focus {
    border-color: var(--accent);
}

.segment-group {
    display: flex;
    background: var(--surface-muted);
    padding: 3px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
}

.segment-item {
    flex: 1;
    min-width: 0;
}

.segment-item input[type="radio"] {
    position: absolute;
    opacity: 0;
    pointer-events: none;
}

.segment-label {
    display: block;
    text-align: center;
    padding: 8px 4px;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-secondary);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all 0.15s ease;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.segment-item input[type="radio"]:checked + .segment-label {
    background: var(--surface);
    color: var(--text);
    font-weight: 600;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
}

/* Tier Strip */
.tier-strip {
    border-radius: var(--radius-lg);
    padding: 12px 16px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 1px solid transparent;
}

.tier-strip.t1 { background: var(--t1-bg); border-color: var(--t1-border); }
.tier-strip.t2 { background: var(--t2-bg); border-color: var(--t2-border); }
.tier-strip.t3 { background: var(--t3-bg); border-color: var(--t3-border); }
.tier-strip.t4 { background: var(--t4-bg); border-color: var(--t4-border); }

.tier-left {
    display: flex;
    align-items: center;
}

.tier-left > *:first-child {
    margin-right: 12px;
}

.tier-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 99px;
    letter-spacing: 0.02em;
    flex-shrink: 0;
}

.tier-tag.t1 { background: #F97316; color: #fff; }
.tier-tag.t2 { background: #2563EB; color: #fff; }
.tier-tag.t3 { background: #059669; color: #fff; }
.tier-tag.t4 { background: #9333EA; color: #fff; }

.tier-name {
    font-size: 14px;
    font-weight: 700;
    color: var(--text);
}

.tier-caption {
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 2px;
}

/* Hero Panel */
.hero-panel {
    background: var(--surface);
    border: 2px solid var(--primary);
    border-radius: var(--radius-xl);
    padding: 22px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
}

.hero-top-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
}

.hero-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.mode-chip {
    font-size: 11px;
    font-weight: 600;
    background: var(--surface-muted);
    color: var(--text-secondary);
    padding: 2px 8px;
    border-radius: 4px;
    border: 1px solid var(--border);
}

.hero-date {
    font-size: 34px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.02em;
    line-height: 1.15;
    margin: 4px 0 12px;
}

.hero-date.cleared {
    font-size: 22px;
    color: #059669;
}

/* Direct Grant Fast-track Card */
.direct-grant-card {
    margin-top: 10px;
    margin-bottom: 14px;
    padding: 12px 14px;
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    font-size: 13px;
    color: #166534;
    line-height: 1.5;
}

.direct-grant-card > *:first-child {
    margin-right: 10px;
}

.dg-badge {
    display: inline-flex;
    align-items: center;
    background: #16A34A;
    color: #FFFFFF;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    white-space: nowrap;
    flex-shrink: 0;
    letter-spacing: 0.02em;
}

.dg-text {
    flex: 1;
}

.dg-date-highlight {
    font-weight: 700;
    color: #15803D;
    text-decoration: underline;
}

/* Metric Cards */
.metric-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 10px;
    gap: 10px;
    margin-bottom: 18px;
}

.metric-cell {
    background: var(--surface-subtle);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 10px 12px;
}

.metric-cell-label {
    font-size: 11px;
    color: var(--text-muted);
    margin-bottom: 2px;
}

.metric-cell-val {
    font-size: 14px;
    font-weight: 700;
    color: var(--text);
}

/* Progress Block */
.progress-block {
    background: var(--surface-subtle);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 14px 16px;
}

.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.progress-title {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-muted);
}

.progress-badge {
    font-size: 12px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 99px;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    color: var(--accent);
}

.progress-badge.complete {
    background: #ECFDF5;
    border-color: #A7F3D0;
    color: #059669;
}

.progress-line {
    height: 9px;
    background: var(--surface-muted);
    border-radius: 99px;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    background: var(--accent);
    border-radius: 99px;
    transition: width 0.4s ease;
}

.progress-bar.complete {
    background: #059669;
}

.progress-labels {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 8px;
    font-weight: 500;
}

/* Seamless Mental Massage Card */
.blessing-card {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: var(--radius-xl);
    padding: 16px 18px;
    margin-bottom: 16px;
    display: flex;
    align-items: flex-start;
}

.blessing-card > *:first-child {
    margin-right: 14px;
}

.blessing-avatar {
    font-size: 22px;
    line-height: 1;
    padding-top: 2px;
    flex-shrink: 0;
}

.blessing-main {
    flex: 1;
}

.blessing-msg {
    font-size: 13px;
    color: #166534;
    line-height: 1.65;
    margin-bottom: 10px;
}

.blessing-msg strong {
    color: #14532D;
    font-weight: 600;
}

.blessing-footer {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
}

.blessing-footer > *:first-child {
    margin-right: 12px;
}

.koi-btn {
    background: #16A34A;
    color: #FFFFFF;
    border: none;
    padding: 6px 14px;
    border-radius: var(--radius-md);
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.koi-btn:active {
    opacity: 0.85;
}

.koi-feedback {
    font-size: 12px;
    font-weight: 600;
    color: #15803D;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.koi-feedback.visible {
    opacity: 1;
}

/* 4 Modes Section */
.modes-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-gap: 12px;
    gap: 12px;
}

@media (max-width: 768px) {
    .modes-container {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 480px) {
    .modes-container {
        grid-template-columns: 1fr;
    }
}

.mode-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
}

.mode-card.active {
    border-color: var(--accent);
    box-shadow: 0 0 0 1px var(--accent);
}

.mode-badge-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
}

.mode-id {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
}

.rec-tag {
    font-size: 10px;
    font-weight: 600;
    padding: 2px 7px;
    border-radius: 4px;
    letter-spacing: 0.01em;
    white-space: nowrap;
}

.rec-tag.verified {
    background: #ECFDF5;
    color: #065F46;
    border: 1px solid #A7F3D0;
}

.rec-tag.neutral {
    background: #F1F5F9;
    color: #475569;
    border: 1px solid #E2E8F0;
}

.rec-tag.obsolete {
    background: #FEF2F2;
    color: #991B1B;
    border: 1px solid #FECACA;
}

.mode-card.obsolete {
    opacity: 0.68;
    background: #FAFAFA;
    border-style: dashed;
}

.mode-title-text {
    font-size: 13px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 8px;
}

.mode-date-val {
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.01em;
    margin-bottom: 6px;
}

.mode-desc-text {
    font-size: 11px;
    color: var(--text-secondary);
    line-height: 1.4;
}

/* Live Daily Activity Tracker Banner */
.live-tracker-banner {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: var(--radius-xl);
    padding: 16px 18px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

.tracker-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}

.tracker-badge {
    display: inline-flex;
    align-items: center;
    font-size: 13px;
    font-weight: 700;
    color: var(--text);
}

.pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10B981;
    margin-right: 6px;
}

.tracker-time {
    font-size: 12px;
    color: var(--text-muted);
}

.tracker-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    grid-gap: 12px;
    gap: 12px;
}

.tracker-col {
    background: var(--surface-subtle);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
}

.tracker-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 0.02em;
    margin-bottom: 4px;
}

.tracker-val {
    font-size: 13px;
    color: var(--text);
    margin-bottom: 4px;
}

.tracker-val strong {
    color: var(--accent);
    font-weight: 700;
}

.tracker-hint {
    font-size: 11px;
    color: var(--text-secondary);
    line-height: 1.4;
}

/* Feed List */
.feed-rows {
    display: flex;
    flex-direction: column;
}

.feed-rows > * {
    margin-bottom: 8px;
}

.feed-rows > *:last-child {
    margin-bottom: 0;
}

.feed-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 14px;
    background: var(--surface-subtle);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    font-size: 13px;
}

.feed-occ {
    font-weight: 600;
    color: var(--text);
}

.feed-sub {
    font-size: 11px;
    color: var(--text-muted);
    margin-left: 6px;
}

.feed-status {
    display: inline-flex;
    align-items: center;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
    background: #ECFDF5;
    color: #059669;
}

.feed-tag-dg {
    display: inline-flex;
    align-items: center;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    background: #EFF6FF;
    color: #1D4ED8;
    border: 1px solid #BFDBFE;
}

/* Accordions */
.acc-item {
    border-bottom: 1px solid var(--border);
    padding: 12px 0;
}

.acc-item:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.acc-trigger {
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
}

.acc-body {
    display: none;
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-top: 8px;
}

/* 25-Month Table Tabs */
.table-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}

.table-mode-tabs {
    display: flex;
    flex-wrap: wrap;
}

.table-mode-tabs > * {
    margin-right: 6px;
    margin-bottom: 6px;
}

.table-tab-btn {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
}

.table-tab-btn.active {
    background: var(--primary);
    color: #FFFFFF;
    border-color: var(--primary);
    font-weight: 600;
}

.table-mode-hint {
    font-size: 12px;
    color: var(--text-muted);
    margin-bottom: 10px;
    line-height: 1.45;
    background: var(--surface-subtle);
    padding: 8px 12px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
}

.table-mode-hint strong {
    color: var(--text);
}

.table-wrap {
    overflow-x: auto;
    margin-top: 10px;
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    min-width: 540px;
}

th, td {
    padding: 8px 12px;
    border-bottom: 1px solid var(--border);
    text-align: center;
}

th {
    background: var(--surface-muted);
    color: var(--text);
    font-weight: 600;
}

td:first-child {
    text-align: left;
    font-weight: 600;
    color: var(--text);
}

/* Bottom Action Buttons */
.action-row {
    display: flex;
    justify-content: center;
    margin-top: 24px;
}

.action-row > * {
    margin: 0 5px;
}

.btn-primary {
    background: var(--primary);
    color: #fff;
    border: 1px solid var(--primary);
    padding: 10px 20px;
    border-radius: var(--radius-md);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
}

.btn-primary:active {
    opacity: 0.85;
}

.btn-outline {
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 10px 18px;
    border-radius: var(--radius-md);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
}

.btn-outline:active {
    background: var(--surface-muted);
}

/* In-Page Share Modal Component */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(15, 23, 42, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
    padding: 16px;
}

.modal-card {
    background: #FFFFFF;
    width: 100%;
    max-width: 480px;
    border-radius: var(--radius-xl);
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
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
    color: var(--text);
}

.modal-close {
    background: none;
    border: none;
    font-size: 18px;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px;
}

.modal-hint {
    font-size: 12px;
    color: var(--text-muted);
    margin-bottom: 12px;
}

.modal-textarea {
    width: 100%;
    height: 140px;
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 10px;
    font-size: 13px;
    font-family: inherit;
    line-height: 1.5;
    background: var(--surface-subtle);
    color: var(--text);
    resize: none;
    outline: none;
    margin-bottom: 14px;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
}

/* Footer */
.app-footer {
    text-align: center;
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 40px;
    line-height: 1.6;
}
'''

with open(DIST_DIR / 'style.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

# 3. Build index.html
html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
    <title>澳洲 190 · MD122 智能批签预测</title>
    <link rel="stylesheet" href="./style.css" />
</head>
<body>

<div class="app-layout">

    <!-- Header -->
    <header class="app-header">
        <div class="meta-tags">
            <span class="status-pill"><span class="status-dot"></span>9月23日实盘校准完成 · 吻合度&gt;96%</span>
            <span class="info-pill">FOI 24,196人唯一人头底盘</span>
            <span class="info-pill">MD122 官方四Tier体系</span>
            <span class="info-pill" style="color:var(--accent);border-color:var(--accent-border);background:var(--accent-light);">实测确证：境内外双轨并行</span>
        </div>
        <h1 class="app-title">澳洲 190 · MD122 智能批签预测</h1>
        <p class="app-desc">
            基于内政部官方底盘数据与最新部长令执行节奏，输入递交月份与申请人属性，即刻测算批签窗口与多模式推演。
        </p>
    </header>

    <!-- Input Form Panel -->
    <section class="panel">
        <div class="panel-header">
            <h2 class="panel-title">申请人画像与参数配置</h2>
        </div>
        <div class="control-grid">

            <!-- Lodged Month -->
            <div class="field">
                <label class="field-label" for="lodged-select">递交月份 (Date of Lodged)</label>
                <div class="select-shell">
                    <select id="lodged-select" class="custom-select">
                        <!-- Filled by JS -->
                    </select>
                </div>
            </div>

            <!-- Location -->
            <div class="field">
                <label class="field-label">当前所在地</label>
                <div class="segment-group">
                    <div class="segment-item">
                        <input type="radio" id="loc-onshore" name="location" value="onshore" checked />
                        <label class="segment-label" for="loc-onshore">境内 (Onshore)</label>
                    </div>
                    <div class="segment-item">
                        <input type="radio" id="loc-offshore" name="location" value="offshore" />
                        <label class="segment-label" for="loc-offshore">境外 (Offshore)</label>
                    </div>
                </div>
            </div>

            <!-- Occupation Type -->
            <div class="field">
                <label class="field-label">职业属性</label>
                <div class="segment-group">
                    <div class="segment-item">
                        <input type="radio" id="occ-priority" name="occupation" value="priority" />
                        <label class="segment-label" for="occ-priority">优先职业 (Priority)</label>
                    </div>
                    <div class="segment-item">
                        <input type="radio" id="occ-non-priority" name="occupation" value="non-priority" checked />
                        <label class="segment-label" for="occ-non-priority">非优先职业 (General)</label>
                    </div>
                </div>
                <div class="field-desc">优先职业含：医疗护理、教师、建筑建造、农业、国防等关键领域</div>
            </div>

            <!-- Family Composition -->
            <div class="field">
                <label class="field-label">申请人结构</label>
                <div class="segment-group">
                    <div class="segment-item">
                        <input type="radio" id="fam-single" name="family" value="single" checked />
                        <label class="segment-label" for="fam-single">单人申请</label>
                    </div>
                    <div class="segment-item">
                        <input type="radio" id="fam-family" name="family" value="family" />
                        <label class="segment-label" for="fam-family">携副申请人</label>
                    </div>
                </div>
                <div class="field-desc">境外非优先将依此细分为单人赛道 (Tier 3) 与家庭赛道 (Tier 4)</div>
            </div>

        </div>
    </section>

    <!-- Tier Strip -->
    <div id="tier-strip" class="tier-strip t2">
        <div class="tier-left">
            <span id="tier-tag" class="tier-tag t2">Tier 2</span>
            <div>
                <div id="tier-name" class="tier-name">境内非优先职业赛道</div>
                <div id="tier-caption" class="tier-caption">澳洲境内非优先通道，占用境内独立流水线（~94人/日），配额充足稳健。</div>
            </div>
        </div>
    </div>

    <!-- Hero Result Card -->
    <section class="hero-panel">
        <div class="hero-top-row">
            <span class="hero-label">预计批签下签时间</span>
            <span class="mode-chip">推荐模式 2 · 官方双目标兑现</span>
        </div>
        <div id="grant-date-display" class="hero-date">2026-10-09</div>

        <!-- Direct Grant Fast-track Window -->
        <div class="direct-grant-card" id="direct-grant-card">
            <span class="dg-badge">⚡ 免补料直签先锋窗口</span>
            <span class="dg-text" id="dg-text">若材料齐全无 s56 补料，预计可提前 3~7 个工作日率先突围下签！</span>
        </div>

        <!-- Metrics row -->
        <div class="metric-cards">
            <div class="metric-cell">
                <div class="metric-cell-label">距离今日约</div>
                <div class="metric-cell-val" id="days-remaining">17 天</div>
            </div>
            <div class="metric-cell">
                <div class="metric-cell-label">移民局净工作日</div>
                <div class="metric-cell-val" id="workdays-remaining">13 天</div>
            </div>
            <div class="metric-cell">
                <div class="metric-cell-label">配额财年归属</div>
                <div class="metric-cell-val" id="fy-label">FY27 境内</div>
            </div>
        </div>

        <!-- Progress Bar with Percentage -->
        <div class="progress-block">
            <div class="progress-header">
                <span class="progress-title">全程排期等待进度</span>
                <span class="progress-badge" id="progress-badge">
                    <span id="progress-pct-text">已完成 75%</span>
                </span>
            </div>
            <div class="progress-line">
                <div class="progress-bar" id="progress-bar" style="width: 75%;"></div>
            </div>
            <div class="progress-labels">
                <span id="label-start">递交申请</span>
                <span style="color:var(--text-secondary);font-weight:600;">2026-09-19 切入MD122</span>
                <span id="label-end">预计获批</span>
            </div>
        </div>
    </section>

    <!-- Seamless Mental Massage & Koi Blessing Card -->
    <div class="blessing-card" id="blessing-card">
        <div class="blessing-avatar">🐟✨</div>
        <div class="blessing-main">
            <div class="blessing-msg" id="blessing-msg">
                <!-- Dynamically filled by JS -->
            </div>
            <div class="blessing-footer">
                <button class="koi-btn" id="btn-koi">
                    <span>点亮今日下签锦鲤</span>
                </button>
                <span class="koi-feedback" id="koi-feedback"></span>
            </div>
        </div>
    </div>

    <!-- Four Modes Comparison -->
    <section class="panel">
        <div class="panel-header">
            <h2 class="panel-title">四套情景模式推演对照</h2>
        </div>
        <div class="modes-container">

            <!-- Mode 2 (Active / Rec) -->
            <div class="mode-card active">
                <div>
                    <div class="mode-badge-top">
                        <span class="mode-id">模式 2</span>
                        <span class="rec-tag verified">实测吻合 96% · 官方运行模式</span>
                    </div>
                    <div class="mode-title-text">双目标兑现 · 提速</div>
                </div>
                <div class="mode-date-val" id="m2-date">-</div>
                <div class="mode-desc-text">境内94+境外40人/日。实测印证：双轨独立全速推进，打满全财年35,500总配额。</div>
            </div>

            <!-- Mode 1 -->
            <div class="mode-card">
                <div>
                    <div class="mode-badge-top">
                        <span class="mode-id">模式 1</span>
                        <span class="rec-tag neutral">基准参考</span>
                    </div>
                    <div class="mode-title-text">128人/日 · 固定基准</div>
                </div>
                <div class="mode-date-val" id="m1-date">-</div>
                <div class="mode-desc-text">固定产能不借调，节奏较保守，全财年略有1,198人未消化。</div>
            </div>

            <!-- Mode 3 -->
            <div class="mode-card">
                <div>
                    <div class="mode-badge-top">
                        <span class="mode-id">模式 3</span>
                        <span class="rec-tag neutral">观察参考</span>
                    </div>
                    <div class="mode-title-text">T3单人优先并行</div>
                </div>
                <div class="mode-date-val" id="m3-date">-</div>
                <div class="mode-desc-text">境外单人分得64%产能。当前实盘以T1冲刺为主，此模式作中远期参考。</div>
            </div>

            <!-- Mode 4 -->
            <div class="mode-card obsolete">
                <div>
                    <div class="mode-badge-top">
                        <span class="mode-id">模式 4</span>
                        <span class="rec-tag obsolete">已落空 · 实测证伪</span>
                    </div>
                    <div class="mode-title-text" style="color:var(--text-muted);text-decoration:line-through;">单通道顺序 (已失效)</div>
                </div>
                <div class="mode-date-val" id="m4-date" style="text-decoration:line-through;color:var(--text-muted);">-</div>
                <div class="mode-desc-text" style="color:var(--text-muted);">假定境内全清才轮到境外。实盘显示境外已大面积下签，此倒退模式彻底失效。</div>
            </div>

        </div>
    </section>

    <!-- Live Daily Activity Tracker (SmartVisaGuide #17784) -->
    <div class="live-tracker-banner">
        <div class="tracker-header">
            <span class="tracker-badge"><span class="pulse-dot"></span> 9月23日 官方审批实盘雷达 (MD122 运行第 5 日)</span>
            <span class="tracker-time">数据源：SmartVisaGuide Post #17784 &amp; 官方 Subclass 190 宏观数据</span>
        </div>
        <div class="tracker-grid">
            <div class="tracker-col">
                <div class="tracker-label">🌟 Priority 优先通道实测 (医疗/幼教/紧缺基建)</div>
                <div class="tracker-val">推进至 <strong>2026-04-13</strong> (医疗极速) / <strong>2025-11-04</strong> (工程直签)</div>
                <div class="tracker-hint">
                    官方周期：<strong>25% 3.7个月 | 50% 5.2个月 | 75% 12.7个月</strong>。<br>
                    实盘：9.23 塔州急诊护士仅 <strong>5.4个月(163天)</strong> 秒批！NSW境外电工与土木10~12个月免补料直签。
                </div>
            </div>
            <div class="tracker-col">
                <div class="tracker-label">🦘 Onshore 境内普通通道实测 (Tier 2/3)</div>
                <div class="tracker-val">前沿推进至 <strong>2026-01-28</strong> · 旧案集中出清至 <strong>2025-05</strong></div>
                <div class="tracker-hint">
                    官方周期：<strong>25% 8.5个月 | 50% 9.3个月 | 90% 14.8个月</strong>。<br>
                    实盘：9.23 SA机械工程师与NSW汽车技师在完成s56补料后集中获批（16.5个月）；1月新递交案稳定消化。
                </div>
            </div>
            <div class="tracker-col">
                <div class="tracker-label">🌏 Offshore 境外普通通道实测 (Tier 4)</div>
                <div class="tracker-val">稳步消化至 <strong>2025-04 ~ 2025-05</strong></div>
                <div class="tracker-hint">
                    官方周期：<strong>25% 15.5个月 | 50% 15.9个月 | 90% 17.1个月</strong>。<br>
                    实盘：9.21 计算机网络工程师历时 17.4 个月获批。配额仍处于审慎控盘阶段，建议维持稳健排期预期。
                </div>
            </div>
        </div>
    </div>

    <!-- Real-world Activity Feed -->
    <section class="panel">
        <div class="panel-header">
            <h2 class="panel-title">9月21日 ~ 9月23日 实盘批签追踪实录 (SmartVisaGuide)</h2>
        </div>
        <div class="feed-rows">
            <!-- 9/23 Grants -->
            <div class="feed-row">
                <div>
                    <span class="feed-occ">重症与急诊注册护士 (Critical Care RN)</span>
                    <span class="feed-sub">TAS 境内 190 · 2026-04-13 递交 (85分)</span>
                </div>
                <div style="display:flex;align-items:center;">
                    <span class="feed-tag-dg" style="margin-right:8px;">⚡ 5.4个月极速下签</span>
                    <span class="feed-status">9/23 下签 · Tier 1 医疗先锋</span>
                </div>
            </div>
            <div class="feed-row">
                <div>
                    <span class="feed-occ">机械工程师 (Mechanical Engineer)</span>
                    <span class="feed-sub">SA 境内 190 · 2025-05-06 递交 (75分)</span>
                </div>
                <div style="display:flex;align-items:center;">
                    <span style="font-size:12px;color:var(--text-muted);margin-right:8px;">8/21 s56工作证明</span>
                    <span class="feed-status">9/23 下签 · 历时16.6个月(旧案清盘)</span>
                </div>
            </div>
            <div class="feed-row">
                <div>
                    <span class="feed-occ">汽车技术工种 (Automotive)</span>
                    <span class="feed-sub">NSW 境内 190 · 2025-05-07 递交</span>
                </div>
                <div style="display:flex;align-items:center;">
                    <span style="font-size:12px;color:var(--text-muted);margin-right:8px;">8/24 s56补料</span>
                    <span class="feed-status">9/23 下签 · 历时16.5个月</span>
                </div>
            </div>
            <!-- 9/22 Direct Grant & Priority -->
            <div class="feed-row">
                <div>
                    <span class="feed-occ">通用电工 (Electrician General)</span>
                    <span class="feed-sub">NSW 境外 190 · 2025-09-22 递交 (70分)</span>
                </div>
                <div style="display:flex;align-items:center;">
                    <span class="feed-tag-dg" style="margin-right:8px;">⚡ 免补料直签 (Direct Grant)</span>
                    <span class="feed-status">9/22 下签 · 整整12.0个月秒批</span>
                </div>
            </div>
            <div class="feed-row">
                <div>
                    <span class="feed-occ">土木工程师 (Civil Engineer)</span>
                    <span class="feed-sub">NSW 境外 190 · 2025-11-04 递交 (85分)</span>
                </div>
                <div style="display:flex;align-items:center;">
                    <span class="feed-tag-dg" style="margin-right:8px;">⚡ 免补料直签 (Direct Grant)</span>
                    <span class="feed-status">9/22 下签 · 历时10.6个月(破纪录)</span>
                </div>
            </div>
            <div class="feed-row">
                <div>
                    <span class="feed-occ">建筑项目经理 (Construction PM)</span>
                    <span class="feed-sub">WA 境外 190 · 2025-06-29 递交</span>
                </div>
                <div style="display:flex;align-items:center;">
                    <span style="font-size:12px;color:var(--text-muted);margin-right:8px;">无s56补料</span>
                    <span class="feed-status">9/22 下签 · Tier 1 兑现</span>
                </div>
            </div>
            <div class="feed-row">
                <div>
                    <span class="feed-occ">厨师 (Chef - TSE快速通道)</span>
                    <span class="feed-sub">TAS 境内 190 · 2026-01-28 递交</span>
                </div>
                <div>
                    <span class="feed-status">9/21 下签 · 历时7.8个月(吻合25%前沿)</span>
                </div>
            </div>
            <div class="feed-row">
                <div>
                    <span class="feed-occ">计算机网络系统工程师 (Network Engineer)</span>
                    <span class="feed-sub">NSW 境外 190 · 2025-04-10 递交</span>
                </div>
                <div>
                    <span class="feed-status">9/21 下签 · 历时17.4个月(境外非优先)</span>
                </div>
            </div>
            <div class="feed-row">
                <div>
                    <span class="feed-occ">中学教师 (Secondary Teacher)</span>
                    <span class="feed-sub">SA 境外 190 · 2025-11-23 递交</span>
                </div>
                <div>
                    <span class="feed-status">9/21 下签 · Tier 1 教师批次</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Checklist Accordion -->
    <section class="panel">
        <div class="panel-header">
            <h2 class="panel-title">审理前置准备与注意事项</h2>
        </div>
        <div class="acc-item">
            <div class="acc-trigger" data-acc="1">
                <span>1. 体检 (Medicals) 即将满 1 年是否需要主动重做？</span>
                <span class="acc-arrow">＋</span>
            </div>
            <div class="acc-body">
                不建议提前盲目重做。体检有效期为12个月。如果审到你的案子时体检过期，签证官会下发 s56 补料通知并给予 28 天窗口。收到正式通知后再预约体检，可避免白白产生二次费用。
            </div>
        </div>
        <div class="acc-item">
            <div class="acc-trigger" data-acc="2">
                <span>2. 澳洲 AFP 与国内无犯罪证明的有效期准备</span>
                <span class="acc-arrow">＋</span>
            </div>
            <div class="acc-body">
                澳洲联邦警局无犯罪证明 (AFP) 办理周期通常为 1-3 个工作日；国内公证大约需 1-2 周。建议在预估批签节点前 1-2 个月检查有效期即可。
            </div>
        </div>
        <div class="acc-item">
            <div class="acc-trigger" data-acc="3">
                <span>3. 搬家、换护照或变更邮箱的申报流程</span>
                <span class="acc-arrow">＋</span>
            </div>
            <div class="acc-body">
                请在 ImmiAccount 个人后台直接提交 Form 929（Update details），确保签证官发出的 s56 补料通知或获批准迁信能及时送达。
            </div>
        </div>
        <div class="acc-item">
            <div class="acc-trigger" data-acc="4">
                <span>4. 移民局批签发信时间习惯与查询频率</span>
                <span class="acc-arrow">＋</span>
            </div>
            <div class="acc-body">
                移民局通常在澳洲东部时间工作日上午9点至下午4点之间集中派发批签信。在无补料要求或个人信息变更的情况下，无需频繁刷新 ImmiAccount，避免触发系统安全验证锁定。
            </div>
        </div>
    </section>

    <!-- Global 25-Month Table Accordion -->
    <section class="panel">
        <div class="acc-trigger" id="full-table-trigger" style="font-size:15px;">
            <span>📊 展开 25个月 × 4模式 全局预测对照总表</span>
            <span id="table-arrow">＋</span>
        </div>
        <div class="acc-body" id="full-table-content" style="display:none;margin-top:14px;">
            <div class="table-toolbar">
                <span style="font-size:12px;font-weight:600;color:var(--text);">切换推演模式：</span>
                <div class="table-mode-tabs">
                    <button class="table-tab-btn active" data-mode="m2">模式 2 · 双目标提速 (实测推荐)</button>
                    <button class="table-tab-btn" data-mode="m1">模式 1 · 128人基准</button>
                    <button class="table-tab-btn" data-mode="m3">模式 3 · T3单人优先</button>
                    <button class="table-tab-btn" data-mode="m4">模式 4 · 单通道 (已失效)</button>
                </div>
            </div>
            <div class="table-mode-hint" id="table-mode-hint">
                当前展示：<strong>【模式 2 · 双目标提速】</strong> 境内94+境外40人/日，双轨独立全速推进（与9.21~9.22官方审批实测吻合度最高）。
            </div>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>Lodged 月份</th>
                            <th>Tier 1 优先</th>
                            <th>Tier 2 境内</th>
                            <th>Tier 3 境外单人</th>
                            <th>Tier 4 境外带副申</th>
                        </tr>
                    </thead>
                    <tbody id="full-table-body">
                        <!-- Filled by JS -->
                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <!-- Action Buttons -->
    <div class="action-row">
        <button class="btn-primary" id="btn-share">查看 / 复制我的批签预测结论</button>
        <button class="btn-outline" id="btn-reset">重置为默认条件</button>
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
                <button class="btn-primary" id="modal-ok-btn">我知道了</button>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="app-footer">
        <p>数据基准：澳洲内政部 FOI 官方底盘数据 (P+S 24,196人) ｜ 实施政策：MD122 Ministerial Direction</p>
        <p>所有预测均基于历史消耗均速与配额数学模型情景测算，仅供移民规划与排期进度参考，不构成官方审批时限承诺。</p>
    </footer>

</div>

<script src="./app.js"></script>
</body>
</html>
'''

with open(DIST_DIR / 'index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# 4. Build app.js
js_content = f'''// --- EMBEDDED FORECAST DATA ---
var DATA = {json_data_str};

var months = DATA.months;
var today = new Date(2026, 8, 23); // Current baseline: 2026-09-23 (SmartVisaGuide #17784)

// Initialize Dropdown
function initSelect() {{
    var select = document.getElementById('lodged-select');
    if (!select) return;
    months.forEach(function(m, idx) {{
        var opt = document.createElement('option');
        opt.value = idx;
        opt.textContent = m.indexOf('<=') === 0 ? '2025年06月及以前 (旧案积压)' : m.replace('-', '年') + '月';
        if (m === '2026-01') opt.selected = true;
        select.appendChild(opt);
    }});
}}

// Determine Tier
function getTier(location, occ, family) {{
    if (occ === 'priority') return 1;
    if (location === 'onshore') return 2;
    if (family === 'single') return 3;
    return 4;
}}

// Parse string to Date
function parseDate(dateStr) {{
    if (!dateStr || dateStr === '-') return null;
    var p = dateStr.split('-');
    return new Date(parseInt(p[0], 10), parseInt(p[1], 10) - 1, parseInt(p[2], 10));
}}

// Working Days Count
function countWorkdays(start, end) {{
    if (start >= end) return 0;
    var count = 0;
    var cur = new Date(start.getTime());
    while (cur < end) {{
        cur.setDate(cur.getDate() + 1);
        var day = cur.getDay();
        if (day !== 0 && day !== 6) count++;
    }}
    return count;
}}

function subtractWorkdays(startDate, numDays) {{
    var d = new Date(startDate.getTime());
    var counted = 0;
    while (counted < numDays) {{
        d.setDate(d.getDate() - 1);
        var day = d.getDay();
        if (day !== 0 && day !== 6) counted++;
    }}
    return d;
}}

function formatDateStr(d) {{
    var y = d.getFullYear();
    var m = String(d.getMonth() + 1).padStart(2, '0');
    var day = String(d.getDate()).padStart(2, '0');
    return y + '-' + m + '-' + day;
}}

// Main Calculation
function calculateForecast() {{
    var selectEl = document.getElementById('lodged-select');
    if (!selectEl) return;
    var mIdx = parseInt(selectEl.value, 10);
    var locChecked = document.querySelector('input[name="location"]:checked');
    var occChecked = document.querySelector('input[name="occupation"]:checked');
    var famChecked = document.querySelector('input[name="family"]:checked');

    var location = locChecked ? locChecked.value : 'onshore';
    var occ = occChecked ? occChecked.value : 'non-priority';
    var family = famChecked ? famChecked.value : 'single';

    var tier = getTier(location, occ, family);
    updateTierStrip(tier);

    var monthLabel = months[mIdx];
    var isClearedT2 = (tier === 2 && mIdx < 7);

    var m1_info = DATA.m1[tier][mIdx];
    var m2_info = DATA.m2[tier][mIdx];
    var m3_info = DATA.m3[tier][mIdx];
    var m4_info = DATA.m4[tier][mIdx];

    var m1_date = m1_info ? m1_info.date : '-';
    var m2_date = m2_info ? m2_info.date : '-';
    var m3_date = m3_info ? m3_info.date : '-';
    var m4_date = m4_info ? m4_info.date : '-';

    document.getElementById('m1-date').textContent = isClearedT2 ? 'MD119已完成' : m1_date;
    document.getElementById('m2-date').textContent = isClearedT2 ? 'MD119已完成' : m2_date;
    document.getElementById('m3-date').textContent = isClearedT2 ? 'MD119已完成' : m3_date;
    document.getElementById('m4-date').textContent = isClearedT2 ? 'MD119已完成' : m4_date;

    var grantDisplay = document.getElementById('grant-date-display');
    var daysEl = document.getElementById('days-remaining');
    var workdaysEl = document.getElementById('workdays-remaining');
    var fyEl = document.getElementById('fy-label');
    var barEl = document.getElementById('progress-bar');
    var badgeEl = document.getElementById('progress-badge');
    var pctTextEl = document.getElementById('progress-pct-text');
    var labelStart = document.getElementById('label-start');
    var labelEnd = document.getElementById('label-end');
    var dgCard = document.getElementById('direct-grant-card');
    var dgText = document.getElementById('dg-text');

    // Parse applicant lodgement date
    var lDate;
    if (monthLabel.indexOf('<=') === 0) {{
        lDate = new Date(2025, 4, 1);
        labelStart.textContent = '递交申请 (≤2025-06)';
    }} else {{
        var parts = monthLabel.split('-');
        lDate = new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, 1);
        labelStart.textContent = '递交申请 (' + monthLabel + ')';
    }}

    if (isClearedT2) {{
        grantDisplay.textContent = 'MD119 阶段已审理完成';
        grantDisplay.className = 'hero-date cleared';
        daysEl.textContent = '0 天 (在池中)';
        workdaysEl.textContent = '等待系统发信';
        fyEl.textContent = 'FY27 境内';

        barEl.style.width = '100%';
        barEl.className = 'progress-bar complete';
        badgeEl.className = 'progress-badge complete';
        pctTextEl.textContent = '已完成 100%';
        labelEnd.textContent = '审理完毕 (池中待信)';

        dgCard.style.display = 'none';
    }} else if (m2_date && m2_date !== '-') {{
        grantDisplay.textContent = m2_date;
        grantDisplay.className = 'hero-date';

        var gDate = parseDate(m2_date);
        var diffTime = gDate - today;
        var diffDays = Math.max(0, Math.ceil(diffTime / (1000 * 60 * 60 * 24)));
        var workdays = countWorkdays(today, gDate);

        daysEl.textContent = diffDays + ' 天';
        workdaysEl.textContent = workdays + ' 个工作日';
        fyEl.textContent = m2_info.fy + (tier === 1 ? (location === 'onshore' ? ' 境内' : ' 境外') : (tier === 2 ? ' 境内' : ' 境外'));

        var totalSpan = gDate.getTime() - lDate.getTime();
        var elapsed = Math.max(0, today.getTime() - lDate.getTime());
        var pct = Math.round((elapsed / totalSpan) * 100);
        pct = Math.max(8, Math.min(99, pct));

        barEl.style.width = pct + '%';
        if (pct >= 90) {{
            barEl.className = 'progress-bar complete';
            badgeEl.className = 'progress-badge complete';
            pctTextEl.textContent = '临近获批 · 已完成 ' + pct + '%';
        }} else {{
            barEl.className = 'progress-bar';
            badgeEl.className = 'progress-badge';
            pctTextEl.textContent = '排期已完成 ' + pct + '%';
        }}

        labelEnd.textContent = '预计获批 (' + m2_date + ')';

        // Direct Grant Window
        dgCard.style.display = 'flex';
        if (gDate <= today) {{
            dgText.innerHTML = '该月份已整体处于<strong>官方批签实盘验证窗口</strong>。近期 9.21~9.23 密集出现的多例直签（如 2025年9月电工直签、11月土木直签、2026年4月急诊护士）即印证了先锋放量。';
        }} else {{
            var earlyD = subtractWorkdays(gDate, 7);
            var lateD = subtractWorkdays(gDate, 3);
            var earlyStr = formatDateStr(earlyD);
            var lateStr = formatDateStr(lateD);
            var note = '';
            if (tier === 1) {{
                note = '<br><span style="color:#D97706;font-size:11px;font-weight:600;">🩺 极速通道提示：若属于医疗护理或教师类急需职业，据 SmartVisaGuide 官方最新数据，中位数获批仅需 3.7 ~ 5.2 个月（实测 2026-04 护士已于 9.23 获批），实际获批预计将显著早于基准排期！</span>';
            }}
            dgText.innerHTML = '免补料直签 (Direct Grant) 先锋窗口：若材料齐全无需s56补料，预计可提前至 <strong class="dg-date-highlight">' + earlyStr + ' ~ ' + lateStr + '</strong> 率先突围下签！' + note;
        }}
    }} else {{
        grantDisplay.textContent = '待排期';
        daysEl.textContent = '-';
        workdaysEl.textContent = '-';
        fyEl.textContent = '-';
        barEl.style.width = '10%';
        barEl.className = 'progress-bar';
        badgeEl.className = 'progress-badge';
        pctTextEl.textContent = '排期中 10%';
        labelEnd.textContent = '预计获批';

        dgCard.style.display = 'none';
    }}

    updateBlessingMsg(tier, isClearedT2);
}}

function updateTierStrip(tier) {{
    var strip = document.getElementById('tier-strip');
    var tag = document.getElementById('tier-tag');
    var name = document.getElementById('tier-name');
    var cap = document.getElementById('tier-caption');
    if (!strip) return;

    strip.className = 'tier-strip t' + tier;
    tag.className = 'tier-tag t' + tier;
    tag.textContent = 'Tier ' + tier;

    if (tier === 1) {{
        name.textContent = '全球优先职业赛道 (Tier 1)';
        cap.textContent = '无论境内或境外，优先职业均列为第一优先级，当前正全速集中清理。';
    }} else if (tier === 2) {{
        name.textContent = '境内非优先职业赛道 (Tier 2)';
        cap.textContent = '澳洲境内非优先通道，占用境内独立流水线（~94人/日），大盘扎实平稳。';
    }} else if (tier === 3) {{
        name.textContent = '境外单人非优先赛道 (Tier 3)';
        cap.textContent = '境外单人申请（无副申配额负担），优先级高于带副申，大幅提前出签。';
    }} else {{
        name.textContent = '境外带副申非优先赛道 (Tier 4)';
        cap.textContent = '境外家庭类申请，顺次消化，模型测算2027年上半年配额依然有席位。';
    }}
}}

function updateBlessingMsg(tier, isClearedT2) {{
    var el = document.getElementById('blessing-msg');
    if (!el) return;
    var text = '';
    if (isClearedT2) {{
        text = '<strong>官方流水线已全部审毕。</strong> 你的递交批次在 MD119 阶段已经全额推平。若目前暂未收信，大多属于材料最终复核、体检补办或系统发信排队。请保持电话与邮箱畅通，静候好消息。';
    }} else if (tier === 1) {{
        text = '<strong>优先职业正处全速放量期。</strong> 9.21~9.23 境内外优先（急诊护士、电工直签、土木直签、项目经理、教师）连续密集放量，无补料个案与医疗急需案加速领跑。你的材料正处在最高优先通道，胜利近在咫尺，安心做好生活与登陆规划。';
    }} else if (tier === 2) {{
        text = '<strong>境内基本盘极其稳固。</strong> 境内年配额高达 24,850 人，流水线每天稳定吞吐近百人，9.21~9.23 连续出现 1月下旬递交的下签（如Chef等），旧案补料后也迅速出清。你的排队序号非常靠前，节奏健康，安心享受在澳工作与生活。';
    }} else if (tier === 3) {{
        text = '<strong>单人赛道迎来制度红利。</strong> MD122 设立 Tier 3 让你彻底脱离了家庭案的副申人头挤占，占用配额极少。在 11 月中下旬境外优先清空后将迎来加速放量，好饭不怕晚，属于你的高光就在眼前。';
    }} else {{
        text = '<strong>家庭同行是长远的依靠。</strong> 虽因副申人头拉长了整体消化周期，但客观数据粉碎了“无限期搁置”的恐慌谣言——2027上半年配额依然有充裕席位。稳住心态，全家顺利登陆那一刻，一切等待都将值得。';
    }}
    el.innerHTML = text;
}}

// --- INLINE CANVAS CONFETTI (NO EXTERNAL SCRIPT) ---
function runInlineConfetti() {{
    var canvas = document.getElementById('confetti-canvas');
    if (!canvas) {{
        canvas = document.createElement('canvas');
        canvas.id = 'confetti-canvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '9999';
        document.body.appendChild(canvas);
    }}
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    var ctx = canvas.getContext('2d');
    var colors = ['#16A34A', '#2563EB', '#D97706', '#9333EA', '#059669', '#E11D48', '#FFD700'];
    var particles = [];
    for (var i = 0; i < 90; i++) {{
        particles.push({{
            x: window.innerWidth * (0.3 + Math.random() * 0.4),
            y: window.innerHeight * 0.55,
            vx: (Math.random() - 0.5) * 16,
            vy: -Math.random() * 18 - 8,
            size: Math.random() * 8 + 4,
            color: colors[Math.floor(Math.random() * colors.length)],
            rotation: Math.random() * 360,
            rSpeed: (Math.random() - 0.5) * 12,
            gravity: 0.55,
            life: 1.0,
            decay: 0.012 + Math.random() * 0.008
        }});
    }}

    var animId;
    function frame() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        var alive = false;
        particles.forEach(function(p) {{
            p.x += p.vx;
            p.y += p.vy;
            p.vy += p.gravity;
            p.rotation += p.rSpeed;
            p.life -= p.decay;
            if (p.life > 0) {{
                alive = true;
                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate((p.rotation * Math.PI) / 180);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = Math.max(0, p.life);
                ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
                ctx.restore();
            }}
        }});
        if (alive) {{
            animId = requestAnimationFrame(frame);
        }} else {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }}
    }}
    frame();
}}

// Koi Blessings
var koiBlessings = [
    "🎉 锦鲤显灵！测算显示你的案子排期稳步推进，材料齐全直签先锋窗口已打开，祝你免s56直接下签！",
    "✨ 鸿运当头！你的排期节点平稳可期，获批就在前方，心态放平！",
    "🐟 好事花生！大吉大利，签证官正有序审理，期待你的获批通知！",
    "🌈 愿望送达！生活大于签证，专注当下每一天，顺风顺水必拿PR！",
    "🍀 锦鲤护体！坚持终有回响，祝你与家人如期顺利登陆澳洲！"
];

function triggerKoiBlessing() {{
    runInlineConfetti();
    var fb = document.getElementById('koi-feedback');
    var b = koiBlessings[Math.floor(Math.random() * koiBlessings.length)];
    fb.textContent = b;
    fb.className = 'koi-feedback visible';
}}

// 25-Month Table Logic
var currentTableMode = 'm2';

var tableModeHints = {{
    'm2': '当前展示：<strong>【模式 2 · 双目标提速】</strong> 境内94+境外40人/日，双轨独立全速推进（与9.21~9.23官方审批实测吻合度最高）。',
    'm1': '当前展示：<strong>【模式 1 · 固定基准】</strong> 128人/日固定速度（不借调配额，节奏较保守，全财年略有1,198人未消化）。',
    'm3': '当前展示：<strong>【模式 3 · T3优先并行】</strong> 境外单人优先分得64%配额，与T4家庭类并行消化。',
    'm4': '当前展示：<strong>【模式 4 · 单通道顺延】</strong> 假定境内全清才轮到境外（实盘已大面积下签境外，此模式已落空被证伪）。'
}};

function switchTableMode(modeKey, btn) {{
    currentTableMode = modeKey;
    document.querySelectorAll('.table-tab-btn').forEach(function(b) {{ b.classList.remove('active'); }});
    if (btn) btn.classList.add('active');

    var hintEl = document.getElementById('table-mode-hint');
    if (hintEl && tableModeHints[modeKey]) {{
        hintEl.innerHTML = tableModeHints[modeKey];
    }}
    renderFullTable(modeKey);
}}

function renderFullTable(modeKey) {{
    var tbody = document.getElementById('full-table-body');
    if (!tbody) return;
    tbody.innerHTML = '';

    var modeData = DATA[modeKey] || DATA.m2;

    months.forEach(function(m, idx) {{
        var tr = document.createElement('tr');
        var t1_d = modeData['1'] && modeData['1'][idx] ? modeData['1'][idx].date : '-';
        var t2_d = idx < 7 ? '<span style="color:#059669;font-weight:600">MD119已完成</span>' : (modeData['2'] && modeData['2'][idx] ? modeData['2'][idx].date : '-');
        var t3_d = modeData['3'] && modeData['3'][idx] ? modeData['3'][idx].date : '-';
        var t4_d = modeData['4'] && modeData['4'][idx] ? modeData['4'][idx].date : '-';

        tr.innerHTML = '<td>' + m + '</td>' +
            '<td style="color:var(--t1)">' + t1_d + '</td>' +
            '<td style="color:var(--t2)">' + t2_d + '</td>' +
            '<td style="color:var(--t3)">' + t3_d + '</td>' +
            '<td style="color:var(--t4)">' + t4_d + '</td>';
        tbody.appendChild(tr);
    }});
}}

// Share Modal Controller (Compliant with container: no navigator.clipboard)
function openShareModal() {{
    var month = document.getElementById('lodged-select').selectedOptions[0].text;
    var tier = document.getElementById('tier-name').textContent;
    var date = document.getElementById('grant-date-display').textContent;
    var days = document.getElementById('days-remaining').textContent;

    var text = '【澳洲190 MD122批签预测】\\n' +
        '递交月份：' + month + '\\n' +
        '所属赛道：' + tier + '\\n' +
        '预计获批：' + date + ' (距今约' + days + ')\\n' +
        '测算基准：FOI官方24,196人底盘与MD122四Tier模型\\n' +
        '仅供排期参考，祝早日下签！';

    var modal = document.getElementById('share-modal');
    var txtArea = document.getElementById('share-text-area');
    if (modal && txtArea) {{
        txtArea.value = text;
        modal.style.display = 'flex';
        txtArea.focus();
        txtArea.select();
    }}
}}

function closeShareModal() {{
    var modal = document.getElementById('share-modal');
    if (modal) modal.style.display = 'none';
}}

// Reset inputs to default
function resetDefaults() {{
    var select = document.getElementById('lodged-select');
    if (select) select.value = '7'; // 2026-01
    var rLoc = document.getElementById('loc-onshore');
    if (rLoc) rLoc.checked = true;
    var rOcc = document.getElementById('occ-non-priority');
    if (rOcc) rOcc.checked = true;
    var rFam = document.getElementById('fam-single');
    if (rFam) rFam.checked = true;
    calculateForecast();
}}

// --- BIND ALL EVENT LISTENERS (NO INLINE ON* PER CONTAINER CSP) ---
window.addEventListener('DOMContentLoaded', function() {{
    initSelect();
    calculateForecast();

    // Select change
    var selectEl = document.getElementById('lodged-select');
    if (selectEl) {{
        selectEl.addEventListener('change', calculateForecast);
    }}

    // Radios change
    var radios = document.querySelectorAll('input[type="radio"]');
    radios.forEach(function(r) {{
        r.addEventListener('change', calculateForecast);
    }});

    // Koi button
    var btnKoi = document.getElementById('btn-koi');
    if (btnKoi) {{
        btnKoi.addEventListener('click', triggerKoiBlessing);
    }}

    // Accordions
    var accTriggers = document.querySelectorAll('.acc-trigger[data-acc]');
    accTriggers.forEach(function(trigger) {{
        trigger.addEventListener('click', function() {{
            var body = this.nextElementSibling;
            var arrow = this.querySelector('.acc-arrow');
            var isOpen = body.style.display === 'block';
            body.style.display = isOpen ? 'none' : 'block';
            if (arrow) arrow.textContent = isOpen ? '＋' : '－';
        }});
    }});

    // Full table accordion
    var fullTableTrigger = document.getElementById('full-table-trigger');
    if (fullTableTrigger) {{
        fullTableTrigger.addEventListener('click', function() {{
            var body = document.getElementById('full-table-content');
            var arrow = document.getElementById('table-arrow');
            var isOpen = body.style.display === 'block';
            body.style.display = isOpen ? 'none' : 'block';
            if (arrow) arrow.textContent = isOpen ? '＋' : '－';
            if (!isOpen && !document.getElementById('full-table-body').children.length) {{
                renderFullTable(currentTableMode);
            }}
        }});
    }}

    // Table mode tabs
    var tableTabs = document.querySelectorAll('.table-tab-btn');
    tableTabs.forEach(function(tab) {{
        tab.addEventListener('click', function() {{
            var mode = this.getAttribute('data-mode');
            switchTableMode(mode, this);
        }});
    }});

    // Action buttons
    var btnShare = document.getElementById('btn-share');
    if (btnShare) {{
        btnShare.addEventListener('click', openShareModal);
    }}

    var btnReset = document.getElementById('btn-reset');
    if (btnReset) {{
        btnReset.addEventListener('click', resetDefaults);
    }}

    // Modal close buttons
    var modalClose = document.getElementById('modal-close-btn');
    if (modalClose) {{
        modalClose.addEventListener('click', closeShareModal);
    }}

    var modalOk = document.getElementById('modal-ok-btn');
    if (modalOk) {{
        modalOk.addEventListener('click', closeShareModal);
    }}

    var modalOverlay = document.getElementById('share-modal');
    if (modalOverlay) {{
        modalOverlay.addEventListener('click', function(e) {{
            if (e.target === modalOverlay) closeShareModal();
        }});
    }}
}});
'''

with open(DIST_DIR / 'app.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("[build_minitool] Files generated in:", DIST_DIR)

# 5. Create 190-grant-predictor-minitool.zip
print("[build_minitool] Packing zip archive:", ZIP_PATH)
with zipfile.ZipFile(ZIP_PATH, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for item in sorted(DIST_DIR.rglob('*')):
        if item.is_file() and not item.name.startswith('.') and '__MACOSX' not in item.parts:
            arcname = item.relative_to(DIST_DIR).as_posix()
            zf.write(item, arcname)

print(f"[build_minitool] Zip created successfully: {ZIP_PATH.stat().st_size} bytes")

# 6. Audit artifact
audit_script = SCRIPT_DIR / 'audit_artifact.py'
if audit_script.exists():
    ret = subprocess.run([sys.executable, str(audit_script), str(ZIP_PATH)], capture_output=True, text=True)
    print("[build_minitool] Audit output:")
    print(ret.stdout.strip())
    if ret.returncode != 0:
        print("[build_minitool] Audit FAILED:\n", ret.stderr.strip())
        sys.exit(ret.returncode)
else:
    print("[build_minitool] audit_artifact.py not found, skipping audit.")

