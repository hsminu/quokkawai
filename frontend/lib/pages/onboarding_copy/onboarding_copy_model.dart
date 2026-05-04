import '/components/onboarding_feature_card_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'onboarding_copy_widget.dart' show OnboardingCopyWidget;
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

class OnboardingCopyModel extends FlutterFlowModel<OnboardingCopyWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for OnboardingFeatureCard.
  late OnboardingFeatureCardModel onboardingFeatureCardModel1;
  // Model for OnboardingFeatureCard.
  late OnboardingFeatureCardModel onboardingFeatureCardModel2;

  @override
  void initState(BuildContext context) {
    onboardingFeatureCardModel1 =
        createModel(context, () => OnboardingFeatureCardModel());
    onboardingFeatureCardModel2 =
        createModel(context, () => OnboardingFeatureCardModel());
  }

  @override
  void dispose() {
    onboardingFeatureCardModel1.dispose();
    onboardingFeatureCardModel2.dispose();
  }
}
