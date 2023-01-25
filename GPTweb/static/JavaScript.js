$(document).ready(function() {
    $("#registerForm").validate({
        rules: {
            username: {
                required: true,
                minlength: 3
            },
            password: {
                required: true,
                minlength: 8
            }
        },
        messages: {
            username: {
                required: "Please enter a username",
                minlength: "Your username must be at least 3 characters long"
            },
            password: {
                required: "Please provide a password",
                minlength: "Your password must be at least 8 characters long"
            }
        },
        submitHandler: function(form) {
            // code to handle the form submission
        }
    });
});

