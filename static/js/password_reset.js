document.addEventListener('DOMContentLoaded', function(){
  // clear all input values on page load
  const inputs = document.querySelectorAll('.input-field');
  inputs.forEach(function(input){
    input.value = '';
  });

  const emailInput = document.getElementById('email-input');
  const submitBtn = document.getElementById('submit-btn');
  const emailError = document.getElementById('email-error');

  let emailValid = false;

  // validate email in real time
  emailInput.addEventListener('input', function(){
    const email = this.value.trim();
    let error = '';

    if(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if(!emailRegex.test(email)) {
        error = 'Email inválido.';
      }
    }

    emailValid = !error && email.length > 0;
    emailError.textContent = error;
    emailError.classList.toggle('hidden', !error);
    
    // enable submit only if email is valid
    submitBtn.disabled = !emailValid;
  });

  // click-to-activate animation for inputs that start readonly
  const allInputs = document.querySelectorAll('.input-field');
  allInputs.forEach(function(input){
    const wrap = input.closest('.input-wrap');
    
    input.addEventListener('click', function(e){
      if(!input.hasAttribute('readonly') || !wrap) return;
      e.preventDefault();
      wrap.classList.add('activating');
      setTimeout(function(){
        input.removeAttribute('readonly');
        wrap.classList.remove('activating');
        input.focus();
        try {
          const len = input.value ? input.value.length : 0;
          input.setSelectionRange(len, len);
        } catch (err) {}
      }, 220);
    });
  });
});
