import sys
import time
import yaml
from playwright.sync_api import sync_playwright
import check_timestamp

# ======================== 0. 初始化命令 ========================
check_timestamp.check(run_interval_hours=0, run_interval_days=15)

# ======================== 1. 读取配置 ========================
with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

headless = True
if "--gui" in sys.argv:
    headless = False

with sync_playwright() as p:
    browser_type = p.chromium

    # ======================== 2. 启动持久化上下文，复用用户数据 ========================
    context = browser_type.launch_persistent_context(
        user_data_dir=config["browser"]["user_data_dir"],
        headless=headless,
        viewport={'width': 1920, 'height': 1080},
        args=["--start-maximized", "--window-size=1920,1080"],
    )

    page = context.new_page()

    # ======================== 3. 打开目标页面 ========================
    page.goto("https://www.tjupt.org/attendance.php")

    if not headless:
        input("请在浏览器中完成登录后，按回车继续...")

    # ======================== 4. 查找所有 <label> 元素 ========================
    labels = page.query_selector_all("label")

    radio_count = 0
    third_radio = None

    # ======================== 5. 找到第3个包含 <input> 的 label 并点击该 input ========================
    for label in labels:
        try:
            radio_input = label.query_selector("input")
            if radio_input:
                radio_count += 1
                if radio_count == 3:
                    third_radio = radio_input
                    third_label_text = label.inner_text().strip()
                    print(f"找到第3个有效选项：{third_label_text}")
                    radio_input.click()
                    break
        except Exception:
            continue

    # ======================== 6. 点击提交按钮 ========================
    if third_radio:
        submit_button = page.query_selector("input[type='submit']")
        if submit_button:
            submit_button.click()
            print("已选中并提交签到！")
        else:
            print("未找到提交按钮！")
    else:
        print(f"没有找到第3个有效选项，页面中只找到 {radio_count} 个有效选项。")

    # ======================== 7. 等待响应并截图 ========================
    time.sleep(5)  # 等待页面更新
    page.screenshot(path="sign_result.pt.png")
    print("截图已保存到 sign_result.pt.png，请检查是否签到成功。")

    # ======================== 8. 退出 ========================
    print("签到结束. 退出浏览器")
    if not headless:
        input("按回车关闭浏览器...")
    context.close()
