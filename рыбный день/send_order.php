<?php
$to = "ваш_email@домен.ru"; // Замените на email магазина
$subject = "Новый заказ с сайта Рыбныйдень";


$name = $_POST['name'] ?? '';
$phone = $_POST['phone'] ?? '';
$email = $_POST['email'] ?? '';
$address = $_POST['address'] ?? '';
$comment = $_POST['comment'] ?? '';
$order = $_POST['order'] ?? '';


$message = "НОВЫЙ ЗАКАЗ\n\n";
$message .= "Имя: $name\n";
$message .= "Телефон: $phone\n";
$message .= "Email: $email\n";
$message .= "Адрес: $address\n";
$message .= "Комментарий: $comment\n\n";
$message .= $order . "\n\n";
$message .= "Дата: " . date('d.m.Y H:i:s');

$headers = "From: сайт@рыбныйдень.ru\r\n";
$headers .= "Reply-To: $email\r\n";
$headers .= "Content-Type: text/plain; charset=utf-8\r\n";

if (mail($to, $subject, $message, $headers)) {
    $orderData = [
        'date' => date('d.m.Y H:i:s'),
        'name' => $name,
        'phone' => $phone,
        'email' => $email,
        'address' => $address,
        'comment' => $comment,
        'order' => $order
    ];
    
    file_put_contents('orders_backup.txt', json_encode($orderData, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n---\n", FILE_APPEND);
    
    echo json_encode(['success' => true, 'message' => 'Заказ успешно отправлен']);
} else {
    echo json_encode(['success' => false, 'message' => 'Ошибка отправки заказа']);
}
?>