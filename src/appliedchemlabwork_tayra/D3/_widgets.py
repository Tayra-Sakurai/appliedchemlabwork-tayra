from PyQt6.QtWidgets import QWidget, QMainWindow, QGraphicsView, QVBoxLayout, QFileDialog, QLineEdit, QLabel, QGroupBox, QFormLayout, QPushButton, QGraphicsScene
from PyQt6.QtCore import QStandardPaths, Qt
from PyQt6.QtGui import QImage


class SuperWindow(QMainWindow):
    """The main window of the GUI tools.

    Parameters
    ----------
    parent : QWidget | None
        The parent widget.
    flags : WindowType | None
        The flags.

    Attributes
    ----------
    file_source : QLineEdit
        The text box for the file path to the source image.
    result_location : str | None
        The result output location.
    pick_source_btn : QPushButton
        The file picking button to open the source image.
    start_btn : QPushButton
        The button to start detection process.
    img : QImage
        The image on the window.

    Methods
    -------
    __init__(parent=None,flags=...)
        Initializes the class.
    createWindowContents()
        Creates the window main contents.
    pick_file()
        Picks the file.
    """
    file_source: QLineEdit
    result_location: str | None
    pick_source_btn: QPushButton
    start_btn: QPushButton
    img: QImage

    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Window
    ):
        """Initializes the window with the parts.

        Parameters
        ----------
        parent : QWidget, optional
            The parent widget.
        flags : WindowType, optional
            The ``WindowType`` of the window.

        Notes
        -----
        This method must be called
        after ``QApplication`` object was initilized.

        Examples
        --------
        in this example, the application was launched from ``QApplication``.
        >>> from PyQt6.QtWidget import QApplication
        >>> from appliedchemlabwork_tayra.D3 import SuperWindow
        >>> import sys
        >>> app = QApplication(argv=sys.argv)
        >>> app
        QApplication
        >>> m_window = SuperWindow()
        >>> sys.exit(app.exec())
        """
        super().__init__(parent, flags)
        self.createWindowContents()

    def createWindowContents(self):
        """Creates the window's main contents.

        Extended Summary
        ----------------
        This method defines the window's ``CentralWidget`` contents.
        """
        cWidget = self.centralWidget()
        if cWidget is None:
            cWidget = QWidget()
            self.setCentralWidget(cWidget)
        mainLayout = QVBoxLayout(cWidget)
        group1 = QGroupBox('Settings', cWidget)
        g1Layout = QFormLayout(group1)
        self.file_source = QLineEdit(group1)
        file_source_label = QLabel('Source file', group1)
        g1Layout.addRow(file_source_label, self.file_source)
        file_pick_label = QLabel('Or', group1)
        self.pick_source_btn = QPushButton('Select file in place', group1)
        self.pick_source_btn.clicked.connect(self.pick_file)
        g1Layout.addRow(file_pick_label, self.pick_source_btn)
        mainLayout.addWidget(group1)
        cWidget.setLayout(mainLayout)

    def pick_file(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            'Please pick the source file.',
            QStandardPaths.displayName(
                QStandardPaths.StandardLocation.PicturesLocation
            ),
            'Image files (*.avif *.bmp *.dng *.heic *.heif *.jp2 *.jpeg2000 *.jpg *.mpo *.png *.tif *.tiff *.webp);;Video files (*.asf *.avi *.gif *.m4v *.mkv *.mov *.mp4 *.mpeg *.mpg *.ts *.wmv *.webm)'
        )
        self.file_source.setText(filePath)
