document.addEventListener('DOMContentLoaded', () => {
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (loginLink) {
        if (token) {
            loginLink.style.display = 'none';
        } else {
            loginLink.style.display = 'block';
        }
    }


    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); 
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`; 
                    window.location.href = 'index.html'; 
                } else {
                    alert('Login failed: ' + response.statusText);
                }
            } catch (error) {
                console.error('Network Error:', error);
                alert('Connection to API failed.');
            }
        });
    }


    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');
    
    if (placesList) {
        let allPlaces = []; 

        async function fetchPlaces() {
            try {
                const headers = {};
                if (token) headers['Authorization'] = `Bearer ${token}`;

                const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
                    method: 'GET',
                    headers: headers
                });

                if (response.ok) {
                    allPlaces = await response.json();
                    displayPlaces(allPlaces);
                }
            } catch (error) {
                console.error('Error fetching places:', error);
            }
        }

        function displayPlaces(places) {
            placesList.innerHTML = '';
            
            places.forEach((place, index) => {
                const imgNumber = (index % 10) + 1; 
                
                const card = document.createElement('div');
                card.className = 'place-card';
                card.innerHTML = `
                    <img src="imgs/img${imgNumber}.jpg" alt="${place.title}">
                    <h3>${place.title}</h3>
                    <p>Price: $${place.price} per night</p>
                    <a href="place.html?id=${place.id}" class="details-button">View Details</a>
                `;
                placesList.appendChild(card);
            });
        }

        if (priceFilter) {
            priceFilter.addEventListener('change', (event) => {
                const maxPrice = event.target.value;
                if (maxPrice === 'All') {
                    displayPlaces(allPlaces);
                } else {
                    const filtered = allPlaces.filter(place => place.price <= parseInt(maxPrice));
                    displayPlaces(filtered);
                }
            });
        }

        fetchPlaces();
    }
});