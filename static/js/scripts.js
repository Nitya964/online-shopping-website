console.log("navbar loaded successfully");
console.log("App loaded successfully");


// ==================== CSRF TOKEN SETUP ====================
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


const csrftoken = getCookie('csrftoken');


// ==================== HELPER FUNCTIONS ====================


// Show Toast Notification
function showToast(icon, title) {
  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer);
      toast.addEventListener('mouseleave', Swal.resumeTimer);
    }
  });


  Toast.fire({
    icon: icon,
    title: title
  });
}


// Show SweetAlert Modal
function showAlert(icon, title, text) {
  return Swal.fire({
    icon: icon,
    title: title,
    text: text,
    confirmButtonColor: icon === 'error' ? '#d33' : '#151315'
  });
}


// Update navbar count
function updateNavbarCount(type, count) {
  const links = document.querySelectorAll(`a[href*="${type}"]`);
  links.forEach(link => {
    link.textContent = type === 'cart' ? ` Cart (${count})` : `Wishlist (${count})`;
  });
}


// ==================== ADD TO CART AJAX ====================
document.addEventListener('click', function (e) {
  if (e.target.classList.contains('add-to-cart-btn')) {
    e.preventDefault();


    const productId = e.target.dataset.productId;
    const btn = e.target;


    // Show loading state
    btn.disabled = true;
    btn.textContent = 'Adding...';


    fetch(`/add-to-cart-ajax/${productId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          showToast('success', data.message || 'Added to Cart successfully!');
          if (data.cart_count !== undefined) {
            updateNavbarCount('cart', data.cart_count);
          }
        } else if (data.status === 'error') {
          showAlert('error', 'Error', data.message || 'Something went wrong!');
        }
      })
      .catch(error => {
        showAlert('error', 'Error', 'Something went wrong! Please try again.');
      })
      .finally(() => {
        btn.disabled = false;
        btn.textContent = 'Add to Cart';
      });
  }
});


// ==================== ADD TO WISHLIST AJAX (SweetAlert Modal) ====================
document.addEventListener('click', function (e) {
  if (e.target.classList.contains('add-to-wishlist-btn')) {
    e.preventDefault();


    const productId = e.target.dataset.productId;
    const btn = e.target;


    // Show loading state
    btn.disabled = true;
    btn.textContent = 'Adding...';


    fetch(`/add-to-wishlist-ajax/${productId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          // Show SweetAlert Modal for Wishlist
          Swal.fire({
            icon: 'success',
            title: 'Added to Wishlist!',
            text: data.message || 'Product has been added to your wishlist.',
            confirmButtonColor: '#e74c3c',
            timer: 2000,
            timerProgressBar: true
          });
          if (data.wishlist_count !== undefined) {
            updateNavbarCount('wishlist', data.wishlist_count);
          }
        } else if (data.status === 'error') {
          showAlert('error', 'Error', data.message || 'Something went wrong!');
        }
      })
      .catch(error => {
        showAlert('error', 'Error', 'Something went wrong! Please try again.');
      })
      .finally(() => {
        btn.disabled = false;
        btn.textContent = 'Add to Wishlist';
      });
  }
});


