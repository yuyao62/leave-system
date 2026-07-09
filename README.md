# 🏖️ Leave Management System

一套使用 **Python + PySide6 + SQLite** 開發的桌面版特休 / 請假管理系統。

本專案目的是取代傳統網頁式或 Excel 請假管理方式，提供簡潔、美觀且容易維護的 Windows 視窗程式。

---

## ✨ 功能

### 👤 員工管理

- 新增員工
- 修改員工
- 刪除員工
- 記錄到職日
- 自動計算年資

---

### 🏖️ 特休管理

- 自動計算年度特休
- 顯示：
  - 給假天數
  - 給假時數
  - 已休特休
  - 剩餘特休
- 支援以小時計算

---

### 📝 請假管理

支援：

- 特休
- 補休
- 病假
- 事假
- 家庭照顧假
- 婚假
- 喪假
- 公假
- 其他

功能包含：

- 新增
- 修改
- 刪除
- 備註

---

### 📊 統計

依年度統計：

- 給假
- 已休
- 剩餘
- 總請假

可依員工查詢。

---

### 💾 資料庫

使用 SQLite

```
leave_system.db
```

不用另外安裝資料庫即可使用。

---

## 🖥️ 技術

- Python 3.11+
- PySide6
- SQLite3

---

## 📁 專案結構

```
leave-system/
│
├── leave_gui.py
├── leave_system.db
├── requirements.txt
├── README.md
├── LICENSE
└── screenshots/
```

---

## 🚀 安裝

安裝套件

```bash
pip install PySide6
```

執行

```bash
python leave_gui.py
```

---

## 📸 畫面

（可放系統截圖）

```
screenshots/main.png
```

---

## 📅 未來規劃

- [ ] Excel 匯出
- [ ] Excel 匯入員工資料
- [ ] 勞基法完整特休規則
- [ ] 特休到期提醒
- [ ] 補休到期提醒
- [ ] 月曆檢視
- [ ] 多使用者登入
- [ ] 權限管理
- [ ] PDF 報表
- [ ] EXE 發佈版本

---

## 📜 License

MIT License

---

## 作者

GitHub：
https://github.com/你的帳號

2026
# 🏖 Leave Management System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PySide6](https://img.shields.io/badge/PySide6-6.x-green)
![SQLite](https://img.shields.io/badge/SQLite-3-blue)
![License](https://img.shields.io/badge/License-MIT-orange)
