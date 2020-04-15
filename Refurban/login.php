<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title> Refurban - Login </title>

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

        <!--================Login Box Area =================-->
        <section class="login_box_area section-margin">
            <div class="container">
                <div class="row">
                    <div class="col-lg-6">
                        <div class="login_box_img">
                            <div class="hover">
                                <h4>New to our website?</h4>
                                <p>Login to receive latest deals and updates!</p>
                                <a class="button button-account" href="register.php">Create an Account</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <div class="login_form_inner">
                            <h3>Log in to enter</h3>
                            <form class="row login_form" action="#/" id="contactForm">
                                <div class="col-md-12 form-group">
                                    <input type="text" class="form-control" id="Telehandle" name="Telehandle" placeholder="Telehandle" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Telehandle'">
                                </div>
                                <div class="col-md-12 form-group">
                                    <input type="password" class="form-control" id="Password" name="Password" placeholder="Password" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Password'">
                                </div>
                                <div class="col-md-12 form-group">
                                    <button type="submit" value="submit" id="submitLogin" class="button button-login w-100">Log In</button>
                                    <a href="#">Forgot Password?</a>
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
            $("#login").addClass("active");
            $(async() => {
                console.log("test");
                $("#submitLogin").click(function (e) {
                    e.preventDefault();
                    var Telehandle = $("#Telehandle").val();
                    var Password = $("#Password").val();

                    
                    if (Telehandle != "" && Password != "") {
                        console.log(Telehandle, Password);
                        Auth(Telehandle, Password);                        
                    }


                });

            });

            // $(async () =>{
            //     start_ups();
            // });


            async function Auth(Telehandle, Password){
                var serviceURL = `http://localhost:5000/login/${Telehandle}/${Password}`;
                // console.log(serviceURL);
                try {
                    const response = await fetch(serviceURL, {
                        method: "GET"
                    });
                    const data = await response.json();
                    if (data.message){
                        window.location.replace("index.php");
                        sessionStorage.setItem("login_session", JSON.stringify(data.customer_details));
                    }else{
                        alert("Invalid Password/Telehandler")
                    }
                    
                } catch (error) {
                    alert(error);
                }
            };

            // async function start_ups(){
            //     var service1URL = `http://localhost:8990/`;
            //     // console.log(serviceURL);
            //     try {
            //         const response = await fetch(service1URL, {
            //             method: "GET"
            //         });
            //         const data = await response.json();
                    
            //     } catch (error) {
            //         console.log(error);
            //     }

            //     var service2URL = `http://localhost:5006/`;
            //     // console.log(serviceURL);
            //     try {
            //         const response = await fetch(service2URL, {
            //             method: "GET"
            //         });
            //         const data = await response.json();
                    
            //     } catch (error) {
            //         console.log(error);
            //     }
            // }

        </script>
</body>

</html>
    