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

  Future<void> updateMed(int id, Map<String, dynamic> data) async {
    try {
      final response = await http.put(
        Uri.parse('http://192.168.18.138:5000/meds/$id'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      if (response.statusCode == 200) {
        print('Medicine updated successfully');
        fetchMeds(); // Refresh medicine data after update
      } else {
        print('Failed to update medicine');
      }
    } catch (error) {
      print('Error updating medicine: $error');
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
          final med = meds[index];
          return ListTile(
            title: Text(med['name']),
            subtitle: Text('${med['dosage']} - \$${med['price']}'),
            onTap: () {
              _editMed(context, med);
            },
          );
        },
      ),
    );
  }

  void _editMed(BuildContext context, Map<String, dynamic> med) {
    TextEditingController nameController = TextEditingController(text: med['name']);
    TextEditingController dosageController = TextEditingController(text: med['dosage']);
    TextEditingController priceController = TextEditingController(text: med['price'].toString());

    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Edit Medicine'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              TextField(
                controller: nameController,
                decoration: InputDecoration(labelText: 'Name'),
              ),
              TextField(
                controller: dosageController,
                decoration: InputDecoration(labelText: 'Dosage'),
              ),
              TextField(
                controller: priceController,
                decoration: InputDecoration(labelText: 'Price'),
                keyboardType: TextInputType.number,
              ),
            ],
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () {
                Map<String, dynamic> updatedMed = {
                  'name': nameController.text,
                  'dosage': dosageController.text,
                  'price': double.parse(priceController.text),
                };
                updateMed(med['id'], updatedMed);
                Navigator.of(context).pop();
              },
              child: Text('Save'),
            ),
          ],
        );
      },
    );
  }
}
