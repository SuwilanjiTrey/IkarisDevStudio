from PyQt5.QtGui import QFont, QColor, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtWidgets import QTextEdit

class CommentHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(CommentHighlighter, self).__init__(parent)

        # Define the format for highlighting comments
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#7CFC00"))  # Light green for comments
        self.comment_format.setFontItalic(True)

        # Define formats for different highlights
        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor('#FC0261'))  # Purple for return types

        self.brace_content_format = QTextCharFormat()
        self.brace_content_format.setForeground(QColor('lightblue'))  # Light blue for brace content

        self.inheritance_format = QTextCharFormat()
        self.inheritance_format.setForeground(QColor("#FFD700"))  # Gold for class inheritance

        self.parameter_format = QTextCharFormat()
        self.parameter_format.setForeground(QColor("lightblue"))  # Light blue for function parameters

        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#FF8C00"))  # Orange for keywords
        self.keyword_format.setFontWeight(QFont.Bold)

        self.other_format = QTextCharFormat()
        self.other_format.setForeground(QColor("#91FE00"))  # Light green
        self.other_format.setFontWeight(QFont.Bold)

        # Define the format for @... in XML
        self.xml_at_format = QTextCharFormat()
        self.xml_at_format.setForeground(QColor("#FFA500"))  # Orange

        # Format for color codes
        self.color_box_format = QTextCharFormat()

        # Regular expressions
        self.kotlin_keywords = [
            r'\bval\b', r'\bvar\b', r'\bfun\b', r'\bclass\b', r'\bif\b', r'\belse\b',
            r'\bwhen\b', r'\bfor\b', r'\bwhile\b', r'\bbreak\b', r'\bcontinue\b',
            r'\breturn\b', r'\bobject\b', r'\bnull\b', r'\btrue\b', r'\bfalse\b', r'\bimport\b', r'\bsuper\b',
            r'\bimplementation\b', r'\btestImplementation\b', r'\bandroidTestImplementation\b'
        ]

        self.custom_keywords = [
            r'\boverride\b', r'\bprivate\b', r'\bpublic\b', r'\bpackage\b', r'\bandroid\b', r'\bandroidx\b', r'\bandroidmini\b',
            r'\bMainActivity\b', r'\bcom\b', r'\bgoogle\b', r'\bAndroid\b', r'\bandroidApplication\b', r'\bjetbrainsKotlinAndroid\b',
            r'\bR.id\b'
        ]

        self.buildfile_keywords = [
            r'\bJavaVersion\b', r'\bcore\b', r'\bktx\b', r'\bappcompat\b', r'\bmaterial\b', r'\blibs\b',
            r'\bconstraintlayout\b', r'\blifecycle\b', r'\bnavigation\b', r'\bjunit\b'
        ]

        self.buildfile_important_words = [
            r'\bplugins\b', r'\bbuildTypes\b', r'\bcompileOptions\b', r'\bkotlinOptions\b', r'\bbuildFeatures\b', r'\bdependencies\b'
        ]

        # Regex for inheritance patterns (e.g., ": AppCompatActivity()")
        self.kotlin_inheritance_pattern = QRegularExpression(r'class\s+\w+\s*:\s*(\w+\s*\(.*?\))')

        # Regex for parameters with types (e.g., "(savedInstanceState: Bundle?)")
        self.kotlin_parameter_pattern = QRegularExpression(r'\(\s*(\w+\s*:\s*\w+\??)\s*\)')

        # Regex for function return types (e.g., "fun foo(): Int")
        self.kotlin_function_pattern = QRegularExpression(r'fun\s+\w+\s*\(.*?\)\s*:\s*(\w+)\s*\{')

        # Regex for content within curly braces
        self.curly_brace_pattern = QRegularExpression(r'\{([^{}]*)\}')

        # Regex for XML comments (e.g., <!-- comment -->)
        self.xml_comment_pattern = QRegularExpression(r'<!--.*?-->')

        # Regex for @... patterns in XML (e.g., @layout/something)
        self.xml_at_pattern = QRegularExpression(r'@[\w+]+/[^\s>]+')

        # Regex for XML color tags (e.g., <color name="...">#RRGGBB</color>)        
        self.xml_color_tag_pattern = QRegularExpression(r'<color\s+name="[^"]+">\s*(#[0-9a-fA-F]{6,8})\s*</color>')

    def highlightBlock(self, text):
        # Highlight single-line comments
        comment_match = QRegularExpression(r"//.*").globalMatch(text)
        while comment_match.hasNext():
            match = comment_match.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.comment_format)

        # Highlight inheritance (e.g., AppCompatActivity())
        inheritance_match = self.kotlin_inheritance_pattern.globalMatch(text)
        while inheritance_match.hasNext():
            match = inheritance_match.next()
            self.setFormat(match.capturedStart(1), match.capturedLength(1), self.inheritance_format)

        # Highlight function parameters (e.g., savedInstanceState: Bundle?)
        parameter_match = self.kotlin_parameter_pattern.globalMatch(text)
        while parameter_match.hasNext():
            match = parameter_match.next()
            self.setFormat(match.capturedStart(1), match.capturedLength(1), self.parameter_format)

        # Highlight function return types (after ":")
        function_match = self.kotlin_function_pattern.match(text)
        if function_match.hasMatch():
            start_index = function_match.capturedStart(1)  # Capture return type
            end_index = function_match.capturedEnd(1)
            self.setFormat(start_index, end_index - start_index, self.function_format)

        # Highlight content within curly braces
        curly_match = self.curly_brace_pattern.globalMatch(text)
        while curly_match.hasNext():
            match = curly_match.next()
            self.setFormat(match.capturedStart(1), match.capturedLength(1), self.brace_content_format)

        # Apply Kotlin keywords
        for keyword in self.kotlin_keywords:
            keyword_pattern = QRegularExpression(keyword)
            keyword_match = keyword_pattern.globalMatch(text)
            while keyword_match.hasNext():
                match = keyword_match.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.keyword_format)

        # Apply Kotlin custom keywords
        for keyword in self.custom_keywords:
            keyword_pattern = QRegularExpression(keyword)
            keyword_match = keyword_pattern.globalMatch(text)
            while keyword_match.hasNext():
                match = keyword_match.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.function_format)

        # Apply Gradle custom keywords
        for keyword in self.buildfile_keywords:
            keyword_pattern = QRegularExpression(keyword)
            keyword_match = keyword_pattern.globalMatch(text)
            while keyword_match.hasNext():
                match = keyword_match.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.brace_content_format)

        # Apply Gradle important keywords
        for keyword in self.buildfile_important_words:
            keyword_pattern = QRegularExpression(keyword)
            keyword_match = keyword_pattern.globalMatch(text)
            while keyword_match.hasNext():
                match = keyword_match.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.other_format)

        # Highlight XML comments
        xml_comment_match = self.xml_comment_pattern.globalMatch(text)
        while xml_comment_match.hasNext():
            match = xml_comment_match.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.comment_format)

        # Highlight @... patterns in XML
        xml_at_match = self.xml_at_pattern.globalMatch(text)
        while xml_at_match.hasNext():
            match = xml_at_match.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.xml_at_format)

        # Highlight XML color tags and add color boxes
        color_tag_match = self.xml_color_tag_pattern.globalMatch(text)
        while color_tag_match.hasNext():
            match = color_tag_match.next()
            color_code = match.captured(1)  # Capture the color code (e.g., #FF0000)
            self.setFormat(match.capturedStart(), match.capturedLength(), self.brace_content_format)

            # Create a small colored box at the end of the color code
            self.add_color_box(match.capturedStart(1), color_code)

    def add_color_box(self, start, color_code):
        """
        Adds a small colored box next to the color code.
        """
        self.color_box_format.setForeground(QColor(color_code))
        self.setFormat(start, 9, self.color_box_format)  # Assuming color codes are 7 characters long (e.g., #RRGGBB)
