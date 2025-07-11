import streamlit as st
import os

# Page configuration
st.set_page_config(page_title="About Defects", page_icon="🔍")

st.title("🔍 Surface Defect Types")
st.markdown("Learn more about each defect type with examples and descriptions.")

# Path to sample images
image_dir = "data/sample_defects"

# List of defects
defects = [
    {
        "name": "Inclusion",
        "file": "inclusion.bmp",
        "desc": """Inclusions are non-metallic particles trapped inside the steel during manufacturing. 
They usually come from slag or oxidized particles that did not completely melt. 
These create small internal flaws or surface disruptions and weaken the steel structurally."""
    },
    {
        "name": "Pitted Surface",
        "file": "pitted_surface.bmp",
        "desc": """Pitted surfaces are formed due to corrosion or trapped gas on the steel surface. 
They appear as small, deep round holes or indentations that damage the smooth finish. 
This defect can significantly affect the appearance and coating performance of the steel."""
    },
    {
        "name": "Rolled-in Scale",
        "file": "rolled_in_scale.bmp",
        "desc": """Rolled-in scale occurs when oxide layers (scale) from the hot rolling process 
get pressed into the steel strip instead of being cleaned off. 
This creates rough, dark spots on the surface that affect appearance and quality."""
    },
    {
        "name": "Scratches",
        "file": "scratches.bmp",
        "desc": """Scratches are linear, shallow marks caused by mechanical contact with rough surfaces 
during processing, handling, or transport. 
They reduce the visual quality of steel and can be entry points for corrosion if left untreated."""
    },
    {
        "name": "Patches",
        "file": "patches.bmp",
        "desc": """Patch defects are uneven or discolored regions on the steel surface. 
They may result from surface contamination, cooling irregularities, or defects in coating processes. 
Patches can create weak spots and irregular textures in the material."""
    },
    {
        "name": "Crazing",
        "file": "crazing.bmp",
        "desc": """Crazing appears as a web or network of fine cracks on the surface. 
It usually forms due to rapid cooling, stress release, or thermal shock. 
Though often shallow, it can indicate underlying structural stress in the steel."""
    },
]

# Display in columns
for defect in defects:
    st.markdown(f"### 🛠️ {defect['name']}")
    cols = st.columns([1, 3])
    
    img_path = os.path.join(image_dir, defect["file"])
    if os.path.exists(img_path):
        cols[0].image(img_path, width=120)
    else:
        cols[0].warning("Image not found.")
    
    cols[1].markdown(defect["desc"])
    st.markdown("---")
