import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MedsApp());
}

class MedsApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Meds',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MedsListScreen(),
    );
  }
}

class MedsListScreen extends StatefulWidget {
  @override
  _MedsListScreenState createState() => _MedsListScreenState();
}

class _MedsListScreenState extends State<MedsListScreen> {
  List<dynamic> meds = [];

  @override
  void initState() {
    super.initState();
    fetchMeds();
  }

  Future<void> fetchMeds() async {
    try {
      final response = await http.get(Uri.parse('http://192.168.18.138:5000/meds'));
      if (response.statusCode == 200) {
        setState(() {
          meds = json.decode(response.body);
        });
      } else {
        print('Failed to fetch meds');
      }
    } catch (error) {
      print('Error fetching meds: $error');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Meds List'),
      ),
      body: ListView.builder(
        itemCount: meds.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(meds[index]['name']),
            subtitle: Text(meds[index]['dosage']),
            onTap: () {
              // Handle medicine item tap
            },
          );
        },
      ),
    );
  }
}
