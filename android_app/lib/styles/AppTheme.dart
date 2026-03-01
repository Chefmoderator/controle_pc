import 'package:flutter/material.dart';

class AppTheme {
  static final ThemeData main = ThemeData(
    brightness: Brightness.dark,
    scaffoldBackgroundColor: Color.fromARGB(255, 49, 49, 49),
    appBarTheme: const AppBarTheme(
      backgroundColor: Color.fromARGB(255, 199, 196, 4),
      foregroundColor: Colors.white,
    ),
    cardTheme: CardTheme(
      color: Colors.grey[900],
      elevation: 0,
      margin: const EdgeInsets.all(8),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
    ),
    textTheme: const TextTheme(
      bodyMedium: TextStyle(color: Colors.white),
    ),
  );
}