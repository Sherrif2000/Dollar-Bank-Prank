
import sys
import random
from pathlib import Path
from datetime import datetime

from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QGraphicsDropShadowEffect,
    QMessageBox,
)


APP_NAME = "Dollar bank"
APP_ID = "com.earthos.dollarbank"
BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = BASE_DIR / "EarthOSFree.icns"

STARTING_BALANCE = 1_000_000.00
MAX_WINDOWS = 30
SPAWN_INTERVAL_MS = 1000

BG = "#10141D"
SIDEBAR = "#151A25"
PANEL = "#1B2230"
PANEL_LIGHT = "#222B3B"
BORDER = "#303A4B"
TEXT = "#F1F5FC"
MUTED = "#8995A9"
GREEN = "#71E0AE"
BLUE = "#7BA8FF"
RED = "#FF8585"


STYLE = f"""
QMainWindow, QWidget#root {{
    background: {BG};
    color: {TEXT};
    font-family: -apple-system, "Helvetica Neue", sans-serif;
    font-size: 13px;
}}

QWidget#sidebar {{
    background: {SIDEBAR};
    border-right: 1px solid {BORDER};
}}

QLabel {{
    color: {TEXT};
    background: transparent;
}}

QLabel#brand {{
    font-size: 19px;
    font-weight: 800;
}}

QLabel#brandSub {{
    color: {MUTED};
    font-size: 10px;
    letter-spacing: 2px;
}}

QLabel#pageTitle {{
    font-size: 28px;
    font-weight: 800;
}}

QLabel#subtitle {{
    color: {MUTED};
    font-size: 12px;
}}

QLabel#sectionTitle {{
    font-size: 15px;
    font-weight: 750;
}}

QLabel#muted {{
    color: {MUTED};
    font-size: 11px;
}}

QLabel#balance {{
    font-size: 39px;
    font-weight: 800;
}}

QLabel#smallBalance {{
    font-size: 22px;
    font-weight: 750;
}}

QLabel#positive {{
    color: {GREEN};
    font-weight: 700;
}}

QLabel#negative {{
    color: {RED};
    font-weight: 700;
}}

QFrame#panel {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 17px;
}}

QFrame#balanceCard {{
    background: #253D38;
    border: 1px solid #3B6656;
    border-radius: 20px;
}}

QFrame#statCard {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 15px;
}}

QPushButton {{
    color: {TEXT};
    background: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 11px 13px;
    text-align: left;
    font-weight: 650;
}}

QPushButton:hover {{
    background: {PANEL_LIGHT};
}}

QPushButton#navActive {{
    background: #293B35;
    color: {GREEN};
    border: 1px solid #39584B;
}}

QPushButton#primary {{
    background: {GREEN};
    color: #10241B;
    border: none;
    font-weight: 800;
    padding: 12px 16px;
}}

QPushButton#primary:hover {{
    background: #91EDC4;
}}

QPushButton#danger {{
    background: #46262D;
    color: #FFB5B5;
    border: 1px solid #70404A;
    font-weight: 800;
    padding: 12px 16px;
}}

QPushButton#danger:hover {{
    background: #5A2C36;
}}

QPushButton#secondary {{
    background: {PANEL_LIGHT};
    border: 1px solid {BORDER};
    padding: 12px 16px;
}}

QTableWidget {{
    background: {PANEL};
    color: {TEXT};
    border: none;
    gridline-color: {BORDER};
    selection-background-color: #2C3B4D;
    selection-color: {TEXT};
    outline: none;
}}

QHeaderView::section {{
    background: {PANEL};
    color: {MUTED};
    border: none;
    border-bottom: 1px solid {BORDER};
    padding: 10px 8px;
    font-size: 10px;
    font-weight: 800;
}}

QTableWidget::item {{
    padding: 8px;
    border-bottom: 1px solid {BORDER};
}}

QScrollBar:vertical {{
    background: {BG};
    width: 8px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: {BORDER};
    min-height: 25px;
    border-radius: 4px;
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0;
}}
"""


