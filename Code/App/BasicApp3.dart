import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

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
  void initState() {
    super.initState();
    // Retrieve medicine data when the app starts
    _loadMedicineData();
  }

  // Function to retrieve medicine data from SharedPreferences
  void _loadMedicineData() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      medicineNames = prefs.getStringList('medicineNames') ?? [];
      quantities = prefs.getStringList('quantities')?.map(int.parse).toList() ?? [];
    });
  }

  // Function to save medicine data to SharedPreferences
  void _saveMedicineData() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setStringList('medicineNames', medicineNames);
    prefs.setStringList('quantities', quantities.map((e) => e.toString()).toList());
  }

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
                        // Save medicine data after adding new medicine
                        _saveMedicineData();
                      },
                      existingMedicineNames: medicineNames,
                      existingQuantities: quantities,
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
  final List<String> existingMedicineNames;
  final List<int> existingQuantities;

  const AddMedicinePage({
    Key? key,
    required this.onSave,
    required this.existingMedicineNames,
    required this.existingQuantities,
  }) : super(key: key);

  @override
  _AddMedicinePageState createState() => _AddMedicinePageState();
}

class _AddMedicinePageState extends State<AddMedicinePage> {
  late List<String> medicineNames;
  late List<int> quantities;

  @override
  void initState() {
    super.initState();
    // Initialize lists with existing data
    medicineNames = List.from(widget.existingMedicineNames);
    quantities = List.from(widget.existingQuantities);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Edit Medicine in Vending Machine'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: ListView(
          children: List.generate(10, (index) {
            int stackNumber = index + 1;
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Stack $stackNumber:',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                TextFormField(
                  initialValue: medicineNames[index],
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
                const SizedBox(height: 8),
                TextFormField(
                  initialValue: quantities[index].toString(),
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
                const SizedBox(height: 16),
              ],
            );
          }),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Save edited medicine data
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

  Color _getStatusColor(int quantity) {
    if (quantity <= 5) {
      return Colors.red; // Low stock
    } else if (quantity <= 15) {
      return Colors.yellow; // Medium stock
    } else {
      return Colors.green; // High stock
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Medicine Stock'),
      ),
      body: ListView.builder(
        itemCount: medicineNames.length,
        itemBuilder: (context, index) {
          int stackNumber = index + 1;
          return ListTile(
            title: Text('Stack $stackNumber: ${medicineNames[index]}'),
            subtitle: LinearProgressIndicator(
              value: quantities[index] / 20, // Assuming max stock is 20
              backgroundColor: Colors.grey,
              valueColor: AlwaysStoppedAnimation<Color>(
                _getStatusColor(quantities[index]),
              ),
            ),
          );
        },
      ),
    );
  }
}
