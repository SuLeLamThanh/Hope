function addToCart(id, name, price) {
    fetch('/cart', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    }).catch(err => console.error(err))
}

function updateCart(productId, obj) {
    fetch(`/cart/${productId}`, {
        method: 'put',
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let d2 = document.getElementsByClassName("cart-amount")
        for (let i = 0; i < d2.length; i++)
            d2[i].innerText = data.total_amount.toLocaleString("en-US")
    }).catch(err => console.error(err))
}

function deleteCart(productId) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch(`/cart/${productId}`, {
            method: 'delete'
        }).then(res => res.json()).then(data => {
            let d = document.getElementsByClassName("cart-counter")
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity

            let d2 = document.getElementsByClassName("cart-amount")
            for (let i = 0; i < d2.length; i++)
                d2[i].innerText = data.total_amount.toLocaleString("en-US")

            let r = document.getElementById(`cart${productId}`)
            r.style.display = "none"
        }).catch(err => console.error(err))
    }
}
function pay() {
    if (confirm('Bạn chắc chắn thanh toán?') == true) {
        fetch("/pay").then(res => res.json).then(data => location.reload()).catch(err => console.info(err))
    }

}

function pay1() {
    if (confirm('Bạn có chắc chắn thanh toán online không?') == true) {
        fetch('/api/pay1', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.code === 200)
                redirect('{{url_for("get_info"}}')
        })
    }
}

function addComment(productId) {
    let content = document.getElementById('commentId')
    if (content !== null) {
        fetch('/api/comments', {
            method: 'post',
            body: JSON.stringify({
                'product_id': productId,
                'content': content.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data =>{
            if (data.status == 201) {
                let c = data.comment

                let area = document.getElementById('commentArea')

                area.innerHTML = `
                     <div class="row comment">
                         <div class="col-md-1 col-xs-4">
                            <img src="${c.user.avatar}"
                            class=" img-fluid rounded-circle" alt="demo" />
                        </div>
                        <div class="col-md-11 col-xs-8">
                            <p>${c.content}</p>
                            <p><em>${moment(c.created_date).locale('vi').fromNow()}</em></p>
                        </div>
                    </div>
                `+area.innerHTML
            } else if (data.status == 404)
                alert(data.err_msg)
        })
    }
}