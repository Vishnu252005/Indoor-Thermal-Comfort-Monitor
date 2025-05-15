# 🔵 Indoor Thermal Comfort Monitor

A modern, interactive Streamlit web application for real-time thermal comfort monitoring and analysis. This application calculates and visualizes PMV (Predicted Mean Vote) and PPD (Predicted Percentage of Dissatisfied) values based on environmental parameters using the ISO 7730-2005 standard.

## 📁 Project Structure

```
thermal-comfort-monitor/
├── app.py                 # Main application file
├── requirements.txt       # Project dependencies
├── README.md             # Project documentation
├── calculations/         # Calculation modules
│   └── thermal_comfort.py # PMV/PPD calculations
├── components/           # UI components
│   └── ui_components.py  # Reusable UI elements
├── sensors/             # Sensor interface
│   └── sensor_interface.py # Arduino sensor integration
├── styles/              # Custom styling
│   └── custom_css.py    # Custom CSS styles
└── utils/               # Utility functions
    └── helpers.py       # Helper functions
```

## ✨ Key Features

### 1. Real-Time Monitoring
- Live PMV/PPD calculations using ISO 7730-2005 model
- Instant updates of comfort metrics
- Real-time visualization of comfort status
- Optional Arduino sensor integration for automatic data collection

### 2. Environmental Parameters
- Air Temperature (°C)
- Mean Radiant Temperature (°C)
- Relative Humidity (%)
- Air Velocity (m/s)
- Metabolic Rate (met)
- Clothing Insulation (clo)
- Automatic sensor readings (when using Arduino)

### 3. Interactive Visualizations
- PMV History Chart
- PPD History Chart
- Comfort Timeline
- Comfort vs Discomfort Statistics
- User Feedback Pie Chart

### 4. Session Management
- Save session data (JSON format)
- Load previous sessions
- Session tagging and color coding
- User notes for each session

### 5. Customization Options
- Customizable app title and subtitle
- Session tag and color selection
- Adjustable comfort thresholds
- Modern, responsive UI design

### 6. User Feedback System
- Real-time comfort feedback collection
- Visual feedback statistics
- Three-level comfort rating (Too Cold, Comfortable, Too Hot)

### 7. Sensor Integration
- Arduino-compatible sensor support
- Real-time environmental data collection
- Automatic parameter updates
- Easy sensor connection/disconnection
- Support for multiple sensor types:
  - Temperature sensors
  - Humidity sensors
  - Air velocity sensors
  - Mean radiant temperature sensors

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/thermal-comfort-monitor.git
   cd thermal-comfort-monitor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## 📖 Detailed Usage Guide

### 1. Setting Up Parameters
- Use the sidebar to adjust all environmental parameters
- Set your comfort thresholds (PMV and PPD ranges)
- Customize the app appearance with title, subtitle, and colors

### 2. Monitoring Comfort
- View real-time PMV/PPD values
- Check comfort status indicators
- Monitor environmental parameters
- Track session duration

### 3. Analyzing Data
- View historical PMV/PPD trends
- Analyze comfort timeline
- Check comfort statistics
- Review user feedback distribution

### 4. Session Management
- Save current session data
- Load previous sessions
- Add session notes
- Tag sessions for easy identification

### 5. User Feedback
- Submit comfort feedback
- View feedback statistics
- Track comfort trends over time

### 6. Using Sensors (Optional)
1. Connect your Arduino with compatible sensors
2. Upload the provided Arduino code to your board
3. Uncomment the sensor interface code in app.py
4. Update the COM port in the code if needed
5. Click "Connect to Sensors" in the sidebar
6. View real-time sensor readings and automatic updates

## 🔧 Technical Details

### PMV (Predicted Mean Vote)
- Range: -3 (cold) to +3 (hot)
- Comfort zone: -0.5 to +0.5
- Based on ISO 7730-2005 standard

### PPD (Predicted Percentage of Dissatisfied)
- Range: 0% to 100%
- Comfort threshold: < 10%
- Calculated from PMV values

### Sensor Integration
- Uses pyserial for Arduino communication
- Supports multiple sensor types
- Automatic data parsing and validation
- Error handling for connection issues

## 📦 Dependencies

- streamlit>=1.24.0
- pandas>=1.5.0
- numpy>=1.21.0
- altair>=4.2.0
- pythermalcomfort>=2.0.0
- Pillow>=9.0.0
- qrcode>=7.3.1
- pyserial>=3.5 (for sensor integration)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- UI inspired by modern dashboard best practices
- Sensor integration based on Arduino and pyserial