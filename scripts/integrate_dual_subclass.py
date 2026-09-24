import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('Original file length:', len(html))

# 1. Update CSS
css_needle = '/* Visa Subclass Nav Switcher */'
if css_needle not in html:
    # Insert right before </style>
    style_end = html.find('</style>')
    switcher_css = """
        /* Visa Subclass Nav Switcher */
        .subclass-nav-wrapper {
            display: flex;
            justify-content: center;
            margin-bottom: 24px;
        }

        .subclass-switcher {
            display: inline-flex;
            background: #E2E8F0;
            padding: 4px;
            border-radius: 14px;
            gap: 6px;
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.06);
            width: 100%;
            max-width: 580px;
        }

        .subclass-tab {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 10px 18px;
            border: none;
            border-radius: 10px;
            background: transparent;
            color: var(--text-secondary);
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            white-space: nowrap;
        }

        .subclass-tab:hover {
            color: var(--text);
        }

        .subclass-tab.active {
            background: #FFFFFF;
            color: var(--text);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04);
        }

        .subclass-tab .tab-badge {
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 800;
            background: var(--surface-muted);
            color: var(--text-muted);
            transition: all 0.2s ease;
        }

        .subclass-tab.active#tab-190 .tab-badge {
            background: var(--accent);
            color: #FFFFFF;
        }

        .subclass-tab.active#tab-491 .tab-badge {
            background: #D97706; /* Amber for regional 491 */
            color: #FFFFFF;
        }

        /* Quota Exhaustion Warning Card on Hero */
        .quota-warning-banner {
            display: none;
            margin-top: 14px;
            padding: 14px 18px;
            background: #FFFBEB;
            border: 1px solid #FDE68A;
            border-radius: var(--radius-md);
            font-size: 13px;
            color: #92400E;
            line-height: 1.6;
            align-items: flex-start;
            gap: 12px;
        }

        .quota-warning-banner.visible {
            display: flex;
        }

        .quota-warning-icon {
            font-size: 18px;
            line-height: 1;
            flex-shrink: 0;
            margin-top: 2px;
        }

        @media (max-width: 640px) {
            .subclass-tab {
                padding: 8px 10px;
                font-size: 13px;
                gap: 6px;
            }
            .subclass-tab .tab-badge {
                font-size: 10px;
                padding: 1px 5px;
            }
        }
    """
    html = html[:style_end] + switcher_css + '\n' + html[style_end:]
    print('Added CSS for switcher and quota warning.')

# 2. Update Header HTML with Switcher and IDs
header_pattern = r'<header class="app-header">[\s\S]*?</header>'
new_header = """<header class="app-header">
        <!-- Subclass Switcher Tabs -->
        <div class="subclass-nav-wrapper">
            <div class="subclass-switcher" role="tablist" aria-label="签证类别切换">
                <button type="button" class="subclass-tab active" id="tab-190" role="tab" aria-selected="true" onclick="switchSubclass('190')">
                    <span>Subclass 190 州担保技术移民</span>
                    <span class="tab-badge">永居 PR</span>
                </button>
                <button type="button" class="subclass-tab" id="tab-491" role="tab" aria-selected="false" onclick="switchSubclass('491')">
                    <span>Subclass 491 偏远地区州担/亲属</span>
                    <span class="tab-badge">准永居 TR</span>
                </button>
            </div>
        </div>

        <div class="meta-tags">
            <span class="status-pill" id="meta-calibration"><span class="status-dot"></span>9月24日实盘校准完成 · 吻合度>96%</span>
            <span class="info-pill" id="meta-backlog">FOI 24,196人唯一人头底盘</span>
            <span class="info-pill" id="meta-md">MD122 官方四Tier体系</span>
            <span class="info-pill" id="meta-speed" style="color:var(--accent);border-color:var(--accent-border);background:var(--accent-light);">实测确证：境内外双轨并行</span>
        </div>
        <h1 class="app-title" id="app-title">澳洲 190 · MD122 智能批签预测</h1>
        <p class="app-desc" id="app-desc">
            基于内政部官方底盘数据与最新部长令执行节奏，输入递交月份与申请人属性，即刻测算批签窗口与多模式推演。
        </p>
    </header>"""

