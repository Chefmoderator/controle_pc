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
  "Read File",
  "Edit File",
  "Create Zip",
];

class FileManagerPage extends StatefulWidget {
  final PC pc;

  const FileManagerPage({super.key, required this.pc});

  @override
  State<FileManagerPage> createState() => _FileManagerPageState();
}

class _FileManagerPageState extends State<FileManagerPage> {
  final List<String> consoleLogs = [];
  final Map<String, List<String>> responses = {};

  static const int maxLogs = 20;

  final Map<String, TextEditingController> pathControllers = {};
  final Map<String, TextEditingController> contentControllers = {};
  final Map<String, TextEditingController> dstControllers = {};

  @override
  void initState() {
    super.initState();

    for (var cmd in fileCommands) {
      responses[cmd] = [];
      pathControllers[cmd] = TextEditingController();
      contentControllers[cmd] = TextEditingController();
      dstControllers[cmd] = TextEditingController();
    }
  }

void send(String cmd, {String? arg1, String? arg2}) async {
  responses[cmd] = responses[cmd] ?? [];

  responses[cmd]!.clear();
  setState(() {});

  String commandToSend = cmd;
  if (arg1 != null) commandToSend += " $arg1";
  if (arg2 != null) commandToSend += " $arg2";

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
    responses[cmd]!.add(data.toString());
    consoleLogs.add(data.toString());
  } catch (e) {
    responses[cmd]!.add("Error: $e");
    consoleLogs.add("Error: $e");
  }

  if (consoleLogs.length > maxLogs) consoleLogs.removeAt(0);
  setState(() {});
}

  Widget buildCommand(String cmd) {
    bool needsPath = [
      "Search File",
      "Inspect Folder",
      "Create Folder",
      "Create File",
      "Delete Item",
      "Move Item",
      "Read File",
      "Edit File",
      "Create Zip",
    ].contains(cmd);

    bool needsContent = ["Create File", "Edit File"].contains(cmd);
    bool needsDst = ["Move Item", "Create Zip"].contains(cmd);

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
          Row(
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
            ],
          ),
          if (needsPath) ...[
            const SizedBox(height: 10),
            TextField(
              controller: pathControllers[cmd],
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: "Enter path or filename",
                hintStyle: const TextStyle(color: Colors.grey),
                filled: true,
                fillColor: Colors.grey.shade800,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
          ],
          if (needsContent) ...[
            const SizedBox(height: 10),
            TextField(
              controller: contentControllers[cmd],
              style: const TextStyle(color: Colors.white),
              maxLines: 3,
              decoration: InputDecoration(
                hintText: "Content / New text",
                hintStyle: const TextStyle(color: Colors.grey),
                filled: true,
                fillColor: Colors.grey.shade800,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
          ],
          if (needsDst) ...[
            const SizedBox(height: 10),
            TextField(
              controller: dstControllers[cmd],
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: "Destination path",
                hintStyle: const TextStyle(color: Colors.grey),
                filled: true,
                fillColor: Colors.grey.shade800,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
          ],
          const SizedBox(height: 10),
          GestureDetector(
            onTap: () {
              String path = pathControllers[cmd]!.text.trim();
              String content = contentControllers[cmd]!.text.trim();
              String dst = dstControllers[cmd]!.text.trim();

              switch (cmd) {
                case "Search File":
                  send("search file", arg1: path);
                  break;
                case "Inspect Folder":
                  send("inspection", arg1: path);
                  break;
                case "Create Folder":
                  send("create folder", arg1: path);
                  break;
                case "Create File":
                  send("create file", arg1: path, arg2: content);
                  break;
                case "Delete Item":
                  send("delete item", arg1: path);
                  break;
                case "Move Item":
                  send("move item", arg1: path, arg2: dst);
                  break;
                case "Read File":
                  send("read file", arg1: path);
                  break;
                case "Edit File":
                  send("edit file", arg1: path, arg2: content);
                  break;
                case "Create Zip":
                  send("create zip", arg1: path, arg2: dst);
                  break;
              }

              pathControllers[cmd]!.clear();
              contentControllers[cmd]!.clear();
              dstControllers[cmd]!.clear();
            },
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: Colors.blue,
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Text(
                "EXECUTE",
                style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
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
                    .map((e) => Text(
                          e,
                          style: const TextStyle(color: Colors.greenAccent),
                        ))
                    .toList(),
              ),
            )
          ],
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("File Manager"),
      ),
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
