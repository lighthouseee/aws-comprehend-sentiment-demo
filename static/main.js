// --- main.js ---

// Bước 1: "DOMContentLoaded" đảm bảo code chỉ chạy khi toàn bộ trang HTML đã được tải xong.
document.addEventListener('DOMContentLoaded', () => {

    // Bước 2: Lấy các element quan trọng từ HTML để tương tác.
    const analyzeBtn = document.getElementById('analyzeBtn');
    const inputText = document.getElementById('inputText');
    const resultContainer = document.getElementById('result');
    const resultPre = resultContainer.querySelector('pre');
    const loader = document.getElementById('loader');

    // Bước 3: Gắn một hàm xử lý sự kiện vào nút bấm.
    // Hàm này sẽ được gọi mỗi khi người dùng click vào nút "Phân Tích".
    analyzeBtn.addEventListener('click', async () => {

        // Lấy văn bản từ ô textarea
        const text = inputText.value;

        // Kiểm tra xem người dùng có nhập gì không
        if (!text.trim()) {
            resultContainer.className = 'error'; // Thêm lớp CSS để báo lỗi
            resultPre.textContent = 'Lỗi: Vui lòng nhập văn bản.';
            return; // Dừng hàm tại đây
        }

        // --- Chuẩn bị giao diện cho việc gọi API ---
        loader.style.display = 'block';         // Hiển thị vòng xoay loading
        resultContainer.className = '';         // Xóa các màu kết quả cũ
        resultPre.textContent = 'Đang phân tích...';
        analyzeBtn.disabled = true;             // Vô hiệu hóa nút bấm để tránh spam click

        try {
            // Bước 4: Gửi yêu cầu đến Backend bằng Fetch API
            const response = await fetch('/analyze', {
                method: 'POST', // Phương thức là POST vì chúng ta gửi dữ liệu đi
                headers: {
                    'Content-Type': 'application/json' // Báo cho server biết ta gửi dữ liệu JSON
                },
                // Chuyển object JavaScript thành chuỗi JSON để gửi đi
                body: JSON.stringify({ text: text })
            });

            // Bước 5: Chuyển đổi phản hồi từ server thành object JSON
            const data = await response.json();

            // Bước 6: Cập nhật giao diện với kết quả nhận được
            if (data.error) {
                // Nếu có lỗi do server trả về
                resultContainer.className = 'error';
                resultPre.textContent = `Lỗi: ${data.error}`;
            } else {
                // Nếu thành công
                // Thêm lớp CSS màu tương ứng với kết quả (positive, negative, etc.)
                resultContainer.classList.add(data.Sentiment.toLowerCase());

                // Hiển thị kết quả JSON đã được định dạng đẹp
                resultPre.textContent = JSON.stringify(data, null, 2);
            }

        } catch (error) {
            // Xử lý các lỗi mạng (ví dụ: mất kết nối internet, server backend bị sập)
            resultContainer.className = 'error';
            resultPre.textContent = `Đã xảy ra lỗi khi kết nối đến server: ${error}`;
            console.error("Fetch Error:", error); // In lỗi chi tiết ra console cho lập trình viên
        } finally {
            // Bước 7: Dọn dẹp giao diện sau khi có kết quả (bất kể thành công hay thất bại)
            loader.style.display = 'none';      // Ẩn vòng xoay loading
            analyzeBtn.disabled = false;        // Kích hoạt lại nút bấm
        }
    });
});