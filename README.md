# 🏖 Leave Management System

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![PySide6](https://img.shields.io/badge/PySide6-6.x-green)
![SQLite](https://img.shields.io/badge/SQLite-3-blue)
![License](https://img.shields.io/badge/License-MIT-orange)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

一套使用 **Python + PySide6 + SQLite** 開發的 **特休 / 請假管理系統**。

本專案目的是提供一套簡潔、美觀且容易維護的請假管理工具，可取代傳統 Excel 或舊式網頁請假系統。

---

# 📸 系統畫面

> 可放置系統截圖

| 主畫面 | 員工管理 | 統計畫面 |
|--------|---------|---------|
| ![](screenshots/main.png) | ![](screenshots/employee.png) | ![](screenshots/statistics.png) |

---

# ✨ 功能

## 👤 員工管理

- 新增員工
- 修改員工
- 刪除員工
- 到職日管理
- 年資自動計算

---

## 🏖 特休管理

- 自動計算年度特休
- 給假天數
- 給假時數
- 已休特休
- 剩餘特休
- 小時計算

---

## 📝 請假管理

支援

- 特休
- 補休
- 病假
- 事假
- 家庭照顧假
- 婚假
- 喪假
- 公假
- 其他

功能包含

- 新增
- 修改
- 刪除
- 備註

---

## 📊 統計

依年度統計

- 給假
- 已休
- 剩餘
- 總請假

可依員工查詢。

---

## 💾 資料庫

使用

```
SQLite
```

資料儲存在

```
leave_system.db
```

不用另外安裝資料庫。

---

# 🚀 GitHub Pages

專案首頁

https://yuyao62.github.io/leave-system/

---

# 📦 安裝

## 安裝 Python

Python 3.11 以上

https://www.python.org/

---

## 安裝套件

```bash
pip install -r requirements.txt
```

或

```bash
pip install PySide6
```

---

## 執行

```bash
python leave_gui_fixed.py
```

---

# 📂 專案結構

```
leave-system
│
├── index.html                 GitHub Pages 首頁
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── leave_gui_fixed.py          主程式
├── leave_system.db             SQLite資料庫
│
└── screenshots
    ├── main.png
    ├── employee.png
    └── statistics.png
```

---

# 📑 使用流程

```
新增員工
      │
      ▼
輸入到職日
      │
      ▼
新增請假紀錄
      │
      ▼
系統自動統計
      │
      ▼
查看剩餘特休
```

---

# 🔧 技術

| 技術 | 說明 |
|------|------|
| Python | 程式語言 |
| PySide6 | Windows GUI |
| SQLite | 資料庫 |
| GitHub | 版本控制 |
| GitHub Pages | 專案展示 |

---

# 📅 Roadmap

## v1.0

- [x] 員工管理
- [x] 請假管理
- [x] 特休統計
- [x] SQLite

---

## v1.1

- [ ] Excel 匯出
- [ ] Excel 匯入員工
- [ ] 修改請假紀錄
- [ ] 搜尋功能

---

## v1.2

- [ ] 勞基法完整特休規則
- [ ] 到期提醒
- [ ] 月曆模式
- [ ] 報表列印

---

## v2.0

- [ ] 使用者登入
- [ ] 權限管理
- [ ] 多人共用
- [ ] 雲端同步
- [ ] API

---

# 💡 未來功能

- PDF 報表
- Excel 報表
- EXE 發佈
- Email 通知
- 行事曆整合
- QR Code 打卡
- 公休日設定
- 國定假日管理

---

# 🖥 系統需求

Windows 10 / Windows 11

Python 3.11+

---

# 📜 License

MIT License

---

# 👨‍💻 Author

GitHub

https://github.com/yuyao62

---

如果這個專案對你有幫助，歡迎 ⭐ Star！
