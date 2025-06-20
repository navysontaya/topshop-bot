from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def extract_product_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find("title").text.strip()[:100]
    image = re.search(r'"image":"(https:[^\"]+)",', response.text)
    price = re.search(r'"price":"(\d+\.\d+)",', response.text)
    discount = re.search(r'"discount":"(\d+)%"', response.text)

    return {
        "title": title,
        "image": image.group(1) if image else None,
        "price": price.group(1) if price else "N/A",
        "discount": discount.group(1) + "%" if discount else "ไม่มีส่วนลด"
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/extract", methods=["POST"])
def extract():
    url = request.form.get("url")
    if not url or "shopee" not in url:
        return jsonify({"error": "กรุณาวางลิงก์ Shopee ที่ถูกต้อง"})

    data = extract_product_info(url)
    aff_url = url.split('?')[0] + "?sub_id=psfb168"

    post_text = f"✨ สัมผัสแบบนี้... คุณเคยลองหรือยัง?\n🚚 พร้อมส่ง ⚡️ ส่งไว 💰 เก็บเงินปลายทาง\n👉 กดตรงนี้: {aff_url}"

    return jsonify({
        "title": data['title'],
        "price": data['price'],
        "image": data['image'],
        "discount": data['discount'],
        "aff_url": aff_url,
        "post": post_text
    })

if __name__ == "__main__":
    app.run(debug=True)