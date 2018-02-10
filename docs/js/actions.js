/* script to manipulate the interface events*/
let ajax = function (options) {
    function setDefaultVal(value, defaultValue){
        return (value === undefined) ? defaultValue : value;
    }
    let settings = {
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
        let data = new FormData();
        if (settings.data !== undefined) {
            Object.keys(settings.data).forEach(function (key) {
                data.append(key, settings.data[key]);
            });
        }

        function checkStatus(response) {
            if (response.status >= 200 && response.status < 300) {
                return response
            } else {
                let error = new Error(response.statusText);
                error.response = response;
                throw error;
            }
        }

        function parseData(response) {
            let type = response.headers.get('Content-Type');
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

let server = "https://binarywards.herokuapp.com/"

let toast = function (message) {
    Materialize.toast(message, 6000)
};

let redeem_code = function () {
    let phone = document.querySelector('#phoneNumber').value;
    let code = document.querySelector('#redemptionCode').value;
    ajax({
        url: server+"api/redeem",
        type: "POST",
        data: {
            redemptionCode: code,
            phoneNumber: phone
        },
        dataTye: "json",
        success: function (response) {
            // Process your data here e.g:
            let success = response['success']
            if (success) {
                let message = response['message'];
                toast(message)
            } else {
                let message = response.message;
                toast(message)
            }

        }
    });
};

function signUp() {

    let companyCode = document.querySelector('#companyCode').value;
    let companyName = document.querySelector('#companyName').value;
    let companyEmail = document.querySelector('#email').value;
    let companyPhone = document.querySelector('#companyPhone').value;
    let password = document.querySelector('#registerPassword').value;
    ajax({
        url: server+"api/company_add",
        type: "POST",
        data: {
            company_code: companyCode,
            name: companyName,
            email:companyEmail,
            phone_number:companyPhone,
            password:password
        },
        dataTye: "json",
        success: function (response) {
            let success = response['success'];
            if (success) {
                let message = response['message'];
                toast(message);
            } else {
                let message = response.message;
                toast(message);
            }
        }

    });

};