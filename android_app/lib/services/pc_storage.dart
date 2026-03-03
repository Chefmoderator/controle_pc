import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import './api_client.dart';
import '../model/pc_model.dart';

class PCStorage {
  static const String key = "pc_list";

  static Future<void> savePCs(List<PC> list) async {
    final prefs = await SharedPreferences.getInstance();

    final jsonList = list.map((pc) => pc.toJson()).toList();

    await prefs.setString(key, jsonEncode(jsonList));
  }

  static Future<List<PC>> loadPCs() async {
    final prefs = await SharedPreferences.getInstance();

    final raw = prefs.getString(key);
    if (raw == null) return [];

    final List decoded = jsonDecode(raw);

    return decoded.map((item) => PC.fromJson(item)).toList();
  }

  static Future<void> addPC(PC pc) async {
    final list = await loadPCs();
    list.add(pc);
    await savePCs(list);
  }

  static Future<void> removePC(String pcId) async {
    final list = await loadPCs();
    list.removeWhere((pc) => pc.pcId == pcId);
    await savePCs(list);
    ApiClient.removePc(pcId);
  }

  static Future<PC?> get(String pcId) async {
    final list = await loadPCs();
    return list.firstWhere((pc) => pc.pcId == pcId);
  }
}
