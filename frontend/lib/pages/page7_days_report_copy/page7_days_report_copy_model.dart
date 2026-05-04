import '/components/app_usage_item_kr_widget.dart';
import '/components/stat_card_kr_widget.dart';
import '/components/std_button_widget.dart';
import '/flutter_flow/flutter_flow_charts.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'page7_days_report_copy_widget.dart' show Page7DaysReportCopyWidget;
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:percent_indicator/percent_indicator.dart';
import 'package:provider/provider.dart';

class Page7DaysReportCopyModel
    extends FlutterFlowModel<Page7DaysReportCopyWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for StatCardKr.
  late StatCardKrModel statCardKrModel1;
  // Model for StatCardKr.
  late StatCardKrModel statCardKrModel2;
  // Model for AppUsageItemKr.
  late AppUsageItemKrModel appUsageItemKrModel1;
  // Model for AppUsageItemKr.
  late AppUsageItemKrModel appUsageItemKrModel2;
  // Model for AppUsageItemKr.
  late AppUsageItemKrModel appUsageItemKrModel3;
  // Model for AppUsageItemKr.
  late AppUsageItemKrModel appUsageItemKrModel4;
  // Model for StdButton.
  late StdButtonModel stdButtonModel;

  @override
  void initState(BuildContext context) {
    statCardKrModel1 = createModel(context, () => StatCardKrModel());
    statCardKrModel2 = createModel(context, () => StatCardKrModel());
    appUsageItemKrModel1 = createModel(context, () => AppUsageItemKrModel());
    appUsageItemKrModel2 = createModel(context, () => AppUsageItemKrModel());
    appUsageItemKrModel3 = createModel(context, () => AppUsageItemKrModel());
    appUsageItemKrModel4 = createModel(context, () => AppUsageItemKrModel());
    stdButtonModel = createModel(context, () => StdButtonModel());
  }

  @override
  void dispose() {
    statCardKrModel1.dispose();
    statCardKrModel2.dispose();
    appUsageItemKrModel1.dispose();
    appUsageItemKrModel2.dispose();
    appUsageItemKrModel3.dispose();
    appUsageItemKrModel4.dispose();
    stdButtonModel.dispose();
  }
}
