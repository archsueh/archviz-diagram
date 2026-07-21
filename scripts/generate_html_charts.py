import os
import sys
from pathlib import Path

# Repo root on path so we can import engine
_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO))

from archviz_diagram.engine import render

# Output directory (override with ARCHVIZ_CHART_OUT)
out_dir = os.environ.get("ARCHVIZ_CHART_OUT", str(_REPO / "exports" / "charts"))
os.makedirs(out_dir, exist_ok=True)

# ----------------- CHART 1a: 全省文旅总收入 -----------------
data_1a = {
    "labels": ["2023年", "2024年", "2025年"],
    "datasets": [
        {
            "label": "全省文旅总收入 (万亿元)",
            "data": [1.44, 1.49, 1.27]
        }
    ]
}
html_1a = render("line-chart", data_1a, {"theme": "warm-paper", "title": "全省文旅总收入趋势 (2023-2025)"})
path_1a = os.path.join(out_dir, "chart1a_development_revenue.html")
with open(path_1a, "w", encoding="utf-8") as f:
    f.write(html_1a)
print(f"Saved: {path_1a}")

# ----------------- CHART 1b: 互联网服务业增速 -----------------
data_1b = {
    "labels": ["2023年", "2024年", "2025年"],
    "datasets": [
        {
            "label": "互联网和相关服务业增速 (%)",
            "data": [48.2, 54.5, 51.7]
        }
    ]
}
html_1b = render("line-chart", data_1b, {"theme": "warm-paper", "title": "互联网和相关服务业增速趋势 (2023-2025)"})
path_1b = os.path.join(out_dir, "chart1b_development_growth.html")
with open(path_1b, "w", encoding="utf-8") as f:
    f.write(html_1b)
print(f"Saved: {path_1b}")

# ----------------- CHART 1c: 数字创意类岗位新增数量 -----------------
data_1c = {
    "labels": ["2023年", "2024年", "2025年"],
    "datasets": [
        {
            "label": "数字创意类岗位新增数量 (个)",
            "data": [2100, 2700, 3200]
        }
    ]
}
html_1c = render("line-chart", data_1c, {"theme": "warm-paper", "title": "数字创意类岗位新增数量趋势 (2023-2025)"})
path_1c = os.path.join(out_dir, "chart1c_development_jobs.html")
with open(path_1c, "w", encoding="utf-8") as f:
    f.write(html_1c)
print(f"Saved: {path_1c}")

# ----------------- CHART 2: 人才供需对比 -----------------
data_2 = {
    "labels": ["艺术+科技复合型人才", "纯艺术设计类人才", "纯数字技术类人才"],
    "datasets": [
        {
            "label": "年均人才需求总量",
            "values": [3200, 1800, 2100]
        },
        {
            "label": "省内高校年均人才供给量",
            "values": [460, 1620, 1580]
        }
    ]
}
html_2 = render("stacked-bar", data_2, {"theme": "warm-paper", "title": "云南省智慧文旅与非遗数字化领域人才供需对比"})
path_2 = os.path.join(out_dir, "chart2_talent_supply.html")
with open(path_2, "w", encoding="utf-8") as f:
    f.write(html_2)
print(f"Saved: {path_2}")

# ----------------- CHART 3: 岗位能力匹配对比 -----------------
data_3 = {
    "axes": [
        "AI文旅内容设计师 (AIGC应用+民族文化)",
        "沉浸式文旅场景设计师 (交互设计+空间艺术)",
        "非遗数字化设计师 (传统工艺+数字建模)"
    ],
    "datasets": [
        {
            "label": "核心岗位人才短板反馈占比 (%)",
            "values": [78, 82, 75]
        }
    ]
}
html_3 = render("radar", data_3, {"theme": "warm-paper", "title": "核心岗位人才短板反馈占比 (受访企业)"})
path_3 = os.path.join(out_dir, "chart3_skill_gap.html")
with open(path_3, "w", encoding="utf-8") as f:
    f.write(html_3)
print(f"Saved: {path_3}")
