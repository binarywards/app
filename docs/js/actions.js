/* script to manipulate the interface events*/
var homePage= document.querySelector('#home');
var campaign_registration = document.querySelector('#campaign_registration');
var companyLogin = document.querySelector('#company_login');
var redeem = document.querySelector('#redeem_code');

function redeemPage() {
     if (redeem.classList.contains('d-none')){
         homePage.classList.add('d-none');
         companyLogin.classList.add('d-none');
         campaign_registration.classList.add('d-none');
         redeem.classList.remove('d-none');
     }
}

function loginPage(){
    if (companyLogin.classList.contains('d-none')){
        homePage.classList.add('d-none');
        redeem.classList.add('d-none');
        campaign_registration.classList.add('d-none');
        companyLogin.classList.remove('d-none');
    }
}