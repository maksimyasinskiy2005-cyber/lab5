import os
import logging
from flask import Flask, render_template, redirect, url_for, flash
from forms import ContactForm
from products.routes import products_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-change-in-production'

# Створення директорії для логів
os.makedirs('logs', exist_ok=True)

# Налаштування логування контактної форми
logger = logging.getLogger('contact_logger')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/contact.log', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
if not logger.handlers:
    logger.addHandler(file_handler)

# Реєстрація блюпринта продуктів
app.register_blueprint(products_bp)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            log_entry = (
                f"Name: {form.name.data} | Email: {form.email.data} | "
                f"Phone: {form.phone.data} | Subject: {form.subject.data} | "
                f"Message: {form.message.data}"
            )
            logger.info(log_entry)
            flash("Дякуємо! Ваше повідомлення успішно надіслано та збережено.", "success")
            return redirect(url_for('contact'))
        except Exception as e:
            logger.error(f"Помилка під час запису форми: {e}")
            flash("Виникла помилка під час обробки вашого запиту.", "danger")
            return redirect(url_for('contact'))

    return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
