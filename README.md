# 🛡️ SnapShield AI

### AI-Powered Image Privacy & Safety Scanner

SnapShield AI is an AI-powered image privacy and safety scanner that analyzes images for sensitive information before they are shared online.

It uses OCR-based detection to identify potentially sensitive information such as email addresses, phone numbers, personal identification numbers, and card-like numbers. When sensitive information is detected, SnapShield AI can automatically redact those regions and generate a protected version of the image.

The project also uses Cloudinary for secure media storage, image optimization, background removal, and delivery.

---

## 🎯 Problem Statement

Images shared online can accidentally expose sensitive personal information.

Examples include:

- Email addresses
- Phone numbers
- Personal identification numbers
- Card numbers
- Metadata
- High-resolution personal documents

Users may not notice this information before uploading or sharing an image.

### SnapShield AI solves this problem by:

1. Uploading the image
2. Scanning the image using OCR
3. Detecting potential privacy risks
4. Calculating a privacy risk score
5. Showing detected risks and recommendations
6. Redacting detected sensitive information
7. Uploading the protected image to Cloudinary
8. Providing a protected image for preview and download

---

## 🚀 Key Features

### 🔍 Privacy Risk Analysis

SnapShield AI analyzes uploaded images and calculates a privacy risk score from 0–100.

Risk levels include:

- **Low Risk**
- **Low-Medium Risk**
- **Medium Risk**
- **High Risk**

The scanner considers factors such as:

- Sensitive filenames
- EXIF metadata
- High-resolution images
- Large file sizes
- Email addresses
- Phone numbers
- 12-digit identification numbers
- Card-like numbers

---

### 🧠 OCR-Based Sensitive Data Detection

SnapShield AI uses **Tesseract OCR** to extract text from images.

It then analyzes the extracted text for patterns such as:

- Email addresses
- Indian phone numbers
- 12-digit identification numbers
- 16-digit card-like numbers

---

### 🔒 Sensitive Information Protection

When sensitive information is detected, SnapShield AI can automatically protect it.

Detected regions are covered using black redaction boxes.

Example:

```text
Email:  ███████████████████

Phone:  ███████████████

ID:     ███████████████
```

The protected image is then uploaded to Cloudinary.

---

### ☁️ Cloudinary Media Pipeline

Cloudinary is an important part of the SnapShield AI workflow.

It is used for:

- Image upload
- Media storage
- Image delivery
- Image optimization
- Background removal
- Protected-image storage
- Downloadable protected images

The workflow is:

```text
User Image
    ↓
SnapShield AI
    ↓
OCR Analysis
    ↓
Privacy Risk Detection
    ↓
Sensitive Data Detection
    ↓
Redaction
    ↓
Cloudinary
    ↓
Protected Image
    ↓
Preview / Download
```

---

### ⚡ Image Optimization

SnapShield AI can generate an optimized Cloudinary image URL using automatic:

- Quality optimization
- Format selection

Cloudinary transformations are used to generate optimized media for delivery.

---

### 🖼️ Background Removal

SnapShield AI also integrates Cloudinary background removal transformations.

This allows the application to generate a version of an uploaded image with its background removed.

---

### 📥 Protected Image Download

After sensitive information is redacted, SnapShield AI generates a downloadable version of the protected image.

Users can:

- Preview the protected image
- Open the protected image
- Download the protected image
- Share the protected version instead of the original

---

# 🏆 Hackathon Track

## PS-01 — AI Media Pipelines

SnapShield AI is developed for the:

**Pixels to Products — Cloudinary AI Hackathon 2026**

Track:

**PS-01 — AI Media Pipelines**

The project demonstrates an automated media workflow that:

```text
Ingests
   ↓
Analyzes
   ↓
Protects
   ↓
Transforms
   ↓
Optimizes
   ↓
Delivers
```

Cloudinary is integrated directly into this media pipeline.

---

# 🧰 Technology Stack

## Frontend

- React.js
- Vite
- JavaScript
- CSS

## Backend

- Python
- FastAPI
- Uvicorn

## AI / Image Processing

- Tesseract OCR
- Pytesseract
- Pillow
- Regular-expression based sensitive-data detection

## Cloud / Media

- Cloudinary

## Development Tools

- PyCharm
- Git
- GitHub

---

# 📁 Project Structure

```text
SnapShield-AI/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .gitignore
├── LICENSE
└── README.md
```

---

# ⚙️ Local Installation

