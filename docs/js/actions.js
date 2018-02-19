/* Presentation mode */
var current_slide = 1;
var before = '#home';
function presentation_mode(e) {
    var ctrlPressed;
    var altPressed;

    var evt = (e == null ? event : e);

    altPressed = evt.altKey;
    ctrlPressed = evt.ctrlKey;
    var total = 5;
    // Toggle Presentation mode
    if ((altPressed && ctrlPressed && evt.keyCode === 80)) {
        if(document.querySelector("#presentation").classList.contains('d-none')){
            before = window.location.hash;
            switch_page("#presentation");
        }else{
            switch_page(before);
        }
    }

    // Next Slide
    if ((altPressed && ctrlPressed && evt.keyCode === 78)) {
        if(!document.querySelector("#presentation").classList.contains('d-none')) {
            hide_all_slides();
            var next = current_slide + 1;
            if (next > total) {
                next -= total;
            }
            current_slide = next;
            document.querySelector("#slide_"+next).classList.remove('d-none');
            Materialize.toast("Slide "+next+" of "+total, 2500);
        }
    }
    // Prevoius Slide
    if ((altPressed && ctrlPressed && evt.keyCode === 66)) {
        if(!document.querySelector("#presentation").classList.contains('d-none')) {
            hide_all_slides();
            var prev = current_slide - 1;
            if (prev < 1) {
                prev += total;
            }
            current_slide = prev;
            document.querySelector("#slide_"+prev).classList.remove('d-none');
            Materialize.toast("Slide "+prev+" of "+total, 2500);
        }
    }
    return true;
}

var hide_all_slides = function () {
    document.querySelector("#slide_1").classList.add('d-none');
    document.querySelector("#slide_2").classList.add('d-none');
    document.querySelector("#slide_3").classList.add('d-none');
    document.querySelector("#slide_4").classList.add('d-none');
    document.querySelector("#slide_5").classList.add('d-none');
};

document.onkeydown = presentation_mode;

/* script to manipulate the interface events*/
var ajax = function (options) {
    function setDefaultVal(value, defaultValue) {
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
    if (Window.fetch) {
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
    } else {
        $.ajax(settings);
    }
};

/* print() coz console.log() is way too long */
var print = function (data) {
    console.log(data);
};

var server = "https://binarywards.herokuapp.com/";

var toast = function (message) {
    Materialize.toast(message, 10000);
};


var start_loading = function () {
    if (document.querySelector("#preloader").classList.contains('d-none')) {
        document.querySelector("#preloader").classList.remove('d-none');
    }
};

var stop_loading = function () {
    document.querySelector("#preloader").classList.add('d-none');
};

var update_title = function (title) {
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
            if (error.responseJSON === undefined) {
                response = JSON.parse(error.responseText);
            }
            toast(response.message);
            stop_loading();
        }
    });
};

var current_campaign = null;

var open_campaign = function (campaign_code, silent){
    if (silent === undefined || silent === null)
        silent = false;
    if (!silent)
        start_loading();
    var token = window.sessionStorage.getItem('auth_token');
    var code = window.sessionStorage.getItem('company_code');

    var camp_list_header = document.querySelector("#camp_list_header");
    var camp_list = document.querySelector("#camp_list");
    var camp_content_header = document.querySelector("#camp_content_header");
    var camp_content_new = document.querySelector("#camp_content_new");
    var camp_content = document.querySelector("#camp_content");

    ajax({
        url: "api/company_campaign", dataType: "json",
        data: {
            campaign_code: campaign_code
        },
        headers: {
            token: token,
            company_code: code
        },
        success: function (response) {
            if (response.success) {
                current_campaign = campaign_code;
                fill_class('.campaign_name', response.message['name']);
                fill_class('.campaign_code', response.message['campaign_code']);
                fill_class('.campaign_desc', response.message['details']);
                fill_class('.campaign_spend', response.message['total_spent'].toFixed(3));
                fill_class('.campaign_call', response.message['callback']);
                fill_class('.campaign_message', response.message['message']);
                fill_class('.campaign_custom', response.message['custom_message']);
                fill_class('.campaign_reward', response.message['token_call']);

                if (camp_content_header.classList.contains("hide-on-small-and-down"))
                    camp_content_header.classList.remove("hide-on-small-and-down");
                if (camp_content.classList.contains("hide-on-small-and-down"))
                    camp_content.classList.remove("hide-on-small-and-down");
                if (camp_content.classList.contains("d-none"))
                    camp_content.classList.remove("d-none");
                camp_content_new.classList.add("d-none");
                camp_list_header.classList.add("hide-on-small-and-down");
                camp_list.classList.add("hide-on-small-and-down");
                stop_loading();
            } else {
                toast(response.message);
            }
            stop_loading();
        },
        error: function (error) {
            var response = error.responseJSON;
            if (response === undefined) {
                response = JSON.parse(error.responseText);
            }
            toast(response.message);
            stop_loading();
        }
    });
};

