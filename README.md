# Megabus Price Tracker

<p align="center">
  <img src="https://via.placeholder.com/600x300?text=Screenshot+1" alt="Screenshot 1" />
</p>
<p align="center">
  <img src="https://via.placeholder.com/600x300?text=Screenshot+2" alt="Screenshot 2" />
</p>

Megabus Price Tracker is a web app that monitors Megabus ticket prices and sends you an email alert when prices match your preferred criteria. Built with affordability, speed, and simplicity in mind — perfect for budget travelers who want to catch deals without constantly refreshing the Megabus site.

---

## ✨ Features

- 🔍 Search for Megabus trips between Canadian cities  
- 🎯 Set custom filters: date range, price range, number of passengers  
- 📬 Receive real-time email alerts when matching tickets are found  
- 🔐 Secure login system using Firebase Authentication  
- 🗃️ Tracker data stored in Firebase Firestore  
- 🚀 Automated price checks every 3 hours using GitHub Actions  
- 🧹 Auto-deletes trackers after a match is found or when past their end date

---

## 🛠 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)  
- **Database**: Firebase Firestore  
- **Authentication**: Firebase Auth  
- **Email Service**: AWS SES  
- **Automation**: GitHub Actions  
- **Backend Logic**: Python (with `requests`, `pytz`, `firebase-admin`, etc.)

---

## 📌 Live Demo

[🔗 Streamlit App (Insert your link here)](https://your-streamlit-app-link)

---

## 🛡️ Security

- Sensitive data (e.g., API keys, credentials) is stored securely using `secrets.toml` in Streamlit and GitHub Actions secrets.
- `.env` and sensitive files are gitignored and excluded from version control.

---

## 💡 Future Improvements

- SMS notifications  
- User dashboard to manage active trackers  
- Price history visualizations

---

## 📬 Contact

For inquiries or feedback, feel free to reach out: **janekhuong05@gmail.com**

---

