<?php
// 1. 锁死本地路径，不走任何网络请求
$history_file = 'history.json';
$test_file    = 'test.json';

// 1.5 检查是否通过命令行输入了参数
if (!isset($argv[1])) {
    die("❌ 错误: 缺少必填参数！\n使用示例: php m.php USD_VND\n");
}

// 接收参数并过滤空格、自动转大写
$code = strtoupper(trim($argv[1]));

// 校验格式是否为 3位字母_3位字母 (例如 USD_VND)
if (!preg_match('/^[A-Z]{3}_[A-Z]{3}$/', $code)) {
    die("❌ 错误: 参数格式不合法！必须是类似 'USD_VND' 的格式（3位大写字母+下划线+3位大写字母）。\n");
}

if (!file_exists($history_file) || !file_exists($test_file)) {
    die("❌ 离线错误：找不到 history.json 或 test.json 文件，请核对路径！\n");
}

// 2. 将两个文件读取并解码为 PHP 关联数组
$history_data = json_decode(file_get_contents($history_file), true);
$code_data     = json_decode(file_get_contents($test_file), true);

if (!is_array($history_data) || !is_array($code_data)) {
    die("❌ 解析错误：JSON 格式损坏，请确认两个文件不是空白！\n");
}

echo "🚀 PHP 正在进行全量日期盒子深度熔断合并...\n";
$merged_count = 0;

// 3. 循环遍历您的历史主数据，进行对象层级的无损嵌入
foreach ($history_data as $date => &$day_box) {
    // 只要 test.json 里有这一天的币种真实数字
    if (isset($code_data[$date]) && is_array($day_box)) {
        // 直接在 PHP 节点的下方，无缝钻进去并命名为 USD_VND
        $day_box[$code] = (float)$code_data[$date];
        $merged_count++;
    }
}
unset($day_box); // 释放引用保护

// 4. 将合并后完美无瑕的 币种大矩阵写回原文件（保持优雅的缩进格式）
$final_json = json_encode($history_data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_PRESERVE_ZERO_FRACTION);
file_put_contents($history_file, $final_json);

echo "✨ 完美成功！PHP 已为 $merged_count 个历史节点并排加满了真实的 '$code' 资产数据！\n";

