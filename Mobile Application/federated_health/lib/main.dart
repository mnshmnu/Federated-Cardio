import 'package:federated_health/app/login/login_page.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Federated Health',
      theme: ThemeData(
        primarySwatch: Colors.red,
      ),
      home: SignInPage(),
    );
  }
}
