$(document).ready(function () {
  $('#edit_blog').click(function () {
    let blog_title = $('#blog_title').text();
    let blog_paragraph = $('#blog_paragraph_body').text().trim();
    $('#blog_title').replaceWith(
      `<input value=${blog_title} id='blog_title' name='blog_title' style='flex-grow: 1;'></input>`
    );
    $('#blog_paragraph_body').replaceWith(
      `<textarea id='blog_paragraph_body' name='blog_paragraph_body' style="margin: auto 0;">${blog_paragraph}</textarea>`
    );
    $('#cancel_button')
      .css({ display: 'block' })
      .click(function () {
        $('#blog_title').replaceWith(
          `<div id="blog_title" name="blog_title" style='font-weight: 700; font-size: 1.25rem; line-height: 1.75rem; flex-grow: 1; text-align: right;'>${blog_title}</div>`
        );
        $('#blog_paragraph_body').replaceWith(
          `<div id="blog_paragraph_body" name="blog_paragraph_body" style='margin-top: auto; margin-bottom: auto; text-align: right;'>${blog_paragraph}</div>`
        );
        $('#cancel_button').css({ display: 'none' });
      });
  });
});
