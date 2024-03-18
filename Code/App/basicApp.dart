import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Medicine Vending Machine',
      theme: ThemeData(
        primaryColor: Colors.blue,
        scaffoldBackgroundColor: Colors.white,
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.blue,
          ),
        ),
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<String> medicineNames = [];
  List<int> quantities = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Medicine Vending Machine'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => AddMedicinePage(
                      onSave: (List<String> names, List<int> quantities) {
                        setState(() {
                          medicineNames = names;
                          this.quantities = quantities;
                        });
                      },
                    ),
                  ),
                );
              },
              child: const Text(
                'Add Medicine',
                style: TextStyle(fontSize: 20),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => ViewMedicinePage(medicineNames, quantities),
                  ),
                );
              },
              child: const Text(
                'View Medicines',
                style: TextStyle(fontSize: 20),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class AddMedicinePage extends StatefulWidget {
  final Function(List<String> names, List<int> quantities) onSave;

  const AddMedicinePage({Key? key, required this.onSave}) : super(key: key);

  @override
  _AddMedicinePageState createState() => _AddMedicinePageState();
}

class _AddMedicinePageState extends State<AddMedicinePage> {
  List<String> medicineNames = List.filled(10, '');
  List<int> quantities = List.filled(10, 0);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add Medicine to Vending Machine'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: ListView.builder(
          itemCount: 10,
          itemBuilder: (context, index) {
            return Column(
              children: [
                const SizedBox(height: 20),
                TextFormField(
                  onChanged: (value) {
                    medicineNames[index] = value;
                  },
                  decoration: InputDecoration(
                    labelText: 'Medicine Name',
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10.0),
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                TextFormField(
                  onChanged: (value) {
                    quantities[index] = int.tryParse(value) ?? 0;
                  },
                  keyboardType: TextInputType.number,
                  decoration: InputDecoration(
                    labelText: 'Quantity',
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10.0),
                    ),
                  ),
                ),
              ],
            );
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Save medicine data
          // For demonstration purposes, print medicine data
          print('Medicine Names: $medicineNames');
          print('Quantities: $quantities');
          // You can add logic here to save data to a database or any other storage
          widget.onSave(medicineNames, quantities);
          Navigator.pop(context); // Go back to HomePage
        },
        child: const Icon(Icons.save),
      ),
    );
  }
}

class ViewMedicinePage extends StatelessWidget {
  final List<String> medicineNames;
  final List<int> quantities;

  const ViewMedicinePage(this.medicineNames, this.quantities, {Key? key})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Medicine Stock'),
      ),
      body: ListView.builder(
        itemCount: medicineNames.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(medicineNames[index]),
            subtitle: Text('Stock: ${quantities[index]}'),
          );
        },
      ),
    );
  }
}
