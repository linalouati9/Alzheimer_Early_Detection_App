import 'package:flutter/material.dart';
import 'main_page.dart';

void main() {
  runApp(CookieTestApp());
}

class CookieTestApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cookie Test App',
      theme: ThemeData(primarySwatch: Colors.cyan),
      debugShowCheckedModeBanner: false,
      debugShowMaterialGrid: false,
      home: MainPage(),
    );
  }
}
