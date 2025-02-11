# 🍽 Verdant Restaurant Website  

This repository contains the source code for the **Verdant Restaurant** website. The website allows users to view the menu, make reservations, sign up for newsletters, and more. It is built using **Flask (Python web framework)** and uses **SQLite** as the database.  

## 🚀 Features  
- **User Authentication**: Sign up, log in, and log out.  
- **Role-Based Access Control**: Customers and admins have different permissions.  
- **Dynamic Menu**: View categorized menu items with images.  
- **Reservations System**: Book tables with available dates and times.  
- **Admin Panel**: Manage menu items, reservations, and availability.  
- **Staff View**: See all reservations for a selected date.  
- **Events Page**: Browse upcoming restaurant events.  
- **Newsletter Signup**: Subscribe for updates.  

## 🗄 Database Models  
- **User**: Stores user information (name, email, role, etc.).  
- **Reservation**: Stores reservation details (date, time, guests, etc.).  
- **MenuItem**: Stores food item details (name, price, category, etc.).  
- **Availability**: Stores available time slots for reservations.  
- **Events**: Stores upcoming event details.  
- **NewsletterSignup**: Stores subscriber emails.  

## 🔗 Routes  
- `/` - Home Page  
- `/sign_up` - User Registration  
- `/login` - User Login  
- `/menu` - Menu Page  
- `/reservation` - Make a Reservation  
- `/events` - View Events  
- `/staff/reservation` - Admin Reservation Management  
- `/contact_us` - Contact Page  
- `/about_us` - About Page  

## ⚙️ Installation  
1. **Set up a virtual environment**  
   ```bash
      python -m venv venv 
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**
   ```bash
   python app.py
   ```
🌐 Demo
Live Website: https://verdant-vegan-restaurant.onrender.com/


