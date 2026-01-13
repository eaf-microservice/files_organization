import os
import shutil
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QTextEdit, QMessageBox, QDialog, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

# أنواع الملفات
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Programs": [".exe", ".msi"],
    "Compressed": [".zip", ".rar", ".7z"]
}


class OrganizerThread(QThread):
    """Thread class to handle file organization without freezing the UI"""
    progress = pyqtSignal(int)
    log_message = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
    
    def run(self):
        try:
            self.log_message.emit("Starting organization...")
            
            # إنشاء الفولدرات إذا لم تكن موجودة
            for folder in file_types.keys():
                folder_dir = os.path.join(self.folder_path, folder)
                os.makedirs(folder_dir, exist_ok=True)
                self.log_message.emit(f"Created folder: {folder}")
            
            # فولدر للملفات غير المعروفة
            others_folder = os.path.join(self.folder_path, "Others")
            os.makedirs(others_folder, exist_ok=True)
            self.log_message.emit("Created folder: Others")
            
            # بدء التنظيم
            files_to_move = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]
            total_files = len(files_to_move)
            files_moved = 0

            for file_name in files_to_move:
                file_path = os.path.join(self.folder_path, file_name)
                
                moved = False
                
                for folder, extensions in file_types.items():
                    if os.path.splitext(file_name)[1].lower() in extensions:
                        dest_path = os.path.join(self.folder_path, folder, file_name)
                        shutil.move(file_path, dest_path)
                        self.log_message.emit(f"Moved: {file_name} → {folder}")
                        moved = True
                        break
                
                if not moved:
                    dest_path = os.path.join(others_folder, file_name)
                    shutil.move(file_path, dest_path)
                    self.log_message.emit(f"Moved: {file_name} → Others")

                files_moved += 1
                progress_percentage = int((files_moved / total_files) * 100)
                self.progress.emit(progress_percentage)

            self.finished.emit(f"✅ Folder organized successfully! (Files moved: {files_moved})")
            
        except Exception as e:
            self.error.emit(f"An error occurred: {e}")