// ==================== REMOVE FROM CART AJAX ====================
document.addEventListener('click', function (e) {
  if (e.target.classList.contains('remove-from-cart-btn')) {
    e.preventDefault();


    const cartId = e.target.dataset.cartId;
    const row = e.target.closest('.cart-item');


    // Show SweetAlert Confirmation
    Swal.fire({
      title: 'Are you sure?',
      text: "You want to remove this item from cart?",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Yes, remove it!'
    }).then((result) => {
      if (result.isConfirmed) {
        fetch(`/remove-from-cart-ajax/${cartId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
          }
        })
          .then(response => response.json())
          .then(data => {
            if (data.status === 'success') {
              showToast('success', 'Item removed from cart!');


              // Remove the row with animation
              row.style.opacity = '0';
              row.style.transition = 'opacity 0.3s';
              setTimeout(() => row.remove(), 300);


              // Update cart count in navbar
              if (data.cart_count !== undefined) {
                updateNavbarCount('cart', data.cart_count);
              }


              // Update total
              if (data.total !== undefined) {
                const totalElement = document.querySelector('.cart-total-amount');
                if (totalElement) {
                  totalElement.textContent = 'Cart Total: $' + data.total;
                }
              }
            }
          })
          .catch(error => {
            showAlert('error', 'Error', 'Something went wrong!');
          });
      }
    });
  }
});


// ==================== REMOVE FROM WISHLIST AJAX (SweetAlert Modal) ====================
document.addEventListener('click', function (e) {
  if (e.target.classList.contains('remove-from-wishlist-btn')) {
    e.preventDefault();


    const wishlistId = e.target.dataset.wishlistId;
    const row = e.target.closest('.wishlist-item');


    // Show SweetAlert Confirmation
    Swal.fire({
      title: 'Are you sure?',
      text: "You want to remove this item from wishlist?",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#e74c3c',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Yes, remove it!'
    }).then((result) => {
      if (result.isConfirmed) {
        fetch(`/remove-from-wishlist-ajax/${wishlistId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
          }
        })
          .then(response => response.json())
          .then(data => {
            if (data.status === 'success') {
              // Show SweetAlert Success Modal for Wishlist
              Swal.fire({
                icon: 'success',
                title: 'Removed!',
                text: 'Item removed from wishlist!',
                confirmButtonColor: '#e74c3c',
                timer: 1500,
                timerProgressBar: true
              });


              // Remove the row with animation
              row.style.opacity = '0';
              row.style.transition = 'opacity 0.3s';
              setTimeout(() => row.remove(), 300);


              // Update wishlist count in navbar
              if (data.wishlist_count !== undefined) {
                updateNavbarCount('wishlist', data.wishlist_count);
              }
            }
          })
          .catch(error => {
            showAlert('error', 'Error', 'Something went wrong!');
          });
      }
    });
  }
});


// ==================== QUANTITY PLUS/MINUS BUTTONS ====================
document.addEventListener('click', function (e) {
  if (e.target.classList.contains('qty-btn-plus')) {
    const input = e.target.parentElement.querySelector('.cart-quantity-input');
    const currentValue = parseInt(input.value) || 1;
    input.value = currentValue + 1;
    // Dispatch change event with bubbles: true
    const changeEvent = new Event('change', { bubbles: true });
    input.dispatchEvent(changeEvent);
  }


  if (e.target.classList.contains('qty-btn-minus')) {
    const input = e.target.parentElement.querySelector('.cart-quantity-input');
    const currentValue = parseInt(input.value) || 1;
    if (currentValue > 1) {
      input.value = currentValue - 1;
      // Dispatch change event with bubbles: true
      const changeEvent = new Event('change', { bubbles: true });
      input.dispatchEvent(changeEvent);
    }
  }
});


// ==================== UPDATE CART QUANTITY AJAX ====================
document.addEventListener('change', function (e) {
  if (e.target.classList.contains('cart-quantity-input')) {
    const cartId = e.target.dataset.cartId;
    const quantity = parseInt(e.target.value);
    const cartItem = e.target.closest('.cart-item');
    const priceElement = cartItem.querySelector('.item-total-price');
    const minusBtn = cartItem.querySelector('.qty-btn-minus');


    console.log('Change event triggered:', { cartId, quantity, cartItem, priceElement });


    // Validate quantity
    if (isNaN(quantity) || quantity < 1) {
      showAlert('error', 'Error', 'Quantity must be at least 1');
      e.target.value = 1; // Reset to 1
      return;
    }


    const formData = new FormData();
    formData.append('quantity', quantity);


    console.log('Sending AJAX request:', { cartId, quantity });


    fetch(`/update-cart-quantity-ajax/${cartId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken
      },
      body: formData
    })
      .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Response data:', data);
        if (data.status === 'success') {
          showToast('success', 'Quantity updated!');


          // Update item total price
          if (data.item_total !== undefined) {
            if (priceElement) {
              console.log('Updating item total:', data.item_total);
              priceElement.textContent = data.item_total;
            } else {
              console.error('Item total price element not found!');
            }
          }


          // Update cart total
          if (data.total !== undefined) {
            const totalElement = document.querySelector('.cart-total-amount');
            if (totalElement) {
              console.log('Updating cart total:', data.total);
              totalElement.textContent = 'Cart Total: $' + data.total;
            } else {
              console.error('Cart total element not found!');
            }
          }


          // Update minus button state
          if (minusBtn) {
            minusBtn.disabled = quantity <= 1;
          }
        } else {
          showAlert('error', 'Error', data.message || 'Failed to update quantity!');
        }
      })
      .catch(error => {
        console.error('Error updating quantity:', error);
        showAlert('error', 'Error', 'Failed to update quantity! Please try again.');
      });
  }
});
