function csrf_token() {
      return $('#csrf-token-element').data('csrf-token');
}

//post utility function
function post(url, callback, errortext) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);
  var form = new FormData()
  form.append("csrf_token", csrf_token());
  xhr.withCredentials=true;
  xhr.onerror=function() { 
      $('#toast-error .toast-text').text(errortext);
      $('#toast-error').toast('show')
  };
  xhr.onload = function() {
    if (xhr.status >= 200 && xhr.status < 300) {
      callback();
    } else {
      xhr.onerror();
    }
  };
  xhr.send(form);
}

function post_toast(url, callback=function(xhr){}) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);
  var form = new FormData()
  form.append("csrf_token", csrf_token());
  xhr.withCredentials=true;

  xhr.onload = function() {
    if (xhr.status==204){
      return
    }
    data=JSON.parse(xhr.response);
    $('.toast').toast('dispose')
    if (xhr.status >= 200 && xhr.status < 300) {
      $('#toast-success .toast-text').text(data['message']);
      $('#toast-success').toast('show');
    } else if (xhr.status >= 300 && xhr.status < 400 ) {
      window.location.href=data['redirect']
    } else {
      $('#toast-error .toast-text').text(data['error']);
      $('#toast-error').toast('show')
    }
    callback(xhr);
  };

  xhr.send(form);

  }

function post_reload(url) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);
  var form = new FormData()
  form.append("csrf_token", csrf_token());
  xhr.withCredentials=true;

  xhr.onload = function() {
    $('.toast').toast('dispose');
    if (xhr.status >= 200 && xhr.status < 300) {
      window.location.reload();
    } else if (xhr.status >= 300 && xhr.status < 400 ) {
      data=JSON.parse(xhr.response);
      window.location.href=data['redirect']
    } else {
      data=JSON.parse(xhr.response);
      $('#toast-error .toast-text').text(data['error']);
      $('#toast-error').toast('show')
    }
  };

  xhr.send(form);

  }

//delete utility function
function delete_toast(url) {
  var xhr = new XMLHttpRequest();
  xhr.open("DELETE", url, true);
  var form = new FormData()
  form.append("csrf_token", csrf_token());
  xhr.withCredentials=true;
  xhr.onerror=function() { 
      $('#toast-error .toast-text').text("Something went wrong. Please try again later.");
      $('#toast-error').toast('show')
  };
  xhr.onload = function() {
    data=JSON.parse(xhr.response);
    if (xhr.status >= 200 && xhr.status < 300) {
      $('#toast-success .toast-text').text(data['message']);
      $('#toast-success').toast('show')
    } else if (xhr.status >= 300 && xhr.status < 400 ) {
      window.location.href=data['redirect']
    } else {
      $('#toast-error .toast-text').text(data['error']);
      $('#toast-error').toast('show')
    }
  };
  xhr.send(form)
}

$(document).on('click', ".post-toast", function(){
  post_toast($(this).data('post-url'))
})

$(document).on('click', ".post-toast-reload", function(){
  post_reload($(this).data('post-url'))
})


//attach delete function to delete buttons
$(".delete-btn").click(function(){
  delete_toast(window.location.href)
})

//post form toast utility function
$('.toast-form-submit').click(function(){
  var form_id=$(this).data('form')
  var xhr = new XMLHttpRequest();
  url=$('#'+form_id).prop('action');
  xhr.open("POST", $('#'+form_id).prop('action'), true);
  var form = new FormData(document.querySelector('#'+form_id));
  xhr.withCredentials=true;
  xhr.onerror=function() { 
      $('#toast-error .toast-text').text("Something went wrong. Please try again later.");
      $('#toast-error').toast('show')
  };
  xhr.onload = function() {
    data=JSON.parse(xhr.response);
    if (xhr.status >= 200 && xhr.status < 300) {
      $('#toast-success .toast-text').text(data['message']);
      $('#toast-success').toast('show')
    } else if (xhr.status >= 300 && xhr.status < 400 ) {
      window.location.href=data['redirect']
    } else {
      $('#toast-error .toast-text').text(data['error']);
      $('#toast-error').toast('show')
    }
  };
  xhr.send(form);
})

//Dark mode toggle
$("#dark-mode-toggle").click(function(){
  post('/toggle_darkmode',
    callback=function(){
      var s = $('#mainstyle')
      if( s.prop('href').endsWith('light.css?v=0.0.1')){
        s.prop('href','/assets/style/dark.css?v=0.0.1')
      }
      else{
        s.prop('href','/assets/style/light.css?v=0.0.1')
      }
    })
})

//Initialize popovers
$('[data-toggle="popover"]').popover()