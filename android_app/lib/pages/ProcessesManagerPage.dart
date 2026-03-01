import 'package:flutter/material.dart';
import '../model/pc_model.dart';

class Processesmanager extends StatelessWidget {
  final PC pc;

  const Processesmanager({super.key, required this.pc});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Processes for ${pc.name}'),
        centerTitle: true,
      ),
      body: const Center(
        child: Text("Process Manager Page"),
      ),
    );
  }
}