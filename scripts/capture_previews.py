#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chụp các lát cắt màn hình (screenshots) từng phần quan trọng của báo cáo HTML:
- cover_page.png: Trang bìa, thông tin nhóm, phân công 5 thành viên.
- toc_and_lists.png: Mục lục, danh mục bảng, danh mục hình ảnh.
- section_g_metrics.png: Bảng G.1, Bảng G.2, Bảng G.3, Hình G.1, Hình G.2.
- section_g_figures.png: Hình G.3, Hình G.4, Code Smell Bảng G.4.
- section_g_rca.png: Bảng G.5, G.6 (RCA Error-Fault-Failure).
- section_g_proofs.png: Chứng minh đại số Boolean và CFG.
- section_h_cicd.png: Sơ đồ CI/CD và Hướng dẫn tái hiện 1-lệnh.
"""

import os
import subprocess

HTML_PATH = os.path.abspath("REPORT_R01_K03.html")
PREVIEW_DIR = os.path.abspath(os.path.join("reports", "figures", "preview"))
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(PREVIEW_DIR, exist_ok=True)

# Để chụp từng trang/khu vực một cách sắc nét, ta có thể tạo các HTML snippet nhỏ
# hoặc dùng CSS media print / scroll
with open("REPORT_R01_K03.html", "r", encoding="utf-8") as f:
    full_html = f.read()

# Tạo snippet cho Cover & TOC
# Tìm vị trí bắt đầu của các phần
pos_cover = full_html.find('<h1 class="report-title">')
pos_part_a = full_html.find('<h2>PHẦN A:')
pos_part_d = full_html.find('<h2>PHẦN D:')
pos_part_g = full_html.find('<h2>PHẦN G:')
pos_part_g3 = full_html.find('<h3>G.3.')
pos_part_g4 = full_html.find('<h3>G.4.')
pos_part_h = full_html.find('<h2>PHẦN H:')
pos_refs = full_html.find('<h2>TÀI LIỆU THAM KHẢO')

head_part = full_html[:full_html.find('<body>') + 6]
tail_part = "</body></html>"

sections = [
    ("preview_01_cover_and_toc.html", "preview_01_cover_and_toc.png", full_html[pos_cover:pos_part_a]),
    ("preview_02_part_d_rip.html", "preview_02_part_d_rip.png", full_html[pos_part_d:pos_part_d + 5000]),
    ("preview_03_part_g_metrics.html", "preview_03_part_g_metrics.png", full_html[pos_part_g:pos_part_g3]),
    ("preview_04_part_g_rca.html", "preview_04_part_g_rca.png", full_html[pos_part_g3:pos_part_g4]),
    ("preview_05_part_g_proofs.html", "preview_05_part_g_proofs.png", full_html[pos_part_g4:pos_part_h]),
    ("preview_06_part_h_cicd.html", "preview_06_part_h_cicd.png", full_html[pos_part_h:pos_refs])
]

for html_name, png_name, body_chunk in sections:
    html_file = os.path.join(PREVIEW_DIR, html_name)
    png_file = os.path.join(PREVIEW_DIR, png_name)
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(head_part + body_chunk + tail_part)
        
    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--window-size=1200,1600",
        f"--screenshot={png_file}",
        f"file:///{html_file}"
    ]
    subprocess.run(cmd, capture_output=True)
    if os.path.exists(png_file):
        print(f"Da chup: {png_name} ({os.path.getsize(png_file)} bytes)")

print("Hoan tat chup anh preview cac phan!")
