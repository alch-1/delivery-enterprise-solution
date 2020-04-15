<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Refurban - Category</title>

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

    <style>
      .card-img-top {
        width: 100%;
        height: 20vw;
        object-fit: contain;
      }
    </style>

</head>
<body>

  <script>
    if (sessionStorage.getItem("login_session") == null){
      window.location.replace("./login.php");
    }
  </script>
  <script>
    // using session to store data added to cart
    function add_to_cart(product_id){
      
      if (sessionStorage.getItem("cart") == null){
        cart = [{"product_id": product_id, "quantity": 1}]
        sessionStorage.setItem("cart", JSON.stringify(cart));
      }else{
        cart = JSON.parse(sessionStorage.getItem("cart"))
        let existing = false;
        for (const item of cart) {
          if (item.product_id == product_id){
            existing = true;
            item.quantity += 1
          }
        }
        if (existing == false){
          cart.push({"product_id": product_id, "quantity": 1})
        }
        
        sessionStorage.setItem("cart", JSON.stringify(cart));
      }
      // console.log(cart);
      alert("Successfully added to cart");
    }
  </script>

  <!--================ Start Header Menu Area =================-->
	<?php include "./header.html" ?>
	<!--================ End Header Menu Area =================-->

  <!-- ================ category section start ================= -->	
      

  <section class="section-margin--small mb-5">
    <div class="container">
      <div class="row">
        <div class="col-10 offset-1">
          <div class="filter-bar d-flex flex-wrap align-items-center">
            <div class="ml-auto">
              <div class="input-group filter-bar-search">
                <input type="text" placeholder="Search" id="search_input">
                <div class="input-group-append">
                  <button type="button" id="search_button"><i class="ti-search"></i></button>
                </div>
              </div>
            </div>
          </div>
          <!-- End Filter Bar -->

          <!-- DISPLAY ALL THE PRODUCTS HERE -->
          <!-- Start Best Seller -->
          <section class="lattest-product-area pb-40 category-list">
            <!-- append all the items to row -->
            <div class="row" id="product_listing">
            </div>
            <!--end of the row tab is here-->
          </section>
          <!-- End Best Seller -->
        </div>
      </div>
    </div>
  </section>
	<!-- ================ category section end ================= -->		  

  <!----------- include fetch from product microservice ---------->

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
      // helper function to display error Message 
      function showError(message){
          $('#booksTable').hide();
          $('#addBookBtn').hide();

          // display an error under the main container
          $('#main-container').append("<label>"+message+"<label>");
      }
      

      //function to run async function
      async function getData(search_url){
        var param = {
                method : "get",
                mode : 'cors'
            };
        try {
            const response = await fetch (search_url, param);
            const data = await response.json();
            var furniture = data.Furnitures; //the arr is in data.books of json data
            // array or array.length are falsy
            // console.log(furniture);
            if (!furniture || !furniture.length) {
                showError ('furniture list empty or undefined. ')
            } else {
                // for loops to set up all table tows with the obtained book data
                furniture_data = "";
                var data_category = [];
                for (const single_furniture of furniture){
                  console.log(single_furniture);
                  furniture_data += 
                  `<div class="col-md-6 col-lg-4 d-flex">
                    <div class="card text-center card-product flex-fill">
                      <div class="card-product__img">
                        <img class="card-img-top img-fluid" src='./${single_furniture.image}' alt="image not available">
                        <ul class="card-product__imgOverlay">
                          <li><button><i class="ti-shopping-cart" id="checkout_products" name=${single_furniture.product_id} onclick= add_to_cart(${single_furniture.product_id})></i></button></li>
                          <li><button><i class="ti-heart"></i></button></li>
                        </ul>
                      </div>
                      <div class="card-body">
                        <p>${single_furniture.category}</p>
                        <h4 class="card-product__title"><a href="#">${single_furniture.product_name}</a></h4>
                        <p class="card-product__price">$${parseFloat(single_furniture.price).toFixed(2)}</p>
                      </div>
                    </div>
                  </div>`
                  if ((data_category.includes(`${single_furniture.category}`)== false) ){
                    data_category.push(`${single_furniture.category}`);
                  }
                } 
              $('#product_listing').empty();
              $('#product_listing').append(furniture_data);
              
            }
        }
        //catch error here
        catch(error){
                // Errors when calling the service such as network errors,
                //service offline
                showError('There is a problem retrieving books data, please try again later. <br/>' + error);
            }
      }

      // anonymous async function
      // using await required the function that calls it to be async
      //fetch data to display all the product from the database
      
      $('#search_button').click( function (e) {
        //code for search input
        var search_input = $("#search_input").val();
        var serviceURL = "http://127.0.0.1:5003/furniture/" + search_input;
        getData(serviceURL);
      });


      // when page load
      $(document).ready(function(){
        var serviceURL = "http://127.0.0.1:5003/furniture";
        getData(serviceURL);
      });

    $("#category").addClass("active")
  </script>
</body>
</html>