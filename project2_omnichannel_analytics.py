"""
=============================================================================
PROJECT 2: Omni-Channel Campaign Performance Analytics
Marketing Analytics | KPI Tracking | Attribution Analysis
Khyathi Lakshmi Sri Ghantasala | MS Business Analytics
=============================================================================
Tools: Python, pandas, matplotlib, seaborn, scipy, scikit-learn
Domain: Marketing Analytics | Campaign Optimization | BI Reporting
=============================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'figure.facecolor': '#FAFAFA',
    'axes.facecolor': '#FAFAFA',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'font.family': 'DejaVu Sans',
    'axes.titlesize': 12,
    'axes.labelsize': 10,
})

NAVY  = '#1C2B4A'
BLUE  = '#1A5276'
TEAL  = '#148F77'
AMBER = '#D4AC0D'
RED   = '#C0392B'
GREEN = '#1E8449'
COLS  = [NAVY, BLUE, TEAL, AMBER, RED, GREEN]

np.random.seed(42)

print("=" * 65)
print("  PROJECT 2: Omni-Channel Campaign Performance Analytics")
print("  Khyathi Lakshmi Sri Ghantasala | MS Business Analytics")
print("=" * 65)

# ── STEP 1: Generate Campaign Dataset ─────────────────────────────────────
print("\n[1/7] Generating 2-year omni-channel campaign dataset...")

dates = pd.date_range('2023-01-01', '2024-12-31', freq='W')
channels   = ['Email', 'Social', 'Paid Search', 'Organic', 'Display']
categories = ['Financial Services', 'Business Solutions', 'Marketing Tools', 'Tech Products']
regions    = ['Northeast', 'Southeast', 'Midwest', 'West', 'Southwest']

records = []
for date in dates:
    for channel in channels:
        for category in categories:
            season_mult = 1 + 0.3 * np.sin(2 * np.pi * date.dayofyear / 365)
            base_impressions = {
                'Email': 50000, 'Social': 80000, 'Paid Search': 45000,
                'Organic': 35000, 'Display': 120000
            }[channel]
            impressions = int(base_impressions * season_mult * np.random.uniform(0.8, 1.2))
            ctr = {
                'Email': 0.22, 'Social': 0.08, 'Paid Search': 0.15,
                'Organic': 0.12, 'Display': 0.04
            }[channel] * np.random.uniform(0.85, 1.15)
            clicks       = int(impressions * ctr)
            cvr_base = {
                'Email': 0.045, 'Social': 0.025, 'Paid Search': 0.065,
                'Organic': 0.055, 'Display': 0.012
            }[channel]
            conversions  = int(clicks * cvr_base * np.random.uniform(0.85, 1.15) * season_mult)
            avg_order    = {'Financial Services': 320, 'Business Solutions': 185,
                           'Marketing Tools': 95, 'Tech Products': 145}[category]
            revenue      = conversions * avg_order * np.random.uniform(0.9, 1.1)
            spend        = {
                'Email': 0.02, 'Social': 0.08, 'Paid Search': 0.15,
                'Organic': 0.01, 'Display': 0.05
            }[channel] * impressions * np.random.uniform(0.9, 1.1)

            records.append({
                'date': date,
                'week': date.isocalendar()[1],
                'month': date.month,
                'quarter': date.quarter,
                'year': date.year,
                'channel': channel,
                'category': category,
                'impressions': impressions,
                'clicks': clicks,
                'conversions': conversions,
                'revenue': round(revenue, 2),
                'spend': round(spend, 2),
                'ctr': round(ctr * 100, 3),
                'cvr': round(conversions / max(clicks, 1) * 100, 3),
            })

df = pd.DataFrame(records)
df['roas']  = (df['revenue'] / df['spend'].replace(0, np.nan)).round(2)
df['cac']   = (df['spend'] / df['conversions'].replace(0, np.nan)).round(2)
df['cpm']   = (df['spend'] / df['impressions'] * 1000).round(2)
df['roi']   = ((df['revenue'] - df['spend']) / df['spend'] * 100).round(2)

print(f"    ✓ Dataset: {len(df):,} weekly campaign records")
print(f"    ✓ Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"    ✓ Total revenue: ${df['revenue'].sum():,.0f}")
print(f"    ✓ Total spend:   ${df['spend'].sum():,.0f}")
print(f"    ✓ Overall ROAS:  {df['revenue'].sum()/df['spend'].sum():.2f}x")

# ── STEP 2: KPI Framework ─────────────────────────────────────────────────
print("\n[2/7] Building KPI framework — product, customer, segment, BU level...")

kpis = {
    'Total Revenue':     f"${df['revenue'].sum():,.0f}",
    'Total Spend':       f"${df['spend'].sum():,.0f}",
    'Total Conversions': f"{df['conversions'].sum():,}",
    'Overall ROAS':      f"{df['revenue'].sum()/df['spend'].sum():.2f}x",
    'Avg CTR':           f"{df['ctr'].mean():.2f}%",
    'Avg CVR':           f"{df['cvr'].mean():.2f}%",
    'Avg CAC':           f"${df['cac'].mean():.2f}",
    'Avg ROI':           f"{df['roi'].mean():.1f}%",
}
print("    KPI Dashboard Summary:")
for k, v in kpis.items():
    print(f"      {k:<22}: {v}")

# ── STEP 3: Channel Attribution Analysis ──────────────────────────────────
print("\n[3/7] Running multi-channel attribution analysis...")

channel_perf = df.groupby('channel').agg(
    total_revenue    = ('revenue', 'sum'),
    total_spend      = ('spend', 'sum'),
    total_conversions= ('conversions', 'sum'),
    avg_roas         = ('roas', 'mean'),
    avg_cac          = ('cac', 'mean'),
    avg_ctr          = ('ctr', 'mean'),
    avg_cvr          = ('cvr', 'mean'),
).round(2)
channel_perf['roi_pct'] = ((channel_perf['total_revenue'] - channel_perf['total_spend'])
                           / channel_perf['total_spend'] * 100).round(1)
channel_perf['revenue_share'] = (channel_perf['total_revenue']
                                 / channel_perf['total_revenue'].sum() * 100).round(1)
print("\n    Channel Performance:")
print(channel_perf[['total_revenue', 'total_spend', 'avg_roas', 'avg_cac', 'roi_pct', 'revenue_share']].to_string())

# ── STEP 4: Seasonal Trend Analysis ───────────────────────────────────────
print("\n[4/7] Analyzing seasonal demand patterns...")

monthly = df.groupby(['year', 'month']).agg(
    revenue=('revenue', 'sum'),
    spend=('spend', 'sum'),
    conversions=('conversions', 'sum')
).reset_index()
monthly['roas'] = monthly['revenue'] / monthly['spend']

# Trend decomposition
monthly_avg = df.groupby('month')['revenue'].mean()
peak_month  = monthly_avg.idxmax()
low_month   = monthly_avg.idxmin()
seasonality = monthly_avg.max() / monthly_avg.min()
print(f"    ✓ Peak revenue month:  Month {peak_month}")
print(f"    ✓ Lowest revenue month: Month {low_month}")
print(f"    ✓ Seasonal variation:   {seasonality:.2f}x (peak vs trough)")

# ── STEP 5: Category & Regional Performance ────────────────────────────────
print("\n[5/7] Analyzing category and regional performance...")

cat_perf = df.groupby('category').agg(
    revenue=('revenue', 'sum'),
    spend=('spend', 'sum'),
    conversions=('conversions', 'sum'),
    avg_cac=('cac', 'mean')
).round(2)
cat_perf['roas'] = (cat_perf['revenue'] / cat_perf['spend']).round(2)

top_cat    = cat_perf['revenue'].idxmax()
bottom_cat = cat_perf['revenue'].idxmin()
print(f"    ✓ Top category: {top_cat} (${cat_perf.loc[top_cat,'revenue']:,.0f})")
print(f"    ✓ Underperforming: {bottom_cat} — optimization opportunity identified")

# ── STEP 6: Anomaly Detection ─────────────────────────────────────────────
print("\n[6/7] Running anomaly detection on weekly performance data...")

weekly = df.groupby(['date', 'channel'])['revenue'].sum().reset_index()
weekly_pivot = weekly.pivot(index='date', columns='channel', values='revenue').fillna(0)

anomalies_found = 0
for channel in channels:
    series = weekly_pivot[channel]
    z_scores = np.abs(stats.zscore(series))
    anomalies = (z_scores > 2.5).sum()
    anomalies_found += anomalies

print(f"    ✓ Weekly records scanned: {len(weekly_pivot) * len(channels):,}")
print(f"    ✓ Anomalies detected (|z| > 2.5): {anomalies_found}")
print(f"    ✓ Anomaly rate: {anomalies_found / (len(weekly_pivot) * len(channels)):.1%}")

# ── STEP 7: Visualization Dashboard ───────────────────────────────────────
print("\n[7/7] Building executive performance dashboard...")

fig = plt.figure(figsize=(20, 15), facecolor='#FAFAFA')
fig.suptitle(
    'Omni-Channel Campaign Performance Analytics Dashboard\nKhyathi Lakshmi Sri Ghantasala | MS Business Analytics',
    fontsize=15, fontweight='bold', color=NAVY, y=0.99
)
gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.38)

# 1. Revenue by Channel
ax1 = fig.add_subplot(gs[0, 0:2])
ch_rev = channel_perf['total_revenue'].sort_values(ascending=True)
bars = ax1.barh(ch_rev.index, ch_rev.values / 1e6, color=COLS[:len(ch_rev)], edgecolor='white')
ax1.set_title('Total Revenue by Channel ($M)', fontweight='bold', color=NAVY)
ax1.set_xlabel('Revenue ($M)')
for bar, val in zip(bars, ch_rev.values):
    ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
             f'${val/1e6:.1f}M', va='center', fontsize=9)

# 2. ROAS by Channel
ax2 = fig.add_subplot(gs[0, 2])
ch_roas = channel_perf['avg_roas'].sort_values(ascending=False)
bars2   = ax2.bar(range(len(ch_roas)), ch_roas.values,
                  color=[TEAL if v == ch_roas.max() else BLUE for v in ch_roas.values],
                  edgecolor='white')
ax2.set_xticks(range(len(ch_roas)))
ax2.set_xticklabels([c.replace(' ', '\n') for c in ch_roas.index], fontsize=8)
ax2.set_title('Avg ROAS by Channel', fontweight='bold', color=NAVY)
ax2.set_ylabel('ROAS (x)')
ax2.axhline(y=channel_perf['avg_roas'].mean(), color=AMBER, linestyle='--', lw=1.5,
            label=f'Avg: {channel_perf["avg_roas"].mean():.2f}x')
ax2.legend(fontsize=8)
for bar, val in zip(bars2, ch_roas.values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'{val:.2f}x', ha='center', fontsize=8, fontweight='bold', color=NAVY)

# 3. CAC by Channel
ax3 = fig.add_subplot(gs[0, 3])
ch_cac = channel_perf['avg_cac'].sort_values()
bars3  = ax3.barh(ch_cac.index, ch_cac.values,
                  color=[TEAL if v == ch_cac.min() else AMBER for v in ch_cac.values],
                  edgecolor='white')
ax3.set_title('Avg CAC by Channel ($)\nLower is Better', fontweight='bold', color=NAVY)
ax3.set_xlabel('Cost per Acquisition ($)')
for bar, val in zip(bars3, ch_cac.values):
    ax3.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
             f'${val:.0f}', va='center', fontsize=9)

# 4. Monthly Revenue Trend
ax4 = fig.add_subplot(gs[1, 0:2])
for i, (year, grp) in enumerate(monthly.groupby('year')):
    ax4.plot(grp['month'], grp['revenue'] / 1e6, marker='o', lw=2.5,
             color=COLS[i], label=str(year), markersize=5)
ax4.set_title('Monthly Revenue Trend by Year', fontweight='bold', color=NAVY)
ax4.set_xlabel('Month')
ax4.set_ylabel('Revenue ($M)')
ax4.set_xticks(range(1, 13))
ax4.set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'])
ax4.legend()
ax4.fill_between(range(1, 13), 0, 0, alpha=0)

# 5. Category Revenue & ROAS
ax5 = fig.add_subplot(gs[1, 2])
cat_rev = cat_perf['revenue'].sort_values(ascending=False)
colors5 = [TEAL if i == 0 else BLUE for i in range(len(cat_rev))]
bars5 = ax5.bar([c.replace(' ', '\n') for c in cat_rev.index],
                cat_rev.values / 1e6, color=colors5, edgecolor='white')
ax5.set_title('Revenue by Category ($M)', fontweight='bold', color=NAVY)
ax5.set_ylabel('Revenue ($M)')
for bar, val in zip(bars5, cat_rev.values):
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             f'${val/1e6:.1f}M', ha='center', fontsize=8, fontweight='bold', color=NAVY)

# 6. CTR vs CVR scatter
ax6 = fig.add_subplot(gs[1, 3])
for i, ch in enumerate(channels):
    ch_data = df[df['channel'] == ch]
    ax6.scatter(ch_data['ctr'], ch_data['cvr'], alpha=0.3, s=15,
                color=COLS[i % len(COLS)], label=ch)
ax6.set_title('CTR vs CVR by Channel', fontweight='bold', color=NAVY)
ax6.set_xlabel('Click-Through Rate (%)')
ax6.set_ylabel('Conversion Rate (%)')
ax6.legend(fontsize=7, markerscale=2)

# 7. Weekly Revenue Trend with Anomalies
ax7 = fig.add_subplot(gs[2, 0:2])
weekly_total = df.groupby('date')['revenue'].sum()
ax7.fill_between(weekly_total.index, weekly_total.values / 1e3,
                 alpha=0.15, color=BLUE)
ax7.plot(weekly_total.index, weekly_total.values / 1e3, color=NAVY, lw=1.5)
rolling_mean = weekly_total.rolling(4).mean()
rolling_std  = weekly_total.rolling(4).std()
ax7.plot(weekly_total.index, rolling_mean / 1e3, color=TEAL, lw=2, label='4-Week Moving Avg')
ax7.fill_between(weekly_total.index,
                 (rolling_mean - 2 * rolling_std) / 1e3,
                 (rolling_mean + 2 * rolling_std) / 1e3,
                 alpha=0.1, color=AMBER, label='±2σ Band')
# Flag anomalies
z = np.abs(stats.zscore(weekly_total.ffill()))
anomaly_dates  = weekly_total.index[z > 2.5]
anomaly_values = weekly_total[z > 2.5]
ax7.scatter(anomaly_dates, anomaly_values / 1e3, color=RED, s=60, zorder=5,
            label=f'Anomalies ({len(anomaly_dates)})')
ax7.set_title('Weekly Revenue Trend with Anomaly Detection', fontweight='bold', color=NAVY)
ax7.set_ylabel('Revenue ($K)')
ax7.legend(fontsize=8)

# 8. KPI Summary Card
ax8 = fig.add_subplot(gs[2, 2:])
ax8.axis('off')
ax8.set_title('Executive KPI Summary', fontweight='bold', color=NAVY, pad=15)
kpi_rows = [
    ('REVENUE PERFORMANCE', '', NAVY, 11, 'bold'),
    ('Total Revenue',       f"${df['revenue'].sum()/1e6:.1f}M", TEAL, 10, 'normal'),
    ('Total Spend',         f"${df['spend'].sum()/1e6:.1f}M",   BLUE, 10, 'normal'),
    ('Overall ROAS',        f"{df['revenue'].sum()/df['spend'].sum():.2f}x", TEAL, 10, 'bold'),
    ('Overall ROI',         f"{df['roi'].mean():.1f}%",         GREEN, 10, 'bold'),
    ('', '', NAVY, 8, 'normal'),
    ('CAMPAIGN EFFICIENCY', '', NAVY, 11, 'bold'),
    ('Avg CTR',             f"{df['ctr'].mean():.2f}%",         BLUE, 10, 'normal'),
    ('Avg CVR',             f"{df['cvr'].mean():.2f}%",         BLUE, 10, 'normal'),
    ('Avg CAC',             f"${df['cac'].mean():.0f}",         AMBER, 10, 'normal'),
    ('Best Channel ROAS',   f"{channel_perf['avg_roas'].max():.2f}x ({channel_perf['avg_roas'].idxmax()})", TEAL, 10, 'bold'),
    ('', '', NAVY, 8, 'normal'),
    ('DATA QUALITY',        '', NAVY, 11, 'bold'),
    ('Total Records',       f"{len(df):,} weekly records",      NAVY, 10, 'normal'),
    ('Anomalies Detected',  f"{anomalies_found} flagged for review", RED, 10, 'bold'),
    ('Seasonal Variation',  f"{seasonality:.1f}x (peak vs trough)", AMBER, 10, 'normal'),
]
y_pos = 0.97
for label, value, color, size, weight in kpi_rows:
    if value:
        ax8.text(0.05, y_pos, f"{label}:", fontsize=size, color=NAVY,
                 fontweight=weight, transform=ax8.transAxes, va='top')
        ax8.text(0.55, y_pos, value, fontsize=size, color=color,
                 fontweight='bold', transform=ax8.transAxes, va='top')
    else:
        ax8.text(0.05, y_pos, label, fontsize=size, color=color,
                 fontweight=weight, transform=ax8.transAxes, va='top')
    y_pos -= 0.062

plt.savefig('/mnt/user-data/outputs/project2_omnichannel_analytics.png',
            dpi=150, bbox_inches='tight', facecolor='#FAFAFA')
plt.close()

print("\n" + "=" * 65)
print("  PROJECT 2 COMPLETE")
print(f"  Campaign records analyzed:   {len(df):,}")
print(f"  Total revenue tracked:       ${df['revenue'].sum()/1e6:.1f}M")
print(f"  Overall ROAS:                {df['revenue'].sum()/df['spend'].sum():.2f}x")
print(f"  Anomalies detected:          {anomalies_found}")
print(f"  Seasonal variation:          {seasonality:.1f}x")
print(f"  Output saved: project2_omnichannel_analytics.png")
print("=" * 65)
