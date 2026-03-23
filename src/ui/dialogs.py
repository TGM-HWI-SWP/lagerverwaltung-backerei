"""Dialogs - Dialogfenster für die Lagerverwaltung"""

from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QLabel,
    QComboBox,
)


class ProductDialogWindow(QDialog):
    """Dialog zum Hinzufügen/Bearbeiten von Produkten"""

    def __init__(self, parent=None, product_data=None):
        super().__init__(parent)
        self._edit_mode = product_data is not None
        self.setWindowTitle("Produkt bearbeiten" if self._edit_mode else "Produkt hinzufügen")
        self.setGeometry(100, 100, 400, 300)

        layout = QFormLayout()

        self.product_id_field = QLineEdit()
        self.name_field = QLineEdit()
        self.description_field = QLineEdit()
        self.price_field = QDoubleSpinBox()
        self.price_field.setMaximum(999999)
        self.price_field.setDecimals(2)
        self.price_field.setSuffix(" €")
        self.quantity_field = QSpinBox()
        self.quantity_field.setMaximum(999999)
        self.category_field = QLineEdit()

        layout.addRow("Produkt-ID:", self.product_id_field)
        layout.addRow("Name:", self.name_field)
        layout.addRow("Beschreibung:", self.description_field)
        layout.addRow("Preis:", self.price_field)
        layout.addRow("Menge:", self.quantity_field)
        layout.addRow("Kategorie:", self.category_field)

        if self._edit_mode:
            self.product_id_field.setText(product_data["product_id"])
            self.product_id_field.setReadOnly(True)
            self.name_field.setText(product_data["name"])
            self.description_field.setText(product_data.get("description", ""))
            self.price_field.setValue(product_data["price"])
            self.quantity_field.setValue(product_data["quantity"])
            self.quantity_field.setReadOnly(True)
            self.category_field.setText(product_data.get("category", ""))

        button_layout = QHBoxLayout()
        ok_btn = QPushButton("Speichern" if self._edit_mode else "Hinzufügen")
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


class StockDialog(QDialog):
    """Dialog für Bestandsänderungen (Einlagern/Auslagern)"""

    def __init__(self, parent=None, product_name="", mode="in"):
        super().__init__(parent)
        is_in = mode == "in"
        self.setWindowTitle("Einlagern" if is_in else "Auslagern")
        self.setGeometry(100, 100, 350, 200)

        layout = QFormLayout()

        product_label = QLabel(product_name)
        product_label.setStyleSheet("font-weight: bold;")
        layout.addRow("Produkt:", product_label)

        self.quantity_field = QSpinBox()
        self.quantity_field.setMinimum(1)
        self.quantity_field.setMaximum(999999)
        layout.addRow("Menge:", self.quantity_field)

        self.reason_field = QLineEdit()
        self.reason_field.setPlaceholderText("z.B. Lieferung, Verkauf, Korrektur...")
        layout.addRow("Grund:", self.reason_field)

        self.user_field = QLineEdit()
        self.user_field.setPlaceholderText("Name des Mitarbeiters")
        layout.addRow("Benutzer:", self.user_field)

        button_layout = QHBoxLayout()
        ok_btn = QPushButton("Einlagern" if is_in else "Auslagern")
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
            "quantity": self.quantity_field.value(),
            "reason": self.reason_field.text(),
            "user": self.user_field.text() or "system",
        }
