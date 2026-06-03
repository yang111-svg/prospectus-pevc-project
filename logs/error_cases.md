# 失败案例记录

## 案例1：MinerU启动失败 - 缺少gradio组件
- **公司**: 全部8家公司（影响启动MinerU）
- **股票代码**: 不适用
- **环节**: 解析（PDF解析）
- **问题表现**: 双击"启动MinerU.bat"后报错 ModuleNotFoundError: No module named gradio
- **可能原因**: MinerU 3.2.1版本依赖gradio组件，但安装MinerU时未自动安装
- **已尝试方法**: 在命令提示符中执行 pip install gradio 安装gradio，安装成功后重新启动MinerU
- **当前状态**: 已解决
- **后续建议**: 安装MinerU时建议同时安装所有依赖

## 案例2：MinerU启动失败 - 缺少gradio_pdf组件
- **公司**: 全部8家公司（影响启动MinerU）
- **股票代码**: 不适用
- **环节**: 解析（PDF解析）
- **问题表现**: 安装gradio后重新启动MinerU，再次报错 ModuleNotFoundError: No module named gradio_pdf
- **可能原因**: MinerU的Web界面额外依赖gradio_pdf组件
- **已尝试方法**: 在命令提示符中执行 pip install gradio_pdf 安装gradio_pdf，安装成功后重新启动MinerU
- **当前状态**: 已解决

## 案例3：MinerU启动失败 - 启动脚本命令错误
- **公司**: 全部8家公司（影响启动MinerU）
- **股票代码**: 不适用
- **环节**: 解析（PDF解析）
- **问题表现**: 安装完依赖后，启动MinerU仍然报错 AttributeError: module mineru.cli.gradio_app has no attribute demo
- **可能原因**: MinerU 3.2.1版本中gradio_app模块没有demo函数，正确的入口函数是main
- **已尝试方法**: 检查MinerU源码确认正确的函数名，修改启动脚本将demo()改为main()，改用命令行方式直接调用
- **当前状态**: 已解决
- **后续建议**: 如果MinerU更新版本，需要检查API是否有变化

## 案例4：首次PDF解析内容不完整
- **公司**: 全部8家公司
- **股票代码**: 001282, 603418, 301581, 301563, 688758, 688775, 920100, 920116
- **环节**: 解析（PDF解析）
- **问题表现**: 首次解析只提取了前100页中包含关键词的页面，没有完整解析整本PDF的所有页面内容
- **可能原因**: 解析脚本中设置了range(min(page_count, 100))限制，且只提取包含特定关键词的页面
- **已尝试方法**: 修改解析脚本移除100页限制改为range(page_count)解析所有页面，重新运行完整解析脚本，确认8个PDF的所有页面都已完整解析
- **当前状态**: 已解决 - 8个PDF全部完整解析（476页、398页、343页、443页、468页、555页、382页、365页）
- **后续建议**: 解析脚本应默认解析所有页面，不应设置页数限制

## 案例5：GitHub Desktop无法显示本地提交记录
- **公司**: 不适用
- **股票代码**: 不适用
- **环节**: 提交（GitHub操作）
- **问题表现**: GitHub Desktop中History标签只显示昨天的3条记录，看不到今天的提交记录，显示Fetching origin - Hang on...
- **可能原因**: GitHub Desktop的网络连接不稳定，无法同步远程仓库状态
- **已尝试方法**: 使用命令行git log --oneline确认本地提交记录完整，使用命令行git push origin main直接推送
- **当前状态**: 部分解决 - 本地提交记录完整，但GitHub Desktop显示可能有延迟
- **后续建议**: 如果GitHub Desktop无法同步，可以使用命令行git push origin main直接推送

## 案例6：企业清单CSV文件WPS打开显示旧内容
- **公司**: 不适用
- **股票代码**: 不适用
- **环节**: 文件管理
- **问题表现**: 在WPS中打开week1_public_samples.csv文件，显示的仍是旧内容（download_status为待下载），而不是更新后的success
- **可能原因**: 用户打开了错误路径的文件（新建文件夹中的旧文件，而非prospectus-pevc-project仓库中的更新文件）
- **已尝试方法**: 指导用户打开正确路径的文件，指导用户使用Ctrl+H查找替换功能手动更新
- **当前状态**: 已解决
- **后续建议**: 建议用户始终从GitHub仓库文件夹打开文件，避免打开其他位置的副本

## 案例7：WPS自动修改CSV日期格式
- **公司**: 不适用
- **股票代码**: 不适用
- **环节**: 文件管理
- **问题表现**: 用WPS打开CSV文件后，日期格式从2023-05-17被自动修改为2023/5/17
- **可能原因**: WPS表格默认会自动识别和格式化日期单元格
- **已尝试方法**: 使用Python脚本重新写入标准日期格式YYYY-MM-DD，建议用户使用记事本而非WPS编辑CSV文件
- **当前状态**: 已解决
- **后续建议**: 编辑CSV文件时建议使用纯文本编辑器（如记事本、VS Code），避免WPS/Excel自动格式化
