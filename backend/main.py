import os
import re
import io
from urllib.parse import urlparse

import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary import CloudinaryImage

import pytesseract
from PIL import Image, ImageDraw

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# CLOUDINARY CONFIGURATION
# =========================================================

cloudinary_url = os.getenv("CLOUDINARY_URL")

if not cloudinary_url:
    raise RuntimeError("CLOUDINARY_URL is not configured")

parsed = urlparse(cloudinary_url)

cloudinary.config(
    cloud_name=parsed.hostname,
    api_key=parsed.username,
    api_secret=parsed.password,
    secure=True
)


# =========================================================
# TESSERACT CONFIGURATION
# =========================================================

if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
else:
    pytesseract.pytesseract.tesseract_cmd = "tesseract"


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="SnapShield AI",
    description="Smart Image Safety & Privacy Scanner",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://snapshield-ai.vercel.app",
        "https://snapshield-ai-git-main-avengers-b5f3.vercel.app",
        "https://snapshield-421g2jhn4-avengers-b5f3.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def root():
    return {
        "status": "success",
        "message": "SnapShield AI backend is running!"
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


# =========================================================
# CLOUDINARY CONNECTION TEST
# =========================================================

@app.get("/cloudinary-test")
def cloudinary_test():
    try:
        result = cloudinary.api.ping()

        return {
            "status": "success",
            "cloudinary": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Cloudinary connection failed: {str(e)}"
        )


# =========================================================
# UPLOAD IMAGE
# =========================================================

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):

    try:

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Empty file"
            )

        result = cloudinary.uploader.upload(
            contents,
            folder="snapshield"
        )

        return {
            "status": "success",
            "message": "Image uploaded successfully",
            "public_id": result.get("public_id"),
            "secure_url": result.get("secure_url"),
            "width": result.get("width"),
            "height": result.get("height"),
            "format": result.get("format"),
            "resource_type": result.get("resource_type")
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


# =========================================================
# IMAGE INFO
# =========================================================

@app.get("/image-info/{public_id:path}")
def image_info(public_id: str):

    try:

        result = cloudinary.api.resource(
            public_id
        )

        return {
            "status": "success",
            "public_id": result.get("public_id"),
            "secure_url": result.get("secure_url"),
            "width": result.get("width"),
            "height": result.get("height"),
            "format": result.get("format"),
            "bytes": result.get("bytes"),
            "created_at": result.get("created_at")
        }

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=f"Image not found: {str(e)}"
        )


# =========================================================
# OPTIMIZE IMAGE
# =========================================================

@app.get("/optimize-image/{public_id:path}")
def optimize_image(public_id: str):

    try:

        optimized_url = CloudinaryImage(
            public_id
        ).build_url(
            quality="auto",
            fetch_format="auto"
        )

        return {
            "status": "success",
            "message": "Optimized image URL generated",
            "optimized_url": optimized_url
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Optimization failed: {str(e)}"
        )


# =========================================================
# REMOVE BACKGROUND
# =========================================================

@app.get("/remove-background/{public_id:path}")
def remove_background(public_id: str):

    try:

        background_removed_url = CloudinaryImage(
            public_id
        ).build_url(
            effect="background_removal"
        )

        return {
            "status": "success",
            "message": "Background removal URL generated",
            "background_removed_url": background_removed_url
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Background removal failed: {str(e)}"
        )


# =========================================================
# PRIVACY ANALYSIS
# =========================================================

