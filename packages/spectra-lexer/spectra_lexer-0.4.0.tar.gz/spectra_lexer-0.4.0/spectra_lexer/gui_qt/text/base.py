from functools import partial

from PyQt5.QtWidgets import QLineEdit, QWidget

from spectra_lexer import on, pipe, SpectraComponent
from spectra_lexer.gui_qt.text.text_graph_widget import TextGraphWidget
from spectra_lexer.rules import StenoRule


class GUIQtTextDisplay(SpectraComponent):
    """ GUI operations class for displaying rules and finding the mouse position over the text graph.
        Also displays engine output such as status messages and exceptions. """

    w_title: QLineEdit         # Displays status messages and mapping of keys to word.
    w_text: TextGraphWidget    # Displays formatted text breakdown graph.

    def __init__(self, *widgets:QWidget):
        super().__init__()
        self.w_title, self.w_text = widgets

    @on("configure")
    def signal_connect(self, **cfg_dict) -> None:
        """ Register the mouseover signal. Keyboard input may also be available from this widget in the future. """
        self.w_text.mouseOverCharacter.connect(partial(self.engine_call, "sig_process_mouseover"))

    @on("new_status")
    def display_status(self, msg:str) -> None:
        """ Display engine status messages in the title bar. """
        self.w_title.setText(msg)

    @on("new_lexer_result")
    def display_title(self, rule:StenoRule) -> None:
        """ For a new lexer result, set the title from the rule. """
        self.w_title.setText(str(rule))

    @on("new_output_graph")
    def display_new_graph(self, text:str, **kwargs) -> None:
        """ Display a finished interactive HTML text graph in the main text widget. """
        self.w_text.set_text_display(text, html=True, interactive=True, **kwargs)

    @on("new_output_text")
    def display_new_text(self, text:str, **kwargs) -> None:
        """ Display non-interactive plaintext in the main text widget. """
        self.w_text.set_text_display(text, html=False, interactive=False,  **kwargs)

    @pipe("sig_process_mouseover", "output_format_node_at", unpack=True)
    def process_mouseover(self, row:int, col:int) -> tuple:
        """ Pass a mouseover event to the cascaded text formatter. """
        return row, col
