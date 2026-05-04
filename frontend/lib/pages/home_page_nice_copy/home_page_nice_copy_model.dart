import '/components/activity_item907fb0e8_widget.dart';
import '/components/std_button2b7b0cb0_widget.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'home_page_nice_copy_widget.dart' show HomePageNiceCopyWidget;
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:percent_indicator/percent_indicator.dart';
import 'package:provider/provider.dart';

class HomePageNiceCopyModel extends FlutterFlowModel<HomePageNiceCopyWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for StdButton2b7b0cb0.
  late StdButton2b7b0cb0Model stdButton2b7b0cb0Model;
  // Model for ActivityItem907fb0e8.
  late ActivityItem907fb0e8Model activityItem907fb0e8Model1;
  // Model for ActivityItem907fb0e8.
  late ActivityItem907fb0e8Model activityItem907fb0e8Model2;

  @override
  void initState(BuildContext context) {
    stdButton2b7b0cb0Model =
        createModel(context, () => StdButton2b7b0cb0Model());
    activityItem907fb0e8Model1 =
        createModel(context, () => ActivityItem907fb0e8Model());
    activityItem907fb0e8Model2 =
        createModel(context, () => ActivityItem907fb0e8Model());
  }

  @override
  void dispose() {
    stdButton2b7b0cb0Model.dispose();
    activityItem907fb0e8Model1.dispose();
    activityItem907fb0e8Model2.dispose();
  }
}
