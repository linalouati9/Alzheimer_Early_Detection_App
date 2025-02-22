import 'package:flutter/material.dart';

class ResultPage extends StatelessWidget {
  final int processedData; // Binary result: 0 or 1

  ResultPage({required this.processedData});

  @override
  Widget build(BuildContext context) {
    // Determine result message and background color
    String resultMessage;
    Color backgroundColor;

    if (processedData == 1) {
      resultMessage =
          "The person might have dementia. Please consult a specialist for further evaluation.";
      backgroundColor = Colors.grey; // Red for potential dementia
    } else {
      resultMessage =
          "The person does not show signs of dementia based on the test.";
      backgroundColor = Colors.blueGrey; // Green for no signs of dementia
    }

    return Scaffold(
      appBar: AppBar(title: Text('Dementia Test Result')),
      body: Container(
        color: backgroundColor, // Set background color
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Text(
              resultMessage,
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.white, // Ensure text is readable on both colors
              ),
              textAlign: TextAlign.center,
            ),
          ),
        ),
      ),
    );
  }
}
