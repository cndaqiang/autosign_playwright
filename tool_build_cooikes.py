import json
import yaml
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# ======================== 1. 读取配置 ========================
with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# ======================== 2. 确定是否有头模式 ========================
headless = True
if "--gui" in sys.argv:
    headless = False

# ======================== 3. 是否导出所有 cookies ========================
export_all = "--all" in sys.argv

# ======================== 4. 启动 Playwright，创建持久化浏览器上下文 ========================
with sync_playwright() as p:
    browser_type = p.chromium

    context = browser_type.launch_persistent_context(
        user_data_dir=config["browser"]["user_data_dir"],
        headless=headless,
        viewport={'width': 1920, 'height': 1080},
        args=[
            "--start-maximized",
        ],
    )

    print("Edge (Chromium) 浏览器已启动！")
    print("请在浏览器中自由访问并完成所有需要的登录。")
    print("完成后请回到命令行按回车，脚本将收集 cookies。")
    input("按回车开始收集 cookies...")

    all_cookies = {}

    if export_all:
        # ======================== 5A. 获取所有域 cookies ========================
        cookies = context.cookies()
        print(f"导出所有域的 {len(cookies)} 条 cookies")
        # 将所有 cookies 按 domain 分组
        for cookie in cookies:
            domain = cookie["domain"]
            all_cookies.setdefault(domain, []).append(cookie)
    else:
        # ======================== 5B. 只获取当前页面 cookies ========================
        for page in context.pages:
            current_url = page.url
            if current_url.startswith("data:") or current_url in ("about:blank", ""):
                continue  # 排除空白或无效标签页

            domain = page.evaluate("document.domain")
            cookies = context.cookies([current_url])
            if cookies:
                print(f"收集到域名 [{domain}] 的 {len(cookies)} 条 cookies")
                all_cookies[domain] = cookies

    # ======================== 6. 保存到文件 ========================
    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(all_cookies, f, ensure_ascii=False, indent=2)
    print("所有 cookies 已保存到 cookies.json")

    # ======================== 7. 关闭浏览器 ========================
    if not headless:
        input("按回车关闭浏览器...")
    context.close()
