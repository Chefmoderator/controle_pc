import 'package:flutter/material.dart';
import '../model/pc_model.dart';
import './PowerManagerPage.dart';
import './VolumeManagerPage.dart';
import './SystemInfoPage.dart';
import './ScreenBrightnessPage.dart';
import './LaunchProgramPage.dart';
import './FileManager.dart';
import './ProcessManagerPage.dart';
import './CameraManager.dart';

final List<String> commands = [
  "System info",
  "Power manager",
  "Volume manager",
  "Brightness manager",
  "Launch program",
  "Process manager",
  "File manager",
  "Camera manager",
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
      case "Volume manager":
        page = VolumeManagerPage(pc: pc);
        break;
      case "System info":
        page = SystemInfoPage(pc: pc);
        break;
      case "Brightness manager":
        page = BrightnessManagerPage(pc: pc);
        break;
      case "Launch program":
        page = ProgramManagerPage(pc: pc);
        break;
      case "File manager":
        page = FileManagerPage(pc: pc);
        break;
      case "Process manager":
        page = ProcessManagerPage(pc: pc);
        break;
      case "Camera manager":
        page = CameraPage(pc: pc);
        break;
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
