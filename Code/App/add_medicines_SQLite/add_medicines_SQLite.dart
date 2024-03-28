import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MedsApp());
}

class MedsApp extends StatelessWidget {
  const MedsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Meds',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const MedsListScreen(),
    );
  }
}

class MedsListScreen extends StatefulWidget {
  const MedsListScreen({super.key});

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

  Future<void> addMed(Map<String, dynamic> data) async {
    try {
      final response = await http.post(
        Uri.parse('http://192.168.18.138:5000/meds'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      if (response.statusCode == 201) {
        print('Medicine added successfully');
        fetchMeds(); // Refresh medicine data after adding
      } else {
        print('Failed to add medicine');
      }
    } catch (error) {
      print('Error adding medicine: $error');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Meds List'),
      ),
      body: ListView.builder(
        itemCount: meds.length,
        itemBuilder: (context, index) {
          final med = meds[index];
          return ListTile(
            title: Text('${med['id']}.  ${med['name']} ${med['dosage']}mg  - ₹${med['price']}'),

            onTap: () {
              _editMed(context, med);
            },
          );


        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          _addMed(context);
        },
        child: const Icon(Icons.add),
      ),
    );
  }

  void _editMed(BuildContext context, Map<String, dynamic> med) {
    // Implement edit medicine functionality
  }

  void _addMed(BuildContext context) {
    TextEditingController nameController = TextEditingController();
    TextEditingController dosageController = TextEditingController();
    TextEditingController priceController = TextEditingController();

    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Add Medicine'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              TextField(
                controller: nameController,
                decoration: const InputDecoration(labelText: 'Name'),
              ),
              TextField(
                controller: dosageController,
                decoration: const InputDecoration(labelText: 'Dosage'),
              ),
              TextField(
                controller: priceController,
                decoration: const InputDecoration(labelText: 'Price'),
                keyboardType: TextInputType.number,
              ),
            ],
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () {
                Map<String, dynamic> newMed = {
                  'name': nameController.text,
                  'dosage': dosageController.text,
                  'price': double.parse(priceController.text),
                };
                addMed(newMed);
                Navigator.of(context).pop();
              },
              child: const Text('Save'),
            ),
          ],
        );
      },
    );
  }
}
