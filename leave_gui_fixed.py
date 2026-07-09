# -*- coding: utf-8 -*-
"""
特休 / 請假統計系統 - 視窗版

使用方式：
1. pip install PySide6
2. python leave_gui_fixed.py

資料會存在同資料夾的 leave_system.db
"""

import sys
import sqlite3
from datetime import date, datetime
from pathlib import Path

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QMessageBox, QDateEdit, QDoubleSpinBox,
    QTabWidget, QHeaderView, QSpinBox
)

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "leave_system.db"

LEAVE_TYPES = [
    "特休", "補休", "病假", "事假", "家庭照顧假",
    "喪假", "婚假", "產假", "公假", "其他"
]


def get_conn():
    return sqlite3.connect(DB_FILE)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_no TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        hire_date TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS leave_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_no TEXT NOT NULL,
        leave_date TEXT NOT NULL,
        leave_type TEXT NOT NULL,
        hours REAL NOT NULL,
        note TEXT DEFAULT '',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def tw_hours_text(hours):
    try:
        h = float(hours)
    except Exception:
        h = 0
    whole = int(h)
    minutes = int(round((h - whole) * 60))
    if minutes == 60:
        whole += 1
        minutes = 0
    return f"{whole}時 {minutes}分"


def annual_leave_days(hire_date_str, target_year):
    """
    簡化版特休規則，可再依你們公司規則調整。
    目前用年資粗估：
    未滿 1 年：3 天
    1 年：7 天
    2 年：10 天
    3~4 年：14 天
    5~9 年：15 天
    10 年以上：每年 +1 天，上限 30 天
    """
    hire = datetime.strptime(hire_date_str, "%Y-%m-%d").date()
    target = date(target_year, 1, 1)

    years = target.year - hire.year
    if (target.month, target.day) < (hire.month, hire.day):
        years -= 1

    if years < 0:
        return 0
    if years < 1:
        return 3
    if years < 2:
        return 7
    if years < 3:
        return 10
    if years < 5:
        return 14
    if years < 10:
        return 15
    return min(30, 15 + (years - 10))


def annual_leave_hours(hire_date_str, target_year):
    return annual_leave_days(hire_date_str, target_year) * 8


class LeaveSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("特休 / 請假統計系統")
        self.resize(1200, 720)
        self.selected_record_id = None

        self.build_ui()
        self.reload_all()

    def build_ui(self):
        root = QVBoxLayout(self)

        title = QLabel("特休 / 請假統計系統")
        title.setStyleSheet("font-size: 22px; font-weight: bold; padding: 8px;")
        root.addWidget(title)

        self.tabs = QTabWidget()
        root.addWidget(self.tabs)

        self.page_main = QWidget()
        self.page_employee = QWidget()
        self.tabs.addTab(self.page_main, "請假紀錄 / 統計")
        self.tabs.addTab(self.page_employee, "員工資料")

        self.build_main_page()
        self.build_employee_page()

    def build_main_page(self):
        layout = QVBoxLayout(self.page_main)

        input_row = QHBoxLayout()

        self.leave_emp_combo = QComboBox()
        self.leave_date = QDateEdit()
        self.leave_date.setCalendarPopup(True)
        self.leave_date.setDate(QDate.currentDate())

        self.leave_type = QComboBox()
        self.leave_type.addItems(LEAVE_TYPES)

        self.leave_hours = QDoubleSpinBox()
        self.leave_hours.setRange(0.5, 999)
        self.leave_hours.setSingleStep(0.5)
        self.leave_hours.setValue(8)
        self.leave_hours.setSuffix(" 小時")

        self.leave_note = QLineEdit()
        self.leave_note.setPlaceholderText("備註")

        btn_add_leave = QPushButton("新增請假")
        btn_add_leave.clicked.connect(self.add_leave)

        btn_update_leave = QPushButton("修改選取紀錄")
        btn_update_leave.clicked.connect(self.update_leave)

        btn_delete_leave = QPushButton("刪除選取紀錄")
        btn_delete_leave.clicked.connect(self.delete_leave)

        input_row.addWidget(QLabel("員工"))
        input_row.addWidget(self.leave_emp_combo, 2)
        input_row.addWidget(QLabel("日期"))
        input_row.addWidget(self.leave_date)
        input_row.addWidget(QLabel("假別"))
        input_row.addWidget(self.leave_type)
        input_row.addWidget(QLabel("時數"))
        input_row.addWidget(self.leave_hours)
        input_row.addWidget(self.leave_note, 2)
        input_row.addWidget(btn_add_leave)
        input_row.addWidget(btn_update_leave)
        input_row.addWidget(btn_delete_leave)

        layout.addLayout(input_row)

        filter_row = QHBoxLayout()
        self.year_spin = QSpinBox()
        self.year_spin.setRange(2000, 2100)
        self.year_spin.setValue(date.today().year)
        self.year_spin.valueChanged.connect(self.load_summary_and_records)

        self.filter_emp_combo = QComboBox()
        self.filter_emp_combo.currentIndexChanged.connect(self.load_summary_and_records)

        btn_refresh = QPushButton("重新整理")
        btn_refresh.clicked.connect(self.reload_all)

        filter_row.addWidget(QLabel("年度"))
        filter_row.addWidget(self.year_spin)
        filter_row.addWidget(QLabel("篩選員工"))
        filter_row.addWidget(self.filter_emp_combo, 1)
        filter_row.addWidget(btn_refresh)
        filter_row.addStretch()
        layout.addLayout(filter_row)

        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(10)
        self.summary_table.setHorizontalHeaderLabels([
            "員工編號", "姓名", "到職日", "年度",
            "給假", "給假時數", "已休特休", "剩餘特休",
            "已休其他假", "總請假"
        ])
        layout.addWidget(QLabel("年度統計"))
        layout.addWidget(self.summary_table, 1)

        self.records_table = QTableWidget()
        self.records_table.setColumnCount(7)
        self.records_table.setHorizontalHeaderLabels([
            "ID", "員工編號", "姓名", "日期", "假別", "時數", "備註"
        ])
        self.records_table.setColumnHidden(0, True)
        self.records_table.cellClicked.connect(self.on_record_clicked)
        layout.addWidget(QLabel("請假明細"))
        layout.addWidget(self.records_table, 2)

    def build_employee_page(self):
        layout = QVBoxLayout(self.page_employee)

        row = QHBoxLayout()
        self.emp_no = QLineEdit()
        self.emp_no.setPlaceholderText("員工編號，例如 100274")
        self.emp_name = QLineEdit()
        self.emp_name.setPlaceholderText("姓名")
        self.hire_date = QDateEdit()
        self.hire_date.setCalendarPopup(True)
        self.hire_date.setDate(QDate.currentDate())

        btn_add = QPushButton("新增 / 更新員工")
        btn_add.clicked.connect(self.add_or_update_employee)

        btn_delete = QPushButton("刪除員工")
        btn_delete.clicked.connect(self.delete_employee)

        row.addWidget(QLabel("員編"))
        row.addWidget(self.emp_no)
        row.addWidget(QLabel("姓名"))
        row.addWidget(self.emp_name)
        row.addWidget(QLabel("到職日"))
        row.addWidget(self.hire_date)
        row.addWidget(btn_add)
        row.addWidget(btn_delete)
        layout.addLayout(row)

        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(3)
        self.employee_table.setHorizontalHeaderLabels(["員工編號", "姓名", "到職日"])
        self.employee_table.cellClicked.connect(self.on_employee_clicked)
        layout.addWidget(self.employee_table)

    def reload_all(self):
        self.load_employee_combos()
        self.load_employees_table()
        self.load_summary_and_records()

    def load_employee_combos(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT emp_no, name FROM employees ORDER BY emp_no")
        rows = cur.fetchall()
        conn.close()

        self.leave_emp_combo.blockSignals(True)
        self.filter_emp_combo.blockSignals(True)

        self.leave_emp_combo.clear()
        self.filter_emp_combo.clear()
        self.filter_emp_combo.addItem("全部員工", "")

        for emp_no, name in rows:
            label = f"{emp_no} - {name}"
            self.leave_emp_combo.addItem(label, emp_no)
            self.filter_emp_combo.addItem(label, emp_no)

        self.leave_emp_combo.blockSignals(False)
        self.filter_emp_combo.blockSignals(False)

    def load_employees_table(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT emp_no, name, hire_date FROM employees ORDER BY emp_no")
        rows = cur.fetchall()
        conn.close()
        self.fill_table(self.employee_table, rows)

    def add_or_update_employee(self):
        emp_no = self.emp_no.text().strip()
        name = self.emp_name.text().strip()
        hire = self.hire_date.date().toString("yyyy-MM-dd")

        if not emp_no or not name:
            QMessageBox.warning(self, "提醒", "請輸入員工編號與姓名")
            return

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO employees(emp_no, name, hire_date)
            VALUES (?, ?, ?)
            ON CONFLICT(emp_no) DO UPDATE SET
                name = excluded.name,
                hire_date = excluded.hire_date
        """, (emp_no, name, hire))
        conn.commit()
        conn.close()

        self.reload_all()
        QMessageBox.information(self, "完成", "員工資料已儲存")

    def delete_employee(self):
        emp_no = self.emp_no.text().strip()
        if not emp_no:
            QMessageBox.warning(self, "提醒", "請先點選員工")
            return

        ans = QMessageBox.question(
            self, "確認刪除",
            f"確定刪除員工 {emp_no}？\n這會一併刪除他的請假紀錄。"
        )
        if ans != QMessageBox.Yes:
            return

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM leave_records WHERE emp_no = ?", (emp_no,))
        cur.execute("DELETE FROM employees WHERE emp_no = ?", (emp_no,))
        conn.commit()
        conn.close()

        self.emp_no.clear()
        self.emp_name.clear()
        self.reload_all()

    def on_employee_clicked(self, row, col):
        self.emp_no.setText(self.employee_table.item(row, 0).text())
        self.emp_name.setText(self.employee_table.item(row, 1).text())
        d = QDate.fromString(self.employee_table.item(row, 2).text(), "yyyy-MM-dd")
        if d.isValid():
            self.hire_date.setDate(d)

    def add_leave(self):
        emp_no = self.leave_emp_combo.currentData()
        if not emp_no:
            QMessageBox.warning(self, "提醒", "請先新增員工")
            return

        leave_date = self.leave_date.date().toString("yyyy-MM-dd")
        leave_type = self.leave_type.currentText()
        hours = float(self.leave_hours.value())
        note = self.leave_note.text().strip()

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO leave_records(emp_no, leave_date, leave_type, hours, note)
            VALUES (?, ?, ?, ?, ?)
        """, (emp_no, leave_date, leave_type, hours, note))
        conn.commit()
        conn.close()

        self.leave_note.clear()
        self.load_summary_and_records()

    def update_leave(self):
        if not self.selected_record_id:
            QMessageBox.warning(self, "提醒", "請先點選下面請假明細的一筆紀錄")
            return

        emp_no = self.leave_emp_combo.currentData()
        leave_date = self.leave_date.date().toString("yyyy-MM-dd")
        leave_type = self.leave_type.currentText()
        hours = float(self.leave_hours.value())
        note = self.leave_note.text().strip()

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE leave_records
            SET emp_no = ?, leave_date = ?, leave_type = ?, hours = ?, note = ?
            WHERE id = ?
        """, (emp_no, leave_date, leave_type, hours, note, self.selected_record_id))
        conn.commit()
        conn.close()

        self.load_summary_and_records()
        QMessageBox.information(self, "完成", "請假紀錄已修改")

    def delete_leave(self):
        if not self.selected_record_id:
            QMessageBox.warning(self, "提醒", "請先點選下面請假明細的一筆紀錄")
            return

        ans = QMessageBox.question(self, "確認刪除", "確定刪除這筆請假紀錄？")
        if ans != QMessageBox.Yes:
            return

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM leave_records WHERE id = ?", (self.selected_record_id,))
        conn.commit()
        conn.close()

        self.selected_record_id = None
        self.load_summary_and_records()

    def on_record_clicked(self, row, col):
        self.selected_record_id = int(self.records_table.item(row, 0).text())
        emp_no = self.records_table.item(row, 1).text()
        leave_date = self.records_table.item(row, 3).text()
        leave_type = self.records_table.item(row, 4).text()
        hours_text = self.records_table.item(row, 5).text()
        note = self.records_table.item(row, 6).text() if self.records_table.item(row, 6) else ""

        idx = self.leave_emp_combo.findData(emp_no)
        if idx >= 0:
            self.leave_emp_combo.setCurrentIndex(idx)

        d = QDate.fromString(leave_date, "yyyy-MM-dd")
        if d.isValid():
            self.leave_date.setDate(d)

        idx = self.leave_type.findText(leave_type)
        if idx >= 0:
            self.leave_type.setCurrentIndex(idx)

        try:
            self.leave_hours.setValue(float(hours_text.replace(" 小時", "")))
        except Exception:
            pass
        self.leave_note.setText(note)

    def load_summary_and_records(self):
        year = int(self.year_spin.value())
        emp_filter = self.filter_emp_combo.currentData() if self.filter_emp_combo.count() else ""

        conn = get_conn()
        cur = conn.cursor()

        if emp_filter:
            cur.execute("SELECT emp_no, name, hire_date FROM employees WHERE emp_no = ? ORDER BY emp_no", (emp_filter,))
        else:
            cur.execute("SELECT emp_no, name, hire_date FROM employees ORDER BY emp_no")
        employees = cur.fetchall()

        summary_rows = []
        for emp_no, name, hire in employees:
            total_allow = annual_leave_hours(hire, year)
            days = annual_leave_days(hire, year)

            cur.execute("""
                SELECT leave_type, SUM(hours)
                FROM leave_records
                WHERE emp_no = ? AND substr(leave_date, 1, 4) = ?
                GROUP BY leave_type
            """, (emp_no, str(year)))
            leave_sum = {k: (v or 0) for k, v in cur.fetchall()}

            used_special = leave_sum.get("特休", 0)
            total_used = sum(leave_sum.values())
            used_other = total_used - used_special
            remain = total_allow - used_special

            summary_rows.append([
                emp_no, name, hire, str(year),
                f"{days:g} 天", tw_hours_text(total_allow),
                tw_hours_text(used_special), tw_hours_text(remain),
                tw_hours_text(used_other), tw_hours_text(total_used)
            ])

        if emp_filter:
            cur.execute("""
                SELECT r.id, e.emp_no, e.name, r.leave_date, r.leave_type, r.hours, COALESCE(r.note, '')
                FROM leave_records r
                JOIN employees e ON r.emp_no = e.emp_no
                WHERE substr(r.leave_date, 1, 4) = ? AND e.emp_no = ?
                ORDER BY r.leave_date DESC, r.id DESC
            """, (str(year), emp_filter))
        else:
            cur.execute("""
                SELECT r.id, e.emp_no, e.name, r.leave_date, r.leave_type, r.hours, COALESCE(r.note, '')
                FROM leave_records r
                JOIN employees e ON r.emp_no = e.emp_no
                WHERE substr(r.leave_date, 1, 4) = ?
                ORDER BY r.leave_date DESC, r.id DESC
            """, (str(year),))
        records = cur.fetchall()
        conn.close()

        self.fill_table(self.summary_table, summary_rows)
        self.fill_table(self.records_table, records)
        self.records_table.setColumnHidden(0, True)

    def fill_table(self, table, rows):
        table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                if isinstance(value, float):
                    text = f"{value:g}"
                else:
                    text = "" if value is None else str(value)
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(r, c, item)

        table.resizeColumnsToContents()
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        if table.columnCount() > 0:
            header.setStretchLastSection(True)


if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    win = LeaveSystem()
    win.show()
    sys.exit(app.exec())