@app.post("/analyze-privacy")
async def analyze_privacy(
    file: UploadFile = File(...)
):

    try:

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Empty file"
            )

        image = Image.open(
            io.BytesIO(contents)
        )

        filename = file.filename or ""

        width, height = image.size

        file_size_mb = len(contents) / (
            1024 * 1024
        )

        risks = []

        score = 0

        # -------------------------------------------------
        # FILENAME RISK
        # -------------------------------------------------

        filename_lower = filename.lower()

        filename_keywords = [
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

        filename_risk = any(
            keyword in filename_lower
            for keyword in filename_keywords
        )

        if filename_risk:

            risks.append({
                "type": "Sensitive filename",
                "description":
                    "The filename suggests that the image may contain personal or private information.",
                "severity": "Medium"
            })

            score += 20

        # -------------------------------------------------
        # EXIF RISK
        # -------------------------------------------------

        try:

            exif_data = image.getexif()

            if exif_data:

                risks.append({
                    "type": "EXIF metadata",
                    "description":
                        "The image contains metadata that may reveal information about the image or device.",
                    "severity": "Medium"
                })

                score += 20

        except Exception:
            pass

        # -------------------------------------------------
        # HIGH RESOLUTION RISK
        # -------------------------------------------------

        if width >= 4000 or height >= 3000:

            risks.append({
                "type": "High resolution",
                "description":
                    "High-resolution images may expose more visual information.",
                "severity": "Low"
            })

            score += 10

        # -------------------------------------------------
        # FILE SIZE RISK
        # -------------------------------------------------

        if file_size_mb > 5:

            risks.append({
                "type": "Large file size",
                "description":
                    "The image is larger than 5 MB.",
                "severity": "Low"
            })

            score += 10

        # -------------------------------------------------
        # OCR
        # -------------------------------------------------

        ocr_text = pytesseract.image_to_string(
            image
        )

        # -------------------------------------------------
        # EMAIL DETECTION
        # -------------------------------------------------

        email_pattern = (
            r"\b[A-Za-z0-9._%+-]+@"
            r"[A-Za-z0-9.-]+\."
            r"[A-Za-z]{2,}\b"
        )

        emails = re.findall(
            email_pattern,
            ocr_text
        )

        if emails:

            risks.append({
                "type": "Email address",
                "description":
                    f"Detected {len(emails)} email address(es).",
                "severity": "High"
            })

            score += 25

        # -------------------------------------------------
        # PHONE DETECTION
        # -------------------------------------------------

        phone_pattern = (
            r"(?:\+91[\s-]?)?"
            r"[6-9]\d{9}"
        )

        phones = re.findall(
            phone_pattern,
            ocr_text
        )

        if phones:

            risks.append({
                "type": "Phone number",
                "description":
                    f"Detected {len(phones)} phone number(s).",
                "severity": "High"
            })

            score += 25

        # -------------------------------------------------
        # 12 DIGIT ID DETECTION
        # -------------------------------------------------

        id_pattern = r"\b\d{12}\b"

        ids = re.findall(
            id_pattern,
            ocr_text
        )

        if ids:

            risks.append({
                "type": "12-digit ID",
                "description":
                    f"Detected {len(ids)} possible 12-digit ID number(s).",
                "severity": "High"
            })

            score += 30

        # -------------------------------------------------
        # CARD-LIKE NUMBER DETECTION
        # -------------------------------------------------

        card_pattern = (
            r"\b(?:\d{4}[\s-]?){3}\d{4}\b"
        )

        cards = re.findall(
            card_pattern,
            ocr_text
        )

        if cards:

            risks.append({
                "type": "Card-like number",
                "description":
                    f"Detected {len(cards)} possible card number(s).",
                "severity": "Critical"
            })

            score += 40

        # -------------------------------------------------
        # SCORE LIMIT
        # -------------------------------------------------

        score = min(score, 100)

        # -------------------------------------------------
        # RISK LEVEL
        # -------------------------------------------------

        if score >= 70:

            risk_level = "High Risk"

        elif score >= 40:

            risk_level = "Medium Risk"

        elif score >= 20:

            risk_level = "Low-Medium"

        else:

            risk_level = "Low Risk"

        # -------------------------------------------------
        # RECOMMENDATIONS
        # -------------------------------------------------

        recommendations = []

        if emails:
            recommendations.append(
                "Redact detected email addresses."
            )

        if phones:
            recommendations.append(
                "Redact detected phone numbers."
            )

        if ids:
            recommendations.append(
                "Redact detected identification numbers."
            )

        if cards:
            recommendations.append(
                "Redact detected card-like numbers."
            )

        if filename_risk:
            recommendations.append(
                "Avoid sharing files with sensitive filenames."
            )

        if not recommendations:

            recommendations.append(
                "No major sensitive information was detected."
            )

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        return {
            "status": "success",
            "privacy_score": score,
            "risk_score": score,
            "risk_level": risk_level,
            "risks": risks,
            "recommendations": recommendations,
            "ocr_text": ocr_text,
            "sensitive_data": {
                "emails": len(emails),
                "phones": len(phones),
                "ids": len(ids),
                "cards": len(cards)
            },
            "email_count": len(emails),
            "phone_count": len(phones),
            "id_count": len(ids),
            "card_count": len(cards)
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Privacy analysis failed: {str(e)}"
        )


# =========================================================
# PROTECT IMAGE
# =========================================================

@app.post("/protect-image")
async def protect_image(
    file: UploadFile = File(...)
):

    try:

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Empty file"
            )

        image = Image.open(
            io.BytesIO(contents)
        ).convert("RGB")

        # -------------------------------------------------
        # OCR DATA
        # -------------------------------------------------

        data = pytesseract.image_to_data(
            image,
            output_type=pytesseract.Output.DICT
        )

        draw = ImageDraw.Draw(image)

        protected_regions = []

        email_count = 0
        phone_count = 0
        id_count = 0
        card_count = 0

        # -------------------------------------------------
        # PROCESS OCR WORDS
        # -------------------------------------------------

        n = len(data["text"])

        for i in range(n):

            text = data["text"][i].strip()

            if not text:
                continue

            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]

            if w <= 0 or h <= 0:
                continue

            # -------------------------------------------------
            # EMAIL
            # -------------------------------------------------

            if re.search(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                text
            ):

                draw.rectangle(
                    [x, y, x + w, y + h],
                    fill="black"
                )

                protected_regions.append({
                    "type": "email",
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                })

                email_count += 1

            # -------------------------------------------------
            # PHONE
            # -------------------------------------------------

            elif re.search(
                r"(?:\+91[\s-]?)?[6-9]\d{9}",
                text
            ):

                draw.rectangle(
                    [x, y, x + w, y + h],
                    fill="black"
                )

                protected_regions.append({
                    "type": "phone",
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                })

                phone_count += 1

            # -------------------------------------------------
            # 12 DIGIT ID
            # -------------------------------------------------

            elif re.search(
                r"\b\d{12}\b",
                text
            ):

                draw.rectangle(
                    [x, y, x + w, y + h],
                    fill="black"
                )

                protected_regions.append({
                    "type": "id",
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                })

                id_count += 1

            # -------------------------------------------------
            # CARD
            # -------------------------------------------------

            elif re.search(
                r"(?:\d{4}[\s-]?){3}\d{4}",
                text
            ):

                draw.rectangle(
                    [x, y, x + w, y + h],
                    fill="black"
                )

                protected_regions.append({
                    "type": "card",
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                })

                card_count += 1

        # -------------------------------------------------
        # ADD PROTECTED IMAGE BANNER
        # -------------------------------------------------

        banner_height = 70

        protected_image = Image.new(
            "RGB",
            (
                image.width,
                image.height + banner_height
            ),
            "white"
        )

        protected_image.paste(
            image,
            (0, banner_height)
        )

        banner_draw = ImageDraw.Draw(
            protected_image
        )

        banner_draw.rectangle(
            [
                0,
                0,
                image.width,
                banner_height
            ],
            fill="red"
        )

        banner_draw.text(
            (20, 20),
            "SNAPSHIELD PROTECTED IMAGE",
            fill="white"
        )

        # -------------------------------------------------
        # SAVE TO MEMORY
        # -------------------------------------------------

        output = io.BytesIO()

        protected_image.save(
            output,
            format="PNG"
        )

        output.seek(0)

        # -------------------------------------------------
        # UPLOAD TO CLOUDINARY
        # -------------------------------------------------

        result = cloudinary.uploader.upload(
            output.getvalue(),
            folder="snapshield/protected",
            resource_type="image",
            format="png"
        )

        protected_url = result.get(
            "secure_url"
        )

        protected_public_id = result.get(
            "public_id"
        )

        # -------------------------------------------------
        # DOWNLOAD URL
        # -------------------------------------------------

        download_url = CloudinaryImage(
            protected_public_id
        ).build_url(
            flags=["attachment"]
        )

        total_regions = len(
            protected_regions
        )

        return {
            "status": "success",
            "message": "Image protected successfully",
            "protected_url": protected_url,
            "download_url": download_url,
            "public_id": protected_public_id,
            "protected_regions": protected_regions,
            "protected_region_count": total_regions,
            "sensitive_content_found": total_regions > 0,
            "sensitive_counts": {
                "emails": email_count,
                "phones": phone_count,
                "ids": id_count,
                "cards": card_count
            }
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Protection failed: {str(e)}"
        )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(
            os.getenv("PORT", 8000)
        )
    )