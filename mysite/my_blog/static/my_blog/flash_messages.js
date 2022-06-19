$(document).ready(function() {
  let flash_messages = $("#flash_messages").children();
  let flash_messages_container = $("#flash_messages_container").children();
  if (flash_messages_container !== 0){
    setTimeout(function() {
      $("#messages").slideUp()  
    }, 2000)
  };
});