# Plugin Development Document - 插件开发文档

## 中文

创建：

```plaintext
在 “plugins” 下创建一个文件夹
必须包含：
    1.config.json
    2.__init__.py
    3.自己的版本日志文件
    4.图标文件路径（建议为64X64或32X32的大小）
    5.描述信息的Markdown文件路径
    6.AithonEditorPlugin

config.json 文件格式：
{
    "EditionLogsFilePath": "版本日志文件路径",
    "state": "状态（启用（Enabled）/禁用（Disabled））",
    "IconFilePath": "图标文件路径",
    "OverviewText": "概述文本",
    "MarkdownFilePathForDescribingInformation": "描述信息的Markdown文件路径",
}
版本日志文件格式：
版本 Version:
    日志
版本 Version:
    日志
AithonEditorPlugin 文件格式：
1376046_1421686_1434237_1420545_1428532_1427391_1380610_1415981_1421686_1434237_1428532_1431955_1393161_1425109_1435378_1419404_1421686_1427391_
版本请参考codes/VersionSystem/VersionSystemRules.md

```

导入：

```python
from ..PluginAPI import (
    # 要导入的东西
)
```

使用的UI库：tkinter、tkintertools
