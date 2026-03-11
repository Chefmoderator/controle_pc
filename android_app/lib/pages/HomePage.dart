import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/pc_storage.dart';
import '../services/serverСonfig.dart';
import '../model/pc_model.dart';
import 'register_pc_page.dart';
import 'process_list_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<PC> pcs = [];

  String systemServer = "192.168.0.136:8443";
  String? userServer;
  String currentServer = "192.168.0.136:8443";



  @override
  void initState() {
    super.initState();
    loadPCs();
    loadServers();
  }

  Future<void> loadServers() async {
    final prefs = await SharedPreferences.getInstance();

    currentServer = await ServerConfig.loadServer();
    userServer = prefs.getString("user_server_url");

    setState(() {});
  }

  Future<void> saveUserServer(String url) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString("user_server_url", url);
    userServer = url;
    setState(() {});
  }

  Future<void> loadPCs() async {
    pcs = await PCStorage.loadPCs();
    setState(() {});
  }

  void openRegisterPC() async {
    await Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => const RegisterPCPage()),
    );
    loadPCs();
  }

  void openPC(PC pc) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => ProcessListPage(pc: pc)),
    );
  }

  void addUserServerDialog() {
    final ipController = TextEditingController();
    final portController = TextEditingController();

    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text("Добавить свой сервер"),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: ipController,
              decoration: const InputDecoration(hintText: "IP адрес"),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: portController,
              decoration: const InputDecoration(hintText: "Порт"),
              keyboardType: TextInputType.number,
            ),
          ],
        ),
        actions: [
          TextButton(
            child: const Text("Отмена"),
            onPressed: () => Navigator.pop(context),
          ),
          TextButton(
            child: const Text("Сохранить"),
            onPressed: () async {
              if (ipController.text.isNotEmpty &&
                  portController.text.isNotEmpty) {
                String url =
                    "http://${ipController.text.trim()}:${portController.text.trim()}";
                await saveUserServer(url);
              }
              Navigator.pop(context);
            },
          ),
        ],
      ),
    );
  }

  void setActiveServer(String url) async {
    await ServerConfig.saveServer(url);
    currentServer = url;
    setState(() {});
  }

  Widget serverTile({
    required String title,
    required String url,
  }) {
    return CheckboxListTile(
      title: Text(
        "$title\n$url",
        style: const TextStyle(fontSize: 14),
      ),
      value: currentServer == url,
      onChanged: (_) => setActiveServer(url),
      controlAffinity: ListTileControlAffinity.leading,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Your PCs"),
        centerTitle: true,
      ),

      floatingActionButton: FloatingActionButton(
        onPressed: openRegisterPC,
        child: const Icon(Icons.add),
      ),

      body: Column(
        children: [

          Expanded(
            child: pcs.isEmpty
                ? const Center(child: Text("No PCs added yet"))
                : ListView.builder(
                    itemCount: pcs.length,
                    itemBuilder: (context, index) {
                      final pc = pcs[index];
                      return ListTile(
                        title: Text(pc.name),
                        subtitle: Text("ID: ${pc.pcId}"),
                        trailing: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            IconButton(
                              icon: const Icon(Icons.close, color: Colors.red),
                              onPressed: () async {
                                await PCStorage.removePC(pc.pcId);
                                loadPCs();
                              },
                            ),
                            const Icon(Icons.arrow_forward_ios),
                          ],
                        ),
                        onTap: () => openPC(pc),
                      );
                    },
                  ),
          ),

          const Divider(height: 1, thickness: 1),

          Container(
            color: Colors.blueGrey.shade900,
            padding: const EdgeInsets.all(12),
            child: Column(
              children: [
                const Text(
                  "Change Server ",
                  style: TextStyle(color: Colors.white, fontSize: 18),
                ),
                const SizedBox(height: 12),

                serverTile(title: "Creator Server", url: systemServer),

                if (userServer != null)
                  serverTile(title: "User Server", url: userServer!),

                const SizedBox(height: 10),

                ElevatedButton(
                  onPressed: addUserServerDialog,
                  child: const Text("Add user server"),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}