<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Refurban - Checkout</title>

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
    <!-- #fetch the input of the items in cart here -->


    <!--================ Start Header Menu Area =================-->
    <?php include "./header.html" ?>
    <!--================ End Header Menu Area =================-->


    <!--================Checkout Area =================-->
    <section class="checkout_area section-margin--small">
        <div class="container">
            <div class="billing_details">
                <div class="row">
                    <div class="col-lg-8">
                        <h3>Billing Details</h3>
                        <form class="row contact_form" action="#" method="post" novalidate="novalidate">
                            <!-- Telehandle -->
                            <div class="col-md-12 form-group p_star">
                                <input type="text" class="form-control" id="telehandle" name="telehandle" placeholder="Telegram Handle" required>
                                <span class="placeholder"></span>
                            </div>
                            <!-- Addr -->
                            <div class="col-md-12 form-group p_star">
                                <input type="text" class="form-control" id="address" name="address" placeholder="Address" required>
                                <span class="placeholder"></span>
                            </div>
                            
                            <div class="col-md-8 form-group">
                                <input type="text" class="form-control" id="postal_code" name="postal_code" placeholder="Postcode/ZIP" required>
                            </div>
                            <!-- Dlvry timeslot -->
                            <div class="col-md-4 form-group p_star">
                                <select id="timeslot" class="form-control">
                                    <option value="" selected disabled hidden>Choose your Timeslot</option>
                                    <option value="AM">AM</option>
                                    <option value="PM">PM</option>
                                </select>
                            </div>
                            <!-- Date of delivery -->
                            <div class="col-md-12 form-group p_star">
                                <input type="text" class="form-control" id="date_of_delivery" name="date_of_delivery" placeholder="Date of Delivery (YYYY-MM-DD)" required>
                                <span class="placeholder"></span>
                            </div>
                        </form>
                    </div>
                    <div class="col-lg-4">
                        <div class="order_box">
                            <h2>Your Order</h2>
                            <ul class="list" id="order_list">
                                <li><a href="#"><h4>Product <span>Total</span></h4></a></li>
                                
                            </ul>
                            <ul class="list list_2" id="price_list">
                                <input type="hidden" name="total_price" id="total_price" value=''>
                            </ul>
                            <div class="payment_item active">
                                <div class="radion_btn">
                                    <input type="radio" id="paypal" name="selector">
                                    <label for="paypal">Paypal </label>
                                    <img src="img/product/card.jpg" alt="">
                                    <div class="check"></div>
                                </div>
                                <p>Pay via PayPal; you can pay with your credit card if you don’t have a PayPal account.</p>
                            </div>
                            <div class="creat_account">
                                <input type="checkbox" id="f-option4" name="selector">
                                <label for="f-option4">I’ve read and accept the </label>
                                <a href="#">terms & conditions*</a>
                            </div>
                            <div class="text-center">
                                <a id="submit" class="button button-paypal" href="#">Make Payment</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!--================End Checkout Area =================-->



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
        }else{
            console.log(sessionStorage.getItem("login_session"));
            var customer_details = JSON.parse(sessionStorage.getItem("login_session"));
            console.log(customer_details);
            $("#telehandle").val(customer_details.telehandle);
            $("#address").val(customer_details.address);
            $("#postal_code").val(customer_details.postal_code);            
        }
    </script>
    
    <script>
        function retrieve_cart(){
            // document.getElementById("result").innerHTML = sessionStorage.getItem("product_id");
            var cart = sessionStorage.getItem("cart");
            if (cart){
                return cart
            }
            return "No Items in Cart"
        }

        $(function(){
            var cart = JSON.parse(retrieve_cart());
            var total_price = 0
            for (const element of cart) {
                console.log(element)
                total_price += parseFloat(element.price) * parseInt(element.quantity);
                $("#order_list").append(
                    `<li><a href="#">
                    <div class="row">
                        <div class="col-6">${element.product_name}</div>
                        <div class="col-3 text-right">x ${element.quantity}</div> 
                        <div class="col-3 text-right">$${element.price}</div>
                    </div>
                    </a></li>`
                )
            }
            $("#price_list").append(
                `
                <li><a href="#">Total <span>$${total_price.toFixed(2)}</span></a></li>
                `
            )
            $("#total_price").val(total_price);

        });

        async function make_payment(total_price){
            var cart = JSON.parse(retrieve_cart());
            var telehandle = $("#telehandle").val();
            var address = $("#address").val();
            var postal_code = parseInt($("#postal_code").val());
            var date_of_delivery = $("#date_of_delivery").val();
            var timeslot = $("#timeslot").val();
            if (telehandle == '' || cart == "" || address == "" || postal_code == "" || timeslot == "" || date_of_delivery == ""){
                alert("Please fill in your details accordingly.")
            }else{
                requestBody = {
                    "amount": {
                        "total": total_price.toFixed(2),
                        "currency": "SGD"
                    },
                    "purchase_details": {
                        "total_price": parseFloat(total_price),
                        "telehandle" : telehandle,
                        "address": address,
                        "postal_code": postal_code,
                        "date_of_delivery": date_of_delivery,
                        "timeslot": timeslot,
                        "cart_details": cart
                    }
                }
                paymentURL = "http://127.0.0.1:5002/payment/create"
                params = {
                    method: "POST",
                    mode: "cors",
                    headers: {"content-type" : "application/json; charset=UTF-8;"},
                    body: JSON.stringify(requestBody)
                }
                try {
                    const response = await fetch(paymentURL, params)
                    const data = await response.json();
                    console.log(data.approval_url);
                    
                    window.location.replace(data.approval_url);
                } catch (error) {
                    console.log('There is a problem, please try again later. \n' + error);
                }
            }
            
        }

        


        $("#checkout").addClass("active");
        $("#submit").click(async (event) => {
            
            event.preventDefault();
            var total_price = parseFloat($("#total_price").val());
            make_payment(total_price);            
        });
    </script>
</body>
</html>