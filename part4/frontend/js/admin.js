const API_URL = 'https://hbnb.onrender.com/api/v1/users/';

// دالة لاستخراج التوكن من المتصفح
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

async function fetchUsers() {
    const token = getCookie('token');
    
    // الطرد الفوري إذا لم يكن المستخدم مسجلاً للدخول
    if (!token) {
        alert("Access Denied! Admins only.");
        window.location.href = 'index.html';
        return;
    }

    const tableBody = document.getElementById('users-table-body');
    
    try {
        const response = await fetch(API_URL, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}` // إرسال هويتك للسيرفر
            }
        });
        
        // الطرد الفوري إذا رفض السيرفر الطلب (إذا لم يكن الإيميل مطابقاً)
        if (response.status === 403 || response.status === 401) {
            alert("Access Denied! Admins only.");
            window.location.href = 'index.html';
            return;
        }
        
        if (!response.ok) throw new Error('Failed to fetch users');
        
        const users = await response.json();
        tableBody.innerHTML = ''; // تنظيف الجدول
        
        if (users.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding: 20px;">No users found.</td></tr>';
            return;
        }
        
        // رسم البيانات
        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="font-size: 0.85rem; color: #717171;">${user.id}</td>
                <td><strong>${user.first_name}</strong></td>
                <td><strong>${user.last_name}</strong></td>
                <td><a href="mailto:${user.email}" style="color: #3a5a40; text-decoration: none;">${user.email}</a></td>
            `;
            tableBody.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error fetching users:', error);
        tableBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color: #e63946; padding: 20px;">Error loading users.</td></tr>';
    }
}

document.addEventListener('DOMContentLoaded', fetchUsers);