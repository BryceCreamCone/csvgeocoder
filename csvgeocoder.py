from flask import Flask, render_template, request, send_file
import pandas
from geopy.geocoders import Nominatim
from werkzeug.utils import secure_filename

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success/", methods=["POST"])
def success():
    global filename
    if request.method=='POST':
        if '.csv' in request.files["file"].filename:
            csvfile=request.files["file"]
            try:
                table=pandas.read_csv(csvfile, sep=',')
            except:
                return render_template("index.html", message="That file cannot be read as a CSV file")
            filename=secure_filename(csvfile.filename)
            nom=Nominatim(scheme='https')
            if table.columns.str.contains("Address" or "address").any()==True:
                table["Latitude"]=table["Address"or"address"].apply(nom.geocode).apply(lambda x: x.latitude if x != None else None)
                table["Longitude"]=table["Address"or"address"].apply(nom.geocode).apply(lambda x: x.longitude if x != None else None)
                table.to_csv("uploads/new"+filename, sep=',', index=False, encoding='utf-8')
                data=table.to_html(classes="table", index=False, index_names=False, justify='center', na_rep='--')
                return render_template("success.html", data=data, btn="download.html")
            else:
                return render_template("index.html", message="There doesn't seem to be an Address (or address) column in your file")
        else:
            return render_template("index.html", message="That doesn't appear to be a CSV file. Please select a CSV file")

@app.route("/download/")
def download():
    return send_file("uploads/new"+filename, attachment_filename="new"+filename, as_attachment=True)

if __name__=='__main__':
    app.debug=True
    app.run()
