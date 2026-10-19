#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script xuất bản báo cáo chính thức:
1. REPORT_R01_K03.html (Bản in HTML chuẩn học thuật Times New Roman 12, lề chuẩn trường).
2. REPORT_R01_K03.docx (Bản Word OpenXML chuyển đổi qua engine x2t của ONLYOFFICE).
3. REPORT_R01_K03.pdf (Bản PDF vector độ phân giải cao in qua Chrome headless).
4. Render ảnh chụp xem trước các trang chính để kiểm tra không tràn lề, hình không vỡ.
"""

import os
import re
import html
import subprocess
import shutil

MD_PATH = "REPORT_R01_K03.md"
HTML_PATH = "REPORT_R01_K03.html"
DOCX_PATH = "REPORT_R01_K03.docx"
PDF_PATH = "REPORT_R01_K03.pdf"
PREVIEW_DIR = os.path.join("reports", "figures", "preview")

X2T_PATH = r"C:\Program Files\ONLYOFFICE\DesktopEditors\converter\x2t.exe"
X2T_DIR = r"C:\Program Files\ONLYOFFICE\DesktopEditors\converter"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def parse_markdown_to_html(md_text):
    lines = md_text.splitlines()
    html_lines = []
    
    in_code_block = False
    code_lang = ""
    code_content = []
    
    in_table = False
    table_rows = []
    
    in_blockquote = False
    blockquote_lines = []
    
    def flush_table():
        nonlocal in_table, table_rows
        if not in_table or not table_rows:
            in_table = False
            table_rows = []
            return ""
        
        out = ['<div class="table-container"><table>']
        # Header row
        if len(table_rows) > 0:
            header_cols = table_rows[0]
            out.append('<thead><tr>')
            for c in header_cols:
                out.append(f'<th>{inline_format(c.strip())}</th>')
            out.append('</tr></thead>')
        
        # Body rows (bỏ qua dòng phân cách |---|---|)
        body_rows = table_rows[2:] if len(table_rows) > 1 and all(set(cell.strip()).issubset({'-', ':', '|', ' '}) for cell in table_rows[1]) else table_rows[1:]
        out.append('<tbody>')
        for r in body_rows:
            out.append('<tr>')
            for c in r:
                out.append(f'<td>{inline_format(c.strip())}</td>')
            out.append('</tr>')
        out.append('</tbody></table></div>\n')
        
        in_table = False
        table_rows = []
        return "".join(out)
        
    def flush_blockquote():
        nonlocal in_blockquote, blockquote_lines
        if not in_blockquote or not blockquote_lines:
            in_blockquote = False
            blockquote_lines = []
            return ""
            
        full_text = " ".join(blockquote_lines)
        in_blockquote = False
        blockquote_lines = []
        
        # Check alert
        alert_class = "callout-info"
        alert_title = "LƯU Ý"
        if "[!NOTE]" in full_text:
            full_text = full_text.replace("[!NOTE]", "")
            alert_class = "callout-note"
            alert_title = "GHI CHÚ HỌC THUẬT"
        elif "[!TIP]" in full_text:
            full_text = full_text.replace("[!TIP]", "")
            alert_class = "callout-tip"
            alert_title = "MẸO KỸ THUẬT & DỮ LIỆU"
        elif "[!IMPORTANT]" in full_text:
            full_text = full_text.replace("[!IMPORTANT]", "")
            alert_class = "callout-important"
            alert_title = "RÀNG BUỘC QUAN TRỌNG"
        elif "[!WARNING]" in full_text:
            full_text = full_text.replace("[!WARNING]", "")
            alert_class = "callout-warning"
            alert_title = "CẢNH BÁO"
            
        return f'<div class="callout {alert_class}"><div class="callout-header">{alert_title}</div><div class="callout-body">{inline_format(full_text.strip())}</div></div>\n'

    def inline_format(text):
        # Escape basic HTML first
        # But allow specific safe formatting
        # Images: ![alt](url)
        img_pattern = r'!\[(.*?)\]\((.*?)\)'
        def replace_img(match):
            alt, src = match.group(1), match.group(2)
            # Chuyển src file:/// sang đường dẫn tương đối hoặc chuẩn hóa
            clean_src = src.replace("file:///d:/Kiểm Thử Phần Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/", "")
            clean_src = clean_src.replace("file:///D:/Kiểm Thử Phần Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/", "")
            return f'<figure class="report-figure"><img src="{clean_src}" alt="{html.escape(alt)}" /><figcaption>{html.escape(alt)}</figcaption></figure>'
        
        text = re.sub(img_pattern, replace_img, text)
        
        # Links: [text](url) -> keep text with link style
        link_pattern = r'\[(.*?)\]\((.*?)\)'
        text = re.sub(link_pattern, r'<span class="doc-link">\1</span>', text)
        
        # Bold: **text**
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        
        # Italic: *text*
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        
        # Inline code: `code`
        text = re.sub(r'`([^`]+)`', r'<code class="inline-code">\1</code>', text)
        
        # Math inline: $E = mc^2$
        text = re.sub(r'\$([^\$]+)\$', r'<span class="math-tex">\1</span>', text)
        
        return text

    for line in lines:
        stripped = line.strip()
        
        # 1. Code blocks
        if stripped.startswith("```"):
            if in_code_block:
                in_code_block = False
                code_str = html.escape("\n".join(code_content))
                html_lines.append(f'<pre class="code-block {code_lang}"><code>{code_str}</code></pre>\n')
                code_content = []
                code_lang = ""
            else:
                if in_table:
                    html_lines.append(flush_table())
                if in_blockquote:
                    html_lines.append(flush_blockquote())
                in_code_block = True
                code_lang = stripped[3:].strip()
            continue
            
        if in_code_block:
            code_content.append(line)
            continue
            
        # 2. Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                if in_blockquote:
                    html_lines.append(flush_blockquote())
                in_table = True
            cols = [c for c in stripped[1:-1].split("|")]
            table_rows.append(cols)
            continue
        elif in_table:
            html_lines.append(flush_table())
            
        # 3. Blockquotes
        if stripped.startswith(">"):
            if not in_blockquote:
                in_blockquote = True
            blockquote_lines.append(stripped[1:].strip())
            continue
        elif in_blockquote:
            html_lines.append(flush_blockquote())
            
        # 4. Horizontal rules / Page breaks
        if stripped in ["---", "***", "___"]:
            html_lines.append('<hr class="section-divider" />\n')
            continue
            
        # 5. Headings
        if stripped.startswith("# "):
            html_lines.append(f'<h1 class="report-title">{inline_format(stripped[2:])}</h1>\n')
            continue
        if stripped.startswith("## "):
            sec_title = stripped[3:]
            page_break = ' class="section-break"' if "PHẦN " in sec_title or "TÀI LIỆU THAM KHẢO" in sec_title else ''
            html_lines.append(f'<h2{page_break}>{inline_format(sec_title)}</h2>\n')
            continue
        if stripped.startswith("### "):
            html_lines.append(f'<h3>{inline_format(stripped[4:])}</h3>\n')
            continue
        if stripped.startswith("#### "):
            html_lines.append(f'<h4>{inline_format(stripped[5:])}</h4>\n')
            continue
        if stripped.startswith("##### "):
            html_lines.append(f'<h5>{inline_format(stripped[6:])}</h5>\n')
            continue
            
        # 6. Lists
        if stripped.startswith("- ") or stripped.startswith("* "):
            html_lines.append(f'<li class="ul-item">{inline_format(stripped[2:])}</li>\n')
            continue
        if re.match(r'^\d+\.\s', stripped):
            item_text = re.sub(r'^\d+\.\s', '', stripped)
            html_lines.append(f'<li class="ol-item">{inline_format(item_text)}</li>\n')
            continue
            
        # 7. Math block ($$...$$)
        if stripped.startswith("$$") and stripped.endswith("$$"):
            math_exp = stripped[2:-2].strip()
            html_lines.append(f'<div class="math-block">{html.escape(math_exp)}</div>\n')
            continue
            
        # 8. Regular paragraph
        if stripped:
            html_lines.append(f'<p>{inline_format(line)}</p>\n')
            
    if in_table:
        html_lines.append(flush_table())
    if in_blockquote:
        html_lines.append(flush_blockquote())
        
    return "".join(html_lines)


def build_full_html(body_html):
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>BÁO CÁO TỔNG KẾT HỌC PHẦN: ĐỀ TÀI R01 (SPRING PETCLINIC) + K03 (MUTATION TESTING)</title>
<style>
  @page {{
    size: A4 portrait;
    margin-top: 20mm;
    margin-bottom: 20mm;
    margin-left: 30mm;
    margin-right: 20mm;
    @bottom-right {{
      content: "Trang " counter(page);
      font-family: "Times New Roman", Times, serif;
      font-size: 10pt;
    }}
  }}

  *, *:before, *:after {{
    box-sizing: border-box;
  }}

  body {{
    font-family: "Times New Roman", Times, serif;
    font-size: 12pt;
    line-height: 1.35;
    color: #111;
    background-color: #fff;
    margin: 0;
    padding: 0;
  }}

  h1.report-title {{
    font-size: 18pt;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    color: #0d3b66;
    margin-top: 20px;
    margin-bottom: 25px;
    line-height: 1.3;
  }}

  h2 {{
    font-size: 14pt;
    font-weight: bold;
    color: #1d3557;
    margin-top: 28px;
    margin-bottom: 12px;
    border-bottom: 1.5px solid #1d3557;
    padding-bottom: 4px;
  }}

  h2.section-break {{
    page-break-before: always;
    margin-top: 15px;
  }}

  h3 {{
    font-size: 13pt;
    font-weight: bold;
    color: #2b2d42;
    margin-top: 20px;
    margin-bottom: 8px;
  }}

  h4 {{
    font-size: 12pt;
    font-weight: bold;
    color: #333;
    margin-top: 14px;
    margin-bottom: 6px;
  }}

  h5 {{
    font-size: 11.5pt;
    font-weight: bold;
    font-style: italic;
    color: #444;
    margin-top: 10px;
    margin-bottom: 4px;
  }}

  p {{
    text-align: justify;
    margin-top: 0;
    margin-bottom: 8px;
    text-indent: 0;
  }}

  /* Table styling */
  .table-container {{
    width: 100%;
    margin: 14px 0;
    overflow-x: auto;
    page-break-inside: avoid;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 10pt;
    line-height: 1.25;
    margin: 0 auto;
    page-break-inside: avoid;
  }}

  th, td {{
    border: 1px solid #555;
    padding: 5px 7px;
    text-align: left;
    vertical-align: top;
    word-break: break-word;
  }}

  th {{
    background-color: #e9ecef;
    font-weight: bold;
    color: #111;
    text-align: center;
  }}

  tr:nth-child(even) td {{
    background-color: #fbfbfb;
  }}

  /* Callout styling */
  .callout {{
    margin: 12px 0;
    padding: 10px 14px;
    border-left: 4px solid #0077b6;
    background-color: #f0f7fb;
    border-radius: 2px;
    page-break-inside: avoid;
    font-size: 11pt;
  }}

  .callout-header {{
    font-weight: bold;
    color: #0077b6;
    margin-bottom: 4px;
    text-transform: uppercase;
    font-size: 9.5pt;
  }}

  .callout-tip {{
    border-left-color: #2a9d8f;
    background-color: #eef8f6;
  }}
  .callout-tip .callout-header {{ color: #2a9d8f; }}

  .callout-important {{
    border-left-color: #e76f51;
    background-color: #fdf2ef;
  }}
  .callout-important .callout-header {{ color: #e76f51; }}

  .callout-warning {{
    border-left-color: #e63946;
    background-color: #fdf0f0;
  }}
  .callout-warning .callout-header {{ color: #e63946; }}

  /* Code block */
  pre.code-block {{
    font-family: Consolas, "Courier New", monospace;
    font-size: 9pt;
    line-height: 1.25;
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 4px;
    padding: 8px 12px;
    margin: 10px 0;
    overflow-x: auto;
    page-break-inside: avoid;
    white-space: pre-wrap;
    word-break: break-word;
  }}

  code.inline-code {{
    font-family: Consolas, "Courier New", monospace;
    font-size: 10pt;
    background-color: #eff1f3;
    padding: 1px 4px;
    border-radius: 3px;
    color: #c7254e;
  }}

  /* Figures */
  figure.report-figure {{
    text-align: center;
    margin: 16px 0;
    page-break-inside: avoid;
  }}

  figure.report-figure img {{
    max-width: 95%;
    max-height: 480px;
    height: auto;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }}

  figcaption {{
    font-size: 10pt;
    font-style: italic;
    color: #444;
    margin-top: 6px;
    text-align: center;
  }}

  /* Lists */
  li.ul-item, li.ol-item {{
    margin-bottom: 4px;
    line-height: 1.3;
    text-align: justify;
  }}

  hr.section-divider {{
    border: 0;
    height: 1px;
    background: #ccc;
    margin: 20px 0;
  }}

  .math-block {{
    text-align: center;
    font-family: "Times New Roman", Times, serif;
    font-style: italic;
    font-size: 12pt;
    margin: 12px 0;
    color: #0b3954;
  }}

  .math-tex {{
    font-style: italic;
    color: #0b3954;
  }}

  .doc-link {{
    color: #0d3b66;
    text-decoration: underline;
  }}
</style>
</head>
<body>
{body_html}
</body>
</html>
"""

