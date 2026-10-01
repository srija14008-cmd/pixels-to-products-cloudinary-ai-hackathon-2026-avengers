import { useState } from "react";
import "./index.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [optimizedUrl, setOptimizedUrl] = useState(null);
  const [backgroundRemovedUrl, setBackgroundRemovedUrl] = useState(null);
  const [privacyResult, setPrivacyResult] = useState(null);
  const [protectedUrl, setProtectedUrl] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // =========================================================
  // PRODUCTION BACKEND
  // =========================================================

  const API_URL = "https://snapshield-ai-2026.onrender.com";

  // =========================================================
  // FILE SELECTION
  // =========================================================

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    setSelectedFile(file);
    setUploadResult(null);
    setOptimizedUrl(null);
    setBackgroundRemovedUrl(null);
    setPrivacyResult(null);
    setProtectedUrl(null);
    setDownloadUrl(null);
    setError("");
  };

  // =========================================================
  // UPLOAD
  // =========================================================

  const uploadImage = async () => {
    if (!selectedFile) {
      setError("Please select an image first.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_URL}/upload-image`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.status === "success") {
        setUploadResult(data);
        await analyzePrivacy();
      } else {
        setError(data.message || "Image upload failed.");
      }
    } catch (err) {
      setError("Could not connect to SnapShield backend.");
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // PRIVACY ANALYSIS
  // =========================================================

  const analyzePrivacy = async () => {
    if (!selectedFile) return;

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_URL}/analyze-privacy`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.status === "success") {
        setPrivacyResult(data);
      } else {
        setError(data.message || "Privacy analysis failed.");
      }
    } catch (err) {
      setError("Could not analyze the image.");
    }
  };

  // =========================================================
  // OPTIMIZE
  // =========================================================

  const optimizeImage = async () => {
    if (!uploadResult?.public_id) return;

    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        `${API_URL}/optimize-image/${encodeURIComponent(
          uploadResult.public_id
        )}`
      );

      const data = await response.json();

      if (data.status === "success") {
        setOptimizedUrl(data.optimized_url);
      } else {
        setError(data.message || "Image optimization failed.");
      }
    } catch (err) {
      setError("Could not optimize the image.");
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // BACKGROUND REMOVAL
  // =========================================================

  const removeBackground = async () => {
    if (!uploadResult?.public_id) return;

    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        `${API_URL}/remove-background/${encodeURIComponent(
          uploadResult.public_id
        )}`
      );

      const data = await response.json();

      if (data.status === "success") {
        setBackgroundRemovedUrl(data.background_removed_url);
      } else {
        setError(data.message || "Background removal failed.");
      }
    } catch (err) {
      setError("Could not remove the background.");
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // PROTECT IMAGE
  // =========================================================

  const protectImage = async () => {
    if (!selectedFile) {
      setError("Please select an image first.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_URL}/protect-image`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.status === "success") {
        setProtectedUrl(data.protected_url);
        setDownloadUrl(data.download_url);
      } else {
        setError(data.message || "Image protection failed.");
      }
    } catch (err) {
      setError("Could not connect to the protection service.");
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // RESET
  // =========================================================

  const resetApp = () => {
    setSelectedFile(null);
    setUploadResult(null);
    setOptimizedUrl(null);
    setBackgroundRemovedUrl(null);
    setPrivacyResult(null);
    setProtectedUrl(null);
    setDownloadUrl(null);
    setError("");

    const fileInput = document.getElementById("file-input");

    if (fileInput) {
      fileInput.value = "";
    }
  };

  // =========================================================
  // SENSITIVE DATA COUNT
  // =========================================================

  const sensitiveCount =
    (privacyResult?.sensitive_data?.emails ?? 0) +
    (privacyResult?.sensitive_data?.phones ?? 0) +
    (privacyResult?.sensitive_data?.ids ?? 0) +
    (privacyResult?.sensitive_data?.cards ?? 0);

  // =========================================================
  // UI
  // =========================================================

  return (
    <div className="app">

      {/* NAVBAR */}

      <nav className="navbar">
        <div className="logo">
          <span className="logo-icon">🛡️</span>

          <span>
            SnapShield <strong>AI</strong>
          </span>
        </div>

        <div className="nav-status">
          <span className="status-dot"></span>
          Privacy Scanner Online
        </div>
      </nav>

      {/* HERO */}

      <section className="hero">

        <div className="hero-badge">
          AI-POWERED IMAGE PRIVACY
        </div>

        <h1>
          Protect Your Images
          <br />
          <span>Before You Share.</span>
        </h1>

        <p>
          SnapShield AI analyzes images for sensitive information,
          detects privacy risks, protects sensitive content and
          optimizes media.
        </p>

      </section>

      {/* MAIN */}

      <main className="main-container">

        {/* UPLOAD */}

        <section className="upload-card">

          <div className="upload-header">

            <div>
              <h2>Upload Image</h2>

              <p>
                Select an image to scan for privacy risks.
              </p>
            </div>

            <div className="upload-icon">
              📤
            </div>

          </div>

          <label
            htmlFor="file-input"
            className="upload-area"
          >

            <div className="upload-symbol">
              ☁️
            </div>

            <h3>
              Choose an image
            </h3>

            <p>
              PNG, JPG, JPEG or WEBP
            </p>

            <span className="choose-button">
              Browse Files
            </span>

          </label>

          <input
            id="file-input"
            type="file"
            accept="image/png,image/jpeg,image/jpg,image/webp"
            onChange={handleFileChange}
            hidden
          />

          {selectedFile && (
            <div className="selected-file">

              <div>
                <strong>Selected:</strong>{" "}
                {selectedFile.name}
              </div>

              <div>
                {(selectedFile.size / 1024).toFixed(1)}
                {" KB"}
              </div>

            </div>
          )}

          <button
            className="primary-button upload-button"
            onClick={uploadImage}
            disabled={!selectedFile || loading}
          >
            {loading
              ? "Processing..."
              : "🚀 Scan Image"}
          </button>

          {error && (
            <div className="error-message">
              ❌ {error}
            </div>
          )}

        </section>

        {/* UPLOADED IMAGE + OPTIMIZATION */}

        {uploadResult && (
          <section className="dashboard-grid">

            {/* ORIGINAL */}

            <div className="result-card">

              <div className="card-header">

                <div>

                  <span className="card-label">
                    ORIGINAL IMAGE
                  </span>

                  <h3>
                    Uploaded Media
                  </h3>

                </div>

                <span className="success-badge">
                  ✓ Uploaded
                </span>

              </div>

              <img
                src={
                  uploadResult.secure_url ||
                  uploadResult.url
                }
                alt="Original"
                className="preview-image"
              />

              <div className="image-details">

                <div>
                  <span>Format</span>

                  <strong>
                    {uploadResult.format}
                  </strong>
                </div>

                <div>
                  <span>Width</span>

                  <strong>
                    {uploadResult.width}px
                  </strong>
                </div>

                <div>
                  <span>Height</span>

                  <strong>
                    {uploadResult.height}px
                  </strong>
                </div>

              </div>

            </div>

            {/* OPTIMIZATION */}

            <div className="result-card">

              <div className="card-header">

                <div>

                  <span className="card-label">
                    CLOUDINARY
                  </span>

                  <h3>
                    Smart Optimization
                  </h3>

                </div>

                <span className="cloudinary-badge">
                  AI MEDIA
                </span>

              </div>

              <p className="card-description">
                Automatically optimize image quality
                and delivery format using Cloudinary.
              </p>

              {!optimizedUrl ? (
                <button
                  className="secondary-button"
                  onClick={optimizeImage}
                  disabled={loading}
                >
                  ⚡ Optimize with Cloudinary
                </button>
              ) : (
                <div>

                  <img
                    src={optimizedUrl}
                    alt="Optimized"
                    className="preview-image"
                  />

                  <a
                    href={optimizedUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="secondary-button"
                  >
                    🔗 Open Optimized Image
                  </a>

                </div>
              )}

            </div>

          </section>
        )}

        {/* BACKGROUND REMOVAL */}

        {uploadResult && (
          <section className="result-card full-card">

            <div className="card-header">

              <div>

                <span className="card-label">
                  CLOUDINARY AI
                </span>

                <h3>
                  Background Removal
                </h3>

              </div>

              <span className="cloudinary-badge">
                TRANSFORMATION
              </span>

            </div>

            <p className="card-description">
              Remove the image background using
              Cloudinary's background removal
              transformation.
            </p>

            {!backgroundRemovedUrl ? (
              <button
                className="secondary-button"
                onClick={removeBackground}
                disabled={loading}
              >
                ✨ Remove Background
              </button>
            ) : (
              <div>

                <img
                  src={backgroundRemovedUrl}
                  alt="Background Removed"
                  className="preview-image"
                />

                <a
                  href={backgroundRemovedUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="secondary-button"
                >
                  🔗 Open Background Removed Image
                </a>

              </div>
            )}

          </section>
        )}

        {/* PRIVACY ANALYSIS */}

        {privacyResult && (
          <section className="privacy-section">

            <div className="section-title">

              <div>

                <span className="card-label">
                  PRIVACY INTELLIGENCE
                </span>

                <h2>
                  Privacy Analysis
                </h2>

              </div>

              <div className="risk-badge">
                {privacyResult.risk_level}
              </div>

            </div>

            {/* SCORE */}

            <div className="privacy-grid">

              <div className="score-card">

                <div className="score-label">
                  PRIVACY RISK SCORE
                </div>

                <div className="score-number">

                  {
                    privacyResult.privacy_score ??
                    privacyResult.risk_score ??
                    0
                  }

                  <span>
                    /100
                  </span>

                </div>

                <div className="score-description">

                  {
                    privacyResult.risks?.length ?? 0
                  }

                  {" "}
                  privacy risk(s) detected

                </div>

              </div>

              {/* OCR COUNTS */}

              <div className="ocr-card">

                <div className="score-label">
                  OCR DETECTION
                </div>

                <div className="ocr-stats">

                  <div>
                    <strong>
                      {privacyResult.sensitive_data?.emails ?? 0}
                    </strong>

                    <span>
                      Emails
                    </span>
                  </div>

                  <div>
                    <strong>
                      {privacyResult.sensitive_data?.phones ?? 0}
                    </strong>

                    <span>
                      Phones
                    </span>
                  </div>

                  <div>
                    <strong>
                      {privacyResult.sensitive_data?.ids ?? 0}
                    </strong>

                    <span>
                      IDs
                    </span>
                  </div>

                  <div>
                    <strong>
                      {privacyResult.sensitive_data?.cards ?? 0}
                    </strong>

                    <span>
                      Cards
                    </span>
                  </div>

                </div>

              </div>

            </div>

            {/* RISKS */}

            {privacyResult.risks?.length > 0 && (
              <div className="result-card full-card">

                <div className="card-header">

                  <div>

                    <span className="card-label">
                      DETECTED INDICATORS
                    </span>

                    <h3>
                      Privacy Risks
                    </h3>

                  </div>

                </div>

                <div className="risk-list">

                  {privacyResult.risks.map(
                    (risk, index) => (
                      <div
                        className="risk-item"
                        key={index}
                      >

                        <div className="risk-item-left">

                          <span className="risk-icon">
                            ⚠️
                          </span>

                          <div>

                            <strong>
                              {risk.type}
                            </strong>

                            <p>
                              {
                                risk.message ||
                                risk.description ||
                                ""
                              }
                            </p>

                          </div>

                        </div>

                        <span className="severity">
                          {risk.severity}
                        </span>

                      </div>
                    )
                  )}

                </div>

              </div>
            )}

            {/* OCR TEXT */}

            {(
              privacyResult.ocr?.text_detected ||
              privacyResult.ocr?.detected_text ||
              privacyResult.ocr?.text
            ) && (
              <div className="result-card full-card">

                <div className="card-header">

                  <div>

                    <span className="card-label">
                      OCR
                    </span>

                    <h3>
                      Detected Text
                    </h3>

                  </div>

                </div>

                <div className="ocr-text">

                  {
                    privacyResult.ocr?.detected_text ||
                    privacyResult.ocr?.text ||
                    ""
                  }

                </div>

              </div>
            )}

            {/* RECOMMENDATIONS */}

            {privacyResult.recommendations?.length > 0 && (
              <div className="result-card full-card">

                <div className="card-header">

                  <div>

                    <span className="card-label">
                      SNAPSHIELD ADVICE
                    </span>

                    <h3>
                      Recommendations
                    </h3>

                  </div>

                </div>

                <div className="recommendation-list">

                  {privacyResult.recommendations.map(
                    (recommendation, index) => (
                      <div
                        className="recommendation-item"
                        key={index}
                      >

                        <span>
                          ✓
                        </span>

                        <p>
                          {recommendation}
                        </p>

                      </div>
                    )
                  )}

                </div>

              </div>
            )}

            {/* PROTECT */}

            {sensitiveCount > 0 && (
              <div className="result-card full-card protection-card">

                <div className="card-header">

                  <div>

                    <span className="card-label">
                      PRIVACY PROTECTION
                    </span>

                    <h3>
                      🛡️ Protect Sensitive Content
                    </h3>

                  </div>

                  <span className="protection-badge">
                    SAFE COPY
                  </span>

                </div>

                <p className="card-description">

                  Sensitive information was detected.
                  Create a protected copy before
                  sharing or posting the image.

                </p>

                {!protectedUrl ? (
                  <button
                    className="primary-button"
                    onClick={protectImage}
                    disabled={loading}
                  >

                    {loading
                      ? "Protecting Image..."
                      : "🛡️ Protect Image"}

                  </button>
                ) : (
                  <div className="protected-result">

                    <div className="success-message">
                      ✅ Sensitive information
                      successfully redacted.
                    </div>

                    <img
                      src={protectedUrl}
                      alt="Protected version"
                      className="preview-image"
                    />

                    <div className="protected-actions">

                      <a
                        href={protectedUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="secondary-button"
                      >
                        🔗 Open Protected Image
                      </a>

                      {downloadUrl && (
                        <a
                          href={downloadUrl}
                          className="download-button"
                        >
                          ⬇️ Download Protected Image
                        </a>
                      )}

                    </div>

                    <p className="download-help">
                      Download this protected version
                      and safely post or share it.
                    </p>

                  </div>
                )}

              </div>
            )}

          </section>
        )}

        {/* WORKFLOW */}

        <section className="workflow-section">

          <div className="section-title">

            <div>

              <span className="card-label">
                HOW IT WORKS
              </span>

              <h2>
                SnapShield Workflow
              </h2>

            </div>

          </div>

          <div className="workflow-grid">

            <div className="workflow-card">

              <div className="workflow-number">
                01
              </div>

              <div className="workflow-icon">
                📤
              </div>

              <h3>
                Upload
              </h3>

              <p>
                Upload your image securely to Cloudinary.
              </p>

            </div>

            <div className="workflow-card">

              <div className="workflow-number">
                02
              </div>

              <div className="workflow-icon">
                🔍
              </div>

              <h3>
                Analyze
              </h3>

              <p>
                OCR scans the image for potentially
                sensitive information.
              </p>

            </div>

            <div className="workflow-card">

              <div className="workflow-number">
                03
              </div>

              <div className="workflow-icon">
                ⚠️
              </div>

              <h3>
                Assess
              </h3>

              <p>
                SnapShield calculates a privacy
                risk score and provides recommendations.
              </p>

            </div>

            <div className="workflow-card">

              <div className="workflow-number">
                04
              </div>

              <div className="workflow-icon">
                🛡️
              </div>

              <h3>
                Protect
              </h3>

              <p>
                Sensitive regions are automatically
                redacted.
              </p>

            </div>

            <div className="workflow-card">

              <div className="workflow-number">
                05
              </div>

              <div className="workflow-icon">
                ⬇️
              </div>

              <h3>
                Download
              </h3>

              <p>
                Download the protected image
                and safely share it.
              </p>

            </div>

            <div className="workflow-card">

              <div className="workflow-number">
                06
              </div>

              <div className="workflow-icon">
                ⚡
              </div>

              <h3>
                Optimize
              </h3>

              <p>
                Optimize media delivery with Cloudinary.
              </p>

            </div>

          </div>

        </section>

        {/* RESET */}

        {(selectedFile ||
          uploadResult ||
          privacyResult) && (

          <div className="reset-container">

            <button
              className="reset-button"
              onClick={resetApp}
            >
              ↻ Start New Scan
            </button>

          </div>
        )}

      </main>

      {/* FOOTER */}

      <footer>

        <p>
          🛡️ SnapShield AI • Smart Image Safety & Privacy Scanner
        </p>

        <p>
          Powered by Cloudinary + FastAPI + OCR
        </p>

      </footer>

    </div>
  );
}

export default App;