import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SelectField, DecimalField, IntegerField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange, InputRequired, ValidationError

def validate_image_size(form, field):
    """Перевірка розміру завантажуваного зображення (макс. 5 МБ)"""
    if field.data and hasattr(field.data, 'read'):
        field.data.seek(0, os.SEEK_END)
        file_size = field.data.tell()
        field.data.seek(0)
        max_size = 5 * 1024 * 1024  # 5 MB
        if file_size > max_size:
            raise ValidationError('Розмір файлу не повинен перевищувати 5 МБ.')

class ContactForm(FlaskForm):
    """Форма зворотного зв'язку"""
    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Це поле є обов'язковим"),
            Length(min=4, max=10, message="Ім'я повинно містити від 4 до 10 символів")
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Це поле є обов'язковим"),
            Email(message="Некоректний формат електронної пошти")
        ]
    )
    phone = StringField(
        "Phone",
        validators=[
            DataRequired(message="Це поле є обов'язковим"),
            Regexp(r'^\+380\d{9}$', message="Формат телефону повинен бути: +380XXXXXXXXX")
        ]
    )
    subject = SelectField(
        "Subject",
        choices=[
            ('general', 'Загальне питання'),
            ('tech', 'Технічна підтримка'),
            ('billing', 'Оплата та рахунки'),
            ('other', 'Інше')
        ],
        validators=[DataRequired(message="Оберіть тему")]
    )
    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Це поле є обов'язковим"),
            Length(max=500, message="Повідомлення не повинно перевищувати 500 символів")
        ]
    )
    submit = SubmitField("Send Message")

class ProductForm(FlaskForm):
    """Форма для створення та редагування товарів"""
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Вкажіть назву товару"),
            Length(min=3, message="Назва повинна містити мінімум 3 символи")
        ]
    )
    content = TextAreaField(
        "Опис товару",
        render_kw={"rows": 5, "cols": 40},
        validators=[DataRequired(message="Заповніть опис товару")]
    )
    price = DecimalField(
        "Ціна",
        places=2,
        validators=[
            DataRequired(message="Вкажіть ціну"),
            NumberRange(min=0.01, message="Ціна повинна бути додатною")
        ]
    )
    category = SelectField(
        "Категорія",
        choices=[
            ('electronics', 'Електроніка'),
            ('clothing', 'Одяг'),
            ('books', 'Книги'),
            ('home', 'Дім та сад')
        ],
        validators=[DataRequired(message="Оберіть категорію")]
    )
    quantity = IntegerField(
        "Кількість",
        validators=[
            InputRequired(message="Укажіть кількість"),
            NumberRange(min=0, message="Кількість не може бути від'ємною")
        ]
    )
    image = FileField(
        "Зображення товару",
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png'], 'Дозволено тільки формати PNG, JPG та JPEG'),
            validate_image_size
        ]
    )
    submit = SubmitField("Зберегти")
