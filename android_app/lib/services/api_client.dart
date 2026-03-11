import 'dart:convert';
import 'package:http/http.dart' as http;
import './serverСonfig.dart';
import 'package:web_socket_channel/io.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class ApiClient {
  static Future<String> getServerUrl() async {
    return await ServerConfig.loadServer();
  }

  static Future<Map<String, dynamic>> registerPC(String ip, String port) async {
    final baseUrl = await getServerUrl();
    final url = Uri.parse("http://$baseUrl/client/register_pc");
    print("port: $port");
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"pc_ip": ip, "pc_port": port}),
    );

    if (response.statusCode != 200) {
      throw Exception("Server error: ${response.body}");
    }

    return jsonDecode(response.body);
  }

  static Future<Map<String, dynamic>> removePc(String id) async {
    final baseUrl = await getServerUrl();
    final url = Uri.parse("http://$baseUrl/client/remove_pc");
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"pc_id": id}),
    );

    if (response.statusCode != 200) {
      throw Exception("Server error: ${response.body}");
    }

    return jsonDecode(response.body);
  }

  static Future<Map<String, dynamic>> sendCommand({
    required String pcId,
    required String token,
    required String command,
    String? content,
  }) async {
    final baseUrl = await getServerUrl();
    final url = Uri.parse("http://$baseUrl/client/send_command");
    final body = {"pc_id": pcId, "command": command, "token": token};
    print(content);
    if (content != null && content.isNotEmpty && content != "null") {
      print(1);
      body["content"] = content;
      print("body: $body");
    }

    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(body),
    );

    if (response.statusCode != 200) {
      throw Exception("Server error: ${response.body}");
    }

    return jsonDecode(response.body);
  }

  static Stream<Map<String, dynamic>> wsSendCommand({
    required String pcId,
    required String token,
    required String command,
    String? content,
  }) async* {
    final baseUrl = await getServerUrl();
    final wsUrl = "ws://$baseUrl/client/ws_send_command";

    final channel = IOWebSocketChannel.connect(Uri.parse(wsUrl));
    final body = {
      "pc_id": pcId,
      "token": token,
      "command": command,
      "content": content,
    };

    channel.sink.add(jsonEncode(body));

    try {
      await for (final msg in channel.stream) {
        final data = jsonDecode(msg);
        yield data;
      }
    } catch (e) {
      print("WS stream error: $e");
      yield {"error": e.toString()};
    } finally {
      await channel.sink.close();
    }
  }
}
