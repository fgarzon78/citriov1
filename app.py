from flask import Flask, request, render_template_string, send_file
import qrcode
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

# Route to generate QR code
@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    timestamp = request.args.get('timestamp', 'Unknown Date')
    expiration = request.args.get('expiration', 'Unknown Date')
    qr_data = f"http://your-domain.com/details?timestamp={timestamp}&expiration={expiration}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')

# Route to display details and countdown
@app.route('/details', methods=['GET'])
def details():
    timestamp = request.args.get('timestamp', 'Unknown Date')
    expiration = request.args.get('expiration', 'Unknown Date')
    expiration_datetime = datetime.strptime(expiration, "%Y-%m-%d %H:%M:%S")
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Orange Juice Details</title>
        </head>
        <body>
            <h1>Orange Juice Details</h1>
            <p><strong>Bottled On:</strong> {{ timestamp }}</p>
            <p><strong>Expires On:</strong> {{ expiration }}</p>
            <h2>Time Left Until Expiration:</h2>
            <div id="countdown"></div>
            <script>
                const expirationDate = new Date("{{ expiration }}").getTime();
                const timer = setInterval(() => {
                    const now = new Date().getTime();
                    const distance = expirationDate - now;
                    if (distance < 0) {
                        clearInterval(timer);
                        document.getElementById("countdown").innerHTML = "Expired";
                        return;
                    }
                    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                    const seconds = Math.floor((distance % (1000 * 60)) / 1000);
                    document.getElementById("countdown").innerHTML = 
                        days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
                }, 1000);
            </script>
        </body>
        </html>
    ''', timestamp=timestamp, expiration=expiration)

if __name__ == '__main__':
    app.run(debug=True)
