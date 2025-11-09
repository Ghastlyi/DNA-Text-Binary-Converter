from flask import Flask, render_template_string, request

app = Flask(__name__)

binary_to_dna = {'00': 'A', '01': 'T', '10': 'G', '11': 'C'}
dna_to_binary = {v: k for k, v in binary_to_dna.items()}

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    # Ensure binary length is multiple of 8 by removing extra bits
    binary = binary[:len(binary) - (len(binary) % 8)]
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chars if len(b) == 8)

def binary_to_dna_seq(binary):
    # Remove any spaces and ensure even length
    binary = binary.replace(' ', '')
    if len(binary) % 2 != 0:
        binary = binary[:-1]  # Remove last bit to make even
    return ''.join(binary_to_dna.get(binary[i:i+2], '?') for i in range(0, len(binary), 2))

def dna_to_binary_seq(dna):
    # Remove any spaces and convert to uppercase
    dna = dna.upper().replace(' ', '')
    binary = ''
    for base in dna:
        if base in dna_to_binary:
            binary += dna_to_binary[base]
        else:
            binary += '??'
    return binary

def text_to_dna(text):
    binary = text_to_binary(text)
    return binary_to_dna_seq(binary)

def dna_to_text(dna):
    binary = dna_to_binary_seq(dna)
    return binary_to_text(binary)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Converter | DNA Genetic Encoding</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --primary: #00f0ff;
            --secondary: #7b42f6;
            --accent: #00ff88;
            --dark: #0a0e17;
            --darker: #050811;
            --card-bg: rgba(10, 14, 23, 0.9);
            --glow: 0 0 20px;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body {
            min-height: 100vh;
            font-family: 'Rajdhani', monospace;
            background: var(--darker);
            color: #e0f7fa;
            overflow-x: hidden;
            position: relative;
        }

        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                linear-gradient(45deg, var(--darker) 0%, var(--dark) 100%),
                repeating-linear-gradient(0deg, 
                    transparent 0px, 
                    transparent 1px, 
                    rgba(0, 240, 255, 0.03) 2px, 
                    transparent 3px
                );
            z-index: 1;
        }

        .dna-helix-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 2;
            opacity: 0.15;
        }

        .helix {
            position: absolute;
            width: 2px;
            height: 200px;
            background: linear-gradient(to bottom, transparent, var(--primary), transparent);
            animation: float 15s infinite linear;
        }

        .helix::before, .helix::after {
            content: '';
            position: absolute;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent);
            left: -3px;
        }

        .helix::before { top: 0; animation: pulse 2s infinite; }
        .helix::after { bottom: 0; animation: pulse 2s infinite 1s; }

        @keyframes float {
            0% { transform: translateY(100vh) rotate(0deg); }
            100% { transform: translateY(-100vh) rotate(360deg); }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.5); opacity: 0.5; }
        }

        .container {
            position: relative;
            z-index: 3;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 60px;
            padding: 60px 40px;
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            border: 1px solid rgba(0, 240, 255, 0.3);
            box-shadow: 
                var(--glow) rgba(0, 240, 255, 0.3),
                inset 0 0 100px rgba(0, 240, 255, 0.1);
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(
                transparent, 
                rgba(0, 240, 255, 0.1), 
                transparent 30%
            );
            animation: rotate 10s linear infinite;
        }

        @keyframes rotate {
            100% { transform: rotate(360deg); }
        }

        .logo {
            font-size: 4em;
            margin-bottom: 20px;
            filter: drop-shadow(0 0 20px var(--primary));
        }

        h1 {
            font-size: 3.5em;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            font-weight: 700;
            letter-spacing: 3px;
        }

        .subtitle {
            font-size: 1.4em;
            color: #88e0f7;
            margin-bottom: 10px;
            line-height: 1.6;
        }

        .mba-tech {
            font-size: 1.1em;
            color: rgba(136, 224, 247, 0.7);
            margin-bottom: 30px;
            font-style: italic;
        }

        .converter-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }

        @media (max-width: 968px) {
            .converter-grid {
                grid-template-columns: 1fr;
            }
        }

        .converter-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 40px;
            border: 1px solid rgba(123, 66, 246, 0.3);
            box-shadow: 
                var(--glow) rgba(123, 66, 246, 0.2),
                inset 0 0 80px rgba(123, 66, 246, 0.1);
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .converter-card:hover {
            transform: translateY(-5px);
            box-shadow: 
                0 15px 30px rgba(123, 66, 246, 0.3),
                var(--glow) rgba(123, 66, 246, 0.2),
                inset 0 0 80px rgba(123, 66, 246, 0.1);
        }

        .converter-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(123, 66, 246, 0.1),
                transparent
            );
            transition: left 0.6s;
        }

        .converter-card:hover::before {
            left: 100%;
        }

        .card-title {
            font-size: 1.6em;
            color: var(--secondary);
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .form-group {
            margin-bottom: 25px;
        }

        label {
            display: block;
            color: var(--primary);
            font-size: 1.1em;
            margin-bottom: 12px;
            font-weight: 600;
        }

        select, input[type="text"], textarea {
            width: 100%;
            padding: 18px 20px;
            background: rgba(15, 20, 35, 0.8);
            border: 2px solid var(--primary);
            border-radius: 12px;
            color: #e0f7fa;
            font-size: 1.1em;
            font-family: inherit;
            transition: all 0.3s ease;
            resize: vertical;
        }

        select:focus, input[type="text"]:focus, textarea:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.3);
        }

        .btn-convert {
            width: 100%;
            padding: 20px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            border-radius: 12px;
            color: var(--darker);
            font-size: 1.3em;
            font-weight: 700;
            letter-spacing: 2px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            position: relative;
            overflow: hidden;
        }

        .btn-convert::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }

        .btn-convert:hover::before {
            left: 100%;
        }

        .btn-convert:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0, 240, 255, 0.4);
        }

        .result-container {
            margin-top: 30px;
            animation: slideUp 0.5s ease-out;
            position: relative;
        }

        @keyframes slideUp {
            from { 
                opacity: 0; 
                transform: translateY(20px); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0); 
            }
        }

        .result-label {
            color: var(--accent);
            font-size: 1.2em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .result-box {
            background: rgba(15, 20, 35, 0.9);
            border: 2px solid var(--accent);
            border-radius: 12px;
            padding: 25px;
            color: #e0f7fa;
            font-size: 1.1em;
            word-break: break-all;
            min-height: 100px;
            max-height: 300px;
            overflow-y: auto;
            box-shadow: inset 0 0 30px rgba(0, 255, 136, 0.1);
        }

        .footer {
            text-align: center;
            margin-top: 60px;
            padding: 30px;
            color: #88e0f7;
            font-size: 1em;
            border-top: 1px solid rgba(0, 240, 255, 0.2);
        }

        .made-by {
            color: rgba(136, 224, 247, 0.3);
            font-size: 0.8em;
            margin-top: 10px;
            font-style: italic;
        }

        .copy-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0, 240, 255, 0.2);
            border: 1px solid var(--primary);
            color: var(--primary);
            border-radius: 6px;
            padding: 6px 12px;
            cursor: pointer;
            font-size: 0.8em;
            transition: all 0.3s ease;
            font-family: inherit;
            z-index: 10;
        }

        .copy-btn:hover {
            background: rgba(0, 240, 255, 0.3);
            transform: scale(1.05);
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Advanced Background -->
    <div class="matrix-bg"></div>
    
    <div class="dna-helix-container" id="helixContainer"></div>

    <div class="container">
        <div class="header">
            <div class="logo">🧬</div>
            <h1>DNA Genetic Encoder</h1>
            <div class="subtitle">
                Advanced DNA Genetic Encoding System<br>
                Convert between Text, Binary, and DNA sequences with precision
            </div>
            <div class="mba-tech">MBA TECH A DIV</div>
        </div>

        <div class="converter-grid">
            <!-- Encoder Card -->
            <div class="converter-card">
                <div class="card-title">🔮 Encoder</div>
                <form method="post" autocomplete="off">
                    <input type="hidden" name="form_type" value="encoder">
                    <div class="form-group">
                        <label for="conversion">Conversion Mode</label>
                        <select id="conversion" name="conversion" required>
                            <option value="text_to_dna">📝 Text → 🧬 DNA Sequence</option>
                            <option value="text_to_binary">📝 Text → 🔢 Binary</option>
                            <option value="binary_to_dna">🔢 Binary → 🧬 DNA Sequence</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="data">Input Data</label>
                        <textarea 
                            id="data" 
                            name="data" 
                            required 
                            rows="4"
                            placeholder="Enter your text or binary code to encode..."
                        >{{ encoder_data if encoder_data else '' }}</textarea>
                    </div>

                    <button type="submit" class="btn-convert">
                        🚀 Encode Data
                    </button>
                </form>

                {% if encoder_result %}
                <div class="result-container">
                    <div class="result-label">📊 Encoded Output</div>
                    <button class="copy-btn" onclick="copyToClipboard('{{ encoder_result }}')">Copy</button>
                    <div class="result-box">{{ encoder_result }}</div>
                </div>
                {% endif %}
            </div>

            <!-- Decoder Card -->
            <div class="converter-card">
                <div class="card-title">🔍 Decoder</div>
                <form method="post" autocomplete="off">
                    <input type="hidden" name="form_type" value="decoder">
                    <div class="form-group">
                        <label for="conversion2">Conversion Mode</label>
                        <select id="conversion2" name="conversion" required>
                            <option value="dna_to_text">🧬 DNA Sequence → 📝 Text</option>
                            <option value="dna_to_binary">🧬 DNA Sequence → 🔢 Binary</option>
                            <option value="binary_to_text">🔢 Binary → 📝 Text</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="data2">Input Data</label>
                        <textarea 
                            id="data2" 
                            name="data" 
                            required 
                            rows="4"
                            placeholder="Enter DNA sequence or binary code to decode..."
                        >{{ decoder_data if decoder_data else '' }}</textarea>
                    </div>

                    <button type="submit" class="btn-convert">
                        🔓 Decode Data
                    </button>
                </form>

                {% if decoder_result %}
                <div class="result-container">
                    <div class="result-label">📊 Decoded Output</div>
                    <button class="copy-btn" onclick="copyToClipboard('{{ decoder_result }}')">Copy</button>
                    <div class="result-box">{{ decoder_result }}</div>
                </div>
                {% endif %}
            </div>
        </div>

        <div class="footer">
            Converter &copy; 2025 | DNA Genetic Encoding Technology
            <div class="made-by">Made By Parth Pawar</div>
        </div>
    </div>

    <script>
        // Create floating DNA helixes
        function createHelixes() {
            const container = document.getElementById('helixContainer');
            for (let i = 0; i < 15; i++) {
                const helix = document.createElement('div');
                helix.className = 'helix';
                helix.style.left = Math.random() * 100 + 'vw';
                helix.style.animationDelay = Math.random() * 15 + 's';
                container.appendChild(helix);
            }
        }

        // Copy to clipboard function
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                // Show a subtle notification instead of alert
                const copyBtn = event.target;
                const originalText = copyBtn.textContent;
                copyBtn.textContent = 'Copied!';
                copyBtn.style.background = 'rgba(0, 255, 136, 0.3)';
                copyBtn.style.borderColor = 'var(--accent)';
                
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                    copyBtn.style.background = 'rgba(0, 240, 255, 0.2)';
                    copyBtn.style.borderColor = 'var(--primary)';
                }, 2000);
            }, function(err) {
                console.error('Could not copy text: ', err);
                alert('Failed to copy to clipboard');
            });
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            createHelixes();

            // Add interactive effects
            const inputs = document.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                input.addEventListener('focus', function() {
                    this.parentElement.style.transform = 'scale(1.02)';
                });
                
                input.addEventListener('blur', function() {
                    this.parentElement.style.transform = 'scale(1)';
                });
            });

            // Update placeholders based on selection
            const conversionSelects = document.querySelectorAll('select[name="conversion"]');
            conversionSelects.forEach(select => {
                select.addEventListener('change', function() {
                    const textarea = this.closest('form').querySelector('textarea');
                    const options = {
                        'text_to_dna': 'Enter text to convert to DNA sequence...',
                        'text_to_binary': 'Enter text to convert to binary...',
                        'binary_to_dna': 'Enter binary code (e.g., 01001000) to convert to DNA...',
                        'dna_to_text': 'Enter DNA sequence (e.g., ATGC) to decode to text...',
                        'dna_to_binary': 'Enter DNA sequence to convert to binary...',
                        'binary_to_text': 'Enter binary code to decode to text...'
                    };
                    textarea.placeholder = options[this.value] || 'Enter data...';
                });
            });
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    encoder_result = None
    decoder_result = None
    encoder_data = ''
    decoder_data = ''
    
    if request.method == 'POST':
        data = request.form['data'].strip()
        conversion = request.form['conversion']
        form_type = request.form.get('form_type', '')
        
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
            else:
                result = "Invalid conversion type"
                
            # Store results based on form type
            if form_type == 'encoder':
                encoder_result = result
                encoder_data = data
            elif form_type == 'decoder':
                decoder_result = result
                decoder_data = data
                
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            if form_type == 'encoder':
                encoder_result = error_msg
                encoder_data = data
            elif form_type == 'decoder':
                decoder_result = error_msg
                decoder_data = data
    
    return render_template_string(
        HTML_TEMPLATE, 
        encoder_result=encoder_result,
        decoder_result=decoder_result,
        encoder_data=encoder_data,
        decoder_data=decoder_data
    )

if __name__ == '__main__':
    app.run(debug=True)