var close_campaign = function () {
    var camp_list_header = document.querySelector("#camp_list_header");
    var camp_list = document.querySelector("#camp_list");
    var camp_content_header = document.querySelector("#camp_content_header");
    var camp_content_new = document.querySelector("#camp_content_new");
    var camp_content = document.querySelector("#camp_content");

    if (camp_list_header.classList.contains("hide-on-small-and-down"))
        camp_list_header.classList.remove("hide-on-small-and-down");
    if (camp_list.classList.contains("hide-on-small-and-down"))
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

    if (camp_content_header.classList.contains("hide-on-small-and-down"))
        camp_content_header.classList.remove("hide-on-small-and-down");
    if (camp_content_new.classList.contains("hide-on-small-and-down"))
        camp_content_new.classList.remove("hide-on-small-and-down");
    if (camp_content_new.classList.contains("d-none"))
        camp_content_new.classList.remove("d-none");
    camp_content.classList.add("d-none");
    camp_list_header.classList.add("hide-on-small-and-down");
    camp_list.classList.add("hide-on-small-and-down");
};

var dummy_login = function () {
    window.sessionStorage.setItem("company_code", "BINA");
    window.sessionStorage.setItem("auth_token", "begufvdgg87438y4figf87873gfe87");
    window.sessionStorage.setItem("email", "me@billcountry.tech");
    window.sessionStorage.setItem("balance", 10);
    window.sessionStorage.setItem("name", "Bina Rywards");
    window.sessionStorage.setItem("phone", "0728824727");
};

var company_logged_in = function () {
    var company_code = window.sessionStorage.getItem('company_code');
    var auth_token = window.sessionStorage.getItem('auth_token');
    return company_code !== null && auth_token !== null;
};

var fill_class = function (_class, data) {
    var items = document.querySelectorAll(_class);
    for (var pos in items) {
        var item = items[pos];
        if (item.classList === undefined)
            continue;
        var tag = item.tagName.toLocaleLowerCase();
        if (tag === "input" || tag === "textarea") {
            item.value = data;
        } else {
            item.innerHTML = data;
        }
    }
};

var company_visuals = function () {
    var items = document.querySelectorAll('.company_logged');
    var logged = company_logged_in();
    var pos, item;
    if (logged) {
        for (pos in items) {
            item = items[pos];
            if (item.classList === undefined)
                continue;
            if (item.classList.contains('d-none')) {
                item.classList.remove('d-none');
            }
        }
        fetch_campaigns(true);
        fill_class('.company_name', window.sessionStorage.getItem("name"), false);
        fill_class('.company_code', window.sessionStorage.getItem("company_code"), false);
        fill_class('.company_balance', parseInt(window.sessionStorage.getItem("balance")).toFixed(3), false);
        fill_class('.company_email', window.sessionStorage.getItem("email"), false);
        fill_class('.company_phone', window.sessionStorage.getItem("phone"), false);
    } else {
        for (pos in items) {
            item = items[pos];
            if (item.classList === undefined)
                continue;
            item.classList.add('d-none');
        }
    }
};

var signUp = function () {
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
                document.querySelector("#company_code").value = companyCode;
                document.querySelector("#password").value = password;
                document.forms.new_company.reset();
                toast("You will be automatically logged in in 6 seconds");
                setTimeout("logIn()", 6000);
            } else {
                toast(message);
            }
            stop_loading();
        },
        error: function (error) {
            var response = error.responseJSON;
            if (error.responseJSON === undefined) {
                response = JSON.parse(error.responseText);
            }
            toast(response.message);
            stop_loading();
        }

    });

};

