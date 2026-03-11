import 'package:shared_preferences/shared_preferences.dart';

class ServerConfig {
  static const String serverKey = "current_server";

  static Future<String> loadServer() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(serverKey) ?? "192.168.0.136:8443";
  }

  static Future<void> saveServer(String url) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(serverKey, url);
  }
}
