import '/components/app_usage_item_kr_widget.dart';
import '/components/stat_card_kr_widget.dart';
import '/components/std_button_widget.dart';
import '/flutter_flow/flutter_flow_charts.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:percent_indicator/percent_indicator.dart';
import 'package:provider/provider.dart';
import 'package:app_usage/app_usage.dart';
import 'package:app_settings/app_settings.dart';
import '7days_report_model.dart';
export '7days_report_model.dart';
import 'package:device_apps/device_apps.dart';
import 'dart:typed_data';


Map<String, Uint8List?> _appIcons = {}; // 패키지명 : 아이콘 데이터
Map<String, String> _appLabels = {};    // 패키지명 : 진짜 앱 이름

class Page7DaysReportCopyWidget extends StatefulWidget {
  const Page7DaysReportCopyWidget({super.key});

  static String routeName = 'Page7DaysReportCopy';
  static String routePath = '/page7DaysReportCopy';

  @override
  State<Page7DaysReportCopyWidget> createState() =>
      _Page7DaysReportCopyWidgetState();
}

class _Page7DaysReportCopyWidgetState extends State<Page7DaysReportCopyWidget>
    with WidgetsBindingObserver {
  late Page7DaysReportCopyModel _model;
  final scaffoldKey = GlobalKey<ScaffoldState>();

  List<AppUsageInfo> _usageData = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => Page7DaysReportCopyModel());
    WidgetsBinding.instance.addObserver(this);

    _fetchUsageData();
  }

  // 7day data 가져오기 + 권한
  Future<void> _fetchUsageData() async {
    try {
      DateTime endDate = DateTime.now();
      DateTime startDate = endDate.subtract(const Duration(days: 7));
      List<AppUsageInfo> infoList = await AppUsage().getAppUsage(startDate, endDate);
      infoList.sort((a, b) => b.usage.inSeconds.compareTo(a.usage.inSeconds));

      for (var info in infoList.take(10)) {
        Application? app = await DeviceApps.getApp(info.packageName, true);

        if (app is ApplicationWithIcon) {
          _appIcons[info.packageName] = app.icon; // 아이콘(바이트 데이터) 저장
          _appLabels[info.packageName] = app.appName; // 진짜 이름(카카오톡 등) 저장
        }
      }

      //새로고침
      setState(() {
        _usageData = infoList;
        _isLoading = false;
      });
    } catch (e) {
      print('권한 오류: $e');
      // 에러가 나면 무한 로딩에 빠지지 않게 처리하고, 설정 창으로 보내기
      setState(() => _isLoading = false);
      AppSettings.openAppSettings(type: AppSettingsType.security);
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _model.dispose();
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      // 권한 허용하고 다시 앱으로 돌아왔을 때, 로딩 띄우고 데이터 다시 가져오기
      setState(() => _isLoading = true);
      _fetchUsageData();
    }
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        FocusScope.of(context).unfocus();
        FocusManager.instance.primaryFocus?.unfocus();
      },
      child: Scaffold(
        key: scaffoldKey,
        backgroundColor: FlutterFlowTheme.of(context).primaryBackground,
        body: Stack(
          alignment: AlignmentDirectional(-1.0, -1.0),
          children: [
            SingleChildScrollView(
              primary: false,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Padding(
                    padding:
                    EdgeInsetsDirectional.fromSTEB(0.0, 0.0, 0.0, 100.0),
                    child: Container(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Container(
                            decoration: BoxDecoration(
                              color: FlutterFlowTheme.of(context)
                                  .primaryBackground,
                              shape: BoxShape.rectangle,
                            ),
                            child: Padding(
                              padding: EdgeInsetsDirectional.fromSTEB(
                                  24.0, 24.0, 24.0, 16.0),
                              child: Container(
                                child: Row(
                                  mainAxisSize: MainAxisSize.max,
                                  mainAxisAlignment:
                                  MainAxisAlignment.spaceBetween,
                                  crossAxisAlignment: CrossAxisAlignment.center,
                                  children: [
                                    Column(
                                      mainAxisSize: MainAxisSize.min,
                                      mainAxisAlignment:
                                      MainAxisAlignment.start,
                                      crossAxisAlignment:
                                      CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          '7일 분석',
                                          style: FlutterFlowTheme.of(context)
                                              .labelLarge
                                              .override(
                                            font:
                                            GoogleFonts.plusJakartaSans(
                                              fontWeight:
                                              FlutterFlowTheme.of(
                                                  context)
                                                  .labelLarge
                                                  .fontWeight,
                                              fontStyle:
                                              FlutterFlowTheme.of(
                                                  context)
                                                  .labelLarge
                                                  .fontStyle,
                                            ),
                                            color:
                                            FlutterFlowTheme.of(context)
                                                .primary,
                                            letterSpacing: 0.0,
                                            fontWeight:
                                            FlutterFlowTheme.of(context)
                                                .labelLarge
                                                .fontWeight,
                                            fontStyle:
                                            FlutterFlowTheme.of(context)
                                                .labelLarge
                                                .fontStyle,
                                            lineHeight: 1.3,
                                          ),
                                        ),
                                        Text(
                                          '사용 트렌드',
                                          style: FlutterFlowTheme.of(context)
                                              .headlineMedium
                                              .override(
                                            font:
                                            GoogleFonts.plusJakartaSans(
                                              fontWeight:
                                              FlutterFlowTheme.of(
                                                  context)
                                                  .headlineMedium
                                                  .fontWeight,
                                              fontStyle:
                                              FlutterFlowTheme.of(
                                                  context)
                                                  .headlineMedium
                                                  .fontStyle,
                                            ),
                                            color:
                                            FlutterFlowTheme.of(context)
                                                .primaryText,
                                            letterSpacing: 0.0,
                                            fontWeight:
                                            FlutterFlowTheme.of(context)
                                                .headlineMedium
                                                .fontWeight,
                                            fontStyle:
                                            FlutterFlowTheme.of(context)
                                                .headlineMedium
                                                .fontStyle,
                                            lineHeight: 1.25,
                                          ),
                                        ),
                                      ].divide(SizedBox(height: 4.0)),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ),
                          Padding(
                            padding: EdgeInsetsDirectional.fromSTEB(
                                24.0, 0.0, 24.0, 16.0),
                            child: Container(
                              child: Container(
                                decoration: BoxDecoration(
                                  color: FlutterFlowTheme.of(context)
                                      .secondaryBackground,
                                  borderRadius: BorderRadius.circular(24.0),
                                  shape: BoxShape.rectangle,
                                ),
                                child: Padding(
                                  padding: EdgeInsets.all(24.0),
                                  child: Container(
                                    child: Column(
                                      mainAxisSize: MainAxisSize.min,
                                      mainAxisAlignment:
                                      MainAxisAlignment.start,
                                      crossAxisAlignment:
                                      CrossAxisAlignment.stretch,
                                      children: [
                                        Column(
                                          mainAxisSize: MainAxisSize.min,
                                          mainAxisAlignment:
                                          MainAxisAlignment.start,
                                          crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                          children: [
                                            Text(
                                              '일평균 사용 시간',
                                              style:
                                              FlutterFlowTheme.of(context)
                                                  .bodySmall
                                                  .override(
                                                font: GoogleFonts.inter(
                                                  fontWeight:
                                                  FlutterFlowTheme.of(
                                                      context)
                                                      .bodySmall
                                                      .fontWeight,
                                                  fontStyle:
                                                  FlutterFlowTheme.of(
                                                      context)
                                                      .bodySmall
                                                      .fontStyle,
                                                ),
                                                color:
                                                FlutterFlowTheme.of(
                                                    context)
                                                    .secondaryText,
                                                letterSpacing: 0.0,
                                                fontWeight:
                                                FlutterFlowTheme.of(
                                                    context)
                                                    .bodySmall
                                                    .fontWeight,
                                                fontStyle:
                                                FlutterFlowTheme.of(
                                                    context)
                                                    .bodySmall
                                                    .fontStyle,
                                                lineHeight: 1.4,
                                              ),
                                            ),
                                            Row(
                                              mainAxisSize: MainAxisSize.max,
                                              mainAxisAlignment:
                                              MainAxisAlignment.start,
                                              crossAxisAlignment:
                                              CrossAxisAlignment.center,
                                              children: [
                                                Text(
                                                  '--test0시간 00분',
                                                  style: FlutterFlowTheme.of(
                                                      context)
                                                      .headlineLarge
                                                      .override(
                                                    font: GoogleFonts
                                                        .plusJakartaSans(
                                                      fontWeight:
                                                      FlutterFlowTheme.of(
                                                          context)
                                                          .headlineLarge
                                                          .fontWeight,
                                                      fontStyle:
                                                      FlutterFlowTheme.of(
                                                          context)
                                                          .headlineLarge
                                                          .fontStyle,
                                                    ),
                                                    color:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .primaryText,
                                                    letterSpacing: 0.0,
                                                    fontWeight:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .headlineLarge
                                                        .fontWeight,
                                                    fontStyle:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .headlineLarge
                                                        .fontStyle,
                                                    lineHeight: 1.2,
                                                  ),
                                                ),
                                                Text(
                                                  '--test+00% 지난주 대비',
                                                  style: FlutterFlowTheme.of(
                                                      context)
                                                      .labelSmall
                                                      .override(
                                                    font: GoogleFonts
                                                        .plusJakartaSans(
                                                      fontWeight:
                                                      FlutterFlowTheme.of(
                                                          context)
                                                          .labelSmall
                                                          .fontWeight,
                                                      fontStyle:
                                                      FlutterFlowTheme.of(
                                                          context)
                                                          .labelSmall
                                                          .fontStyle,
                                                    ),
                                                    color:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .onSurface,
                                                    letterSpacing: 0.0,
                                                    fontWeight:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .labelSmall
                                                        .fontWeight,
                                                    fontStyle:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .labelSmall
                                                        .fontStyle,
                                                    lineHeight: 1.2,
                                                  ),
                                                ),
                                              ].divide(SizedBox(width: 4.0)),
                                            ),
                                          ].divide(SizedBox(height: 4.0)),
                                        ),
                                        Container(
                                          height: 200.0,
                                          child: Container(
                                            height: 200.0,
                                            child: FlutterFlowBarChart(
                                              barData: [
                                                FFBarChartData(
                                                  yData: ([
                                                    4.2,
                                                    5.8,
                                                    3.5,
                                                    7.2,
                                                    4.8,
                                                    6.1,
                                                    5.7
                                                  ])!,
                                                  color: FlutterFlowTheme.of(
                                                      context)
                                                      .primary,
                                                )
                                              ],
                                              xLabels: ([
                                                '월',
                                                '화',
                                                '수',
                                                '목',
                                                '금',
                                                '토',
                                                '일'
                                              ])!,
                                              barWidth: 24.0,
                                              barBorderRadius:
                                              BorderRadius.circular(4.0),
                                              groupSpace: 12.0,
                                              alignment:
                                              BarChartAlignment.spaceEvenly,
                                              chartStylingInfo:
                                              ChartStylingInfo(
                                                backgroundColor:
                                                Colors.transparent,
                                                showGrid: true,
                                                showBorder: false,
                                              ),
                                              axisBounds: AxisBounds(
                                                minY: 0.0,
                                                maxX: 6.0,
                                                maxY: 8.64,
                                              ),
                                              xAxisLabelInfo: AxisLabelInfo(
                                                showLabels: true,
                                                labelTextStyle:
                                                FlutterFlowTheme.of(context)
                                                    .bodySmall
                                                    .override(
                                                  font:
                                                  GoogleFonts.inter(
                                                    fontWeight:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .bodySmall
                                                        .fontWeight,
                                                    fontStyle:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .bodySmall
                                                        .fontStyle,
                                                  ),
                                                  color: FlutterFlowTheme
                                                      .of(context)
                                                      .secondaryText,
                                                  fontSize: 10.0,
                                                  letterSpacing: 0.0,
                                                  fontWeight:
                                                  FlutterFlowTheme.of(
                                                      context)
                                                      .bodySmall
                                                      .fontWeight,
                                                  fontStyle:
                                                  FlutterFlowTheme.of(
                                                      context)
                                                      .bodySmall
                                                      .fontStyle,
                                                  lineHeight: 1.0,
                                                ),
                                                reservedSize: 20.0,
                                              ),
                                              yAxisLabelInfo: AxisLabelInfo(
                                                reservedSize: 0.0,
                                              ),
                                            ),
                                          ),
                                        ),
                                      ].divide(SizedBox(height: 24.0)),
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ),
                          Padding(
                            padding: EdgeInsetsDirectional.fromSTEB(
                                24.0, 0.0, 24.0, 16.0),
                            child: Row(
                              mainAxisSize: MainAxisSize.max,
                              mainAxisAlignment: MainAxisAlignment.start,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                Expanded(
                                  flex: 1,
                                  child: wrapWithModel(
                                    model: _model.statCardKrModel1,
                                    updateCallback: () => safeSetState(() {}),
                                    child: StatCardKrWidget(
                                      label: '잠금 해제',
                                      value: '--test0회',
                                    ),
                                  ),
                                ),
                                Expanded(
                                  flex: 1,
                                  child: wrapWithModel(
                                    model: _model.statCardKrModel2,
                                    updateCallback: () => safeSetState(() {}),
                                    child: StatCardKrWidget(
                                      label: '알림',
                                      value: '--test0개',
                                    ),
                                  ),
                                ),
                              ].divide(SizedBox(width: 16.0)),
                            ),
                          ),
                          Padding(
                            padding: EdgeInsetsDirectional.fromSTEB(
                                24.0, 0.0, 24.0, 24.0),
                            child: Container(
                              child: Container(
                                decoration: BoxDecoration(
                                  color:
                                  FlutterFlowTheme.of(context).secondary30,
                                  borderRadius: BorderRadius.circular(24.0),
                                  shape: BoxShape.rectangle,
                                  border: Border.all(
                                    color:
                                    FlutterFlowTheme.of(context).secondary,
                                    width: 1.0,
                                  ),
                                ),
                                child: Padding(
                                  padding: EdgeInsets.all(24.0),
                                  child: Container(
                                    child: Row(
                                      mainAxisSize: MainAxisSize.max,
                                      mainAxisAlignment:
                                      MainAxisAlignment.start,
                                      crossAxisAlignment:
                                      CrossAxisAlignment.center,
                                      children: [
                                        Expanded(
                                          flex: 1,
                                          child: Column(
                                            mainAxisSize: MainAxisSize.min,
                                            mainAxisAlignment:
                                            MainAxisAlignment.start,
                                            crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                            children: [
                                              Text(
                                                '밸런스 점수',
                                                style:
                                                FlutterFlowTheme.of(context)
                                                    .titleMedium
                                                    .override(
                                                  font: GoogleFonts
                                                      .plusJakartaSans(
                                                    fontWeight:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .titleMedium
                                                        .fontWeight,
                                                    fontStyle:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .titleMedium
                                                        .fontStyle,
                                                  ),
                                                  color: FlutterFlowTheme
                                                      .of(context)
                                                      .onSecondary,
                                                  letterSpacing: 0.0,
                                                  fontWeight:
                                                  FlutterFlowTheme.of(
                                                      context)
                                                      .titleMedium
                                                      .fontWeight,
                                                  fontStyle:
                                                  FlutterFlowTheme.of(
                                                      context)
                                                      .titleMedium
                                                      .fontStyle,
                                                  lineHeight: 1.4,
                                                ),
                                              ),
                                              Text(
                                                'test ai Text',
                                                maxLines: 3,
                                                style: FlutterFlowTheme.of(
                                                    context)
                                                    .bodySmall
                                                    .override(
                                                  font: GoogleFonts.inter(
                                                    fontWeight:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .bodySmall
                                                        .fontWeight,
                                                    fontStyle:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .bodySmall
                                                        .fontStyle,
                                                  ),
                                                  color:
                                                  FlutterFlowTheme.of(
                                                      context)
                                                      .onSecondary80,
                                                  letterSpacing: 0.0,
                                                  fontWeight:
                                                  FlutterFlowTheme.of(
                                                      context)
                                                      .bodySmall
                                                      .fontWeight,
                                                  fontStyle:
                                                  FlutterFlowTheme.of(
                                                      context)
                                                      .bodySmall
                                                      .fontStyle,
                                                  lineHeight: 1.4,
                                                ),
                                              ),
                                            ].divide(SizedBox(height: 8.0)),
                                          ),
                                        ),
                                        Container(
                                          width: 80.0,
                                          height: 80.0,
                                          child: Stack(
                                            alignment:
                                            AlignmentDirectional(0.0, 0.0),
                                            children: [
                                              CircularPercentIndicator(
                                                percent: 0.72,
                                                radius: 40.0,
                                                lineWidth: 8.0,
                                                animation: true,
                                                animateFromLastPercent: true,
                                                progressColor:
                                                FlutterFlowTheme.of(context)
                                                    .tertiary,
                                                backgroundColor:
                                                FlutterFlowTheme.of(context)
                                                    .surface50,
                                              ),
                                              Text(
                                                '72',
                                                style:
                                                FlutterFlowTheme.of(context)
                                                    .titleLarge
                                                    .override(
                                                  font: GoogleFonts
                                                      .plusJakartaSans(
                                                    fontWeight:
                                                    FontWeight.w800,
                                                    fontStyle:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .titleLarge
                                                        .fontStyle,
                                                  ),
                                                  color: FlutterFlowTheme
                                                      .of(context)
                                                      .onSecondary,
                                                  letterSpacing: 0.0,
                                                  fontWeight:
                                                  FontWeight.w800,
                                                  fontStyle:
                                                  FlutterFlowTheme.of(
                                                      context)
                                                      .titleLarge
                                                      .fontStyle,
                                                  lineHeight: 1.3,
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                      ].divide(SizedBox(width: 24.0)),
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ),
                          Padding(
                            padding: EdgeInsetsDirectional.fromSTEB(
                                24.0, 0.0, 24.0, 32.0),
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              mainAxisAlignment: MainAxisAlignment.start,
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                Padding(
                                  padding: EdgeInsetsDirectional.fromSTEB(
                                      0.0, 0.0, 0.0, 16.0),
                                  child: Row(
                                    mainAxisSize: MainAxisSize.max,
                                    mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                    crossAxisAlignment:
                                    CrossAxisAlignment.center,
                                    children: [
                                      Text(
                                        '가장 많이 사용한 앱',
                                        style: FlutterFlowTheme.of(context)
                                            .titleMedium
                                            .override(
                                          font: GoogleFonts.plusJakartaSans(
                                            fontWeight:
                                            FlutterFlowTheme.of(context)
                                                .titleMedium
                                                .fontWeight,
                                            fontStyle:
                                            FlutterFlowTheme.of(context)
                                                .titleMedium
                                                .fontStyle,
                                          ),
                                          color:
                                          FlutterFlowTheme.of(context)
                                              .primaryText,
                                          letterSpacing: 0.0,
                                          fontWeight:
                                          FlutterFlowTheme.of(context)
                                              .titleMedium
                                              .fontWeight,
                                          fontStyle:
                                          FlutterFlowTheme.of(context)
                                              .titleMedium
                                              .fontStyle,
                                          lineHeight: 1.4,
                                        ),
                                      ),
                                      Text(
                                        '모두 보기',
                                        style: FlutterFlowTheme.of(context)
                                            .labelLarge
                                            .override(
                                          font: GoogleFonts.plusJakartaSans(
                                            fontWeight:
                                            FlutterFlowTheme.of(context)
                                                .labelLarge
                                                .fontWeight,
                                            fontStyle:
                                            FlutterFlowTheme.of(context)
                                                .labelLarge
                                                .fontStyle,
                                          ),
                                          color:
                                          FlutterFlowTheme.of(context)
                                              .primary,
                                          letterSpacing: 0.0,
                                          fontWeight:
                                          FlutterFlowTheme.of(context)
                                              .labelLarge
                                              .fontWeight,
                                          fontStyle:
                                          FlutterFlowTheme.of(context)
                                              .labelLarge
                                              .fontStyle,
                                          lineHeight: 1.3,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                                _isLoading
                                    ? const Padding(
                                  padding: EdgeInsets.all(24.0),
                                  child: Center(
                                      child: CircularProgressIndicator()),
                                )
                                    : _usageData.isEmpty
                                    ? const Padding(
                                  padding: EdgeInsets.all(24.0),
                                  child: Center(
                                      child: Text(
                                          '앱 사용 기록이 없거나 접근 권한이 필요합니다.')),
                                )
                                    : Column(
                                  children:
                                  _usageData.take(4).map<Widget>((info) {
                                    int hours = info.usage.inHours;
                                    int minutes = info.usage.inMinutes
                                        .remainder(60);
                                    String timeString = hours > 0
                                        ? '$hours시간 $minutes분'
                                        : '$minutes분';

                                    return AppUsageItemKrWidget(
                                      app_name: _appLabels[info.packageName] ?? info.appName,
                                      category: '분석 중...',
                                      time: timeString,
                                      iconBytes: _appIcons[info.packageName],
                                    );
                                  }).toList(),
                                ),
                              ],
                            ),
                          ),
                          Padding(
                            padding: EdgeInsetsDirectional.fromSTEB(
                                24.0, 0.0, 24.0, 24.0),
                            child: Container(
                              child: Container(
                                decoration: BoxDecoration(
                                  color: FlutterFlowTheme.of(context).accent15,
                                  borderRadius: BorderRadius.circular(24.0),
                                  shape: BoxShape.rectangle,
                                  border: Border.all(
                                    color:
                                    FlutterFlowTheme.of(context).accent40,
                                    width: 1.0,
                                  ),
                                ),
                                child: Padding(
                                  padding: EdgeInsets.all(24.0),
                                  child: Container(
                                    child: Column(
                                      mainAxisSize: MainAxisSize.min,
                                      mainAxisAlignment:
                                      MainAxisAlignment.start,
                                      crossAxisAlignment:
                                      CrossAxisAlignment.stretch,
                                      children: [
                                        Row(
                                          mainAxisSize: MainAxisSize.max,
                                          mainAxisAlignment:
                                          MainAxisAlignment.start,
                                          crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                          children: [
                                            ClipRRect(
                                              borderRadius:
                                              BorderRadius.circular(9999.0),
                                              child: Container(
                                                width: 56.0,
                                                height: 56.0,
                                                decoration: BoxDecoration(
                                                  color: FlutterFlowTheme.of(
                                                      context)
                                                      .secondaryBackground,
                                                  borderRadius:
                                                  BorderRadius.circular(
                                                      9999.0),
                                                  shape: BoxShape.rectangle,
                                                ),
                                                child: Image.asset(
                                                  'assets/images/QCZJBMt7kezUUZ32UHZE',
                                                  fit: BoxFit.cover,
                                                  alignment:
                                                  Alignment(0.0, 0.0),
                                                ),
                                              ),
                                            ),
                                            Expanded(
                                              flex: 1,
                                              child: Column(
                                                mainAxisSize: MainAxisSize.min,
                                                mainAxisAlignment:
                                                MainAxisAlignment.start,
                                                crossAxisAlignment:
                                                CrossAxisAlignment.start,
                                                children: [
                                                  Text(
                                                    '쿼카코치의 조언',
                                                    style: FlutterFlowTheme.of(
                                                        context)
                                                        .titleMedium
                                                        .override(
                                                      font: GoogleFonts
                                                          .plusJakartaSans(
                                                        fontWeight:
                                                        FlutterFlowTheme.of(
                                                            context)
                                                            .titleMedium
                                                            .fontWeight,
                                                        fontStyle:
                                                        FlutterFlowTheme.of(
                                                            context)
                                                            .titleMedium
                                                            .fontStyle,
                                                      ),
                                                      color: FlutterFlowTheme
                                                          .of(context)
                                                          .primaryText,
                                                      letterSpacing: 0.0,
                                                      fontWeight:
                                                      FlutterFlowTheme.of(
                                                          context)
                                                          .titleMedium
                                                          .fontWeight,
                                                      fontStyle:
                                                      FlutterFlowTheme.of(
                                                          context)
                                                          .titleMedium
                                                          .fontStyle,
                                                      lineHeight: 1.4,
                                                    ),
                                                  ),
                                                  Text(
                                                    '이번 목요일에 평소보다 유튜브를 45% 더 많이 사용하셨어요. 주중 스트리밍 제한 설정을 고려해보세요.',
                                                    style: FlutterFlowTheme.of(
                                                        context)
                                                        .bodyMedium
                                                        .override(
                                                      font:
                                                      GoogleFonts.inter(
                                                        fontWeight:
                                                        FlutterFlowTheme.of(
                                                            context)
                                                            .bodyMedium
                                                            .fontWeight,
                                                        fontStyle:
                                                        FlutterFlowTheme.of(
                                                            context)
                                                            .bodyMedium
                                                            .fontStyle,
                                                      ),
                                                      color: FlutterFlowTheme
                                                          .of(context)
                                                          .primaryText,
                                                      letterSpacing: 0.0,
                                                      fontWeight:
                                                      FlutterFlowTheme.of(
                                                          context)
                                                          .bodyMedium
                                                          .fontWeight,
                                                      fontStyle:
                                                      FlutterFlowTheme.of(
                                                          context)
                                                          .bodyMedium
                                                          .fontStyle,
                                                      lineHeight: 1.4,
                                                    ),
                                                  ),
                                                ].divide(SizedBox(height: 4.0)),
                                              ),
                                            ),
                                          ].divide(SizedBox(width: 16.0)),
                                        ),
                                        wrapWithModel(
                                          model: _model.stdButtonModel,
                                          updateCallback: () =>
                                              safeSetState(() {}),
                                          child: StdButtonWidget(
                                            content: 'AI 코칭 리포트 확인하기',
                                            color: FlutterFlowTheme.of(context)
                                                .primary,
                                            icon: false,
                                            icon_end: false,
                                            size: 'small',
                                            variant: 'primary',
                                            loading: true,
                                            full_width: true,
                                          ),
                                        ),
                                      ].divide(SizedBox(height: 16.0)),
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
            Align(
              alignment: AlignmentDirectional(0.0, 1.0),
              child: ClipRRect(
                borderRadius: BorderRadius.only(),
                child: BackdropFilter(
                  filter: ImageFilter.blur(
                    sigmaX: 12.0,
                    sigmaY: 12.0,
                  ),
                  child: Container(
                    height: 100.0,
                    decoration: BoxDecoration(
                      color: FlutterFlowTheme.of(context).secondaryBackground,
                      shape: BoxShape.rectangle,
                      border: Border.all(
                        color: FlutterFlowTheme.of(context).alternate,
                        width: 1.0,
                      ),
                    ),
                    child: Padding(
                      padding:
                      EdgeInsetsDirectional.fromSTEB(0.0, 0.0, 0.0, 16.0),
                      child: Container(
                        child: Container(
                          height: 100.0,
                          child: Stack(
                            alignment: AlignmentDirectional(0.0, 0.0),
                            children: [
                              Align(
                                alignment: AlignmentDirectional(0.0, 1.0),
                                child: Padding(
                                  padding: EdgeInsets.all(12.0),
                                  child: Container(
                                    alignment: AlignmentDirectional(0.0, 1.0),
                                    child: Container(
                                      height: 70.0,
                                      decoration: BoxDecoration(
                                        color: FlutterFlowTheme.of(context)
                                            .secondaryBackground,
                                        shape: BoxShape.rectangle,
                                      ),
                                      child: Column(
                                        mainAxisSize: MainAxisSize.min,
                                        crossAxisAlignment:
                                        CrossAxisAlignment.stretch,
                                        children: [
                                          Container(
                                            height: 1.0,
                                            decoration: BoxDecoration(
                                              color:
                                              FlutterFlowTheme.of(context)
                                                  .alternate,
                                              shape: BoxShape.rectangle,
                                            ),
                                          ),
                                          Padding(
                                            padding:
                                            EdgeInsetsDirectional.fromSTEB(
                                                16.0, 0.0, 16.0, 0.0),
                                            child: Container(
                                              child: Container(
                                                height: 69.0,
                                                alignment: AlignmentDirectional(
                                                    0.0, 0.0),
                                                child: Row(
                                                  mainAxisSize:
                                                  MainAxisSize.max,
                                                  mainAxisAlignment:
                                                  MainAxisAlignment
                                                      .spaceAround,
                                                  crossAxisAlignment:
                                                  CrossAxisAlignment.center,
                                                  children: [
                                                    Column(
                                                      mainAxisSize:
                                                      MainAxisSize.min,
                                                      mainAxisAlignment:
                                                      MainAxisAlignment
                                                          .start,
                                                      crossAxisAlignment:
                                                      CrossAxisAlignment
                                                          .center,
                                                      children: [
                                                        Icon(
                                                          Icons
                                                              .bar_chart_rounded,
                                                          color: FlutterFlowTheme
                                                              .of(context)
                                                              .secondaryText,
                                                          size: 26.0,
                                                        ),
                                                        Text(
                                                          '통계',
                                                          style: FlutterFlowTheme
                                                              .of(context)
                                                              .labelSmall
                                                              .override(
                                                            font: GoogleFonts
                                                                .plusJakartaSans(
                                                              fontWeight: FlutterFlowTheme.of(
                                                                  context)
                                                                  .labelSmall
                                                                  .fontWeight,
                                                              fontStyle: FlutterFlowTheme.of(
                                                                  context)
                                                                  .labelSmall
                                                                  .fontStyle,
                                                            ),
                                                            color: FlutterFlowTheme.of(
                                                                context)
                                                                .secondaryText,
                                                            letterSpacing:
                                                            0.0,
                                                            fontWeight: FlutterFlowTheme.of(
                                                                context)
                                                                .labelSmall
                                                                .fontWeight,
                                                            fontStyle: FlutterFlowTheme.of(
                                                                context)
                                                                .labelSmall
                                                                .fontStyle,
                                                            lineHeight: 1.2,
                                                          ),
                                                        ),
                                                      ].divide(SizedBox(
                                                          height: 4.0)),
                                                    ),
                                                    Column(
                                                      mainAxisSize:
                                                      MainAxisSize.min,
                                                      mainAxisAlignment:
                                                      MainAxisAlignment
                                                          .start,
                                                      crossAxisAlignment:
                                                      CrossAxisAlignment
                                                          .center,
                                                      children: [
                                                        Icon(
                                                          Icons.people_rounded,
                                                          color: FlutterFlowTheme
                                                              .of(context)
                                                              .secondaryText,
                                                          size: 26.0,
                                                        ),
                                                        Text(
                                                          '친구',
                                                          style: FlutterFlowTheme
                                                              .of(context)
                                                              .labelSmall
                                                              .override(
                                                            font: GoogleFonts
                                                                .plusJakartaSans(
                                                              fontWeight: FlutterFlowTheme.of(
                                                                  context)
                                                                  .labelSmall
                                                                  .fontWeight,
                                                              fontStyle: FlutterFlowTheme.of(
                                                                  context)
                                                                  .labelSmall
                                                                  .fontStyle,
                                                            ),
                                                            color: FlutterFlowTheme.of(
                                                                context)
                                                                .secondaryText,
                                                            letterSpacing:
                                                            0.0,
                                                            fontWeight: FlutterFlowTheme.of(
                                                                context)
                                                                .labelSmall
                                                                .fontWeight,
                                                            fontStyle: FlutterFlowTheme.of(
                                                                context)
                                                                .labelSmall
                                                                .fontStyle,
                                                            lineHeight: 1.2,
                                                          ),
                                                        ),
                                                      ].divide(SizedBox(
                                                          height: 4.0)),
                                                    ),
                                                    Container(
                                                      width: 60.0,
                                                    ),
                                                    Column(
                                                      mainAxisSize:
                                                      MainAxisSize.min,
                                                      mainAxisAlignment:
                                                      MainAxisAlignment
                                                          .start,
                                                      crossAxisAlignment:
                                                      CrossAxisAlignment
                                                          .center,
                                                      children: [
                                                        Icon(
                                                          Icons
                                                              .settings_rounded,
                                                          color: FlutterFlowTheme
                                                              .of(context)
                                                              .secondaryText,
                                                          size: 26.0,
                                                        ),
                                                        Text(
                                                          '설정',
                                                          style: FlutterFlowTheme
                                                              .of(context)
                                                              .labelSmall
                                                              .override(
                                                            font: GoogleFonts
                                                                .plusJakartaSans(
                                                              fontWeight: FlutterFlowTheme.of(
                                                                  context)
                                                                  .labelSmall
                                                                  .fontWeight,
                                                              fontStyle: FlutterFlowTheme.of(
                                                                  context)
                                                                  .labelSmall
                                                                  .fontStyle,
                                                            ),
                                                            color: FlutterFlowTheme.of(
                                                                context)
                                                                .secondaryText,
                                                            letterSpacing:
                                                            0.0,
                                                            fontWeight: FlutterFlowTheme.of(
                                                                context)
                                                                .labelSmall
                                                                .fontWeight,
                                                            fontStyle: FlutterFlowTheme.of(
                                                                context)
                                                                .labelSmall
                                                                .fontStyle,
                                                            lineHeight: 1.2,
                                                          ),
                                                        ),
                                                      ].divide(SizedBox(
                                                          height: 4.0)),
                                                    ),
                                                    Column(
                                                      mainAxisSize:
                                                      MainAxisSize.min,
                                                      mainAxisAlignment:
                                                      MainAxisAlignment
                                                          .start,
                                                      crossAxisAlignment:
                                                      CrossAxisAlignment
                                                          .center,
                                                      children: [
                                                        Icon(
                                                          Icons.person_rounded,
                                                          color: FlutterFlowTheme
                                                              .of(context)
                                                              .secondaryText,
                                                          size: 26.0,
                                                        ),
                                                        Text(
                                                          '마이',
                                                          style: FlutterFlowTheme
                                                              .of(context)
                                                              .labelSmall
                                                              .override(
                                                            font: GoogleFonts
                                                                .plusJakartaSans(
                                                              fontWeight: FlutterFlowTheme.of(
                                                                  context)
                                                                  .labelSmall
                                                                  .fontWeight,
                                                              fontStyle: FlutterFlowTheme.of(
                                                                  context)
                                                                  .labelSmall
                                                                  .fontStyle,
                                                            ),
                                                            color: FlutterFlowTheme.of(
                                                                context)
                                                                .secondaryText,
                                                            letterSpacing:
                                                            0.0,
                                                            fontWeight: FlutterFlowTheme.of(
                                                                context)
                                                                .labelSmall
                                                                .fontWeight,
                                                            fontStyle: FlutterFlowTheme.of(
                                                                context)
                                                                .labelSmall
                                                                .fontStyle,
                                                            lineHeight: 1.2,
                                                          ),
                                                        ),
                                                      ].divide(SizedBox(
                                                          height: 4.0)),
                                                    ),
                                                  ],
                                                ),
                                              ),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              Align(
                                alignment: AlignmentDirectional(0.0, -1.0),
                                child: Padding(
                                  padding: EdgeInsetsDirectional.fromSTEB(
                                      0.0, 0.0, 0.0, 10.0),
                                  child: Container(
                                    alignment: AlignmentDirectional(0.0, -1.0),
                                    child: Container(
                                      width: 64.0,
                                      height: 64.0,
                                      decoration: BoxDecoration(
                                        color: FlutterFlowTheme.of(context)
                                            .primary,
                                        borderRadius:
                                        BorderRadius.circular(9999.0),
                                        shape: BoxShape.rectangle,
                                      ),
                                      child: Padding(
                                        padding: EdgeInsetsDirectional.fromSTEB(
                                            0.0, 12.0, 0.0, 8.0),
                                        child: Container(
                                          child: Column(
                                            mainAxisSize: MainAxisSize.min,
                                            mainAxisAlignment:
                                            MainAxisAlignment.start,
                                            crossAxisAlignment:
                                            CrossAxisAlignment.center,
                                            children: [
                                              Icon(
                                                Icons.home_rounded,
                                                color:
                                                FlutterFlowTheme.of(context)
                                                    .onPrimary,
                                                size: 28.0,
                                              ),
                                              Text(
                                                '홈',
                                                style:
                                                FlutterFlowTheme.of(context)
                                                    .labelSmall
                                                    .override(
                                                  font: GoogleFonts
                                                      .plusJakartaSans(
                                                    fontWeight:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .labelSmall
                                                        .fontWeight,
                                                    fontStyle:
                                                    FlutterFlowTheme.of(
                                                        context)
                                                        .labelSmall
                                                        .fontStyle,
                                                  ),
                                                  color: FlutterFlowTheme
                                                      .of(context)
                                                      .onPrimary,
                                                  letterSpacing: 0.0,
                                                  fontWeight:
                                                  FlutterFlowTheme.of(
                                                      context)
                                                      .labelSmall
                                                      .fontWeight,
                                                  fontStyle:
                                                  FlutterFlowTheme.of(
                                                      context)
                                                      .labelSmall
                                                      .fontStyle,
                                                  lineHeight: 1.2,
                                                ),
                                              ),
                                            ].divide(SizedBox(height: 2.0)),
                                          ),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}