## 1. Clone the repository

```bash
git clone https://github.com/srija14008-cmd/pixels-to-products-cloudinary-ai-hackathon-2026-avengers.git
```

Move into the project:

```bash
cd pixels-to-products-cloudinary-ai-hackathon-2026-avengers
```

---

# 🐍 Backend Setup

Move into the backend:

```bash
cd backend
```

Create and activate a virtual environment if required:

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create:

```text
backend/.env
```

Add your Cloudinary configuration:

```env
CLOUDINARY_URL=cloudinary://YOUR_API_KEY:YOUR_API_SECRET@YOUR_CLOUD_NAME
```

### Important

Never commit `.env` to GitHub.

The project `.gitignore` already excludes environment files.

---

# 🔎 Tesseract OCR Setup

SnapShield AI uses Tesseract OCR for text detection.

Install Tesseract OCR on your system and make sure the executable is available.

On Windows, the application can use:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

The backend checks this path when available.

---

# ▶️ Run the Backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# ⚛️ Frontend Setup

Open another terminal.

Move into:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

The Vite development server will provide the frontend URL in the terminal.

---

# 🧪 How to Test SnapShield AI

### Step 1

Open the SnapShield AI frontend.

### Step 2

Select an image using:

**Browse Files**

### Step 3

Click:

**Scan Image**

### Step 4

SnapShield AI uploads the image and analyzes it.

### Step 5

Review:

- Privacy score
- Risk level
- Detected risks
- OCR text
- Sensitive information counts
- Recommendations

### Step 6

If sensitive information is detected, use:

**Protect Sensitive Content**

### Step 7

SnapShield AI creates a protected version of the image.

### Step 8

Preview or download the protected image.

---

# 🔗 API Endpoints

The FastAPI backend provides the following endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Backend status |
| GET | `/health` | Health check |
| GET | `/cloudinary-test` | Test Cloudinary connection |
| POST | `/upload-image` | Upload image to Cloudinary |
| GET | `/image-info/{public_id}` | Retrieve image information |
| GET | `/optimize-image/{public_id}` | Generate optimized image |
| GET | `/remove-background/{public_id}` | Generate background-removed image |
| POST | `/analyze-privacy` | Analyze privacy risks |
| POST | `/protect-image` | Detect and redact sensitive information |

---

# 🛡️ Privacy Protection Workflow

```text
                    ┌──────────────────┐
                    │   Upload Image   │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │    Cloudinary    │
                    │      Upload      │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │    OCR Scan      │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Privacy Analysis │
                    └────────┬─────────┘
                             ↓
                ┌──────────────────────────┐
                │ Sensitive Data Detection│
                └────────────┬─────────────┘
                             ↓
                    ┌──────────────────┐
                    │     Redaction    │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │    Cloudinary    │
                    │ Protected Image  │
                    └────────┬─────────┘
                             ↓
                 ┌───────────────────────┐
                 │ Preview / Download    │
                 └───────────────────────┘
```

---

# ☁️ Cloudinary Integration

Cloudinary is integrated into the core media workflow.

### Image Upload

Images are uploaded to Cloudinary under:

```text
snapshield
```

### Protected Images

Protected images are stored under:

```text
snapshield/protected
```

### Optimization

Cloudinary transformations are used for automatic:

```text
quality = auto
format = auto
```

### Background Removal

Cloudinary background-removal transformation is used to generate background-free versions.

### Delivery

Cloudinary secure URLs are used for image preview and delivery.

---

# 🔒 Security

SnapShield AI follows basic credential protection practices.

Sensitive configuration such as:

```text
.env
```

is excluded from the Git repository.

Never expose:

- Cloudinary API secrets
- Environment variables
- Private credentials

---

# 🎥 Demo

### Live Demo

Coming soon.

### Demo Video

Coming soon.

---

# 👥 Team

## Team Avengers

**Project:** SnapShield AI

**Hackathon:** Pixels to Products — Cloudinary AI Hackathon 2026

**Track:** PS-01 — AI Media Pipelines

---

# 📌 Project Vision

SnapShield AI aims to make image sharing safer by helping users identify and protect sensitive information before publishing or sharing images online.

Instead of manually checking every image, SnapShield AI combines:

```text
OCR
+
Privacy Risk Analysis
+
Sensitive Data Detection
+
Automatic Redaction
+
Cloudinary Media Processing
```

into a single workflow.

---

## 📄 License

This project is licensed under the MIT License.