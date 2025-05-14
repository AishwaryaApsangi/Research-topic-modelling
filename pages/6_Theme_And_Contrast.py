import streamlit as st
import wcag_contrast_ratio as contrast
import util

def contrast_summary(label: str, foreground_rgb_hex: str, background_rgb_hex: str) -> None:
    rgb_foreground = util.parse_hex(foreground_rgb_hex)
    rgb_background = util.parse_hex(background_rgb_hex)
    contrast_ratio = contrast.rgb(rgb_foreground, rgb_background)
    contrast_ratio_str = f"{contrast_ratio:.2f}"

    st.metric(label, value=f"{contrast_ratio_str} : 1", label_visibility="collapsed")

    if contrast.passes_AAA(contrast_ratio):
        st.success(" WCAG AAA")
    elif contrast.passes_AA(contrast_ratio):
        st.info(" WCAG AA")
    else:
        st.error(" Fails WCAG")

    st.markdown(
        f'<p style="color: {foreground_rgb_hex}; background-color: {background_rgb_hex}; padding: 12px; border-radius: 8px">Lorem ipsum text sample</p>',
        unsafe_allow_html=True
    )

def sample_components(key: str):
    st.subheader(" Sample Interactive Components")
    st.text_input("Text input", key=f"{key}:text_input")
    st.slider("Slider", min_value=0, max_value=100, key=f"{key}:slider")
    st.button("Button", key=f"{key}:button")
    st.checkbox("Checkbox", key=f"{key}:checkbox", value=True)
    st.radio("Radio", options=["Option 1", "Option 2"], key=f"{key}:radio")
    st.selectbox("Selectbox", options=["Option 1", "Option 2"], key=f"{key}:selectbox")

# Main Layout
st.set_page_config(page_title="Theme & Contrast Explorer", layout="wide")
st.title(" Theme & Contrast Explorer")

st.markdown("Use this panel to test theme colors, WCAG compliance, and explore Streamlit component styling.")

col1, col2 = st.columns(2)

with col1:
    st.header(" WCAG Contrast Checker")
    fg = st.color_picker("Text Color", "#1C2833", key="fg")
    bg = st.color_picker("Background Color", "#EBF5FB", key="bg")
    contrast_summary("Contrast Ratio", fg, bg)

with col2:
    sample_components("preview")

st.divider()
st.subheader(" Current Theme in config.toml")
st.code(\"\"\"
[theme]
primaryColor="#7FB3D5"
backgroundColor="#FDFEFE"
secondaryBackgroundColor="#EBF5FB"
textColor="#1C2833"
font="sans serif"
\"\"\")
