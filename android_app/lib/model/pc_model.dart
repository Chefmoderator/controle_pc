class PC {
  final String name;
  final String pcId;
  final String token;

  PC({required this.name, required this.pcId, required this.token});

  Map<String, dynamic> toJson() => {
    'name': name,
    'pc_id': pcId,
    'token': token,
  };

  factory PC.fromJson(Map<String, dynamic> json) => PC(
    name: json['name'],
    pcId: json['pc_id'],
    token: json['token'],
  );
}