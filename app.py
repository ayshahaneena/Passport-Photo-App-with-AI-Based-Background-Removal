from PIL import Image, ImageOps
import streamlit as st
import torch
import numpy as np
import cv2
import io
import segmentation_models_pytorch as smp

# --- Page Config ---
st.set_page_config(page_title="AI Passport Photo Generator", layout="wide")

# --- Session Defaults ---
if "bg_choice" not in st.session_state:
    st.session_state.bg_choice = "White"
if "use_camera" not in st.session_state:
    st.session_state.use_camera = False

# --- Premium Minimal CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(#6495ED, #0047AB, #00008B);
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        color: #ffffff;
    }
    h1 {
        font-size: 2.6rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.3em;
        color: #ffffff;
    }
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2em;
        color: #d1d5db;
    }
    label, .stCheckbox label, .stSelectbox label, .stRadio label {
        font-size: 1.1rem !important;
        font-weight: 600;
        color: #ffffff !important;
    }
    .stButton>button, .stDownloadButton>button {
        font-size: 1.15rem !important;
        padding: 10px 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
        transform: scale(1.02);
    }
    .bg-swatch {
        display: inline-block;
        width: 45px; height: 30px;
        margin-right: 0.8em;
        border-radius: 6px;
        border: 3px solid transparent;
        cursor: pointer;
    }
    .bg-swatch.selected {
        border-color: #ffffff;
    }
    .footer-info {
        text-align: center;
        font-size: 1rem;
        color: #9ca3af;
        margin-top: 2em;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Model ---
@st.cache_resource
def load_model():
    m = smp.Unet("resnet34", encoder_weights=None, in_channels=3, classes=1)
    m.load_state_dict(torch.load("unet_resnet34.pth", map_location="cpu"))
    m.eval()
    return m
model = load_model()

# --- Title ---
st.markdown("<h1>📸 AI Passport Photo Generator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Upload or capture a photo, pick background & size, and get your passport-ready image instantly</p>", unsafe_allow_html=True)

# --- Layout: Left controls / Right preview ---
left_col, right_col = st.columns([1, 1.3])

with left_col:
    # Upload / Camera
    st.subheader("Upload or Capture")
    uploaded_file = st.file_uploader("Upload photo", type=["jpg","jpeg","png"])
    use_camera = st.checkbox("Use Live Camera", value=st.session_state.use_camera)
    st.session_state.use_camera = use_camera
    camera_file = st.camera_input("Camera Preview", label_visibility="collapsed") if use_camera else None

    # Background selection
    st.subheader("Background")
    cols = st.columns(3)
    labels = ["White","Blue","Transparent"]
    colors = ["#ffffff", "#109fe6", "repeating-conic-gradient(#444 0% 25%, #666 0% 50%)"]
    for label, clr, col in zip(labels, colors, cols):
        is_sel = (st.session_state.bg_choice == label)
        style = f"background:{clr}" + (";border: 3px solid #ffffff;" if is_sel else "")
        with col:
            if st.button(label, key=f"bg_{label}"):
                st.session_state.bg_choice = label
            st.markdown(f"<div class='bg-swatch{' selected' if is_sel else ''}' style='{style}'></div>", unsafe_allow_html=True)

    # Size selection
    st.subheader("Photo Size")
    size_option = st.selectbox("Select size:", ["2x2 inch (51×51 mm)", "35×45 mm", "40×50 mm"])

with right_col:
    st.subheader("Preview & Download")

    # Sizes
    size_map = {"2x2 inch (51×51 mm)": (600,600), "35×45 mm": (413,531), "40×50 mm": (472,591)}
    

    # Input photo (upload or camera)
    input_file = camera_file if (use_camera and camera_file) else uploaded_file

    if input_file:
        image = Image.open(input_file).convert("RGB")
        image = ImageOps.exif_transpose(image)
        img_np = np.array(image)

        # preprocess for model
        img_resized = cv2.resize(img_np, (256,256))
        inp = torch.tensor(img_resized.transpose(2,0,1)).unsqueeze(0).float()/255.
        with torch.no_grad():
            pred = torch.sigmoid(model(inp))[0,0].numpy()
        mask = (pred > 0.5).astype(np.uint8)
        mask_resized = cv2.resize(mask, (img_np.shape[1], img_np.shape[0]))

        if st.session_state.bg_choice == "White":
            bg = np.ones_like(img_np)*255
            final_np = img_np * mask_resized[...,None] + bg * (1-mask_resized[...,None])
            final = Image.fromarray(final_np.astype(np.uint8)).resize(size_map[size_option])
        elif st.session_state.bg_choice == "Blue":
            bg = np.zeros_like(img_np)
            bg[:,:,2] = 200
            final_np = img_np * mask_resized[...,None] + bg * (1-mask_resized[...,None])
            final = Image.fromarray(final_np.astype(np.uint8)).resize(size_map[size_option])
        else:
            img_rgba = cv2.cvtColor(img_np, cv2.COLOR_RGB2RGBA)
            img_rgba[:,:,3] = mask_resized*255
            final = Image.fromarray(img_rgba).resize(size_map[size_option])

        # Save & display (smaller preview width)
        buf = io.BytesIO()
        final.save(buf, format="PNG")
        buf.seek(0)
        st.image(final, caption="✅ Passport Photo", width=300)
        st.download_button("📥 Download PNG", data=buf, file_name="passport.png", mime="image/png")
    else:
        st.info("Upload or capture a photo to preview here")

# --- Footer ---
st.markdown("<div class='footer-info'>AI-powered • Passport / ID ready</div>", unsafe_allow_html=True)

