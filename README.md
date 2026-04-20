#  Delivery Visibility Dashboard

##  Overview
This project is a Supply Chain Management dashboard that provides real-time visibility into shipment tracking and delivery status.

##  Features
- Track shipment updates
- Add/Delete tracking records
- KPI dashboard (Total updates, delays, shipments)
- Status and location analysis
- Delay prediction using ETA logic

##  Tech Stack
- Python
- Streamlit
- SQLite
- Pandas
- 
 ##  Database
The project uses SQLite (`delivery.db`) to store shipment tracking data.  
Each record represents a tracking update containing shipment ID, timestamp, location, and status.

##  ML Component
A rule-based delay prediction approach is implemented using ETA comparison.  
If the current time exceeds the expected delivery time (ETA) and the shipment is not delivered, it is classified as delayed.  
This serves as a foundation for future machine learning-based prediction models.
  

##  How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
