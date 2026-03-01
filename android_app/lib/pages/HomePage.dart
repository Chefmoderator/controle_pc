import 'package:flutter/material.dart';
import '../services/pc_storage.dart';
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

  @override
  void initState() {
    super.initState();
    loadPCs();
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
      body: pcs.isEmpty
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
    );
  }
}
