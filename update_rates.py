import json
import os
from datetime import datetime, timedelta, timezone

# 1. 锁定泰国时间 (UTC+7)
tz = timezone(timedelta(hours=7))
now = datetime.now(tz)
today_key = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H:%M:%S")

# 2. 读取你手动校准好的 rates.json
rates_file = 'rates.json'
if not os.path.exists(rates_file):
    print(f"❌ 错误：找不到 {rates_file}")
    exit(0)

with open(rates_file, 'r', encoding='utf-8') as f:
    try:
        current_rates = json.load(f)
    except Exception as e:
        print(f"❌ 错误：解析 rates.json 失败: {e}")
        exit(0)

# 3. 读取历史数据库 history.json
history_file = 'history.json'
history_data = {}
if os.path.exists(history_file) and os.path.getsize(history_file) > 0:
    with open(history_file, 'r', encoding='utf-8') as f:
        try:
            history_data = json.load(f)
        except Exception as e:
            print(f"⚠️ 警告：解析 history.json 失败: {e}")
            history_data = {}

# 4. 写入今日数据 (自动补全时间)
history_data[today_key] = {
    "update_time": current_rates.get("update_time", current_time),
    "USD_THB": current_rates.get("USD_THB", "0.00"),
    "USD_CNY": current_rates.get("USD_CNY", "0.00"),
    "USD_PHP": current_rates.get("USD_PHP", "0.00")
}

# 5. 全量保存 (不截断，永久留存)
with open(history_file, 'w', encoding='utf-8') as f:
    json.dump(history_data, f, indent=4, ensure_ascii=False)

print(f"✅ 同步成功: {today_key} {history_data[today_key]['update_time']}")

