from flask import Flask, render_template, request, redirect, url_for, flash
import configparser
import pyperclip
import math  # Matematik fonksiyonları için eklenmiştir.

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
            ns = float(request.form["ns"])  # N/S değeri float olarak alındı
            ew = float(request.form["ew"])    # E/W değeri float olarak alındı
            dls = request.form["dls"]
            offset = float(request.form["offset"])
            
            # Bit Depth hesaplama
            bit_depth = survey_depth + offset

            # VS değerini hesaplama
            vs = math.sqrt(ns**2 + ew**2)

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
                f"VS: {vs:.2f} m\n"  # Hesaplanan VS değeri burada gösterildi
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
        pyperclip.copy(result)  # pyperclip yerine tkinter kullanılıyor
        flash("Metin panoya kopyalandı!", "success")
    else:
        flash("Kopyalanacak metin yok.", "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
