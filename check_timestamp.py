# check_timestamp.py
import os
import sys
from datetime import datetime

def check(run_interval_hours=0, run_interval_days=0):
    """
    在调用脚本中检查基于脚本文件名的时间戳文件。
    若距上次执行时间超过指定间隔，则更新时间戳并继续执行；
    否则脚本退出。

    参数:
    run_interval_hours: 超过多少小时允许执行
    run_interval_days:  超过多少天允许执行
    """
    # 计算调用者脚本名称
    caller_script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    timestamp_file = f"{caller_script}.txt"
    now = datetime.now()


    if os.path.exists(timestamp_file):
        try:
            with open(timestamp_file, "r", encoding="utf-8") as f:
                last_ts = datetime.fromtimestamp(float(f.read().strip()))
            time_diff = now - last_ts
            hours_diff = time_diff.total_seconds() / 3600
            days_diff = time_diff.days

            print(f"上次运行时间: {last_ts.strftime('%Y-%m-%d %H:%M:%S')} (距现在 {hours_diff:.2f} 小时 / {days_diff} 天)")

            LETRUN = True
            if run_interval_hours > 0:
                LETRUN = LETRUN and hours_diff > run_interval_hours
            if run_interval_days > 0:
                LETRUN = LETRUN and days_diff > run_interval_days

            if LETRUN:
                print("超过指定间隔，将继续执行并更新时间戳。")
                with open(timestamp_file, "w", encoding="utf-8") as f:
                    f.write(str(now.timestamp()))
            else:
                print("距离上次执行过短，脚本退出。")
                sys.exit(0)

        except Exception as e:
            print(f"时间戳解析失败({e})，重新创建并继续执行。")
            with open(timestamp_file, "w", encoding="utf-8") as f:
                f.write(str(now.timestamp()))

    else:
        print("首次执行，创建时间戳文件并继续执行。")
        with open(timestamp_file, "w", encoding="utf-8") as f:
            f.write(str(now.timestamp()))
