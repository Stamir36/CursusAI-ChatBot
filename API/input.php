<?php
    include "../../service/config.php";

    header('Content-Type: application/json; charset=utf-8');

    $mysql = new mysqli($Host, $User, $Password, $Database);

    $result = $mysql->query("SELECT * FROM `messages` WHERE `incoming_msg_id` = '0' AND `see` = ' false' LIMIT 1");
    $result = $result->fetch_assoc();

    echo json_encode($result);  
    
    $mysql->close();  
?>