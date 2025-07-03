# autosign_playwright

一个基于 **Playwright (Chromium)** 的自动化签到工具，帮助你自动完成网页签到、兑换奖励等任务。

## 主要功能

- 复用浏览器用户数据目录，实现登录状态持久化，无需重复扫码登录
- 自动打开指定签到页面，定位按钮并完成签到操作
- 支持有头（GUI）和无头（Headless）两种运行模式，方便调试与自动化部署
- 自动保存签到结果截图，方便查看执行状态
- 支持从浏览器导出与导入 cookies，方便跨机器和无头环境使用
- 通过配置文件灵活管理浏览器用户数据目录

## 环境准备

1. 安装 Python（推荐 3.8+）  
2. 安装项目依赖（建议在项目根目录执行）：  
   ```
   pip install -r requirements.txt
   ```

3. 安装 Playwright 浏览器核心：

   ```
   playwright install
   ```

## 配置说明

* 复制 `config_example.yml` 为 `config.yml`
* 修改 `config.yml` 中的 `browser.user_data_dir` 路径，指向你自定义的浏览器运行数据目录（用于保存登录状态等信息），**不是浏览器程序的安装目录**

## 使用方法

### 启动签到脚本

* **无头模式（自动化后台执行）**

  ```
  python www.ablesci.com.py
  ```
* **带界面模式（便于手动登录调试）**

  ```
  python www.ablesci.com.py --gui
  ```

### Cookies 管理

* **导出浏览器所有 cookies：**

  ```
  python tool_build_cooikes.py --all
  ```
* **导入 cookies 并自动登录：**

  ```
  python tool_import_cooikes.py
  ```

### 其他工具

* `tool_open_browser.py`：启动持久化 Chromium 浏览器，方便手动操作和登录状态调试
* `check_timestamp.py`：脚本运行时间检查工具，控制运行间隔，避免重复签到

## 项目结构

```
├── www.ablesci.com.py           主签到脚本
├── tool_build_cooikes.py        导出 cookies 工具
├── tool_import_cooikes.py       导入 cookies 工具
├── tool_open_browser.py         打开持久化浏览器工具
├── check_timestamp.py           脚本运行时间检查工具（本仓库模块）
├── config_example.yml           配置示例
├── requirements.txt             依赖列表
├── cookies.json                 导出/导入的 cookies 文件（被 .gitignore 忽略）
├── sign_result.png              截图结果（被 .gitignore 忽略）
├── README.md                    项目说明
└── __pycache__/                 缓存文件夹
```

## 注意事项

* 请确保 `config.yml` 不提交版本库，已通过 `.gitignore` 保护
* 登录状态保存在 `user_data_dir`，可跨脚本复用
* Playwright 会自动下载 Chromium 浏览器核心，首次安装需耐心等待

---

## 作者声明

本项目脚本和 README 由 OpenAI ChatGPT 协助生成，结合作者个人调试优化。