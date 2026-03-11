import 'package:flutter/material.dart';
import '../services/api_client.dart';
import './HomePage.dart';
import '../model/pc_model.dart';
import "../services/pc_storage.dart";

class RegisterPCPage extends StatefulWidget {
  const RegisterPCPage({super.key});

  @override
  State<RegisterPCPage> createState() => _RegisterPCPageState();
}

class _RegisterPCPageState extends State<RegisterPCPage> {
  final ipController = TextEditingController();
  final portController = TextEditingController();

  void returnToMainMenu() {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => HomePage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Register PC"),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: ipController,
              decoration: const InputDecoration(
                labelText: "PC IP Address",
                hintText: "Enter PC IP",
              ),
              keyboardType: TextInputType.number,
            ),
            const SizedBox(height: 16),
            TextField(
              controller: portController,
              decoration: const InputDecoration(
                labelText: "PC Port",
                hintText: "Enter PC port",
              ),
              keyboardType: TextInputType.number,
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () async {
                final ip = ipController.text.trim();
                final port = portController.text.trim();

                if (ip.isEmpty || port.isEmpty) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text("Please enter both IP and Port")),
                  );
                  return;
                }

                try {
                  final response = await ApiClient.registerPC(ip, port);

                  final existingPCs = await PCStorage.loadPCs();

                  for (var pcData in response["pcs"]) {
                    if (existingPCs.any((p) => p.pcId == pcData["pc_id"].toString())) {
                      continue;
                    }
                    final pc = PC(
                      name: "My PC",
                      pcId: pcData['pc_id'].toString(),
                      token: response["jwt"],
                    );
                    await PCStorage.addPC(pc);
                  }

                  returnToMainMenu();
                } catch (e) {
                  print("Error registering PC: $e");
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text("Error registering PC: $e")),
                  );
                }
              },
              child: const Text("Register"),
              style: ElevatedButton.styleFrom(
                minimumSize: const Size.fromHeight(50),
              ),
            ),
          ],
        ),
      ),
    );
  }
}