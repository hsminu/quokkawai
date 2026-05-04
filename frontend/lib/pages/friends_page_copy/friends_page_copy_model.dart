import '/components/friend_card_widget.dart';
import '/components/std_button_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'friends_page_copy_widget.dart' show FriendsPageCopyWidget;
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

class FriendsPageCopyModel extends FlutterFlowModel<FriendsPageCopyWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for FriendCard.
  late FriendCardModel friendCardModel1;
  // Model for FriendCard.
  late FriendCardModel friendCardModel2;
  // Model for FriendCard.
  late FriendCardModel friendCardModel3;
  // Model for FriendCard.
  late FriendCardModel friendCardModel4;
  // Model for FriendCard.
  late FriendCardModel friendCardModel5;
  // Model for StdButton.
  late StdButtonModel stdButtonModel;

  @override
  void initState(BuildContext context) {
    friendCardModel1 = createModel(context, () => FriendCardModel());
    friendCardModel2 = createModel(context, () => FriendCardModel());
    friendCardModel3 = createModel(context, () => FriendCardModel());
    friendCardModel4 = createModel(context, () => FriendCardModel());
    friendCardModel5 = createModel(context, () => FriendCardModel());
    stdButtonModel = createModel(context, () => StdButtonModel());
  }

  @override
  void dispose() {
    friendCardModel1.dispose();
    friendCardModel2.dispose();
    friendCardModel3.dispose();
    friendCardModel4.dispose();
    friendCardModel5.dispose();
    stdButtonModel.dispose();
  }
}