html = re.sub(header_pattern, new_header, html, count=1)
print('Updated Header HTML.')

# 3. Update Hero section with hero-mode-chip, dg-badge, and quota-warning-banner
hero_pattern = r'(<span class="hero-label">预计批签下签时间</span>\s*<span class="mode-chip">)[^<]+(</span>)'
html = re.sub(hero_pattern, r'\1<span id="hero-mode-chip">推荐模式 2 · 官方双目标兑现</span>\2', html)

if 'id="hero-mode-chip"' not in html:
    html = html.replace('<span class="mode-chip">推荐模式 2 · 官方双目标兑现</span>', '<span class="mode-chip" id="hero-mode-chip">推荐模式 2 · 官方双目标兑现</span>')

if 'id="dg-badge"' not in html:
    html = html.replace('<span class="dg-badge">⚡ 免补料直签先锋窗口</span>', '<span class="dg-badge" id="dg-badge">⚡ 免补料直签先锋窗口</span>')

if 'id="quota-warning-banner"' not in html:
    target_pos = html.find('id="direct-grant-card"')
    if target_pos != -1:
        card_end = html.find('</div>', target_pos) + 6
        quota_banner_html = """

        <!-- Quota Warning Banner for 491 Offshore -->
        <div class="quota-warning-banner" id="quota-warning-banner">
            <span class="quota-warning-icon">⚠️</span>
            <div>
                <strong>491 境外本财年配额耗尽熔断预警：</strong>
                由于 FY27 偏远地区总配额大幅腰斩 (-57.2%)，境外普通赛道预计在推进至 2026年4月递交时打满全财年 10,912 人配额上限。该批次预计需顺延至 <strong>FY28 新财年 (2027年7月后)</strong> 启动审理下签。
            </div>
        </div>"""
        html = html[:card_end] + quota_banner_html + html[card_end:]
        print('Inserted quota-warning-banner into Hero Panel.')

# 4. Add IDs to Tracker and Feed Rows
if 'id="tracker-grid"' not in html:
    html = html.replace('<div class="tracker-grid">', '<div class="tracker-grid" id="tracker-grid">')
if 'id="feed-rows"' not in html:
    html = html.replace('<div class="feed-rows">', '<div class="feed-rows" id="feed-rows">')
if 'id="feed-panel-title"' not in html:
    html = html.replace('<h2 class="panel-title">9月21日 ~ 9月24日 实盘批签追踪实录 (SmartVisaGuide)</h2>', '<h2 class="panel-title" id="feed-panel-title">9月21日 ~ 9月24日 实盘批签追踪实录 (SmartVisaGuide)</h2>')

# 5. Check JS switchSubclass function and enhance it
# Let's inspect switchSubclass in the file and replace it with a comprehensive robust version
js_switch_needle = 'function switchSubclass(sc) {'
js_switch_end = 'function getCurrentData() {'

