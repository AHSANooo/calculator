"""
Simple Calculator Application
A clean, modern calculator with a beautiful UI
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QGridLayout, QPushButton, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class CalculatorButton(QPushButton):
    """Custom styled button for the calculator"""
    
    def __init__(self, text, button_type="number"):
        super().__init__(text)
        self.button_type = button_type
        self.setFixedSize(80, 80)
        self.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)
        self.apply_style()
    
    def apply_style(self):
        if self.button_type == "number":
            # Grey number buttons
            self.setStyleSheet("""
                QPushButton {
                    background-color: #505050;
                    color: white;
                    border: none;
                    border-radius: 40px;
                    font-size: 24px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #686868;
                }
                QPushButton:pressed {
                    background-color: #8a8a8a;
                }
            """)
        elif self.button_type == "operator":
            # Yellow operation buttons
            self.setStyleSheet("""
                QPushButton {
                    background-color: #FF9500;
                    color: white;
                    border: none;
                    border-radius: 40px;
                    font-size: 24px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #FFa833;
                }
                QPushButton:pressed {
                    background-color: #CC7700;
                }
            """)
        elif self.button_type == "function":
            # Light grey function buttons (AC, +/-, %)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #a5a5a5;
                    color: black;
                    border: none;
                    border-radius: 40px;
                    font-size: 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c5c5c5;
                }
                QPushButton:pressed {
                    background-color: #d5d5d5;
                }
            """)


class Calculator(QMainWindow):
    """Main Calculator Window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(360, 560)
        self.setStyleSheet("background-color: #000000;")
        
        # Calculator state
        self.current_input = "0"
        self.previous_value = None
        self.current_operator = None
        self.should_reset_input = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the calculator UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(15, 20, 15, 20)
        
        # Display
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setFont(QFont("Segoe UI", 48, QFont.Light))
        self.display.setFixedHeight(100)
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: #000000;
                color: white;
                border: none;
                padding-right: 15px;
                font-size: 48px;
            }
        """)
        main_layout.addWidget(self.display)
        
        # Button grid
        button_layout = QGridLayout()
        button_layout.setSpacing(12)
        
        # Button configuration: (text, row, col, button_type)
        buttons = [
            ("AC", 0, 0, "function"),
            ("+/-", 0, 1, "function"),
            ("%", 0, 2, "function"),
            ("÷", 0, 3, "operator"),
            
            ("7", 1, 0, "number"),
            ("8", 1, 1, "number"),
            ("9", 1, 2, "number"),
            ("×", 1, 3, "operator"),
            
            ("4", 2, 0, "number"),
            ("5", 2, 1, "number"),
            ("6", 2, 2, "number"),
            ("−", 2, 3, "operator"),
            
            ("1", 3, 0, "number"),
            ("2", 3, 1, "number"),
            ("3", 3, 2, "number"),
            ("+", 3, 3, "operator"),
            
            ("0", 4, 0, "number"),
            (".", 4, 2, "number"),
            ("=", 4, 3, "operator"),
        ]
        
        for text, row, col, btn_type in buttons:
            button = CalculatorButton(text, btn_type)
            
            # Make the 0 button span 2 columns
            if text == "0":
                button.setFixedSize(172, 80)  # Wider button
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #505050;
                        color: white;
                        border: none;
                        border-radius: 40px;
                        font-size: 24px;
                        font-weight: bold;
                        padding-left: 30px;
                        text-align: left;
                    }
                    QPushButton:hover {
                        background-color: #686868;
                    }
                    QPushButton:pressed {
                        background-color: #8a8a8a;
                    }
                """)
                button_layout.addWidget(button, row, col, 1, 2)
            else:
                button_layout.addWidget(button, row, col)
            
            button.clicked.connect(lambda checked, t=text: self.button_clicked(t))
        
        main_layout.addLayout(button_layout)
    
    def button_clicked(self, text):
        """Handle button clicks"""
        if text.isdigit():
            self.handle_digit(text)
        elif text == ".":
            self.handle_decimal()
        elif text == "AC":
            self.handle_clear()
        elif text == "+/-":
            self.handle_negate()
        elif text == "%":
            self.handle_percent()
        elif text == "=":
            self.handle_equals()
        else:
            self.handle_operator(text)
        
        self.update_display()
    
    def handle_digit(self, digit):
        """Handle digit input"""
        if self.should_reset_input or self.current_input == "0":
            self.current_input = digit
            self.should_reset_input = False
        else:
            if len(self.current_input.replace(".", "").replace("-", "")) < 9:
                self.current_input += digit
    
    def handle_decimal(self):
        """Handle decimal point"""
        if self.should_reset_input:
            self.current_input = "0."
            self.should_reset_input = False
        elif "." not in self.current_input:
            self.current_input += "."
    
    def handle_clear(self):
        """Clear all"""
        self.current_input = "0"
        self.previous_value = None
        self.current_operator = None
        self.should_reset_input = False
    
    def handle_negate(self):
        """Toggle positive/negative"""
        if self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
    
    def handle_percent(self):
        """Convert to percentage"""
        try:
            value = float(self.current_input)
            self.current_input = self.format_result(value / 100)
        except ValueError:
            pass
    
    def handle_operator(self, operator):
        """Handle operator input"""
        if self.previous_value is not None and not self.should_reset_input:
            self.calculate()
        
        self.previous_value = float(self.current_input)
        self.current_operator = operator
        self.should_reset_input = True
    
    def handle_equals(self):
        """Calculate result"""
        if self.previous_value is not None and self.current_operator:
            self.calculate()
            self.current_operator = None
    
    def calculate(self):
        """Perform calculation"""
        if self.previous_value is None or self.current_operator is None:
            return
        
        try:
            current = float(self.current_input)
            
            if self.current_operator == "+":
                result = self.previous_value + current
            elif self.current_operator == "−":
                result = self.previous_value - current
            elif self.current_operator == "×":
                result = self.previous_value * current
            elif self.current_operator == "÷":
                if current == 0:
                    self.current_input = "Error"
                    self.previous_value = None
                    self.should_reset_input = True
                    return
                result = self.previous_value / current
            else:
                return
            
            self.current_input = self.format_result(result)
            self.previous_value = result
            self.should_reset_input = True
            
        except (ValueError, OverflowError):
            self.current_input = "Error"
            self.previous_value = None
            self.should_reset_input = True
    
    def format_result(self, value):
        """Format the result for display"""
        if value == int(value):
            result = str(int(value))
        else:
            result = f"{value:.8f}".rstrip("0").rstrip(".")
        
        # Limit display length
        if len(result) > 12:
            result = f"{value:.6e}"
        
        return result
    
    def update_display(self):
        """Update the display"""
        display_text = self.current_input
        
        # Format with thousand separators for whole numbers
        try:
            if "." in display_text:
                parts = display_text.split(".")
                if parts[0].lstrip("-").isdigit():
                    sign = "-" if parts[0].startswith("-") else ""
                    integer_part = parts[0].lstrip("-")
                    formatted = f"{int(integer_part):,}"
                    display_text = f"{sign}{formatted}.{parts[1]}"
            elif display_text.lstrip("-").isdigit():
                sign = "-" if display_text.startswith("-") else ""
                display_text = f"{sign}{int(display_text.lstrip('-')):,}"
        except (ValueError, IndexError):
            pass
        
        self.display.setText(display_text)


def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Calculator")
    app.setStyle("Fusion")
    
    calculator = Calculator()
    calculator.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