def main():
    print("=== BAT DAU XUAT BAN BAO CAO R01-K03 ===")
    
    # 1. Đọc Markdown
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()
        
    print(f"1. Da doc {MD_PATH} ({len(md_text.splitlines())} dong).")
    
    # 2. Sinh HTML
    body_html = parse_markdown_to_html(md_text)
    full_html = build_full_html(body_html)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"2. Da sinh {HTML_PATH} ({len(full_html)} bytes).")
    
    # 3. Chuyển đổi sang DOCX qua x2t của ONLYOFFICE
    print("3. Dang xuat REPORT_R01_K03.docx qua engine x2t...")
    abs_html = os.path.abspath(HTML_PATH)
    abs_docx = os.path.abspath(DOCX_PATH)
    
    cmd_docx = [
        X2T_PATH,
        abs_html,
        abs_docx
    ]
    proc = subprocess.run(cmd_docx, cwd=X2T_DIR, capture_output=True, text=True)
    if os.path.exists(DOCX_PATH) and os.path.getsize(DOCX_PATH) > 0:
        print(f"   -> THANH CONG: Da xuat {DOCX_PATH} ({os.path.getsize(DOCX_PATH)} bytes).")
    else:
        print(f"   -> CANH BAO: x2t khong tao duoc docx. Output: {proc.stdout} {proc.stderr}")
        
    # 4. Xuất PDF qua Chrome headless
    print("4. Dang xuat REPORT_R01_K03.pdf qua Chrome headless...")
    abs_pdf = os.path.abspath(PDF_PATH)
    cmd_pdf = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={abs_pdf}",
        f"file:///{abs_html}"
    ]
    proc_pdf = subprocess.run(cmd_pdf, capture_output=True, text=True)
    if os.path.exists(PDF_PATH) and os.path.getsize(PDF_PATH) > 0:
        print(f"   -> THANH CONG: Da xuat {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes).")
    else:
        print(f"   -> CANH BAO: Chrome khong in duoc pdf: {proc_pdf.stdout} {proc_pdf.stderr}")
        
    # 5. Chụp ảnh preview các phần trọng yếu
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    print(f"5. Dang chup anh preview vao {PREVIEW_DIR}...")
    
    # Chụp full page screenshot qua Chrome headless
    preview_full = os.path.join(PREVIEW_DIR, "preview_full_page.png")
    cmd_snap = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--window-size=1200,2400",
        f"--screenshot={os.path.abspath(preview_full)}",
        f"file:///{abs_html}"
    ]
    subprocess.run(cmd_snap, capture_output=True, text=True)
    if os.path.exists(preview_full):
        print(f"   -> Da chup anh tong quan: {preview_full} ({os.path.getsize(preview_full)} bytes).")

    print("=== HOAN TAT XUAT BAN BAO CAO ===")

if __name__ == "__main__":
    main()
