import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import '../model/pc_model.dart';
import '../services/api_client.dart'; 

import './PowerManagerPage.dart';
import './VolumeManagerPage.dart';
import './SystemInfoPage.dart';
import './ScreenBrightnessPage.dart';
import './LaunchProgramPage.dart';
import './FileManager.dart';
import './ProcessManagerPage.dart';
import './CameraManager.dart';
import './Stream.dart';

final List<String> commands = [
  "System info",
  "Power manager",
  "Volume manager",
  "Brightness manager",
  "Launch program",
  "Process manager",
  "File manager",
  "Camera manager",
  "Stream"
];

class ProcessListPage extends StatefulWidget {
  final PC pc;

  const ProcessListPage({super.key, required this.pc});

  @override
  State<ProcessListPage> createState() => _ProcessListPageState();
}

class _ProcessListPageState extends State<ProcessListPage> {
  late PC pc;

  bool isOnline = false;
  DateTime? lastOnlineTime;

  Timer? autoCheckTimer;

  @override
  void initState() {
    super.initState();
    pc = widget.pc;

    checkPCstatus();
    startAutoCheck(); 
  }

  void startAutoCheck() {
    autoCheckTimer = Timer.periodic(
      const Duration(minutes: 30),
      (_) => checkPCstatus(),
    );
  }

  @override
  void dispose() {
    autoCheckTimer?.cancel();
    super.dispose();
  }

  Future<void> checkPCstatus() async {
    try {
      final response = await ApiClient.sendCommand(
        pcId: pc.pcId,
        token: pc.token,
        command: "system info",
      ).timeout(const Duration(seconds: 5));

      if (response["error"] != null) {

        setState(() => isOnline = false);
        return;
      }


      setState(() {
        isOnline = true;
        lastOnlineTime = DateTime.now();
      });

    } on TimeoutException {
      setState(() => isOnline = false);
    } on SocketException {
      setState(() => isOnline = false);
    } catch (e) {
      setState(() => isOnline = false);
    }
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
      case "Stream":
        page = StreamPage(pc: pc);
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

      body: Column(
        children: [

          Container(
            width: double.infinity,
            margin: const EdgeInsets.all(12),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.grey.shade900,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Column(
              children: [
                Text(
                  isOnline ? "PC ONLINE" : "PC OFFLINE",
                  style: TextStyle(
                    color: isOnline ? Colors.greenAccent : Colors.redAccent,
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),

                const SizedBox(height: 10),

                Text(
                  lastOnlineTime != null
                      ? "Last online: ${lastOnlineTime!.toLocal()}"
                      : "No data",
                  style: const TextStyle(color: Colors.white70),
                ),

                const SizedBox(height: 12),

                GestureDetector(
                  onTap: () => checkPCstatus(),
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16, vertical: 10),
                    decoration: BoxDecoration(
                      color: Colors.blue,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Text(
                      "CHECK NOW",
                      style:
                          TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                  ),
                )
              ],
            ),
          ),

          const Divider(height: 1),

          Expanded(
            child: ListView.builder(
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
          ),
        ],
      ),
    );
  }
}
