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

/* print() coz console.log() is way too long */
var print = function (data) {
    console.log(data);
};

var server = "https://binarywards.herokuapp.com/";

var toast = function (message) {
    Materialize.toast(message, 10000)
};


var start_loading = function () {
    if(document.querySelector("#preloader").classList.contains('d-none')){
        document.querySelector("#preloader").classList.remove('d-none');
    }
};

var stop_loading = function () {
    document.querySelector("#preloader").classList.add('d-none');
};

var update_title = function(title) {
    document.querySelector('title').innerText = "Bina Rywards - " + title;
};

var redeem_code = function () {
    start_loading();
    var phone = document.querySelector('#phoneNumber').value;
    var code = document.querySelector('#redemptionCode').value;
    ajax({
        url: "api/redeem_token",
        type: "POST",
        data: {
            redemptionCode: code,
            phoneNumber: phone
        },
        dataType: "json",
        success: function (response) {
            // Process your data here e.g:
            var success = response.success;
            var message = response.message;
            if (success) {
                toast(message);
                document.forms.redeem.reset();
            } else {
                toast(message);
            }
            stop_loading();
        },
        error: function (error) {
            var response = error.responseJSON;
            if(error.responseJSON === undefined){
                response = JSON.parse(error.responseText);
            }
            toast(response.message);
            stop_loading();
        }
    });
};

var open_campaign = function (compaign_code) {
    var camp_list_header = document.querySelector("#camp_list_header");
    var camp_list = document.querySelector("#camp_list");
    var camp_content_header = document.querySelector("#camp_content_header");
    var camp_content_new = document.querySelector("#camp_content_new");
    var camp_content = document.querySelector("#camp_content");

    if(camp_content_header.classList.contains("hide-on-small-and-down"))
        camp_content_header.classList.remove("hide-on-small-and-down");
    if(camp_content.classList.contains("hide-on-small-and-down"))
        camp_content.classList.remove("hide-on-small-and-down");
    if(camp_content.classList.contains("d-none"))
        camp_content.classList.remove("d-none");
    camp_content_new.classList.add("d-none");
    camp_list_header.classList.add("hide-on-small-and-down");
    camp_list.classList.add("hide-on-small-and-down");
};
var close_campaign = function () {
    var camp_list_header = document.querySelector("#camp_list_header");
    var camp_list = document.querySelector("#camp_list");
    var camp_content_header = document.querySelector("#camp_content_header");
    var camp_content_new = document.querySelector("#camp_content_new");
    var camp_content = document.querySelector("#camp_content");

    if(camp_list_header.classList.contains("hide-on-small-and-down"))
        camp_list_header.classList.remove("hide-on-small-and-down");
    if(camp_list.classList.contains("hide-on-small-and-down"))
        camp_list.classList.remove("hide-on-small-and-down");
    camp_content_new.classList.add("hide-on-small-and-down");
    camp_content_header.classList.add("hide-on-small-and-down");
    camp_content.classList.add("hide-on-small-and-down");
};
var new_campaign = function () {
    var camp_list_header = document.querySelector("#camp_list_header");
    var camp_list = document.querySelector("#camp_list");
    var camp_content_header = document.querySelector("#camp_content_header");
    var camp_content_new = document.querySelector("#camp_content_new");
    var camp_content = document.querySelector("#camp_content");

    if(camp_content_header.classList.contains("hide-on-small-and-down"))
        camp_content_header.classList.remove("hide-on-small-and-down");
    if(camp_content_new.classList.contains("hide-on-small-and-down"))
        camp_content_new.classList.remove("hide-on-small-and-down");
    if(camp_content_new.classList.contains("d-none"))
        camp_content_new.classList.remove("d-none");
    camp_content.classList.add("d-none");
    camp_list_header.classList.add("hide-on-small-and-down");
    camp_list.classList.add("hide-on-small-and-down");
};

var company_logged_in = function () {
    var company_code = window.sessionStorage.getItem('company_code');
    var auth_token = window.sessionStorage.getItem('auth_token');
    return company_code !== null && auth_token !== null;
};

var company_visuals = function() {
    var items = document.querySelectorAll('.company_logged');
    var logged = company_logged_in();
    var pos, item;
    if(logged) {
        for (pos in items) {
            item = items[pos];
            if (item.classList === undefined)
                continue;
            if (item.classList.contains('d-none')) {
                item.classList.remove('d-none');
            }
        }
    }else{
        for (pos in items) {
            item = items[pos];
            if (item.classList === undefined)
                continue;
            item.classList.add('d-none');
        }
    }
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
        dataType: "json",
        success: function (response) {
            var success = response.success;
            var message = response.message;
            if (success) {
                toast(message);
                document.forms.new_company.reset();
            } else {
                toast(message);
            }
            stop_loading();
        },
        error: function (error) {
            var response = error.responseJSON;
            if(error.responseJSON === undefined){
                response = JSON.parse(error.responseText);
            }
            toast(response.message);
            stop_loading();
        }

    });

}

function logIn() {
    var company_code = document.querySelector("#company_code").value;
    var password = document.querySelector("#password").value;
    start_loading();
    ajax({
        url: "api/company_login",
        type: "POST",
        data: {
            company_code: company_code,
            password: password
        },
        dataType: "json",
        success: function (response) {
            if (response.success) {
                document.forms.company_login.reset();
                toast("Login successful");
                window.sessionStorage.setItem("company_code", company_code);
                window.sessionStorage.setItem("auth_token", response.message);
                switch_page("#dashboard");
                company_visuals();
            } else {
                toast(response.message);
            }
            stop_loading();
        },
        error: function (error) {
            var response = error.responseJSON;
            if(error.responseJSON === undefined){
                response = JSON.parse(error.responseText);
            }
            toast(response.message);
            stop_loading();
        }

    })
}