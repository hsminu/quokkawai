import '/components/std_textfield_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'form_field_group_widget.dart' show FormFieldGroupWidget;
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

class FormFieldGroupModel extends FlutterFlowModel<FormFieldGroupWidget> {
  ///  State fields for stateful widgets in this component.

  // Model for StdTextfield.
  late StdTextfieldModel stdTextfieldModel;

  @override
  void initState(BuildContext context) {
    stdTextfieldModel = createModel(context, () => StdTextfieldModel());
  }

  @override
  void dispose() {
    stdTextfieldModel.dispose();
  }
}
