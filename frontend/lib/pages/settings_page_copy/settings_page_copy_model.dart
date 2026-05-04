import '/components/settings_group_header_widget.dart';
import '/components/settings_item_widget.dart';
import '/components/std_button_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'settings_page_copy_widget.dart' show SettingsPageCopyWidget;
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

class SettingsPageCopyModel extends FlutterFlowModel<SettingsPageCopyWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for StdButton.
  late StdButtonModel stdButtonModel;
  // Model for SettingsGroupHeader.
  late SettingsGroupHeaderModel settingsGroupHeaderModel1;
  // Model for SettingsItem.
  late SettingsItemModel settingsItemModel1;
  // Model for SettingsItem.
  late SettingsItemModel settingsItemModel2;
  // Model for SettingsGroupHeader.
  late SettingsGroupHeaderModel settingsGroupHeaderModel2;
  // Model for SettingsItem.
  late SettingsItemModel settingsItemModel3;
  // Model for SettingsItem.
  late SettingsItemModel settingsItemModel4;
  // Model for SettingsItem.
  late SettingsItemModel settingsItemModel5;
  // Model for SettingsGroupHeader.
  late SettingsGroupHeaderModel settingsGroupHeaderModel3;
  // Model for SettingsItem.
  late SettingsItemModel settingsItemModel6;
  // Model for SettingsItem.
  late SettingsItemModel settingsItemModel7;
  // Model for SettingsItem.
  late SettingsItemModel settingsItemModel8;

  @override
  void initState(BuildContext context) {
    stdButtonModel = createModel(context, () => StdButtonModel());
    settingsGroupHeaderModel1 =
        createModel(context, () => SettingsGroupHeaderModel());
    settingsItemModel1 = createModel(context, () => SettingsItemModel());
    settingsItemModel2 = createModel(context, () => SettingsItemModel());
    settingsGroupHeaderModel2 =
        createModel(context, () => SettingsGroupHeaderModel());
    settingsItemModel3 = createModel(context, () => SettingsItemModel());
    settingsItemModel4 = createModel(context, () => SettingsItemModel());
    settingsItemModel5 = createModel(context, () => SettingsItemModel());
    settingsGroupHeaderModel3 =
        createModel(context, () => SettingsGroupHeaderModel());
    settingsItemModel6 = createModel(context, () => SettingsItemModel());
    settingsItemModel7 = createModel(context, () => SettingsItemModel());
    settingsItemModel8 = createModel(context, () => SettingsItemModel());
  }

  @override
  void dispose() {
    stdButtonModel.dispose();
    settingsGroupHeaderModel1.dispose();
    settingsItemModel1.dispose();
    settingsItemModel2.dispose();
    settingsGroupHeaderModel2.dispose();
    settingsItemModel3.dispose();
    settingsItemModel4.dispose();
    settingsItemModel5.dispose();
    settingsGroupHeaderModel3.dispose();
    settingsItemModel6.dispose();
    settingsItemModel7.dispose();
    settingsItemModel8.dispose();
  }
}
