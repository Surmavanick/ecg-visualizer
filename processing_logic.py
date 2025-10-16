import os
import wfdb
import numpy as np
import ecg_plot
import matplotlib.pyplot as plt
import matplotlib as mpl

# --- SVG ტექსტი დარჩეს ტექსტად ---
mpl.rcParams['svg.fonttype'] = 'none'

def process_ecg_files(data_dir, output_dir):
    """
    ამუშავებს data_dir-ში არსებულ ყველა .hea ფაილს და შედეგებს ინახავს output_dir-ში.
    აბრუნებს დამუშავებული და შეცდომით დასრულებული ფაილების სიას.
    """
    processed_files = []
    error_files = []

    records = [f.replace(".hea", "") for f in os.listdir(data_dir) if f.endswith(".hea")]
    records.sort()

    if not records:
        return processed_files, error_files, "⚠️ საქაღალდეში არ მოიძებნა .hea ფაილები."

    for record_name in records:
        try:
            rec = wfdb.rdrecord(os.path.join(data_dir, record_name))
            data = rec.p_signal

            if data.ndim != 2:
                raise ValueError(f"Unexpected ECG array shape: {data.shape}")

            if data.shape[1] == 12 and data.shape[0] != 12:
                data = data.T
            elif data.shape[0] == 12:
                pass
            else:
                if 12 in data.shape:
                    data = data if data.shape[0] == 12 else data.T
                else:
                    raise ValueError(f"Expected 12-lead ECG, got shape {data.shape}")

            # დახატვა
            ecg_plot.plot(
                data,
                sample_rate=rec.fs,
                title=f"{record_name} - 12 Lead ECG (25mm/s, 10mm/mV)"
            )

            fig = plt.gcf()
            fig.canvas.draw()
            
            # --- SVG შენახვა ---
            svg_path = os.path.join(output_dir, record_name + ".svg")
            fig.savefig(svg_path, format="svg", bbox_inches="tight", dpi=300)

            # --- PNG შენახვა ---
            png_path = os.path.join(output_dir, record_name + ".png")
            ecg_plot.save_as_png(record_name, output_dir) # ecg_plot-ი თავად ამატებს .png-ს

            plt.close(fig)
            processed_files.append(record_name)

        except Exception as e:
            error_files.append(f"{record_name}: {e}")
            plt.close('all') # დავხუროთ ყველა ფიგურა შეცდომის შემთხვევაში

    return processed_files, error_files, None
