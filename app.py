"""
WhatsApp Chat Analyzer - Flask Backend
Main application file
"""

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import traceback

from whatsapp_parser import parse_whatsapp_chat
from ai_analyzer import WhatsAppAIAnalyzer

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'WhatsApp Chat Analyzer'})


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze WhatsApp chat file
    Expects a file upload with key 'chat_file'
    """
    try:
        # Check if file is present in request
        if 'chat_file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400

        file = request.files['chat_file']

        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400

        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Please upload a .txt file'
            }), 400

        # Read file content
        try:
            # Try UTF-8 first
            content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            # Fallback to latin-1 if UTF-8 fails
            file.seek(0)
            content = file.read().decode('latin-1')

        # Validate content
        if not content or len(content.strip()) == 0:
            return jsonify({
                'success': False,
                'error': 'File is empty'
            }), 400

        # Parse WhatsApp chat
        try:
            parsed_data = parse_whatsapp_chat(content)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to parse WhatsApp chat: {str(e)}'
            }), 400

        # Validate parsed data
        if parsed_data['message_count'] == 0:
            return jsonify({
                'success': False,
                'error': 'No valid messages found in the file. Please ensure this is a WhatsApp chat export.'
            }), 400

        # Initialize AI analyzer
        try:
            analyzer = WhatsAppAIAnalyzer()
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': 'AI analyzer not configured. Please set ANTHROPIC_API_KEY in .env file'
            }), 500

        # Run AI analysis
        analysis_result = analyzer.analyze_conversation(
            chat_text=parsed_data['text'],
            participants=parsed_data['participants']
        )

        if not analysis_result['success']:
            return jsonify({
                'success': False,
                'error': f"Analysis failed: {analysis_result.get('error', 'Unknown error')}"
            }), 500

        # Combine parsed data with analysis
        response = {
            'success': True,
            'metadata': {
                'participants': parsed_data['participants'],
                'message_count': parsed_data['message_count'],
                'date_range': parsed_data['date_range']
            },
            'analysis': analysis_result['analysis']
        }

        return jsonify(response)

    except Exception as e:
        # Log the full error for debugging
        print(f"Error in /analyze endpoint: {str(e)}")
        print(traceback.format_exc())

        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/quick-parse', methods=['POST'])
def quick_parse():
    """
    Quick parse endpoint - just parses the file without AI analysis
    Useful for testing or quick metadata extraction
    """
    try:
        if 'chat_file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400

        file = request.files['chat_file']

        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Please upload a .txt file'
            }), 400

        # Read and parse
        try:
            content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            file.seek(0)
            content = file.read().decode('latin-1')

        parsed_data = parse_whatsapp_chat(content)

        return jsonify({
            'success': True,
            'data': parsed_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    # Run the Flask app
    print("🚀 Starting WhatsApp Chat Analyzer...")
    print("📝 Make sure you have set ANTHROPIC_API_KEY in your .env file")
    print("🌐 Access the application at: http://localhost:5000")

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
