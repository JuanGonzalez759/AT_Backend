document.addEventListener('DOMContentLoaded', function(){
  // clear all input values on page load
  const inputs = document.querySelectorAll('.input-field');
  inputs.forEach(function(input){
    input.value = '';
  });

  const emailInput = document.getElementById('email-input');
  const usernameInput = document.getElementById('username-input');
  const passwordInput = document.getElementById('password-input');
  const passwordConfirmInput = document.getElementById('password-confirm-input');
  const submitBtn = document.getElementById('submit-btn');

  const emailError = document.getElementById('email-error');
  const usernameError = document.getElementById('username-error');
  const passwordError = document.getElementById('password-error');
  const passwordConfirmError = document.getElementById('password-confirm-error');

  // validation state
  const validation = {
    email: false,
    username: false,
    password: false,
    passwordConfirm: false,
    passwordStrength: 0
  };

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

    validation.email = !error && email.length > 0;
    emailError.textContent = error;
    emailError.classList.toggle('hidden', !error);
    updateSubmitBtn();
  });

  // validate username in real time
  usernameInput.addEventListener('input', function(){
    const username = this.value.trim();
    let error = '';

    if(username) {
      if(!/^[a-zA-Z0-9_.-]+$/.test(username)) {
        error = 'Solo letras, números, guiones y puntos.';
      } else if(username.length < 3) {
        error = 'Mínimo 3 caracteres.';
      }
    }

    validation.username = !error && username.length > 0;
    usernameError.textContent = error;
    usernameError.classList.toggle('hidden', !error);
    updateSubmitBtn();
  });

  // password strength meter
  const strengthFill = document.querySelector('.password-strength-fill');
  const strengthText = document.querySelector('.password-strength-text');
  
  passwordInput.addEventListener('input', function(){
    const pwd = this.value;
    let strength = 0;
    let errors = [];
    
    // length check
    if(pwd.length >= 8) strength += 20;
    else errors.push('Mínimo 8 caracteres');
    if(pwd.length >= 12) strength += 5;
    
    // lowercase
    if(/[a-z]/.test(pwd)) strength += 20;
    else errors.push('Incluye minúsculas');
    
    // uppercase
    if(/[A-Z]/.test(pwd)) strength += 20;
    else errors.push('Incluye mayúsculas');
    
    // numbers
    if(/[0-9]/.test(pwd)) strength += 20;
    else errors.push('Incluye números');
    
    // special chars
    if(/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(pwd)) strength += 15;
    
    // cap at 100
    strength = Math.min(strength, 100);
    validation.passwordStrength = strength;
    validation.password = strength >= 80 && pwd.length > 0;
    
    // update bar
    strengthFill.style.width = strength + '%';
    
    // update text
    let text = 'Débil';
    if(strength >= 80) text = 'Fuerte';
    else if(strength >= 60) text = 'Medio';
    else if(strength >= 40) text = 'Regular';
    
    strengthText.textContent = text;

    // show error if not strong enough
    let error = '';
    if(pwd && strength < 80) {
      error = 'La contraseña debe ser Fuerte. ' + errors.join(', ');
    }

    passwordError.textContent = error;
    passwordError.classList.toggle('hidden', !error);

    // check confirmation match
    if(passwordConfirmInput.value) {
      validatePasswordConfirm();
    }

    updateSubmitBtn();
  });

  // validate password confirm
  function validatePasswordConfirm(){
    const pwd = passwordInput.value;
    const pwdConfirm = passwordConfirmInput.value;
    let error = '';

    if(pwdConfirm && pwd !== pwdConfirm) {
      error = 'Las contraseñas no coinciden.';
    }

    validation.passwordConfirm = !error && pwdConfirm.length > 0;
    passwordConfirmError.textContent = error;
    passwordConfirmError.classList.toggle('hidden', !error);
    updateSubmitBtn();
  }

  passwordConfirmInput.addEventListener('input', validatePasswordConfirm);

  // enable submit only if all validations pass
  function updateSubmitBtn(){
    const allValid = validation.email && validation.username && validation.password && validation.passwordConfirm;
    submitBtn.disabled = !allValid;
  }

  // toggle show/hide password for both password fields
  const toggleBtn1 = document.querySelector('.toggle-pwd-1');
  const toggleBtn2 = document.querySelector('.toggle-pwd-2');

  if(toggleBtn1){
    toggleBtn1.addEventListener('click', function(e){
      e.preventDefault();
      if(passwordInput.type === 'password'){
        passwordInput.type = 'text';
        toggleBtn1.textContent = 'ocultar';
      } else {
        passwordInput.type = 'password';
        toggleBtn1.textContent = 'mostrar';
      }
    });
  }

  if(toggleBtn2){
    toggleBtn2.addEventListener('click', function(e){
      e.preventDefault();
      if(passwordConfirmInput.type === 'password'){
        passwordConfirmInput.type = 'text';
        toggleBtn2.textContent = 'ocultar';
      } else {
        passwordConfirmInput.type = 'password';
        toggleBtn2.textContent = 'mostrar';
      }
    });
  }

  // click-to-activate animation for inputs that start readonly
  const allInputs = document.querySelectorAll('.input-field');
  allInputs.forEach(function(input){
    const wrap = input.closest('.input-wrap');
    
    input.addEventListener('click', function(e){
      if(!input.hasAttribute('readonly') || !wrap) return;
      e.preventDefault();
      wrap.classList.add('activating');
      
      // for password fields, temporarily change type to prevent Firefox autofill popup
      const isPassword = input.type === 'password';
      if(isPassword) {
        input.type = 'text';
      }
      
      setTimeout(function(){
        input.removeAttribute('readonly');
        if(isPassword) {
          input.type = 'password';
        }
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


