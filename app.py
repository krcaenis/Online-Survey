from flask import Flask, render_template, request, redirect, url_for, flash
import configparser
import tkinter as tk

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Config dosyası ile offset değeri yönetimi
config = configparser.ConfigParser()
config_file = "config.ini"

def load_config():
    config.read(config_file)
    if "Settings" not in config:
        config["Settings"] = {}
    if "offset" not in config["Settings"]:
        config["Settings"]["offset"] = "0"
        save_config()

def save_config():
    with open(config_file, "w") as file:
        config.write(file)

def copy_to_clipboard(text):
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle
    root.clipboard_clear()  # Panoyu temizle
    root.clipboard_append(text)  # Metni panoya ekle
    root.update()  # Panoyu güncelle
    root.destroy()  # Tkinter'ı kapat

@app.route("/", methods=["GET", "POST"])
def index():
    load_config()
    offset_value = float(config["Settings"]["offset"])
    
    result = ""
    if request.method == "POST":
        try:
            survey_depth = float(request.form["survey_depth"])
            inc = request.form["inc"]
            azm = request.form["azm"]
            tvd = request.form["tvd"]
            ns = request.form["ns"]
            ew = request.form["ew"]
            vs = request.form["vs"]
            dls = request.form["dls"]
            offset = float(request.form["offset"])
            
            # Bit Depth hesaplama
            bit_depth = survey_depth + offset

            # Kopyalanacak metin
            result = (
                "SURVEY\n"
                f"Bit Depth: {bit_depth:.2f} m\n"
                f"Survey Depth: {survey_depth} m\n"
                f"Inc: {inc} °\n"
                f"Azm: {azm} °\n"
                f"TVD: {tvd} m\n"
                f"N/S: {ns} m\n"
                f"E/W: {ew} m\n"
                f"VS: {vs} m\n"
                f"DLS: {dls} °/30m"
            )
            
            # Offset değerini kaydet
            config["Settings"]["offset"] = str(offset)
            save_config()

        except ValueError:
            flash("Lütfen tüm alanlara geçerli sayısal değerler girin.", "danger")
    
    return render_template("index.html", result=result, offset=offset_value)

@app.route("/copy", methods=["POST"])
def copy_text():
    result = request.form.get("result")
    if result:
        copy_to_clipboard(result)  # pyperclip yerine tkinter kullanılıyor
        flash("Metin panoya kopyalandı!", "success")
    else:
        flash("Kopyalanacak metin yok.", "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
