 var swiper = new Swiper(".mySwiper-1",{
        slidesPerView:1,
        spaceBetween:30,
        loop:true,
        pagination:{
            el:".swiper-pagination",
            clickable:true,

        },
        navigation: {
            nextEl:".swiper-button-next",
            prevEl:".swiper-button-prev",
        }
    });
    
     var swiper = new Swiper(".mySwiper-2",{
        slidesPerView:3,
        spaceBetween:20,
        loop:true,
        loopFillGroupWithBlank:true,
        navigation: {
            nextEl:".swiper-button-next",
            prevEl:".swiper-button-prev",
        },
        breakpoints:{
            0: {
                slidesPerView:1,

            },
            520:{
                slidesPerView:2,

            },
            950:{
                slidesPerView:3,
            }
        }

    });
    let tabInputs = document.querySelectorAll(".tabInput");
    tabInputs.forEach(function(input){
        input.addEventListener('change',function(){
            let id=input.value;
            let thisSwiper = document.getElementById('swiper'+ id);
            thisSwiper.swiper.update(); 

        })
    }
    )

    /*carrito de compras*/

   let cart = [];
let total = 0;

function updateCart() {
    let cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = ""; 

    cart.forEach((item, index) => {
        let li = document.createElement('li');
        li.textContent = `${item.name} - $${item.price} `;

        // botón eliminar
        let removeBtn = document.createElement('button');
        removeBtn.textContent = "x";
        removeBtn.style.marginLeft = "10px";
        removeBtn.addEventListener('click', () => {
            total -= item.price;
            cart.splice(index, 1);
            updateCart();
        });

        li.appendChild(removeBtn);
        cartItems.appendChild(li);
    });

    document.getElementById('cart-total').textContent = total;
}

document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', () => {
        let name = button.getAttribute('data-name');
        let price = parseFloat(button.getAttribute('data-price'));

        cart.push({ name, price });
        total += price;

        updateCart();
    });
});

/*compra via whatsap*/
document.getElementById("checkout").addEventListener("click", async () => {
    if (cart.length === 0) {
        alert("Tu carrito está vacío.");
        return;
    }

    try {
        // Guardar orden en la base de datos
        const orderData = {
            items: cart,
            total: total,
            phone: "573028611023",
            name: "Cliente desde web"
        };

        const response = await fetch('/save_order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData)
        });

        const result = await response.json();
        
        if (result.success) {
            console.log('Orden guardada con ID:', result.order_id);
        } else {
            console.warn('Error al guardar orden:', result.error);
        }
    } catch (error) {
        console.warn('Error de conexión al guardar orden:', error);
    }

    // Crear el mensaje con los productos
    let message = "¡Hola! Quiero hacer este pedido:\n\n";
    cart.forEach(item => {
        message += `- ${item.name}: $${item.price}\n`;
    });
    message += `\nTotal: $${total}`;

    // Codificar el mensaje para URL
    let encodedMessage = encodeURIComponent(message);

    // Número de WhatsApp (ejemplo Colombia)
    let phoneNumber = "573028611023";

    // Redirigir a WhatsApp
    window.open(`https://wa.me/${phoneNumber}?text=${encodedMessage}`, "_blank");
    
    // Limpiar carrito después del checkout
    cart = [];
    total = 0;
    updateCart();
});
