$(document).ready(function () {
  console.log('im ready');
  let left_sidebar_state = true;
  $('#left-sidebar-btn').click(function () {
    if (left_sidebar_state) {
      left_sidebar_state = false;
      $('#left-sidebar').css({
        display: 'block',
        position: 'absolute',
        top: '60px',
        left: '60px',
        width: '15rem',
        'background-color': 'rgb(229 231 235)',
        height: '100vh',
        padding: '20px',
        'padding-left': '0px',
      });
    } else {
      left_sidebar_state = true;
      $('#left-sidebar').hide();
    }
  });
  $('#blog-post').click(function () {
    $('#new_blog').css('display', 'block');
    console.log('I have been clicked');
  });
  $('#edit_blog').click(function () {
    $('#cancel_edit_blog').css({ display: 'block' });
    console.log('edit');
  });
});
