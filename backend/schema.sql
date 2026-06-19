-- Pharmacy Management System - Database Schema
-- Run this in Supabase SQL Editor (https://supabase.com)

-- 1. Suppliers table (created first because medicines reference it)
CREATE TABLE IF NOT EXISTS suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(150),
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(150),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role VARCHAR(50) DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. Medicines table
CREATE TABLE IF NOT EXISTS medicines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    expiry_date DATE NOT NULL,
    supplier_id INTEGER REFERENCES suppliers(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 4. Customers table
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(150) UNIQUE,
    address TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 5. Sales table
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    medicine_id INTEGER NOT NULL REFERENCES medicines(id),
    user_id INTEGER REFERENCES users(id),
    quantity_sold INTEGER NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    sale_date TIMESTAMP DEFAULT NOW()
);

-- 6. Prescriptions table
CREATE TABLE IF NOT EXISTS prescriptions (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    medicine_id INTEGER NOT NULL REFERENCES medicines(id),
    dosage VARCHAR(100) NOT NULL,
    duration VARCHAR(100) NOT NULL,
    prescribed_by VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Sample data for testing
INSERT INTO suppliers (name, contact_person, phone, email) VALUES
('MediSupply Co.', 'Ali Raza', '0300-1111111', 'ali@medisupply.com'),
('Pharma Distributors', 'Sara Khan', '0300-2222222', 'sara@pharma.com');

INSERT INTO medicines (name, category, quantity, price, expiry_date, supplier_id) VALUES
('Panadol', 'Painkiller', 150, 25.00, '2027-06-01', 1),
('Augmentin', 'Antibiotic', 80, 350.00, '2026-12-15', 1),
('Vitamin C', 'Supplement', 200, 150.00, '2027-03-20', 2),
('Insulin', 'Diabetes', 5, 1200.00, '2026-08-10', 2);

INSERT INTO customers (name, phone, email, address) VALUES
('Ahmed Hassan', '0300-3333333', 'ahmed@email.com', 'Lahore'),
('Fatima Ali', '0300-4444444', 'fatima@email.com', 'Karachi');
