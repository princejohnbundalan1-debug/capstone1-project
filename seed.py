from app import create_app
from extensions import db, bcrypt
from models import User, Product, Customer, Sale, SaleItem, InventoryLog, Branch
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    # 1. Ensure tables exist
    db.create_all()

    # 2. Create Branches (using a loop to check each one)
    print("Checking branches...")
    branch_data = [
        {'name': 'Tagbak Branch', 'location': 'Iloilo City'},
        {'name': 'Zarraga Branch', 'location': 'Iloilo'},
        {'name': 'Leganes Branch', 'location': 'Iloilo'}
    ]
    
    for b_info in branch_data:
        if not Branch.query.filter_by(name=b_info['name']).first():
            new_branch = Branch(name=b_info['name'], location=b_info['location'])
            db.session.add(new_branch)
    
    db.session.commit()

    # Re-fetch branches to get their IDs
    b1 = Branch.query.filter_by(name='Tagbak Branch').first()
    b2 = Branch.query.filter_by(name='Zarraga Branch').first()
    b3 = Branch.query.filter_by(name='Leganes Branch').first()

    # 3. Create Users (Checking one by one)
    print("Checking users...")
    pw_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
    
    user_data = [
        {'username': 'admin', 'email': 'rreynieljosh@gmail.com', 'role': 'admin', 'branch_id': b1.id},
        {'username': 'staff_tagbak', 'email': 'staff_tag@h2ops.com', 'role': 'staff', 'branch_id': b1.id},
        {'username': 'staff_zarraga', 'email': 'staff_zar@h2ops.com', 'role': 'staff', 'branch_id': b2.id},
        {'username': 'staff_leganes', 'email': 'staff_leg@h2ops.com', 'role': 'staff', 'branch_id': b3.id}
    ]

    for u_info in user_data:
        if not User.query.filter_by(username=u_info['username']).first():
            new_user = User(
                username=u_info['username'],
                email=u_info['email'],
                password_hash=pw_hash,
                role=u_info['role'],
                branch_id=u_info['branch_id']
            )
            db.session.add(new_user)
    
    db.session.commit()

    # 4. Create Products
    print("Checking products...")
    branches = [b1, b2, b3]
    for b in branches:
        product_name = f'Mineral Water - {b.name}'
        if not Product.query.filter_by(name=product_name, branch_id=b.id).first():
            p1 = Product(name=product_name, type='Mineral', price=40.0, current_stock=250, branch_id=b.id)
            db.session.add(p1)
            
    db.session.commit()
    print("Database sync complete!")
