import sys
import json
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QComboBox, QTextEdit, QPushButton,
                             QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt


class APITester(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("API Testing Tool")
        self.setGeometry(100, 100, 900, 700)
        
        self.init_ui()
        self.load_last_config()
    
    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Tab widget for different sections
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # Request Tab
        request_tab = QWidget()
        tab_widget.addTab(request_tab, "Request")
        
        # Request layout
        request_layout = QVBoxLayout(request_tab)
        
        # Method and URL
        method_url_layout = QHBoxLayout()
        
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
        method_url_layout.addWidget(self.method_combo)
        
        self.url_input = QLineEdit("http://")
        self.url_input.setPlaceholderText("Enter API URL")
        method_url_layout.addWidget(self.url_input)
        
        request_layout.addLayout(method_url_layout)
        
        # Headers
        headers_group = QWidget()
        headers_layout = QVBoxLayout(headers_group)
        
        headers_label = QLabel("Headers:")
        headers_layout.addWidget(headers_label)
        
        self.headers_table = QTableWidget()
        self.headers_table.setColumnCount(2)
        self.headers_table.setHorizontalHeaderLabels(["Key", "Value"])
        self.headers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.headers_table.verticalHeader().setVisible(False)
        headers_layout.addWidget(self.headers_table)
        
        headers_buttons_layout = QHBoxLayout()
        add_header_btn = QPushButton("Add Header")
        add_header_btn.clicked.connect(self.add_header_row)
        headers_buttons_layout.addWidget(add_header_btn)
        
        remove_header_btn = QPushButton("Remove Header")
        remove_header_btn.clicked.connect(self.remove_header_row)
        headers_buttons_layout.addWidget(remove_header_btn)
        
        headers_layout.addLayout(headers_buttons_layout)
        request_layout.addWidget(headers_group)
        
        # Request Body
        body_group = QWidget()
        body_layout = QVBoxLayout(body_group)
        
        body_label = QLabel("Request Body:")
        body_layout.addWidget(body_label)
        
        self.body_type_combo = QComboBox()
        self.body_type_combo.addItems(["None", "Form Data", "Raw JSON", "Text"])
        body_layout.addWidget(self.body_type_combo)
        
        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("Enter request body content")
        body_layout.addWidget(self.body_input)
        
        request_layout.addWidget(body_group)
        
        # Send button
        send_btn = QPushButton("Send Request")
        send_btn.clicked.connect(self.send_request)
        request_layout.addWidget(send_btn)
        
        # Response Tab
        response_tab = QWidget()
        tab_widget.addTab(response_tab, "Response")
        
        # Response layout
        response_layout = QVBoxLayout(response_tab)
        
        # Status
        self.status_label = QLabel("Status: Not sent")
        response_layout.addWidget(self.status_label)
        
        # Response headers
        response_headers_label = QLabel("Response Headers:")
        response_layout.addWidget(response_headers_label)
        
        self.response_headers_table = QTableWidget()
        self.response_headers_table.setColumnCount(2)
        self.response_headers_table.setHorizontalHeaderLabels(["Key", "Value"])
        self.response_headers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.response_headers_table.verticalHeader().setVisible(False)
        response_layout.addWidget(self.response_headers_table)
        
        # Response body
        response_body_label = QLabel("Response Body:")
        response_layout.addWidget(response_body_label)
        
        self.response_body = QTextEdit()
        self.response_body.setReadOnly(True)
        response_layout.addWidget(self.response_body)
        
        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        save_action = file_menu.addAction("Save Configuration")
        save_action.triggered.connect(self.save_config)
        
        load_action = file_menu.addAction("Load Configuration")
        load_action.triggered.connect(self.load_config)
        
        # Add a couple of default headers
        self.add_header_row("Content-Type", "application/json")
        self.add_header_row("Accept", "application/json")
    
    def add_header_row(self, key="", value=""):
        row = self.headers_table.rowCount()
        self.headers_table.insertRow(row)
        
        key_item = QTableWidgetItem(key)
        value_item = QTableWidgetItem(value)
        
        self.headers_table.setItem(row, 0, key_item)
        self.headers_table.setItem(row, 1, value_item)
    
    def remove_header_row(self):
        current_row = self.headers_table.currentRow()
        if current_row >= 0:
            self.headers_table.removeRow(current_row)
    
    def get_headers(self):
        headers = {}
        for row in range(self.headers_table.rowCount()):
            key = self.headers_table.item(row, 0).text().strip()
            value = self.headers_table.item(row, 1).text().strip()
            if key:
                headers[key] = value
        return headers
    
    def get_request_data(self):
        body_type = self.body_type_combo.currentText()
        body_text = self.body_input.toPlainText().strip()
        
        if body_type == "None" or not body_text:
            return None
        
        if body_type == "Raw JSON":
            try:
                return json.loads(body_text)
            except json.JSONDecodeError:
                QMessageBox.warning(self, "Invalid JSON", "The request body contains invalid JSON.")
                return None
        elif body_type == "Form Data":
            data = {}
            for line in body_text.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    data[key.strip()] = value.strip()
            return data
        else:  # Text
            return body_text
    
    def send_request(self):
        method = self.method_combo.currentText()
        url = self.url_input.text().strip()
        headers = self.get_headers()
        data = self.get_request_data()
        
        if not url:
            QMessageBox.warning(self, "Missing URL", "Please enter a URL to test.")
            return
        
        try:
            if method in ["GET", "HEAD", "DELETE", "OPTIONS"]:
                response = requests.request(method, url, headers=headers)
            else:
                if isinstance(data, dict):
                    response = requests.request(method, url, headers=headers, json=data)
                else:
                    response = requests.request(method, url, headers=headers, data=data)
            
            self.display_response(response)
        except requests.exceptions.RequestException as e:
            self.status_label.setText(f"Status: Error - {str(e)}")
            self.response_body.setPlainText(str(e))
    
    def display_response(self, response):
        # Status
        self.status_label.setText(f"Status: {response.status_code} {response.reason}")
        
        # Headers
        self.response_headers_table.setRowCount(0)
        for key, value in response.headers.items():
            row = self.response_headers_table.rowCount()
            self.response_headers_table.insertRow(row)
            self.response_headers_table.setItem(row, 0, QTableWidgetItem(key))
            self.response_headers_table.setItem(row, 1, QTableWidgetItem(value))
        
        # Body
        try:
            # Try to parse as JSON for pretty printing
            json_data = response.json()
            self.response_body.setPlainText(json.dumps(json_data, indent=2))
        except ValueError:
            # Fall back to raw text
            self.response_body.setPlainText(response.text)
    
    def save_config(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Configuration", "", "JSON Files (*.json);;All Files (*)", options=options)
        
        if file_name:
            config = {
                "method": self.method_combo.currentText(),
                "url": self.url_input.text(),
                "headers": self.get_headers(),
                "body_type": self.body_type_combo.currentText(),
                "body": self.body_input.toPlainText()
            }
            
            try:
                with open(file_name, 'w') as f:
                    json.dump(config, f, indent=2)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save configuration: {str(e)}")
    
    def load_config(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Load Configuration", "", "JSON Files (*.json);;All Files (*)", options=options)
        
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    config = json.load(f)
                
                self.method_combo.setCurrentText(config.get("method", "GET"))
                self.url_input.setText(config.get("url", "http://"))
                
                self.headers_table.setRowCount(0)
                for key, value in config.get("headers", {}).items():
                    self.add_header_row(key, value)
                
                self.body_type_combo.setCurrentText(config.get("body_type", "None"))
                self.body_input.setPlainText(config.get("body", ""))
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load configuration: {str(e)}")
    
    def load_last_config(self):
        # You could implement loading the last used config from a default location
        pass
    
    def closeEvent(self, event):
        # You could implement saving the current state before closing
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = APITester()
    window.show()
    sys.exit(app.exec_())