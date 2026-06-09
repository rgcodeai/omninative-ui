# examples/demo.py
import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication, QMessageBox, QInputDialog, 
    QFileDialog, QColorDialog, QFontDialog, QGridLayout, QWidget
)
from omninative_ui import (
    OWindow, OGroup, OLabel, OButton, 
    OComboBox, OCheckBox, OLineEdit, OTextBox, OSpinBox, OScrollArea, 
    OVirtualTable, OStatusBar, OSlider, OTabs, OSeparator, ORadioButton,
    OTreeWidget, QTreeWidgetItem, OOptionRow, OAudioPlayer, OProgressBar, OFileItem,
    OImageViewer, OChatView, OChatInput, OActionMenu
)

def main():
    app = QApplication(sys.argv)
    
    window = OWindow(title="OmniNative UI Components Demo", width=500, height=800, resizable=True)
    
    scroll = OScrollArea(window.body)
    scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
    window.body.layout().addWidget(scroll)
    
    main_group = OGroup(scroll)
    scroll.setWidget(main_group)
    scroll.setWidgetResizable(True)
    
    main_group.layout_.setSpacing(10)
    main_group.layout_.setContentsMargins(20, 10, 20, 10)
    
    # -----------------------------------------------------------------------
    # OTabs
    # -----------------------------------------------------------------------
    tree_tabs = OTreeWidget(main_group, text="OTabs", expanded=False)
    tabs = OTabs(tree_tabs.content)
    tab1 = tabs.add("Pestaña 1")
    tab1.layout().addWidget(OLabel(tab1, text="Contenido de la primera pestaña"))
    tab1.layout().addStretch()
    
    tab2 = tabs.add("Pestaña 2")
    tab2.layout().addWidget(OLabel(tab2, text="Contenido de la segunda pestaña"))
    tab2.layout().addWidget(OButton(tab2, text="Botón en Tab 2"))
    tab2.layout().addStretch()
    
    tree_tabs.add_widget(tabs)
    main_group.layout_.addWidget(tree_tabs)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OLabel
    # -----------------------------------------------------------------------
    tree_labels = OTreeWidget(main_group, text="OLabel", expanded=False)
    label_group = OGroup(tree_labels.content, orientation="h")
    label_group.layout_.addWidget(OLabel(label_group, text="Standard Label"))
    label_group.layout_.addWidget(OLabel(label_group, text="Bold Label", bold=True))
    label_group.layout_.addWidget(OLabel(label_group, text="Bright Label", bright=True))
    tree_labels.add_widget(label_group)
    main_group.layout_.addWidget(tree_labels)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OSeparator
    # -----------------------------------------------------------------------
    tree_sep = OTreeWidget(main_group, text="OSeparator", expanded=False)
    tree_sep.add_widget(OSeparator(tree_sep.content))
    main_group.layout_.addWidget(tree_sep)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OButton
    # -----------------------------------------------------------------------
    tree_btns = OTreeWidget(main_group, text="OButton", expanded=False)
    btn_group = OGroup(tree_btns.content, orientation="h")
    btn_group.layout_.addWidget(OButton(btn_group, text="Primary", primary=True))
    btn_group.layout_.addWidget(OButton(btn_group, text="Standard"))
    btn_group.layout_.addWidget(OButton(btn_group, text="Danger", danger=True))
    tree_btns.add_widget(btn_group)
    main_group.layout_.addWidget(tree_btns)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OLineEdit
    # -----------------------------------------------------------------------
    tree_lineedit = OTreeWidget(main_group, text="OLineEdit", expanded=False)
    tree_lineedit.add_widget(OLineEdit(tree_lineedit.content, placeholder="Line Edit... Type something..."))
    tree_lineedit.add_widget(OLineEdit(tree_lineedit.content, placeholder="Password...", password=True))
    ro_edit = OLineEdit(tree_lineedit.content, read_only=True)
    ro_edit.set("Contenido de solo lectura")
    tree_lineedit.add_widget(ro_edit)
    main_group.layout_.addWidget(tree_lineedit)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OTextBox
    # -----------------------------------------------------------------------
    tree_textbox = OTreeWidget(main_group, text="OTextBox", expanded=False)
    tree_textbox.add_widget(OTextBox(tree_textbox.content, height=60))
    main_group.layout_.addWidget(tree_textbox)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OSpinBox
    # -----------------------------------------------------------------------
    tree_spinbox = OTreeWidget(main_group, text="OSpinBox", expanded=False)
    tree_spinbox.add_widget(OSpinBox(tree_spinbox.content, from_=0, to=100, value=50))
    main_group.layout_.addWidget(tree_spinbox)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OSlider
    # -----------------------------------------------------------------------
    tree_slider = OTreeWidget(main_group, text="OSlider", expanded=False)
    tree_slider.add_widget(OSlider(tree_slider.content, orientation="h", from_=0, to=100, value=25))
    main_group.layout_.addWidget(tree_slider)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OProgressBar
    # -----------------------------------------------------------------------
    tree_prog = OTreeWidget(main_group, text="OProgressBar", expanded=False)
    prog_group = OGroup(tree_prog.content, orientation="v")
    
    prog_group.layout_.addWidget(OLabel(prog_group, text="Determinate (45%)"))
    prog_det = OProgressBar(prog_group)
    prog_det.set(45)
    prog_group.layout_.addWidget(prog_det)
    
    prog_group.layout_.addWidget(OLabel(prog_group, text="Indeterminate"))
    prog_indet = OProgressBar(prog_group)
    prog_indet.set_indeterminate(True)
    prog_group.layout_.addWidget(prog_indet)
    
    tree_prog.add_widget(prog_group)
    main_group.layout_.addWidget(tree_prog)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OComboBox
    # -----------------------------------------------------------------------
    tree_combo = OTreeWidget(main_group, text="OComboBox", expanded=False)
    combo = OComboBox(tree_combo.content, values=["---", "Option 1", "Option 2", "Option 3"])
    tree_combo.add_widget(combo)
    main_group.layout_.addWidget(tree_combo)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OCheckBox
    # -----------------------------------------------------------------------
    tree_checkbox = OTreeWidget(main_group, text="OCheckBox", expanded=False)
    tree_checkbox.add_widget(OCheckBox(tree_checkbox.content, text="Enable Feature"))
    main_group.layout_.addWidget(tree_checkbox)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # ORadioButton
    # -----------------------------------------------------------------------
    tree_radio = OTreeWidget(main_group, text="ORadioButton", expanded=False)
    rb_group = OGroup(tree_radio.content, orientation="v")
    
    group_left = OGroup(rb_group, orientation="v")
    rb1_1 = ORadioButton(group_left, text="Option A1 (Icon Left)", icon_position="left")
    rb1_2 = ORadioButton(group_left, text="Option A2 (Icon Left)", icon_position="left")
    rb1_1.setChecked(True)
    group_left.layout_.addWidget(rb1_1, 0, Qt.AlignRight)
    group_left.layout_.addWidget(rb1_2, 0, Qt.AlignRight)
    
    group_right = OGroup(rb_group, orientation="v")
    rb2_1 = ORadioButton(group_right, text="Option B1 (Icon Right)", icon_position="right")
    rb2_2 = ORadioButton(group_right, text="Option B2 (Icon Right)", icon_position="right")
    rb2_1.setChecked(True)
    group_right.layout_.addWidget(rb2_1, 0, Qt.AlignRight)
    group_right.layout_.addWidget(rb2_2, 0, Qt.AlignRight)
    
    rb_group.layout_.addWidget(group_left, 0, Qt.AlignRight)
    rb_group.layout_.addWidget(group_right, 0, Qt.AlignRight)
    tree_radio.add_widget(rb_group)
    main_group.layout_.addWidget(tree_radio)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OTreeWidget (Collapsible Container)
    # -----------------------------------------------------------------------
    tree_container = OTreeWidget(main_group, text="OTreeWidget (Dropdown Options)", expanded=False)
    
    row1 = OOptionRow(tree_container.content, "Select Tab", label_width=80)
    row1.layout_.addWidget(OComboBox(row1, values=["1", "2", "3", "4", "5", "6", "7", "8"]))
    tree_container.add_widget(row1)
    
    row2 = OOptionRow(tree_container.content, "Position", label_width=80)
    row2.layout_.addWidget(OSlider(row2, from_=0, to=100, value=12))
    tree_container.add_widget(row2)
    
    row3 = OOptionRow(tree_container.content, "Alignment", label_width=80)
    row3.layout_.addWidget(OSlider(row3, from_=0, to=100, value=25))
    tree_container.add_widget(row3)
    
    main_group.layout_.addWidget(tree_container)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OAudioPlayer
    # -----------------------------------------------------------------------
    tree_audio = OTreeWidget(main_group, text="OAudioPlayer", expanded=False)
    audio_player = OAudioPlayer(tree_audio.content)
    tree_audio.add_widget(audio_player)
    main_group.layout_.addWidget(tree_audio)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OImageViewer
    # -----------------------------------------------------------------------
    tree_image = OTreeWidget(main_group, text="OImageViewer", expanded=False)
    image_viewer = OImageViewer(tree_image.content)
    tree_image.add_widget(image_viewer)
    main_group.layout_.addWidget(tree_image)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OFileItem
    # -----------------------------------------------------------------------
    tree_file = OTreeWidget(main_group, text="OFileItem", expanded=False)
    file_item = OFileItem(tree_file.content, filepath="C:/example/report.pdf", filesize_str="2.4 MB")
    tree_file.add_widget(file_item)
    main_group.layout_.addWidget(tree_file)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OVirtualTable
    # -----------------------------------------------------------------------
    tree_table = OTreeWidget(main_group, text="OVirtualTable", expanded=False)
    table_columns = ("ID", "Name", "Status")
    table_widgets = [
        {"class": "QLabel", "weight": 1},
        {"class": "OTextBox", "weight": 2},
        {"class": "OComboBox", "kwargs": {"values": ["Active", "Inactive"]}, "weight": 1}
    ]
    table = OVirtualTable(tree_table.content, columns=table_columns, column_widgets=table_widgets, visible_rows=3)
    table.update_data([
        (1, "Item A", "Active"),
        (2, "Item B", "Inactive"),
        (3, "Item C", "Active"),
    ])
    tree_table.add_widget(table)
    main_group.layout_.addWidget(tree_table)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OStatusBar
    # -----------------------------------------------------------------------
    tree_status = OTreeWidget(main_group, text="OStatusBar", expanded=False)
    status = OStatusBar(tree_status.content)
    status.set("Demo loaded successfully", "success")
    tree_status.add_widget(status)
    main_group.layout_.addWidget(tree_status)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OChatView
    # -----------------------------------------------------------------------
    tree_chat = OTreeWidget(main_group, text="OChatView", expanded=False)
    chat_view = OChatView(tree_chat.content)
    chat_view.setMinimumHeight(300)
    
    # Initial messages
    chat_view.add_message("user", "Hola, necesito ayuda con un componente.")
    chat_view.add_message("assistant", "¡Claro! ¿Qué componente de **omninative_ui** estás construyendo?")
    
    # Input area
    chat_input = OChatInput()
    
    # Action Menu
    action_menu = OActionMenu()
    action_menu.add_action("Agregar fotos y archivos", "📎")
    action_menu.add_action("Archivos recientes", "📄", has_chevron=True)
    action_menu.add_separator()
    action_menu.add_action("Crea una imagen", "🖼")
    action_menu.add_action("Razonamiento", "💡")
    action_menu.add_action("Investigar a fondo", "🔭")
    action_menu.add_action("Busca en la web", "🌐")
    action_menu.add_action("Más", "⋯", has_chevron=True)
    action_menu.add_separator()
    action_menu.add_action("Proyectos", "📁", has_chevron=True)
    
    chat_input.add_clicked.connect(lambda: action_menu.show_above(chat_input.btn_add))
    
    # Simulation logic
    def simulate_chat(text):
        chat_view.add_message("user", text)
        
        # Create empty assistant message
        chat_view.add_message("assistant", "")
        
        response = "Entendido. Aquí tienes una demostración de *streaming* en tiempo real utilizando el método `append_chunk` en tu nuevo componente OChatView. ¡Espero que te sea muy útil!"
        words = response.split(" ")
        
        def stream_next_word(idx=0):
            if idx < len(words):
                chat_view.append_chunk(words[idx] + " ")
                QTimer.singleShot(100, lambda: stream_next_word(idx + 1))
                
        QTimer.singleShot(500, stream_next_word)
    
    chat_input.submitted.connect(simulate_chat)
    action_menu.action_triggered.connect(lambda text: simulate_chat(f"*[Acción Seleccionada]: {text}*"))
    
    tree_chat.add_widget(chat_view)
    main_group.layout_.addWidget(tree_chat)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    tree_input = OTreeWidget(main_group, text="OChatInput", expanded=False)
    tree_input.add_widget(chat_input)
    main_group.layout_.addWidget(tree_input)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # OActionMenu (Vista estática)
    # -----------------------------------------------------------------------
    tree_action_menu = OTreeWidget(main_group, text="OActionMenu", expanded=False)
    
    from omninative_ui import OActionMenuItem, OMNINATIVE
    from PySide6.QtWidgets import QFrame, QVBoxLayout
    
    # Contenedor que simula visualmente la ventana flotante
    menu_window = QFrame()
    menu_window.setObjectName("menu_container_demo")
    menu_window.setStyleSheet(f"#menu_container_demo {{ background-color: #2F2F2F; border-radius: 12px; border: 1px solid #3F3F3F; }}")
    menu_window.setFixedWidth(280)
    
    menu_layout = QVBoxLayout(menu_window)
    menu_layout.setContentsMargins(6, 6, 6, 6)
    menu_layout.setSpacing(2)
    
    menu_layout.addWidget(OActionMenuItem("Agregar fotos y archivos", "📎"))
    menu_layout.addWidget(OActionMenuItem("Archivos recientes", "📄", has_chevron=True))
    
    # Separador
    sep = QFrame()
    sep.setFixedHeight(1)
    sep.setStyleSheet(f"background-color: {OMNINATIVE['dark']}; margin: 4px 10px;")
    menu_layout.addWidget(sep)
    
    menu_layout.addWidget(OActionMenuItem("Crea una imagen", "🖼"))
    menu_layout.addWidget(OActionMenuItem("Razonamiento", "💡"))
    menu_layout.addWidget(OActionMenuItem("Más", "⋯", has_chevron=True))
    
    tree_action_menu.add_widget(menu_window)
    main_group.layout_.addWidget(tree_action_menu)
    main_group.layout_.addWidget(OSeparator(main_group))
    
    # -----------------------------------------------------------------------
    # Native Dialogs
    # -----------------------------------------------------------------------
    tree_dialogs = OTreeWidget(main_group, text="Native Dialogs", expanded=False)
    
    dialog_desc = OLabel(tree_dialogs.content, text="Hacé click en los botones para abrir cada diálogo:", bold=True)
    tree_dialogs.add_widget(dialog_desc)
    
    dialog_grid_widget = QWidget()
    dialog_grid = QGridLayout(dialog_grid_widget)
    dialog_grid.setContentsMargins(0, 5, 0, 0)
    dialog_grid.setSpacing(10)
    
    # Dialog functions
    def show_info(): QMessageBox.information(None, "Info", "Mensaje de información")
    def show_warning(): QMessageBox.warning(None, "Warning", "Mensaje de advertencia")
    def show_question(): QMessageBox.question(None, "Question", "¿Estás seguro?")
    def show_critical(): QMessageBox.critical(None, "Critical", "Error crítico")
    def show_get_text(): QInputDialog.getText(None, "Input", "Ingresa un texto:")
    def show_get_int(): QInputDialog.getInt(None, "Input", "Ingresa un número:")
    def show_open_file(): QFileDialog.getOpenFileName(None, "Abrir archivo")
    def show_save_file(): QFileDialog.getSaveFileName(None, "Guardar archivo")
    def show_color(): QColorDialog.getColor(Qt.white, None, "Selecciona un color")
    def show_font(): QFontDialog.getFont(None)
    
    btn_info = OButton(dialog_grid_widget, text="QMessageBox.information", command=show_info)
    btn_warn = OButton(dialog_grid_widget, text="QMessageBox.warning", command=show_warning)
    btn_quest = OButton(dialog_grid_widget, text="QMessageBox.question", command=show_question)
    btn_crit = OButton(dialog_grid_widget, text="QMessageBox.critical", command=show_critical)
    btn_text = OButton(dialog_grid_widget, text="QInputDialog.getText", command=show_get_text)
    btn_int = OButton(dialog_grid_widget, text="QInputDialog.getInt", command=show_get_int)
    btn_open = OButton(dialog_grid_widget, text="QFileDialog.getOpenFileName", command=show_open_file)
    btn_save = OButton(dialog_grid_widget, text="QFileDialog.getSaveFileName", command=show_save_file)
    btn_color = OButton(dialog_grid_widget, text="QColorDialog.getColor", command=show_color)
    btn_font = OButton(dialog_grid_widget, text="QFontDialog.getFont", command=show_font)
    
    dialog_grid.addWidget(btn_info, 0, 0)
    dialog_grid.addWidget(btn_warn, 0, 1)
    dialog_grid.addWidget(btn_quest, 1, 0)
    dialog_grid.addWidget(btn_crit, 1, 1)
    dialog_grid.addWidget(btn_text, 2, 0)
    dialog_grid.addWidget(btn_int, 2, 1)
    dialog_grid.addWidget(btn_open, 3, 0)
    dialog_grid.addWidget(btn_save, 3, 1)
    dialog_grid.addWidget(btn_color, 4, 0)
    dialog_grid.addWidget(btn_font, 4, 1)
    
    tree_dialogs.add_widget(dialog_grid_widget)
    main_group.layout_.addWidget(tree_dialogs)
    
    main_group.layout_.addStretch()
    
    window.omninativeui_reveal_when_ready()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
