<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require 'PHPMailer-master/src/Exception.php';
require 'PHPMailer-master/src/PHPMailer.php';
require 'PHPMailer-master/src/SMTP.php';

header('Content-Type: application/json');

$response = ['status' => 'error', 'message' => 'An unknown error occurred'];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $contentType = isset($_SERVER["CONTENT_TYPE"]) ? trim($_SERVER["CONTENT_TYPE"]) : '';
    $errorDetails = '';

    function sendMail($subject, $body, $recipient, &$response, &$errorDetails) {
        $mail = new PHPMailer(true);

        try {
            $mail->isSMTP();
            $mail->Host = 'send.one.com';
            $mail->SMTPAuth = true;
            $mail->Username = '{{ email }}';
            $mail->Password = '{{ email_pwd }}';
            $mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS;
            $mail->Port = 465;

            $mail->setFrom('{{ email }}', 'Website form');
            $mail->addAddress($recipient);

            $mail->isHTML(true);
            $mail->Subject = $subject;
            $mail->Body    = $body;
            $mail->AltBody = strip_tags($body);

            $mail->send();
            $response['status'] = 'success';
            $response['message'] = 'Message has been sent';
        } catch (Exception $e) {
            $response['message'] = "Message could not be sent. Mailer Error: {$mail->ErrorInfo}";
            $errorDetails = "Mailer Error: " . $mail->ErrorInfo;
        }
    }

    if ($contentType === "application/json") {
        $input = json_decode(file_get_contents('php://input'), true);

        if ($input && isset($input['name'], $input['email'], $input['emailBody'])) {
            $name = $input['name'];
            $email = $input['email'];
            $emailBody = $input['emailBody'];
            $message = isset($input['message']) ? $input['message'] : '';

            sendMail('New Quote Request', $emailBody, '{{ email }}', $response, $errorDetails);

            if ($response['status'] === 'success') {
                $thankYouBody = "Dear $name,<br><br>Thank you for your interest in our services. We have received your request and will get back to you soon.<br><br>Best regards,<br>AllroundWebsite Team";
                sendMail('Thank You for Your Request', $thankYouBody, $email, $response, $errorDetails);
            }
        } else {
            $response['message'] = 'Invalid input data';
            $errorDetails = 'Invalid input data received';
        }
    } else {
        if (isset($_POST['email'], $_POST['name'], $_POST['message'])) {
            $fromEmail = $_POST['email'];
            $name = $_POST['name'];
            $message = $_POST['message'];

            // Log the values of the received data
            file_put_contents('php://stderr', "Received email: $fromEmail, name: $name, message: $message\n");

            // Include the name in the email body
            $emailBody = "From: $fromEmail<br>Name: $name<br>Message: $message";

            sendMail("Message from $name", $emailBody, '{{ email }}', $response, $errorDetails);
        } else {
            $response['message'] = 'Invalid input data';
            $errorDetails = 'Invalid input data received';
        }
    }

    if ($response['status'] === 'error') {
        $mail = new PHPMailer(true);
        try {
            $mail->isSMTP();
            $mail->Host = 'send.one.com';
            $mail->SMTPAuth = true;
            $mail->Username = '{{ email }}';
            $mail->Password = '{{ email_pwd }}';
            $mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS;
            $mail->Port = 465;

            $mail->setFrom('{{ email }}', 'Website form');
            $mail->addAddress('{{ email }}');

            $mail->isHTML(true);
            $mail->Subject = 'Error in Sending Email';
            $mail->Body    = "An error occurred while trying to send an email.<br>Error Details:<br>{$response['message']}<br>{$errorDetails}";
            $mail->AltBody = strip_tags($mail->Body);

            $mail->send();
        } catch (Exception $e) {
            error_log("Error Notification Mailer Error: " . $mail->ErrorInfo);
        }
    }
} else {
    $response['message'] = 'Invalid request method';
}

echo json_encode($response);
?>