def panel():
    frame = QFrame()
    frame.setObjectName("panel")
    return frame


def label(text, object_name=None):
    result = QLabel(text)
    if object_name:
        result.setObjectName(object_name)
    return result


def button(text, object_name=None):
    result = QPushButton(text)
    if object_name:
        result.setObjectName(object_name)
    result.setCursor(Qt.CursorShape.PointingHandCursor)
    return result


class TinyWindow(QWidget):
    """A tiny floating window that dodges close attempts during the prank."""

    def __init__(self, controller, number):
        super().__init__(None)
        self.controller = controller
        self.number = number

        self.setWindowTitle(f"Dollar bank · Notice {number}")
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setFixedSize(235, 120)

        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))

        self.setStyleSheet("""
            QWidget {
                background: #18251F;
                color: #F1F5FC;
                font-family: -apple-system, sans-serif;
            }
            QLabel#emoji { font-size: 25px; }
            QLabel#heading { font-size: 13px; font-weight: 800; }
            QLabel#hint { font-size: 10px; color: #A0B8AB; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(3)

        layout.addWidget(label("💵", "emoji"))
        layout.addWidget(label("Transaction processing...", "heading"))
        layout.addWidget(label(
            f"Notice #{number} · Please wait",
            "hint"
        ))

        self.move_randomly()

    def move_randomly(self):
        screen = QApplication.screenAt(self.frameGeometry().center())
        if screen is None:
            screen = QApplication.primaryScreen()
        if screen is None:
            return

        area = screen.availableGeometry()
        max_x = max(area.left(), area.right() - self.width() + 1)
        max_y = max(area.top(), area.bottom() - self.height() + 1)

        self.move(
            random.randint(area.left(), max_x),
            random.randint(area.top(), max_y),
        )

    def dodge(self):
        self.move_randomly()
        self.raise_()

    def closeEvent(self, event):
        if self.controller.prank_running:
            self.dodge()
            event.ignore()
        else:
            event.accept()


class DollarBank(QMainWindow):
    def __init__(self):
        super().__init__()

        self.balance = STARTING_BALANCE
        self.prank_running = False
        self.window_count = 0
        self.tiny_windows = []
        self.nav_buttons = {}

        self.setWindowTitle(APP_NAME)
        self.resize(1050, 720)
        self.setMinimumSize(780, 570)

        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))

        self.spawn_timer = QTimer(self)
        self.spawn_timer.setInterval(SPAWN_INTERVAL_MS)
        self.spawn_timer.timeout.connect(self.spawn_tiny_window)

        self.stack = QStackedWidget()
        self.stack.setObjectName("pageStack")

        self.dashboard_page = self.make_dashboard()
        self.activity_page = self.make_activity()
        self.prank_page = self.make_prank_page()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.activity_page)
        self.stack.addWidget(self.prank_page)

        self.build_shell()
        self.refresh_balance()
        self.refresh_prank_status()
        self.show_page(0)

    def build_shell(self):
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        outer = QHBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        side = QVBoxLayout(sidebar)
        side.setContentsMargins(17, 25, 17, 18)
        side.setSpacing(9)

        brand_row = QHBoxLayout()
        brand_icon = label("🌍")
        brand_icon.setStyleSheet("font-size: 25px;")

        brand_text = QVBoxLayout()
        brand_text.setSpacing(2)
        brand_text.addWidget(label("Dollar bank", "brand"))
        brand_text.addWidget(label("EARTHOS EDITION", "brandSub"))

        brand_row.addWidget(brand_icon)
        brand_row.addLayout(brand_text)
        brand_row.addStretch()
        side.addLayout(brand_row)
        side.addSpacing(25)

        side.addWidget(label("WORKSPACE", "muted"))

        nav_items = [
            ("⌂   Overview", 0),
            ("↗   Activity", 1),
            ("✳   Prank lab", 2),
        ]

        for text, index in nav_items:
            nav = button(text)
            nav.clicked.connect(
                lambda checked=False, i=index: self.show_page(i)
            )
            self.nav_buttons[index] = nav
            side.addWidget(nav)

        side.addStretch()

        account = QFrame()
        account.setObjectName("panel")
        account_layout = QVBoxLayout(account)
        account_layout.setContentsMargins(12, 13, 12, 13)
        account_layout.setSpacing(5)
        account_layout.addWidget(label("●  DEMO ACCOUNT", "positive"))
        account_layout.addWidget(label("Local simulation only", "muted"))
        side.addWidget(account)

        main_area = QWidget()
        main_layout = QVBoxLayout(main_area)
        main_layout.setContentsMargins(27, 22, 27, 20)
        main_layout.setSpacing(15)

        topbar = QHBoxLayout()
        topbar.addWidget(label("PERSONAL FINANCE", "muted"))
        topbar.addStretch()
        topbar.addWidget(label("●  Offline demo", "positive"))
        main_layout.addLayout(topbar)
        main_layout.addWidget(self.stack, 1)

        outer.addWidget(sidebar)
        outer.addWidget(main_area, 1)

        file_menu = self.menuBar().addMenu("&File")

        dashboard_action = QAction("Overview", self)
        dashboard_action.triggered.connect(lambda: self.show_page(0))
        file_menu.addAction(dashboard_action)

        stop_action = QAction("Stop Prank", self)
        stop_action.triggered.connect(self.stop_prank)
        file_menu.addAction(stop_action)

        file_menu.addSeparator()

        quit_action = QAction("Quit Dollar bank", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        prank_menu = self.menuBar().addMenu("&Prank")
        start_action = QAction("Start Prank", self)
        start_action.triggered.connect(self.start_prank)
        prank_menu.addAction(start_action)
        prank_menu.addAction(stop_action)

    def make_dashboard(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(17)

        layout.addWidget(label("Your money, your universe.", "pageTitle"))
        layout.addWidget(label(
            "Welcome back. Here's your fictional financial snapshot.",
            "subtitle"
        ))

        balance_card = QFrame()
        balance_card.setObjectName("balanceCard")
        card = QVBoxLayout(balance_card)
        card.setContentsMargins(24, 22, 24, 22)
        card.setSpacing(9)

        card.addWidget(label("TOTAL DEMO BALANCE", "muted"))
        self.balance_label = label("$1,000,000.00", "balance")
        card.addWidget(self.balance_label)
        card.addWidget(label(
            "USD  /  SIMULATED ACCOUNT  /  NO REAL FUNDS",
            "muted"
        ))

        card_bottom = QHBoxLayout()
        card_bottom.addWidget(label("●  Account active", "positive"))
        card_bottom.addStretch()
        card_bottom.addWidget(label("••••  2048", "muted"))
        card.addLayout(card_bottom)

        layout.addWidget(balance_card)

        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)

        stats = [
            ("MONTHLY INCOME", "$8,450.00", "+12.8%"),
            ("MONTHLY SPENDING", "$2,180.00", "Demo data"),
        ]

        for title, amount, note in stats:
            box = QFrame()
            box.setObjectName("statCard")
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(16, 15, 16, 15)
            box_layout.setSpacing(7)
            box_layout.addWidget(label(title, "muted"))
            box_layout.addWidget(label(amount, "smallBalance"))
            box_layout.addWidget(label(note, "positive"))
            stats_row.addWidget(box)

        layout.addLayout(stats_row)

        recent = panel()
        recent_layout = QVBoxLayout(recent)
        recent_layout.setContentsMargins(17, 15, 17, 12)
        recent_layout.setSpacing(9)

        heading = QHBoxLayout()
        heading.addWidget(label("Recent activity", "sectionTitle"))
        heading.addStretch()
        view_all = button("View all  →")
        view_all.clicked.connect(lambda: self.show_page(1))
        heading.addWidget(view_all)
        recent_layout.addLayout(heading)

        self.recent_table = self.create_transaction_table()
        self.recent_table.setMaximumHeight(190)
        recent_layout.addWidget(self.recent_table)

        layout.addWidget(recent, 1)

        prank_strip = QFrame()
        prank_strip.setObjectName("statCard")
        strip = QHBoxLayout(prank_strip)
        strip.setContentsMargins(15, 12, 15, 12)

        strip_text = QVBoxLayout()
        strip_text.addWidget(label("Feeling mischievous?", "sectionTitle"))
        strip_text.addWidget(label(
            "The Prank Lab is one click away.",
            "muted"
        ))

        prank_button = button("Open Prank Lab  →", "primary")
        prank_button.clicked.connect(lambda: self.show_page(2))

        strip.addLayout(strip_text)
        strip.addStretch()
        strip.addWidget(prank_button)
        layout.addWidget(prank_strip)

        return page

    def create_transaction_table(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["TRANSACTION", "DATE", "AMOUNT"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        table.setShowGrid(False)
        table.setAlternatingRowColors(False)

        header = table.horizontalHeader()
        header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )

        transactions = [
            ("Salary · Demo employer", "Today", "+$4,200.00"),
            ("Coffee House", "Yesterday", "-$8.50"),
            ("Freelance payment", "Oct 16", "+$850.00"),
            ("Groceries", "Oct 15", "-$64.20"),
            ("Game store", "Oct 13", "-$29.99"),
        ]

        table.setRowCount(len(transactions))

        for row, transaction in enumerate(transactions):
            for col, value in enumerate(transaction):
                item = QTableWidgetItem(value)
                item.setFlags(
                    Qt.ItemFlag.ItemIsEnabled
                    | Qt.ItemFlag.ItemIsSelectable
                )

                if col == 2:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight
                        | Qt.AlignmentFlag.AlignVCenter
                    )
                    item.setForeground(
                        Qt.GlobalColor.green
                        if value.startswith("+")
                        else Qt.GlobalColor.white
                    )

                table.setItem(row, col, item)

            table.setRowHeight(row, 35)

        return table

    def make_activity(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        layout.addWidget(label("Activity", "pageTitle"))
        layout.addWidget(label(
            "A closer look at your fictional transactions.",
            "subtitle"
        ))

        info = panel()
        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(18, 17, 18, 17)
        info_layout.addWidget(label("Transaction ledger", "sectionTitle"))
        info_layout.addWidget(label(
            "Sample records for UI demonstration only.",
            "muted"
        ))
        layout.addWidget(info)

        ledger = panel()
        ledger_layout = QVBoxLayout(ledger)
        ledger_layout.setContentsMargins(12, 12, 12, 12)

        self.activity_table = self.create_transaction_table()
        self.activity_table.setRowCount(8)

        extra_transactions = [
            ("Music subscription", "Oct 12", "-$10.99"),
            ("Demo refund", "Oct 11", "+$15.00"),
            ("Book shop", "Oct 09", "-$22.00"),
        ]

        for row, transaction in enumerate(extra_transactions, start=5):
            for col, value in enumerate(transaction):
                item = QTableWidgetItem(value)
                item.setFlags(
                    Qt.ItemFlag.ItemIsEnabled
                    | Qt.ItemFlag.ItemIsSelectable
                )
                self.activity_table.setItem(row, col, item)
            self.activity_table.setRowHeight(row, 35)

        ledger_layout.addWidget(self.activity_table)
        layout.addWidget(ledger, 1)

        note = label(
            "This simulator doesn't connect to banks or process payments.",
            "muted"
        )
        layout.addWidget(note)

        return page

    def make_prank_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        layout.addWidget(label("Prank Lab", "pageTitle"))
        layout.addWidget(label(
            "A little chaos, carefully contained.",
            "subtitle"
        ))

        hero = QFrame()
        hero.setObjectName("balanceCard")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(23, 23, 23, 23)
        hero_layout.setSpacing(10)

        hero_layout.addWidget(label("✳  TINY WINDOW GENERATOR", "muted"))
        hero_layout.addWidget(label(
            "One second. One window.",
            "sectionTitle"
        ))
        hero_layout.addWidget(label(
            "Start the prank to spawn a tiny floating window every "
            "second. Try closing one and it'll dodge away.",
            "subtitle"
        ))

        self.prank_counter = label("0 / 30 windows", "smallBalance")
        hero_layout.addWidget(self.prank_counter)

        self.prank_status = label("●  Ready to launch", "positive")
        hero_layout.addWidget(self.prank_status)

        layout.addWidget(hero)

        buttons = QHBoxLayout()
        self.start_prank_button = button("▶   Start Prank", "primary")
        self.start_prank_button.clicked.connect(self.start_prank)

        self.stop_prank_button = button("■   Stop & Close All", "danger")
        self.stop_prank_button.clicked.connect(self.stop_prank)

        buttons.addWidget(self.start_prank_button)
        buttons.addWidget(self.stop_prank_button)
        layout.addLayout(buttons)

        safety = panel()
        safety_layout = QVBoxLayout(safety)
        safety_layout.setContentsMargins(18, 17, 18, 17)
        safety_layout.setSpacing(8)

        safety_layout.addWidget(label("Safety controls", "sectionTitle"))
        safety_layout.addWidget(label(
            "• A maximum of 30 windows can be spawned per run.\n"
            "• Stop & Close All disables the dodge behavior and closes "
            "every prank window.\n"
            "• ⌘Q quits Dollar bank and stops the prank.\n"
            "• All displayed balances and transactions are fictional.",
            "subtitle"
        ))

        layout.addWidget(safety)
        layout.addStretch()

        return page

    def show_page(self, index):
        self.stack.setCurrentIndex(index)

        for i, nav in self.nav_buttons.items():
            nav.setObjectName("navActive" if i == index else "")
            nav.style().unpolish(nav)
            nav.style().polish(nav)
            nav.update()

    def refresh_balance(self):
        self.balance_label.setText(f"${self.balance:,.2f}")

    def start_prank(self):
        if self.prank_running:
            self.show_page(2)
            return

        if self.window_count >= MAX_WINDOWS:
            self.window_count = 0

        self.prank_running = True
        self.spawn_timer.start()
        self.refresh_prank_status()
        self.show_page(2)

    def spawn_tiny_window(self):
        if not self.prank_running:
            return

        if self.window_count >= MAX_WINDOWS:
            self.spawn_timer.stop()
            self.prank_running = False
            self.refresh_prank_status()
            return

        self.window_count += 1

        tiny = TinyWindow(self, self.window_count)
        self.tiny_windows.append(tiny)
        tiny.show()
        tiny.raise_()

        self.refresh_prank_status()

        if self.window_count >= MAX_WINDOWS:
            self.spawn_timer.stop()
            self.prank_running = False
            self.refresh_prank_status()

    def stop_prank(self):
        self.prank_running = False
        self.spawn_timer.stop()

        old_windows = self.tiny_windows[:]
        self.tiny_windows.clear()

        for tiny in old_windows:
            tiny.close()
            tiny.deleteLater()

        self.refresh_prank_status()

    def refresh_prank_status(self):
        self.prank_counter.setText(
            f"{self.window_count} / {MAX_WINDOWS} windows"
        )

        if self.prank_running:
            self.prank_status.setText("●  Prank is running")
            self.prank_status.setStyleSheet(f"color: {BLUE};")
        elif self.window_count >= MAX_WINDOWS:
            self.prank_status.setText("●  Safety limit reached")
            self.prank_status.setStyleSheet(f"color: {GREEN};")
        else:
            self.prank_status.setText("●  Ready to launch")
            self.prank_status.setStyleSheet(f"color: {MUTED};")

        self.start_prank_button.setEnabled(not self.prank_running)
        self.stop_prank_button.setEnabled(
            self.prank_running or bool(self.tiny_windows)
        )

    def closeEvent(self, event):
        self.stop_prank()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("EarthOS")
    app.setQuitOnLastWindowClosed(True)

    if ICON_PATH.exists():
        app.setWindowIcon(QIcon(str(ICON_PATH)))

    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)

    window = DollarBank()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
