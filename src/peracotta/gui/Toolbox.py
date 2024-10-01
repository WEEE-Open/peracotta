from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Union

from PyQt5 import QtCore, QtGui, QtWidgets

from ..commons import item_only_features
from ..constants import ICON
from ..peralog import logger
from . import prettyprinter


class ItemEnumDelegate(QtWidgets.QStyledItemDelegate):
    # class ItemEnumAlignDelegate(QtWidgets.QStyledItemDelegate):
    #     def initStyleOption(self, option, index):
    #         super().initStyleOption(option, index)
    #         option.displayAlignment = QtCore.Qt.AlignLeft

    def createEditor(self, parent, option, index):
        the_type = str(index.model().data(index, QtCore.Qt.ItemDataRole.UserRole))
        if the_type == "e":
            editor = QtWidgets.QComboBox(parent)
            editor.currentTextChanged.connect(self.handle_editor_change)
            editor.setEditable(True)
            return editor
        else:
            return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        model: CustomTableModel = index.model()
        if isinstance(editor, QtWidgets.QComboBox):
            values = model.row_all_enum_values_for_editor(index.row())
            current = model.row_current_enum_value_for_editor(index.row())
            if values and current:
                # editor.setItemDelegate(self.ItemEnumAlignDelegate(editor))
                for k, v in values.items():
                    editor.addItem(v, k)
                    i = editor.count() - 1
                    if current == k:
                        editor.setCurrentIndex(i)
        else:
            return super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QtWidgets.QComboBox):
            model.setData(index, editor.currentData(), QtCore.Qt.EditRole)
        else:
            return super().setModelData(editor, model, index)

    def handle_editor_change(self):
        editor = self.sender()
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)


class CustomTableView(QtWidgets.QTableView):
    def __init__(self):
        super().__init__()
        self.setItemDelegateForColumn(1, ItemEnumDelegate())

    def minimumSizeHint(self) -> QtCore.QSize:
        default_size = super().minimumSizeHint()

        frame = self.frameWidth() * 2

        header = self.verticalHeader().sizeHint().height()
        rows = self.verticalHeader().length()
        # rows = self.model().rowCount() * self.horizontalHeader().defaultSectionSize()
        h = header + rows + frame
        # print(f"{header} + {rows} + {frame} = {h} > {default_size.height()}")

        return QtCore.QSize(default_size.width(), h)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        menu = QtWidgets.QMenu(self)
        remove_action = QtWidgets.QAction("Remove feature", self)
        remove_action.triggered.connect(self.remove_row)
        menu.addAction(remove_action)
        menu.popup(QtGui.QCursor.pos())

    def remove_row(self):
        self.model().removeRow(self.selectedIndexes()[1].row(), self.selectedIndexes()[1].parent())


