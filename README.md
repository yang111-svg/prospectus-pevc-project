# PE/VC上市前投资信息抽取项目

<<<<<<< Updated upstream
=======
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
## 项目简介
本项目旨在利用AI工具和程序化流程，从上市公司招股说明书中识别并提取其上市前PE/VC投资相关信息。

## 仓库结构

```
.
├── README.md                          # 项目说明
├── company_lists/                     # 企业清单
│   └── week1_public_samples.csv       # 第一周公共样本
├── source_notes/                      # 数据来源说明
│   ├── data_sources.md               # 数据来源
│   ├── prospectus_download_method.md # 招股说明书下载方法
│   └── version_rules.md              # 文件版本规则
├── code/                             # 代码
│   ├── 01_build_company_list/        # 构建企业清单
│   ├── 02_fetch_prospectus_urls/     # 获取招股书URL
│   ├── 03_download_pdfs/             # 下载PDF
│   ├── 04_parse_pdf_to_markdown/     # PDF解析
│   ├── 05_locate_relevant_sections/  # 章节定位
│   ├── 06_extract_pevc_info/         # 信息抽取
│   └── 07_validate_outputs/          # 输出校验
├── outputs/                          # 输出结果
│   ├── week1_sample_json/            # 第一周JSON输出
│   └── week1_candidate_texts/        # 候选文本
├── logs/                             # 日志
│   ├── download_log.csv              # 下载日志
│   ├── parse_log.csv                 # 解析日志
│   ├── locate_log.csv                # 定位日志
│   ├── extraction_log.csv            # 抽取日志
│   ├── validation_log.csv            # 校验日志
│   └── error_cases.md                # 错误案例
├── review/                           # 互查记录
│   ├── week3_intra_group_review.csv  # 组内互查
│   ├── week4_inter_group_review_given.csv    # 组间检查（给出）
│   └── week4_inter_group_review_received.csv # 组间检查（收到）
├── weekly_reports/                   # 周报
│   └── week1.md                      # 第一周周报
└── presentation/                     # 最终汇报
    ├── final_presentation.pptx
    └── final_presentation.pdf
```

## 第一周任务
处理8个公共样本，跑通从PDF到JSON的完整闭环。

### 8个公共样本
<<<<<<< Updated upstream
| sample_id | 板块 | 公司简称 | 股票代码 |
|-----------|------|----------|----------|
| MB001 | 主板 | 三联锻造 | 001282 |
| MB002 | 主板 | 友升股份 | 603418 |
| GEM001 | 创业板 | 黄山谷捷 | 301581 |
| GEM002 | 创业板 | 云汉芯城 | 301563 |
| STAR001 | 科创板 | 赛分科技 | 688758 |
| STAR002 | 科创板 | 影石创新 | 688775 |
| BSE001 | 北交所 | 三协电机 | 920100 |
| BSE002 | 北交所 | 星图测控 | 920116 |
=======
| sample_id | 板块 | 公司简称 | 股票代码 | 来源平台 |
|-----------|------|----------|----------|----------|
| MB001 | 主板 | 三联锻造 | 001282 | 巨潮资讯 |
| MB002 | 主板 | 友升股份 | 603418 | 巨潮资讯 |
| GEM001 | 创业板 | 黄山谷捷 | 301581 | 巨潮资讯 |
| GEM002 | 创业板 | 云汉芯城 | 301563 | 巨潮资讯 |
| STAR001 | 科创板 | 赛分科技 | 688758 | 巨潮资讯 |
| STAR002 | 科创板 | 影石创新 | 688775 | 巨潮资讯 |
| BSE001 | 北交所 | 三协电机 | 920100 | 北交所 |
| BSE002 | 北交所 | 星图测控 | 920116 | 北交所 |
>>>>>>> Stashed changes

## 处理流程

```
企业清单构建
    ↓
招股说明书来源确认
    ↓
PDF下载与文件识别
    ↓
PDF解析为Markdown或文本
    ↓
目录识别与相关章节定位
    ↓
关键词检索与候选文本截取
    ↓
融资事件与投资方信息抽取
    ↓
结构化JSON输出
    ↓
字段校验与异常记录
    ↓
人工复核与小组互查
```

## 团队成员
- 成员1：杨苗鑫
- 成员2：赵秉清

## 提交记录
- Week 1: 公共样本最小闭环
<<<<<<< Updated upstream
=======
>>>>>>> parent of 0fa3f90 (Update team member names in README)
>>>>>>> Stashed changes
