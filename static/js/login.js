document.addEventListener('DOMContentLoaded', function(){
  // clear all input values on page load
  const inputs = document.querySelectorAll('.input-field');
  inputs.forEach(function(input){
    input.value = '';
  });

  const toggle = document.getElementById('toggle');
  const pwd = document.getElementById('password');

  // toggle show/hide password
  if(toggle && pwd){
    toggle.addEventListener('click', function(){
      if(pwd.type === 'password'){
        pwd.type = 'text';
        toggle.textContent = 'ocultar';
      } else {
        pwd.type = 'password';
        toggle.textContent = 'mostrar';
      }
    });
  }

  // click-to-activate animation for inputs that start readonly; animate only the underline
  const allInputs = document.querySelectorAll('.input-field');
  allInputs.forEach(function(input){
    const wrap = input.closest('.input-wrap');
    
    // activate on click
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
