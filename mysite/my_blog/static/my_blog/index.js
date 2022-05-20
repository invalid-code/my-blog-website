$(document).ready(function () {
  console.log('im ready');
  $('#blog-post').click(function () {
    $('#new_blog').css('display', 'block');
    console.log('I have been clicked');
  });
  $('#edit_blog').click(function () {
    console.log('edit');
  });
});
