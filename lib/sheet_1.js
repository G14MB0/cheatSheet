
// Function to send email
const nodemailer = require('nodemailer');
function sendEmail() {
    let transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: 'youremail@gmail.com',
            pass: 'YOUR_APP_PASSWORD'
        }
    });

    let mailOptions = {
        from: 'youremail@gmail.com',
        to: 'recipientemail@example.com',
        subject: 'Sending Email using Node.js and Electron',
        text: 'That was easy!'
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.log(error);
        } else {
            console.log('Email sent: ' + info.response);
        }
    });
}