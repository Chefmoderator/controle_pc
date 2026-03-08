import 'package:flutter/material.dart';
import '../model/pc_model.dart';
import '../services/api_client.dart';

class SystemInfoPage extends StatefulWidget {
  final PC pc;

  const SystemInfoPage({super.key, required this.pc});

  @override
  State<SystemInfoPage> createState() => _SystemInfoPage();
}

class _SystemInfoPage extends State<SystemInfoPage> {
  Map<String, dynamic>? systemData;
  bool loading = false;

  void send(String cmd) async {
      setState(() {
        loading = true;
      });

      try {
        final response = await ApiClient.sendCommand(
          pcId: widget.pc.pcId,
          token: widget.pc.token,
          command: cmd,
        );

        systemData = response["data"];
      } catch (e) {
        systemData = {"error": e.toString()};
      }

      setState(() {
        loading = false;
      });
    }

  Widget buildBlock(String title, Widget child) {
    return Container(
      margin: const EdgeInsets.only(bottom: 14),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.grey.shade900,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [

          Text(
            title,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),

          const SizedBox(height: 8),

          child
        ],
      ),
    );
  }

  Widget buildText(String text) {
    return Text(
      text,
      style: const TextStyle(
        color: Colors.greenAccent,
        fontSize: 15,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.pc.name),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [

            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: loading ? null : () => send("systeminfo"),
                child: loading
                    ? const CircularProgressIndicator()
                    : const Text("Get System Info"),
              ),
            ),

            const SizedBox(height: 16),

            Expanded(
              child: systemData == null
                  ? const Center(
                      child: Text(
                        "Press button to load system info",
                        style: TextStyle(color: Colors.grey),
                      ),
                    )
                  : ListView(
                      children: [

                        if (systemData!.containsKey("get_system_version"))
                          buildBlock(
                            "System Version",
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                buildText(
                                    systemData!["get_system_version"]["os"]),
                                buildText(systemData!["get_system_version"]
                                    ["full_os"]),
                              ],
                            ),
                          ),

                        if (systemData!.containsKey("get_user"))
                          buildBlock(
                            "User",
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                buildText(
                                    "PC: ${systemData!["get_user"]["pc_name"]}"),
                                buildText(
                                    "User: ${systemData!["get_user"]["user"]}"),
                              ],
                            ),
                          ),

                        if (systemData!.containsKey("get_computer_hardware"))
                          buildBlock(
                            "Computer Hardware",
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [

                                buildText(
                                    "CPU: ${systemData!["get_computer_hardware"]["cpu"]}"),

                                buildText(
                                    "Machine: ${systemData!["get_computer_hardware"]["machine"]}"),

                                const SizedBox(height: 6),

                                buildText(
                                    "RAM Total: ${systemData!["get_computer_hardware"]["ram"]["total_gb"]} GB"),

                                buildText(
                                    "RAM Used: ${systemData!["get_computer_hardware"]["ram"]["used_gb"]} GB"),

                                const SizedBox(height: 6),

                                ...List.generate(
                                  systemData!["get_computer_hardware"]["disks"]
                                      .length,
                                  (i) {
                                    final disk = systemData![
                                        "get_computer_hardware"]["disks"][i];

                                    return buildText(
                                        "Disk ${disk["device"]} — ${disk["used_percent"]}% used");
                                  },
                                )
                              ],
                            ),
                          ),

                        if (systemData!.containsKey("get_temperature") && !(systemData!["get_temperature"] is Map && systemData!["get_temperature"].containsKey("error")))
                          buildBlock(
                            "Temperature",
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                ...systemData!["get_temperature"].entries.map<Widget>((entry) {
                                  final sensors = entry.value;
                                  return Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: sensors.map<Widget>((sensor) {
                                      return buildText("${sensor["label"]}: ${sensor["temperature_c"]}°C");
                                    }).toList(),
                                  );
                                }).toList()
                              ],
                            ),
                          ),

                        if (systemData!.containsKey("get_uptime"))
                          buildBlock(
                            "Uptime",
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                buildText(
                                    "Boot: ${systemData!["get_uptime"]["boot_time"]}"),
                                buildText(
                                    "Uptime: ${systemData!["get_uptime"]["uptime"]}"),
                              ],
                            ),
                          ),

                        if (systemData!.containsKey("get_battery"))
                          buildBlock(
                            "Battery",
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                buildText(
                                    "Level: ${systemData!["get_battery"]["level_percent"] ?? "N/A"}%"),
                                buildText(
                                    "Plugged: ${systemData!["get_battery"]["plugged_in"]}"),
                                buildText(
                                    "Time left: ${systemData!["get_battery"]["time_left"] ?? "N/A"}"),
                              ],
                            ),
                          ),
                      ],
                    ),
            )
          ],
        ),
      ),
    );
  }
}