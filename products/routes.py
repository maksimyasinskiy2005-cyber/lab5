import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from tinydb import TinyDB, Query
from forms import ProductForm

products_bp = Blueprint(
    'products',
    __name__,
    template_folder='../templates/products'
)

def get_db():
    os.makedirs('data', exist_ok=True)
    return TinyDB('data/products.json')

def get_next_id(db):
    items = db.all()
    if not items:
        return 1
    return max(item['id'] for item in items) + 1

@products_bp.route('/product', methods=['GET'])
def list_products():
    db = get_db()
    products = db.all()
    return render_template('list.html', products=products)

@products_bp.route('/product/<int:id>', methods=['GET'])
def detail_product(id):
    db = get_db()
    Product = Query()
    product = db.get(Product.id == id)
    if not product:
        abort(404, description="Товар не знайдено")
    return render_template('detail.html', product=product)

@products_bp.route('/product/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            file = form.image.data
            ext = os.path.splitext(file.filename)[1].lower()
            filename = f"{uuid.uuid4().hex}{ext}"
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, filename))
            image_path = f"uploads/{filename}"

        db = get_db()
        product_data = {
            'id': get_next_id(db),
            'name': form.name.data,
            'content': form.content.data,
            'price': float(form.price.data),
            'category': form.category.data,
            'quantity': form.quantity.data,
            'image': image_path,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        db.insert(product_data)
        flash("Товар успішно додано!", "success")
        return redirect(url_for('products.list_products'))

    return render_template('add.html', form=form)

@products_bp.route('/product/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    db = get_db()
    Product = Query()
    product = db.get(Product.id == id)
    if not product:
        abort(404, description="Товар не знайдено")

    form = ProductForm(data=product)

    if form.validate_on_submit():
        image_path = product.get('image')
        if form.image.data:
            file = form.image.data
            ext = os.path.splitext(file.filename)[1].lower()
            filename = f"{uuid.uuid4().hex}{ext}"
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, filename))
            image_path = f"uploads/{filename}"

        updated_data = {
            'name': form.name.data,
            'content': form.content.data,
            'price': float(form.price.data),
            'category': form.category.data,
            'quantity': form.quantity.data,
            'image': image_path
        }
        db.update(updated_data, Product.id == id)
        flash("Дані про товар успішно оновлено!", "success")
        return redirect(url_for('products.detail_product', id=id))

    return render_template('edit.html', form=form, product=product)

@products_bp.route('/product/<int:id>/delete', methods=['POST'])
def delete_product(id):
    db = get_db()
    Product = Query()
    if not db.contains(Product.id == id):
        abort(404, description="Товар не знайдено")
    db.remove(Product.id == id)
    flash("Товар успішно видалено!", "warning")
    return redirect(url_for('products.list_products'))
