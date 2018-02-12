/* script to manipulate the interface events*/
var ajax = function (options) {
    function setDefaultVal(value, defaultValue){
        return (value === undefined) ? defaultValue : value;
    }
    var settings = {
        url: setDefaultVal(options.url, ""),
        type: setDefaultVal(options.type, "GET"),
        headers: setDefaultVal(options.headers, {}),
        data: setDefaultVal(options.data, {}),
        dataType: setDefaultVal(options.dataType, "text"),
        success: setDefaultVal(options.success, function (response) {
            console.log(response);
        }),
        error: setDefaultVal(options.error, function (error) {
            console.log(error)
        })
    };
    // Can implement multiple methods of Ajax
    if(Window.fetch) {
        var data = new FormData();
        if (settings.data !== undefined) {
            Object.keys(settings.data).forEach(function (key) {
                data.append(key, settings.data[key]);
            });
        }

        function checkStatus(response) {
            if (response.status >= 200 && response.status < 300) {
                return response
            } else {
                var error = new Error(response.statusText);
                error.response = response;
                throw error;
            }
        }

        function parseData(response) {
            var type = response.headers.get('Content-Type');
            if (settings.dataType === "json" || type.index("json") >= 0) {
                return response.json();
            } else {
                return response.text()
            }
        }

        fetch(settings.url, {
            method: settings.type,
            body: data
        }).then(checkStatus).then(parseData).then(settings.success).catch(settings.error)
    }else{
        $.ajax(settings);
    }
};

var server = "https://binarywards.herokuapp.com/";

var toast = function (message) {
    Materialize.toast(message, 6000)
};


var start_loading = function () {
    if(document.querySelector("#preloader").classList.contains('d-none')){
        document.querySelector("#preloader").classList.remove('d-none');
    }
};

var stop_loading = function () {
    document.querySelector("#preloader").classList.add('d-none');
};

var redeem_code = function () {
    start_loading();
    var phone = document.querySelector('#phoneNumber').value;
    var code = document.querySelector('#redemptionCode').value;
    $.ajax({
        url: "api/redeem_token",
        type: "POST",
        data: {
            redemptionCode: code,
            phoneNumber: phone
        },
        dataTye: "json",
        success: function (response) {
            // Process your data here e.g:
            var success = response['success'];
            var message = response['message'];
            console.log(message);
            if (success) {
                toast(message)
            } else {
                toast(message)
            }
            stop_loading();
        },
        error: function (error) {
            console.log();
            toast(error.responseJSON.message);
            stop_loading();
        }
    });
};

function signUp() {
    start_loading();
    var companyCode = document.querySelector('#companyCode').value;
    var companyName = document.querySelector('#companyName').value;
    var companyEmail = document.querySelector('#email').value;
    var companyPhone = document.querySelector('#companyPhone').value;
    var password = document.querySelector('#registerPassword').value;
    ajax({
        url: "api/company_add",
        type: "POST",
        data: {
            company_code: companyCode,
            name: companyName,
            email: companyEmail,
            phone_number: companyPhone,
            password: password
        },
        dataTye: "json",
        success: function (response) {
            var success = response['success'];
            var message = response['message'];
            if (success) {
                toast("Company added successfully");
                toast(message);
            } else {
                toast("Company added successfully");
                toast(message);
            }
            stop_loading();
        },
        error: function (error) {
            toast(error.responseText);
            toast("An error occurred");
            stop_loading();
        }

    });

}

function logIn() {

}