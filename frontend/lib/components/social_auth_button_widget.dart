import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'social_auth_button_model.dart';
export 'social_auth_button_model.dart';

class SocialAuthButtonWidget extends StatefulWidget {
  const SocialAuthButtonWidget({
    super.key,
    String? provider,
  }) : this.provider =
            provider ?? 'https://cdn.simpleicons.org/google/2d2926.svg';

  final String provider;

  @override
  State<SocialAuthButtonWidget> createState() => _SocialAuthButtonWidgetState();
}

class _SocialAuthButtonWidgetState extends State<SocialAuthButtonWidget> {
  late SocialAuthButtonModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => SocialAuthButtonModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 56.0,
      height: 56.0,
      decoration: BoxDecoration(
        color: FlutterFlowTheme.of(context).secondaryBackground,
        borderRadius: BorderRadius.circular(9999.0),
        shape: BoxShape.rectangle,
        border: Border.all(
          color: FlutterFlowTheme.of(context).alternate,
          width: 1.0,
        ),
      ),
      alignment: AlignmentDirectional(0.0, 0.0),
      child: SvgPicture.network(
        valueOrDefault<String>(
          widget!.provider,
          'https://cdn.simpleicons.org/google/2d2926.svg',
        ),
        width: 24.0,
        height: 24.0,
        fit: BoxFit.contain,
      ),
    );
  }
}
