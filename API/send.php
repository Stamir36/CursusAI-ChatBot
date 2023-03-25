<?php
    include "../../service/config.php";

    header('Content-Type: application/json; charset=utf-8');

    $mysql = new mysqli($Host, $User, $Password, $Database);

    $msg_id = $_GET["msg_id"];
    $user = $_GET["user"];
    $msg = $_GET["msg"];

    $mysql->query("UPDATE `messages` SET `see` = 'true' WHERE `messages`.`msg_id` = $msg_id");
    $mysql->query("INSERT INTO `messages` (`msg_id`, `incoming_msg_id`, `outgoing_msg_id`, `msg`, `time`, `see`) VALUES (NULL, '$user', '0', '$msg', CURRENT_TIMESTAMP, 'true')");

    $mysql->close();  
?>