import csv
import json
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("C:/Users/HP/Desktop/prospectus-pevc-project")
INPUT_DIR = BASE_DIR / "outputs" / "week1_candidate_texts"
OUTPUT_DIR = BASE_DIR / "outputs" / "week1_sample_json"
COMPANY_LIST = BASE_DIR / "company_lists" / "week1_public_samples.csv"
LOG_FILE = BASE_DIR / "logs" / "extraction_log.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_pevc_info(candidate_text, company_info):
    """从候选文本中提取PE/VC信息"""
    events = []
    text = candidate_text
    
    # 查找融资事件模式
    patterns = [
        r"(\d{4})年?(\d{1,2})月?\s*([\u589e\u8d44\u80a1\u6743\u8f6c\u8ba9\u51fa\u8d44\u8ba4\u8d2d\u5165\u80a1]+)\s*([^，。\n]{2,20})\s*([^，。\n]{2,30})",
        r"([\u589e\u8d44\u80a1\u6743\u8f6c\u8ba9]+)\s*([^，。\n]{2,20})\s*(\d{4})年",
        r"([\u6295\u8d44\u8005|PE|VC|\u521b\u6295|\u79c1\u52df\u80a1\u6743]+)\s*([^，。\n]{2,30})\s*(\d{4})年",
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            event = {
                "event_type": "增资" if "增" in match.group(0) else "股权转让" if "转让" in match.group(0) else "其他",
                "date": match.group(1) if len(match.groups()) > 0 else "",
                "amount": "",
                "investor": "",
                "valuation_pre": "",
                "valuation_post": "",
                "share_percentage": "",
                "lock_up_period": "",
                "evidence_text": match.group(0)[:200]
            }
            events.append(event)
    
    # 去重
    seen = set()
    unique_events = []
    for e in events:
        key = e["evidence_text"]
        if key not in seen:
            seen.add(key)
            unique_events.append(e)
    
    return unique_events[:10]  # 最多返回10个事件

def process_company(company):
    code = company["stock_code"]
    name = company["company_name"]
    
    # 查找候选文本文件
    candidate_file = None
    for f in INPUT_DIR.glob(f"{code}*候选文本.md"):
        candidate_file = f
        break
    
    if not candidate_file:
        return {"success": False, "error": "候选文本文件不存在"}
    
    with open(candidate_file, "r", encoding="utf-8") as f:
        candidate_text = f.read()
    
    # 提取PE/VC信息
    events = extract_pevc_info(candidate_text, company)
    
    # 构建JSON输出
    output = {
        "company": {
            "company_name": name,
            "stock_code": code,
            "exchange": company.get("exchange", ""),
            "board": company.get("board", ""),
            "listing_date": company.get("listing_date", ""),
            "prospectus_title": company.get("prospectus_title", ""),
            "prospectus_url": company.get("prospectus_url", ""),
            "prospectus_version": company.get("prospectus_version", ""),
            "prospectus_date": company.get("prospectus_date", "")
        },
        "financing_events": events,
        "processing": {
            "download_status": company.get("download_status", ""),
            "parse_status": company.get("parse_status", ""),
            "locate_status": company.get("locate_status", ""),
            "extract_status": "success" if events else "partial",
            "review_status": "待复核",
            "notes": company.get("notes", "")
        }
    }
    
    # 保存JSON
    output_file = OUTPUT_DIR / f"{code}_{name.split('股份')[0]}_pevc_info.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    return {
        "success": True,
        "events_count": len(events),
        "output_file": str(output_file)
    }

# 读取企业清单
companies = []
with open(COMPANY_LIST, "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        companies.append(row)

print(f"共 {len(companies)} 家公司\n")

results = []
for company in companies:
    code = company["stock_code"]
    name = company["company_name"]
    print(f"抽取: {name} ({code})")
    
    result = process_company(company)
    if result["success"]:
        print(f"  事件数: {result['events_count']} -> {Path(result['output_file']).name}")
    else:
        print(f"  失败: {result['error']}")
    
    results.append({
        "code": code,
        "name": name,
        "status": "success" if result["success"] else "fail",
        "events": result.get("events_count", 0),
        "file": result.get("output_file", ""),
        "error": result.get("error", "")
    })

# 更新企业清单
rows = []
with open(COMPANY_LIST, "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        for r in results:
            if row["stock_code"] == r["code"]:
                if r["status"] == "success" and r["events"] > 0:
                    row["extract_status"] = "success"
                elif r["status"] == "success":
                    row["extract_status"] = "partial"
                else:
                    row["extract_status"] = "fail"
        rows.append(row)

with open(COMPANY_LIST, "w", encoding="utf-8", newline="") as f:
    csv.DictWriter(f, fieldnames=rows[0].keys()).writeheader()
    csv.DictWriter(f, fieldnames=rows[0].keys()).writerows(rows)

print("\n企业清单已更新")

# 更新日志
log_exists = LOG_FILE.exists()
with open(LOG_FILE, "a", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    if not log_exists:
        w.writerow(["company_name", "stock_code", "candidate_text_path", "model_name", "prompt_version", "json_path", "status", "error_message"])
    for r in results:
        w.writerow([r["name"], r["code"], f"outputs/week1_candidate_texts/{r['code']}_候选文本.md", "rule-based", "v1", r["file"], r["status"], r["error"]])

print("抽取日志已更新")
print(f"\n完成: {sum(1 for x in results if x['status'] == 'success')}/{len(results)}")
