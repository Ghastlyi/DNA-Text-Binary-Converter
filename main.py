from flask import Flask, render_template_string, request

app = Flask(__name__)

binary_to_dna = {'00': 'A', '01': 'T', '10': 'G', '11': 'C'}
dna_to_binary = {v: k for k, v in binary_to_dna.items()}

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chars if b)

def binary_to_dna_seq(binary):
    if len(binary) % 2 != 0:
        binary += '0'
    return ''.join(binary_to_dna.get(binary[i:i+2], '?') for i in range(0, len(binary), 2))

def dna_to_binary_seq(dna):
    return ''.join(dna_to_binary.get(base, '??') for base in dna)

def text_to_dna(text):
    binary = text_to_binary(text)
    return binary_to_dna_seq(binary)

def dna_to_text(dna):
    binary = dna_to_binary_seq(dna)
    return binary_to_text(binary)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>DNA ↔ Text/Binary Converter</title>
    <style>
        html, body {
            min-height: 100vh;
            margin: 0;
        }
        body {
            font-family: 'Share Tech Mono', 'Roboto Mono', monospace;
            background: radial-gradient(ellipse at top, #051629 70%, #0fffd7 170%);
            position: relative;
            overflow-x: hidden;
        }
        .dna-background {
            width: 90vw;
            max-width: 1100px;
            height: 400px;
            position: absolute;
            left: 50%;
            top: 40px;
            z-index: 0;
            transform: translateX(-50%);
            opacity: 0.78;
        }
        .container {
            position: relative;
            z-index: 2;
            background: rgba(19,40,60,0.97);
            max-width: 600px;
            margin: 70px auto 40px auto;
            padding: 44px 38px 46px 38px;
            border-radius: 20px;
            box-shadow: 0 0 64px #19ffe0aa, 0 0 14px #0fffd7bb inset;
            border: 2.5px solid #0fffd7;
        }
        h1 {
            text-align: center;
            color: #19ffe0;
            font-size: 2.30em;
            margin-bottom: 18px;
            font-weight: 700;
            text-shadow: 0 0 18px #13ffe066;
        }
        .subtitle {
            color: #13ffe0;
            text-align: center;
            font-size: 1.13em;
            margin-bottom: 30px;
            letter-spacing: 2px;
            text-shadow: 0 0 8px #0fffd76f;
        }
        form {
            margin-top: 10px;
        }
        label {
            color: #13ffe0;
            font-size: 1.10em;
        }
        select, input[type=text] {
            background: #172d46;
            color: #19ffe0;
            border: 2px solid #13ffe0;
            box-shadow: 0 0 12px #19ffe057;
            font-size: 1.12em;
            padding: 13px;
            border-radius: 8px;
            margin-bottom: 20px;
            outline: none;
            width: 100%;
            transition: box-shadow .23s;
        }
        select:focus, input[type=text]:focus {
            box-shadow: 0 0 23px #13ffe0c8, 0 0 16px #19ffe0cc inset;
        }
        input[type=submit] {
            background: linear-gradient(90deg, #19ffe0 0%, #13ffe0 100%);
            color: #171f27;
            border: none;
            padding: 13px 0;
            border-radius: 10px;
            width: 100%;
            font-size: 1.19em;
            letter-spacing: 2px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 0 21px #13ffe093, 0 1px 15px #18ffe073;
            transition: background .22s, color .19s;
            margin-bottom: 12px;
        }
        input[type=submit]:hover {
            background: linear-gradient(90deg, #13ffe0 15%, #19ffe0 85%);
            color: #051629;
            box-shadow: 0 0 36px #13ffe060;
        }
        .result {
            background: linear-gradient(100deg, #051629 10%, #19ffe0 100%);
            border-left: 9px solid #19ffe0;
            padding: 22px 16px 18px 24px;
            margin-top: 36px;
            font-size: 1.18em;
            color: #13283c;
            font-weight: 600;
            word-break:break-all;
            box-shadow: 0 0 29px #13ffe099 inset;
            border-radius: 13px;
            display: flex;
            align-items: center;
            gap: 25px;
        }
        footer {
            margin-top: 30px;
            text-align: center;
            color: #13ffe0cc;
            font-size: 1.09em;
            letter-spacing: 2px;
        }
        @media (max-width: 900px) {
            .container { max-width:92vw; padding: 2vw 3vw;}
            .dna-background { width:100vw; left:0; transform:none;}
        }
    </style>
    <link href="https://fonts.googleapis.com/css?family=Share+Tech+Mono:400" rel="stylesheet">

</head>
<body>
    <!-- Big DNA background - bright and clear -->
    <div class="dna-background">
      <svg viewBox="0 0 1100 400" width="100%" height="100%">
        <defs>
          <linearGradient id="helixGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#19ffe0"/>
            <stop offset="100%" stop-color="#2a99fc"/>
          </linearGradient>
          <radialGradient id="nucGrad1" cx="50%" cy="50%" r="50%">
            <stop offset="10%" stop-color="#fff"/>
            <stop offset="100%" stop-color="#19ffe0"/>
          </radialGradient>
          <radialGradient id="nucGrad2" cx="50%" cy="50%" r="50%">
            <stop offset="10%" stop-color="#fff"/>
            <stop offset="100%" stop-color="#2a99fc"/>
          </radialGradient>
        </defs>
        <g>
          <!-- Main double helix curves -->
          <path d="M120,340 Q360,80 550,340 T1000,340" fill="none" stroke="url(#helixGrad)" stroke-width="28" opacity="0.91"/>
          <path d="M120,60 Q360,320 550,60 T1000,60" fill="none" stroke="url(#helixGrad)" stroke-width="27" opacity="0.89"/>
          <!-- Nucleotides Left-to-Right -->
          <circle cx="210" cy="120" r="32" fill="url(#nucGrad1)"/>
          <circle cx="210" cy="280" r="32" fill="url(#nucGrad2)"/>
          <circle cx="370" cy="260" r="32" fill="url(#nucGrad1)"/>
          <circle cx="370" cy="110" r="32" fill="url(#nucGrad2)"/>
          <circle cx="570" cy="115" r="32" fill="url(#nucGrad1)"/>
          <circle cx="570" cy="270" r="32" fill="url(#nucGrad2)"/>
          <circle cx="780" cy="282" r="32" fill="url(#nucGrad1)"/>
          <circle cx="780" cy="100" r="32" fill="url(#nucGrad2)"/>
          <circle cx="950" cy="120" r="32" fill="url(#nucGrad1)"/>
          <circle cx="950" cy="265" r="32" fill="url(#nucGrad2)"/>
          <!-- Connector lines -->
          <line x1="210" y1="120" x2="210" y2="280" stroke="#fff" stroke-width="5"/>
          <line x1="370" y1="110" x2="370" y2="260" stroke="#fff" stroke-width="5"/>
          <line x1="570" y1="115" x2="570" y2="270" stroke="#fff" stroke-width="5"/>
          <line x1="780" y1="100" x2="780" y2="282" stroke="#fff" stroke-width="5"/>
          <line x1="950" y1="120" x2="950" y2="265" stroke="#fff" stroke-width="5"/>
        </g>
      </svg>
    </div>
    <div class="container">
        <h1>DNA &#x21C4; Text/Binary Converter</h1>
        <div class="subtitle">
            Encode messages using DNA nitrogen bases.<br>
            Convert freely between text, binary, and DNA code!
        </div>
        <form method="post" autocomplete="off">
            <label for="conversion">Conversion Type:</label>
            <select id="conversion" name="conversion" required>
                <option value="text_to_dna">Text → DNA (A,T,G,C)</option>
                <option value="dna_to_text">DNA → Text</option>
                <option value="binary_to_dna">Binary → DNA</option>
                <option value="dna_to_binary">DNA → Binary</option>
                <option value="text_to_binary">Text → Binary</option>
                <option value="binary_to_text">Binary → Text</option>
            </select>
            <label for="data">Your Input:</label>
            <input type="text" id="data" name="data" required>
            <input type="submit" value="Convert">
        </form>
        {% if result %}
            <div class="result">
                <span><strong>Result:</strong> {{ result }}</span>
            </div>
        {% endif %}
    </div>
    <footer>
        DNA Nitrogen Base Converter &copy; 2025 · Full-Page DNA Neon Theme
    </footer>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        data = request.form['data']
        conversion = request.form['conversion']
        try:
            if conversion == 'text_to_dna':
                result = text_to_dna(data)
            elif conversion == 'dna_to_text':
                result = dna_to_text(data)
            elif conversion == 'binary_to_dna':
                result = binary_to_dna_seq(data)
            elif conversion == 'dna_to_binary':
                result = dna_to_binary_seq(data)
            elif conversion == 'text_to_binary':
                result = text_to_binary(data)
            elif conversion == 'binary_to_text':
                result = binary_to_text(data)
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template_string(HTML, result=result)

if __name__ == '__main__':
    app.run(debug=True)