class CustomTableModel(QtCore.QAbstractTableModel):
    emergency_resize = QtCore.pyqtSignal(name="emergency_resize")

    def __init__(self, data: List[dict], item_features: dict, product: Optional[dict], default_features: dict):
        super().__init__()

        self._data = data
        self.ref_features = item_features
        self.ref_product = product
        self.default_features = default_features

        self.features = {}
        self.feature_keys = []
        self._productize(item_features, product)

    def _productize(self, item_features: dict, product: Optional[dict]):
        if product:
            self.features = product["features"].copy()
        else:
            self.features = {}
        self.features.update(item_features)
        self.feature_keys = list(self.features)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.feature_keys)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 2

    # noinspection PyMethodOverriding
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole and orientation == QtCore.Qt.Orientation.Horizontal:
            if section == 0:
                return "Feature"
            else:
                return "Value"
        return None

    def flags(self, index):
        if index.column() == 1:
            return QtCore.Qt.ItemFlag.ItemIsEditable | QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable
        else:
            return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable

    def row_all_enum_values_for_editor(self, row: int) -> Optional[Dict[str, str]]:
        if row < 0 or row >= len(self.feature_keys):
            return None

        name = self.feature_keys[row]
        feature_type = self._get_feature_type(name)
        if feature_type == "e":
            return self.default_features["values"][name]
        return None

    def row_current_enum_value_for_editor(self, row: int):
        if row < 0 or row >= len(self.features):
            return None

        name = self.feature_keys[row]
        return self.features.get(name)

    # def _row_to_name(self, row) -> Optional[str]:
    #     for i, name in enumerate(self.combined):
    #         if i == row:
    #             return name
    #         else:
    #             return None

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        row = index.row()
        if row < 0 or row >= len(self.feature_keys):
            return None

        if role == QtCore.Qt.ItemDataRole.DisplayRole or role == QtCore.Qt.ItemDataRole.EditRole or role == QtCore.Qt.ItemDataRole.UserRole:
            column = index.column()
            name = self.feature_keys[row]
            if column == 0:
                return self.default_features["names"].get(name, name)
            elif column == 1:
                feature_type = self._get_feature_type(name)
                if role == QtCore.Qt.ItemDataRole.UserRole:
                    return feature_type
                value = self.features[name]
                if feature_type == "e":
                    return self.default_features["values"][name].get(value, value)
                elif feature_type in ("d", "i"):
                    return prettyprinter.print_feature(name, value, feature_type)
                else:
                    return value
        elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            column = index.column()
            if column == 0:
                return QtCore.Qt.AlignmentFlag.AlignLeft + QtCore.Qt.AlignmentFlag.AlignVCenter
            elif column == 1:
                return QtCore.Qt.AlignmentFlag.AlignRight + QtCore.Qt.AlignmentFlag.AlignVCenter

        return None

    # noinspection PyMethodOverriding
    def setData(self, index, value, role):
        if role == QtCore.Qt.ItemDataRole.EditRole:
            row = index.row()
            col = index.column()
            if col != 1:
                return False
            if row < 0 or row >= len(self.feature_keys):
                return False

            # Feature name
            name = self.feature_keys[row]
            # Normalize and validate, with EXTREME intensity
            ok, value = self.extreme_validation(name, value)
            if ok:
                # Add to features, this is a local copy of merged
                # item and product features
                self.features[name] = value
                product_to_add = None
                # Search if a product is there but not linked,
                # this is needed when a new item is added
                # since brand, model and variant are filled
                # one at a time
                if not self.ref_product:
                    product_to_add = ToolBoxWidget.find_matching_product(self._data, self.features)
                    if product_to_add:
                        self.beginResetModel()
                        self._productize(self.features, product_to_add)
                # If this feature exists in the product, add it there.
                # Otherwise, if the item has it, add it there.
                # Otherwise, find where it should be added.
                if self.ref_product and name in self.ref_product["features"]:
                    self.ref_product["features"][name] = value
                elif name in self.ref_features:
                    self.ref_features[name] = value
                    # If brand or model or variant was changed
                    # update product and related items, too
                    if self.ref_product and name in ("brand", "model", "variant"):
                        self._rename_product(self.ref_product, name, value)
                else:
                    self._add_to_ref(name, value)
                if product_to_add:
                    self.endResetModel()
                    self.emergency_resize.emit()
            return ok
        return False

    def extreme_validation(self, name: str, value: Union[str, int, float]) -> Tuple[bool, Union[str, int, float]]:
        feature_type = self._get_feature_type(name)
        if isinstance(value, str):
            value = value.strip()
        if feature_type == "e":
            value = str(value).lower()
            if value not in self.default_features["values"][name]:
                return False, None
        elif feature_type == "d":
            value = self._printable_to_value(name, value)
            value = float(value)
            if value <= 0:
                return False, None
        elif feature_type == "i":
            value = self._printable_to_value(name, value)
            value = int(round(value))
            if value <= 0:
                return False, None
        else:
            if len(value) <= 0:
                return False, None
        return True, value

    def _rename_product(self, product: dict, feature: str, value: str):
        if "brand" not in product or "model" not in product or "variant" not in product:
            # Sanity check, but should never happen
            return

        for maybe in self._data:
            if maybe.get("type") == "I":
                if ToolBoxWidget.bmv_match(product, maybe.get("features", {})):
                    maybe["features"][feature] = value

        # Finally, update product itself
        self.ref_product[feature] = value

    def removeRow(self, row: int, parent: QtCore.QModelIndex() = ...) -> bool:
        # TODO: remove this limitation asd
        if not self._pre_delete_check(row):
            return False

        self.beginRemoveRows(parent, row, row)
        try:
            removed = self.feature_keys.pop(row)
            try:
                del self.features[removed]
                # TODO: remove from features but show product one if it exists
                if removed in self.ref_features:
                    del self.ref_features[removed]
                if self.ref_product and removed in self.ref_product["features"]:
                    del self.ref_product["features"][removed]
            except IndexError:
                pass
        except IndexError:
            self.endRemoveRows()
            return False
        self.endRemoveRows()
        return True

    def _pre_delete_check(self, row) -> bool:
        feature_name = self.feature_keys[row]
        if self.features.get(feature_name) in ("brand", "model", "variant"):
            if self.ref_product:
                return False
        return True

    @staticmethod
    def _printable_to_value(name, value):
        # noinspection PyBroadException
        try:
            value = prettyprinter.printable_to_value(prettyprinter.name_to_unit(name), value)
        except BaseException:
            value = 0
        return value

    def _get_feature_type(self, name):
        feature_type = self.default_features["types"].get(name, "s")
        return feature_type

    def insert_row(self, feature: str, value: str) -> bool:
        if feature in self.feature_keys:
            return False

        row_index = self.rowCount()

        ok, value = self.extreme_validation(feature, value)
        product_to_add = None
        if ok:
            self.beginInsertRows(QtCore.QModelIndex(), row_index, row_index)
            self.feature_keys.append(feature)
            self.features[feature] = value
            if not self.ref_product:
                product_to_add = ToolBoxWidget.find_matching_product(self._data, self.features)
            self._add_to_ref(feature, value)
            self.endInsertRows()

        if product_to_add:
            self.beginResetModel()
            self._productize(self.features, product_to_add)
            self.endResetModel()

        self.emergency_resize.emit()

        return ok

    def features_in_table(self):
        return self.feature_keys

    def _add_to_ref(self, name: str, value):
        if name in item_only_features():
            target = self.ref_features
        elif self.ref_product:
            target = self.ref_product["features"]
        else:
            target = self.ref_features
        target[name] = value


