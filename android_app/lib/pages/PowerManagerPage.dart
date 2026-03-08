import 'package:flutter/material.dart';
import '../services/api_client.dart';
import '../model/pc_model.dart';

final List<String> commands = [
  "Shutdown",
  "Restart",
  "Sleep",
  "Hibernate",
];

class PowerManagerPage extends StatefulWidget {
  final PC pc;

  const PowerManagerPage({super.key, required this.pc});

  @override
  State<PowerManagerPage> createState() => _PowerManagerPageState();
}

class _PowerManagerPageState extends State<PowerManagerPage> {
  final List<String> consoleLogs = [];

  void send(String cmd) async {
    consoleLogs.add("> Sending: $cmd");
    setState(() {});

    try {
      final response = await ApiClient.sendCommand(
        pcId: widget.pc.pcId,
        token: widget.pc.token,
        command: cmd,
      );

      consoleLogs.add("Result: ${response["data"]}");
    } catch (e) {
      consoleLogs.add("Error: $e");
    }

    setState(() {});
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
            child: ListView.builder(
              itemCount: commands.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text(commands[index]),
                  onTap: () => send(commands[index]),
                );
              },
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
          )
        ],
      ),
    );
  }
}
