"""Product Dialog - Dialog für Produkteingabe"""

from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
)


class ProductDialogWindow(QDialog):
    """Dialog zum Hinzufügen/Bearbeiten von Produkten"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Produkt hinzufügen")
        self.setGeometry(100, 100, 400, 300)

        layout = QFormLayout()

        self.product_id_field = QLineEdit()
        self.name_field = QLineEdit()
        self.description_field = QLineEdit()
        self.price_field = QDoubleSpinBox()
        self.price_field.setMaximum(999999)
        self.quantity_field = QSpinBox()
        self.category_field = QLineEdit()

        layout.addRow("Produkt-ID:", self.product_id_field)
        layout.addRow("Name:", self.name_field)
        layout.addRow("Beschreibung:", self.description_field)
        layout.addRow("Preis (€):", self.price_field)
        layout.addRow("Menge:", self.quantity_field)
        layout.addRow("Kategorie:", self.category_field)

        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Abbrechen")

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

        layout.addRow(button_layout)
        self.setLayout(layout)

    def get_data(self):
        """Eingegebene Daten abrufen"""
        return {
            "product_id": self.product_id_field.text(),
            "name": self.name_field.text(),
            "description": self.description_field.text(),
            "price": self.price_field.value(),
            "quantity": self.quantity_field.value(),
            "category": self.category_field.text(),
        }
