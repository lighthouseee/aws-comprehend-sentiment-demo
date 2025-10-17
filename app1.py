# app.py (Phiên bản gọi API thật của AWS)

from flask import Flask, request, jsonify, render_template
import boto3

app = Flask(__name__)

try:
    comprehend_client = boto3.client(
        'comprehend',
        region_name='us-east-1'
    )
    print("✅ Boto3 client đã được khởi tạo thành công.")
except Exception as e:
    print(f"❌ LỖI: Không thể khởi tạo Boto3 client: {e}")
    comprehend_client = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    if not comprehend_client:
        return jsonify({"error": "AWS Comprehend client chưa được cấu hình đúng."}), 500

    data = request.get_json()

    if not data or 'text' not in data or not data['text'].strip():
        return jsonify({"error": "Vui lòng cung cấp văn bản để phân tích."}), 400

    text_to_analyze = data['text']

    try:
        print(f"➡️  Đang gửi văn bản tới AWS Comprehend: '{text_to_analyze[:40]}...'")
        response = comprehend_client.detect_sentiment(
            Text=text_to_analyze,
            LanguageCode='en'
        )
        print("⬅️  Đã nhận phản hồi từ AWS.")

        sentiment_result = {
            "Sentiment": response.get("Sentiment"),
            "SentimentScore": response.get("SentimentScore")
        }
        return jsonify(sentiment_result)
    except Exception as e:
        print(f"❌ LỖI từ API của AWS: {e}")
        return jsonify({"error": f"Lỗi từ API của AWS: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)