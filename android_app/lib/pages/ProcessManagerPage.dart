import 'package:flutter/material.dart';
import '../model/pc_model.dart';
import '../services/api_client.dart';

final List<String> processCommands = [
  "List Processes",
  "Search Process",
  "Kill Process",
  "Start Process",
  "Restart Process",
  "Process Info",
];

class ProcessManagerPage extends StatefulWidget {
  final PC pc;

  const ProcessManagerPage({super.key, required this.pc});

  @override
  State<ProcessManagerPage> createState() => _ProcessManagerPageState();
}

class _ProcessManagerPageState extends State<ProcessManagerPage> {
  final Map<String, List<String>> responses = {}; 
  final Map<String, TextEditingController> pidControllers = {};
  final Map<String, TextEditingController> nameControllers = {};
  final Map<String, TextEditingController> pathControllers = {};

  static const int maxLogs = 20;
  final List<String> consoleLogs = []; 

  @override
  void initState() {
    super.initState();

    for (var cmd in processCommands) {
      responses[cmd] = [];
      pidControllers[cmd] = TextEditingController();
      nameControllers[cmd] = TextEditingController();
      pathControllers[cmd] = TextEditingController();
    }
  }

  void send(String cmd, {String? arg1, String? arg2}) async {
    responses[cmd]!.clear();
    setState(() {});

    String commandToSend = cmd;
    if (arg1 != null && arg1.isNotEmpty) commandToSend += " $arg1";
    if (arg2 != null && arg2.isNotEmpty) commandToSend += " $arg2";

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
      if (data is List) {
        for (var item in data) {
          responses[cmd]!.add(item.toString());
        }
      } else if (data is Map) {
        data.forEach((key, value) {
          responses[cmd]!.add("$key: $value");
        });
      } else {
        responses[cmd]!.add(data.toString());
      }

      consoleLogs.add("Response received for $cmd");
    } catch (e) {
      responses[cmd]!.add("Error: $e");
      consoleLogs.add("Error: $e");
    }

    if (consoleLogs.length > maxLogs) consoleLogs.removeAt(0);
    setState(() {});
  }

  Widget buildCommand(String cmd) {
    bool needsPid =
        ["Kill Process", "Restart Process", "Process Info"].contains(cmd);
    bool needsName = ["Search Process"].contains(cmd);
    bool needsPath = ["Start Process"].contains(cmd);

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.grey.shade900,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(cmd, style: const TextStyle(color: Colors.white, fontSize: 18)),
          const SizedBox(height: 8),
          if (needsPid)
            TextField(
              controller: pidControllers[cmd],
              keyboardType: TextInputType.number,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: "Enter PID",
                hintStyle: const TextStyle(color: Colors.grey),
                filled: true,
                fillColor: Colors.grey.shade800,
                border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: BorderSide.none),
              ),
            ),
          if (needsName)
            TextField(
              controller: nameControllers[cmd],
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: "Enter process name",
                hintStyle: const TextStyle(color: Colors.grey),
                filled: true,
                fillColor: Colors.grey.shade800,
                border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: BorderSide.none),
              ),
            ),
          if (needsPath)
            TextField(
              controller: pathControllers[cmd],
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: "Enter executable path",
                hintStyle: const TextStyle(color: Colors.grey),
                filled: true,
                fillColor: Colors.grey.shade800,
                border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: BorderSide.none),
              ),
            ),
          const SizedBox(height: 10),
          GestureDetector(
            onTap: () {
              String pid = pidControllers[cmd]?.text.trim() ?? "";
              String name = nameControllers[cmd]?.text.trim() ?? "";
              String path = pathControllers[cmd]?.text.trim() ?? "";

              switch (cmd) {
                case "List Processes":
                  send("List Processes");
                  break;
                case "Search Process":
                  send("Search Process", arg1: name);
                  break;
                case "Kill Process":
                  send("Kill Process", arg1: pid);
                  break;
                case "Start Process":
                  send("Start Process", arg1: path);
                  break;
                case "Restart Process":
                  send("Restart Process", arg1: pid);
                  break;
                case "Process Info":
                  send("Info Process", arg1: pid);
                  break;
              }

              pidControllers[cmd]?.clear();
              nameControllers[cmd]?.clear();
              pathControllers[cmd]?.clear();
            },
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration:
                  BoxDecoration(color: Colors.blue, borderRadius: BorderRadius.circular(8)),
              child: const Text(
                "EXECUTE",
                style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
              ),
            ),
          ),
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
                children: responses[cmd]!
                    .map((e) => Text(e, style: const TextStyle(color: Colors.greenAccent)))
                    .toList(),
              ),
            ),
          ],
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Process Manager")),
      body: Column(
        children: [
          Expanded(
            flex: 2,
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: processCommands.map(buildCommand).toList(),
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
                  return Text(consoleLogs[index],
                      style: const TextStyle(color: Colors.greenAccent));
                },
              ),
            ),
          ),
        ],
      ),
    );
  }
}