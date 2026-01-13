# File Organizer

A simple and efficient desktop application built with PyQt6 to automatically organize your files by extension into categorized folders.

## 📋 Features

- **Automatic File Organization**: Organize files by their extensions into predefined categories
- **User-Friendly GUI**: Modern and intuitive interface built with PyQt6
- **Real-Time Progress Tracking**: See live updates as files are being organized with a progress bar.
- **Thread-Safe Operations**: File organization runs in a separate thread to keep the UI responsive
- **Multiple File Categories**: Support for Images, Documents, Videos, Audio, Programs, Compressed files, and more
- **Folder Selection**: Easy folder browsing and selection dialog
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Windows Context Menu Integration**: Right-click on any folder in Windows Explorer to organize it directly.

## 🎯 Supported File Categories

The application automatically organizes files into the following categories:

- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`
- **Documents**: `.pdf`, `.docx`, `.doc`, `.txt`, `.xlsx`, `.xls`, `.pptx`, `.ppt`
- **Videos**: `.mp4`, `.mkv`, `.avi`, `.mov`, `.flv`
- **Audio**: `.mp3`, `.wav`, `.aac`
- **Programs**: `.exe`, `.msi`
- **Compressed**: `.zip`, `.rar`, `.7z`
- **Others**: All other file types are moved to an "Others" folder

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Steps

1. Clone the repository or download the source code:
   ```bash
   git clone https://github.com/eaf-microservice/files_organization.git
   cd files_organization
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### From the Application

1. Run the application:
   ```bash
   python main.py
   ```

2. Click the **"Browse Folder"** button to select the folder you want to organize

3. Once a folder is selected, click the **"Organize Files"** button to start the organization process

4. Watch the progress in the status log and the progress bar as files are moved to their respective categories

5. A success message will appear when the organization is complete

### From Windows Explorer Context Menu

1.  After installing the application using the installer (which registers the context menu item), right-click on any folder in Windows Explorer.
2.  Select the **"Organiser avec l'application"** option from the context menu.
3.  The File Organizer application will launch and automatically start organizing the selected folder.

## 📁 Project Structure

```
organisateur/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── assets/             # Application assets (icons, etc.)
└── venv/               # Virtual environment (not included in git)
```

## 🛠️ Requirements

The main dependencies are:

- **PyQt6** (6.10.2): GUI framework
- **PyQt6-Qt6** (6.10.1): Qt6 bindings
- **PyQt6_sip** (13.10.3): SIP bindings for PyQt6

For building executables:
- **PyInstaller** (6.17.0): Package the application into an executable

See `requirements.txt` for the complete list of dependencies.

## 📝 How It Works

1. The application scans the selected folder for all files
2. For each file, it checks the file extension
3. Files are moved to the appropriate category folder based on their extension
4. If a file doesn't match any known category, it's moved to the "Others" folder
5. Category folders are created automatically if they don't exist

## ⚠️ Important Notes

- **Backup Important Files**: Always backup your files before organizing, especially if working with important data
- **Folder Selection**: Make sure you have write permissions for the selected folder
- **File Movement**: Files are moved (not copied), so they will be removed from the original location
- **Existing Folders**: The application will create category folders if they don't exist, but won't overwrite existing folders

## 🐛 Troubleshooting

### Application won't start
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.7 or higher: `python --version`

### Files not organizing
- Check that you have write permissions for the selected folder
- Ensure the folder path is valid and accessible
- Check the status log for error messages

### Icon not displaying
- Make sure `assets/icon.png` exists in the project directory
- If the icon file is missing, the application will still work but without an icon

## 👨‍💻 Author

**Fouad El Azbi**

- **Company**: EAF microservices
- **Email**: EAF.microservice@gmail.com

## 📄 Version

**Current Version**: 1.0.0

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

© 2026 EAF microservices - File Organizer

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 🙏 Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Python standard library modules: `os`, `shutil`

---

**Note**: This application is designed to help organize files efficiently. Always ensure you have backups of important data before running file organization operations.

