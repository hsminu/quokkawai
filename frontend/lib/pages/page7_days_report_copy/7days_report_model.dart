import '/components/app_usage_item_kr_widget.dart';
import '/components/stat_card_kr_widget.dart';
import '/components/std_button_widget.dart';
import '/flutter_flow/flutter_flow_charts.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import '7days_report_widget.dart' show Page7DaysReportCopyWidget;
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:percent_indicator/percent_indicator.dart';
import 'package:provider/provider.dart';
import 'package:app_usage/app_usage.dart';

//실제 7일 data 가져오기
Future<List<AppUsageInfo>> fetch7DaysUsage() async {
  try {
    DateTime endDate = DateTime.now();
    DateTime startDate = endDate.subtract(const Duration(days: 7));

    // app_usage 패키지를 통해 데이터 패치
    List<AppUsageInfo> infoList = await AppUsage().getAppUsage(startDate, endDate);

    // 사용 시간이 높은 순으로 정렬 (가장 많이 사용한 앱을 보여주기 위함)
    infoList.sort((a, b) => b.usage.inSeconds.compareTo(a.usage.inSeconds));

    return infoList;
  } catch (exception) {
    print('권한이 없거나 에러가 발생했습니다: $exception');
    return [];
  }
}

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
