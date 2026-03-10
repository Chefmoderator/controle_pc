import 'dart:convert';
import 'package:http/http.dart' as http;
import './serverСonfig.dart';

class ApiClient {
  static Future<String> getServerUrl() async {
    return await ServerConfig.loadServer();
  }

  static Future<Map<String, dynamic>> registerPC(String ip) async {
    final baseUrl = await getServerUrl();
    final url = Uri.parse("$baseUrl/client/register_pc");
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"pc_ip": ip}),
    );

    if (response.statusCode != 200) {
      throw Exception("Server error: ${response.body}");
    }

    return jsonDecode(response.body);
  }

  static Future<Map<String, dynamic>> removePc(String id) async {
    final baseUrl = await getServerUrl();
    final url = Uri.parse("$baseUrl/client/remove_pc");
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
    final url = Uri.parse("$baseUrl/client/send_command");
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
}
