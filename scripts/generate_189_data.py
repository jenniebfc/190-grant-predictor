import json
from datetime import date, timedelta

# Australian Net Working Days Calendar Engine (excluding weekends & 14 DHA holidays)
DHA_HOLIDAYS_2026_2027 = {
    date(2026, 10, 5),   # Labour Day (ACT/NSW/SA)
    date(2026, 12, 25),  # Christmas Day
    date(2026, 12, 28),  # Boxing Day obs
    date(2026, 12, 29),  # DHA Christmas shutdown
    date(2026, 12, 30),  # DHA Christmas shutdown
    date(2026, 12, 31),  # DHA Christmas shutdown
    date(2027, 1, 1),    # New Year's Day
    date(2027, 1, 26),   # Australia Day
    date(2027, 3, 8),    # Canberra Day
    date(2027, 3, 26),   # Good Friday
    date(2027, 3, 29),   # Easter Monday
    date(2027, 4, 26),   # ANZAC Day obs
    date(2027, 5, 31),   # Reconciliation Day
    date(2027, 6, 14),   # King's Birthday
}

def is_workday(d):
    if d.weekday() >= 5: # Sat or Sun
        return False
    if d in DHA_HOLIDAYS_2026_2027:
        return False
    return True

def add_workdays(start_date, workdays):
    cur = start_date
    added = 0
    while added < workdays:
        cur += timedelta(days=1)
        if is_workday(cur):
            added += 1
    return cur

def workdays_between(d1, d2):
    if d1 >= d2:
        return 0
    cur = d1
    count = 0
    while cur < d2:
        cur += timedelta(days=1)
        if is_workday(cur):
            count += 1
    return count

months = [
    '<=2024-10', '2024-11', '2024-12', '2025-01', '2025-02', '2025-03',
    '2025-04', '2025-05', '2025-06', '2025-07', '2025-08', '2025-09',
    '2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03',
    '2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09',
    '2026-10', '2026-11', '2026-12'
]

# Baseline date: 2026-09-24
START_DATE = date(2026, 7, 1)

# Mode 2 (79 people/day) exact benchmarks from Ethan's spreadsheet
# Ethan verified dates:
# Nov-25: T1 18/9/2026, T2 Cleared, T3 23/10/2026, T4 23/10/2026
# Dec-25: T1 21/9/2026, T2 Cleared, T3 23/10/2026, T4 23/10/2026
# Jan-26 to May-26: T1 21/9/2026, T2 Cleared, T3 26/10/2026, T4 26/10/2026
# Jun-26: T1 28/9/2026, T2 16/10/2026, T3 16/11/2026, T4 16/11/2026
# Jul-26: T1 30/9/2026, T2 23/10/2026, T3 25/11/2026, T4 25/11/2026

ethan_m2_dates = {
    '2025-11': {'1': '2026-09-18', '2': 'MD119已完成', '3': '2026-10-23', '4': '2026-10-23'},
    '2025-12': {'1': '2026-09-21', '2': 'MD119已完成', '3': '2026-10-23', '4': '2026-10-23'},
    '2026-01': {'1': '2026-09-21', '2': 'MD119已完成', '3': '2026-10-26', '4': '2026-10-26'},
    '2026-02': {'1': '2026-09-21', '2': 'MD119已完成', '3': '2026-10-26', '4': '2026-10-26'},
    '2026-03': {'1': '2026-09-21', '2': 'MD119已完成', '3': '2026-10-26', '4': '2026-10-26'},
    '2026-04': {'1': '2026-09-21', '2': 'MD119已完成', '3': '2026-10-26', '4': '2026-10-26'},
    '2026-05': {'1': '2026-09-21', '2': 'MD119已完成', '3': '2026-10-26', '4': '2026-10-26'},
    '2026-06': {'1': '2026-09-28', '2': '2026-10-16', '3': '2026-11-16', '4': '2026-11-16'},
    '2026-07': {'1': '2026-09-30', '2': '2026-10-23', '3': '2026-11-25', '4': '2026-11-25'},
    '2026-08': {'1': '2026-10-08', '2': '2026-11-06', '3': '2026-12-08', '4': '2026-12-08'},
    '2026-09': {'1': '2026-10-15', '2': '2026-11-20', '3': '2026-12-22', '4': '2026-12-22'},
    '2026-10': {'1': '2026-10-22', '2': '2026-12-04', '3': '2027-01-15', '4': '2027-01-15'},
    '2026-11': {'1': '2026-10-29', '2': '2026-12-18', '3': '2027-02-05', '4': '2027-02-05'},
    '2026-12': {'1': '2026-11-05', '2': '2027-01-08', '3': '2027-02-26', '4': '2027-02-26'},
}

