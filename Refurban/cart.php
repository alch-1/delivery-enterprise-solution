<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Refurban - Cart</title>

    <link rel="icon" href="img/Fevicon.png" type="image/png">
    <link rel="stylesheet" href="vendors/fontawesome/css/all.min.css">
    <link rel="stylesheet" href="vendors/themify-icons/themify-icons.css">
    <link rel="stylesheet" href="vendors/linericon/style.css">
    <link rel="stylesheet" href="vendors/owl-carousel/owl.theme.default.min.css">
    <link rel="stylesheet" href="vendors/owl-carousel/owl.carousel.min.css">
    <link rel="stylesheet" href="vendors/nice-select/nice-select.css">
    <link rel="stylesheet" href="vendors/nouislider/nouislider.min.css">

    <link rel="stylesheet" href="css/style.css">
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet"
    href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css"
    integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" 
    crossorigin="anonymous">

    

  
</head>
<body>
    <!--================ Start Header Menu Area =================-->
    <?php include "./header.html" ?>
    <!--================ End Header Menu Area =================-->

    <!-- ================ start banner area ================= -->	
    <!-- <section class="blog-banner-area" id="category">
        <div class="container h-100">
            <div class="blog-banner">
                <div class="text-center">
                    <h1>Shopping Cart</h1>
                    <nav aria-label="breadcrumb" class="banner-breadcrumb">
                        <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="#">Home</a></li>
                        <li class="breadcrumb-item active" aria-current="page">Shopping Cart</li>
                        </ol>
                    </nav>
                </div>
            </div>
        </div>
    </section> -->
    <!-- ================ end banner area ================= -->

    <!--================Cart Area =================-->
    <!-- retrieve cart -->
    <section class="cart_area">
        <div class="container">
            <div class="cart_inner">
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th scope="col">Product</th>
                                <th scope="col">Price</th>
                                <th scope="col">Quantity</th>
                            </tr>
                        </thead>
                        <tbody id="cart_data">
                            
                        </tbody>
                        <tfoot>
                            <tr class="text-center">
                                <td></td>
                                <td>
                                    <h5>Subtotal</h5>
                                </td>
                                <td>
                                    <h5 id="total_price">-</h5>
                                </td>
                            </tr>
                            
                            <!-- input cart products here -->
                            <tr class="bottom_button">
                                <td>
                                    <a class="button" id="clear_session" href="#">Clear Cart</a>
                                </td>
                                <td>
                                    <input type="hidden" id="product_details" name="product_details" value=furniture>
                                    <a class="button" href="category.php">Update Cart</a>
                                </td>
                                <td>
                                    <input type="submit" name="Proceed To Checkout" value="Checkout" class="button" onclick=submitfunction()></a>
                                </td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </div>
        </div>
    </section>
    <!--================End Cart Area =================-->

    <!--================ Start footer Area  =================-->	
    <?php include "./footer.html" ?>
    <!--================ End footer Area  =================-->
    
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="vendors/skrollr.min.js"></script>
    <script src="vendors/owl-carousel/owl.carousel.min.js"></script>
    <script src="vendors/nice-select/jquery.nice-select.min.js"></script>
    <script src="vendors/nouislider/nouislider.min.js"></script>
    <script src="vendors/jquery.ajaxchimp.min.js"></script>
    <script src="vendors/mail-script.js"></script>
    <script src="js/main.js"></script> 
    

    <script
    src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js"
    integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut"
    crossorigin="anonymous"></script>

    <script 
    src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js"
    integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k"
    crossorigin="anonymous"></script>

    <script>
        if (sessionStorage.getItem("login_session") == null){
        window.location.replace("./login.php");
        }
    </script>

    <script>

        async function update_price(product_id){
            var cart = JSON.parse(sessionStorage.getItem("cart"));
            console.log(cart);
            var new_cart = [];
            var quantity = $(`#${product_id}`).val();
            for (const item of cart) {
                if (item.product_id == product_id){
                    var change = quantity - item.quantity
                    var price = item.price;
                    var current_total = parseFloat($("#total_price").text());
                    // console.log(change, price, current_total);
                    var new_total = current_total + (price * change);
                    $("#total_price").text(new_total.toFixed(2));

                    item.quantity = quantity
                    if (quantity == 0){
                        console.log(quantity);
                    }else{
                        new_cart.push(item)
                        console.log(new_cart);
                    }
                }else{
                    new_cart.push(item)
                    console.log(new_cart);
                }
            }
            if (new_cart.length > 0){
                console.log(new_cart);
                sessionStorage.setItem("cart", JSON.stringify(new_cart));
                list_data();
            }else{
                clear_session();
            }
            
            
        
        }

        function update_cart_details(cart_items, furniture){
            for (const single_furniture of furniture) {
                for (const item of cart_items) {
                    if (single_furniture.product_id == item.product_id){
                        item.price = parseFloat(single_furniture.price);
                        item.product_name = single_furniture.product_name;
                    }
                }
            }
            sessionStorage.setItem("cart", JSON.stringify(cart_items));
        }

        function clear_session(){
            sessionStorage.removeItem("cart");
            location.reload();
        }

        function submitfunction(){
            if (sessionStorage.getItem("cart") == null){
                alert("No Items in cart")
            }
            else{
                window.location.replace("checkout.php");
            }
            
        }

        function retrieve_cart(){
            var cart_items = sessionStorage.getItem("cart");
            if (cart_items){
                return JSON.parse(cart_items)
            }
            return "No Items in cart"
        }

        function get_quantity(cart_items, product_id){
            for (const item of cart_items) {
                if (item.product_id == product_id){
                    return item.quantity;
                }
            }
        }

        async function get_data(search_url, cart_items){
            var param = {
                    method : "get",
                    mode : 'cors'
                };
            const response = await fetch (search_url, param);
            const data = await response.json();
            var furniture = data.Furniture;

            update_cart_details(cart_items, furniture);
            // assign all the cart items to session
            // sessionStorage.setItem("product_details", JSON.stringify(furniture));

            if (!furniture || !furniture.length) {
                showError ('furniture list empty or undefined. ')
            } else {
                let furniture_data = "";
                let total_price = 0.0;
                for (const single_furniture of furniture){
                    var quantity = get_quantity(cart_items, single_furniture.product_id);
                    total_price += parseFloat(single_furniture.price) * quantity;
                    furniture_data += 
                    `<tr>
                        <td>
                            <div class="media">
                                <div class="d-flex">
                                    <img src='./${single_furniture.image}' alt="" style="height:10vw;">
                                </div>
                                <div class="media-body">
                                    <p><B>${single_furniture.product_name}</B></p>
                                </div>
                            </div>
                        </td>
                        <td>
                            <h5 id="price${single_furniture.product_id}">$${parseFloat(single_furniture.price).toFixed(2)}</h5>
                        </td>
                        <td>
                            <div class="product_count">
                                <input type="number" name="${single_furniture.product_name}" id="${single_furniture.product_id}" value="${quantity}" min="0" onchange="update_price(${single_furniture.product_id})">
                            </div>
                        </td>
                    </tr>`
                }
                $("#cart_data").empty();
                $('#cart_data').prepend(furniture_data);
                console.log(furniture);
                $("#total_price").text(total_price.toFixed(2));
            }
        }
        
        function get_cart_id(cart_items){
            var cart_ids = "";
            if (typeof(cart_items) == 'object') {
                for (const item of cart_items) {
                    cart_ids += item["product_id"] + ","
                }
            }
            return cart_ids.slice(0,-1)
        }

        async function list_data(){
            var cart_items = retrieve_cart();

            var cart_ids = get_cart_id(cart_items);
            
            var serviceURL = "http://127.0.0.1:5003/furniture/product/" + cart_ids;
            get_data(serviceURL, cart_items);
        }
        
        $(async () =>{
            list_data();
        });

        $("#cart").addClass("active");

        $("#clear_session").click(function(e){
            e.preventDefault();
            clear_session();
        });
    </script>


</body>
</html>