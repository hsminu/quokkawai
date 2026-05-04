import '/components/app_limit_item_widget.dart';
import '/components/coaching_bubble_widget.dart';
import '/components/schedule_card_widget.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'set_goals_page_copy_widget.dart' show SetGoalsPageCopyWidget;
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

class SetGoalsPageCopyModel extends FlutterFlowModel<SetGoalsPageCopyWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for CoachingBubble.
  late CoachingBubbleModel coachingBubbleModel;
  // State field(s) for Slider widget.
  double? sliderValue;
  // Model for AppLimitItem.
  late AppLimitItemModel appLimitItemModel1;
  // Model for AppLimitItem.
  late AppLimitItemModel appLimitItemModel2;
  // Model for ScheduleCard.
  late ScheduleCardModel scheduleCardModel1;
  // Model for ScheduleCard.
  late ScheduleCardModel scheduleCardModel2;

  @override
  void initState(BuildContext context) {
    coachingBubbleModel = createModel(context, () => CoachingBubbleModel());
    appLimitItemModel1 = createModel(context, () => AppLimitItemModel());
    appLimitItemModel2 = createModel(context, () => AppLimitItemModel());
    scheduleCardModel1 = createModel(context, () => ScheduleCardModel());
    scheduleCardModel2 = createModel(context, () => ScheduleCardModel());
  }

  @override
  void dispose() {
    coachingBubbleModel.dispose();
    appLimitItemModel1.dispose();
    appLimitItemModel2.dispose();
    scheduleCardModel1.dispose();
    scheduleCardModel2.dispose();
  }
}
