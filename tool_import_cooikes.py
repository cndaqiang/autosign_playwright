import json
import time
import yaml
import sys
from playwright.sync_api import sync_playwright

# ======================== 1. 读取配置文件 ========================
with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# ======================== 2. 确定是否有头模式 ========================
headless = True
if "--gui" in sys.argv:
    headless = False

# ======================== 3. 启动 Playwright 并创建持久化上下文 ========================
with sync_playwright() as p:
    browser_type = p.chromium

    # 用 launch_persistent_context 以复用 user-data-dir
    context = browser_type.launch_persistent_context(
        user_data_dir=config["browser"]["user_data_dir"],
        headless=headless,
        viewport={'width': 1920, 'height': 1080},
        args=[
            "--start-maximized",
        ],
    )

    print("Edge (Chromium) 已启动，准备注入 cookies...")

    # ======================== 4. 加载 cookies 文件 ========================
    with open("cookies.json", "r", encoding="utf-8") as f:
        all_cookies = json.load(f)

    # ======================== 5. 遍历域名，访问并注入 cookies ========================
    for domain, cookies in all_cookies.items():
        url = f"https://{domain}/"
        print(f"访问 {url} 并注入 {len(cookies)} 个 cookies...")

        # 在 context 中新开一个页面
        page = context.new_page()

        # 首先访问目标域名，让 Playwright 建立该域的 session
        page.goto(url)
        page.wait_for_timeout(3000)  # 等待页面加载

        # Playwright 没有 delete_all_cookies 接口，因此先清理 context 里的 cookies
        # 获取当前 context 的所有 cookies并删除域内 cookies
        existing_cookies = context.cookies([url])
        if existing_cookies:
            existing_names = [c['name'] for c in existing_cookies]
            print(f"现有 cookies：{existing_names}，将被覆盖。")

        # 注入 cookies
        # Playwright 的 context.add_cookies 接受一个 cookies 列表
        # 每个 cookie 必须带有 url 或 domain + path
        cookies_to_add = []
        for cookie in cookies:
            cookie_dict = {
                "name": cookie.get("name"),
                "value": cookie.get("value"),
                "domain": cookie.get("domain"),
                "path": cookie.get("path", "/"),
                "expires": cookie.get("expiry"),
                "secure": cookie.get("secure", False),
                "httpOnly": cookie.get("httpOnly", False),
                "sameSite": cookie.get("sameSite") if "sameSite" in cookie else None,
            }
            # 删除值为 None 的键
            cookie_dict = {k: v for k, v in cookie_dict.items() if v is not None}
            cookies_to_add.append(cookie_dict)

        try:
            context.add_cookies(cookies_to_add)
            print(f"成功注入 {len(cookies_to_add)} 个 cookies。")
        except Exception as e:
            print(f"注入 cookies 出错: {e}")

        # 刷新页面以使 cookies 生效
        page.reload()
        page.wait_for_timeout(3000)

        page.close()

    print("所有 cookies 已成功注入。你现在可以无需重新登录访问这些网站。")

    # ======================== 6. 退出浏览器 ========================
    if not headless:
        input("按回车关闭浏览器...")
    context.close()
