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
  });
  $('#edit_blog').click(function () {
    let blog_title = $('#blog_title').text();
    let blog_paragraph = $('#blog_paragraph_body').text();
    $('#blog_title').replaceWith(
      `<input value=${blog_title} name='blog_title'></input>`
    );
    $('#blog_paragraph_body').replaceWith(
      `<input value=${blog_paragraph} name='blog_paragraph_body'></input>`
    );
    $('#cancel_button').css({ display: 'block' });
  });
});
