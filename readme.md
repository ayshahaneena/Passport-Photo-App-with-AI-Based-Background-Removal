# 📸 AI-Powered Instant Passport Photo Generator  

An end-to-end AI app that automatically removes photo backgrounds and generates **passport/ID-ready images** in real-time. Built with **UNet (ResNet34 encoder)** for human segmentation and deployed using **Streamlit**.  

🔗 **Live Demo**: [Try the App Here](https://passport-photo-app-with-ai-based-background-removal-erjdayuggm.streamlit.app/)  

---


## ✨ Features  
- ✅ Real-time **human segmentation & background removal**  
- ✅ **Multiple backgrounds**: White (passport), Blue (visa/ID), Transparent (custom)  
- ✅ Supports **camera capture** or **image upload**  
- ✅ **Automatic cropping & resizing** to passport standards:  
  - 2×2 inch (51×51 mm)  
  - 35×45 mm  
  - 40×50 mm  
- ✅ Instant **downloadable outputs** (PNG/JPG)  

---

## 📂 Dataset  
- **Custom dataset**: 100 selfie/portrait images  
- **Masks**: Generated using `rembg` (U²-Net) and LabelMe 
- **Augmentation**: Horizontal flip, rotation, brightness/contrast adjustment, random crop, resize  
- **Split**: 80% training, 20% validation  

---

## 🧠 Model Pipeline  
- **Architecture**: UNet with ResNet34 encoder (pretrained on ImageNet)  
- **Loss Function**: Dice + Binary Cross-Entropy (hybrid)  
- **Training**: 20 epochs on augmented dataset  
- **Performance**:  
  - Mean IoU: **0.88**  
  - Pixel Accuracy: **0.95**  

---

## 🚀 Getting Started  

### 1. Clone the Repository  
```bash
git clone https://github.com/<your-username>/passport-photo-app.git
cd passport-photo-app
```

### 2. Setup Envoirnment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Run the App
```bash
streamlit run app.py
```

---

##  Objectives  
- ✅ Build accurate real-time segmentation model for background removal  
- ✅ Support multiple backgrounds (White, Blue, Transparent)  
- ✅ Enable both **image upload** & **camera capture**  
- ✅ Automatically crop to global passport standards (2×2 inch, 35×45 mm, 40×50 mm)  
- ✅ Provide instant **downloadable outputs** (JPG/PNG)  

---

##  Methodology  

### 📂  Dataset & Preprocessing  
- Custom dataset: **100 selfies/portraits**  
- Masks generated using **rembg (U²-Net)**  
- Augmentation: flips, rotations, brightness/contrast, resize, random crops  
- Split: **80% train / 20% validation**  

### 🧠  Model Architecture  
- Model: **UNet with ResNet34 encoder** (ImageNet pretrained)  
- Loss: Hybrid **Dice + BCE**  
- Training: **20 epochs** on augmented dataset  

### 💻  App Implementation  
- Frontend: **Streamlit** (file upload or live camera)  
- Background replacement: White / Blue / Transparent  
- Output: Cropped, resized passport photo with **download option**  

---

## Results & Evaluation  

### 📈 Quantitative Metrics  
| Metric              | Value |
|----------------------|-------|
| Mean IoU             | 0.88  |
| Pixel Accuracy       | 0.95  |
| Training Epochs      | 20    |

### 👁️ Qualitative Results  
- Clean human segmentation  
- Minimal background noise  
- Works under different lighting conditions & poses  

---

## Conclusion & Future Work  

### ✅ Conclusion  
The project successfully developed an **AI-powered passport photo generator** that is accurate, real-time, and user-friendly.  

### 🚀 Future Work  
- 🌍 Add global passport size standards  
- 💡 Improve robustness under extreme lighting  
- 📱 Develop an **offline mobile version**  
- 🎯 Integrate **auto face detection** for centering  

---
