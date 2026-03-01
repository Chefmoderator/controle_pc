import 'package:flutter/material.dart';

class PowerStyle {
  static const EdgeInsets cardMargin =
      EdgeInsets.symmetric(horizontal: 16, vertical: 8);

  static final BorderRadius cardRadius = BorderRadius.circular(10);

  static const TextStyle programTextStyle = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.w600,
    color: Color.fromARGB(255, 65, 65, 65),
  );

  static const EdgeInsets cardPadding = EdgeInsets.all(12);

  static EdgeInsets listPadding(BuildContext context) {
    return EdgeInsets.only(
      top: MediaQuery.of(context).size.height * 0.1,
    );
  }
}
