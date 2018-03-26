<?php
session_start();
require_once "pdo.php";

if ( isset($_POST['cancel'] ) ) {
    header("Location: index.php");
    return;
}


$salt = 'XyZzy12*_';
$stored_hash = '1a52e17fa899cf40fb04cfc42e6352f1';  // Pw is php123

//$_SESSION['error'] = false;

// Check to see if we have some POST data, if we do process it
if ( isset($_POST['email']) && isset($_POST['pass']) ) {
  //unset($_SESSION['name']);
    if ( strlen($_POST['email']) < 1 || strlen($_POST['pass']) < 1 ) {
        $_SESSION['error'] ='Email and password are required';
        header('Location:login.php');
        //error_log("Login fail".$_POST['email']);
        return;
      } else {
        $check_email = preg_match('/^[0-9a-zA-Z]([\-.\w]*[0-9a-zA-Z\-_+])*@(.)+$/', $_POST['email']);
        if ($check_email) {
          $check = hash('md5', $salt.$_POST['pass']);
          if ( $check == $stored_hash) {
            // Redirect the browser
            $_SESSION['name']=$_POST['email'];
            //$_SESSION['success'] = 'Logged in';
            header("Location: index.php");
            error_log("Login success".$_POST['email']);
            return;
          } else {
            $_SESSION['error'] = 'Incorrect password.';
            header('Location: login.php');
            error_log("Login fail".$_POST['email']."$check");
            return;
          }
        } else {
          $_SESSION['error'] = 'Email must have an at-sign(@)';
          header('Location: login.php');
          error_log("Login fail".$_POST['email']);
          return;
        }
      }
    }

// Fall through into the View
?>
<!DOCTYPE html>
<html>
<head>
<title>Jun Ha Park's Login Page</title>
</head>
<body>
<h1>Please Log In</h1>
<?php
// Note triple not equals and think how badly double
// not equals would work here...
if ( isset($_SESSION['error'])) {
    // Look closely at the use of single and double quotes
    echo('<p style="color: red;">'.htmlentities($_SESSION['error'])."</p>\n");
    unset($_SESSION['error']);
}
?>
<form method="POST">
<label for="nam">User Name</label>
<input type="text" name="email" id="nam"><br/>
<label for="id_1723">Password</label>
<input type="text" name="pass" id="id_1723"><br/>
<input type="submit" value="Log In">
<a href="index.php">Cancel</a>
</form>

