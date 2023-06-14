<?php
    include "../../service/config.php";

    header('Content-Type: application/json; charset=utf-8');

    $mysql = new mysqli($Host, $User, $Password, $Database);
    $conn = mysqli_connect($Host, $User, $Password, $Database);
    mysqli_set_charset($conn, "utf8mb4");
  
    $msg_id = $_GET["msg_id"];
    $user = $_GET["user"];
    $msg = $_GET["msg"];
    
    $message = mysqli_real_escape_string($conn, "<img style='max-height: 400px; border-radius: 5px; max-width: 500px; width: 100%; height: 100%;' src='/app/cursus/files/".$msg."' alt='image file'>");

    $mysql->query("UPDATE `messages` SET `see` = 'true' WHERE `messages`.`msg_id` = $msg_id");
    
    if(!empty($message)){
        $sql = mysqli_query($conn, "INSERT INTO messages (incoming_msg_id, outgoing_msg_id, msg) VALUES ({$user}, '0', '{$message}')") or die();
    }

    $mysql->close();  
?>