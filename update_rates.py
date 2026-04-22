import json
import os
from datetime import datetime, timedelta, timezone

# 1. 动态获取当天的日期和具体时间（强制指定 UTC+7 时区）
# 泰国和北京时间都是 UTC+7
tz = timezone(timedelta(hours=7)) 
now = datetime.now(tz)

today_key = now.strftime("%Y-%m-%d")
now_time = now.strftime("%H:%M:%S")

# 2. 这是你提供的最新汇率数据
today_rates = {
    "update_time": now_time,
    "USD_THB": 32.25,
    "USD_CNY": 6.84,
    "USD_PHP": 60.12
}

# 3. 读取现有的历史记录
history_file = 'history.json'
history_data = {}

if os.path.exists(history_file) and os.path.getsize(history_file) > 0:
    with open(history_file, 'r', encoding='utf-8') as f:
        try:
            history_data = json.load(f)
        except:
            history_data = {}

# 4. 核心逻辑：以动态日期为 Key
history_data[today_key] = today_rates

# 5. 保存回文件
with open(history_file, 'w', encoding='utf-8') as f:
    json.dump(history_data, f, indent=4, ensure_ascii=False)

# 同时更新单日参考文件
with open('rates.json', 'w', encoding='utf-8') as f:
    json.dump({"date": today_key, **today_rates}, f, indent=4, ensure_ascii=False)

print(f"✅ 数据已成功同步到日期标题: {today_key} (本地时间: {now_time})")

