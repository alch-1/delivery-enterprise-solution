<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title> Refurban - Home</title>

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
        height: 25vw;
        object-fit: contain;
    }
  </style>

</head>
<body>
  <!--================ Start Header Menu Area =================-->
  <?php include "./header.html" ?>
	
	<!--================ End Header Menu Area =================-->

  <main class="site-main">
  
    
    <!--================ Hero banner start =================-->
    <section class="hero-banner">
      <div class="container">
        <div class="row no-gutters align-items-center pt-60px">
          <div class="col-5 d-none d-sm-block">
            <div class="hero-banner__img">
              <img class="img-fluid" src="img/mainoffice.jfif" alt="">
            </div>
          </div>
          <div class="col-sm-7 col-lg-6 offset-lg-1 pl-4 pl-md-5 pl-lg-0">
            <div class="hero-banner__content">
              <h4>Refurbish Your Urban Office</h4>
              <h1>Designed For Your Comfort</h1>
              <!-- <p>Welcome!</p> -->
              <a class="button button-hero" href="category.php">Browse Now</a>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!--================ Hero banner start =================-->

  

    <!--================ Hero Carousel start =================-->
    <!-- <section class="section-margin mt-0">
      <div class="owl-carousel owl-theme hero-carousel">
        <div class="hero-carousel__slide">
          <img src="img/Desk2.jpg" alt="" class="img-fluid">
          <a href="#" class="hero-carousel__slideOverlay">
            <h3>Desk table</h3>
          </a>
        </div>
        <div class="hero-carousel__slide">
          <img src="img/home/hero-slide2.png" alt="" class="img-fluid">
          <a href="#" class="hero-carousel__slideOverlay">
            <h3>Chair</h3>
          </a>
        </div>
        <div class="hero-carousel__slide">
          <img src="img/home/hero-slide3.png" alt="" class="img-fluid">
          <a href="#" class="hero-carousel__slideOverlay">
            <h3>Storage Shelves</h3>
          </a>
        </div>
      </div>
    </section> -->
    <!--================ Hero Carousel end =================-->

    <!-- ================  Just for you section start ================= -->  
    <section class="section-margin container">
        <div class="section-intro pb-60px">
          <h2>Just For <span class="section-intro__style">You</span></h2>
        </div>
        <div class="row" id="product_listing"></div>
    </section>
    <!-- ================ trending product section end ================= -->  

    <!-- ================ Subscribe section start ================= --> 
    <!-- <section class="subscribe-position">
      <div class="container">
        <div class="subscribe text-center">
          <h3 class="subscribe__title">Get Updates From Us!</h3>
          <p>20% off on your first order!</p>
          <div id="mc_embed_signup">
            <form target="_blank" action="https://spondonit.us12.list-manage.com/subscribe/post?u=1462626880ade1ac87bd9c93a&amp;id=92a4423d01" method="get" class="subscribe-form form-inline mt-5 pt-1">
              <div class="form-group ml-sm-auto">
                <input class="form-control mb-1" type="email" name="EMAIL" placeholder="Enter your email" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Your Email Address '" >
                <div class="info"></div>
              </div>
              <button class="button button-subscribe mr-auto mb-1" type="submit">Subscribe Now</button>
              <div style="position: absolute; left: -5000px;">
                <input name="b_36c4fd991d266f23781ded980_aefe40901a" tabindex="-1" value="" type="text">
              </div>

            </form>
          </div>
          
        </div>
      </div>
    </section> -->
    <!-- ================ Subscribe section end ================= --> 

    

  </main>

  <!-- Modal -->
  <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true" data-backdrop="false">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLongTitle">Thank you for purchasing with us!</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          To complete your experience, sign up to our telegram bot to get notification on your delivery! <br><br>
          <div class="text-center">
            <a target="_blank" class="btn btn-primary btn-sm" rel="noopener noreferrer" href="http://t.me/qilinpo_shopping_bot">Furniture Messenger Bot</a>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>




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
    $("#home").addClass("active")
  </script>
  <script>
    $(function (){
      if (window.location.search != ''){
        let searchParams = new URLSearchParams(window.location.search)
        if (searchParams.has('modal')){
          sessionStorage.removeItem("cart");
          $('#myModal').modal('show');
        }
      }

    });
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

  <script>
      $(async() => {
          // change the service URL to your own URL
          console.log('this should run');
          var serviceURL = "http://127.0.0.1:5003/furniture";
          var param = {
              method : "get",
              mode : 'cors'
          };

          try {
              const response = await fetch (serviceURL, param);
              const data = await response.json();
              var furniture = data.Furnitures; //the arr is in data.books of json data
              // array or array.length are false

              if (!furniture || !furniture.length) {
                  showError ('furniture list empty or undefined. ')
              } else {

              //  console.log('print items');
                  // for loops to set up all table tows with the obtained book data
                  furniture_data = "";
                  i = 0;
                  while (furniture.length != 0 && i < 12) {
                    random_index = Math.floor(Math.random() * furniture.length);
                    random_furniture = furniture[random_index];
                    furniture.splice(random_index, 1);
                    i++;
                    console.log(random_furniture);
                    furniture_data += 
                    `<div class="col-md-6 col-lg-4 col-xl-3 d-flex">
                      <div class="card text-center card-product flex-fill">
                        <div class="card-product__img">
                          <img class="card-img-top img-fluid" src='./${random_furniture.image}' alt="image not available">
                          <ul class="card-product__imgOverlay">
                            <li><button><i class="ti-shopping-cart" id="checkout_products" name=${random_furniture.product_id} onclick= add_to_cart(${random_furniture.product_id})></i></button></li>
                            <li><button><i class="ti-heart"></i></button></li>
                          </ul>
                        </div>
                        <div class="card-body">
                          <p>${random_furniture.category}</p>
                          <h4 class="card-product__title"><a>${random_furniture.product_name}</a></h4>
                          <p class="card-product__price">$${parseFloat(random_furniture.price).toFixed(2)}</p>
                        </div>
                      </div>
                    </div>`
                  }
                  
                  $('#product_listing').append(furniture_data);
                
              }
          } catch(error){
              // Errors when calling the service such as network errors,
              //service offline
              showError
              ('There is a problem retrieving books data, please try again later. <br/>' + error);
          }
      });
</script>
</body>
</html>


