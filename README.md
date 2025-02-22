# Dementia Early Detection App

The **Dementia Detection App** is a Flutter-based mobile application designed to aid in the early detection of Alzheimer's disease. By analyzing speech patterns, the app utilizes advanced audio processing techniques and a TensorFlow Lite (TFLite) model to predict potential early signs of dementia.

This app is an **ALX Webstack Portfolio Project**, demonstrating proficiency in mobile app development, backend integration, machine learning, and containerized deployments.

---

## Table of Contents

- [Features](#features)
- [Project Architecture](#project-architecture)
- [Setup Instructions](#setup-instructions)
- [Usage Guidelines](#usage-guidelines)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Speech Recording**: Records a user's speech through the device microphone.
- **Audio Preprocessing**: Extracts Mel-Frequency Cepstral Coefficients (MFCCs) for analysis.
- **Machine Learning Inference**: Uses a TensorFlow Lite (TFLite) model to analyze MFCCs and predict early dementia symptoms.
- **Backend Integration**: Processes requests and provides additional functionalities via a Flask backend.
- **Dockerized Backend**: Ensures efficient deployment and portability of the backend using Docker.
- **User-Friendly UI**: Intuitive interface designed for ease of use.

---

## Project Architecture

The Dementia Detection App is structured as follows:

1. **Frontend**:
   - Built with **Flutter** for a seamless cross-platform experience on both iOS and Android.
   - Utilizes Flutter packages like `audio_recorder`, and `path_provider` for speech recording and processing.

2. **Audio Preprocessing**:
   - Extracts Mel-Frequency Cepstral Coefficients (MFCCs) from recorded audio for machine learning analysis.
   - Uses native **TensorFlow Lite** integration in Flask.

3. **Backend**:
   - Developed using **Flask**, the backend handles requests from the Flutter app and processes data as needed.
   - Includes APIs for logging, data processing, and model validation.

4. **Model**:
   - A pre-trained **TFLite model** predicts patterns indicative of dementia.

5. **Containerization**:
   - The Flask backend is containerized using **Docker** for easier deployment and scalability.

---

## Setup Instructions

Follow these steps to set up and run the Dementia Detection App locally:

### Prerequisites

- **Frontend**:
  - Flutter SDK (version >= 3.4.3)
  - Android Studio or Xcode (for Android and iOS development)

- **Backend**:
  - Docker
  - Docker Compose

- **Machine Learning**:
  - TensorFlow Lite (TFLite) model file (`.tflite`)

### Frontend Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repository-url/dementia-early-detection-app.git
   cd dementia-early-detection-app/dementia-detection-app
   ```

2. **Install Dependencies**:
   ```bash
   flutter pub get
   ```

3. **Run the App**:
   - For Android:
     ```bash
     flutter run
     ```
   - For iOS:
     ```bash
     flutter run --release
     ```

### Backend Installation

1. **Navigate to the Backend Directory**:
   ```bash
   cd dementia-early-detection-app/backend_app
   ```

2. **Build the Docker Image**:
   ```bash
   docker build -t dementia-backend .
   ```

3. **Run the Docker Container**:
   ```bash
   docker run -p 5000:5000 dementia-backend
   ```

   The backend will now be available at `http://localhost:5000`.

4. **Test the Backend API** (Optional):
   Use tools like `curl` or Postman to test the endpoints.

### Running with Docker Compose

For easier management of multi-container environments, use Docker Compose:

1. **Start the Application**:
   ```bash
   docker-compose up
   ```

2. **Stop the Application**:
   ```bash
   docker-compose down
   ```

---

## Usage Guidelines

1. Launch the app on your mobile device.
2. Use the **Record Speech** button to record your voice.
3. Wait for the app to process the recording and send it to the Flask backend.
4. The backend will process the data and return the prediction to the app.
5. View the result indicating whether early dementia symptoms are detected.

**Note**: This app is intended for research and educational purposes only. It should not be used as a substitute for professional medical advice.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request describing your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

This project is part of my **first** professional research project and was inspired by the need to leverage technology for advancements in healthcare. Special thanks to the creators of TensorFlow Lite, Flask, Docker, and the Flutter community for their support and resources.

---
