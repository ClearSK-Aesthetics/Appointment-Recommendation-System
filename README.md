 ClearSK Appointment Recommendation System

The ClearSK Appointment Recommendation System is a tool designed to recommend the most suitable clinic locations based on a user's home and work postal codes, preferred days of the week, and preferred appointment time segments.

This system helps users conveniently identify which ClearSK clinics are most accessible for them, improving booking experience and optimizing clinic assignment.

Features
1. Distance-Based Clinic Recommendation
- Converts Singapore 6-digit postal codes into geographic coordinates using Geocoding (Google Maps API or internal postal database).
- Calculates straight-line distance (Haversine formula) between user locations and clinic locations.
- Recommends the **nearest clinic to Home** and **nearest clinic to Work**.
- Handles duplication: if both nearest results are the same clinic, the system provides a second-nearest option.


2. User Preference Collection
The system collects:
Home postal code
Work postal code
Preferred Days of the Week (user selects 2)
Preferred Time Slots:
2pm  
  - PM slot — 4pm to 6pm or 7pm to 9pm

Preferences are displayed for user confirmation.

---

3. Simple and Clean Streamlit UI
- Web-based interface built with Streamlit
- Fast and mobile-friendly
- Easy for clinic staff and customers to use
- Minimal setup required

---
 System Architecture

