import '/components/std_button_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'activity_item_widget.dart' show ActivityItemWidget;
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

class ActivityItemModel extends FlutterFlowModel<ActivityItemWidget> {
  ///  State fields for stateful widgets in this component.

  // Model for StdButton.
  late StdButtonModel stdButtonModel;

  @override
  void initState(BuildContext context) {
    stdButtonModel = createModel(context, () => StdButtonModel());
  }

  @override
  void dispose() {
    stdButtonModel.dispose();
  }
}
