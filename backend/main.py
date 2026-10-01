import os
import io
import re
from urllib.parse import urlparse

import cloudinary
import cloudinary.uploader
import cloudinary.api

from cloudinary import CloudinaryImage
from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image, ImageDraw, ImageFont

import pytesseract


# =========================================================
# TESSERACT CONFIGURATION
# =========================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

cloudinary_url = os.getenv("CLOUDINARY_URL")

if not cloudinary_url:
    raise RuntimeError("CLOUDINARY_URL not found in .env")


# =========================================================
# CLOUDINARY CONFIGURATION
# =========================================================

parsed = urlparse(cloudinary_url)

cloud_name = parsed.hostname
api_key = parsed.username
api_secret = parsed.password

print("Cloud name found:", bool(cloud_name))
print("API key found:", bool(api_key))
print("API secret found:", bool(api_secret))

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret,
    secure=True
)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="SnapShield AI",
    description="AI-powered image privacy and media protection system",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "status": "success",
        "message": "SnapShield AI backend is running!"
    }


# =========================================================
# CLOUDINARY TEST
# =========================================================

@app.get("/cloudinary-test")
def cloudinary_test():

    try:

        result = cloudinary.uploader.upload(
            "https://res.cloudinary.com/demo/image/upload/sample.jpg",
            public_id="snapshield_test"
        )

        return {
            "status": "success",
            "message": "Cloudinary connection is working!",
            "public_id": result.get("public_id"),
            "url": result.get("secure_url")
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# =========================================================
# UPLOAD IMAGE
# =========================================================

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):

    try:

        contents = await file.read()

        result = cloudinary.uploader.upload(
            contents,
            folder="snapshield"
        )

        return {
            "status": "success",
            "message": "Image uploaded successfully!",
            "filename": file.filename,
            "public_id": result.get("public_id"),
            "url": result.get("secure_url"),
            "width": result.get("width"),
            "height": result.get("height"),
            "format": result.get("format")
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# =========================================================
# IMAGE INFORMATION
# =========================================================

@app.get("/image-info/{public_id:path}")
def image_info(public_id: str):

    try:

        result = cloudinary.api.resource(public_id)

        return {
            "status": "success",
            "public_id": result.get("public_id"),
            "url": result.get("secure_url"),
            "width": result.get("width"),
            "height": result.get("height"),
            "format": result.get("format"),
            "bytes": result.get("bytes"),
            "resource_type": result.get("resource_type")
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# =========================================================
# OPTIMIZE IMAGE
# =========================================================

@app.get("/optimize-image/{public_id:path}")
def optimize_image(public_id: str):

    try:

        optimized_url = CloudinaryImage(
            public_id
        ).build_url(
            transformation=[
                {
                    "quality": "auto",
                    "fetch_format": "auto"
                }
            ]
        )

        return {
            "status": "success",
            "message": "Image optimized successfully!",
            "original_public_id": public_id,
            "optimized_url": optimized_url
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# =========================================================
# REMOVE BACKGROUND
# =========================================================

@app.get("/remove-background/{public_id:path}")
def remove_background(public_id: str):

    try:

        background_removed_url = CloudinaryImage(
            public_id
        ).build_url(
            transformation=[
                {
                    "effect": "background_removal"
                }
            ]
        )

        return {
            "status": "success",
            "message": "Background removal transformation created!",
            "original_public_id": public_id,
            "background_removed_url": background_removed_url
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# =========================================================
# ANALYZE PRIVACY
# =========================================================

@app.post("/analyze-privacy")
async def analyze_privacy(file: UploadFile = File(...)):

    try:

        contents = await file.read()

        image = Image.open(
            io.BytesIO(contents)
        )

        width, height = image.size

        image_format = image.format or "Unknown"

        file_size = len(contents)

        privacy_score = 0

        risks = []

        recommendations = []


        # =================================================
        # FILENAME
        # =================================================

        filename = file.filename or ""

        filename_lower = filename.lower()

        sensitive_filename_patterns = [
            "aadhaar",
            "aadhar",
            "pan",
            "passport",
            "license",
            "licence",
            "id",
            "personal",
            "private",
            "document"
        ]

        filename_sensitive = any(
            pattern in filename_lower
            for pattern in sensitive_filename_patterns
        )

        if filename_sensitive:

            privacy_score += 20

            risks.append({
                "type": "Filename",
                "severity": "Medium",
                "message": "The filename may contain sensitive information."
            })

            recommendations.append(
                "Use a neutral filename before sharing the image."
            )


        # =================================================
        # EXIF
        # =================================================

        exif_data = image.getexif()

        if exif_data and len(exif_data) > 0:

            privacy_score += 20

            risks.append({
                "type": "EXIF Metadata",
                "severity": "Medium",
                "message": "The image contains embedded metadata."
            })

            recommendations.append(
                "Remove metadata before publicly sharing the image."
            )


        # =================================================
        # HIGH RESOLUTION
        # =================================================

        if width >= 4000 or height >= 3000:

            privacy_score += 10

            risks.append({
                "type": "High Resolution",
                "severity": "Low",
                "message": "The image has a very high resolution."
            })

            recommendations.append(
                "Consider resizing the image before public sharing."
            )


        # =================================================
        # LARGE FILE
        # =================================================

        if file_size > 5 * 1024 * 1024:

            privacy_score += 10

            risks.append({
                "type": "Large File",
                "severity": "Low",
                "message": "The image file is relatively large."
            })

            recommendations.append(
                "Optimize or compress the image before sharing."
            )


        # =================================================
        # OCR
        # =================================================

        detected_text = pytesseract.image_to_string(
            image
        ).strip()


        # =================================================
        # EMAIL
        # =================================================

        email_matches = re.findall(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            detected_text
        )


        # =================================================
        # PHONE
        # =================================================

        phone_matches = re.findall(
            r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",
            detected_text
        )


        # =================================================
        # ID
        # =================================================

        id_matches = re.findall(
            r"(?<!\d)\d{12}(?!\d)",
            detected_text
        )


        # =================================================
        # CARD
        # =================================================

        card_matches = re.findall(
            r"(?<!\d)(?:\d{4}[\s-]?){3}\d{4}(?!\d)",
            detected_text
        )


        # =================================================
        # EMAIL RISK
        # =================================================

        if email_matches:

            privacy_score += 25

            risks.append({
                "type": "Email Address",
                "severity": "High",
                "message": "An email address was detected in the image."
            })

            recommendations.append(
                "Blur or remove the email address before sharing."
            )


        # =================================================
        # PHONE RISK
        # =================================================

        if phone_matches:

            privacy_score += 25

            risks.append({
                "type": "Phone Number",
                "severity": "High",
                "message": "A possible phone number was detected in the image."
            })

            recommendations.append(
                "Blur or remove the phone number before sharing."
            )


        # =================================================
        # ID RISK
        # =================================================

        if id_matches:

            privacy_score += 30

            risks.append({
                "type": "Possible ID Number",
                "severity": "High",
                "message": "A long numeric identifier was detected in the image."
            })

            recommendations.append(
                "Do not publicly share documents containing identification numbers."
            )


        # =================================================
        # CARD RISK
        # =================================================

        if card_matches:

            privacy_score += 40

            risks.append({
                "type": "Possible Card Number",
                "severity": "High",
                "message": "A possible card number was detected in the image."
            })

            recommendations.append(
                "Blur or remove card numbers before sharing."
            )


        # =================================================
        # GENERAL OCR
        # =================================================

        if detected_text and len(detected_text) > 20:

            recommendations.append(
                "Review visible text in the image before sharing it publicly."
            )


        # =================================================
        # SCORE
        # =================================================

        privacy_score = min(
            privacy_score,
            100
        )


        # =================================================
        # RISK LEVEL
        # =================================================

        if privacy_score >= 70:

            risk_level = "High Risk"

        elif privacy_score >= 40:

            risk_level = "Medium Risk"

        elif privacy_score >= 20:

            risk_level = "Low-Medium Risk"

        else:

            risk_level = "Low Risk"


        # =================================================
        # RESPONSE
        # =================================================

        return {

            "status": "success",

            "filename": filename,

            "image": {
                "width": width,
                "height": height,
                "format": image_format,
                "file_size": file_size
            },

            "privacy_score": privacy_score,

            "risk_level": risk_level,

            "risk_count": len(risks),

            "risks": risks,

            "recommendations": recommendations,

            "ocr": {

                "text_detected": bool(detected_text),

                "detected_text": detected_text,

                "email_count": len(email_matches),

                "phone_count": len(phone_matches),

                "id_count": len(id_matches),

                "card_count": len(card_matches)
            }
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# =========================================================
# PROTECT IMAGE
# ACTUAL SENSITIVE TEXT REDACTION + DOWNLOAD
# =========================================================

@app.post("/protect-image")
async def protect_image(file: UploadFile = File(...)):

    try:

        # -------------------------------------------------
        # READ IMAGE
        # -------------------------------------------------

        contents = await file.read()

        image = Image.open(
            io.BytesIO(contents)
        ).convert("RGB")


        # -------------------------------------------------
        # OCR WITH BOUNDING BOXES
        # -------------------------------------------------

        ocr_data = pytesseract.image_to_data(
            image,
            output_type=pytesseract.Output.DICT
        )


        # -------------------------------------------------
        # REGEX
        # -------------------------------------------------

        email_regex = re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        )

        phone_regex = re.compile(
            r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)"
        )

        id_regex = re.compile(
            r"(?<!\d)\d{12}(?!\d)"
        )

        card_regex = re.compile(
            r"(?<!\d)(?:\d{4}[\s-]?){3}\d{4}(?!\d)"
        )


        # -------------------------------------------------
        # GROUP WORDS BY LINE
        # -------------------------------------------------

        lines = {}

        total_words = len(
            ocr_data["text"]
        )

        for i in range(total_words):

            text = ocr_data["text"][i].strip()

            if not text:
                continue

            block_num = ocr_data["block_num"][i]
            par_num = ocr_data["par_num"][i]
            line_num = ocr_data["line_num"][i]

            line_key = (
                block_num,
                par_num,
                line_num
            )

            word_info = {

                "text": text,

                "x": ocr_data["left"][i],

                "y": ocr_data["top"][i],

                "w": ocr_data["width"][i],

                "h": ocr_data["height"][i]
            }

            if line_key not in lines:

                lines[line_key] = []

            lines[line_key].append(
                word_info
            )


        # -------------------------------------------------
        # DRAW
        # -------------------------------------------------

        draw = ImageDraw.Draw(
            image
        )

        protected_regions = 0

        detected_sensitive = {

            "emails": 0,

            "phone_numbers": 0,

            "possible_ids": 0,

            "possible_cards": 0
        }


        # -------------------------------------------------
        # PROCESS LINES
        # -------------------------------------------------

        for line_words in lines.values():

            line_words.sort(
                key=lambda item: item["x"]
            )

            line_text = ""

            word_ranges = []

            for word in line_words:

                if line_text:
                    line_text += " "

                start = len(line_text)

                line_text += word["text"]

                end = len(line_text)

                word_ranges.append({

                    "start": start,

                    "end": end,

                    "word": word
                })


            # -------------------------------------------------
            # SEARCH SENSITIVE PATTERNS
            # -------------------------------------------------

            patterns = [

                (
                    email_regex,
                    "emails"
                ),

                (
                    phone_regex,
                    "phone_numbers"
                ),

                (
                    id_regex,
                    "possible_ids"
                ),

                (
                    card_regex,
                    "possible_cards"
                )
            ]

            matched_ranges = []

            for pattern, category in patterns:

                matches = pattern.finditer(
                    line_text
                )

                for match in matches:

                    matched_ranges.append(
                        (
                            match.start(),
                            match.end(),
                            category
                        )
                    )


            # -------------------------------------------------
            # REDACT
            # -------------------------------------------------

            for (
                match_start,
                match_end,
                category
            ) in matched_ranges:

                matched_words = []

                for word_range in word_ranges:

                    if (
                        word_range["end"] > match_start
                        and
                        word_range["start"] < match_end
                    ):

                        matched_words.append(
                            word_range["word"]
                        )


                if not matched_words:
                    continue


                # -------------------------------------------------
                # BOUNDING BOX
                # -------------------------------------------------

                x1 = min(
                    word["x"]
                    for word in matched_words
                )

                y1 = min(
                    word["y"]
                    for word in matched_words
                )

                x2 = max(
                    word["x"] + word["w"]
                    for word in matched_words
                )

                y2 = max(
                    word["y"] + word["h"]
                    for word in matched_words
                )


                # -------------------------------------------------
                # PADDING
                # -------------------------------------------------

                padding_x = max(
                    8,
                    int((x2 - x1) * 0.08)
                )

                padding_y = max(
                    6,
                    int((y2 - y1) * 0.25)
                )

                x1 = max(
                    0,
                    x1 - padding_x
                )

                y1 = max(
                    0,
                    y1 - padding_y
                )

                x2 = min(
                    image.width,
                    x2 + padding_x
                )

                y2 = min(
                    image.height,
                    y2 + padding_y
                )


                # -------------------------------------------------
                # BLACK REDACTION
                # -------------------------------------------------

                draw.rectangle(
                    [
                        x1,
                        y1,
                        x2,
                        y2
                    ],
                    fill=(0, 0, 0)
                )

                protected_regions += 1

                detected_sensitive[
                    category
                ] += 1


        # -------------------------------------------------
        # PROTECTION BANNER
        # -------------------------------------------------

        banner_height = min(
            70,
            max(
                45,
                image.height // 12
            )
        )

        draw.rectangle(
            [
                0,
                0,
                image.width,
                banner_height
            ],
            fill=(120, 20, 20)
        )


        # -------------------------------------------------
        # FONT
        # -------------------------------------------------

        try:

            font = ImageFont.truetype(
                "arial.ttf",
                max(
                    16,
                    image.width // 55
                )
            )

        except:

            font = None


        # -------------------------------------------------
        # BANNER TEXT
        # -------------------------------------------------

        draw.text(
            (
                20,
                banner_height // 4
            ),
            "SNAPSHIELD PROTECTED IMAGE",
            fill=(255, 255, 255),
            font=font
        )


        # -------------------------------------------------
        # SAVE IMAGE
        # -------------------------------------------------

        output = io.BytesIO()

        image.save(
            output,
            format="PNG"
        )

        output.seek(0)


        # -------------------------------------------------
        # UPLOAD PROTECTED IMAGE TO CLOUDINARY
        # -------------------------------------------------

        result = cloudinary.uploader.upload(
            output.getvalue(),
            folder="snapshield/protected",
            resource_type="image"
        )


        # -------------------------------------------------
        # CREATE DOWNLOAD URL
        # -------------------------------------------------

        download_url = CloudinaryImage(
            result.get("public_id")
        ).build_url(
            flags=["attachment"]
        )


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {

            "status": "success",

            "message":
                "Sensitive information was successfully redacted.",

            "protected_url":
                result.get("secure_url"),

            "download_url":
                download_url,

            "public_id":
                result.get("public_id"),

            "protected_regions":
                protected_regions,

            "sensitive_counts":
                detected_sensitive,

            "sensitive_content_found":
                protected_regions > 0
        }


    except Exception as e:

        return {

            "status": "error",

            "message": str(e)
        }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {

        "status": "healthy",

        "service": "SnapShield AI"
    }