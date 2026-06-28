# examples/demo.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QStackedWidget
from omninative_ui import (
    OWindow, OGroup, OLabel, OButton, 
    OComboBox, OCheckBox, OLineEdit, OTextBox, OSpinBox, OScrollArea, 
    OVirtualTable, OSlider, OTabs, OSeparator, ORadioButton,
    OTreeWidget, OAudioPlayer, OProgressBar, OFileItem,
    OImageViewer, OChatView, OChatInput, OActionMenu, OAudioRecorderOverlay, OHotkeyInput,
    OInfoIcon, OSidebar
)

def create_page(parent_stack):
    scroll = OScrollArea(parent_stack)
    scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
    main_group = OGroup(scroll)
    scroll.setWidget(main_group)
    scroll.setWidgetResizable(True)
    main_group.layout_.setSpacing(10)
    main_group.layout_.setContentsMargins(30, 20, 30, 20)
    main_group.layout_.setAlignment(Qt.AlignTop)
    return scroll, main_group


def build_layouts_page(stack):
    scroll, page = create_page(stack)
    
    # OGroup
    page.layout_.addWidget(OLabel(page, text="OGroup", bright=True, bold=True, size=14))
    page.layout_.addWidget(OLabel(page, text="50% / 50% Split"))
    r_50 = OGroup(page, orientation="h")
    c_50_1 = OGroup(r_50, width="50%", panel=True, pad=10)
    c_50_1.layout_.addWidget(OLabel(c_50_1, text="50%"))
    c_50_2 = OGroup(r_50, width="50%", panel=True, pad=10)
    c_50_2.layout_.addWidget(OLabel(c_50_2, text="50%"))
    r_50.layout_.addWidget(c_50_1)
    r_50.layout_.addWidget(c_50_2)
    page.layout_.addWidget(r_50)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    page.layout_.addWidget(OLabel(page, text="70% / 30% Split"))
    r_70 = OGroup(page, orientation="h")
    c_70_1 = OGroup(r_70, width="70%", panel=True, pad=10)
    c_70_1.layout_.addWidget(OLabel(c_70_1, text="70%"))
    c_70_2 = OGroup(r_70, width="30%", panel=True, pad=10)
    c_70_2.layout_.addWidget(OLabel(c_70_2, text="30%"))
    r_70.layout_.addWidget(c_70_1)
    r_70.layout_.addWidget(c_70_2)
    page.layout_.addWidget(r_70)

    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    page.layout_.addWidget(OLabel(page, text="33% / 33% / 33% Split"))
    r_33 = OGroup(page, orientation="h")
    c_33_1 = OGroup(r_33, width="33%", panel=True, pad=10)
    c_33_1.layout_.addWidget(OLabel(c_33_1, text="33%"))
    c_33_2 = OGroup(r_33, width="33%", panel=True, pad=10)
    c_33_2.layout_.addWidget(OLabel(c_33_2, text="33%"))
    c_33_3 = OGroup(r_33, width="33%", panel=True, pad=10)
    c_33_3.layout_.addWidget(OLabel(c_33_3, text="33%"))
    r_33.layout_.addWidget(c_33_1)
    r_33.layout_.addWidget(c_33_2)
    r_33.layout_.addWidget(c_33_3)
    page.layout_.addWidget(r_33)

    page.layout_.addWidget(OSeparator(page, pad_y=10))

    page.layout_.addWidget(OLabel(page, text="25% / 25% / 25% / 25% Split"))
    r_25 = OGroup(page, orientation="h")
    for i in range(4):
        c_25 = OGroup(r_25, width="25%", panel=True, pad=10)
        c_25.layout_.addWidget(OLabel(c_25, text="25%"))
        r_25.layout_.addWidget(c_25)
    page.layout_.addWidget(r_25)

    page.layout_.addWidget(OSeparator(page, pad_y=10))

    page.layout_.addWidget(OLabel(page, text="Fixed Width (200px) + Auto (Flex-grow)"))
    r_mix = OGroup(page, orientation="h")
    c_fixed = OGroup(r_mix, width=200, panel=True, pad=10)
    c_fixed.layout_.addWidget(OLabel(c_fixed, text="Fixed 200px"))
    c_auto = OGroup(r_mix, panel=True, pad=10)
    c_auto.layout_.addWidget(OLabel(c_auto, text="Auto (Flex-grow)"))
    r_mix.layout_.addWidget(c_fixed)
    r_mix.layout_.addWidget(c_auto, 1) # flex-grow=1
    page.layout_.addWidget(r_mix)

    page.layout_.addWidget(OSeparator(page, pad_y=10))

    page.layout_.addWidget(OLabel(page, text="Nested Groups (50% containing two 50%)"))
    r_nested = OGroup(page, orientation="h")
    c_n1 = OGroup(r_nested, width="50%", panel=True, pad=10)
    c_n1.layout_.addWidget(OLabel(c_n1, text="Outer 50% (Left)"))
    
    c_n2 = OGroup(r_nested, width="50%", panel=True, pad=10)
    c_n2.layout_.addWidget(OLabel(c_n2, text="Outer 50% (Right)"))
    
    r_inner = OGroup(c_n2, orientation="h")
    c_in1 = OGroup(r_inner, width="50%", panel=True, pad=10, bg_color="#1E1E1E")
    c_in1.layout_.addWidget(OLabel(c_in1, text="Inner 50%"))
    c_in2 = OGroup(r_inner, width="50%", panel=True, pad=10, bg_color="#1E1E1E")
    c_in2.layout_.addWidget(OLabel(c_in2, text="Inner 50%"))
    r_inner.layout_.addWidget(c_in1)
    r_inner.layout_.addWidget(c_in2)
    c_n2.layout_.addWidget(r_inner)
    
    r_nested.layout_.addWidget(c_n1)
    r_nested.layout_.addWidget(c_n2)
    page.layout_.addWidget(r_nested)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OTabs
    page.layout_.addWidget(OLabel(page, text="OTabs", bright=True, bold=True, size=14))
    tabs = OTabs(page)
    t1 = tabs.add("General")
    t1.layout().addWidget(OLabel(t1, text="Tab content"))
    tabs.add("Advanced")
    page.layout_.addWidget(tabs)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OTreeWidget
    page.layout_.addWidget(OLabel(page, text="OTreeWidget", bright=True, bold=True, size=14))
    tree1 = OTreeWidget(page, text="Advanced Configuration")
    tree1.add_widget(OLabel(tree1.content, text="Item inside tree"))
    page.layout_.addWidget(tree1)
    
    page.layout_.addStretch()
    return scroll

