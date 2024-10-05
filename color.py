from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QSyntaxHighlighter, QPainter, QTextFormat
from PyQt5.QtCore import QRegularExpression


class ColorCoat(QSyntaxHighlighter):
    def __init__(self, parent=None, filename=None):
        super(ColorCoat, self).__init__(parent)
        
        self.filename = filename  # Store the filename to be checked later

        # Define the format for highlighting comments (same as in your existing code)
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#7CFC00"))
        self.comment_format.setFontItalic(True)

        # Define the color format
        self.color_format = QTextCharFormat()

        # Regular expression for hex color values in colors.xml (e.g., #FFFFFF)
        self.color_pattern = QRegularExpression(r'#(?:[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})\b')  # 6 or 8-character hex code
        
        # Regular expression for <color> tags in colors.xml
        self.color_tag_pattern = QRegularExpression(r'<color\s+name="[^"]+">([^<]+)</color>')

    def highlightBlock(self, text):
        # Apply the highlighting logic if the file is colors.xml
        if self.filename == "colors.xml":
            # Match color tag
            color_tag_match = self.color_tag_pattern.globalMatch(text)
            while color_tag_match.hasNext():
                match = color_tag_match.next()
                color_code = match.captured(1)  # Get the color value (e.g., #FFFFFF)
                self.setFormat(match.capturedStart(1), match.capturedLength(1), self.color_format)

                # Call the method to add a color box if it's a valid color code
                color = QColor(color_code)
                if color.isValid():
                    self.add_color_box(color, match.capturedStart(1), match.capturedLength(1), text)
        else:
            # Regular highlighting logic for other files (existing code)...
            super().highlightBlock(text)

    def add_color_box(self, color, start, length, text):
        """Adds a colored box at the end of the line for color values."""
        block = self.currentBlock()
        layout = block.layout()

        # Get the bounding rect of the text layout
        rect = layout.boundingRect()

        # Set up the painter and color
        painter = QPainter(self.parent())
        painter.setBrush(QColor(color))  # Set the brush color to the color code
        box_size = 10  # Set the size of the box
        box_x = rect.right() + 5  # Place it at the end of the text (with padding)
        box_y = rect.top() + (rect.height() - box_size) / 2  # Center it vertically
        painter.drawRect(box_x, box_y, box_size, box_size)  # Draw the box
        painter.end()

# Now you can use it like this
#editor = QTextEdit()  # Your text edit widget
#highlighter = ColorCoat(editor.document(), filename="colors.xml")