new_switch_subclass = """function switchSubclass(sc) {
    if (currentSubclass === sc) return;
    currentSubclass = sc;

    // 1. Update Tab Styles
    const tab190 = document.getElementById('tab-190');
    const tab491 = document.getElementById('tab-491');
    if (tab190) {
        tab190.classList.toggle('active', sc === '190');
        tab190.setAttribute('aria-selected', sc === '190');
    }
    if (tab491) {
        tab491.classList.toggle('active', sc === '491');
        tab491.setAttribute('aria-selected', sc === '491');
    }

    // 2. Update Titles, Meta, and Labels
    const titleEl = document.getElementById('app-title');
    const descEl = document.getElementById('app-desc');
    const calEl = document.getElementById('meta-calibration');
    const backlogEl = document.getElementById('meta-backlog');
    const mdEl = document.getElementById('meta-md');
    const speedEl = document.getElementById('meta-speed');
    const heroModeChip = document.getElementById('hero-mode-chip');
    const dgText = document.getElementById('dg-text');
    const dsEl = document.getElementById('tracker-datasource');
    const trackerGrid = document.getElementById('tracker-grid');
    const feedTitle = document.getElementById('feed-panel-title');
    const feedRows = document.getElementById('feed-rows');
    const footerEl = document.getElementById('footer-data-baseline');
    const aiInsightEl = document.getElementById('ai-insight-text');

    // Mode Card Headers
    const m1Title = document.getElementById('m1-title');
    const m1Desc = document.getElementById('m1-desc');
    const m2Title = document.getElementById('m2-title');
    const m2Desc = document.getElementById('m2-desc');
    const m3Title = document.getElementById('m3-title');
    const m3Desc = document.getElementById('m3-desc');
    const m4Title = document.getElementById('m4-title');
    const m4Desc = document.getElementById('m4-desc');

    if (sc === '190') {
        if (titleEl) titleEl.textContent = '澳洲 190 · MD122 智能批签预测';
        if (descEl) descEl.textContent = '基于内政部官方底盘数据与最新部长令执行节奏，输入递交月份与申请人属性，即刻测算批签窗口与多模式推演。';
        if (calEl) calEl.innerHTML = '<span class="status-dot"></span>9月24日实盘校准完成 · 吻合度>96%';
        if (backlogEl) backlogEl.textContent = 'FOI 24,196人唯一人头底盘';
        if (mdEl) mdEl.textContent = 'MD122 官方四Tier体系';
        if (speedEl) speedEl.textContent = '实测确证：境内外双轨并行 (日均128人)';
        if (heroModeChip) heroModeChip.textContent = '推荐模式 2 · 官方双目标兑现';
        if (dgText) dgText.textContent = '若材料齐全无 s56 补料，预计可提前 3~7 个工作日率先突围下签！';
        if (dsEl) dsEl.textContent = '数据源：SmartVisaGuide Database & 官方 Subclass 190 宏观大盘';
        if (footerEl) footerEl.textContent = '数据基准：澳洲内政部 FOI 官方底盘数据 (P+S 24,196人) ｜ 实施政策：MD122 Ministerial Direction';

        if (m2Title) m2Title.textContent = '双目标兑现 · 提速';
        if (m2Desc) m2Desc.textContent = '境内94+境外40人/日。实测印证：双轨独立全速推进，打满全财年35,500总配额。';
        if (m1Title) m1Title.textContent = '128人/日 · 固定基准';
        if (m1Desc) m1Desc.textContent = '固定产能不借调，节奏较保守，全财年略有1,198人未消化。';
        if (m3Title) m3Title.textContent = 'T3单人优先并行';
        if (m3Desc) m3Desc.textContent = '境外单人分得64%产能。当前实盘以T1冲刺为主，此模式作中远期参考。';
        if (m4Title) m4Title.textContent = '单通道顺序 (已失效)';
        if (m4Desc) m4Desc.textContent = '假定境内全清才轮到境外。实盘显示境外已大面积下签，此倒退模式彻底失效。';

        if (aiInsightEl) {
            aiInsightEl.innerHTML = `<p><strong>【审理格局定论】</strong>官方三大队列审理中位数（优先 <strong>7.2个月</strong> / 境内普通 <strong>9.2个月</strong> / 境外普通 <strong>15.9个月</strong>）持续紧密契合<strong>模式 2 (双目标提速模型)</strong>，实测吻合度达 <strong>>96%</strong>。</p>
<p><strong>【今日重磅异动洞察 (9月24日)】</strong><br>
① 💻 <strong>境内 IT 普工破冰</strong>：维州 190 境内软件工程师 (2026-01-29 递交·100分) 仅 <strong>7.8 个月 (236天)</strong> 免补料直签，境内普通工种正式突围进入 2026 年 1 月底，大盘中位数缩短至 <strong>9.2 个月</strong>！<br>
② 🏗️ <strong>境外紧缺基建飞速推进</strong>：维州境外土木工程师 (2026-02-13 递交) 与昆州境外 CPM (2026-01-27 递交) 耗时仅 <strong>7.3 ~ 7.9 个月</strong>，MD122 基建优先在境外全面提速！<br>
③ 🩺 <strong>医疗极速前锋提速</strong>：南澳境外精神科护士 <strong>7.3 个月</strong> 下签，官方 25% 极速前锋进一步压缩至创纪录的 <strong>3.5 个月</strong>！<br>
④ 🔄 <strong>s56 出清顺畅</strong>：NSW 机械工程师 (2025-12-14 递交) 在重新体检后火速批签，耗时精准吻合 9.3 个月。</p>`;
        }

        if (trackerGrid) {
            trackerGrid.innerHTML = `
                <div class="tracker-col">
                    <div class="tracker-label">🌟 Priority 优先通道实测 (医疗/幼教/紧缺基建)</div>
                    <div class="tracker-val">推进至 <strong>2026-04-13</strong> (境内医疗) / <strong>2026-02-13</strong> (境外土木/护士)</div>
                    <div class="tracker-hint">
                        官方周期：<strong>25% 3.5个月 | 50% 7.2个月 | 75% 12.7个月</strong>。<br>
                        实盘：9.24 维州境外土木(2026-02-13)与南澳境外护士仅 <strong>7.3个月</strong> 秒批！25%极速位进一步压缩至 3.5 个月。
                    </div>
                </div>
                <div class="tracker-col">
                    <div class="tracker-label">🦘 Onshore 境内普通通道实测 (Tier 2/3)</div>
                    <div class="tracker-val">前沿推进至 <strong>2026-01-29</strong> (VIC软件工程师) · 补料推进至 <strong>2025-12</strong></div>
                    <div class="tracker-hint">
                        官方周期：<strong>25% 8.5个月 | 50% 9.2个月 | 75% 10.0个月 | 90% 15.1个月</strong>。<br>
                        实盘：9.24 维州境内软件工程师(100分)仅 <strong>7.8个月</strong> 免补料直签！境内中位数提速收窄至 9.2 个月。
                    </div>
                </div>
                <div class="tracker-col">
                    <div class="tracker-label">🌏 Offshore 境外普通通道实测 (Tier 4)</div>
                    <div class="tracker-val">稳步消化至 <strong>2025-04 ~ 2025-05</strong> (普通非优先)</div>
                    <div class="tracker-hint">
                        官方周期：<strong>25% 15.4个月 | 50% 15.9个月 | 75% 16.4个月 | 90% 17.1个月</strong>。<br>
                        实盘：普通非优先维持 15.9 个月控盘中位数；优先类境外基建/技工则享受独立提速通道。
                    </div>
                </div>
            `;
        }

        if (feedTitle) feedTitle.textContent = '9月21日 ~ 9月24日 实盘批签追踪实录 (SmartVisaGuide)';
        if (feedRows) {
            feedRows.innerHTML = `
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">软件工程师 (Software Engineer - 非优先普工)</span>
                        <span class="feed-sub">VIC 境内 190 · 2026-01-29 递交 (100分)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-tag-dg">⚡ 7.8个月免补料直签</span>
                        <span class="feed-status">9/24 下签 · 境内普通推进至1月底</span>
                    </div>
                </div>
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">土木工程师 (Civil Engineer - Priority)</span>
                        <span class="feed-sub">VIC 境外 190 · 2026-02-13 递交 (100分)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-tag-dg">⚡ 7.3个月秒批</span>
                        <span class="feed-status">9/24 下签 · 境外基建推进至2月中旬</span>
                    </div>
                </div>
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">精神科注册护士 (Registered Nurse - Priority)</span>
                        <span class="feed-sub">SA 境外 190 · 2026-02-11 递交 (85分)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-tag-dg">⚡ 7.3个月秒签</span>
                        <span class="feed-status">9/24 下签 · 医疗绿色通道提速</span>
                    </div>
                </div>
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">机械工程师 (Mechanical Engineer - 非优先普工)</span>
                        <span class="feed-sub">NSW 境内 190 · 2025-12-14 递交 (95分)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-status" style="background:#F1F5F9;color:#475569;border-color:#CBD5E1">9.3个月 (含s56补料)</span>
                        <span class="feed-status">9/24 下签 · 体检补办后火速获批</span>
                    </div>
                </div>
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">施工项目经理 (Construction Project Manager - Priority)</span>
                        <span class="feed-sub">QLD 境外 190 · 2026-01-27 递交 (95分)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-tag-dg">⚡ 7.9个月免补料直签</span>
                        <span class="feed-status">9/24 下签 · 基建急需优先通道</span>
                    </div>
                </div>
            `;
        }

    } else {
        // Subclass 491
        if (titleEl) titleEl.textContent = '澳洲 491 · MD122 智能批签预测';
        if (descEl) descEl.textContent = '基于内政部官方 18,364 人完整月度底盘数据与 44人/日出清模型，融合 MD122 优先级及境外配额熔断机制。';
        if (calEl) calEl.innerHTML = '<span class="status-dot"></span>9月24日实盘校准完成 · MD122适用';
        if (backlogEl) backlogEl.textContent = 'FOI 18,364人官方底盘 (主申9,358人)';
        if (mdEl) mdEl.textContent = 'FY27 联邦配额 14,110 个 (腰斩 -57%)';
        if (speedEl) speedEl.textContent = '出清速率：日均44人 · 扣除14天假日';
        if (heroModeChip) heroModeChip.textContent = '推荐模式 2 · 官方标称实盘 44人/日';
        if (dgText) dgText.textContent = '491 优先职业或境内材料完备个案，免补料直签通常可提前 5~10 个工作日突围！';
        if (dsEl) dsEl.textContent = '数据源：SmartVisaGuide Database & 官方 Subclass 491 宏观大盘';
        if (footerEl) footerEl.textContent = '数据基准：澳洲内政部 FOI 官方底盘数据 (P+S 18,364人) ｜ 实施政策：MD122 Ministerial Direction';

        if (m2Title) m2Title.textContent = '官方标称实盘 · 44人/日 (推荐)';
        if (m2Desc) m2Desc.textContent = '扣除14天节假日闭馆日。境内平稳出清；境外于2026年4月处触发本财年配额耗尽熔断。';
        if (m1Title) m1Title.textContent = '38人/日 · 保守严控';
        if (m1Desc) m1Desc.textContent = '日均38人稳健推进，严格防止财年配额超支，境外顺延时间略有拉长。';
        if (m3Title) m3Title.textContent = '50人/日 · 提速冲刺';
        if (m3Desc) m3Desc.textContent = '假设移民局调集人手消化偏远地区积压，出清速率提升至50人/日。';
        if (m4Title) m4Title.textContent = '32人/日 · 极限制约';
        if (m4Desc) m4Desc.textContent = '偏远地区配额受雇主担保494挤压情景，仅作下限压力测试参考。';

        if (aiInsightEl) {
            aiInsightEl.innerHTML = `<p><strong>【491 审理格局核心定论】</strong>根据最新内政部官方数据（DA26/08/00490），491 州担保大盘在池 <strong>18,364 人</strong>（主申 <strong>9,358 人</strong>，家庭带眷系数高达 <strong>1.962</strong>）。受 FY27 偏远地区总配额大幅腰斩 <strong>57.2%</strong>（降至 14,110 个）限制，移民局日均消耗产能锁定在 <strong>44 人/净工作日</strong>。</p>
<p><strong>【三大赛道关键研判】</strong><br>
① 🩺 <strong>Priority 优先职业秒批</strong>：医疗、教师、建筑等优先工种无论境内外均享受顶级通道，2026年4-7月递交者已在 2026年9月密集获批，周期仅 <strong>2 ~ 4 个月</strong>；<br>
② 🦘 <strong>Onshore 境内普通稳步出清</strong>：日均分配约 26 人，截至 2026年7月递交的境内大部队预计将在 <strong>2027年2月底前</strong> 全部出清；<br>
③ 🌏 <strong>Offshore 境外遭遇配额熔断</strong>：境外普通赛道在排至 <strong>2026年4月递交</strong> 时，本财年 1.1 万个 491 配额宣告耗尽（“财年配额结束”），4月及以后递交者将顺延至 <strong>FY28 新财年 (2027年7月后)</strong> 获批。</p>`;
        }

        if (trackerGrid) {
            trackerGrid.innerHTML = `
                <div class="tracker-col">
                    <div class="tracker-label">🌟 Priority 优先通道实测 (偏远医疗/教师/紧缺基建)</div>
                    <div class="tracker-val">推进至 <strong>2026-05-18</strong> (境内医疗) / <strong>2026-04-10</strong> (境外幼教)</div>
                    <div class="tracker-hint">
                        官方周期：<strong>25% 2.3个月 | 50% 3.8个月 | 75% 5.5个月</strong>。<br>
                        实盘：9.23 塔州境内护士(2026-05-18)仅 <strong>3.8个月</strong> 免补料秒批！偏远地区急需优先通道全球免排队。
                    </div>
                </div>
                <div class="tracker-col">
                    <div class="tracker-label">🦘 Onshore 境内普通通道实测 (Tier 2)</div>
                    <div class="tracker-val">前沿推进至 <strong>2025-11-03</strong> (QLD厨师) · 稳步消化 <strong>2025年下半年</strong></div>
                    <div class="tracker-hint">
                        官方周期：<strong>25% 7.8个月 | 50% 10.5个月 | 75% 12.2个月</strong>。<br>
                        实盘：境内分配约 26人/日流水线，2025年积压平稳出清中，预计 2027年2月底前基本清空全量存量。
                    </div>
                </div>
                <div class="tracker-col">
                    <div class="tracker-label">🌏 Offshore 境外普通通道实测 (Tier 3/4 · 配额预警)</div>
                    <div class="tracker-val">推进至 <strong>2025-07-15</strong> (NSW机械工程) · <strong>配额熔断线：2026-04</strong></div>
                    <div class="tracker-hint">
                        官方周期：<strong>25% 12.8个月 | 50% 14.2个月 | 75% 16.0个月</strong>。<br>
                        实盘：境外普通赛道日均分配约 18人/日。2026年4月及以后递交案已打满本财年配额，顺延至 FY28。
                    </div>
                </div>
            `;
        }

        if (feedTitle) feedTitle.textContent = '9月19日 ~ 9月24日 491 偏远地区实盘批签追踪实录 (SmartVisaGuide)';
        if (feedRows) {
            feedRows.innerHTML = `
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">注册护士 (Registered Nurse - 偏远急需优先)</span>
                        <span class="feed-sub">TAS 境内 491 · 2026-05-18 递交 (85分)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-tag-dg">⚡ 3.8个月免补料直签</span>
                        <span class="feed-status">9/23 下签 · 医疗绿色通道秒批</span>
                    </div>
                </div>
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">幼儿教师 (Early Childhood Teacher - 偏远急需优先)</span>
                        <span class="feed-sub">SA 境外 491 · 2026-04-10 递交 (80分)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-tag-dg">⚡ 4.5个月免补料直签</span>
                        <span class="feed-status">9/22 下签 · 幼教急需跨国直签</span>
                    </div>
                </div>
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">厨师 (Chef - 偏远境内普通非优先)</span>
                        <span class="feed-sub">QLD 境内 491 · 2025-11-03 递交 (75分)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-status" style="background:#F1F5F9;color:#475569;border-color:#CBD5E1">10.5个月直签</span>
                        <span class="feed-status">9/21 下签 · 境内餐饮技工稳健推进</span>
                    </div>
                </div>
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">机械工程师 (Mechanical Engineer - 境外家庭普通)</span>
                        <span class="feed-sub">NSW 境外 491 · 2025-07-15 递交 (85分·带配偶)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-status" style="background:#F1F5F9;color:#475569;border-color:#CBD5E1">14.2个月下签</span>
                        <span class="feed-status">9/20 下签 · 境外带副申正常排期推进</span>
                    </div>
                </div>
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">会计师 (General Accountant - 境外单人普通)</span>
                        <span class="feed-sub">WA 境外 491 · 2025-08-22 递交 (90分·单身)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-tag-dg">⚡ 13.1个月下签</span>
                        <span class="feed-status">9/19 下签 · 单人Tier 3享受优先红利</span>
                    </div>
                </div>
            `;
        }
    }

    // Re-initialize select options
    initSelect();
    calculateForecast();
    if (document.getElementById('full-table-content') && document.getElementById('full-table-content').style.display === 'block') {
        renderFullTable(currentTableMode);
    }
}
"""

p_start = html.find(js_switch_needle)
p_end = html.find(js_switch_end)
if p_start != -1 and p_end != -1:
    html = html[:p_start] + new_switch_subclass + '\n' + html[p_end:]
    print('Updated switchSubclass in JS.')
else:
    print('Warning: Could not find switchSubclass anchors.')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated index.html successfully! New length:', len(html))