def build_components_page(stack):
    scroll, page = create_page(stack)
    
    # OLabel
    page.layout_.addWidget(OLabel(page, text="OLabel", bright=True, bold=True, size=14))
    page.layout_.addWidget(OLabel(page, text="This is an OLabel component."))
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OButton
    page.layout_.addWidget(OLabel(page, text="OButton", bright=True, bold=True, size=14))
    btn_row = OGroup(page, orientation="h")
    btn_std = OButton(btn_row, text="Standard OButton")
    btn_prim = OButton(btn_row, text="Primary OButton", primary=True)
    btn_danger = OButton(btn_row, text="Danger OButton", danger=True)
    btn_row.layout_.addWidget(btn_std)
    btn_row.layout_.addWidget(btn_prim)
    btn_row.layout_.addWidget(btn_danger)
    page.layout_.addWidget(btn_row)
    
    btn_feedback = OButton(page, text="Click for Feedback (Changes Color)", primary=True)
    btn_feedback.clicked.connect(lambda: btn_feedback.show_feedback("Action Completed!", success=True))
    page.layout_.addWidget(btn_feedback)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OCheckBox
    page.layout_.addWidget(OLabel(page, text="OCheckBox", bright=True, bold=True, size=14))
    check1 = OCheckBox(page, text="This is an OCheckBox")
    check1.set(True)
    page.layout_.addWidget(check1)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # ORadioButton
    page.layout_.addWidget(OLabel(page, text="ORadioButton", bright=True, bold=True, size=14))
    radio_group = OGroup(page, orientation="h")
    r1 = ORadioButton(radio_group, text="ORadioButton 1")
    r2 = ORadioButton(radio_group, text="ORadioButton 2")
    r1.set(True)
    radio_group.layout_.addWidget(r1)
    radio_group.layout_.addWidget(r2)
    page.layout_.addWidget(radio_group)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OInfoIcon
    page.layout_.addWidget(OLabel(page, text="OInfoIcon", bright=True, bold=True, size=14))
    info_icon = OInfoIcon(page, tooltip_text="Tooltip for OInfoIcon")
    page.layout_.addWidget(info_icon)
    
    page.layout_.addStretch()
    return scroll

