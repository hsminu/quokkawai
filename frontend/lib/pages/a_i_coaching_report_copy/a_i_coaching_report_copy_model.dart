import '/components/action_card_kr_widget.dart';
import '/components/coaching_bubble_widget.dart';
import '/components/stat_card_kr_widget.dart';
import '/components/std_button_widget.dart';
import '/flutter_flow/flutter_flow_charts.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'a_i_coaching_report_copy_widget.dart' show AICoachingReportCopyWidget;
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

class AICoachingReportCopyModel
    extends FlutterFlowModel<AICoachingReportCopyWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for CoachingBubble.
  late CoachingBubbleModel coachingBubbleModel;
  // Model for StatCardKr.
  late StatCardKrModel statCardKrModel1;
  // Model for StatCardKr.
  late StatCardKrModel statCardKrModel2;
  // Model for ActionCardKr.
  late ActionCardKrModel actionCardKrModel1;
  // Model for ActionCardKr.
  late ActionCardKrModel actionCardKrModel2;
  // Model for ActionCardKr.
  late ActionCardKrModel actionCardKrModel3;
  // Model for StdButton.
  late StdButtonModel stdButtonModel;

  @override
  void initState(BuildContext context) {
    coachingBubbleModel = createModel(context, () => CoachingBubbleModel());
    statCardKrModel1 = createModel(context, () => StatCardKrModel());
    statCardKrModel2 = createModel(context, () => StatCardKrModel());
    actionCardKrModel1 = createModel(context, () => ActionCardKrModel());
    actionCardKrModel2 = createModel(context, () => ActionCardKrModel());
    actionCardKrModel3 = createModel(context, () => ActionCardKrModel());
    stdButtonModel = createModel(context, () => StdButtonModel());
  }

  @override
  void dispose() {
    coachingBubbleModel.dispose();
    statCardKrModel1.dispose();
    statCardKrModel2.dispose();
    actionCardKrModel1.dispose();
    actionCardKrModel2.dispose();
    actionCardKrModel3.dispose();
    stdButtonModel.dispose();
  }
}
