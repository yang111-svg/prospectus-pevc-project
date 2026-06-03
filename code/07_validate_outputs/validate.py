import csv
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("C:/Users/HP/Desktop/prospectus-pevc-project")
JSON_DIR = BASE_DIR / "outputs" / "week1_sample_json"
COMPANY_LIST = BASE_DIR / "company_lists" / "week1_public_samples.csv"
LOG_FILE = BASE_DIR / "logs" / "validation_log.csv"

def validate_json(json_file):
    """校验JSON文件"""
    result = {
        "valid": False,
        "missing_fields": [],
        "type_errors": [],
        "logic_errors": [],
        "review_required": False
    }
    
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 检查必需字段
        required_company_fields = ["company_name", "stock_code", "exchange", "board"]
        required_processing_fields = ["download_status", "parse_status", "locate_status", "extract_status"]
        
        if "company" not in data:
            result["missing_fields"].append("company")
        else:
            for field in required_company_fields:
                if field not in data["company"] or not data["company"][field]:
                    result["missing_fields"].append(f"company.{field}")
        
        if "financing_events" not in data:
            result["missing_fields"].append("financing_events")
        
        if "processing" not in data:
            result["missing_fields"].append("processing")
        else:
            for field in required_processing_fields:
                if field not in data["processing"] or not data["processing"][field]:
                    result["missing_fields"].append(f"processing.{field}")
        
        # 检查逻辑错误
        if "financing_events" in data:
            events = data["financing_events"]
            if not events:
                result["logic_errors"].append("financing_events为空列表")
            else:
                for i, event in enumerate(events):
                    if not event.get("evidence_text"):
                        result["logic_errors"].append(f"事件{i+1}缺少evidence_text")
        
        # 判断是否需要复核
        if result["missing_fields"] or result["logic_errors"]:
            result["review_required"] = True
        
        result["valid"] = len(result["missing_fields"]) == 0 and len(result["logic_errors"]) == 0
        
    except Exception as e:
        result["logic_errors"].append(f"JSON解析错误: {str(e)}")
    
    return result

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
    
    json_file = None
    for f in JSON_DIR.glob(f"{code}*.json"):
        json_file = f
        break
    
    if not json_file:
        print(f"找不到JSON: {code}")
        results.append({"code": code, "name": name, "valid": False, "missing": "JSON文件不存在", "type": "", "logic": "", "review": True})
        continue
    
    print(f"校验: {name} ({code})")
    result = validate_json(json_file)
    
    status = "valid" if result["valid"] else "invalid"
    print(f"  状态: {status}")
    if result["missing_fields"]:
        print(f"  缺失字段: {', '.join(result['missing_fields'])}")
    if result["logic_errors"]:
        print(f"  逻辑错误: {', '.join(result['logic_errors'])}")
    
    results.append({
        "code": code,
        "name": name,
        "valid": result["valid"],
        "missing": "; ".join(result["missing_fields"]),
        "type": "; ".join(result["type_errors"]),
        "logic": "; ".join(result["logic_errors"]),
        "review": result["review_required"]
    })

# 更新日志
log_exists = LOG_FILE.exists()
with open(LOG_FILE, "a", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    if not log_exists:
        w.writerow(["company_name", "stock_code", "json_path", "validation_status", "missing_fields", "type_errors", "logic_errors", "review_required"])
    for r in results:
        w.writerow([r["name"], r["code"], f"outputs/week1_sample_json/{r['code']}_pevc_info.json", "valid" if r["valid"] else "invalid", r["missing"], r["type"], r["logic"], "yes" if r["review"] else "no"])

print("\n校验日志已更新")
print(f"\n完成: {sum(1 for x in results if x['valid'])}/{len(results)} 通过校验")
