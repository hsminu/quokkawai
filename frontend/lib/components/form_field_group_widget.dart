import '/components/std_textfield_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'form_field_group_model.dart';
export 'form_field_group_model.dart';

class FormFieldGroupWidget extends StatefulWidget {
  const FormFieldGroupWidget({
    super.key,
    String? hint,
    this.icon,
    String? label,
    this.trailing,
    double? value,
  })  : this.hint = hint ?? '이름을 입력해주세요',
        this.label = label ?? '이름',
        this.value = value ?? 42.0;

  final String hint;
  final Widget? icon;
  final String label;
  final Widget? trailing;
  final double value;

  @override
  State<FormFieldGroupWidget> createState() => _FormFieldGroupWidgetState();
}

class _FormFieldGroupWidgetState extends State<FormFieldGroupWidget> {
  late FormFieldGroupModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => FormFieldGroupModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.start,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          valueOrDefault<String>(
            widget!.label,
            '이름',
          ),
          style: FlutterFlowTheme.of(context).labelLarge.override(
                font: GoogleFonts.plusJakartaSans(
                  fontWeight:
                      FlutterFlowTheme.of(context).labelLarge.fontWeight,
                  fontStyle: FlutterFlowTheme.of(context).labelLarge.fontStyle,
                ),
                color: FlutterFlowTheme.of(context).primaryText,
                letterSpacing: 0.0,
                fontWeight: FlutterFlowTheme.of(context).labelLarge.fontWeight,
                fontStyle: FlutterFlowTheme.of(context).labelLarge.fontStyle,
                lineHeight: 1.3,
              ),
        ),
        Container(
          child: Container(
            decoration: BoxDecoration(
              color: FlutterFlowTheme.of(context).secondaryBackground,
              borderRadius: BorderRadius.circular(16.0),
              shape: BoxShape.rectangle,
              border: Border.all(
                color: FlutterFlowTheme.of(context).alternate,
                width: 1.0,
              ),
            ),
            child: Padding(
              padding: EdgeInsetsDirectional.fromSTEB(8.0, 16.0, 8.0, 16.0),
              child: Container(
                child: Row(
                  mainAxisSize: MainAxisSize.max,
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    widget!.icon!,
                    Expanded(
                      flex: 1,
                      child: wrapWithModel(
                        model: _model.stdTextfieldModel,
                        updateCallback: () => safeSetState(() {}),
                        child: StdTextfieldWidget(
                          error: 'true',
                          hint: valueOrDefault<String>(
                            widget!.hint,
                            '이름을 입력해주세요',
                          ),
                          value: valueOrDefault<String>(
                            widget!.value.toString(),
                            '42',
                          ),
                          helper: false,
                          label: false,
                          leading_icon: false,
                          trailing_icon: valueOrDefault<bool>(
                            widget!.trailing,
                            false,
                          ),
                          variant: 'ghost',
                        ),
                      ),
                    ),
                  ].divide(SizedBox(width: 16.0)),
                ),
              ),
            ),
          ),
        ),
      ].divide(SizedBox(height: 8.0)),
    );
  }
}
