"""Main Window - Hauptfenster der Lagerverwaltung"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QLineEdit,
    QMessageBox,
    QTabWidget,
    QTextEdit,
    QHeaderView,
    QStatusBar,
    QFileDialog,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from ..adapters.repository import RepositoryFactory
from ..adapters.report import ConsoleReportAdapter
from ..services import WarehouseService
from .dialogs import ProductDialogWindow, StockDialog

# Schwellenwerte für Bestandsfarben
STOCK_CRITICAL = 5
STOCK_WARNING = 15


class WarehouseMainWindow(QMainWindow):
    """Hauptfenster der Lagerverwaltungsanwendung"""

    def __init__(self, repository_type: str = "memory", db_path: str = "data.db"):
        super().__init__()
        self.setWindowTitle("Lagerverwaltungssystem v0.4.0")
        self.setGeometry(100, 100, 1100, 700)
        self.setMinimumSize(800, 500)

        # Initialisiere Service
        self.repository = RepositoryFactory.create_repository(
            repository_type,
            db_path=db_path,
        )
        self.service = WarehouseService(self.repository)

        # Erstelle UI
        self._create_ui()
        self._create_status_bar()

        # Beim Start sofort Daten aus Repository anzeigen
        self._refresh_products()
        self._refresh_movements()

    def closeEvent(self, event):
        """Schließt offene Ressourcen beim Beenden der Anwendung."""
        close_fn = getattr(self.repository, "close", None)
        if callable(close_fn):
            close_fn()
        super().closeEvent(event)

    def _create_ui(self):
        """Erstelle die Benutzeroberfläche"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # Tab-Widget
        self.tabs = QTabWidget()
        self._create_products_tab()
        self._create_movements_tab()
        self._create_reports_tab()

        main_layout.addWidget(self.tabs)
        central_widget.setLayout(main_layout)

    def _create_status_bar(self):
        """Statusleiste mit Lager-Statistiken"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_product_count = QLabel("Produkte: 0")
        self.status_total_value = QLabel("Gesamtwert: 0.00 \u20ac")
        self.status_bar.addPermanentWidget(self.status_product_count)
        self.status_bar.addPermanentWidget(QLabel("  |  "))
        self.status_bar.addPermanentWidget(self.status_total_value)
        self._update_status_bar()

    def _update_status_bar(self):
        """Statusleiste aktualisieren"""
        products = self.service.get_all_products()
        count = len(products)
        total = self.service.get_total_inventory_value()
        self.status_product_count.setText(f"Produkte: {count}")
        self.status_total_value.setText(f"Gesamtwert: {total:.2f} \u20ac")

    # ── Produkte-Tab ──────────────────────────────────────────────

    def _create_products_tab(self):
        """Tab für Produktverwaltung"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Suchleiste
        search_layout = QHBoxLayout()
        search_label = QLabel("Suche:")
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Nach Name, ID oder Kategorie filtern...")
        self.search_field.textChanged.connect(self._filter_products)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_field)
        layout.addLayout(search_layout)

        # Buttons
        button_layout = QHBoxLayout()

        add_btn = QPushButton("Produkt hinzuf\u00fcgen")
        edit_btn = QPushButton("Bearbeiten")
        delete_btn = QPushButton("L\u00f6schen")
        delete_btn.setObjectName("delete_btn")
        stock_in_btn = QPushButton("Einlagern")
        stock_in_btn.setObjectName("stock_in_btn")
        stock_out_btn = QPushButton("Auslagern")
        stock_out_btn.setObjectName("stock_out_btn")
        refresh_btn = QPushButton("Aktualisieren")

        add_btn.clicked.connect(self._add_product)
        edit_btn.clicked.connect(self._edit_product)
        delete_btn.clicked.connect(self._delete_product)
        stock_in_btn.clicked.connect(self._stock_in)
        stock_out_btn.clicked.connect(self._stock_out)
        refresh_btn.clicked.connect(self._refresh_products)

        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(stock_in_btn)
        button_layout.addWidget(stock_out_btn)
        button_layout.addWidget(refresh_btn)

        layout.addLayout(button_layout)

        # Produkttabelle
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(6)
        self.products_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Kategorie", "Bestand", "Preis (\u20ac)", "Gesamtwert (\u20ac)"]
        )
        self.products_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.products_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.products_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.products_table.setAlternatingRowColors(True)
        self.products_table.horizontalHeader().setStretchLastSection(True)
        self.products_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        self.products_table.horizontalHeader().setMinimumSectionSize(80)
        self.products_table.setMinimumHeight(200)
        layout.addWidget(self.products_table)

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Produkte")

    # ── Lagerbewegungen-Tab ───────────────────────────────────────

    def _create_movements_tab(self):
        """Tab für Lagerbewegungen"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Buttons
        button_layout = QHBoxLayout()
        refresh_mov_btn = QPushButton("Aktualisieren")
        refresh_mov_btn.clicked.connect(self._refresh_movements)
        button_layout.addWidget(refresh_mov_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Bewegungs-Tabelle
        self.movements_table = QTableWidget()
        self.movements_table.setColumnCount(6)
        self.movements_table.setHorizontalHeaderLabels(
            ["Zeitstempel", "Produkt", "Typ", "Menge", "Grund", "Benutzer"]
        )
        self.movements_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.movements_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.movements_table.setAlternatingRowColors(True)
        self.movements_table.horizontalHeader().setStretchLastSection(True)
        self.movements_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        self.movements_table.horizontalHeader().setMinimumSectionSize(80)
        self.movements_table.setMinimumHeight(200)
        layout.addWidget(self.movements_table)

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Lagerbewegungen")

    # ── Berichte-Tab ──────────────────────────────────────────────

    def _create_reports_tab(self):
        """Tab für Berichte"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Report-Buttons
        button_layout = QHBoxLayout()
        inventory_btn = QPushButton("Lagerbestandsbericht")
        movement_btn = QPushButton("Bewegungsprotokoll")
        self.export_btn = QPushButton("Als Datei exportieren")
        self.export_btn.setEnabled(False)

        inventory_btn.clicked.connect(self._show_inventory_report)
        movement_btn.clicked.connect(self._show_movement_report)
        self.export_btn.clicked.connect(self._export_report)

        button_layout.addWidget(inventory_btn)
        button_layout.addWidget(movement_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.export_btn)
        layout.addLayout(button_layout)

        # Textfeld für Report-Ausgabe
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setPlaceholderText(
            "Klicke auf einen der Buttons oben, um einen Bericht zu erstellen..."
        )
        layout.addWidget(self.report_text)

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Berichte")

    # ── Hilfsmethode: Ausgewähltes Produkt ────────────────────────

    def _get_selected_product_id(self):
        """Gibt die ID des ausgewählten Produkts zurück oder None"""
        selected = self.products_table.selectedItems()
        if not selected:
            QMessageBox.warning(
                self, "Keine Auswahl", "Bitte w\u00e4hle zuerst ein Produkt aus der Tabelle."
            )
            return None
        row = selected[0].row()
        return self.products_table.item(row, 0).text()

    # ── Produkt hinzufügen ────────────────────────────────────────

    def _add_product(self):
        """Neues Produkt hinzufügen"""
        dialog = ProductDialogWindow(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.service.create_product(
                    product_id=data["product_id"],
                    name=data["name"],
                    description=data["description"],
                    price=data["price"],
                    category=data["category"],
                    initial_quantity=data["quantity"],
                )
                QMessageBox.information(self, "Erfolg", "Produkt erfolgreich hinzugef\u00fcgt.")
                self._refresh_products()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", str(e))

    # ── Produkt bearbeiten ────────────────────────────────────────

    def _edit_product(self):
        """Ausgewähltes Produkt bearbeiten"""
        product_id = self._get_selected_product_id()
        if not product_id:
            return

        product = self.service.get_product(product_id)
        if not product:
            QMessageBox.critical(self, "Fehler", "Produkt nicht gefunden.")
            return

        dialog = ProductDialogWindow(
            self,
            product_data={
                "product_id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "quantity": product.quantity,
                "category": product.category,
            },
        )

        if dialog.exec():
            data = dialog.get_data()
            try:
                product.name = data["name"]
                product.description = data["description"]
                product.price = data["price"]
                product.category = data["category"]
                self.repository.save_product(product)
                QMessageBox.information(self, "Erfolg", "Produkt erfolgreich aktualisiert.")
                self._refresh_products()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", str(e))

    # ── Produkt löschen ───────────────────────────────────────────

    def _delete_product(self):
        """Ausgewähltes Produkt löschen"""
        product_id = self._get_selected_product_id()
        if not product_id:
            return

        product = self.service.get_product(product_id)
        name = product.name if product else product_id

        reply = QMessageBox.question(
            self,
            "L\u00f6schen best\u00e4tigen",
            f"Soll das Produkt \"{name}\" (ID: {product_id}) wirklich gel\u00f6scht werden?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.service.delete_product(product_id)
                QMessageBox.information(self, "Erfolg", "Produkt erfolgreich gel\u00f6scht.")
                self._refresh_products()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", str(e))

    # ── Bestandsänderungen ────────────────────────────────────────

    def _stock_in(self):
        """Bestand einlagern"""
        self._adjust_stock("in")

    def _stock_out(self):
        """Bestand auslagern"""
        self._adjust_stock("out")

    def _adjust_stock(self, mode):
        """Bestand ändern (ein- oder auslagern)"""
        product_id = self._get_selected_product_id()
        if not product_id:
            return

        product = self.service.get_product(product_id)
        if not product:
            QMessageBox.critical(self, "Fehler", "Produkt nicht gefunden.")
            return

        dialog = StockDialog(self, product_name=product.name, mode=mode)
        if dialog.exec():
            data = dialog.get_data()
            try:
                if mode == "in":
                    self.service.add_to_stock(
                        product_id, data["quantity"], data["reason"], data["user"]
                    )
                else:
                    self.service.remove_from_stock(
                        product_id, data["quantity"], data["reason"], data["user"]
                    )
                QMessageBox.information(
                    self,
                    "Erfolg",
                    f"Bestand erfolgreich {'erh\u00f6ht' if mode == 'in' else 'verringert'}.",
                )
                self._refresh_products()
                self._refresh_movements()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", str(e))

    # ── Tabellen aktualisieren ────────────────────────────────────

    def _refresh_products(self):
        """Produkttabelle aktualisieren"""
        products = self.service.get_all_products()
        self.products_table.setRowCount(len(products))

        for row, (product_id, product) in enumerate(products.items()):
            self.products_table.setItem(row, 0, QTableWidgetItem(product_id))
            self.products_table.setItem(row, 1, QTableWidgetItem(product.name))
            self.products_table.setItem(row, 2, QTableWidgetItem(product.category))

            # Bestand mit Farbcodierung
            qty_item = QTableWidgetItem(str(product.quantity))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if product.quantity <= STOCK_CRITICAL:
                qty_item.setBackground(QColor("#e74c3c"))
                qty_item.setForeground(QColor("#ffffff"))
            elif product.quantity <= STOCK_WARNING:
                qty_item.setBackground(QColor("#f39c12"))
                qty_item.setForeground(QColor("#ffffff"))
            else:
                qty_item.setBackground(QColor("#27ae60"))
                qty_item.setForeground(QColor("#ffffff"))
            self.products_table.setItem(row, 3, qty_item)

            self.products_table.setItem(row, 4, QTableWidgetItem(f"{product.price:.2f}"))
            self.products_table.setItem(
                row, 5, QTableWidgetItem(f"{product.get_total_value():.2f}")
            )

        # Suchfilter erneut anwenden falls aktiv
        search_text = self.search_field.text()
        if search_text:
            self._filter_products(search_text)

        self._update_status_bar()

    def _refresh_movements(self):
        """Lagerbewegungen-Tabelle aktualisieren"""
        movements = self.service.get_movements()
        # Neueste zuerst (bei gleichen Timestamps OUT priorisieren)
        # Sortiere nach Zeitstempel absteigend; bei gleichen Zeitstempeln OUT zuerst
        movements_sorted = sorted(
            movements,
            key=lambda m: (m.timestamp, 1 if m.movement_type == "OUT" else 0),
            reverse=True,
        )
        self.movements_table.setRowCount(len(movements_sorted))

        for row, movement in enumerate(movements_sorted):
            self.movements_table.setItem(
                row, 0, QTableWidgetItem(movement.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
            )
            self.movements_table.setItem(
                row, 1, QTableWidgetItem(f"{movement.product_name} ({movement.product_id})")
            )

            # Bewegungstyp farblich markieren
            type_item = QTableWidgetItem(movement.movement_type)
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if movement.movement_type == "IN":
                type_item.setForeground(QColor("#27ae60"))
            elif movement.movement_type == "OUT":
                type_item.setForeground(QColor("#c0392b"))
            self.movements_table.setItem(row, 2, type_item)

            qty_item = QTableWidgetItem(f"{movement.quantity_change:+d}")
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.movements_table.setItem(row, 3, qty_item)

            self.movements_table.setItem(
                row, 4, QTableWidgetItem(movement.reason or "")
            )
            self.movements_table.setItem(
                row, 5, QTableWidgetItem(movement.performed_by)
            )

    # ── Suchfunktion ──────────────────────────────────────────────

    def _filter_products(self, search_text):
        """Produkttabelle nach Suchbegriff filtern"""
        search_lower = search_text.lower()
        for row in range(self.products_table.rowCount()):
            match = False
            # Spalten 0 (ID), 1 (Name), 2 (Kategorie) durchsuchen
            for col in range(3):
                item = self.products_table.item(row, col)
                if item and search_lower in item.text().lower():
                    match = True
                    break
            self.products_table.setRowHidden(row, not match)

    # ── Berichte ──────────────────────────────────────────────────

    def _show_inventory_report(self):
        """Lagerbestandsbericht generieren und anzeigen"""
        products = self.service.get_all_products()
        adapter = ConsoleReportAdapter(products=products)
        report = adapter.generate_inventory_report()
        self.report_text.setText(report)
        self.export_btn.setEnabled(True)

    def _show_movement_report(self):
        """Bewegungsprotokoll generieren und anzeigen"""
        movements = self.service.get_movements()
        adapter = ConsoleReportAdapter(movements=movements)
        report = adapter.generate_movement_report()
        self.report_text.setText(report)
        self.export_btn.setEnabled(True)

    def _export_report(self):
        """Aktuellen Bericht als Textdatei exportieren"""
        content = self.report_text.toPlainText()
        if not content:
            QMessageBox.warning(self, "Kein Bericht", "Es gibt keinen Bericht zum Exportieren.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Bericht exportieren",
            "bericht.txt",
            "Textdateien (*.txt);;Alle Dateien (*)",
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                QMessageBox.information(
                    self, "Erfolg", f"Bericht erfolgreich exportiert nach:\n{file_path}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Export fehlgeschlagen: {e}")
