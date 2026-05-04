import '/components/std_switch_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'schedule_card_widget.dart' show ScheduleCardWidget;
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

class ScheduleCardModel extends FlutterFlowModel<ScheduleCardWidget> {
  ///  State fields for stateful widgets in this component.

  // Model for StdSwitch.
  late StdSwitchModel stdSwitchModel;

  @override
  void initState(BuildContext context) {
    stdSwitchModel = createModel(context, () => StdSwitchModel());
  }

  @override
  void dispose() {
    stdSwitchModel.dispose();
  }
}
