# File Manager

A simple Python utility that automatically organizes files in a watched directory by moving them into category-based subdirectories according to their file extensions.

## Features

- Monitors a specified directory for new files
- Automatically categorizes files based on their extensions
- Moves files to appropriate category folders
- Handles filename conflicts by creating unique filenames
- Preserves file permissions
- Minimal dependencies

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/file-manager.git
   cd file-manager
   ```

2. Install the required dependencies:
   ```
   pip install watchdog
   ```

## Usage

### Basic Usage

Run the script to monitor your Downloads folder (default):

```
python file_manager.py
```

### Custom Directory

Specify a custom directory to monitor:

```
python file_manager.py /path/to/your/directory
```

### Customizing Categories

You can modify the `EXTENSION_MAPPINGS` dictionary in the script to customize the categories and file extensions.

### Changing the Watched Directory

The script monitors your Downloads folder by default:

```python
WATCH_DIRECTORY = os.path.expanduser("~/Downloads")
```

To change the watched directory, you can edit the `WATCH_DIRECTORY` variable in the script directly

## How It Works

The script creates the following category folders in the watched directory:

- PDF
- Images
- Video
- Audio
- Documents
- Zip
- Ebook
- Installers
- Others (for files with extensions not matching any category)

When a new file is detected in the watched directory, the script:

1. Determines the appropriate category based on the file extension
2. Creates the category folder if it doesn't exist
3. Moves the file to the category folder
4. Handles filename conflicts by appending a number to the filename

## Requirements

- Python 3.6+
- watchdog library

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! If you'd like to contribute to this project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Create a new Pull Request

Please ensure your code follows the existing style and includes appropriate documentation.

## Disclaimer

This software is provided "as is" without warranty of any kind, either express or implied. The author and contributors are not responsible for any damages, data loss, or consequences that may arise from using this PDF manipulation tool. Users should:

- Verify the output files after using the tool.
- Exercise caution when handling sensitive or important documents.
- Use the tool responsibly and at your own risk.

By using File Manager, you acknowledge and accept these risks and limitations.

## Author

[Romain Mendez](https://github.com/romaindez)
