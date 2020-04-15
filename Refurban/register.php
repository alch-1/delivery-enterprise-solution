<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title> Refurban - Register </title>

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
  <main class="site-main">
  
  <!-- ================ start banner area ================= -->	
  <!-- <section class="blog-banner-area" id="category">
    <div class="container h-100">
      <div class="blog-banner">
        <div class="text-center">
          <h1>Register</h1>
          <nav aria-label="breadcrumb" class="banner-breadcrumb">
            <ol class="breadcrumb">
              <li class="breadcrumb-item"><a href="#">Home</a></li>
              <li class="breadcrumb-item active" aria-current="page">Register</li>
            </ol>
          </nav>
        </div>
      </div>
    </div>
  </section> -->
  <!-- ================ end banner area ================= -->
  
  <!--================Login Box Area =================-->
  <section class="login_box_area section-margin">
    <div class="container">
      <div class="row">
        <div class="col-lg-6">
          <div class="login_box_img">
            <div class="hover">
              <h4>Already have an account?</h4>
              <p>Login to receive all our latest deals and events</p>
              <a class="button button-account" href="login.php">Login Now</a>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="login_form_inner register_form_inner">
            <h3>Create an account</h3>
              <form class="row login_form" action="#/" id="register_form"method="post" >
              <div class="col-md-12 form-group">
                <input type="text" class="form-control" id="Telehandle" name="Telehandle" placeholder="Telehandle" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Telehandle'">
              </div>
              <div class="col-md-12 form-group">
                <input type="text" class="form-control" id="Address" name="Address" placeholder="Address" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Address'">
              </div>
              <div class="col-md-12 form-group">
                <input type="text" class="form-control" id="PostalCode" name="PostalCode" placeholder="Postal Code" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Postal Code'">
              </div>
              <div class="col-md-12 form-group">
                <input type="password" class="form-control" id="Password" name="Password" placeholder="Password" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Password'">
              </div>
              <div class="col-md-12 form-group">
                <input type="password" class="form-control" id="ConfirmPassword" name="ConfirmPassword" placeholder="Confirm Password" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Confirm Password'">
              </div>
              <div class="col-md-12 form-group">
                <button type="submit" value="submit" id="submitRegister" class="button button-register w-100">Register</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>
  <!--================End Login Box Area =================-->


  <!--================ Start footer Area  =================-->
  <?php include "./footer.html" ?>
  
  <!--================ End footer Area  =================-->
  <script src="vendors/skrollr.min.js"></script>
        <script src="vendors/owl-carousel/owl.carousel.min.js"></script>
        <script src="vendors/nice-select/jquery.nice-select.min.js"></script>
        <script src="vendors/nouislider/nouislider.min.js"></script>
        <script src="vendors/jquery.ajaxchimp.min.js"></script>
        <script src="vendors/mail-script.js"></script>
        <script src="js/main.js"></script> 
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js"
        integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut"
        crossorigin="anonymous"></script>
        
        <script 
        src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js"
        integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k"
        crossorigin="anonymous"></script>

  
    <script>
      $("#register").addClass("active");
      // anonymous async function - using await requires the function that calls it to be async
      $(async() => {        
        $("#submitRegister").click(function (e){
          e.preventDefault();
          var Telehandle = $("#Telehandle").val(); 
          var Address = $("#Address").val(); 
          var PostalCode = $("#PostalCode").val(); 
          var Password = $("#Password").val(); 
          var ConfirmPassword = $("#ConfirmPassword").val();

          
          
          if (Telehandle != "" && Address != "" && PostalCode != "" && Password != ""&& ConfirmPassword != "" && Password == ConfirmPassword){
            var params = {
              "address": $("#Address").val(),
              "postal_code": $("#PostalCode").val(),
              "password": $("#Password").val(),
            };
            Register(Telehandle,params);
          }

        });

      });

        // Change serviceURL to your own
      async function Register(Telehandle, params){       
        var serviceURL = `http://127.0.0.1:5000/register/${Telehandle}`;

        try {
          var requestParams = {
            method: 'POST',
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json; charset=utf-8;'
            },
            body: JSON.stringify(params)
          }
          const response = await fetch(serviceURL, requestParams);
          const data = await response.json();
          if (data.telehandle){
            alert("Success");
            window.location.replace("login.php");   
          }else{
            alert(data.message);
          }
        } catch (error) {
          console.log(error);
        }


      };
    </script>

</body>
</html>