var logIn = function () {
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
                window.sessionStorage.setItem("auth_token", response.message.token);
                window.sessionStorage.setItem("email", response.message.email);
                window.sessionStorage.setItem("balance", response.message.balance);
                window.sessionStorage.setItem("name", response.message.name);
                window.sessionStorage.setItem("phone", response.message.phone);
                switch_page("#dashboard");
                company_visuals();
            } else {
                toast(response.message);
            }
            stop_loading();
        },
        error: function (error) {
            var response = error.responseJSON;
            if (error.responseJSON === undefined) {
                response = JSON.parse(error.responseText);
            }
            toast(response.message);
            stop_loading();
        }
    })
};

var update_company = function (key, value) {

};

var clear = function (element) {
    while (element.hasChildNodes()) {
        element.removeChild(element.lastChild);
    }
};

var fetch_campaigns = function (silent) {
    if (silent === undefined || silent === null)
        silent = false;
    if (!silent)
        start_loading();
    var token = window.sessionStorage.getItem('auth_token');
    var code = window.sessionStorage.getItem('company_code');
    ajax({
        url: "api/company_campaigns",
        dataType: "json",
        headers: {
            token: token,
            company_code: code
        },
        success: function (response) {
            if (response.success) {
                var campaigns = response.message;
                var camp_list = document.querySelector('#camp_list_actual');
                clear(camp_list);
                for (var i in campaigns) {
                    var campaign = campaigns[i];
                    var li = document.createElement('li');
                    var a = document.createElement('a');
                    li.classList.add('collection-item');
                    a.className = 'amber-text text-darken-4';
                    a.href = '#campaigns/' + campaign['campaign_code'];
                    a.setAttribute('onclick', "open_campaign('" + campaign['campaign_code'] + "')");
                    a.appendChild(new Text(campaign['campaign_code'] + " : " + campaign['name']));
                    a.title = campaign['details'];
                    li.appendChild(a);
                    camp_list.appendChild(li);
                }
                stop_loading();
            } else {
                toast(response.message);
            }
            stop_loading();
        },
        error: function (error) {
            var response = error.responseJSON;
            if (response === undefined) {
                response = JSON.parse(error.responseText);
            }
            toast(response.message);
            stop_loading();
        }
    });
};

var add_campaign = function () {
    start_loading();
    var campaignCode = document.querySelector("#campaignCode").value;
    var campaignName = document.querySelector("#campaignName").value;
    var description = document.querySelector("#description").value;
    var callBack = document.querySelector("#callBack").value;
    var rywardCalls = document.querySelector("#rywardCalls").value;
    // company_code, campaign_name, campaign_code, message, custom_message, details, callback, token_call, token
    ajax({
        url: "api/company_new_campaign",
        type: "POST",
        data: {
            company_code: window.sessionStorage.getItem('company_code'),
            token: window.sessionStorage.getItem('auth_token'),
            campaign_name: campaignName,
            campaign_code: campaignCode,
            message: '',
            custom_message: '',
            details: description,
            token_call: rywardCalls,
            callback: callBack
        },
        dataType: 'json',
        success: function (response) {
            if (response.success) {
                toast(response.message);
                document.forms.new_campaign.reset();
                toast("Refreshing campaigns...");
                fetch_campaigns();
            } else {
                toast(response.message);
            }
            stop_loading();
        },
        error: function (error) {
            var response = error.responseJSON;
            if (response === undefined) {
                response = JSON.parse(error.responseText);
            }
            toast(response.message);
            stop_loading();
        }
    });
};

var logout = function () {
    var token = window.sessionStorage.getItem('auth_token');
    var code = window.sessionStorage.getItem('company_code');
    window.sessionStorage.clear();
    company_visuals();
    switch_page('#home');
};

var add_token = function () {
    start_loading();
    var token = window.sessionStorage.getItem('auth_token');
    var code = window.sessionStorage.getItem('company_code');
    var rd_code = document.querySelector("#txt_new_token").value;
    var amount = document.querySelector("#txt_amount").value;
    // company_code, campaign_code, token, redeem_code, ryward_type, amount
    ajax({
        url: "api/company_new_campaign_token",
        type: "POST",
        data: {
            company_code: code,
            campaign_code: current_campaign,
            token: token,
            redeem_code: rd_code,
            ryward_type: 'Airtime',
            amount: amount
        },
        dataType: "json",
        success: function(response) {
            if (response.success) {
                toast(response.message);
                document.forms.new_token.reset();
            } else {
                toast(response.message);
            }
            stop_loading();
        },
        error: function (error) {
            var response = error.responseJSON;
            if (response === undefined) {
                response = JSON.parse(error.responseText);
            }
            toast(response.message);
            stop_loading();
        }
    });
};
