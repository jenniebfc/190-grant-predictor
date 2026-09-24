import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('Original index.html len:', len(html))

# 1. Load forecast_data_189.json
with open('scripts/forecast_data_189.json', 'r', encoding='utf-8') as f:
    data_189_json = f.read().strip()

# Insert const DATA_189 right before const DATA_190
p_190 = html.find('const DATA_190 =')
if 'const DATA_189 =' not in html and p_190 != -1:
    html = html[:p_190] + f"const DATA_189 = {data_189_json};\n\n" + html[p_190:]
    print("Injected const DATA_189.")

# 2. Update CSS for tab-189 active badge
css_189_badge = """
        .subclass-tab.active#tab-189 .tab-badge {
            background: #059669; /* Emerald Green for 189 Independent PR */
            color: #FFFFFF;
        }
"""
if '#tab-189' not in html:
    p_badge_end = html.find('.subclass-tab.active#tab-190 .tab-badge')
    if p_badge_end != -1:
        html = html[:p_badge_end] + css_189_badge + html[p_badge_end:]
        print("Added CSS for tab-189 active badge.")

# 3. Update Header HTML with 3-tab Switcher
old_switcher_pattern = r'<div class="subclass-nav-wrapper">[\s\S]*?</div>\s*</div>'
new_switcher_html = """<div class="subclass-nav-wrapper">
            <div class="subclass-switcher" role="tablist" aria-label="选择澳洲移民签证类别">
                <button type="button" class="subclass-tab" id="tab-189" role="tab" aria-selected="false" onclick="switchSubclass('189')">
                    <span class="tab-title">
                        <span class="tab-prefix">Subclass </span><span class="tab-code">189</span><span class="tab-desc-desktop"> 独立技术移民</span><span class="tab-desc-mobile"> 独立</span>
                    </span>
                    <span class="tab-badge">
                        <span class="badge-desktop">永居 PR</span>
                        <span class="badge-mobile">PR</span>
                    </span>
                </button>
                <button type="button" class="subclass-tab active" id="tab-190" role="tab" aria-selected="true" onclick="switchSubclass('190')">
                    <span class="tab-title">
                        <span class="tab-prefix">Subclass </span><span class="tab-code">190</span><span class="tab-desc-desktop"> 州担保技术移民</span><span class="tab-desc-mobile"> 州担</span>
                    </span>
                    <span class="tab-badge">
                        <span class="badge-desktop">永居 PR</span>
                        <span class="badge-mobile">PR</span>
                    </span>
                </button>
                <button type="button" class="subclass-tab" id="tab-491" role="tab" aria-selected="false" onclick="switchSubclass('491')">
                    <span class="tab-title">
                        <span class="tab-prefix">Subclass </span><span class="tab-code">491</span><span class="tab-desc-desktop"> 偏远地区州担/亲属</span><span class="tab-desc-mobile"> 偏远</span>
                    </span>
                    <span class="tab-badge">
                        <span class="badge-desktop">准永居 TR</span>
                        <span class="badge-mobile">TR</span>
                    </span>
                </button>
            </div>
        </div>"""

html = re.sub(old_switcher_pattern, new_switcher_html, html, count=1)
print("Updated HTML header with 3-visa switcher (189 / 190 / 491).")

# 4. Update JS switchSubclass function and support functions
js_switch_needle = 'function switchSubclass(sc) {'
js_switch_end = 'function getCurrentData() {'

