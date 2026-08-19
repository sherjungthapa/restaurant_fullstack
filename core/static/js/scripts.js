const input = document.querySelector("#phone");
const error_msg = document.getElementById("error_msg")
const ho = window.intlTelInput(input, {
    initialCountry:"np"})
window.intlTelInput(input, {
    initialCountry:'np',
    loadUtils: () => import("https://cdn.jsdelivr.net/npm/intl-tel-input@29.2.2/dist/js/utils.js"),
  });

  document.getElementById('contactForm').addEventListener('submit',function(e){
    if (ho.isValidNumber()){
        input.value=ho.getNumber(); //full country code
        error_msg.style.display='none';

    }
    else{
        e.preventDefault();
        error_msg.style.display='inline';
    }
  })