class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Organizing Files...")
        self.setWindowIcon(QIcon("assets/icon.png")) 
        self.setModal(True)
        self.setFixedSize(400, 120)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.status_label = QLabel("Organizing your files, please wait...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.status_label.font()
        font.setPointSize(10)
        self.status_label.setFont(font)
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_bar)

        self.details_label = QLabel("")
        self.details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.details_label.font()
        font.setPointSize(9)
        self.details_label.setFont(font)
        layout.addWidget(self.details_label)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_details(self, message):
        if "Moved:" in message:
            file_info = message.split("→")[0].replace("Moved:", "").strip()
            self.details_label.setText(f"Processing: {file_info}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_folder = ""
        self.init_ui()
        
        # Check for command-line arguments
        args = QApplication.arguments()
        if len(args) > 1 and os.path.isdir(args[1]):
            self.set_selected_folder(args[1])

    def init_ui(self):
        self.setWindowTitle("File Organizer")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setGeometry(100, 100, 600, 500)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Title
        title = QLabel("File Organizer")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Folder selection section
        folder_label = QLabel("Selected Folder:")
        folder_label.setFont(QFont("Arial", 10))
        layout.addWidget(folder_label)
        
        self.folder_path_label = QLabel("No folder selected")
        self.folder_path_label.setStyleSheet("padding: 5px; background-color: #f0f0f0; border: 1px solid #ccc;")
        self.folder_path_label.setWordWrap(True)
        layout.addWidget(self.folder_path_label)
        
        # Browse button
        browse_btn = QPushButton("Browse Folder")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        browse_btn.clicked.connect(self.browse_folder)
        layout.addWidget(browse_btn)
        
        # Organize button
        self.organize_btn = QPushButton("Organize Files")
        self.organize_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                font-size: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.organize_btn.clicked.connect(self.organize_files)
        self.organize_btn.setEnabled(False)
        layout.addWidget(self.organize_btn)

        # Status log
        log_label = QLabel("Status:")
        log_label.setFont(QFont("Arial", 10))
        layout.addWidget(log_label)
        
        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)
        self.status_log.setStyleSheet("""
            QTextEdit {
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                padding: 5px;
            }
        """)
        layout.addWidget(self.status_log)
        
        # File types info
        info_label = QLabel("File Categories:")
        info_label.setFont(QFont("Arial", 10))
        layout.addWidget(info_label)
        
        categories_text = ", ".join(file_types.keys())
        categories_label = QLabel(categories_text)
        categories_label.setStyleSheet("padding: 5px; background-color: #e3f2fd; border: 1px solid #90caf9;")
        categories_label.setWordWrap(True)
        layout.addWidget(categories_label)
        
        # About button
        about_btn = QPushButton("About")
        about_btn.setStyleSheet("""
            QPushButton {
                background-color: #9E9E9E;
                color: white;
                padding: 8px;
                font-size: 11px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #757575;
            }
        """)
        about_btn.clicked.connect(self.show_about)
        layout.addWidget(about_btn)

    def set_selected_folder(self, folder):
        if folder:
            self.selected_folder = folder
            self.folder_path_label.setText(folder)
            self.organize_btn.setEnabled(True)
            self.status_log.clear()
            self.status_log.append(f"Folder selected: {folder}")

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Organize")
        self.set_selected_folder(folder)
    
    def organize_files(self):
        if not self.selected_folder:
            QMessageBox.warning(self, "Warning", "Please select a folder first!")
            return
        
        if not os.path.exists(self.selected_folder):
            QMessageBox.warning(self, "Warning", "Selected folder does not exist!")
            return
        
        # Disable button during organization
        self.organize_btn.setEnabled(False)
        self.status_log.clear()
        self.status_log.append("Starting file organization...\n")

        # Create and show progress dialog
        self.progress_dialog = ProgressDialog(self)
        
        # Create and start thread
        self.organizer_thread = OrganizerThread(self.selected_folder)
        self.organizer_thread.progress.connect(self.progress_dialog.update_progress)
        self.organizer_thread.log_message.connect(self.update_status)
        self.organizer_thread.log_message.connect(self.progress_dialog.update_details)
        self.organizer_thread.finished.connect(self.organization_complete)
        self.organizer_thread.error.connect(self.organization_error)
        self.organizer_thread.start()

        # Show the dialog modally
        self.progress_dialog.exec()
    
    def update_status(self, message):
        self.status_log.append(message)
        # Auto-scroll to bottom
        self.status_log.verticalScrollBar().setValue(
            self.status_log.verticalScrollBar().maximum()
        )

    def organization_complete(self, message):
        self.progress_dialog.close()
        self.status_log.append(f"\n{message}")
        self.organize_btn.setEnabled(True)
        QMessageBox.information(self, "Success", message)
    
    def organization_error(self, error_message):
        self.progress_dialog.close()
        self.status_log.append(f"\n❌ {error_message}")
        self.organize_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", error_message)
    
    def show_about(self):
        about_text = """
        <h2>File Organizer</h2>
        <h3>By: Fouad El Azbi</h3>
        <h3>Company: EAF microservices</h3>
        <h3>Email: EAF.microservice@gmail.com</h3>
        <p><b>Version:</b> 1.0.2</p>
        <p>A simple and efficient tool to organize your files by extension.</p>
        
        <h3>Features:</h3>
        <ul>
            <li>Organize files by type automatically</li>
            <li>Support for multiple file categories</li>
            <li>Real-time progress tracking</li>
            <li>User-friendly interface</li>
        </ul>
        
        <h3>File Categories:</h3>
        <ul>
            <li><b>Images:</b> JPG, JPEG, PNG, GIF, BMP</li>
            <li><b>Documents:</b> PDF, DOCX, DOC, TXT, XLSX, XLS, PPTX, PPT</li>
            <li><b>Videos:</b> MP4, MKV, AVI, MOV, FLV</li>
            <li><b>Audio:</b> MP3, WAV, AAC</li>
            <li><b>Programs:</b> EXE, MSI</li>
            <li><b>Compressed:</b> ZIP, RAR, 7Z</li>
            <li><b>Others:</b> All other file types</li>
        </ul>
        
        
        <p>EAF microservices © 2026 File Organizer</p>
        """
        
        QMessageBox.about(self, "About File Organizer", about_text)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