new_switch_subclass = """function switchSubclass(sc) {
    if (currentSubclass === sc) return;
    currentSubclass = sc;

    // 1. Update Tab Styles for 189 / 190 / 491
    const tab189 = document.getElementById('tab-189');
    const tab190 = document.getElementById('tab-190');
    const tab491 = document.getElementById('tab-491');
    if (tab189) {
        tab189.classList.toggle('active', sc === '189');
        tab189.setAttribute('aria-selected', sc === '189');
    }
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

    if (sc === '189') {
        if (titleEl) titleEl.textContent = '澳洲 189 · MD122 智能批签预测';
        if (descEl) descEl.textContent = '基于内政部官方约 6,200 人在池底盘数据与 Ethan 实盘 79人/日模型，全池预计将于 2026 年底前全部出清推平！';
        if (calEl) calEl.innerHTML = '<span class="status-dot"></span>9月24日实盘校准完成 · 吻合度>96%';
        if (backlogEl) backlogEl.textContent = 'FOI ~6,242人在池官方底盘';
        if (mdEl) mdEl.textContent = 'FY27 联邦配额 16,900 个 (充裕)';
        if (speedEl) speedEl.textContent = '出清速率：日均79人 · 年底前无积压';
        if (heroModeChip) heroModeChip.textContent = '推荐模式 2 · 官方标称实盘 79人/日';
        if (dgText) dgText.textContent = '189 独立技术移民材料完备者，免补料通常可提前 5~10 个工作日率先直签突围！';
        if (dsEl) dsEl.textContent = '数据源：SmartVisaGuide Database & 官方 Subclass 189 宏观大盘';
        if (footerEl) footerEl.textContent = '数据基准：澳洲内政部 FOI 官方底盘数据 (P+S ~6,242人) ｜ 实施政策：MD122 Ministerial Direction';

        if (m2Title) m2Title.textContent = '官方标称实盘 · 79人/日 (推荐)';
        if (m2Desc) m2Desc.textContent = '严格吻合实盘测算，扣除14天法定假日及闭馆日。优先职业9月底全清，境内10月中下旬全清，境外11月下旬全清。';
        if (m1Title) m1Title.textContent = '68人/日 · 标准平稳';
        if (m1Desc) m1Desc.textContent = '严格按16,900全额规划匀速消化，境外普通顺延至12月中旬出清。';
        if (m3Title) m3Title.textContent = '95人/日 · 年末冲刺';
        if (m3Desc) m3Desc.textContent = '移民局年底集中调派人手推平独立技术存量，较模式2提前约1~2周全部获批。';
        if (m4Title) m4Title.textContent = '55人/日 · 谨慎控盘';
        if (m4Desc) m4Desc.textContent = '假设部分配额借调其他技术通道，仅作保守下限压力测试参考。';

        if (aiInsightEl) {
            aiInsightEl.innerHTML = `<p><strong>【189 审理格局核心定论】</strong>根据最新内政部官方底盘数据与实盘监测，189 独立技术移民在池存量仅约 <strong>6,242 人</strong>，而 FY27 联邦规划配额高达 <strong>16,900 个</strong>。出水能力远大于池内积压，官方标称以 <strong>79 人/净工作日</strong> 极速推进，<strong>全大盘将于 2026 年 11 月底前彻底出清</strong>！</p>
<p><strong>【三大赛道关键研判】</strong><br>
① 🩺 <strong>Priority 优先职业秒批</strong>：医疗、教师、紧缺建造等无论境内外均已推进至 2026年6-7月递交批次，9月底前全量出清，周期仅 <strong>2 ~ 3.5 个月</strong>；<br>
② 🦘 <strong>Onshore 境内普通</strong>：2026年5月及以前递交案在 MD119 阶段已全部审毕！6月集中递交的大部队预计将在 <strong>2026年10月中旬</strong> 集中获批；<br>
③ 🌏 <strong>Offshore 境外普通</strong>：顺次推进消化，6月批次预计在 <strong>2026年11月下旬</strong> 获批。年底前全澳 189 将实现真正的零积压！</p>`;
        }

        if (trackerGrid) {
            trackerGrid.innerHTML = `
                <div class="tracker-col">
                    <div class="tracker-label">🌟 Priority 优先通道实测 (医疗/幼教/紧缺基建)</div>
                    <div class="tracker-val">推进至 <strong>2026-06-25</strong> (境内医疗) / <strong>2026-06-18</strong> (境外基建)</div>
                    <div class="tracker-hint">
                        官方周期：<strong>25% 2.5个月 | 50% 3.2个月 | 75% 4.0个月</strong>。<br>
                        实盘：9.24 维州境外土木与昆州境内护士仅 <strong>2.9 ~ 3.2个月</strong> 秒签！优先通道免排队直接批复。
                    </div>
                </div>
                <div class="tracker-col">
                    <div class="tracker-label">🦘 Onshore 境内普通通道实测 (Tier 2)</div>
                    <div class="tracker-val">前沿推进至 <strong>2026-06-12</strong> (NSW软件工程) · 5月前已全清</div>
                    <div class="tracker-hint">
                        官方周期：<strong>25% 3.0个月 | 50% 3.8个月 | 75% 5.2个月</strong>。<br>
                        实盘：境内旧案在 MD119 已全部审毕；6月大批次免补料直签密集涌现，10月中旬基本推平。
                    </div>
                </div>
                <div class="tracker-col">
                    <div class="tracker-label">🌏 Offshore 境外普通通道实测 (Tier 3/4)</div>
                    <div class="tracker-val">推进至 <strong>2026-02-15</strong> (WA机械工程) · <strong>11月全出清</strong></div>
                    <div class="tracker-hint">
                        官方周期：<strong>25% 5.5个月 | 50% 7.2个月 | 75% 8.6个月</strong>。<br>
                        实盘：189配额高度充裕，无任何熔断风险，境外6月大部队将于 11月下旬全部获批。
                    </div>
                </div>
            `;
        }

        if (feedTitle) feedTitle.textContent = '9月20日 ~ 9月24日 189 独立技术实盘批签追踪实录 (SmartVisaGuide)';
        if (feedRows) {
            feedRows.innerHTML = `
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">软件工程师 (Software Engineer - 189境内非优先)</span>
                        <span class="feed-sub">NSW 境内 189 · 2026-06-12 递交 (95分)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-tag-dg">⚡ 3.4个月免补料直签</span>
                        <span class="feed-status">9/24 下签 · 6月大批次直签突围</span>
                    </div>
                </div>
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">土木工程师 (Civil Engineer - 189优先职业)</span>
                        <span class="feed-sub">VIC 境外 189 · 2026-06-18 递交 (90分)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-tag-dg">⚡ 3.2个月秒批</span>
                        <span class="feed-status">9/23 下签 · 境外优先极速获批</span>
                    </div>
                </div>
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">注册护士 (Registered Nurse - 189优先职业)</span>
                        <span class="feed-sub">QLD 境内 189 · 2026-06-25 递交 (85分)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-tag-dg">⚡ 2.9个月秒签</span>
                        <span class="feed-status">9/23 下签 · 医疗绿色通道免排队</span>
                    </div>
                </div>
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">机械工程师 (Mechanical Engineer - 189境外普通)</span>
                        <span class="feed-sub">WA 境外 189 · 2026-02-15 递交 (85分)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-status" style="background:#F1F5F9;color:#475569;border-color:#CBD5E1">7.2个月直签</span>
                        <span class="feed-status">9/21 下签 · 境外积压顺利清空</span>
                    </div>
                </div>
                <div class="feed-row">
                    <div>
                        <span class="feed-occ">物理治疗师 (Physiotherapist - 189优先职业)</span>
                        <span class="feed-sub">SA 境外 189 · 2026-06-05 递交 (80分)</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="feed-tag-dg">⚡ 3.6个月免补料直签</span>
                        <span class="feed-status">9/20 下签 · 医疗优先秒下</span>
                    </div>
                </div>
            `;
        }

    } else if (sc === '190') {
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
    print("Updated switchSubclass with 189 support.")

# 5. Update getCurrentData()
old_gcd = """function getCurrentData() {
    return currentSubclass === '190' ? DATA_190 : DATA_491;
}"""
new_gcd = """function getCurrentData() {
    if (currentSubclass === '189') return DATA_189;
    if (currentSubclass === '491') return DATA_491;
    return DATA_190;
}"""
html = html.replace(old_gcd, new_gcd)
print("Updated getCurrentData for 189 / 190 / 491.")

# 6. Update initSelect() for default selection in 189
old_init_select = """        if (currentSubclass === '190' && m === '2026-01') opt.selected = true;
        if (currentSubclass === '491' && m === '2025-06') opt.selected = true;"""
new_init_select = """        if (currentSubclass === '189' && m === '2026-06') opt.selected = true;
        if (currentSubclass === '190' && m === '2026-01') opt.selected = true;
        if (currentSubclass === '491' && m === '2025-06') opt.selected = true;"""
html = html.replace(old_init_select, new_init_select)
print("Updated initSelect default selection.")

# 7. Update calculateForecast() for 189 cleared T2
old_t2_check = "const isClearedT2 = (currentSubclass === '190' && tier === 2 && mIdx < 7);"
new_t2_check = """const isClearedT2 = (currentSubclass === '190' && tier === 2 && mIdx < 7) ||
                        (currentSubclass === '189' && tier === 2 && mIdx < 20);"""
html = html.replace(old_t2_check, new_t2_check)

# 8. Update updateTierStrip(tier) for 189
old_tier_strip_needle = "function updateTierStrip(tier) {"
new_tier_strip = """function updateTierStrip(tier) {
    const tag = document.getElementById('tier-tag');
    const name = document.getElementById('tier-name');
    const cap = document.getElementById('tier-caption');

    tag.className = 'tier-tag t' + tier;
    tag.textContent = 'Tier ' + tier;

    if (currentSubclass === '189') {
        if (tier === 1) {
            name.textContent = '189 全球优先职业赛道 (Tier 1)';
            cap.textContent = '医疗、教育、紧缺基建等，境内外顶级免排队，2026年9月底全部出清（周期仅2~3个月）。';
        } else if (tier === 2) {
            name.textContent = '189 境内普通赛道 (Tier 2)';
            cap.textContent = '境内独立技术申请人，2026年5月及以前在MD119阶段全部审毕！6月批次预计10月中旬全清。';
        } else if (tier === 3) {
            name.textContent = '189 境外单人赛道 (Tier 3)';
            cap.textContent = '境外单身申请人，无副申人头负担，审理顺畅，预计11月中旬全部出清。';
        } else {
            name.textContent = '189 境外家庭普通赛道 (Tier 4)';
            cap.textContent = '境外带副申申请人，年配额高度充裕无熔断，预计11月下旬全池推平，年底前实现零积压！';
        }
    } else if (currentSubclass === '190') {
        if (tier === 1) {
            name.textContent = '全球优先职业赛道 (Tier 1)';
            cap.textContent = '无论境内或境外，优先职业均列为第一优先级，当前正全速集中清理。';
        } else if (tier === 2) {
            name.textContent = '境内非优先职业赛道 (Tier 2)';
            cap.textContent = '澳洲境内非优先通道，占用境内独立流水线（~94人/日），大盘扎实平稳。';
        } else if (tier === 3) {
            name.textContent = '境外单人非优先赛道 (Tier 3)';
            cap.textContent = '境外单人申请（无副申配额负担），优先级高于带副申，大幅提前出签。';
        } else {
            name.textContent = '境外带副申非优先赛道 (Tier 4)';
            cap.textContent = '境外家庭类申请，顺次消化，模型测算2027年上半年配额依然有席位。';
        }
    } else {
        if (tier === 1) {
            name.textContent = '491 全球优先职业赛道 (Tier 1)';
            cap.textContent = '医疗、教育、建筑等偏远地区急需工种，境内外一视同仁顶级秒批（2~4个月）。';
        } else if (tier === 2) {
            name.textContent = '491 境内普通赛道 (Tier 2)';
            cap.textContent = '境内普通偏远地区申请人，日均消耗约 26 人，预计 2027年2月底前基本清空存量。';
        } else if (tier === 3) {
            name.textContent = '491 境外单人赛道 (Tier 3)';
            cap.textContent = '境外单身申请人，优先级高于带副申，排期比家庭件提前约两至三周。';
        } else {
            name.textContent = '491 境外家庭普通赛道 (Tier 4)';
            cap.textContent = '境外家庭带副申件，配额极其吃紧，2026年4月及以后递交者将顺延至 FY28 新财年。';
        }
    }
}"""
p_ts_start = html.find(old_tier_strip_needle)
p_ts_end = html.find("function updateBlessingMsg(tier, isClearedT2) {")
if p_ts_start != -1 and p_ts_end != -1:
    html = html[:p_ts_start] + new_tier_strip + '\n\n' + html[p_ts_end:]
    print("Updated updateTierStrip for 189.")

# 9. Update renderFullTable for 189
old_rft_needle = "if (currentSubclass === '190' && idx < 7) {"
new_rft_block = """if (currentSubclass === '190' && idx < 7) {
            t2_d = '<span style="color:#059669;font-weight:600">MD119已完成</span>';
        }
        if (currentSubclass === '189' && idx < 20) {
            t2_d = '<span style="color:#059669;font-weight:600">MD119已完成</span>';
        }"""
html = html.replace(old_rft_needle, new_rft_block)
print("Updated renderFullTable for 189.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully with full Subclass 189 integration! New length:", len(html))
