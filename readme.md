# 📸 AI-Powered Instant Passport Photo Generator  

An end-to-end AI app that automatically removes photo backgrounds and generates **passport/ID-ready images** in real-time. Built with **UNet (ResNet34 encoder)** for human segmentation and deployed using **Streamlit**.  

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

## 🚀 Getting Started 
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
# run the app 
```bash
streamlit run app.py
```