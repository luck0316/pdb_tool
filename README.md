# pdb_tool

## 简介
- 用于提取PDB（Program Database）文件信息的工具。
  ```
  PDB文件通常包含程序的调试信息，对于软件开发和调试过程非常重要。
  ```

## 功能说明
功能说明
1. `打开文件`\
通过此功能可以选择并打开一个PDB文件，准备进行信息提取。

2. `PDB信息提取`\
该工具可以提取PDB文件的各种信息，包括：
    * PDB_STREAM_PDB的二进制数据
    * PDB版本、时间戳、年龄
    * GUID（全局唯一标识符）信息
    * 第二个GUID信息（如果存在）
3. `关闭窗口`\
关闭当前工具窗口。

## 使用说明
- 工具使用Python编写，基于mmgui库和pdbparse库。
- 环境要求
    * Python 3.x
    * mmgui库
    * pdbparse库

## 使用详解
- 打开文件功能
```
点击工具界面的“打开文件”按钮。
选择要提取信息的PDB文件。
```
- PDB信息提取功能
```
在打开文件后，工具将展示所选文件的各项信息。
可查看PDB版本、时间戳、年龄等基本信息。
提供了PDB_STREAM_PDB的二进制数据的格式化展示。
显示了GUID信息，包括GUID的版本、时间戳、年龄、16进制表示等。
若存在第二个GUID，工具会额外展示第二个GUID的相关信息。
```
- 关闭窗口功能
```
当使用完工具后，点击“关闭窗口”按钮，退出工具界面。
```

## 注意事项
请确保已经安装了所有依赖项。\
在使用工具之前，建议备份PDB文件以防止意外数据损失。
