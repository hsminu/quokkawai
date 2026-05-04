import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'std_textfield_model.dart';
export 'std_textfield_model.dart';

class StdTextfieldWidget extends StatefulWidget {
  const StdTextfieldWidget({
    super.key,
    String? error,
    String? hint,
    String? value,
    bool? helper,
    bool? label,
    bool? leading_icon,
    bool? trailing_icon,
    String? variant,
  })  : this.error = error ?? 'true',
        this.hint = hint ?? 'SlotValue(\$hint)',
        this.value = value ?? 'SlotValue(\$value)',
        this.helper = helper ?? false,
        this.label = label ?? false,
        this.leading_icon = leading_icon ?? false,
        this.trailing_icon = trailing_icon ?? false,
        this.variant = variant ?? 'ghost';

  final String error;
  final String hint;
  final String value;
  final bool helper;
  final bool label;
  final bool leading_icon;
  final bool trailing_icon;
  final String variant;

  @override
  State<StdTextfieldWidget> createState() => _StdTextfieldWidgetState();
}

class _StdTextfieldWidgetState extends State<StdTextfieldWidget> {
  late StdTextfieldModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => StdTextfieldModel());

    _model.inputTextController ??= TextEditingController(
        text: valueOrDefault<String>(
      widget!.value,
      'SlotValue(\$value)',
    ));
    _model.inputFocusNode ??= FocusNode();
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          if (widget!.label ? true : false)
            Text(
              valueOrDefault<String>(
                widget!.label.toString(),
                'false',
              ),
              style: FlutterFlowTheme.of(context).labelMedium.override(
                    font: GoogleFonts.plusJakartaSans(
                      fontWeight:
                          FlutterFlowTheme.of(context).labelMedium.fontWeight,
                      fontStyle:
                          FlutterFlowTheme.of(context).labelMedium.fontStyle,
                    ),
                    color: widget!.error == 'true'
                        ? FlutterFlowTheme.of(context).error
                        : FlutterFlowTheme.of(context).primaryText,
                    letterSpacing: 0.0,
                    fontWeight:
                        FlutterFlowTheme.of(context).labelMedium.fontWeight,
                    fontStyle:
                        FlutterFlowTheme.of(context).labelMedium.fontStyle,
                    lineHeight: 1.3,
                  ),
            ),
          Container(
            decoration: BoxDecoration(
              color: widget!.variant == 'filled'
                  ? FlutterFlowTheme.of(context).secondaryBackground
                  : Colors.transparent,
              borderRadius: BorderRadius.circular(8.0),
              shape: BoxShape.rectangle,
              border: Border.all(
                color: () {
                  if (widget!.error == 'true') {
                    return FlutterFlowTheme.of(context).error;
                  } else if (widget!.variant == 'filled') {
                    return Colors.transparent;
                  } else if (widget!.variant == 'ghost') {
                    return Colors.transparent;
                  } else {
                    return FlutterFlowTheme.of(context).alternate;
                  }
                }(),
                width: () {
                  if (widget!.error == 'true') {
                    return 1.0;
                  } else if (widget!.variant == 'filled') {
                    return 1.0;
                  } else if (widget!.variant == 'ghost') {
                    return 0.0;
                  } else {
                    return 1.0;
                  }
                }(),
              ),
            ),
            child: Padding(
              padding: EdgeInsetsDirectional.fromSTEB(8.0, 8.0, 8.0, 8.0),
              child: Row(
                mainAxisSize: MainAxisSize.max,
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  if (widget!.leading_icon ? true : false) widget!.leading_icon,
                  Expanded(
                    flex: 1,
                    child: TextFormField(
                      controller: _model.inputTextController,
                      focusNode: _model.inputFocusNode,
                      obscureText: false,
                      decoration: InputDecoration(
                        isDense: true,
                        hintText: valueOrDefault<String>(
                          widget!.hint,
                          'SlotValue(\$hint)',
                        ),
                        hintStyle:
                            FlutterFlowTheme.of(context).bodyMedium.override(
                                  font: GoogleFonts.inter(
                                    fontWeight: FlutterFlowTheme.of(context)
                                        .bodyMedium
                                        .fontWeight,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .bodyMedium
                                        .fontStyle,
                                  ),
                                  color: FlutterFlowTheme.of(context).accent3,
                                  letterSpacing: 0.0,
                                  fontWeight: FlutterFlowTheme.of(context)
                                      .bodyMedium
                                      .fontWeight,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .bodyMedium
                                      .fontStyle,
                                  lineHeight: 1.5,
                                ),
                        enabledBorder: InputBorder.none,
                        focusedBorder: InputBorder.none,
                        errorBorder: InputBorder.none,
                        focusedErrorBorder: InputBorder.none,
                      ),
                      style: FlutterFlowTheme.of(context).bodyMedium.override(
                            font: GoogleFonts.inter(
                              fontWeight: FlutterFlowTheme.of(context)
                                  .bodyMedium
                                  .fontWeight,
                              fontStyle: FlutterFlowTheme.of(context)
                                  .bodyMedium
                                  .fontStyle,
                            ),
                            color: FlutterFlowTheme.of(context).primaryText,
                            letterSpacing: 0.0,
                            fontWeight: FlutterFlowTheme.of(context)
                                .bodyMedium
                                .fontWeight,
                            fontStyle: FlutterFlowTheme.of(context)
                                .bodyMedium
                                .fontStyle,
                            lineHeight: 1.5,
                          ),
                      validator: _model.inputTextControllerValidator
                          .asValidator(context),
                    ),
                  ),
                  if (widget!.trailing_icon ? true : false)
                    widget!.trailing_icon,
                ].divide(SizedBox(width: 8.0)),
              ),
            ),
          ),
          if (widget!.helper ? true : false)
            Text(
              valueOrDefault<String>(
                widget!.helper.toString(),
                'false',
              ),
              style: FlutterFlowTheme.of(context).bodySmall.override(
                    font: GoogleFonts.inter(
                      fontWeight:
                          FlutterFlowTheme.of(context).bodySmall.fontWeight,
                      fontStyle:
                          FlutterFlowTheme.of(context).bodySmall.fontStyle,
                    ),
                    color: widget!.error == 'true'
                        ? FlutterFlowTheme.of(context).error
                        : FlutterFlowTheme.of(context).secondaryText,
                    letterSpacing: 0.0,
                    fontWeight:
                        FlutterFlowTheme.of(context).bodySmall.fontWeight,
                    fontStyle: FlutterFlowTheme.of(context).bodySmall.fontStyle,
                    lineHeight: 1.4,
                  ),
            ),
        ].divide(SizedBox(height: 6.0)),
      ),
    );
  }
}
