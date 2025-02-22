import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_sound/flutter_sound.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'result_page.dart';

class TestPage extends StatefulWidget {
  @override
  _TestPageState createState() => _TestPageState();
}

class _TestPageState extends State<TestPage> {
  final FlutterSoundRecorder _recorder = FlutterSoundRecorder();
  bool _isRecording = false;
  bool _isLoading = false;
  String _audioPath = '';

  @override
  void initState() {
    super.initState();
    _initializeRecorder();
  }

  Future<void> _initializeRecorder() async {
    var status = await Permission.microphone.request();
    if (status.isGranted) {
      await _recorder.openRecorder();
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Microphone permission is required')),
      );
    }
  }

  Future<void> _startRecording() async {
    if (!_isRecording) {
      _audioPath = '${Directory.systemTemp.path}/recording.wav';
      await _recorder.startRecorder(toFile: _audioPath, codec: Codec.pcm16WAV);
      setState(() {
        _isRecording = true;
      });
    }
  }

  Future<void> _stopRecording() async {
    if (_isRecording) {
      await _recorder.stopRecorder();
      setState(() {
        _isRecording = false;
      });
      // Delay the loading screen for 1 second before sending the audio
      await Future.delayed(Duration(seconds: 2), () {
        setState(() {
          _isLoading = true; // Show loading indicator after the delay
        });

        // Send audio file to server
        _sendAudioFileToServer();
      });
    }
  }

  Future<void> _sendAudioFileToServer() async {
    setState(() {
      _isLoading = true; // Show loading indicator
    });
    try {
      File audioFile = File(_audioPath);

      // Send file to the Python server
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('http://192.168.1.33:5000/process-audio'),
      );
      request.files
          .add(await http.MultipartFile.fromPath('file', audioFile.path));

      var response = await request.send();

      if (response.statusCode == 200) {
        final responseData = await http.Response.fromStream(response);
        final data = json.decode(responseData.body);
        print("Predictions: ${data['predictions']}");
        // Extract the result (0 or 1)
        int result = data['result'];
        print("Result: $result");

        // Navigate to the result page (or handle result as needed)
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => ResultPage(processedData: result),
          ),
        );
      } else {
        print("Error: ${response.reasonPhrase}");
      }
    } catch (e) {
      print("Error: $e");
      // Fallback to manually specified result
      int fallbackResult = 0; // Set this to 0 or 1 for testing
      print("Using fallback result: $fallbackResult");

      // Navigate to the result page with the fallback result
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ResultPage(processedData: fallbackResult),
        ),
      );
    }finally {
      setState(() {
        _isLoading = false; // Hide loading indicator
      });
    }
  }

  @override
  void dispose() {
    _recorder.closeRecorder();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Cookie Theft Test'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Title of the test page
            Text(
              'Describe the Scene',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 16),

            // Image for the user to describe
            Image.asset(
              'assets/cookie_theft.png',
              height: 250,
            ),
            SizedBox(height: 16),

            // Question asking the user to describe the scene
            Text(
              'Question: What is happening in this picture?',
              style: TextStyle(fontSize: 18),
            ),
            SizedBox(height: 24),

            // Start or stop recording button
            Center(
              child: ElevatedButton(
                onPressed: _isRecording ? _stopRecording : _startRecording,
                child: Text(_isRecording ? 'Stop Recording' : 'Start Recording'),
              ),
            ),

            // Show additional UI when recording is in progress
            if (_isRecording) ...[
              SizedBox(height: 32),
              Center(
                child: Column(
                  children: [
                    Text(
                      'Recording in progress...',
                      style: TextStyle(fontSize: 16, color: Colors.red),
                    ),
                    SizedBox(height: 8),
                    Icon(Icons.mic, color: Colors.red, size: 40),
                  ],
                ),
              ),
            ],

            // Show a loading indicator if the file is being processed
            if (_isLoading) ...[
              SizedBox(height: 32),
              Center(
                child: CircularProgressIndicator(),
              ),
            ],
          ],
        ),
      ),
    );
  }
}