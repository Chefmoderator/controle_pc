import 'dart:convert';
import 'package:flutter/material.dart';
import '../model/pc_model.dart';
import '../services/api_client.dart';

final List<String> cameraCommands = [
  "Screen Screenshot",
  "Camera Capture",
];

class CameraPage extends StatefulWidget {
  final PC pc;

  const CameraPage({super.key, required this.pc});

  @override
  State<CameraPage> createState() => _CameraPageState();
}

class _CameraPageState extends State<CameraPage> {

  String? imageBase64;

  static const int maxLogs = 20;
  final List<String> consoleLogs = [];

  void send(String cmd) async {
    consoleLogs.add("> $cmd");
    if (consoleLogs.length > maxLogs) {
      consoleLogs.removeAt(0);
    }
    setState(() {});
    try {
      final response = await ApiClient.sendCommand(
        pcId: widget.pc.pcId,
        token: widget.pc.token,
        command: cmd,
      );

      final data = response["data"];
      if (data != null && data.toString().isNotEmpty) {
        imageBase64 = data;
      }
      consoleLogs.add("Response received for $cmd");
    } catch (e) {
      consoleLogs.add("Error: $e");
    }
    if (consoleLogs.length > maxLogs) {
      consoleLogs.removeAt(0);
    }
    setState(() {});
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
          Text(
            cmd,
            style: const TextStyle(color: Colors.white, fontSize: 18),
          ),
          const SizedBox(height: 10),
          GestureDetector(
            onTap: () {
              switch (cmd) {
                case "Screen Screenshot":
                  send("screen screenshot");
                  break;

                case "Camera Capture":
                  send("camera capture");
                  break;
              }
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
          )
        ],
      ),
    );
  }

  Widget imageViewer() {

    if (imageBase64 == null) {
      return const Center(
        child: Text(
          "No image",
          style: TextStyle(color: Colors.white),
        ),
      );
    }
    return Image.memory(
      base64Decode(imageBase64!),
      fit: BoxFit.contain,
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
            child: Container(
              color: Colors.black,
              width: double.infinity,
              child: imageViewer(),
            ),
          ),
          Expanded(
            flex: 2,
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: cameraCommands.map(buildCommand).toList(),
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