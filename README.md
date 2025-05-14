# 🔵 Indoor Thermal Comfort Monitor (Simulation)

A modern, interactive Streamlit web app to monitor, analyze, and visualize indoor thermal comfort in real time. Designed for researchers, building managers, and anyone interested in understanding and optimizing indoor comfort conditions.

---

## 🚀 Features

- **Real-Time PMV/PPD Calculation:**
  - Uses the ISO 7730:2005 standard for accurate comfort metrics.
- **Customizable Environmental Parameters:**
  - Adjust air temperature, mean radiant temperature, humidity, air velocity, metabolic rate, and clothing insulation.
- **User-Defined Comfort Thresholds:**
  - Set your own PMV and PPD comfort ranges.
- **Session Management:**
  - Save and load session data (JSON), including all parameters and history.
- **Session Tagging & Color Coding:**
  - Tag sessions (e.g., Office, Home) and assign a color for easy identification.
- **Live Metrics Dashboard:**
  - Beautiful, responsive metric cards for all key parameters.
- **Comfort Analysis Visualizations:**
  - PMV/PPD history charts
  - Comfort timeline visualization
  - Comfort vs Discomfort pie chart
  - Session statistics (min, max, avg)
- **User Notes:**
  - Add and save notes for each session.
- **User Feedback Poll:**
  - Users can rate their comfort (Too Cold, Comfortable, Too Hot) and see a live pie chart of all feedback.
- **Downloadable History:**
  - Export PMV/PPD history as CSV.
- **Reset Options:**
  - Reset PMV/PPD history with one click.
- **Responsive UI:**
  - Works in both light and dark mode, with custom CSS for a modern look.
- **Help & Documentation:**
  - Built-in help section for new users.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Vishnu252005/Indoor-Thermal-Comfort-Monitor.git
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

4. **Open in your browser:**
   - By default, visit [http://localhost:8501](http://localhost:8501)

---

## 🖥️ Usage Guide

### 1. **Adjust Parameters**
- Use the sidebar to set environmental and personal parameters.
- All changes update the comfort metrics and charts in real time.

### 2. **Set Comfort Thresholds**
- Define your own PMV/PPD comfort zone for personalized recommendations.

### 3. **Session Management**
- Save your session (all data and settings) as a JSON file.
- Load previous sessions to continue analysis or compare results.

### 4. **Tag & Color Sessions**
- Add a tag (e.g., "Office") and pick a color for easy session identification.

### 5. **User Notes**
- Add notes for each session in the sidebar.

### 6. **User Feedback Poll**
- Rate your comfort using the poll and see live feedback statistics.

### 7. **Download History**
- Download your PMV/PPD history as a CSV file for further analysis.

### 8. **Visualizations**
- View real-time and historical comfort data with:
  - PMV/PPD line charts
  - Comfort timeline (color-coded)
  - Comfort vs Discomfort pie chart
  - Session statistics (min, max, avg)

### 9. **Help & Documentation**
- Expand the help section in the app for quick instructions and metric explanations.

---

## 📊 Example Screenshots

> _Add screenshots of the app in both light and dark mode here._

---

## 📦 Dependencies

- streamlit
- pandas
- numpy
- altair
- qrcode
- Pillow
- pythermalcomfort

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Credits

- Built with [Streamlit](https://streamlit.io/)
- PMV/PPD calculations via [pythermalcomfort](https://github.com/CenterForTheBuiltEnvironment/pythermalcomfort)
- UI inspired by modern dashboard best practices

---

## 💡 Contributing

Pull requests and suggestions are welcome! Please open an issue or submit a PR. 