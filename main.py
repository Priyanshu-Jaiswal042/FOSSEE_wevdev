import sys
import requests
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QFileDialog, QTabWidget, QMessageBox, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_URL = 'http://localhost:8000/api'


class LoginWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Login')
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        title = QLabel('Chemical Equipment Visualizer')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.mode_label = QLabel('Login')
        self.mode_label.setFont(QFont('Arial', 14))
        self.mode_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mode_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        layout.addWidget(self.username_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Email (optional for registration)')
        self.email_input.hide()
        layout.addWidget(self.email_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        self.error_label = QLabel('')
        self.error_label.setStyleSheet('color: red;')
        layout.addWidget(self.error_label)
        
        self.login_btn = QPushButton('Login')
        self.login_btn.clicked.connect(self.handle_auth)
        layout.addWidget(self.login_btn)
        
        self.toggle_btn = QPushButton('Switch to Register')
        self.toggle_btn.clicked.connect(self.toggle_mode)
        layout.addWidget(self.toggle_btn)
        
        self.setLayout(layout)
        self.is_register = False
    
    def toggle_mode(self):
        self.is_register = not self.is_register
        if self.is_register:
            self.mode_label.setText('Register')
            self.login_btn.setText('Register')
            self.toggle_btn.setText('Switch to Login')
            self.email_input.show()
        else:
            self.mode_label.setText('Login')
            self.login_btn.setText('Login')
            self.toggle_btn.setText('Switch to Register')
            self.email_input.hide()
    
    def handle_auth(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()
        
        if not username or not password:
            self.error_label.setText('Username and password are required')
            return
        
        try:
            endpoint = '/auth/register/' if self.is_register else '/auth/login/'
            payload = {'username': username, 'password': password}
            
            if self.is_register:
                payload['email'] = email
            
            response = requests.post(f'{API_URL}{endpoint}', json=payload)
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.main_window.set_token(data['token'], data['user'])
                self.close()
                self.main_window.show()
            else:
                self.error_label.setText(response.json().get('error', 'Authentication failed'))
        
        except Exception as e:
            self.error_label.setText(f'Error: {str(e)}')


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.token = None
        self.user = None
        self.current_dataset = None
        self.datasets = []
        
        self.login_window = LoginWindow(self)
        self.login_window.show()
    
    def set_token(self, token, user):
        self.token = token
        self.user = user
        self.init_ui()
        self.load_history()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Parameter Visualizer')
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        # Header
        header = QHBoxLayout()
        title = QLabel(f'Welcome, {self.user["username"]}')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        header.addWidget(title)
        
        logout_btn = QPushButton('Logout')
        logout_btn.clicked.connect(self.logout)
        header.addWidget(logout_btn)
        
        main_layout.addLayout(header)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Upload Tab
        self.upload_tab = self.create_upload_tab()
        self.tabs.addTab(self.upload_tab, 'Upload CSV')
        
        # Visualization Tab
        self.viz_tab = self.create_visualization_tab()
        self.tabs.addTab(self.viz_tab, 'Visualization')
        
        # History Tab
        self.history_tab = self.create_history_tab()
        self.tabs.addTab(self.history_tab, 'History')
        
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
    
    def create_upload_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel('Select CSV File to Upload')
        label.setFont(QFont('Arial', 12))
        layout.addWidget(label)
        
        file_layout = QHBoxLayout()
        self.file_label = QLabel('No file selected')
        file_layout.addWidget(self.file_label)
        
        browse_btn = QPushButton('Browse')
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
        upload_btn = QPushButton('Upload & Analyze')
        upload_btn.clicked.connect(self.upload_file)
        layout.addWidget(upload_btn)
        
        info = QLabel('Expected CSV Format:\nColumns: Equipment Name, Type, Flowrate, Pressure, Temperature')
        info.setStyleSheet('background-color: #f0f0f0; padding: 10px; border-radius: 5px;')
        layout.addWidget(info)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_visualization_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Summary section
        self.summary_label = QLabel('No dataset loaded')
        self.summary_label.setFont(QFont('Arial', 10))
        layout.addWidget(self.summary_label)
        
        # Charts
        self.chart_canvas = MplCanvas(self, width=10, height=8, dpi=100)
        layout.addWidget(self.chart_canvas)
        
        # Data table
        self.data_table = QTableWidget()
        layout.addWidget(self.data_table)
        
        # PDF button
        pdf_btn = QPushButton('Generate PDF Report')
        pdf_btn.clicked.connect(self.generate_pdf)
        layout.addWidget(pdf_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel('Upload History (Last 5)')
        label.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(label)
        
        self.history_combo = QComboBox()
        self.history_combo.currentIndexChanged.connect(self.load_dataset_from_history)
        layout.addWidget(self.history_combo)
        
        self.history_details = QTextEdit()
        self.history_details.setReadOnly(True)
        layout.addWidget(self.history_details)
        
        widget.setLayout(layout)
        return widget
    
    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if filename:
            self.selected_file = filename
            self.file_label.setText(filename.split('/')[-1])
    
    def upload_file(self):
        if not hasattr(self, 'selected_file'):
            QMessageBox.warning(self, 'Warning', 'Please select a file first')
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                headers = {'Authorization': f'Token {self.token}'}
                
                response = requests.post(
                    f'{API_URL}/datasets/upload_csv/',
                    files=files,
                    headers=headers
                )
            
            if response.status_code == 201:
                self.current_dataset = response.json()
                self.update_visualization()
                self.load_history()
                self.tabs.setCurrentIndex(1)
                QMessageBox.information(self, 'Success', 'File uploaded successfully!')
            else:
                QMessageBox.critical(self, 'Error', response.json().get('error', 'Upload failed'))
        
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
    
    def load_history(self):
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(f'{API_URL}/datasets/history/', headers=headers)
            
            if response.status_code == 200:
                self.datasets = response.json()
                self.history_combo.clear()
                
                for dataset in self.datasets:
                    self.history_combo.addItem(
                        f"{dataset['filename']} - {dataset['upload_date'][:10]}",
                        dataset['id']
                    )
        
        except Exception as e:
            print(f'Failed to load history: {e}')
    
    def load_dataset_from_history(self, index):
        if index < 0 or index >= len(self.datasets):
            return
        
        dataset_id = self.datasets[index]['id']
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(f'{API_URL}/datasets/{dataset_id}/', headers=headers)
            
            if response.status_code == 200:
                self.current_dataset = response.json()
                
                # Update history details
                details = f"""
                Filename: {self.current_dataset['filename']}
                Upload Date: {self.current_dataset['upload_date']}
                Total Equipment: {self.current_dataset['total_equipment']}
                Average Flowrate: {self.current_dataset['avg_flowrate']:.2f}
                Average Pressure: {self.current_dataset['avg_pressure']:.2f}
                Average Temperature: {self.current_dataset['avg_temperature']:.2f}
                
                Equipment Type Distribution:
                """
                
                for eq_type, count in self.current_dataset['type_distribution'].items():
                    details += f"\n  {eq_type}: {count}"
                
                self.history_details.setText(details)
                
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load dataset: {e}')
    
    def update_visualization(self):
        if not self.current_dataset:
            return
        
        # Update summary
        summary = f"""
        Filename: {self.current_dataset['filename']}
        Total Equipment: {self.current_dataset['total_equipment']}
        Avg Flowrate: {self.current_dataset['avg_flowrate']:.2f}
        Avg Pressure: {self.current_dataset['avg_pressure']:.2f}
        Avg Temperature: {self.current_dataset['avg_temperature']:.2f}
        """
        self.summary_label.setText(summary)
        
        # Update charts
        self.chart_canvas.axes.clear()
        
        # Create subplots
        self.chart_canvas.figure.clear()
        ax1 = self.chart_canvas.figure.add_subplot(121)
        ax2 = self.chart_canvas.figure.add_subplot(122)
        
        # Type distribution pie chart
        types = list(self.current_dataset['type_distribution'].keys())
        counts = list(self.current_dataset['type_distribution'].values())
        ax1.pie(counts, labels=types, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Equipment Type Distribution')
        
        # Parameter bar chart
        if self.current_dataset['raw_data']:
            df = pd.DataFrame(self.current_dataset['raw_data'])
            params = ['Flowrate', 'Pressure', 'Temperature']
            avg_values = [df[param].mean() for param in params]
            ax2.bar(params, avg_values, color=['#FF6384', '#36A2EB', '#4BC0C0'])
            ax2.set_title('Average Parameters')
            ax2.set_ylabel('Value')
        
        self.chart_canvas.figure.tight_layout()
        self.chart_canvas.draw()
        
        # Update data table
        if self.current_dataset['raw_data']:
            df = pd.DataFrame(self.current_dataset['raw_data'])
            self.data_table.setRowCount(len(df))
            self.data_table.setColumnCount(len(df.columns))
            self.data_table.setHorizontalHeaderLabels(df.columns)
            
            for i, row in df.iterrows():
                for j, value in enumerate(row):
                    self.data_table.setItem(i, j, QTableWidgetItem(str(value)))
    
    def generate_pdf(self):
        if not self.current_dataset:
            QMessageBox.warning(self, 'Warning', 'No dataset loaded')
            return
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(
                f"{API_URL}/datasets/{self.current_dataset['id']}/generate_pdf/",
                headers=headers
            )
            
            if response.status_code == 200:
                filename, _ = QFileDialog.getSaveFileName(
                    self, 'Save PDF', f"report_{self.current_dataset['filename']}.pdf", 
                    'PDF Files (*.pdf)'
                )
                
                if filename:
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, 'Success', 'PDF report generated successfully!')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to generate PDF')
        
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
    
    def logout(self):
        self.token = None
        self.user = None
        self.current_dataset = None
        self.close()
        self.login_window = LoginWindow(self)
        self.login_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())