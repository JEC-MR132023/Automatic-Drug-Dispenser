//this app allows the user to edit the ip address to which the app communicates

import 'dart:async';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  SharedPreferences prefs = await SharedPreferences.getInstance();
  String editedApiUrl = prefs.getString('editedApiUrl') ?? 'http://192.168.7.22:5000';
  runApp(MedsApp(editedApiUrl: editedApiUrl));
}

class MedsApp extends StatefulWidget {
  final String editedApiUrl;

  const MedsApp({Key? key, required this.editedApiUrl}) : super(key: key);

  @override
  _MedsAppState createState() => _MedsAppState();
}

class _MedsAppState extends State<MedsApp> {
  late String apiUrl;

  @override
  void initState() {
    super.initState();
    apiUrl = widget.editedApiUrl;
  }

  void updateApiUrl(String newApiUrl) {
    setState(() {
      apiUrl = newApiUrl;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Meds',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: LoginPage(apiUrl: apiUrl, updateApiUrl: updateApiUrl),
    );
  }
}

class LoginPage extends StatefulWidget {
  final String apiUrl;
  final Function(String) updateApiUrl;

  const LoginPage({Key? key, required this.apiUrl, required this.updateApiUrl}) : super(key: key);

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  TextEditingController emailController = TextEditingController();
  TextEditingController passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Automatic Medicine Dispenser',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Colors.black,
            letterSpacing: 1.5,
          ),
        ),
        centerTitle: true,
        actions: [
          IconButton(
            onPressed: () async {
              String? updatedUrl = await Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => SettingsPage(apiUrl: widget.apiUrl)),
              );
              if (updatedUrl != null) {
                widget.updateApiUrl(updatedUrl);
              }
            },
            icon: Icon(Icons.settings),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            TextField(
              controller: emailController,
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16.0),
            TextField(
              controller: passwordController,
              decoration: const InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
            ),
            const SizedBox(height: 16.0),
            ElevatedButton(
              onPressed: () => login(widget.apiUrl),
              child: const Text('Login'),
            ),
            const SizedBox(height: 8.0),
            ElevatedButton(
              onPressed: () => register(widget.apiUrl),
              child: const Text('Register'),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> login(String apiUrl) async {
    final response = await http.post(
      Uri.parse('$apiUrl/login'),
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
        MaterialPageRoute(builder: (context) => MedsListScreen(apiUrl: apiUrl, token: token)),
      );
    } else {
      // Login failed
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('Error'),
            content: const Text('Login failed. Please check your credentials.'),
            actions: <Widget>[
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: const Text('OK'),
              ),
            ],
          );
        },
      );
    }
  }

  Future<void> register(String apiUrl) async {
    final response = await http.post(
      Uri.parse('$apiUrl/register'),
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
            title: const Text('Success'),
            content: const Text('Registration successful. You can now login.'),
            actions: <Widget>[
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: const Text('OK'),
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
            title: const Text('Error'),
            content: const Text('Registration failed. Please try again later.'),
            actions: <Widget>[
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: const Text('OK'),
              ),
            ],
          );
        },
      );
    }
  }
}

class SettingsPage extends StatefulWidget {
  final String apiUrl;

  const SettingsPage({Key? key, required this.apiUrl}) : super(key: key);

  @override
  _SettingsPageState createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  TextEditingController ipAddressController = TextEditingController();

  @override
  void initState() {
    super.initState();
    ipAddressController.text = widget.apiUrl.replaceAll('http://', '');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Settings - IP Address'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextField(
              controller: ipAddressController,
              decoration: InputDecoration(
                labelText: 'Current IP Address: ${widget.apiUrl}',
                hintText: 'Enter new IP address',
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                String newIpAddress = ipAddressController.text.trim();
                saveIpAddress(newIpAddress);
                Navigator.pop(context, 'http://$newIpAddress');
              },
              child: Text('Save'),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> saveIpAddress(String newIpAddress) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString('editedApiUrl', 'http://$newIpAddress');
  }
}

class MedsListScreen extends StatefulWidget {
  final String apiUrl;
  final String token;

  const MedsListScreen({Key? key, required this.apiUrl, required this.token}) : super(key: key);

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
    Timer.periodic(const Duration(seconds: 30), (Timer timer) {
      fetchMeds();
    });
  }

  Future<void> fetchMeds() async {
    try {
      final response = await http.get(Uri.parse('${widget.apiUrl}/meds'));
      if (response.statusCode == 200) {
        setState(() {
          meds = json.decode(response.body);
        });

        checkLowStock();
      } else {
        print('Failed to fetch meds');
      }
    } catch (error) {
      print('Error fetching meds: $error');
    }
  }

  void checkLowStock() {
    for (var med in meds) {
      if (med['stock'] < 10) {
        showLowStockAlert(med);
      }
    }
  }

  void showLowStockAlert(Map<String, dynamic> med) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Low Stock Alert'),
          content: Text('${med['name']} is running low on stock (${med['stock']} left)'),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('OK'),
            ),
          ],
        );
      },
    );
  }

  Future<void> updateMed(int id, Map<String, dynamic> data) async {
    try {
      final response = await http.put(
        Uri.parse('${widget.apiUrl}/meds/$id'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      if (response.statusCode == 200) {
        print('Medicine updated successfully');
        fetchMeds();
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
        Uri.parse('${widget.apiUrl}/meds'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      if (response.statusCode == 201) {
        print('Medicine added successfully');
        fetchMeds();
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
            title: Text('ID: ${med['id']} - ${med['name']} ${med['dosage']}mg - ₹${med['price']}'),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                Text('Stock: ${med['stock']}'),
                const SizedBox(height: 8),
                LinearProgressIndicator(
                  value: med['stock'] / maxStock,
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
        child: const Icon(Icons.add),
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
          title: const Text('Edit Medicine'),
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
              TextField(
                controller: stockController,
                decoration: const InputDecoration(labelText: 'stock'),
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
                Map<String, dynamic> updatedMed = {
                  'name': nameController.text,
                  'dosage': dosageController.text,
                  'price': double.parse(priceController.text),
                  'stock': double.parse(stockController.text),
                };
                updateMed(med['id'], updatedMed);
                Navigator.of(context).pop();
              },
              child: const Text('Save'),
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
    TextEditingController stockController = TextEditingController();
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
              TextField(
                controller: stockController,
                decoration: const InputDecoration(labelText: 'Stock'),
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
                  'stock': int.parse(stockController.text),
                };
                addMed(newMed);
                Navigator.of(context).pop();
              },
              child: const Text('Add'),
            ),
          ],
        );
      },
    );
  }
}
