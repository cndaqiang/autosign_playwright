import sys
import yaml
from playwright.sync_api import sync_playwright

# ======================== 1. 读取配置文件 ========================
with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# ======================== 2. 确定是否有头模式 ========================
headless = False

# ======================== 3. 启动 Playwright 并加载持久化浏览器上下文 ========================
with sync_playwright() as p:
    browser_type = p.chromium  # Edge 也是 Chromium 内核，这里用 Chromium 即可

    context = browser_type.launch_persistent_context(
        user_data_dir=config["browser"]["user_data_dir"],
        headless=headless,
        viewport={'width': 1920, 'height': 1080},
        args=[
            "--start-maximized",
            "--window-size=1920,1080"
        ],
    )

    page = context.new_page()

    # ======================== 4. 打开目标网址 ========================
    page.goto("https://www.bing.com")

    # ======================== 5. 提示用户完成登录 ========================
    print("👉 请在浏览器中完成相关网站登录后，回到命令行按回车退出")
    input("按回车关闭浏览器...")

    # ======================== 6. 退出浏览器 ========================
    #context.close()
