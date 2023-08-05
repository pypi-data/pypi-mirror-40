import os
import tkinter as tk
from tkinter.font import Font
import xml.etree.ElementTree as ET


class HelpWindow(tk.Frame):

    def __init__(self, master:tk.Frame):
        super().__init__(master)
        self.master = master
        self.text = None
        self.config_help()
        self.write_text()

    def config_help(self):
        self.text = tk.Text(self.master, background="#FFFFFF", state=tk.DISABLED, wrap=tk.WORD,
                            padx = 20)

        scrollbar = tk.Scrollbar(self.master, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text['yscrollcommand'] = scrollbar.set

        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        headline_1_tag = Font(size=20, weight="bold")
        headline_2_tag = Font(size=16, weight="bold")
        headline_3_tag = Font(size=12, weight="bold")
        text_tag = Font(size=10)
        bold_tag = Font(size=10, weight="bold")
        code_tag = Font(family="Courier", size=10)

        self.text.tag_configure("HEADLINE_1", font=headline_1_tag)
        self.text.tag_configure("HEADLINE_2", font=headline_2_tag)
        self.text.tag_configure("HEADLINE_3", font=headline_3_tag)
        self.text.tag_configure("TEXT", font=text_tag)
        self.text.tag_configure("BOLD", font=bold_tag)
        self.text.tag_configure("CODE", font=code_tag)

    def write_text(self):
        self.text.config(state=tk.NORMAL)
        package_directory = os.path.dirname(os.path.abspath(__file__))
        with open (os.path.join(package_directory, 'files/help.xml'), 'r') as f:
            file_content = f.read()
            root = ET.fromstring(file_content)
            self.process_element(root)
        self.text.config(state=tk.DISABLED)

    def process_element(self, element: ET.Element):
        if element.tag == "Article":
            for subelement in element:
                self.process_element(subelement)
            self.text.insert(tk.END, "\n", "TEXT")
        elif element.tag == "Section":
            self.text.insert(tk.END, "\n", "TEXT")
            for subelement in element:
                self.process_element(subelement)
        elif element.tag == "Headline1":
            self.text.insert(tk.END, element.text + "\n", "HEADLINE_1")
        elif element.tag == "Headline2":
            self.text.insert(tk.END, "\n", "TEXT")
            self.text.insert(tk.END, element.text + "\n", "HEADLINE_2")
        elif element.tag == "Headline3":
            self.text.insert(tk.END, element.text + "\n", "HEADLINE_3")
        elif element.tag == "Bold":
            self.text.insert(tk.END, element.text + "\n", "BOLD")
        elif element.tag == "Text":
            self.text.insert(tk.END, element.text + "\n", "TEXT")
        elif element.tag == "Code":
            self.text.insert(tk.END, element.text + "\n", "CODE")

