import streamlit as st
import os
import tempfile
import zipfile
from processing_logic import process_ecg_files

st.set_page_config(layout="wide")
st.title("⚕️ ECG ფაილების (.hea, .dat) ვიზუალიზატორი")
st.markdown("ატვირთეთ თქვენი WFDB ფორმატის ECG ფაილები (`.hea` და `.dat`) და მიიღეთ დამუშავებული სურათები (`.svg` და `.png`) ZIP არქივში.")

# ფაილების ასატვირთი კომპონენტი
uploaded_files = st.file_uploader(
    "აირჩიეთ .hea და .dat ფაილები",
    accept_multiple_files=True,
    type=['hea', 'dat']
)

if uploaded_files:
    if st.button("🚀 დამუშავების დაწყება"):
        with st.spinner('მიმდინარეობს ფაილების დამუშავება... გთხოვთ, დაიცადოთ.'):
            # შევქმნათ დროებითი საქაღალდეები, სადაც ფაილები შეინახება და დამუშავდება
            with tempfile.TemporaryDirectory() as temp_dir:
                input_dir = os.path.join(temp_dir, "input")
                output_dir = os.path.join(temp_dir, "output")
                os.makedirs(input_dir)
                os.makedirs(output_dir)

                # ავტვირთოთ ფაილები დროებით input საქაღალდეში
                for uploaded_file in uploaded_files:
                    with open(os.path.join(input_dir, uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getbuffer())

                # გამოვიძახოთ ჩვენი ლოგიკა
                processed, errors, message = process_ecg_files(input_dir, output_dir)

                if message:
                    st.warning(message)
                
                if processed:
                    st.success(f"✅ წარმატებით დამუშავდა {len(processed)} ჩანაწერი.")
                    
                    # შევქმნათ ZIP არქივი
                    zip_path = os.path.join(temp_dir, "ecg_results.zip")
                    with zipfile.ZipFile(zip_path, 'w') as zipf:
                        for root, _, files in os.walk(output_dir):
                            for file in files:
                                zipf.write(os.path.join(root, file), arcname=file)
                    
                    # შევთავაზოთ მომხმარებელს გადმოწერა
                    with open(zip_path, "rb") as fp:
                        st.download_button(
                            label="📥 შედეგების გადმოწერა (ZIP)",
                            data=fp,
                            file_name="ecg_results.zip",
                            mime="application/zip"
                        )

                if errors:
                    st.error("❌ ზოგიერთ ფაილზე დაფიქსირდა შეცდომა:")
                    for error in errors:
                        st.code(error)