def build_inputs_page(stack):
    scroll, page = create_page(stack)
    
    # OComboBox
    page.layout_.addWidget(OLabel(page, text="OComboBox", bright=True, bold=True, size=14))
    combo = OComboBox(page, values=["Option 1", "Option 2", "Option 3"])
    page.layout_.addWidget(combo)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OLineEdit
    page.layout_.addWidget(OLabel(page, text="OLineEdit", bright=True, bold=True, size=14))
    line_edit = OLineEdit(page, placeholder="This is an OLineEdit...")
    page.layout_.addWidget(line_edit)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OTextBox
    page.layout_.addWidget(OLabel(page, text="OTextBox", bright=True, bold=True, size=14))
    textbox = OTextBox(page, height=80, placeholder="This is an OTextBox...")
    page.layout_.addWidget(textbox)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OHotkeyInput
    page.layout_.addWidget(OLabel(page, text="OHotkeyInput", bright=True, bold=True, size=14))
    hotkey = OHotkeyInput(page, width=200)
    hotkey.set("alt+v")
    page.layout_.addWidget(hotkey)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OSpinBox
    page.layout_.addWidget(OLabel(page, text="OSpinBox", bright=True, bold=True, size=14))
    spin = OSpinBox(page, from_=0, to=100)
    page.layout_.addWidget(spin)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OSlider
    page.layout_.addWidget(OLabel(page, text="OSlider", bright=True, bold=True, size=14))
    slider = OSlider(page, orientation="h", show_entry=True)
    slider.set(50)
    page.layout_.addWidget(slider)
    
    page.layout_.addStretch()
    return scroll


def build_tables_page(stack):
    scroll, page = create_page(stack)
    
    # OVirtualTable
    page.layout_.addWidget(OLabel(page, text="OVirtualTable", bright=True, bold=True, size=14))
    
    table = OVirtualTable(
        page, 
        columns=("ID", "Status", "Description", "Action"),
        hug=False,
        visible_rows=10,
        column_widgets=[
            {"class": "QLabel"},
            {"class": "OComboBox", "kwargs": {"values": ["Pending", "Active"]}},
            {"class": "OTextBox"},
            {"class": "QPushButton", "kwargs": {"text": "Delete"}}
        ]
    )
    
    data = []
    for i in range(20):
        data.append((
            f"T-{i}",
            "Active" if i % 2 == 0 else "Pending",
            f"Row {i} in OVirtualTable",
            None
        ))
    table.update_data(data)
    page.layout_.addWidget(table)
    
    page.layout_.addStretch()
    return scroll

def build_media_page(stack):
    scroll, page = create_page(stack)
    
    # OAudioPlayer
    page.layout_.addWidget(OLabel(page, text="OAudioPlayer", bright=True, bold=True, size=14))
    player = OAudioPlayer(page)
    page.layout_.addWidget(player)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OImageViewer
    page.layout_.addWidget(OLabel(page, text="OImageViewer", bright=True, bold=True, size=14))
    viewer = OImageViewer(page, height=200)
    page.layout_.addWidget(viewer)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OProgressBar
    page.layout_.addWidget(OLabel(page, text="OProgressBar (Determinate)", bright=True, bold=True, size=14))
    prog_det = OProgressBar(page)
    prog_det.set(45)
    page.layout_.addWidget(prog_det)
    
    page.layout_.addWidget(OSeparator(page, pad_y=5))
    
    page.layout_.addWidget(OLabel(page, text="OProgressBar (Indeterminate)", bright=True, bold=True, size=14))
    prog_indet = OProgressBar(page)
    prog_indet.set_indeterminate(True)
    page.layout_.addWidget(prog_indet)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OFileItem
    page.layout_.addWidget(OLabel(page, text="OFileItem", bright=True, bold=True, size=14))
    fitem = OFileItem(page, filepath="C:/example/dataset.csv", filesize_str="2.4 MB")
    page.layout_.addWidget(fitem)
    
    page.layout_.addStretch()
    return scroll

def build_chat_page(stack):
    scroll, page = create_page(stack)
    
    # OChatView
    page.layout_.addWidget(OLabel(page, text="OChatView", bright=True, bold=True, size=14))
    chat_view = OChatView(page, height=300) 
    page.layout_.addWidget(chat_view)
    chat_view.add_message("assistant", "Hello! I am OmniNative AI. How can I help you today?")
    chat_view.add_message("user", "Can you show me a table of data?")
    chat_view.add_message("assistant", "Sure, here is a markdown table:\n\n| Item | Value |\n|---|---|\n| Apple | 10 |\n| Banana | 20 |")
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OChatInput
    page.layout_.addWidget(OLabel(page, text="OChatInput", bright=True, bold=True, size=14))
    chat_input = OChatInput(page)
    chat_input.submitted.connect(lambda text: chat_view.add_message("user", text))
    page.layout_.addWidget(chat_input)
    
    page.layout_.addStretch()
    return scroll

