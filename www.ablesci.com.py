import sys
import time
import yaml  # 用于读取配置文件
from playwright.sync_api import sync_playwright
import check_timestamp

# ======================== 0. 初始化命令 ========================
check_timestamp.check(run_interval_hours=1e-6, run_interval_days=0)

# ======================== 1. 读取配置 ========================
with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# ======================== 2. 确定是否有头模式 ========================
headless = True
if "--gui" in sys.argv:
    headless = False

# ======================== 3. 启动 Playwright 并创建浏览器上下文 ========================
with sync_playwright() as p:
    # Playwright 支持 chromium/firefox/webkit
    browser_type = p.chromium

    # 启动浏览器
    browser = browser_type.launch(
        headless=headless,
        args=[
            "--start-maximized",
            "--window-size=1920,1080"
        ],
    )

    # 通过持久化用户数据目录实现登录态复用
    # 类似 Selenium 的 user-data-dir，但 Playwright 需要用 launch_persistent_context
    context = browser_type.launch_persistent_context(
        user_data_dir=config['browser']['user_data_dir'],
        headless=headless,
        viewport={'width': 1920, 'height': 1080},  # 固定分辨率
        args=[
            "--start-maximized"
        ],
    )

    # 创建页面
    page = context.new_page()

    try:
        # ======================== 4. 打开目标页面 ========================
        page.goto("https://www.ablesci.com/")

        # 如果是有头模式，需要用户扫码登录
        if not headless:
            input("请在浏览器中完成登录后，按回车继续...")

        # ======================== 5. 全局等待超时设置 ========================
        # Playwright 自带智能等待，通常不需要显式设置隐式等待
        # 但可以用 set_default_timeout 设置 find/wait 超时时间
        page.set_default_timeout(10 * 1000)  # 单位是毫秒

        # ======================== 6. 查找签到按钮 ========================
        # Playwright 提供 querySelectorAll = page.query_selector_all()
        # CSS 选择器支持与 Selenium 完全相同的语法

        sign_buttons = page.query_selector_all("button.btn-sign")

        found = False
        for btn in sign_buttons:
            # 获取按钮文本内容并去掉首尾空白
            btn_text = btn.inner_text().strip()
            print(f"检查按钮内容: {btn_text}")

            # 可以通过 btn.get_attribute("id") 等方法获取属性
            # Playwright 不区分 find_element/find_elements，query_selector_all 返回列表，query_selector 返回第一个

            if "今日打卡签到" in btn_text:
                print("确认是需要的签到按钮，正在点击...")
                btn.click()
                print("已点击签到按钮！")
                found = True
                break

        if not found:
            print("没有找到符合条件的签到按钮，可能今天已签到或页面状态异常。")

        # ======================== 7. 等待响应并截图 ========================
        time.sleep(5)
        page.screenshot(path="sign_result.ablesci.png")
        print("截图已保存到 sign_result.ablesci.png，请检查是否签到成功。")

    finally:
        # ======================== 8. 退出浏览器 ========================
        print("签到结束. 退出浏览器")
        if not headless:
            input("按回车关闭浏览器...")
        context.close()
        browser.close()
