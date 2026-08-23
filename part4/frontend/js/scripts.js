document.addEventListener('DOMContentLoaded', () => {

    
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) {
            const token = parts.pop().split(';').shift();
            return (token === 'undefined' || token === 'null' || token === '') ? null : token;
        }
        return null;
    }

    function parseJwt(token) {
        try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
            return JSON.parse(jsonPayload);
        } catch (e) { return null; }
    }

    const token = getCookie('token');
    const tokenData = token ? parseJwt(token) : null;
    const currentUserId = tokenData ? tokenData.sub : null;

    function extractData(rawDesc) {
        let desc = rawDesc || "";
        let urls = [];
        if (desc.includes('[IMG:')) {
            const parts = desc.split('[IMG:');
            desc = parts[0].trim();
            const urlStr = parts[1].replace(']', '').trim();
            urls = urlStr.split('|').filter(u => u.trim() !== '');
        }
        if (urls.length === 0) urls = ['imgs/img1.jpg']; 
        return { desc, urls };
    }

    
    function getAmenityIcon(name) {
        const n = name.toLowerCase();
        if (n.includes('wifi') || n.includes('internet')) return 'fa-wifi';
        if (n.includes('pool') || n.includes('swim')) return 'fa-water-ladder';
        if (n.includes('air') || n.includes('ac') || n.includes('condition')) return 'fa-snowflake';
        if (n.includes('park') || n.includes('garage')) return 'fa-square-parking';
        if (n.includes('tv') || n.includes('television')) return 'fa-tv';
        if (n.includes('kitchen') || n.includes('cook')) return 'fa-kitchen-set';
        if (n.includes('gym') || n.includes('fitness')) return 'fa-dumbbell';
        if (n.includes('breakfast') || n.includes('coffee')) return 'fa-mug-saucer';
        return 'fa-check-circle'; 
    }

    
    const loginLink = document.getElementById('login-link');
    const addPlaceLink = document.getElementById('add-place-link');
    const accountLink = document.getElementById('account-link');
    
    if (token) {
        if (loginLink) loginLink.style.display = 'none';
        if (addPlaceLink) addPlaceLink.style.display = 'inline-block';
        if (accountLink) accountLink.style.display = 'inline-block';
    } else {
        if (loginLink) loginLink.style.display = 'inline-block';
        if (addPlaceLink) addPlaceLink.style.display = 'none';
        if (accountLink) accountLink.style.display = 'none';
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
                    document.cookie = `token=${data.access_token}; path=/; max-age=2592000`; 
                    window.location.href = 'index.html'; 
                } else {
                    const errorData = await response.json();
                    alert('Login failed: ' + (errorData.error || response.statusText));
                }
            } catch (error) { console.error('Network Error:', error); alert('Connection to API failed.'); }
        });
    }

    
    window.toggleFavorite = async function(placeId, btnElement) {
        if (!token) {
            window.location.href = 'login.html';
            return;
        }
        try {
            const res = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/favorite`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                const icon = btnElement.querySelector('i');
                if (data.isFavorite) {
                    icon.classList.remove('fa-regular');
                    icon.classList.add('fa-solid');
                    btnElement.style.color = '#e63946'; 
                } else {
                    icon.classList.remove('fa-solid');
                    icon.classList.add('fa-regular');
                    btnElement.style.color = 'var(--text-muted)';
                }
                
                
                if (document.getElementById('my-favorites-list') && document.getElementById('my-favorites-list').style.display === 'grid') {
                    if (typeof window.fetchMyFavorites === 'function') window.fetchMyFavorites();
                }
            }
        } catch (e) { console.error('Error toggling favorite', e); }
    };

    
    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');
    
    if (placesList) {
        let allPlaces = []; 
        let currentUserFavIds = []; 

        async function fetchPlaces() {
            try {
                const headers = {};
                if (token) {
                    headers['Authorization'] = `Bearer ${token}`;
                    
                    try {
                        const favRes = await fetch('http://127.0.0.1:5000/api/v1/users/favorites', { headers });
                        if (favRes.ok) {
                            const favs = await favRes.json();
                            currentUserFavIds = favs.map(f => f.id);
                        }
                    } catch (e) { console.error("Could not load user favorites for index"); }
                }

                const response = await fetch('http://127.0.0.1:5000/api/v1/places/', { headers });
                if (response.ok) {
                    allPlaces = await response.json();
                    displayPlaces(allPlaces, currentUserFavIds);
                }
            } catch (error) { console.error('Error fetching places:', error); }
        }

        function displayPlaces(places, userFavIds = []) {
            placesList.innerHTML = '';
            places.forEach((place) => {
                const { urls } = extractData(place.description);
                let displayImg = urls[0]; 
                
                const isFav = userFavIds.includes(place.id);
                const heartIcon = isFav ? 'fa-solid' : 'fa-regular';
                const heartColor = isFav ? '#e63946' : 'var(--text-muted)';
                
                const card = document.createElement('div');
                card.className = 'place-card';
                card.innerHTML = `
                    <div class="card-img-wrapper" style="position: relative;">
                        <img src="${displayImg}" alt="${place.title.replace(/'/g, "\\'")}">
                        <div class="card-price-badge" style="font-weight: 400;">$${place.price} <span style="font-weight: 400;">/ night</span></div>
                        <button class="btn-favorite" style="color: ${heartColor};" onclick="toggleFavorite('${place.id}', this)">
                            <i class="${heartIcon} fa-heart"></i>
                        </button>
                    </div>
                    <div class="card-info">
                        <h3 style="font-weight: 400;">${place.title}</h3>
                        <a href="place.html?id=${place.id}" class="btn-view" style="font-weight: 400;">Explore <i class="fa-solid fa-arrow-right"></i></a>
                    </div>
                `;
                placesList.appendChild(card);
            });
        }

        if (priceFilter) {
            priceFilter.addEventListener('change', (event) => {
                const maxPrice = event.target.value;
                if (maxPrice === 'All') displayPlaces(allPlaces, currentUserFavIds);
                else displayPlaces(allPlaces.filter(place => place.price <= parseInt(maxPrice)), currentUserFavIds);
            });
        }
        fetchPlaces();
    }

    
    const placeDetailsContainer = document.getElementById('place-details');
    
    if (placeDetailsContainer) {
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');
        const addReviewBtn = document.getElementById('add-review-btn');
        const reviewsList = document.getElementById('reviews-list');
        let currentPlacePrice = 0; 
        let bookedDates = []; 

        if (token && addReviewBtn) {
            addReviewBtn.style.display = 'inline-block';
            addReviewBtn.href = `add_review.html?id=${placeId}`;
        }

        if (placeId) {
            fetchPlaceBookedDates(placeId).then(() => {
                fetchPlaceDetails(placeId);
                fetchPlaceReviews(placeId);
            });
        } else {
            document.getElementById('place-title').innerText = "Place not found.";
        }

        window.openLightbox = function() {
            document.getElementById('lightbox-modal').style.display = 'block';
        };

        async function fetchPlaceBookedDates(id) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${id}/bookings`);
                if (response.ok) bookedDates = await response.json(); 
            } catch (error) { console.error("Could not fetch booked dates."); }
        }

        async function fetchPlaceDetails(id) {
            try {
                
                let isFav = false;
                if (token) {
                    try {
                        const favRes = await fetch('http://127.0.0.1:5000/api/v1/users/favorites', {
                            headers: { 'Authorization': `Bearer ${token}` }
                        });
                        if (favRes.ok) {
                            const favs = await favRes.json();
                            isFav = favs.some(f => f.id === id); 
                        }
                    } catch (e) { console.error("Could not load favorites"); }
                }

                const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${id}`);
                if (response.ok) {
                    const place = await response.json();
                    currentPlacePrice = place.price; 
                    
                    document.getElementById('place-title').innerText = place.title;
                    document.getElementById('booking-price-display').innerText = `$${place.price}`;
                    
                    
                    const favBtn = document.getElementById('place-page-fav-btn');
                    if (favBtn) {
                        favBtn.style.display = 'flex';
                        const heartIcon = isFav ? 'fa-solid' : 'fa-regular';
                        const heartColor = isFav ? '#e63946' : 'var(--text-muted)';
                        favBtn.style.color = heartColor;
                        favBtn.innerHTML = `<i class="${heartIcon} fa-heart"></i>`;
                        
                        
                        favBtn.onclick = () => toggleFavorite(place.id, favBtn);
                    }

                    
                    const { desc, urls } = extractData(place.description);
                    document.getElementById('place-description').innerText = desc;

                    
                    const galleryContainer = document.getElementById('photo-gallery');
                    galleryContainer.innerHTML = '';
                    
                    if (urls.length === 1) {
                        galleryContainer.style.gridTemplateColumns = '1fr';
                        galleryContainer.innerHTML = `<img src="${urls[0]}" class="main-photo" onclick="openLightbox()">`;
                    } else if (urls.length === 2) {
                        galleryContainer.style.gridTemplateColumns = '1fr 1fr';
                        galleryContainer.innerHTML = `
                            <img src="${urls[0]}" class="main-photo" onclick="openLightbox()">
                            <img src="${urls[1]}" class="main-photo" onclick="openLightbox()">
                        `;
                    } else {
                        galleryContainer.innerHTML = `
                            <img src="${urls[0]}" class="main-photo" onclick="openLightbox()">
                            <img src="${urls[1]}" class="side-photo" onclick="openLightbox()">
                            <img src="${urls[2]}" class="side-photo" onclick="openLightbox()">
                        `;
                    }
                    if (urls.length > 3) {
                        galleryContainer.innerHTML += `<button class="show-all-btn" onclick="openLightbox()" style="font-weight: 400;"><i class="fa-solid fa-images"></i> Show all ${urls.length} photos</button>`;
                    }

                    const lightboxContent = document.getElementById('lightbox-content');
                    if (lightboxContent) {
                        lightboxContent.innerHTML = urls.map(u => `<img src="${u}">`).join('');
                    }

                    
                    const amenitiesContainer = document.getElementById('place-amenities');
                    if (amenitiesContainer) {
                        amenitiesContainer.innerHTML = ''; 
                        if (place.amenities && place.amenities.length > 0) {
                            place.amenities.forEach(am => {
                                amenitiesContainer.innerHTML += `
                                    <div style="display: flex; align-items: center; gap: 15px; font-size: 1.1rem; color: var(--text-dark); font-weight: 400;">
                                        <i class="fa-solid ${getAmenityIcon(am.name)}" style="color: var(--text-dark); width: 30px; font-size: 1.3rem; text-align: center;"></i>
                                        <span>${am.name}</span>
                                    </div>
                                `;
                            });
                        } else {
                            amenitiesContainer.innerHTML = '<p style="color: var(--text-muted); font-weight: 400;">No specific amenities listed for this place.</p>';
                        }
                    }

                    
                    if (currentUserId === place.owner_id) {
                        if (addReviewBtn) addReviewBtn.style.display = 'none';
                        const sidebar = document.querySelector('.booking-sidebar');
                        if (sidebar) {
                            sidebar.innerHTML = `
                                <div class="booking-card" style="text-align: center; padding: 40px 20px;">
                                    <h3 style="font-weight: 400;"><i class="fa-solid fa-house-user" style="color: var(--accent-green); margin-right: 8px;"></i> This is your property</h3>
                                    <p style="color: var(--text-muted); margin: 15px 0; font-weight: 400;">You cannot book your own place.</p>
                                    <a href="account.html" class="btn-primary" style="display: block; text-decoration: none; font-weight: 400;">Go to Dashboard</a>
                                </div>
                            `;
                        }
                    }
                    fetchHostDetails(place.owner_id);
                }
            } catch (error) { console.error("Error fetching place:", error); }
        }

        async function fetchHostDetails(ownerId) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/v1/users/${ownerId}`);
                if (response.ok) {
                    const user = await response.json();
                    document.getElementById('place-host').innerText = `Host: ${user.first_name} ${user.last_name}`;
                }
            } catch (error) { console.log("Could not load host details."); }
        }

        async function fetchPlaceReviews(id) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/${id}/reviews`);
                if (response.ok) {
                    const reviews = await response.json();
                    if (reviews.length === 0) {
                        reviewsList.innerHTML = '<p style="color: var(--text-muted); padding: 20px 0; font-weight: 400;">No reviews yet. Be the first to review!</p>';
                        return;
                    }
                    reviewsList.innerHTML = ''; 
                    
                    for (const review of reviews) {
                        let reviewerName = "HBnB Guest";
                        let initials = "HG";
                        try {
                            const userRes = await fetch(`http://127.0.0.1:5000/api/v1/users/${review.user_id}`);
                            if (userRes.ok) {
                                const userData = await userRes.json();
                                reviewerName = `${userData.first_name} ${userData.last_name}`;
                                initials = (userData.first_name[0] + userData.last_name[0]).toUpperCase();
                            }
                        } catch (err) { console.error("Could not fetch user info"); }

                        const isOwner = review.user_id === currentUserId;
                        let actionsHtml = '';
                        if (isOwner) {
                            actionsHtml = `
                                <div style="display: flex; gap: 15px; margin-top: 15px; padding-top: 15px; border-top: 1px solid var(--border-soft);">
                                    <button onclick="openEditReviewModal('${review.id}', ${review.rating}, \`${review.text.replace(/`/g, "\\`")}\`)" style="background: transparent; border: none; color: var(--text-dark); cursor: pointer; font-size: 0.95rem; font-family: var(--font-main); font-weight: 400; transition: 0.2s;" onmouseover="this.style.color='var(--accent-green)'" onmouseout="this.style.color='var(--text-dark)'"><i class="fa-regular fa-pen-to-square"></i> Edit</button>
                                    <button onclick="deleteReview('${review.id}')" style="background: transparent; border: none; color: var(--text-muted); cursor: pointer; font-size: 0.95rem; font-family: var(--font-main); font-weight: 400; transition: 0.2s;" onmouseover="this.style.color='#e63946'" onmouseout="this.style.color='var(--text-muted)'"><i class="fa-regular fa-trash-can"></i> Delete</button>
                                </div>
                            `;
                        }

                        const card = document.createElement('div');
                        card.className = 'review-card';
                        const fullStars = '<i class="fa-solid fa-star"></i>'.repeat(review.rating);
                        const emptyStars = '<i class="fa-regular fa-star"></i>'.repeat(5 - review.rating);
                        
                        card.innerHTML = `
                            <div class="review-header">
                                <div class="reviewer-avatar">${initials}</div>
                                <div class="reviewer-info">
                                    <h4 style="font-weight: 400;">${reviewerName}</h4>
                                    <div class="rating">${fullStars}${emptyStars}</div>
                                </div>
                            </div>
                            <p class="review-text" style="font-weight: 400;">"${review.text}"</p>
                            ${actionsHtml}
                        `;
                        reviewsList.appendChild(card);
                    }
                }
            } catch (error) { console.error("Error fetching reviews:", error); }
        }

        const reviewModal = document.getElementById('edit-review-modal');
        if (reviewModal) {
            window.openEditReviewModal = (id, rating, text) => {
                document.getElementById('edit-review-id').value = id;
                document.getElementById('edit-review-rating').value = rating;
                document.getElementById('edit-review-text').value = text;
                reviewModal.style.display = 'flex';
            };

            document.getElementById('edit-review-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const id = document.getElementById('edit-review-id').value;
                try {
                    const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/${id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                        body: JSON.stringify({
                            rating: parseInt(document.getElementById('edit-review-rating').value),
                            text: document.getElementById('edit-review-text').value
                        })
                    });
                    if (response.ok) {
                        reviewModal.style.display = 'none';
                        fetchPlaceReviews(placeId); 
                    } else { alert("Failed to update review."); }
                } catch (error) { alert("Connection error."); }
            });

            window.deleteReview = async (id) => {
                if (!confirm("Are you sure you want to delete this review?")) return;
                try {
                    const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/${id}`, {
                        method: 'DELETE',
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (response.ok) fetchPlaceReviews(placeId);
                    else alert("Failed to delete review.");
                } catch (error) { alert("Connection error."); }
            };
        }

        const checkinInput = document.getElementById('checkin-date');
        const checkoutInput = document.getElementById('checkout-date');
        const breakdownDiv = document.getElementById('price-breakdown');
        
        if (checkinInput && checkoutInput) {
            let checkinDate = null;
            let checkoutDate = null;

            function calculateTotal() {
                if (checkinDate && checkoutDate && currentPlacePrice > 0) {
                    const diffTime = Math.abs(checkoutDate - checkinDate);
                    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
                    if (diffDays > 0) {
                        document.getElementById('calc-nights').innerText = `$${currentPlacePrice} x ${diffDays} nights`;
                        document.getElementById('calc-total').innerText = `$${currentPlacePrice * diffDays}`;
                        document.getElementById('final-total').innerText = `$${currentPlacePrice * diffDays}`;
                        breakdownDiv.style.display = 'block';
                    }
                }
            }

            const fpCheckout = flatpickr(checkoutInput, {
                minDate: "today",
                disable: bookedDates, 
                onChange: function(selectedDates) {
                    checkoutDate = selectedDates[0];
                    calculateTotal();
                }
            });

            flatpickr(checkinInput, {
                minDate: "today",
                disable: bookedDates, 
                onChange: function(selectedDates) {
                    checkinDate = selectedDates[0];
                    fpCheckout.set('minDate', checkinDate.fp_incr(1));
                    calculateTotal();
                }
            });

            const bookingForm = document.getElementById('booking-form');
            if (bookingForm) {
                bookingForm.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    if (!token) {
                        alert("Please login to make a reservation.");
                        window.location.href = 'login.html';
                        return;
                    }
                    if (!checkinDate || !checkoutDate) {
                        alert("Please select check-in and check-out dates.");
                        return;
                    }
                    const diffDays = Math.ceil(Math.abs(checkoutDate - checkinDate) / (1000 * 60 * 60 * 24));
                    const payload = {
                        place_id: placeId,
                        start_date: checkinInput.value,
                        end_date: checkoutInput.value,
                        total_price: currentPlacePrice * diffDays
                    };

                    try {
                        const response = await fetch('http://127.0.0.1:5000/api/v1/bookings/', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                            body: JSON.stringify(payload)
                        });
                        if (response.ok) {
                            alert('Booking confirmed successfully!');
                            window.location.href = 'account.html';
                        } else { 
                            const errorData = await response.json();
                            alert('Failed to create booking: ' + (errorData.error || response.statusText)); 
                        }
                    } catch (error) { console.error(error); }
                });
            }
        }
    }

    
    const addPlaceForm = document.getElementById('add-place-form');
    if (addPlaceForm) {
        if (!token) window.location.href = 'login.html';

        const addImgBtn = document.getElementById('add-more-imgs-btn');
        const imgContainer = document.getElementById('image-inputs-container');
        if (addImgBtn && imgContainer) {
            addImgBtn.addEventListener('click', () => {
                const newDiv = document.createElement('div');
                newDiv.className = 'input-group';
                newDiv.style.marginTop = '10px';
                newDiv.innerHTML = `<input type="url" class="place-image-url" placeholder="https://example.com/img.jpg">`;
                imgContainer.appendChild(newDiv);
            });
        }

        const amenitiesSelectionWrapper = document.getElementById('amenities-selection-wrapper');
        const amenitiesListManage = document.getElementById('amenities-list-manage');
        
        async function fetchAndRenderAmenities() {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/amenities/');
                if (response.ok) {
                    const amenities = await response.json();
                    
                    if (amenitiesSelectionWrapper) {
                        amenitiesSelectionWrapper.innerHTML = amenities.map(am => `
                            <label>
                                <input type="checkbox" class="amenity-checkbox" value="${am.id}">
                                <span class="amenity-pill"><i class="fa-solid ${getAmenityIcon(am.name)}" style="margin-right: 5px;"></i> <span style="font-weight: 400;">${am.name}</span></span>
                            </label>
                        `).join('');
                    }

                    if (amenitiesListManage) {
                        amenitiesListManage.innerHTML = amenities.map(am => `
                            <div class="amenity-list-item">
                                <div>
                                    <h4 style="font-weight: 400;"><i class="fa-solid ${getAmenityIcon(am.name)}" style="color: var(--accent-green); margin-right: 5px;"></i> ${am.name}</h4>
                                    <p style="font-weight: 400;">${am.description || "No description"}</p>
                                </div>
                                <div style="flex: 0; display: flex; gap: 10px;">
                                    <button class="btn-icon edit" onclick="editAmenity('${am.id}', '${am.name.replace(/'/g, "\\'")}', '${(am.description||"").replace(/'/g, "\\'")}')"><i class="fa-solid fa-pen"></i></button>
                                    <button class="btn-icon delete" onclick="deleteAmenity('${am.id}')"><i class="fa-solid fa-trash"></i></button>
                                </div>
                            </div>
                        `).join('');
                    }
                }
            } catch (err) { console.error("Error fetching amenities:", err); }
        }

        fetchAndRenderAmenities();

        const amModal = document.getElementById('amenities-modal');
        window.openAmenitiesModal = () => { amModal.style.display = 'flex'; };
        window.closeAmenitiesModal = () => { 
            amModal.style.display = 'none'; 
            document.getElementById('manage-amenity-form').reset();
            document.getElementById('amenity-id-input').value = '';
        };

        window.deleteAmenity = async (id) => {
            if (!confirm("Delete this amenity globally?")) return;
            try {
                const res = await fetch(`http://127.0.0.1:5000/api/v1/amenities/${id}`, {
                    method: 'DELETE',
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (res.ok) fetchAndRenderAmenities();
                else alert("Failed to delete.");
            } catch (e) { alert("Error connecting to API."); }
        };

        window.editAmenity = (id, name, desc) => {
            document.getElementById('amenity-id-input').value = id;
            document.getElementById('amenity-name-input').value = name;
            document.getElementById('amenity-desc-input').value = desc;
        };

        document.getElementById('manage-amenity-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const id = document.getElementById('amenity-id-input').value;
            const payload = {
                name: document.getElementById('amenity-name-input').value,
                description: document.getElementById('amenity-desc-input').value
            };

            const method = id ? 'PUT' : 'POST';
            const url = id ? `http://127.0.0.1:5000/api/v1/amenities/${id}` : `http://127.0.0.1:5000/api/v1/amenities/`;

            try {
                const res = await fetch(url, {
                    method: method,
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify(payload)
                });
                if (res.ok) {
                    fetchAndRenderAmenities();
                    document.getElementById('manage-amenity-form').reset();
                    document.getElementById('amenity-id-input').value = '';
                } else { alert("Failed to save amenity."); }
            } catch (e) { alert("Error connecting to API."); }
        });

        addPlaceForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const title = document.getElementById('place-title').value;
            const rawDescription = document.getElementById('place-description').value;
            const price = parseFloat(document.getElementById('place-price').value);
            const latitude = parseFloat(document.getElementById('place-lat').value);
            const longitude = parseFloat(document.getElementById('place-lng').value);

            const urlInputs = document.querySelectorAll('.place-image-url');
            const urls = Array.from(urlInputs).map(i => i.value.trim()).filter(v => v !== "");
            let finalDescription = rawDescription;
            if (urls.length > 0) {
                finalDescription += ` [IMG:${urls.join('|')}]`;
            }

            const checkedAmenities = Array.from(document.querySelectorAll('.amenity-checkbox:checked')).map(cb => cb.value);

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify({
                        title: title, description: finalDescription,
                        price: price, latitude: latitude, longitude: longitude,
                        owner_id: "auto-filled",
                        amenities: checkedAmenities 
                    })
                });

                if (response.ok) {
                    const newPlace = await response.json();
                    alert('Place added successfully!');
                    window.location.href = `place.html?id=${newPlace.id}`; 
                } else {
                    const errorData = await response.json();
                    alert('Failed to add place: ' + (errorData.error || response.statusText));
                }
            } catch (error) { alert('Connection to API failed.'); }
        });
    }

    
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        if (!token) window.location.href = 'index.html';
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');
        if (!placeId) window.location.href = 'index.html';

        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const rating = document.getElementById('review-rating').value;
            const text = document.getElementById('review-text').value;

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify({
                        text: text,
                        rating: parseInt(rating),
                        place_id: placeId,
                        user_id: "auto-filled"
                    })
                });

                if (response.ok) {
                    alert('Review submitted successfully!');
                    window.location.href = `place.html?id=${placeId}`; 
                } else {
                    const errorData = await response.json();
                    alert('Failed to submit review: ' + (errorData.error || response.statusText));
                }
            } catch (error) { alert('Connection to API failed.'); }
        });
    }

    
    const accountDashboardWrapper = document.querySelector('.dashboard-wrapper');
    if (accountDashboardWrapper) {
        if (!token) window.location.href = 'login.html';

        const myPlacesList = document.getElementById('my-places-list');
        const myBookingsList = document.getElementById('my-bookings-list');
        const myFavoritesList = document.getElementById('my-favorites-list');
        const tabPlaces = document.getElementById('tab-places');
        const tabBookings = document.getElementById('tab-bookings');
        const tabFavorites = document.getElementById('tab-favorites');

        document.getElementById('logout-btn').addEventListener('click', (e) => {
            e.preventDefault();
            document.cookie = 'token=; Max-Age=0; path=/';
            window.location.href = 'index.html';
        });

        
        async function fetchMyPlaces() {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (response.ok) {
                    const allPlaces = await response.json();
                    const myPlaces = allPlaces.filter(p => p.owner_id === currentUserId);
                    renderMyPlaces(myPlaces);
                }
            } catch (error) { console.error('Error fetching places:', error); }
        }

        function renderMyPlaces(places) {
            if(!myPlacesList) return;
            myPlacesList.innerHTML = '';
            if (places.length === 0) {
                myPlacesList.innerHTML = '<p style="font-weight: 400;">You have not hosted any places yet.</p>';
                return;
            }

            places.forEach((place) => {
                const { urls } = extractData(place.description);
                let displayImg = urls[0];

                const card = document.createElement('div');
                card.className = 'place-card';
                card.innerHTML = `
                    <img src="${displayImg}" alt="${place.title.replace(/'/g, "\\'")}" class="card-img">
                    <div class="card-body">
                        <h3 style="font-weight: 400;">${place.title}</h3>
                        <p style="font-weight: 400;">$${place.price} / night</p>
                        <div class="card-actions">
                            <button class="btn-edit" style="font-weight: 400;" onclick="openModal('${place.id}')"><i class="fa-solid fa-pen"></i> Edit</button>
                            <button class="btn-delete" style="font-weight: 400;" onclick="deletePlace('${place.id}')"><i class="fa-solid fa-trash"></i> Delete</button>
                        </div>
                    </div>
                `;
                myPlacesList.appendChild(card);
            });
        }

        async function fetchMyBookings() {
            if(!myBookingsList) return;
            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/bookings/', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (response.ok) {
                    const bookings = await response.json();
                    myBookingsList.innerHTML = bookings.length ? '' : '<p style="font-weight: 400;">No booking history found.</p>';

                    for (const booking of bookings) {
                        const placeRes = await fetch(`http://127.0.0.1:5000/api/v1/places/${booking.place_id}`);
                        const placeData = placeRes.ok ? await placeRes.json() : { title: "Unknown Place" };

                        myBookingsList.innerHTML += `
                            <div class="place-card" style="padding: 20px;">
                                <h3 style="font-weight: 400;"><i class="fa-solid fa-location-dot" style="color: var(--accent-green); margin-right: 5px;"></i> ${placeData.title}</h3>
                                <p style="color: var(--text-muted); margin: 10px 0; font-weight: 400;">
                                    <i class="fa-solid fa-calendar-days" style="margin-right: 5px;"></i> ${booking.start_date} to ${booking.end_date}
                                </p>
                                <strong style="color: var(--accent-green); font-size: 1.2rem; font-weight: 400;">Total: $${booking.total_price}</strong>
                            </div>
                        `;
                    }
                }
            } catch (err) { console.error('Error fetching bookings', err); }
        }

        window.fetchMyFavorites = async function() {
            if(!myFavoritesList) return;
            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/users/favorites', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (response.ok) {
                    const favorites = await response.json();
                    myFavoritesList.innerHTML = '';
                    if (favorites.length === 0) {
                        myFavoritesList.innerHTML = '<p style="font-weight: 400;">You have no favorite places yet.</p>';
                        return;
                    }
                    
                    favorites.forEach((place) => {
                        const { urls } = extractData(place.description);
                        let displayImg = urls[0];
                        const card = document.createElement('div');
                        card.className = 'place-card';
                        card.innerHTML = `
                            <div class="card-img-wrapper" style="position: relative;">
                                <img src="${displayImg}" alt="${place.title.replace(/'/g, "\\'")}">
                                <button class="btn-favorite" style="color: #e63946;" onclick="toggleFavorite('${place.id}', this)">
                                    <i class="fa-solid fa-heart"></i>
                                </button>
                            </div>
                            <div class="card-info">
                                <h3 style="font-weight: 400;">${place.title}</h3>
                                <a href="place.html?id=${place.id}" class="btn-view" style="font-weight: 400;">Explore <i class="fa-solid fa-arrow-right"></i></a>
                            </div>
                        `;
                        myFavoritesList.appendChild(card);
                    });
                }
            } catch (error) { console.error('Error fetching favorites:', error); }
        }

        
        function switchTab(activeTabId, showSectionId, titleId) {
            ['tab-places', 'tab-bookings', 'tab-favorites'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.classList.remove('active');
            });
            const activeTab = document.getElementById(activeTabId);
            if(activeTab) activeTab.classList.add('active');

            ['my-places-list', 'my-bookings-list', 'my-favorites-list'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.style.display = 'none';
            });
            const showSection = document.getElementById(showSectionId);
            if(showSection) showSection.style.display = 'grid';

            const pTitle = document.querySelector('.main-content .section-title:not(#bookings-title):not(#favorites-title)');
            const bTitle = document.getElementById('bookings-title');
            const fTitle = document.getElementById('favorites-title');
            
            if (pTitle) pTitle.style.display = 'none';
            if (bTitle) bTitle.style.display = 'none';
            if (fTitle) fTitle.style.display = 'none';
            
            if (titleId === 'places-title' && pTitle) pTitle.style.display = 'block';
            else if (document.getElementById(titleId)) document.getElementById(titleId).style.display = 'block';
        }

        if (tabPlaces) {
            tabPlaces.addEventListener('click', (e) => {
                e.preventDefault();
                switchTab('tab-places', 'my-places-list', 'places-title');
                
                fetchMyPlaces();
            });
        }
        if (tabBookings) {
            tabBookings.addEventListener('click', (e) => {
                e.preventDefault();
                switchTab('tab-bookings', 'my-bookings-list', 'bookings-title');
                fetchMyBookings();
            });
        }
        if (tabFavorites) {
            tabFavorites.addEventListener('click', (e) => {
                e.preventDefault();
                switchTab('tab-favorites', 'my-favorites-list', 'favorites-title');
                fetchMyFavorites();
            });
        }

        
        const modal = document.getElementById('edit-modal');
        if (modal) {
            const editAddImgBtn = document.getElementById('edit-add-more-imgs-btn');
            if (editAddImgBtn) {
                editAddImgBtn.addEventListener('click', () => {
                    const imgContainer = document.getElementById('edit-image-inputs-container');
                    const div = document.createElement('div');
                    div.className = 'input-group';
                    div.style.marginTop = '10px';
                    div.innerHTML = `<input type="url" class="edit-place-image-url" placeholder="https://example.com/img.jpg" required>`;
                    imgContainer.appendChild(div);
                });
            }

            window.openModal = async function(placeId) {
                try {
                    const res = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`);
                    if (!res.ok) throw new Error("Place not found");
                    const place = await res.json();

                    document.getElementById('edit-place-id').value = place.id;
                    document.getElementById('edit-title').value = place.title;
                    document.getElementById('edit-price').value = place.price;

                    const { desc, urls } = extractData(place.description);
                    document.getElementById('edit-description').value = desc;

                    const imgContainer = document.getElementById('edit-image-inputs-container');
                    imgContainer.innerHTML = '<label style="font-weight: 400;">Place Images</label>'; 
                    urls.forEach(url => {
                        const div = document.createElement('div');
                        div.className = 'input-group';
                        div.style.marginTop = '10px';
                        div.innerHTML = `<input type="url" class="edit-place-image-url" value="${url}" required>`;
                        imgContainer.appendChild(div);
                    });

                    const amRes = await fetch('http://127.0.0.1:5000/api/v1/amenities/');
                    if (amRes.ok) {
                        const allAmenities = await amRes.json();
                        const placeAmenityIds = (place.amenities || []).map(a => a.id);
                        
                        const amContainer = document.getElementById('edit-amenities-selection-wrapper');
                        amContainer.innerHTML = allAmenities.map(am => `
                            <label>
                                <input type="checkbox" class="edit-amenity-checkbox" value="${am.id}" ${placeAmenityIds.includes(am.id) ? 'checked' : ''}>
                                <span class="amenity-pill" style="font-weight: 400;"><i class="fa-solid ${getAmenityIcon(am.name)}" style="margin-right: 5px;"></i> ${am.name}</span>
                            </label>
                        `).join('');
                    }
                    modal.style.display = 'flex';
                } catch (e) { alert("Could not load place details for editing."); }
            };

            document.getElementById('close-modal-btn').addEventListener('click', () => modal.style.display = 'none');

            document.getElementById('edit-place-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const id = document.getElementById('edit-place-id').value;
                const rawDesc = document.getElementById('edit-description').value;
                
                const urlInputs = document.querySelectorAll('.edit-place-image-url');
                const urls = Array.from(urlInputs).map(i => i.value.trim()).filter(v => v !== "");
                
                let finalDesc = rawDesc;
                if (urls.length > 0) finalDesc += ` [IMG:${urls.join('|')}]`;

                const checkedAmenities = Array.from(document.querySelectorAll('.edit-amenity-checkbox:checked')).map(cb => cb.value);

                const payload = {
                    title: document.getElementById('edit-title').value,
                    description: finalDesc,
                    price: parseFloat(document.getElementById('edit-price').value),
                    amenities: checkedAmenities
                };

                try {
                    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                        body: JSON.stringify(payload)
                    });

                    if (response.ok) {
                        modal.style.display = 'none';
                        fetchMyPlaces(); 
                    } else { alert('Failed to update. Session may have expired, please log in again.'); }
                } catch (error) { alert('Connection error.'); }
            });
        }

        window.deletePlace = async function(placeId) {
            if (!confirm("Are you sure you want to delete this place?")) return;
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
                    method: 'DELETE',
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (response.ok) fetchMyPlaces();
                else alert('Failed to delete place.');
            } catch (error) { alert('Connection error.'); }
        };

        const deleteAccountBtn = document.getElementById('delete-account-btn');
        if (deleteAccountBtn) {
            deleteAccountBtn.addEventListener('click', async () => {
                if (!confirm("WARNING: This will permanently delete your account. Proceed?")) return;
                try {
                    const response = await fetch(`http://127.0.0.1:5000/api/v1/users/${currentUserId}`, {
                        method: 'DELETE',
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (response.ok) {
                        document.cookie = 'token=; Max-Age=0; path=/';
                        window.location.href = 'register.html';
                    } else { alert('Failed to delete account.'); }
                } catch (error) { alert('Connection error.'); }
            });
        }

        
        fetchMyPlaces();
    }
});