def build_overlays_page(stack, main_window):
    scroll, page = create_page(stack)
    
    # OActionMenu
    page.layout_.addWidget(OLabel(page, text="OActionMenu", bright=True, bold=True, size=14))
    btn_menu = OButton(page, text="Trigger OActionMenu", primary=True, width=200)
    menu = OActionMenu(main_window)
    item1 = menu.add_action("Edit Profile")
    item2 = menu.add_action("Settings")
    btn_menu.clicked.connect(lambda: menu.show_above(btn_menu))
    page.layout_.addWidget(btn_menu)
    
    page.layout_.addWidget(OSeparator(page, pad_y=10))
    
    # OAudioRecorderOverlay
    page.layout_.addWidget(OLabel(page, text="OAudioRecorderOverlay", bright=True, bold=True, size=14))
    recorder = OAudioRecorderOverlay(main_window, chunk_ms=500)
    btn_rec = OButton(page, text="Toggle OAudioRecorderOverlay", danger=True, width=250)
    btn_rec.clicked.connect(recorder.toggle)
    page.layout_.addWidget(btn_rec)
    
    page.layout_.addStretch()
    return scroll


def main():
    app = QApplication(sys.argv)
    
    window = OWindow(title="OmniNative UI Components Demo", width=1100, height=800, resizable=True)
    window.body.layout().setContentsMargins(0, 0, 0, 0)
    window.body.layout().setSpacing(0)
    
    # Main Horizontal Layout
    main_layout = OGroup(window.body, orientation="h")
    main_layout.layout_.setContentsMargins(0, 0, 0, 0)
    main_layout.layout_.setSpacing(0)
    window.body.layout().addWidget(main_layout)
    
    # Left Sidebar (OSidebar)
    sidebar = OSidebar(main_layout, width=240)
    # Adjust header margin to compensate for the 8px internal padding of the app icon
    # so that the visual circle perfectly aligns with the text of the sidebar items.
    sidebar.header_layout.setContentsMargins(17, 0, 25, 0)
    main_layout.layout_.addWidget(sidebar)
    
    from omninative_ui.icons import _get_cached_app_icon
    app_icon = OLabel(sidebar.header_group)
    app_icon.setPixmap(_get_cached_app_icon(32).pixmap(32, 32))
    app_icon.setStyleSheet("background: transparent;")
    sidebar.header_layout.addWidget(app_icon)

    sidebar.header_layout.setSpacing(0)

    logo = OLabel(sidebar.header_group, text="OmniNative UI")
    logo.setStyleSheet("color: #FFFFFF; font-family: 'Cormorant Garamond'; font-size: 20px; font-weight: bold; font-style: italic; background: transparent;")
    sidebar.header_layout.addWidget(logo)
    
    version = OLabel(sidebar.footer_group, text="v0.1.13", size=9)
    sidebar.footer_layout.addWidget(version)
    
    # Right Content (Stacked Widget)
    stacked = QStackedWidget(main_layout)
    stacked.setStyleSheet("background: transparent;")
    main_layout.layout_.addWidget(stacked, 1) # flex-grow 1
    
    # Build Pages
    pages = {
        "Layouts": build_layouts_page(stacked),
        "Buttons & Labels": build_components_page(stacked),
        "Inputs & Forms": build_inputs_page(stacked),
        "Data Tables": build_tables_page(stacked),
        "Media & Files": build_media_page(stacked),
        "Chat Interface": build_chat_page(stacked),
        "Overlays": build_overlays_page(stacked, window)
    }
    
    # Add pages to stacked widget and sidebar
    for i, (name, page_widget) in enumerate(pages.items()):
        stacked.addWidget(page_widget)
        # We need to capture the current value of i in the lambda
        # by passing it as a default argument `index=i`
        sidebar.add_item(name, lambda index=i: stacked.setCurrentIndex(index))
        
    sidebar.set_active_item("Layouts")
    stacked.setCurrentIndex(0)
    
    # Reveal and run
    window.omninativeui_reveal_when_ready()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
