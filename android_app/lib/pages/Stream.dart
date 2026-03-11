import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import '../model/pc_model.dart';
import 'package:flutter/material.dart';
import '../services/api_client.dart';

class StreamPage extends StatefulWidget {
  final PC pc;

  const StreamPage({super.key, required this.pc});

  @override
  State<StreamPage> createState() => _StreamPage();
}

class _StreamPage extends State<StreamPage> {
  Uint8List? currentFrame;
  bool streaming = false;
  Offset? lastTouch;
  StreamSubscription<Map<String, dynamic>>? _streamSubscription;

  void startStream() {
    setState(() {
      streaming = true;
    });

    _streamSubscription = ApiClient.wsSendCommand(
      pcId: widget.pc.pcId,
      token: widget.pc.token,
      command: "start",
    ).listen((response) {
      if (response["status"] == "ok") {
        final frameB64 = response["data"];
        setState(() {
          currentFrame = base64Decode(frameB64);
        });
      } else if (response.containsKey("error")) {
        print("Stream error: ${response["error"]}");
      }
    }, onError: (err) {
      print("WS subscription error: $err");
      stopStream();
    }, onDone: () {
      stopStream(); 
    });
  }

  void stopStream() {
    _streamSubscription?.cancel();
    _streamSubscription = null;

    ApiClient.wsSendCommand(
      pcId: widget.pc.pcId,
      token: widget.pc.token,
      command: "end",
    );

    setState(() {
      streaming = false;
      currentFrame = null;
      lastTouch = null;
    });
  }

  void handleTouch(DragUpdateDetails details, Size touchpadSize) {
    if (!streaming) return;

    final dx = details.delta.dx / touchpadSize.width;
    final dy = details.delta.dy / touchpadSize.height;

    if (dx.abs() < 0.001 && dy.abs() < 0.001) return; 

    ApiClient.wsSendCommand(
      pcId: widget.pc.pcId,
      token: widget.pc.token,
      command: "mousemove",
      content: jsonEncode({"dx": dx, "dy": dy}),
    );
  }

  @override
  void dispose() {
    _streamSubscription?.cancel();
    _streamSubscription = null;
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final mediaSize = MediaQuery.of(context).size;
    return Scaffold(
      appBar: AppBar(title: Text("Stream: ${widget.pc.name}")),
      body: Column(
        children: [
          Expanded(
            flex: 7,
            child: Container(
              width: mediaSize.width,
              color: Colors.black,
              child: currentFrame != null
                  ? Image.memory(currentFrame!, fit: BoxFit.contain)
                  : const Center(
                      child: Text(
                        "Stream stopped",
                        style: TextStyle(color: Colors.white, fontSize: 18),
                      ),
                    ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 12),
            child: ElevatedButton(
              onPressed: streaming ? stopStream : startStream,
              child: Text(streaming ? "STOP" : "START"),
              style: ElevatedButton.styleFrom(
                  minimumSize: Size(mediaSize.width * 0.6, 50)),
            ),
          ),
          if (streaming)
            Expanded(
              flex: 3,
              child: Padding(
                padding: const EdgeInsets.all(12.0),
                child: GestureDetector(
                  onPanUpdate: (details) => handleTouch(
                      details, Size(mediaSize.width, mediaSize.height / 3)),
                  child: Container(
                    width: double.infinity,
                    decoration: BoxDecoration(
                      color: Colors.grey.shade800,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Center(
                        child: Text(
                      "Touchpad: drag to move cursor",
                      style: TextStyle(color: Colors.white),
                    )),
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}