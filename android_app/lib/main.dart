import 'package:flutter/material.dart';
import 'styles/AppTheme.dart';
import 'pages/HomePage.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      
      theme: AppTheme.main, 

      home: const HomePage(),
    );
  }
}