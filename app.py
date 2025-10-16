# app.py

# --- Bước 1: Import các thư viện cần thiết ---
from flask import Flask, request, jsonify, render_template
# import boto3  # <<< TẠM THỜI VÔ HIỆU HÓA BOTO3
from textblob import TextBlob # <<< THÊM THƯ VIỆN TEXTBLOB

# --- Bước 2: Khởi tạo ứng dụng Flask ---
app = Flask(_name_)

# --- BƯỚC 3 (TẠM THỜI VÔ HIỆU HÓA): Khởi tạo Boto3 client ---
# try:
#     comprehend_client = boto3.client(
#         'comprehend',
#         region_name='us-east-1'
#     )
#     print("Boto3 client đã được khởi tạo thành công.")
# except Exception as e:
#     print(f"LỖI: Không thể khởi tạo Boto3 client: {e}")
#     comprehend_client = None

# --- BƯỚC 3 (THAY THẾ): Hàm phân tích cảm xúc cục bộ bằng TextBlob ---
# Hàm này sẽ được sử dụng trong khi chờ tài khoản AWS được kích hoạt.
def detect_sentiment_local(text):
    """
    Phân tích cảm xúc bằng TextBlob và trả về kết quả
    theo định dạng giống AWS Comprehend để dễ dàng thay thế.
    """
    print(f"Đang phân tích cục bộ bằng TextBlob: '{text[:30]}...'")
    analysis = TextBlob(text)

    # Quy đổi điểm polarity của TextBlob [-1, 1] sang định dạng của AWS
    if analysis.sentiment.polarity > 0.1:
        sentiment = "POSITIVE"
    elif analysis.sentiment.polarity < -0.1:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    # Tạo một dictionary có cấu trúc giống hệt phản hồi của AWS Comprehend
    response = {
        'Sentiment': sentiment,
        'SentimentScore': {
            'Positive': analysis.sentiment.polarity if analysis.sentiment.polarity > 0 else 0,
            'Negative': -analysis.sentiment.polarity if analysis.sentiment.polarity < 0 else 0,
            'Neutral': 1.0 - abs(analysis.sentiment.polarity),
            'Mixed': 0.0  # TextBlob không có điểm Mixed
        }
    }
    print("Đã hoàn tất phân tích bằng TextBlob.")
    return response

# --- Bước 4: Định nghĩa Route cho trang chủ ---
@app.route('/')
def home():
    return render_template('index.html')

# --- Bước 5: Định nghĩa API Endpoint để phân tích cảm xúc ---
@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    """
    Hàm này nhận văn bản, gọi hàm phân tích (hiện tại là TextBlob) và trả kết quả.
    """
    data = request.get_json()

    if not data or 'text' not in data or not data['text'].strip():
        return jsonify({"error": "Vui lòng cung cấp văn bản để phân tích."}), 400

    text_to_analyze = data['text']

    try:
        # --- THAY ĐỔI QUAN TRỌNG ---
        # Dòng code gọi AWS Comprehend đã được thay thế bằng hàm cục bộ.

        # === CÁCH 1: DÙNG TEXTBLOB (HIỆN TẠI) ===
        response = detect_sentiment_local(text_to_analyze)

        # === CÁCH 2: DÙNG AWS COMPREHEND (KHI TÀI KHOẢN ĐÃ KÍCH HOẠT) ===
        # Khi tài khoản AWS của bạn hoạt động, hãy xóa dòng code trên
        # và bỏ comment (dấu #) cho đoạn code dưới đây.
        # ------------------------------------------------------------------
        # if not comprehend_client:
        #    return jsonify({"error": "AWS Comprehend client chưa được cấu hình đúng."}), 500
        # print(f"Đang gửi văn bản tới AWS Comprehend: '{text_to_analyze[:30]}...'")
        # response_aws = comprehend_client.detect_sentiment(
        #     Text=text_to_analyze,
        #     LanguageCode='en'
        # )
        # print("Đã nhận phản hồi từ AWS.")
        # response = {
        #     "Sentiment": response_aws.get("Sentiment"),
        #     "SentimentScore": response_aws.get("SentimentScore")
        # }
        # ------------------------------------------------------------------

        # Trả kết quả về cho Frontend dưới dạng JSON
        return jsonify(response)

    except Exception as e:
        # Xử lý các lỗi có thể xảy ra
        print(f"LỖI: {e}")
        return jsonify({"error": f"Đã xảy ra lỗi: {str(e)}"}), 500

# --- Bước 6: Chạy ứng dụng ---
if _name_ == '_main_':
    # Sửa lỗi cú pháp name và main thành _name_ và _main_
    app.run(debug=True, port=5000)