# For months before 2025-11: all cleared in MD119
for m in months:
    if m not in ethan_m2_dates:
        ethan_m2_dates[m] = {
            '1': '2026-09-18',
            '2': 'MD119已完成',
            '3': 'MD119已完成',
            '4': 'MD119已完成'
        }

# Generate 4 modes:
# Mode 2: 79 people/day (Ethan reference)
# Mode 1: 68 people/day (Standard quota 16.9k)
# Mode 3: 95 people/day (Accelerated push)
# Mode 4: 55 people/day (Conservative)

data = {
    'months': months,
    'counts': {},
    'm1': {'1': {}, '2': {}, '3': {}, '4': {}},
    'm2': {'1': {}, '2': {}, '3': {}, '4': {}},
    'm3': {'1': {}, '2': {}, '3': {}, '4': {}},
    'm4': {'1': {}, '2': {}, '3': {}, '4': {}},
}

SEP_24 = date(2026, 9, 24)

for idx, m in enumerate(months):
    # Mode 2
    for t in ['1', '2', '3', '4']:
        d_str = ethan_m2_dates[m][t]
        data['m2'][t][str(idx)] = {
            'date': d_str,
            'fy': 'FY27'
        }

        # Calculate workdays relative to 2026-07-01
        if d_str == 'MD119已完成':
            data['m1'][t][str(idx)] = {'date': 'MD119已完成', 'fy': 'FY27'}
            data['m3'][t][str(idx)] = {'date': 'MD119已完成', 'fy': 'FY27'}
            data['m4'][t][str(idx)] = {'date': 'MD119已完成', 'fy': 'FY27'}
        else:
            y, mo, day = [int(x) for x in d_str.split('-')]
            target_date = date(y, mo, day)
            w_days = workdays_between(START_DATE, target_date)
            # Scale workdays by ratio:
            # m1 (68): w_days * (79 / 68)
            w1 = int(round(w_days * (79.0 / 68.0)))
            d1 = add_workdays(START_DATE, w1)
            fy1 = 'FY27' if d1 < date(2027, 7, 1) else 'FY28'
            data['m1'][t][str(idx)] = {'date': d1.strftime('%Y-%m-%d'), 'fy': fy1}

            # m3 (95): w_days * (79 / 95)
            w3 = int(round(w_days * (79.0 / 95.0)))
            d3 = add_workdays(START_DATE, w3)
            fy3 = 'FY27' if d3 < date(2027, 7, 1) else 'FY28'
            data['m3'][t][str(idx)] = {'date': d3.strftime('%Y-%m-%d'), 'fy': fy3}

            # m4 (55): w_days * (79 / 55)
            w4 = int(round(w_days * (79.0 / 55.0)))
            d4 = add_workdays(START_DATE, w4)
            fy4 = 'FY27' if d4 < date(2027, 7, 1) else 'FY28'
            data['m4'][t][str(idx)] = {'date': d4.strftime('%Y-%m-%d'), 'fy': fy4}

out_path = '/Users/jennie/.gemini/antigravity/scratch/public_app/scripts/forecast_data_189.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Generated 189 dataset successfully at {out_path}!")
print("Sample Jun-26 Mode 2:")
print("T1:", data['m2']['1'][str(months.index('2026-06'))])
print("T2:", data['m2']['2'][str(months.index('2026-06'))])
print("T3:", data['m2']['3'][str(months.index('2026-06'))])
print("T4:", data['m2']['4'][str(months.index('2026-06'))])