class ToolBoxItem(QtWidgets.QWidget):
    def __init__(self, data: List[dict], features: dict, product: Optional[dict], default_features: dict):
        super().__init__()
        self.default_features = default_features

        self.main_layout = QtWidgets.QVBoxLayout()
        self.table = CustomTableView()
        self.features_combo_box = QtWidgets.QComboBox()
        self.feature_line_edit = QtWidgets.QLineEdit()
        self.feature_selector = QtWidgets.QComboBox()
        self.add_feature_button = QtWidgets.QPushButton("Add")
        self.add_feature_button.clicked.connect(self.add_feature)
        self.add_feature_button.setMinimumWidth(60)

        # setup
        self.table_setup(data, features, product, default_features)
        self.adder_layout = self._create_feature_adder()
        self.main_layout.addLayout(self.adder_layout)
        self.setLayout(self.main_layout)

    def external_size_hint_height(self):
        h1 = max(self.table.minimumSizeHint().height(), self.table.sizeHint().height())
        h2 = self.adder_layout.sizeHint().height()

        return h1 + h2

    def table_setup(self, data: List[dict], features: dict, product: Optional[dict], default_features: dict):
        ctm = CustomTableModel(data, features, product, default_features)
        ctm.emergency_resize.connect(self._do_the_emergency_resize)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setModel(ctm)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.verticalScrollBar().hide()
        self.table.verticalScrollBar().resize(0, 0)
        self.main_layout.addWidget(self.table)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        hh = QtWidgets.QHeaderView = self.table.horizontalHeader()
        hh.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)

    def _do_the_emergency_resize(self):
        self.parentWidget().parentWidget().updateGeometry()
        self.table.resizeColumnToContents(0)

    def _create_feature_adder(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.features_combo_box)
        layout.addWidget(self.feature_line_edit)
        layout.addWidget(self.feature_selector)
        layout.addWidget(self.add_feature_button)
        for name in self.default_features["names"]:
            self.features_combo_box.addItem(self.default_features["names"][name])
        self.features_combo_box.currentTextChanged.connect(self.set_input_type)
        self.set_input_type()
        return layout

    def set_input_type(self):
        for the_type in self.default_features["types"]:
            if self.default_features["names"][the_type] == self.features_combo_box.currentText():
                # set input type
                if self.default_features["types"][the_type] == "e":
                    self.feature_line_edit.setHidden(True)
                    self.feature_selector.setHidden(False)
                    self.feature_selector.clear()
                    i = 0
                    for value in self.default_features["values"][the_type]:
                        self.feature_selector.addItem(self.default_features["values"][the_type][value])
                        self.feature_selector.setItemData(i, value)
                        i += 1
                else:
                    self.feature_line_edit.setHidden(False)
                    self.feature_selector.setHidden(True)
                # disable button if feature already in table
                if the_type in self.table.model().features_in_table():
                    self.set_add_control_enabled(False)
                else:
                    self.set_add_control_enabled(True)

    def add_feature(self):
        feature = list(self.default_features["types"])[self.features_combo_box.currentIndex()]
        if self.feature_line_edit.isVisible():
            value = self.feature_line_edit.text()
        elif self.feature_selector.isVisible():
            value = self.feature_selector.currentData()
        else:
            return
        model: CustomTableModel = self.table.model()
        ok = model.insert_row(feature, value)
        if ok:
            self.set_add_control_enabled(False)
        self.feature_line_edit.clear()

    def set_add_control_enabled(self, flag: bool):
        self.add_feature_button.setEnabled(flag)
        self.feature_line_edit.setEnabled(flag)
        self.feature_selector.setEnabled(flag)

    def minimumSizeHint(self) -> QtCore.QSize:
        return self.table.minimumSizeHint()


