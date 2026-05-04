import '/components/achievement_hero_widget.dart';
import '/components/activity_item_widget.dart';
import '/components/coaching_bubble_widget.dart';
import '/components/stat_card_kr_widget.dart';
import '/components/std_button_widget.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'home_page_angry_copy_widget.dart' show HomePageAngryCopyWidget;
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

class HomePageAngryCopyModel extends FlutterFlowModel<HomePageAngryCopyWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for AchievementHero.
  late AchievementHeroModel achievementHeroModel;
  // Model for StdButton.
  late StdButtonModel stdButtonModel;
  // Model for StatCardKr.
  late StatCardKrModel statCardKrModel1;
  // Model for StatCardKr.
  late StatCardKrModel statCardKrModel2;
  // Model for StatCardKr.
  late StatCardKrModel statCardKrModel3;
  // Model for CoachingBubble.
  late CoachingBubbleModel coachingBubbleModel;
  // Model for ActivityItem.
  late ActivityItemModel activityItemModel1;
  // Model for ActivityItem.
  late ActivityItemModel activityItemModel2;

  @override
  void initState(BuildContext context) {
    achievementHeroModel = createModel(context, () => AchievementHeroModel());
    stdButtonModel = createModel(context, () => StdButtonModel());
    statCardKrModel1 = createModel(context, () => StatCardKrModel());
    statCardKrModel2 = createModel(context, () => StatCardKrModel());
    statCardKrModel3 = createModel(context, () => StatCardKrModel());
    coachingBubbleModel = createModel(context, () => CoachingBubbleModel());
    activityItemModel1 = createModel(context, () => ActivityItemModel());
    activityItemModel2 = createModel(context, () => ActivityItemModel());
  }

  @override
  void dispose() {
    achievementHeroModel.dispose();
    stdButtonModel.dispose();
    statCardKrModel1.dispose();
    statCardKrModel2.dispose();
    statCardKrModel3.dispose();
    coachingBubbleModel.dispose();
    activityItemModel1.dispose();
    activityItemModel2.dispose();
  }
}
