import 'package:flutter/material.dart';
import '../model/pc_model.dart';
import '../services/api_client.dart';

final List<String> commands = [
  "Launch Program",
  "List Running",
  "Close Program",
];

class ProgramManagerPage extends StatefulWidget {
  final PC pc;

  const ProgramManagerPage({super.key, required this.pc});

  @override
  State<ProgramManagerPage> createState() => _ProgramManagerPageState();
}

class _ProgramManagerPageState extends State<ProgramManagerPage> {

  final List<String> consoleLogs = [];
  final Map<String, List<String>> responses = {};

  final TextEditingController programController = TextEditingController();
  final TextEditingController pidController = TextEditingController();

  List<dynamic> runningPrograms = [];

  static const int maxLogs = 20;

  @override
  void initState() {
    super.initState();

    for (var cmd in commands) {
      responses[cmd] = [];
    }
  }

  void send(String cmd, {String? arg}) async {

    String commandToSend = cmd;
    if (arg != null) {
      commandToSend = "$cmd $arg";
    }

    consoleLogs.add("> $commandToSend");
    if (consoleLogs.length > maxLogs) consoleLogs.removeAt(0);

    setState(() {});

    try {
      final response = await ApiClient.sendCommand(
        pcId: widget.pc.pcId,
        token: widget.pc.token,
        command: commandToSend,
      );

      final data = response["data"];

      if (cmd == "listrunning") {
        runningPrograms = data["programs"] ?? [];
        consoleLogs.add("Loaded ${runningPrograms.length} processes");
      } else {
        String pretty = data.toString();
        consoleLogs.add(pretty);
        responses[cmd]!.clear();
        responses[cmd]!.add(pretty);
      }
    } catch (e) {
      consoleLogs.add("Error: $e");
    }

    if (consoleLogs.length > maxLogs) consoleLogs.removeAt(0);
    setState(() {});
  }

  Widget buildCommand(String cmd) {

    bool isLaunch = cmd == "Launch Program";
    bool isClose = cmd == "Close Program";
    bool isList = cmd == "List Running";

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.grey.shade900,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        children: [

          GestureDetector(
            onTap: () {
              if (cmd == "List Running") send("listrunning");
            },
            child: Row(
              children: [
                Expanded(
                  child: Text(
                    cmd,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                    ),
                  ),
                ),
                const Icon(Icons.keyboard_arrow_down, color: Colors.white)
              ],
            ),
          ),

          if (isLaunch) ...[
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: programController,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: "program.exe",
                      hintStyle: const TextStyle(color: Colors.grey),
                      filled: true,
                      fillColor: Colors.grey.shade800,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: BorderSide.none,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                GestureDetector(
                  onTap: () {
                    if (programController.text.isEmpty) return;
                    send("launch", arg: programController.text);
                    programController.clear();
                  },
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    decoration: BoxDecoration(
                      color: Colors.blue,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Text(
                      "RUN",
                      style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                )
              ],
            )
          ],

          if (isClose) ...[
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: pidController,
                    keyboardType: TextInputType.number,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: "PID",
                      hintStyle: const TextStyle(color: Colors.grey),
                      filled: true,
                      fillColor: Colors.grey.shade800,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: BorderSide.none,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                GestureDetector(
                  onTap: () {
                    if (pidController.text.isEmpty) return;
                    send("close", arg: pidController.text);
                    pidController.clear();
                  },
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    decoration: BoxDecoration(
                      color: Colors.red,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Text(
                      "KILL",
                      style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                )
              ],
            )
          ],

          if (isList && runningPrograms.isNotEmpty) ...[
            const SizedBox(height: 10),
            Container(
              height: 250,
              decoration: BoxDecoration(
                color: Colors.grey.shade800,
                borderRadius: BorderRadius.circular(8),
              ),
              child: ListView.builder(
                itemCount: runningPrograms.length,
                itemBuilder: (context, index) {
                  final proc = runningPrograms[index];
                  final name = proc["name"] ?? "Unknown";
                  final pid = proc["pid"];
                  return ListTile(
                    dense: true,
                    title: Text(name, style: const TextStyle(color: Colors.white)),
                    trailing: Text("PID $pid", style: const TextStyle(color: Colors.greenAccent)),
                  );
                },
              ),
            )
          ],

          if (responses[cmd]!.isNotEmpty) ...[
            const SizedBox(height: 10),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: Colors.grey.shade800,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: responses[cmd]!.map((e) => Text(
                  e,
                  style: const TextStyle(color: Colors.greenAccent),
                )).toList(),
              ),
            )
          ]

        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.pc.name),
      ),
      body: Column(
        children: [
          Expanded(
            flex: 2,
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: commands.map(buildCommand).toList(),
            ),
          ),
          const Divider(height: 1),
          Expanded(
            flex: 1,
            child: Container(
              color: Colors.black,
              padding: const EdgeInsets.all(8),
              child: ListView.builder(
                itemCount: consoleLogs.length,
                itemBuilder: (context, index) {
                  return Text(
                    consoleLogs[index],
                    style: const TextStyle(color: Colors.greenAccent),
                  );
                },
              ),
            ),
          ),
        ],
      ),
    );
  }

}