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
  final IpAddressPC = TextEditingController();

  void returnTomainMenu() {
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
              controller: IpAddressPC,
              decoration: const InputDecoration(labelText: "PC Ip address"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () async {
                final ip = IpAddressPC.text;
                try {
                  final response = await ApiClient.registerPC(ip);

                  final existingPCs = await PCStorage.loadPCs();

                  for (var pcData in response["pcs"]) {
                    if (existingPCs.any((p) => p.pcId == pcData["pc_id"].toString())) {
                      continue;
                    }
                    final pc = PC(
                      name: "My Pc ",
                      pcId: pcData['pc_id'].toString(),
                      token: response["jwt"]);
                    await PCStorage.addPC(pc);
                  }
                  returnTomainMenu();
                } catch (e) {
                  print("Ошибка при регистрации ПК: $e");
                }
              },
              child: const Text("send"),
            ),
          ],
        ),
      ),
    );
  }
}
