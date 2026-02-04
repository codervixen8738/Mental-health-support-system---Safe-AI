# Mental-health-support-system---Safe-AI
End-to-End Deep Learning Mental Health Support System 
# 🧠 SAFE-MIND AI

**An End-to-End Deep Learning Mental Health Support System for Sexual Assault Survivors**

SAFE-MIND AI is a responsible, trauma‑informed AI system designed to support early detection of **PTSD and sleep disturbances** in sexual assault survivors. The project integrates **TensorFlow deep learning**, **clinical + synthetic data augmentation**, a **mental‑health chatbot**, **emergency support suggestions**, and **automated report generation** into a deployable full‑stack application.

> ⚠️ This system is for educational and research purposes only and does **not** provide medical diagnosis.

---

## 🚀 Key Features

* **Deep Learning Risk Prediction**
  TensorFlow/Keras model predicting PTSD & sleep‑disturbance risk levels (Low / Moderate / High).

* **Dataset Engineering & Augmentation**
  Merges a small clinical PTSD dataset with **5,000+ synthetically generated samples** to improve robustness.

* **Trauma‑Informed Chatbot**
  Supportive, non‑judgmental conversational AI designed specifically for survivors.

* **Emergency & Safety Suggestions**
  Context‑aware recommendations and quick‑dial guidance for:

  * Medical emergencies
  * Crisis & safety helplines
  * Trusted contacts

* **Automated Report Generation**
  Generates anonymized mental‑health reports summarizing:

  * Risk level
  * Model confidence
  * Personalized recommendations

* **Full‑Stack Integration**
  Frontend UI connected to trained models, chatbot, and backend APIs.

---

## 🧠 Tech Stack

* **Deep Learning:** TensorFlow, Keras
* **ML & Data:** NumPy, Pandas, Scikit‑learn
* **Backend:** Flask
* **Frontend:** Streamlit
* **Chatbot:** Rule‑based safety layer (AWS Lex/Bedrock ready)
* **Reporting:** ReportLab (PDF generation)

---

## 📊 Dataset Details

* **Primary Dataset:** Sleep & PTSD After Sexual Assault (Clinical Dataset)
* **Augmentation Techniques:**

  * Bootstrapping
  * Noise injection
  * Statistical sampling
* **Final Dataset Size:** 5,000+ records
* **Target Outputs:**

  * PTSD Risk
  * Sleep Disturbance Severity

> 🔒 All data used is anonymized. No personally identifiable information is stored.

---

## 🏗️ System Architecture

1. User inputs sleep & psychological indicators
2. Deep learning model predicts PTSD risk
3. Chatbot provides trauma‑informed support
4. Emergency suggestions triggered for high‑risk cases
5. Automated PDF report generated

---

## 📂 Project Structure

```
SAFE-MIND-AI/
│── data/
│── model/
│── chatbot/
│── backend/
│── frontend/
│── requirements.txt
│── README.md
```

---

## ▶️ How to Run Locally

```bash
pip install -r requirements.txt
python model/train_model.py
python backend/app.py
streamlit run frontend/streamlit_app.py
```

---

## 🎯 Use Cases

* Early PTSD screening support
* Mental health research & analytics
* NGO & healthcare assistive tools
* Academic & AI/ML portfolio project

---

## ⚖️ Ethical Considerations

* Trauma‑informed responses only
* No medical diagnosis claims
* Emergency escalation for high‑risk cases
* Privacy‑first and anonymized data handling

---

## 🧑‍💻 Author

**Vaishnavi Srivastava**
AI / ML Engineer | Deep Learning | 

---

## ⭐ Future Enhancements

* AWS Lex / Bedrock chatbot integration
* Multilingual support (English + Hindi)
* Voice‑based distress detection
* Mobile application deployment
* Clinical validation studies

---

💙 SAFE‑MIND AI is built to support survivors with empathy, ethics, and responsible AI design.

