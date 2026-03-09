import 'package:flutter/material.dart';
import '../model/pc_model.dart';
import '../services/api_client.dart';

final List<String> fileCommands = [
  "Search File",
  "Inspect Folder",
  "Create Folder",
  "Create File",
  "Delete Item",
  "Move Item",
  "Create Zip",
  "Read File",
];

class FileManagerPage extends StatefulWidget {
  final PC pc;

  const FileManagerPage({super.key, required this.pc});

  @override
  State<FileManagerPage> createState() => _FileManagerPageState();
}

class _FileManagerPageState extends State<FileManagerPage> {
  final Map<String, List<String>> responses = {};

  final Map<String, TextEditingController> pathControllers = {};
  final Map<String, TextEditingController> nameControllers = {};
  final Map<String, TextEditingController> srcControllers = {};
  final Map<String, TextEditingController> dstControllers = {};

  static const int maxLogs = 20;
  final List<String> consoleLogs = [];

  @override
  void initState() {
    super.initState();
    for (var cmd in fileCommands) {
      responses[cmd] = [];
      pathControllers[cmd] = TextEditingController();
      nameControllers[cmd] = TextEditingController();
      srcControllers[cmd] = TextEditingController();
      dstControllers[cmd] = TextEditingController();
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
        for (var item in data) responses[cmd]!.add(item.toString());
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

  Widget inputField(TextEditingController controller, String hint) {
    return TextField(
      controller: controller,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        hintText: hint,
        hintStyle: const TextStyle(color: Colors.grey),
        filled: true,
        fillColor: Colors.grey.shade800,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: BorderSide.none,
        ),
      ),
    );
  }

  Widget buildCommand(String cmd) {
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

          if (cmd == "Search File") inputField(nameControllers[cmd]!, "File name"),
          if (["Inspect Folder","Create Folder","Create File","Delete Item","Read File","Edit File"]
              .contains(cmd)) inputField(pathControllers[cmd]!, "Path"),
          if (["Move Item","Create Zip"].contains(cmd)) ...[
            inputField(srcControllers[cmd]!, "Source path"),
            const SizedBox(height: 6),
            inputField(dstControllers[cmd]!, "Destination path"),
          ],

          const SizedBox(height: 10),
          GestureDetector(
            onTap: () {
              String path = pathControllers[cmd]?.text.trim() ?? "";
              String name = nameControllers[cmd]?.text.trim() ?? "";
              String src = srcControllers[cmd]?.text.trim() ?? "";
              String dst = dstControllers[cmd]?.text.trim() ?? "";

              switch (cmd) {
                case "Search File":
                  send(cmd, arg1: name);
                  break;
                case "Inspect Folder":
                case "Create Folder":
                case "Create File":
                case "Delete Item":
                case "Read File":
                case "Edit File":
                  send(cmd, arg1: path);
                  break;
                case "Move Item":
                case "Create Zip":
                  send(cmd, arg1: src, arg2: dst);
                  break;
              }

              pathControllers[cmd]?.clear();
              nameControllers[cmd]?.clear();
              srcControllers[cmd]?.clear();
              dstControllers[cmd]?.clear();
            },
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(color: Colors.blue, borderRadius: BorderRadius.circular(8)),
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
            )
          ]
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.pc.name)),
      body: Column(
        children: [
          Expanded(
            flex: 2,
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: fileCommands.map(buildCommand).toList(),
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
                itemBuilder: (context, index) => Text(
                  consoleLogs[index],
                  style: const TextStyle(color: Colors.greenAccent),
                ),
              ),
            ),
          )
        ],
      ),
    );
  }
}