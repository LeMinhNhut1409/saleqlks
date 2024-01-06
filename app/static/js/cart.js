function addToCart(id, name, price) {
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        let c = document.getElementsByClassName('cart-counter');
        for (let d of c)
            d.innerText = data.total_quantity
    })
}

function updateCart(id, obj) {
    obj.disabled = true;
    fetch(`/api/cart/${id}`, {
        method: 'put',
        body: JSON.stringify({
            'quantity': obj.value
        }),  headers: {
            'Content-Type': "application/json"
        }
    }).then(res => res.json()).then(data => {
        obj.disabled = false;
        let c = document.getElementsByClassName('cart-counter');
        for (let d of c)
            d.innerText = data.total_quantity
    });
}

function deleteCart(id, obj) {
    if (confirm("Ban chac chan xoa khong?") === true) {
        obj.disabled = true;
        fetch(`/api/cart/${id}`, {
            method: 'delete'
        }).then(res => res.json()).then(data => {
            obj.disabled = false;
            let c = document.getElementsByClassName('cart-counter');
            for (let d of c)
                d.innerText = data.total_quantity

            let r = document.getElementById(`product${id}`);
            r.style.display = "none";
        });
    }
}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán!") === true) {
        fetch("/api/pay", {
            method: "post"
        }).then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload();
            else
                alert(data.err_msg);
        })
    }
}