class ToolBoxWidget(QtWidgets.QToolBox):
    def __init__(self, data: List[dict], default_features: dict, encountered_types_count: dict):
        super().__init__()
        self.data = data
        self.default_features = default_features
        self.encountered_types_count = encountered_types_count
        self.menu = None

        # variables
        self.encountered_types_current_count = defaultdict(lambda: 0)

    def clear(self):
        for idx in range(self.count()):
            self.removeItem(0)
        self.encountered_types_count.clear()
        self.encountered_types_current_count.clear()

    def load_items(self, data: List[dict]):
        if data:
            self.clear()
            self.data = data
            self.types_count()

        # find brand, model and variant of all products in data
        products = {}
        for idx, entry in enumerate(self.data):
            if entry["type"] == "P":
                products[idx] = (entry["brand"], entry["model"], entry["variant"])

        for entry in self.data:
            self.add_item(entry)

        # remove scroll in toolbox's scrollAreas
        for scroll_area in self.findChildren(QtWidgets.QScrollArea):
            scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll_area.verticalScrollBar().hide()
            scroll_area.verticalScrollBar().resize(0, 0)

    def add_item(self, item: Optional[dict] = None, item_type: Optional[str] = None, single_item: Optional[bool] = False):
        if single_item:
            self.data.append(
                {
                    "type": "I",
                    "features": {
                        "type": item_type,
                    },
                }
            )
            found_product = None
        else:
            found_product = self.find_matching_product(self.data, item.get("features", {}))

        if item and item["type"] != "I":
            return

        counter = ""

        if item_type is None and item:
            item_type = item["features"]["type"]
        if self.encountered_types_count[item_type] > 1:
            self.encountered_types_current_count[item_type] += 1
            counter = f" #{self.encountered_types_current_count[item_type]}"
        if single_item:
            features = self.data[-1]["features"]
        else:
            features = item["features"]

        self.addItem(
            ToolBoxItem(self.data, features, found_product, self.default_features),
            f"{self.print_type_cool(item_type)}{counter}",
        )
        if item_type in ICON:
            icon = QtGui.QIcon(ICON[item_type])
            self.setItemIcon(self.count() - 1, icon)

        self.set_context_menu()

    @staticmethod
    def find_matching_product(data: List[dict], features: dict):
        if "model" in features and "brand" in features and "variant" in features:
            for maybe in data:
                if maybe.get("type") == "P":
                    if ToolBoxWidget.bmv_match(features, maybe):
                        return maybe
        return None

    @staticmethod
    def bmv_match(dict1, dict2) -> bool:
        return dict1.get("brand") == dict2.get("brand") and dict1.get("model") == dict2.get("model") and dict1.get("variant") == dict2.get("variant")

    def set_context_menu(self):
        counter = 0
        for item in self.children():
            if type(item) == QtWidgets.QAbstractButton:
                item: QtWidgets.QAbstractButton
                item.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
                item.customContextMenuRequested.connect(self.show_menu)
                counter += 1

    def print_type_cool(self, the_type: str) -> str:
        if the_type in self.default_features["values"]["type"]:
            return self.default_features["values"]["type"][the_type]
        else:
            return the_type.title()

    def show_menu(self):
        button = self.sender()
        self.menu = QtWidgets.QMenu()
        remove_action = QtWidgets.QAction("Remove item", self)
        remove_action.triggered.connect(lambda: self.remove_item_from_toolbox(button))
        self.menu.addAction(remove_action)
        self.menu.popup(QtGui.QCursor.pos())

    def minimumSizeHint(self) -> QtCore.QSize:
        h = 0
        for child in self.children():
            if isinstance(child, QtWidgets.QScrollArea):
                if child.isHidden():
                    # print("Hidden!")
                    pass
                    # print(f"Hidden min {child.minimumSizeHint().height()}")
                    # print(f"Hidden {child.sizeHint().height()}")
                    # h += child.minimumSizeHint().height()
                else:
                    the_widget = child.widget()
                    if the_widget and isinstance(the_widget, ToolBoxItem):
                        hinted = the_widget.external_size_hint_height()
                        # print(f"Hinted: {hinted}")
                        h += hinted
                    else:
                        # h += max(child.sizeHint().height(), child.minimumSizeHint().height())
                        pass
            elif isinstance(child, QtWidgets.QAbstractButton):
                # print(f"{child}: {child.sizeHint().height()} {child.minimumSizeHint().height()}")
                # Why 1.5? Dunno, they're ~40 pixels and sizeHint is 25 (minimum 24).
                h += int(child.sizeHint().height() * 1.5)
        old = super().minimumSizeHint()
        if h > old.height():
            return QtCore.QSize(old.width(), h)
        return old

    def remove_item_from_toolbox(self, button):
        i = 0
        for item in self.children():
            if isinstance(item, QtWidgets.QAbstractButton):
                if item == button:
                    self.removeItem(i)
                    break
                else:
                    i += 1

    def removeItem(self, index: int) -> None:
        i = 0
        data_index = None
        for data_index, entry in enumerate(self.data):
            if entry["type"] != "I":
                continue
            if index == i:
                break
            i += 1

        item_to_remove = self.data[data_index]
        item_b = item_to_remove["features"].get("brand")
        item_m = item_to_remove["features"].get("model")
        item_v = item_to_remove["features"].get("variant")
        counter = 0
        product_index = None
        deleted = False
        try:
            if item_b and item_m and item_v:
                for idx, entry in enumerate(self.data):
                    # count items with the same product
                    if entry["type"] == "I" and idx != data_index:
                        test_b = entry["features"].get("brand")
                        test_m = entry["features"].get("model")
                        test_v = entry["features"].get("variant")
                        if item_b == test_b and item_m == test_m and item_v == test_v:
                            counter += 1
                    # find the product itself
                    elif entry["type"] == "P":
                        p_test_b = entry.get("brand")
                        p_test_m = entry.get("model")
                        p_test_v = entry.get("variant")
                        if item_b == p_test_b and item_m == p_test_m and item_v == p_test_v:
                            product_index = idx
                if counter <= 0 and product_index:
                    # If both item and product have to be deleted, delete them
                    # without f...messing up indexes
                    if data_index >= product_index:
                        del self.data[data_index]
                        del self.data[product_index]
                    else:
                        del self.data[product_index]
                        del self.data[data_index]
                    deleted = True
        except KeyError as e:
            logger.error("Item to be removed is missing something")
            logger.error(f"{entry = }")
            raise e
        # All other cases (item with no product, product not found, other items linked to product):
        # just delete the product
        if not deleted:
            del self.data[data_index]

        widget_ref = self.widget(index)
        super().removeItem(index)
        widget_ref.deleteLater()

    def types_count(self, data: list = None):
        if data is not None:
            self.data = data
        for entry in self.data:
            if entry["type"] != "I":
                continue
            the_type = entry["features"]["type"]
            self.encountered_types_count[the_type] += 1
