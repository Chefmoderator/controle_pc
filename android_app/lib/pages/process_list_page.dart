import 'package:flutter/material.dart';
import '../model/pc_model.dart';
import './PowerManagerPage.dart';
import './ProcessesManagerPage.dart';

final List<String> commands = [
  "System info",
  "Power manager",
  "Volume manager",
  "Brightness manager",
  "Launch program",
  "Process manager",
  "File manager",
];

class ProcessListPage extends StatefulWidget {
  final PC pc;

  const ProcessListPage({super.key, required this.pc});

  @override
  State<ProcessListPage> createState() => _ProcessListPageState();
}

class _ProcessListPageState extends State<ProcessListPage> {
  late PC pc;

  @override
  void initState() {
    super.initState();
    pc = widget.pc;
  }

  void openPage(String command) {
    Widget? page;

    switch (command) {
      case "Power manager":
        page = PowerManagerPage(pc: pc);
        break;
      case "Process manager":
        page = Processesmanager(pc: pc);
    }

    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => page!),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Menu PC: ${pc.name}"),
        centerTitle: true,
      ),
      body: ListView.builder(
        itemCount: commands.length,
        itemBuilder: (context, index) {
          final command = commands[index];

          return ListTile(
            title: Text(command),
            trailing: const Icon(Icons.arrow_forward_ios),
            onTap: () => openPage(command),
          );
        },
      ),
    );
  }
}
