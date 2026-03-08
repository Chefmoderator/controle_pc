import 'package:flutter/material.dart';
import '../model/pc_model.dart';
import '../services/api_client.dart';

final List<String> commands = [
  "Mute",
  "Unmute",
  "Get Volume",
  "Set Volume",
];

class VolumeManagerPage extends StatefulWidget {
  final PC pc;

  const VolumeManagerPage({super.key, required this.pc});

  @override
  State<VolumeManagerPage> createState() => _VolumeManagerPageState();
}

class _VolumeManagerPageState extends State<VolumeManagerPage> {

  final List<String> consoleLogs = [];
  final Map<String, List<String>> responses = {};

  final TextEditingController volumeController = TextEditingController();

  static const int maxLogs = 20;

  @override
  void initState() {
    super.initState();

    for (var cmd in commands) {
      responses[cmd] = [];
    }
  }

  String formatResponse(String cmd, dynamic data) {

    if (cmd == "Mute") {
      return "PC muted";
    }

    if (cmd == "Unmute") {
      return "PC unmuted";
    }

    if (cmd == "Get Volume") {
      if (data is Map && data.containsKey("current_volume")) {
        return "Volume: ${data["current_volume"]}%";
      }
      return "Volume received";
    }

    if (cmd == "Set Volume") {
      if (data is Map && data.containsKey("current_volume")) {
        return "Volume set to ${data["current_volume"]}%";
      }
      return "Volume updated";
    }

    return data.toString();
  }

  void send(String cmd, {String? arg}) async {

    String commandToSend = cmd;

    if (arg != null) {
      commandToSend = "$cmd $arg";
    }

    consoleLogs.add("> $commandToSend");

    if (consoleLogs.length > maxLogs) {
      consoleLogs.removeAt(0);
    }

    setState(() {});

    try {

      final response = await ApiClient.sendCommand(
        pcId: widget.pc.pcId,
        token: widget.pc.token,
        command: commandToSend,
      );

      final data = response["data"];

      final pretty = formatResponse(cmd, data);

      consoleLogs.add(pretty);

      responses[cmd]!.add(pretty);

      if (responses[cmd]!.length > 1) {
        responses[cmd]!.removeAt(0);
      }

    } catch (e) {

      consoleLogs.add("Error");

    }

    if (consoleLogs.length > maxLogs) {
      consoleLogs.removeAt(0);
    }

    setState(() {});
  }

  Widget buildCommand(String cmd) {

    bool isSetVolume = cmd == "Set Volume";

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
              if (!isSetVolume) {
                send(cmd);
              }
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

          if (isSetVolume) ...[

            const SizedBox(height: 10),

            Row(
              children: [

                Expanded(
                  child: TextField(
                    controller: volumeController,
                    keyboardType: TextInputType.number,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: "0 - 100",
                      hintStyle: TextStyle(color: Colors.grey),
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

                    if (volumeController.text.trim().isEmpty) {
                      consoleLogs.add("Volume empty");
                      setState(() {});
                      return;
                    }

                    send(cmd, arg: volumeController.text);

                    volumeController.clear();
                  },
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16, vertical: 12),
                    decoration: BoxDecoration(
                      color: Colors.blue,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Text(
                      "SET",
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
                    .map(
                      (e) => Text(
                        e,
                        style: const TextStyle(
                          color: Colors.greenAccent,
                        ),
                      ),
                    )
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
                    style: const TextStyle(
                      color: Colors.greenAccent,
                    ),
                  );
                },
              ),
            ),
          )

        ],
      ),
    );
  }
}