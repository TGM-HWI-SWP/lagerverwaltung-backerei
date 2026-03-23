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
    QMessageBox,
    QTabWidget,
)

from ..adapters.repository import RepositoryFactory
from ..services import WarehouseService
from .dialogs import ProductDialogWindow


class WarehouseMainWindow(QMainWindow):
    """Hauptfenster der Lagerverwaltungsanwendung"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lagerverwaltungssystem v0.2.0")
        self.setGeometry(100, 100, 1000, 600)

        # Initialisiere Service
        self.repository = RepositoryFactory.create_repository("memory")
        self.service = WarehouseService(self.repository)

        # Erstelle UI
        self._create_ui()

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

    def _create_products_tab(self):
        """Tab für Produktverwaltung"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Produkt hinzufügen")
        refresh_btn = QPushButton("Aktualisieren")
        delete_btn = QPushButton("Löschen")

        add_btn.clicked.connect(self._add_product)
        refresh_btn.clicked.connect(self._refresh_products)
        delete_btn.clicked.connect(self._delete_product)

        button_layout.addWidget(add_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(delete_btn)

        layout.addLayout(button_layout)

        # Produkttabelle
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(6)
        self.products_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Kategorie", "Bestand", "Preis (€)", "Gesamtwert (€)"]
        )
        layout.addWidget(self.products_table)

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Produkte")

    def _create_movements_tab(self):
        """Tab für Lagerbewegungen"""
        widget = QWidget()
        layout = QVBoxLayout()

        info_label = QLabel("Lagerbewegungen werden hier angezeigt")
        layout.addWidget(info_label)

        self.movements_table = QTableWidget()
        self.movements_table.setColumnCount(5)
        self.movements_table.setHorizontalHeaderLabels(
            ["Zeitstempel", "Produkt", "Typ", "Menge", "Grund"]
        )
        layout.addWidget(self.movements_table)

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Lagerbewegungen")

    def _create_reports_tab(self):
        """Tab für Berichte"""
        widget = QWidget()
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        inventory_btn = QPushButton("Lagerbestandsbericht")
        movement_btn = QPushButton("Bewegungsprotokoll")

        inventory_btn.clicked.connect(self._show_inventory_report)
        movement_btn.clicked.connect(self._show_movement_report)

        button_layout.addWidget(inventory_btn)
        button_layout.addWidget(movement_btn)
        layout.addLayout(button_layout)

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Berichte")

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
                QMessageBox.information(self, "Erfolg", "Produkt erfolgreich hinzugefügt")
                self._refresh_products()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", str(e))

    def _refresh_products(self):
        """Produkttabelle aktualisieren"""
        products = self.service.get_all_products()
        self.products_table.setRowCount(len(products))

        for row, (product_id, product) in enumerate(products.items()):
            self.products_table.setItem(row, 0, QTableWidgetItem(product_id))
            self.products_table.setItem(row, 1, QTableWidgetItem(product.name))
            self.products_table.setItem(row, 2, QTableWidgetItem(product.category))
            self.products_table.setItem(row, 3, QTableWidgetItem(str(product.quantity)))
            self.products_table.setItem(row, 4, QTableWidgetItem(f"{product.price:.2f}"))
            self.products_table.setItem(
                row, 5, QTableWidgetItem(f"{product.get_total_value():.2f}")
            )

    def _delete_product(self):
        """Produkt löschen"""
        QMessageBox.information(self, "Info", "Delete-Funktion wird implementiert")

    def _show_inventory_report(self):
        """Lagerbestandsbericht anzeigen"""
        QMessageBox.information(
            self, "Lagerbestandsbericht", "Report-Funktion wird implementiert"
        )

    def _show_movement_report(self):
        """Bewegungsprotokoll anzeigen"""
        QMessageBox.information(
            self, "Bewegungsprotokoll", "Report-Funktion wird implementiert"
        )
