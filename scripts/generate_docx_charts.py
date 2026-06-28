import matplotlib.pyplot as plt
import numpy as np
import os

# Set Chinese fonts support (Sans-serif: Microsoft YaHei / PingFang SC; Serif: FangSong / STFangsong)
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'PingFang SC', 'Heiti SC', 'Source Han Sans SC', 'sans-serif']
plt.rcParams['font.serif'] = ['STFangsong', 'FangSong', 'SimSun', 'STSong', 'serif']
plt.rcParams['font.family'] = 'sans-serif'  # Default to sans-serif
plt.rcParams['axes.unicode_minus'] = False  # correct minus sign rendering

# Output directory (same as docx file)
out_dir = "/Users/mac/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_684n8iag9kyn12_e751/temp/drag"
os.makedirs(out_dir, exist_ok=True)

# ----------------- CHART 1: 产业发展数据统计 -----------------
# We will use a 3-panel horizontal layout to show the three trends cleanly with different scales
fig, axes = plt.subplots(1, 3, figsize=(15, 5.5), facecolor='#FAF9F5')
fig.suptitle('2023-2025年云南省文旅与数字经济核心产业发展指标趋势', fontsize=16, fontweight='bold', color='#1B365D', y=0.98, family='serif')

years = ['2023年', '2024年', '2025年']

# Subplot 1: 全省文旅总收入 (万亿元)
axes[0].plot(years, [1.44, 1.49, 1.27], marker='o', linewidth=3, color='#002FA7', markersize=8)
axes[0].set_title('全省文旅总收入 (万亿元)', fontsize=12, fontweight='bold', color='#1B365D', family='serif')
axes[0].set_ylim(1.0, 1.7)
for i, txt in enumerate([1.44, 1.49, 1.27]):
    axes[0].annotate(f"{txt}万亿", (years[i], txt), textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold', color='#1B365D')
axes[0].set_facecolor('#FAF9F5')
axes[0].grid(axis='y', linestyle='--', alpha=0.5)

# Subplot 2: 互联网和相关服务业增速 (%)
axes[1].plot(years, [48.2, 54.5, 51.7], marker='s', linewidth=3, color='#c96442', markersize=8)
axes[1].set_title('互联网和相关服务业增速 (%)', fontsize=12, fontweight='bold', color='#1B365D', family='serif')
axes[1].set_ylim(40, 60)
for i, txt in enumerate([48.2, 54.5, 51.7]):
    axes[1].annotate(f"{txt}%", (years[i], txt), textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold', color='#1B365D')
axes[1].set_facecolor('#FAF9F5')
axes[1].grid(axis='y', linestyle='--', alpha=0.5)

# Subplot 3: 数字创意类岗位新增数量 (个)
axes[2].plot(years, [2100, 2700, 3200], marker='o', linewidth=3, color='#3B6D11', markersize=8)

axes[2].set_title('数字创意类岗位新增数量 (个)', fontsize=12, fontweight='bold', color='#1B365D', family='serif')
axes[2].set_ylim(1800, 3500)
for i, txt in enumerate([2100, 2700, 3200]):
    axes[2].annotate(f"{txt}个", (years[i], txt), textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold', color='#1B365D')
axes[2].set_facecolor('#FAF9F5')
axes[2].grid(axis='y', linestyle='--', alpha=0.5)

# Apply styling to all subplots
for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#d6d3d1')
    ax.spines['bottom'].set_color('#d6d3d1')
    ax.tick_params(colors='#5e5d59')

plt.tight_layout()
chart1_path = os.path.join(out_dir, "chart1_development.png")
plt.savefig(chart1_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"Chart 1 saved to: {chart1_path}")


# ----------------- CHART 2: 人才供需对比分析 -----------------
categories = ['艺术+科技复合型人才', '纯艺术设计类人才', '纯数字技术类人才']
demand = [3200, 1800, 2100]
supply = [460, 1620, 1580]

x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6.5), facecolor='#FAF9F5')
ax.set_facecolor('#FAF9F5')

rects1 = ax.bar(x - width/2, demand, width, label='年均人才需求总量', color='#002FA7')
rects2 = ax.bar(x + width/2, supply, width, label='省内高校年均人才供给量', color='#c96442')

ax.set_title('云南省智慧文旅与非遗数字化领域人才供需对比', fontsize=15, fontweight='bold', color='#1B365D', pad=20, family='serif')
ax.set_ylabel('人数 (人)', fontsize=12, color='#1B365D')
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11, fontweight='bold', color='#1B365D')
ax.legend(frameon=False, fontsize=11)

# Annotate bars
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height}人',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color='#5e5d59')

autolabel(rects1)
autolabel(rects2)

# Supply percentage annotations
percentages = ['供给占比 <15%', '供给占比 90%', '供给占比 75.2%']
for i in range(len(categories)):
    ax.text(i, max(demand[i], supply[i]) + 150, percentages[i], ha='center', va='bottom', color='#A32D2D', fontweight='bold', fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="#FAF9F5", ec="#d6d3d1", lw=1))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#d6d3d1')
ax.spines['bottom'].set_color('#d6d3d1')
ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
chart2_path = os.path.join(out_dir, "chart2_talent_supply.png")
plt.savefig(chart2_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"Chart 2 saved to: {chart2_path}")


# ----------------- CHART 3: 岗位能力匹配对比 -----------------
jobs = ['AI文旅内容设计师\n(AIGC应用+民族文化创意)', '沉浸式文旅场景设计师\n(交互设计+空间艺术+虚拟搭建)', '非遗数字化设计师\n(传统工艺+数字建模+IP转化)']
gaps = [78, 82, 75]

fig, ax = plt.subplots(figsize=(10, 5), facecolor='#FAF9F5')
ax.set_facecolor('#FAF9F5')

y_pos = np.arange(len(jobs))
bars = ax.barh(y_pos, gaps, height=0.5, color='#A32D2D', alpha=0.9)

ax.set_yticks(y_pos)
ax.set_yticklabels(jobs, fontsize=11, fontweight='bold', color='#1B365D')
ax.invert_yaxis()  # top-down

# Add title and labels
ax.set_title('核心岗位人才短板反馈占比 (受访企业反馈)', fontsize=15, fontweight='bold', color='#1B365D', pad=20, family='serif')
ax.set_xlabel('占比 (%)', fontsize=12, color='#1B365D')
ax.set_xlim(0, 100)

# Annotate values
for bar in bars:
    width = bar.get_width()
    ax.text(width + 1.5, bar.get_y() + bar.get_height()/2, f'{width}%',
            ha='left', va='center', fontsize=11, fontweight='bold', color='#A32D2D')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#d6d3d1')
ax.spines['bottom'].set_color('#d6d3d1')
ax.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()
chart3_path = os.path.join(out_dir, "chart3_skill_gap.png")
plt.savefig(chart3_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"Chart 3 saved to: {chart3_path}")
