$(document).ready(function () {
  $('#edit_blog').click(function () {
    let blog_title = $('#blog_title').text();
    let blog_paragraph = $('#blog_paragraph_body').text();
    console.log(blog_paragraph);
    $('#blog_title').replaceWith(
      `<input value=${blog_title} name='blog_title'></input>`
    );
    $('#blog_paragraph_body').replaceWith(
      `<textarea name='blog_paragraph_body' style="margin:10px">${blog_paragraph.trim()}</textarea>`
    );
    $('#cancel_button')
      .css({ display: 'block' })
      .click(function () {
        $().replaceWith();
      });
  });
});
