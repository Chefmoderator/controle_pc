import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiClient {
  static const String baseUrl = "http://192.168.0.136:8443";

  static Future<Map<String, dynamic>> registerPC(String ip) async {
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
  }) async {
    final url = Uri.parse("$baseUrl/client/send_command");

    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "pc_id": pcId,
        "command": command,
        "token": token,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception("Server error: ${response.body}");
    }

    return jsonDecode(response.body);
  }
}
