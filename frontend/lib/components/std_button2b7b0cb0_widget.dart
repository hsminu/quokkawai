import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:percent_indicator/percent_indicator.dart';
import 'package:provider/provider.dart';
import 'std_button2b7b0cb0_model.dart';
export 'std_button2b7b0cb0_model.dart';

class StdButton2b7b0cb0Widget extends StatefulWidget {
  const StdButton2b7b0cb0Widget({
    super.key,
    String? content,
    this.icon_end,
    String? icon,
    String? size,
    String? variant,
    bool? loading,
  })  : this.content = content ?? '목표 재설정',
        this.icon = icon ?? 'refresh_rounded',
        this.size = size ?? 'small',
        this.variant = variant ?? 'outline',
        this.loading = loading ?? true;

  final String content;
  final Widget? icon_end;
  final String icon;
  final String size;
  final String variant;
  final bool loading;

  @override
  State<StdButton2b7b0cb0Widget> createState() =>
      _StdButton2b7b0cb0WidgetState();
}

class _StdButton2b7b0cb0WidgetState extends State<StdButton2b7b0cb0Widget> {
  late StdButton2b7b0cb0Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => StdButton2b7b0cb0Model());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: () {
          if (widget!.variant == 'destructive') {
            return Color(0x00000000);
          } else if (widget!.variant == 'ghost') {
            return Color(0x00000000);
          } else if (widget!.variant == 'secondary') {
            return FlutterFlowTheme.of(context).secondary;
          } else {
            return Colors.transparent;
          }
        }(),
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(valueOrDefault<double>(
            widget!.size == 'large' ? 0.0 : 8.0,
            0.0,
          )),
          topRight: Radius.circular(valueOrDefault<double>(
            widget!.size == 'large' ? 0.0 : 8.0,
            0.0,
          )),
          bottomLeft: Radius.circular(valueOrDefault<double>(
            widget!.size == 'large' ? 0.0 : 8.0,
            0.0,
          )),
          bottomRight: Radius.circular(valueOrDefault<double>(
            widget!.size == 'large' ? 0.0 : 8.0,
            0.0,
          )),
        ),
        shape: BoxShape.rectangle,
      ),
      child: Stack(
        alignment: AlignmentDirectional(0.0, 0.0),
        children: [
          Padding(
            padding: EdgeInsetsDirectional.fromSTEB(
                valueOrDefault<double>(
                  widget!.size == 'large' ? 0.0 : 16.0,
                  0.0,
                ),
                valueOrDefault<double>(
                  widget!.size == 'large' ? 0.0 : 4.0,
                  0.0,
                ),
                valueOrDefault<double>(
                  widget!.size == 'large' ? 0.0 : 16.0,
                  0.0,
                ),
                valueOrDefault<double>(
                  widget!.size == 'large' ? 0.0 : 4.0,
                  0.0,
                )),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                if (widget!.icon == 'true' ? true : false) widget!.icon,
                Text(
                  valueOrDefault<String>(
                    widget!.content,
                    '목표 재설정',
                  ),
                  style: FlutterFlowTheme.of(context).labelMedium.override(
                        font: GoogleFonts.plusJakartaSans(
                          fontWeight: FlutterFlowTheme.of(context)
                              .labelMedium
                              .fontWeight,
                          fontStyle: FlutterFlowTheme.of(context)
                              .labelMedium
                              .fontStyle,
                        ),
                        color: () {
                          if (widget!.variant == 'destructive') {
                            return Color(0x00000000);
                          } else if (widget!.variant == 'ghost') {
                            return Color(0x00000000);
                          } else if (widget!.variant == 'secondary') {
                            return FlutterFlowTheme.of(context).onSecondary;
                          } else {
                            return FlutterFlowTheme.of(context).primaryText;
                          }
                        }(),
                        letterSpacing: 0.0,
                        fontWeight:
                            FlutterFlowTheme.of(context).labelMedium.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).labelMedium.fontStyle,
                        lineHeight: 1.3,
                      ),
                ),
                if (widget!.icon_end == true ? true : false) widget!.icon_end!,
              ].divide(SizedBox(width: 8.0)),
            ),
          ),
          if (widget!.loading == true ? true : false)
            CircularPercentIndicator(
              percent: 0.0,
              radius: 7.0,
              lineWidth: 2.0,
              animation: true,
              animateFromLastPercent: true,
              progressColor: () {
                if (widget!.variant == 'destructive') {
                  return Color(0x00000000);
                } else if (widget!.variant == 'ghost') {
                  return Color(0x00000000);
                } else if (widget!.variant == 'secondary') {
                  return FlutterFlowTheme.of(context).onSecondary;
                } else {
                  return FlutterFlowTheme.of(context).primaryText;
                }
              }(),
              backgroundColor: FlutterFlowTheme.of(context).alternate,
            ),
        ],
      ),
    );
  }
}
