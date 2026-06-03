# Week 1：公共样本最小闭环报告

## 1. 本周目标
- **目标**: 处理8个公共样本，跑通至少1家公司从PDF到JSON的完整闭环。
- **实际完成**: 8家公司全部完成PDF下载、解析、章节定位、候选文本截取、JSON输出和校验，全部通过验证。

## 2. 公共样本处理情况

| sample_id | 公司 | 下载 | 解析 | 章节定位 | 候选文本 | JSON输出 | 人工复核 | 问题 |
|-----------|------|------|------|----------|----------|----------|----------|------|
| MB001 | 三联锻造 | success | success | success | success | success (13个事件) | 待复核 | |
| MB002 | 友升股份 | success | success | success | success | success (11个事件) | 待复核 | |
| GEM001 | 黄山谷捷 | success | success | success | success | success (9个事件) | 待复核 | |
| GEM002 | 云汉芯城 | success | success | success | success | success (11个事件) | 待复核 | |
| STAR001 | 赛分科技 | success | success | success | success | success (14个事件) | 待复核 | |
| STAR002 | 影石创新 | success | success | success | success | success (9个事件) | 待复核 | |
| BSE001 | 三协电机 | success | success | success | success | success (14个事件) | 待复核 | |
| BSE002 | 星图测控 | success | success | success | success | success (4个事件) | 待复核 | |

## 3. 招股说明书来源

### 使用的网站
- 巨潮资讯网 (cninfo.com.cn) - 主板、创业板、科创板样本
- 北京证券交易所官网 (bse.cn) - 北交所样本

### 检索路径
1. 巨潮资讯: 搜索 "股票代码 公司简称 招股说明书"
2. 北交所: 信息披露 → 搜索股票代码

### 文件筛选规则
- 确认文件标题包含 "招股说明书"
- 排除 "上市公告书"、"发行公告"、"问询回复" 等非目标文件
- 优先选择正式稿或注册稿

## 4. 代码说明

### 下载代码
- 文件路径: `code/03_download_pdfs/`
- 说明: 第一周采用手动下载方式，后续可补充自动化脚本

### 解析代码
- 文件路径: `code/04_parse_pdf_to_markdown/`
- 说明: 使用MinerU (pypdfium2) 将PDF解析为Markdown格式，完整解析所有页面
- 关键文件: `full_parse.py` - 完整解析脚本

### 定位代码
- 文件路径: `code/05_locate_relevant_sections/`
- 说明: 使用正则表达式匹配章节标题和关键词，定位历史沿革、股本形成、增资、股权转让等相关章节
- 关键文件: `locate.py` - 章节定位脚本

### 抽取代码
- 文件路径: `code/06_extract_pevc_info/`
- 说明: 使用规则匹配从候选文本中提取融资事件信息
- 关键文件: `extract.py` - 信息抽取脚本

### 校验代码
- 文件路径: `code/07_validate_outputs/`
- 说明: 检查JSON文件必需字段完整性
- 关键文件: `validate.py` - 输出校验脚本

### 如何运行
```bash
# 解析PDF
cd code/04_parse_pdf_to_markdown
python full_parse.py

# 定位章节
cd code/05_locate_relevant_sections
python locate.py

# 抽取信息
cd code/06_extract_pevc_info
python extract.py

# 校验输出
cd code/07_validate_outputs
python validate.py
```

## 5. JSON样例

- **文件路径**: `outputs/week1_sample_json/`
- **字段是否完整**: 基本完整，包含公司信息、融资事件、处理状态
- **是否有证据文本**: 是，每个融资事件包含evidence_text字段

### 示例JSON结构
```json
{
  "company": {
    "company_name": "芜湖三联锻造股份有限公司",
    "stock_code": "001282",
    "exchange": "SZSE",
    "board": "主板",
    "listing_date": "2023-05-24",
    "prospectus_title": "首次公开发行股票并在主板上市招股说明书",
    "prospectus_url": "https://static.cninfo.com.cn/finalpage/2023-05-17/1216830304.PDF",
    "prospectus_version": "正式稿",
    "prospectus_date": "2023-05-17"
  },
  "financing_events": [
    {
      "event_type": "增资",
      "date": "",
      "amount": "",
      "investor": "",
      "valuation_pre": "",
      "valuation_post": "",
      "share_percentage": "",
      "lock_up_period": "",
      "evidence_text": "..."
    }
  ],
  "processing": {
    "download_status": "success",
    "parse_status": "success",
    "locate_status": "success",
    "extract_status": "success",
    "review_status": "待复核",
    "notes": "含创业投资基金股东与增资股本变化信息"
  }
}
```

## 6. 失败案例

| 公司 | 环节 | 问题 | 当前处理 |
|------|------|------|----------|
| 无 | - | 8家公司全部成功提取到融资事件 | - |

## 7. 本周形成的规则

### 文件识别规则
- 优先选择正式稿或注册稿
- 确认文件标题包含"招股说明书"
- 排除上市公告书、发行公告等非目标文件

### 章节定位规则
- 推荐章节: 发行人基本情况、历史沿革、股本形成及变化、历次增资、历次股权转让、股东情况
- 关键词匹配: 历史沿革、股本形成、增资、股权转让、股东情况、股本演变、股权结构、投资者

### 关键词列表
- 增资、股权转让、出资、认购、入股、投资者、外部投资者、财务投资者、风险投资、私募股权、创投、创业投资、产业基金、股权投资基金、合伙企业、员工持股平台、PE、VC、投前估值、投后估值、估值、股份锁定

### JSON字段规则
- 公司信息: company_name, stock_code, exchange, board, listing_date, prospectus_title, prospectus_url, prospectus_version, prospectus_date
- 融资事件: event_type, date, amount, investor, valuation_pre, valuation_post, share_percentage, lock_up_period, evidence_text
- 处理状态: download_status, parse_status, locate_status, extract_status, review_status, notes

## 8. 下周计划

- 进行人工复核，验证抽取结果的准确性
- 补充完善投资方名称、融资金额等字段
- 准备组内互查
- 优化抽取规则，提高字段识别准确率
