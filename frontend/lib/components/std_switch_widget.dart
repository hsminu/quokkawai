import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'std_switch_model.dart';
export 'std_switch_model.dart';

class StdSwitchWidget extends StatefulWidget {
  const StdSwitchWidget({
    super.key,
    bool? label,
    String? variant,
    bool? active,
  })  : this.label = label ?? false,
        this.variant = variant ?? 'i_o_s',
        this.active = active ?? true;

  final bool label;
  final String variant;
  final bool active;

  @override
  State<StdSwitchWidget> createState() => _StdSwitchWidgetState();
}

class _StdSwitchWidgetState extends State<StdSwitchWidget> {
  late StdSwitchModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => StdSwitchModel());

    _model.switchValue = widget!.active == true ? true : false;
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.start,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        if (widget!.variant == 'i_o_s_26' ? false : true)
          Switch.adaptive(
            value: _model.switchValue!,
            onChanged: (newValue) async {
              safeSetState(() => _model.switchValue = newValue!);
            },
            activeTrackColor: FlutterFlowTheme.of(context).primary,
            inactiveTrackColor: FlutterFlowTheme.of(context).alternate,
            inactiveThumbColor: FlutterFlowTheme.of(context).primaryBackground,
          ),
        if (widget!.variant == 'i_o_s_26' ? true : false)
          Container(
            width: widget!.variant == 'i_o_s_26' ? 64.0 : 56.0,
            height: widget!.variant == 'i_o_s_26' ? 28.0 : 32.0,
            decoration: BoxDecoration(
              color: widget!.active == true
                  ? FlutterFlowTheme.of(context).primary
                  : FlutterFlowTheme.of(context).alternate,
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(valueOrDefault<double>(
                  widget!.variant == 'i_o_s_26' ? 9999.0 : 16.0,
                  0.0,
                )),
                topRight: Radius.circular(valueOrDefault<double>(
                  widget!.variant == 'i_o_s_26' ? 9999.0 : 16.0,
                  0.0,
                )),
                bottomLeft: Radius.circular(valueOrDefault<double>(
                  widget!.variant == 'i_o_s_26' ? 9999.0 : 16.0,
                  0.0,
                )),
                bottomRight: Radius.circular(valueOrDefault<double>(
                  widget!.variant == 'i_o_s_26' ? 9999.0 : 16.0,
                  0.0,
                )),
              ),
              shape: BoxShape.rectangle,
            ),
            child: Padding(
              padding: EdgeInsetsDirectional.fromSTEB(
                  valueOrDefault<double>(
                    widget!.variant == 'i_o_s_26' ? 2.0 : 3.0,
                    0.0,
                  ),
                  valueOrDefault<double>(
                    widget!.variant == 'i_o_s_26' ? 2.0 : 3.0,
                    0.0,
                  ),
                  valueOrDefault<double>(
                    widget!.variant == 'i_o_s_26' ? 2.0 : 3.0,
                    0.0,
                  ),
                  valueOrDefault<double>(
                    widget!.variant == 'i_o_s_26' ? 2.0 : 3.0,
                    0.0,
                  )),
              child: Container(
                child: Container(
                  width: widget!.variant == 'i_o_s_26' ? 39.0 : 26.0,
                  height: widget!.variant == 'i_o_s_26' ? 24.0 : 26.0,
                  decoration: BoxDecoration(
                    color: widget!.active == true
                        ? FlutterFlowTheme.of(context).onPrimary
                        : FlutterFlowTheme.of(context).primaryBackground,
                    borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(valueOrDefault<double>(
                        widget!.variant == 'i_o_s_26' ? 9999.0 : 13.0,
                        0.0,
                      )),
                      topRight: Radius.circular(valueOrDefault<double>(
                        widget!.variant == 'i_o_s_26' ? 9999.0 : 13.0,
                        0.0,
                      )),
                      bottomLeft: Radius.circular(valueOrDefault<double>(
                        widget!.variant == 'i_o_s_26' ? 9999.0 : 13.0,
                        0.0,
                      )),
                      bottomRight: Radius.circular(valueOrDefault<double>(
                        widget!.variant == 'i_o_s_26' ? 9999.0 : 13.0,
                        0.0,
                      )),
                    ),
                    shape: BoxShape.rectangle,
                  ),
                ),
              ),
            ),
          ),
        if (widget!.label ? true : false)
          Padding(
            padding: EdgeInsetsDirectional.fromSTEB(8.0, 0.0, 0.0, 0.0),
            child: Container(
              child: Text(
                valueOrDefault<String>(
                  widget!.label.toString(),
                  'false',
                ),
                style: FlutterFlowTheme.of(context).bodyMedium.override(
                      font: GoogleFonts.inter(
                        fontWeight:
                            FlutterFlowTheme.of(context).bodyMedium.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).bodyMedium.fontStyle,
                      ),
                      color: FlutterFlowTheme.of(context).primaryText,
                      letterSpacing: 0.0,
                      fontWeight:
                          FlutterFlowTheme.of(context).bodyMedium.fontWeight,
                      fontStyle:
                          FlutterFlowTheme.of(context).bodyMedium.fontStyle,
                      lineHeight: 1.5,
                    ),
              ),
            ),
          ),
      ],
    );
  }
}
