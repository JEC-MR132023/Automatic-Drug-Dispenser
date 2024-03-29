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
      home: LoginPage(),
    );
  }
}

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  TextEditingController emailController = TextEditingController();
  TextEditingController passwordController = TextEditingController();

  Future<void> login() async {
    final apiUrl = Uri.parse('http://192.168.18.138:5000/login');
    final response = await http.post(
      apiUrl,
      body: jsonEncode({
        'username': emailController.text,
        'password': passwordController.text,
      }),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      // Login successful
      final responseData = json.decode(response.body);
      final token = responseData['token'];
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => MedsListScreen(token)),
      );
    } else {
      // Login failed
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text('Error'),
            content: Text('Login failed'),
            actions: <Widget>[
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: Text('OK'),
              ),
            ],
          );
        },
      );
    }
  }

  Future<void> register() async {
    final apiUrl = Uri.parse('http://192.168.18.138:5000/register');
    final response = await http.post(
      apiUrl,
      body: jsonEncode({
        'username': emailController.text,
        'password': passwordController.text,
      }),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 201) {
      // Registration successful
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text('Success'),
            content: Text('Registration successful'),
            actions: <Widget>[
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: Text('OK'),
              ),
            ],
          );
        },
      );
    } else {
      // Registration failed
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text('Error'),
            content: Text('Registration failed'),
            actions: <Widget>[
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: Text('OK'),
              ),
            ],
          );
        },
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Automatic Medicine Dispenser',

          style: TextStyle(
            fontSize: 20, // Adjust font size
            fontWeight: FontWeight.bold, // Apply bold font weight
            color: Colors.black, // Set text color
            letterSpacing: 1.5, // Set letter spacing
            // Add more text style properties as needed
                  ),
              ),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            TextField(
              controller: emailController,
              decoration: InputDecoration(labelText: 'Email'),
            ),
            TextField(
              controller: passwordController,
              decoration: InputDecoration(labelText: 'Password'),
              obscureText: true,
            ),
            SizedBox(height: 16.0),
            ElevatedButton(
              onPressed: login,
              child: Text('Login'),
            ),
            SizedBox(height: 8.0),
            ElevatedButton(
              onPressed: register,
              child: Text('Register'),
            ),
          ],
        ),
      ),
    );
  }
}

class MedsListScreen extends StatefulWidget {
  MedsListScreen(token);

  @override
  _MedsListScreenState createState() => _MedsListScreenState();
}

class _MedsListScreenState extends State<MedsListScreen> {
  List<dynamic> meds = [];
  int maxStock = 100;

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

  Future<void> addMed(Map<String, dynamic> data) async {
    try {
      final response = await http.post(
        Uri.parse('http://192.168.18.138:5000/meds'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      if (response.statusCode == 201) {
        print('Medicine added successfully');
        fetchMeds(); // Refresh medicine data after addition
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
        title: Text('Meds List'),
      ),
      body: ListView.builder(
        itemCount: meds.length,
        itemBuilder: (context, index) {
          final med = meds[index];
          return ListTile(
            title: Text('ID: ${med['id']} - ${med['name']} ${med['dosage']}mg - ₹${med['price']}'),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                Text('Stock: ${med['stock']}'),
                SizedBox(height: 8), // Add spacing between subtitle and progress bar
                LinearProgressIndicator(
                  value: med['stock'] / maxStock, // Calculate the progress value
                  backgroundColor: Colors.grey[300],
                  valueColor: AlwaysStoppedAnimation<Color>(
                    med['stock'] > 0.2 * maxStock ? Colors.green : Colors.red,
                  ),
                ),
              ],
            ),
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
        child: Icon(Icons.add),
      ),
    );
  }

  void _editMed(BuildContext context, Map<String, dynamic> med) {
    TextEditingController nameController = TextEditingController(text: med['name']);
    TextEditingController dosageController = TextEditingController(text: med['dosage']);
    TextEditingController priceController = TextEditingController(text: med['price'].toString());
    TextEditingController stockController = TextEditingController(text: med['stock'].toString());
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
              TextField(
                controller: stockController,
                decoration: InputDecoration(labelText: 'stock'),
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
                  'stock': double.parse(stockController.text),
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

  void _addMed(BuildContext context) {
    TextEditingController nameController = TextEditingController();
    TextEditingController dosageController = TextEditingController();
    TextEditingController priceController = TextEditingController();
    TextEditingController stockController = TextEditingController(); // Add stock controller

    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Add Medicine'),
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
              TextField(
                controller: stockController,
                decoration: InputDecoration(labelText: 'Stock'), // Add stock field
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
                Map<String, dynamic> newMed = {
                  'name': nameController.text,
                  'dosage': dosageController.text,
                  'price': double.parse(priceController.text),
                  'stock': int.parse(stockController.text), // Add stock field
                };
                addMed(newMed);
                Navigator.of(context).pop();
              },
              child: Text('Add'),
            ),
          ],
        );
      },
    );
  }}
