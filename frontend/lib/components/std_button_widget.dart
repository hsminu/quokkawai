import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:percent_indicator/percent_indicator.dart';
import 'package:provider/provider.dart';
import 'std_button_model.dart';
export 'std_button_model.dart';
import '/flutter_flow/flutter_flow_util.dart';

class StdButtonWidget extends StatefulWidget {
  const StdButtonWidget({
    super.key,
    String? content,
    Color? color,
    bool? icon,
    bool? icon_end,
    String? size,
    String? variant,
    bool? loading,
    bool? full_width,
  })  : this.content = content ?? '회원가입',
        this.color = color ?? Colors.blue,
        this.icon = icon ?? false,
        this.icon_end = icon_end ?? false,
        this.size = size ?? 'small',
        this.variant = variant ?? 'ghost',
        this.loading = loading ?? true,
        this.full_width = full_width ?? true;

  final String content;
  final Color color;
  final bool icon;
  final bool icon_end;
  final String size;
  final String variant;
  final bool loading;
  final bool full_width;

  @override
  State<StdButtonWidget> createState() => _StdButtonWidgetState();
}

class _StdButtonWidgetState extends State<StdButtonWidget> {
  late StdButtonModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => StdButtonModel());
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
          } else if (widget!.variant == 'outline') {
            return Colors.transparent;
          } else if (widget!.variant == 'secondary') {
            return FlutterFlowTheme.of(context).secondary;
          } else if (widget!.variant == 'primary') {
            return Color(0x00000000);
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
          Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(valueOrDefault<double>(
                  widget!.variant == 'primary' ? 20.0 : 0.0,
                  0.0,
                )),
                topRight: Radius.circular(valueOrDefault<double>(
                  widget!.variant == 'primary' ? 20.0 : 0.0,
                  0.0,
                )),
                bottomLeft: Radius.circular(valueOrDefault<double>(
                  widget!.variant == 'primary' ? 20.0 : 0.0,
                  0.0,
                )),
                bottomRight: Radius.circular(valueOrDefault<double>(
                  widget!.variant == 'primary' ? 20.0 : 0.0,
                  0.0,
                )),
              ),
              shape: BoxShape.rectangle,
            ),
            child: Padding(
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
                  // if (widget!.icon ? true : false) widget!.icon,
                  Text(
                    valueOrDefault<String>(
                      widget!.content,
                      '회원가입',
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
                            } else if (widget!.variant == 'outline') {
                              return FlutterFlowTheme.of(context).primaryText;
                            } else if (widget!.variant == 'secondary') {
                              return FlutterFlowTheme.of(context).onSecondary;
                            } else if (widget!.variant == 'primary') {
                              return Color(0x00000000);
                            } else {
                              return FlutterFlowTheme.of(context).primary;
                            }
                          }(),
                          letterSpacing: 0.0,
                          fontWeight: FlutterFlowTheme.of(context)
                              .labelMedium
                              .fontWeight,
                          fontStyle: FlutterFlowTheme.of(context)
                              .labelMedium
                              .fontStyle,
                          lineHeight: 1.3,
                        ),
                  ),
                  // if (widget!.icon_end ? true : false) widget!.icon_end,
                // ].divide(SizedBox(width: 8.0)),
                ],
              ),
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
                } else if (widget!.variant == 'outline') {
                  return FlutterFlowTheme.of(context).primaryText;
                } else if (widget!.variant == 'secondary') {
                  return FlutterFlowTheme.of(context).onSecondary;
                } else if (widget!.variant == 'primary') {
                  return Color(0x00000000);
                } else {
                  return FlutterFlowTheme.of(context).primary;
                }
              }(),
              backgroundColor: FlutterFlowTheme.of(context).alternate,
            ),
        ],
      ),
    );
  }
}
